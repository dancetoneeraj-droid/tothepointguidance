import type { LocalStudentStore } from "@/lib/storage/types";
import { comprehensionRecordId } from "@/lib/storage/client";

export function quizDayFromId(quizId: string): number | null {
  const match = quizId.match(/^day(\d+)-/);
  return match ? parseInt(match[1]!, 10) : null;
}

export function quizIdInDayRange(
  quizId: string,
  fromDay: number,
  toDay: number
): boolean {
  const day = quizDayFromId(quizId);
  return day !== null && day >= fromDay && day <= toDay;
}

/**
 * Fully clears progress for days [fromDay, toDay] so the student can retake them.
 * Sets adminClearedDaysThrough so login merge does not restore these days from local cache.
 */
export function resetStudentDayRange(
  store: LocalStudentStore,
  fromDay: number,
  toDay: number
): LocalStudentStore {
  const low = Math.min(fromDay, toDay);
  const high = Math.max(fromDay, toDay);

  const dayProgress = { ...(store.dayProgress ?? {}) };
  const englishProgress = { ...(store.englishProgress ?? {}) };
  const gkProgress = { ...(store.gkProgress ?? {}) };
  const comprehensionRecords = { ...(store.comprehensionRecords ?? {}) };

  for (let d = low; d <= high; d++) {
    const key = String(d);
    delete dayProgress[key];
    delete englishProgress[key];
    delete gkProgress[key];
    delete comprehensionRecords[comprehensionRecordId(d)];
  }

  const clearedThrough = Math.max(store.adminClearedDaysThrough ?? 0, high);

  return {
    ...store,
    dayProgress,
    englishProgress,
    gkProgress,
    comprehensionRecords,
    completedQuizzes: (store.completedQuizzes ?? []).filter(
      (id) => !quizIdInDayRange(id, low, high)
    ),
    quizReviewRecords: Object.fromEntries(
      Object.entries(store.quizReviewRecords ?? {}).filter(
        ([id]) => !quizIdInDayRange(id, low, high)
      )
    ),
    vocabDaysCompleted: (store.vocabDaysCompleted ?? []).filter(
      (d) => d < low || d > high
    ),
    vocabProgress: Object.fromEntries(
      Object.entries(store.vocabProgress ?? {}).filter(
        ([, entry]) => entry.learnedDay < low || entry.learnedDay > high
      )
    ),
    completedDays: (store.completedDays ?? []).filter(
      (d) => d < low || d > high
    ),
    adminClearedDaysThrough: clearedThrough,
    updatedAt: new Date().toISOString(),
  };
}

/** Remove admin-cleared days from a store copy before merging with cloud. */
export function applyAdminDayClearance(store: LocalStudentStore): LocalStudentStore {
  const through = store.adminClearedDaysThrough ?? 0;
  if (through <= 0) return store;
  return resetStudentDayRange(store, 1, through);
}
