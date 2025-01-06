import { ReactNode } from "react";
import { Label } from "./label";

interface FormFieldProps {
  label: string;
  description?: string;
  children: ReactNode;
  className?: string;
}

export function FormField({
  label,
  description,
  children,
  className = "",
}: FormFieldProps) {
  return (
    <div className={`flex ${className}`}>
      <div className="flex flex-col gap-2 w-[25rem]">
        <Label>{label}</Label>
        {description && (
          <p className="text-sm text-muted-light">{description}</p>
        )}
      </div>
      <div className="flex-1 max-w-lg">{children}</div>
    </div>
  );
}

interface FormDividerProps {
  className?: string;
}

export function FormDivider({ className = "" }: FormDividerProps) {
  return <div className={`flex w-full h-px bg-gray-200 ${className}`} />;
}

interface FormActionsProps {
  children: ReactNode;
  className?: string;
}

export function FormActions({ children, className = "" }: FormActionsProps) {
  return (
    <div className={`flex justify-end gap-3 ${className}`}>{children}</div>
  );
}
