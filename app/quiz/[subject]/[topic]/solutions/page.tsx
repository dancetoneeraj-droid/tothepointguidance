"use client";

import { use, useMemo, type ComponentType } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  GraduationCap,
  Lightbulb,
  XCircle,
} from "lucide-react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { Card } from "@/components/ui/Card";
import { useAuth } from "@/components/providers/AuthProvider";
import { canAccessDay } from "@/lib/premium-access";
import { formatTopic } from "@/lib/day-system";
import { loadQuizAnalytics } from "@/lib/api/ecosystem";
import { getQuizReviewRecord } from "@/lib/storage";
import { getQuestionBank } from "@/lib/quiz-loader";
import { getReviewQuestions, getReviewStatus } from "@/lib/quiz/review";

export default function QuizSolutionsPage({
  params,
}: {
  params: Promise<{ subject: string; topic: string }>;
}) {
  const { subject, topic } = use(params);
  const searchParams = useSearchParams();
  const day = parseInt(searchParams.get("day") ?? "1", 10);
  const { studentId, user } = useAuth();

  const data = useMemo(() => {
    if (!studentId) return null;

    const saved = getQuizReviewRecord(studentId, day, subject, topic);
    if (saved) return saved;

    const recent = loadQuizAnalytics();
    if (
      recent &&
      recent.day === day &&
      recent.subject === subject &&
      recent.topic === topic
    ) {
      return recent;
    }

    return null;
  }, [studentId, day, subject, topic]);

  if (!canAccessDay(day, user?.email)) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#08080a] py-12 px-4">
          <PremiumLockCard day={day} />
        </div>
      </ProtectedRoute>
    );
  }

  if (!data) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#08080a] flex items-center justify-center px-4">
          <Card className="p-8 text-center max-w-md">
            <p className="text-white font-medium">No solution data found</p>
            <p className="mt-2 text-sm text-muted">
              Complete the quiz first to open coaching-style solutions.
            </p>
            <Link
              href={`/quiz/${subject}/${topic}?day=${day}`}
              className="mt-6 inline-flex text-sm text-violet-300 hover:text-violet-200"
            >
              Back to result
            </Link>
          </Card>
        </div>
      </ProtectedRoute>
    );
  }

  const questions = getReviewQuestions(
    getQuestionBank(subject as "maths" | "reasoning" | "gk", topic),
    data.questionIds
  );
  const title = `${formatTopic(topic)} — Day ${day}`;
  const correctCount = questions.filter(
    (question) => getReviewStatus(question, data.answers) === "correct"
  ).length;
  const wrongCount = questions.filter(
    (question) => getReviewStatus(question, data.answers) === "wrong"
  ).length;
  const unattemptedCount = questions.length - correctCount - wrongCount;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#08080a] px-4 py-8 sm:px-6">
        <div className="mx-auto max-w-6xl space-y-6">
          <Link
            href={`/quiz/${subject}/${topic}?day=${day}`}
            className="inline-flex items-center gap-1 text-sm text-zinc-500 hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to result
          </Link>

          <header className="overflow-hidden rounded-[28px] border border-white/10 bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.15),_transparent_42%),linear-gradient(180deg,rgba(18,18,24,0.96),rgba(10,10,15,0.96))] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.32)]">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-emerald-300">
                  Coaching Review
                </p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
                  View Solutions
                </h1>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-400">
                  {title}. Review what you marked, what was correct, and the
                  explanation behind every question in a clean coaching-institute
                  format.
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <SolutionSummaryChip
                  icon={CheckCircle2}
                  label="Correct"
                  value={correctCount}
                  tone="emerald"
                />
                <SolutionSummaryChip
                  icon={XCircle}
                  label="Wrong"
                  value={wrongCount}
                  tone="rose"
                />
                <SolutionSummaryChip
                  icon={Circle}
                  label="Unattempted"
                  value={unattemptedCount}
                  tone="slate"
                />
              </div>
            </div>
          </header>

          <div className="space-y-4">
            {questions.map((question, index) => {
              const selectedAnswer = data.answers[question.id];
              const status = getReviewStatus(question, data.answers);
              const badge =
                status === "correct"
                  ? {
                      label: "Correct",
                      tone: "border-emerald-400/20 bg-emerald-500/10 text-emerald-300",
                      icon: CheckCircle2,
                    }
                  : status === "wrong"
                    ? {
                        label: "Wrong",
                        tone: "border-rose-400/20 bg-rose-500/10 text-rose-300",
                        icon: XCircle,
                      }
                    : {
                        label: "Unattempted",
                        tone: "border-zinc-400/20 bg-zinc-500/10 text-zinc-300",
                        icon: Circle,
                      };
              const StatusIcon = badge.icon;

              return (
                <Card
                  key={question.id}
                  className="overflow-hidden border-white/10 bg-[#121218]/90"
                >
                  <div className="border-b border-white/10 bg-white/[0.03] px-5 py-4 sm:px-6">
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-violet-300">
                          Question {index + 1}
                        </p>
                        <p className="mt-2 text-base leading-7 text-zinc-100">
                          {question.question}
                        </p>
                        {question.questionHi ? (
                          <p
                            className="mt-3 text-base leading-7 text-amber-50/90"
                            lang="hi"
                          >
                            {question.questionHi}
                          </p>
                        ) : null}
                      </div>
                      <div
                        className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-semibold ${badge.tone}`}
                      >
                        <StatusIcon className="h-4 w-4" />
                        {status === "correct" ? "✅" : status === "wrong" ? "❌" : "⚪"}{" "}
                        {badge.label}
                      </div>
                    </div>
                  </div>

                  <div className="grid gap-4 px-5 py-5 sm:px-6 lg:grid-cols-2">
                    <AnswerPanel
                      label="Your selected answer"
                      value={selectedAnswer ?? "Not attempted"}
                      tone={
                        status === "correct"
                          ? "border-emerald-400/20 bg-emerald-500/10 text-emerald-200"
                          : status === "wrong"
                            ? "border-rose-400/20 bg-rose-500/10 text-rose-200"
                            : "border-zinc-400/20 bg-zinc-500/10 text-zinc-200"
                      }
                    />
                    <AnswerPanel
                      label="Correct answer"
                      value={question.correctAnswer}
                      tone="border-violet-400/20 bg-violet-500/10 text-violet-100"
                    />
                  </div>

                  <div className="border-t border-white/10 px-5 py-5 sm:px-6">
                    <div className="flex items-center gap-2 text-emerald-300">
                      <GraduationCap className="h-4 w-4" />
                      <p className="text-sm font-semibold uppercase tracking-[0.18em]">
                        Explanation / Solution
                      </p>
                    </div>
                    <div className="mt-3 rounded-2xl border border-white/10 bg-black/20 p-4 sm:p-5">
                      {question.explanation ? (
                        <p className="text-sm leading-7 text-zinc-200 whitespace-pre-wrap">
                          {question.explanation}
                        </p>
                      ) : (
                        <div className="flex items-start gap-3 text-sm text-zinc-400">
                          <Lightbulb className="mt-0.5 h-4 w-4 text-amber-300" />
                          <p>
                            Detailed explanation has not been added for this question
                            yet. The correct answer for coaching review is{" "}
                            <span className="font-medium text-violet-200">
                              {question.correctAnswer}
                            </span>
                            .
                          </p>
                        </div>
                      )}
                      {question.explanationHi ? (
                        <p
                          className="mt-4 border-t border-white/10 pt-4 text-sm leading-7 text-amber-50/90 whitespace-pre-wrap"
                          lang="hi"
                        >
                          {question.explanationHi}
                        </p>
                      ) : null}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}

function SolutionSummaryChip({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: ComponentType<{ className?: string }>;
  label: string;
  value: number;
  tone: "emerald" | "rose" | "slate";
}) {
  const tones = {
    emerald: "border-emerald-400/20 bg-emerald-500/10 text-emerald-300",
    rose: "border-rose-400/20 bg-rose-500/10 text-rose-300",
    slate: "border-zinc-400/20 bg-zinc-500/10 text-zinc-300",
  };

  return (
    <div className={`rounded-2xl border px-4 py-3 ${tones[tone]}`}>
      <div className="flex items-center gap-2">
        <Icon className="h-4 w-4" />
        <p className="text-[11px] font-semibold uppercase tracking-[0.16em]">
          {label}
        </p>
      </div>
      <p className="mt-2 text-xl font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}

function AnswerPanel({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: string;
}) {
  return (
    <div className={`rounded-2xl border p-4 ${tone}`}>
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-400">
        {label}
      </p>
      <p className="mt-3 text-sm leading-6 text-current whitespace-pre-wrap">
        {value}
      </p>
    </div>
  );
}
