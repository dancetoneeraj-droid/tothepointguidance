"""
Parse datas/Spotting error.pdf (scanned) into data/english/pronoun.json.
Questions on pages 1-23; answer key on pages 24-26.
Appends from pronoun_763 onward without modifying existing entries.

Run: python scripts/import-spotting-error-pronoun.py
Requires ANTHROPIC_API_KEY in .env.local
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "datas" / "English" / "spotting-error-pages"
TARGET = ROOT / "data" / "english" / "pronoun.json"
ENV_PATH = ROOT / ".env.local"
OUT_JSON = ROOT / "datas" / "English" / "spotting-error-parsed.json"

QUESTION_PAGES = list(range(1, 24))  # pages 1-23
ANSWER_PAGES = [24, 25, 26]
START_ID = 763


def load_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key.strip()
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            m = re.match(r"ANTHROPIC_API_KEY\s*=\s*(.+)", line)
            if m:
                return m.group(1).strip().strip("'\"")
    raise SystemExit("ANTHROPIC_API_KEY not found in .env.local")


def image_block(path: Path) -> dict:
    import base64

    media = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media, "data": data},
    }


def call_vision(client, prompt: str, image_paths: list[Path]) -> str:
    content = [image_block(p) for p in image_paths]
    content.append({"type": "text", "text": prompt})
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=16000,
        messages=[{"role": "user", "content": content}],
    )
    return msg.content[0].text


def parse_json(text: str):
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    raw = fenced.group(1) if fenced else text
    return json.loads(raw.strip())


def extract_questions(client) -> list[dict]:
    all_q: list[dict] = []
    for i in range(0, len(QUESTION_PAGES), 2):
        batch = QUESTION_PAGES[i : i + 2]
        paths = [PAGES_DIR / f"page-{p:02d}.png" for p in batch]
        prompt = (
            "Extract ALL spot-the-error MCQ questions from these textbook page images.\n"
            "This is Chapter 16 Spotting Errors with Exercises A, B, C, D, E (25 Q each).\n"
            "Return JSON array ONLY. Each item:\n"
            "{\n"
            '  "exercise": "A|B|C|D|E",\n'
            '  "num": <question number within that exercise 1-25>,\n'
            '  "globalNum": <sequential number across all exercises: A1=1, B1=26, etc>,\n'
            '  "question": "<full sentence without part labels>",\n'
            '  "parts": {"a":"...", "b":"...", "c":"..."},\n'
            '  "noErrorLabel": "d"\n'
            "}\n"
            "Rules:\n"
            "- Every question has exactly parts a, b, c as underlined segments, plus d = No error.\n"
            "- question = full sentence as one line (concatenate a+b+c naturally).\n"
            "- Include every numbered question visible on these pages.\n"
            "- Preserve exact wording from the book.\n"
            "- globalNum: Exercise A Q1=1, A Q25=25, B Q1=26, ... E Q25=125.\n"
        )
        print(f"Extracting questions from pages {batch}...", flush=True)
        text = call_vision(client, prompt, paths)
        batch_q = parse_json(text)
        all_q.extend(batch_q)
        time.sleep(0.5)

    # Deduplicate by globalNum
    by_num: dict[int, dict] = {}
    for q in all_q:
        g = int(q.get("globalNum") or q.get("num", 0))
        if "exercise" in q and "num" in q:
            ex_map = {"A": 0, "B": 25, "C": 50, "D": 75, "E": 100}
            g = ex_map.get(q["exercise"], 0) + int(q["num"])
        by_num[g] = q
    result = [by_num[k] for k in sorted(by_num)]
    print(f"Extracted {len(result)} unique questions", flush=True)
    return result


def extract_answers(client) -> dict[int, dict]:
    paths = [PAGES_DIR / f"page-{p:02d}.png" for p in ANSWER_PAGES]
    prompt = (
        "Extract the COMPLETE answer key from these three answer pages.\n"
        "Covers Exercises A, B, C, D, E (25 questions each = 125 total).\n"
        "Return JSON object mapping global question number (string keys \"1\" to \"125\") to:\n"
        '{"letter":"a|b|c|d","fix":"explanation text","noError":true/false}\n'
        "Rules:\n"
        "- letter is the correct option letter shown in parentheses, usually (a), (b), (c), or (d).\n"
        "- If answer says 'No error', set noError=true and letter='d'.\n"
        "- fix = the correction explanation after the letter (e.g. \"Say 'speaking to' for 'to speak'\").\n"
        "- For No error, fix can be empty or \"No error\".\n"
        "- globalNum: A1=1, A25=25, B1=26, B25=50, C1=51, ... E25=125.\n"
        "- Include ALL 125 answers.\n"
    )
    print("Extracting answer key from pages 24-26...", flush=True)
    text = call_vision(client, prompt, paths)
    raw = parse_json(text)
    out: dict[int, dict] = {}
    for k, v in raw.items():
        out[int(k)] = v
    print(f"Extracted {len(out)} answers", flush=True)
    return out


def to_entry(global_num: int, q: dict, ans: dict) -> dict:
    parts = q.get("parts", {})
    options = [
        re.sub(r"\s+", " ", parts.get("a", "")).strip(),
        re.sub(r"\s+", " ", parts.get("b", "")).strip(),
        re.sub(r"\s+", " ", parts.get("c", "")).strip(),
        "No error",
    ]

    letter = (ans.get("letter") or "d").lower()
    fix_text = (ans.get("fix") or "").strip()
    no_err = ans.get("noError") or letter == "d" and (
        not fix_text or fix_text.lower().startswith("no error")
    )

    letter_map = {"a": 0, "b": 1, "c": 2, "d": 3}
    idx = letter_map.get(letter, 3)

    if no_err or fix_text.lower().startswith("no error"):
        correct = "No error"
    else:
        correct = options[idx] if idx < 3 else "No error"

    if correct == "No error":
        explanation = "No grammatical error in the sentence."
    elif fix_text:
        explanation = fix_text[0].upper() + fix_text[1:] if len(fix_text) > 1 else fix_text
        if not explanation.endswith("."):
            explanation += "."
    else:
        explanation = f"Correct the error in part ({letter})."

    return {
        "id": f"pronoun_{START_ID + global_num - 1:03d}",
        "question": re.sub(r"\s+", " ", q.get("question", "")).strip(),
        "options": options,
        "correctAnswer": correct,
        "explanation": explanation,
    }


def main() -> None:
    import anthropic

    if not PAGES_DIR.exists():
        raise SystemExit(f"Page images not found at {PAGES_DIR}. Run page render first.")

    client = anthropic.Anthropic(api_key=load_api_key())

    if OUT_JSON.exists():
        cached = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        questions = cached.get("questions", [])
        answers = {int(k): v for k, v in cached.get("answers", {}).items()}
        print(f"Loaded cache: {len(questions)} questions, {len(answers)} answers")
    else:
        questions = extract_questions(client)
        answers = extract_answers(client)
        OUT_JSON.write_text(
            json.dumps({"questions": questions, "answers": answers}, indent=2),
            encoding="utf-8",
        )
        print(f"Cached parsed data -> {OUT_JSON}")

    existing = json.loads(TARGET.read_text(encoding="utf-8"))
    assert len(existing) == START_ID - 1, (
        f"Expected {START_ID - 1} existing entries, got {len(existing)}"
    )

    added: list[dict] = []
    missing_q: list[int] = []
    missing_ans: list[int] = []
    errors: list[str] = []

    by_global: dict[int, dict] = {}
    for q in questions:
        g = int(q.get("globalNum", 0))
        if not g and "exercise" in q:
            ex_map = {"A": 0, "B": 25, "C": 50, "D": 75, "E": 100}
            g = ex_map.get(q["exercise"], 0) + int(q["num"])
        by_global[g] = q

    for g in range(1, 126):
        q = by_global.get(g)
        ans = answers.get(g)
        if not q:
            missing_q.append(g)
            continue
        if not ans:
            missing_ans.append(g)
            ans = {"letter": "d", "fix": "No error", "noError": True}
        entry = to_entry(g, q, ans)
        if entry["correctAnswer"] not in entry["options"]:
            errors.append(f"{entry['id']}: correctAnswer not in options: {entry['correctAnswer']!r}")
        added.append(entry)

    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))

    merged = existing + added
    TARGET.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    print(f"\nAdded {len(added)} questions -> {TARGET}")
    print(f"IDs: pronoun_{START_ID:03d} .. pronoun_{START_ID + len(added) - 1:03d}")
    if missing_q:
        print(f"Warning: missing questions for global #{missing_q}")
    if missing_ans:
        print(f"Warning: missing answers for global #{missing_ans}")


if __name__ == "__main__":
    main()
