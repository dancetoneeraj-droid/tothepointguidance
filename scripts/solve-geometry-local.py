"""
Solve geometry questions (maths_geometry_152 onward) locally using sympy/math.
Run: python scripts/solve-geometry-local.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "geometry.json"
START = 151


def normalize(s: str) -> str:
    s = str(s).lower().strip()
    s = s.replace("cm²", "cm2").replace("cm^2", "cm2").replace("sq. cm", "cm2")
    s = s.replace(" ", "").replace(",", "")
    s = s.replace("−", "-").replace("–", "-")
    return s


def parse_num(text: str) -> float | None:
    if text is None:
        return None
    s = str(text).strip()
    s = re.sub(r"\bcm2?\b|m2|°|sq\.?cm|\(|\)", "", s, flags=re.I)
    s = s.replace("√", "sqrt").replace("π", "pi")
    s = re.sub(r"(\d)sqrt", r"\1*sqrt", s)
    s = re.sub(r"sqrt(\d)", r"sqrt(\1)", s)
    try:
        val = float(s)
        return val
    except ValueError:
        pass
    try:
        allowed = {"sqrt": math.sqrt, "pi": math.pi}
        return float(eval(s, {"__builtins__": {}}, allowed))  # noqa: S307
    except Exception:
        return None


def match_option(computed: float, options: list[str], tol: float = 0.02) -> str | None:
    best = None
    best_diff = float("inf")
    for opt in options:
        val = parse_num(opt)
        if val is None:
            continue
        diff = abs(val - computed) / max(abs(computed), 1e-9)
        if diff < best_diff:
            best_diff = diff
            best = opt
    if best is not None and best_diff <= tol:
        return best
    return None


def match_option_text(computed_str: str, options: list[str]) -> str | None:
    c = normalize(computed_str)
    for opt in options:
        if normalize(opt) == c:
            return opt
    cv = parse_num(computed_str)
    if cv is not None:
        return match_option(cv, options, tol=0.05)
    return None


def extract_floats(text: str) -> list[float]:
    text = text.replace("√", " sqrt")
    nums: list[float] = []
    for m in re.finditer(
        r"(\d+(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?(?:\s*\*\s*sqrt\s*\(\s*\d+\s*\))?|\d+\s*sqrt\s*\(\s*\d+\s*\))",
        text,
        re.I,
    ):
        v = parse_num(m.group(1).replace(" ", ""))
        if v is not None:
            nums.append(v)
    return nums


def extract_angle_deg(text: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)\s*°", text)
    return float(m.group(1)) if m else None


def fmt_sqrt(val: float, unit: str = "") -> str:
    """Format numeric result trying common SSC forms."""
    for denom in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 20, 24, 25, 27, 30, 36, 49, 64]:
        for num in range(1, 200):
            for rt in [2, 3, 5, 6, 7, 10, 11, 13, 21]:
                cand = num * math.sqrt(rt) / denom
                if abs(cand - val) / max(val, 1e-9) < 0.005:
                    if denom == 1:
                        s = f"{num}√{rt}" if rt != 1 else str(num)
                    else:
                        s = f"{num}√{rt}/{denom}" if rt != 1 else f"{num}/{denom}"
                    return s + unit
    if abs(val - round(val)) < 0.01:
        return str(int(round(val))) + unit
    return f"{val:.4g}{unit}"


def sol_md(steps: str, answer: str) -> str:
    return steps.rstrip() + f"\n\n**Answer: {answer}**"


def try_area_two_sides_angle(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(
        r"two sides are (\d+(?:\.\d+)?)\s*cm.*?(\d+(?:\.\d+)?)\s*cm.*?angle between them is (\d+(?:\.\d+)?)\s*°",
        q,
        re.I | re.S,
    )
    if not m:
        return None
    a, b, ang = float(m.group(1)), float(m.group(2)), float(m.group(3))
    area = 0.5 * a * b * math.sin(math.radians(ang))
    ans = match_option(area, opts, tol=0.03)
    if not ans:
        return None
    return ans, sol_md(
        f"**Formula:** Area = ½ × a × b × sin θ\n\n"
        f"= ½ × {a} × {b} × sin {ang}° = {area:.4g} cm²",
        ans,
    )


def try_cos_theta_area(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(
        r"area (\d+(?:\.\d+)?).*?AB\s*=\s*(\d+(?:\.\d+)?).*?BC\s*=\s*(\d+(?:\.\d+)?).*?cos\s*θ",
        q,
        re.I | re.S,
    )
    if not m:
        return None
    area, ab, bc = float(m.group(1)), float(m.group(2)), float(m.group(3))
    sin_t = 2 * area / (ab * bc)
    cos_t = math.sqrt(max(0, 1 - sin_t**2))
    for opt in opts:
        ov = parse_num(opt)
        if ov and abs(ov - cos_t) < 0.02:
            return opt, sol_md(
                f"Area = ½ × AB × BC × sin θ = {area}\n"
                f"sin θ = {sin_t:.4g}, cos θ = √(1 − sin²θ) = {cos_t:.4g}",
                opt,
            )
    return None


def try_angle_bisector(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(
        r"AB\s*=\s*(\d+(?:\.\d+)?)\s*cm.*?AC\s*=\s*(\d+(?:\.\d+)?)\s*cm.*?∠BAC\s*=\s*(\d+(?:\.\d+)?)\s*°.*?length of AD",
        q,
        re.I | re.S,
    )
    if not m:
        return None
    ab, ac, ang = float(m.group(1)), float(m.group(2)), float(m.group(3))
    ad = (2 * ab * ac / (ab + ac)) * math.cos(math.radians(ang / 2))
    for opt in opts:
        ov = parse_num(opt)
        if ov and abs(ov - ad) / ad < 0.02:
            return opt, sol_md(
                f"**Angle bisector:** AD = (2·AB·AC)/(AB+AC) × cos(A/2)\n"
                f"= (2×{ab}×{ac})/({ab}+{ac}) × cos({ang/2}°) = {ad:.4g} cm",
                opt,
            )
    return None


def try_similar_area_ratio(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(r"ratio.*?(\d+)\s*:\s*(\d+).*?areas", q, re.I | re.S)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    r = (a / b) ** 2
    target = f"{a*a} : {b*b}"
    for opt in opts:
        if normalize(opt) == normalize(target):
            return opt, sol_md(
                f"Area ratio of similar triangles = (side ratio)² = ({a}/{b})² = {a*a}:{b*b}",
                opt,
            )
    return None


def try_parallel_line_similar(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(
        r"AB\s*=\s*(\d+(?:\.\d+)?).*?BC\s*=\s*(\d+(?:\.\d+)?).*?BX\s*=\s*(\d+(?:\.\d+)?).*?length of XY",
        q,
        re.I | re.S,
    )
    if not m:
        return None
    ab, bc, bx = float(m.group(1)), float(m.group(2)), float(m.group(3))
    ax = ab - bx
    xy = bc * ax / ab
    ans = match_option(xy, opts)
    if not ans:
        return None
    return ans, sol_md(
        f"ΔAXY ~ ΔABC ⇒ XY/BC = AX/AB = {ax}/{ab}\nXY = {xy:.4g} cm",
        ans,
    )


def try_incentre_circumcenter_dist(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(r"sides are (\d+),?\s*(\d+)\s*and\s*(\d+)", q, re.I)
    if not m or "incentre" not in q.lower() and "incenter" not in q.lower():
        return None
    a, b, c = sorted([float(m.group(1)), float(m.group(2)), float(m.group(3))])
    if abs(a**2 + b**2 - c**2) > 0.1:  # not right triangle
        return None
    r = (a + b - c) / 2
    R = c / 2
    d = math.sqrt(R * (R - 2 * r))
    ans = match_option(d, opts)
    if not ans:
        for opt in opts:
            if "√5" in opt and abs(d - math.sqrt(5)) < 0.05:
                return opt, sol_md(
                    f"Right triangle 6-8-10: r = {r}, R = {R}\n"
                    f"Distance = √(R(R−2r)) = √5 cm",
                    opt,
                )
    if ans:
        return ans, sol_md(f"For right triangle, distance = √(R(R−2r)) = {d:.4g} cm", ans)
    return None


def try_rhombus_hectares(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(r"side is (\d+)\s*m.*?diagonal.*?(\d+)\s*m", q, re.I | re.S)
    if not m or "rhombus" not in q.lower():
        return None
    s, d1 = float(m.group(1)), float(m.group(2))
    d2 = 2 * math.sqrt(s**2 - (d1 / 2) ** 2)
    area_m2 = d1 * d2 / 2
    ha = area_m2 / 10000
    ans = match_option(ha, opts, tol=0.01)
    if ans:
        return ans, sol_md(
            f"d₂ = 2√(s² − (d₁/2)²) = {d2:.2f} m\n"
            f"Area = d₁d₂/2 = {area_m2:.0f} m² = {ha:.4f} ha",
            ans,
        )
    return None


def try_tangent_length(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(
        r"radius (\d+(?:\.\d+)?).*?distance (\d+(?:\.\d+)?).*?tangent AP",
        q,
        re.I | re.S,
    )
    if not m:
        return None
    r, d = float(m.group(1)), float(m.group(2))
    half = math.sqrt(r**2 - d**2)
    # P at (r^2/d, 0) style; AP = sqrt((r^2/d - r*...)) 
    # coordinates: O origin, chord at x=d, half chord h=sqrt(r^2-d^2), A=(d,h)
    # tangent at A: dx+hy=r^2; with B=(d,-h) intersection P=(r^2/d, 0)
    ap = math.sqrt((r**2 / d - d) ** 2 + half**2)
    ans = match_option(ap, opts, tol=0.02)
    if ans:
        return ans, sol_md(
            f"Half chord = √(r²−d²) = {half:.2g} cm\n"
            f"Tangents at A,B meet at P; AP = {ap:.4g} cm",
            ans,
        )
    return None


def try_median_inequality(q: str, opts: list[str]) -> tuple[str, str] | None:
    if "medians" not in q.lower() or "true statement" not in q.lower():
        return None
    for opt in opts:
        if "AD+BE+CF<AB+BC+CA" in opt.replace(" ", ""):
            return opt, sol_md(
                "Sum of medians is always **less than** the perimeter of the triangle.",
                opt,
            )
    return None


def try_isosceles_right_perimeter(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(r"isosceles right.*?area of (\d+(?:\.\d+)?)\s*cm", q, re.I | re.S)
    if not m:
        return None
    area = float(m.group(1))
    leg = math.sqrt(2 * area)
    peri = 2 * leg + leg * math.sqrt(2)
    ans = match_option(peri, opts, tol=0.03)
    if ans:
        return ans, sol_md(
            f"Leg a: area = a²/2 = {area} ⇒ a = {leg:.4g}\n"
            f"Perimeter = 2a + a√2 = {peri:.4g} cm",
            ans,
        )
    return None


def try_heron_max_area(q: str, opts: list[str]) -> tuple[str, str] | None:
    m = re.search(r"sides.*?(\d+)cm.*?(\d+)cm.*?x cm.*?maximum", q, re.I | re.S)
    if not m:
        return None
    b, c = float(m.group(1)), float(m.group(2))
    # maximize area with sides b, c, x: x = sqrt(b^2+c^2) for right triangle? 
    # Actually max when angle between b and c is 90°, x = sqrt(b^2+c^2)
    x = math.sqrt(b**2 + c**2)
    ans = match_option(x, opts, tol=0.02)
    if ans:
        return ans, sol_md(
            f"Area is maximum when the triangle is right-angled at the included angle.\n"
            f"x = √({b}²+{c}²) = {x:.4g} cm",
            ans,
        )
    return None


SOLVERS = [
    try_area_two_sides_angle,
    try_cos_theta_area,
    try_angle_bisector,
    try_similar_area_ratio,
    try_parallel_line_similar,
    try_incentre_circumcenter_dist,
    try_rhombus_hectares,
    try_tangent_length,
    try_median_inequality,
    try_isosceles_right_perimeter,
    try_heron_max_area,
]


def solve_entry(q: str, opts: list[str]) -> tuple[str, str] | None:
    for fn in SOLVERS:
        try:
            res = fn(q, opts)
            if res:
                return res
        except Exception:
            continue
    return None


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    solved = 0
    failed: list[str] = []
    for i in range(START, START + 472):
        entry = bank[i]
        if entry.get("solution") and "Placeholder" not in entry.get("solution", ""):
            continue
        q = entry.get("question", "")
        opts = entry.get("options", [])
        if not q or not opts:
            failed.append(entry["id"])
            continue
        res = solve_entry(q, opts)
        if res:
            entry["correctAnswer"], entry["solution"] = res
            entry.pop("explanation", None)
            solved += 1
        else:
            failed.append(entry["id"])

    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Locally solved {solved}; {len(failed)} remaining")
    if failed[:10]:
        print("First unsolved:", ", ".join(failed[:10]))


if __name__ == "__main__":
    main()
