"""Algebra Sheet-3 (128 questions) -> maths_algebra_215 .. maths_algebra_342.

Answers are the options highlighted in the sheet; each was re-derived here.

Two places where the sheet itself is unclear and the derivation decides:
  Q23  - the highlighter covers both "-√2" and "√2". 7a + 7/a = √98 gives
         a + 1/a = √2, so a = e^(±iπ/4) with period 8; a^17 + a^-25 = 2cos(π/4)
         = +√2, so option B is used.
  Q115 - the sheet prints 1364 as both option B and option D. The duplicate is
         replaced by 1298, the value you get from the wrong sign convention,
         so the four options stay distinct.
"""

from algebra_import_lib import import_sheet

START_INDEX = 214  # maths_algebra_215

QUESTIONS = [
    (
        "If x + 1/x = c + 1/c, then the value of x is:",
        ["c, 1/c", "c, c²", "c, 2c", "0, 1"],
        "c, 1/c",
        "x + 1/x = c + 1/c ⇒ x − c = 1/c − 1/x = (x − c)/(cx).\n"
        "So (x − c)(1 − 1/(cx)) = 0, giving x = c or cx = 1 i.e. x = 1/c.\n"
        "Answer: c, 1/c",
    ),
    (
        "If x³ + 1/x³ = 65/8 and y³ + 1/y³ = 730/27, then which of the following is a value of xy?",
        ["3", "6", "8", "9"],
        "6",
        "65/8 = 8 + 1/8, so x = 2 satisfies x³ + 1/x³ = 65/8.\n"
        "730/27 = 27 + 1/27, so y = 3 satisfies y³ + 1/y³ = 730/27.\n"
        "Hence xy = 2 × 3 = 6.\n"
        "Answer: 6",
    ),
    (
        "If x^150 = (6 − √21)/(6 + √21), then x^150 + 1/x^150 = ?",
        ["8.7", "8.6", "6.7", "7.6"],
        "7.6",
        "Let u = (6 − √21)/(6 + √21); then 1/u = (6 + √21)/(6 − √21).\n"
        "u + 1/u = [(6 − √21)² + (6 + √21)²]/[(6 + √21)(6 − √21)] = 2(36 + 21)/(36 − 21).\n"
        "= 114/15 = 7.6.\n"
        "Answer: 7.6",
    ),
    (
        "If x = (√5 + 1)/(√5 − 1) and y = (√5 − 1)/(√5 + 1), then find the value of x² − y².",
        ["√5", "2√5", "3√5", "4√5"],
        "3√5",
        "x = (√5 + 1)²/4 = (6 + 2√5)/4 = (3 + √5)/2 and y = (3 − √5)/2.\n"
        "x + y = 3 and x − y = √5.\n"
        "x² − y² = (x + y)(x − y) = 3√5.\n"
        "Answer: 3√5",
    ),
    (
        "If the value of (3x√y + 2y√x)/(3x√y − 2y√x) − (3x√y − 2y√x)/(3x√y + 2y√x) is the same as that of √x·√y, then which relation holds?",
        ["9x − 4y = 36", "9x + 4y = 24", "9x + 4y = 36", "9x − 4y = 24"],
        "9x − 4y = 24",
        "Put P = 3x√y and Q = 2y√x; the expression is (P + Q)/(P − Q) − (P − Q)/(P + Q) = 4PQ/(P² − Q²).\n"
        "P² − Q² = 9x²y − 4xy² = xy(9x − 4y) and 4PQ = 24xy√(xy).\n"
        "So the expression is 24√(xy)/(9x − 4y); setting this equal to √(xy) gives 9x − 4y = 24.\n"
        "Answer: 9x − 4y = 24",
    ),
    (
        "If A = (1 + 2x)/(1 − 2x) and B = (1 − 2x)/(1 + 2x), then the value of (A + B)/(A − B) is:",
        ["x + 1/(4x)", "x − 1/(4x)", "1/(4x) − x", "1/(4x²) + x²"],
        "x + 1/(4x)",
        "A + B = [(1 + 2x)² + (1 − 2x)²]/[(1 − 2x)(1 + 2x)] = (2 + 8x²)/(1 − 4x²).\n"
        "A − B = [(1 + 2x)² − (1 − 2x)²]/(1 − 4x²) = 8x/(1 − 4x²).\n"
        "(A + B)/(A − B) = (2 + 8x²)/(8x) = 1/(4x) + x.\n"
        "Answer: x + 1/(4x)",
    ),
    (
        "If x = √6 + 2 and y = √6 − 2, then what is the value of (x/y + y/x)² − 3?",
        ["42", "97", "35", "22"],
        "97",
        "xy = 6 − 4 = 2 and x² + y² = (6 + 4√6 + 4) + (6 − 4√6 + 4) = 20.\n"
        "x/y + y/x = (x² + y²)/xy = 20/2 = 10.\n"
        "(10)² − 3 = 97.\n"
        "Answer: 97",
    ),
    (
        "If 8r/(r² − 8r + 1) = 1/14, then the value of (r + 1/r) is:",
        ["88", "100", "120", "60"],
        "120",
        "Invert: (r² − 8r + 1)/(8r) = 14 ⇒ r² − 8r + 1 = 112r.\n"
        "Divide by r: r + 1/r − 8 = 112.\n"
        "r + 1/r = 120.\n"
        "Answer: 120",
    ),
    (
        "If x + 1/x = 10, then find the value of 7x/(x² + 1 − 8x).",
        ["3.5", "4.5", "2.5", "5.5"],
        "3.5",
        "Divide numerator and denominator by x: 7/((x + 1/x) − 8).\n"
        "= 7/(10 − 8) = 7/2.\n"
        "Answer: 3.5",
    ),
    (
        "If x + 1/x = 15, then the value of (7x² − 9x + 7)/(x² − x + 1) is:",
        ["-48/7", "-22/7", "48/7", "22/7"],
        "48/7",
        "Divide numerator and denominator by x: (7(x + 1/x) − 9)/((x + 1/x) − 1).\n"
        "= (7 × 15 − 9)/(15 − 1) = 96/14.\n"
        "= 48/7.\n"
        "Answer: 48/7",
    ),
    (
        "If a² + 2/a² = 16, then find the value of 72a²/(a⁴ + 2 + 8a²).",
        ["3", "1", "4", "2"],
        "3",
        "Divide numerator and denominator by a²: 72/((a² + 2/a²) + 8).\n"
        "= 72/(16 + 8) = 72/24.\n"
        "= 3.\n"
        "Answer: 3",
    ),
    (
        "If x⁸ − 32x⁴ + 256 = 0, then the positive value of (x² + 1/x²) is:",
        ["3.75", "5.75", "2.25", "4.25"],
        "4.25",
        "Treat it as a quadratic in x⁴: x⁴ = [32 ± √(1024 − 1024)]/2 = 16.\n"
        "So x² = 4 (positive root), i.e. x = 2.\n"
        "x² + 1/x² = 4 + 0.25 = 4.25.\n"
        "Answer: 4.25",
    ),
    (
        "If x + 81/x = 18 where x > 0, then the value of x² + 162/x² is:",
        ["78", "83", "85", "81"],
        "83",
        "Multiply by x: x² − 18x + 81 = 0 ⇒ (x − 9)² = 0 ⇒ x = 9.\n"
        "x² + 162/x² = 81 + 162/81 = 81 + 2.\n"
        "= 83.\n"
        "Answer: 83",
    ),
    (
        "If x + 49/(x + 48) = −34, then find (2x + 83)³ + 1/(2x + 83)³.",
        ["7", "2", "-2", "1"],
        "2",
        "Multiply through by (x + 48): x² + 48x + 49 = −34x − 1632.\n"
        "x² + 82x + 1681 = 0 ⇒ (x + 41)² = 0 ⇒ x = −41.\n"
        "Then 2x + 83 = 1, so 1³ + 1/1³ = 2.\n"
        "Answer: 2",
    ),
    (
        "If a − 24/a = 5, where a > 0, then the value of a² + 64/a² is:",
        ["45", "56", "60", "65"],
        "65",
        "Multiply by a: a² − 5a − 24 = 0 ⇒ (a − 8)(a + 3) = 0 ⇒ a = 8 (a > 0).\n"
        "a² + 64/a² = 64 + 64/64.\n"
        "= 65.\n"
        "Answer: 65",
    ),
    (
        "If p = 13 + 2√42, then find (p² + 1)/(p² − 1).",
        ["13/(2√42)", "13/√42", "1/(2√42)", "1"],
        "13/(2√42)",
        "(13 + 2√42)(13 − 2√42) = 169 − 168 = 1, so 1/p = 13 − 2√42.\n"
        "Divide numerator and denominator by p: (p + 1/p)/(p − 1/p).\n"
        "p + 1/p = 26 and p − 1/p = 4√42, so the value is 26/(4√42) = 13/(2√42).\n"
        "Answer: 13/(2√42)",
    ),
    (
        "If x = 10 + 3√11, then find √x + 1/√x.",
        ["4.84", "4.69", "5.69", "3.92"],
        "4.69",
        "(10 + 3√11)(10 − 3√11) = 100 − 99 = 1, so 1/x = 10 − 3√11 and x + 1/x = 20.\n"
        "(√x + 1/√x)² = x + 2 + 1/x = 22.\n"
        "√x + 1/√x = √22 ≈ 4.69.\n"
        "Answer: 4.69",
    ),
    (
        "If (x + 1/x) = 8.5, what is the value of (x² + 1/x²)?",
        ["70.25", "74.25", "72.25", "75.25"],
        "70.25",
        "x² + 1/x² = (x + 1/x)² − 2.\n"
        "= 72.25 − 2.\n"
        "= 70.25.\n"
        "Answer: 70.25",
    ),
    (
        "If the sum of a number and its reciprocal is 15, what is the sum of the square of the number and the square of its reciprocal?",
        ["111 × 2 + 1", "111 × 2 + 2", "111 × 2 + 3", "111 × 2 + 4"],
        "111 × 2 + 1",
        "x + 1/x = 15 ⇒ x² + 1/x² = 225 − 2 = 223.\n"
        "223 = 222 + 1 = 111 × 2 + 1.\n"
        "Answer: 111 × 2 + 1",
    ),
    (
        "If x^12.5 + 1/x^12.5 = 16, then x^25 + 1/x^25 = ?",
        ["254", "258", "260", "256"],
        "254",
        "x^25 + 1/x^25 = (x^12.5 + 1/x^12.5)² − 2.\n"
        "= 256 − 2.\n"
        "= 254.\n"
        "Answer: 254",
    ),
    (
        "If (x^42 + 1)/x^21 = 7, then (x^84 + 1)/x^42 = ?",
        ["51", "49", "53", "47"],
        "47",
        "The condition says x^21 + 1/x^21 = 7.\n"
        "(x^84 + 1)/x^42 = x^42 + 1/x^42 = 7² − 2.\n"
        "= 47.\n"
        "Answer: 47",
    ),
    (
        "If x^200/y^200 + y^200/x^200 = 8, then find x^400/y^400 + y^400/x^400.",
        ["60", "64", "62", "66"],
        "62",
        "Let t = x^200/y^200, so t + 1/t = 8.\n"
        "t² + 1/t² = 8² − 2.\n"
        "= 62.\n"
        "Answer: 62",
    ),
    (
        "If 7a + 7/a = √98, then find a^17 + 1/a^25.",
        ["-√2", "√2", "-√1", "1"],
        "√2",
        "√98 = 7√2, so a + 1/a = √2, i.e. 2cosθ = √2 and a = e^(±iπ/4).\n"
        "Then a⁸ = 1, so a^17 = a and a^(−25) = a^(−25+32) = a⁷ = 1/a.\n"
        "a^17 + 1/a^25 = a + 1/a = √2.\n"
        "Answer: √2",
    ),
    (
        "If √x + 1/√x = 3 and x > 0, then x²(x² − 47) = ?",
        ["0", "2", "-1", "-2"],
        "-1",
        "Squaring: x + 2 + 1/x = 9 ⇒ x + 1/x = 7 ⇒ x² + 1/x² = 47.\n"
        "So x⁴ + 1 = 47x², i.e. x⁴ − 47x² = −1.\n"
        "x²(x² − 47) = x⁴ − 47x² = −1.\n"
        "Answer: -1",
    ),
    (
        "If x^2019 = 11 − 2√30, then x^4038 + 1/x^4038 = ?",
        ["443", "439", "486", "482"],
        "482",
        "(11 − 2√30)(11 + 2√30) = 121 − 120 = 1, so u = 11 − 2√30 has u + 1/u = 22.\n"
        "x^4038 + 1/x^4038 = u² + 1/u² = 22² − 2.\n"
        "= 482.\n"
        "Answer: 482",
    ),
    (
        "If P = 7 + 4√3 and PQ = 1, then what is the value of (1/P²) + (1/Q²)?",
        ["148", "189", "194", "204"],
        "194",
        "PQ = 1 means Q = 1/P, so 1/P² + 1/Q² = Q² + P².\n"
        "P + Q = (7 + 4√3) + (7 − 4√3) = 14 and PQ = 1.\n"
        "P² + Q² = 196 − 2 = 194.\n"
        "Answer: 194",
    ),
    (
        "If x = (√5 + 2)/(√5 − 2), then the value of x² + x⁻² is:",
        ["350", "345", "284", "322"],
        "322",
        "x = (√5 + 2)²/(5 − 4) = 9 + 4√5, so 1/x = 9 − 4√5.\n"
        "x + 1/x = 18.\n"
        "x² + 1/x² = 324 − 2 = 322.\n"
        "Answer: 322",
    ),
    (
        "If a = (√3 + √2)/(√3 − √2) and b = (√3 − √2)/(√3 + √2), then the value of a² + b² − ab is:",
        ["97", "2√3 + 2", "4√6 + 1", "98"],
        "97",
        "a = (√3 + √2)² = 5 + 2√6 and b = 5 − 2√6, so a + b = 10 and ab = 1.\n"
        "a² + b² = 100 − 2 = 98.\n"
        "a² + b² − ab = 98 − 1 = 97.\n"
        "Answer: 97",
    ),
    (
        "If x = (√5 − √3)/(√5 + √3) and y = (√5 + √3)/(√5 − √3), then (x² + xy + y²)/(x² − xy + y²) = ?",
        ["63/61", "67/65", "65/63", "69/67"],
        "63/61",
        "x = 4 − √15 and y = 4 + √15, so x + y = 8 and xy = 1.\n"
        "x² + y² = 64 − 2 = 62.\n"
        "(62 + 1)/(62 − 1) = 63/61.\n"
        "Answer: 63/61",
    ),
    (
        "If 1/(x − 2) + x = 8, then what is the value of 1/(x − 2)² + (x − 2)²?",
        ["38", "36", "40", "34"],
        "34",
        "Rewrite as 1/(x − 2) + (x − 2) = 8 − 2 = 6.\n"
        "Squaring: (x − 2)² + 2 + 1/(x − 2)² = 36.\n"
        "So the required value is 36 − 2 = 34.\n"
        "Answer: 34",
    ),
    (
        "If x is the fourth root of (3 + 2√2)/(3 − 2√2), then x⁸ + 1/x⁸ = ?",
        ["1156", "1154", "1152", "1158"],
        "1154",
        "(3 + 2√2)/(3 − 2√2) = (3 + 2√2)²/(9 − 8) = 17 + 12√2, so x⁴ = 17 + 12√2.\n"
        "Its reciprocal is 17 − 12√2, so x⁴ + 1/x⁴ = 34.\n"
        "x⁸ + 1/x⁸ = 34² − 2 = 1154.\n"
        "Answer: 1154",
    ),
    (
        "If x + (1/x) = (√3 + 1)/2, then what is the value of x⁴ + (1/x⁴)?",
        ["(4√3 − 1)/4", "(4√3 + 1)/2", "(−4√3 − 1)/4", "(−4√3 − 1)/2"],
        "(−4√3 − 1)/4",
        "x² + 1/x² = ((√3 + 1)/2)² − 2 = (4 + 2√3)/4 − 2 = (√3 − 2)/2.\n"
        "x⁴ + 1/x⁴ = ((√3 − 2)/2)² − 2 = (7 − 4√3)/4 − 2.\n"
        "= (7 − 4√3 − 8)/4 = (−4√3 − 1)/4.\n"
        "Answer: (−4√3 − 1)/4",
    ),
    (
        "If x = 97 + 56√3, then what is the value of the fourth root of x plus the reciprocal of the fourth root of x?",
        ["7", "6", "5", "4"],
        "4",
        "97² − 56² × 3 = 9409 − 9408 = 1, so 1/x = 97 − 56√3 and x + 1/x = 194.\n"
        "(√x + 1/√x)² = 194 + 2 = 196 ⇒ √x + 1/√x = 14.\n"
        "(x^(1/4) + x^(−1/4))² = 14 + 2 = 16 ⇒ the value is 4.\n"
        "Answer: 4",
    ),
    (
        "If p = 13 + 2√42, then the value of (p² + 1)/(p² − 1) is:",
        ["13/(2√42)", "1/(2√42)", "13/√42", "1"],
        "13/(2√42)",
        "Since (13 + 2√42)(13 − 2√42) = 1, we have 1/p = 13 − 2√42.\n"
        "(p² + 1)/(p² − 1) = (p + 1/p)/(p − 1/p) after dividing by p.\n"
        "= 26/(4√42) = 13/(2√42).\n"
        "Answer: 13/(2√42)",
    ),
    (
        "If x − 1/x = 0.4 and x > 0, then find x² + 1/x².",
        ["4.16", "3.32", "1.84", "2.16"],
        "2.16",
        "x² + 1/x² = (x − 1/x)² + 2.\n"
        "= 0.16 + 2.\n"
        "= 2.16.\n"
        "Answer: 2.16",
    ),
    (
        "If a² − 13a − 1 = 0, then find the value of a² + 1/a².",
        ["13", "169", "167", "171"],
        "171",
        "Divide by a: a − 1/a = 13.\n"
        "a² + 1/a² = 13² + 2.\n"
        "= 171.\n"
        "Answer: 171",
    ),
    (
        "If x(5 − 2/x) = 5/x, then the value of x² + 1/x² is equal to:",
        ["2 4/25", "2 1/25", "3 4/25", "2 3/25"],
        "2 4/25",
        "5x − 2 = 5/x ⇒ 5(x − 1/x) = 2 ⇒ x − 1/x = 2/5.\n"
        "x² + 1/x² = 4/25 + 2.\n"
        "= 2 4/25.\n"
        "Answer: 2 4/25",
    ),
    (
        "If x − 5√x − 1 = 0, then x² + 1/x² is equal to:",
        ["625", "731", "729", "727"],
        "727",
        "x − 1 = 5√x; dividing by √x gives √x − 1/√x = 5.\n"
        "So x + 1/x = 25 + 2 = 27.\n"
        "x² + 1/x² = 27² − 2 = 727.\n"
        "Answer: 727",
    ),
    (
        "If x² + (4 − √3)x − 1 = 0, then what is the value of x² + 1/x²?",
        ["9 − 8√3", "21 − 12√3", "21 − 8√3", "17 − 8√3"],
        "21 − 8√3",
        "Divide by x: x − 1/x = −(4 − √3) = √3 − 4.\n"
        "x² + 1/x² = (√3 − 4)² + 2 = (19 − 8√3) + 2.\n"
        "= 21 − 8√3.\n"
        "Answer: 21 − 8√3",
    ),
    (
        "If 4·x^(9/4) − 9·x^(9/8) + 4 = 0, then x^(9/4) + x^(−9/4) = ?",
        ["49/16", "53/20", "67/32", "9/4"],
        "49/16",
        "Put u = x^(9/8), so the equation is 4u² − 9u + 4 = 0.\n"
        "Divide by u: 4(u + 1/u) = 9 ⇒ u + 1/u = 9/4.\n"
        "x^(9/4) + x^(−9/4) = u² + 1/u² = 81/16 − 2 = 49/16.\n"
        "Answer: 49/16",
    ),
    (
        "If 2x/(5x² − 7x + 5) = 1/3, then x² + 1/x² = ?",
        ["219/25", "119/25", "69/25", "138/25"],
        "119/25",
        "6x = 5x² − 7x + 5 ⇒ 5x² − 13x + 5 = 0.\n"
        "Divide by x: 5(x + 1/x) = 13 ⇒ x + 1/x = 13/5.\n"
        "x² + 1/x² = 169/25 − 2 = 119/25.\n"
        "Answer: 119/25",
    ),
    (
        "If x + 1/x = 9, then find x⁴ + 1/x⁴.",
        ["5431", "6561", "6156", "6239"],
        "6239",
        "x² + 1/x² = 81 − 2 = 79.\n"
        "x⁴ + 1/x⁴ = 79² − 2 = 6241 − 2.\n"
        "= 6239.\n"
        "Answer: 6239",
    ),
    (
        "If x + 1/x = −13, what is the value of x⁴ + 1/x⁴?",
        ["27887", "27891", "29243", "28561"],
        "27887",
        "x² + 1/x² = 169 − 2 = 167.\n"
        "x⁴ + 1/x⁴ = 167² − 2 = 27889 − 2.\n"
        "= 27887.\n"
        "Answer: 27887",
    ),
    (
        "If √x + 1/√x = 2√3, then what will be the value of x⁴ + 1/x⁴?",
        ["10402", "9606", "9602", "10406"],
        "9602",
        "Squaring: x + 2 + 1/x = 12 ⇒ x + 1/x = 10.\n"
        "x² + 1/x² = 100 − 2 = 98.\n"
        "x⁴ + 1/x⁴ = 98² − 2 = 9602.\n"
        "Answer: 9602",
    ),
    (
        "If a/(a² + 3a + 1) = 7, then find a²/(a⁴ + 3a² + 1).",
        ["35/537", "49/417", "449/49", "49/449"],
        "49/449",
        "Inverting: a + 3 + 1/a = 1/7 ⇒ a + 1/a = 1/7 − 3 = −20/7.\n"
        "(a⁴ + 3a² + 1)/a² = a² + 1/a² + 3 = (400/49 − 2) + 3 = 449/49.\n"
        "So a²/(a⁴ + 3a² + 1) = 49/449.\n"
        "Answer: 49/449",
    ),
    (
        "If √x − 1/√x = 7, then x² + 1/x² is equal to:",
        ["2599", "2603", "2508", "2560"],
        "2599",
        "Squaring: x − 2 + 1/x = 49 ⇒ x + 1/x = 51.\n"
        "x² + 1/x² = 51² − 2 = 2601 − 2.\n"
        "= 2599.\n"
        "Answer: 2599",
    ),
    (
        "If x^(1.08√2) − 1/x^(1.08√2) = √5, then find x^(4.32√2) + 1/x^(4.32√2).",
        ["45", "47", "7", "11"],
        "47",
        "Let u = x^(1.08√2), so u − 1/u = √5 and u² + 1/u² = 5 + 2 = 7.\n"
        "Since 4.32 = 4 × 1.08, the target is u⁴ + 1/u⁴ = 7² − 2.\n"
        "= 47.\n"
        "Answer: 47",
    ),
    (
        "If x² − 15x + 1 = 0, then what is the value of x⁴ − 223x² + 6?",
        ["9", "5", "6", "0"],
        "5",
        "Divide by x: x + 1/x = 15, so x² + 1/x² = 223, i.e. x⁴ + 1 = 223x².\n"
        "x⁴ − 223x² + 6 = (x⁴ + 1) − 223x² + 5 = 5.\n"
        "Answer: 5",
    ),
    (
        "If x² − 11x + 1 = 0, then find x⁸ − 14159x⁴ + 11.",
        ["9", "10", "12", "11"],
        "11",
        "x + 1/x = 11 ⇒ x² + 1/x² = 119 ⇒ x⁴ + 1/x⁴ = 119² − 2 = 14159.\n"
        "So x⁸ + 1 = 14159x⁴.\n"
        "x⁸ − 14159x⁴ + 11 = 11 − 1 + 1 = 11.\n"
        "Answer: 11",
    ),
    (
        "If (3x + 2/x − 4) = 10, then what is the value of (9x² + 4/x² + 24)?",
        ["214", "208", "256", "218"],
        "208",
        "3x + 2/x = 14.\n"
        "Squaring: 9x² + 12 + 4/x² = 196 ⇒ 9x² + 4/x² = 184.\n"
        "Adding 24 gives 208.\n"
        "Answer: 208",
    ),
    (
        "If 5x + 1/(3x) = 4, then what is the value of 9x² + 1/(25x²)?",
        ["174/125", "144/125", "114/25", "119/25"],
        "114/25",
        "Multiply the condition by 3/5: 3x + 1/(5x) = 12/5.\n"
        "Squaring: 9x² + 6/5 + 1/(25x²) = 144/25.\n"
        "9x² + 1/(25x²) = 144/25 − 30/25 = 114/25.\n"
        "Answer: 114/25",
    ),
    (
        "If 12x² − 21x + 1 = 0, then what is the value of 9x² + (16x²)⁻¹?",
        ["429/8", "465/16", "417/16", "453/8"],
        "417/16",
        "Divide by x: 12x + 1/x = 21, so 3x + 1/(4x) = 21/4.\n"
        "Squaring: 9x² + 3/2 + 1/(16x²) = 441/16.\n"
        "9x² + 1/(16x²) = 441/16 − 24/16 = 417/16.\n"
        "Answer: 417/16",
    ),
    (
        "If 7b − 1/(4b) = 7, then what is the value of 16b² + 1/(49b²)?",
        ["80/49", "104/7", "120/7", "7/2"],
        "120/7",
        "Multiply the condition by 4/7: 4b − 1/(7b) = 4.\n"
        "Squaring: 16b² − 8/7 + 1/(49b²) = 16.\n"
        "16b² + 1/(49b²) = 16 + 8/7 = 120/7.\n"
        "Answer: 120/7",
    ),
    (
        "If (2x − 3/x) = 2, then what is the value of (16x⁴ + 81/x⁴)?",
        ["184", "328", "180", "220"],
        "184",
        "Squaring: 4x² − 12 + 9/x² = 4 ⇒ 4x² + 9/x² = 16.\n"
        "Squaring again: 16x⁴ + 72 + 81/x⁴ = 256.\n"
        "16x⁴ + 81/x⁴ = 184.\n"
        "Answer: 184",
    ),
    (
        "If x²/y² + y²/x² = 223, then find x/y + y/x.",
        ["±15", "15", "-15", "√221"],
        "±15",
        "Let t = x/y + y/x, so t² = (x²/y² + y²/x²) + 2 = 225.\n"
        "t = ±15, and both signs are attainable.\n"
        "Answer: ±15",
    ),
    (
        "If [3(x² + 1) − 7x]/(3x) = 6 with x ≠ 0, then the value of √x + 1/√x is:",
        ["√(25/3)", "√(31/3)", "√(11/3)", "√(35/3)"],
        "√(31/3)",
        "3x² + 3 − 7x = 18x ⇒ 3x² + 3 = 25x.\n"
        "Divide by 3x: x + 1/x = 25/3.\n"
        "(√x + 1/√x)² = 25/3 + 2 = 31/3, so the value is √(31/3).\n"
        "Answer: √(31/3)",
    ),
    (
        "If x⁴ + 1/x⁴ = 3842, then the positive value of x + 1/x will be:",
        ["12", "8", "10", "6"],
        "8",
        "x² + 1/x² = √(3842 + 2) = √3844 = 62.\n"
        "x + 1/x = √(62 + 2) = √64.\n"
        "= 8.\n"
        "Answer: 8",
    ),
    (
        "If x⁴ + 1/x⁴ = 14159 and x(x − t) = −1, then the value of t is:",
        ["9", "12", "10", "11"],
        "11",
        "x² + 1/x² = √(14159 + 2) = √14161 = 119, so x + 1/x = √121 = 11.\n"
        "x(x − t) = −1 gives x² + 1 = tx, i.e. t = x + 1/x.\n"
        "t = 11.\n"
        "Answer: 11",
    ),
    (
        "If x² + 1/x² = 51, then the value of (x² − 1)/x is:",
        ["7", "6", "8", "9"],
        "7",
        "(x − 1/x)² = (x² + 1/x²) − 2 = 49.\n"
        "So x − 1/x = 7, and (x² − 1)/x = x − 1/x.\n"
        "= 7.\n"
        "Answer: 7",
    ),
    (
        "If 3a² + 3/a² = 54, then the value of (a² + 2a − 1)/a is:",
        ["-6, -2", "6, -2", "-6, 2", "6, 2"],
        "6, -2",
        "a² + 1/a² = 18, so (a − 1/a)² = 16 and a − 1/a = ±4.\n"
        "(a² + 2a − 1)/a = (a − 1/a) + 2.\n"
        "= 4 + 2 = 6 or −4 + 2 = −2.\n"
        "Answer: 6, -2",
    ),
    (
        "If x > 1 and x⁴ + 1/x⁴ = 79, what is the value of x − 1/x?",
        ["2√2", "√7", "√11", "√10"],
        "√7",
        "x² + 1/x² = √(79 + 2) = √81 = 9.\n"
        "(x − 1/x)² = 9 − 2 = 7.\n"
        "Since x > 1, x − 1/x = √7.\n"
        "Answer: √7",
    ),
    (
        "If x⁴ + 1/x⁴ = 6887, then the positive value of x − 1/x is:",
        ["12", "9", "15", "8"],
        "9",
        "x² + 1/x² = √(6887 + 2) = √6889 = 83.\n"
        "(x − 1/x)² = 83 − 2 = 81.\n"
        "x − 1/x = 9.\n"
        "Answer: 9",
    ),
    (
        "If x⁸ − 1442x⁴ + 1 = 0, then a possible value of x − 1/x is:",
        ["5", "8", "6", "4"],
        "6",
        "Divide by x⁴: x⁴ + 1/x⁴ = 1442.\n"
        "x² + 1/x² = √1444 = 38, so (x − 1/x)² = 36.\n"
        "x − 1/x = 6.\n"
        "Answer: 6",
    ),
    (
        "If x⁴ + 16/x⁴ = 27217 with x > 0, then the value of x + 2/x is:",
        ["17", "11", "15", "13"],
        "13",
        "(x² + 4/x²)² = x⁴ + 8 + 16/x⁴ = 27225, so x² + 4/x² = 165.\n"
        "(x + 2/x)² = x² + 4 + 4/x² = 169.\n"
        "x + 2/x = 13.\n"
        "Answer: 13",
    ),
    (
        "If x² + 1/x² = 38, then find the value of 6x(x − 1)/(x³ − x² − x + 1).",
        ["0", "1", "2", "3"],
        "1",
        "Factor the denominator: x²(x − 1) − (x − 1) = (x − 1)²(x + 1).\n"
        "So the expression is 6x/((x − 1)(x + 1)) = 6x/(x² − 1) = 6/((x² − 1)/x).\n"
        "(x − 1/x)² = 38 − 2 = 36, so (x² − 1)/x = 6 and the value is 1.\n"
        "Answer: 1",
    ),
    (
        "If m⁴ + 1/m⁴ = 119, then find m − 1/m.",
        ["4", "-5", "3", "11"],
        "3",
        "m² + 1/m² = √(119 + 2) = √121 = 11.\n"
        "(m − 1/m)² = 11 − 2 = 9.\n"
        "m − 1/m = 3.\n"
        "Answer: 3",
    ),
    (
        "If x⁴ + x⁻⁴ = 119 with x > 0, then the value of (2x − 3)² is:",
        ["12", "13", "15", "14"],
        "13",
        "x² + 1/x² = 11, so (x − 1/x)² = 9 and x − 1/x = 3, i.e. x² = 3x + 1.\n"
        "(2x − 3)² = 4x² − 12x + 9 = 4(3x + 1) − 12x + 9.\n"
        "= 13.\n"
        "Answer: 13",
    ),
    (
        "If 3x + 1/(2x) = 3, then find (3x² − 1)².",
        ["3/2", "3/4", "5/6", "4/3"],
        "3/4",
        "Multiply by 2x: 6x² − 6x + 1 = 0, so x = (3 ± √3)/6 and x² = x − 1/6.\n"
        "3x² − 1 = 3x − 1/2 − 1 = 3x − 3/2 = ±√3/2 for the two roots.\n"
        "(3x² − 1)² = 3/4.\n"
        "Answer: 3/4",
    ),
    (
        "If 3√x + 1/(2√x) = 3 with x > 0, then find x²(18x² − 7).",
        ["-1/36", "-2/63", "-1/72", "-2/81"],
        "-1/72",
        "With t = √x: 6t² − 6t + 1 = 0 gives t = (3 + √3)/6, so x = t² = (2 + √3)/6.\n"
        "x² = (7 + 4√3)/36 and 18x² − 7 = (7 + 4√3)/2 − 7 = (4√3 − 7)/2.\n"
        "x²(18x² − 7) = (7 + 4√3)(4√3 − 7)/72 = (48 − 49)/72 = −1/72.\n"
        "Answer: -1/72",
    ),
    (
        "If m^117/n^109 − n^109/m^117 = 9, then find m^117/n^109 + n^109/m^117.",
        ["√90", "√85", "√10", "√82"],
        "√85",
        "Let u be the first ratio, so u − 1/u = 9.\n"
        "(u + 1/u)² = (u − 1/u)² + 4 = 81 + 4 = 85.\n"
        "u + 1/u = √85.\n"
        "Answer: √85",
    ),
    (
        "If a = 1/(a − 5) with a > 0, then the value of a + 1/a is:",
        ["√29", "2√29", "-√29", "√21"],
        "√29",
        "a(a − 5) = 1 ⇒ a − 5 = 1/a ⇒ a − 1/a = 5.\n"
        "(a + 1/a)² = 25 + 4 = 29.\n"
        "Since a > 0, a + 1/a = √29.\n"
        "Answer: √29",
    ),
    (
        "If (A + B)/√(AB) = 10√2, then (A − B)/√(AB) = ?",
        ["12", "14", "13", "9√2"],
        "14",
        "Let r = A/B, so √r + 1/√r = 10√2 and squaring gives r + 1/r = 200 − 2 = 198.\n"
        "((A − B)/√(AB))² = r − 2 + 1/r = 196.\n"
        "So the value is 14.\n"
        "Answer: 14",
    ),
    (
        "If x + 1/(x + 7) = 0, then x − 1/(x + 7) = ?",
        ["3√5 − 5", "3√5 − 7", "3√7 − 5", "3√7 − 7"],
        "3√5 − 7",
        "Put y = x + 7. Then (y − 7) + 1/y = 0 ⇒ y + 1/y = 7.\n"
        "y − 1/y = √(49 − 4) = 3√5.\n"
        "x − 1/(x + 7) = (y − 1/y) − 7 = 3√5 − 7.\n"
        "Answer: 3√5 − 7",
    ),
    (
        "If sec x − cos x = 4, then what will be the value of (1 + cos²x)/cos x?",
        ["9/4", "1/4", "2√5", "√5"],
        "2√5",
        "(1 + cos²x)/cos x = sec x + cos x.\n"
        "(sec x + cos x)² = (sec x − cos x)² + 4 = 16 + 4 = 20.\n"
        "So the value is 2√5.\n"
        "Answer: 2√5",
    ),
    (
        "If x + 1/x = 8, find x² − 1/x².",
        ["16√15", "15√15", "62", "10√15"],
        "16√15",
        "(x − 1/x)² = 64 − 4 = 60, so x − 1/x = 2√15.\n"
        "x² − 1/x² = (x + 1/x)(x − 1/x) = 8 × 2√15.\n"
        "= 16√15.\n"
        "Answer: 16√15",
    ),
    (
        "If x > 1 and x² + 1/x² = 2√5, what is the value of x⁴ − 1/x⁴?",
        ["4√5", "4√30", "8√5", "8√6"],
        "8√5",
        "(x² − 1/x²)² = (2√5)² − 4 = 16, so x² − 1/x² = 4.\n"
        "x⁴ − 1/x⁴ = (x² + 1/x²)(x² − 1/x²) = 2√5 × 4.\n"
        "= 8√5.\n"
        "Answer: 8√5",
    ),
    (
        "If x² − 7x + 1 = 0 and 0 < x < 1, what is the value of x² − 1/x²?",
        ["21√5", "−21√5", "28√5", "−28√5"],
        "−21√5",
        "x + 1/x = 7; since 0 < x < 1 we have x < 1/x, so x − 1/x = −√(49 − 4) = −3√5.\n"
        "x² − 1/x² = (x + 1/x)(x − 1/x) = 7 × (−3√5).\n"
        "= −21√5.\n"
        "Answer: −21√5",
    ),
    (
        "If 3x − 1/(4x) = 6, then 4x + 1/(3x) = ?",
        ["2√17", "4√13/√3", "2√15", "4√17/√3"],
        "4√13/√3",
        "Squaring the condition: 9x² − 3/2 + 1/(16x²) = 36 ⇒ 9x² + 1/(16x²) = 75/2.\n"
        "Multiplying that by 16/9: 16x² + 1/(9x²) = (16/9)(75/2) = 200/3.\n"
        "(4x + 1/(3x))² = 200/3 + 8/3 = 208/3, so the value is √208/√3 = 4√13/√3.\n"
        "Answer: 4√13/√3",
    ),
    (
        "If 2x − 5/(9x) = 3, then 36x² − 25/(9x²) = ?",
        ["99", "119", "123", "101"],
        "99",
        "Multiply the condition by 3: 6x − 5/(3x) = 9.\n"
        "(6x + 5/(3x))² = 81 + 4 × 10 = 121, so 6x + 5/(3x) = 11.\n"
        "36x² − 25/(9x²) = (6x − 5/(3x))(6x + 5/(3x)) = 9 × 11 = 99.\n"
        "Answer: 99",
    ),
    (
        "If x² − 16x + 59 = 0, then find the value of (x − 6)² + 1/(x − 6)².",
        ["14", "18", "16", "20"],
        "18",
        "Put y = x − 6: (y + 6)² − 16(y + 6) + 59 = y² − 4y − 1 = 0.\n"
        "Divide by y: y − 1/y = 4.\n"
        "y² + 1/y² = 16 + 2 = 18.\n"
        "Answer: 18",
    ),
    (
        "If x² − 12x + 33 = 0, then what is the value of (x − 4)⁴ + 1/(x − 4)⁴?",
        ["227", "326", "167", "194"],
        "194",
        "Put y = x − 4: (y + 4)² − 12(y + 4) + 33 = y² − 4y + 1 = 0 ⇒ y + 1/y = 4.\n"
        "y² + 1/y² = 16 − 2 = 14.\n"
        "y⁴ + 1/y⁴ = 196 − 2 = 194.\n"
        "Answer: 194",
    ),
    (
        "If x² + 2x − 7 = 0, then (x + 4)⁴ + 1/(x + 4)⁴ = ?",
        ["527", "2207", "1154", "128"],
        "1154",
        "Put y = x + 4: (y − 4)² + 2(y − 4) − 7 = y² − 6y + 1 = 0 ⇒ y + 1/y = 6.\n"
        "y² + 1/y² = 36 − 2 = 34.\n"
        "y⁴ + 1/y⁴ = 1156 − 2 = 1154.\n"
        "Answer: 1154",
    ),
    (
        "If x² − 22x + 111 = 0, then what is the value of (x − 8)² − 1/(x − 8)²?",
        ["12√10", "8√5", "8√3", "18"],
        "12√10",
        "Put y = x − 8: (y + 8)² − 22(y + 8) + 111 = y² − 6y − 1 = 0 ⇒ y − 1/y = 6.\n"
        "y + 1/y = √(36 + 4) = 2√10.\n"
        "y² − 1/y² = 2√10 × 6 = 12√10.\n"
        "Answer: 12√10",
    ),
    (
        "If (x + 1/x) = 11/5, what is the value of (x³ + 1/x³)?",
        ["4 6/125", "5 101/125", "10 81/125", "17 31/125"],
        "4 6/125",
        "x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x).\n"
        "= 1331/125 − 33/5 = 1331/125 − 825/125 = 506/125.\n"
        "= 4 6/125.\n"
        "Answer: 4 6/125",
    ),
    (
        "If x^15 + 1/x^15 = 9, then x^45 + 1/x^45 = ?",
        ["729", "756", "702", "774"],
        "702",
        "With u = x^15: u³ + 1/u³ = (u + 1/u)³ − 3(u + 1/u).\n"
        "= 729 − 27.\n"
        "= 702.\n"
        "Answer: 702",
    ),
    (
        "If x^0.18 + 1/x^0.18 = 8, then find x^0.54 + 1/x^0.54.",
        ["488", "536", "523", "62"],
        "488",
        "0.54 = 3 × 0.18, so with u = x^0.18 we need u³ + 1/u³.\n"
        "= 8³ − 3 × 8.\n"
        "= 512 − 24 = 488.\n"
        "Answer: 488",
    ),
    (
        "If (a + b)/√(ab) = 4, then (a/b)^(3/2) + (b/a)^(3/2) = ?",
        ["52", "60", "48", "68"],
        "52",
        "Let t = √(a/b); then (a + b)/√(ab) = t + 1/t = 4.\n"
        "The required value is t³ + 1/t³ = 4³ − 3 × 4.\n"
        "= 52.\n"
        "Answer: 52",
    ),
    (
        "If x + 1/x = 2cosθ, then x³ + 1/x³ = ?",
        ["2cos2θ", "cos3θ", "2cos3θ", "cos2θ"],
        "2cos3θ",
        "x³ + 1/x³ = (2cosθ)³ − 3(2cosθ) = 8cos³θ − 6cosθ.\n"
        "= 2(4cos³θ − 3cosθ).\n"
        "= 2cos3θ.\n"
        "Answer: 2cos3θ",
    ),
    (
        "If √x + 1/√x = 11 with x > 0, then x√x(x√x − 1298) + 11 = ?",
        ["10", "12", "11", "8"],
        "10",
        "Let A = x√x = x^(3/2). Then A + 1/A = (√x + 1/√x)³ − 3(√x + 1/√x) = 1331 − 33 = 1298.\n"
        "So A² + 1 = 1298A, i.e. A(A − 1298) = −1.\n"
        "The expression equals −1 + 11 = 10.\n"
        "Answer: 10",
    ),
    (
        "If √x − 1/√x = √7, then the value of x³ + 1/x³ is:",
        ["679", "702", "756", "729"],
        "702",
        "Squaring: x − 2 + 1/x = 7 ⇒ x + 1/x = 9.\n"
        "x³ + 1/x³ = 729 − 27.\n"
        "= 702.\n"
        "Answer: 702",
    ),
    (
        "If x² + 1/x² = 167 with x > 0, then the value of x³ + 1/x³ is:",
        ["2171", "2194", "2158", "2233"],
        "2158",
        "x + 1/x = √(167 + 2) = √169 = 13.\n"
        "x³ + 1/x³ = 13³ − 3 × 13 = 2197 − 39.\n"
        "= 2158.\n"
        "Answer: 2158",
    ),
    (
        "If (m^28 + 1)/m^14 = 23, then find (m^42 + 1)/m^21.",
        ["110", "48", "25", "78"],
        "110",
        "The condition is m^14 + 1/m^14 = 23; with u = m⁷ this is u² + 1/u² = 23, so u + 1/u = 5.\n"
        "(m^42 + 1)/m^21 = u³ + 1/u³ = 125 − 15.\n"
        "= 110.\n"
        "Answer: 110",
    ),
    (
        "If x√x + 1/(x√x) = 7, then x⁶ + 1/x⁶ = ?",
        ["2401", "2207", "2399", "2211"],
        "2207",
        "Let A = x^(3/2), so A + 1/A = 7 and A² + 1/A² = 47.\n"
        "x⁶ + 1/x⁶ = A⁴ + 1/A⁴ = 47² − 2.\n"
        "= 2207.\n"
        "Answer: 2207",
    ),
    (
        "If x⁴ + 1/x⁴ = 1154 with x > 0, then what is the value of x³ + 1/x³?",
        ["205", "214", "185", "198"],
        "198",
        "x² + 1/x² = √1156 = 34 and x + 1/x = √36 = 6.\n"
        "x³ + 1/x³ = 216 − 18.\n"
        "= 198.\n"
        "Answer: 198",
    ),
    (
        "If x + 1/x = 79, then find x√x + 1/(x√x).",
        ["702", "716", "756", "727"],
        "702",
        "(√x + 1/√x)² = 79 + 2 = 81, so √x + 1/√x = 9.\n"
        "x√x + 1/(x√x) = 9³ − 3 × 9.\n"
        "= 702.\n"
        "Answer: 702",
    ),
    (
        "If x = (√5 − √3)/(√5 + √3) and y is the reciprocal of x, then what is the value of (x³ + y³)?",
        ["504", "476", "472", "488"],
        "488",
        "x = (√5 − √3)²/2 = 4 − √15 and y = 4 + √15, so x + y = 8 and xy = 1.\n"
        "x³ + y³ = 8³ − 3 × 1 × 8.\n"
        "= 488.\n"
        "Answer: 488",
    ),
    (
        "If a = (√7 + √6)/(√7 − √6) and b = (√7 − √6)/(√7 + √6), then find a²/b + b²/a.",
        ["17498", "17550", "17654", "17576"],
        "17498",
        "a = (√7 + √6)² = 13 + 2√42 and b = 13 − 2√42, so a + b = 26 and ab = 1.\n"
        "a²/b + b²/a = (a³ + b³)/ab = a³ + b³ = 26³ − 3 × 26.\n"
        "= 17576 − 78 = 17498.\n"
        "Answer: 17498",
    ),
    (
        "If a + 1/(a + 1) = 3, then what is the value of (a + 1)³ + 1/(a + 1)³?",
        ["8", "52", "2", "62"],
        "52",
        "Add 1 to both sides: (a + 1) + 1/(a + 1) = 4.\n"
        "(a + 1)³ + 1/(a + 1)³ = 4³ − 3 × 4.\n"
        "= 52.\n"
        "Answer: 52",
    ),
    (
        "If x² + 6x + 1 = 0, then the value of (x + 6)³ + 1/(x + 6)³ is:",
        ["245", "216", "186", "198"],
        "198",
        "x(x + 6) = −1 means x + 6 = −1/x, so with y = x + 6 we get 1/y = −x.\n"
        "y³ + 1/y³ = −(x³ + 1/x³), and dividing the equation by x gives x + 1/x = −6.\n"
        "x³ + 1/x³ = −216 + 18 = −198, so the answer is 198.\n"
        "Answer: 198",
    ),
    (
        "If x² − 6√3x + 1 = 0, then the value of x³ + 1/x³ will be:",
        ["234√3", "216√3", "666√3", "630√3"],
        "630√3",
        "Divide by x: x + 1/x = 6√3.\n"
        "x³ + 1/x³ = (6√3)³ − 3(6√3) = 648√3 − 18√3.\n"
        "= 630√3.\n"
        "Answer: 630√3",
    ),
    (
        "If x + 1/x = 17, what is the value of (x⁴ + 1/x²)/(x² − 3x + 1)?",
        ["2431/7", "3375/7", "3375/14", "3985/9"],
        "2431/7",
        "Divide numerator and denominator by x³: the numerator becomes x³ + 1/x³ and the denominator becomes (x + 1/x) − 3.\n"
        "x² + 1/x² = 287 and x³ + 1/x³ = 17³ − 3 × 17 = 4862.\n"
        "So the value is 4862/(17 − 3) = 4862/14 = 2431/7.\n"
        "Answer: 2431/7",
    ),
    (
        "Given that x⁸ − 34x⁴ + 1 = 0 with x > 0, what is the value of (x³ + x⁻³)?",
        ["5√8", "6√6", "5√6", "6√8"],
        "5√8",
        "Divide by x⁴: x⁴ + 1/x⁴ = 34, so x² + 1/x² = 6 and x + 1/x = √8 = 2√2.\n"
        "x³ + x⁻³ = (2√2)³ − 3(2√2) = 16√2 − 6√2 = 10√2.\n"
        "10√2 = 5 × 2√2 = 5√8.\n"
        "Answer: 5√8",
    ),
    (
        "If x(x − 5) = −1, then the value of x³(x³ − 110) = ?",
        ["0", "-1", "1", "2"],
        "-1",
        "x² + 1 = 5x gives x + 1/x = 5, so x³ + 1/x³ = 125 − 15 = 110.\n"
        "Hence x⁶ + 1 = 110x³, i.e. x⁶ − 110x³ = −1.\n"
        "x³(x³ − 110) = −1.\n"
        "Answer: -1",
    ),
    (
        "If x(x − 3) = −1, then find x⁵(x² − 7)(x³ − 18).",
        ["0", "+1", "2", "-1"],
        "+1",
        "x + 1/x = 3, so x² + 1/x² = 7 and x³ + 1/x³ = 18.\n"
        "Therefore x² − 7 = −1/x² and x³ − 18 = −1/x³.\n"
        "x⁵ × (−1/x²) × (−1/x³) = 1.\n"
        "Answer: +1",
    ),
    (
        "If (0.4x + 1/x) = 5, what is the value of (0.064x³ + 1/x³)?",
        ["125", "110", "119", "105"],
        "119",
        "0.064 = 0.4³, so we need (0.4x)³ + (1/x)³ with (0.4x)(1/x) = 0.4.\n"
        "= 5³ − 3 × 0.4 × 5.\n"
        "= 125 − 6 = 119.\n"
        "Answer: 119",
    ),
    (
        "If 3x + 1/(2x) = 5, then 8x³ + 1/(27x³) = ?",
        ["946/27", "820/27", "730/27", "973/27"],
        "820/27",
        "Multiply the condition by 2/3: 2x + 1/(3x) = 10/3, and (2x)(1/(3x)) = 2/3.\n"
        "8x³ + 1/(27x³) = (10/3)³ − 3(2/3)(10/3).\n"
        "= 1000/27 − 180/27 = 820/27.\n"
        "Answer: 820/27",
    ),
    (
        "If x + 1/(16x) = 3, then the value of 16x³ + 1/(256x³) is:",
        ["423", "414", "432", "441"],
        "423",
        "With A = x and B = 1/(16x): A + B = 3 and AB = 1/16.\n"
        "A³ + B³ = 27 − 3(1/16)(3) = 27 − 9/16 = 423/16.\n"
        "16x³ + 1/(256x³) = 16(A³ + B³) = 16 × 423/16 = 423.\n"
        "Answer: 423",
    ),
    (
        "If (3x² + 1/(2x²)) = 2.5, what is the value of (27x⁶ + 1/(8x⁶))?",
        ["5.125", "6.275", "3.325", "4.375"],
        "4.375",
        "With A = 3x² and B = 1/(2x²): A + B = 2.5 and AB = 1.5.\n"
        "A³ + B³ = 2.5³ − 3 × 1.5 × 2.5.\n"
        "= 15.625 − 11.25 = 4.375.\n"
        "Answer: 4.375",
    ),
    (
        "If (y² − 1)/y = 6, then the value of (y⁶ − 1)/y³ will be:",
        ["234", "220", "254", "184"],
        "234",
        "The condition is y − 1/y = 6.\n"
        "(y⁶ − 1)/y³ = y³ − 1/y³ = 6³ + 3 × 6.\n"
        "= 216 + 18 = 234.\n"
        "Answer: 234",
    ),
    (
        "If y + 1/y = 11, then the value of y³ − 1/y³ is:",
        ["345√13", "360√13", "352√13", "368√13"],
        "360√13",
        "(y − 1/y)² = 121 − 4 = 117, so y − 1/y = 3√13.\n"
        "y³ − 1/y³ = (3√13)³ + 3(3√13) = 351√13 + 9√13.\n"
        "= 360√13.\n"
        "Answer: 360√13",
    ),
    (
        "If a − 1/(a − 5) = 18, then the value of (a − 5)³ − 1/(a − 5)³ is:",
        ["2236", "2168", "2239", "2201"],
        "2236",
        "Put y = a − 5: (y + 5) − 1/y = 18 ⇒ y − 1/y = 13.\n"
        "y³ − 1/y³ = 13³ + 3 × 13 = 2197 + 39.\n"
        "= 2236.\n"
        "Answer: 2236",
    ),
    (
        "If x^12 + 1/x^12 = 10√2, then x^36 − 1/x^36 = ?",
        ["2786", "2702", "2744", "2828"],
        "2786",
        "Let u = x^12, so u + 1/u = 10√2 and (u − 1/u)² = 200 − 4 = 196, giving u − 1/u = 14.\n"
        "u³ − 1/u³ = 14³ + 3 × 14 = 2744 + 42.\n"
        "= 2786.\n"
        "Answer: 2786",
    ),
    (
        "If x²/(x⁴ + 1) = 1/83, then find x³ − 1/x³.",
        ["718", "756", "702", "765"],
        "756",
        "Inverting: x² + 1/x² = 83, so (x − 1/x)² = 81 and x − 1/x = 9.\n"
        "x³ − 1/x³ = 9³ + 3 × 9 = 729 + 27.\n"
        "= 756.\n"
        "Answer: 756",
    ),
    (
        "If p⁴ = 4354 − 1/p⁴, then the value of p³ − 1/p³ can be:",
        ["536", "436", "416", "516"],
        "536",
        "p⁴ + 1/p⁴ = 4354, so p² + 1/p² = √4356 = 66 and (p − 1/p)² = 64.\n"
        "p − 1/p = 8, so p³ − 1/p³ = 512 + 24.\n"
        "= 536.\n"
        "Answer: 536",
    ),
    (
        "If x² − 5√5x + 1 = 0 with x > 0, then find x³ − 1/x³.",
        ["1331", "1364", "1244", "1298"],
        "1364",
        "Divide by x: x + 1/x = 5√5, so (x − 1/x)² = 125 − 4 = 121 and x − 1/x = 11.\n"
        "x³ − 1/x³ = 11³ + 3 × 11 = 1331 + 33.\n"
        "= 1364.\n"
        "Answer: 1364",
    ),
    (
        "If x = √3 − √2, then the value of x³ − x⁻³ is:",
        ["22√3", "-22√2", "22√2", "-22√3"],
        "-22√2",
        "1/x = √3 + √2, so x − 1/x = −2√2.\n"
        "x³ − 1/x³ = (−2√2)³ + 3(−2√2) = −16√2 − 6√2.\n"
        "= −22√2.\n"
        "Answer: -22√2",
    ),
    (
        "If x = (√3 + 1)/(√3 − 1) and y = (√3 − 1)/(√3 + 1), then what is the value of x³ − y³?",
        ["60", "45√3", "30√3", "90"],
        "30√3",
        "x = 2 + √3 and y = 2 − √3, so x − y = 2√3 and xy = 1.\n"
        "x³ − y³ = (x − y)³ + 3xy(x − y) = 24√3 + 6√3.\n"
        "= 30√3.\n"
        "Answer: 30√3",
    ),
    (
        "If 6x − 4/(9x) = 1, then 729x³ − 8/(27x³) = ?",
        ["41/4", "99/8", "243/8", "195/8"],
        "243/8",
        "Multiply the condition by 3/2: 9x − 2/(3x) = 3/2, with (9x)(2/(3x)) = 6.\n"
        "729x³ − 8/(27x³) = (3/2)³ + 3 × 6 × (3/2).\n"
        "= 27/8 + 27 = 243/8.\n"
        "Answer: 243/8",
    ),
    (
        "If 2x − 1/x = 3 with x ≠ 0, then simplify 8x⁶ − 25x³ − 1.",
        ["20x³", "18x³", "27x³", "34x³"],
        "20x³",
        "8x³ − 1/x³ = (2x − 1/x)³ + 3(2x)(1/x)(2x − 1/x) = 27 + 18 = 45.\n"
        "Multiplying by x³: 8x⁶ − 1 = 45x³.\n"
        "8x⁶ − 25x³ − 1 = 45x³ − 25x³ = 20x³.\n"
        "Answer: 20x³",
    ),
    (
        "If 2x − 5/(6x) = 3, then (32x³)/5 − 25/(54x³) = ?",
        ["33.6", "32", "31.5", "34.8"],
        "33.6",
        "With A = 2x and B = 5/(6x): A − B = 3 and AB = 5/3, so A³ − B³ = 27 + 3(5/3)(3) = 42.\n"
        "That is 8x³ − 125/(216x³) = 42.\n"
        "The target is 4/5 of this: (4/5) × 42 = 33.6.\n"
        "Answer: 33.6",
    ),
    (
        "If x − 1/x = 3, then what is the value of (2x⁴ + 3x³ + 13x² − 3x + 2)/(3x⁴ + 3)?",
        ["1/3", "2/3", "4/3", "5/3"],
        "4/3",
        "x − 1/x = 3 gives x² − 1 = 3x and x² + 1/x² = 11, so x⁴ + 1 = 11x².\n"
        "Numerator = 2(x⁴ + 1) + 3x(x² − 1) + 13x² = 22x² + 9x² + 13x² = 44x².\n"
        "Denominator = 3(x⁴ + 1) = 33x², so the ratio is 44/33 = 4/3.\n"
        "Answer: 4/3",
    ),
    (
        "If x² − 4x − 3 = 0, then what is the value of (x⁴ − 27/x²)/(x² + 4x − 3)?",
        ["9 1/4", "10 1/2", "9 1/8", "12 1/2"],
        "12 1/2",
        "Dividing the equation by x gives x − 3/x = 4, so x³ − 27/x³ = 4³ + 3 × 3 × 4 = 100.\n"
        "Numerator = x(x³ − 27/x³) = 100x, and since x² − 3 = 4x the denominator is 4x + 4x = 8x.\n"
        "100x/(8x) = 12.5.\n"
        "Answer: 12 1/2",
    ),
    (
        "If x² − 3x − 1 = 0, then the value of (x² + 8x − 1)(x³ + x⁻¹)⁻¹ is:",
        ["3/8", "8", "1", "3"],
        "1",
        "x² − 1 = 3x and x − 1/x = 3, so x² + 1/x² = 11.\n"
        "Numerator = (x² − 1) + 8x = 3x + 8x = 11x.\n"
        "Denominator = x³ + 1/x = x(x² + 1/x²) = 11x, so the ratio is 1.\n"
        "Answer: 1",
    ),
    (
        "If 1/a⁴ + a⁴ = 50 with a > 0, then find the value of a³ + 1/a³.",
        [
            "√(2(1 + √13)) × (−1 − 2√13)",
            "√(2(1 − √13)) × (−1 + 2√13)",
            "√(2(1 + √13)) + (−1 + 2√13)",
            "√(2(1 + √13)) × (−1 + 2√13)",
        ],
        "√(2(1 + √13)) × (−1 + 2√13)",
        "a² + 1/a² = √52 = 2√13, so a + 1/a = √(2√13 + 2) = √(2(1 + √13)).\n"
        "a³ + 1/a³ = (a + 1/a)[(a + 1/a)² − 3] = √(2(1 + √13)) × (2√13 + 2 − 3).\n"
        "= √(2(1 + √13)) × (2√13 − 1).\n"
        "Answer: √(2(1 + √13)) × (−1 + 2√13)",
    ),
    (
        "If x² − 4x + 1 = 0, then find (x³ − 26)².",
        ["545", "675", "625", "91.125"],
        "675",
        "x + 1/x = 4, so t = x³ satisfies t + 1/t = 4³ − 3 × 4 = 52, i.e. t² − 52t = −1.\n"
        "(t − 26)² = t² − 52t + 676 = −1 + 676.\n"
        "= 675.\n"
        "Answer: 675",
    ),
    (
        "If x² + x = 5, then (x + 3)³ + 1/(x + 3)³ = ?",
        ["110", "125", "140", "0"],
        "110",
        "Put y = x + 3: (y − 3)² + (y − 3) = y² − 5y + 6 = 5 ⇒ y² − 5y + 1 = 0.\n"
        "So y + 1/y = 5 and y³ + 1/y³ = 125 − 15.\n"
        "= 110.\n"
        "Answer: 110",
    ),
    (
        "If p² − 29p + 199 = 0, find (p − 11)³ − 1/(p − 11)³.",
        ["135√5", "122√5", "144√5", "126√5"],
        "144√5",
        "Put y = p − 11: (y + 11)² − 29(y + 11) + 199 = y² − 7y + 1 = 0 ⇒ y + 1/y = 7.\n"
        "y − 1/y = √(49 − 4) = 3√5.\n"
        "y³ − 1/y³ = (3√5)³ + 3(3√5) = 135√5 + 9√5 = 144√5.\n"
        "Answer: 144√5",
    ),
    (
        "If (x − a)(x − b) = 1 and a − b + 5 = 0, then (x − a)³ − 1/(x − a)³ = ?",
        ["110", "1", "125", "140"],
        "140",
        "b = a + 5, so with y = x − a we have x − b = y − 5 and y(y − 5) = 1.\n"
        "That gives y − 5 = 1/y, i.e. y − 1/y = 5.\n"
        "y³ − 1/y³ = 125 + 15 = 140.\n"
        "Answer: 140",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-3")
