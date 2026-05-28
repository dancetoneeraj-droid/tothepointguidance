import type { Question } from "@/types";

export type ReviewStatus = "correct" | "wrong" | "unattempted";

export function getReviewQuestions(
  bank: Question[],
  questionIds: string[]
): Question[] {
  const lookup = new Map(bank.map((question) => [question.id, question]));
  return questionIds
    .map((questionId) => lookup.get(questionId))
    .filter((question): question is Question => Boolean(question));
}

export function getReviewStatus(
  question: Question,
  answers: Record<string, string>
): ReviewStatus {
  const selected = answers[question.id];
  if (!selected) return "unattempted";
  return selected === question.correctAnswer ? "correct" : "wrong";
}
