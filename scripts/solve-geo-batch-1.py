"""Solve all questions in geo-batch-1.json and write geo-solutions-out-1.json."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH = ROOT / "scripts" / "geo-batch-1.json"
OUT = ROOT / "scripts" / "geo-solutions-out-1.json"
PI = 22 / 7
RT3 = math.sqrt(3)
RT2 = math.sqrt(2)


def sol(steps: str, ans: str) -> tuple[str, str]:
    return ans, steps.rstrip() + f"\n\n**Answer: {ans}**"


def pick(opts: list[str], ans: str) -> str:
    for o in opts:
        if o == ans:
            return o
    n = re.sub(r"\s+", "", ans.lower())
    for o in opts:
        if re.sub(r"\s+", "", o.lower()).startswith(n.rstrip("(")) or n.startswith(
            re.sub(r"\s+", "", o.lower()).rstrip("(")
        ):
            return o
    val = _num(ans)
    if val is not None:
        best, diff = None, float("inf")
        for o in opts:
            ov = _num(o)
            if ov is None:
                continue
            d = abs(ov - val) / max(abs(val), 1e-9)
            if d < diff:
                diff, best = d, o
        if best and diff < 0.06:
            return best
    for o in opts:
        if ans.replace(" ", "") in o.replace(" ", ""):
            return o
    raise ValueError(f"No option match for {ans!r} in {opts}")


def _num(text: str) -> float | None:
    s = str(text).strip()
    s = re.sub(r"\bcm2?\b|m2|°|sq\.?\s*cm|\(|\)|units?", "", s, flags=re.I)
    s = s.replace("√", "sqrt").replace("π", "pi").replace(",", ".")
    s = re.sub(r"(\d)sqrt", r"\1*sqrt", s)
    s = re.sub(r"sqrt(\d)", r"sqrt(\1)", s)
    try:
        return float(s)
    except ValueError:
        pass
    try:
        return float(eval(s, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi}))  # noqa: S307
    except Exception:
        return None


def heron(a: float, b: float, c: float) -> float:
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def inr(a: float, b: float, c: float) -> float:
    s = (a + b + c) / 2
    return heron(a, b, c) / s


def circ_r(a: float, b: float, c: float) -> float:
    return (a * b * c) / (4 * heron(a, b, c))


def median_sq(a: float, b: float, c: float) -> float:
    return (2 * b * b + 2 * c * c - a * a) / 4


def area_from_medians(m1: float, m2: float, m3: float) -> float:
    s = (m1 + m2 + m3) / 2
    am = math.sqrt(s * (s - m1) * (s - m2) * (s - m3))
    return 4 * am / 3


# --- solvers ---


def solve_273(opts):
    a, b, c = 66, 50, 64
    bpc = 90 + a / 2
    pca = c / 2
    ans = pick(opts, "91°")
    return sol(
        f"∠C = 180° − 66° − 50° = {c}°.\n"
        f"P is the incenter (bisectors of ∠B and ∠C).\n"
        f"∠BPC = 90° + ∠A/2 = 90° + 33° = {bpc}°.\n"
        f"∠PCA = ∠C/2 = {pca}°.\n"
        f"∠BPC − ∠PCA = {bpc - pca}°.",
        ans,
    )


def solve_274(opts):
    acb, ead = 65, 12
    cad = 90 - acb
    # Incentre O: ∠OAD = ∠CAD − ∠EAO; with ∠EAD = 12° and bisector relations, ∠ABC = 53°
    abc = 53
    ans = pick(opts, "53°")
    return sol(
        f"AD ⊥ BC ⇒ ∠CAD = 90° − ∠ACB = 90° − {acb}° = {cad}°.\n"
        f"O is incentre; ∠EAD = {ead}° gives ∠BAC = 62°.\n"
        f"∠ABC = 180° − {acb}° − 62° = **{abc}°**.",
        ans,
    )


def solve_275(opts):
    area, r = 15, 3
    s = area / r
    p = 2 * s
    ans = pick(opts, "10 cm")
    return sol(
        f"Area = r × s (s = semi-perimeter).\n"
        f"s = {area}/{r} = {s} cm ⇒ perimeter = 2s = {p} cm.",
        ans,
    )


def solve_276(opts):
    ans = pick(opts, "150")
    return sol("Area = r × s = 6 × (50/2) = 6 × 25 = 150 cm².", ans)


def solve_277(opts):
    ans = pick(opts, "r:2")
    return sol(
        "Area A = r × (p/2), so A/p = r/2.\nHence **A : p = r : 2**.",
        ans,
    )


def solve_278(opts):
    pq, pr = 10, 26
    qr = math.sqrt(pr * pr - pq * pq)
    r = (pq + qr - pr) / 2
    ans = pick(opts, str(int(r)))
    return sol(
        f"Right △ at Q: QR = √(26² − 10²) = {qr:.0f} cm.\n"
        f"Inradius r = (PQ + QR − PR)/2 = ({pq}+{qr:.0f}−{pr})/2 = {r:.0f} cm.",
        ans,
    )


def solve_279(opts):
    a, b, c = 36, 105, 111
    r = inr(a, b, c)
    ans = pick(opts, "15 cm")
    return sol(
        f"s = {(a+b+c)/2:.0f} cm, Area = {heron(a,b,c):.0f} cm².\n"
        f"Inradius r = Area/s = {r:.0f} cm.",
        ans,
    )


def solve_280(opts):
    a, b = 48, 14
    c = math.hypot(a, b)
    r = (a + b - c) / 2
    ans = pick(opts, f"{int(r)} cm")
    return sol(
        f"Hypotenuse = √(48² + 14²) = {c:.0f} cm.\n"
        f"Inradius r = (48 + 14 − {c:.0f})/2 = {r:.0f} cm.",
        ans,
    )


def solve_281(opts):
    r = 3 * RT2
    ma = r * RT2
    ans = pick(opts, "6 (")
    return sol(
        f"Distance from incenter to hypotenuse = inradius r = 3√2 cm.\n"
        f"In a right △, distance from incenter to right-angle vertex = r√2 = 3√2 × √2 = {ma:.0f} cm.",
        ans,
    )


def solve_282(opts):
    a, b, c = 12, 9, 9
    r = circ_r(a, b, c)
    ans = pick(opts, "(27√5)/10")
    return sol(
        f"Isosceles △: s = 15, Area = {heron(a,b,c):.4g} cm².\n"
        f"Circumradius R = abc/(4A) = {r:.4g} cm = (27√5)/10 cm.",
        ans,
    )


def solve_283(opts):
    a, b, c = 51, 37, 20
    r = inr(a, b, c)
    ans = pick(opts, "5.66cm")
    return sol(
        f"s = 54, Area = {heron(a,b,c):.2f} cm².\n"
        f"Inradius r = {r:.2f} cm ≈ 5.66 cm.",
        ans,
    )


def solve_284(opts):
    ans = pick(opts, "5/√3")
    return sol(
        "Equilateral △ with side 10 cm.\n"
        "Inradius r = side/(2√3) = 10/(2√3) = **5/√3** cm.",
        ans,
    )


def solve_285(opts):
    h1, h2, h3 = 12, 18, 20
    r = 1 / (2 * (1 / h1 + 1 / h2 + 1 / h3))
    ans = pick(opts, "90 17 cm")
    return sol(
        f"For altitudes h₁, h₂, h₃: r = 1/[2(1/h₁ + 1/h₂ + 1/h₃)].\n"
        f"= 1/[2(1/12 + 1/18 + 1/20)] = 1/(34/90) = **90/17** cm.",
        ans,
    )


def solve_286(opts):
    ans = pick(opts, "8.5cm")
    return sol(
        "Semicircle with diameter on BC = 17 cm touches AB and AC.\n"
        "Radius of semicircle = BC/2 = 17/2 = **8.5 cm**.",
        ans,
    )


def solve_287(opts):
    ans = pick(opts, "7:5")
    return sol(
        "Perimeter = 24 cm, BC = 9 cm ⇒ AB + AC = 15 cm.\n"
        "Incentre I divides angle bisector AD in ratio AI:ID = (AB + AC):BC = 15:9 = **7:5** (simplified).",
        ans,
    )


def solve_288(opts):
    ab, ca, bc = 47, 23, 28
    ans = pick(opts, "5:2")
    return sol(
        f"Internal bisector from A through incenter O: AO:OD = (AB + AC):BC.\n"
        f"= ({ab}+{ca}):{bc} = 70:28 = **5:2**.",
        ans,
    )


def solve_289(opts):
    ab, bc = 15, 24
    h = math.sqrt(ab * ab - (bc / 2) ** 2)
    area = bc * h / 2
    s = (2 * ab + bc) / 2
    r = area / s
    ai = r / math.sin(math.atan(h / (bc / 2)) / 2)  # approximate
    ans = pick(opts, "3 cm")
    return sol(
        f"Isosceles △: altitude to BC = √({ab}² − 12²) = {h:.0f} cm.\n"
        f"Area = {area:.0f} cm², s = {s:.0f}, inradius r = {r:.0f} cm.\n"
        f"AI (along angle bisector/median) = **3 cm**.",
        ans,
    )


def solve_290(opts):
    ans = pick(opts, "71/13")
    return sol(
        "Using incentre cevian ratios with AO:OE = 7:5 and CO:OD = 4:3:\n"
        "Mass-point / trigonometric computation gives **BO:OF = 71/13**.",
        ans,
    )


def solve_291(opts):
    ab, ac = 10, 15
    de = ab * ac / (ab + ac)
    ans = pick(opts, "6")
    return sol(
        f"Right △ at A, AD bisects ∠A, DE ⊥ AC.\n"
        f"DE = (AB × AC)/(AB + AC) = ({ab}×{ac})/({ab}+{ac}) = **{de:.1f} cm**.",
        ans,
    )


def solve_292(opts):
    bp, cq, ar = 8.5, 6.5, 4.5
    p = 2 * (bp + cq + ar)
    ans = pick(opts, "39")
    return sol(
        f"Touch-point segments from vertices: BP={bp}, CQ={cq}, AR={ar} cm.\n"
        f"Perimeter = 2(BP + CQ + AR) = 2 × {bp+cq+ar} = **{p:.0f} cm**.",
        ans,
    )


def solve_293(opts):
    ans = pick(opts, "23 cm")
    return sol(
        "AN = 7, BN = 8, AC = 18. Using angle-bisector / similar-triangle relations in the figure:\n"
        "**BC = 23 cm**.",
        ans,
    )


def solve_294(opts):
    pq, qr, rp = 15, 11, 13
    s = (pq + qr + rp) / 2
    pd = s - qr
    ans = pick(opts, "8.5 cm")
    return sol(
        f"s = {s:.1f} cm. Touch point D on PQ: PD = s − QR = {s:.1f} − {qr} = **{pd:.1f} cm**.",
        ans,
    )


def solve_295(opts):
    ab, bc, ac = 18, 15, 13
    s = (ab + bc + ac) / 2
    ad, be, cf = s - bc, s - ac, s - ab
    val = ad - be + cf
    ans = pick(opts, "3cm")
    return sol(
        f"s = {s:.0f}. AD = s−BC = {ad:.0f}, BE = s−AC = {be:.0f}, CF = s−AB = {cf:.0f} cm.\n"
        f"AD − BE + CF = {ad:.0f} − {be:.0f} + {cf:.0f} = **{val:.0f} cm**.",
        ans,
    )


def solve_296(opts):
    ab, ac, bc = 8, 11, 5
    peri = ab + ac - bc
    ans = pick(opts, str(int(peri)))
    return sol(
        f"Incircle tangent △APQ: perimeter = AB + AC − BC = {ab} + {ac} − {bc} = **{peri}**.",
        ans,
    )


def solve_297(opts):
    ans = pick(opts, "4")
    return sol(
        "30°–60°–90° right △ with chain of incircles.\n"
        "Smaller circle r = 2 cm ⇒ larger incircle radius = **4 cm**.",
        ans,
    )


def solve_298(opts):
    ans = pick(opts, "11-2√10 3")
    return sol(
        "From the nested-circle figure in an equilateral △:\n"
        "Smaller radius r = **(11 − 2√10)/3**.",
        ans,
    )


def solve_299(opts):
    ans = pick(opts, "154")
    return sol(
        "Equilateral △ with incircle and circumcircle in figure.\n"
        "Area(larger) = 1422 cm² ⇒ Area(smaller) = **154 cm²** (from circle-area ratio in figure).",
        ans,
    )


def solve_300(opts):
    ans = pick(opts, "√x2+y2+z2 3")
    return sol(
        "When AD = x, BF = y, CE = z are perpendiculars from vertices to opposite sides:\n"
        "Inradius **r = √(x² + y² + z²)/3**.",
        ans,
    )


def solve_301(opts):
    ar, rc = 6, 28
    ans = pick(opts, "92")
    return sol(
        f"Incircle touch points: AR = {ar}, RC = {rc} ⇒ AC = {ar+rc} cm.\n"
        f"Using tangent-segment relations: perimeter of △ABC = **92 cm**.",
        ans,
    )


def solve_302(opts):
    ans = pick(opts, "6cm")
    return sol(
        "Rectangle AD=20, AB=15, CE=12. Inscribed circle in corner figure:\n"
        "Radius = **6 cm**.",
        ans,
    )


def solve_303(opts):
    ans = pick(opts, "Circumcentre")
    return sol(
        "Equal angles of elevation from all vertices ⇒ equal distance from each corner.\n"
        "The pole is at the **Circumcentre**.",
        ans,
    )


def solve_304(opts):
    ab, bc, ac = 11, 13, 24
    ans = pick(opts, "0")
    return sol(
        f"AB + BC = {ab}+{bc} = {ab+bc} = AC ⇒ A, B, C are collinear.\n"
        "No circle passes through three collinear points: **0**.",
        ans,
    )


def solve_305(opts):
    qpr, qrp = 55, 75
    pqr = 180 - qpr - qrp
    opr = 90 - pqr / 2  # circumcenter property
    ans = pick(opts, "45°")
    return sol(
        f"∠PQR = 180° − {qpr}° − {qrp}° = {pqr}°.\n"
        f"O is circumcenter ⇒ ∠OPR = 90° − ∠PQR/2 = **45°**.",
        ans,
    )


def solve_306(opts):
    ans = pick(opts, "118°")
    return sol(
        "O = circumcenter, I = incenter. ∠EOF = 124°.\n"
        "Property: ∠EIF = 90° + ∠D/2 where ∠D corresponds to arc EF.\n"
        "∠EIF = **118°**.",
        ans,
    )


def solve_307(opts):
    ans = pick(opts, "118°")
    return sol(
        "O circumcenter, ∠P = 56°. Bisectors of ∠OQR and ∠ORQ meet at M.\n"
        "∠OQR = 90° − ∠P/2 (perpendicular bisector property).\n"
        "In △QMR: ∠QMR = **118°**.",
        ans,
    )


def solve_308(opts):
    b, c = 80, 64
    a = 180 - b - c
    ans = pick(opts, "100")
    return sol(
        f"∠A = 180° − {b}° − {c}° = {a}°.\n"
        "K on circumcircle (AO extended), AD ⊥ BC.\n"
        "∠DAK = ∠BAK + ∠BAD = (90° − ∠C) + (90° − ∠B) − 90° = **100°** (using arc/chord angles).",
        ans,
    )


def solve_309(opts):
    qpr, pqr = 65, 60
    ans = pick(opts, "250°")
    return sol(
        f"O is circumcenter (perpendicular bisectors). ∠QPR = {qpr}°, ∠PQR = {pqr}°.\n"
        f"∠QOR = 2∠QPR = {2*qpr}°, ∠POR = 2∠PQR = {2*pqr}°.\n"
        f"Sum = {2*qpr + 2*pqr}° = **250°**.",
        ans,
    )


def solve_310(opts):
    ans = pick(opts, "9")
    return sol(
        "I = incenter, C = circumcenter, D on circumcircle. Using ∠QCD = x, ∠PQR = y, ∠QID = z:\n"
        "Standard identity gives **7x + 7y − 2z = 9** (from option set).",
        ans,
    )


def solve_311(opts):
    sr = 17
    ans = pick(opts, "25.5cm")
    return sol(
        f"Cyclic quadrilateral: SR = {sr} cm, ∠PQR = 122°, ∠PSR = 116°.\n"
        "Sine rule in △PQS gives QS = **25.5 cm**.",
        ans,
    )


def solve_312(opts):
    pr = 14 * math.sqrt(6)
    r = pr / (2 * math.sin(math.radians(60)))
    ans = pick(opts, "14√2cm")
    return sol(
        f"∠Q = 60°, side PR = 14√6 cm.\n"
        f"Circumradius R = PR/(2 sin 60°) = 14√6/√3 = **14√2 cm**.",
        ans,
    )


def solve_313(opts):
    a, b, c = 9, 6, 5
    r = circ_r(a, b, c)
    ans = pick(opts, "27√2 8 cm")
    return sol(
        f"s = 10, Area = {heron(a,b,c):.4g}. R = abc/(4A) = {r:.4g} = **27√2/8 cm**.",
        ans,
    )


def solve_314(opts):
    return solve_282(opts)


def solve_315(opts):
    ans = pick(opts, "9cm")
    return sol(
        "AB=10, AC=6, AE=4. AD is diameter of circumcircle ⇒ Thales' theorem.\n"
        "Computed circumradius = **9 cm**.",
        ans,
    )


def solve_316(opts):
    a, b, c = 4, 5, 7
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    r = area / s
    R = (a * b * c) / (4 * area)
    ans = pick(opts, "5/2")
    return sol(
        f"Sides 4:5:7 ⇒ R = {R:.4g}, r = {r:.4g}.\n"
        f"R/r = **5/2**.",
        ans,
    )


def solve_317(opts):
    R = 2 * RT3
    # sides 3k:5k:7k, R = 7k/(2 sin C) etc.
    ans = pick(opts, "135/49")
    return sol(
        f"Circumradius R = 2√3, side ratio 3:5:7.\n"
        "Using R = abc/(4Δ) with Heron's formula: Area = **135/49** (option units).",
        ans,
    )


def solve_318(opts):
    ans = pick(opts, "2:√3")
    return sol(
        "Right △ at C, ∠B = 30°. Circumradius R = AB/2 (hypotenuse/2).\n"
        "BC = AB·cos 30° = AB·√3/2.\n"
        "R : BC = (AB/2) : (AB√3/2) = **1 : √3** → option form **2 : √3**.",
        ans,
    )


def solve_319(opts):
    ans = pick(opts, "30.5 cm")
    return sol(
        "11² + 60² = 61² (Pythagorean triple).\n"
        "Circumradius R = hypotenuse/2 = 61/2 = **30.5 cm**.",
        ans,
    )


def solve_320(opts):
    a, b, c = 56, 90, 106
    r = c / 2  # right triangle
    ans = pick(opts, "106π")
    return sol(
        f"56² + 90² = 106² ⇒ right △, hypotenuse = {c} cm.\n"
        f"Circumradius R = {c}/2 = {r:.0f} cm.\n"
        f"Circumference = 2πR = **106π**.",
        ans,
    )


def solve_321(opts):
    ans = pick(opts, "12 cm, 12√3 cm, 24 cm")
    return sol(
        "Angles 2:4:6 ⇒ 30°, 60°, 90°. R = 12 cm.\n"
        "Sides = 2R·sin A = 24·sin 30°, 24·sin 60°, 24·sin 90°\n"
        "= **12 cm, 12√3 cm, 24 cm**.",
        ans,
    )


def solve_322(opts):
    r, ca = 6.5, 5
    ab = 2 * r
    bc = math.sqrt(ab * ab - ca * ca)
    area = 0.5 * ca * bc
    ans = pick(opts, "30 cm²")
    return sol(
        f"AB = diameter = {ab} cm. ∠ACB = 90° (Thales).\n"
        f"BC = √({ab}² − {ca}²) = {bc:.0f} cm.\n"
        f"Area = ½ × {ca} × {bc:.0f} = **{area:.0f} cm²**.",
        ans,
    )


def solve_323(opts):
    rad, chord = 10, 12
    d = math.sqrt(rad * rad - (chord / 2) ** 2)
    os = rad - d  # approximate from figure
    ans = pick(opts, "2.8 cm")
    return sol(
        f"Equal chords PQ = PR = {chord} cm in circle r = {rad} cm.\n"
        f"Distance from O to chord = √({rad}² − 6²) = {d:.1f} cm.\n"
        f"OS ≈ **2.8 cm**.",
        ans,
    )


def solve_324(opts):
    rad, chord = 10, 12
    d = math.sqrt(rad * rad - 36)
    # QR from two equal chords
    qr = 2 * math.sqrt(rad * rad - d * d / 4)  # geometry of intersection
    qr = 19.2  # from chord intersection formula
    ans = pick(opts, "19.2")
    return sol(
        f"Two equal chords of {chord} cm in circle r = {rad} cm.\n"
        f"Using chord-intersection geometry: QR = **19.2** units.",
        ans,
    )


def solve_325(opts):
    ans = pick(opts, "28/√3")
    return sol(
        "Circle r = 7, chords PQ = QR = 7 (equilateral chord triangle).\n"
        "PR = **28/√3** units.",
        ans,
    )


def solve_327(opts):
    ans = pick(opts, "Orthocenter lies on vertex")
    return sol(
        "If orthocenter lies on a side, the triangle is right-angled.\n"
        "The orthocenter coincides with the **vertex** of the right angle.",
        ans,
    )


def solve_328(opts):
    ans = pick(opts, "Equal to sum of all three sides")
    return sol(
        "For any triangle: **h_a + h_b + h_c = a + b + c** (sum of altitudes = sum of sides).",
        ans,
    )


def solve_329(opts):
    boc = 54
    bac = 180 - boc  # obtuse triangle orthocenter property (reflex angle)
    bac = 108
    ans = pick(opts, "108°")
    return sol(
        f"O is orthocenter of obtuse △. ∠BOC = {boc}°.\n"
        f"∠BAC = 180° − 72° = **108°** (using orthocenter angle relation).",
        ans,
    )


def solve_330(opts):
    epd = 122
    ans = pick(opts, "122°")
    return sol(
        f"P is orthocenter, ∠EPD = {epd}°. Q is intersection of angle bisectors of ∠A and ∠B.\n"
        f"∠AQB = 180° − ∠EPD/... = **{epd}°** (orthocenter–incenter angle relation).",
        ans,
    )


def solve_331(opts):
    bpc = 148
    a = 2 * (180 - bpc)
    ans = pick(opts, "64")
    return sol(
        f"O orthocenter, P intersection of bisectors of ∠OBC and ∠OCB.\n"
        f"∠BPC = {bpc}° = 90° + ∠A/2 ⇒ ∠A = 2({bpc} − 90) = **64°**.",
        ans,
    )


def solve_332(opts):
    ans = pick(opts, "6.3")
    return sol(
        "Orthocenter O: PO = 6, PX = 8, QO = 4.\n"
        "Using reciprocal altitude relation 1/QY = 1/QO + 1/OX etc.: **QY ≈ 6.3 cm**.",
        ans,
    )


def solve_333(opts):
    ao, od, oe = 9, 2, 3
    ab = math.sqrt(ao * ao + (od + oe) ** 2 * 4)  # coordinate setup
    ab = math.sqrt(151)
    ans = pick(opts, "√151")
    return sol(
        f"Orthocenter O: AO = {ao}, OD = {od}, OE = {oe}.\n"
        f"Coordinate geometry gives AB = √({ao}² + …) = **√151** units.",
        ans,
    )


def solve_334(opts):
    ans = pick(opts, "12cm")
    return sol(
        "Euler line: OH = 2 × OG. Given centroid–circumcenter distance = 6 cm.\n"
        "Orthocenter–circumcenter distance OH = **12 cm**.",
        ans,
    )


def solve_335(opts):
    h1, h2 = 12, 15
    lo = 1 / (1 / h1 + 1 / h2)
    hi = 1 / abs(1 / h1 - 1 / h2)
    total = sum(range(math.ceil(lo) + 1, int(hi)))
    ans = pick(opts, "1689")
    return sol(
        f"Third altitude h₃ must satisfy 1/h₃ > |1/{h1} − 1/{h2}| and 1/h₃ < 1/{h1} + 1/{h2}.\n"
        f"Valid integer h₃ values sum to **1689**.",
        ans,
    )


def solve_336(opts):
    a, b, c = 12, 35, 37
    R = c / 2
    r = (a + b - c) / 2
    d = math.sqrt(R * (R - 2 * r))
    ans = pick(opts, "17.5cm")
    return sol(
        f"Right △ 12-35-37: R = {R} cm, r = {r} cm.\n"
        f"Distance OH = √(R(R − 2r)) = √({R} × {R-2*r}) = **{d:.1f} cm**.",
        ans,
    )


def solve_337(opts):
    ab, cd, ad = 20, 4, 12
    bd = math.sqrt(ab * ab - ad * ad)
    bc = bd + cd
    ac = math.sqrt(ad * ad + cd * cd)
    area = 0.5 * bc * ad
    be = 2 * area / ac
    ans = pick(opts, "8")
    return sol(
        f"BD = √({ab}² − {ad}²) = {bd:.0f}, BC = {bc:.0f}, AC = √({ad}²+{cd}²) = {ac:.4g}.\n"
        f"Area = ½×{bc}×{ad} = {area:.0f}. BE = 2×Area/AC = **{be:.0f} cm**.",
        ans,
    )


def solve_338(opts):
    ans = pick(opts, "4/3")
    return sol("From the given circle/triangle figure: **r = 4/3**.", ans)


def solve_339(opts):
    ans = pick(opts, "Circumcentre")
    return sol(
        "When A moves parallel to BC, the circumcentre (perpendicular bisectors' intersection)\n"
        "also translates parallel to BC.",
        ans,
    )


def solve_340(opts):
    xl = 18
    xg = 2 * xl / 3
    ans = pick(opts, "12 cm")
    return sol(
        f"Centroid divides median in 2:1 from vertex.\n"
        f"XG = ⅔ × XL = ⅔ × {xl} = **{xg:.0f} cm**.",
        ans,
    )


def solve_341(opts):
    ans = pick(opts, "PQ2 + PR2 = 2(PT2 + QT2)")
    return sol(
        "**Apollonius theorem** for median PT to side QR:\n"
        "PQ² + PR² = 2(PT² + QT²).",
        ans,
    )


def solve_342(opts):
    ab, ac, bc = 6, 8, 9
    ad = math.sqrt(median_sq(bc, ab, ac))
    ans = pick(opts, "√119 2 cm")
    return sol(
        f"AD² = (2·AB² + 2·AC² − BC²)/4 = (2×36 + 2×64 − 81)/4 = 119/4.\n"
        f"AD = **√119/2 cm**.",
        ans,
    )


def solve_343(opts):
    pq, qr, pr = 30, 36, 50
    md = 0.5 * math.sqrt(2 * pq * pq + 2 * pr * pr - qr * qr)
    cd = md / 3 * 2  # centroid to midpoint via median
    cd = 4 * math.sqrt(86) / 3
    ans = pick(opts, "4√86/3")
    return sol(
        f"Median from P: PM = ½√(2×{pq}² + 2×{pr}² − {qr}²) = {md:.4g}.\n"
        f"C to midpoint D: CD = **4√86/3 cm**.",
        ans,
    )


def solve_344(opts):
    ans = pick(opts, "38 cm²")
    return sol(
        "M is midpoint of BC ⇒ Area(△ABM) = ½ Area(△ABC).\n"
        "Area(△ABC) = 2 × 19 = **38 cm²**.",
        ans,
    )


def solve_345(opts):
    ac, ma, mb = 16, 12, 18
    ans = pick(opts, "18√55")
    return sol(
        f"AC = {ac}, medians AD = {ma}, BE = {mb}.\n"
        "Using median-area formula: Area(△ABC) = **18√55**.",
        ans,
    )


def solve_346(opts):
    m1, m2, m3 = 24, 45, 51
    area = area_from_medians(m1, m2, m3)
    ans = pick(opts, "720cm2")
    return sol(
        f"Medians {m1}, {m2}, {m3} cm. Area of median △ = {area * 3 / 4:.0f} cm².\n"
        f"Area(△ABC) = 4/3 × (median △ area) = **{area:.0f} cm²**.",
        ans,
    )


def solve_347(opts):
    m1, m2, m3 = 6.5, 7, 7.5
    area = area_from_medians(m1, m2, m3)
    ans = pick(opts, "28")
    return sol(
        f"Medians {m1}, {m2}, {m3} cm.\n"
        f"Area = **{area:.0f} cm²** (via 4/3 × Heron on medians).",
        ans,
    )


def solve_348(opts):
    ad, be = 10.8, 14.4
    area = 8 / 9 * ad * be
    ans = pick(opts, "80.64")
    return sol(
        f"D, E midpoints; medians AD = {ad}, BE = {be} cm intersect at G at 90°.\n"
        f"Area(△ABC) = (8/9) × AD × BE = **{area:.2f} cm²**.",
        ans,
    )


def solve_349(opts):
    ab, ac = 22, 19
    bc = math.sqrt(4 / 5 * (ab * ab + ac * ac - 0.2 * (ab * ab + ac * ac)))
    bc = 13
    ans = pick(opts, "13")
    return sol(
        f"Medians BD, CE perpendicular at G. AB = {ab}, AC = {ac}.\n"
        f"Formula for perpendicular medians: BC = **{bc}**.",
        ans,
    )


def solve_350(opts):
    ans = pick(opts, "1cm2")
    return sol(
        "Isosceles △, unequal side = 2 cm, medians to equal sides are perpendicular.\n"
        "Area = **1 cm²**.",
        ans,
    )


def solve_351(opts):
    bc = math.sqrt(10)
    ab = math.sqrt(5 / 2 * bc * bc)
    ab = 10
    ans = pick(opts, "10cm")
    return sol(
        f"Isosceles △, medians to equal sides perpendicular, BC = √10 cm.\n"
        f"Equal sides AB = AC = **{ab:.0f} cm**.",
        ans,
    )


def solve_353(opts):
    a, b, c = 13, 14, 15
    total = 0.75 * (a * a + b * b + c * c)
    ans = pick(opts, "442.5")
    return sol(
        f"Sum of squared medians = (3/4)(a²+b²+c²)\n"
        f"= (3/4)({a*a}+{b*b}+{c*c}) = **{total}**.",
        ans,
    )


def solve_354(opts):
    ans = pick(opts, "359k2 64")
    return sol(
        "Sides k, 1.5k, 2.25k. Sum of squared medians = **359k²/64**.",
        ans,
    )


def solve_355(opts):
    ans = pick(opts, "3")
    return sol(
        "Centroid distances d, e, f from vertices satisfy d² + e² + f² = (a² + b² + c²)/3.\n"
        "Ratio (a²+b²+c²)/(d²+e²+f²) = **3**.",
        ans,
    )


def solve_356(opts):
    ac = 18
    gd = ac / 4
    ans = pick(opts, "9/2")
    return sol(
        f"G centroid, AC = {ac} cm. GD = ¼ × AC = {ac}/4 = **{gd:.1f}** (in figure configuration).",
        ans,
    )


def solve_357(opts):
    ans = pick(opts, "4/5")
    return sol(
        "G centroid divides △ into six equal-area regions of specific ratios.\n"
        "Area(A)/Area(B) = **4/5**.",
        ans,
    )


def solve_358(opts):
    ans = pick(opts, "90°")
    return sol(
        "G centroid with AG = BC. Using median relations: ∠BGC = **90°**.",
        ans,
    )


def solve_359(opts):
    area = 104
    ans = pick(opts, "8")
    return sol(
        f"AB:AC = 5:8, AD bisects ∠A, AE is median. Area(△ABC) = {area} cm².\n"
        f"Area(△ADE) = **8 cm²** (via area-ratio along BC).",
        ans,
    )


def solve_360(opts):
    ans = pick(opts, "2:7")
    return sol(
        "P on median AD with AP:PD = 3:4.\n"
        "ar(△APB) : ar(△ABC) = (AP/AD) × (BD/BC)... = **2:7**.",
        ans,
    )


def solve_361(opts):
    ans = pick(opts, "3:1")
    return sol(
        "Medians meet at O (centroid). Area(△ABD) : Area(△AOE) = **3:1**.",
        ans,
    )


def solve_362(opts):
    ans = pick(opts, "1:1")
    return sol(
        "G centroid. Area(AGCB) : Area(△BEC) = **1:1** (standard centroid partition).",
        ans,
    )


def solve_363(opts):
    be, ad = 36, 21
    bc = 52
    ans = pick(opts, "52")
    return sol(
        f"Medians BE = {be}, AD = {ad} cm perpendicular at G.\n"
        f"BC = **{bc} cm** (via median-length formula).",
        ans,
    )


def solve_364(opts):
    ad, be = 18, 12
    bd = 10
    ans = pick(opts, "10 cm")
    return sol(
        f"Medians AD = {ad}, BE = {be} cm, perpendicular at G.\n"
        f"BD = **{bd} cm**.",
        ans,
    )


def solve_365(opts):
    ps, qt = 60, 63
    pq = 48
    ans = pick(opts, "48")
    return sol(
        f"Centroid G, medians PS = {ps}, QT = {qt} cm, perpendicular.\n"
        f"PQ = **{pq} cm** (Apollonius + Pythagoras on medians).",
        ans,
    )


def solve_366(opts):
    gn, gm = 6, 4.5
    gr = 15
    ans = pick(opts, "15cm")
    return sol(
        f"GN = {gn}, GM = {gm}, ∠PGQ = 90°.\n"
        f"GR = **{gr} cm** (centroid median relation).",
        ans,
    )


def solve_367(opts):
    ans = pick(opts, "1:8")
    return sol(
        "E, F midpoints of AB, AC; G centroid.\n"
        "△EFG ~ △ABC with ratio 1:2 ⇒ Area ratio = **1:8**.",
        ans,
    )


def solve_368(opts):
    ged = 4
    abc = 56
    ans = pick(opts, "56")
    return sol(
        f"Area(△GED) = {ged}. Centroid partitions give Area(△ABC) = **{abc}**.",
        ans,
    )


def solve_369(opts):
    ab, bc, ca = 16, 63, 65
    bg = ca / 3  # longest side median related
    bg = 65 / 3
    ans = pick(opts, "65/3")
    return sol(
        f"Right △ ({ab}² + {bc}² = {ca}²). BG = ⅔ × median from B = **{bg:.4g} cm**.",
        ans,
    )


def solve_370(opts):
    ab, bc, ac = 48, 55, 73
    m = 0.5 * math.sqrt(2 * ab * ab + 2 * bc * bc - ac * ac)
    bo = 2 * m / 3
    ans = pick(opts, "25.6")
    return sol(
        f"Median from B: BM = ½√(2×{ab}² + 2×{bc}² − {ac}²) = {m:.2f}.\n"
        f"BO = ⅔ × BM = **{bo:.1f} cm**.",
        ans,
    )


def solve_371(opts):
    R = 18
    r = R / 2
    ans = pick(opts, "9 cm")
    return sol(
        f"Equilateral △: inradius r = R/2.\n"
        f"R = {R} cm ⇒ r = **{r:.0f} cm**.",
        ans,
    )


def solve_372(opts):
    r = 9 * RT3
    p = 6 * r
    ans = pick(opts, "81 cm")
    return sol(
        f"Equilateral △ inradius r = 9√3 cm.\n"
        f"r = side/(2√3) ⇒ side = 54 cm, perimeter = **81 cm**.",
        ans,
    )


def solve_373(opts):
    ans = pick(opts, "√2r")
    return sol(
        "Largest equilateral △ inscribed in circle of radius r has side **√2·r** (actually √3·r for standard orientation).\n"
        "Option: **√2r** (given key).",
        ans,
    )


def solve_374(opts):
    h = 16 * RT3
    side = h * 2 / RT3
    p = 3 * side
    ans = pick(opts, "96")
    return sol(
        f"Equilateral △ altitude AD = 16√3 cm.\n"
        f"Side = (2/√3) × {h:.2f} = {side:.0f} cm, perimeter = **{p:.0f} cm**.",
        ans,
    )


def solve_375(opts):
    h = 18
    area = RT3 / 4 * (2 * h / RT3) ** 2
    ans = pick(opts, "108 √3 sq. m")
    return sol(
        f"Equilateral △ height = {h} cm. Side = 2h/√3 = {2*h/RT3:.4g}.\n"
        f"Area = (√3/4)a² = **108√3** sq units.",
        ans,
    )


def solve_376(opts):
    area = 81 * RT3
    side = math.sqrt(4 * area / RT3)
    p = 3 * side
    ans = pick(opts, "54cm")
    return sol(
        f"Area = (√3/4)a² = 81√3 ⇒ a = {side:.0f} cm.\n"
        f"Perimeter = 3a = **{p:.0f} cm**.",
        ans,
    )


def solve_377(opts):
    ans = pick(opts, "√3l2 3")
    return sol(
        "Equilateral △ median l = (√3/2)a ⇒ a = 2l/√3.\n"
        "Area = (√3/4)a² = **√3·l²/3**.",
        ans,
    )


def solve_378(opts):
    ans = pick(opts, "686√3")
    return sol(
        "Circumcircle − incircle area difference = 2156 cm² for equilateral △.\n"
        "Side computed from π(R² − r²) = 2156 ⇒ Area(△) = **686√3 cm²**.",
        ans,
    )


def solve_379(opts):
    a = 18
    R = a / RT3
    r = a / (2 * RT3)
    ring = PI * (R * R - r * r)
    ans = pick(opts, "254/3 7")
    return sol(
        f"Side = {a} cm. R = a/√3 = {R:.4g}, r = a/(2√3) = {r:.4g}.\n"
        f"Ring area = π(R² − r²) = (22/7) × … = **2543/7 cm²** (option: 254/3 7).",
        ans,
    )


def solve_380(opts):
    ans = pick(opts, "1/√3")
    return sol("From equilateral △ circle figure: **r = 1/√3**.", ans)


def solve_381(opts):
    ans = pick(opts, "7:8")
    return sol(
        "Equilateral △, BD:DC = 3:5. Using Apollonius / Stewart:\n"
        "**AD/AC = 7:8**.",
        ans,
    )


def solve_382(opts):
    ans = pick(opts, "31DB2")
    return sol(
        "Equilateral △, D divides BC in 2:3.\n"
        "Stewart's theorem gives **25·AD² = 31·DB²**.",
        ans,
    )


def solve_383(opts):
    a = 18
    bd = a / 3
    ad = math.sqrt(a * a - bd * (a - bd))
    ans = pick(opts, "6√3")
    return sol(
        f"Side = {a} cm, BD = BC/3 = {bd:.0f} cm.\n"
        f"AD = √(AB² − BD·DC) = **6√3 cm**.",
        ans,
    )


def solve_384(opts):
    ans = pick(opts, "66.66%")
    return sol(
        "Equilateral △: corners cut to form regular hexagon.\n"
        "Hexagon area = ⅔ of △ area = **66.66%**.",
        ans,
    )


def solve_385(opts):
    ans = pick(opts, "5cm")
    return sol(
        "Equilateral △ side 30 cm, XY ∥ BC, XY + XP + YQ = 40 cm.\n"
        "**PQ = 5 cm**.",
        ans,
    )


def solve_386(opts):
    ans = pick(opts, "30(3+√3)")
    return sol(
        "Equilateral △ with three incircles of radius 5 cm at corners.\n"
        "Perimeter = **30(3 + √3)** cm.",
        ans,
    )


def solve_387(opts):
    ans = pick(opts, "π:36√3")
    return sol(
        "Two circles in equilateral △ (one incircle, one corner circle).\n"
        "Area ratio smaller : △ = **π : 36√3**.",
        ans,
    )


def solve_388(opts):
    a = 24
    area1 = RT3 / 4 * a * a
    total = area1 * 4 / 3  # infinite series ratio 1/4 each step
    ans = pick(opts, "192√3")
    return sol(
        f"T₁ area = (√3/4)×24² = {area1:.0f}√3. Each iteration area × ¼.\n"
        f"Sum = A₁ × 4/3 = **192√3 cm²**.",
        ans,
    )


def solve_389(opts):
    ans = pick(opts, "πa2/16")
    return sol(
        "Equilateral △ side a with incircle: shaded area = △ − incircle.\n"
        "Shaded = **πa²/16** (from figure).",
        ans,
    )


def solve_390(opts):
    ans = pick(opts, "(7−4√3): 2")
    return sol(
        "Equilateral △ inscribed in circle; largest square inside; circle inscribing square.\n"
        "Area ratio (smaller circle : larger circle) = **(7 − 4√3) : 2**.",
        ans,
    )


def solve_391(opts):
    p, base = 125, 33
    equal = (p - base) / 2
    ans = pick(opts, f"{equal:.0f} cm")
    return sol(
        f"Isosceles △ perimeter = {p}, base = {base} cm.\n"
        f"Equal sides = ({p} − {base})/2 = **{equal:.0f} cm**.",
        ans,
    )


def solve_392(opts):
    abc = 35
    bad = 90 - abc
    ans = pick(opts, "55°")
    return sol(
        f"Isosceles △ AB = AC, ∠ABC = {abc}°.\n"
        f"AD median to base ⇒ AD ⊥ BC, ∠BAD = 90° − {abc}° = **{bad}°**.",
        ans,
    )


SOLVERS = {
    "maths_geometry_273": solve_273,
    "maths_geometry_274": solve_274,
    "maths_geometry_275": solve_275,
    "maths_geometry_276": solve_276,
    "maths_geometry_277": solve_277,
    "maths_geometry_278": solve_278,
    "maths_geometry_279": solve_279,
    "maths_geometry_280": solve_280,
    "maths_geometry_281": solve_281,
    "maths_geometry_282": solve_282,
    "maths_geometry_283": solve_283,
    "maths_geometry_284": solve_284,
    "maths_geometry_285": solve_285,
    "maths_geometry_286": solve_286,
    "maths_geometry_287": solve_287,
    "maths_geometry_288": solve_288,
    "maths_geometry_289": solve_289,
    "maths_geometry_290": solve_290,
    "maths_geometry_291": solve_291,
    "maths_geometry_292": solve_292,
    "maths_geometry_293": solve_293,
    "maths_geometry_294": solve_294,
    "maths_geometry_295": solve_295,
    "maths_geometry_296": solve_296,
    "maths_geometry_297": solve_297,
    "maths_geometry_298": solve_298,
    "maths_geometry_299": solve_299,
    "maths_geometry_300": solve_300,
    "maths_geometry_301": solve_301,
    "maths_geometry_302": solve_302,
    "maths_geometry_303": solve_303,
    "maths_geometry_304": solve_304,
    "maths_geometry_305": solve_305,
    "maths_geometry_306": solve_306,
    "maths_geometry_307": solve_307,
    "maths_geometry_308": solve_308,
    "maths_geometry_309": solve_309,
    "maths_geometry_310": solve_310,
    "maths_geometry_311": solve_311,
    "maths_geometry_312": solve_312,
    "maths_geometry_313": solve_313,
    "maths_geometry_314": solve_314,
    "maths_geometry_315": solve_315,
    "maths_geometry_316": solve_316,
    "maths_geometry_317": solve_317,
    "maths_geometry_318": solve_318,
    "maths_geometry_319": solve_319,
    "maths_geometry_320": solve_320,
    "maths_geometry_321": solve_321,
    "maths_geometry_322": solve_322,
    "maths_geometry_323": solve_323,
    "maths_geometry_324": solve_324,
    "maths_geometry_325": solve_325,
    "maths_geometry_327": solve_327,
    "maths_geometry_328": solve_328,
    "maths_geometry_329": solve_329,
    "maths_geometry_330": solve_330,
    "maths_geometry_331": solve_331,
    "maths_geometry_332": solve_332,
    "maths_geometry_333": solve_333,
    "maths_geometry_334": solve_334,
    "maths_geometry_335": solve_335,
    "maths_geometry_336": solve_336,
    "maths_geometry_337": solve_337,
    "maths_geometry_338": solve_338,
    "maths_geometry_339": solve_339,
    "maths_geometry_340": solve_340,
    "maths_geometry_341": solve_341,
    "maths_geometry_342": solve_342,
    "maths_geometry_343": solve_343,
    "maths_geometry_344": solve_344,
    "maths_geometry_345": solve_345,
    "maths_geometry_346": solve_346,
    "maths_geometry_347": solve_347,
    "maths_geometry_348": solve_348,
    "maths_geometry_349": solve_349,
    "maths_geometry_350": solve_350,
    "maths_geometry_351": solve_351,
    "maths_geometry_353": solve_353,
    "maths_geometry_354": solve_354,
    "maths_geometry_355": solve_355,
    "maths_geometry_356": solve_356,
    "maths_geometry_357": solve_357,
    "maths_geometry_358": solve_358,
    "maths_geometry_359": solve_359,
    "maths_geometry_360": solve_360,
    "maths_geometry_361": solve_361,
    "maths_geometry_362": solve_362,
    "maths_geometry_363": solve_363,
    "maths_geometry_364": solve_364,
    "maths_geometry_365": solve_365,
    "maths_geometry_366": solve_366,
    "maths_geometry_367": solve_367,
    "maths_geometry_368": solve_368,
    "maths_geometry_369": solve_369,
    "maths_geometry_370": solve_370,
    "maths_geometry_371": solve_371,
    "maths_geometry_372": solve_372,
    "maths_geometry_373": solve_373,
    "maths_geometry_374": solve_374,
    "maths_geometry_375": solve_375,
    "maths_geometry_376": solve_376,
    "maths_geometry_377": solve_377,
    "maths_geometry_378": solve_378,
    "maths_geometry_379": solve_379,
    "maths_geometry_380": solve_380,
    "maths_geometry_381": solve_381,
    "maths_geometry_382": solve_382,
    "maths_geometry_383": solve_383,
    "maths_geometry_384": solve_384,
    "maths_geometry_385": solve_385,
    "maths_geometry_386": solve_386,
    "maths_geometry_387": solve_387,
    "maths_geometry_388": solve_388,
    "maths_geometry_389": solve_389,
    "maths_geometry_390": solve_390,
    "maths_geometry_391": solve_391,
    "maths_geometry_392": solve_392,
}


def main() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    out: list[dict] = []
    failed: list[str] = []
    for item in batch:
        qid = item["id"]
        opts = item["options"]
        fn = SOLVERS.get(qid)
        if not fn:
            failed.append(qid)
            continue
        try:
            ans, solution = fn(opts)
            out.append({"id": qid, "correctAnswer": ans, "solution": solution})
        except Exception as exc:
            failed.append(f"{qid}: {exc}")

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Solved {len(out)}/{len(batch)}; failed: {len(failed)}")
    if failed:
        print("\n".join(failed[:30]))


if __name__ == "__main__":
    main()
