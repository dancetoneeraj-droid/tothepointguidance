"use client";

import { use, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  BookOpen,
  Check,
  CircleDot,
  RotateCcw,
  Sparkles,
  Trophy,
} from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { AppShell } from "@/components/layout/AppShell";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { canAccessDay } from "@/lib/premium-access";
import { getVocabDeckForDay, hasVocabForDay } from "@/lib/vocab";
import {
  getVocabProgress,
  markVocabDayCompleted,
  recordVocabReview,
} from "@/lib/storage";
import type { VocabWord, VocabWordProgress } from "@/types";

export default function VocabPage({
  params,
}: {
  params: Promise<{ day: string }>;
}) {
  const { day: dayParam } = use(params);
  const dayNum = parseInt(dayParam, 10);
  const { studentId, progress, user } = useAuth();

  const [vocabProgress, setVocabProgress] = useState<
    Record<string, VocabWordProgress>
  >(() => (studentId ? getVocabProgress(studentId) : {}));

  // The deck is frozen at mount so reviewing words mid-session does not
  // re-order the cards under the student.
  const deck = useMemo(() => {
    const { reviewWords, newWords } = getVocabDeckForDay(dayNum, vocabProgress);
    return [...reviewWords, ...newWords];
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dayNum]);

  const reviewCount = useMemo(() => {
    return getVocabDeckForDay(dayNum, vocabProgress).reviewWords.length;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dayNum]);

  const [index, setIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [knewCount, setKnewCount] = useState(0);
  const [circledCount, setCircledCount] = useState(0);
  const [finished, setFinished] = useState(false);

  if (!studentId || !progress) return null;

  if (!canAccessDay(dayNum, user?.email)) {
    return (
      <ProtectedRoute>
        <AppShell>
          <PremiumLockCard day={dayNum} />
        </AppShell>
      </ProtectedRoute>
    );
  }

  if (!hasVocabForDay(dayNum) || deck.length === 0) {
    return (
      <ProtectedRoute>
        <AppShell>
          <Card className="mx-auto max-w-lg border-white/10 bg-white/[0.03] p-8 text-center">
            <h1 className="text-xl font-semibold text-white">
              Day {dayNum} Vocabulary
            </h1>
            <p className="mt-2 text-sm text-zinc-400">
              Vocabulary words for this day are not added yet.
            </p>
            <Link
              href={`/day/${dayNum}`}
              className="mt-6 inline-block text-sm text-violet-400"
            >
              ← Back to Day {dayNum}
            </Link>
          </Card>
        </AppShell>
      </ProtectedRoute>
    );
  }

  const total = deck.length;
  const currentWord: VocabWord = deck[Math.min(index, total - 1)]!;
  const isReviewCard = index < reviewCount;
  const existingCircles = vocabProgress[currentWord.id]?.circles ?? 0;
  const completionPercent = Math.round((index / total) * 100);

  const handleAnswer = (knew: boolean) => {
    recordVocabReview(
      studentId,
      currentWord.id,
      knew,
      dayNum,
      currentWord.day
    );

    setVocabProgress((prev) => ({
      ...prev,
      [currentWord.id]: {
        wordId: currentWord.id,
        circles: knew ? prev[currentWord.id]?.circles ?? 0 : existingCircles + 1,
        mastered: knew,
        learnedDay: prev[currentWord.id]?.learnedDay ?? currentWord.day,
        lastReviewedDay: dayNum,
      },
    }));

    if (knew) setKnewCount((c) => c + 1);
    else setCircledCount((c) => c + 1);

    if (index + 1 >= total) {
      markVocabDayCompleted(studentId, dayNum);
      setFinished(true);
      return;
    }

    setIndex((i) => i + 1);
    setRevealed(false);
  };

  if (finished) {
    return (
      <ProtectedRoute>
        <AppShell>
          <div className="mx-auto max-w-2xl space-y-6 animate-in">
            <Card glow className="border-white/10 bg-white/[0.03] p-8 text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-emerald-400/30 bg-emerald-500/15 text-emerald-300">
                <Trophy className="h-7 w-7" />
              </div>
              <h1 className="mt-5 text-2xl font-semibold text-white">
                Day {dayNum} vocabulary done!
              </h1>
              <p className="mt-2 text-sm text-zinc-400">
                Circled words will come back for revision on your next day —
                exactly like your circle method.
              </p>

              <div className="mt-6 grid grid-cols-3 gap-3">
                <SummaryStat label="Reviewed" value={total} tone="violet" />
                <SummaryStat label="Knew it" value={knewCount} tone="emerald" />
                <SummaryStat
                  label="Circled"
                  value={circledCount}
                  tone="amber"
                />
              </div>

              <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:justify-center">
                <Link href={`/day/${dayNum}`}>
                  <Button variant="secondary" className="w-full sm:w-auto">
                    <ArrowLeft className="h-4 w-4" />
                    Back to Day {dayNum}
                  </Button>
                </Link>
                <Button
                  className="w-full sm:w-auto"
                  onClick={() => {
                    setIndex(0);
                    setRevealed(false);
                    setKnewCount(0);
                    setCircledCount(0);
                    setFinished(false);
                  }}
                >
                  <RotateCcw className="h-4 w-4" />
                  Revise again
                </Button>
              </div>
            </Card>
          </div>
        </AppShell>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AppShell>
        <div className="mx-auto max-w-2xl space-y-6 animate-in">
          <header className="space-y-4">
            <Link
              href={`/day/${dayNum}`}
              className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground"
            >
              <ArrowLeft className="h-4 w-4" />
              Day {dayNum}
            </Link>
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-200">
                <Sparkles className="h-3.5 w-3.5" />
                Day {dayNum} Vocabulary
              </span>
              {reviewCount > 0 ? (
                <span className="inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1 text-xs text-amber-200">
                  <CircleDot className="h-3.5 w-3.5" />
                  {reviewCount} to revise
                </span>
              ) : null}
            </div>
            <ProgressBar
              value={completionPercent}
              label={`Word ${index + 1} of ${total}`}
            />
          </header>

          <Card
            glow
            className="border-white/10 bg-[linear-gradient(180deg,rgba(124,58,237,0.08),rgba(255,255,255,0.02))] p-7 sm:p-9"
          >
            <div className="flex items-center justify-between">
              <span
                className={`rounded-full border px-3 py-1 text-[11px] font-medium ${
                  isReviewCard
                    ? "border-amber-500/20 bg-amber-500/10 text-amber-200"
                    : "border-violet-500/20 bg-violet-500/10 text-violet-200"
                }`}
              >
                {isReviewCard ? "Revision" : "New word"}
              </span>
              {existingCircles > 0 ? (
                <span className="inline-flex items-center gap-1 text-xs text-amber-300">
                  {Array.from({ length: Math.min(existingCircles, 5) }).map(
                    (_, i) => (
                      <CircleDot key={i} className="h-3.5 w-3.5" />
                    )
                  )}
                  {existingCircles} circle{existingCircles === 1 ? "" : "s"}
                </span>
              ) : null}
            </div>

            <div className="mt-6 text-center">
              <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                {currentWord.word}
              </h2>
            </div>

            {revealed ? (
              <div className="mt-7 space-y-3 text-left animate-in">
                <DetailRow label="Meaning" value={currentWord.meaning} />
                <DetailRow label="Hindi" value={currentWord.hindi} />
                <div className="grid gap-3 sm:grid-cols-2">
                  <DetailRow
                    label="Synonym"
                    value={currentWord.synonym}
                    tone="emerald"
                  />
                  <DetailRow
                    label="Antonym"
                    value={currentWord.antonym}
                    tone="rose"
                  />
                </div>
                <DetailRow
                  label="Example"
                  value={currentWord.example}
                  italic
                />
              </div>
            ) : (
              <p className="mt-7 text-center text-sm text-zinc-500">
                Try to recall the meaning, then reveal.
              </p>
            )}

            <div className="mt-8">
              {!revealed ? (
                <Button
                  size="lg"
                  className="w-full justify-center"
                  onClick={() => setRevealed(true)}
                >
                  <BookOpen className="h-4 w-4" />
                  Reveal meaning
                </Button>
              ) : (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  <Button
                    size="lg"
                    variant="secondary"
                    className="w-full justify-center border-amber-500/30 bg-amber-500/10 text-amber-200 hover:bg-amber-500/20"
                    onClick={() => handleAnswer(false)}
                  >
                    <CircleDot className="h-4 w-4" />
                    Put a circle (revise again)
                  </Button>
                  <Button
                    size="lg"
                    className="w-full justify-center bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500"
                    onClick={() => handleAnswer(true)}
                  >
                    <Check className="h-4 w-4" />
                    Knew it
                  </Button>
                </div>
              )}
            </div>
          </Card>
        </div>
      </AppShell>
    </ProtectedRoute>
  );
}

function DetailRow({
  label,
  value,
  tone = "default",
  italic,
}: {
  label: string;
  value: string;
  tone?: "default" | "emerald" | "rose";
  italic?: boolean;
}) {
  const toneClasses: Record<string, string> = {
    default: "border-white/10 bg-white/[0.03] text-zinc-200",
    emerald: "border-emerald-500/20 bg-emerald-500/[0.07] text-emerald-100",
    rose: "border-rose-500/20 bg-rose-500/[0.07] text-rose-100",
  };
  return (
    <div className={`rounded-2xl border px-4 py-3 ${toneClasses[tone]}`}>
      <p className="text-[11px] uppercase tracking-[0.2em] text-zinc-500">
        {label}
      </p>
      <p className={`mt-1 text-sm leading-6 ${italic ? "italic" : ""}`}>
        {value}
      </p>
    </div>
  );
}

function SummaryStat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "violet" | "emerald" | "amber";
}) {
  const toneClasses: Record<string, string> = {
    violet: "border-violet-500/15 bg-violet-500/[0.06] text-violet-200",
    emerald: "border-emerald-500/15 bg-emerald-500/[0.06] text-emerald-200",
    amber: "border-amber-500/15 bg-amber-500/[0.06] text-amber-200",
  };
  return (
    <div className={`rounded-2xl border px-4 py-3 ${toneClasses[tone]}`}>
      <p className="text-2xl font-semibold text-white">{value}</p>
      <p className="mt-1 text-xs">{label}</p>
    </div>
  );
}
