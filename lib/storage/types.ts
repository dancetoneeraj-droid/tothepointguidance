import type {
  DayProgress,
  OverrideRecord,
  QuizReviewRecord,
  ComprehensionRecord,
  VocabWordProgress,
} from "@/types";

/** Full student record — localStorage cache + Firestore cloud backup. */
export interface LocalStudentStore {
  version: number;
  uid: string;
  displayName: string;
  email: string;
  phone?: string;
  photoURL?: string;
  isGuest: boolean;
  currentDay: number;
  unlockedDay: number;
  completedDays: number[];
  completedQuizzes: string[];
  quizReviewRecords: Record<string, QuizReviewRecord>;
  comprehensionRecords: Record<string, ComprehensionRecord>;
  /** Per-word vocabulary revision progress (keyed by word id). */
  vocabProgress: Record<string, VocabWordProgress>;
  /** Days on which the vocabulary task has been completed at least once. */
  vocabDaysCompleted: number[];
  overrideHistory: OverrideRecord[];
  mathsProgress: Record<string, number>;
  reasoningProgress: Record<string, number>;
  englishProgress: Record<string, DayProgress["english"]>;
  gkProgress: Record<string, DayProgress["gk"]>;
  dayProgress: Record<string, DayProgress>;
  streak: number;
  totalQuestionsSolved: number;
  totalCorrect: number;
  accuracy: number;
  topicIndices: Record<string, number>;
  /** Question IDs the student has bookmarked for later review. */
  bookmarkedQuestions: string[];
  lastStudyDate?: string;
  /** ISO timestamp of the most recent login — synced to Firestore. */
  lastLogin?: string;
  createdAt: string;
  updatedAt: string;
}
