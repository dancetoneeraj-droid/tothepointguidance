/**
 * Create 300-question placeholder banks for all 17 maths topics.
 */
import { writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

const TOPICS = [
  "percentage",
  "ratio-proportion",
  "profit-loss",
  "time-work",
  "time-speed-distance",
  "average",
  "partnership",
  "mixture-alligation",
  "simple-interest",
  "compound-interest",
  "trigonometry",
  "di",
  "mensuration-3d",
  "algebra",
  "mensuration-2d",
  "geometry",
  "number-system",
];

const BANK_SIZE = 300;

function makeBank(topic) {
  const prefix = `maths_${topic.replace(/-/g, "_")}`;
  const label = topic
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
  return Array.from({ length: BANK_SIZE }, (_, i) => {
    const n = i + 1;
    return {
      id: `${prefix}_${String(n).padStart(3, "0")}`,
      question: `${label} — Question ${n} (add real content in datas/maths/${topic}.json)`,
      options: ["Option A", "Option B", "Option C", "Option D"],
      correctAnswer: "Option A",
      explanation: `Placeholder for ${label}.`,
    };
  });
}

const dir = join(root, "data", "maths");
mkdirSync(dir, { recursive: true });

for (const topic of TOPICS) {
  const path = join(dir, `${topic}.json`);
  writeFileSync(path, JSON.stringify(makeBank(topic), null, 2));
  console.log(`Wrote ${topic}.json (${BANK_SIZE} slots)`);
}
