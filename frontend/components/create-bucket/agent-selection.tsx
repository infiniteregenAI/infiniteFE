import { Card } from "@/components/ui/card";
import { Agent } from "@/lib/types";
import { motion } from "framer-motion";
import { Check } from "lucide-react";

interface AgentSelectionProps {
  agents: Agent[];
  selectedAgents: Agent[];
  onSelect: (agents: Agent[]) => void;
  maxAgents: number;
}

export default function AgentSelection({
  agents,
  selectedAgents,
  onSelect,
  maxAgents,
}: AgentSelectionProps) {
  const handleAgentClick = (agent: Agent) => {
    if (selectedAgents.find((a) => a.id === agent.id)) {
      onSelect(selectedAgents.filter((a) => a.id !== agent.id));
    } else if (selectedAgents.length < maxAgents) {
      onSelect([...selectedAgents, agent]);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2  gap-4">
      {agents?.map((agent) => {
        const isSelected = selectedAgents.some((a) => a.id === agent.id);
        return (
          <motion.div
            key={agent.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Card
              className={`p-4 cursor-pointer h-full relative ${
                isSelected
                  ? "border-primary border-2"
                  : selectedAgents.length >= maxAgents
                  ? "border opacity-50 cursor-not-allowed"
                  : "border hover:border-primary/50"
              }`}
              onClick={() => handleAgentClick(agent)}
            >
              {isSelected && (
                <div className="absolute top-2 right-2">
                  <Check className="w-5 h-5 text-primary" />
                </div>
              )}
              <div className="flex items-start gap-3">
                <div className="text-2xl size-10 overflow-hidden flex items-center justify-center bg-gray-100 rounded-full">
                  {agent.avatar}
                </div>
                <div>
                  <h3 className="font-semibold mb-1">{agent.name}</h3>
                  <p className="text-sm text-muted-foreground mb-2">
                    {agent.role}
                  </p>
                </div>
              </div>
            </Card>
          </motion.div>
        );
      })}
    </div>
  );
}
