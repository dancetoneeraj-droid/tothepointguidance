import {
  mergeStudentStores,
  loadStoreFromFirestore,
  queueStudentPersist,
} from "@/lib/firebase/firestore";
import type { LocalStudentStore } from "@/lib/storage/types";
import { reconcileProgressWithCompletions } from "@/lib/quiz/completion-state";
import { loadStore, writeLocalCache } from "@/lib/storage/client";
import { invalidateCompletionCache } from "@/lib/storage/completion-cache";

const SYNC_COOLDOWN_MS = 45_000;
const lastSyncAt = new Map<string, number>();

function progressSnapshot(store: LocalStudentStore): string {
  return JSON.stringify({
    completedQuizzes: store.completedQuizzes ?? [],
    adminClearedDaysThrough: store.adminClearedDaysThrough ?? 0,
    adminClearedAt: store.adminClearedAt ?? null,
    completedDays: store.completedDays ?? [],
    vocabDaysCompleted: store.vocabDaysCompleted ?? [],
    currentDay: store.currentDay,
    unlockedDay: store.unlockedDay,
  });
}

function shouldSkipSync(uid: string, force?: boolean): boolean {
  if (force) return false;
  const last = lastSyncAt.get(uid) ?? 0;
  return Date.now() - last < SYNC_COOLDOWN_MS;
}

/**
 * Merge local + cloud progress. Throttled on page loads; skips Firestore
 * writes when nothing meaningful changed.
 */
export async function syncStudentProgress(
  uid: string,
  options?: { force?: boolean }
): Promise<boolean> {
  if (!uid) return false;
  if (shouldSkipSync(uid, options?.force)) return false;

  lastSyncAt.set(uid, Date.now());

  const local = loadStore(uid);
  const cloud = await loadStoreFromFirestore(uid, {
    skipReviews: !!local,
    fallbackReviews: local?.quizReviewRecords,
  });

  if (!cloud && !local) return false;

  if (!cloud && local) {
    queueStudentPersist(reconcileProgressWithCompletions(local));
    return false;
  }

  if (cloud && !local) {
    const normalized = reconcileProgressWithCompletions(cloud);
    writeLocalCache(normalized);
    invalidateCompletionCache();
    return true;
  }

  if (cloud && local) {
    const merged = reconcileProgressWithCompletions(
      mergeStudentStores(local, cloud)
    );
    const changed = progressSnapshot(local) !== progressSnapshot(merged);

    writeLocalCache(merged);
    invalidateCompletionCache();

    if (changed) {
      merged.updatedAt = new Date().toISOString();
      writeLocalCache(merged);
      queueStudentPersist(merged);
    }

    return changed;
  }

  return false;
}

/** @deprecated Use syncStudentProgress */
export async function pullCloudProgressIfNewer(uid: string): Promise<boolean> {
  return syncStudentProgress(uid);
}
