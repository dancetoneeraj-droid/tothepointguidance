"use client";

import { Send, X } from "lucide-react";
import { Button } from "@/components/ui/Button";

export interface SubmitSummary {
  total: number;
  answered: number;
  notAnswered: number;
  visited: number;
  notVisited: number;
}

interface QuizSubmitModalProps {
  open: boolean;
  summary: SubmitSummary;
  submitting: boolean;
  /** When time is up, user must submit (no continue). */
  timeExpired?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

function StatRow({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-white/10 bg-white/[0.03] px-4 py-3">
      <span className="text-sm text-zinc-400">{label}</span>
      <span className="text-base font-semibold text-white tabular-nums">{value}</span>
    </div>
  );
}

export function QuizSubmitModal({
  open,
  summary,
  submitting,
  timeExpired = false,
  onConfirm,
  onCancel,
}: QuizSubmitModalProps) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="submit-quiz-title"
    >
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-[#121218] shadow-2xl">
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
          <h2 id="submit-quiz-title" className="text-lg font-semibold text-white">
            Submit Test?
          </h2>
          {!timeExpired ? (
            <button
              type="button"
              onClick={onCancel}
              disabled={submitting}
              className="rounded-lg p-1.5 text-zinc-500 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-40"
              aria-label="Close"
            >
              <X className="h-5 w-5" />
            </button>
          ) : null}
        </div>

        <div className="px-5 py-4 space-y-2">
          <StatRow label="Total Questions" value={summary.total} />
          <StatRow label="Answered" value={summary.answered} />
          <StatRow label="Not Answered" value={summary.notAnswered} />
          <StatRow label="Visited" value={summary.visited} />
          <StatRow label="Not Visited" value={summary.notVisited} />
        </div>

        <p className="px-5 text-xs text-zinc-500">
          Once submitted, you cannot change your answers for this attempt.
        </p>

        <div className="flex gap-3 border-t border-white/10 px-5 py-4">
          {!timeExpired ? (
            <Button
              variant="secondary"
              className="flex-1"
              onClick={onCancel}
              disabled={submitting}
            >
              Continue Test
            </Button>
          ) : null}
          <Button
            variant="primary"
            className={`${timeExpired ? "w-full" : "flex-1"} bg-amber-600 hover:bg-amber-500`}
            onClick={onConfirm}
            loading={submitting}
          >
            <Send className="h-4 w-4" />
            {timeExpired ? "Time Up — Submit Test" : "Submit Test"}
          </Button>
        </div>
      </div>
    </div>
  );
}
