import type { DailyPlan, DayProgress, PendingTask, StudentProgress } from "@/types";
import {
  applySectionDefaultsToDayProgress,
  getDaySectionAvailability,
} from "@/lib/day-section-defaults";
import { canAccessDay, FREE_ACCESS_DAYS } from "@/lib/premium-access";
import { getDailyPlan, isDayPublished, MAX_PUBLISHED_DAY } from "./daily-plans";
import { formatMathsTopic, getMathsTopic } from "./maths-topics";

export type DayAccessStatus =
  | "available"
  | "locked_future"
  | "locked_sequential"
  | "premium_locked"
  | "coming_soon";

export interface DayAccessResult {
  status: DayAccessStatus;
  canAccess: boolean;
  requiresOverride: boolean;
  message?: string;
}

export function getDayAccess(
  day: number,
  progress: StudentProgress,
  previousDayProgress: DayProgress | null,
  options?: { userEmail?: string | null }
): DayAccessResult {
  const userEmail = options?.userEmail ?? progress.email;

  if (!canAccessDay(day, userEmail)) {
    return {
      status: "premium_locked",
      canAccess: false,
      requiresOverride: false,
      message: "Premium content locked.",
    };
  }

  if (!isDayPublished(day)) {
    return {
      status: "coming_soon",
      canAccess: false,
      requiresOverride: false,
      message: "Coming Soon",
    };
  }

  if (day <= FREE_ACCESS_DAYS) {
    return {
      status: "available",
      canAccess: true,
      requiresOverride: false,
    };
  }

  // Signed-in users can open any published day. Pacing is controlled by
  // publish flags in the schedule, not by a sequential unlock cursor.
  return {
    status: "available",
    canAccess: true,
    requiresOverride: false,
  };
}

export function isDayFullyComplete(dayProgress: DayProgress | null): boolean {
  if (!dayProgress) return false;
  if (dayProgress.completed) return true;
  const plan = getDailyPlan(dayProgress.day);
  if (!plan) return false;
  return getDayCompletionPercent(dayProgress, plan) === 100;
}

export function getDayCompletionPercent(
  dayProgress: DayProgress | null,
  plan: DailyPlan | null
): number {
  if (!dayProgress || !plan) return 0;
  if (dayProgress.completed) return 100;

  const dp = applySectionDefaultsToDayProgress(plan.day, dayProgress);
  const avail = getDaySectionAvailability(plan.day);

  let total = 0;
  let done = 0;

  plan.maths.forEach((m) => {
    total++;
    if (dp.maths[m.topic]?.completed) done++;
  });

  if (avail.grammar) {
    total++;
    if (dp.english.grammar) done++;
  }
  if (avail.vocabulary) {
    total++;
    if (dp.english.vocabulary) done++;
  }
  if (avail.comprehension) {
    total++;
    if (dp.english.comprehension) done++;
  }

  if (avail.reasoning) {
    total++;
    if (dp.reasoning.completed) done++;
  }

  if (avail.gkMaterials) {
    total++;
    if (dp.gk.materialsCompleted) done++;
  }
  if (avail.gkRevision) {
    total++;
    if (dp.gk.revisionQuizCompleted) done++;
  }

  return total > 0 ? Math.round((done / total) * 100) : 0;
}

export function getPendingTasks(
  dayProgress: DayProgress | null,
  plan: DailyPlan | null
): PendingTask[] {
  if (!plan) return [];
  const tasks: PendingTask[] = [];
  const day = plan.day;
  const dp = dayProgress
    ? applySectionDefaultsToDayProgress(day, dayProgress)
    : null;
  const avail = getDaySectionAvailability(day);

  plan.maths.forEach((m) => {
    if (!dp?.maths[m.topic]?.completed) {
      tasks.push({
        id: `maths-${m.topic}`,
        day,
        subject: "maths",
        label: `Maths: ${formatTopic(m.topic)}`,
        type: "quiz",
      });
    }
  });

  if (avail.grammar && !dp?.english.grammar) {
    tasks.push({
      id: "english-grammar",
      day,
      subject: "english",
      label: "English: Grammar",
      type: "reading",
    });
  }
  if (avail.vocabulary && !dp?.english.vocabulary) {
    tasks.push({
      id: "english-vocab",
      day,
      subject: "english",
      label: "English: Vocabulary",
      type: "reading",
    });
  }
  if (avail.comprehension && !dp?.english.comprehension) {
    tasks.push({
      id: "english-comp",
      day,
      subject: "english",
      label: "English: Comprehension",
      type: "reading",
    });
  }

  if (avail.reasoning && !dp?.reasoning.completed) {
    tasks.push({
      id: "reasoning-quiz",
      day,
      subject: "reasoning",
      label: `Reasoning: ${formatTopic(plan.reasoning!.topic)}`,
      type: "quiz",
    });
  }

  if (avail.gkMaterials && !dp?.gk.materialsCompleted) {
    tasks.push({
      id: "gk-materials",
      day,
      subject: "gk",
      label: "GK: Study today's topics",
      type: "reading",
    });
  }
  if (avail.gkRevision && !dp?.gk.revisionQuizCompleted) {
    tasks.push({
      id: "gk-revision",
      day,
      subject: "gk",
      label: "GK: Revision quiz",
      type: "revision",
    });
  }

  return tasks;
}

