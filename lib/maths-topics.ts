export type MathsTopicCategory = "arithmetic" | "advance";

export interface MathsTopicDefinition {
  slug: string;
  label: string;
  category: MathsTopicCategory;
  /** Days after first appearance when topic must repeat (Average → 4th day = gap 3). */
  repeatGap: number;
  targetSessions: number;
}

/** 17 SSC CGL maths topics — ~275 questions each (11 × 25) over 75 days. */
export const MATHS_TOPICS: MathsTopicDefinition[] = [
  { slug: "percentage", label: "Percentage", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "ratio-proportion", label: "Ratio and Proportion", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "profit-loss", label: "Profit and Loss", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "time-work", label: "Time and Work", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "time-speed-distance", label: "Time, Speed and Distance", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "average", label: "Average", category: "arithmetic", repeatGap: 3, targetSessions: 11 },
  { slug: "partnership", label: "Partnership", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "mixture-alligation", label: "Mixture and Alligation", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "simple-interest", label: "Simple Interest", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "compound-interest", label: "Compound Interest", category: "arithmetic", repeatGap: 2, targetSessions: 11 },
  { slug: "trigonometry", label: "Trigonometry", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "di", label: "Data Interpretation", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "mensuration-3d", label: "3D Mensuration", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "algebra", label: "Algebra", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "mensuration-2d", label: "2D Mensuration", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "geometry", label: "Geometry", category: "advance", repeatGap: 2, targetSessions: 11 },
  { slug: "number-system", label: "Number System", category: "advance", repeatGap: 2, targetSessions: 11 },
];

export const MATHS_QUIZ_QUESTIONS = 25;
export const MATHS_QUIZ_DURATION = 25;
export const PROGRAM_DAYS = 75;

export function getMathsTopic(slug: string): MathsTopicDefinition | undefined {
  return MATHS_TOPICS.find((t) => t.slug === slug);
}

export function formatMathsTopic(slug: string): string {
  return getMathsTopic(slug)?.label ?? slug;
}
