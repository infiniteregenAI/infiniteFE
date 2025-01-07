"use client";

import { Button } from "@/components/ui/button";
import { FormField } from "@/components/ui/form-field";
import { Textarea } from "@/components/ui/textarea";
import { Database, X } from "lucide-react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";

interface FileWithPreview extends File {
  preview?: string;
  progress?: number;
}

interface TrainingPersonalityProps {
  onNext: () => void;
  onBack: () => void;
  formData: any;
  setFormData: (data: any) => void;
}

export default function TrainingPersonality({
  onNext,
  onBack,
  formData,
  setFormData,
}: TrainingPersonalityProps) {
  const [documents, setDocuments] = useState<FileWithPreview[]>(
    formData?.documents || []
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      personality: formData?.personality || "",
    },
  });

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((file) =>
      Object.assign(file, {
        preview: URL.createObjectURL(file),
        progress: 100,
      })
    );
    setDocuments((prev) => [...prev, ...newFiles]);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
      "application/epub+zip": [".epub"],
    },
  });

  const removeDocument = (index: number) => {
    setDocuments((prev) => {
      const newDocs = prev.filter((_, i) => i !== index);
      // Clean up the URL.createObjectURL
      if (prev[index]?.preview) {
        URL.revokeObjectURL(prev[index].preview!);
      }
      return newDocs;
    });
  };

  const onSubmit = (data: any) => {
    setFormData({
      ...formData,
      personality: data.personality,
      documents: documents,
    });
    onNext();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6">
      <FormField label="Training Data" description="Upload training data files">
        <div className="flex-1 max-w-lg">
          <div
            {...getRootProps()}
            className="border-2 border-dashed bg-background rounded-lg px-8 py-14 text-center cursor-pointer"
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-2">
              <div className="size-10 bg-primary/10 rounded-full mb-2 flex items-center justify-center">
                <Database size={24} className="text-primary" />
              </div>
              <p className="text-sm font-medium">
                Drag & Drop or <span className="text-primary">Choose file</span>{" "}
                to upload
              </p>
              <p className="text-xs text-muted-light">
                PDF, DOC, EPUB (Max size: 10MB)
              </p>
            </div>
          </div>

          <div className="mt-4 flex flex-col gap-2">
            {documents.map((doc, index) => (
              <div
                key={index}
                className="border rounded-lg p-4 flex items-center justify-between"
              >
                <div className="flex items-center gap-3 w-full">
                  <img src="/file.svg" alt="file" className="size-10" />
                  <div className="flex-1 w-full gap-1.5 flex flex-col">
                    <p className="text-sm font-medium">{doc.name}</p>
                    <span className="text-xs text-muted-light">
                      {Math.round(doc.size / 1024)} KB
                    </span>
                  </div>
                </div>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  onClick={() => removeDocument(index)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      </FormField>

      <FormField
        label="Personality Prompt"
        description="Define your agent's tone and behaviors"
      >
        <div className="flex-1 space-y-2 max-w-lg">
          <Textarea
            {...register("personality", {
              required: "Personality prompt is required",
            })}
            placeholder="Describe the agent's personality in natural language. For example: Empathetic, analytical, and formal in tone. This guides how the agent responds."
            className="min-h-[120px]"
          />
          {errors.personality && (
            <p className="text-sm text-red-500">
              {errors.personality.message as string}
            </p>
          )}
          <p className="text-xs text-muted-light">Must be around 100 words.</p>
        </div>
      </FormField>

      <div className="flex justify-end gap-3">
        <Button type="button" variant="outline" onClick={onBack}>
          Back
        </Button>
        <Button type="submit">Continue</Button>
      </div>
    </form>
  );
}
