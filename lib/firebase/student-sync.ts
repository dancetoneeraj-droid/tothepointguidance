/**
 * Reliable Firestore persistence for student progress.
 *
 * - Main doc holds progress metadata (no quizReviewRecords — avoids 1 MiB limit).
 * - Quiz reviews live in students/{uid}/quizReviews/{quizId}.
 * - Login merges local + cloud so neither copy silently wins.
 */

import type { DayProgress, QuizReviewRecord } from "@/types";
import type { LocalStudentStore } from "@/lib/storage/types";
import { applyAdminDayClearance } from "@/lib/admin/reset-days";
import { reconcileProgressWithCompletions } from "@/lib/quiz/completion-state";

export const STUDENTS_COLLECTION = "students";
export const QUIZ_REVIEWS_SUBCOLLECTION = "quizReviews";

const MAX_PERSIST_ATTEMPTS = 5;
const RETRY_BASE_MS = 800;

const persistQueues = new Map<string, LocalStudentStore>();
const persistInflight = new Map<string, Promise<boolean>>();

export type PersistResult =
  | { ok: true }
  | { ok: false; error: string };

function isBrowser(): boolean {
  return typeof window !== "undefined";
}

function maxNum(a: number, b: number): number {
  return Math.max(a, b);
}

function unionStrings(a: string[], b: string[]): string[] {
  return [...new Set([...a, ...b])];
}

function unionNumbers(a: number[], b: number[]): number[] {
  return [...new Set([...a, ...b])];
}

function mergeMaxRecords(
  a: Record<string, number>,
  b: Record<string, number>
): Record<string, number> {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  const out: Record<string, number> = {};
  for (const key of keys) {
    out[key] = maxNum(a[key] ?? 0, b[key] ?? 0);
  }
  return out;
}

function mergeEnglishSection(
  a: DayProgress["english"],
  b: DayProgress["english"]
): DayProgress["english"] {
  return {
    grammar: a.grammar || b.grammar,
    vocabulary: a.vocabulary || b.vocabulary,
    comprehension: a.comprehension || b.comprehension,
  };
}

function mergeGkSection(
  a: DayProgress["gk"],
  b: DayProgress["gk"]
): DayProgress["gk"] {
  return {
    materialsCompleted: a.materialsCompleted || b.materialsCompleted,
    revisionQuizCompleted: a.revisionQuizCompleted || b.revisionQuizCompleted,
  };
}

function dayProgressScore(d: DayProgress): number {
  let score = d.completed ? 100 : 0;
  if (d.english.grammar) score += 1;
  if (d.english.vocabulary) score += 1;
  if (d.english.comprehension) score += 1;
  if (d.reasoning.completed) score += 1;
  if (d.gk.materialsCompleted) score += 1;
  if (d.gk.revisionQuizCompleted) score += 1;
  for (const m of Object.values(d.maths)) {
    if (m.completed) score += 1;
  }
  return score;
}

function mergeDayProgressEntry(
  a: DayProgress,
  b: DayProgress
): DayProgress {
  const primary = dayProgressScore(a) >= dayProgressScore(b) ? a : b;
  const secondary = primary === a ? b : a;

  const maths: DayProgress["maths"] = { ...primary.maths };
  for (const [topic, entry] of Object.entries(secondary.maths)) {
    const existing = maths[topic];
    if (!existing) {
      maths[topic] = entry;
      continue;
    }
    maths[topic] = {
      currentIndex: maxNum(existing.currentIndex, entry.currentIndex),
      completed: existing.completed || entry.completed,
      lastScore: existing.lastScore ?? entry.lastScore,
      lastAccuracy: existing.lastAccuracy ?? entry.lastAccuracy,
    };
  }

  return {
    day: primary.day,
    completed: primary.completed || secondary.completed,
    completedAt: primary.completedAt ?? secondary.completedAt,
    english: mergeEnglishSection(primary.english, secondary.english),
    reasoning: {
      currentIndex: maxNum(
        primary.reasoning.currentIndex,
        secondary.reasoning.currentIndex
      ),
      completed: primary.reasoning.completed || secondary.reasoning.completed,
      lastScore: primary.reasoning.lastScore ?? secondary.reasoning.lastScore,
      lastAccuracy:
        primary.reasoning.lastAccuracy ?? secondary.reasoning.lastAccuracy,
    },
    gk: mergeGkSection(primary.gk, secondary.gk),
    maths,
  };
}

