import type { LocalStudentStore } from "@/lib/storage/types";
import { comprehensionRecordId, quizCompletionId } from "@/lib/storage/client";

export interface ParsedQuizCompletionId {
  day: number;
  subject: string;
  topic: string;
  from?: number;
}

/** Parse ids like day6-maths-algebra-f25 or day6-gk-revision. */
export function parseQuizCompletionId(
  quizId: string
): ParsedQuizCompletionId | null {
  const match = quizId.match(/^day(\d+)-(\w+)-(.+)$/);
  if (!match) return null;

  const day = parseInt(match[1]!, 10);
  const subject = match[2]!;
  let topic = match[3]!;
  let from: number | undefined;

  const fromMatch = topic.match(/-f(\d+)$/);
  if (fromMatch) {
    from = parseInt(fromMatch[1]!, 10);
    topic = topic.slice(0, -fromMatch[0].length);
  }

  return { day, subject, topic, from };
}

export function isQuizIdCompleted(
  store: LocalStudentStore,
  day: number,
  subject: string,
  topic: string,
  from?: number
): boolean {
  const id = quizCompletionId(day, subject, topic, from);
  return (store.completedQuizzes ?? []).includes(id);
}

function dayHasSubjectQuiz(
  store: LocalStudentStore,
  day: number,
  subject: string
): boolean {
  return (store.completedQuizzes ?? []).some((id) => {
    const parsed = parseQuizCompletionId(id);
    return parsed?.day === day && parsed.subject === subject;
  });
}

/**
 * Align dayProgress flags with completedQuizzes so UI never shows
 * "View result" when the official attempt was reset.
 */
export function reconcileProgressWithCompletions(
  store: LocalStudentStore
): LocalStudentStore {
  const completed = new Set(store.completedQuizzes ?? []);
  const dayProgress = { ...(store.dayProgress ?? {}) };

  for (const [dayKey, dp] of Object.entries(dayProgress)) {
    const day = dp.day ?? parseInt(dayKey, 10);
    const maths = { ...dp.maths };

    for (const [topic, entry] of Object.entries(maths)) {
      const stillDone = [...completed].some((id) => {
        const parsed = parseQuizCompletionId(id);
        return (
          parsed?.day === day &&
          parsed.subject === "maths" &&
          parsed.topic === topic
        );
      });
      if (entry.completed && !stillDone) {
        maths[topic] = { ...entry, completed: false };
      } else if (!entry.completed && stillDone) {
        maths[topic] = { ...entry, completed: true };
      }
    }

    const reasoningDone = dayHasSubjectQuiz(store, day, "reasoning");
    const englishQuizDone = dayHasSubjectQuiz(store, day, "english");
    const vocabDone = (store.vocabDaysCompleted ?? []).includes(day);
    const comprehensionDone = Boolean(
      store.comprehensionRecords?.[comprehensionRecordId(day)]
    );
    const gkRevisionDone = [...completed].some((id) => {
      const parsed = parseQuizCompletionId(id);
      return (
        parsed?.day === day &&
        parsed.subject === "gk" &&
        parsed.topic === "revision"
      );
    });

    dayProgress[dayKey] = {
      ...dp,
      maths,
      reasoning: {
        ...dp.reasoning,
        completed: reasoningDone,
      },
      english: {
        grammar: englishQuizDone,
        vocabulary: vocabDone,
        comprehension: comprehensionDone,
      },
      gk: {
        ...dp.gk,
        revisionQuizCompleted: gkRevisionDone,
      },
      completed: false,
    };
  }

  const englishProgress = { ...(store.englishProgress ?? {}) };
  const gkProgress = { ...(store.gkProgress ?? {}) };
  for (const [dayKey, dp] of Object.entries(dayProgress)) {
    englishProgress[dayKey] = dp.english;
    gkProgress[dayKey] = dp.gk;
  }

  return {
    ...store,
    dayProgress,
    englishProgress,
    gkProgress,
  };
}

/** Remove one quiz attempt and all related dayProgress flags. */
export function clearQuizCompletion(
  store: LocalStudentStore,
  quizId: string
): LocalStudentStore {
  const parsed = parseQuizCompletionId(quizId);
  if (!parsed) {
    return reconcileProgressWithCompletions({
      ...store,
      completedQuizzes: (store.completedQuizzes ?? []).filter((id) => id !== quizId),
      quizReviewRecords: Object.fromEntries(
        Object.entries(store.quizReviewRecords ?? {}).filter(([k]) => k !== quizId)
      ),
      updatedAt: new Date().toISOString(),
    });
  }

  const { day, subject, topic } = parsed;
  const dayKey = String(day);
  const next: LocalStudentStore = {
    ...store,
    completedQuizzes: (store.completedQuizzes ?? []).filter((id) => id !== quizId),
    quizReviewRecords: Object.fromEntries(
      Object.entries(store.quizReviewRecords ?? {}).filter(([k]) => k !== quizId)
    ),
    updatedAt: new Date().toISOString(),
  };

  const dp = next.dayProgress?.[dayKey];
  if (dp) {
    const dayProgress = { ...next.dayProgress! };
    const entry = { ...dp };

    if (subject === "maths" && entry.maths[topic]) {
      entry.maths = {
        ...entry.maths,
        [topic]: { ...entry.maths[topic]!, completed: false },
      };
    } else if (subject === "reasoning") {
      entry.reasoning = { ...entry.reasoning, completed: false };
    } else if (subject === "english") {
      entry.english = { ...entry.english, grammar: false };
      next.englishProgress = {
        ...(next.englishProgress ?? {}),
        [dayKey]: entry.english,
      };
    } else if (subject === "gk" && topic === "revision") {
      entry.gk = { ...entry.gk, revisionQuizCompleted: false };
      next.gkProgress = {
        ...(next.gkProgress ?? {}),
        [dayKey]: entry.gk,
      };
    }

    dayProgress[dayKey] = entry;
    next.dayProgress = dayProgress;
  }

  return reconcileProgressWithCompletions(next);
}
