import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Agent } from "../types";

export interface BucketData {
  id: string;
  // Basic Details
  name: string;
  description: string;
  llmModel: string;

  // Goals & Criteria
  goals: string;
  objectives: string;
  numberOfExchanges: number;

  // Agent Configuration
  selectedAgents: Agent[];
  members: string[];
  accessLevel: string;
  createdAt: Date;
  conversationStarted: boolean;
}

interface BucketState {
  buckets: BucketData[];
  currentBucket: Partial<BucketData>;
  updateBucketField: <K extends keyof BucketData>(
    field: K,
    value: BucketData[K]
  ) => void;
  resetBucket: () => void;
  addBucket: (bucket: BucketData) => void;
  removeBucket: (id: string) => void;
  updateBucketFieldById: (
    id: string,
    field: keyof BucketData,
    value: BucketData[keyof BucketData]
  ) => void;
}

const initialBucketState: Partial<BucketData> = {
  id: "",
  name: "InfiniteRegen Backroom",
  description: "InfiniteRegen chat",
  llmModel: "",
  goals: "",
  objectives: "",
  numberOfExchanges: 4,
  selectedAgents: [],
  members: [],
  accessLevel: "",
  conversationStarted: false,
};

export const useBucketStore = create<BucketState>()(
  persist(
    (set) => ({
      buckets: [],
      currentBucket: initialBucketState,
      updateBucketField: (field, value) =>
        set((state) => ({
          currentBucket: {
            ...state.currentBucket,
            [field]: value,
          },
        })),
      resetBucket: () =>
        set({
          currentBucket: initialBucketState,
        }),
      addBucket: (bucket) =>
        set((state) => ({
          buckets: [...state.buckets, bucket],
        })),
      updateBucketFieldById: (id, field, value) =>
        set((state) => ({
          buckets: state.buckets.map((bucket) =>
            bucket.id === id ? { ...bucket, [field]: value } : bucket
          ),
        })),
      removeBucket: (id) =>
        set((state) => ({
          buckets: state.buckets.filter((bucket) => bucket.id !== id),
        })),
    }),
    {
      name: "bucket-storage",
      version: 0.3,
    }
  )
);
