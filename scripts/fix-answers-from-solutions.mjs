/**
 * Align correctAnswer with the final **Answer:** stated in each solution.
 * Run: node scripts/fix-answers-from-solutions.mjs
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");
const mathsDir = join(root, "data", "maths");

const RANGES = [
  ["mensuration-3d", 100, 25],
  ["average", 100, 25],
  ["ratio-proportion", 100, 25],
  ["simple-interest", 100, 20],
  ["compound-interest", 100, 25],
  ["time-work", 150, 25],
  ["percentage", 150, 25],
  ["mixture-alligation", 150, 25],
];

function normalize(s) {
  return String(s)
    .trim()
    .replace(/\s+/g, " ")
    .replace(/[₹Rs.]/gi, "")
    .replace(/,/g, "")
    .toLowerCase();
}

function matchOption(text, options) {
  const t = normalize(text);
  for (const opt of options) {
    if (normalize(opt) === t) return opt;
  }
  for (const opt of options) {
    const o = normalize(opt);
    if (t.includes(o) || o.includes(t)) return opt;
  }
  const num = parseFloat(t.replace(/[^\d.-]/g, ""));
  if (!Number.isNaN(num)) {
    for (const opt of options) {
      const n = parseFloat(normalize(opt).replace(/[^\d.-]/g, ""));
      if (!Number.isNaN(n) && Math.abs(n - num) < 0.05) return opt;
    }
  }
  return null;
}

function extractAnswer(solution) {
  const matches = [...solution.matchAll(/\*\*Answer:?\s*([^*\n]+)\*\*/gi)];
  if (matches.length === 0) {
    const plain = [...solution.matchAll(/Answer:\s*([^\n]+)/gi)];
    if (plain.length === 0) return null;
    return plain[plain.length - 1][1].trim().replace(/[✓.]/g, "").trim();
  }
  return matches[matches.length - 1][1]
    .trim()
    .replace(/[✓.]/g, "")
    .replace(/\(option\s*\d+\)/gi, "")
    .trim();
}

let fixed = 0;
let unresolved = [];

for (const [topic, from, count] of RANGES) {
  const filePath = join(mathsDir, `${topic}.json`);
  const questions = JSON.parse(readFileSync(filePath, "utf8"));
  let changed = false;

  for (let i = from; i < from + count; i++) {
    const q = questions[i];
    if (!q?.solution) {
      unresolved.push(q?.id ?? `${topic}@${i}`);
      continue;
    }

    const extracted = extractAnswer(q.solution);
    if (!extracted) {
      unresolved.push(q.id);
      continue;
    }

    const matched = matchOption(extracted, q.options);
    if (matched && matched !== q.correctAnswer) {
      console.log(`  ${q.id}: ${q.correctAnswer} → ${matched}`);
      q.correctAnswer = matched;
      fixed++;
      changed = true;
    } else if (!matched) {
      unresolved.push(`${q.id} (extracted: ${extracted})`);
    }
  }

  if (changed) writeFileSync(filePath, JSON.stringify(questions, null, 2));
}

console.log(`\nFixed ${fixed} answers.`);
if (unresolved.length) {
  console.log(`Unresolved (${unresolved.length}):`);
  unresolved.forEach((u) => console.log(`  - ${u}`));
}
