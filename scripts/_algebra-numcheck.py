"""Independent numeric re-check of the arithmetic-heavy algebra answers.

For each entry the target is recomputed from the question's own hypothesis with
mpmath (complex arithmetic where the constraint has no real solution) and then
compared against the correctAnswer string stored in data/maths/algebra.json.
"""

import json
import re
from pathlib import Path

from mpmath import mp, mpc, mpf, sqrt, power, findroot

mp.dps = 40

ROOT = Path(__file__).resolve().parent.parent
BANK = json.loads((ROOT / "data" / "maths" / "algebra.json").read_text(encoding="utf-8"))

# id = start_index + 1 + position, where position is 1-based within the sheet's list
SHEET_START = {2: 188, 3: 215, 4: 343}


def qid(sheet, pos):
    return f"maths_algebra_{SHEET_START[sheet] + pos - 1}"


def parse_answer(text):
    """Parse the answer strings used in these banks into (value, sign_agnostic)."""
    s = text.strip().replace("−", "-").replace("×", "*")
    either = s.startswith("±")
    if either:
        s = s[1:].strip()
    return _parse_magnitude(s), either


def _parse_magnitude(s):
    m = re.fullmatch(r"(-?[\d.]*)\s*/\s*√\s*(\d+)", s)  # "2/√5"
    if m:
        coeff = mpf(m.group(1)) if m.group(1) not in ("", "-") else mpf(m.group(1) + "1")
        return coeff / sqrt(int(m.group(2)))
    m = re.fullmatch(r"(-?\d+)\s+(\d+)/(\d+)", s)  # mixed number "4 6/125"
    if m:
        a, b, c = (int(g) for g in m.groups())
        return mpf(a) + mpf(b) / c
    m = re.fullmatch(r"(-?[\d.]*)\s*√\s*(\d+)\s*/\s*(\d+)", s)  # "3√5/2"
    if m:
        coeff = mpf(m.group(1)) if m.group(1) not in ("", "-") else mpf(m.group(1) + "1")
        return coeff * sqrt(int(m.group(2))) / int(m.group(3))
    m = re.fullmatch(r"(-?[\d.]*)\s*√\s*(\d+)", s)  # "24√2", "√85"
    if m:
        coeff = mpf(m.group(1)) if m.group(1) not in ("", "-") else mpf(m.group(1) + "1")
        return coeff * sqrt(int(m.group(2)))
    m = re.fullmatch(r"(-?\d+)/(\d+)", s)  # "2431/7"
    if m:
        return mpf(int(m.group(1))) / int(m.group(2))
    return mpf(s)


def root_of_sum(s):
    """x with x + 1/x = s (complex branch when |s| < 2)."""
    return (mpc(s) + sqrt(mpc(s) ** 2 - 4)) / 2


def root_of_diff(d):
    """x with x - 1/x = d."""
    return (mpc(d) + sqrt(mpc(d) ** 2 + 4)) / 2


pw = power
CHECKS = []


def check(sheet, pos, value):
    CHECKS.append((qid(sheet, pos), value))


# ---- Sheet-2 -------------------------------------------------------------
check(2, 20, sum(1 / (mpf(10) ** n + 1) for n in range(-9, 10)))
x = root_of_sum(112)
check(2, 21, pw(x - 112, 15) + pw(1 / x, 15))

# ---- Sheet-3 -------------------------------------------------------------
u = (6 - sqrt(21)) / (6 + sqrt(21))
check(3, 3, u + 1 / u)
a = root_of_sum(sqrt(2))
check(3, 23, pw(a, 17) + 1 / pw(a, 25))
x = root_of_diff(mpf("0.4"))
check(3, 35, x**2 + 1 / x**2)
x = root_of_sum(9)
check(3, 42, pw(x, 4) + 1 / pw(x, 4))
x = root_of_sum(-13)
check(3, 43, pw(x, 4) + 1 / pw(x, 4))
x = root_of_sum(2 * sqrt(3)) ** 2
check(3, 44, pw(x, 4) + 1 / pw(x, 4))
x = root_of_sum(sqrt(40))  # x^2 + 1/x^2 = 38
check(3, 65, 6 * x * (x - 1) / (x**3 - x**2 - x + 1))
x = root_of_sum(11) ** 2  # sqrt(x) + 1/sqrt(x) = 11
A = x * sqrt(x)
check(3, 89, A * (A - 1298) + 11)
x = root_of_sum(mpf(11) / 5)
check(3, 84, pw(x, 3) + 1 / pw(x, 3))
x = root_of_sum(17)
check(3, 101, (pw(x, 4) + 1 / x**2) / (x**2 - 3 * x + 1))
x = root_of_diff(3)
check(3, 121, (2 * x**4 + 3 * x**3 + 13 * x**2 - 3 * x + 2) / (3 * x**4 + 3))
x = (4 + sqrt(28)) / 2  # x^2 - 4x - 3 = 0
check(3, 122, (x**4 - 27 / x**2) / (x**2 + 4 * x - 3))
x = (3 + sqrt(13)) / 2  # x^2 - 3x - 1 = 0
check(3, 123, (x**2 + 8 * x - 1) / (x**3 + 1 / x))
x = root_of_sum(4)
check(3, 125, (pw(x, 3) - 26) ** 2)
x = root_of_sum(5 * sqrt(5))
check(3, 115, pw(x, 3) - 1 / pw(x, 3))

