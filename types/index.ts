export type Subject = "maths" | "english" | "reasoning" | "gk";

export interface Question {
  id: string;
  question: string;
  /** Hindi question text (Devanagari). */
  questionHi?: string;
  /** Alias used in some JSON banks. */
  questionHindi?: string;
  /** Optional figure/diagram image URL (Google Drive share link or direct URL). */
  image?: string;
  options: string[];
  optionsHi?: string[];
  correctAnswer: string;
  explanation?: string;
  explanationHi?: string;
  /** AI-generated step-by-step solution (added via add-solutions script). */
  solution?: string;
  /** Shared passage/scenario text for set-based questions (e.g. seating arrangement puzzles). */
  passage?: string;
  /** 1-based position of this question within its passage group. */
  passageIndex?: number;
  /** Total questions sharing this passage. */
  passageTotal?: number;
}

export interface MathsQuizConfig {
  topic: string;
  questions: number;
  duration: number;
  /** Fixed 0-based start index in the question bank. When set, ignores progressive stored index. */
  from?: number;
}

export interface EnglishConfig {
  grammarPdf?: string;
  vocabPdf?: string;
  comprehensionPdf?: string;
  grammarMindmap?: string;
  vocabNotes?: string;
  grammarQuiz?: string;
  /** Display name for the grammar quiz (e.g. "Grammar", "Noun"). Defaults to "Grammar". */
  grammarQuizLabel?: string;
  /** Fixed 0-based start index in the grammar question bank. When set, ignores progressive stored index. */
  grammarQuizFrom?: number;
  comprehensionQuiz?: string;
}

export interface ReasoningConfig {
  topic: string;
  questions: number;
  duration: number;
  /** Optional display label (e.g. "Number Series Quiz"). Defaults to formatted topic name. */
  label?: string;
  /** Fixed 0-based start index in the question bank. When set, ignores progressive stored index. */
  from?: number;
}

export interface GkConfig {
  todayTopicPdf?: string;
  todayTopicPdf2?: string;
  todayMindmap?: string;
  todayNotes?: string;
  revisionQuiz?: string;
  revisionTopic?: string;
  /** Fixed 0-based start index in the revision bank. When set, ignores progressive stored index. */
  from?: number;
}

export interface DailyPlan {
  day: number;
  published: boolean;
  maths: MathsQuizConfig[];
  english: EnglishConfig;
  reasoning?: ReasoningConfig;
  /** Optional extra reasoning quizzes shown as separate task cards on the day page. */
  reasoningQuizzes?: ReasoningConfig[];
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

export interface VocabWord {
  id: string;
  /** The day this word is first introduced (1-75). */
  day: number;
  word: string;
  meaning: string;
  synonym: string;
  antonym: string;
  example: string;
  /** Hindi meaning. */
  hindi: string;
}

/**
 * Spaced-repetition state for a single vocabulary word.
 * `circles` mirrors the student's "put a circle on it" revision method —
 * each time a word can't be recalled, a circle (box level) is added and it
 * stays due for revision until it is finally mastered.
 */
export interface VocabWordProgress {
  wordId: string;
  /** Number of circles (times the student failed to recall it). */
  circles: number;
  /** True once the student has confidently recalled it. */
  mastered: boolean;
  /** Day the word was first learned. */
  learnedDay: number;
  /** Day it was last reviewed. */
  lastReviewedDay: number;
}
