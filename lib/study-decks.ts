import type { VocabWord, VocabWordProgress } from "@/types";
import vocabData from "@/data/english/vocab.json";
import idiomData from "@/data/english/idioms.json";
import owsData from "@/data/english/ows.json";

export type StudyCategory = "vocab" | "idiom" | "ows";

export interface StudyCardDetail {
  label: string;
  value: string;
  tone?: "default" | "emerald" | "rose";
  italic?: boolean;
}

/** A single normalized revision card shared across all three decks. */
export interface StudyCard {
  id: string;
  day: number;
  category: StudyCategory;
  /** The prompt shown before the meaning is revealed. */
  front: string;
  /** Small caption under the front prompt. */
  frontHint?: string;
  /** Detail rows shown once the student reveals the answer. */
  details: StudyCardDetail[];
}

interface IdiomEntry {
  id: string;
  day: number;
  idiom: string;
  meaning: string;
}

interface OwsEntry {
  id: string;
  day: number;
  word: string;
  meaning: string;
}

export const CATEGORY_META: Record<
  StudyCategory,
  { label: string; tabLabel: string; promptHint: string }
> = {
  vocab: {
    label: "Vocabulary",
    tabLabel: "View Vocab",
    promptHint: "Recall the meaning, then reveal.",
  },
  idiom: {
    label: "Idioms & Phrases",
    tabLabel: "View Idiom",
    promptHint: "Recall what this idiom means, then reveal.",
  },
  ows: {
    label: "One Word Substitution",
    tabLabel: "View One Word",
    promptHint: "Recall the one word for this definition, then reveal.",
  },
};

function buildVocabCards(): StudyCard[] {
  return (vocabData as VocabWord[]).map((w) => ({
    id: w.id,
    day: w.day,
    category: "vocab" as const,
    front: w.word,
    details: [
      { label: "Meaning", value: w.meaning },
      { label: "Hindi", value: w.hindi },
      { label: "Synonym", value: w.synonym, tone: "emerald" as const },
      { label: "Antonym", value: w.antonym, tone: "rose" as const },
      { label: "Example", value: w.example, italic: true },
    ],
  }));
}

function buildIdiomCards(): StudyCard[] {
  return (idiomData as IdiomEntry[]).map((e) => ({
    id: e.id,
    day: e.day,
    category: "idiom" as const,
    front: e.idiom,
    details: [{ label: "Meaning", value: e.meaning }],
  }));
}

function buildOwsCards(): StudyCard[] {
  return (owsData as OwsEntry[]).map((e) => ({
    id: e.id,
    day: e.day,
    category: "ows" as const,
    // For one-word substitution the student sees the definition and recalls
    // the single word — so the definition is the front of the card.
    front: e.meaning,
    frontHint: "What is the one word for this?",
    details: [{ label: "One word", value: e.word, tone: "emerald" as const }],
  }));
}

const DECKS: Record<StudyCategory, StudyCard[]> = {
  vocab: buildVocabCards().sort((a, b) => a.day - b.day || a.id.localeCompare(b.id)),
  idiom: buildIdiomCards().sort((a, b) => a.day - b.day || a.id.localeCompare(b.id)),
  ows: buildOwsCards().sort((a, b) => a.day - b.day || a.id.localeCompare(b.id)),
};

export function getMaxDayForCategory(category: StudyCategory): number {
  return DECKS[category].reduce((max, c) => Math.max(max, c.day), 0);
}

export function hasDeckForDay(category: StudyCategory, day: number): boolean {
  return DECKS[category].some((c) => c.day === day);
}

/** True when any of the three decks has cards for this day. */
export function hasAnyDeckForDay(day: number): boolean {
  return (
    hasDeckForDay("vocab", day) ||
    hasDeckForDay("idiom", day) ||
    hasDeckForDay("ows", day)
  );
}

export function getCardById(
  category: StudyCategory,
  id: string
): StudyCard | undefined {
  return DECKS[category].find((c) => c.id === id);
}

function getNewCardsForDay(category: StudyCategory, day: number): StudyCard[] {
  return DECKS[category].filter((c) => c.day === day);
}

/**
 * Cards introduced on earlier days that are still circled (not yet mastered) —
 * the spaced-repetition "circle" pool.
 */
function getReviewCardsForDay(
  category: StudyCategory,
  day: number,
  progress: Record<string, VocabWordProgress>
): StudyCard[] {
  return DECKS[category].filter((c) => {
    if (c.day >= day) return false;
    const p = progress[c.id];
    return Boolean(p) && !p!.mastered;
  });
}

export interface StudyDeck {
  reviewCards: StudyCard[];
  newCards: StudyCard[];
}

/** Builds the deck for a day: circled cards to revise first, then the new set. */
export function getDeckForDay(
  category: StudyCategory,
  day: number,
  progress: Record<string, VocabWordProgress>
): StudyDeck {
  return {
    reviewCards: getReviewCardsForDay(category, day, progress),
    newCards: getNewCardsForDay(category, day),
  };
}

export function isStudyCategory(value: string | null): value is StudyCategory {
  return value === "vocab" || value === "idiom" || value === "ows";
}
