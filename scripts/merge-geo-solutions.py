"""Merge geo-solutions-out-*.json into geometry.json (indices 151+ only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "geometry.json"
START = 151


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    by_id = {e["id"]: i for i, e in enumerate(bank)}
    merged = 0
    for path in sorted((ROOT / "scripts").glob("geo-solutions-out-*.json")):
        items = json.loads(path.read_text(encoding="utf-8"))
        for item in items:
            qid = item.get("id")
            if qid not in by_id:
                continue
            idx = by_id[qid]
            if idx < START:
                continue
            entry = bank[idx]
            entry["correctAnswer"] = item["correctAnswer"]
            entry["solution"] = item["solution"]
            entry.pop("explanation", None)
            merged += 1
    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Merged {merged} solutions into {BANK}")


if __name__ == "__main__":
    main()
