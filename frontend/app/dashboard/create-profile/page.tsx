"use client";

import BasicProfileSetup from "@/components/create-profile/basic-profile-setup";
import CapabilitiesIntegration from "@/components/create-profile/capabilities-integration";
import ProgressSteps from "@/components/create-profile/progress-steps";
import TrainingPersonality from "@/components/create-profile/training-personality";
import { useState } from "react";

const steps = [
  {
    id: 1,
    title: "Basic Profile Setup",
    description: "Define agent's identity.",
  },
  {
    id: 2,
    title: "Training & Personality",
    description: "Customize behavior and tone.",
  },
  {
    id: 3,
    title: "Capabilities & Integration",
    description: "Enable skills and AI tools.",
  },
];

export default function CreateProfile() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<any>({});

  const handleNext = () => {
    setCurrentStep((prev) => Math.min(prev + 1, steps.length));
  };

  const handleBack = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 1));
  };

  return (
    <div className="container">
      <div className="bg-white rounded-xl p-6 border">
        <div>
          <div className="mb-8">
            <h1 className="text-2xl font-semibold mb-1">Create Profile</h1>
            <p className="text-sm text-muted-light">
              Create your AI agent profile
            </p>
          </div>

          <div>
            <div className="mb-12">
              <ProgressSteps steps={steps} currentStep={currentStep} />
            </div>

            <div>
              {currentStep === 1 && (
                <BasicProfileSetup
                  onNext={handleNext}
                  formData={formData}
                  setFormData={setFormData}
                />
              )}
              {currentStep === 2 && (
                <TrainingPersonality
                  onNext={handleNext}
                  onBack={handleBack}
                  formData={formData}
                  setFormData={setFormData}
                />
              )}
              {currentStep === 3 && (
                <CapabilitiesIntegration
                  onBack={handleBack}
                  formData={formData}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
