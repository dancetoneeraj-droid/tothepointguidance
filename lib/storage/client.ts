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

export function saveStore(store: LocalStudentStore): void {
  if (!isBrowser()) return;
  store.updatedAt = new Date().toISOString();
  localStorage.setItem(studentDataKey(store.uid), JSON.stringify(store));
}

export function quizCompletionId(
  day: number,
  subject: string,
  topic: string
): string {
  return `day${day}-${subject}-${topic}`;
}