function mergeDayProgressMap(
  a: Record<string, DayProgress>,
  b: Record<string, DayProgress>
): Record<string, DayProgress> {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  const out: Record<string, DayProgress> = {};
  for (const key of keys) {
    const da = a[key];
    const db = b[key];
    if (da && db) out[key] = mergeDayProgressEntry(da, db);
    else out[key] = (da ?? db)!;
  }
  return out;
}

function mergeQuizReviewRecords(
  a: Record<string, QuizReviewRecord>,
  b: Record<string, QuizReviewRecord>
): Record<string, QuizReviewRecord> {
  const out = { ...a };
  for (const [id, record] of Object.entries(b)) {
    const existing = out[id];
    if (!existing) {
      out[id] = record;
      continue;
    }
    const existingTime = new Date(existing.completedAt).getTime();
    const recordTime = new Date(record.completedAt).getTime();
    out[id] = recordTime >= existingTime ? record : existing;
  }
  return out;
}

function mergeEnglishProgressMap(
  a: Record<string, DayProgress["english"]>,
  b: Record<string, DayProgress["english"]>
): Record<string, DayProgress["english"]> {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  const out: Record<string, DayProgress["english"]> = {};
  for (const key of keys) {
    out[key] = mergeEnglishSection(
      a[key] ?? { grammar: false, vocabulary: false, comprehension: false },
      b[key] ?? { grammar: false, vocabulary: false, comprehension: false }
    );
  }
  return out;
}

function mergeGkProgressMap(
  a: Record<string, DayProgress["gk"]>,
  b: Record<string, DayProgress["gk"]>
): Record<string, DayProgress["gk"]> {
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  const out: Record<string, DayProgress["gk"]> = {};
  for (const key of keys) {
    out[key] = mergeGkSection(
      a[key] ?? { materialsCompleted: false, revisionQuizCompleted: false },
      b[key] ?? { materialsCompleted: false, revisionQuizCompleted: false }
    );
  }
  return out;
}

