"use client";

import Link from "next/link";
import { CheckCircle2 } from "lucide-react";

export interface DayProgressItem {
  day: number;
  percent: number;
  complete: boolean;
}

export function DayWiseProgressList({ days }: { days: DayProgressItem[] }) {
  return (
    <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
      {days.map((d) => (
        <Link
          key={d.day}
          href={`/day/${d.day}`}
          className="block rounded-xl border border-border bg-surface-hover/30 p-3 hover:border-violet-500/30 transition-colors"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-foreground flex items-center gap-2">
              Day {d.day}
              {d.complete ? (
                <CheckCircle2 className="h-4 w-4 text-emerald-400" />
              ) : null}
            </span>
            <span
              className={`text-xs font-semibold tabular-nums ${
                d.complete ? "text-emerald-400" : "text-violet-400"
              }`}
            >
              {d.percent}%
            </span>
          </div>
          <div className="w-full h-2 rounded-full bg-surface-hover overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                d.complete
                  ? "bg-emerald-500"
                  : "bg-gradient-to-r from-violet-500 to-indigo-500"
              }`}
              style={{ width: `${d.percent}%` }}
            />
          </div>
        </Link>
      ))}
    </div>
  );
}
