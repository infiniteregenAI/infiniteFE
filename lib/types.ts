export type Avatar = "💡";

export interface Agent {
  avatar: string;
  document_count: number;
  documents: null | string[];
  expertise: string[];
  has_knowledge_base: boolean;
  id: string;
  name: string;
  personality: string;
  role: string;
}
