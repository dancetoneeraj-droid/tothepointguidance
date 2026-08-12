/**
 * Import Problem-on-Ages PDF questions into data/maths/mixture-alligation.json
 * starting at mixture_alligation_185 (0-based index 184).
 *
 * Run:
 *   python scripts/parse-problems-on-ages-pdf.py
 *   node scripts/import-problems-on-ages.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "problems-on-ages.json");
const TARGET = join(root, "data", "maths", "mixture-alligation.json");
const START_INDEX = 184; // mixture_alligation_185

function normalize(raw, index) {
  const entry = {
    id: `mixture_alligation_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: (raw.correctAnswer || "").trim(),
    solution: raw.solution?.trim() || "video solution will be provided soon",
  };

  const questionHi = (raw.questionHindi || raw.questionHi || "").trim();
  if (questionHi) entry.questionHindi = questionHi;

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-problems-on-ages-pdf.py`);
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
    `(mixture_alligation_${String(START_INDEX + 1).padStart(3, "0")} …)`
);
