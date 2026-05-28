"use client";

import { Pause, Play } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface QuizPauseConfirmModalProps {
  open: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export function QuizPauseConfirmModal({
  open,
  onConfirm,
  onCancel,
}: QuizPauseConfirmModalProps) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="pause-confirm-title"
    >
      <div className="w-full max-w-sm rounded-2xl border border-white/10 bg-[#121218] p-6 shadow-2xl text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-amber-500/15">
          <Pause className="h-6 w-6 text-amber-400" />
        </div>
        <h2 id="pause-confirm-title" className="text-lg font-semibold text-white">
          Pause this test?
        </h2>
        <p className="mt-2 text-sm text-zinc-400">
          Are you sure that you want to pause this test?
        </p>
        <div className="mt-6 flex gap-3">
          <Button variant="secondary" className="flex-1" onClick={onCancel}>
            No, Continue
          </Button>
          <Button
            variant="primary"
            className="flex-1 bg-amber-600 hover:bg-amber-500"
            onClick={onConfirm}
          >
            Yes, Pause
          </Button>
        </div>
      </div>
    </div>
  );
}

interface QuizPausedOverlayProps {
  open: boolean;
  onResume: () => void;
}

export function QuizPausedOverlay({ open, onResume }: QuizPausedOverlayProps) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-40 flex items-center justify-center bg-[#08080a]/90 backdrop-blur-md"
      role="status"
      aria-live="polite"
    >
      <div className="text-center px-6">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-violet-500/15 border border-violet-500/30">
          <Pause className="h-8 w-8 text-violet-400" />
        </div>
        <h2 className="text-xl font-semibold text-white">Test Paused</h2>
        <p className="mt-2 text-sm text-zinc-400 max-w-xs mx-auto">
          Timer is paused. Resume to continue from the same question.
        </p>
        <Button
          variant="primary"
          size="lg"
          className="mt-6 min-w-[160px]"
          onClick={onResume}
        >
          <Play className="h-4 w-4" />
          Resume Test
        </Button>
      </div>
    </div>
  );
}
