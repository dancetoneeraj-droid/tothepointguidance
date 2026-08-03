/**
 * Solves Day 23 & Day 24 maths questions independently, updates correctAnswer,
 * and writes step-by-step solutions.
 *
 * Run: node scripts/add-solutions-day23-24.mjs
 * Requires ANTHROPIC_API_KEY in .env.local
 *
 * Clears existing solutions in target ranges before regenerating.
 * Saves after every question (safe to interrupt & resume).
 */

import Anthropic from "@anthropic-ai/sdk";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

function loadEnvKey() {
  const envPath = join(root, ".env.local");
  if (!existsSync(envPath)) return null;
  for (const line of readFileSync(envPath, "utf8").split("\n")) {
    const m = line.match(/^ANTHROPIC_API_KEY\s*=\s*(.+)$/);
    if (m) return m[1].trim().replace(/^["']|["']$/g, "");
  }
  return null;
}

const apiKey = process.env.ANTHROPIC_API_KEY || loadEnvKey();
if (!apiKey) {
  console.error("\n❌ ANTHROPIC_API_KEY not found in .env.local\n");
  process.exit(1);
}

const client = new Anthropic({ apiKey });

// [topic, from, count] — derived from schedule-75.json days 23 & 24
const RANGES = [
  // Day 23
  ["mensuration-3d", 100, 25],
  ["average", 100, 25],
  ["ratio-proportion", 100, 25],
  ["simple-interest", 100, 20],
  // Day 24
  ["compound-interest", 100, 25],
  ["time-work", 150, 25],
  ["percentage", 150, 25],
  ["mixture-alligation", 150, 25],
];

const TOPIC_LABELS = {
  average: "Average",
  "compound-interest": "Compound Interest",
  "mensuration-3d": "3D Mensuration",
  "mixture-alligation": "Mixture & Alligation",
  percentage: "Percentage",
  "ratio-proportion": "Ratio & Proportion",
  "simple-interest": "Simple Interest",
  "time-work": "Time & Work",
};

function normalize(s) {
  return String(s)
    .trim()
    .replace(/\s+/g, " ")
    .replace(/₹/g, "")
    .replace(/,/g, "")
    .toLowerCase();
}

function matchOption(computed, options) {
  const c = normalize(computed);
  for (const opt of options) {
    if (normalize(opt) === c) return opt;
  }
  for (const opt of options) {
    const o = normalize(opt);
    if (o.includes(c) || c.includes(o)) return opt;
  }
  const num = parseFloat(c.replace(/[^\d.-]/g, ""));
  if (!Number.isNaN(num)) {
    for (const opt of options) {
      const n = parseFloat(normalize(opt).replace(/[^\d.-]/g, ""));
      if (!Number.isNaN(n) && Math.abs(n - num) < 0.02) return opt;
    }
  }
  return null;
}

function parseJson(text) {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  let raw = fenced ? fenced[1].trim() : text.trim();
  // Strip trailing commas before closing braces
  raw = raw.replace(/,\s*}/g, "}").replace(/,\s*]/g, "]");
  try {
    return JSON.parse(raw);
  } catch {
    // Fallback: extract answer and solution fields manually
    const answerMatch = raw.match(/"answer"\s*:\s*"((?:\\.|[^"\\])*)"/);
    const solMatch = raw.match(/"solution"\s*:\s*"((?:\\.|[^"\\])*)"/s);
    if (answerMatch && solMatch) {
      return {
        answer: JSON.parse('"' + answerMatch[1] + '"'),
        solution: JSON.parse('"' + solMatch[1] + '"'),
      };
    }
    throw new Error("Could not parse JSON response");
  }
}

function pickOption(parsed, options) {
  // Prefer numeric option index (1-based)
  if (parsed.optionIndex !== undefined) {
    const idx = Number(parsed.optionIndex) - 1;
    if (idx >= 0 && idx < options.length) return options[idx];
  }
  if (parsed.answer !== undefined) {
    const matched = matchOption(parsed.answer, options);
    if (matched) return matched;
  }
  throw new Error(`Could not match answer to options: ${options.join(" | ")}`);
}

async function solveQuestion(question, options, topic) {
  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 800,
    messages: [
      {
        role: "user",
        content:
          `You are an SSC CGL maths expert. Solve this ${topic} question independently.\n` +
          `Do NOT trust any pre-marked answer — compute from scratch.\n\n` +
          `Question:\n${question}\n\n` +
          `Options (pick exactly one):\n${options.map((o, i) => `${i + 1}. ${o}`).join("\n")}\n\n` +
          `Respond with ONLY valid JSON:\n` +
          `{\n` +
          `  "optionIndex": <1-4 number of the correct option>,\n` +
          `  "answer": "<exact text of the chosen option>",\n` +
          `  "solution": "<3-6 step markdown solution ending with **Answer: ...**>"\n` +
          `}`,
      },
    ],
  });

  const text = response.content[0].text.trim();
  const parsed = parseJson(text);
  const matched = pickOption(parsed, options);
  return { correctAnswer: matched, solution: parsed.solution.trim() };
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function processRange(topic, from, count) {
  const filePath = join(root, "data", "maths", `${topic}.json`);
  const questions = JSON.parse(readFileSync(filePath, "utf8"));
  const label = TOPIC_LABELS[topic] ?? topic;

  console.log(`\n📝 ${topic}.json [${from}–${from + count - 1}]`);

  let done = 0;
  let skipped = 0;
  for (let i = from; i < from + count; i++) {
    const q = questions[i];
    if (!q) {
      console.error(`  ⚠ Missing question at index ${i}`);
      continue;
    }

    // Only process questions missing a solution
    if (q.solution) {
      skipped++;
      continue;
    }

    let attempts = 0;
    while (attempts < 3) {
      try {
        const result = await solveQuestion(q.question, q.options, label);
        const prev = q.correctAnswer;
        q.correctAnswer = result.correctAnswer;
        q.solution = result.solution;
        if (prev !== result.correctAnswer) {
          console.log(`\n  ↪ ${q.id}: ${prev} → ${result.correctAnswer}`);
        }
        writeFileSync(filePath, JSON.stringify(questions, null, 2));
        done++;
        process.stdout.write(`\r  [${done}/${count}] ${q.id}   `);
        await sleep(200);
        break;
      } catch (err) {
        attempts++;
        if (attempts >= 3) {
          console.error(`\n  ⚠ Failed ${q.id} after 3 attempts: ${err.message}`);
        } else {
          await sleep(3000);
        }
      }
    }
  }

  console.log(`\n  ✅ ${topic}.json — ${done} added, ${skipped} already had solutions`);
  return done;
}

async function main() {
  const total = RANGES.reduce((s, [, , c]) => s + c, 0);
  console.log(`🚀 Solving Day 23 & 24 maths (${total} questions)…\n`);

  const start = Date.now();
  let processed = 0;
  for (const [topic, from, count] of RANGES) {
    processed += await processRange(topic, from, count);
  }

  const elapsed = ((Date.now() - start) / 60000).toFixed(1);
  console.log(`\n🎉 Done! ${processed} questions processed in ${elapsed} min.`);
}

main().catch((err) => {
  console.error("\n❌ Fatal:", err.message);
  process.exit(1);
});
