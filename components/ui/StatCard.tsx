import type { LucideIcon } from "lucide-react";
import { Card } from "./Card";

interface StatCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon: LucideIcon;
  accent?: "violet" | "emerald" | "amber" | "sky";
}

const accents = {
  violet: "text-violet-400 bg-violet-500/10",
  emerald: "text-emerald-400 bg-emerald-500/10",
  amber: "text-amber-400 bg-amber-500/10",
  sky: "text-sky-400 bg-sky-500/10",
};

export function StatCard({
  label,
  value,
  subtext,
  icon: Icon,
  accent = "violet",
}: StatCardProps) {
  return (
    <Card className="p-4 sm:p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-muted uppercase tracking-wider">
            {label}
          </p>
          <p className="mt-1 text-2xl font-semibold text-foreground tabular-nums">
            {value}
          </p>
          {subtext ? (
            <p className="mt-0.5 text-xs text-muted">{subtext}</p>
          ) : null}
        </div>
        <div
          className={`flex h-10 w-10 items-center justify-center rounded-xl ${accents[accent]}`}
        >
          <Icon className="h-5 w-5" />
        </div>
      </div>
    </Card>
  );
}
