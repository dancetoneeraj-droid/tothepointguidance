"""Reader for datas/QUESTION BANK.pdf (SSC Exams 2025, 24 chapters, 3151 questions).

The PDF keeps English body text, the legacy-font Hindi translation, the exam
stamp and the page furniture in different fonts, so the clean English can be
recovered by filtering spans on the font name instead of guessing from the
flattened text.

Content page numbers printed on the sheet are 9 less than the PDF page index.
"""

import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "datas" / "QUESTION BANK.pdf"

PAGE_OFFSET = 9  # printed page N lives at PDF page N + 9

# chapter -> (first question page, last question page, answer-key page, printed count)
CHAPTERS = {
    "Percentage": (1, 12, 12, 144),
    "Profit and Loss": (23, 32, 32, 114),
    "Discount": (41, 52, 52, 138),
    "Simple Interest": (63, 72, 72, 110),
    "Compound Interest": (81, 87, 87, 86),
    "Ratio & Proportion": (96, 103, 104, 100),
    "Partnership": (112, 121, 121, 110),
    "Mixture and Alligation": (130, 141, 141, 116),
    "Average": (152, 164, 165, 153),
    "Time and Work": (176, 187, 187, 126),
    "Pipe and Cistern": (198, 199, 199, 13),
    "Time and Distance": (201, 210, 210, 104),
    "Train": (219, 220, 220, 15),
    "Number System": (223, 230, 230, 93),
    "Lcm And Hcf": (235, 236, 237, 27),
    "Simplification": (239, 251, 251, 207),
    "Algebra": (261, 267, 267, 99),
    "Trigonometry": (274, 290, 291, 218),
    "Height and distance": (309, 313, 313, 46),
    "Geometry": (319, 350, 351, 416),
    "Co-ordinate geometry": (384, 391, 391, 106),
    "Mensuration 2D & 3D": (400, 444, 445, 592),
    "Probability": (486, 487, 487, 9),
    "Data Interpratation": (489, 490, 490, 9),
}

BODY_FONTS = ("Bookman Old Style",)
DROP_FONTS = (
    "Walkman-Chanakya",  # legacy-font Hindi translation
    "Plump MT",
    "Poppins",
    "Impact",
)
STAMP_FONT = "Bookman Old Style Bold I"  # "SSC CGL 12/09/2025 (Shift-03)"
RUPEE_FONT = "Rupee Foradian"

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# Symbol-encoded glyphs arrive as private-use codepoints (0xF000 + ASCII)
SYMBOL_MAP = {
    "\uf071": "θ", "\uf070": "π", "\uf061": "α", "\uf062": "β", "\uf067": "γ",
    "\uf064": "δ", "\uf044": "Δ", "\uf02b": "+", "\uf02d": "−", "\uf03d": "=",
    "\uf0b4": "×", "\uf0b8": "÷", "\uf0d6": "√", "\uf0a3": "≤", "\uf0b3": "≥",
    "\uf0b9": "≠", "\uf028": "(", "\uf029": ")", "\uf03c": "<", "\uf03e": ">",
}
# glyphs used to draw multi-line brackets: their presence means stacked layout
BRACKET_BUILDERS = set("\uf0e6\uf0e7\uf0e8\uf0f6\uf0f7\uf0f8\uf0e9\uf0eb\uf0f9\uf0fb")

SUSPECT = "\u2591"  # marker for a line that sits on a drawn fraction bar or radical


def _bars(page):
    """Short horizontal rules on the page: fraction bars and radical overbars."""
    out = []
    for drawing in page.get_drawings():
        rect = drawing["rect"]
        if rect.height <= 2.5 and 6 <= rect.width <= 110:
            out.append(rect)
    return out