export function formatTopic(topic: string): string {
  return getMathsTopic(topic)?.label ?? topic
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

/** English grammar quizzes may use a shared bank slug (e.g. pronoun); show a friendly label instead. */
export function formatEnglishGrammarQuizLabel(customLabel?: string): string {
  return customLabel?.trim() || "Grammar";
}

export function formatReasoningQuizLabel(
  topic: string,
  customLabel?: string
): string {
  return customLabel?.trim() || formatTopic(topic);
}

export function getReasoningQuizLabel(
  plan: DailyPlan | null | undefined,
  topic: string
): string | undefined {
  if (!plan) return undefined;
  const extra = plan.reasoningQuizzes?.find((q) => q.topic === topic);
  if (extra?.label) return extra.label;
  if (plan.reasoning?.topic === topic) return plan.reasoning.label;
  return undefined;
}

export function getEnglishQuizLabel(
  plan: DailyPlan | null | undefined,
  topic: string,
  from?: number
): string | undefined {
  if (!plan) return undefined;
  const quizzes = plan.english.grammarQuizzes ?? [];
  if (from !== undefined) {
    const match = quizzes.find((q) => q.topic === topic && q.from === from);
    if (match?.label) return match.label;
  }
  const byTopic = quizzes.find((q) => q.topic === topic);
  if (byTopic?.label) return byTopic.label;
  if (plan.english.grammarQuiz === topic) {
    return plan.english.grammarQuizLabel;
  }
  return undefined;
}

/**
 * Resolve the bank `from` offset for a scheduled quiz on a day.
 * Used so solutions/analysis can load review records saved as `dayN-subject-topic-f{from}`.
 */
export function resolveScheduledQuizFrom(
  plan: DailyPlan | null | undefined,
  subject: string,
  topic: string,
  fromParam?: number
): number | undefined {
  if (fromParam !== undefined && Number.isFinite(fromParam)) return fromParam;
  if (!plan) return undefined;

  if (subject === "maths") {
    return plan.maths.find((m) => m.topic === topic)?.from;
  }
  if (subject === "reasoning") {
    if (plan.reasoning?.topic === topic) return plan.reasoning.from;
    return plan.reasoningQuizzes?.find((q) => q.topic === topic)?.from;
  }
  if (subject === "english") {
    const quizzes = (plan.english.grammarQuizzes ?? []).filter(
      (q) => q.topic === topic
    );
    if (quizzes.length === 1) return quizzes[0].from;
    if (plan.english.grammarQuiz === topic) return plan.english.grammarQuizFrom;
    return undefined;
  }
  if (subject === "gk") {
    return plan.gk.from;
  }
  return undefined;
}

export function formatQuizTitle(
  subject: string,
  topic: string,
  day: number,
  options?: { englishLabel?: string; reasoningLabel?: string }
): string {
  const name =
    subject === "english"
      ? formatEnglishGrammarQuizLabel(options?.englishLabel)
      : subject === "reasoning"
        ? formatReasoningQuizLabel(topic, options?.reasoningLabel)
        : formatTopic(topic);
  return `${name} — Day ${day}`;
}

export { formatMathsTopic };

export function getLockedDaysPreview(
  progress: StudentProgress,
  options?: { userEmail?: string | null }
): { day: number; status: "locked" | "coming_soon" | "available" | "premium" }[] {
  const days: {
    day: number;
    status: "locked" | "coming_soon" | "available" | "premium";
  }[] = [];

  const userEmail = options?.userEmail ?? progress.email;

  for (let d = 1; d <= MAX_PUBLISHED_DAY + 2; d++) {
    if (!isDayPublished(d)) {
      days.push({ day: d, status: "coming_soon" });
    } else if (!canAccessDay(d, userEmail)) {
      days.push({ day: d, status: "premium" });
    } else {
      days.push({ day: d, status: "available" });
    }
  }

  return days;
}
