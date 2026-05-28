import type { DayProgress } from "@/types";
import { getAllPublishedPlans } from "@/lib/daily-plans";
import { canAccessDay } from "@/lib/premium-access";
import { loadStore } from "@/lib/storage/client";
import {
  getProgramTaskCatalog,
  isTaskCompleted,
  type ProgramTask,
} from "@/lib/tasks/program-tasks";

export function collectDayProgressMap(
  studentId: string
): Record<number, DayProgress | null> {
  const store = loadStore(studentId);
  const map: Record<number, DayProgress | null> = {};
  if (!store) return map;
  for (const [key, dp] of Object.entries(store.dayProgress)) {
    map[Number(key)] = dp;
  }
  return map;
}

export function getCompletedTaskIds(studentId: string): string[] {
  const catalog = getProgramTaskCatalog();
  const map = collectDayProgressMap(studentId);
  const completed: string[] = [];
  for (const task of catalog) {
    const dp = map[task.day] ?? null;
    if (isTaskCompleted(dp, task)) completed.push(task.id);
  }
  return completed;
}

export function getDayWiseProgress(
  studentId: string,
  userEmail?: string | null
): Array<{ day: number; percent: number; complete: boolean }> {
  const map = collectDayProgressMap(studentId);
  return getAllPublishedPlans()
    .filter((p) => canAccessDay(p.day, userEmail))
    .map((plan) => {
      const dp = map[plan.day] ?? null;
      const dayTasks = getProgramTaskCatalog().filter((t) => t.day === plan.day);
      const done = dayTasks.filter((t) => isTaskCompleted(dp, t)).length;
      const percent =
        dayTasks.length > 0
          ? Math.round((done / dayTasks.length) * 100)
          : 0;
      return {
        day: plan.day,
        percent,
        complete: percent === 100,
      };
    });
}

export function getTaskLabel(task: ProgramTask): string {
  return task.label;
}
