"""Algebra Sheet-4 -> maths_algebra_343 .. maths_algebra_426.

Sheet-4 prints no answer key, so every answer here was derived from scratch.

Two items on the sheet are not MCQs and are skipped: Q15 and Q35 are multi-part
drills ((i)…(vii) sub-questions) printed without any options.

Two places where the sheet itself is defective and the derivation decides:
  Q79 - (x+5)(x+6) + 9/(x(x−1)) = 0 groups as [x(x+5)][(x−1)(x+6)] = −9, i.e.
        u(u−6) = −9 with u = x²+5x, so u = 3 and 2x²+10x+7 = 13. None of the
        printed options is 13, so the stray option 17 is replaced by 13.
  Q85 - the sheet prints 2abc/(ab+bc−ac) as both option [a] and option [d];
        the duplicate is replaced by 2abc/(ab+bc+ca) to keep four distinct
        options. The correct answer, 2abc/(ac+bc−ab), is unaffected.
"""

from algebra_import_lib import import_sheet

START_INDEX = 342  # maths_algebra_343

QUESTIONS = [
    (
        "If x² − √8x + 1 = 0, then the value of (x⁴ − 1/x⁴) is:",
        ["24√6", "24√2", "20√2", "20√6"],
        "24√2",
        "Divide by x: x + 1/x = √8 = 2√2, so (x − 1/x)² = 8 − 4 = 4 and x − 1/x = 2.\n"
        "x² + 1/x² = 6 and x² − 1/x² = 2√2 × 2 = 4√2.\n"
        "x⁴ − 1/x⁴ = 6 × 4√2 = 24√2.\n"
        "Answer: 24√2",
    ),
    (
        "If (x − 1/x) = √6 and x > 1, then what is the value of (x⁸ − 1/x⁸)?",
        ["1024√15", "992√15", "998√15", "1012√15"],
        "992√15",
        "x + 1/x = √(6 + 4) = √10, so x² − 1/x² = √6 × √10 = 2√15 and x² + 1/x² = 8.\n"
        "x⁴ − 1/x⁴ = 8 × 2√15 = 16√15 and x⁴ + 1/x⁴ = 64 − 2 = 62.\n"
        "x⁸ − 1/x⁸ = 62 × 16√15 = 992√15.\n"
        "Answer: 992√15",
    ),
    (
        "If x² − 2√5x + 1 = 0, then what is the value of x⁵ + 1/x⁵?",
        ["408√5", "610√5", "406√5", "612√5"],
        "610√5",
        "x + 1/x = 2√5, so x² + 1/x² = 18 and x³ + 1/x³ = 40√5 − 6√5 = 34√5.\n"
        "x⁵ + 1/x⁵ = (x² + 1/x²)(x³ + 1/x³) − (x + 1/x) = 18 × 34√5 − 2√5.\n"
        "= 612√5 − 2√5 = 610√5.\n"
        "Answer: 610√5",
    ),
    (
        "If X = 4 − 1/(4 − 1/(4 − 1/(4 − …))) continuing to infinity, then find X⁵ + 1/X⁵.",
        ["656", "548", "732", "724"],
        "724",
        "The continued fraction satisfies X = 4 − 1/X, so X + 1/X = 4.\n"
        "X² + 1/X² = 14 and X³ + 1/X³ = 64 − 12 = 52.\n"
        "X⁵ + 1/X⁵ = 14 × 52 − 4 = 728 − 4 = 724.\n"
        "Answer: 724",
    ),
    (
        "If x − 1/x = −6, what will be the value of x⁵ − 1/x⁵?",
        ["-8898", "-8896", "-8886", "-8892"],
        "-8886",
        "x² + 1/x² = 36 + 2 = 38 and x³ − 1/x³ = (−6)³ + 3(−6) = −234.\n"
        "x⁵ − 1/x⁵ = (x² + 1/x²)(x³ − 1/x³) − (x − 1/x) = 38 × (−234) + 6.\n"
        "= −8892 + 6 = −8886.\n"
        "Answer: -8886",
    ),
    (
        "If x² + 13x + 39 = 0, then (x + 8)⁵ − 1/(x + 8)⁵ = ?",
        ["393", "396", "392", "394"],
        "393",
        "Put y = x + 8: (y − 8)² + 13(y − 8) + 39 = y² − 3y − 1 = 0, so y − 1/y = 3.\n"
        "y² + 1/y² = 11 and y³ − 1/y³ = 27 + 9 = 36.\n"
        "y⁵ − 1/y⁵ = 11 × 36 − 3 = 393.\n"
        "Answer: 393",
    ),
    (
        "If x² − 4x + 1 = 0, then what is the value of (x⁶ + x⁻⁶)?",
        ["2786", "2702", "2716", "2744"],
        "2702",
        "x + 1/x = 4, so x² + 1/x² = 14 and x³ + 1/x³ = 64 − 12 = 52.\n"
        "x⁶ + 1/x⁶ = 52² − 2.\n"
        "= 2702.\n"
        "Answer: 2702",
    ),
    (
        "If x + 1/x = 7, then the value of x⁶ + 1/x⁶ is:",
        ["113682", "103682", "103882", "103862"],
        "103682",
        "x³ + 1/x³ = 343 − 21 = 322.\n"
        "x⁶ + 1/x⁶ = 322² − 2 = 103684 − 2.\n"
        "= 103682.\n"
        "Answer: 103682",
    ),
    (
        "If (a + 1/a) = 7√3, then what is the value of (a⁶ + a⁻⁶)?",
        ["3048190", "3048542", "3048132", "3048625"],
        "3048190",
        "a³ + 1/a³ = (7√3)³ − 3(7√3) = 1029√3 − 21√3 = 1008√3.\n"
        "a⁶ + 1/a⁶ = (1008√3)² − 2 = 1008² × 3 − 2.\n"
        "= 3048192 − 2 = 3048190.\n"
        "Answer: 3048190",
    ),
    (
        "If (x − 1/x = 4), then what is the value of (x⁶ + 1/x⁶)?",
        ["4689", "4786", "5832", "5778"],
        "5778",
        "x³ − 1/x³ = 4³ + 3 × 4 = 76.\n"
        "x⁶ + 1/x⁶ = (x³ − 1/x³)² + 2 = 5776 + 2.\n"
        "= 5778.\n"
        "Answer: 5778",
    ),
    (
        "If (x + 1/x) = 5√2 and x > 1, what is the value of (x⁶ − 1/x⁶)?",
        ["22970√23", "23030√23", "23060√23", "22960√23"],
        "23030√23",
        "x − 1/x = √(50 − 4) = √46, so x³ + 1/x³ = 250√2 − 15√2 = 235√2.\n"
        "x³ − 1/x³ = (√46)³ + 3√46 = 49√46.\n"
        "x⁶ − 1/x⁶ = 235√2 × 49√46 = 11515√92 = 23030√23.\n"
        "Answer: 23030√23",
    ),
    (
        "If x > 0 and x⁴ + 1/x⁴ = 2207, then find x⁷ + 1/x⁷.",
        ["710649", "710647", "710654", "710661"],
        "710647",
        "x² + 1/x² = √2209 = 47 and x + 1/x = √49 = 7, so x³ + 1/x³ = 322.\n"
        "x⁷ + 1/x⁷ = (x³ + 1/x³)(x⁴ + 1/x⁴) − (x + 1/x) = 322 × 2207 − 7.\n"
        "= 710654 − 7 = 710647.\n"
        "Answer: 710647",
    ),
    (
        "If x⁵ − 1/x⁵ = √7, then find x³⁵ − 1/x³⁵.",
        ["791√7", "789√7", "790√7", "792√7"],
        "791√7",
        "With u = x⁵: u − 1/u = √7, so u² + 1/u² = 9, u³ − 1/u³ = 7√7 + 3√7 = 10√7 and u⁴ + 1/u⁴ = 79.\n"
        "u⁷ − 1/u⁷ = (u³ − 1/u³)(u⁴ + 1/u⁴) + (u − 1/u) = 10√7 × 79 + √7.\n"
        "= 791√7.\n"
        "Answer: 791√7",
    ),
    (
        "If x + 1/x = 4, then x⁷ − 1/x⁷ = ?",
        ["5844√3", "5842√3", "5824√3", "5822√3"],
        "5822√3",
        "x − 1/x = √12 = 2√3, x² + 1/x² = 14 and x⁴ + 1/x⁴ = 194.\n"
        "x³ − 1/x³ = (2√3)³ + 3(2√3) = 30√3.\n"
        "x⁷ − 1/x⁷ = (x³ − 1/x³)(x⁴ + 1/x⁴) + (x − 1/x) = 30√3 × 194 + 2√3 = 5822√3.\n"
        "Answer: 5822√3",
    ),
    (
        "If x + 1/x ≠ 0 and x³ + 1/x³ = 0, then the value of (x + 1/x)⁴ is:",
        ["9", "12", "15", "16"],
        "9",
        "Let t = x + 1/x. Then x³ + 1/x³ = t³ − 3t = 0, so t(t² − 3) = 0.\n"
        "Since t ≠ 0, t² = 3.\n"
        "t⁴ = 9.\n"
        "Answer: 9",
    ),
    (
        "If x² + x(6 − √3) + 10 − 3√3 = 0, then find the value of (x + 3)^17 + 1/(x + 3)^17.",
        ["√3", "−√3", "1", "-1"],
        "−√3",
        "Put y = x + 3: (y − 3)² + (y − 3)(6 − √3) + 10 − 3√3 = y² − √3y + 1 = 0.\n"
        "So y + 1/y = √3 = 2cos(π/6), giving y = e^(±iπ/6) with period 12.\n"
        "17 mod 12 = 5, so the value is 2cos(5π/6) = −√3.\n"
        "Answer: −√3",
    ),
    (
        "If x² − 3x + 1 = 0, then find the value of x⁹ + x⁷ + x⁻⁹ + x⁻⁷.",
        ["6621", "4414", "9208", "6069"],
        "6621",
        "x + 1/x = 3, so with Sₙ = xⁿ + 1/xⁿ the recurrence Sₙ = 3Sₙ₋₁ − Sₙ₋₂ gives\n"
        "S₂ = 7, S₃ = 18, S₄ = 47, S₅ = 123, S₆ = 322, S₇ = 843, S₈ = 2207, S₉ = 5778.\n"
        "S₉ + S₇ = 5778 + 843 = 6621.\n"
        "Answer: 6621",
    ),
    (
        "If x² − 4x + 1 = 0, then what is the value of x⁹ + x⁷ − 194x⁵ − 194x³?",
        ["4", "-4", "1", "-1"],
        "-4",
        "Factor: x³(x² + 1)(x⁴ − 194), and x² + 1 = 4x from the equation.\n"
        "x + 1/x = 4 gives x² + 1/x² = 14 and x⁴ + 1/x⁴ = 194, so x⁴ − 194 = −1/x⁴.\n"
        "The expression = x³ × 4x × (−1/x⁴) = −4.\n"
        "Answer: -4",
    ),
    (
        "If x² − 3x + 1 = 0, then what is the value of x¹² + x⁸ − 123x⁷ − 123x³?",
        ["7", "-3", "-7", "3"],
        "-7",
        "Factor: x³(x⁴ + 1)(x⁵ − 123).\n"
        "x + 1/x = 3 gives x² + 1/x² = 7, so x⁴ + 1 = 7x², and x⁵ + 1/x⁵ = 123 so x⁵ − 123 = −1/x⁵.\n"
        "The expression = x³ × 7x² × (−1/x⁵) = −7.\n"
        "Answer: -7",
    ),
    (
        "If x³ − 1/x³ = √(k² − 4)(k² − 1), then x² − 1/x² = ?",
        ["k√(k² − 4)", "k√(k² + 4)", "k(k² − 4)", "k(k² + 4)"],
        "k√(k² − 4)",
        "If x + 1/x = k then x − 1/x = √(k² − 4) and x³ − 1/x³ = (x − 1/x)[(x − 1/x)² + 3] = √(k² − 4)(k² − 1), matching the given form.\n"
        "So x + 1/x = k.\n"
        "x² − 1/x² = (x + 1/x)(x − 1/x) = k√(k² − 4).\n"
        "Answer: k√(k² − 4)",
    ),
    (
        "If x√x + 3√x + 1/a³ − a³ = 0, then find (a² + 1/a² − x).",
        ["3", "2", "1", "4"],
        "2",
        "Rewrite as t³ + 3t = a³ − 1/a³ with t = √x, and a³ − 1/a³ = u³ + 3u where u = a − 1/a.\n"
        "Since z³ + 3z is strictly increasing, t = u, so x = (a − 1/a)² = a² + 1/a² − 2.\n"
        "Therefore a² + 1/a² − x = 2.\n"
        "Answer: 2",
    ),
    (
        "If x − 1/x = 1, then [1/(x − 1) − 1/(x + 1) + 1/(x² + 1) − 1/(x² − 1)] = ?",
        ["±√5", "2/5", "±2/√5", "±√5/2"],
        "±2/√5",
        "x² − x − 1 = 0, so x² − 1 = x and x⁴ = 3x + 2.\n"
        "1/(x − 1) − 1/(x + 1) = 2/(x² − 1) = 2/x, and 1/(x² + 1) − 1/(x² − 1) = −2/(x⁴ − 1) = −2/(3x + 1).\n"
        "With x = (1 ± √5)/2 the total 2/x − 2/(3x + 1) evaluates to ±2/√5.\n"
        "Answer: ±2/√5",
    ),
    (
        "If x√x + 1/(x√x) = 110, then find x²√x + 1/(x²√x).",
        ["2525", "12098", "140", "3645"],
        "2525",
        "With t = √x the condition is t³ + 1/t³ = 110, and t + 1/t = 5 since 125 − 15 = 110.\n"
        "Using Sₙ = 5Sₙ₋₁ − Sₙ₋₂: S₂ = 23, S₃ = 110, S₄ = 527, S₅ = 2525.\n"
        "x²√x + 1/(x²√x) = t⁵ + 1/t⁵ = 2525.\n"
        "Answer: 2525",
    ),
    (
        "If x + 1/x = 4 and x > 0, then find the value of x¹⁰ + 1/x¹⁰.",
        ["524176", "524174", "524172", "524178"],
        "524174",
        "Using Sₙ = 4Sₙ₋₁ − Sₙ₋₂ with S₀ = 2, S₁ = 4:\n"
        "S₂ = 14, S₃ = 52, S₄ = 194, S₅ = 724, S₆ = 2702, S₇ = 10084, S₈ = 37634, S₉ = 140452.\n"
        "S₁₀ = 4 × 140452 − 37634 = 524174.\n"
        "Answer: 524174",
    ),
    (
        "If K + 1/K − 2 = 0 and K > 0, then what is the value of K¹⁷ + 1/K¹²?",
        ["2", "1", "0", "12"],
        "2",
        "K + 1/K = 2 forces K = 1.\n"
        "K¹⁷ + 1/K¹² = 1 + 1.\n"
        "= 2.\n"
        "Answer: 2",
    ),
    (
        "If x + 1/x = 2, then the value of x¹¹ + 1/x²⁰ is:",
        ["7", "2", "1", "0"],
        "2",
        "x + 1/x = 2 forces x = 1.\n"
        "x¹¹ + 1/x²⁰ = 1 + 1.\n"
        "= 2.\n"
        "Answer: 2",
    ),
    (
        "If x + 1/(x − 9) = 11, then (x − 11)¹² + 1/(x − 11)¹³ = ?",
        ["0", "2", "-2", "1"],
        "0",
        "Subtract 9 from both sides: (x − 9) + 1/(x − 9) = 2, so x − 9 = 1 and x = 10.\n"
        "x − 11 = −1, so (−1)¹² = 1 and 1/(−1)¹³ = −1.\n"
        "The sum is 0.\n"
        "Answer: 0",
    ),
    (
        "If a + 1/(a − 4) = 6, then (a − 3)⁷ + 1/(a − 7)³ = ?",
        ["63 7/8", "255 1/8", "127 7/8", "216"],
        "127 7/8",
        "Subtract 4: (a − 4) + 1/(a − 4) = 2, so a − 4 = 1 and a = 5.\n"
        "(a − 3)⁷ = 2⁷ = 128 and (a − 7)³ = (−2)³ = −8, so 1/(a − 7)³ = −1/8.\n"
        "128 − 1/8 = 127 7/8.\n"
        "Answer: 127 7/8",
    ),
    (
        "If x + 1/x = −2, then x^(2n+1) + 1/x^(2n+4) = ? (where n is an integer)",
        ["2", "4", "-2", "0"],
        "0",
        "x + 1/x = −2 forces x = −1.\n"
        "2n + 1 is odd so x^(2n+1) = −1, and 2n + 4 is even so 1/x^(2n+4) = 1.\n"
        "The sum is 0.\n"
        "Answer: 0",
    ),
    (
        "If K + 1/K + 2 = 0 and K < 0, then what is the value of K¹⁷ + 1/K¹¹?",
        ["-17", "-2", "-1", "0"],
        "-2",
        "K + 1/K = −2 forces K = −1.\n"
        "K¹⁷ = −1 and 1/K¹¹ = 1/(−1) = −1.\n"
        "The sum is −2.\n"
        "Answer: -2",
    ),
    (
        "If x + 1/(x + 5) = −7, then (x + 5)¹⁹ − 1/(x + 7)²⁸ = ?",
        ["0", "2", "-2", "1"],
        "-2",
        "Add 5: (x + 5) + 1/(x + 5) = −2, so x + 5 = −1 and x = −6.\n"
        "(x + 5)¹⁹ = (−1)¹⁹ = −1, and x + 7 = 1 so 1/(x + 7)²⁸ = 1.\n"
        "−1 − 1 = −2.\n"
        "Answer: -2",
    ),
    (
        "If 3x + 1/(3x) + 2 = 0, then 243x⁷ + 1/(81x²) = ?",
        ["2", "4", "0", "1"],
        "0",
        "3x + 1/(3x) = −2 forces 3x = −1, i.e. x = −1/3.\n"
        "243x⁷ = 243 × (−1/2187) = −1/9 and 81x² = 9, so 1/(81x²) = 1/9.\n"
        "−1/9 + 1/9 = 0.\n"
        "Answer: 0",
    ),
    (
        "If x/5 + 5/x = −2, then what is the value of x³?",
        ["-125", "-25", "1/125", "625"],
        "-125",
        "With u = x/5: u + 1/u = −2 forces u = −1, so x = −5.\n"
        "x³ = (−5)³.\n"
        "= −125.\n"
        "Answer: -125",
    ),
    (
        "If x/y + y/x = 1 with x, y ≠ 0, then find the value of x⁶ + y⁶ + 2x³y³.",
        ["0", "1", "x³y³", "3x³y³"],
        "0",
        "x/y + y/x = 1 gives x² + y² = xy, i.e. x² − xy + y² = 0.\n"
        "So x³ + y³ = (x + y)(x² − xy + y²) = 0.\n"
        "x⁶ + y⁶ + 2x³y³ = (x³ + y³)² = 0.\n"
        "Answer: 0",
    ),
    (
        "If r/13 + 13/r = 1, then the value of r³ is:",
        ["-2157", "2197", "2157", "-2197"],
        "-2197",
        "With u = r/13: u + 1/u = 1 gives u² − u + 1 = 0, hence u³ = −1.\n"
        "r³ = (13u)³ = 2197u³.\n"
        "= −2197.\n"
        "Answer: -2197",
    ),
    (
        "If x + 1/x = 1, then (1 + x + x²)(1 − x − x²) = ?",
        ["0", "4", "-2", "1"],
        "4",
        "x² − x + 1 = 0, so x² = x − 1.\n"
        "1 + x + x² = 1 + x + x − 1 = 2x, and 1 − x − x² = 1 − x − x + 1 = 2 − 2x.\n"
        "Product = 2x(2 − 2x) = 4x − 4x² = 4x − 4(x − 1) = 4.\n"
        "Answer: 4",
    ),
    (
        "If 4x² + 1/x² = 2, then find 8x³ + 1/x³.",
        ["0", "1", "2", "4"],
        "0",
        "(2x + 1/x)² = 4x² + 4 + 1/x² = 6, so 2x + 1/x = √6.\n"
        "8x³ + 1/x³ = (2x + 1/x)³ − 3(2x)(1/x)(2x + 1/x) = 6√6 − 6√6.\n"
        "= 0.\n"
        "Answer: 0",
    ),
    (
        "If x + 1/x = 1, then the value of x¹² + x⁹ + x⁶ + x³ + 1 is:",
        ["1", "-1", "0", "-2"],
        "1",
        "x² − x + 1 = 0 means x³ + 1 = (x + 1)(x² − x + 1) = 0, so x³ = −1.\n"
        "x⁶ = 1, x⁹ = −1, x¹² = 1.\n"
        "1 − 1 + 1 − 1 + 1 = 1.\n"
        "Answer: 1",
    ),
    (
        "If x⁵ + 1/x⁵ = 1, then x¹⁸⁰ + x¹⁶⁵ + x¹⁴⁵ + x¹³⁰ − 2x¹⁰⁵ + x⁸⁰ + x⁷⁰ − x¹⁵ + 3 = ?",
        ["3", "6", "4", "5"],
        "5",
        "With u = x⁵: u + 1/u = 1 gives u³ = −1 and u² = u − 1.\n"
        "Reducing each power: x¹⁸⁰ = 1, x¹⁶⁵ = −1, x¹⁴⁵ = −u², x¹³⁰ = u², −2x¹⁰⁵ = 2, x⁸⁰ = −u, x⁷⁰ = u², −x¹⁵ = 1.\n"
        "Total = 6 + u² − u = 6 − 1 = 5.\n"
        "Answer: 5",
    ),
    (
        "If (x + 2)² + 1/[(x + 2)(x + 3) − (x + 1)] = 0, then find (x² + 4x + 5)³.",
        ["0", "1", "-1", "343"],
        "-1",
        "(x + 2)(x + 3) − (x + 1) = x² + 4x + 5 = (x + 2)² + 1, so with y = (x + 2)² the equation is y + 1/(y + 1) = 0.\n"
        "That gives y² + y + 1 = 0, hence y + 1 = −y² and y³ = 1.\n"
        "(x² + 4x + 5)³ = (y + 1)³ = −y⁶ = −1.\n"
        "Answer: -1",
    ),
    (
        "If x + 3/x = 3, then find (x − 1)⁸ + 1/(x − 1)⁸.",
        ["1", "-1", "2", "0"],
        "-1",
        "x² − 3x + 3 = 0; put y = x − 1 to get y² − y + 1 = 0, so y + 1/y = 1 and y³ = −1.\n"
        "y⁶ = 1, so y⁸ = y² and 1/y⁸ = 1/y².\n"
        "y² + 1/y² = 1² − 2 = −1.\n"
        "Answer: -1",
    ),
    (
        "If x/(5√6) + 1 = −5√6/x, then find the value of x⁵ − 750√6x² + 1.",
        ["25√6", "1", "0", "1+5√6"],
        "1",
        "With u = x/(5√6) the equation is u + 1 = −1/u, i.e. u² + u + 1 = 0, so u³ = 1.\n"
        "Then x³ = (5√6)³u³ = 750√6, so x³ − 750√6 = 0.\n"
        "x⁵ − 750√6x² + 1 = x²(x³ − 750√6) + 1 = 1.\n"
        "Answer: 1",
    ),
    (
        "If x² − 7x + 13 = 0, then (x − 3)²² + 1/(x − 3)²² = ?",
        ["3", "1", "-1", "-2"],
        "-1",
        "Put y = x − 3: (y + 3)² − 7(y + 3) + 13 = y² − y + 1 = 0, so y + 1/y = 1 and y³ = −1.\n"
        "y⁶ = 1 and 22 mod 6 = 4, so y²² = y⁴ = −y and 1/y²² = −1/y.\n"
        "y²² + 1/y²² = −(y + 1/y) = −1.\n"
        "Answer: -1",
    ),
    (
        "If a/b + b/a = −1 and a − b = 2, then the value of a³ − b³ is:",
        ["0", "1/2", "1", "-1"],
        "0",
        "a/b + b/a = −1 gives a² + b² = −ab, i.e. a² + ab + b² = 0.\n"
        "a³ − b³ = (a − b)(a² + ab + b²) = 2 × 0.\n"
        "= 0.\n"
        "Answer: 0",
    ),
    (
        "If 3x + 1/(2x) = √3, then find 6x² + 1/(6x²).",
        ["-1", "0", "2", "1"],
        "0",
        "Squaring: 9x² + 3 + 1/(4x²) = 3, so 9x² + 1/(4x²) = 0.\n"
        "Multiplying by 2/3 turns 9x² into 6x² and 1/(4x²) into 1/(6x²).\n"
        "So 6x² + 1/(6x²) = (2/3) × 0 = 0.\n"
        "Answer: 0",
    ),
    (
        "If 5x + 1/(2x) = √5, then find 50x⁴ + 1/(100x⁴).",
        ["-1", "-1/2", "-4/3", "-3/2"],
        "-3/2",
        "Squaring: 25x² + 5 + 1/(4x²) = 5, so 25x² = −1/(4x²) and hence x⁴ = −1/100.\n"
        "50x⁴ = −1/2 and 1/(100x⁴) = 1/(−1) = −1.\n"
        "Sum = −1/2 − 1 = −3/2.\n"
        "Answer: -3/2",
    ),
    (
        "If x² + y² = x⁻²(777 − y⁴) and x + y = x⁻¹(37 − y²), then find the value of x² + y(y − x).",
        ["29", "21", "23", "31"],
        "21",
        "The second condition gives x² + xy + y² = 37; the first gives x⁴ + x²y² + y⁴ = 777.\n"
        "Since x⁴ + x²y² + y⁴ = (x² + xy + y²)(x² − xy + y²), we get 37(x² − xy + y²) = 777.\n"
        "x² − xy + y² = 21, which is exactly x² + y(y − x).\n"
        "Answer: 21",
    ),
    (
        "If x² − xy + y² = 13 and x² + xy + y² = 37, then the value of (x⁶ − y⁶)/(x² − y²) is:",
        ["481", "500", "520", "444"],
        "481",
        "(x⁶ − y⁶)/(x² − y²) = x⁴ + x²y² + y⁴.\n"
        "= (x² − xy + y²)(x² + xy + y²) = 13 × 37.\n"
        "= 481.\n"
        "Answer: 481",
    ),
    (
        "If x⁴ + x²y² + y⁴ = 273 and x² − xy + y² = 13, then the value of xy is:",
        ["4", "10", "6", "8"],
        "4",
        "x⁴ + x²y² + y⁴ = (x² − xy + y²)(x² + xy + y²), so 13(x² + xy + y²) = 273 and x² + xy + y² = 21.\n"
        "Subtracting the two expressions: 2xy = 21 − 13 = 8.\n"
        "xy = 4.\n"
        "Answer: 4",
    ),
    (
        "If x⁴ + y⁴ + x²y² = 117 and x² + y² − xy = 3(4 + √3), then find x² + y².",
        ["9", "6√3", "12", "13√3"],
        "12",
        "x⁴ + x²y² + y⁴ = (x² − xy + y²)(x² + xy + y²), so 3(4 + √3)(x² + xy + y²) = 117.\n"
        "x² + xy + y² = 39/(4 + √3) = 3(4 − √3).\n"
        "x² + y² = [3(4 + √3) + 3(4 − √3)]/2 = 24/2 = 12.\n"
        "Answer: 12",
    ),
    (
        "If x² − xy + y² = 17 and x⁴ + x²y² + y⁴ = 425, then the value of x/y + y/x is:",
        ["6.25", "5.25", "6.4", "5.5"],
        "5.25",
        "425 = 17(x² + xy + y²), so x² + xy + y² = 25.\n"
        "x² + y² = (17 + 25)/2 = 21 and xy = (25 − 17)/2 = 4.\n"
        "x/y + y/x = 21/4 = 5.25.\n"
        "Answer: 5.25",
    ),
    (
        "If x² − xy + y² = 7 and x⁴ + x²y² + y⁴ = 105, then the value of x³/y³ + y³/x³ is:",
        ["437/32", "317/16", "713/64", "803/64"],
        "803/64",
        "105 = 7(x² + xy + y²), so x² + xy + y² = 15, giving x² + y² = 11 and xy = 4.\n"
        "x/y + y/x = 11/4.\n"
        "x³/y³ + y³/x³ = (11/4)³ − 3(11/4) = 1331/64 − 528/64 = 803/64.\n"
        "Answer: 803/64",
    ),
    (
        "If x⁴ + x²y² + y⁴ = 21/256 and x² + xy + y² = 3/16, then (x + y) = ?",
        ["1/16", "5/8", "3/8", "1/4"],
        "1/4",
        "(x² − xy + y²)(3/16) = 21/256 gives x² − xy + y² = 7/16.\n"
        "x² + y² = 5/16 and xy = (3/16 − 7/16)/2 = −1/8.\n"
        "(x + y)² = 5/16 − 1/4 = 1/16, so x + y = 1/4.\n"
        "Answer: 1/4",
    ),
    (
        "If x⁴ + y⁴ + x²y² = 17 1/16 and x² − xy + y² = 5 1/4, then one of the values of (x − y) is:",
        ["5/2", "3/4", "5/4", "3/2"],
        "5/2",
        "(21/4)(x² + xy + y²) = 273/16 gives x² + xy + y² = 13/4.\n"
        "x² + y² = (21/4 + 13/4)/2 = 17/4 and xy = (13/4 − 21/4)/2 = −1.\n"
        "(x − y)² = 17/4 + 2 = 25/4, so x − y = 5/2.\n"
        "Answer: 5/2",
    ),
    (
        "If 1 + 9r² + 81r⁴ = 256 and 1 + 3r + 9r² = 32, then find the value of 1 − 3r + 9r².",
        ["8", "4", "16", "12"],
        "8",
        "(1 + 3r + 9r²)(1 − 3r + 9r²) = 1 + 9r² + 81r⁴ = 256.\n"
        "So 32 × (1 − 3r + 9r²) = 256.\n"
        "1 − 3r + 9r² = 8.\n"
        "Answer: 8",
    ),
    (
        "If 16a⁴ + 36a²b² + 81b⁴ = 91 and 4a² + 9b² − 6ab = 13, then what is the value of 3ab?",
        ["-3", "5", "3/2", "-3/2"],
        "-3/2",
        "(4a² − 6ab + 9b²)(4a² + 6ab + 9b²) = 16a⁴ + 36a²b² + 81b⁴ = 91, so 4a² + 6ab + 9b² = 7.\n"
        "Subtracting: 12ab = 7 − 13 = −6, so ab = −1/2.\n"
        "3ab = −3/2.\n"
        "Answer: -3/2",
    ),
    (
        "The value of [(4.6)⁴ + (5.4)⁴ + (24.84)²]/[(4.6)² + (5.4)² + 24.84] is:",
        ["24.42", "25.48", "24.24", "25.42"],
        "25.48",
        "Since 4.6 × 5.4 = 24.84, this is (a⁴ + b⁴ + a²b²)/(a² + b² + ab) with a = 4.6, b = 5.4.\n"
        "a⁴ + a²b² + b⁴ = (a² + ab + b²)(a² − ab + b²), so the value is a² − ab + b².\n"
        "= 21.16 + 29.16 − 24.84 = 25.48.\n"
        "Answer: 25.48",
    ),
    (
        "If (81m⁴ + 256n⁴ + 144m²n²)/(9m² + 16n² + 12mn) = [A√3m² + B√2n² − C√3mn], then the value of A² + B² − C² is:",
        ["127", "107", "117", "137"],
        "107",
        "With a = 3m and b = 4n the numerator is a⁴ + a²b² + b⁴ = (a² + ab + b²)(a² − ab + b²), so the quotient is 9m² − 12mn + 16n².\n"
        "Matching: A√3 = 9, B√2 = 16, C√3 = 12, i.e. A² = 27, B² = 128, C² = 48.\n"
        "A² + B² − C² = 27 + 128 − 48 = 107.\n"
        "Answer: 107",
    ),
    (
        "The value of 1/(a² + ax + x²) − 1/(a² − ax + x²) + 2ax/(a⁴ + a²x² + x⁴) = ?",
        ["2", "1", "-1", "0"],
        "0",
        "The first two terms combine to [(a² − ax + x²) − (a² + ax + x²)]/[(a² + ax + x²)(a² − ax + x²)].\n"
        "= −2ax/(a⁴ + a²x² + x⁴).\n"
        "Adding the third term gives 0.\n"
        "Answer: 0",
    ),
    (
        "Using algebraic identities, simplify the expression (x⁴ + x² + 1)/(x² + x + 1).",
        ["x² − 2x + 1", "x² + x + 1", "x² + 2x + 1", "x² − x + 1"],
        "x² − x + 1",
        "x⁴ + x² + 1 = (x² + 1)² − x² = (x² + x + 1)(x² − x + 1).\n"
        "Cancelling the common factor leaves x² − x + 1.\n"
        "Answer: x² − x + 1",
    ),
    (
        "Simplify: [(0.25)⁴ + 2 × (0.25)² + 1 − (0.25)²]/[(0.25)² + 0.25 + 1]",
        ["0.6755", "0.9025", "0.8125", "0.7835"],
        "0.8125",
        "The numerator is x⁴ + x² + 1 with x = 0.25, which factors as (x² + x + 1)(x² − x + 1).\n"
        "Cancelling x² + x + 1 leaves x² − x + 1 = 0.0625 − 0.25 + 1.\n"
        "= 0.8125.\n"
        "Answer: 0.8125",
    ),
    (
        "If x² + xy + y² = 119 and x − √(xy) + y = 7, then find xy.",
        ["25", "5", "50", "36"],
        "25",
        "x² + xy + y² = (x + y)² − xy = (x + y + √(xy))(x + y − √(xy)).\n"
        "So 7(x + y + √(xy)) = 119, giving x + y + √(xy) = 17 while x + y − √(xy) = 7.\n"
        "Subtracting: 2√(xy) = 10, so √(xy) = 5 and xy = 25.\n"
        "Answer: 25",
    ),
    (
        "If a⁴ − 7a²b² + b⁴ = 84 and a² − 3ab + b² = 12, find (a³ + b³)/(a + b).",
        ["26/3", "31/3", "43/4", "59/6"],
        "31/3",
        "(a² − 3ab + b²)(a² + 3ab + b²) = a⁴ − 7a²b² + b⁴ = 84, so a² + 3ab + b² = 7.\n"
        "Adding gives a² + b² = 19/2; subtracting gives 6ab = −5, so ab = −5/6.\n"
        "(a³ + b³)/(a + b) = a² − ab + b² = 19/2 + 5/6 = 31/3.\n"
        "Answer: 31/3",
    ),
    (
        "If 9x⁴ + 20x²y² + 16y⁴ = 91 and 3x² + 2xy + 4y² = 13, then find the value of x/(4y) + y/(3x).",
        ["7/12", "0.625", "2/3", "5/9"],
        "5/9",
        "(3x² + 2xy + 4y²)(3x² − 2xy + 4y²) = 9x⁴ + 20x²y² + 16y⁴ = 91, so 3x² − 2xy + 4y² = 7.\n"
        "Subtracting: 4xy = 6 so xy = 3/2; adding: 3x² + 4y² = 10.\n"
        "x/(4y) + y/(3x) = (3x² + 4y²)/(12xy) = 10/18 = 5/9.\n"
        "Answer: 5/9",
    ),
    (
        "If a² + b² = x and ab = y, then (a⁴ + b⁴)/(a² − ab√2 + b²) = ?",
        ["x + 2y", "x + √2y", "y + √2x", "2x + y"],
        "x + √2y",
        "a⁴ + b⁴ = (a² + b²)² − 2a²b² = (a² + ab√2 + b²)(a² − ab√2 + b²).\n"
        "Cancelling gives a² + ab√2 + b².\n"
        "= x + √2y.\n"
        "Answer: x + √2y",
    ),
    (
        "If a⁴ + b⁴ = 63 and a² + b² + ab√2 = 9, then find ab.",
        ["1", "1/√2", "2", "0"],
        "1/√2",
        "a⁴ + b⁴ = (a² + ab√2 + b²)(a² − ab√2 + b²), so 9(a² − ab√2 + b²) = 63 and a² − ab√2 + b² = 7.\n"
        "Subtracting: 2ab√2 = 9 − 7 = 2, so ab√2 = 1.\n"
        "ab = 1/√2.\n"
        "Answer: 1/√2",
    ),
    (
        "If the semi-perimeter and area of a rectangle whose length and breadth are x and y are 12 cm and 28 cm² respectively, then find the value of x⁴ + x²y² + y⁴.",
        ["6609", "6906", "6960", "6690"],
        "6960",
        "x + y = 12 and xy = 28, so x² + y² = 144 − 56 = 88.\n"
        "x⁴ + x²y² + y⁴ = (x² + y²)² − x²y² = 88² − 28².\n"
        "= 7744 − 784 = 6960.\n"
        "Answer: 6960",
    ),
    (
        "If x⁴ + x³ + x² + x + 1 = 0, then x²⁰¹⁵ + x³⁰¹⁵ + 5 = ?",
        ["6", "7", "8", "-9"],
        "7",
        "Multiplying by (x − 1) gives x⁵ = 1 with x ≠ 1.\n"
        "2015 and 3015 are both multiples of 5, so x²⁰¹⁵ = x³⁰¹⁵ = 1.\n"
        "1 + 1 + 5 = 7.\n"
        "Answer: 7",
    ),
    (
        "If a⁹ + a⁸ + a⁷ + a⁶ + a⁵ + a⁴ + a³ + a² + a + 1 = 0, then find a²⁰²⁰ + 1/a²⁰³⁰ + a²⁰⁴⁰ + 1/a²⁰⁵⁰.",
        ["1", "4", "0", "2"],
        "4",
        "Multiplying by (a − 1) gives a¹⁰ = 1 with a ≠ 1.\n"
        "Each of 2020, 2030, 2040 and 2050 is a multiple of 10, so every term equals 1.\n"
        "The sum is 4.\n"
        "Answer: 4",
    ),
    (
        "If y = 1 + √3 + √4, then the value of 2y⁴ − 8y³ − 6y² + 28y − 84 is:",
        ["40√3", "80√3", "20√3", "60√3"],
        "40√3",
        "y = 3 + √3, so y − 3 = √3 and y² − 6y + 6 = 0.\n"
        "Dividing 2y⁴ − 8y³ − 6y² + 28y − 84 by y² − 6y + 6 leaves remainder 40y − 120.\n"
        "40(y − 3) = 40√3.\n"
        "Answer: 40√3",
    ),
    (
        "If a³ + 4a² + 16a = 1, then what is the value of a³ + (4/a)?",
        ["63", "65", "67", "68"],
        "65",
        "From the equation, a³ = 1 − 4a² − 16a.\n"
        "a⁴ = a·a³ = a − 4a³ − 16a² = a − 4(1 − 4a² − 16a) − 16a² = 65a − 4.\n"
        "a³ + 4/a = (a⁴ + 4)/a = 65a/a = 65.\n"
        "Answer: 65",
    ),
    (
        "If a³ + 5a² + 25a + 2 = 0, then find the value of a³ − 10/a.",
        ["127", "125", "25", "123"],
        "123",
        "From the equation, a³ = −5a² − 25a − 2.\n"
        "a⁴ = a·a³ = −5a³ − 25a² − 2a = 25a² + 125a + 10 − 25a² − 2a = 123a + 10.\n"
        "a³ − 10/a = (a⁴ − 10)/a = 123a/a = 123.\n"
        "Answer: 123",
    ),
    (
        "If x² + 2 = 2x, then x⁴ − x³ + x² + 2 = ?",
        ["0", "1", "-1", "√2"],
        "0",
        "x² = 2x − 2, so x³ = 2x² − 2x = 2x − 4 and x⁴ = 2x² − 4x = −4.\n"
        "x⁴ − x³ + x² + 2 = −4 − (2x − 4) + (2x − 2) + 2.\n"
        "= 0.\n"
        "Answer: 0",
    ),
    (
        "If 3√((1 − a)/a) + 9 = 19 − 3√(a/(1 − a)), then what is the value of a?",
        ["3/10, 7/10", "1/10, 9/10", "2/5, 3/5", "1/5, 4/5"],
        "1/10, 9/10",
        "Let t = √((1 − a)/a), so √(a/(1 − a)) = 1/t and the equation becomes 3t + 3/t = 10.\n"
        "3t² − 10t + 3 = 0 gives t = 3 or t = 1/3.\n"
        "t² = (1 − a)/a gives a = 1/10 (for t = 3) and a = 9/10 (for t = 1/3).\n"
        "Answer: 1/10, 9/10",
    ),
    (
        "If √(x/y) + 1/√2 = √(y/x) and x + y = 18, then what is the value of xy?",
        ["80", "45", "56", "72"],
        "72",
        "The condition says √(y/x) − √(x/y) = 1/√2, i.e. (y − x)/√(xy) = 1/√2.\n"
        "So ((x + y)/√(xy))² = 1/2 + 4 = 9/2, i.e. 324/xy = 9/2.\n"
        "xy = 648/9 = 72.\n"
        "Answer: 72",
    ),
    (
        "If √(a/b) = 8/3 + √(b/a) and (a + b) = 30, then what is the value of ab?",
        ["64", "28", "81", "26"],
        "81",
        "The condition says (a − b)/√(ab) = 8/3.\n"
        "So ((a + b)/√(ab))² = 64/9 + 4 = 100/9, giving 30/√(ab) = 10/3.\n"
        "√(ab) = 9, so ab = 81.\n"
        "Answer: 81",
    ),
    (
        "If (x + 5)(x + 6) + 9/(x(x − 1)) = 0, then 2x² + 10x + 7 = ?",
        ["10", "11", "9", "13"],
        "13",
        "Multiply by x(x − 1) and regroup as [x(x + 5)][(x − 1)(x + 6)] = −9.\n"
        "With u = x² + 5x this is u(u − 6) = −9, i.e. (u − 3)² = 0, so u = 3.\n"
        "2x² + 10x + 7 = 2u + 7 = 13.\n"
        "Answer: 13",
    ),
    (
        "If x³ − 6x² + 35 = 8(x − 2), then find the value of x² + 3/(x − 6).",
        ["6", "8", "9", "12"],
        "8",
        "x³ − 6x² = x²(x − 6), so x²(x − 6) = 8x − 16 − 35 = 8x − 51 and x² = (8x − 51)/(x − 6).\n"
        "x² + 3/(x − 6) = (8x − 51 + 3)/(x − 6) = (8x − 48)/(x − 6).\n"
        "= 8(x − 6)/(x − 6) = 8.\n"
        "Answer: 8",
    ),
    (
        "Given that x, y, z are positive real numbers, if (x + y)² − z² = 130, (y + z)² − x² = 150 and (x + z)² − y² = 120, then x is:",
        ["35/8", "25/4", "15/2", "16/3"],
        "25/4",
        "With s = x + y + z the three conditions are s(s − 2z) = 130, s(s − 2x) = 150, s(s − 2y) = 120.\n"
        "Adding: 3s² − 2s² = s² = 400, so s = 20.\n"
        "From 20(20 − 2x) = 150: 20 − 2x = 7.5, so x = 25/4.\n"
        "Answer: 25/4",
    ),
    (
        "If x = 2 + √3, y = 2 − √3, z = 1, then what is the value of (x/yz) + (y/xz) + (z/xy) + 2[(1/x) + (1/y) + (1/z)]?",
        ["25", "22", "17", "43"],
        "25",
        "xy = 1 and xyz = 1, so x/(yz) = x², y/(xz) = y² and z/(xy) = z²; their sum is 14 + 1 = 15.\n"
        "Also 1/x = y, 1/y = x and 1/z = 1, so the bracket is 4 + 1 = 5.\n"
        "Total = 15 + 2 × 5 = 25.\n"
        "Answer: 25",
    ),
    (
        "If x = √5 + 1 and y = √5 − 1, then what is the value of (x²/y²) + (y²/x²) + 4(x/y) + 4(y/x) + 6?",
        ["31", "23√5", "27√5", "25"],
        "25",
        "xy = 4 and x² + y² = 12, so x/y + y/x = 12/4 = 3.\n"
        "x²/y² + y²/x² = 3² − 2 = 7.\n"
        "Total = 7 + 4 × 3 + 6 = 25.\n"
        "Answer: 25",
    ),
    (
        "If ab/(a + b) = 1/3, bc/(b + c) = 1/4 and ca/(c + a) = 1/5, then find the value of abc/(ab + bc + ca).",
        ["1/6", "1/12", "6", "1/4"],
        "1/6",
        "Inverting each: 1/a + 1/b = 3, 1/b + 1/c = 4, 1/c + 1/a = 5.\n"
        "Adding: 2(1/a + 1/b + 1/c) = 12, so 1/a + 1/b + 1/c = 6.\n"
        "abc/(ab + bc + ca) = 1/(1/a + 1/b + 1/c) = 1/6.\n"
        "Answer: 1/6",
    ),
    (
        "If xy/(x + y) = a, xz/(x + z) = b and yz/(y + z) = c where a, b, c are all non-zero numbers, then x equals:",
        [
            "2abc/(ab + bc − ac)",
            "2abc/(ab + ac − bc)",
            "2abc/(ac + bc − ab)",
            "2abc/(ab + bc + ca)",
        ],
        "2abc/(ac + bc − ab)",
        "Inverting: 1/a = 1/x + 1/y, 1/b = 1/x + 1/z, 1/c = 1/y + 1/z.\n"
        "1/a + 1/b − 1/c = 2/x, so x = 2/((bc + ac − ab)/abc).\n"
        "x = 2abc/(ac + bc − ab).\n"
        "Answer: 2abc/(ac + bc − ab)",
    ),
    (
        "If 2018^x + 2018^(-x) = 3, then find √[(2018^(6x) − 2018^(-6x))/(2018^x − 2018^(-x))].",
        ["16", "10", "12", "9"],
        "12",
        "With u = 2018^x: u + 1/u = 3, so u − 1/u = √5 and u³ + 1/u³ = 27 − 9 = 18.\n"
        "u³ − 1/u³ = 5√5 + 3√5 = 8√5, so u⁶ − 1/u⁶ = 8√5 × 18 = 144√5.\n"
        "The ratio is 144√5/√5 = 144, whose square root is 12.\n"
        "Answer: 12",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-4")
