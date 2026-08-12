"""Show what the importer keeps and what it throws away, chapter by chapter."""

import importlib.util
import random
import sys
from pathlib import Path

import fitz

import qbank_lib as Q
from qbank_lib import CHAPTERS

# the importer's filename has hyphens, so load it by path to reuse its filters
spec = importlib.util.spec_from_file_location(
    "qbimport", Path(__file__).resolve().parent / "import-question-bank.py"
)
qbimport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qbimport)

LETTERS = "abcd"


def report(chapter, samples=3):
    doc = fitz.open(Q.PDF)
    first, last, keypage, _ = CHAPTERS[chapter]
    text = Q.cut_answer_key(Q.chapter_text(doc, first, last))
    blocks = Q.split_questions(text)
    key = Q.parse_answer_key(Q.chapter_text(doc, keypage, keypage + 1))

    kept, dropped = [], []
    for number in sorted(blocks):
        parsed = Q.parse_block(blocks[number])
        letter = key.get(number)
        if not parsed or letter not in LETTERS:
            dropped.append((number, "unparsed / no key", (parsed or ("", []))[0][:90]))
            continue
        stem, options = parsed
        if not qbimport.usable(stem, options):
            reason = (
                "needs artwork"
                if qbimport.NEEDS_ART.search(stem)
                else "duplicate options"
                if len(set(options)) != 4
                else "junk tail"
                if qbimport.JUNK_RUN.search(stem)
                else "other"
            )
            dropped.append((number, reason, stem[:90]))
            continue
        kept.append((number, stem, options, options[LETTERS.index(letter)]))

    print(f"===== {chapter}: kept {len(kept)}, dropped {len(dropped)} =====")
    for number, reason, stem in dropped:
        print(f"  DROP {number:4} [{reason}] {stem}")
    print("  ---- samples ----")
    for number, stem, options, answer in random.sample(kept, min(samples, len(kept))):
        print(f"  Q{number}: {stem}")
        print(f"     options: {options}")
        print(f"     answer : {answer}")


if __name__ == "__main__":
    random.seed(7)
    for chapter in sys.argv[1:]:
        report(chapter)
