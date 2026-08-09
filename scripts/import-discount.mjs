/**
 * Import Discount PDF questions into data/maths/profit-loss.json
 * starting at maths_profit_loss_160 (0-based index 159).
 *
 * Run:
 *   python scripts/parse-discount-pdf.py
 *   node scripts/import-discount.mjs
 */
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const SOURCE = join(root, "datas", "maths", "discount.json");
const TARGET = join(root, "data", "maths", "profit-loss.json");
const START_INDEX = 159; // maths_profit_loss_160
const MAX_SLOTS = 141; // 160..300 inclusive

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
    id: `maths_profit_loss_${String(index + 1).padStart(3, "0")}`,
    question: (raw.question || "").trim(),
    options: raw.options.map((o) => String(o).trim()),
    correctAnswer: correct,
  };

  const hindi = (raw.questionHindi || raw.questionHi || raw.question_hi || "").trim();
  if (hindi) entry.questionHindi = hindi;

  const explanation = raw.explanation?.trim();
  if (explanation) entry.explanation = explanation;

  return entry;
}

if (!existsSync(SOURCE)) {
  console.error(`Missing ${SOURCE} — run: python scripts/parse-discount-pdf.py`);
  process.exit(1);
}

const imported = JSON.parse(readFileSync(SOURCE, "utf8"));
const bank = JSON.parse(readFileSync(TARGET, "utf8"));
const count = Math.min(imported.length, MAX_SLOTS);

for (let i = 0; i < count; i++) {
  const targetIndex = START_INDEX + i;
  bank[targetIndex] = normalize(imported[i], targetIndex);
}

writeFileSync(TARGET, JSON.stringify(bank, null, 2) + "\n", "utf-8");
console.log(
  `Imported ${count} questions into ${TARGET} ` +
    `(maths_profit_loss_160 … maths_profit_loss_${String(START_INDEX + count).padStart(3, "0")})`
);
if (imported.length > MAX_SLOTS) {
  console.warn(`Note: ${imported.length - MAX_SLOTS} PDF question(s) did not fit (bank ends at 300).`);
}
