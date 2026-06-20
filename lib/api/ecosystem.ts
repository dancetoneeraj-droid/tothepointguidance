import type { QuizRankingResult } from "@/lib/db/quiz-ranking";
import type { QuizReviewRecord } from "@/types";

const ANALYTICS_KEY = "tothepoint:last-quiz-analytics";

export type StoredQuizAnalytics = QuizReviewRecord;

export async function submitQuizToServer(payload: {
  studentId: string;
  displayName: string;
  email?: string;
  day: number;
  subject: string;
  topic: string;
  correct: number;
  total: number;
  accuracy: number;
  scoreMarks: number;
  timeSeconds: number;
  isRetry: boolean;
}): Promise<QuizRankingResult | null> {
  try {
    const res = await fetch("/api/quiz/attempt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) return null;
    return (await res.json()) as QuizRankingResult;
  } catch {
    return null;
  }
}

export async function syncStudentToServer(payload: {
  studentId: string;
  displayName: string;
  email?: string;
  currentDay: number;
  tasksCompleted: number;
  accuracy?: number;
  streak: number;
  completedTaskIds: string[];
}): Promise<void> {
  try {
    await fetch("/api/students/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch {
    // offline — ignore
  }
}

export function saveQuizAnalytics(data: StoredQuizAnalytics): void {
  if (typeof window === "undefined") return;
  try {
    sessionStorage.setItem(ANALYTICS_KEY, JSON.stringify(data));
  } catch {
    // ignore
  }
}

export function loadQuizAnalytics(): StoredQuizAnalytics | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = sessionStorage.getItem(ANALYTICS_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as StoredQuizAnalytics;
  } catch {
    return null;
  }
}
