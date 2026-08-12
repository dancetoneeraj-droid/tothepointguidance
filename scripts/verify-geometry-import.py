import json
from pathlib import Path

g = json.loads((Path(__file__).resolve().parent.parent / "data/maths/geometry.json").read_text(encoding="utf-8"))

assert len(g) == 623, f"expected 623 entries, got {len(g)}"

bad = []
for i in range(151, 623):
    q = g[i]
    if not q.get("question", "").strip():
        bad.append(f"empty question {q['id']}")
    if not q.get("solution", "").strip():
        bad.append(f"no solution {q['id']}")
    if q["correctAnswer"] not in q["options"]:
        bad.append(f"answer not in options {q['id']}: {q['correctAnswer']!r}")

print("total entries:", len(g))
print("152:", g[151]["id"], "->", g[151]["correctAnswer"])
print("623:", g[622]["id"], "->", g[622]["correctAnswer"])
print("151 (last old):", g[150]["id"], "->", g[150]["correctAnswer"])
if bad:
    print(f"ISSUES ({len(bad)}):", bad[:15])
else:
    print("ALL 472 NEW QUESTIONS OK")