def page_text(page, keep_stamp=False):
    """English-only text of one page, with the Hindi and page furniture removed."""
    out = []
    bars = _bars(page)
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            fonts = [s["font"] for s in line["spans"]]
            # Hindi lines carry their numerals in the English font, so a line that
            # is Hindi anywhere has to go as a whole or those digits leak into the stem
            if any(f.startswith(d) for f in fonts for d in DROP_FONTS):
                continue
            parts = []
            for span in line["spans"]:
                font, text = span["font"], span["text"]
                if font.startswith(RUPEE_FONT):
                    parts.append(text.replace("`", "₹"))
                    continue
                if font == STAMP_FONT and not keep_stamp:
                    continue
                if font.startswith("Symbol") or font.startswith("symbol"):
                    if any(ch in BRACKET_BUILDERS for ch in text):
                        parts.append(SUSPECT)
                    else:
                        parts.append("".join(SYMBOL_MAP.get(ch, "") for ch in text))
                    continue
                if any(font.startswith(b) for b in BODY_FONTS):
                    # a superscript is only meaningful right after a unit letter (cm2 -> cm²);
                    # the flag is also set on stray fragments of stacked fractions
                    tail = parts[-1][-1:] if parts and parts[-1] else ""
                    if span["flags"] & 1 and tail.isalpha() and len(text.strip()) <= 2:
                        text = text.translate(SUPERSCRIPT)
                    parts.append(text)
            joined = "".join(parts).strip()
            if joined:
                box = line["bbox"]
                if any(
                    box[1] - 13 <= (b.y0 + b.y1) / 2 <= box[3] + 3
                    and b.x1 > box[0] - 4
                    and b.x0 < box[2] + 4
                    for b in bars
                ):
                    joined += SUSPECT
                out.append(joined)
    return "\n".join(out)


def chapter_text(doc, first_printed, last_printed, **kw):
    return "\n".join(
        page_text(doc[n + PAGE_OFFSET - 1], **kw)
        for n in range(first_printed, last_printed + 1)
    )


QNUM = re.compile(r"^\s*(\d{1,3})\.\s*$|^\s*(\d{1,3})\.\s+(?=\S)")
OPTION = re.compile(r"\(([a-d])\)")

# the answer key often starts on the same page as the last question
KEY_RUN = re.compile(r"(?:\d{1,3}\.\s*\([a-d]\)\s*){4,}")


def cut_answer_key(text):
    """Drop the answer-key run that trails the final question of a chapter."""
    flat = re.sub(r"\s*\n\s*", " ", text)
    m = KEY_RUN.search(flat)
    if not m:
        return text
    # map the cut point back onto the original text by matching the first key entry
    head = flat[: m.start()]
    words = head.split()
    if not words:
        return text
    anchor = " ".join(words[-6:])
    idx = re.sub(r"\s*\n\s*", " ", text).find(anchor)
    if idx < 0:
        return text
    # rebuild by walking the original lines until the anchor is consumed
    kept, seen = [], ""
    for line in text.split("\n"):
        if len(seen) >= idx + len(anchor):
            break
        kept.append(line)
        seen += line + " "
    return "\n".join(kept)


def split_questions(text):
    """Split a chapter's question pages into {number: raw block}."""
    blocks, current, buf = {}, None, []
    for line in text.split("\n"):
        m = QNUM.match(line)
        num = m and int(m.group(1) or m.group(2))
        # a genuine question number only ever moves forward by one
        if num is not None and (current is None or num == current + 1):
            if current is not None:
                blocks[current] = "\n".join(buf).strip()
            current, buf = num, []
            rest = line[m.end():].strip()
            if rest:
                buf.append(rest)
        elif current is not None:
            buf.append(line)
    if current is not None:
        blocks[current] = "\n".join(buf).strip()
    return blocks


def parse_block(raw):
    """Split one question block into (stem, [4 options]) or None if it is not a clean MCQ."""
    flat = re.sub(r"\s*\n\s*", " ", raw).strip()
    positions = [(m.group(1), m.start()) for m in OPTION.finditer(flat)]
    wanted = ["a", "b", "c", "d"]
    starts = {}
    for letter, pos in positions:
        if letter in wanted and letter not in starts:
            expected = wanted[len(starts)] if len(starts) < 4 else None
            if letter == expected:
                starts[letter] = pos
    if len(starts) != 4:
        return None

    cuts = [starts[l] for l in wanted]
    stem = flat[: cuts[0]].strip()
    options = []
    for i, letter in enumerate(wanted):
        end = cuts[i + 1] if i + 1 < 4 else len(flat)
        body = flat[cuts[i] : end]
        body = body[body.index(")") + 1 :].strip()
        options.append(clean(body))
    stem = clean(stem)
    if not stem or any(not o for o in options):
        return None
    return stem, options


ANSWER_KEY = re.compile(r"(\d{1,3})\.\s*\(([a-d])\)")


def parse_answer_key(text):
    """{question number: 'a'} from an answer-key page."""
    key = {}
    for m in ANSWER_KEY.finditer(re.sub(r"\s+", " ", text)):
        key[int(m.group(1))] = m.group(2)
    return key


SPACE = re.compile(r"[ \t]+")


def clean(s):
    s = s.replace("\u00a0", " ").replace("`", "₹")
    s = SPACE.sub(" ", s)
    s = re.sub(r"\s+([,.;:%\)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    return s.strip()
