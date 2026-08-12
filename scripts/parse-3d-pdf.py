"""Parse datas/maths/3D.pdf into datas/maths/3d.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "maths" / "3D.pdf"
OUT_PATH = ROOT / "datas" / "maths" / "3d.json"
MAX_Q = 50

HEADER = re.compile(r"BY Gagan Pratap", re.I)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|SELECTION POST|CGL|UP POLICE|DSSB|DP CONSTABLE)[^)]*\)",
    re.I,
)
GARBAGE = re.compile(
    r"^(?:BY Gagan Pratap|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|Kkr dhft|Kkr djsaA|dk vk;ru|dk eku|fdruk gksxk)\b.*)$",
    re.I,
)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    repl = {
        "−": "-",
        "–": "-",
        "—": "-",
        "½": "1/2",
        "¼": "1/4",
        "¾": "3/4",
        "": "π",
        "𝝅": "π",
        "𝒄𝒎": "cm",
        "𝟐": "2",
        "𝟑": "3",
        "𝟒": "4",
        "𝟓": "5",
        "𝟔": "6",
        "𝟕": "7",
        "𝟖": "8",
        "𝟗": "9",
        "𝟎": "0",
        "𝟏": "1",
        "√": "√",
    }
    for old, new in repl.items():
        text = text.replace(old, new)
    text = re.sub(r"(\d)\s*[oO]\b", r"\1°", text)
    text = re.sub(r"\bcm2\b", "cm²", text, flags=re.I)
    text = re.sub(r"\bcm3\b", "cm³", text, flags=re.I)
    text = re.sub(r"\bm2\b", "m²", text, flags=re.I)
    text = re.sub(r"\bm3\b", "m³", text, flags=re.I)
    text = re.sub(r"\bsq\.?\s*cm\b", "cm²", text, flags=re.I)
    text = re.sub(r"\bh2\b", "h²", text)
    text = re.sub(r"\btan2\b", "tan²", text)
    text = re.sub(r"\bsec2\b", "sec²", text)
    text = re.sub(r"\b(\d)\s+(\d)π", r"\1/\2π", text)
    text = re.sub(r"\s+\([a-d]\)\s*$", "", text, flags=re.I)
    text = EXAM_TAG.sub("", text).strip()
    return re.sub(r"\s+", " ", text).strip()


def clean_option(text: str) -> str:
    text = normalize_text(text)
    text = re.sub(r"\s*(?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|DSSB|DP CONSTABLE)[^)]*\)?\s*$", "", text, flags=re.I)
    text = re.sub(r"\s*\([a-d]\)\s*$", "", text, flags=re.I)
    return text.strip()


def join_fraction_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        cur = lines[i].strip()
        if not cur:
            i += 1
            continue
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if (
                re.match(r"^[\d%./+\-()π√Rs]+$", cur, re.I)
                and re.match(r"^[\d%./+\-()π√Rs]+$", nxt, re.I)
                and len(cur) < 24
                and len(nxt) < 24
                and "/" not in cur
            ):
                out.append(f"{cur}/{nxt}")
                i += 2
                continue
        out.append(cur)
        i += 1
    return out


def extract_pdf_text() -> str:
    doc = fitz.open(PDF_PATH)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def find_block(text: str, num: int) -> str | None:
    no_dot_kw = (
        r"If |The |A |An |What |Find |Radius |From |In |Akshay |Take |"
        r"From a |A sector |A semicircular |A right |A cone |A reservoir |"
        r"The radius |The height |The volume |The circumference |The curved |"
        r"The vertical |The radii |The slant "
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
    nxt_kw = (
        r"If |The |A |An |What |Find |Radius |From |In |Akshay |"
        r"A sector |A semicircular |A right |A cone |A reservoir |"
        r"The radius |The height |The volume |The circumference |The curved |"
        r"The vertical |The radii |The slant "
    )
    nxt = re.compile(rf"(?:^|\n)\s*{num + 1}(?:\.\s|\s+\.\s|\s+(?!\.)(?:{nxt_kw}))", re.M)
    m2 = nxt.search(text, m.end())
    return text[m.start() : (m2.start() if m2 else len(text))].strip()


def strip_header(block: str) -> str:
    block = re.sub(r"^\d+\s*\.\s*", "", block, count=1)
    block = re.sub(r"^\d+\s+(?!\.)(?=[A-Za-z])", "", block, count=1)
    return HEADER.sub("", block).strip()


def collect_line_options(body: str, pat: re.Pattern) -> list[tuple[int, str]]:
    lines = body.splitlines()
    results: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        m = pat.match(lines[i].strip())
        if m:
            pos = body.find(lines[i])
            val = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
            parts = [val.strip()]
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or pat.match(nxt) or GARBAGE.match(nxt):
                    break
                if re.match(r"^[A-D]\)|\([a-d]\)|\[?[A-D]\]?", nxt, re.I):
                    break
                parts.append(nxt)
                i += 1
            results.append((pos, normalize_text(" ".join(join_fraction_lines(parts)))))
        else:
            i += 1
    return results


OPTION_MARKERS = re.compile(
    r"(?:^|\s)(?:"
    r"\(([a-d])\)|"
    r"([A-D])\)|"
    r"\[([A-D])\]|"
    r"([A-D])\.\s*|"
    r"([1-4])\.\s*"
    r")",
    re.I | re.M,
)


def split_by_markers(body: str) -> list[tuple[str, str]]:
    """Split body into [(letter, text), ...] using option markers."""
    matches = list(OPTION_MARKERS.finditer(body))
    if not matches:
        return []

    pairs: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        letter = next(g.upper() for g in m.groups() if g)
        if letter in "1234":
            letter = "ABCD"[int(letter) - 1]
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end].strip()
        lines = [ln.strip() for ln in chunk.splitlines() if ln.strip() and not GARBAGE.match(ln.strip())]
        lines = join_fraction_lines(lines)
        text = normalize_text(" ".join(lines))
        if text:
            pairs.append((letter, text))
    return pairs


def extract_numbered_options(body: str) -> tuple[int, list[str]] | None:
    """Handle '1.288π' style (no space after dot) and '2. 125π' style."""
    lines = body.splitlines()
    opts: list[str] = []
    first_pos = None
    for ln in lines:
        m = re.match(r"^\s*([1-4])\.(\s*)(.+)$", ln.strip())
        if not m:
            continue
        if first_pos is None:
            first_pos = body.find(ln)
        val = m.group(3).strip()
        if re.match(r"^\d", val) and not re.match(r"^\d+\s*(cm|m|π|%|√)", val, re.I):
            # e.g. "288π" after "1." got merged as "1.288π" on one token — strip leading digits from split
            val = re.sub(r"^\d+\.", "", f"{m.group(1)}.{val}") if "." in f"{m.group(1)}.{val}" else val
        opts.append(normalize_text(val))
        if len(opts) >= 4:
            break
    if len(opts) >= 4 and first_pos is not None:
        return first_pos, opts[:4]
    return None


def extract_options(body: str) -> tuple[int, list[str]] | None:
    # Numbered without space: 1.288π
    numbered = extract_numbered_options(body)
    if numbered:
        return numbered

    marker_pairs = split_by_markers(body)
    if len(marker_pairs) >= 4:
        by_letter: dict[str, str] = {}
        for letter, text in marker_pairs:
            if letter not in by_letter and text:
                by_letter[letter] = text
        options = [by_letter.get(ch, "") for ch in "ABCD"]
        if all(options):
            pos = body.find(marker_pairs[0][1][: min(8, len(marker_pairs[0][1]))])
            if pos < 0:
                pos = OPTION_MARKERS.search(body).start()
            return pos, options

    line_pats = [
        re.compile(r"^\([a-d]\)\s*(.*)$", re.I),
        re.compile(r"^[A-D]\)\s*(.*)$"),
        re.compile(r"^[A-D]\.\s*(.*)$"),
        re.compile(r"^\[([A-D])\]\s*(.*)$", re.I),
        re.compile(r"^([1-4])\.\s+(.*)$"),
    ]
    for pat in line_pats:
        collected = collect_line_options(body, pat)
        if len(collected) >= 4:
            return collected[0][0], [v for _, v in collected[:4]]

    # Multi-option lines: (a) xxx (b) yyy
    multi = re.findall(r"\(([a-d])\)\s*([^()]+?)(?=\s*\([a-d]\)|$)", body, re.I | re.S)
    if len(multi) >= 4:
        pos = body.find(f"({multi[0][0].lower()})")
        return pos, [normalize_text(v) for _, v in multi[:4]]

    inline = re.findall(r"(?:^|\s*)([A-D])\)\s*([^A-D)]+?)(?=\s+[A-D]\)|$)", body, re.M)
    if len(inline) >= 4:
        pos = body.find(f"{inline[0][0]})")
        return pos, [normalize_text(v) for _, v in inline[:4]]

    inline2 = re.findall(r"(?:^|\s*)([a-d])\)\s*([^a-d)]+?)(?=\s+[a-d]\)|$)", body, re.I | re.M)
    if len(inline2) >= 4:
        pos = body.lower().find(f"{inline2[0][0].lower()})")
        return pos, [normalize_text(v) for _, v in inline2[:4]]
    if len(inline2) == 3:
        # d) may be on next line — try marker split again with relaxed count
        marker_pairs = split_by_markers(body)
        if len(marker_pairs) >= 4:
            by_letter = {l: t for l, t in marker_pairs if l not in locals().get("by_letter", {})}
            options = [by_letter.get(ch, "") for ch in "ABCD"]
            if all(options):
                return OPTION_MARKERS.search(body).start(), options

    bracket = re.findall(r"\[([A-D])\]\s*([^\[]+?)(?=\s*\[[A-D]\]|$)", body, re.I | re.S)
    if len(bracket) >= 4:
        pos = body.find(f"[{bracket[0][0]}]")
        return pos, [normalize_text(v) for _, v in bracket[:4]]

    return None


def parse_question(num: int, block: str) -> dict:
    body = strip_header(block)
    found = extract_options(body)
    if not found:
        raise ValueError("no options found")
    opt_start, options = found
    if len(options) < 4 or not all(options[:4]):
        raise ValueError(f"incomplete options: {options}")

    pre_lines = join_fraction_lines([
        ln.strip()
        for ln in body[:opt_start].splitlines()
        if ln.strip() and not GARBAGE.match(ln.strip())
    ])

    question_en = ""
    question_hi = ""
    exam = ""
    hindi_idx = next((i for i, ln in enumerate(pre_lines) if DEVANAGARI.search(ln)), len(pre_lines))

    for ln in pre_lines[:hindi_idx]:
        tag = EXAM_TAG.search(ln)
        if tag:
            exam = f" ({tag.group(0).strip('()')})"
            ln = EXAM_TAG.sub("", ln).strip()
        if ln:
            question_en = normalize_text(f"{question_en} {ln}".strip()) if question_en else normalize_text(ln)

    for ln in pre_lines[hindi_idx:]:
        if DEVANAGARI.search(ln) and not question_hi:
            question_hi = re.sub(r"\s+", " ", ln).strip()
            break

    if exam and exam.strip(" ()") not in question_en:
        question_en = f"{question_en}{exam}".strip()

    options = [clean_option(o) for o in options[:4]]
    if not all(options):
        raise ValueError(f"incomplete options after clean: {options}")

    entry: dict = {
        "question": question_en,
        "options": options,
        "correctAnswer": options[0],
        "explanation": "",
    }
    if question_hi:
        entry["questionHindi"] = question_hi
    return entry


def main() -> None:
    text = extract_pdf_text()
    parsed: list[dict] = []
    errors: list[str] = []

    for num in range(1, MAX_Q + 1):
        block = find_block(text, num)
        if not block:
            errors.append(f"Q{num}: block not found")
            continue
        try:
            parsed.append(parse_question(num, block))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Q{num}: {exc}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Parsed {len(parsed)}/{MAX_Q} questions -> {OUT_PATH}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
