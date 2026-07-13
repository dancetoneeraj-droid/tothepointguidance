import type { Question } from "@/types";

export type ReviewStatus = "correct" | "wrong" | "unattempted";

function normalizeQuestionId(id: string): string {
  return id.replace(/\s+/g, "").replace(/_+/g, "_");
}

export function getReviewQuestions(
  bank: Question[],
  questionIds: string[]
): Question[] {
  const lookup = new Map<string, Question>();
  const normalizedLookup = new Map<string, Question>();

  for (const question of bank) {
    if (!lookup.has(question.id)) {
      lookup.set(question.id, question);
    }
    const normalizedId = normalizeQuestionId(question.id);
    if (!normalizedLookup.has(normalizedId)) {
      normalizedLookup.set(normalizedId, question);
    }
  }

  return questionIds
    .map(
      (questionId) =>
        lookup.get(questionId) ??
        normalizedLookup.get(normalizeQuestionId(questionId))
    )
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
