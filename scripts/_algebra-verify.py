"""One-off check that the algebra sheet import touched only its own slots."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REL = "data/maths/algebra.json"

new = json.loads((ROOT / REL).read_text(encoding="utf-8"))
old = json.loads(
    subprocess.run(
        ["git", "show", f"HEAD:{REL}"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode("utf-8")
)

print(f"entries: {len(old)} -> {len(new)}")

changed = [i for i in range(len(old)) if old[i] != new[i]]
print(f"changed within the original {len(old)}: index {min(changed)}..{max(changed)} "
      f"({len(changed)} entries), contiguous={changed == list(range(changed[0], changed[0] + len(changed)))}")
print(f"untouched before the block: {all(old[i] == new[i] for i in range(changed[0]))}")

bad_id = [i for i, q in enumerate(new) if q["id"] != f"maths_algebra_{i + 1}"]
print(f"id/index mismatches: {bad_id}")

block = new[187:426]
print(f"imported block size: {len(block)}")
print(f"placeholders left in block: {sum('add real content' in q['question'] for q in block)}")
print(f"answer not in options: {[q['id'] for q in block if q['correctAnswer'] not in q['options']]}")
print(f"not 4 options: {[q['id'] for q in block if len(q['options']) != 4]}")
print(f"duplicate options: {[q['id'] for q in block if len(set(q['options'])) != 4]}")
print(f"missing solution: {[q['id'] for q in block if not q.get('solution')]}")
print(f"solution not ending in answer: "
      f"{[q['id'] for q in block if not q['solution'].rstrip().endswith(q['correctAnswer'])]}")
print(f"remaining placeholders after 426: {sum('add real content' in q['question'] for q in new[426:])}")

texts = [q["question"] for q in block]
dupes = {t for t in texts if texts.count(t) > 1}
print(f"duplicate question texts inside block: {len(dupes)}")
for t in sorted(dupes):
    print("   ", t[:90])
