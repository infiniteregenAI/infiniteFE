import { useQuery } from "@tanstack/react-query";
import api from "../axios";

export function useAgents() {
  return useQuery({
    queryKey: ["agents"],
    queryFn: async () => {
      const response = await api.get("/api/agents");
      return response.data;
    },
  });
}
