import type { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  glow?: boolean;
}

export function Card({
  className = "",
  glow,
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={`rounded-2xl border border-border bg-surface/80 backdrop-blur-sm ${
        glow ? "shadow-glow" : "shadow-card"
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
