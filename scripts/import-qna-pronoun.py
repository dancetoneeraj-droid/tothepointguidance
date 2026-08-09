"""
Parse datas/English/qna.pdf (scanned) into data/english/pronoun.json.
Uses Claude vision on page images + answer key from pages 11-12.

Run: python scripts/import-qna-pronoun.py
Requires ANTHROPIC_API_KEY in .env.local
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "datas" / "English" / "qna-pages"
TARGET = ROOT / "data" / "english" / "pronoun.json"
ENV_PATH = ROOT / ".env.local"

QUESTION_PAGES = list(range(1, 11))  # pages 1-10
ANSWER_PAGES = [11, 12]


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
        max_tokens=8000,
        messages=[{"role": "user", "content": content}],
    )
    return msg.content[0].text


def parse_json(text: str):
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    raw = fenced.group(1) if fenced else text
    return json.loads(raw.strip())


def extract_questions(client) -> list[dict]:
    all_q: list[dict] = []
    # Batch 2 pages at a time
    for i in range(0, len(QUESTION_PAGES), 2):
        batch = QUESTION_PAGES[i : i + 2]
        paths = [PAGES_DIR / f"page-{p:02d}.png" for p in batch]
        prompt = (
            "Extract ALL spot-the-error MCQ questions from these textbook page images.\n"
            "Return JSON array ONLY. Each item:\n"
            "{\n"
            '  "num": <question number>,\n'
            '  "question": "<full sentence without part labels>",\n'
            '  "parts": {"a":"...", "b":"...", "c":"...", "d":"..." optional},\n'
            '  "hasPartD": true/false,\n'
            '  "noErrorLabel": "d" or "e"\n'
            "}\n"
            "Rules:\n"
            "- Include every numbered question visible.\n"
            "- parts.a/b/c are the underlined segments exactly as printed.\n"
            "- If only a,b,c plus No error (no 4th content part), hasPartD=false.\n"
            "- If a,b,c,d content parts plus No error, hasPartD=true and include parts.d.\n"
            "- question = full sentence as one line.\n"
        )
        print(f"Extracting questions from pages {batch}...", flush=True)
        text = call_vision(client, prompt, paths)
        batch_q = parse_json(text)
        all_q.extend(batch_q)
        time.sleep(0.5)
    all_q.sort(key=lambda x: x["num"])
    return all_q


def extract_answers(client) -> dict[int, dict]:
    paths = [PAGES_DIR / f"page-{p:02d}.png" for p in ANSWER_PAGES]
    prompt = (
        "Extract the COMPLETE answer key from these two answer pages.\n"
        "Return JSON object mapping question number (string keys) to:\n"
        '{"letter":"a|b|c|d|e","fix":"explanation text","noError":true/false}\n'
        "Rules:\n"
        "- letter is the correct option letter shown in parentheses.\n"
        "- If answer says 'No error', set noError=true and letter to the No error option (d or e).\n"
        "- fix = the correction explanation after the letter (empty if just No error).\n"
        "- Include ALL numbered answers from Review Exercise (1-74) and Done General English (75-114).\n"
        "- Use numeric string keys: \"1\", \"2\", ... \"114\".\n"
    )
    print("Extracting answer key from pages 11-12...", flush=True)
    text = call_vision(client, prompt, paths)
    raw = parse_json(text)
    out: dict[int, dict] = {}
    for k, v in raw.items():
        out[int(k)] = v
    return out


def to_entry(num: int, q: dict, ans: dict, next_id: int) -> dict:
    parts = q.get("parts", {})
    has_d = q.get("hasPartD", bool(parts.get("d")))
    no_err = ans.get("noError") or ans.get("letter", "").lower() in ("d", "e") and (
        "no error" in ans.get("fix", "").lower() or ans.get("fix", "").strip() == ""
    )

    if has_d and parts.get("d") and parts["d"].strip().lower() not in ("no error",):
        options = [parts.get("a", ""), parts.get("b", ""), parts.get("c", ""), parts.get("d", "")]
        letter_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 3}
    else:
        options = [parts.get("a", ""), parts.get("b", ""), parts.get("c", ""), "No error"]
        letter_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 3}

    letter = ans.get("letter", "a").lower()
    idx = letter_map.get(letter, 0)

    # No error answers: if fix explicitly says No error or letter is no-error slot
    fix_text = (ans.get("fix") or "").strip()
    if no_err or fix_text.lower().startswith("no error") or fix_text.lower() == "no ertor":
        correct = "No error" if "No error" in options else options[-1]
    else:
        correct = options[idx] if idx < len(options) else options[0]

    explanation = fix_text if fix_text and not fix_text.lower().startswith("no error") else (
        "No grammatical error in the sentence." if correct == "No error" else fix_text or f"Correct the error in the marked part ({letter})."
    )

    # Clean options
    options = [re.sub(r"\s+", " ", o).strip() for o in options]

    entry = {
        "id": f"pronoun_{next_id:03d}",
        "question": re.sub(r"\s+", " ", q.get("question", "")).strip(),
        "options": options,
        "correctAnswer": correct.strip(),
        "explanation": explanation.strip(),
    }
    return entry


def main() -> None:
    import anthropic

    client = anthropic.Anthropic(api_key=load_api_key())

    questions = extract_questions(client)
    answers = extract_answers(client)

    existing = json.loads(TARGET.read_text(encoding="utf-8"))
    if not isinstance(existing, list):
        existing = existing if isinstance(existing, list) else [existing]

    start_id = len(existing) + 1
    added: list[dict] = []
    missing_ans: list[int] = []

    for q in questions:
        num = q["num"]
        ans = answers.get(num)
        if not ans:
            missing_ans.append(num)
            ans = {"letter": "e", "fix": "No error", "noError": True}
        added.append(to_entry(num, q, ans, start_id + len(added)))

    merged = existing + added
    TARGET.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    print(f"\nAdded {len(added)} questions -> {TARGET}")
    print(f"IDs: pronoun_{start_id:03d} .. pronoun_{start_id + len(added) - 1:03d}")
    if missing_ans:
        print(f"Warning: missing answers for Q{missing_ans}")


if __name__ == "__main__":
    main()
