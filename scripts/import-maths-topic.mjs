/**
 * Import datas/maths/{topic}.json → data/maths/{topic}.json
 * Usage: node scripts/import-maths-topic.mjs percentage
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const topicArg = process.argv[2];
if (!topicArg) {
  console.error("Usage: node scripts/import-maths-topic.mjs <topic-slug>");
  console.error("  e.g. percentage | mensuration-2d | 2d");
  process.exit(1);
}

/** CLI shorthand → canonical quiz topic slug */
const TOPIC_ALIASES = {
  "2d": "mensuration-2d",
  "3d": "mensuration-3d",
  tw: "time-work",
  ma: "mixture-alligation",
};

const topic = TOPIC_ALIASES[topicArg] ?? topicArg;

/** Canonical slug → possible datas/maths/*.json filenames (first match wins) */
const SOURCE_FILES = {
  "mensuration-2d": ["mensuration-2d", "2d"],
  "mensuration-3d": ["mensuration-3d", "3d"],
  "time-work": ["time-work", "tw"],
  "mixture-alligation": ["mixture-alligation", "ma"],
};

const BANK_SIZE = 300;
const targetDir = join(root, "data", "maths");
const targetPath = join(targetDir, `${topic}.json`);

function resolveSourcePath() {
  const names = SOURCE_FILES[topic] ?? [topic];
  for (const name of names) {
    const p = join(root, "datas", "maths", `${name}.json`);
    if (existsSync(p)) return p;
  }
  return join(root, "datas", "maths", `${topic}.json`);
}

const sourcePath = resolveSourcePath();

function letterToOption(letter, options) {
  const idx = letter.toUpperCase().charCodeAt(0) - 65;
  if (idx < 0 || idx >= options.length) return letter;
  return options[idx];
}

function normalize(raw, index) {
  let correct = raw.correctAnswer?.trim() ?? "";
  if (/^[A-D]$/i.test(correct)) {
    correct = letterToOption(correct, raw.options);
  }
  const prefix = `maths_${topic.replace(/-/g, "_")}`;
  const questionHi = (raw.questionHi || raw.question_hi || "").trim();
  const optionsHi = Array.isArray(raw.optionsHi)
    ? raw.optionsHi.map((o) => String(o).trim())
    : Array.isArray(raw.options_hi)
      ? raw.options_hi.map((o) => String(o).trim())
      : undefined;

  const entry = {
    id: `${prefix}_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || raw.questionEn || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: correct,
    explanation: raw.explanation?.trim() || undefined,
  };

  if (questionHi) entry.questionHi = questionHi;
  if (optionsHi?.length) entry.optionsHi = optionsHi;
  const explanationHi = (raw.explanationHi || raw.explanation_hi || "").trim();
  if (explanationHi) entry.explanationHi = explanationHi;

  return entry;
}

if (!existsSync(sourcePath)) {
  console.error(`Missing ${sourcePath}`);
  process.exit(1);
}

const raw = JSON.parse(readFileSync(sourcePath, "utf-8"));
if (!Array.isArray(raw)) {
  console.error("Source must be a JSON array");
  process.exit(1);
}

const imported = raw.map((q, i) => normalize(q, i));
mkdirSync(targetDir, { recursive: true });

let bank = imported;
if (bank.length < BANK_SIZE) {
  const prefix = `maths_${topic.replace(/-/g, "_")}`;
  while (bank.length < BANK_SIZE) {
    const n = bank.length + 1;
    bank.push({
      id: `${prefix}_${String(n).padStart(3, "0")}`,
      question: `[Add content] ${topic} — Question ${n}`,
      options: ["Option A", "Option B", "Option C", "Option D"],
      correctAnswer: "Option A",
      explanation: "Replace with real SSC CGL question.",
    });
  }
}

writeFileSync(targetPath, JSON.stringify(bank, null, 2) + "\n", "utf-8");
console.log(
  `Imported ${imported.length} from ${sourcePath} → ${targetPath} (bank size ${bank.length})`
);
