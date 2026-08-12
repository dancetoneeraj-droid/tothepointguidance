"""Scope and integrity check for the Sheet 4-6 import into mensuration-3d.json.

Compares the working copy against the committed version so that any edit outside
the intended block shows up immediately.
"""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REL = "data/maths/mensuration-3d.json"
START, COUNT = 187, 99

new = json.loads((ROOT / REL).read_text(encoding="utf-8"))
old = json.loads(
    subprocess.run(
        ["git", "show", f"HEAD:{REL}"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode("utf-8")
)

print(f"entries: {len(old)} -> {len(new)}")

changed = [i for i in range(min(len(old), len(new))) if old[i] != new[i]]
print(
    f"changed indices: {changed[0]}..{changed[-1]} ({len(changed)} entries), "
    f"contiguous={changed == list(range(changed[0], changed[-1] + 1))}"
)
print(f"changes confined to the intended block: {changed == list(range(START, START + COUNT))}")
print(f"ids preserved everywhere: {[q['id'] for q in old] == [q['id'] for q in new]}")

nums = [int(re.search(r"(\d+)$", q["id"]).group(1)) for q in new]
print(f"ids strictly increasing: {all(b > a for a, b in zip(nums, nums[1:]))}")

block = new[START : START + COUNT]
print(f"placeholders left in block: {sum('add real content' in q['question'] for q in block)}")
print(f"answer not in options: {[q['id'] for q in block if q['correctAnswer'] not in q['options']]}")
print(f"not 4 options: {[q['id'] for q in block if len(q['options']) != 4]}")
print(f"duplicate options: {[q['id'] for q in block if len(set(q['options'])) != 4]}")
print(f"missing solution: {[q['id'] for q in block if not q.get('solution')]}")
print(
    "solution not ending in answer: "
    f"{[q['id'] for q in block if not q['solution'].rstrip().endswith(q['correctAnswer'])]}"
)
texts = [q["question"] for q in block]
print(f"duplicate question texts inside block: {len(texts) - len(set(texts))}")
print(f"placeholders remaining after the block: {sum('add real content' in q['question'] for q in new[START + COUNT:])}")
