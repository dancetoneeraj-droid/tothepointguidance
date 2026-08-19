import type { Question } from "@/types";
/**
 * Sequential progression per topic (250–300 questions across 75 days).
 * Each quiz takes the next `count` questions from the student's stored index.
 */
export function resolveQuizSlice(
  bank: Question[],
  storedIndex: number,
  count: number
) {
  if (bank.length === 0) {
    return {
      questions: [],
      setStart: 0,
      endIndex: 0,
      requestedCount: count,
      isPartial: true,
    };
  }

  // Wrap when the schedule offset or student cursor moves past the bank end —
  // otherwise later reasoning days load zero questions.
  const setStart =
    ((storedIndex % bank.length) + bank.length) % bank.length;
  const questions: Question[] = [];
  let idx = setStart;

  while (questions.length < count) {
    questions.push(bank[idx % bank.length]);
    idx++;
  }

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
