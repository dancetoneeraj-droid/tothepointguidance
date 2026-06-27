import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const filePath = join(root, 'data', 'reasoning', 'coding-decoding.json');
const raw = readFileSync(filePath, 'utf8');

// Show lines with deep indentation (nested wrongly)
const lines = raw.split('\n');
console.log('=== Lines with deep indentation (possible nesting issue) ===');
for (let i = 0; i < lines.length; i++) {
  const m = lines[i].match(/^(\s*)/);
  const indent = m ? m[1].length : 0;
  if (indent >= 14) {
    console.log(`Line ${i+1} (indent ${indent}): ${lines[i].trim().slice(0, 80)}`);
  }
}

// Find the position of the JSON error
try {
  JSON.parse(raw);
  console.log('JSON is valid!');
} catch (e) {
  console.log('\nJSON error:', e.message);
}
