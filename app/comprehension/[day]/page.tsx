"use client";

import { use, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  BookOpenText,
  CheckCircle2,
  RotateCcw,
  ScrollText,
  Shuffle,
  XCircle,
} from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { AppShell } from "@/components/layout/AppShell";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { canAccessDay } from "@/lib/premium-access";
import { markEnglishSection } from "@/lib/storage";
import {
  getComprehensionForDay,
  hasComprehensionForDay,
  scoreComprehension,
  type ComprehensionQuestion,
  type ScoreResult,
} from "@/lib/comprehension";

export default function ComprehensionPage({
  params,
}: {
  params: Promise<{ day: string }>;
}) {
  const { day: dayParam } = use(params);
  const dayNum = parseInt(dayParam, 10);
  const { studentId, progress, user } = useAuth();

  const set = useMemo(() => getComprehensionForDay(dayNum), [dayNum]);

  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<ScoreResult | null>(null);

  const DURATION = (set?.rc.questions.length ?? 5) <= 5 ? 5 * 60 : 20 * 60;
  const [timeLeft, setTimeLeft] = useState(DURATION);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (result !== null) {
      if (timerRef.current) clearInterval(timerRef.current);
      return;
    }
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current!);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result]);

  const timerExpired = timeLeft === 0 && result === null;
  useEffect(() => {
    if (timerExpired && set) {
      const score = scoreComprehension(set, answers);
      setResult(score);
      void markEnglishSection(studentId ?? "", dayNum, "comprehension");
      if (typeof window !== "undefined") window.scrollTo({ top: 0, behavior: "smooth" });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timerExpired]);

  const formatTime = (s: number) =>
    `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;

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

  if (!hasComprehensionForDay(dayNum) || !set) {
    return (
      <ProtectedRoute>
        <AppShell>
          <Card className="mx-auto max-w-lg border-white/10 bg-white/[0.03] p-8 text-center">
            <h1 className="text-xl font-semibold text-white">
              Day {dayNum} Comprehension
            </h1>
            <p className="mt-2 text-sm text-zinc-400">
              Comprehension practice for this day is being added.
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

  const submitted = result !== null;

  const select = (key: string, option: string) => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [key]: option }));
  };

  const handleSubmit = () => {
    const score = scoreComprehension(set, answers);
    setResult(score);
    void markEnglishSection(studentId, dayNum, "comprehension");
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleRetake = () => {
    setAnswers({});
    setResult(null);
  };

  const answeredCount = Object.keys(answers).length;

  return (
    <ProtectedRoute>
      <AppShell>
        <div className="mx-auto max-w-3xl space-y-6 animate-in pb-28">
          <header className="space-y-4">
            <Link
              href={`/day/${dayNum}`}
              className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground"
            >
              <ArrowLeft className="h-4 w-4" />
              Day {dayNum}
            </Link>
            <div className="flex items-start justify-between gap-4">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight text-white">
                  Day {dayNum} · Comprehension Practice
                </h1>
                <p className="mt-1 text-sm text-zinc-400">
                  {[
                    set.rc.questions.length > 0 && "Reading Comprehension",
                    set.cloze && "Cloze Test",
                    set.parajumble && "Para Jumbles",
                  ].filter(Boolean).join(" · ")}{" "}
                  · SSC marking +2 / −0.5 ·{" "}
                  {set.rc.questions.length +
                    (set.cloze?.questions.length ?? 0) +
                    (set.parajumble?.items.length ?? 0)}{" "}
                  questions
                </p>
              </div>
              {!result && (
                <div className={`shrink-0 rounded-lg px-4 py-2 text-lg font-mono font-bold tabular-nums ${
                  timeLeft <= 60 ? "bg-red-500/20 text-red-400" : "bg-white/5 text-white"
                }`}>
                  {formatTime(timeLeft)}
                </div>
              )}
            </div>
          </header>

          {submitted && result ? <ScoreCard result={result} /> : null}

          {/* Reading Comprehension */}
          <SectionHeading
            icon={<BookOpenText className="h-4 w-4" />}
            title={set.rc.title}
            directions={set.rc.directions}
          />
          <Card className="border-white/10 bg-white/[0.03] p-6">
            <p className="whitespace-pre-line text-[15px] leading-7 text-zinc-200">
              {set.rc.passage}
            </p>
          </Card>
          {set.rc.questions.map((q, i) => (
            <QuestionBlock
              key={`rc-${i}`}
              q={q}
              selected={answers[`rc-${i}`]}
              submitted={submitted}
              onSelect={(opt) => select(`rc-${i}`, opt)}
            />
          ))}

          {/* Cloze Test */}
          {set.cloze && (
            <>
              <SectionHeading
                icon={<ScrollText className="h-4 w-4" />}
                title={set.cloze.title}
                directions={set.cloze.directions}
              />
              <Card className="border-white/10 bg-white/[0.03] p-6">
                <p className="whitespace-pre-line text-[15px] leading-7 text-zinc-200">
                  {set.cloze.passage}
                </p>
              </Card>
              {set.cloze.questions.map((q, i) => (
                <QuestionBlock
                  key={`cloze-${i}`}
                  q={q}
                  selected={answers[`cloze-${i}`]}
                  submitted={submitted}
                  onSelect={(opt) => select(`cloze-${i}`, opt)}
                />
              ))}
            </>
          )}

          {/* Para Jumbles */}
          {set.parajumble && (
            <>
              <SectionHeading
                icon={<Shuffle className="h-4 w-4" />}
                title={set.parajumble.title}
                directions={set.parajumble.directions}
              />
              {set.parajumble.items.map((item, i) => (
            <div key={`pj-${i}`} className="space-y-3">
              <Card className="border-white/10 bg-white/[0.02] p-5">
                <p className="text-[11px] uppercase tracking-[0.2em] text-zinc-500">
                  Para Jumble {i + 1}
                </p>
                <div className="mt-3 space-y-1.5">
                  {item.parts.map((part) => (
                    <p key={part.label} className="text-sm text-zinc-200">
                      <span className="mr-2 inline-flex h-5 w-5 items-center justify-center rounded-md border border-violet-500/30 bg-violet-500/10 text-[11px] font-semibold text-violet-200">
                        {part.label}
                      </span>
                      {part.text}
                    </p>
                  ))}
                </div>
              </Card>
              <QuestionBlock
                q={{
                  question: "Select the correct sequence:",
                  options: item.options,
                  answer: item.answer,
                  explanation: item.explanation,
                }}
                selected={answers[`pj-${i}`]}
                submitted={submitted}
                onSelect={(opt) => select(`pj-${i}`, opt)}
              />
            </div>
          ))}
            </>
          )}

          <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
            {submitted ? (
              <>
                <Link href={`/day/${dayNum}`}>
                  <Button variant="secondary" className="w-full sm:w-auto">
                    <ArrowLeft className="h-4 w-4" />
                    Back to Day {dayNum}
                  </Button>
                </Link>
                <Button className="w-full sm:w-auto" onClick={handleRetake}>
                  <RotateCcw className="h-4 w-4" />
                  Practice again
                </Button>
              </>
            ) : (
              <Button
                size="lg"
                className="w-full sm:w-auto"
                onClick={handleSubmit}
              >
                Submit ({answeredCount}/{set.rc.questions.length +
                  (set.cloze?.questions.length ?? 0) +
                  (set.parajumble?.items.length ?? 0)}{" "}
                answered)
              </Button>
            )}
          </div>
        </div>
      </AppShell>
    </ProtectedRoute>
  );
}

function SectionHeading({
  icon,
  title,
  directions,
}: {
  icon: React.ReactNode;
  title: string;
  directions: string;
}) {
  return (
    <div className="pt-2">
      <div className="flex items-center gap-2 text-violet-200">
        <span className="inline-flex h-7 w-7 items-center justify-center rounded-lg border border-violet-500/25 bg-violet-500/10">
          {icon}
        </span>
        <h2 className="text-lg font-semibold text-white">{title}</h2>
      </div>
      <p className="mt-1.5 text-xs leading-5 text-zinc-500">{directions}</p>
    </div>
  );
}

function QuestionBlock({
  q,
  selected,
  submitted,
  onSelect,
}: {
  q: ComprehensionQuestion;
  selected?: string;
  submitted: boolean;
  onSelect: (option: string) => void;
}) {
  return (
    <Card className="border-white/10 bg-white/[0.03] p-5">
      <p className="text-sm font-medium leading-6 text-zinc-100">{q.question}</p>
      <div className="mt-3 space-y-2">
        {q.options.map((opt) => {
          const isSelected = selected === opt;
          const isCorrect = opt === q.answer;

          let cls =
            "border-white/10 bg-white/[0.02] text-zinc-300 hover:border-white/25";
          if (submitted) {
            if (isCorrect) {
              cls = "border-emerald-500/40 bg-emerald-500/10 text-emerald-100";
            } else if (isSelected) {
              cls = "border-rose-500/40 bg-rose-500/10 text-rose-100";
            } else {
              cls = "border-white/10 bg-white/[0.02] text-zinc-500";
            }
          } else if (isSelected) {
            cls = "border-violet-500/50 bg-violet-500/15 text-white";
          }

          return (
            <button
              key={opt}
              type="button"
              disabled={submitted}
              onClick={() => onSelect(opt)}
              className={`flex w-full items-center justify-between rounded-xl border px-4 py-2.5 text-left text-sm transition ${cls}`}
            >
              <span>{opt}</span>
              {submitted && isCorrect ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
              ) : submitted && isSelected ? (
                <XCircle className="h-4 w-4 shrink-0 text-rose-400" />
              ) : null}
            </button>
          );
        })}
      </div>
      {submitted && q.explanation ? (
        <div className="mt-3 rounded-xl border border-white/10 bg-white/[0.02] px-4 py-3">
          <p className="text-[11px] uppercase tracking-[0.2em] text-zinc-500">
            Explanation
          </p>
          <p className="mt-1 text-sm leading-6 text-zinc-300">{q.explanation}</p>
        </div>
      ) : null}
    </Card>
  );
}

function ScoreCard({ result }: { result: ScoreResult }) {
  return (
    <Card
      glow
      className="border-white/10 bg-[linear-gradient(180deg,rgba(124,58,237,0.10),rgba(255,255,255,0.02))] p-6"
    >
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
            Your score
          </p>
          <p className="mt-1 text-3xl font-semibold text-white">
            {result.marks} / {result.maxMarks}
          </p>
        </div>
        <p className="text-sm text-zinc-400">Accuracy {result.accuracy}%</p>
      </div>
      <div className="mt-5 grid grid-cols-3 gap-3">
        <Stat label="Correct" value={result.correct} tone="emerald" />
        <Stat label="Wrong" value={result.wrong} tone="rose" />
        <Stat label="Skipped" value={result.unattempted} tone="zinc" />
      </div>
      <p className="mt-4 text-xs text-zinc-500">
        Correct answers and explanations are shown below each question.
      </p>
    </Card>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "emerald" | "rose" | "zinc";
}) {
  const toneClasses: Record<string, string> = {
    emerald: "border-emerald-500/15 bg-emerald-500/[0.06] text-emerald-200",
    rose: "border-rose-500/15 bg-rose-500/[0.06] text-rose-200",
    zinc: "border-white/10 bg-white/[0.03] text-zinc-300",
  };
  return (
    <div className={`rounded-2xl border px-4 py-3 text-center ${toneClasses[tone]}`}>
      <p className="text-2xl font-semibold text-white">{value}</p>
      <p className="mt-1 text-xs">{label}</p>
    </div>
  );
}
