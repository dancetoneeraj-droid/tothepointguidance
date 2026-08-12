"""Independent numeric re-check of the Sheet 4-6 mensuration answers.

Every value below is recomputed from the question's own data with mpmath and then
compared against the correctAnswer string stored in data/maths/mensuration-3d.json.
Answers that are ratios, pairs or purely symbolic are not machine-checkable and
are left out.
"""

import json
import re
from pathlib import Path

from mpmath import mp, mpf, pi, sqrt, cbrt, floor

mp.dps = 40

ROOT = Path(__file__).resolve().parent.parent
BANK = json.loads((ROOT / "data" / "maths" / "mensuration-3d.json").read_text(encoding="utf-8"))
BY_ID = {q["id"]: q for q in BANK}

SHEET_START = {4: 189, 5: 249, 6: 267}
P22 = mpf(22) / 7

UNITS = [
    "cubic cm", "sq cm", "sq mm", "cm³", "cm²", "cm3", "cm2", "m³", "m²",
    "minutes", "litres", " cm", " mm", " m", " L", " kg", "₹", "Rs", "%", ",",
]


def parse_answer(text):
    s = text.strip()
    for unit in UNITS:
        s = s.replace(unit, "")
    s = s.replace("−", "-").replace("(", "").replace(")", "").strip()
    s = re.sub(r"[A-Za-z]+$", "", s).strip()
    if "+" in s:
        return sum(parse_term(part) for part in s.split("+"))
    return parse_term(s)


def parse_term(s):
    s = s.strip()
    factor = mpf(1)
    if "×10⁶" in s.replace(" ", ""):
        s = s.replace(" ", "").replace("×10⁶", "")
        factor *= mpf(10) ** 6
    if "π" in s:
        s = s.replace("π", "").strip()
        factor *= pi
        if not s:
            return factor

    m = re.fullmatch(r"(-?[\d.]*)∛\s*([\d./]+)", s)
    if m:
        coeff = mpf(m.group(1)) if m.group(1) not in ("", "-") else mpf(m.group(1) + "1")
        return factor * coeff * cbrt(_ratio(m.group(2)))

    m = re.fullmatch(r"(-?[\d.]*)√\s*([\d./]+)\s*(?:/\s*(\d+))?", s)
    if m:
        coeff = mpf(m.group(1)) if m.group(1) not in ("", "-") else mpf(m.group(1) + "1")
        value = factor * coeff * sqrt(_ratio(m.group(2)))
        return value / int(m.group(3)) if m.group(3) else value

    m = re.fullmatch(r"(-?\d+)\s+(\d+)/(\d+)", s)  # mixed number "26 1/3"
    if m:
        a, b, c = (int(g) for g in m.groups())
        return factor * (mpf(a) + mpf(b) / c)

    return factor * _ratio(s)


def _ratio(s):
    if "/" in s:
        num, den = s.split("/")
        return mpf(num) / mpf(den)
    return mpf(s)


CHECKS = []


def check(sheet, number, value, tol=mpf("1e-15")):
    """tol is a relative tolerance, loosened only where the sheet rounds its option."""
    CHECKS.append((f"maths_mensuration_3d_{SHEET_START[sheet] + number - 1}", value, tol))


def heron(a, b, c):
    s = mpf(a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))


