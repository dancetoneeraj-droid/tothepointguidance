"use client";

import type { PaletteStatus } from "./types";

interface QuestionPaletteProps {
  total: number;
  safeIndex: number;
  getStatus: (index: number) => PaletteStatus;
  answered: number;
  unanswered: number;
  marked: number;
  disabled?: boolean;
  onSelect: (index: number) => void;
}

const statusStyles: Record<PaletteStatus, string> = {
  current:
    "ring-2 ring-violet-400 ring-offset-2 ring-offset-[#121218] bg-violet-600 text-white",
  answered: "bg-emerald-600/90 text-white border-emerald-500/50",
  marked: "bg-amber-500/90 text-black border-amber-400/50",
  "answered-marked": "bg-emerald-600 text-white ring-2 ring-amber-400",
  unanswered:
    "bg-[#1a1a22] text-zinc-400 border border-white/10 hover:border-white/25 hover:text-white",
};

export function QuestionPalette({
  total,
  safeIndex,
  getStatus,
  answered,
  unanswered,
  marked,
  disabled = false,
  onSelect,
}: QuestionPaletteProps) {
  return (
    <aside className="flex flex-col h-full rounded-xl border border-white/10 bg-[#121218] overflow-hidden">
      <div className="border-b border-white/10 px-4 py-3">
        <h2 className="text-sm font-semibold text-white">Question Palette</h2>
        <p className="text-xs text-zinc-500 mt-0.5">Click to jump</p>
      </div>

      <div className="p-3 grid grid-cols-6 gap-2 overflow-y-auto max-h-[320px] lg:max-h-none lg:flex-1">
        {Array.from({ length: total }, (_, i) => {
          const status = getStatus(i);
          return (
            <button
              key={i}
              type="button"
              disabled={disabled}
              onClick={() => onSelect(i)}
              className={`h-9 w-full rounded-md text-xs font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed ${statusStyles[status]}`}
              aria-label={`Question ${i + 1}`}
              aria-current={i === safeIndex ? "step" : undefined}
            >
              {i + 1}
            </button>
          );
        })}
      </div>

      <div className="mt-auto border-t border-white/10 p-4 space-y-3 text-xs">
        <div className="flex justify-between text-zinc-400">
          <span>Answered</span>
          <span className="text-emerald-400 font-medium">{answered}</span>
        </div>
        <div className="flex justify-between text-zinc-400">
          <span>Unanswered</span>
          <span className="text-zinc-300 font-medium">{unanswered}</span>
        </div>
        <div className="flex justify-between text-zinc-400">
          <span>Marked</span>
          <span className="text-amber-400 font-medium">{marked}</span>
        </div>
        <div className="flex flex-wrap gap-2 pt-2 border-t border-white/5">
          <Legend dot="bg-emerald-600" label="Answered" />
          <Legend dot="bg-amber-500" label="Marked" />
          <Legend dot="bg-violet-600" label="Current" />
          <Legend dot="bg-[#1a1a22] border border-white/10" label="Pending" />
        </div>
      </div>
    </aside>
  );
}

function Legend({ dot, label }: { dot: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1 text-zinc-500">
      <span className={`h-2.5 w-2.5 rounded-sm ${dot}`} />
      {label}
    </span>
  );
}
