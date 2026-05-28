"use client";

import { Clock, Maximize2, Minimize2, Pause, Send } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface QuizTopBarProps {
  title: string;
  subjectLabel: string;
  secondsLeft: number;
  isPaused: boolean;
  isFullscreen: boolean;
  submitting: boolean;
  onSubmit: () => void;
  onPause: () => void;
  onToggleFullscreen: () => void;
}

function formatTime(s: number) {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
  }
  return `${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
}

export function QuizTopBar({
  title,
  subjectLabel,
  secondsLeft,
  isPaused,
  isFullscreen,
  submitting,
  onSubmit,
  onPause,
  onToggleFullscreen,
}: QuizTopBarProps) {
  const urgent = secondsLeft < 300;

  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-[#0a0a0c]/95 backdrop-blur-md">
      <div className="flex h-14 items-center justify-between gap-3 px-3 sm:px-5">
        <div className="min-w-0 flex-1">
          <p className="text-[10px] uppercase tracking-widest text-violet-400/90 font-medium">
            {subjectLabel}
          </p>
          <h1 className="truncate text-sm sm:text-base font-semibold text-white">
            {title}
          </h1>
        </div>

        <div className="flex items-center gap-2">
          <div
            className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 font-mono text-sm tabular-nums ${
              isPaused
                ? "border-amber-500/40 bg-amber-500/10 text-amber-400"
                : urgent
                  ? "border-red-500/40 bg-red-500/10 text-red-400 animate-pulse"
                  : "border-white/10 bg-white/5 text-emerald-400"
            }`}
          >
            <Clock className="h-4 w-4 shrink-0" />
            <span>{isPaused ? "PAUSED" : formatTime(secondsLeft)}</span>
          </div>
          <button
            type="button"
            onClick={onPause}
            disabled={isPaused || submitting}
            className="inline-flex h-9 items-center gap-1.5 rounded-lg border border-white/10 px-2.5 sm:px-3 text-xs font-medium text-zinc-300 hover:text-white hover:bg-white/5 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Pause className="h-4 w-4 shrink-0" />
            <span className="hidden sm:inline">Pause</span>
          </button>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            type="button"
            onClick={onToggleFullscreen}
            className="hidden sm:flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-muted hover:text-white hover:bg-white/5 transition-colors"
            aria-label={isFullscreen ? "Exit fullscreen" : "Fullscreen"}
          >
            {isFullscreen ? (
              <Minimize2 className="h-4 w-4" />
            ) : (
              <Maximize2 className="h-4 w-4" />
            )}
          </button>
          <Button
            variant="primary"
            size="sm"
            onClick={onSubmit}
            loading={submitting}
            className="bg-amber-600 hover:bg-amber-500 shadow-amber-500/20"
          >
            <Send className="h-4 w-4" />
            <span className="hidden sm:inline">Submit Test</span>
            <span className="sm:hidden">Submit</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
