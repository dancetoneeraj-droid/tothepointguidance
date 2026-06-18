"use client";

import type {
  DayProgress,
  OverrideRecord,
  QuizReviewRecord,
  StudentProgress,
  VocabWordProgress,
} from "@/types";
import { GUEST_STUDENT_ID } from "./constants";
import {
  getActiveStudentId,
  loadStore,
  quizCompletionId,
  saveStore,
  setActiveStudentId,
} from "./client";
import type { LocalStudentStore } from "./types";

function createDefaultStore(
  uid: string,
  profile: {
    displayName: string;
    email: string;
    phone?: string;
    photoURL?: string;
    isGuest?: boolean;
  }
): LocalStudentStore {
  const now = new Date().toISOString();
  return {
    version: 1,
    uid,
    displayName: profile.displayName,
    email: profile.email,
    phone: profile.phone,
    photoURL: profile.photoURL,
    isGuest: profile.isGuest ?? uid === GUEST_STUDENT_ID,
    currentDay: 1,
    unlockedDay: 1,
    completedDays: [],
    completedQuizzes: [],
    quizReviewRecords: {},
    vocabProgress: {},
    vocabDaysCompleted: [],
    overrideHistory: [],
    mathsProgress: {},
    reasoningProgress: {},
    englishProgress: {},
    gkProgress: {},
    dayProgress: {},
    streak: 0,
    totalQuestionsSolved: 0,
    totalCorrect: 0,
    accuracy: 0,
    topicIndices: {},
    createdAt: now,
    updatedAt: now,
  };
}

function ensureStoreCollections(store: LocalStudentStore): LocalStudentStore {
  if (!store.quizReviewRecords) {
    store.quizReviewRecords = {};
  }
  if (!store.vocabProgress) {
    store.vocabProgress = {};
  }
  if (!store.vocabDaysCompleted) {
    store.vocabDaysCompleted = [];
  }
  return store;
}

export function storeToStudentProgress(store: LocalStudentStore): StudentProgress {
  return {
    uid: store.uid,
    displayName: store.displayName,
    email: store.email,
    phone: store.phone,
    photoURL: store.photoURL,
    currentDay: store.currentDay,
    unlockedDay: store.unlockedDay,
    completedDays: store.completedDays,
    streak: store.streak,
    totalQuestionsSolved: store.totalQuestionsSolved,
    totalCorrect: store.totalCorrect,
    accuracy: store.accuracy,
    topicIndices: store.topicIndices,
    overrides: store.overrideHistory,
    lastStudyDate: store.lastStudyDate,
    createdAt: store.createdAt,
    updatedAt: store.updatedAt,
  };
}

function getStore(studentId: string): LocalStudentStore {
  const existing = loadStore(studentId);
  if (existing) return ensureStoreCollections(existing);
  const created = createDefaultStore(studentId, {
    displayName: studentId === GUEST_STUDENT_ID ? "Guest Student" : "Student",
    email: studentId === GUEST_STUDENT_ID ? "guest@local" : "",
    isGuest: studentId === GUEST_STUDENT_ID,
  });
  saveStore(created);
  return created;
}

export async function getStudentProgress(
  studentId: string
): Promise<StudentProgress | null> {
  const store = loadStore(studentId);
  if (!store) return null;
  return storeToStudentProgress(ensureStoreCollections(store));
}

export async function initStudentProgress(
  studentId: string,
  profile: {
    displayName: string;
    email: string;
    phone?: string;
    photoURL?: string;
    isGuest?: boolean;
  }
): Promise<StudentProgress> {
  const existing = loadStore(studentId);
  if (existing) {
    ensureStoreCollections(existing);
    if (profile.displayName && !existing.isGuest) {
      existing.displayName = profile.displayName;
      existing.email = profile.email;
      if (profile.photoURL) existing.photoURL = profile.photoURL;
      saveStore(existing);
    }
    return storeToStudentProgress(existing);
  }
  const store = createDefaultStore(studentId, profile);
  saveStore(store);
  return storeToStudentProgress(store);
}

function ensureDayInStore(store: LocalStudentStore, day: number): DayProgress {
  const key = String(day);
  if (store.dayProgress[key]) return store.dayProgress[key]!;

  const dayProgress: DayProgress = {
    day,
    maths: {},
    english: store.englishProgress[key] ?? {
      grammar: false,
      vocabulary: false,
      comprehension: false,
    },
    reasoning: { currentIndex: 0, completed: false },
    gk: store.gkProgress[key] ?? {
      materialsCompleted: false,
      revisionQuizCompleted: false,
    },
    completed: false,
  };

  store.dayProgress[key] = dayProgress;
  store.englishProgress[key] = dayProgress.english;
  store.gkProgress[key] = dayProgress.gk;
  return dayProgress;
}

