import { writeFileSync, mkdirSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

function makeQuestions(prefix, topicLabel, count) {
  return Array.from({ length: count }, (_, i) => {
    const n = i + 1;
    return {
      id: `${prefix}_${String(n).padStart(3, "0")}`,
      question: `${topicLabel} — Question ${n}: What is the correct answer?`,
      options: ["Option A", "Option B", "Option C", "Option D"],
      correctAnswer: "Option A",
      explanation: `Review ${topicLabel} concept for question ${n}.`,
    };
  });
}

/** 8 days × 30 questions per maths topic (CGL pattern) */
const MATHS_BANK_SIZE = 240;

const banks = {
  maths: {
    percentage: MATHS_BANK_SIZE,
    algebra: MATHS_BANK_SIZE,
    "profit-loss": MATHS_BANK_SIZE,
    "number-system": MATHS_BANK_SIZE,
    "simple-interest": MATHS_BANK_SIZE,
  },
  reasoning: {
    "coding-decoding": 60,
    puzzle: 60,
    analogy: 60,
  },
  gk: {
    revision: 40,
  },
};

for (const [subject, topics] of Object.entries(banks)) {
  const dir = join(root, "data", subject);
  mkdirSync(dir, { recursive: true });
  for (const [topic, count] of Object.entries(topics)) {
    const prefix = `${subject}_${topic.replace(/-/g, "_")}`;
    const label = topic
      .split("-")
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(" ");
    const questions = makeQuestions(prefix, label, count);
    writeFileSync(
      join(dir, `${topic}.json`),
      JSON.stringify(questions, null, 2)
    );
    console.log(`Wrote ${subject}/${topic}.json (${count} questions)`);
  }
}
