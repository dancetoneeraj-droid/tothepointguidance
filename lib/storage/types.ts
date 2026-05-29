import type {
  DayProgress,
  OverrideRecord,
  QuizReviewRecord,
  VocabWordProgress,
} from "@/types";

/** Local-only student record (MVP). Firebase can sync this shape later. */
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
  lastStudyDate?: string;
  createdAt: string;
  updatedAt: string;
}
