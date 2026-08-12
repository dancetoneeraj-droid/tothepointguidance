"""Prove the question-bank import only filled placeholders.

Compares every touched bank against the copy taken just before the write and
fails loudly on any change to a question that was already real.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP = Path(__file__).resolve().parent / "_qbank-backup"
PLACEHOLDER_MARK = "add real content"
SUSPECT = "\u2591"

failures = 0


def fail(message):
    global failures
    failures += 1
    print("FAIL:", message)


for backup in sorted(BACKUP.glob("*.json")):
    live = next(ROOT.joinpath("data").rglob(backup.name))
    before = json.loads(backup.read_text(encoding="utf-8"))
    after = json.loads(live.read_text(encoding="utf-8"))

    if len(before) != len(after):
        fail(f"{backup.name}: length changed {len(before)} -> {len(after)}")
        continue

    filled = 0
    for index, (old, new) in enumerate(zip(before, after)):
        if old["id"] != new["id"]:
            fail(f"{backup.name}[{index}]: id changed {old['id']} -> {new['id']}")
            continue
        if old == new:
            continue
        if PLACEHOLDER_MARK not in (old.get("question") or ""):
            fail(f"{backup.name}: {old['id']} was a real question and got modified")
            continue

        filled += 1
        options = new.get("options") or []
        if len(options) != 4 or len(set(options)) != 4:
            fail(f"{backup.name}: {new['id']} does not have 4 distinct options")
        if new.get("correctAnswer") not in options:
            fail(f"{backup.name}: {new['id']} answer is not one of its options")
        if PLACEHOLDER_MARK in new["question"] or "Option A" in options:
            fail(f"{backup.name}: {new['id']} still holds placeholder text")
        for text in [new["question"], *options]:
            if SUSPECT in text:
                fail(f"{backup.name}: {new['id']} kept a collapsed-maths marker")
        if set(new) - {"id", "question", "options", "correctAnswer"}:
            fail(f"{backup.name}: {new['id']} has unexpected keys {sorted(new)}")

    remaining = sum(1 for q in after if PLACEHOLDER_MARK in (q.get("question") or ""))
    print(f"{backup.name:26} filled {filled:4}  placeholders left {remaining:4}")

print("FAILURES:", failures)
