"""Dump failed geometry question blocks for manual review."""
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parent.parent
GEO_DIR = ROOT / "datas" / "maths" / "geometry"
SHEETS = {
    4: GEO_DIR / "Geometry-Sheet-4.pdf",
    5: GEO_DIR / "Geometry-Sheet-5.pdf",
    6: GEO_DIR / "Geometry-Sheet-6.pdf",
    8: GEO_DIR / "Geometry-Sheet-8.pdf",
    9: GEO_DIR / "Geometry-Sheet--9.pdf",
    10: ROOT / "datas" / "maths" / "Geometry-10.pdf",
    11: GEO_DIR / "Geometry-Sheet-11.pdf",
    12: GEO_DIR / "Geometry-Sheet--12.pdf",
}
FAILS = [
    (4, 15),
    (5, 7),
    (5, 25),
    (5, 54),
    (5, 66),
    (6, 4),
    (6, 14),
    (8, 24),
    (9, 14),
    (10, 20),
    (11, 31),
    (12, 33),
    (12, 117),
    (12, 149),
]


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
    return text[m.start() : (m2.start() if m2 else len(text))]


def main() -> None:
    parts: list[str] = []
    for sheet, q in FAILS:
        path = SHEETS[sheet]
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        block = find_block(text, q)
        parts.append(f"=== SHEET {sheet} Q{q} ===\n{block or 'NOT FOUND'}")

    out = GEO_DIR / "failed-blocks.txt"
    out.write_text("\n\n".join(parts), encoding="utf-8")
    print(f"Written {len(FAILS)} blocks -> {out}")


if __name__ == "__main__":
    main()
