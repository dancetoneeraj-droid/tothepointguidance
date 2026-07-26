"""Build vocab-extracted.tsv from part files. Run: python scripts/build-vocab-tsv.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "datas" / "English" / "vocab-extracted.tsv"
PART1 = ROOT / "datas" / "English" / "vocab-part1.tsv"
PART2 = ROOT / "datas" / "English" / "vocab-part2.tsv"

parts = []
for p in (PART1, PART2):
    if p.exists():
        parts.append(p.read_text(encoding="utf-8").strip())
    else:
        print(f"WARNING: missing {p}")

merged = "\n".join(parts) + "\n"
OUT.write_text(merged, encoding="utf-8")

lines = [l for l in merged.splitlines() if l.strip() and not l.startswith("#")]
nums = [int(l.split("|")[0]) for l in lines]
print(f"Wrote {OUT} with {len(lines)} entries (#{min(nums)}-#{max(nums)})")
