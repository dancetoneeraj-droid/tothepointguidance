"""
Bulk geometry solver: numeric brute-force + formula library.
Outputs scripts/geo-solutions-bulk.json
"""
from __future__ import annotations

import json
import math
import re
from itertools import combinations, permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "geometry.json"
OUT = ROOT / "scripts" / "geo-solutions-bulk.json"
START = 151
COUNT = 472


def parse_num(text: str) -> float | None:
    s = str(text).strip()
    s = re.sub(r"\bcm2?\b|m2|°|sq\.?cm|\(|\)|hectares?", "", s, flags=re.I)
    s = s.replace(" ", "").replace("√", "sqrt").replace("π", "pi").replace(",", "")
    s = re.sub(r"(\d)sqrt", r"\1*sqrt", s)
    try:
        return float(s)
    except ValueError:
        try:
            return float(eval(s, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi}))  # noqa: S307
        except Exception:
            return None


def extract_numbers(text: str) -> list[float]:
    text = text.replace("√", " sqrt")
    found: list[float] = []
    for m in re.finditer(
        r"(\d+(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?|\d+\s*sqrt\s*\(\s*\d+\s*\))",
        text,
        re.I,
    ):
        v = parse_num(m.group(1))
        if v is not None and v not in found:
            found.append(v)
    return found


def match_option(val: float, options: list[str], tol: float = 0.025) -> str | None:
    best, best_d = None, float("inf")
    for opt in options:
        ov = parse_num(opt)
        if ov is None:
            continue
        d = abs(ov - val) / max(abs(val), 1e-9)
        if d < best_d:
            best_d, best = d, opt
    return best if best_d <= tol else None


def candidates_from_numbers(nums: list[float]) -> list[float]:
    c: set[float] = set()
    for n in nums:
        if n <= 0:
            continue
        c.update([n, n**2, math.sqrt(n), 2 * n, n / 2, math.pi * n, n * math.pi])
    for a, b in permutations(nums, 2):
        if b == 0:
            continue
        c.update([a + b, abs(a - b), a * b, a / b, (a + b) / 2, math.sqrt(a**2 + b**2)])
        c.add(0.5 * a * b)
        for ang in (30, 45, 60, 90, 120):
            c.add(0.5 * a * b * math.sin(math.radians(ang)))
    for a, b, d in permutations(nums, 3):
        s = (a + b + d) / 2
        if s > a and s > b and s > d:
            try:
                c.add(math.sqrt(s * (s - a) * (s - b) * (s - d)))
            except ValueError:
                pass
        # similar triangles area ratio
        if b:
            c.add((a / b) ** 2)
    return [x for x in c if math.isfinite(x) and x > 0]


