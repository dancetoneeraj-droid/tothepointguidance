"""Algebra Sheet-2 (27 questions) -> maths_algebra_188 .. maths_algebra_214.

Answers are the options highlighted in the sheet; each was re-derived here.
"""

from algebra_import_lib import import_sheet

START_INDEX = 187  # maths_algebra_188

QUESTIONS = [
    (
        "If 3^x = 4^y = 12^z, then z is equal to?",
        ["xy", "x + y", "xy/(x+y)", "4x + 3"],
        "xy/(x+y)",
        "Let 3^x = 4^y = 12^z = k.\n"
        "Then 1/x = log_k 3, 1/y = log_k 4 and 1/z = log_k 12.\n"
        "Since 12 = 3 × 4: 1/z = log_k 3 + log_k 4 = 1/x + 1/y = (x + y)/xy.\n"
        "Answer: xy/(x+y)",
    ),
    (
        "If 2^x = 3^y = 18^(-z), then which option is correct?",
        ["1/x + 2/y + 1/z = 0", "2/x + 1/y + 1/z = 0", "1/x + 2/y − 1/z = 0", "1/x − 2/y + 1/z = 0"],
        "1/x + 2/y + 1/z = 0",
        "Let 2^x = 3^y = 18^(−z) = k, so 1/x = log_k 2 and 1/y = log_k 3.\n"
        "From 18^(−z) = k: −1/z = log_k 18 = log_k(2 × 3²) = log_k 2 + 2 log_k 3 = 1/x + 2/y.\n"
        "Hence 1/x + 2/y + 1/z = 0.\n"
        "Answer: 1/x + 2/y + 1/z = 0",
    ),
    (
        "If 5^a = 4^b = 100, then find 2/a + 1/b.",
        ["-1", "1", "2", "0"],
        "1",
        "1/a = log_100 5 and 1/b = log_100 4.\n"
        "2/a + 1/b = log_100 25 + log_100 4 = log_100 100 = 1.\n"
        "Answer: 1",
    ),
    (
        "If 169^a = 403^(-2b) = 961^c, then find (1/a + 1/b + 1/c)^2021.",
        ["0", "1", "2", "-1"],
        "0",
        "Note 169 = 13², 961 = 31² and 403 = 13 × 31. Let the common value be k.\n"
        "1/a = 2 log_k 13, 1/c = 2 log_k 31, and from 403^(−2b) = k, 1/b = −2(log_k 13 + log_k 31).\n"
        "So 1/a + 1/b + 1/c = 0, and 0^2021 = 0.\n"
        "Answer: 0",
    ),
    (
        "If x^(2a) = y^(2b) = z^(2c) ≠ 0 and x² = yz, then the value of (ab + bc + ca)/bc is:",
        ["3ac", "3", "3ab", "3bc"],
        "3",
        "Let x^(2a) = y^(2b) = z^(2c) = k, so log x = L/2a, log y = L/2b, log z = L/2c where L = log k.\n"
        "x² = yz gives 2 log x = log y + log z ⇒ 1/a = 1/(2b) + 1/(2c) ⇒ 2/a = 1/b + 1/c.\n"
        "(ab + bc + ca)/bc = a/c + 1 + a/b = a(1/b + 1/c) + 1 = a(2/a) + 1 = 3.\n"
        "Answer: 3",
    ),
    (
        "If a, b, c are non-zero numbers and 14^a = 36^b = 84^c, then 6b(1/c − 1/a) is equal to:",
        ["6", "3", "4", "1.5"],
        "3",
        "Let 14^a = 36^b = 84^c = k, so 1/a = log_k 14, 1/b = log_k 36, 1/c = log_k 84.\n"
        "1/c − 1/a = log_k(84/14) = log_k 6 = (1/2) log_k 36 = 1/(2b).\n"
        "So 6b × 1/(2b) = 3.\n"
        "Answer: 3",
    ),
    (
        "If 9^x = 5^y = 75^z and z = 2xy/(y + kx), then find the value of k^(1/k).",
        ["4", "2", "√2", "2^(1/3)"],
        "√2",
        "Let 9^x = 5^y = 75^z = m, so 1/x = log_m 9, 1/y = log_m 5, 1/z = log_m 75.\n"
        "75 = 3 × 5², so 1/z = log_m 3 + 2 log_m 5 = 1/(2x) + 2/y = (y + 4x)/(2xy).\n"
        "Thus z = 2xy/(y + 4x), giving k = 4.\n"
        "k^(1/k) = 4^(1/4) = √2.\n"
        "Answer: √2",
    ),
    (
        "If (5.55)^x = (0.555)^y = 1000, then the value of 1/x − 1/y is:",
        ["3", "1", "1/3", "2/3"],
        "1/3",
        "1/x = log_1000 5.55 and 1/y = log_1000 0.555.\n"
        "1/x − 1/y = log_1000 (5.55/0.555) = log_1000 10 = 1/3.\n"
        "Answer: 1/3",
    ),
    (
        "If 27^x = 343^y = 1331^z = 231, then find 123xyz/(xy + yz + zx).",
        ["31", "41", "51", "61.5"],
        "41",
        "27 = 3³, 343 = 7³, 1331 = 11³ and 231 = 3 × 7 × 11.\n"
        "1/x = 3 log_231 3, 1/y = 3 log_231 7, 1/z = 3 log_231 11, so 1/x + 1/y + 1/z = 3 log_231 231 = 3.\n"
        "123xyz/(xy + yz + zx) = 123/(1/x + 1/y + 1/z) = 123/3 = 41.\n"
        "Answer: 41",
    ),
    (
        "If the x-th root of 75 equals the y-th root of 45 equals the z-th root of 15, then which of the following statements is true?",
        ["x + y = 2z", "x − y = 3z", "x + y = 3z", "2x + 3y = 4z"],
        "x + y = 3z",
        "Let 75^(1/x) = 45^(1/y) = 15^(1/z) = k, so log 75 = x log k, log 45 = y log k, log 15 = z log k.\n"
        "Since 75 × 45 = 3375 = 15³, log 75 + log 45 = 3 log 15.\n"
        "Therefore x + y = 3z.\n"
        "Answer: x + y = 3z",
    ),
    (
        "If 3^a = 27^b = 81^c and abc = 144, then the value of 12(1/a + 1/(2b) + 1/(5c)) is:",
        ["18/120", "18/10", "33/10", "17/120"],
        "33/10",
        "3^a = 3^(3b) = 3^(4c) gives a = 3b = 4c, so take a = 12t, b = 4t, c = 3t.\n"
        "abc = 144t³ = 144 ⇒ t = 1, hence a = 12, b = 4, c = 3.\n"
        "12(1/12 + 1/8 + 1/15) = 12 × 33/120 = 33/10.\n"
        "Answer: 33/10",
    ),
    (
        "A and B are positive integers. If A + B + AB = 186, then what is the difference between A and B (A, B ≤ 20)?",
        ["7", "8", "5", "6"],
        "6",
        "A + B + AB = 186 ⇒ (A + 1)(B + 1) = 187 = 11 × 17.\n"
        "So A + 1 = 11 and B + 1 = 17, giving A = 10 and B = 16.\n"
        "Difference = 16 − 10 = 6.\n"
        "Answer: 6",
    ),
    (
        "If x + y + xy = 0, y + z + yz = 3 and z + x + zx = 8, then find 12xyz.",
        ["-8", "-5", "-10", "-15"],
        "-10",
        "The equations become (1+x)(1+y) = 1, (1+y)(1+z) = 4 and (1+z)(1+x) = 9.\n"
        "Multiplying: [(1+x)(1+y)(1+z)]² = 36 ⇒ (1+x)(1+y)(1+z) = 6.\n"
        "So 1+z = 6/1 = 6, 1+x = 6/4 = 1.5, 1+y = 6/9 = 2/3, i.e. z = 5, x = 0.5, y = −1/3.\n"
        "xyz = 0.5 × (−1/3) × 5 = −5/6, so 12xyz = −10.\n"
        "Answer: -10",
    ),
    (
        "If a² + b² = 25, x² + y² = 17 and ax + by = 8, then ay − bx = ?",
        ["20", "17", "18", "19"],
        "19",
        "Using the identity (a² + b²)(x² + y²) = (ax + by)² + (ay − bx)².\n"
        "25 × 17 = 425 = 8² + (ay − bx)² = 64 + (ay − bx)².\n"
        "(ay − bx)² = 361 ⇒ ay − bx = 19.\n"
        "Answer: 19",
    ),
    (
        "Let a, b, x, y be real numbers such that a² + b² = 25, x² + y² = 169, and ax + by = 65. If k = ay − bx, then:",
        ["k = 0", "0 < k < 5/13", "k > 5/13", "k = 5/13"],
        "k = 0",
        "(a² + b²)(x² + y²) = (ax + by)² + (ay − bx)².\n"
        "25 × 169 = 4225 and 65² = 4225, so (ay − bx)² = 0.\n"
        "Hence k = 0.\n"
        "Answer: k = 0",
    ),
    (
        "If x = (√19 + √13)/(√19 − √13) and y = (√19 − √13)/(√19 + √13), then 1/(x³ + 1) + 1/(y³ + 1) = ?",
        ["8", "4", "1", "2"],
        "1",
        "x and y are reciprocals, so y = 1/x.\n"
        "1/(y³ + 1) = 1/(1/x³ + 1) = x³/(1 + x³).\n"
        "Sum = 1/(x³ + 1) + x³/(x³ + 1) = (1 + x³)/(1 + x³) = 1.\n"
        "Answer: 1",
    ),
    (
        "If a = (13 + 2√42) and b = √(13 − 2√42), then find 1/(a⁸ + 1) + 1/(b¹⁶ + 1).",
        ["8", "4", "1", "2"],
        "1",
        "(13 + 2√42)(13 − 2√42) = 169 − 168 = 1, so 13 − 2√42 = 1/a.\n"
        "Then b = a^(−1/2) and b¹⁶ = a^(−8) = 1/a⁸.\n"
        "1/(a⁸ + 1) + 1/(1/a⁸ + 1) = 1/(a⁸ + 1) + a⁸/(a⁸ + 1) = 1.\n"
        "Answer: 1",
    ),
    (
        "If a(7 + 4√3) = b(7 − 4√3) = 1, then the value of 1/(a⁵ + 1) + 1/(b⁵ + 1) is:",
        ["4", "3", "7", "1"],
        "1",
        "a = 1/(7 + 4√3) = 7 − 4√3 and b = 1/(7 − 4√3) = 7 + 4√3, so ab = 1.\n"
        "With b = 1/a: 1/(b⁵ + 1) = a⁵/(1 + a⁵).\n"
        "Sum = 1/(a⁵ + 1) + a⁵/(a⁵ + 1) = 1.\n"
        "Answer: 1",
    ),
    (
        "If tanθ = 2019/2018, then 1/(1 + tan^2017 θ) + 1/(1 + cot^2017 θ) = ?",
        ["0", "1", "4", "2"],
        "1",
        "Put t = tan^2017 θ, so cot^2017 θ = 1/t.\n"
        "1/(1 + t) + 1/(1 + 1/t) = 1/(1 + t) + t/(1 + t) = 1.\n"
        "The value of tanθ does not matter.\n"
        "Answer: 1",
    ),
    (
        "Find the value of 1/(10⁻⁹ + 1) + 1/(10⁻⁸ + 1) + ... + 1/(10⁸ + 1) + 1/(10⁹ + 1).",
        ["9", "8", "9.5", "10"],
        "9.5",
        "Pair the terms with exponents n and −n: 1/(10ⁿ + 1) + 1/(10⁻ⁿ + 1) = 1.\n"
        "For n = 1 to 9 there are 9 such pairs contributing 9.\n"
        "The middle term (n = 0) is 1/(1 + 1) = 0.5.\n"
        "Total = 9 + 0.5 = 9.5.\n"
        "Answer: 9.5",
    ),
    (
        "If p + 1/p = 112, then the value of (p − 112)^15 + (1/p)^15 will be:",
        ["0", "1", "112", "-1"],
        "0",
        "From p + 1/p = 112 we get p − 112 = −1/p.\n"
        "So (p − 112)^15 = (−1/p)^15 = −(1/p)^15 since 15 is odd.\n"
        "Sum = −(1/p)^15 + (1/p)^15 = 0.\n"
        "Answer: 0",
    ),
    (
        "If (11 − 13x)/x + (11 − 13y)/y + (11 − 13z)/z = 5, then what is the value of 1/x + 1/y + 1/z?",
        ["5", "13/11", "13/5", "4"],
        "4",
        "Each term splits as 11/x − 13, so the sum is 11(1/x + 1/y + 1/z) − 39.\n"
        "11(1/x + 1/y + 1/z) − 39 = 5 ⇒ 11(1/x + 1/y + 1/z) = 44.\n"
        "1/x + 1/y + 1/z = 4.\n"
        "Answer: 4",
    ),
    (
        "If x + 4√3/x = 5, then (x² + 7x + 4√3)/(x²(5 − x)) = ?",
        ["√3", "2√3", "3√3", "2"],
        "√3",
        "From x + 4√3/x = 5 we get x² + 4√3 = 5x, and also 5 − x = 4√3/x.\n"
        "Numerator = (x² + 4√3) + 7x = 5x + 7x = 12x.\n"
        "Denominator = x² × 4√3/x = 4√3·x.\n"
        "Ratio = 12x/(4√3·x) = 3/√3 = √3.\n"
        "Answer: √3",
    ),
    (
        "If (3x + 4y)(5x − 6y) = ax² + 2hxy + by², then what is the value of (4a − h + 2b)?",
        ["13", "107", "108", "11"],
        "11",
        "(3x + 4y)(5x − 6y) = 15x² − 18xy + 20xy − 24y² = 15x² + 2xy − 24y².\n"
        "So a = 15, 2h = 2 ⇒ h = 1, and b = −24.\n"
        "4a − h + 2b = 60 − 1 − 48 = 11.\n"
        "Answer: 11",
    ),
    (
        "The identity 4(z + 7)(2z − 1) = Az² + Bz + C holds for all real values of z. Find the value of A² − B − C.",
        ["-16", "40", "36", "16"],
        "40",
        "4(z + 7)(2z − 1) = 4(2z² + 13z − 7) = 8z² + 52z − 28.\n"
        "So A = 8, B = 52, C = −28.\n"
        "A² − B − C = 64 − 52 + 28 = 40.\n"
        "Answer: 40",
    ),
    (
        "If (2x + 3y + 4)(2x + 3y − 5) is equivalent to (ax² + by² + 2hxy + 2gx + 2fy + C), then what is the value of {(g + f − C)/abh}?",
        ["37/216", "19/216", "19/108", "35/432"],
        "35/432",
        "Put u = 2x + 3y: (u + 4)(u − 5) = u² − u − 20 = 4x² + 12xy + 9y² − 2x − 3y − 20.\n"
        "Comparing: a = 4, b = 9, h = 6, g = −1, f = −1.5, C = −20.\n"
        "(g + f − C)/(abh) = (−1 − 1.5 + 20)/(4 × 9 × 6) = 17.5/216 = 35/432.\n"
        "Answer: 35/432",
    ),
    (
        "If (a + 1)/a = k, then find the value of (a² − 1)/a².",
        ["k − 2k²", "k² + 2", "k + 2", "2k − k²"],
        "2k − k²",
        "(a + 1)/a = 1 + 1/a = k, so 1/a = k − 1.\n"
        "(a² − 1)/a² = 1 − 1/a² = 1 − (k − 1)².\n"
        "= 1 − (k² − 2k + 1) = 2k − k².\n"
        "Answer: 2k − k²",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-2")
