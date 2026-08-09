/**
 * Import Trigonometry2 PDF questions into data/maths/trigonometry.json
 * starting at maths_trigonometry_156 (0-based index 155).
 *
 * Run:
 *   python scripts/parse-trigonometry2-pdf.py
 *   node scripts/import-trigonometry2.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "trigonometry2.json");
const TARGET = join(root, "data", "maths", "trigonometry.json");
const START_INDEX = 155; // maths_trigonometry_156

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

  const entry = {
    id: `maths_trigonometry_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: correct,
  };

  const questionHi = (raw.questionHi || raw.question_hi || "").trim();
  if (questionHi) entry.questionHi = questionHi;

  const explanation = raw.explanation?.trim();
  if (explanation) entry.explanation = explanation;

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-trigonometry2-pdf.py`);
  process.exit(1);
}

const imported = JSON.parse(readFileSync(SOURCE, "utf8"));
if (!Array.isArray(imported)) {
  console.error("Source must be a JSON array");
  process.exit(1);
}

const bank = JSON.parse(readFileSync(TARGET, "utf8"));

for (let i = 0; i < imported.length; i++) {
  const targetIndex = START_INDEX + i;
  if (targetIndex >= bank.length) {
    console.warn(`Bank ends at ${bank.length}; skipping remaining imports`);
    break;
  }
  bank[targetIndex] = normalize(imported[i], targetIndex);
}

writeFileSync(TARGET, JSON.stringify(bank, null, 2) + "\n", "utf-8");
console.log(
  `Imported ${imported.length} questions into ${TARGET} ` +
    `(maths_trigonometry_${String(START_INDEX + 1).padStart(3, "0")} …)`
);
