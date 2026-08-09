"""Parse datas/maths/Discount.pdf into datas/maths/discount.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "datas" / "maths" / "Discount.pdf"
OUT_PATH = ROOT / "datas" / "maths" / "discount.json"
MAX_Q = 142

HEADER = re.compile(r"BY:-GAGAN PRATAP", re.I)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|SELECTION POST|CGL|UP POLICE)[^)]*\)",
    re.I,
)
GARBAGE = re.compile(
    r"^(?:BY:-GAGAN PRATAP|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|Kkr djsaA|oLrqvksa|foØ;|ewY;|ykHk|NwV)\b.*)$",
    re.I,
)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for old, new in {"−": "-", "–": "-", "—": "-", "½": "1/2", "¼": "1/4", "¾": "3/4"}.items():
        text = text.replace(old, new)
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
                re.match(r"^[\d%./+\-()₹Rs]+$", cur, re.I)
                and re.match(r"^[\d%./+\-()₹Rs]+$", nxt, re.I)
                and len(cur) < 20 and len(nxt) < 20 and "/" not in cur
            ):
                out.append(f"{cur}/{nxt}")
                i += 2
                continue
            if i + 2 < len(lines) and re.match(r"^\d+$", cur) and re.match(r"^\d+$", nxt):
                third = lines[i + 2].strip()
                if third.endswith("%"):
                    out.append(f"{cur} {nxt}/{third.replace('%', '')}%")
                    i += 3
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
        r"When |A shopkeeper |A store |A dealer |A merchant |A seller |A trader |"
        r"A distributor |A renowned |A Rs |If |The |Under |After |Due |Ramesh |"
        r"Satish |Rahim |Rajesh |Harish |Sam |CP |MP |Even |Find |Calculate |"
        r"Determine |Evaluate |What |How |An |In |On |By |Two |Three |Four |Five |"
        r"Raghu |Manish |Mahesh |Ramesh |Harish |Rajesh |Due to |The marked |"
        r"The cost |The difference |A person |A milkman |A shopkeeper |A 45"
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
        r"When |A shopkeeper |A store |A dealer |A merchant |A seller |If |The |"
        r"Under |After |Due |Even |What |How |An |Raghu |Find |Calculate |"
        r"A person |A Rs |A 45 |A renowned |A distributor |A trader |Ramesh "
    )
    nxt = re.compile(rf"(?:^|\n)\s*{num + 1}(?:\.\s|\s+\.\s|\s+(?!\.)(?:{nxt_kw}))", re.M)
    m2 = nxt.search(text, m.end())
    return text[m.start() : (m2.start() if m2 else len(text))].strip()


def strip_header(block: str) -> str:
    block = re.sub(r"^\d+\s*\.\s*", "", block, count=1)
    block = re.sub(r"^\d+\s+(?!\.)(?=[A-Za-z])", "", block, count=1)
    return HEADER.sub("", block).strip()


def collect_line_options(body: str, pat: re.Pattern) -> list[tuple[int, str]]:
    """Collect options where value may continue on following non-option lines."""
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
                if re.match(r"^[A-D]\)|\([a-d]\)|[1-4]\.", nxt, re.I):
                    break
                parts.append(nxt)
                i += 1
            results.append((pos, normalize_text(" ".join(join_fraction_lines(parts)))))
        else:
            i += 1
    return results
def extract_options(body: str) -> tuple[int, list[str]] | None:
    """Return (start_index, [4 options])."""
    line_pats = [
        re.compile(r"^\([a-d]\)\s*(.*)$", re.I),
        re.compile(r"^[A-D]\)\s*(.*)$"),
        re.compile(r"^[A-D]\.\s*(.*)$"),
        re.compile(r"^([1-4])\.\s+(.*)$"),
    ]
    for pat in line_pats:
        collected = collect_line_options(body, pat)
        if len(collected) >= 4:
            return collected[0][0], [v for _, v in collected[:4]]
        if len(collected) == 3:
            return collected[0][0], [v for _, v in collected] + [""]

    pat_num = re.compile(r"(?m)^\s*([1-4])\.\s+(.+)$")
    matches = list(pat_num.finditer(body))
    if len(matches) >= 4:
        return matches[0].start(), [normalize_text(m.group(2)) for m in matches[:4]]

    # Inline: A)xxx B)yyy C)zzz D)www
    inline = re.findall(r"(?:^|\s)([A-D])\)\s*([^A-D)]+?)(?=\s+[A-D]\)|$)", body)
    if len(inline) >= 4:
        pos = body.find(f"{inline[0][0]})")
        return pos, [normalize_text(v) for _, v in inline[:4]]

    # Inline lowercase a) b) c) d)
    inline2 = re.findall(r"(?:^|\s)([a-d])\)\s*([^a-d)]+?)(?=\s+[a-d]\)|$)", body, re.I)
    if len(inline2) >= 3:
        pos = body.lower().find(f"{inline2[0][0].lower()})")
        opts = [normalize_text(v) for _, v in inline2]
        while len(opts) < 4:
            opts.append("")
        return pos, opts[:4]

    return None


def parse_question(num: int, block: str) -> dict:
    body = strip_header(block)
    found = extract_options(body)
    if not found:
        raise ValueError("no options found")
    opt_start, options = found
    if len(options) < 4 or not all(options[:3]):
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
        if re.search(r"(?:\?\s*$|is:|are:|find |calculate |determine |what |how much)", ln, re.I):
            break

    for ln in pre_lines[hindi_idx:]:
        if DEVANAGARI.search(ln) and not question_hi:
            question_hi = re.sub(r"\s+", " ", ln).strip()
            break

    if exam and exam.strip(" ()") not in question_en:
        question_en = f"{question_en}{exam}".strip()

    entry: dict = {
        "question": question_en,
        "options": options[:4],
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


if __name__ == "__main__":
    main()
