"""Apply parsed race-sheet answers + markdown solutions locally (no API)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "time-speed-distance.json"
START = 190  # maths_time_speed_distance_191

# (correctAnswer, solution markdown)
SOLUTIONS: list[tuple[str, str]] = [
    (
        "66.67 m",
        "**Given:** Geeta is 5/2 times as fast as Babita; Geeta gives Babita a 40 m lead.\n\n"
        "**Step 1:** Let Babita's speed = v. Geeta's speed = 2.5v.\n\n"
        "**Step 2:** Relative speed = 2.5v − v = 1.5v.\n\n"
        "**Step 3:** Time to catch = 40/(1.5v). Distance from start where they meet (Geeta's distance)\n"
        "= 2.5v × 40/(1.5v) = 100/1.5 = 66.67 m.\n\n**Answer: 66.67 m**",
    ),
    (
        "256 m",
        "**Given:** Ashok is 2⅔ (= 8/3) times as fast as Bharat; Bharat gets 160 m head start.\n\n"
        "**Step 1:** Speed ratio Ashok : Bharat = 8 : 3.\n\n"
        "**Step 2:** Let winning post be x m from Ashok's start. Bharat runs (x − 160) m.\n\n"
        "**Step 3:** Equal time: (x − 160)/3 = x/8 → 8x − 1280 = 3x → 5x = 1280 → x = 256 m.\n\n**Answer: 256 m**",
    ),
    (
        "168m",
        "**Given:** A is 40% faster than B and gives B 48 m lead for a dead heat.\n\n"
        "**Step 1:** Speed ratio A : B = 1.4 : 1 = 7 : 5.\n\n"
        "**Step 2:** (L − 48)/5 = L/7 → 7L − 336 = 5L → 2L = 336 → L = 168 m.\n\n**Answer: 168m**",
    ),
    (
        "27 m",
        "**Given:** A is 30% faster than B; race length = 117 m; dead heat needed.\n\n"
        "**Step 1:** Speed ratio A : B = 13 : 10.\n\n"
        "**Step 2:** A runs 117 m, B runs (117 − h) m in same time.\n\n"
        "**Step 3:** (117 − h)/10 = 117/13 → 117 − h = 90 → h = 27 m.\n\n**Answer: 27 m**",
    ),
    (
        "720 metres",
        "**Given:** A takes 220 s, B takes 240 s; A beats B by 60 m.\n\n"
        "**Step 1:** In 220 s, B covers (220/240)L = 11L/12.\n\n"
        "**Step 2:** A beats B by L − 11L/12 = L/12 = 60 → L = 720 m.\n\n**Answer: 720 metres**",
    ),
    (
        "325 m",
        "**Given:** 1170 m race; Raman in 65 s, Mohan in 90 s.\n\n"
        "**Step 1:** Mohan's distance when Raman finishes = 1170 × (65/90) = 845 m.\n\n"
        "**Step 2:** Beating distance = 1170 − 845 = 325 m.\n\n**Answer: 325 m**",
    ),
    (
        "220 m",
        "**Given:** 1200 m race; speeds Meenal : Nitu = 5 : 7; Meenal has 500 m start.\n\n"
        "**Step 1:** Meenal runs 700 m to finish; Nitu runs 1200 m.\n\n"
        "**Step 2:** When Meenal finishes (t = 700/5 = 140), Nitu covers 140 × 7 = 980 m.\n\n"
        "**Step 3:** Meenal wins by 1200 − 980 = 220 m.\n\n**Answer: 220 m**",
    ),
    (
        "S, 2.63",
        "**Given:** In 120 m, P beats S by 6 m → vP/vS = 120/114 = 20/19.\n"
        "100 m race; S has 7.5 m head start (S runs 92.5 m).\n\n"
        "**Step 1:** Let vS = 19k, vP = 20k.\n\n"
        "**Step 2:** S time = 92.5/19k = 4.868k; P time = 100/20k = 5k.\n\n"
        "**Step 3:** S finishes first. When S finishes, P at 20×92.5/19 = 97.37 m → S wins by 2.63 m.\n\n**Answer: S, 2.63**",
    ),
    (
        "76",
        "**Given:** 500 m: A beats B by 50 m → vA/vB = 10/9. 600 m: B beats C by 60 m → vB/vC = 10/9.\n\n"
        "**Step 1:** vA : vB : vC = 100 : 90 : 81.\n\n"
        "**Step 2:** When A runs 400 m, C runs 400×81/100 = 324 m.\n\n"
        "**Step 3:** A beats C by 400 − 324 = 76 m.\n\n**Answer: 76**",
    ),
    (
        "217.50 m",
        "**Given:** 1500 m: Anil beats Bakul by 150 m; Bakul beats Charles by 75 m.\n\n"
        "**Step 1:** When Anil finishes, Bakul at 1350 m → vB/vA = 9/10.\n\n"
        "**Step 2:** When Bakul finishes, Charles at 1425 m → vC/vB = 19/20.\n\n"
        "**Step 3:** Charles at 1500×(9/10)×(19/20) = 1282.5 m when Anil finishes.\n\n"
        "**Step 4:** Anil beats Charles by 1500 − 1282.5 = 217.5 m.\n\n**Answer: 217.50 m**",
    ),
    (
        "352",
        "**Given:** 1000 m: Prakash beats Ved by 280 m; Ved beats Rahul by 100 m.\n\n"
        "**Step 1:** When Prakash finishes, Ved at 720 m.\n\n"
        "**Step 2:** When Ved runs 720 m, Rahul runs 720×(900/1000) = 648 m.\n\n"
        "**Step 3:** Prakash beats Rahul by 1000 − 648 = 352 m.\n\n**Answer: 352**",
    ),
    (
        "150 m",
        "**Given:** 1500 m: X gives Y 100 m start; X beats Z by 240 m.\n\n"
        "**Step 1:** When X finishes, Y at 1400 m, Z at 1260 m.\n\n"
        "**Step 2:** When Y finishes 1500 m, time factor 1500/1400 → Z at 1260×(15/14) = 1350 m.\n\n"
        "**Step 3:** Y beats Z by 1500 − 1350 = 150 m.\n\n**Answer: 150 m**",
    ),
    (
        "6.66M",
        "**Given:** 1000 m: A gives K 100 m start, beats K by 200 m; beats D by 300 m (both with 100 m start).\n\n"
        "**Step 1:** When A finishes, K at 800 m, D at 700 m → vK/vD = 8/7.\n\n"
        "**Step 2:** In 50 m race (no extra start), K runs 50 m, D runs 50×7/8 = 43.75 m.\n\n"
        "**Step 3:** K beats D by 6.25 m ≈ 6.66 m.\n\n**Answer: 6.66M**",
    ),
    (
        "140 metres",
        "**Given:** 500 m dead heat: Q gives P 50 m → P:Q = 9:10; R gives Q 100 m → Q:R = 4:5.\n\n"
        "**Step 1:** P:Q:R = 18:20:25.\n\n"
        "**Step 2:** For dead heat over 500 m, R runs 500, P runs (500 − h).\n"
        "(500 − h)/18 = 500/25 → h = 140 m.\n\n**Answer: 140 metres**",
    ),
    (
        "240 metres",
        "**Given:** Aman beats Ramesh by 48 m, Naresh by 68 m; Ramesh beats Naresh by 25 m.\n\n"
        "**Step 1:** vR/vN = 48/43 (from margins when Aman finishes).\n\n"
        "**Step 2:** (L − 48)/(L − 68) = 48/43 → 43L − 2064 = 48L − 3264 → L = 240 m.\n\n**Answer: 240 metres**",
    ),
    (
        "450",
        "**Given:** A beats B by 45 km, B beats C by 50 km, A beats C by 90 km.\n\n"
        "**Step 1:** Use formula L = ab/(a + b − c) = (45×50)/(45+50−90) = 2250/5 = 450 km.\n\n**Answer: 450**",
    ),
    (
        "35.2 km/h",
        "**Given:** 1000 m race; John beats Khan by 120 m; John = 40 km/h.\n\n"
        "**Step 1:** Same time: vK = 40 × (880/1000) = 35.2 km/h.\n\n**Answer: 35.2 km/h**",
    ),
    (
        "15 km/h",
        "**Given:** 5 km race; S gives T 500 m start; dead heat; T = 13.5 km/h.\n\n"
        "**Step 1:** S runs 5000 m, T runs 4500 m → vS/vT = 10/9.\n\n"
        "**Step 2:** vS = 13.5 × 10/9 = 15 km/h.\n\n**Answer: 15 km/h**",
    ),
    (
        "4.14 km/h",
        "**Given:** A runs 5 km/h; 100 m race; gives B 8 m start; beats by 8 s.\n\n"
        "**Step 1:** A time = 100 m at 5 km/h = 72 s.\n\n"
        "**Step 2:** B runs 92 m in 80 s → speed = 4.14 km/h.\n\n**Answer: 4.14 km/h**",
    ),
    (
        "11 m/s",
        "**Given:** 400 m; A = 16 m/s; gives B 15 m start; beats by 10 s.\n\n"
        "**Step 1:** A time = 400/16 = 25 s → B time = 35 s.\n\n"
        "**Step 2:** B runs 385 m in 35 s → speed = 11 m/s.\n\n**Answer: 11 m/s**",
    ),
    (
        "10/19",
        "**Given:** 1000 m; A beats B by 50 m or 5 s.\n\n"
        "**Step 1:** vA/vB = 1000/950 = 20/19.\n\n"
        "**Step 2:** 1000/vB − 1000/vA = 5 → vB = 10 m/s, vA = 200/19.\n\n"
        "**Step 3:** Difference = 10/19 m/s.\n\n**Answer: 10/19**",
    ),
    (
        "17/3 m/sec",
        "**Given:** vA:vB = 12:11 (1200/1100); vB:vC = 6:5 (600/500); A beats C by 30 s in 720 m.\n\n"
        "**Step 1:** vA:vC = 72:55.\n\n"
        "**Step 2:** 720/vC − 720/vA = 30 → vC = 17/3 m/sec.\n\n**Answer: 17/3 m/sec**",
    ),
    (
        "220 sec",
        "**Given:** 1 km; P beats Q by 120 m or 30 s.\n\n"
        "**Step 1:** vP/vQ = 1000/880 = 25/22.\n\n"
        "**Step 2:** 1000/vQ − 1000/vP = 30 → vQ = 4 m/s, vP = 50/11 m/s.\n\n"
        "**Step 3:** P's time = 1000/(50/11) = 220 s.\n\n**Answer: 220 sec**",
    ),
    (
        "4",
        "**Given:** 1500 m; A gives B 10 s start; dead heat; B = 6 m/s.\n\n"
        "**Step 1:** B total time = 1500/6 = 250 s; A runs for 240 s.\n\n"
        "**Step 2:** A's time = 240 s = 4 minutes.\n\n**Answer: 4**",
    ),
    (
        "205 s",
        "**Given:** A beats B by 30 s, B beats C by 15 s; A beats C by 180 m in 1 km.\n\n"
        "**Step 1:** tB − tA = 30, tC − tA = 45. When A finishes, C at 820 m → 820/vC = tA.\n\n"
        "**Step 2:** 820/(1000/(tA+45)) = tA → 820×45 = 180 tA → tA = 205 s.\n\n**Answer: 205 s**",
    ),
    (
        "77.5 seconds",
        "**Given:** 200 m; 25 m start → A wins by 10 s; 45 m start → dead heat.\n\n"
        "**Step 1:** From dead heat: vA/vB = 200/155.\n\n"
        "**Step 2:** 175/vB − 200/vA = 10 → 20/vB = 10 → vB = 2 m/s.\n\n"
        "**Step 3:** tA = 200/(400/155) = 77.5 s.\n\n**Answer: 77.5 seconds**",
    ),
    (
        "45 sec",
        "**Given:** 1500 m; 200 m start → P wins by 8 s; 400 m start → dead heat.\n\n"
        "**Step 1:** 1300/vQ − 1500/vP = 8 and 1500/vP = 1100/vQ.\n\n"
        "**Step 2:** 200/vQ = 8 → vQ = 25 m/s; tP = 1500/(1500/44) = 44 ≈ 45 s.\n\n**Answer: 45 sec**",
    ),
    (
        "6:5",
        "**Given:** Ravi beats Vinod (40 m start) by 19 s in 1000 m; 30 s start → Vinod beats Ravi by 40 m.\n\n"
        "**Step 1:** Equations give vR/vV = 6/5.\n\n**Answer: 6:5**",
    ),
    (
        "7.8",
        "**Given:** Pramika gets 396 m head start and starts 9 s before Savitha; Pramika = 6 m/s. "
        "Savitha catches up 250 s after Savitha starts.\n\n"
        "**Step 1:** When they meet, Pramika has run for 250 + 9 = 259 s → 6 × 259 = 1554 m from her start.\n\n"
        "**Step 2:** Same position: 396 + 1554 = 250v → 1950 = 250v.\n\n"
        "**Step 3:** v = 7.8 m/s.\n\n**Answer: 7.8**",
    ),
    (
        "8 hours",
        "**Given:** Walk + ride back = 5 h 45 min; ride both ways = 3 h 30 min.\n\n"
        "**Step 1:** Let walk one way = w, ride one way = r. w + r = 5.75; 2r = 3.5 → r = 1.75 h.\n\n"
        "**Step 2:** w = 5.75 − 1.75 = 4 h.\n\n"
        "**Step 3:** Walk both ways = 2w = 8 h.\n\n**Answer: 8 hours**",
    ),
    (
        "20 minutes",
        "**Given:** Salman usually picks up at 4 pm; Saturday school at 3 pm; children walk; home 20 min early.\n\n"
        "**Step 1:** Total time saved = 20 min → children walked 20 min.\n\n**Answer: 20 minutes**",
    ),
    (
        "15 minutes",
        "**Given:** Monkey: +10 m odd minutes, −2 m even minutes; pole 63 m.\n\n"
        "**Step 1:** After 14 min: 56 m. 15th minute climbs 10 m → reaches 66 m (>63).\n\n"
        "**Answer: 15 minutes**",
    ),
]


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    if len(SOLUTIONS) != 32:
        raise SystemExit(f"Expected 32 solutions, got {len(SOLUTIONS)}")

    for i, (answer, solution) in enumerate(SOLUTIONS):
        idx = START + i
        q = bank[idx]
        q["correctAnswer"] = answer
        q["solution"] = solution
        q.pop("explanation", None)

    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {len(SOLUTIONS)} questions ({bank[START]['id']} … {bank[START+31]['id']})")


if __name__ == "__main__":
    main()
