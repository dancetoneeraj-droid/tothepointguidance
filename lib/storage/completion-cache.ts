import type { LocalStudentStore } from "@/lib/storage/types";

let cache: {
  studentId: string;
  storeUpdatedAt: string;
  view: LocalStudentStore;
} | null = null;

export function getCachedCompletionView(
  studentId: string,
  storeUpdatedAt: string
): LocalStudentStore | null {
  if (
    cache &&
    cache.studentId === studentId &&
    cache.storeUpdatedAt === storeUpdatedAt
  ) {
    return cache.view;
  }
  return null;
}

export function setCachedCompletionView(
  studentId: string,
  storeUpdatedAt: string,
  view: LocalStudentStore
): void {
  cache = { studentId, storeUpdatedAt, view };
}

export function invalidateCompletionCache(): void {
  cache = null;
}
