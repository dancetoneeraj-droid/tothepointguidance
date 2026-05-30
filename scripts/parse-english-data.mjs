// Parses the raw SSC one-word-substitution and idiom text dumps into clean
// JSON decks, spread 30 cards per day. Run: node scripts/parse-english-data.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, "..", "data", "english");

const PER_DAY = 30;

function splitCols(line) {
  return line
    .split(/\s{2,}/)
    .map((s) => s.trim())
    .filter(Boolean);
}

// ---------------------------------------------------------------- OWS ----
function parseOws() {
  const raw = readFileSync(join(dataDir, "ows.txt.txt"), "utf8");
  const lines = raw.split(/\r?\n/);

  const noise =
    /WWW\.|FACEBOOK|BANKINGSHORTCUTS|One Word Substitution asked|Many Words|^\s*One Word\s*$/i;
  const tag = /\((?:[^)]*\d{2,4}[^)]*|CGL|CHSL|CPO|MTS|LDC|DEO|FCI|SO|TA|SAS|MT|Constable|Stenographer|Investigator|Statistical)[^)]*\)/i;

  const entries = [];
  let pendingDef = "";
  let lastEntry = null;

  for (const line of lines) {
    if (!line.trim() || noise.test(line)) continue;
    const segs = splitCols(line);
    if (segs.length === 0) continue;

    const answerSegIdx = segs.findIndex((s) => tag.test(s));
    if (answerSegIdx === -1) {
      const joined = segs.join(" ").trim();
      // A lowercase-starting fragment with no pending definition is almost
      // always the tail of the previous (wrapped) definition.
      if (pendingDef === "" && lastEntry && /^[a-z]/.test(joined)) {
        lastEntry.meaning = `${lastEntry.meaning} ${joined}`
          .replace(/\s+/g, " ")
          .trim();
      } else {
        pendingDef = `${pendingDef} ${joined}`.trim();
      }
      continue;
    }

    const answerSeg = segs[answerSegIdx];
    const answer = answerSeg.split("(")[0].trim();
    const leftParts = segs.slice(0, answerSegIdx).join(" ");
    const def = `${pendingDef} ${leftParts}`.replace(/\s+/g, " ").trim();
    pendingDef = "";

    if (!/^[A-Za-z][A-Za-z '\u2013-]{1,30}$/.test(answer)) continue;
    const words = def.split(" ").filter(Boolean);
    if (words.length < 2 || def.length < 6 || def.length > 140) continue;
    // Reject leaked exam tags / split parens: definitions never have digits.
    if (/\d/.test(def) || /\b(CGL|CHSL|CPO|MTS|LDC|DEO|FCI|Invigilator)\b/.test(def))
      continue;

    const entry = { word: answer, meaning: def };
    entries.push(entry);
    lastEntry = entry;
  }

  return dedupe(entries, (e) => e.word.toLowerCase());
}

// -------------------------------------------------------------- IDIOMS ----
function parseIdioms() {
  const raw = readFileSync(join(dataDir, "idiom.txt.txt"), "utf8");
  const lines = raw.split(/\r?\n/);

  const noise =
    /FREEDOM ACADEMY|PANACEA|An institute|IMPORTANT IDIOMS|Visit www|Downloaded from|PHRASEL|Phrasal verb|^\s*S\. No\.|qmaths/i;

  const entries = [];
  let current = null;

  for (const line of lines) {
    if (!line.trim() || noise.test(line)) continue;
    const numMatch = line.match(/^\s*(\d+)\.\s+(.*)$/);
    if (numMatch) {
      if (current) entries.push(current);
      const rest = numMatch[2];
      const segs = splitCols(rest);
      if (segs.length < 2) {
        current = null;
        continue;
      }
      const idiom = segs[0];
      const meaning = segs[segs.length - 1];
      current = { idiom, meaning };
    } else if (current) {
      // continuation of wrapped English meaning
      const segs = splitCols(line);
      if (segs.length > 0) {
        current.meaning = `${current.meaning} ${segs[segs.length - 1]}`.trim();
      }
    }
  }
  if (current) entries.push(current);

  // ASCII-clean meanings only; drop entries where meaning looks like Krutidev.
  const cleaned = entries
    .map((e) => ({
      idiom: e.idiom.replace(/\s+/g, " ").trim(),
      meaning: e.meaning.replace(/\s+/g, " ").trim(),
    }))
    .filter((e) => {
      if (!/^[A-Za-z][A-Za-z '’\u2013-]{2,40}$/.test(e.idiom)) return false;
      if (e.meaning.length < 4 || e.meaning.length > 120) return false;
      if (/\d/.test(e.meaning)) return false;
      // English meaning should be mostly normal latin words with vowels.
      const vowelRatio =
        (e.meaning.match(/[aeiou]/gi) || []).length / e.meaning.length;
      return vowelRatio > 0.2;
    });

  return dedupe(cleaned, (e) => e.idiom.toLowerCase());
}

function dedupe(arr, keyFn) {
  const seen = new Set();
  const out = [];
  for (const item of arr) {
    const key = keyFn(item);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
  }
  return out;
}

function assignDays(entries, startDay, prefix, build) {
  return entries.map((entry, i) => ({
    id: `${prefix}${String(i + 1).padStart(4, "0")}`,
    day: startDay + Math.floor(i / PER_DAY),
    ...build(entry),
  }));
}

const ows = parseOws();
const idioms = parseIdioms();

// Each deck is independent and starts at Day 1 (30 cards per day).
const owsCards = assignDays(ows, 1, "ows", (e) => ({
  word: e.word,
  meaning: e.meaning,
}));
const idiomCards = assignDays(idioms, 1, "idm", (e) => ({
  idiom: e.idiom,
  meaning: e.meaning,
}));

writeFileSync(
  join(dataDir, "ows.json"),
  JSON.stringify(owsCards, null, 2) + "\n"
);
writeFileSync(
  join(dataDir, "idioms.json"),
  JSON.stringify(idiomCards, null, 2) + "\n"
);

console.log(`OWS:    ${owsCards.length} cards across ${Math.ceil(owsCards.length / PER_DAY)} days`);
console.log(`Idioms: ${idiomCards.length} cards across ${Math.ceil(idiomCards.length / PER_DAY)} days`);
console.log("\n--- OWS sample ---");
console.log(JSON.stringify(owsCards.slice(0, 6), null, 2));
console.log("\n--- Idiom sample ---");
console.log(JSON.stringify(idiomCards.slice(0, 6), null, 2));
