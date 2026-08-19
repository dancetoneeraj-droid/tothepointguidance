"use client";

import { use, useMemo, type ComponentType } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  Clock3,
  Gauge,
  Target,
  Trophy,
  XCircle,
} from "lucide-react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { QuizRankingBanner } from "@/components/quiz/QuizRankingBanner";
import { QuizStatsRings } from "@/components/quiz/QuizStatsRings";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { loadQuizAnalytics } from "@/lib/api/ecosystem";
import { formatMarks } from "@/lib/quiz/scoring";
import { getReviewQuestions, getReviewStatus } from "@/lib/quiz/review";
import { getQuestionBank } from "@/lib/quiz-loader";
import { canAccessDay, resolveStudentEmail } from "@/lib/premium-access";
import {
  formatEnglishGrammarQuizLabel,
  formatQuizTitle,
  formatReasoningQuizLabel,
  formatTopic,
  getReasoningQuizLabel,
  resolveScheduledQuizFrom,
} from "@/lib/day-system";
import { getDailyPlan } from "@/lib/daily-plans";
import { useAuth } from "@/components/providers/AuthProvider";
import { getQuizReviewRecord } from "@/lib/storage";

export default function QuizAnalysisPage({
  params,
}: {
  params: Promise<{ subject: string; topic: string }>;
}) {
  const { subject, topic } = use(params);
  const searchParams = useSearchParams();
  const day = parseInt(searchParams.get("day") ?? "1", 10);
  const fromRaw = searchParams.get("from");
  const fromParam =
    fromRaw != null && fromRaw !== "" ? parseInt(fromRaw, 10) : undefined;
  const { studentId, user, progress } = useAuth();

  const data = useMemo(() => {
    if (!studentId) return null;

    const plan = getDailyPlan(day);
    const quizFrom = resolveScheduledQuizFrom(
      plan,
      subject,
      topic,
      fromParam !== undefined && Number.isFinite(fromParam) ? fromParam : undefined
    );

    const saved =
      getQuizReviewRecord(studentId, day, subject, topic, quizFrom) ??
      (quizFrom !== undefined
        ? getQuizReviewRecord(studentId, day, subject, topic)
        : null);
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
  }, [studentId, day, subject, topic, fromParam]);

  if (!canAccessDay(day, resolveStudentEmail(user?.email, progress?.email))) {
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
            <p className="text-white font-medium">No analysis data found</p>
            <p className="text-sm text-muted mt-2">
              Complete a quiz first to view detailed analysis.
            </p>
            <Link href={`/day/${day}`} className="inline-block mt-6">
              <Button>Back to Day {day}</Button>
            </Link>
          </Card>
        </div>
      </ProtectedRoute>
    );
  }

  const reviewQuestions = getReviewQuestions(
    getQuestionBank(subject as "maths" | "reasoning" | "gk", topic),
    data.questionIds
  );
  const attempted = Object.keys(data.answers).length;
  const correctCount = reviewQuestions.filter(
    (question) => getReviewStatus(question, data.answers) === "correct"
  ).length;
  const wrongCount = reviewQuestions.filter(
    (question) => getReviewStatus(question, data.answers) === "wrong"
  ).length;
  const unattemptedCount = reviewQuestions.length - correctCount - wrongCount;
  const averageSecondsPerQuestion =
    reviewQuestions.length > 0
      ? Math.round(data.result.timeTakenSeconds / reviewQuestions.length)
      : 0;
  const questionsPerMinute =
    data.result.timeTakenSeconds > 0
      ? Number(((attempted * 60) / data.result.timeTakenSeconds).toFixed(1))
      : 0;
  const attemptRate =
    data.result.total > 0 ? Math.round((attempted / data.result.total) * 100) : 0;
  const precision =
    attempted > 0 ? Math.round((correctCount / attempted) * 100) : 0;
  const speedScore = Math.max(
    0,
    Math.min(100, 100 - Math.round((averageSecondsPerQuestion / 90) * 100))
  );
  const plan = getDailyPlan(day);
  const title = formatQuizTitle(subject, topic, day, {
    englishLabel: plan?.english.grammarQuizLabel,
    reasoningLabel: getReasoningQuizLabel(plan, topic),
  });
  const topicLabel =
    subject === "english"
      ? formatEnglishGrammarQuizLabel(plan?.english.grammarQuizLabel)
      : subject === "reasoning"
        ? formatReasoningQuizLabel(topic, getReasoningQuizLabel(plan, topic))
        : formatTopic(topic);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#08080a] px-4 sm:px-6 py-8">
        <div className="mx-auto max-w-6xl space-y-6">
          <Link
            href={`/quiz/${subject}/${topic}?day=${day}${
              fromParam !== undefined && Number.isFinite(fromParam)
                ? `&from=${fromParam}`
                : ""
            }`}
            className="inline-flex items-center gap-1 text-sm text-zinc-500 hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to result
          </Link>

          <header className="overflow-hidden rounded-[28px] border border-white/10 bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.16),_transparent_45%),linear-gradient(180deg,rgba(18,18,24,0.96),rgba(10,10,15,0.96))] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.32)]">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-violet-300">
              Premium Analysis
            </p>
            <div className="mt-3 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h1 className="text-3xl font-semibold tracking-tight text-white">
                  {title}
                </h1>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-400">
                  A detailed breakdown of your official first attempt with
                  ranking, accuracy, speed, and answer-quality insights.
                </p>
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                <MiniKpi
                  label="Rank"
                  value={
                    data.ranking?.rank != null
                      ? `${data.ranking.rank}/${data.ranking.totalParticipants}`
                      : "Pending"
                  }
                />
                <MiniKpi label="Score" value={formatMarks(data.result.score)} />
                <MiniKpi label="Accuracy" value={`${data.result.accuracy}%`} />
                <MiniKpi
                  label="Percentile"
                  value={
                    data.ranking?.percentile != null
                      ? `${data.ranking.percentile}%`
                      : "—"
                  }
                />
              </div>
            </div>
          </header>

          {data.ranking ? <QuizRankingBanner ranking={data.ranking} /> : null}

          <section className="space-y-4">
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-[0.24em] text-zinc-400">
                Overall Performance
              </h2>
              <p className="mt-1 text-sm text-zinc-500">
                First-attempt metrics used for leaderboard ranking
              </p>
            </div>

            <Card className="border-white/10 bg-[#121218]/90 p-6">
              <h3 className="mb-4 flex items-center gap-2 text-sm font-semibold text-white">
                <Trophy className="h-4 w-4 text-violet-400" />
                Performance Rings
              </h3>
              <QuizStatsRings
                accuracy={data.result.accuracy}
                attempted={attempted}
                total={data.result.total}
                percentile={data.ranking?.percentile ?? null}
              />
            </Card>

            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <MetricCard
                icon={Trophy}
                label="Rank"
                value={
                  data.ranking?.rank != null
                    ? `${data.ranking.rank} / ${data.ranking.totalParticipants}`
                    : "Pending"
                }
                accent="amber"
              />
              <MetricCard
                icon={Target}
                label="Total Score"
                value={`${formatMarks(data.result.score)} / ${data.result.maxScore}`}
                accent="violet"
              />
              <MetricCard
                icon={CheckCircle2}
                label="Correct Questions"
                value={correctCount}
                accent="emerald"
              />
              <MetricCard
                icon={XCircle}
                label="Wrong Questions"
                value={wrongCount}
                accent="rose"
              />
              <MetricCard
                icon={Circle}
                label="Unattempted"
                value={unattemptedCount}
                accent="slate"
              />
              <MetricCard
                icon={Gauge}
                label="Accuracy %"
                value={`${data.result.accuracy}%`}
                accent="sky"
              />
              <MetricCard
                icon={Clock3}
                label="Time Taken"
                value={`${Math.floor(data.result.timeTakenSeconds / 60)}m ${data.result.timeTakenSeconds % 60}s`}
                accent="slate"
              />
              <MetricCard
                icon={Trophy}
                label="Percentile"
                value={
                  data.ranking?.percentile != null
                    ? `${data.ranking.percentile}%`
                    : "—"
                }
                accent="amber"
              />
            </div>
          </section>

          <section className="space-y-4">
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-[0.24em] text-zinc-400">
                Visual Analysis
              </h2>
              <p className="mt-1 text-sm text-zinc-500">
                Coaching-style breakdown for score quality, attempt quality, and pace
              </p>
            </div>

            <div className="grid gap-4 xl:grid-cols-2">
              <Card className="border-white/10 bg-[#121218]/90 p-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <h3 className="text-base font-semibold text-white">
                      Correct vs Wrong
                    </h3>
                    <p className="mt-1 text-sm text-zinc-500">
                      Distribution of your official paper outcome
                    </p>
                  </div>
                  <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-zinc-300">
                    {reviewQuestions.length} questions
                  </span>
                </div>
                <SegmentBar
                  className="mt-5"
                  segments={[
                    {
                      value: correctCount,
                      color: "bg-emerald-400",
                      label: "Correct",
                    },
                    { value: wrongCount, color: "bg-rose-400", label: "Wrong" },
                    {
                      value: unattemptedCount,
                      color: "bg-zinc-500",
                      label: "Unattempted",
                    },
                  ]}
                />
                <div className="mt-5 grid grid-cols-3 gap-3 text-sm">
                  <LegendChip label="Correct" value={correctCount} tone="emerald" />
                  <LegendChip label="Wrong" value={wrongCount} tone="rose" />
                  <LegendChip
                    label="Unattempted"
                    value={unattemptedCount}
                    tone="slate"
                  />
                </div>
              </Card>

              <Card className="border-white/10 bg-[#121218]/90 p-6">
                <div>
                  <h3 className="text-base font-semibold text-white">
                    Accuracy Progress
                  </h3>
                  <p className="mt-1 text-sm text-zinc-500">
                    Overall hit rate and answer precision
                  </p>
                </div>
                <ProgressRow
                  className="mt-5"
                  label="Overall Accuracy"
                  value={`${data.result.accuracy}%`}
                  percent={data.result.accuracy}
                  color="bg-violet-400"
                />
                <ProgressRow
                  className="mt-4"
                  label="Attempt Rate"
                  value={`${attemptRate}%`}
                  percent={attemptRate}
                  color="bg-sky-400"
                />
                <ProgressRow
                  className="mt-4"
                  label="Attempt Precision"
                  value={`${precision}%`}
                  percent={precision}
                  color="bg-emerald-400"
                />
              </Card>

              <Card className="border-white/10 bg-[#121218]/90 p-6">
                <div>
                  <h3 className="text-base font-semibold text-white">
                    Speed Analysis
                  </h3>
                  <p className="mt-1 text-sm text-zinc-500">
                    Review your pace against a serious test-taking rhythm
                  </p>
                </div>
                <div className="mt-5 grid gap-4 sm:grid-cols-3">
                  <SpeedStat
                    label="Avg / Question"
                    value={`${averageSecondsPerQuestion}s`}
                  />
                  <SpeedStat
                    label="Questions / Min"
                    value={`${questionsPerMinute}`}
                  />
                  <SpeedStat
                    label="Speed Score"
                    value={`${speedScore}%`}
                  />
                </div>
                <ProgressRow
                  className="mt-5"
                  label="Pace Efficiency"
                  value={`${speedScore}%`}
                  percent={speedScore}
                  color="bg-amber-400"
                />
              </Card>

              <Card className="border-white/10 bg-[#121218]/90 p-6">
                <div>
                  <h3 className="text-base font-semibold text-white">
                    Subject Performance
                  </h3>
                  <p className="mt-1 text-sm text-zinc-500">
                    Topic-wise snapshot for this quiz set
                  </p>
                </div>
                <div className="mt-5 rounded-2xl border border-white/10 bg-white/[0.03] p-5">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-violet-300">
                        {subject === "gk"
                          ? "General Knowledge"
                          : subject === "english"
                            ? "English"
                          : subject === "reasoning"
                            ? "Reasoning"
                            : "Mathematics"}
                      </p>
                      <p className="mt-2 text-xl font-semibold text-white">
                        {topicLabel}
                      </p>
                    </div>
                    <div className="rounded-2xl border border-violet-400/20 bg-violet-500/10 px-4 py-3 text-right">
                      <p className="text-xs uppercase tracking-[0.18em] text-violet-300">
                        Marks
                      </p>
                      <p className="mt-1 text-2xl font-semibold tabular-nums text-white">
                        {formatMarks(data.result.score)}
                      </p>
                    </div>
                  </div>
                  <div className="mt-5 grid gap-3 sm:grid-cols-3">
                    <SubjectChip
                      label="Accuracy"
                      value={`${data.result.accuracy}%`}
                    />
                    <SubjectChip label="Attempt Rate" value={`${attemptRate}%`} />
                    <SubjectChip label="Precision" value={`${precision}%`} />
                  </div>
                </div>
              </Card>
            </div>
          </section>
        </div>
      </div>
    </ProtectedRoute>
  );
}

