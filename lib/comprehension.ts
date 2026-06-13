import comprehensionData from "@/data/english/comprehension.json";

export interface ComprehensionQuestion {
  question: string;
  options: string[];
  answer: string;
  explanation?: string;
}

export interface RcSection {
  title: string;
  directions: string;
  passage: string;
  questions: ComprehensionQuestion[];
}

export interface ClozeSection {
  title: string;
  directions: string;
  passage: string;
  questions: ComprehensionQuestion[];
}

export interface ParajumblePart {
  label: string;
  text: string;
}

export interface ParajumbleItem {
  parts: ParajumblePart[];
  options: string[];
  answer: string;
  explanation?: string;
}

export interface ParajumbleSection {
  title: string;
  directions: string;
  items: ParajumbleItem[];
}

export interface ComprehensionDay {
  rc?: RcSection;
  cloze?: ClozeSection;
  parajumble?: ParajumbleSection;
}

/** SSC-style marking. */
export const MARK_CORRECT = 2;
export const MARK_WRONG = -0.5;

const DATA = comprehensionData as Record<string, ComprehensionDay>;

export function hasComprehensionForDay(day: number): boolean {
  return Boolean(DATA[String(day)]);
}

export function getComprehensionForDay(day: number): ComprehensionDay | null {
  return DATA[String(day)] ?? null;
}

/** A single answerable item, flattened across all three sections for scoring. */
export interface FlatQuestion {
  key: string;
  answer: string;
}

export function getFlatQuestions(set: ComprehensionDay): FlatQuestion[] {
  const flat: FlatQuestion[] = [];
  set.rc?.questions.forEach((q, i) => flat.push({ key: `rc-${i}`, answer: q.answer }));
  set.cloze?.questions.forEach((q, i) =>
    flat.push({ key: `cloze-${i}`, answer: q.answer })
  );
  set.parajumble?.items.forEach((item, i) =>
    flat.push({ key: `pj-${i}`, answer: item.answer })
  );
  return flat;
}

export interface ScoreResult {
  total: number;
  correct: number;
  wrong: number;
  unattempted: number;
  marks: number;
  maxMarks: number;
  accuracy: number;
}

export function scoreComprehension(
  set: ComprehensionDay,
  answers: Record<string, string>
): ScoreResult {
  const flat = getFlatQuestions(set);
  let correct = 0;
  let wrong = 0;
  let unattempted = 0;

  for (const q of flat) {
    const selected = answers[q.key];
    if (!selected) {
      unattempted += 1;
    } else if (selected === q.answer) {
      correct += 1;
    } else {
      wrong += 1;
    }
  }

  const total = flat.length;
  const attempted = correct + wrong;
  const marks = correct * MARK_CORRECT + wrong * MARK_WRONG;

  return {
    total,
    correct,
    wrong,
    unattempted,
    marks,
    maxMarks: total * MARK_CORRECT,
    accuracy: attempted > 0 ? Math.round((correct / attempted) * 100) : 0,
  };
}