# ---- Sheet-4: sphere and hemisphere --------------------------------------
check(4, 3, 4 * P22 * 112**2)
check(4, 4, 2 * sqrt(mpf(9856) * 7 / 88) / 100)
check(4, 5, mpf(18480) / (4 * P22 * 49))
check(4, 6, (mpf(4) / 3) * P22 * mpf("7.35") ** 3)
check(4, 7, floor((mpf(2) / 3) * mpf("3.14") * mpf("5.5") ** 3 + mpf("0.5")))
check(4, 8, (mpf(4) / 3) * pi * 65**3, tol=mpf("1e-3"))
check(4, 9, cbrt(mpf(38808) * 21 / 88))
check(4, 10, 4 * P22 * cbrt(mpf(4851) * 21 / 88) ** 2)
check(4, 11, (mpf(4) / 3) * P22 * sqrt(mpf(2464) * 7 / 88) ** 3, tol=mpf("1e-6"))
check(4, 12, sqrt((mpf(9240) / mpf("2.40")) * 7 / 88))
check(4, 13, (mpf(704) * 7 / 88 - 4) / 4)
check(4, 14, cbrt(mpf(1**3 + 6**3 + 8**3)))
check(4, 15, 4 * pi * cbrt(mpf(3) ** 3 - 2**3 - mpf("1.5") ** 3) ** 2)
check(4, 16, (1000 - mpf(880) * 21 / 88) / 30)
check(4, 17, floor((mpf(4) / 3) * mpf("3.14") * 8**3 / 24 + mpf("0.5")))
check(4, 18, (mpf(4) / 3) * P22 * mpf("2.8") ** 3, tol=mpf("2e-4"))
check(4, 19, 4 * P22 * (mpf(42) / 2) ** 2)
check(4, 20, 6 * (2 * 15 * sqrt(3) / sqrt(3)) ** 2)
check(4, 21, sqrt(mpf(8**2 + 12**2 + 24**2)) / 2)
check(4, 23, (mpf(20) / mpf("0.5")) ** 3)
check(4, 24, (8000 * (mpf(35) / 20) ** 2 / mpf(35) ** 2 - 1) * 100)
check(4, 25, 4 * pi * (mpf(7) / cbrt(mpf(2744))) ** 2)
check(4, 26, ((mpf(4) / 3) * mpf("1.5") ** 3) / mpf("0.4") ** 2)
check(4, 27, floor((mpf(4) / 3) * mpf("8.4") ** 3 / 144 * 10 + mpf("0.5")) / 10)
check(4, 28, 5 - sqrt(25 - (mpf(4) / 3) * 27 / 4))
check(4, 29, 2 * cbrt((mpf(1) / 4) * mpf("2.8") ** 2 * (mpf("5.2") + 6)))
check(4, 30, mpf(14) ** 2 * mpf("15.75") / ((mpf(4) / 3) * mpf("2.1") ** 3))
check(4, 31, (mpf(4) / 3) * P22 * 8**3, tol=mpf("1e-5"))
check(4, 32, (mpf("3.5") ** 2 * 7 - (mpf(4) / 3) * mpf("3.5") ** 3) / mpf("3.5") ** 2)
check(4, 33, 4 * pi * cbrt(3 * (mpf("4.3") ** 2 - mpf("1.1") ** 2) * (mpf(50) / 3) / 4) ** 2)
check(4, 34, floor(4 * mpf(6**3 - 5**3) / mpf("5.2") ** 2 * 10 + mpf("0.5")) / 10)
check(4, 35, (mpf(4) / 3) * P22 * mpf(11**3 - 9**3) * 36 / 1000)
check(4, 36, 6 - cbrt(216 - (mpf(6688) / mpf("10.5")) * 21 / 88), tol=mpf("1e-9"))
check(4, 37, mpf(40) * (8**3 - 6**3) / 4**3)
check(4, 38, (mpf(2) / 3) * mpf("166.32"))
check(4, 39, 3 * mpf("3.14") * 27**2)
check(4, 40, (4 * P22 * mpf("7.7") ** 2 / 7) * 17)
check(4, 41, (mpf(2) / 3) * P22 * mpf("31.5") ** 3)
check(4, 42, cbrt(mpf("2425.5") * 21 / 44))
check(4, 43, (mpf(2) / 3) * P22 * mpf("10.5") ** 3 * 1000)
check(4, 44, 3 * P22 * cbrt(mpf(19404) * 21 / 44) ** 2)
check(4, 45, (mpf(2) / 3) * P22 * sqrt(mpf("1039.5") * 7 / 66) ** 3)
_r46 = cbrt((mpf(2) / 3) * 21**3 / 14)  # cylinder radius from equal volumes
_v46 = int((mpf(2) / 3) * 21**3)  # volume coefficient of pi
_primes = [2, 3, 5, 7, 11, 13]
_abc = next(
    (a, b, c)
    for a in _primes
    for b in _primes
    for c in _primes
    if a * b**a * c**b == _v46
)
check(4, 46, mpf((_abc[0] + _abc[1]) * _abc[2]))
check(4, 47, cbrt(mpf("0.8") * 20 * 3**3))
check(4, 49, (mpf(2) / 3) * ((mpf(2) / 3) * P22 * mpf("10.5") ** 3 * 1000) / mpf("7.7") / 3600)
check(4, 50, (mpf(2) / 3) * pi * (5**3 - 4**3))
check(4, 51, 2 * pi * 49 + 2 * pi * 36 + pi * (49 - 36))
check(4, 53, (2 * P22 * 16**2 + 2 * P22 * 14**2 + P22 * (16**2 - 14**2)) * mpf("2.5"), tol=mpf("1e-5"))
check(4, 54, cbrt(mpf(20) ** 3 + 3 * ((mpf(1) / 3) * 49 * 18) / 2))
check(4, 55, pi * 36 * sqrt(mpf(36**2 + 105**2)) + 2 * pi * 36**2)
check(
    4,
    56,
    P22 * ((mpf(2) / 3) * mpf("4.2") ** 3 + mpf("4.2") ** 2 * 7 + (mpf(1) / 3) * mpf("4.2") ** 2 * 7),
)
check(4, 57, floor(mpf(49 * 21) / (mpf("2.1") ** 2 * mpf("1.4") + (mpf(2) / 3) * mpf("2.1") ** 3)))
check(4, 58, (mpf(2816) / P22 - (mpf(2) / 3) * 8**3) * 3 / 64 + 8)
check(4, 59, floor((2 * P22 * 3 * 9 + 4 * P22 * 9) + mpf("0.5")))

