"use client";

import ChatLayout from "@/components/chat/ChatLayout";
import { MarkdownComponents } from "@/components/Markdown";
import { Button } from "@/components/ui/button";
import api from "@/lib/axios";
import { useBucketStore } from "@/lib/store/bucket-store";
import { useMutation, useQuery } from "@tanstack/react-query";
import { saveAs } from "file-saver";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

interface ChatMessage {
  role: string;
  content: string;
  exchangeNumber: number;
}

export default function BucketDetail() {
  const params = useParams();
  const { buckets, updateBucketFieldById } = useBucketStore();
  const [isStreaming, setIsStreaming] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streamingMessages, setStreamingMessages] = useState<ChatMessage[]>([]);
  const [typingAgents, setTypingAgents] = useState<Set<string>>(new Set());
  const [currentExchange, setCurrentExchange] = useState<number>(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentBucket = buckets.find((b) => b.id === params.id);

  const { data: chatData, isLoading } = useQuery({
    queryKey: ["chat", params.id],
    queryFn: async () => {
      const response = await api.get(
        `/conversation/${params.id}/multi-agent-chat`
      );
      return response.data as { messages: ChatMessage[] };
    },
    enabled: !!currentBucket?.conversationStarted,
    refetchOnWindowFocus: false,
    staleTime: 30000,
  });

  const generateReportMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post(
        `/conversation/${params.id}/generate-document-with-multi-agent-chat`,
        {},
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      });

      saveAs(
        blob,
        `${currentBucket?.name || "report"}${
          new Date().toISOString().split("T")[0]
        }.docx`
      );

      return response.data;
    },
  });

  useEffect(() => {
    if (chatData?.messages) {
      setMessages(chatData.messages);
    }
  }, [chatData]);

  const updateStreamingMessage = (
    role: string,
    content: string,
    exchangeNumber: number
  ) => {
    setStreamingMessages((prev) => {
      const existingMessageIndex = prev.findIndex(
        (msg) => msg.role === role && msg.exchangeNumber === exchangeNumber
      );

      if (existingMessageIndex >= 0) {
        const updatedMessages = [...prev];
        updatedMessages[existingMessageIndex] = {
          role,
          content,
          exchangeNumber,
        };
        return updatedMessages;
      } else {
        return [...prev, { role, content, exchangeNumber }];
      }
    });
  };

  const finalizeExchange = (exchangeNumber: number) => {
    const exchangeMessages = streamingMessages.filter(
      (msg) => msg.exchangeNumber === exchangeNumber
    );

    setMessages((prev) => [...prev, ...exchangeMessages]);
    setStreamingMessages((prev) =>
      prev.filter((msg) => msg.exchangeNumber !== exchangeNumber)
    );
  };

  const startConversation = async () => {
    if (!currentBucket) return;

    setIsStreaming(true);
    setStreamingMessages([]);
    setTypingAgents(new Set());
    setMessages([]);
    setCurrentExchange(0);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/conversation/${
          currentBucket.id
        }/chat-between-n-agents?number_of_exchanges=${
          currentBucket.numberOfExchanges || 4
        }&goal=${encodeURIComponent(
          `${currentBucket.goals} ${currentBucket.objectives}`
        )}&conversation_id=${currentBucket.id}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(
            currentBucket?.selectedAgents.map((agent) => agent.id)
          ),
        }
      );

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let currentMessages: { [key: string]: string } = {};

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;

        if (buffer.includes("---")) {
          const parts = buffer.split("---");
          buffer = parts.pop() || "";

          for (const part of parts) {
            const trimmedMessage = part.trim();
            if (!trimmedMessage) continue;

            const agentMatch = trimmedMessage.match(
              /^Agent\s+(\w+)\s+\(Exchange\s+(\d+)\):/
            );
            if (agentMatch) {
              const [fullMatch, agentRole, exchangeNumber] = agentMatch;
              const exchangeNum = parseInt(exchangeNumber, 10);
              const content = trimmedMessage.replace(agentMatch[0], "").trim();

              if (exchangeNum !== currentExchange) {
                finalizeExchange(currentExchange);
                setCurrentExchange(exchangeNum);
                currentMessages = {};
              }

              currentMessages[agentRole] = content;
              setTypingAgents((prev) => new Set(prev).add(agentRole));

              updateStreamingMessage(
                agentRole,
                currentMessages[agentRole],
                exchangeNum
              );
            }
          }
        } else if (buffer.trim()) {
          const agentRegex = /Agent\s+(\w+)\s+\(Exchange\s+(\d+)\):/g;
          let lastAgentMatch = null;
          let match;

          while ((match = agentRegex.exec(buffer)) !== null) {
            lastAgentMatch = match;
          }

          if (lastAgentMatch) {
            const [fullMatch, agentRole, exchangeNumber] = lastAgentMatch;
            const exchangeNum = parseInt(exchangeNumber, 10);

            const content = buffer
              .slice(buffer.lastIndexOf(fullMatch) + fullMatch.length)
              .trim();

            currentMessages[agentRole] = content;
            setTypingAgents((prev) => new Set(prev).add(agentRole));

            updateStreamingMessage(agentRole, content, exchangeNum);

            await new Promise((resolve) => setTimeout(resolve, 50));
          }
        }
      }
    } catch (error) {
      console.error("Streaming error:", error);
    } finally {
      setIsStreaming(false);
      setStreamingMessages([]);
      setTypingAgents(new Set());
      updateBucketFieldById(currentBucket.id, "conversationStarted", true);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessages, isStreaming]);

  const renderMessage = (message: ChatMessage, isStreaming = false) => (
    <div
      className={`p-4 rounded shadow-sm max-w-[70%] transition-all duration-200 ${
        message.role === currentBucket?.selectedAgents[0].name
          ? "ml-auto bg-primary text-white"
          : "bg-white text-black"
      } ${isStreaming ? "animate-fade-in" : ""}`}
    >
      <div className="font-semibold mb-1 font-manrope">{message.role}</div>
      <div
        className={`markdown-content whitespace-pre-wrap prose dark:prose-invert max-w-none ${
          isStreaming ? "prose-sm" : ""
        }`}
      >
        <ReactMarkdown components={MarkdownComponents}>
          {message.content.replace(/```/g, "\n```\n")}
        </ReactMarkdown>
      </div>
    </div>
  );

  return (
    <ChatLayout type="bucket">
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between p-4 border-b bg-white">
          <div>
            <h1 className="text-xl font-semibold">{currentBucket?.name}</h1>
            <p className="text-sm text-muted-light">
              {currentBucket?.description}
            </p>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={() => generateReportMutation.mutate()}
              disabled={
                generateReportMutation.isPending ||
                !currentBucket?.conversationStarted
              }
              variant="outline"
            >
              {generateReportMutation.isPending
                ? "Generating..."
                : "Generate Report"}
            </Button>
            {!currentBucket?.conversationStarted ? (
              <Button
                onClick={startConversation}
                disabled={isStreaming || !currentBucket?.selectedAgents?.length}
              >
                {isStreaming
                  ? "Conversation in Progress..."
                  : "Start Conversation"}
              </Button>
            ) : null}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto space-y-4 p-4">
          {messages.map((message, index) => renderMessage(message))}
          {streamingMessages.map((message, index) =>
            renderMessage(message, true)
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </ChatLayout>
  );
}
