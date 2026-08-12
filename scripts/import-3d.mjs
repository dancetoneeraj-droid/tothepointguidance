/**
 * Import 3D mensuration PDF questions into data/maths/mensuration-3d.json
 * starting at maths_mensuration_cylinder_138 (0-based index 137).
 *
 * Run:
 *   python scripts/parse-3d-pdf.py
 *   node scripts/import-3d.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "3d.json");
const TARGET = join(root, "data", "maths", "mensuration-3d.json");
const START_INDEX = 137; // maths_mensuration_cylinder_138

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
    id: `maths_mensuration_cylinder_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: correct,
  };

  const questionHi = (raw.questionHindi || raw.questionHi || raw.question_hi || "").trim();
  if (questionHi) entry.questionHindi = questionHi;

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-3d-pdf.py`);
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
    `(maths_mensuration_cylinder_${String(START_INDEX + 1).padStart(3, "0")} …)`
);
