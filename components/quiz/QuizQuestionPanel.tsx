"use client";

import { Bookmark, ChevronLeft, ChevronRight } from "lucide-react";
import type { Question } from "@/types";

interface QuizQuestionPanelProps {
  question: Question | undefined;
  questionNumber: number;
  total: number;
  subjectLabel: string;
  selected?: string;
  isMarked: boolean;
  onSelect: (option: string) => void;
  onMark: () => void;
  onPrev: () => void;
  onSaveAndNext: () => void;
  canGoPrev: boolean;
  isLast: boolean;
  disabled?: boolean;
}

const optionLabels = ["A", "B", "C", "D"];

export function QuizQuestionPanel({
  question,
  questionNumber,
  total,
  subjectLabel,
  selected,
  isMarked,
  onSelect,
  onMark,
  onPrev,
  onSaveAndNext,
  canGoPrev,
  isLast,
  disabled = false,
}: QuizQuestionPanelProps) {
  if (!question) {
    return (
      <div className="flex flex-1 items-center justify-center rounded-xl border border-dashed border-white/15 bg-[#121218] p-12">
        <div className="text-center">
          <p className="text-lg font-medium text-white">Question not found</p>
          <p className="text-sm text-zinc-500 mt-2">
            This question is missing from the quiz set. Use the palette or submit
            the test.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col rounded-xl border border-white/10 bg-[#121218] overflow-hidden">
      <div className="flex items-center justify-between border-b border-white/10 px-4 sm:px-6 py-3 bg-[#0f0f14]">
        <div>
          <span className="text-xs text-violet-400 font-medium uppercase tracking-wider">
            {subjectLabel}
          </span>
          <p className="text-sm text-zinc-400 mt-0.5">
            Question{" "}
            <span className="text-white font-semibold">{questionNumber}</span> of{" "}
            <span className="text-white font-semibold">{total}</span>
          </p>
        </div>
        <button
          type="button"
          onClick={onMark}
          disabled={disabled}
          className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors disabled:opacity-40 disabled:cursor-not-allowed ${
            isMarked
              ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
              : "bg-white/5 text-zinc-400 border border-white/10 hover:text-white"
          }`}
        >
          <Bookmark className={`h-3.5 w-3.5 ${isMarked ? "fill-current" : ""}`} />
          Mark for Review
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-5">
        <div className="space-y-3 rounded-xl border border-white/5 bg-[#0a0a0f]/80 p-4 sm:p-5">
          <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500">
            English
          </p>
          <p className="text-base sm:text-lg leading-relaxed text-zinc-100 whitespace-pre-wrap">
            {question.question}
          </p>
          {(question.questionHi ?? question.questionHindi) ? (
            <>
              <div className="border-t border-white/10 pt-3 mt-3">
                <p className="text-[10px] font-semibold uppercase tracking-wider text-amber-400/80 mb-2">
                  हिंदी
                </p>
                <p
                  className="text-base sm:text-lg leading-relaxed text-amber-50/95 whitespace-pre-wrap"
                  lang="hi"
                >
                  {question.questionHi ?? question.questionHindi}
                </p>
              </div>
            </>
          ) : null}
        </div>

        <div className="mt-6 space-y-2.5" role="radiogroup" aria-label="Answer options">
          {question.options.map((option, idx) => {
            const label = optionLabels[idx] ?? String(idx + 1);
            const optionHi = question.optionsHi?.[idx];
            const isSelected = selected === option;
            return (
              <button
                key={`${question.id}-${idx}`}
                type="button"
                role="radio"
                aria-checked={isSelected}
                disabled={disabled}
                onClick={() => onSelect(option)}
                className={`group w-full flex items-start gap-3 rounded-lg border px-4 py-3.5 text-left transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                  isSelected
                    ? "border-violet-500/60 bg-violet-500/15 shadow-[0_0_20px_rgba(139,92,246,0.15)]"
                    : "border-white/10 bg-[#0a0a0f] hover:border-violet-500/30 hover:bg-white/[0.03]"
                }`}
              >
                <span
                  className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-xs font-bold ${
                    isSelected
                      ? "bg-violet-600 text-white"
                      : "bg-white/10 text-zinc-400 group-hover:text-white"
                  }`}
                >
                  {label}
                </span>
                <span className="min-w-0 flex-1 pt-0.5">
                  <span
                    className={`block text-sm sm:text-base ${
                      isSelected ? "text-white" : "text-zinc-300"
                    }`}
                  >
                    {option}
                  </span>
                  {optionHi ? (
                    <span
                      className="block mt-1 text-sm text-amber-100/85 leading-snug"
                      lang="hi"
                    >
                      {optionHi}
                    </span>
                  ) : null}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="flex items-center justify-between gap-3 border-t border-white/10 px-4 sm:px-6 py-4 bg-[#0f0f14]">
        <button
          type="button"
          disabled={disabled || !canGoPrev}
          onClick={onPrev}
          className="inline-flex items-center gap-1 rounded-lg border border-white/10 px-4 py-2 text-sm text-zinc-300 disabled:opacity-40 hover:bg-white/5 transition-colors"
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </button>
        <button
          type="button"
          disabled={disabled}
          onClick={onSaveAndNext}
          className="inline-flex items-center gap-1 rounded-lg bg-violet-600 px-5 py-2 text-sm font-medium text-white hover:bg-violet-500 transition-colors shadow-lg shadow-violet-600/20 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isLast ? "Save & Submit" : "Save & Next"}
          <ChevronRight className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