function MiniKpi({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-zinc-500">
        {label}
      </p>
      <p className="mt-1 text-lg font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}

function MetricCard({
  icon: Icon,
  label,
  value,
  accent,
}: {
  icon: ComponentType<{ className?: string }>;
  label: string;
  value: string | number;
  accent: "amber" | "emerald" | "rose" | "sky" | "slate" | "violet";
}) {
  const accents = {
    amber: "bg-amber-500/10 text-amber-300 border-amber-400/15",
    emerald: "bg-emerald-500/10 text-emerald-300 border-emerald-400/15",
    rose: "bg-rose-500/10 text-rose-300 border-rose-400/15",
    sky: "bg-sky-500/10 text-sky-300 border-sky-400/15",
    slate: "bg-zinc-500/10 text-zinc-300 border-zinc-400/15",
    violet: "bg-violet-500/10 text-violet-300 border-violet-400/15",
  };

  return (
    <Card className={`border p-5 ${accents[accent]}`}>
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
            {label}
          </p>
          <p className="mt-3 text-2xl font-semibold tabular-nums text-white">
            {value}
          </p>
        </div>
        <div className="rounded-xl border border-current/15 bg-black/10 p-2.5">
          <Icon className="h-4 w-4" />
        </div>
      </div>
    </Card>
  );
}

function SegmentBar({
  segments,
  className = "",
}: {
  segments: Array<{ value: number; color: string; label: string }>;
  className?: string;
}) {
  const total = segments.reduce((sum, segment) => sum + segment.value, 0);

  return (
    <div className={`overflow-hidden rounded-full bg-white/5 ${className}`}>
      <div className="flex h-4 w-full">
        {segments.map((segment) => {
          const width = total > 0 ? `${(segment.value / total) * 100}%` : "0%";
          return (
            <div
              key={segment.label}
              className={segment.color}
              style={{ width }}
              title={`${segment.label}: ${segment.value}`}
            />
          );
        })}
      </div>
    </div>
  );
}

function LegendChip({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "emerald" | "rose" | "slate";
}) {
  const tones = {
    emerald: "border-emerald-400/15 bg-emerald-500/10 text-emerald-300",
    rose: "border-rose-400/15 bg-rose-500/10 text-rose-300",
    slate: "border-zinc-400/15 bg-zinc-500/10 text-zinc-300",
  };

  return (
    <div className={`rounded-2xl border px-4 py-3 ${tones[tone]}`}>
      <p className="text-xs font-semibold uppercase tracking-[0.18em]">{label}</p>
      <p className="mt-1 text-lg font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}

function ProgressRow({
  label,
  value,
  percent,
  color,
  className = "",
}: {
  label: string;
  value: string;
  percent: number;
  color: string;
  className?: string;
}) {
  const safePercent = Math.max(0, Math.min(100, percent));

  return (
    <div className={className}>
      <div className="mb-2 flex items-center justify-between gap-3 text-sm">
        <span className="text-zinc-300">{label}</span>
        <span className="font-medium tabular-nums text-white">{value}</span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-white/5">
        <div
          className={`h-full rounded-full ${color} transition-all duration-500`}
          style={{ width: `${safePercent}%` }}
        />
      </div>
    </div>
  );
}

function SpeedStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
        {label}
      </p>
      <p className="mt-2 text-2xl font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}

function SubjectChip({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">
        {label}
      </p>
      <p className="mt-1 text-lg font-semibold tabular-nums text-white">{value}</p>
    </div>
  );
}
