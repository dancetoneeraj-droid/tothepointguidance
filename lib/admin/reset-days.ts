import type { LocalStudentStore } from "@/lib/storage/types";
import { comprehensionRecordId } from "@/lib/storage/client";
import { reconcileProgressWithCompletions } from "@/lib/quiz/completion-state";

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

function isDayInClearedRange(day: number, through: number): boolean {
  return through > 0 && day >= 1 && day <= through;
}

function reviewIsAfterClear(
  store: LocalStudentStore,
  quizId: string,
  clearedAt: string
): boolean {
  const review = store.quizReviewRecords?.[quizId];
  if (!review?.completedAt) return false;
  return new Date(review.completedAt).getTime() > new Date(clearedAt).getTime();
}

function filterQuizzesAfterAdminClear(
  store: LocalStudentStore,
  through: number,
  clearedAt: string
): string[] {
  return (store.completedQuizzes ?? []).filter((id) => {
    const day = quizDayFromId(id);
    if (day === null || !isDayInClearedRange(day, through)) return true;
    return reviewIsAfterClear(store, id, clearedAt);
  });
}

function filterReviewsAfterAdminClear(
  store: LocalStudentStore,
  through: number,
  clearedAt: string
): Record<string, NonNullable<LocalStudentStore["quizReviewRecords"][string]>> {
  return Object.fromEntries(
    Object.entries(store.quizReviewRecords ?? {}).filter(([id]) => {
      const day = quizDayFromId(id);
      if (day === null || !isDayInClearedRange(day, through)) return true;
      return reviewIsAfterClear(store, id, clearedAt);
    })
  );
}

function purgeDayShellProgress(
  store: LocalStudentStore,
  fromDay: number,
  toDay: number
): Pick<
  LocalStudentStore,
  | "dayProgress"
  | "englishProgress"
  | "gkProgress"
  | "comprehensionRecords"
  | "vocabDaysCompleted"
  | "vocabProgress"
  | "completedDays"
> {
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

  return {
    dayProgress,
    englishProgress,
    gkProgress,
    comprehensionRecords,
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
  };
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
  const clearedAt = new Date().toISOString();
  const clearedThrough = Math.max(store.adminClearedDaysThrough ?? 0, high);
  const shell = purgeDayShellProgress(store, low, high);

  return reconcileProgressWithCompletions({
    ...store,
    ...shell,
    completedQuizzes: (store.completedQuizzes ?? []).filter(
      (id) => !quizIdInDayRange(id, low, high)
    ),
    quizReviewRecords: Object.fromEntries(
      Object.entries(store.quizReviewRecords ?? {}).filter(
        ([id]) => !quizIdInDayRange(id, low, high)
      )
    ),
    adminClearedDaysThrough: clearedThrough,
    adminClearedAt: clearedAt,
    updatedAt: clearedAt,
  });
}

/**
 * Before merging phone + cloud: drop stale attempts in admin-cleared days,
 * but keep quizzes the student retook after the reset timestamp.
 */
export function getAdminClearAwareStore(
  store: LocalStudentStore
): LocalStudentStore {
  const through = store.adminClearedDaysThrough ?? 0;
  if (through <= 0) return store;
  return stripStaleClearedDaysForMerge(
    store,
    through,
    store.adminClearedAt ?? store.updatedAt
  );
}

export function stripStaleClearedDaysForMerge(
  store: LocalStudentStore,
  clearedThrough: number,
  clearedAt: string | undefined
): LocalStudentStore {
  if (clearedThrough <= 0) return store;

  const effectiveClearedAt = clearedAt ?? store.adminClearedAt ?? store.updatedAt;

  // Legacy docs: adminClearedDaysThrough set but no timestamp — hard-drop cleared days.
  if (!store.adminClearedAt && !clearedAt) {
    const shell = purgeDayShellProgress(store, 1, clearedThrough);
    return reconcileProgressWithCompletions({
      ...store,
      ...shell,
      completedQuizzes: (store.completedQuizzes ?? []).filter((id) => {
        const day = quizDayFromId(id);
        return day === null || day > clearedThrough;
      }),
      quizReviewRecords: Object.fromEntries(
        Object.entries(store.quizReviewRecords ?? {}).filter(([id]) => {
          const day = quizDayFromId(id);
          return day === null || day > clearedThrough;
        })
      ),
      adminClearedDaysThrough: clearedThrough,
    });
  }

  const completedQuizzes = filterQuizzesAfterAdminClear(
    store,
    clearedThrough,
    effectiveClearedAt
  );
  const quizReviewRecords = filterReviewsAfterAdminClear(
    store,
    clearedThrough,
    effectiveClearedAt
  );

  const shell = purgeDayShellProgress(store, 1, clearedThrough);
  const keptClearedDayKeys = new Set(
    completedQuizzes
      .map((id) => quizDayFromId(id))
      .filter((day): day is number => day !== null && isDayInClearedRange(day, clearedThrough))
      .map(String)
  );

  for (const key of keptClearedDayKeys) {
    if (store.dayProgress?.[key]) shell.dayProgress[key] = store.dayProgress[key]!;
    if (store.englishProgress?.[key]) {
      shell.englishProgress[key] = store.englishProgress[key]!;
    }
    if (store.gkProgress?.[key]) shell.gkProgress[key] = store.gkProgress[key]!;
  }

  for (let d = 1; d <= clearedThrough; d++) {
    const compId = comprehensionRecordId(d);
    const comp = store.comprehensionRecords?.[compId];
    if (
      comp &&
      new Date(comp.completedAt).getTime() > new Date(effectiveClearedAt).getTime()
    ) {
      shell.comprehensionRecords[compId] = comp;
    }
  }

  return reconcileProgressWithCompletions({
    ...store,
    ...shell,
    completedQuizzes,
    quizReviewRecords,
    adminClearedDaysThrough: clearedThrough,
    adminClearedAt: store.adminClearedAt ?? effectiveClearedAt,
  });
}

/** @deprecated Use stripStaleClearedDaysForMerge during sync merge. */
export function applyAdminDayClearance(store: LocalStudentStore): LocalStudentStore {
  const through = store.adminClearedDaysThrough ?? 0;
  if (through <= 0) return store;
  return stripStaleClearedDaysForMerge(
    store,
    through,
    store.adminClearedAt ?? store.updatedAt
  );
}
