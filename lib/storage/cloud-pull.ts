import { mergeStudentStores, loadStoreFromFirestore, queueStudentPersist } from "@/lib/firebase/firestore";
import { loadStore, writeLocalCache } from "@/lib/storage/client";

/** Pull Firestore progress when admin reset or another device has newer data. */
export async function pullCloudProgressIfNewer(uid: string): Promise<boolean> {
  const local = loadStore(uid);
  const cloud = await loadStoreFromFirestore(uid);
  if (!cloud) return false;

  if (!local) {
    writeLocalCache(cloud);
    return true;
  }

  const localTime = new Date(local.updatedAt ?? 0).getTime();
  const cloudTime = new Date(cloud.updatedAt ?? 0).getTime();

  if (cloudTime <= localTime) return false;

  const merged = mergeStudentStores(local, cloud);
  writeLocalCache(merged);
  queueStudentPersist(merged);
  return true;
}
