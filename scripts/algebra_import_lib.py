"""Shared helper for importing the Gagan Pratap Algebra sheets into
data/maths/algebra.json.

Each sheet script supplies its own question list plus the index at which its
block starts. The bank is grown with fresh placeholders when a sheet runs past
the current end, and only the slots belonging to that sheet are written.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "algebra.json"

PLACEHOLDER_MARK = "add real content"


def _placeholder(number: int) -> dict:
    return {
        "id": f"maths_algebra_{number}",
        "question": f"Algebra — Question {number} (add real content in datas/maths/algebra.json)",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correctAnswer": "Option A",
        "explanation": "Placeholder for Algebra.",
    }


def import_sheet(start_index: int, questions: list, sheet_label: str) -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    end = start_index + len(questions)

    grown = 0
    while len(bank) < end:
        bank.append(_placeholder(len(bank) + 1))
        grown += 1

    for offset, entry in enumerate(bank[start_index:end]):
        if PLACEHOLDER_MARK not in (entry.get("question") or ""):
            raise SystemExit(
                f"index {start_index + offset} ({entry['id']}) is not a placeholder"
            )

    for offset, (question, options, answer, solution) in enumerate(questions):
        if answer not in options:
            raise SystemExit(f"{sheet_label} Q{offset + 1}: answer {answer!r} not among options")
        if len(set(options)) != len(options):
            raise SystemExit(f"{sheet_label} Q{offset + 1}: duplicate options")
        if not solution.rstrip().endswith(answer):
            raise SystemExit(f"{sheet_label} Q{offset + 1}: solution does not end with the answer")

        index = start_index + offset
        bank[index] = {
            "id": bank[index]["id"],
            "question": question,
            "options": options,
            "correctAnswer": answer,
            "solution": solution,
        }

    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"{sheet_label}: wrote {len(questions)} questions "
        f"({bank[start_index]['id']} .. {bank[end - 1]['id']}); appended {grown} new slots"
    )
