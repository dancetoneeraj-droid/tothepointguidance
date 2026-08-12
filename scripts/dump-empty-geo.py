"""List PDF blocks for questions with empty parsed text."""
from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
GEO_DIR = ROOT / "datas" / "maths" / "geometry"
SRC = GEO_DIR / "all-sheets.json"

SHEET_FILES = {
    4: GEO_DIR / "Geometry-Sheet-4.pdf",
    5: GEO_DIR / "Geometry-Sheet-5.pdf",
    6: GEO_DIR / "Geometry-Sheet-6.pdf",
    7: GEO_DIR / "Geometry-Sheet-7.pdf",
    8: GEO_DIR / "Geometry-Sheet-8.pdf",
    9: GEO_DIR / "Geometry-Sheet--9.pdf",
    10: ROOT / "datas" / "maths" / "Geometry-10.pdf",
    11: GEO_DIR / "Geometry-Sheet-11.pdf",
    12: GEO_DIR / "Geometry-Sheet--12.pdf",
}


def find_block(text: str, num: int) -> str | None:
    no_dot_kw = (
        r"Find |Let |In |If |The |A |An |What |Which |From |Radius |Area |Two |Three |"
        r"Suhas |D and E |Δ|∆|ABC|PQR|Given |How |At |One |Points |Sides "
    )
    patterns = [
        rf"(?:^|\n)\s*{num}\.\s",
        rf"(?:^|\n)\s*{num}\s+\.\s",
        rf"(?:^|\n)\s*{num}\s+(?!\.)(?:{no_dot_kw})",
    ]
    m = None
    for p in patterns:
        m = re.search(p, text, re.M)
        if m:
            break
    if not m:
        return None
    nxt = re.compile(
        rf"(?:^|\n)\s*{num + 1}(?:\.\s|\s+\.\s|\s+(?!\.)(?:{no_dot_kw}))",
        re.M,
    )
    m2 = nxt.search(text, m.end())
    end = m2.start() if m2 else len(text)
    return text[m.start() : end].strip()


def main() -> None:
    parsed = json.loads(SRC.read_text(encoding="utf-8"))
    empty_by_sheet: dict[int, list[int]] = {}
    sheet_counters: dict[int, int] = {}

    for entry in parsed:
        sheet = entry["sheet"]
        sheet_counters[sheet] = sheet_counters.get(sheet, 0) + 1
        qnum = sheet_counters[sheet]
        if not entry.get("question", "").strip():
            empty_by_sheet.setdefault(sheet, []).append(qnum)

    out_lines: list[str] = []
    for sheet, nums in empty_by_sheet.items():
        doc = fitz.open(SHEET_FILES[sheet])
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        for qnum in nums[:3]:
            block = find_block(text, qnum) or "NOT FOUND"
            out_lines.append(f"=== SHEET {sheet} Q{qnum} ===\n{block[:1200]}\n")

    out = GEO_DIR / "empty-samples.txt"
    out.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Empty by sheet: { {k: len(v) for k, v in empty_by_sheet.items()} }")
    print(f"Samples -> {out}")


if __name__ == "__main__":
    main()
