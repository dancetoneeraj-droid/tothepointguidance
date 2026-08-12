/**
 * Solve geometry sheet questions (maths_geometry_152 onward).
 *
 * Run:
 *   node scripts/add-solutions-geometry-sheets.mjs
 * Requires ANTHROPIC_API_KEY in .env.local
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
  console.error("\nANTHROPIC_API_KEY not found in .env.local\n");
  process.exit(1);
}

const client = new Anthropic({ apiKey });

const START_INDEX = 151;
const COUNT = 472;

function normalize(s) {
  return String(s).trim().replace(/\s+/g, " ").replace(/,/g, "").toLowerCase();
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
  return null;
}

function parseJson(text) {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  let raw = fenced ? fenced[1].trim() : text.trim();
  raw = raw.replace(/,\s*}/g, "}").replace(/,\s*]/g, "]");
  try {
    return JSON.parse(raw);
  } catch {
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

async function solveQuestion(question, options) {
  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 900,
    messages: [
      {
        role: "user",
        content:
          "You are an SSC CGL Geometry expert. Solve independently.\n" +
          "Do NOT trust pre-marked answers. Use π=22/7 unless stated.\n" +
          "For triangle/ circle/ similarity problems use standard theorems.\n\n" +
          `Question:\n${question}\n\n` +
          `Options:\n${options.map((o, i) => `${i + 1}. ${o}`).join("\n")}\n\n` +
          "Respond ONLY with JSON:\n" +
          '{"optionIndex":1-4,"answer":"exact option text","solution":"markdown ending **Answer: ...**"}',
      },
    ],
  });
  const parsed = parseJson(response.content[0].text.trim());
  return { correctAnswer: pickOption(parsed, options), solution: parsed.solution.trim() };
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const filePath = join(root, "data", "maths", "geometry.json");
  const questions = JSON.parse(readFileSync(filePath, "utf8"));
  const end = Math.min(START_INDEX + COUNT, questions.length);
  const missing = [];
  for (let i = START_INDEX; i < end; i++) {
    const q = questions[i];
    if (
      !q?.solution ||
      q.solution.includes("Placeholder") ||
      q.solution.includes("Video solution") ||
      q.solution.includes("uploaded soon")
    ) {
      missing.push(i);
    }
  }

  console.log(`Solving ${missing.length} geometry questions (${questions[START_INDEX]?.id} …)\n`);
  let done = 0;
  for (const i of missing) {
    const q = questions[i];
    let attempts = 0;
    while (attempts < 3) {
      try {
        const result = await solveQuestion(q.question, q.options);
        const prev = q.correctAnswer;
        q.correctAnswer = result.correctAnswer;
        q.solution = result.solution;
        delete q.explanation;
        if (prev !== result.correctAnswer) {
          console.log(`  ${q.id}: ${String(prev).slice(0, 30)} -> ${result.correctAnswer}`);
        }
        writeFileSync(filePath, JSON.stringify(questions, null, 2) + "\n");
        done++;
        process.stdout.write(`\r  [${done}/${missing.length}] ${q.id}   `);
        await sleep(150);
        break;
      } catch (err) {
        attempts++;
        if (attempts >= 3) console.error(`\n  Failed ${q.id}: ${err.message}`);
        else await sleep(2500);
      }
    }
  }
  console.log(`\nDone — ${done} solutions added.`);
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
