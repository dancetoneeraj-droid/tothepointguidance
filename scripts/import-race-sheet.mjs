/**
 * Import Race-Sheet PDF questions into data/maths/time-speed-distance.json
 * starting at maths_time_speed_distance_191 (0-based index 190).
 *
 * Run:
 *   python scripts/parse-race-sheet-pdf.py
 *   node scripts/import-race-sheet.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "race-sheet.json");
const TARGET = join(root, "data", "maths", "time-speed-distance.json");
const START_INDEX = 190; // maths_time_speed_distance_191

function normalize(raw, index) {
  const entry = {
    id: `maths_time_speed_distance_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: (raw.correctAnswer || "").trim(),
  };

  const questionHi = (raw.questionHindi || raw.questionHi || "").trim();
  if (questionHi) entry.questionHindi = questionHi;

  if (raw.solution?.trim()) entry.solution = raw.solution.trim();
  if (raw.explanation?.trim()) entry.explanation = raw.explanation.trim();

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-race-sheet-pdf.py`);
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
    `(maths_time_speed_distance_${String(START_INDEX + 1).padStart(3, "0")} …)`
);
