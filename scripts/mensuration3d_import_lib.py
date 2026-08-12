"""Shared helper for importing the Gagan Pratap Mensuration sheets 4-6 into
data/maths/mensuration-3d.json.

Each sheet script supplies its own question list plus the index at which its
block starts. Only placeholder slots are written, so the questions already in
the bank cannot be overwritten by accident.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "mensuration-3d.json"

PLACEHOLDER_MARK = "add real content"


def import_sheet(start_index: int, questions: list, sheet_label: str) -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    end = start_index + len(questions)

    if end > len(bank):
        raise SystemExit(
            f"{sheet_label}: needs slots up to index {end - 1} but the bank has {len(bank)}"
        )

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
        if len(options) != 4:
            raise SystemExit(f"{sheet_label} Q{offset + 1}: expected 4 options")
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
        f"({bank[start_index]['id']} .. {bank[end - 1]['id']})"
    )
