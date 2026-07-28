"""Extract one-word substitutions from scanned OWS PDF and append to ows.json (day 21+)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "english" / "ows.pdf"
OCR_DIR = ROOT / "datas" / "english" / "ows-pages"
OCR_FULL = ROOT / "datas" / "english" / "ows-ocr-full.txt"
OWS_JSON = ROOT / "data" / "english" / "ows.json"

PER_DAY = 30
START_DAY = 21
STOP_MARKERS = re.compile(r"words\s+denoting\s+young[\-\s]*ones?", re.I)
NOISE = re.compile(
    r"^(chapter|objective|english|one word substitutions|www\.|facebook|banking|general$|^\d{2,3}$)",
    re.I,
)
ENTRY_START = re.compile(
    r"^(\d{1,3})[\._]\s*([A-Za-z][A-Za-z\-']{2,40})\s*(.*)$"
)
NUM_ONLY = re.compile(r"^(\d{1,3})[\._]\s*(.+)$")
SPILLOVER_WORD = re.compile(r"^([A-Z][a-zA-Z\-]{3,40})$")
MEANING_START = re.compile(
    r"^(one|a|an|the|who|person|lover|graveyard|funeral|absence|government|fear|of|morbid|delusion|compulsive|high|extreme|child|book|words|an account|a poem|place|ground|the right|govt|govemment|a person|always|able|capable|loss|commencement|list|the height|the philosophy|the branch|wildly|partner|to |doing|no longer|morbid|delusion)",
    re.I,
)
INVALID_WORDS = {
    "person", "english", "general", "objective", "chapter", "one", "words",
    "mania", "delusion", "ass", "bird", "cat", "cock", "calf", "deer", "dog",
    "duck", "adult", "young", "nestling", "foal", "kitten", "cockerel", "heifer",
    "fawn", "puppy", "duckling", "caterpillar", "butterfly", "moth", "cow", "dob",
}
PHOBIA_TAIL = [
    ("Pyrophobia", "fear of fire"),
    ("Thanatophobia", "fear of death"),
    ("Scelerophobia", "fear of burglars"),
    ("Theophobia", "fear of God"),
    ("Toxicophobia", "fear of poison"),
    ("Triskaidekaphobia", "fear of number thirteen"),
    ("Theomania", "delusion that one is God"),
]


def ensure_page_images() -> list[Path]:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    paths: list[Path] = []
    for i in range(doc.page_count):
        out = OCR_DIR / f"page-{i + 1:02d}.png"
        if not out.exists():
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(str(out))
        paths.append(out)
    doc.close()
    return paths


def ocr_all_pages(image_paths: list[Path]) -> str:
    if OCR_FULL.exists() and OCR_FULL.stat().st_size > 5000:
        return OCR_FULL.read_text(encoding="utf-8")

    import easyocr

    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    chunks: list[str] = []
    for i, img in enumerate(image_paths, start=1):
        print(f"OCR page {i}/{len(image_paths)}...", flush=True)
        per_page = OCR_DIR / f"page-{i:02d}.txt"
        if per_page.exists() and per_page.stat().st_size > 100:
            text = per_page.read_text(encoding="utf-8")
        else:
            lines = reader.readtext(str(img), detail=0, paragraph=False)
            text = "\n".join(lines)
            per_page.write_text(text, encoding="utf-8")
        chunks.append(f"\n--- PAGE {i} ---\n{text}")
    full = "\n".join(chunks)
    OCR_FULL.write_text(full, encoding="utf-8")
    return full


def clean_word(word: str) -> str:
    word = re.sub(r"\s+", " ", word).strip(" .,-")
    word = re.sub(r"[^A-Za-z\-']", "", word)
    return word.strip()


def clean_meaning(meaning: str) -> str:
    meaning = re.sub(r"\s+", " ", meaning).strip(" .,-")
    meaning = re.sub(r"\(Syn\.[^)]*\)", "", meaning, flags=re.I)
    meaning = re.sub(r"\(Ant\.[^)]*\)", "", meaning, flags=re.I)
    # OCR sometimes merges the next numbered entry into the meaning.
    bleed = re.search(r"\s+\d+[\._]\s+[A-Z][a-z]", meaning)
    if bleed:
        meaning = meaning[: bleed.start()]
    meaning = re.sub(r"\s+", " ", meaning).strip(" .,-")
    if re.match(r"^of\b", meaning, re.I):
        meaning = f"fear {meaning}"
    return meaning


def is_valid_word(word: str) -> bool:
    return bool(word) and word.lower() not in INVALID_WORDS and len(word) >= 3


def parse_page(page_text: str) -> list[tuple[str, str]]:
    lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
    entries: list[tuple[str, str]] = []
    orphan_meanings: list[str] = []
    spillover_words: list[str] = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        if NOISE.match(raw) or raw.startswith("--- PAGE"):
            i += 1
            continue
        if STOP_MARKERS.search(raw):
            break
        if re.match(r"^\([A-Z]\)", raw):
            i += 1
            continue

        m = ENTRY_START.match(raw)
        if m and is_valid_word(m.group(2)):
            word = clean_word(m.group(2))
            tail = m.group(3).strip()
            meaning_parts: list[str] = []
            if tail and MEANING_START.match(tail):
                meaning_parts.append(tail)
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if ENTRY_START.match(nxt) or NUM_ONLY.match(nxt):
                    break
                if SPILLOVER_WORD.match(nxt) and not MEANING_START.match(nxt):
                    break
                if NOISE.match(nxt) or re.match(r"^\([A-Z]\)", nxt):
                    j += 1
                    continue
                meaning_parts.append(nxt)
                j += 1
            meaning = clean_meaning(" ".join(meaning_parts))
            if meaning and len(meaning) >= 4:
                entries.append((word, meaning))
            i = j
            continue

        m2 = NUM_ONLY.match(raw)
        if m2:
            body = m2.group(2).strip()
            if MEANING_START.match(body) or body.lower().startswith("fear "):
                meaning_parts = [body]
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if ENTRY_START.match(nxt) or NUM_ONLY.match(nxt):
                        break
                    if SPILLOVER_WORD.match(nxt) and not MEANING_START.match(nxt):
                        break
                    if NOISE.match(nxt):
                        j += 1
                        continue
                    meaning_parts.append(nxt)
                    j += 1
                orphan_meanings.append(clean_meaning(" ".join(meaning_parts)))
                i = j
                continue

        if SPILLOVER_WORD.match(raw) and is_valid_word(raw):
            spillover_words.append(clean_word(raw))
        i += 1

    for word, meaning in zip(spillover_words, orphan_meanings):
        if is_valid_word(word) and meaning:
            entries.append((word, meaning))
    return entries


def parse_entries(text: str) -> list[tuple[str, str]]:
    stop = STOP_MARKERS.search(text)
    if stop:
        text = text[: stop.start()]

    all_entries: list[tuple[str, str]] = []
    for page in re.split(r"--- PAGE \d+ ---", text):
        if page.strip():
            all_entries.extend(parse_page(page))

    # Fix mangled phobia tail from two-column OCR on last page
    tail_words = {w.lower() for w, _ in PHOBIA_TAIL}
    trimmed: list[tuple[str, str]] = []
    for word, meaning in all_entries:
        wl = word.lower()
        if wl in tail_words and wl != "xenophobia":
            continue
        trimmed.append((word, meaning))
        if wl == "xenophobia":
            for w, mn in PHOBIA_TAIL[1:]:
                trimmed.append((w, mn))
            break

    if not trimmed or trimmed[-1][0].lower() != "theomania":
        existing = {w.lower() for w, _ in trimmed}
        for w, mn in PHOBIA_TAIL:
            if w.lower() not in existing:
                trimmed.append((w, mn))

    final: list[tuple[str, str]] = []
    for word, meaning in trimmed:
        final.append((word, meaning))
        if word.lower() == "theomania":
            break
    return final


def dedupe(entries: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for word, meaning in entries:
        key = word.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append((word, meaning))
    return out


def assign_days(entries: list[tuple[str, str]], start_id_num: int, start_day: int) -> list[dict]:
    return [
        {
            "id": f"ows{start_id_num + i:04d}",
            "day": start_day + (i // PER_DAY),
            "word": word,
            "meaning": meaning,
        }
        for i, (word, meaning) in enumerate(entries)
    ]


def main() -> int:
    if not PDF_PATH.exists():
        print(f"Missing PDF: {PDF_PATH}", file=sys.stderr)
        return 1

    existing = json.loads(OWS_JSON.read_text(encoding="utf-8"))
    existing = [x for x in existing if x["day"] <= 20]
    start_id_num = len(existing) + 1

    print(f"Existing: {len(existing)} cards through day 20", flush=True)
    images = ensure_page_images()
    text = ocr_all_pages(images)

    parsed = dedupe(parse_entries(text))
    print(f"Parsed {len(parsed)} entries from PDF", flush=True)
    if len(parsed) < 30:
        print("Too few entries parsed.", file=sys.stderr)
        return 1

    new_cards = assign_days(parsed, start_id_num, START_DAY)
    merged = existing + new_cards
    OWS_JSON.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    days = sorted({c["day"] for c in new_cards})
    print(f"Added {len(new_cards)} cards -> days {days[0]}-{days[-1]}")
    print(f"Total OWS: {len(merged)} cards, max day {days[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
