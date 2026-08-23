/**
 * Firestore cloud sync for student progress.
 *
 * Architecture:
 *   Firestore     = source of truth (with retry + merge on login)
 *   localStorage  = offline cache only
 *
 * Quiz review records are stored in a subcollection to stay under the 1 MiB doc limit.
 */

import { GUEST_STUDENT_ID } from "@/lib/storage/constants";
import type { QuizReviewRecord } from "@/types";
import type { LocalStudentStore } from "@/lib/storage/types";
import {
  STUDENTS_COLLECTION,
  loadQuizReviewsFromSubcollection,
  mergeStudentStores,
  persistStudentStoreToCloud,
  queueStudentPersist,
} from "@/lib/firebase/student-sync";

export {
  STUDENTS_COLLECTION,
  mergeStudentStores,
  queueStudentPersist,
  flushStudentPersistQueue,
  persistStudentStoreToCloud,
  registerPersistOnUnload,
} from "@/lib/firebase/student-sync";

import { getDb } from "@/lib/firebase/db";

function normalizeStore(data: LocalStudentStore): LocalStudentStore {
  return {
    ...data,
    phone: data.phone ?? undefined,
    photoURL: data.photoURL ?? undefined,
    lastStudyDate: data.lastStudyDate ?? undefined,
    lastLogin: data.lastLogin ?? undefined,
    bookmarkedQuestions: data.bookmarkedQuestions ?? [],
    quizReviewRecords: data.quizReviewRecords ?? {},
    comprehensionRecords: data.comprehensionRecords ?? {},
    vocabProgress: data.vocabProgress ?? {},
    vocabDaysCompleted: data.vocabDaysCompleted ?? [],
    completedQuizzes: data.completedQuizzes ?? [],
    dayProgress: data.dayProgress ?? {},
  };
}

/**
 * Saves the full student store to Firestore (main doc + quiz review subcollection).
 * Prefer queueStudentPersist() from the client cache layer for app writes.
 */
export async function saveStoreToFirestore(
  store: LocalStudentStore
): Promise<void> {
  if (!store.uid || store.uid === GUEST_STUDENT_ID || store.isGuest) return;
  const result = await persistStudentStoreToCloud(store);
  if (!result.ok) {
    throw new Error(result.error);
  }
}

/**
 * Loads the student store from Firestore (main doc + quiz review subcollection).
 */
export async function loadStoreFromFirestore(
  uid: string,
  options?: {
    skipReviews?: boolean;
    fallbackReviews?: Record<string, QuizReviewRecord>;
  }
): Promise<LocalStudentStore | null> {
  if (!uid || uid === GUEST_STUDENT_ID) return null;
  try {
    const db = await getDb();
    if (!db) return null;
    const { doc, getDoc } = await import("firebase/firestore");
    const snap = await getDoc(doc(db, STUDENTS_COLLECTION, uid));
    if (!snap.exists()) return null;

    const main = normalizeStore(snap.data() as LocalStudentStore);
    const subReviews = options?.skipReviews
      ? (options.fallbackReviews ?? {})
      : await loadQuizReviewsFromSubcollection(uid);
    const inlineReviews = main.quizReviewRecords ?? {};

    return normalizeStore({
      ...main,
      quizReviewRecords: { ...inlineReviews, ...subReviews },
    });
  } catch (error) {
    console.error("[Firestore] loadStoreFromFirestore failed:", error);
    return null;
  }
}

// ---------------------------------------------------------------------------
// Public leaderboard — separate /leaderboard/{uid} collection
// ---------------------------------------------------------------------------

export interface LeaderboardEntry {
  displayName: string;
  currentDay: number;
  tasksCompleted: number;
  completionPct: number;
  accuracy: number;
  streak: number;
  updatedAt: string;
}

export async function updateLeaderboardEntry(
  uid: string,
  entry: LeaderboardEntry
): Promise<void> {
  if (!uid || uid === GUEST_STUDENT_ID) return;
  const db = await getDb();
  if (!db) {
    console.warn("[Firestore] getDb() returned null — Firebase not initialised yet");
    return;
  }
  const { doc, setDoc } = await import("firebase/firestore");
  await setDoc(doc(db, "leaderboard", uid), entry, { merge: true });
}

export async function getLeaderboardEntries(): Promise<
  Array<LeaderboardEntry & { uid: string }>
> {
  try {
    const db = await getDb();
    if (!db) return [];
    const { collection, getDocs, orderBy, query, limit } = await import(
      "firebase/firestore"
    );
    const snap = await getDocs(
      query(
        collection(db, "leaderboard"),
        orderBy("completionPct", "desc"),
        limit(100)
      )
    );
    const rows = snap.docs.map((d) => ({
      uid: d.id,
      ...(d.data() as LeaderboardEntry),
    }));
    rows.sort((a, b) =>
      b.completionPct !== a.completionPct
        ? b.completionPct - a.completionPct
        : b.accuracy - a.accuracy
    );
    return rows;
  } catch (e) {
    console.error("[Firestore] getLeaderboardEntries error:", e);
    return [];
  }
}

/**
 * On login: merge local cache with Firestore, persist merged result to cloud,
 * then write the merged copy back to localStorage.
 */
export async function hydrateFromFirestore(
  uid: string,
  localStore: LocalStudentStore | null,
  saveToLocal: (store: LocalStudentStore) => void
): Promise<LocalStudentStore | null> {
  const cloudStore = await loadStoreFromFirestore(uid);

  if (!cloudStore && !localStore) return null;

  if (!cloudStore && localStore) {
    saveToLocal(localStore);
    queueStudentPersist(localStore);
    return localStore;
  }

  if (cloudStore && !localStore) {
    saveToLocal(cloudStore);
    return cloudStore;
  }

  if (cloudStore && localStore) {
    const merged = mergeStudentStores(localStore, cloudStore);
    saveToLocal(merged);
    queueStudentPersist(merged);
    return merged;
  }

  return null;
}
