"""Import SSC 2025 QUESTION BANK.pdf into the banks that still have empty slots.

Rules this script enforces:
  * only placeholder slots are written, so existing questions cannot be touched;
  * no bank is grown - each chapter stops when its empty slots run out;
  * questions that need a figure, or that survive extraction in poor shape, are
    dropped rather than imported half-broken;
  * the correct answer comes from the chapter's printed answer key.

Solutions are deliberately left empty: the PDF typesets them as 2D math and the
text layer collapses stacked fractions into unusable lines.

Run with --write to actually modify the banks; the default is a dry run.
"""

import json
import re
import sys
from pathlib import Path

import fitz

import qbank_lib as Q
from qbank_lib import CHAPTERS

ROOT = Path(__file__).resolve().parent.parent
BACKUP = Path(__file__).resolve().parent / "_qbank-backup"
PLACEHOLDER_MARK = "add real content"
LETTERS = "abcd"

# bank file -> list of chapters to draw from, in order
PLAN = [
    ("data/maths/average.json", ["Average"]),
    ("data/maths/simple-interest.json", ["Simple Interest"]),
    ("data/maths/partnership.json", ["Partnership"]),
    ("data/maths/ratio-proportion.json", ["Ratio & Proportion"]),
    ("data/maths/compound-interest.json", ["Compound Interest"]),
    ("data/maths/number-system.json", ["Number System", "Lcm And Hcf"]),
    # Trigonometry is deliberately absent: that chapter draws its radicals and
    # fractions as vector art, so "√2 sinA" extracts as "2 sinA" and the printed
    # question cannot be reproduced faithfully from the text layer.
    ("data/maths/time-speed-distance.json", ["Time and Distance", "Train"]),
    ("data/maths/profit-loss.json", ["Profit and Loss"]),
    ("data/maths/mensuration-3d.json", ["Mensuration 2D & 3D"]),
]

# a question we cannot show faithfully without the artwork that goes with it
NEEDS_ART = re.compile(
    r"\b(figure|fig\.|diagram|shown below|given below the|graph|pie chart|bar chart|"
    r"histogram|the table|following table|adjoining)\b",
    re.I,
)
# leftovers of a collapsed 2D layout: a run of bare numbers with no operator
JUNK_RUN = re.compile(r"(?:(?<=\s)|^)\d[\d,.]*(?:\s+\d[\d,.]*){3,}\s*$")
# a stacked fraction or a radical flattens to two bare numbers side by side
# ("8 17" is 8/17, "5 6" is 5√6) and the meaning is gone
COLLAPSED = re.compile(r"(?<![\d:/])\b\d[\d,]*(?:\.\d+)?\s+\d[\d,]*(?:\.\d+)?\b(?![:/%])")
COLLAPSED_SYMBOL = re.compile(r"[π√]\s*\d|\d\s*[π√]\s+\d")
TRAILING_JUNK = re.compile(r"[?.]\s*[\d\s,.:;+\-–×/()¹²³⁴⁵⁶⁷⁸⁹⁰]{1,20}$")
EXAM_STAMP = re.compile(
    r"\s*(SSC|DP|MTS|DELHI POLICE|ICAR|RRB|UP POLICE)[A-Za-z &\-]{0,20}"
    r"\d{1,2}/\d{1,2}/\d{4}\s*(\([A-Za-z]*-?\s*\d+\))?\s*",  # the "Shift" word is
    re.I,                                                     # sometimes in another font
)
# a stem that opens mid-expression lost its leading function name to the art layer
BROKEN_OPENING = re.compile(r"^[a-z]\s*[=+]|^[=+×/]")
PLAIN_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")

