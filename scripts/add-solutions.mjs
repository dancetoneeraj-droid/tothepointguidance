/**
 * Generates step-by-step solutions for math quiz questions used in Days 1-10.
 * Run: node scripts/add-solutions.mjs
 *
 * Requires ANTHROPIC_API_KEY in .env.local
 * Skips questions that already have a solution field.
 * Saves progress after every question (safe to interrupt & resume).
 */

import Anthropic from "@anthropic-ai/sdk";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

// ── Load API key from .env.local ──────────────────────────────────────────────
function loadEnvKey() {
  const envPath = join(root, ".env.local");
  if (!existsSync(envPath)) return null;
  const lines = readFileSync(envPath, "utf8").split("\n");
  for (const line of lines) {
    const m = line.match(/^ANTHROPIC_API_KEY\s*=\s*(.+)$/);
    if (m) return m[1].trim().replace(/^["']|["']$/g, "");
  }
  return null;
}

const apiKey = process.env.ANTHROPIC_API_KEY || loadEnvKey();
if (!apiKey) {
  console.error(
    "\n❌ ANTHROPIC_API_KEY not found.\n" +
      "   Add it to .env.local:  ANTHROPIC_API_KEY=sk-ant-...\n" +
      "   Or set the env variable before running this script.\n"
  );
  process.exit(1);
}

const client = new Anthropic({ apiKey });

// Only the questions actually used in Days 1-10 quizzes (derived from schedule-75.json)
// [topic, upTo] — add solutions only for questions[0..upTo]
const DAY10_RANGES = [
  ["time-work", 75],
  ["percentage", 75],
  ["mixture-alligation", 75],
  ["mensuration-2d", 75],
  ["trigonometry", 75],
  ["profit-loss", 75],
  ["time-speed-distance", 75],
  ["number-system", 75],
  ["partnership", 50],
  ["geometry", 50],
  ["algebra", 50],
  ["di", 25],
  ["mensuration-3d", 50],
  ["average", 50],
  ["ratio-proportion", 50],
  ["simple-interest", 25],
  ["compound-interest", 25],
];

const TOPIC_LABELS = {
  algebra: "Algebra",
  average: "Average",
  "compound-interest": "Compound Interest",
  di: "Data Interpretation",
  geometry: "Geometry",
  "mensuration-2d": "2D Mensuration",
  "mensuration-3d": "3D Mensuration",
  "mixture-alligation": "Mixture & Alligation",
  "number-system": "Number System",
  partnership: "Partnership",
  percentage: "Percentage",
  "profit-loss": "Profit & Loss",
  "ratio-proportion": "Ratio & Proportion",
  "simple-interest": "Simple Interest",
  "time-speed-distance": "Time, Speed & Distance",
  "time-work": "Time & Work",
  trigonometry: "Trigonometry",
};

async function generateSolution(question, options, correctAnswer, topic) {
  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 350,
    messages: [
      {
        role: "user",
        content:
          `You are an SSC CGL math expert. Solve this ${topic} question with clear, concise steps (3-5 steps).\n\n` +
          `Question: ${question}\n` +
          `Options: ${options.join(" | ")}\n` +
          `Correct Answer: ${correctAnswer}\n\n` +
          `Give only the step-by-step solution. No intro line. End with the answer confirmation.`,
      },
    ],
  });
  return response.content[0].text.trim();
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function processFile(topic, upTo) {
  const filePath = join(root, "data", "maths", `${topic}.json`);
  const questions = JSON.parse(readFileSync(filePath, "utf8"));

  const slice = questions.slice(0, upTo);
  const missing = slice.filter((q) => !q.solution);

  if (missing.length === 0) {
    console.log(`  ✓ ${topic}.json — all ${upTo} day1-10 solutions already present`);
    return 0;
  }

  console.log(`\n📝 ${topic}.json — ${missing.length} of ${upTo} need solutions`);

  let done = 0;
  for (let i = 0; i < upTo; i++) {
    const q = questions[i];
    if (q.solution) continue;

    try {
      q.solution = await generateSolution(
        q.question,
        q.options,
        q.correctAnswer,
        TOPIC_LABELS[topic]
      );
      done++;
      writeFileSync(filePath, JSON.stringify(questions, null, 2));
      process.stdout.write(`\r  [${done}/${missing.length}] ${q.id}   `);
      await sleep(150);
    } catch (err) {
      console.error(`\n  ⚠ Error on ${q.id}: ${err.message}. Retrying in 5s…`);
      await sleep(5000);
      i--;
    }
  }

  console.log(`\n  ✅ ${topic}.json done — ${done} solutions added`);
  return done;
}

async function main() {
  const total = DAY10_RANGES.reduce((s, [, n]) => s + n, 0);
  console.log(`🚀 Adding solutions for Days 1-10 questions (~${total} questions across 17 topics)…\n`);

  const start = Date.now();
  let totalAdded = 0;

  for (const [topic, upTo] of DAY10_RANGES) {
    totalAdded += await processFile(topic, upTo);
  }

  const elapsed = ((Date.now() - start) / 60000).toFixed(1);
  console.log(
    `\n🎉 Done! ${totalAdded} solutions added in ${elapsed} min.`
  );
}

main().catch((err) => {
  console.error("\n❌ Fatal error:", err.message);
  process.exit(1);
});
