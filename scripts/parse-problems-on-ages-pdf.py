"""Parse datas/maths/Problem-on-Ages.pdf into datas/maths/problems-on-ages.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "maths" / "Problem-on-Ages.pdf"
OUT_PATH = ROOT / "datas" / "maths" / "problems-on-ages.json"
MAX_Q = 76

HEADER = re.compile(r"BY Gagan Pratap", re.I)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|SELECTION POST|CGL|UP POLICE|DSSB|DP CONSTABLE|IB ACIO|ALP|NTPC|Group D)[^)]*\)",
    re.I,
)
GARBAGE = re.compile(
    r"^(?:BY Gagan Pratap|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|Kkr dhft|Kkr djsaA|fdruk gksxk|j\[kaM)\b.*)$",
    re.I,
)
ANSWER_LINE = re.compile(r"^\s*(\d+)\.\s*\(?([a-d])\)?\s*$", re.I)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for old, new in {"−": "-", "–": "-", "—": "-", "½": "1/2", "¼": "1/4", "¾": "3/4"}.items():
        text = text.replace(old, new)
    text = re.sub(r"\bcm2\b", "cm²", text, flags=re.I)
    text = re.sub(r"\byears?\b", "years", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def extract_pdf_text() -> str:
    doc = fitz.open(PDF_PATH)
    pages = [page.get_text() for page in doc]
    doc.close()
    return pages


MANUAL_OVERRIDES: dict[int, dict] = {
    45: {
        "question": (
            "Amit's father is aged five times more than Amit. After 6 years, he would be three "
            "and a half times of Amit's age. After further 9 years, how many times of Amit's "
            "age would he be?"
        ),
        "options": [
            "2 3/4 times",
            "2 1/4 times",
            "3 2/7 times",
            "2 3/7 times",
        ],
        "correctAnswer": "2 3/7 times",
    },
    46: {
        "question": (
            "P got married 15 years ago. Today her age is 1 3/5 times her age at the time of "
            "her marriage. At present her son's age is 1/5 of her age. What was her son's age "
            "4 years ago as a fraction of P's age at that time? (SSC CHSL PRE 2024)"
        ),
        "options": ["1/9", "1/8", "1/10", "5/9"],
        "correctAnswer": "1/9",
    },
}


def parse_answers(answer_text: str) -> dict[int, str]:
    answers: dict[int, str] = {}
    lines = [ln.strip() for ln in answer_text.splitlines() if ln.strip() and not HEADER.match(ln.strip())]
    i = 0
    while i < len(lines):
        m = re.match(r"^(\d+)\.\s*(?:\(([a-d])\))?\s*$", lines[i], re.I)
        if not m:
            i += 1
            continue
        num = int(m.group(1))
        letter = m.group(2)
        if not letter and i + 1 < len(lines):
            m2 = re.match(r"^\(([a-d])\)\s*$", lines[i + 1], re.I)
            if m2:
                letter = m2.group(1)
                i += 1
        if letter:
            answers[num] = letter.upper()
        i += 1
    return answers


def find_block(text: str, num: int) -> str | None:
    no_dot_kw = (
        r"The |If |A |An |What |When |In |Harsh |Daya |Priya |Mother |Five |Eight |Seven |"
        r"Two |Three |Suman |Krish |P got |X and Y |Ages |A says |A father "
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
                if re.match(r"^\[[a-d]\]|^[A-D]\)|\([a-d]\)", nxt, re.I):
                    break
                parts.append(nxt)
                i += 1
            results.append((pos, normalize_text(" ".join(parts))))
        else:
            i += 1
    return results


def extract_options(body: str) -> tuple[int, list[str]] | None:
    line_pats = [
        re.compile(r"^\[([a-d])\]\s*(.*)$", re.I),
        re.compile(r"^\([a-d]\)\s*(.*)$", re.I),
        re.compile(r"^[A-D]\)\s*(.*)$"),
        re.compile(r"^[A-D]\.\s*(.*)$"),
    ]
    for pat in line_pats:
        collected = collect_line_options(body, pat)
        if len(collected) >= 4:
            return collected[0][0], [v for _, v in collected[:4]]

    inline = re.findall(r"\[([a-d])\]\s*([^\[]+?)(?=\s*\[[a-d]\]|$)", body, re.I | re.S)
    if len(inline) >= 4:
        pos = body.find(f"[{inline[0][0]}]")
        return pos, [normalize_text(v) for _, v in inline[:4]]

    inline2 = re.findall(r"(?:^|\s*)([a-d])\)\s*([^a-d)]+?)(?=\s+[a-d]\)|$)", body, re.I | re.M)
    if len(inline2) >= 4:
        pos = body.lower().find(f"{inline2[0][0].lower()})")
        return pos, [normalize_text(v) for _, v in inline2[:4]]

    return None


def parse_question(num: int, block: str, answer_letter: str | None) -> dict:
    if num in MANUAL_OVERRIDES:
        ov = MANUAL_OVERRIDES[num]
        entry = {
            "question": ov["question"],
            "options": ov["options"],
            "correctAnswer": ov["correctAnswer"],
            "solution": "video solution will be provided soon",
        }
        body = strip_header(block)
        pre_lines = [ln.strip() for ln in body.splitlines() if ln.strip() and DEVANAGARI.search(ln)]
        if pre_lines:
            entry["questionHindi"] = re.sub(r"\s+", " ", pre_lines[0]).strip()
        return entry

    body = strip_header(block)
    found = extract_options(body)
    if not found:
        raise ValueError("no options found")
    opt_start, options = found
    if len(options) < 4 or not all(options[:4]):
        raise ValueError(f"incomplete options: {options}")

    pre_lines = [
        ln.strip()
        for ln in body[:opt_start].splitlines()
        if ln.strip() and not GARBAGE.match(ln.strip())
    ]

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

    correct = options[0]
    if answer_letter and answer_letter.upper() in "ABCD":
        idx = ord(answer_letter.upper()) - ord("A")
        if 0 <= idx < len(options):
            correct = options[idx]

    entry: dict = {
        "question": question_en,
        "options": options[:4],
        "correctAnswer": correct,
        "solution": "video solution will be provided soon",
    }
    if question_hi:
        entry["questionHindi"] = question_hi
    return entry


def main() -> None:
    pages = extract_pdf_text()
    answer_text = pages[-1]
    body_text = "\n".join(pages[:-1])
    answers = parse_answers(answer_text)

    if len(answers) < MAX_Q:
        print(f"Warning: only {len(answers)} answers found on last page")

    parsed: list[dict] = []
    errors: list[str] = []

    for num in range(1, MAX_Q + 1):
        block = find_block(body_text, num)
        if not block:
            errors.append(f"Q{num}: block not found")
            continue
        try:
            parsed.append(parse_question(num, block, answers.get(num)))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Q{num}: {exc}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Parsed {len(parsed)}/{MAX_Q} questions -> {OUT_PATH}")
    print(f"Answers mapped: {len(answers)}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
