"use client";

import type { ComponentType } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  BarChart3,
  Circle,
  CheckCircle2,
  Clock3,
  Sparkles,
  Target,
  Trophy,
  XCircle,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { QuizRankingBanner } from "./QuizRankingBanner";
import { QuizStatsRings } from "./QuizStatsRings";
import { formatMarks } from "@/lib/quiz/scoring";
import type { Question, QuizRanking, QuizResult } from "@/types";

interface QuizResultScreenProps {
  title: string;
  result: QuizResult;
  ranking: QuizRanking | null;
  questions: Question[];
  answers: Record<string, string>;
  solutionsPath: string;
  analysisPath: string;
}

function formatTime(s: number) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}m ${sec}s`;
}

export function QuizResultScreen({
  title,
  result,
  ranking,
  questions,
  answers,
  solutionsPath,
  analysisPath,
}: QuizResultScreenProps) {
  const router = useRouter();
  const attempted = Object.keys(answers).length;
  const scoreLabel = `${formatMarks(result.score)} / ${result.maxScore}`;
  const strongestMetric =
    result.accuracy >= 75
      ? "Excellent accuracy"
      : result.accuracy >= 50
        ? "Solid attempt"
        : "Needs targeted revision";
  const completionRate =
    result.total > 0 ? Math.round((attempted / result.total) * 100) : 0;

  return (
    <div className="mx-auto max-w-5xl animate-in space-y-6 pb-10">
      <div className="relative overflow-hidden rounded-[28px] border border-white/10 bg-[radial-gradient(circle_at_top,_rgba(139,92,246,0.22),_transparent_45%),linear-gradient(180deg,rgba(18,18,24,0.96),rgba(10,10,15,0.96))] p-8 shadow-[0_30px_80px_rgba(0,0,0,0.35)] backdrop-blur-xl">
        <div className="absolute inset-0 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.03),transparent)] opacity-60" />
        <div className="relative grid gap-8 lg:grid-cols-[1.35fr_0.95fr]">
          <div className="space-y-5">
            <div className="inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-500/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-violet-200">
              <Sparkles className="h-3.5 w-3.5" />
              Official Attempt Submitted
            </div>
            <div>
              <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                {title}
              </h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400 sm:text-base">
                Your first attempt is now locked for ranking. Use the coaching
                review tools below to study solutions and inspect performance in
                detail.
              </p>
            </div>
            <div className="flex flex-wrap gap-3 text-xs text-zinc-300">
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5">
                {strongestMetric}
              </span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5">
                {questions.length} questions reviewed
              </span>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5">
                Ranking uses marks, then faster finish time
              </span>
            </div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <Button
                className="w-full justify-between rounded-2xl px-5 py-4 text-left"
                onClick={() => router.push(solutionsPath)}
              >
                <span className="flex items-center gap-3">
                  <CheckCircle2 className="h-5 w-5" />
                  <span className="flex flex-col items-start">
                    <span>View Solutions</span>
                    <span className="text-xs font-normal text-white/70">
                      Question-wise coaching review
                    </span>
                  </span>
                </span>
                <ArrowRight className="h-4 w-4" />
              </Button>
              <Button
                className="w-full justify-between rounded-2xl border-white/10 px-5 py-4 text-left"
                variant="secondary"
                onClick={() => router.push(analysisPath)}
              >
                <span className="flex items-center gap-3">
                  <BarChart3 className="h-5 w-5" />
                  <span className="flex flex-col items-start">
                    <span>Analysis</span>
                    <span className="text-xs font-normal text-zinc-400">
                      Premium performance dashboard
                    </span>
                  </span>
                </span>
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="rounded-[24px] border border-white/10 bg-black/25 p-6 backdrop-blur-md">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-zinc-500">
                  Final Score
                </p>
                <p className="mt-3 text-4xl font-bold tabular-nums text-white">
                  {scoreLabel}
                </p>
                <p className="mt-2 text-sm text-zinc-400">
                  +2 per correct · -0.5 per wrong · unattempted = 0
                </p>
              </div>
              <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 px-4 py-3 text-right">
                <p className="text-xs uppercase tracking-[0.2em] text-emerald-300">
                  Accuracy
                </p>
                <p className="mt-1 text-2xl font-semibold tabular-nums text-emerald-300">
                  {result.accuracy}%
                </p>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-3">
              <QuickMetric
                icon={Trophy}
                label="Rank"
                value={
                  ranking?.rank != null
                    ? `${ranking.rank} / ${ranking.totalParticipants}`
                    : "Pending"
                }
                tone="amber"
              />
              <QuickMetric
                icon={Target}
                label="Attempted"
                value={`${attempted} / ${result.total}`}
                tone="violet"
              />
              <QuickMetric
                icon={Clock3}
                label="Time Taken"
                value={formatTime(result.timeTakenSeconds)}
                tone="sky"
              />
              <QuickMetric
                icon={Circle}
                label="Completion"
                value={`${completionRate}%`}
                tone="emerald"
              />
            </div>
          </div>
        </div>
      </div>

      {ranking ? <QuizRankingBanner ranking={ranking} /> : null}

      <div className="rounded-[24px] border border-white/10 bg-white/[0.035] p-6 backdrop-blur-sm">
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-[0.22em] text-zinc-400">
              Performance Overview
            </h3>
            <p className="mt-1 text-sm text-zinc-500">
              Snapshot of your final official attempt
            </p>
          </div>
        </div>
        <QuizStatsRings
          accuracy={result.accuracy}
          attempted={attempted}
          total={result.total}
          percentile={ranking?.percentile ?? null}
        />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatBox
          icon={CheckCircle2}
          label="Correct"
          value={result.correct}
          color="text-emerald-400"
        />
        <StatBox
          icon={XCircle}
          label="Wrong"
          value={result.wrong}
          color="text-red-400"
        />
        <StatBox
          icon={Target}
          label="Marks %"
          value={`${result.accuracy}%`}
          color="text-violet-400"
        />
        <StatBox
          icon={Clock3}
          label="Time"
          value={formatTime(result.timeTakenSeconds)}
          color="text-zinc-300"
        />
      </div>
    </div>
  );
}

function QuickMetric({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: ComponentType<{ className?: string }>;
  label: string;
  value: string;
  tone: "amber" | "emerald" | "sky" | "violet";
}) {
  const tones = {
    amber: "border-amber-400/15 bg-amber-500/10 text-amber-300",
    emerald: "border-emerald-400/15 bg-emerald-500/10 text-emerald-300",
    sky: "border-sky-400/15 bg-sky-500/10 text-sky-300",
    violet: "border-violet-400/15 bg-violet-500/10 text-violet-300",
  };

  return (
    <div className={`rounded-2xl border p-4 ${tones[tone]}`}>
      <div className="flex items-center gap-2">
        <Icon className="h-4 w-4" />
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em]">
          {label}
        </p>
      </div>
      <p className="mt-3 text-xl font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}

function StatBox({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: ComponentType<{ className?: string }>;
  label: string;
  value: string | number;
  color: string;
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#121218] p-4 text-center">
      <Icon className={`h-5 w-5 mx-auto mb-2 ${color}`} />
      <p className={`text-xl font-semibold tabular-nums ${color}`}>{value}</p>
      <p className="text-xs text-zinc-500 mt-0.5">{label}</p>
    </div>
  );
}