/** Merge local and cloud copies — never discard the richer progress side. */
export function mergeStudentStores(
  local: LocalStudentStore,
  cloud: LocalStudentStore
): LocalStudentStore {
  const clearedThrough = Math.max(
    local.adminClearedDaysThrough ?? 0,
    cloud.adminClearedDaysThrough ?? 0
  );

  // Admin day reset must win over stale phone cache — strip cleared days on BOTH sides
  // before union merge, otherwise old localStorage quizzes reappear after reset.
  const withClearanceStamp = (store: LocalStudentStore): LocalStudentStore =>
    clearedThrough > 0
      ? { ...applyAdminDayClearance(store), adminClearedDaysThrough: clearedThrough }
      : store;

  const localBase = withClearanceStamp(local);
  const cloudBase = withClearanceStamp(cloud);

  const displayName = cloudBase.displayName || localBase.displayName;
  const email = cloudBase.email || localBase.email;

  const mergedReviews = mergeQuizReviewRecords(
    localBase.quizReviewRecords ?? {},
    cloudBase.quizReviewRecords ?? {}
  );

  const completedQuizzes = unionStrings(
    localBase.completedQuizzes ?? [],
    cloudBase.completedQuizzes ?? []
  );

  // Ensure every review has a matching completion id.
  for (const quizId of Object.keys(mergedReviews)) {
    if (!completedQuizzes.includes(quizId)) completedQuizzes.push(quizId);
  }

  const totalQuestionsSolved = maxNum(
    localBase.totalQuestionsSolved,
    cloudBase.totalQuestionsSolved
  );
  const totalCorrect = maxNum(localBase.totalCorrect, cloudBase.totalCorrect);

  const merged: LocalStudentStore = {
    version: Math.max(localBase.version ?? 1, cloudBase.version ?? 1),
    uid: local.uid,
    displayName,
    email,
    phone: cloudBase.phone ?? localBase.phone,
    photoURL: cloudBase.photoURL ?? localBase.photoURL,
    isGuest: false,
    currentDay: maxNum(localBase.currentDay, cloudBase.currentDay),
    unlockedDay: maxNum(localBase.unlockedDay, cloudBase.unlockedDay),
    completedDays: unionNumbers(
      localBase.completedDays ?? [],
      cloudBase.completedDays ?? []
    ).sort((x, y) => x - y),
    completedQuizzes,
    quizReviewRecords: mergedReviews,
    comprehensionRecords: {
      ...(localBase.comprehensionRecords ?? {}),
      ...(cloudBase.comprehensionRecords ?? {}),
    },
    vocabProgress: {
      ...(localBase.vocabProgress ?? {}),
      ...(cloudBase.vocabProgress ?? {}),
    },
    vocabDaysCompleted: unionNumbers(
      localBase.vocabDaysCompleted ?? [],
      cloudBase.vocabDaysCompleted ?? []
    ).sort((x, y) => x - y),
    overrideHistory: [
      ...(localBase.overrideHistory ?? []),
      ...(cloudBase.overrideHistory ?? []),
    ],
    mathsProgress: mergeMaxRecords(
      localBase.mathsProgress ?? {},
      cloudBase.mathsProgress ?? {}
    ),
    reasoningProgress: mergeMaxRecords(
      localBase.reasoningProgress ?? {},
      cloudBase.reasoningProgress ?? {}
    ),
    englishProgress: mergeEnglishProgressMap(
      localBase.englishProgress ?? {},
      cloudBase.englishProgress ?? {}
    ),
    gkProgress: mergeGkProgressMap(
      localBase.gkProgress ?? {},
      cloudBase.gkProgress ?? {}
    ),
    dayProgress: mergeDayProgressMap(
      localBase.dayProgress ?? {},
      cloudBase.dayProgress ?? {}
    ),
    streak: maxNum(localBase.streak, cloudBase.streak),
    totalQuestionsSolved,
    totalCorrect,
    accuracy:
      totalQuestionsSolved > 0
        ? Math.round((totalCorrect / totalQuestionsSolved) * 100)
        : 0,
    topicIndices: mergeMaxRecords(
      localBase.topicIndices ?? {},
      cloudBase.topicIndices ?? {}
    ),
    bookmarkedQuestions: unionStrings(
      localBase.bookmarkedQuestions ?? [],
      cloudBase.bookmarkedQuestions ?? []
    ),
    lastStudyDate: localBase.lastStudyDate ?? cloudBase.lastStudyDate,
    lastLogin: localBase.lastLogin ?? cloudBase.lastLogin,
    adminClearedDaysThrough: clearedThrough > 0 ? clearedThrough : undefined,
    createdAt: localBase.createdAt ?? cloudBase.createdAt,
    updatedAt: new Date().toISOString(),
  };

  return reconcileProgressWithCompletions(merged);
}

export function stripReviewsForMainDoc(
  store: LocalStudentStore
): Omit<LocalStudentStore, "quizReviewRecords"> & {
  quizReviewRecords: Record<string, never>;
} {
  return {
    ...store,
    quizReviewRecords: {},
  };
}

