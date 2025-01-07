"use client";

import { Message, useChatStore } from "@/lib/store/chat-store";
import { useMutation } from "@tanstack/react-query";
import { Loader2 } from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { MarkdownComponents } from "../Markdown";

interface ChatRequestMessage {
  agent_id: string;
  content: string;
}

interface ChatRequestBody {
  messages: ChatRequestMessage[];
  goal: string;
}

interface ChatInterfaceProps {
  agentId: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ agentId }) => {
  const { addMessage, getMessages } = useChatStore();
  const messages = getMessages(agentId);
  const [inputMessage, setInputMessage] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [streamedContent, setStreamedContent] = useState("");
  const [isMounted, setIsMounted] = useState(false);
  const messageContainerRef = useRef<HTMLDivElement>(null);
  const streamTimeoutRef = useRef<NodeJS.Timeout>();
  const shouldScrollRef = useRef(true);
  const lastScrollHeightRef = useRef(0);
  const previousAgentIdRef = useRef(agentId);
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const scrollToBottom = (force = false) => {
    if (!messageContainerRef.current) return;

    requestAnimationFrame(() => {
      const container = messageContainerRef.current;
      if (!container) return;

      const newScrollHeight = container.scrollHeight;

      if (newScrollHeight === lastScrollHeightRef.current && !force) {
        return;
      }

      if (force || shouldScrollRef.current) {
        container.scrollTop = newScrollHeight;
      }

      lastScrollHeightRef.current = newScrollHeight;
    });
  };

  useEffect(() => {
    const container = messageContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const threshold = 100;
      const position =
        container.scrollHeight - container.scrollTop - container.clientHeight;
      shouldScrollRef.current = position < threshold;
    };

    container.addEventListener("scroll", handleScroll, { passive: true });
    return () => container.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    if (isMounted && messages.length > 0) {
      const isAgentChange = previousAgentIdRef.current !== agentId;
      previousAgentIdRef.current = agentId;

      scrollToBottom(true);

      if (isAgentChange) {
        shouldScrollRef.current = true;
      }
    }
  }, [agentId, messages, isMounted]);

  useEffect(() => {
    const container = messageContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const threshold = 100;
      const position =
        container.scrollHeight - container.scrollTop - container.clientHeight;
      shouldScrollRef.current = position < threshold;
    };

    container.addEventListener("scroll", handleScroll, { passive: true });
    return () => container.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    if (streamedContent && shouldScrollRef.current) {
      scrollToBottom();
    }
  }, [streamedContent]);

  useEffect(() => {
    return () => {
      if (streamTimeoutRef.current) {
        clearTimeout(streamTimeoutRef.current);
      }
    };
  }, []);

  const handleStream = async (response: Response) => {
    if (!response.body) return;

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = "";
    let isHeaderSection = true;
    let buffer = "";

    setIsLoading(false);
    setIsStreaming(true);

    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        let words = buffer.split(/(\s+)/);

        if (!buffer.match(/\s+$/)) {
          buffer = words.pop() || "";
          words = words.filter((w) => w.length > 0);
        } else {
          buffer = "";
        }

        for (const word of words) {
          if (isHeaderSection) {
            if (word.trim() === "") {
              isHeaderSection = false;
            } else if (word.includes(": ")) {
              continue;
            }
          } else {
            const cleanedWord = word
              .replace(/^data: /, "")
              .replace(/\[DONE\]/, "");

            if (cleanedWord) {
              fullContent += cleanedWord;
              setStreamedContent(fullContent);
              scrollToBottom();
            }
          }
        }
      }

      if (buffer.trim()) {
        const cleanedContent = buffer
          .trim()
          .replace(/^data: /, "")
          .replace(/\[DONE\]/, "");

        if (cleanedContent) {
          fullContent += cleanedContent;
          setStreamedContent(fullContent);
        }
      }
    } catch (error) {
      console.error("Error reading stream:", error);
    } finally {
      setIsStreaming(false);
      if (fullContent) {
        const assistantMessage: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: fullContent,
          createdAt: new Date().toISOString(),
        };
        addMessage(agentId, assistantMessage);
      }
      setStreamedContent("");
    }
  };

  const sendMessageMutation = useMutation<void, Error, string>({
    mutationFn: async (messageContent) => {
      setIsLoading(true);
      shouldScrollRef.current = true;

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: messageContent,
        createdAt: new Date().toISOString(),
      };

      addMessage(agentId, userMessage);
      scrollToBottom(true);

      const lastMessages = messages.slice(-2);
      const requestMessages = [
        ...lastMessages.map((msg) => ({
          agent_id: agentId,
          content: msg.content,
        })),
        { agent_id: agentId, content: messageContent },
      ];

      const requestBody: ChatRequestBody = {
        messages: requestMessages,
        goal: "chat",
      };

      try {
        const response = await fetch(`/conversation/${agentId}/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/plain, text/event-stream",
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        console.log("response", response);
        await handleStream(response);
      } catch (error) {
        setIsLoading(false);
        console.error("Error:", error);
        throw error;
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim() && !isStreaming && !isLoading) {
      sendMessageMutation.mutate(inputMessage.trim());
      setInputMessage("");
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-gray-50">
      {isMounted && (
        <div
          ref={messageContainerRef}
          className="flex-1 overflow-y-auto p-4 space-y-4"
        >
          {messages?.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`flex flex-col max-w-[70%] gap-2 ${
                  msg.role === "user" ? "items-end" : "items-start"
                }`}
              >
                <div
                  className={`rounded px-4 py-2 shadow ${
                    msg.role === "user"
                      ? "bg-primary text-white"
                      : "bg-white text-gray-800"
                  }`}
                >
                  <p className="whitespace-pre-wrap leading-relaxed">
                    <ReactMarkdown components={MarkdownComponents}>
                      {msg.content}
                    </ReactMarkdown>
                  </p>
                </div>
                <div className="text-xs text-muted-light">
                  {new Date(msg.createdAt).toLocaleString("en-US", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            </div>
          ))}

          {(isStreaming || isLoading) && (
            <div className="flex justify-start">
              <div className="max-w-[70%] rounded p-4 shadow bg-white text-gray-800">
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Loading...</span>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap leading-relaxed">
                    {streamedContent}
                    <span className="inline-flex ml-1">
                      <span className="w-1 h-1 bg-gray-400 rounded-full animate-bounce delay-0" />
                      <span className="w-1 h-1 bg-gray-400 rounded-full animate-bounce delay-150 mx-1" />
                      <span className="w-1 h-1 bg-gray-400 rounded-full animate-bounce delay-300" />
                    </span>
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} className="p-4 bg-white border-t shadow-sm">
        <div className="flex space-x-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border rounded px-6 py-3 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            disabled={isStreaming || isLoading}
          />
          <button
            type="submit"
            disabled={isStreaming || isLoading || !inputMessage.trim()}
            className="bg-primary flex items-center justify-center text-white rounded size-12 hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <svg
              width="15"
              height="15"
              viewBox="0 0 15 12"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M0.340041 12L14.3334 6L0.340041 0L0.333374 4.66667L10.3334 6L0.333374 7.33333L0.340041 12Z"
                fill="#FBFAFC"
              />
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
