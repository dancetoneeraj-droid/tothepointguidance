import json
from pathlib import Path

p = Path(r"c:\Users\user\OneDrive\Desktop\tothepointguidance\data\maths\mensuration-3d.json")
bank = json.loads(p.read_text(encoding="utf-8"))
print("total", len(bank))
for i, q in enumerate(bank[125:150], start=1):
    print("=" * 80)
    print(f"Q{i}  idx={124 + i}  id={q['id']}")
    print("QUESTION:", q["question"][:800].replace("\n", " | "))
    print("OPTIONS:", q["options"])
    print("ANSWER:", q["correctAnswer"])
    print("EXPL:", (q.get("explanation") or "")[:400])
    sol = (q.get("solution") or "")[:200]
    if sol:
        print("SOL:", sol.replace("\n", " | "))
