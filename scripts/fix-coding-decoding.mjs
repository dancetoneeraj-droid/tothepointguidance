import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const filePath = join(root, 'data', 'reasoning', 'coding-decoding.json');
const raw = readFileSync(filePath, 'utf8');

// The JSON is structurally invalid (badly nested from AI insertions).
// Strategy: use a lenient tokenizer to extract all objects that have an "id" field.
function extractQuestions(text) {
  const questions = [];
  let i = 0;

  while (i < text.length) {
    if (text[i] === '{') {
      // Try to parse a complete object starting here
      let depth = 0;
      let inStr = false;
      let esc = false;
      let start = i;

      for (let j = i; j < text.length; j++) {
        const c = text[j];
        if (esc) { esc = false; continue; }
        if (c === '\\' && inStr) { esc = true; continue; }
        if (c === '"') { inStr = !inStr; continue; }
        if (!inStr) {
          if (c === '{') depth++;
          else if (c === '}') {
            depth--;
            if (depth === 0) {
              const candidate = text.substring(start, j + 1);
              try {
                const obj = JSON.parse(candidate);
                if (obj.id && typeof obj.question === 'string') {
                  questions.push(obj);
                }
              } catch {
                // not a valid JSON object, skip
              }
              i = j + 1;
              break;
            }
          }
        }
      }
      if (depth !== 0) i++;
    } else {
      i++;
    }
  }
  return questions;
}

const questions = extractQuestions(raw);
console.log(`Extracted ${questions.length} questions`);

// Show IDs to verify order
questions.slice(0, 5).forEach(q => console.log(' ', q.id));
console.log('  ...');
questions.slice(-5).forEach(q => console.log(' ', q.id));

// Check for duplicates
const idCounts = {};
for (const q of questions) {
  idCounts[q.id] = (idCounts[q.id] ?? 0) + 1;
}
const dupes = Object.entries(idCounts).filter(([, c]) => c > 1);
if (dupes.length) {
  console.log('\nDuplicate IDs found:');
  dupes.forEach(([id, count]) => console.log(`  ${id} × ${count}`));
} else {
  console.log('\nNo duplicate IDs');
}

// Deduplicate: keep first occurrence of each id
const seen = new Set();
const deduped = questions.filter(q => {
  if (seen.has(q.id)) return false;
  seen.add(q.id);
  return true;
});

console.log(`\nFinal count after dedup: ${deduped.length}`);

// Sort by id number
deduped.sort((a, b) => {
  const na = parseInt(a.id.split('_').pop(), 10);
  const nb = parseInt(b.id.split('_').pop(), 10);
  return na - nb;
});

// Validate the final array
const output = JSON.stringify(deduped, null, 2);
try {
  JSON.parse(output);
  console.log('Output JSON is valid');
} catch (e) {
  console.log('ERROR: output still invalid:', e.message);
  process.exit(1);
}

writeFileSync(filePath, output);
console.log(`\nSaved ${deduped.length} questions to coding-decoding.json`);

// Verify first 30 are unique
const first30Ids = deduped.slice(0, 30).map(q => q.id);
const dupes30 = first30Ids.filter((id, i) => first30Ids.indexOf(id) !== i);
console.log('Duplicate IDs in first 30:', dupes30.length > 0 ? dupes30 : 'none');
