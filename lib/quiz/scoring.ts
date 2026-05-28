import type { Question } from "@/types";

/** +2 marks per correct answer, −0.5 per wrong answer. Unanswered = 0 marks. */
export const MARKS_PER_CORRECT = 2;
export const MARKS_PER_WRONG = -0.5;

export interface QuizMarksBreakdown {
  correct: number;
  wrong: number;
  unanswered: number;
  total: number;
  score: number;
  maxScore: number;
  /** Percentage of maximum marks obtained (can be negative). */
  accuracy: number;
}

export function computeQuizMarks(
  questions: Question[],
  answers: Record<string, string>
): QuizMarksBreakdown {
  let correct = 0;
  let wrong = 0;
  let unanswered = 0;

  for (const q of questions) {
    const selected = answers[q.id];
    if (!selected) {
      unanswered++;
      continue;
    }
    if (selected === q.correctAnswer) {
      correct++;
    } else {
      wrong++;
    }
  }

  const total = questions.length;
  const score = correct * MARKS_PER_CORRECT + wrong * MARKS_PER_WRONG;
  const maxScore = total * MARKS_PER_CORRECT;
  const accuracy =
    maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;

  return {
    correct,
    wrong,
    unanswered,
    total,
    score,
    maxScore,
    accuracy,
  };
}

export function formatMarks(score: number): string {
  return Number.isInteger(score) ? String(score) : score.toFixed(1);
}
