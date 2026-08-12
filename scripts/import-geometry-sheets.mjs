/**
 * Import geometry sheets 4-12 into data/maths/geometry.json
 * starting at maths_geometry_152 (0-based index 151).
 * Appends new entries if questions exceed existing bank length.
 *
 * Run:
 *   python scripts/parse-geometry-sheets.py
 *   node scripts/import-geometry-sheets.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "geometry", "all-sheets.json");
const TARGET = join(root, "data", "maths", "geometry.json");
const START_INDEX = 151; // maths_geometry_152

function normalize(raw, index) {
  const entry = {
    id: `maths_geometry_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: (raw.correctAnswer || raw.options[0] || "").trim(),
  };

  const questionHi = (raw.questionHindi || raw.questionHi || "").trim();
  if (questionHi) entry.questionHindi = questionHi;

  if (raw.explanation?.trim()) entry.explanation = raw.explanation.trim();
  if (raw.solution?.trim()) entry.solution = raw.solution.trim();

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-geometry-sheets.py`);
  process.exit(1);
}

const imported = JSON.parse(readFileSync(SOURCE, "utf8"));
const bank = JSON.parse(readFileSync(TARGET, "utf8"));

const needed = START_INDEX + imported.length;
while (bank.length < needed) {
  const idx = bank.length;
  bank.push({
    id: `maths_geometry_${String(idx + 1).padStart(3, "0")}`,
    question: `Geometry — Question ${idx + 1} (placeholder)`,
    options: ["Option A", "Option B", "Option C", "Option D"],
    correctAnswer: "Option A",
    explanation: "Placeholder for Geometry.",
  });
}

for (let i = 0; i < imported.length; i++) {
  bank[START_INDEX + i] = normalize(imported[i], START_INDEX + i);
}

writeFileSync(TARGET, JSON.stringify(bank, null, 2) + "\n", "utf-8");
console.log(
  `Imported ${imported.length} questions into ${TARGET} ` +
    `(maths_geometry_${String(START_INDEX + 1).padStart(3, "0")} … ` +
    `maths_geometry_${String(START_INDEX + imported.length).padStart(3, "0")})`
);
