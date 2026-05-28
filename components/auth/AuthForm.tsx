"use client";

import { useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";

interface AuthFormProps {
  mode: "login" | "signup";
  onSubmit: (data: {
    fullName: string;
    phone: string;
    email: string;
    password: string;
  }) => Promise<void>;
  loading?: boolean;
  error?: string | null;
}

export function AuthForm({ mode, onSubmit, loading, error }: AuthFormProps) {
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await onSubmit({ fullName, phone, email, password });
  };

  return (
    <form onSubmit={(e) => void handleSubmit(e)} className="space-y-4">
      {mode === "signup" ? (
        <>
          <Field
            label="Full Name"
            value={fullName}
            onChange={setFullName}
            required
            autoComplete="name"
          />
          <Field
            label="Phone Number"
            value={phone}
            onChange={setPhone}
            required
            type="tel"
            autoComplete="tel"
          />
        </>
      ) : null}

      <Field
        label="Gmail ID"
        value={email}
        onChange={setEmail}
        required
        type="email"
        autoComplete="email"
        placeholder="you@gmail.com"
      />

      <Field
        label="Password"
        value={password}
        onChange={setPassword}
        required
        type="password"
        autoComplete={mode === "signup" ? "new-password" : "current-password"}
        minLength={6}
      />

      {error ? (
        <p className="text-sm text-red-400 rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2">
          {error}
        </p>
      ) : null}

      <Button type="submit" className="w-full" size="lg" loading={loading}>
        {mode === "signup" ? "Create account" : "Log in"}
      </Button>
    </form>
  );
}

function Field({
  label,
  value,
  onChange,
  type = "text",
  required,
  autoComplete,
  placeholder,
  minLength,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
  required?: boolean;
  autoComplete?: string;
  placeholder?: string;
  minLength?: number;
}) {
  return (
    <label className="block text-left">
      <span className="text-xs font-medium text-muted uppercase tracking-wider">
        {label}
      </span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        autoComplete={autoComplete}
        placeholder={placeholder}
        minLength={minLength}
        className="mt-1.5 w-full rounded-xl border border-border bg-surface-hover/50 px-4 py-2.5 text-sm text-foreground placeholder:text-muted/60 focus:outline-none focus:ring-2 focus:ring-violet-500/40"
      />
    </label>
  );
}