# ---- Sheet-4 (positions skip the two non-MCQ items, sheet Q15 and Q35) ----
def s4(n):
    """sheet question number -> position in the imported list."""
    return n - (1 if n > 15 else 0) - (1 if n > 35 else 0)


x = root_of_sum(sqrt(8));            check(4, s4(1), pw(x, 4) - 1 / pw(x, 4))
x = root_of_diff(sqrt(6));           check(4, s4(2), pw(x, 8) - 1 / pw(x, 8))
x = root_of_sum(2 * sqrt(5));        check(4, s4(3), pw(x, 5) + 1 / pw(x, 5))
x = root_of_sum(4);                  check(4, s4(4), pw(x, 5) + 1 / pw(x, 5))
x = root_of_diff(-6);                check(4, s4(5), pw(x, 5) - 1 / pw(x, 5))
y = root_of_diff(3);                 check(4, s4(6), pw(y, 5) - 1 / pw(y, 5))
x = root_of_sum(4);                  check(4, s4(7), pw(x, 6) + 1 / pw(x, 6))
x = root_of_sum(7);                  check(4, s4(8), pw(x, 6) + 1 / pw(x, 6))
a = root_of_sum(7 * sqrt(3));        check(4, s4(9), pw(a, 6) + 1 / pw(a, 6))
x = root_of_diff(4);                 check(4, s4(10), pw(x, 6) + 1 / pw(x, 6))
x = root_of_sum(5 * sqrt(2));        check(4, s4(11), pw(x, 6) - 1 / pw(x, 6))
x = root_of_sum(7);                  check(4, s4(12), pw(x, 7) + 1 / pw(x, 7))
u = root_of_diff(sqrt(7));           check(4, s4(13), pw(u, 7) - 1 / pw(u, 7))
x = root_of_sum(4);                  check(4, s4(14), pw(x, 7) - 1 / pw(x, 7))
x = root_of_sum(3);                  check(4, s4(18), pw(x, 9) + pw(x, 7) + 1 / pw(x, 9) + 1 / pw(x, 7))
x = root_of_sum(4);                  check(4, s4(19), pw(x, 9) + pw(x, 7) - 194 * pw(x, 5) - 194 * pw(x, 3))
x = root_of_sum(3);                  check(4, s4(20), pw(x, 12) + pw(x, 8) - 123 * pw(x, 7) - 123 * pw(x, 3))
x = root_of_diff(1)
check(4, s4(23), 1 / (x - 1) - 1 / (x + 1) + 1 / (x**2 + 1) - 1 / (x**2 - 1))
t = root_of_sum(5);                  check(4, s4(24), pw(t, 5) + 1 / pw(t, 5))
x = root_of_sum(4);                  check(4, s4(25), pw(x, 10) + 1 / pw(x, 10))
u = root_of_sum(1)
check(4, s4(41), pw(u, 36) + pw(u, 33) + pw(u, 29) + pw(u, 26) - 2 * pw(u, 21)
      + pw(u, 16) + pw(u, 14) - pw(u, 3) + 3)
y = root_of_sum(1);                  check(4, s4(43), pw(y, 8) + 1 / pw(y, 8))
y = root_of_sum(1);                  check(4, s4(45), pw(y, 22) + 1 / pw(y, 22))
y = 3 + sqrt(3);                     check(4, s4(72), 2 * y**4 - 8 * y**3 - 6 * y**2 + 28 * y - 84)
a = findroot(lambda t: t**3 + 4 * t**2 + 16 * t - 1, mpf("0.06"))
check(4, s4(73), a**3 + 4 / a)
a = findroot(lambda t: t**3 + 5 * t**2 + 25 * t + 2, mpf("-0.08"))
check(4, s4(74), a**3 - 10 / a)
x = (-5 + sqrt(37)) / 2;             check(4, s4(79), 2 * x**2 + 10 * x + 7)
x = findroot(lambda t: t**3 - 6 * t**2 + 35 - 8 * (t - 2), mpf("7.5"))
check(4, s4(80), x**2 + 3 / (x - 6))
u = root_of_sum(3)
check(4, s4(86), sqrt((pw(u, 6) - 1 / pw(u, 6)) / (u - 1 / u)))

BY_ID = {q["id"]: q for q in BANK}
fails = 0
for cid, got in CHECKS:
    stored = BY_ID[cid]["correctAnswer"]
    want, either = parse_answer(stored)
    got_c, want_c = mpc(got), mpc(want)
    if either:
        got_c, want_c = abs(got_c), abs(want_c)
    if abs(got_c - want_c) > mpf("1e-12") * max(1, abs(want_c)):
        fails += 1
        print(f"MISMATCH {cid}: computed {got_c} vs stored {stored!r} ({want_c})")

print(f"{len(CHECKS)} numeric checks against stored answers, {fails} mismatches")
