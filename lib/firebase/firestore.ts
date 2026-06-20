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

/** Returns the Firestore db instance, or null if Firebase is not ready. */
async function getDb() {
  try {
    const { getApps } = await import("firebase/app");
    const apps = getApps();
    if (!apps.length) return null;
    const { getFirestore } = await import("firebase/firestore");
    return getFirestore(apps[0]!);
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
