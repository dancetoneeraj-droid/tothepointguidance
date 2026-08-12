"""Parse geometry sheets 4-12 into datas/maths/geometry/all-sheets.json."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
GEO_DIR = ROOT / "datas" / "maths" / "geometry"
OUT_PATH = GEO_DIR / "all-sheets.json"

SHEET_FILES: list[tuple[int, Path]] = [
    (4, GEO_DIR / "Geometry-Sheet-4.pdf"),
    (5, GEO_DIR / "Geometry-Sheet-5.pdf"),
    (6, GEO_DIR / "Geometry-Sheet-6.pdf"),
    (7, GEO_DIR / "Geometry-Sheet-7.pdf"),
    (8, GEO_DIR / "Geometry-Sheet-8.pdf"),
    (9, GEO_DIR / "Geometry-Sheet--9.pdf"),
    (10, ROOT / "datas" / "maths" / "Geometry-10.pdf"),
    (11, GEO_DIR / "Geometry-Sheet-11.pdf"),
    (12, GEO_DIR / "Geometry-Sheet--12.pdf"),
]

HEADER = re.compile(r"BY:?[-\s]*GAGAN|Equilateral Triangle|Isosceles|Miscellaneous", re.I)
DEVANAGARI = re.compile(r"[\u0900-\u097F]")
EXAM_TAG = re.compile(
    r"\((?:SSC|CDS|RRB|CPO|CHSL|ICAR|MTS|GD|MAINS|PRE|SELECTION POST|CGL|UP POLICE|UPSC|IB ACIO|ALP|NTPC|JE|CLERK)[^)]*\)",
    re.I,
)
GARBAGE = re.compile(
    r"^(?:BY:?[-\s]*GAGAN|Equilateral Triangle|Isosceles|--- Page \d+ ---|\s*$|"
    r".*(?:vkSj|gS\]|rks|Kkr dhft|fdruk gksxk|f=Hkqt|f=Hkqs)\b.*)$",
    re.I,
)

MANUAL: dict[tuple[int, int], dict] = {
    (4, 15): {
        "question": "In the triangle PQR, S is the midpoint of QR. X is any point on PR. T is the point on QR such that PT||SX. If the area of triangle PQR is 6.4 sq. cm, then the area of triangle RTX is",
        "options": ["3.2 sq cm", "2.4 sq cm", "4 sq cm", "CND"],
        "correctAnswer": "3.2 sq cm",
    },
    (5, 7): {
        "question": "The ratio of the lengths of two corresponding sides of two similar triangles is 17 : 13. The ratio of the areas of these two triangles, in the order mentioned, is: (RRB JE 2024)",
        "options": ["289 : 169", "17 : 13", "34 : 26", "290 : 170"],
        "correctAnswer": "289 : 169",
    },
    (5, 25): {
        "question": "In ΔABC, XY is drawn parallel to BC, cutting sides at X and Y, where AB = 5.4 cm, BC = 7.2 cm and BX = 3 cm. What is the length of XY (in cm)?",
        "options": ["4.3", "3.0", "3.2", "2.8"],
        "correctAnswer": "3.2",
    },
    (5, 54): {
        "question": "In ∆ADC, E and B are the points on the sides AD and AC respectively such that ∠ABE = ∠ADC. If AE = 6 cm, BC = 2 cm, BE = 3 cm and CD = 5 cm then, (AB + DE) is equal to?",
        "options": ["14 cm", "16 cm", "49/3 cm", "46/3 cm"],
        "correctAnswer": "14 cm",
    },
    (5, 66): {
        "question": "A man looks at the reflection of the top of the lamp-post on the mirror that is 6.6 m away from the foot of the lamppost. The man's height is 1.25 m and he is standing 2 m away from the mirror. Assuming that the mirror is placed on the ground, facing the sky and the man, and that the mirror and the lamp-post are in a same line, find the height of the lamp-post (in metres). (SSC CHSL Pre 2024)",
        "options": ["4.28", "4.45", "3.97", "4.13"],
        "correctAnswer": "4.13",
    },
    (6, 4): {
        "question": "In ∆ABC and ∆ DEF, ∠A = 55°, AB = DE, AC = DF, ∠ E = 85° and ∠F = 40°. By which property are ∆ ABC and ∆ DEF congruent? (SSC CGL 2022)",
        "options": [
            "SAS property",
            "ASA property",
            "RHS property",
            "SSS property",
        ],
        "correctAnswer": "SAS property",
    },
    (6, 14): {
        "question": "In a triangle ABC, D is the mid point of BC. If DL perpendicular to AB and DM perpendicular to AC such that DL = DM. Then the triangle will be? (SSC CGL PRE 2024)",
        "options": [
            "Isosceles triangle",
            "Right angled triangle",
            "Obtuse angle triangle",
            "Equilateral triangle",
        ],
        "correctAnswer": "Isosceles triangle",
    },
    (8, 24): {
        "question": "Find the distance between incentre and circumcenter of a triangle whose sides are 6, 8 and 10 cm?",
        "options": ["√5 cm", "2 cm", "3 cm", "√13 cm"],
        "correctAnswer": "√5 cm",
    },
    (9, 14): {
        "question": "If AD, BE and CF are the medians of a triangle ABC, then the true statement is?",
        "options": [
            "AD+BE+CF<AB+BC+CA",
            "AD+BE+CF > (3/4)(AB+BC+CA)",
            "AD+BE+CF>AB+BC+CA",
            "AD+BE+CF=√2(AB+BC+CA)",
        ],
        "correctAnswer": "AD+BE+CF<AB+BC+CA",
    },
    (10, 20): {
        "question": "An equilateral triangle ABC is inscribed in a circle as shown in figure. A square of largest possible area is made inside this triangle as shown. Another circle made inscribing the square. What is the ratio of area of smaller circle and the larger circle?",
        "options": [
            "(15−12√3): 1",
            "(63−36√3): 4",
            "(7−4√3): 2",
            "(4−2√3): 3",
        ],
        "correctAnswer": "(7−4√3): 2",
    },
    (11, 31): {
        "question": "An isosceles triangle ABC is right-angled at B, D is a point inside the triangle ABC. P and Q are the feet of the perpendiculars drawn from D on the sides AB and AC respectively of ∆ABC. If AP = a cm, AQ = b cm and BAD = 15°, sin 75° =",
        "options": ["2b/√3a", "2a/√3b", "√3a/2b", "a/2b"],
        "correctAnswer": "2b/√3a",
    },
    (12, 33): {
        "question": "What is the area (in hectares) of a rhombus-shaped field whose side is 146 m and one of its diagonals is 192 m?",
        "options": ["2.102", "2.121", "2.012", "2.112"],
        "correctAnswer": "2.112",
    },
    (12, 117): {
        "question": "Chord AB of a circle of radius 10 cm is at a distance 8 cm from the centre O. If tangents drawn at A and B intersect at P, then the length of the tangent AP (in cm) is:",
        "options": ["4", "15", "3.75", "7.5"],
        "correctAnswer": "7.5",
    },
    (12, 149): {
        "question": "In the given figure ABC is equilateral triangle. If CD = 8 cm and BD = 6 cm, then find the value of x?",
        "options": ["14", "10", "12", "15"],
        "correctAnswer": "10",
    },
}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for old, new in {"−": "-", "–": "-", "—": "-", "½": "1/2", "¼": "1/4", "¾": "3/4"}.items():
        text = text.replace(old, new)
    text = re.sub(r"\bcm2\b", "cm²", text, flags=re.I)
    text = re.sub(r"\bsq\.?\s*cm\b", "cm²", text, flags=re.I)
    text = re.sub(r"(\d)\s+(\d)(°|cm|m|√)", r"\1\2\3", text)
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
                re.match(r"^[\d%./+\-()√°cm²³]+$", cur, re.I)
                and re.match(r"^[\d%./+\-()√°cm²³]+$", nxt, re.I)
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


def count_questions(text: str) -> int:
    found = 0
    for n in range(1, 500):
        if re.search(rf"(?:^|\n)\s*{n}\.\s", text, re.M):
            found = n
        elif n > found + 3:
            break
    return found


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
    block = text[m.start() : end].strip()
    if not m2:
        footer = re.search(r"\n\s*BY:?\s*[-\s]*GAGAN\b", block, re.I)
        if footer and re.search(r"\n\s*1\.\s", block[footer.end() :]):
            block = block[: footer.start()].strip()
    return block


def strip_header(block: str) -> str:
    block = re.sub(r"^\d+\s*\.\s*", "", block, count=1)
    block = re.sub(r"^\d+\s+(?!\.)(?=[A-Za-zΔ∆])", "", block, count=1)
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


def extract_ab_options(body: str) -> tuple[int, list[str]] | None:
    first = re.search(r"(?:^|\n)\s*\(a\)\s*", body, re.I | re.M)
    if not first:
        first = re.search(r"(?:^|\n)\s*a\)\s*", body, re.I | re.M)
    if not first:
        return None
    tail = body[first.start() :]
    markers = list(re.finditer(r"(?<![A-Za-z0-9])([a-d])\)\s*", tail, re.I))
    if len(markers) < 4:
        return None
    options: list[str] = []
    for i in range(4):
        start = markers[i].end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(tail)
        chunk = tail[start:end]
        lines = [
            ln.strip()
            for ln in chunk.splitlines()
            if ln.strip() and not GARBAGE.match(ln.strip())
        ]
        text = normalize_text(" ".join(join_fraction_lines(lines)))
        options.append(text)
    if all(options):
        return first.start(), options
    return None


def split_by_markers(body: str) -> list[tuple[int, str, str]]:
    markers = re.compile(
        r"(?:^|\n)\s*(?:"
        r"\(([a-d])\)|"
        r"([A-D])\)|"
        r"\[([A-D])\]|"
        r"([A-D])\.\s+|"
        r"([1-4])\.\s+"
        r")",
        re.I | re.M,
    )
    matches = list(markers.finditer(body))
    if not matches:
        return []
    pairs: list[tuple[int, str, str]] = []
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
            pairs.append((m.start(), letter, text))
    return pairs


def extract_options(body: str) -> tuple[int, list[str]] | None:
    ab = extract_ab_options(body)
    if ab:
        return ab

    line_pats = [
        re.compile(r"^\([a-d]\)\s*(.*)$", re.I),
        re.compile(r"^[a-d]\)\s*(.*)$", re.I),
        re.compile(r"^[A-D]\)\s*(.*)$"),
        re.compile(r"^\[([A-D])\]\s*(.*)$", re.I),
        re.compile(r"^\[([A-D])\]\s+(.*)$", re.I),
        re.compile(r"^([1-4])\.\s*(.+)$"),
    ]
    for pat in line_pats:
        collected = collect_line_options(body, pat)
        if len(collected) >= 4:
            return collected[0][0], [v for _, v in collected[:4]]

    marker_pairs = split_by_markers(body)
    if len(marker_pairs) >= 4:
        by_letter: dict[str, str] = {}
        first_pos = marker_pairs[0][0]
        for _, letter, text in marker_pairs:
            if letter not in by_letter and text:
                by_letter[letter] = text
        options = [by_letter.get(ch, "") for ch in "ABCD"]
        if all(options):
            return first_pos, options

    multi = re.findall(r"\(([a-d])\)\s*([^()]+?)(?=\s*\([a-d]\)|$)", body, re.I | re.S)
    if len(multi) >= 4:
        return body.find(f"({multi[0][0].lower()})"), [normalize_text(v) for _, v in multi[:4]]

    inline = re.findall(r"(?:^|\s*)([A-D])\)\s*([^A-D)]+?)(?=\s+[A-D]\)|$)", body, re.I | re.M)
    if len(inline) >= 4:
        return body.find(f"{inline[0][0]})"), [normalize_text(v) for _, v in inline[:4]]

    bracket = re.findall(r"\[([A-D])\]\s*([^\[]+?)(?=\s*\[[A-D]\]|$)", body, re.I | re.S)
    if len(bracket) >= 4:
        return body.find(f"[{bracket[0][0]}]"), [normalize_text(v) for _, v in bracket[:4]]

    return None


def parse_question(sheet: int, num: int, block: str) -> dict:
    key = (sheet, num)
    if key in MANUAL:
        ov = MANUAL[key]
        entry = {"question": ov["question"], "options": ov["options"], "correctAnswer": ov["correctAnswer"], "sheet": sheet}
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

    if not question_en.strip():
        if question_hi:
            question_en = question_hi
        elif opt_start > 0:
            question_en = normalize_text(body[:opt_start].strip())

    entry: dict = {
        "question": question_en,
        "options": options[:4],
        "correctAnswer": options[0],
        "sheet": sheet,
    }
    if question_hi:
        entry["questionHindi"] = question_hi
    return entry


def parse_sheet(sheet_num: int, path: Path) -> list[dict]:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    # drop answer key page if present
    if re.search(r"^\s*1\.\s*\([a-d]\)", text.split("BY")[-1], re.I | re.M):
        parts = re.split(r"BY:?[-\s]*GAGAN", text, flags=re.I)
        if len(parts) > 1 and re.search(r"^\s*1\.\s*\([a-d]\)", parts[-1], re.I | re.M):
            text = "BY".join(parts[:-1])

    max_q = count_questions(text)
    parsed: list[dict] = []
    errors: list[str] = []
    for num in range(1, max_q + 1):
        block = find_block(text, num)
        if not block:
            errors.append(f"Q{num}: block not found")
            continue
        try:
            parsed.append(parse_question(sheet_num, num, block))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Q{num}: {exc}")

    print(f"  Sheet {sheet_num}: {len(parsed)}/{max_q} parsed")
    if errors:
        print(f"    errors ({len(errors)}):")
        for err in errors[:15]:
            print(f"      - {err}")
        if len(errors) > 15:
            print(f"      ... +{len(errors)-15} more")
        if len(parsed) < max_q * 0.9:
            raise SystemExit(1)
    return parsed


def main() -> None:
    all_q: list[dict] = []
    for sheet_num, path in SHEET_FILES:
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        print(f"Parsing {path.name}...")
        all_q.extend(parse_sheet(sheet_num, path))

    OUT_PATH.write_text(json.dumps(all_q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTotal {len(all_q)} questions -> {OUT_PATH}")


if __name__ == "__main__":
    main()
