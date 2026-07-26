"""Extract vocab TSV from scanned PDF page images using EasyOCR."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import easyocr

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "datas" / "English" / "vocab-pages"
OUT1 = ROOT / "datas" / "English" / "vocab-part1.tsv"
OUT2 = ROOT / "datas" / "English" / "vocab-part2.tsv"

START_NUM = 31
END_NUM = 1650
PAGE_START = 2
PAGE_END = 63

# Anchors for validation
ANCHORS = {
    31: "Abscond",
    261: "Foray",
    262: "Gracious",
    1650: "Zippy",
}

ENTRY_RE = re.compile(
    r"(\d+)\.\s+"
    r"([A-Za-z][A-Za-z\s'\-]*?)"
    r"\s*\([^)]*\)"
    r"\s*\(([^)]+)\)"
    r"\s*[—~\-_]+"
    r"(.+?)"
    r"(?=\s*\d+\.\s+[A-Za-z]|\Z)",
    re.DOTALL,
)

# Fallback: looser match when POS/meaning parens merge badly in OCR
ENTRY_RE_LOOSE = re.compile(
    r"(\d+)\.\s+"
    r"([A-Za-z][A-Za-z\s'\-]*?)"
    r"\s*\(([^)]+)\)"
    r"\s*[—~\-_]+"
    r"(.+?)"
    r"(?=\s*\d+\.\s+[A-Za-z]|\Z)",
    re.DOTALL,
)


def clean_word(word: str) -> str:
    word = re.sub(r"\s+", " ", word).strip()
    word = re.sub(r"[^A-Za-z\s'\-]", "", word).strip()
    return word.title() if word.isupper() else word.strip()


def clean_meaning(meaning: str) -> str:
    meaning = re.sub(r"\s+", " ", meaning).strip()
    meaning = meaning.strip(".,; ")
    return meaning


def clean_example(example: str) -> str:
    example = re.sub(r"\s+", " ", example).strip()
    example = example.strip(".,; ")
    if example and example[-1] not in ".!?":
        example += "."
    return example


def ocr_page(reader: easyocr.Reader, page_num: int) -> str:
    path = PAGES_DIR / f"page-{page_num:02d}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    lines = reader.readtext(str(path), detail=0, paragraph=False)
    return " ".join(lines)


def parse_entries(text: str) -> list[tuple[str, str, str]]:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    entries: list[tuple[str, str, str]] = []
    for regex in (ENTRY_RE, ENTRY_RE_LOOSE):
        for m in regex.finditer(text):
            word = clean_word(m.group(2))
            meaning = clean_meaning(m.group(3))
            example = clean_example(m.group(4))
            if word and meaning and len(word) > 1:
                entries.append((word, meaning, example))
        if entries:
            break
    return entries


def dedupe_sequential(entries: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen_words: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for word, meaning, example in entries:
        key = word.lower()
        if key in seen_words:
            continue
        seen_words.add(key)
        out.append((word, meaning, example))
    return out


def write_tsv(path: Path, rows: list[str]) -> None:
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> int:
    print("Loading EasyOCR reader...", flush=True)
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    all_entries: list[tuple[str, str, str]] = []
    for page in range(PAGE_START, PAGE_END + 1):
        print(f"OCR page {page}...", flush=True)
        text = ocr_page(reader, page)
        page_entries = parse_entries(text)
        print(f"  -> {len(page_entries)} entries", flush=True)
        all_entries.extend(page_entries)

    all_entries = dedupe_sequential(all_entries)
    needed = END_NUM - START_NUM + 1
    print(f"Total parsed entries: {len(all_entries)} (need {needed})", flush=True)

    if len(all_entries) < needed:
        print("WARNING: fewer entries than expected; writing what we have", flush=True)
        needed = len(all_entries)

    rows: list[str] = []
    for i, (word, meaning, example) in enumerate(all_entries[:needed]):
        num = START_NUM + i
        rows.append(f"{num}|{word}|{meaning}|{example}")

    part1 = [r for r in rows if int(r.split("|")[0]) <= 261]
    part2 = [r for r in rows if int(r.split("|")[0]) >= 262]

    write_tsv(OUT1, part1)
    write_tsv(OUT2, part2)

    print(f"Wrote {OUT1}: {len(part1)} lines")
    print(f"Wrote {OUT2}: {len(part2)} lines")

    for num, expected in ANCHORS.items():
        row = next((r for r in rows if r.startswith(f"{num}|")), None)
        if row:
            got = row.split("|")[1]
            ok = got.lower() == expected.lower()
            print(f"  #{num}: {got} {'OK' if ok else f'EXPECTED {expected}'}")
        else:
            print(f"  #{num}: MISSING (expected {expected})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
