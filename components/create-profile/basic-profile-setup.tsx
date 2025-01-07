"use client";

import { Button } from "@/components/ui/button";
import { FormField } from "@/components/ui/form-field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useForm } from "react-hook-form";

interface BasicProfileSetupProps {
  onNext: () => void;
  formData: any;
  setFormData: (data: any) => void;
}

const EMOJI_OPTIONS = [
  "😊",
  "🤖",
  "🎯",
  "🎨",
  "💡",
  "🔧",
  "📚",
  "💻",
  "🎮",
  "🌟",
];

export default function BasicProfileSetup({
  onNext,
  formData,
  setFormData,
}: BasicProfileSetupProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      name: formData?.name || "",
      role: formData?.role || "",
      avatar: formData?.avatar || "🤖",
    },
  });

  const onSubmit = (data: any) => {
    setFormData({
      ...formData,
      name: data.name,
      role: data.role,
      avatar: formData.avatar || "🤖",
    });
    onNext();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6">
      <FormField
        label="Profile Emoji"
        description="Choose an emoji for your agent"
      >
        <Select
          defaultValue={formData?.avatar || "🤖"}
          onValueChange={(value) => setFormData({ ...formData, avatar: value })}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select emoji" />
          </SelectTrigger>
          <SelectContent>
            {EMOJI_OPTIONS.map((emoji) => (
              <SelectItem key={emoji} value={emoji}>
                {emoji}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </FormField>

      <FormField label="Name" description="Enter the agent name">
        <Input
          {...register("name", { required: "Name is required" })}
          placeholder="Enter agent name"
        />
        {errors.name && (
          <p className="text-sm text-red-500">
            {errors.name.message as string}
          </p>
        )}
      </FormField>

      <FormField label="Role" description="Enter the agent role">
        <Input
          {...register("role", { required: "Role is required" })}
          placeholder="Enter agent role"
        />
        {errors.role && (
          <p className="text-sm text-red-500">
            {errors.role.message as string}
          </p>
        )}
      </FormField>

      <div className="flex justify-end gap-3">
        <Button type="submit">Continue</Button>
      </div>
    </form>
  );
}
