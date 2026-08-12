"""Flag explanations whose quoted phrases do not appear anywhere in their own
question, so a note attached to the wrong question shows up instead of hiding."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bank = json.loads((ROOT / "data" / "english" / "pronoun.json").read_text(encoding="utf-8"))

QUOTED = re.compile(r"'([^']+)'")


def normalise(text):
    return re.sub(r"[^a-z ]", " ", text.lower())


suspect = []
for q in bank[887:]:
    haystack = normalise(" | ".join(q["options"]))
    orphans = []
    for phrase in QUOTED.findall(q["explanation"]):
        words = [w for w in normalise(phrase).split() if len(w) > 2 and w != "one"]
        if not words:
            continue
        # a phrase counts as grounded if most of its words show up in the options
        hits = sum(1 for w in words if w in haystack.split())
        if hits < max(1, len(words) - 1):
            orphans.append(phrase)
    if orphans:
        suspect.append((q, orphans))

print(f"{len(suspect)} of {len(bank) - 887} notes need a look\n")
for q, orphans in suspect:
    print(f"{q['id']}  unmatched: {orphans}")
    print(f"   answer: {q['correctAnswer']}")
    print(f"   note  : {q['explanation']}")
    print()
