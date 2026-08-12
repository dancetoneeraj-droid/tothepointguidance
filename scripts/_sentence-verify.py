"""Check the sentence-selection import: nothing existing changed, and every new
question is well formed and reachable from the schedule."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP = ROOT / "scripts" / "_sentence-backup"

old_bank = json.loads((BACKUP / "pronoun.json").read_text(encoding="utf-8"))
new_bank = json.loads((ROOT / "data" / "english" / "pronoun.json").read_text(encoding="utf-8"))
old_sched = json.loads((BACKUP / "schedule-75.json").read_text(encoding="utf-8"))
new_sched = json.loads((ROOT / "data" / "schedule-75.json").read_text(encoding="utf-8"))

fail = []

# 1. bank: existing untouched, new entries appended
if new_bank[: len(old_bank)] != old_bank:
    fail.append("existing pronoun questions were modified")
added = new_bank[len(old_bank):]
print(f"bank: {len(old_bank)} -> {len(new_bank)} ({len(added)} appended)")

for index, q in enumerate(added):
    where = f"{q.get('id', '?')} (#{index + 1})"
    if q["id"] != f"pronoun_{len(old_bank) + index + 1}":
        fail.append(f"{where}: unexpected id")
    if len(q["options"]) != 4:
        fail.append(f"{where}: {len(q['options'])} options")
    if len(set(q["options"])) != 4:
        fail.append(f"{where}: duplicate options")
    if q["correctAnswer"] not in q["options"]:
        fail.append(f"{where}: correctAnswer is not one of the options")
    if not q["question"].strip() or not all(o.strip() for o in q["options"]):
        fail.append(f"{where}: empty text")

ids = [q["id"] for q in new_bank]
if len(set(ids)) != len(ids):
    fail.append("duplicate ids in the bank")

# 2. schedule: only days 35-38 gained a grammarQuizzes entry
touched = []
for before, after in zip(old_sched["plans"], new_sched["plans"]):
    if before != after:
        touched.append(before["day"])
        stripped = dict(after["english"])
        stripped.pop("grammarQuizzes", None)
        if stripped != before["english"]:
            fail.append(f"day {before['day']}: english block changed beyond grammarQuizzes")
        if {k: v for k, v in after.items() if k != "english"} != {
            k: v for k, v in before.items() if k != "english"
        }:
            fail.append(f"day {before['day']}: changed outside the english block")
if touched != [35, 36, 37, 38]:
    fail.append(f"unexpected set of changed days: {touched}")
for key in old_sched:
    if key != "plans" and old_sched[key] != new_sched[key]:
        fail.append(f"top-level '{key}' changed")

# 3. the four quizzes cover the new questions exactly once, in order
covered = []
for day in touched:
    plan = next(p for p in new_sched["plans"] if p["day"] == day)
    for quiz in plan["english"]["grammarQuizzes"]:
        span = list(range(quiz["from"], quiz["from"] + quiz["questions"]))
        if span[-1] >= len(new_bank):
            fail.append(f"day {day}: quiz runs past the end of the bank")
        covered += span
        served = new_bank[quiz["from"]]["id"], new_bank[span[-1]]["id"]
        print(f"day {day}: {quiz['label']:>18} | {quiz['questions']} questions | "
              f"{served[0]} .. {served[1]}")

if covered != list(range(len(old_bank), len(new_bank))):
    fail.append("the scheduled quizzes do not cover the new questions exactly once")

print()
if fail:
    print("FAILED")
    for problem in fail:
        print(" -", problem)
    raise SystemExit(1)
print("All checks passed.")