async function sleep(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

import { getDb } from "@/lib/firebase/db";

export async function loadQuizReviewsFromSubcollection(
  uid: string
): Promise<Record<string, QuizReviewRecord>> {
  try {
    const db = await getDb();
    if (!db) return {};
    const { collection, getDocs } = await import("firebase/firestore");
    const snap = await getDocs(
      collection(db, STUDENTS_COLLECTION, uid, QUIZ_REVIEWS_SUBCOLLECTION)
    );
    const records: Record<string, QuizReviewRecord> = {};
    for (const docSnap of snap.docs) {
      records[docSnap.id] = docSnap.data() as QuizReviewRecord;
    }
    return records;
  } catch (error) {
    console.error("[student-sync] Failed to load quiz reviews:", error);
    return {};
  }
}

async function syncQuizReviewSubcollection(
  uid: string,
  reviews: Record<string, QuizReviewRecord>
): Promise<void> {
  const db = await getDb();
  if (!db) throw new Error("Firestore unavailable");

  const { collection, doc, getDocs, writeBatch } = await import(
    "firebase/firestore"
  );
  const collRef = collection(
    db,
    STUDENTS_COLLECTION,
    uid,
    QUIZ_REVIEWS_SUBCOLLECTION
  );
  const existing = await getDocs(collRef);
  const batch = writeBatch(db);
  const nextIds = new Set(Object.keys(reviews));

  for (const docSnap of existing.docs) {
    if (!nextIds.has(docSnap.id)) batch.delete(docSnap.ref);
  }

  for (const [quizId, record] of Object.entries(reviews)) {
    batch.set(doc(collRef, quizId), record);
  }

  await batch.commit();
}

/** Persist full store to Firestore (main doc + quiz review subcollection). */
export async function persistStudentStoreToCloud(
  store: LocalStudentStore
): Promise<PersistResult> {
  if (!store.uid || store.isGuest) return { ok: true };

  let lastError = "Unknown error";

  for (let attempt = 0; attempt < MAX_PERSIST_ATTEMPTS; attempt++) {
    try {
      const db = await getDb();
      if (!db) {
        lastError = "Firestore unavailable";
        await sleep(RETRY_BASE_MS * (attempt + 1));
        continue;
      }

      const { doc, setDoc } = await import("firebase/firestore");
      const reviews = store.quizReviewRecords ?? {};

      await setDoc(doc(db, STUDENTS_COLLECTION, store.uid), {
        ...stripReviewsForMainDoc(store),
        phone: store.phone ?? null,
        photoURL: store.photoURL ?? null,
        lastStudyDate: store.lastStudyDate ?? null,
        lastLogin: store.lastLogin ?? null,
      });

      try {
        await syncQuizReviewSubcollection(store.uid, reviews);
      } catch (reviewError) {
        // Main progress doc saved — reviews can retry on next sync.
        console.error(
          "[student-sync] Review subcollection sync failed (main doc saved):",
          reviewError
        );
      }

      return { ok: true };
    } catch (error) {
      lastError =
        error instanceof Error ? error.message : "Firestore write failed";
      console.error(
        `[student-sync] Persist attempt ${attempt + 1}/${MAX_PERSIST_ATTEMPTS} failed:`,
        error
      );
      await sleep(RETRY_BASE_MS * (attempt + 1));
    }
  }

  return { ok: false, error: lastError };
}

export function queueStudentPersist(store: LocalStudentStore): void {
  if (!store.uid || store.isGuest) return;
  persistQueues.set(store.uid, store);
  void flushStudentPersistQueue(store.uid);
}

export async function flushStudentPersistQueue(
  uid: string
): Promise<boolean> {
  const pending = persistQueues.get(uid);
  if (!pending) return true;

  const inflight = persistInflight.get(uid);
  if (inflight) return inflight;

  const work = (async () => {
    const latest = persistQueues.get(uid);
    if (!latest) return true;

    const result = await persistStudentStoreToCloud(latest);
    if (result.ok) {
      persistQueues.delete(uid);
      return true;
    }

    console.error("[student-sync] Cloud save failed after retries:", result.error);
    return false;
  })();

  persistInflight.set(uid, work);
  try {
    return await work;
  } finally {
    persistInflight.delete(uid);
  }
}

export function registerPersistOnUnload(uid: string): () => void {
  if (!isBrowser() || !uid) return () => undefined;

  const flush = () => {
    const pending = persistQueues.get(uid);
    if (!pending) return;
    // Best-effort — cannot await during unload.
    void persistStudentStoreToCloud(pending);
  };

  window.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flush();
  });
  window.addEventListener("pagehide", flush);

  return () => {
    window.removeEventListener("pagehide", flush);
  };
}
