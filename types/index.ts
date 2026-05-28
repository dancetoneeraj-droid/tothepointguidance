export type Subject = "maths" | "english" | "reasoning" | "gk";

export interface Question {
  id: string;
  question: string;
  /** Hindi question text (Devanagari). */
  questionHi?: string;
  options: string[];
  optionsHi?: string[];
  correctAnswer: string;
  explanation?: string;
  explanationHi?: string;
}

export interface MathsQuizConfig {
  topic: string;
  questions: number;
  duration: number;
}

export interface EnglishConfig {
  grammarPdf?: string;
  vocabPdf?: string;
  comprehensionPdf?: string;
  grammarMindmap?: string;
  vocabNotes?: string;
  grammarQuiz?: string;
  comprehensionQuiz?: string;
}

export interface ReasoningConfig {
  topic: string;
  questions: number;
  duration: number;
}

export interface GkConfig {
  todayTopicPdf?: string;
  todayMindmap?: string;
  todayNotes?: string;
  revisionQuiz?: string;
  revisionTopic?: string;
}

export interface DailyPlan {
  day: number;
  published: boolean;
  maths: MathsQuizConfig[];
  english: EnglishConfig;
  reasoning: ReasoningConfig;
  gk: GkConfig;
}

export interface TopicProgress {
  currentIndex: number;
  completed: boolean;
  lastScore?: number;
  lastAccuracy?: number;
}

export interface DayProgress {
  day: number;
  maths: Record<string, TopicProgress>;
  english: {
    grammar: boolean;
    vocabulary: boolean;
    comprehension: boolean;
  };
  reasoning: TopicProgress;
  gk: {
    materialsCompleted: boolean;
    revisionQuizCompleted: boolean;
  };
  completed: boolean;
  completedAt?: string;
}

export interface OverrideRecord {
  fromDay: number;
  toDay: number;
  timestamp: string;
  reason?: string;
}

export interface StudentProgress {
  uid: string;
  displayName: string;
  email: string;
  phone?: string;
  photoURL?: string;
  currentDay: number;
  unlockedDay: number;
  completedDays: number[];
  streak: number;
  totalQuestionsSolved: number;
  totalCorrect: number;
  accuracy: number;
  topicIndices: Record<string, number>;
  overrides: OverrideRecord[];
  lastStudyDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface QuizSession {
  subject: Subject;
  topic: string;
  day: number;
  questions: Question[];
  durationMinutes: number;
  startIndex: number;
}

export interface QuizResult {
  correct: number;
  wrong: number;
  unanswered: number;
  total: number;
  /** Total marks (+2 / −0.5 scheme). */
  score: number;
  maxScore: number;
  accuracy: number;
  timeTakenSeconds: number;
}

export interface QuizRanking {
  rank: number | null;
  totalParticipants: number;
  percentile: number | null;
  countsForLeaderboard: boolean;
  isFirstAttempt: boolean;
  score: number;
  accuracy: number;
  timeSeconds: number;
}

export interface QuizReviewRecord {
  quizId: string;
  title: string;
  subject: Subject;
  topic: string;
  day: number;
  questionIds: string[];
  answers: Record<string, string>;
  result: QuizResult;
  ranking: QuizRanking | null;
  returnPath: string;
  analysisPath: string;
  solutionsPath: string;
  completedAt: string;
}

export interface PendingTask {
  id: string;
  day: number;
  subject: Subject;
  label: string;
  type: "quiz" | "reading" | "revision";
}
