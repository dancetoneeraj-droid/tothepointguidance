import type { Question, Subject } from "@/types";

type RawPuzzleQuestion = {
  question: string;
  options: string[];
  correctAnswer: string;
  explanation?: string;
};

type RawPuzzleSet = {
  id: string;
  passage: string;
  questions: RawPuzzleQuestion[];
};

function flattenPuzzleSets(sets: RawPuzzleSet[]): Question[] {
  const questions: Question[] = [];
  sets.forEach((set) => {
    const total = set.questions.length;
    set.questions.forEach((q, qIdx) => {
      questions.push({
        id: `${set.id}_q${qIdx + 1}`,
        question: q.question,
        options: q.options,
        correctAnswer: q.correctAnswer,
        explanation: q.explanation,
        passage: set.passage,
        passageIndex: qIdx + 1,
        passageTotal: total,
      });
    });
  });
  return questions;
}

import percentageQuestions from "@/data/maths/percentage.json";
import ratioProportionQuestions from "@/data/maths/ratio-proportion.json";
import profitLossQuestions from "@/data/maths/profit-loss.json";
import timeWorkQuestions from "@/data/maths/time-work.json";
import timeSpeedDistanceQuestions from "@/data/maths/time-speed-distance.json";
import averageQuestions from "@/data/maths/average.json";
import partnershipQuestions from "@/data/maths/partnership.json";
import mixtureAlligationQuestions from "@/data/maths/mixture-alligation.json";
import simpleInterestQuestions from "@/data/maths/simple-interest.json";
import compoundInterestQuestions from "@/data/maths/compound-interest.json";
import trigonometryQuestions from "@/data/maths/trigonometry.json";
import diQuestions from "@/data/maths/di.json";
import mensuration3dQuestions from "@/data/maths/mensuration-3d.json";
import algebraQuestions from "@/data/maths/algebra.json";
import mensuration2dQuestions from "@/data/maths/mensuration-2d.json";
import geometryQuestions from "@/data/maths/geometry.json";
import numberSystemQuestions from "@/data/maths/number-system.json";

import codingDecodingQuestions from "@/data/reasoning/coding-decoding.json";
import puzzleQuestions from "@/data/reasoning/puzzle.json";
import seatingArrangementRaw from "@/data/reasoning/seating-arrangement.json";
import analogyQuestions from "@/data/reasoning/analogy.json";
import nsQuestionsRaw from "@/data/reasoning/ns.json";

import gkRevisionQuestions from "@/data/gk/revision.json";
import nounQuestionsRaw from "@/datas/maths/noun.json";
import noun2Questions from "@/data/english/noun2.json";
import pronounQuestions from "@/data/english/pronoun.json";
import spellingErrorQuestions from "@/data/english/spelling-error.json";

type RawLetterBasedQuestion = {
  question: string;
  options: string[];
  correctAnswer: string;
  explanation?: string;
};

function normalizeLetterAnswerQuestions(
  questions: RawLetterBasedQuestion[],
  prefix: string
): Question[] {
  const letterIndexMap: Record<string, number> = {
    A: 0,
    B: 1,
    C: 2,
    D: 3,
    E: 4,
  };

  const normalized: Question[] = [];

  questions.forEach((question, index) => {
      const letter = question.correctAnswer?.trim().toUpperCase();
      const mappedIndex = letterIndexMap[letter];
      const fallback = question.options[0];
      const correctAnswer = question.options[mappedIndex] ?? fallback;
      const options = question.options.filter(Boolean);

      if (!question.question || options.length < 2 || !correctAnswer) {
        return;
      }

      normalized.push({
        id: `${prefix}_${String(index + 1).padStart(3, "0")}`,
        question: question.question,
        options,
        correctAnswer,
        explanation: question.explanation,
      });
    });

  return normalized;
}

const MATHS_BANKS: Record<string, Question[]> = {
  percentage: percentageQuestions as Question[],
  "ratio-proportion": ratioProportionQuestions as Question[],
  "profit-loss": profitLossQuestions as Question[],
  "time-work": timeWorkQuestions as Question[],
  "time-speed-distance": timeSpeedDistanceQuestions as Question[],
  average: averageQuestions as Question[],
  partnership: partnershipQuestions as Question[],
  "mixture-alligation": mixtureAlligationQuestions as Question[],
  "simple-interest": simpleInterestQuestions as Question[],
  "compound-interest": compoundInterestQuestions as Question[],
  trigonometry: trigonometryQuestions as Question[],
  di: diQuestions as Question[],
  "mensuration-3d": mensuration3dQuestions as Question[],
  algebra: algebraQuestions as Question[],
  "mensuration-2d": mensuration2dQuestions as Question[],
  geometry: geometryQuestions as Question[],
  "number-system": numberSystemQuestions as Question[],
};

const REASONING_BANKS: Record<string, Question[]> = {
  "coding-decoding": codingDecodingQuestions as Question[],
  puzzle: puzzleQuestions as Question[],
  "seating-arrangement": flattenPuzzleSets(seatingArrangementRaw as RawPuzzleSet[]),
  analogy: analogyQuestions as Question[],
  ns: normalizeLetterAnswerQuestions(
    nsQuestionsRaw as RawLetterBasedQuestion[],
    "reasoning_ns"
  ),
};

const GK_BANKS: Record<string, Question[]> = {
  revision: gkRevisionQuestions as Question[],
};

const ENGLISH_BANKS: Record<string, Question[]> = {
  noun: normalizeLetterAnswerQuestions(
    nounQuestionsRaw as RawLetterBasedQuestion[],
    "english_noun"
  ),
  noun2: noun2Questions as Question[],
  pronoun: pronounQuestions as Question[],
  "spelling-error": spellingErrorQuestions as Question[],
};

export function getQuestionBank(
  subject: Subject,
  topic: string
): Question[] {
  switch (subject) {
    case "maths":
      return MATHS_BANKS[topic] ?? [];
    case "reasoning":
      return REASONING_BANKS[topic] ?? [];
    case "gk":
      return GK_BANKS[topic] ?? GK_BANKS.revision ?? [];
    case "english":
      return ENGLISH_BANKS[topic] ?? [];
    default:
      return [];
  }
}

export function sliceQuestions(
  bank: Question[],
  startIndex: number,
  count: number
): { questions: Question[]; startIndex: number; endIndex: number } {
  const questions = bank.slice(startIndex, startIndex + count);
  return {
    questions,
    startIndex,
    endIndex: startIndex + questions.length,
  };
}

export function getTopicKey(subject: Subject, topic: string): string {
  return `${subject}_${topic}`;
}
