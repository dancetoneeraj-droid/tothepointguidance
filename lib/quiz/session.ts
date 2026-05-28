import type { Question } from "@/types";
import { sliceQuestions } from "@/lib/quiz-loader";

/**
 * Sequential progression per topic (250–300 questions across 75 days).
 * Each quiz takes the next `count` questions from the student's stored index.
 */
export function resolveQuizSlice(
  bank: Question[],
  storedIndex: number,
  count: number
) {
  const setStart = storedIndex;
  const sliced = sliceQuestions(bank, setStart, count);
  const questions = sliced.questions.slice(0, count);

  return {
    questions,
    setStart,
    endIndex: setStart + questions.length,
    requestedCount: count,
    isPartial: questions.length < count,
  };
}

export function computeNextIndex(
  storedIndex: number,
  setStart: number,
  questionCount: number,
  bankLength: number,
  advance: boolean
): number {
  if (!advance) {
    return storedIndex;
  }
  return Math.min(Math.max(storedIndex, setStart + questionCount), bankLength);
}

export function buildSessionId(
  subject: string,
  topic: string,
  day: number,
  setStart: number
): string {
  return `${subject}-${topic}-d${day}-s${setStart}-official`;
}
