"""Parse datas/maths/Race-Sheet.pdf into datas/maths/race-sheet.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "maths" / "Race-Sheet.pdf"
OUT_PATH = ROOT / "datas" / "maths" / "race-sheet.json"
MAX_Q = 32

HEADER = re.compile(r"BY:-GAGAN PRATAP|Race Sheet", re.I)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|SELECTION POST|CGL|UP POLICE|DSSB|DP CONSTABLE|IB ACIO|ALP|NTPC|Group D|IBPS CLERK|Miscellaneous)[^)]*\)",
    re.I,
)
GARBAGE = re.compile(
    r"^(?:BY:-GAGAN PRATAP|Race Sheet|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|Kkr dhft|Kkr djsaA|fdruk gksxk|nkSM\+|yach)\b.*)$",
    re.I,
)

MANUAL_OVERRIDES: dict[int, dict] = {
    2: {
        "question": (
            "Ashok runs 2 2/3 times as fast as Bharat. If Ashok gives Bharat a head start of "
            "160 m, then how far must the winning post be so that Ashok and Bharat can reach "
            "it at the same time? (SSC CGL 2023 PRE)"
        ),
        "options": ["225 m", "256 m", "240 m", "200 m"],
        "correctAnswer": "256 m",
    },
    4: {
        "question": (
            "A's speed is 30% more than that of B. If A and B run a race on a 117 m length race, "
            "what part of the length of the race should A give B as a head start, so that the race "
            "ends in a dead heat?"
        ),
        "options": ["90 m", "26 m", "27 m", "36 m"],
        "correctAnswer": "27 m",
    },
    21: {
        "question": (
            "In a linear race of 1000 m, A beats B by 50 m or 5 seconds. What is the difference "
            "between the speeds (in m/sec) of A and B? (SSC CGL 2022 PRE)"
        ),
        "options": ["1/10", "10/19", "9/10", "9/19"],
        "correctAnswer": "10/19",
    },
    22: {
        "question": (
            "In a 1200 m race, bike A beats bike B by 100 m. Bike B beats bike C by 100 m in a "
            "600 m race. If bike A beats bike C by 30 sec in a 720 m race, then what is the "
            "speed of bike C? (SSC CGL 2022 PRE)"
        ),
        "options": ["17/3 m/sec", "26/9 m/sec", "17/9 m/sec", "26/3 m/sec"],
        "correctAnswer": "26/9 m/sec",
    },
    28: {
        "question": (
            "In a 1000 m race, Ravi gives Vinod a start of 40 m and beats him by 19 seconds. If "
            "Ravi gives a start of 30 seconds, Vinod beats Ravi by 40 m. What is the ratio of "
            "speed of Ravi to that of Vinod?"
        ),
        "options": ["5:4", "4:3", "6:5", "8:5"],
        "correctAnswer": "6:5",
    },
    31: {
        "question": (
            "Salman reaches school everyday at 4 pm to pickup children. On Saturday school over "
            "at 3 pm and children start walking home. Salman met them on their way and return "
            "home 20 min early. How much time did children walk?"
        ),
        "options": ["10 minutes", "15 minutes", "20 minutes", "25 minutes"],
        "correctAnswer": "20 minutes",
    },
    32: {
        "question": (
            "A monkey climbing up greased pole ascends 10 m in a minute and slips down 2 m in "
            "alternate minute. If pole is 63 m high, how long will it take to reach top of pole?"
        ),
        "options": ["13 minutes", "14 minutes", "15 minutes", "16 minutes"],
        "correctAnswer": "15 minutes",
    },
}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for old, new in {"−": "-", "–": "-", "—": "-", "½": "1/2", "¼": "1/4", "¾": "3/4"}.items():
        text = text.replace(old, new)
    text = re.sub(r"\bcm2\b", "cm²", text, flags=re.I)
    text = re.sub(r"\bm/sec\b", "m/sec", text, flags=re.I)
    text = re.sub(r"\bkm/h\b", "km/h", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


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
                re.match(r"^[\d%./+\-()m/s]+$", cur, re.I)
                and re.match(r"^[\d%./+\-()m/s]+$", nxt, re.I)
                and len(cur) < 20
                and len(nxt) < 20
                and "/" not in cur
            ):
                out.append(f"{cur}/{nxt}")
                i += 2
                continue
        out.append(cur)
        i += 1
    return out


def extract_body_text() -> str:
    doc = fitz.open(PDF_PATH)
    pages = [page.get_text() for page in doc]
    doc.close()
    body_pages = pages
    last = pages[-1] if pages else ""
    if re.search(r"^\s*1\.\s*\([a-d]\)", last, re.I | re.M):
        body_pages = pages[:-1]
    return "\n".join(body_pages)


def parse_answers_from_last_page() -> dict[int, str]:
    doc = fitz.open(PDF_PATH)
    last = doc[-1].get_text()
    doc.close()
    answers: dict[int, str] = {}
    lines = [ln.strip() for ln in last.splitlines() if ln.strip() and not HEADER.match(ln.strip())]
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
        r"Geeta |Ashok |A runs |A's |A takes |In |The |A and B |A gives |Ramesh |Salman |"
        r"A monkey |Savitha |Three |Priya |If |What |When |Ravi |Five |Eight |Seven |Two |"
        r"Krish |Suman |Paulson "
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
                if re.match(r"^[A-D]\)|\([a-d]\)|\[?[A-D]\]?|^[1-4]\.", nxt, re.I):
                    break
                parts.append(nxt)
                i += 1
            results.append((pos, normalize_text(" ".join(join_fraction_lines(parts)))))
        else:
            i += 1
    return results


def split_by_markers(body: str) -> list[tuple[str, str]]:
    markers = re.compile(
        r"(?:^|\s)(?:"
        r"\(([a-d])\)|"
        r"([A-D])\)|"
        r"\[([A-D])\]|"
        r"([A-D])\.\s*|"
        r"([1-4])\.\s*"
        r")",
        re.I | re.M,
    )
    matches = list(markers.finditer(body))
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
        text = normalize_text(" ".join(join_fraction_lines(lines)))
        if text:
            pairs.append((letter, text))
    return pairs


def extract_numbered_options(body: str) -> tuple[int, list[str]] | None:
    lines = body.splitlines()
    opts: list[str] = []
    first_pos = None
    for ln in lines:
        m = re.match(r"^\s*([1-4])\.(\s*)(.+)$", ln.strip())
        if not m:
            continue
        if first_pos is None:
            first_pos = body.find(ln)
        opts.append(normalize_text(m.group(3).strip()))
        if len(opts) >= 4:
            break
    if len(opts) >= 4 and first_pos is not None:
        return first_pos, opts[:4]
    return None


def extract_options(body: str) -> tuple[int, list[str]] | None:
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
            pos = marker_pairs[0][1][:8]
            idx = body.find(pos[: min(6, len(pos))])
            return (idx if idx >= 0 else 0), options

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

    multi = re.findall(r"\(([a-d])\)\s*([^()]+?)(?=\s*\([a-d]\)|$)", body, re.I | re.S)
    if len(multi) >= 4:
        pos = body.find(f"({multi[0][0].lower()})")
        return pos, [normalize_text(v) for _, v in multi[:4]]

    inline = re.findall(r"(?:^|\s*)([A-D])\)\s*([^A-D)]+?)(?=\s+[A-D]\)|$)", body, re.I | re.M)
    if len(inline) >= 4:
        pos = body.find(f"{inline[0][0]})")
        return pos, [normalize_text(v) for _, v in inline[:4]]

    bracket = re.findall(r"\(([A-D])\)\s*([^\(]+?)(?=\s*\([A-D]\)|$)", body, re.I | re.S)
    if len(bracket) >= 4:
        pos = body.find(f"({bracket[0][0]})")
        return pos, [normalize_text(v) for _, v in bracket[:4]]

    return None


def parse_question(num: int, block: str, answer_letter: str | None) -> dict:
    if num in MANUAL_OVERRIDES:
        ov = MANUAL_OVERRIDES[num]
        entry = {
            "question": ov["question"],
            "options": ov["options"],
            "correctAnswer": ov["correctAnswer"],
        }
        body = strip_header(block)
        for ln in body.splitlines():
            if DEVANAGARI.search(ln):
                entry["questionHindi"] = re.sub(r"\s+", " ", ln.strip())
                break
        return entry

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
        if ln and not re.match(r"^[A-Za-z]{1,3}\s+dh\s+", ln):
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
    }
    if question_hi:
        entry["questionHindi"] = question_hi
    return entry


def main() -> None:
    text = extract_body_text()
    answers = parse_answers_from_last_page()
    parsed: list[dict] = []
    errors: list[str] = []

    for num in range(1, MAX_Q + 1):
        block = find_block(text, num)
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
    print(f"Answers from PDF: {len(answers)}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
