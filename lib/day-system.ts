import type { DailyPlan, DayProgress, PendingTask, StudentProgress } from "@/types";
import { canAccessDay, FREE_ACCESS_DAYS, isPremiumEmail } from "@/lib/premium-access";
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

  // Premium users bypass sequential unlock — all published days are open.
  if (isPremiumEmail(userEmail)) {
    return {
      status: "available",
      canAccess: true,
      requiresOverride: false,
    };
  }

  if (day > progress.unlockedDay + 1) {
    return {
      status: "locked_future",
      canAccess: false,
      requiresOverride: false,
      message: `Complete Day ${progress.unlockedDay} to unlock Day ${progress.unlockedDay + 1} first`,
    };
  }

  if (day === progress.unlockedDay + 1) {
    const prevComplete = isDayFullyComplete(previousDayProgress);
    if (!prevComplete) {
      return {
        status: "locked_sequential",
        canAccess: true,
        requiresOverride: true,
        message: `Complete Day ${day - 1} or use override to open Day ${day} only`,
      };
    }
    return {
      status: "available",
      canAccess: true,
      requiresOverride: false,
    };
  }

  return {
    status: "available",
    canAccess: true,
    requiresOverride: false,
  };
}

export function isDayFullyComplete(dayProgress: DayProgress | null): boolean {
  if (!dayProgress) return false;
  if (dayProgress.completed) return true;

  const englishDone =
    dayProgress.english.grammar &&
    dayProgress.english.vocabulary &&
    dayProgress.english.comprehension;

  const reasoningDone = dayProgress.reasoning.completed;
  const gkDone =
    dayProgress.gk.materialsCompleted &&
    (dayProgress.day === 1 || dayProgress.gk.revisionQuizCompleted);

  const mathsTopics = Object.values(dayProgress.maths);
  const mathsDone =
    mathsTopics.length > 0 && mathsTopics.every((t) => t.completed);

  return englishDone && reasoningDone && gkDone && mathsDone;
}

export function getDayCompletionPercent(
  dayProgress: DayProgress | null,
  plan: DailyPlan | null
): number {
  if (!dayProgress || !plan) return 0;
  if (dayProgress.completed) return 100;

  let total = 0;
  let done = 0;

  plan.maths.forEach((m) => {
    total++;
    if (dayProgress.maths[m.topic]?.completed) done++;
  });

  total += 3;
  if (dayProgress.english.grammar) done++;
  if (dayProgress.english.vocabulary) done++;
  if (dayProgress.english.comprehension) done++;

  total += 1;
  if (dayProgress.reasoning.completed) done++;

  total += dayProgress.day === 1 ? 1 : 2;
  if (dayProgress.gk.materialsCompleted) done++;
  if (dayProgress.day > 1 && dayProgress.gk.revisionQuizCompleted) done++;

  return total > 0 ? Math.round((done / total) * 100) : 0;
}

export function getPendingTasks(
  dayProgress: DayProgress | null,
  plan: DailyPlan | null
): PendingTask[] {
  if (!plan) return [];
  const tasks: PendingTask[] = [];
  const day = plan.day;

  plan.maths.forEach((m) => {
    if (!dayProgress?.maths[m.topic]?.completed) {
      tasks.push({
        id: `maths-${m.topic}`,
        day,
        subject: "maths",
        label: `Maths: ${formatTopic(m.topic)}`,
        type: "quiz",
      });
    }
  });

  if (!dayProgress?.english.grammar) {
    tasks.push({
      id: "english-grammar",
      day,
      subject: "english",
      label: "English: Grammar",
      type: "reading",
    });
  }
  if (!dayProgress?.english.vocabulary) {
    tasks.push({
      id: "english-vocab",
      day,
      subject: "english",
      label: "English: Vocabulary",
      type: "reading",
    });
  }
  if (!dayProgress?.english.comprehension) {
    tasks.push({
      id: "english-comp",
      day,
      subject: "english",
      label: "English: Comprehension",
      type: "reading",
    });
  }

  if (plan.reasoning && !dayProgress?.reasoning.completed) {
    tasks.push({
      id: "reasoning-quiz",
      day,
      subject: "reasoning",
      label: `Reasoning: ${formatTopic(plan.reasoning.topic)}`,
      type: "quiz",
    });
  }

  if (!dayProgress?.gk.materialsCompleted) {
    tasks.push({
      id: "gk-materials",
      day,
      subject: "gk",
      label: "GK: Study today's topics",
      type: "reading",
    });
  }
  if (day > 1 && !dayProgress?.gk.revisionQuizCompleted) {
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
    } else if (d > progress.unlockedDay) {
      days.push({ day: d, status: "locked" });
    } else {
      days.push({ day: d, status: "available" });
    }
  }

  return days;
}