export async function getDayProgress(
  studentId: string,
  day: number
): Promise<DayProgress | null> {
  const store = loadStore(studentId);
  if (!store) return null;
  const key = String(day);
  if (store.dayProgress[key]) return store.dayProgress[key]!;
  return ensureDayInStore(store, day);
}

export async function ensureDayProgress(
  studentId: string,
  day: number
): Promise<DayProgress> {
  const store = getStore(studentId);
  const dp = ensureDayInStore(store, day);
  saveStore(store);
  return dp;
}

export interface RecordQuizOptions {
  /** When false, topic index stays put. Default true. */
  advanceIndex?: boolean;
  /** When false, global solved/correct totals are not incremented again. Default true. */
  countInStats?: boolean;
}

export async function recordQuizCompletion(
  studentId: string,
  day: number,
  subject: "maths" | "reasoning" | "gk" | "english",
  topic: string,
  result: {
    correct: number;
    total: number;
    newIndex: number;
    score: number;
    accuracy: number;
  },
  options: RecordQuizOptions = {}
): Promise<void> {
  const { advanceIndex = true, countInStats = true } = options;
  const store = getStore(studentId);
  const topicKey = `${subject}_${topic}`;
  const quizId = quizCompletionId(day, subject, topic);

  if (advanceIndex) {
    store.topicIndices[topicKey] = result.newIndex;
    if (subject === "maths") {
      store.mathsProgress[topic] = result.newIndex;
    } else if (subject === "reasoning") {
      store.reasoningProgress[topic] = result.newIndex;
    }
  }

  if (countInStats) {
    store.totalQuestionsSolved += result.total;
    store.totalCorrect += result.correct;
    store.accuracy =
      store.totalQuestionsSolved > 0
        ? Math.round((store.totalCorrect / store.totalQuestionsSolved) * 100)
        : 0;
  }

  if (!store.completedQuizzes.includes(quizId)) {
    store.completedQuizzes.push(quizId);
  }

  const dayProgress = ensureDayInStore(store, day);

  const scoreUpdate = {
    lastScore: result.score,
    lastAccuracy: result.accuracy,
  };

  if (subject === "maths") {
    const prev = dayProgress.maths[topic];
    dayProgress.maths[topic] = {
      currentIndex: advanceIndex ? result.newIndex : (prev?.currentIndex ?? result.newIndex),
      completed: true,
      ...scoreUpdate,
    };
  } else if (subject === "reasoning") {
    dayProgress.reasoning = {
      currentIndex: advanceIndex
        ? result.newIndex
        : dayProgress.reasoning.currentIndex,
      completed: true,
      ...scoreUpdate,
    };
  } else if (subject === "gk") {
    dayProgress.gk.revisionQuizCompleted = true;
    store.gkProgress[String(day)] = dayProgress.gk;
  } else {
    dayProgress.english.grammar = true;
    store.englishProgress[String(day)] = dayProgress.english;
  }

  store.dayProgress[String(day)] = dayProgress;
  saveStore(store);
}

export function saveQuizReviewRecord(
  studentId: string,
  record: QuizReviewRecord
): void {
  const store = getStore(studentId);
  store.quizReviewRecords[record.quizId] = record;
  saveStore(store);
}

export function getQuizReviewRecord(
  studentId: string,
  day: number,
  subject: string,
  topic: string
): QuizReviewRecord | null {
  const store = loadStore(studentId);
  if (!store) return null;
  const normalized = ensureStoreCollections(store);
  return normalized.quizReviewRecords[quizCompletionId(day, subject, topic)] ?? null;
}

export function hasCompletedQuiz(
  studentId: string,
  day: number,
  subject: string,
  topic: string
): boolean {
  const store = loadStore(studentId);
  if (!store) return false;
  const quizId = quizCompletionId(day, subject, topic);
  return store.completedQuizzes.includes(quizId);
}

export function getVocabProgress(
  studentId: string
): Record<string, VocabWordProgress> {
  const store = loadStore(studentId);
  if (!store) return {};
  return ensureStoreCollections(store).vocabProgress;
}

export function isVocabDayCompleted(studentId: string, day: number): boolean {
  const store = loadStore(studentId);
  if (!store) return false;
  return ensureStoreCollections(store).vocabDaysCompleted.includes(day);
}

/**
 * Records a single word review using the "circle" method:
 * - `knew = true`  → word is mastered (removed from the daily revision pool).
 * - `knew = false` → add a circle; it stays due for revision on later days.
 */
