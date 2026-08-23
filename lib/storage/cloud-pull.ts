import {
  mergeStudentStores,
  loadStoreFromFirestore,
  queueStudentPersist,
  flushStudentPersistQueue,
} from "@/lib/firebase/firestore";
import { reconcileProgressWithCompletions } from "@/lib/quiz/completion-state";
import { loadStore, writeLocalCache } from "@/lib/storage/client";

/**
 * Merge local + cloud progress both ways so attempts are never dropped
 * when cloud is stale or a Firestore write partially failed.
 */
export async function syncStudentProgress(uid: string): Promise<boolean> {
  const local = loadStore(uid);
  const cloud = await loadStoreFromFirestore(uid);

  if (!cloud && !local) return false;

  if (!cloud && local) {
    queueStudentPersist(reconcileProgressWithCompletions(local));
    await flushStudentPersistQueue(uid);
    return false;
  }

  if (cloud && !local) {
    writeLocalCache(reconcileProgressWithCompletions(cloud));
    return true;
  }

  if (cloud && local) {
    const merged = reconcileProgressWithCompletions(
      mergeStudentStores(local, cloud)
    );
    writeLocalCache(merged);
    queueStudentPersist(merged);
    await flushStudentPersistQueue(uid);

    const before = JSON.stringify(local.completedQuizzes ?? []);
    const after = JSON.stringify(merged.completedQuizzes ?? []);
    return before !== after;
  }

  return false;
}

/** @deprecated Use syncStudentProgress */
export async function pullCloudProgressIfNewer(uid: string): Promise<boolean> {
  return syncStudentProgress(uid);
}
