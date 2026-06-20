/**
 * Firestore cloud sync for student progress.
 *
 * Architecture:
 *   localStorage  = primary cache (synchronous, instant reads/writes)
 *   Firestore     = cloud source-of-truth (async, survives browser clears / new devices)
 *
 * On every saveStore()   → data is written to localStorage immediately, then
 *                          pushed to Firestore in the background (fire-and-forget).
 * On every login         → Firestore data is compared with localStorage; whichever
 *                          has a newer `updatedAt` timestamp wins and is written back
 *                          to localStorage so the rest of the app reads it normally.
 */

import { GUEST_STUDENT_ID } from "@/lib/storage/constants";
import type { LocalStudentStore } from "@/lib/storage/types";

const STUDENTS_COLLECTION = "students";

/** Returns the Firestore db instance, initializing Firebase if needed. */
async function getDb() {
  try {
    const { initializeApp, getApps } = await import("firebase/app");
    const apiKey = process.env.NEXT_PUBLIC_FIREBASE_API_KEY;
    const projectId = process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID;
    if (!apiKey || !projectId) return null;

    const app =
      getApps().length > 0
        ? getApps()[0]!
        : initializeApp({
            apiKey,
            authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
            projectId,
            storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
            messagingSenderId:
              process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
            appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
          });

    const { getFirestore } = await import("firebase/firestore");
    return getFirestore(app);
  } catch {
    return null;
  }
}

/**
 * Saves the full student store to Firestore under /students/{uid}.
 * Silently no-ops for guests or when Firestore is unavailable.
 * Always called fire-and-forget — never awaited by the caller.
 */
export async function saveStoreToFirestore(
  store: LocalStudentStore
): Promise<void> {
  if (!store.uid || store.uid === GUEST_STUDENT_ID || store.isGuest) return;
  try {
    const db = await getDb();
    if (!db) return;
    const { doc, setDoc } = await import("firebase/firestore");
    await setDoc(doc(db, STUDENTS_COLLECTION, store.uid), {
      ...store,
      // Firestore does not allow undefined values
      phone: store.phone ?? null,
      photoURL: store.photoURL ?? null,
      lastStudyDate: store.lastStudyDate ?? null,
      lastLogin: store.lastLogin ?? null,
    });
  } catch {
    // Silently fail — localStorage is primary
  }
}

/**
 * Loads the student store from Firestore.
 * Returns null if the document doesn't exist or Firestore is unavailable.
 */
export async function loadStoreFromFirestore(
  uid: string
): Promise<LocalStudentStore | null> {
  if (!uid || uid === GUEST_STUDENT_ID) return null;
  try {
    const db = await getDb();
    if (!db) return null;
    const { doc, getDoc } = await import("firebase/firestore");
    const snap = await getDoc(doc(db, STUDENTS_COLLECTION, uid));
    if (!snap.exists()) return null;
    const data = snap.data() as LocalStudentStore;
    // Normalise null → undefined for optional fields
    return {
      ...data,
      phone: data.phone ?? undefined,
      photoURL: data.photoURL ?? undefined,
      lastStudyDate: data.lastStudyDate ?? undefined,
      lastLogin: data.lastLogin ?? undefined,
      bookmarkedQuestions: data.bookmarkedQuestions ?? [],
    };
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Public leaderboard — separate /leaderboard/{uid} collection
// so it can have permissive read rules without exposing full student data.
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

/**
 * Writes a student's public leaderboard entry to /leaderboard/{uid}.
 * Firestore rules for this collection should allow public reads.
 */
export async function updateLeaderboardEntry(
  uid: string,
  entry: LeaderboardEntry
): Promise<void> {
  if (!uid || uid === GUEST_STUDENT_ID) return;
  console.log("[Firestore] updateLeaderboardEntry called for", uid);
  const db = await getDb();
  if (!db) {
    console.warn("[Firestore] getDb() returned null — Firebase not initialised yet");
    return;
  }
  console.log("[Firestore] Writing to leaderboard/", uid, entry);
  const { doc, setDoc } = await import("firebase/firestore");
  await setDoc(doc(db, "leaderboard", uid), entry, { merge: true });
  console.log("[Firestore] leaderboard write complete for", uid);
}

/**
 * Reads all leaderboard entries, sorted by completionPct desc.
 * Used by the leaderboard page (client-side).
 */
export async function getLeaderboardEntries(): Promise<
  Array<LeaderboardEntry & { uid: string }>
> {
  try {
    const db = await getDb();
    if (!db) {
      console.warn("[Firestore] getLeaderboardEntries: db not ready");
      return [];
    }
    // Single-field orderBy only — no composite index needed.
    // Secondary sort (accuracy) done client-side below.
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
    // Secondary sort by accuracy client-side (avoids composite index requirement)
    rows.sort((a, b) =>
      b.completionPct !== a.completionPct
        ? b.completionPct - a.completionPct
        : b.accuracy - a.accuracy
    );
    console.log("[Firestore] Leaderboard entries loaded:", rows.length);
    return rows;
  } catch (e) {
    console.error("[Firestore] getLeaderboardEntries error:", e);
    return [];
  }
}

/**
 * Merges Firestore data into localStorage on login.
 * Whichever copy has a newer `updatedAt` timestamp is kept.
 * Returns the winning store (already written to localStorage when Firestore wins).
 */
export async function hydrateFromFirestore(
  uid: string,
  localStore: LocalStudentStore | null,
  saveToLocal: (store: LocalStudentStore) => void
): Promise<LocalStudentStore | null> {
  const cloudStore = await loadStoreFromFirestore(uid);
  if (!cloudStore) return localStore;

  // If there is no local copy, use Firestore data directly.
  if (!localStore) {
    saveToLocal(cloudStore);
    return cloudStore;
  }

  // Keep whichever copy was updated most recently.
  const localTime = new Date(localStore.updatedAt ?? 0).getTime();
  const cloudTime = new Date(cloudStore.updatedAt ?? 0).getTime();

  if (cloudTime > localTime) {
    saveToLocal(cloudStore);
    return cloudStore;
  }

  // Local is newer (or equal) — push it to Firestore to keep cloud in sync.
  void saveStoreToFirestore(localStore);
  return localStore;
}
