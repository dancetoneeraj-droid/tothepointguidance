/**
 * Solve Discount questions (maths_profit_loss_160 onward), set correctAnswer,
 * write solutions, and fix options when the computed answer is missing.
 *
 * Run:
 *   node scripts/add-solutions-discount.mjs
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

const START_INDEX = 159; // maths_profit_loss_160
const COUNT = 141;

function normalize(s) {
  return String(s)
    .trim()
    .replace(/\s+/g, " ")
    .replace(/[₹Rs.]/gi, "")
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
      if (!Number.isNaN(n) && Math.abs(n - num) < 0.05) return opt;
    }
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
    const fixMatch = raw.match(/"fixedOptions"\s*:\s*(\[[\s\S]*?\])/);
    const out = {};
    if (answerMatch) out.answer = JSON.parse('"' + answerMatch[1] + '"');
    if (solMatch) out.solution = JSON.parse('"' + solMatch[1] + '"');
    if (fixMatch) out.fixedOptions = JSON.parse(fixMatch[1]);
    if (out.answer && out.solution) return out;
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
          "You are an SSC CGL Profit & Loss / Discount expert. Solve independently.\n" +
          "Do NOT trust any pre-marked answer — compute from scratch.\n" +
          "PDF formatting may be imperfect (fractions, Rs/₹).\n\n" +
          `Question:\n${question}\n\n` +
          `Options (pick exactly one):\n${options.map((o, i) => `${i + 1}. ${o}`).join("\n")}\n\n` +
          "If none of the options exactly match your computed answer, provide corrected option texts.\n" +
          "Respond with ONLY valid JSON:\n" +
          "{\n" +
          '  "optionIndex": <1-4>,\n' +
          '  "answer": "<exact text of chosen option after any fixes>",\n' +
          '  "fixedOptions": ["opt1","opt2","opt3","opt4"] or null if originals are fine,\n' +
          '  "solution": "<3-6 step markdown ending with **Answer: ...**>"\n' +
          "}",
      },
    ],
  });

  const parsed = parseJson(response.content[0].text.trim());
  const opts =
    Array.isArray(parsed.fixedOptions) && parsed.fixedOptions.length === 4
      ? parsed.fixedOptions.map(String)
      : options;
  const matched = pickOption(parsed, opts);
  return { correctAnswer: matched, solution: parsed.solution.trim(), options: opts };
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const filePath = join(root, "data", "maths", "profit-loss.json");
  const questions = JSON.parse(readFileSync(filePath, "utf8"));
  const end = Math.min(START_INDEX + COUNT, questions.length);
  const lastImported = START_INDEX + 126; // 127 discount questions -> 160..286

  const missing = [];
  for (let i = START_INDEX; i <= lastImported && i < end; i++) {
    const q = questions[i];
    if (
      !q?.solution ||
      q.solution === "video solution will be added soon" ||
      q.question?.includes("add real content")
    ) {
      missing.push(i);
    }
  }

  console.log(`Solving ${missing.length} Discount questions (maths_profit_loss_160 …)\n`);

  let done = 0;
  for (const i of missing) {
    const q = questions[i];
    let attempts = 0;
    while (attempts < 3) {
      try {
        const result = await solveQuestion(q.question, q.options);
        const prevAnswer = q.correctAnswer;
        const prevOpts = JSON.stringify(q.options);
        q.options = result.options;
        q.correctAnswer = result.correctAnswer;
        q.solution = result.solution;
        if (prevAnswer !== result.correctAnswer) {
          console.log(`  ${q.id}: answer ${prevAnswer} -> ${result.correctAnswer}`);
        }
        if (prevOpts !== JSON.stringify(result.options)) {
          console.log(`  ${q.id}: options corrected`);
        }
        writeFileSync(filePath, JSON.stringify(questions, null, 2) + "\n");
        done++;
        process.stdout.write(`\r  [${done}/${missing.length}] ${q.id}   `);
        await sleep(200);
        break;
      } catch (err) {
        attempts++;
        if (attempts >= 3) {
          console.error(`\n  Failed ${q.id} after 3 attempts: ${err.message}`);
        } else {
          await sleep(3000);
        }
      }
    }
  }

  console.log(`\nDone — ${done} solutions added.`);
}

main().catch((err) => {
  console.error("\nFatal:", err.message);
  process.exit(1);
});
