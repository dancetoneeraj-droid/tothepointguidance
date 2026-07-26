"""Assemble vocab-part1.tsv and vocab-part2.tsv from transcript extractions."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPT_DIR = Path(
    r"C:\Users\user\.cursor\projects\c-Users-user-OneDrive-Desktop-tothepointguidance\agent-transcripts"
)
OUT1 = ROOT / "datas" / "English" / "vocab-part1.tsv"
OUT2 = ROOT / "datas" / "English" / "vocab-part2.tsv"
PART1_EXTRA = ROOT / "scripts" / "pages2-13_extract.txt"

ENTRY_RE = re.compile(r"(\d+)\|([^|\n]+)\|([^|\n]*)\|([^\n]*)")


def load_from_transcripts() -> dict[int, str]:
    entries: dict[int, str] = {}
    for jsonl in TRANSCRIPT_DIR.rglob("*.jsonl"):
        for raw in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if obj.get("role") != "assistant":
                continue
            for block in obj.get("message", {}).get("content", []):
                if block.get("type") != "text":
                    continue
                for m in ENTRY_RE.finditer(block["text"]):
                    num = int(m.group(1))
                    if 31 <= num <= 1650:
                        entries[num] = (
                            f"{num}|{m.group(2).strip()}|{m.group(3).strip()}|{m.group(4).strip()}"
                        )
    return entries


def load_file(path: Path) -> dict[int, str]:
    entries: dict[int, str] = {}
    if not path.exists():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = ENTRY_RE.match(line)
        if m:
            num = int(m.group(1))
            entries[num] = line
    return entries


def main() -> None:
    entries = load_from_transcripts()
    entries.update(load_file(PART1_EXTRA))

    # Word 1072 missing from page-47 boundary (Fortuitous=1071, Felony=1073 on page 48)
    if 1072 not in entries:
        entries[1072] = "1072|Frisk|search a person, gambol|"

    part1_nums = list(range(31, 262))
    part2_nums = list(range(262, 1651))

    missing1 = [n for n in part1_nums if n not in entries]
    missing2 = [n for n in part2_nums if n not in entries]

    part1 = [entries[n] for n in part1_nums if n in entries]
    part2 = [entries[n] for n in part2_nums if n in entries]

    OUT1.write_text("\n".join(part1) + "\n", encoding="utf-8")
    OUT2.write_text("\n".join(part2) + "\n", encoding="utf-8")

    print(f"Wrote {OUT1}: {len(part1)} lines (expected 231)")
    if part1:
        print(f"  first: #{part1[0].split('|')[0]} {part1[0].split('|')[1]}")
        print(f"  last:  #{part1[-1].split('|')[0]} {part1[-1].split('|')[1]}")
    if missing1:
        print(f"  MISSING part1 ({len(missing1)}): {missing1[:5]}...{missing1[-3:]}")

    print(f"Wrote {OUT2}: {len(part2)} lines (expected 1389)")
    if part2:
        print(f"  first: #{part2[0].split('|')[0]} {part2[0].split('|')[1]}")
        print(f"  last:  #{part2[-1].split('|')[0]} {part2[-1].split('|')[1]}")
    if missing2:
        print(f"  MISSING part2 ({len(missing2)}): {missing2}")


if __name__ == "__main__":
    main()
