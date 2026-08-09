"""Parse datas/maths/Trigonometry2.pdf into datas/maths/trigonometry2.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "maths" / "Trigonometry2.pdf"
OUT_PATH = ROOT / "datas" / "maths" / "trigonometry2.json"

QUESTION_START = re.compile(r"^(\d+)\.\s", re.M)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|SELECTION POST)[^)]*\)",
    re.I,
)
OPTION_SPLIT = re.compile(
    r"(?:^|\s|\()(?:\[([A-D])\]|([A-Da-d])\)|([A-Da-d])\)\s*)",
)
GARBAGE = re.compile(
    r"^(?:BY Gagan Pratap|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|dk eku|ds e/;|ds cjkcj|dk ljyh|Kkr djsaA|dk eku D;k)\b.*)$",
    re.I,
)


def normalize_math(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    repl = {
        "−": "-",
        "–": "-",
        "—": "-",
        "×": "×",
        "÷": "÷",
        "⋅": "·",
        "∠": "<",
        "": "θ",
        "Ø": "θ",
        "'": "'",
    }
    for old, new in repl.items():
        text = text.replace(old, new)
    # Only digit+o/O → degree (avoid corrupting "of", "cos", "cot")
    text = re.sub(r"(\d)\s*[oO]\b", r"\1°", text)
    text = re.sub(r"\s+", " ", text).strip()
    return fix_trig_superscripts(text)


def fix_trig_superscripts(text: str) -> str:
    for fn in ("sin", "cos", "tan", "cot", "sec", "cosec"):
        text = re.sub(rf"\b{fn}2(?=[θαβγABxyφ])", f"{fn}²", text)
        text = re.sub(rf"\b{fn}3(?=[θαβγABxyφ])", f"{fn}³", text)
        text = re.sub(rf"\b{fn}4(?=[θαβγABxyφA])", f"{fn}⁴", text)
        text = re.sub(rf"\b{fn}6(?=[θαβγABxyφ])", f"{fn}⁶", text)
        text = re.sub(rf"\b{fn}8(?=[θαβγABxyφA])", f"{fn}⁸", text)
        text = re.sub(rf"\b{fn}10(?=[θαβγABxyφA])", f"{fn}¹⁰", text)
        text = re.sub(rf"\b{fn}12(?=[θαβγABxyφA])", f"{fn}¹²", text)
    # x2, y2 etc. in algebraic contexts
    text = re.sub(r"\b([xy])2\b", r"\1²", text)
    text = re.sub(r"\b([xy])3\b", r"\1³", text)
    # x² 82+ y² 92 → x²/8² + y²/9² (PDF splits squared denominators)
    text = re.sub(r"([xy])²\s+(\d)2\+", r"\1²/\2²+", text)
    text = re.sub(r"([xy])²\s+(\d)2\b", r"\1²/\2²", text)
    return text


def join_fraction_lines(lines: list[str]) -> list[str]:
    """Merge numerator/denominator lines split by PDF extraction."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        cur = lines[i].strip()
        if not cur:
            i += 1
            continue
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            # num / den where den starts with sqrt or is numeric fraction part
            if (
                nxt
                and not OPTION_SPLIT.search(nxt)
                and not GARBAGE.match(nxt)
                and (
                    nxt.startswith("√")
                    or re.match(r"^[\d√+\-().a-zA-Z²³]+$", nxt)
                )
                and re.match(r"^[\d√+\-().a-zA-Z²³]+$", cur)
                and len(cur) < 40
                and len(nxt) < 40
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


def split_blocks(text: str) -> list[tuple[int, str]]:
    matches = list(QUESTION_START.finditer(text))
    blocks: list[tuple[int, str]] = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((num, text[m.start() : end].strip()))
    return blocks


def strip_header(block: str) -> str:
    block = re.sub(r"^\d+\.\s*", "", block, count=1)
    block = re.sub(r"BY Gagan Pratap", "", block, flags=re.I)
    return block.strip()


def find_first_option(block: str) -> int | None:
    for m in OPTION_SPLIT.finditer(block):
        letter = (m.group(1) or m.group(2) or m.group(3))
        if letter:
            return m.start()
    return None


def split_options(body: str) -> list[tuple[str, str]]:
    """Return [(letter, text), ...] for A-D."""
    matches = list(OPTION_SPLIT.finditer(body))
    if not matches:
        return []

    pairs: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        letter = (m.group(1) or m.group(2) or m.group(3)).upper()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end].strip()
        lines = [ln.strip() for ln in chunk.splitlines() if ln.strip() and not GARBAGE.match(ln.strip())]
        lines = join_fraction_lines(lines)
        text = normalize_math(" ".join(lines))
        pairs.append((letter, text))
    return pairs


def parse_question(num: int, block: str) -> dict:
    body = strip_header(block)
    opt_start = find_first_option(body)
    if opt_start is None:
        raise ValueError("no options found")

    pre = body[:opt_start].strip()
    pre_lines = [ln.strip() for ln in pre.splitlines() if ln.strip() and not GARBAGE.match(ln.strip())]

    question_en = ""
    question_hi = ""
    exam = ""

    # Stop English accumulation at first Hindi line (PDF often repeats the formula after Hindi)
    hindi_idx = next((i for i, ln in enumerate(pre_lines) if DEVANAGARI.search(ln)), len(pre_lines))
    en_lines = pre_lines[:hindi_idx]
    hi_lines = pre_lines[hindi_idx:]

    for ln in en_lines:
        tag = EXAM_TAG.search(ln)
        if tag:
            exam = f" ({tag.group(0).strip('()')})"
            ln = EXAM_TAG.sub("", ln).strip()
        if ln:
            question_en = normalize_math(f"{question_en} {ln}".strip()) if question_en else normalize_math(ln)
        if re.search(r"(?:is equal to:|is:|=\?|\?\s*$)", ln, re.I):
            break

    for ln in hi_lines:
        if DEVANAGARI.search(ln) and not question_hi:
            question_hi = re.sub(r"\s+", " ", ln).strip()
            break

    if exam and exam.strip(" ()") not in question_en:
        question_en = f"{question_en}{exam}".strip()

    opt_pairs = split_options(body[opt_start:])
    if len(opt_pairs) < 4:
        raise ValueError(f"only {len(opt_pairs)} options")

    # Keep first A,B,C,D in order
    by_letter: dict[str, str] = {}
    for letter, text in opt_pairs:
        if letter not in by_letter and text:
            by_letter[letter] = text

    options = [by_letter.get(ch, "") for ch in "ABCD"]
    if any(not o for o in options):
        raise ValueError(f"missing options: {by_letter}")

    entry: dict = {
        "question": question_en,
        "options": options,
        "correctAnswer": "A",
        "explanation": "",
    }
    if question_hi:
        entry["questionHi"] = question_hi
    return entry


def main() -> None:
    text = extract_pdf_text()
    blocks = split_blocks(text)
    parsed: list[dict] = []
    errors: list[str] = []

    for num, block in blocks:
        try:
            parsed.append(parse_question(num, block))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Q{num}: {exc}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Parsed {len(parsed)}/{len(blocks)} questions -> {OUT_PATH}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
