"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { useQuizSession } from "./useQuizSession";
import { QuizTopBar } from "./QuizTopBar";
import { QuizQuestionPanel } from "./QuizQuestionPanel";
import { QuestionPalette } from "./QuestionPalette";
import { QuizResultScreen } from "./QuizResultScreen";
import { QuizSubmitModal } from "./QuizSubmitModal";
import { QuizPauseConfirmModal } from "./QuizPauseOverlay";
import type { Question, QuizRanking, QuizResult } from "@/types";

interface QuizEngineProps {
  questions: Question[];
  durationMinutes: number;
  title: string;
  subjectLabel: string;
  sessionId: string;
  solutionsPath: string;
  analysisPath: string;
  onComplete: (
    result: QuizResult,
    answers: Record<string, string>
  ) => Promise<QuizRanking | null | void>;
  onPauseExit?: () => void;
}

export function QuizEngine({
  questions,
  durationMinutes,
  title,
  subjectLabel,
  sessionId,
  solutionsPath,
  analysisPath,
  onComplete,
  onPauseExit,
}: QuizEngineProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);

  const session = useQuizSession(
    questions,
    durationMinutes,
    sessionId,
    onComplete
  );

  const {
    ready,
    total,
    safeIndex,
    current,
    answers,
    marked,
    secondsLeft,
    isPaused,
    timeExpired,
    finished,
    submitting,
    result,
    ranking,
    stats,
    progressPercent,
    submitSummary,
    showSubmitModal,
    showPauseConfirm,
    interactionsDisabled,
    getPaletteStatus,
    selectAnswer,
    toggleMark,
    goTo,
    goPrev,
    saveAndNext,
    requestSubmit,
    confirmSubmit,
    dismissSubmitModal,
    requestPause,
    pauseAndSave,
    dismissPauseConfirm,
  } = session;

  const handlePauseConfirm = useCallback(() => {
    pauseAndSave();
    onPauseExit?.();
  }, [pauseAndSave, onPauseExit]);
  const loadError =
    total === 0
      ? "No questions loaded for this quiz. Check the question bank JSON."
      : null;

  const toggleFullscreen = useCallback(() => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen?.().catch(() => {});
      setIsFullscreen(false);
    }
  }, []);

  useEffect(() => {
    const onFsChange = () => setIsFullscreen(Boolean(document.fullscreenElement));
    document.addEventListener("fullscreenchange", onFsChange);
    return () => document.removeEventListener("fullscreenchange", onFsChange);
  }, []);

  useEffect(() => {
    if (!ready || finished || interactionsDisabled) return;

    const onKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;

      if (e.key === "ArrowLeft") {
        e.preventDefault();
        goPrev();
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        saveAndNext();
      } else if (e.key >= "1" && e.key <= "4") {
        const idx = parseInt(e.key, 10) - 1;
        const opt = current?.options[idx];
        if (opt) selectAnswer(opt);
      } else if (e.key === "m" || e.key === "M") {
        toggleMark();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [
    ready,
    finished,
    interactionsDisabled,
    goPrev,
    saveAndNext,
    current,
    selectAnswer,
    toggleMark,
  ]);

  if (!ready) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-3">
        <Loader2 className="h-10 w-10 animate-spin text-violet-500" />
        <p className="text-sm text-zinc-500">Loading quiz…</p>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4 max-w-md mx-auto text-center px-4">
        <AlertCircle className="h-12 w-12 text-amber-400" />
        <p className="text-white font-medium">{loadError}</p>
        <Button variant="secondary" onClick={() => window.history.back()}>
          Go back
        </Button>
      </div>
    );
  }

  if (finished && result) {
    return (
      <QuizResultScreen
        title={title}
        result={result}
        ranking={ranking}
        questions={questions}
        answers={answers}
        solutionsPath={solutionsPath}
        analysisPath={analysisPath}
      />
    );
  }

  const selected = current ? answers[current.id] : undefined;

  return (
    <div className="relative flex min-h-[calc(100vh-4rem)] flex-col bg-[#08080a] -mx-4 sm:-mx-6">
      <QuizTopBar
        title={title}
        subjectLabel={subjectLabel}
        secondsLeft={secondsLeft}
        isPaused={isPaused}
        isFullscreen={isFullscreen}
        submitting={submitting}
        onSubmit={requestSubmit}
        onPause={requestPause}
        onToggleFullscreen={toggleFullscreen}
      />

      <div
        className={`flex-1 px-3 sm:px-4 py-4 ${isPaused ? "pointer-events-none select-none opacity-60" : ""}`}
      >
        <div className="mb-3 flex items-center gap-3">
          <div className="flex-1 h-1.5 rounded-full bg-white/10 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-violet-600 to-indigo-500 transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <span className="text-xs text-zinc-500 tabular-nums shrink-0">
            {stats.answered}/{total} answered
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-4 min-h-[520px]">
          <QuizQuestionPanel
            question={current}
            questionNumber={safeIndex + 1}
            total={total}
            subjectLabel={subjectLabel}
            selected={selected}
            isMarked={marked.has(safeIndex)}
            disabled={interactionsDisabled}
            onSelect={selectAnswer}
            onMark={toggleMark}
            onPrev={goPrev}
            onSaveAndNext={saveAndNext}
            canGoPrev={safeIndex > 0}
            isLast={safeIndex >= total - 1}
          />

          <div className="lg:sticky lg:top-[4.5rem] lg:self-start">
            <QuestionPalette
              total={total}
              safeIndex={safeIndex}
              getStatus={getPaletteStatus}
              answered={stats.answered}
              unanswered={stats.unanswered}
              marked={stats.marked}
              disabled={interactionsDisabled}
              onSelect={goTo}
            />
          </div>
        </div>
      </div>

      <QuizSubmitModal
        open={showSubmitModal}
        summary={submitSummary}
        submitting={submitting}
        timeExpired={timeExpired}
        onConfirm={confirmSubmit}
        onCancel={dismissSubmitModal}
      />

      <QuizPauseConfirmModal
        open={showPauseConfirm}
        onConfirm={handlePauseConfirm}
        onCancel={dismissPauseConfirm}
      />
    </div>
  );
}
