import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

interface ChatState {
  chats: Record<string, Message[]>;
  addMessage: (agentId: string, message: Message) => void;
  getMessages: (agentId: string) => Message[];
  clearChat: (agentId: string) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      chats: {},
      addMessage: (agentId: string, message: Message) =>
        set((state) => ({
          chats: {
            ...state.chats,
            [agentId]: [...(state.chats[agentId] || []), message],
          },
        })),
      getMessages: (agentId: string) => get().chats[agentId] || [],
      clearChat: (agentId: string) =>
        set((state) => ({
          chats: {
            ...state.chats,
            [agentId]: [],
          },
        })),
    }),
    {
      name: "chat-storage",
      version: 0.2,
    }
  )
);
