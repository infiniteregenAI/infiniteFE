"use client";

import { Check } from "lucide-react";

interface Step {
  id: number;
  title: string;
  description: string;
}

interface ProgressStepsProps {
  steps: Step[];
  currentStep: number;
}

export default function ProgressSteps({
  steps,
  currentStep,
}: ProgressStepsProps) {
  return (
    <div className="relative border rounded-lg py-6 px-8 bg-background">
      <div className="absolute top-8 left-9 right-9 h-[2px] bg-gray-200">
        <div
          className="h-full bg-primary transition-all duration-300 ease-in-out"
          style={{
            width: `${((currentStep - 1) / (steps.length - 1)) * 100}%`,
          }}
        />
      </div>
      <div className="relative flex items-center justify-between">
        {steps.map((step) => (
          <div
            key={step.id}
            className={`flex bg-background  gap-2 ${
              currentStep >= step.id ? "text-primary" : "text-muted-foreground"
            }`}
          >
            <div
              className={`size-6  rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                currentStep > step.id
                  ? "bg-primary border-primary"
                  : currentStep === step.id
                  ? "bg-primary border-primary"
                  : "bg-white border-gray-200"
              }`}
            >
              {currentStep > step.id ? (
                <Check className="w-5 h-5 text-white" />
              ) : (
                <span
                  className={
                    currentStep === step.id
                      ? "text-white"
                      : "text-muted-foreground"
                  }
                >
                  {step.id}
                </span>
              )}
            </div>
            <div className="flex flex-col ">
              <div className="text-sm font-medium ">{step.title}</div>
              <div className="text-xs text-muted-foreground mt-1  ">
                {step.description}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
