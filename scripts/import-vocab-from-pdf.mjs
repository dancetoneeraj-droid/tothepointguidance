/**
 * Import vocab from extracted PDF TSV (GLOBAL_NUM|WORD|MEANING|EXAMPLE)
 * and append to data/english/vocab.json for days 22+.
 *
 * Day 21 = PDF words 1-30 (already in vocab.json as v601-v630).
 * Day N  = PDF words ((N-21)*30+1) .. ((N-20)*30), starting day 22 at word 31.
 *
 * Run: node scripts/import-vocab-from-pdf.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const VOCAB_PATH = join(ROOT, "data", "english", "vocab.json");
const TSV_PATH = join(ROOT, "datas", "English", "vocab-extracted.tsv");

const PER_DAY = 30;
const START_DAY = 21; // PDF word 1 maps to day 21
const START_ID = 600; // v601 = word 1
const MAX_DAY = 75; // 75-day schedule

function parseTsv(raw) {
  const entries = new Map();
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const parts = trimmed.split("|");
    if (parts.length < 3) continue;
    const num = parseInt(parts[0], 10);
    if (!Number.isFinite(num)) continue;
    entries.set(num, {
      word: parts[1].trim(),
      meaning: parts[2].trim(),
      example: (parts[3] ?? "").trim(),
    });
  }
  return entries;
}

function firstSynonym(meaning) {
  const primary = meaning.split(/[,;]/)[0].trim();
  return primary || meaning;
}

function makeExample(word, example) {
  if (example) return example;
  return `The word "${word}" is commonly tested in SSC exams.`;
}

function wordToDay(globalNum) {
  return START_DAY + Math.floor((globalNum - 1) / PER_DAY);
}

function wordToId(globalNum) {
  return `v${String(START_ID + globalNum).padStart(3, "0")}`;
}

function buildCard(globalNum, entry) {
  const day = wordToDay(globalNum);
  const meaning = entry.meaning.replace(/\s+/g, " ").trim();
  return {
    id: wordToId(globalNum),
    day,
    word: entry.word,
    meaning,
    synonym: firstSynonym(meaning),
    antonym: "—",
    example: makeExample(entry.word, entry.example),
    hindi: "—",
  };
}

const existing = JSON.parse(readFileSync(VOCAB_PATH, "utf8"));
const tsv = readFileSync(TSV_PATH, "utf8");
const extracted = parseTsv(tsv);

const maxGlobal = MAX_DAY - START_DAY + 1;
const lastWordNum = maxGlobal * PER_DAY; // word 1650 for day 75

const newCards = [];
for (let n = 31; n <= lastWordNum; n++) {
  const entry = extracted.get(n);
  if (!entry) {
    console.warn(`Missing word #${n} (day ${wordToDay(n)})`);
    continue;
  }
  newCards.push(buildCard(n, entry));
}

const merged = [...existing, ...newCards];
writeFileSync(VOCAB_PATH, JSON.stringify(merged, null, 2) + "\n");

const days = new Set(newCards.map((c) => c.day));
console.log(
  `Added ${newCards.length} cards for days ${Math.min(...days)}–${Math.max(...days)} (v631–v${START_ID + lastWordNum})`
);
console.log(`Total vocab: ${merged.length} cards`);