def solve_by_keywords(q: str, opts: list[str]) -> tuple[str, str] | None:
    ql = q.lower()
    nums = extract_numbers(q)

    # Similar triangles area ratio
    m = re.search(r"(\d+)\s*:\s*(\d+).*?(?:area|ratio)", ql, re.S)
    if m and "similar" in ql:
        a, b = int(m.group(1)), int(m.group(2))
        t = f"{a*a}:{b*b}"
        for o in opts:
            if t.replace(" ", "") in o.replace(" ", ""):
                return o, f"Area ratio = ({a}/{b})² = {a*a}:{b*b}\n\n**Answer: {o}**"

    # Parallel line XY
    m = re.search(r"ab\s*=\s*(\d+(?:\.\d+)?).*?bc\s*=\s*(\d+(?:\.\d+)?).*?bx\s*=\s*(\d+(?:\.\d+)?)", ql, re.S)
    if m and "xy" in ql:
        ab, bc, bx = map(float, m.groups())
        xy = bc * (ab - bx) / ab
        ans = match_option(xy, opts)
        if ans:
            return ans, f"XY = BC × (AX/AB) = {xy:.4g}\n\n**Answer: {ans}**"

    # Angle bisector
    m = re.search(r"ab\s*=\s*(\d+(?:\.\d+)?).*?ac\s*=\s*(\d+(?:\.\d+)?).*?(\d+(?:\.\d+)?)\s*°", ql, re.S)
    if m and "bisector" in ql:
        ab, ac, ang = float(m.group(1)), float(m.group(2)), float(m.group(3))
        ad = (2 * ab * ac / (ab + ac)) * math.cos(math.radians(ang / 2))
        ans = match_option(ad, opts, 0.03)
        if ans:
            return ans, f"AD = (2·AB·AC)/(AB+AC)·cos(A/2) = {ad:.4g}\n\n**Answer: {ans}**"

    # Two sides + angle area
    m = re.search(r"(\d+(?:\.\d+)?)\s*cm.*?(\d+(?:\.\d+)?)\s*cm.*?(\d+(?:\.\d+)?)\s*°", q, re.S)
    if m and "area" in ql:
        a, b, ang = float(m.group(1)), float(m.group(2)), float(m.group(3))
        area = 0.5 * a * b * math.sin(math.radians(ang))
        ans = match_option(area, opts, 0.03)
        if ans:
            return ans, f"Area = ½ab sin θ = {area:.4g}\n\n**Answer: {ans}**"

    # Heron max x
    m = re.search(r"(\d+)cm.*?(\d+)cm.*?x cm.*?maximum", ql, re.S)
    if m:
        b, c = float(m.group(1)), float(m.group(2))
        x = math.sqrt(b**2 + c**2)
        ans = match_option(x, opts)
        if ans:
            return ans, f"Max area ⟹ right triangle: x = √({b}²+{c}²)\n\n**Answer: {ans}**"

    # Rhombus hectares
    m = re.search(r"side is (\d+).*?diagonal.*?(\d+)", ql, re.S)
    if m and "rhombus" in ql:
        s, d1 = float(m.group(1)), float(m.group(2))
        d2 = 2 * math.sqrt(max(s**2 - (d1 / 2) ** 2, 0))
        ha = d1 * d2 / 2 / 10000
        ans = match_option(ha, opts, 0.015)
        if ans:
            return ans, f"Area = {d1*d2/2:.0f} m² = {ha:.4f} ha\n\n**Answer: {ans}**"

    # Chord tangent AP
    m = re.search(r"radius (\d+(?:\.\d+)?).*?distance (\d+(?:\.\d+)?)", ql, re.S)
    if m and "tangent" in ql and "chord" in ql:
        r, d = float(m.group(1)), float(m.group(2))
        h = math.sqrt(max(r**2 - d**2, 0))
        ap = math.sqrt((r**2 / d - d) ** 2 + h**2) if d else 0
        ans = match_option(ap, opts, 0.03)
        if ans:
            return ans, f"AP = {ap:.4g} cm\n\n**Answer: {ans}**"

    # Medians true statement
    if "medians" in ql and "true statement" in ql:
        for o in opts:
            if "ad+be+cf<ab+bc+ca" in o.lower().replace(" ", ""):
                return o, f"Sum of medians < perimeter.\n\n**Answer: {o}**"

    # Brute numeric from extracted numbers
    for val in candidates_from_numbers(nums):
        ans = match_option(val, opts, 0.02)
        if ans:
            return ans, f"Computed value ≈ {val:.4g}\n\n**Answer: {ans}**"

    return None


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    out: list[dict] = []
    for i in range(START, START + COUNT):
        e = bank[i]
        if e.get("solution") and "Placeholder" not in e.get("solution", ""):
            continue
        q, opts = e.get("question", ""), e.get("options", [])
        if not q or not opts:
            continue
        res = solve_by_keywords(q, opts)
        if res:
            ans, sol = res
            out.append({"id": e["id"], "correctAnswer": ans, "solution": sol})
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Bulk solved {len(out)} -> {OUT}")


if __name__ == "__main__":
    main()
