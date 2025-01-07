"use client";

import AgentSelection from "@/components/create-bucket/agent-selection";
import ProgressSteps from "@/components/create-profile/progress-steps";
import { Button } from "@/components/ui/button";
import {
  FormActions,
  FormDivider,
  FormField,
} from "@/components/ui/form-field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { Textarea } from "@/components/ui/textarea";
import { useAgents } from "@/lib/hooks/use-agents";
import { BucketData, useBucketStore } from "@/lib/store/bucket-store";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useState } from "react";

const steps = [
  {
    id: 1,
    title: "Basic Backroom Details",
    description: "Define backroom details",
  },
  {
    id: 2,
    title: "Set Goals & Criteria",
    description: "Customize behavior and tone.",
  },
  {
    id: 3,
    title: "Invite & Configure Agents",
    description: "Select primary and secondary agents.",
  },
];

export default function CreateBucketForm() {
  const router = useRouter();
  const { currentBucket, updateBucketField, resetBucket, addBucket } =
    useBucketStore();
  const { data: agents, isLoading, error } = useAgents();
  const [currentStep, setCurrentStep] = useState(1);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const validateStep = (step: number) => {
    const newErrors: { [key: string]: string } = {};

    if (step === 1) {
      if (!currentBucket.name?.trim()) {
        newErrors.name = "Backroom name is required";
      }
      if (!currentBucket.description?.trim()) {
        newErrors.description = "Backroom description is required";
      }
      if (!currentBucket.llmModel) {
        newErrors.llmModel = "Please select an LLM model";
      }
    }

    if (step === 2) {
      if (!currentBucket.goals?.trim()) {
        newErrors.goals = "Goals are required";
      }
      if (!currentBucket.objectives?.trim()) {
        newErrors.objectives = "Objectives are required";
      }
      if (
        !currentBucket.numberOfExchanges ||
        currentBucket.numberOfExchanges < 1
      ) {
        newErrors.numberOfExchanges = "Number of exchanges must be at least 1";
      }
    }

    if (step === 3) {
      if (
        !currentBucket.selectedAgents ||
        currentBucket.selectedAgents.length < 2
      ) {
        newErrors.selectedAgents = "Please select at least 2 agents";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(prev + 1, steps.length));
    }
  };

  const handleBack = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 1));
  };

  const handleCreate = () => {
    if (!validateStep(currentStep)) {
      return;
    }

    const newBucket: BucketData = {
      ...(currentBucket as BucketData),
      id: crypto.randomUUID(),
      createdAt: new Date(),
      conversationStarted: false,
    };

    addBucket(newBucket);
    resetBucket();
    router.push(`/dashboard/bucket/${newBucket.id}`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container"
    >
      <div className="bg-white rounded-xl p-6 border">
        <div>
          <div className="mb-8">
            <h1 className="text-2xl font-semibold mb-1">Create Backroom</h1>
            <p className="text-sm text-muted-light">
              Create a new backroom for your project
            </p>
          </div>

          <div>
            <div className="mb-12">
              <ProgressSteps steps={steps} currentStep={currentStep} />
            </div>

            <div>
              {currentStep === 1 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex flex-col gap-6"
                >
                  <FormField
                    label="Backroom Name"
                    description="Choose a name that represents the purpose of this backroom."
                  >
                    <Input
                      placeholder="Enter backroom name"
                      value={currentBucket.name}
                      onChange={(e) => {
                        updateBucketField("name", e.target.value);
                        setErrors((prev) => ({ ...prev, name: "" }));
                      }}
                      disabled
                    />
                    {errors.name && (
                      <p className="text-sm text-red-500 mt-1">{errors.name}</p>
                    )}
                  </FormField>

                  <FormDivider />

                  <FormField
                    label="Backroom Description"
                    description="Write description about your backroom"
                  >
                    <Textarea
                      placeholder="Enter backroom description"
                      value={currentBucket.description}
                      onChange={(e) => {
                        updateBucketField("description", e.target.value);
                        setErrors((prev) => ({ ...prev, description: "" }));
                      }}
                      disabled
                    />
                    {errors.description && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors.description}
                      </p>
                    )}
                  </FormField>

                  <FormDivider />

                  <FormField
                    label="Backroom LLM"
                    description="Choose the language model for this backroom"
                  >
                    <Select
                      value={currentBucket.llmModel}
                      onValueChange={(value) => {
                        updateBucketField("llmModel", value);
                        setErrors((prev) => ({ ...prev, llmModel: "" }));
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select LLM" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gpt4">GPT-4 Turbo</SelectItem>
                        <SelectItem value="gpt35">GPT-3.5 Turbo</SelectItem>
                        <SelectItem value="claude2">Claude 2</SelectItem>
                        <SelectItem value="claude3">Claude 3</SelectItem>
                      </SelectContent>
                    </Select>
                    {errors.llmModel && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors.llmModel}
                      </p>
                    )}
                  </FormField>

                  <FormActions>
                    <Button variant="outline" onClick={resetBucket}>
                      Cancel
                    </Button>
                    <Button onClick={handleNext}>Continue</Button>
                  </FormActions>
                </motion.div>
              )}

              {currentStep === 2 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex flex-col gap-6"
                >
                  <FormField
                    label="Goals"
                    description="Define the main goals for this backroom"
                  >
                    <Textarea
                      placeholder="Enter backroom goals"
                      value={currentBucket.goals}
                      onChange={(e) => {
                        updateBucketField("goals", e.target.value);
                        setErrors((prev) => ({ ...prev, goals: "" }));
                      }}
                    />
                    {errors.goals && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors.goals}
                      </p>
                    )}
                  </FormField>

                  <FormDivider />

                  <FormField
                    label="Objectives"
                    description="List specific objectives to achieve"
                  >
                    <Textarea
                      placeholder="Enter objectives"
                      value={currentBucket.objectives}
                      onChange={(e) => {
                        updateBucketField("objectives", e.target.value);
                        setErrors((prev) => ({ ...prev, objectives: "" }));
                      }}
                    />
                    {errors.objectives && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors.objectives}
                      </p>
                    )}
                  </FormField>

                  <FormDivider />

                  <FormField
                    label="Number of Exchanges"
                    description="Set how many rounds of conversation the agents will have"
                  >
                    <Input
                      type="number"
                      min={1}
                      max={10}
                      placeholder="Enter number of exchanges"
                      value={currentBucket.numberOfExchanges}
                      onChange={(e) => {
                        updateBucketField(
                          "numberOfExchanges",
                          parseInt(e.target.value) || 4
                        );
                        setErrors((prev) => ({
                          ...prev,
                          numberOfExchanges: "",
                        }));
                      }}
                    />
                    {errors.numberOfExchanges && (
                      <p className="text-sm text-red-500 mt-1">
                        {errors.numberOfExchanges}
                      </p>
                    )}
                  </FormField>

                  <FormActions>
                    <Button variant="outline" onClick={handleBack}>
                      Back
                    </Button>
                    <Button onClick={handleNext}>Continue</Button>
                  </FormActions>
                </motion.div>
              )}

              {currentStep === 3 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex flex-col gap-6"
                >
                  <FormField
                    label="Select Agents"
                    description="Choose primary and secondary agents (2 required)"
                  >
                    {isLoading ? (
                      <div className="grid grid-cols-1 md:grid-cols-2  gap-4">
                        {new Array(6).fill(null).map((_, index) => (
                          <Skeleton key={index} className="h-20 w-full" />
                        ))}
                      </div>
                    ) : error ? (
                      <div className="text-red-500 p-4 text-center">
                        Failed to load agents
                      </div>
                    ) : (
                      <AgentSelection
                        agents={agents}
                        selectedAgents={currentBucket.selectedAgents || []}
                        onSelect={(selectedAgents) =>
                          updateBucketField("selectedAgents", selectedAgents)
                        }
                        maxAgents={6}
                      />
                    )}
                  </FormField>

                  <FormDivider />

                  <FormActions>
                    <Button variant="outline" onClick={handleBack}>
                      Back
                    </Button>
                    <Button
                      onClick={handleCreate}
                      disabled={
                        !currentBucket.selectedAgents?.length ||
                        !(currentBucket.selectedAgents.length >= 2)
                      }
                    >
                      Create Bucket
                    </Button>
                  </FormActions>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
