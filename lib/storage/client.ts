"use client";

import { ACTIVE_STUDENT_KEY, studentDataKey } from "./constants";
import type { LocalStudentStore } from "./types";

export function isBrowser(): boolean {
  return typeof window !== "undefined";
}

export function getActiveStudentId(): string | null {
  if (!isBrowser()) return null;
  return localStorage.getItem(ACTIVE_STUDENT_KEY);
}

export function setActiveStudentId(studentId: string): void {
  if (!isBrowser()) return;
  localStorage.setItem(ACTIVE_STUDENT_KEY, studentId);
}

export function loadStore(studentId: string): LocalStudentStore | null {
  if (!isBrowser()) return null;
  const raw = localStorage.getItem(studentDataKey(studentId));
  if (!raw) return null;
  try {
    return JSON.parse(raw) as LocalStudentStore;
  } catch {
    return null;
  }
}

/** Write to localStorage cache only (no cloud sync). Used during hydration. */
export function writeLocalCache(store: LocalStudentStore): void {
  if (!isBrowser()) return;
  localStorage.setItem(studentDataKey(store.uid), JSON.stringify(store));
}

/**
 * Save progress: update local cache immediately, queue reliable Firestore persist.
 */
export function saveStore(store: LocalStudentStore): void {
  if (!isBrowser()) return;
  store.updatedAt = new Date().toISOString();
  writeLocalCache(store);

  if (!store.isGuest && store.uid) {
    void import("@/lib/firebase/firestore").then(({ queueStudentPersist }) =>
      queueStudentPersist(store)
    );
  }
}

/** Wait until the latest queued cloud save for this student completes. */
export async function ensureCloudSaved(studentId: string): Promise<boolean> {
  if (!studentId) return false;
  const { flushStudentPersistQueue } = await import("@/lib/firebase/firestore");
  return flushStudentPersistQueue(studentId);
}

export function quizCompletionId(
  day: number,
  subject: string,
  topic: string,
  from?: number
): string {
  const base = `day${day}-${subject}-${topic}`;
  return from !== undefined ? `${base}-f${from}` : base;
}

export function comprehensionRecordId(day: number): string {
  return `day${day}-english-comprehension`;
}