# a chapter whose questions must mention its own subject, so strays from the
# neighbouring chapter do not land in the wrong bank
TOPIC_WORDS = {
    "Average": re.compile(r"\b(average|mean)\b", re.I),
    "Simple Interest": re.compile(r"\b(interest|principal|annum|rate|sum|invest|borrow)", re.I),
    "Partnership": re.compile(r"\b(invest|partner|capital|profit|share|business)", re.I),
    "Ratio & Proportion": re.compile(r"(ratio|proportion|\d\s*:\s*\d)", re.I),
    "Compound Interest": re.compile(r"\b(compound|interest|annum|amount|principal)", re.I),
    "Number System": re.compile(
        r"\b(number|digit|divisib|remainder|prime|factor|multiple|square|cube|"
        r"rational|irrational|integer|lcm|hcf)", re.I
    ),
    "Lcm And Hcf": re.compile(r"\b(lcm|hcf|gcd|divisib|multiple|factor|remainder|number)", re.I),
    "Trigonometry": re.compile(r"\b(sin|cos|tan|cot|sec|cosec|radian|degree|θ|angle)", re.I),
    "Time and Distance": re.compile(r"\b(speed|km|distance|travel|journey|walk|run|cycl|hour)", re.I),
    "Train": re.compile(r"\b(train|platform|pole|tunnel|bridge)", re.I),
    "Profit and Loss": re.compile(r"\b(profit|loss|cost price|selling|sold|sells|buy|bought|marked)", re.I),
    # the 2D bank is already full, so only solid-geometry questions are wanted here
    "Mensuration 2D & 3D": re.compile(
        r"\b(sphere|hemisphere|cone|cylinder|cylindrical|cube|cuboid|prism|pyramid|"
        r"tetrahedron|frustum|solid|volume)", re.I
    ),
}


def usable(stem, options):
    # a drawn fraction bar or radical means the printed maths cannot survive as text
    if any(Q.SUSPECT in text for text in [stem, *options]):
        return False
    if len(stem) < 25 or NEEDS_ART.search(stem) or BROKEN_OPENING.search(stem):
        return False
    if len(set(options)) != 4 or any(len(o) > 160 for o in options):
        return False
    if any(not re.search(r"[\w₹]", o) for o in options):
        return False
    if JUNK_RUN.search(stem):
        return False
    if stem.count("(") > 12:
        return False
    for text in [stem, *options]:
        flat = text.translate(PLAIN_DIGITS)
        if COLLAPSED.search(flat) or COLLAPSED_SYMBOL.search(flat):
            return False
    return True


def trim(stem):
    """Drop the exam stamp and the numeric debris a collapsed fraction leaves behind."""
    stem = EXAM_STAMP.sub(" ", stem).strip()
    previous = None
    while previous != stem:
        previous = stem
        stem = TRAILING_JUNK.sub(lambda m: m.group(0)[0], stem).strip()
    return stem


def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())[:120]


def harvest(doc, chapter):
    """Clean, answer-keyed MCQs from one chapter, in printed order."""
    first, last, keypage, _ = CHAPTERS[chapter]
    text = Q.cut_answer_key(Q.chapter_text(doc, first, last))
    blocks = Q.split_questions(text)
    key = Q.parse_answer_key(Q.chapter_text(doc, keypage, keypage + 1))

    out, dropped = [], 0
    for number in sorted(blocks):
        parsed = Q.parse_block(blocks[number])
        letter = key.get(number)
        if not parsed or letter not in LETTERS:
            dropped += 1
            continue
        stem, options = trim(parsed[0]), parsed[1]
        topic = TOPIC_WORDS.get(chapter)
        if not usable(stem, options) or (topic and not topic.search(stem)):
            dropped += 1
            continue
        out.append((stem, options, options[LETTERS.index(letter)]))
    return out, dropped


def main(write):
    doc = fitz.open(Q.PDF)
    grand = 0
    for rel, chapters in PLAN:
        path = ROOT / rel
        bank = json.loads(path.read_text(encoding="utf-8"))
        slots = [i for i, q in enumerate(bank) if PLACEHOLDER_MARK in (q.get("question") or "")]
        existing = {normalise(q.get("question") or "") for q in bank}

        pool, dropped = [], 0
        for chapter in chapters:
            got, lost = harvest(doc, chapter)
            pool += got
            dropped += lost

        written, skipped_dupe = 0, 0
        for stem, options, answer in pool:
            if written >= len(slots):
                break
            if normalise(stem) in existing:
                skipped_dupe += 1
                continue
            existing.add(normalise(stem))
            index = slots[written]
            bank[index] = {
                "id": bank[index]["id"],
                "question": stem,
                "options": options,
                "correctAnswer": answer,
            }
            written += 1

        grand += written
        left = len(slots) - written
        name = rel.split("/")[-1]
        print(
            f"{name:26} slots {len(slots):4}  pool {len(pool):4}  written {written:4}"
            f"  slots left {left:4}  dropped {dropped:3}  dupes {skipped_dupe:2}"
        )
        if write and written:
            BACKUP.mkdir(exist_ok=True)
            (BACKUP / path.name).write_bytes(path.read_bytes())
            path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total questions {'written' if write else 'that would be written'}: {grand}")


if __name__ == "__main__":
    main("--write" in sys.argv)
