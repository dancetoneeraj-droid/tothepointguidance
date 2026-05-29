import type { VocabWord, VocabWordProgress } from "@/types";
import vocabData from "@/data/english/vocab.json";

const ALL_VOCAB: VocabWord[] = (vocabData as VocabWord[])
  .slice()
  .sort((a, b) => a.day - b.day || a.id.localeCompare(b.id));

const VOCAB_BY_ID: Record<string, VocabWord> = Object.fromEntries(
  ALL_VOCAB.map((word) => [word.id, word])
);

/** Highest day for which vocabulary words exist. */
export const MAX_VOCAB_DAY = ALL_VOCAB.reduce(
  (max, word) => Math.max(max, word.day),
  0
);

export function hasVocabForDay(day: number): boolean {
  return ALL_VOCAB.some((word) => word.day === day);
}

export function getWordById(id: string): VocabWord | undefined {
  return VOCAB_BY_ID[id];
}

/** The new words introduced on a given day. */
export function getNewWordsForDay(day: number): VocabWord[] {
  return ALL_VOCAB.filter((word) => word.day === day);
}

/**
 * Words from earlier days that the student still needs to revise —
 * i.e. they were circled before and are not yet mastered.
 */
export function getReviewWordsForDay(
  day: number,
  vocabProgress: Record<string, VocabWordProgress>
): VocabWord[] {
  return ALL_VOCAB.filter((word) => {
    if (word.day >= day) return false;
    const progress = vocabProgress[word.id];
    return Boolean(progress) && !progress!.mastered;
  });
}

export interface VocabDayDeck {
  reviewWords: VocabWord[];
  newWords: VocabWord[];
  masteredCount: number;
}

/** Builds the full deck for a day: words to revise first, then the new set. */
export function getVocabDeckForDay(
  day: number,
  vocabProgress: Record<string, VocabWordProgress>
): VocabDayDeck {
  const reviewWords = getReviewWordsForDay(day, vocabProgress);
  const newWords = getNewWordsForDay(day);
  const masteredCount = Object.values(vocabProgress).filter(
    (progress) => progress.mastered
  ).length;

  return { reviewWords, newWords, masteredCount };
}