export function recordVocabReview(
  studentId: string,
  wordId: string,
  knew: boolean,
  day: number,
  learnedDay: number
): void {
  const store = getStore(studentId);
  const existing = store.vocabProgress[wordId];

  const next: VocabWordProgress = {
    wordId,
    circles: existing?.circles ?? 0,
    mastered: knew,
    learnedDay: existing?.learnedDay ?? learnedDay,
    lastReviewedDay: day,
  };

  if (!knew) {
    next.circles = (existing?.circles ?? 0) + 1;
  }

  store.vocabProgress[wordId] = next;
  saveStore(store);
}

export function markVocabDayCompleted(studentId: string, day: number): void {
  const store = getStore(studentId);
  if (!store.vocabDaysCompleted.includes(day)) {
    store.vocabDaysCompleted.push(day);
  }

  // Reflect completion in the day's English vocabulary section.
  const dayProgress = ensureDayInStore(store, day);
  dayProgress.english.vocabulary = true;
  store.englishProgress[String(day)] = dayProgress.english;
  store.dayProgress[String(day)] = dayProgress;

  saveStore(store);
}

export async function markEnglishSection(
  studentId: string,
  day: number,
  section: "grammar" | "vocabulary" | "comprehension"
): Promise<void> {
  const store = getStore(studentId);
  const dayProgress = ensureDayInStore(store, day);
  dayProgress.english[section] = true;
  store.englishProgress[String(day)] = dayProgress.english;
  store.dayProgress[String(day)] = dayProgress;
  saveStore(store);
}

export async function markGkMaterials(
  studentId: string,
  day: number
): Promise<void> {
  const store = getStore(studentId);
  const dayProgress = ensureDayInStore(store, day);
  dayProgress.gk.materialsCompleted = true;
  store.gkProgress[String(day)] = dayProgress.gk;
  store.dayProgress[String(day)] = dayProgress;
  saveStore(store);
}

export async function markGkRevisionComplete(
  studentId: string,
  day: number
): Promise<void> {
  const store = getStore(studentId);
  const dayProgress = ensureDayInStore(store, day);
  dayProgress.gk.revisionQuizCompleted = true;
  store.gkProgress[String(day)] = dayProgress.gk;
  store.dayProgress[String(day)] = dayProgress;
  saveStore(store);
}

/** Override: unlock only the immediate next day (unlockedDay + 1). */
export async function recordOverride(
  studentId: string,
  record: OverrideRecord
): Promise<void> {
  const store = getStore(studentId);
  const targetDay = record.toDay;

  if (targetDay !== store.unlockedDay + 1) {
    return;
  }

  store.overrideHistory.push(record);
  store.unlockedDay = targetDay;
  store.currentDay = Math.max(store.currentDay, targetDay);
  saveStore(store);
}

export async function unlockNextDay(
  studentId: string,
  day: number
): Promise<void> {
  const store = getStore(studentId);

  if (day !== store.unlockedDay) return;

  const nextDay = day + 1;
  if (!store.completedDays.includes(day)) {
    store.completedDays.push(day);
  }

  const dayProgress = ensureDayInStore(store, day);
  dayProgress.completed = true;
  dayProgress.completedAt = new Date().toISOString();
  store.dayProgress[String(day)] = dayProgress;

  store.unlockedDay = nextDay;
  store.currentDay = nextDay;

  updateStreakInStore(store);
  saveStore(store);
}

function updateStreakInStore(store: LocalStudentStore): void {
  const today = new Date().toISOString().split("T")[0]!;
  const lastDate = store.lastStudyDate;

  if (!lastDate) {
    store.streak = 1;
  } else {
    const last = new Date(lastDate);
    const now = new Date(today);
    const diffDays = Math.floor(
      (now.getTime() - last.getTime()) / (1000 * 60 * 60 * 24)
    );
    if (diffDays === 0) {
      // keep streak
    } else if (diffDays === 1) {
      store.streak += 1;
    } else {
      store.streak = 1;
    }
  }
  store.lastStudyDate = today;
}

export function getTopicIndex(
  progress: StudentProgress,
  subject: string,
  topic: string
): number {
  const key = `${subject}_${topic}`;
  return progress.topicIndices[key] ?? 0;
}

export function activateGuestSession(): StudentProgress {
  setActiveStudentId(GUEST_STUDENT_ID);
  const store = getStore(GUEST_STUDENT_ID);
  saveStore(store);
  return storeToStudentProgress(store);
}

export function activateStudentSession(studentId: string): StudentProgress {
  setActiveStudentId(studentId);
  const store = getStore(studentId);
  saveStore(store);
  return storeToStudentProgress(store);
}

export function loadActiveStudentProgress(): StudentProgress | null {
  const id = getActiveStudentId();
  if (!id) return null;
  const store = loadStore(id);
  if (!store) return null;
  return storeToStudentProgress(ensureStoreCollections(store));
}
