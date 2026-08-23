import type { DayProgress } from "@/types";
import { hasComprehensionForDay } from "@/lib/comprehension";
import { getDailyPlan } from "@/lib/daily-plans";
import { hasAnyDeckForDay } from "@/lib/study-decks";

export interface DaySectionAvailability {
  grammar: boolean;
  vocabulary: boolean;
  comprehension: boolean;
  reasoning: boolean;
  gkMaterials: boolean;
  gkRevision: boolean;
}

/** Which section types are actually scheduled for this day. */
export function getDaySectionAvailability(day: number): DaySectionAvailability {
  const plan = getDailyPlan(day);
  if (!plan) {
    return {
      grammar: false,
      vocabulary: false,
      comprehension: false,
      reasoning: false,
      gkMaterials: false,
      gkRevision: false,
    };
  }

  return {
    grammar: !!(
      plan.english.grammarPdf ||
      plan.english.grammarQuiz ||
      plan.english.grammarMindmap ||
      (plan.english.grammarQuizzes?.length ?? 0) > 0
    ),
    vocabulary: hasAnyDeckForDay(day),
    comprehension:
      hasComprehensionForDay(day) || !!plan.english.comprehensionPdf,
    reasoning:
      !!plan.reasoning || (plan.reasoningQuizzes?.length ?? 0) > 0,
    gkMaterials: !!(
      plan.gk.todayTopicPdf ||
      plan.gk.todayTopicPdf2 ||
      plan.gk.todayTopicPdf3 ||
      plan.gk.todayTopicPdf4 ||
      plan.gk.todayMindmap ||
      plan.gk.todayNotes
    ),
    gkRevision: day > 1 && !!plan.gk.revisionQuiz,
  };
}

/** Treat unscheduled sections as complete so they never block the day page. */
export function applySectionDefaultsToDayProgress(
  day: number,
  dp: DayProgress
): DayProgress {
  const avail = getDaySectionAvailability(day);

  return {
    ...dp,
    day,
    english: {
      grammar: dp.english.grammar || !avail.grammar,
      vocabulary: dp.english.vocabulary || !avail.vocabulary,
      comprehension: dp.english.comprehension || !avail.comprehension,
    },
    reasoning: {
      ...dp.reasoning,
      completed: dp.reasoning.completed || !avail.reasoning,
    },
    gk: {
      materialsCompleted: dp.gk.materialsCompleted || !avail.gkMaterials,
      revisionQuizCompleted:
        dp.gk.revisionQuizCompleted || !avail.gkRevision,
    },
  };
}

export function createEmptyDayProgress(day: number): DayProgress {
  return applySectionDefaultsToDayProgress(day, {
    day,
    maths: {},
    english: { grammar: false, vocabulary: false, comprehension: false },
    reasoning: { currentIndex: 0, completed: false },
    gk: { materialsCompleted: false, revisionQuizCompleted: false },
    completed: false,
  });
}
