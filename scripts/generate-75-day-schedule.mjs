/**
 * Generates data/schedule-75.json — 75 days, 4 maths quizzes/day (25 Q, 25 min).
 * Rules:
 * - Each topic introduced once, then mandatory repeat on day+2 (average: day+3)
 * - ~11 sessions per topic (~275 questions) across 75 days
 * - 4 different topics per day (shuffled order)
 */
import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const TOPICS = [
  { slug: "percentage", repeatGap: 2 },
  { slug: "ratio-proportion", repeatGap: 2 },
  { slug: "profit-loss", repeatGap: 2 },
  { slug: "time-work", repeatGap: 2 },
  { slug: "time-speed-distance", repeatGap: 2 },
  { slug: "average", repeatGap: 3 },
  { slug: "partnership", repeatGap: 2 },
  { slug: "mixture-alligation", repeatGap: 2 },
  { slug: "simple-interest", repeatGap: 2 },
  { slug: "compound-interest", repeatGap: 2 },
  { slug: "trigonometry", repeatGap: 2 },
  { slug: "di", repeatGap: 2 },
  { slug: "mensuration-3d", repeatGap: 2 },
  { slug: "algebra", repeatGap: 2 },
  { slug: "mensuration-2d", repeatGap: 2 },
  { slug: "geometry", repeatGap: 2 },
  { slug: "number-system", repeatGap: 2 },
];

const TOTAL_DAYS = 75;
const QUIZZES_PER_DAY = 4;
const SESSIONS_TARGET = 11;
const QUESTIONS = 25;
const DURATION = 25;

function seededShuffle(arr, seed) {
  const a = [...arr];
  let s = seed >>> 0;
  for (let i = a.length - 1; i > 0; i--) {
    s = (Math.imul(1664525, s) + 1013904223) >>> 0;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function countSessions(schedule, slug) {
  let n = 0;
  for (let d = 1; d <= TOTAL_DAYS; d++) {
    n += schedule[d].filter((t) => t === slug).length;
  }
  return n;
}

function ensureOnDay(schedule, day, slug) {
  if (day < 1 || day > TOTAL_DAYS) return;
  if (schedule[day].includes(slug)) return;
  if (schedule[day].length < QUIZZES_PER_DAY) {
    schedule[day].push(slug);
    return;
  }
  for (let i = QUIZZES_PER_DAY - 1; i >= 0; i--) {
    const other = schedule[day][i];
    const otherRepeatDay = topicMeta[other]?.repeatDay;
    if (otherRepeatDay !== day) {
      schedule[day][i] = slug;
      return;
    }
  }
  schedule[day][QUIZZES_PER_DAY - 1] = slug;
}

const topicMeta = {};
const schedule = Array.from({ length: TOTAL_DAYS + 1 }, () => []);

const introOrder = seededShuffle(TOPICS, 2026);
let idx = 0;
for (let d = 1; d <= TOTAL_DAYS && idx < TOPICS.length; d++) {
  while (schedule[d].length < QUIZZES_PER_DAY && idx < TOPICS.length) {
    const t = introOrder[idx++];
    schedule[d].push(t.slug);
    topicMeta[t.slug] = {
      firstDay: d,
      repeatDay: d + t.repeatGap,
      repeatGap: t.repeatGap,
    };
  }
}

for (const t of TOPICS) {
  const meta = topicMeta[t.slug];
  if (!meta) continue;
  ensureOnDay(schedule, meta.repeatDay, t.slug);
}

while (true) {
  const under = TOPICS.filter((t) => countSessions(schedule, t.slug) < SESSIONS_TARGET);
  if (under.length === 0) break;

  under.sort(
    (a, b) => countSessions(schedule, a.slug) - countSessions(schedule, b.slug)
  );
  const pick = under[0].slug;

  let placed = false;
  for (let d = 1; d <= TOTAL_DAYS; d++) {
    if (schedule[d].length >= QUIZZES_PER_DAY) continue;
    if (schedule[d].includes(pick)) continue;
    schedule[d].push(pick);
    placed = true;
    break;
  }

  if (!placed) {
    for (let d = 1; d <= TOTAL_DAYS; d++) {
      if (schedule[d].length < QUIZZES_PER_DAY) {
        schedule[d].push(pick);
        placed = true;
        break;
      }
    }
  }

  if (!placed) {
    console.warn("Could not place more sessions — all days full");
    break;
  }
}

for (let d = 1; d <= TOTAL_DAYS; d++) {
  while (schedule[d].length < QUIZZES_PER_DAY) {
    const candidate = TOPICS.sort(
      (a, b) => countSessions(schedule, a.slug) - countSessions(schedule, b.slug)
    ).find((t) => !schedule[d].includes(t.slug));
    schedule[d].push(candidate?.slug ?? TOPICS[0].slug);
  }
  if (schedule[d].length > QUIZZES_PER_DAY) {
    schedule[d] = schedule[d].slice(0, QUIZZES_PER_DAY);
  }
  schedule[d] = seededShuffle(schedule[d], d * 991);
}

const templateDay = JSON.parse(
  readFileSync(join(root, "data", "daily-plans", "day-1.json"), "utf-8")
);

const reasoningCycle = [
  { topic: "coding-decoding", questions: 50, duration: 45 },
  { topic: "puzzle", questions: 50, duration: 45 },
  { topic: "analogy", questions: 50, duration: 45 },
];

const plans = [];
for (let d = 1; d <= TOTAL_DAYS; d++) {
  const templateIndex = ((d - 1) % 8) + 1;
  let base;
  try {
    base = JSON.parse(
      readFileSync(
        join(root, "data", "daily-plans", `day-${templateIndex}.json`),
        "utf-8"
      )
    );
  } catch {
    base = templateDay;
  }

  plans.push({
    day: d,
    published: true,
    maths: schedule[d].map((topic) => ({
      topic,
      questions: QUESTIONS,
      duration: DURATION,
    })),
    english: base.english,
    reasoning: reasoningCycle[(d - 1) % reasoningCycle.length],
    gk: {
      ...base.gk,
      revisionQuiz: d > 1 ? "revision" : undefined,
      revisionTopic: d > 1 ? `Day ${d - 1} GK revision` : undefined,
    },
  });
}

const output = {
  programDays: TOTAL_DAYS,
  mathsQuiz: { questions: QUESTIONS, duration: DURATION },
  topicSessionsTarget: SESSIONS_TARGET,
  plans,
};

writeFileSync(
  join(root, "data", "schedule-75.json"),
  JSON.stringify(output, null, 2) + "\n",
  "utf-8"
);

console.log(`Generated ${TOTAL_DAYS}-day schedule → data/schedule-75.json`);
for (const t of TOPICS) {
  console.log(`  ${t.slug}: ${countSessions(schedule, t.slug)} sessions`);
}
