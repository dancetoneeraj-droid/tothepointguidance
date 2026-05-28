/**
 * Import Simple Interest question sets into data/maths/simple-interest.json
 * - Set 1 (simple-interest1.json) → indices 0–29 (Day 1 quiz)
 * - Set 2 (simple-interest2.json) → indices 30–59 (Day 2 quiz)
 * Pads set 1 to 30 if fewer than 30 questions; fills days 3–8 with placeholders.
 */
import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SET1_SOURCE = join(root, "datas", "maths", "simple-interest1.json");
const SET2_SOURCE = join(root, "datas", "maths", "simple-interest2.json");
const TARGET = join(root, "data", "maths", "simple-interest.json");

const QUESTIONS_PER_SET = 30;
const PUBLISHED_DAYS = 8;
const BANK_SIZE = PUBLISHED_DAYS * QUESTIONS_PER_SET;

function letterToOption(letter, options) {
  const idx = letter.toUpperCase().charCodeAt(0) - 65;
  if (idx < 0 || idx >= options.length) return letter;
  return options[idx];
}

function normalize(raw, globalIndex) {
  let correct = raw.correctAnswer?.trim() ?? "";
  if (/^[A-D]$/i.test(correct)) {
    correct = letterToOption(correct, raw.options);
  }

  return {
    id: `maths_simple_interest_${String(globalIndex + 1).padStart(3, "0")}`,
    question: raw.question.trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: correct,
    explanation: raw.explanation?.replace(/\n---\s*$/, "").trim() || undefined,
  };
}

function makePlaceholder(globalIndex, setNumber, localNum) {
  return {
    id: `maths_simple_interest_${String(globalIndex + 1).padStart(3, "0")}`,
    question: `[Add content] Simple Interest Set ${setNumber} — Question ${localNum}`,
    options: ["Option A", "Option B", "Option C", "Option D"],
    correctAnswer: "Option A",
    explanation: "Replace with real question content.",
  };
}

function loadSet(path, setNumber) {
  const raw = JSON.parse(readFileSync(path, "utf-8"));
  if (!Array.isArray(raw)) {
    throw new Error(`${path} must be a JSON array`);
  }

  const baseIndex = (setNumber - 1) * QUESTIONS_PER_SET;
  const normalized = raw.map((q, i) => normalize(q, baseIndex + i));

  while (normalized.length < QUESTIONS_PER_SET) {
    const localNum = normalized.length + 1;
    const globalIndex = baseIndex + normalized.length;
    normalized.push(makePlaceholder(globalIndex, setNumber, localNum));
  }

  return normalized.slice(0, QUESTIONS_PER_SET);
}

const set1 = loadSet(SET1_SOURCE, 1);
const set2 = loadSet(SET2_SOURCE, 2);

const bank = [...set1, ...set2];

while (bank.length < BANK_SIZE) {
  const globalIndex = bank.length;
  const setNumber = Math.floor(globalIndex / QUESTIONS_PER_SET) + 1;
  const localNum = (globalIndex % QUESTIONS_PER_SET) + 1;
  bank.push(makePlaceholder(globalIndex, setNumber, localNum));
}

writeFileSync(TARGET, JSON.stringify(bank, null, 2) + "\n", "utf-8");

console.log(`Set 1: ${set1.length} questions (Day 1 Simple Interest)`);
console.log(`Set 2: ${set2.length} questions (Day 2 Simple Interest)`);
console.log(`Bank size: ${bank.length} → ${TARGET}`);
