"use client";
import ChatInterface from "@/components/chat/ChatInterface";
import ChatLayout from "@/components/chat/ChatLayout";
import api from "@/lib/axios";
import { Agent } from "@/lib/types";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";

const Page = () => {
  const { id } = useParams();
  const { data: agent } = useQuery({
    queryKey: ["agent", id],
    queryFn: async () => {
      const response = await api.get<Agent>(`/api/agents/${id}`);
      return response.data;
    },
  });

  console.log(agent);
  return (
    <ChatLayout>
      <div className="flex flex-col">
        <div className="bg-white  px-10 py-4 border-b">
          <h1 className="  text-lg   font-semibold">{agent?.name}</h1>
        </div>
        <ChatInterface agentId={id as string} />
      </div>
    </ChatLayout>
  );
};

export default Page;
