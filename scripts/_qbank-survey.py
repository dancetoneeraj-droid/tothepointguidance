"""Survey pass over QUESTION BANK.pdf: how cleanly does each candidate chapter parse?

Nothing is written to the question banks here; this only reports counts so the
import can be planned.
"""

import fitz

import qbank_lib as Q
from qbank_lib import CHAPTERS


def load(doc, name):
    first, last, keypage, expected = CHAPTERS[name]
    text = Q.cut_answer_key(Q.chapter_text(doc, first, last))
    blocks = Q.split_questions(text)
    key = Q.parse_answer_key(Q.chapter_text(doc, keypage, keypage + 1))
    return blocks, key, expected


if __name__ == "__main__":
    doc = fitz.open(Q.PDF)
    print(f"{'chapter':24} {'want':>5} {'found':>6} {'mcq':>5} {'key':>5} {'ready':>6}")
    for name in CHAPTERS:
        blocks, key, expected = load(doc, name)
        parsed = {n: Q.parse_block(r) for n, r in blocks.items()}
        good = {n for n, p in parsed.items() if p}
        ready = sum(
            1
            for n in good
            if n in key and key[n] in "abcd" and len(parsed[n][1]) == 4
        )
        print(f"{name:24} {expected:5} {len(blocks):6} {len(good):5} {len(key):5} {ready:6}")
