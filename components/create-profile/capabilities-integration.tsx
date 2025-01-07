"use client";

import { Button } from "@/components/ui/button";
import { FormField } from "@/components/ui/form-field";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/axios";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";

interface CapabilitiesIntegrationProps {
  onBack: () => void;
  formData: any;
}

export default function CapabilitiesIntegration({
  onBack,
  formData,
}: CapabilitiesIntegrationProps) {
  const router = useRouter();
  const [expertise, setExpertise] = useState<string[]>(
    formData?.expertise || []
  );
  const [expertiseInput, setExpertiseInput] = useState("");
  const [isPending, setIsPending] = useState(false);
  const { register, handleSubmit } = useForm();

  const addExpertise = () => {
    if (expertiseInput.trim()) {
      setExpertise((prev) => [...prev, expertiseInput.trim()]);
      setExpertiseInput("");
    }
  };

  const removeExpertise = (index: number) => {
    setExpertise((prev) => prev.filter((_, i) => i !== index));
  };

  const onSubmit = async () => {
    setIsPending(true);
    try {
      const form = new FormData();
      form.append("name", formData.name);
      form.append("role", formData.role);
      form.append("avatar", formData.avatar ?? "🤖");
      form.append("expertise", expertise.join(","));
      form.append("personality", formData.personality);

      if (formData.documents && formData.documents.length > 0) {
        formData.documents.forEach((doc: File) => {
          if (doc.name) {
            form.append("documents", doc, doc.name);
          }
        });
      }

      await api.post("/agents", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      router.push("/dashboard/chat");
    } catch (error) {
      console.error("Error creating agent:", error);
    } finally {
      setIsPending(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6">
      <FormField
        label="Expertise Areas"
        description="Add your agent's areas of expertise"
      >
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input
              value={expertiseInput}
              onChange={(e) => setExpertiseInput(e.target.value)}
              placeholder="Type and press Enter to add expertise"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  addExpertise();
                }
              }}
            />
            <Button type="button" onClick={addExpertise}>
              Add
            </Button>
          </div>
          <div className="flex flex-wrap gap-2">
            {expertise.map((item, index) => (
              <div
                key={index}
                className="bg-primary/10 text-primary px-3 py-0.5 text-sm border border-primary/20 rounded-full flex items-center gap-2"
              >
                <span>{item}</span>
                <button
                  type="button"
                  onClick={() => removeExpertise(index)}
                  className="hover:text-primary/80"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      </FormField>

      <div className="flex justify-end gap-3">
        <Button type="button" variant="outline" onClick={onBack}>
          Back
        </Button>
        <Button type="submit">
          {isPending ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            "Save Information"
          )}
        </Button>
      </div>
    </form>
  );
}