# ---- Sheet-5: prism -------------------------------------------------------
check(5, 1, sqrt(mpf(7200) / ((3 * sqrt(3) / 2) * 100 * sqrt(3))))
check(5, 2, heron(13, 20, 21) * 9)
check(5, 3, 2 * heron(4, 13, 15) + (4 + 13 + 15) * (mpf(480) / heron(4, 13, 15)))
check(5, 4, 2 * (4 * mpf(45)) + 90 * (mpf(1200) / (4 * mpf(45))))
check(5, 6, (20 + 21 + 29) * (mpf(7560) / heron(20, 21, 29)))
check(5, 7, 2 * (sqrt(3) / 4) * 100 + 3 * 10 * 10 * sqrt(3))
check(5, 8, (sqrt(3) / 4) * 16 * (mpf(120) / 12))
_a9 = (-18 + sqrt(18**2 + 4 * (sqrt(3) / 2) * 162 * sqrt(3))) / (2 * (sqrt(3) / 2))
check(5, 9, (sqrt(3) / 4) * _a9**2 * 6)
check(5, 10, (mpf("151.20") / mpf("0.20") - 2 * 54) / (9 + 12 + 15))
check(5, 11, mpf(160) / 40)
check(5, 12, 2 * (mpf(160) / 10) + 4 * sqrt(mpf(160) / 10) * 10)
check(5, 13, 2 * 15**2 + 4 * 15 * 8)
_a14 = (-30 + sqrt(900 + 4 * 304)) / 2
check(5, 14, _a14**2 * 15)
check(5, 15, 2 * 64 + 4 * 8 * 80 + 9 * 2 * 64)
_x16 = (-10 + sqrt(100 + 96)) / 2
check(5, 16, 3 * _x16 * 2 * _x16 * 12)
check(5, 17, mpf("1731.6") / ((mpf(1) / 2) * (11 + 15) * 9))
check(5, 18, (9 + 14 + 13 + 12) * (mpf(2070) / ((mpf(1) / 2) * 9 * 12 + heron(13, 14, 15))))

# ---- Sheet-6: pyramid and tetrahedron -------------------------------------
check(6, 2, mpf(45) * sqrt(3) * 3 / ((sqrt(3) / 4) * 36))
check(6, 3, (mpf(1) / 3) * (sqrt(3) / 4) * 64 * 30 * sqrt(3))
_h4 = sqrt(mpf(8**2) / 8)  # 9h^2 = h^2 + inradius^2 with inradius 8
check(6, 4, (mpf(1) / 3) * (sqrt(3) / 4) * (16 * sqrt(3)) ** 2 * _h4)
_l5 = (270 * sqrt(3) - (sqrt(3) / 4) * (10 * sqrt(3)) ** 2) / ((mpf(1) / 2) * 3 * 10 * sqrt(3))
check(6, 5, sqrt(_l5**2 - (10 * sqrt(3) / (2 * sqrt(3))) ** 2))
check(6, 6, sqrt(30**2 - (mpf(20) / sqrt(3)) ** 2))
check(6, 7, (sqrt(3) / 4) * 64 + 3 * (mpf(1) / 2) * 8 * sqrt(mpf(24**2 - 4**2)))
check(6, 8, sqrt((mpf(30) * 2 / 8) ** 2 - (mpf(8) / (2 * sqrt(3))) ** 2))
check(6, 10, (mpf(1) / 3) * (mpf(1152) / 2) * 6)
check(6, 11, 64 + (mpf(1) / 2) * 32 * sqrt(mpf(3**2 + 4**2)))
_a12 = mpf(20) / sqrt(2)
check(6, 12, (mpf(1) / 2) * 4 * _a12 * sqrt(20**2 + (_a12 / 2) ** 2))
_h13 = 3 * mpf(1296) / 324
check(6, 13, (mpf(1) / 2) * 4 * 18 * sqrt(_h13**2 + 9**2))
_a14sq = 3 * mpf(200) / 13
check(6, 14, floor(sqrt(13**2 + _a14sq / 2) + mpf("0.5")))
_v16 = (mpf(1) / 3) * 144 * 21
check(6, 16, _v16 * (mpf(19) / 27 - mpf(1) / 27))
_s17 = 8 * sqrt(3)
check(
    6,
    17,
    (3 * sqrt(3) / 2) * _s17**2 + (mpf(1) / 2) * 6 * _s17 * sqrt(16**2 + ((sqrt(3) / 2) * _s17) ** 2),
)
_a19 = 4 * sqrt(2) / sqrt(mpf(2) / 3)
check(6, 19, sqrt(3) * _a19**2)
check(6, 20, (3 * sqrt(2)) ** 3 / (6 * sqrt(2)))
check(6, 21, sqrt(3) * cbrt(18 * sqrt(2) * 6 * sqrt(2)) ** 2)

fails = 0
for qid, got, tol in CHECKS:
    stored = BY_ID[qid]["correctAnswer"]
    want = parse_answer(stored)
    if abs(got - want) > tol * abs(want):
        fails += 1
        print(f"MISMATCH {qid}: computed {got} vs stored {stored!r} ({want})")

print(f"{len(CHECKS)} numeric checks against stored answers, {fails} mismatches")
