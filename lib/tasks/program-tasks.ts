import type { DailyPlan, DayProgress } from "@/types";
import {
  applySectionDefaultsToDayProgress,
  getDaySectionAvailability,
} from "@/lib/day-section-defaults";
import { getAllPublishedPlans } from "@/lib/daily-plans";
import { canAccessDay } from "@/lib/premium-access";

export interface ProgramTask {
  id: string;
  day: number;
  label: string;
  type: "quiz" | "reading" | "revision";
  subject: "maths" | "english" | "reasoning" | "gk";
}

export function buildTaskId(
  day: number,
  subject: string,
  suffix: string
): string {
  return `d${day}_${subject}_${suffix}`;
}

/** All tasks across the published 75-day program. */
export function getProgramTaskCatalog(): ProgramTask[] {
  const tasks: ProgramTask[] = [];

  for (const plan of getAllPublishedPlans()) {
    plan.maths.forEach((m) => {
      tasks.push({
        id: buildTaskId(plan.day, "maths", m.topic),
        day: plan.day,
        label: `Maths: ${m.topic}`,
        type: "quiz",
        subject: "maths",
      });
    });

    tasks.push(
      {
        id: buildTaskId(plan.day, "english", "grammar"),
        day: plan.day,
        label: "English: Grammar",
        type: "reading",
        subject: "english",
      },
      {
        id: buildTaskId(plan.day, "english", "vocabulary"),
        day: plan.day,
        label: "English: Vocabulary",
        type: "reading",
        subject: "english",
      },
      {
        id: buildTaskId(plan.day, "english", "comprehension"),
        day: plan.day,
        label: "English: Comprehension",
        type: "reading",
        subject: "english",
      }
    );

    if (plan.reasoning) {
      tasks.push({
        id: buildTaskId(plan.day, "reasoning", plan.reasoning.topic),
        day: plan.day,
        label: `Reasoning: ${plan.reasoning.topic}`,
        type: "quiz",
        subject: "reasoning",
      });
    }

    tasks.push({
      id: buildTaskId(plan.day, "gk", "materials"),
      day: plan.day,
      label: "GK: Study materials",
      type: "reading",
      subject: "gk",
    });

    if (plan.day > 1) {
      tasks.push({
        id: buildTaskId(plan.day, "gk", "revision"),
        day: plan.day,
        label: "GK: Revision quiz",
        type: "revision",
        subject: "gk",
      });
    }
  }

  return tasks;
}

export function getTotalProgramTasks(): number {
  return getProgramTaskCatalog().length;
}

export function isTaskCompleted(
  dayProgress: DayProgress | null,
  task: ProgramTask
): boolean {
  if (!dayProgress) return false;

  const dp = applySectionDefaultsToDayProgress(task.day, dayProgress);
  const avail = getDaySectionAvailability(task.day);

  if (task.subject === "maths") {
    const slug = task.id.match(/d\d+_maths_(.+)/)?.[1];
    return Boolean(slug && dp.maths[slug]?.completed);
  }

  if (task.subject === "english") {
    if (task.id.endsWith("grammar")) {
      return !avail.grammar || dp.english.grammar;
    }
    if (task.id.endsWith("vocabulary")) {
      return !avail.vocabulary || dp.english.vocabulary;
    }
    if (task.id.endsWith("comprehension")) {
      return !avail.comprehension || dp.english.comprehension;
    }
  }

  if (task.subject === "reasoning") {
    return !avail.reasoning || dp.reasoning.completed;
  }

  if (task.subject === "gk") {
    if (task.id.endsWith("revision")) {
      return !avail.gkRevision || dp.gk.revisionQuizCompleted;
    }
    return !avail.gkMaterials || dp.gk.materialsCompleted;
  }

  return false;
}

export function getCompletedTasksForDay(
  plan: DailyPlan,
  dayProgress: DayProgress | null
): ProgramTask[] {
  const dayTasks = getProgramTaskCatalog().filter((t) => t.day === plan.day);
  return dayTasks.filter((t) => isTaskCompleted(dayProgress, t));
}

export function getDayTaskPercent(
  plan: DailyPlan,
  dayProgress: DayProgress | null
): number {
  const dayTasks = getProgramTaskCatalog().filter((t) => t.day === plan.day);
  if (dayTasks.length === 0) return 0;
  const done = dayTasks.filter((t) => isTaskCompleted(dayProgress, t)).length;
  return Math.round((done / dayTasks.length) * 100);
}

export function getOverallTaskProgress(
  dayProgressMap: Record<number, DayProgress | null>,
  userEmail?: string | null
): { completed: number; total: number; percent: number } {
  const catalog = getProgramTaskCatalog().filter((t) =>
    canAccessDay(t.day, userEmail)
  );
  const total = catalog.length;
  let completed = 0;
  for (const task of catalog) {
    const dp = dayProgressMap[task.day] ?? null;
    if (isTaskCompleted(dp, task)) completed++;
  }
  return {
    completed,
    total,
    percent: total > 0 ? Math.round((completed / total) * 100) : 0,
  };
}

export function getQuizTaskId(
  day: number,
  subject: string,
  topic: string
): string {
  return buildTaskId(day, subject, topic);
}
