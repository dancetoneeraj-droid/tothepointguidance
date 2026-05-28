/**
 * @deprecated Firestore removed — use @/lib/storage/progress instead.
 * Re-exported for future Firebase adapter migration.
 */
export {
  getStudentProgress,
  initStudentProgress,
  getDayProgress,
  ensureDayProgress,
  recordQuizCompletion,
  markEnglishSection,
  markGkMaterials,
  recordOverride,
  unlockNextDay,
  getTopicIndex,
} from "@/lib/storage/progress";
