"""Mensuration Sheet-6 (Pyramid and Tetrahedron) -> maths_mensuration_3d_267 onward.

Only Q3 and Q12 carry a highlighted answer on the sheet; both agree with the
derivation, and every other answer here was worked out from scratch.

In Q4 "slant height" is the slant height of a lateral face (measured to the
midpoint of a base edge), which is the reading that makes the printed option
128√6 come out exactly.
"""

from mensuration3d_import_lib import import_sheet

START_INDEX = 265  # maths_mensuration_3d_267

QUESTIONS = [
    (
        "A prism and a pyramid have the same base and the same height. Find the ratio of the volume of the prism and the pyramid.",
        ["2:3", "3:1", "1:3", "3:2"],
        "3:1",
        "A pyramid holds one-third of the prism built on the same base with the same height.\n"
        "Prism : pyramid = 1 : (1/3) = 3:1",
    ),
    (
        "The volume of a right pyramid is 45√3 cm³ and its base is an equilateral triangle with side 6 cm. What is the height (in cm) of the pyramid?",
        ["20", "15", "12", "18"],
        "15",
        "Base area = (√3/4)(36) = 9√3 cm².\n"
        "(1/3)(9√3)h = 45√3 gives 3√3h = 45√3, so h = 15",
    ),
    (
        "The base of a right pyramid is an equilateral triangle with side 8 cm, and its height is 30√3 cm. The volume (in cm³) of the pyramid is:",
        ["480", "360√3", "360", "240√3"],
        "480",
        "Base area = (√3/4)(64) = 16√3 cm².\n"
        "V = (1/3)(16√3)(30√3) = (1/3)(16 × 30 × 3) = 480",
    ),
    (
        "Find the volume of a pyramid whose base is an equilateral triangle of side 16√3 cm and whose slant height is 3 times its height.",
        ["128√6 cm²", "128√3", "256√3", "256√2"],
        "128√6 cm²",
        "The inradius of the base is 16√3/(2√3) = 8 cm, and the face slant height satisfies l² = h² + 8².\n"
        "With l = 3h: 9h² = h² + 64, so h² = 8 and h = 2√2 cm.\n"
        "V = (1/3)(√3/4)(768)(2√2) = (1/3)(192√3)(2√2) = 128√6 cm²",
    ),
    (
        "The base of a right pyramid is an equilateral triangle of side 10√3 cm. If the total surface area of the pyramid is 270√3 sq cm, its height is:",
        ["12√3cm", "10cm", "12cm", "10√3cm"],
        "12cm",
        "Base area = (√3/4)(300) = 75√3, so the lateral surface is 270√3 − 75√3 = 195√3.\n"
        "(1/2)(30√3)l = 195√3 gives the face slant height l = 13 cm, and the inradius is 10√3/(2√3) = 5 cm.\n"
        "h = √(169 − 25) = 12cm",
    ),
    (
        "The base of a right pyramid is an equilateral triangle, each side of which is 20 cm. Each slant edge is 30 cm. The vertical height (in cm) of the pyramid is:",
        ["5√3", "10√3", "5√(23/3)", "10√(23/3)"],
        "10√(23/3)",
        "The base's circumradius is 20/√3, and the slant edge reaches a vertex.\n"
        "h = √(30² − 400/3) = √(2300/3) = 10√(23/3)",
    ),
    (
        "The base of a pyramid is an equilateral triangle whose each side is 8 cm. Its slant edge is 24 cm. What is the total surface area of the pyramid?",
        [
            "(24√3 + 36√35) cm²",
            "(16√3 + 48√35) cm²",
            "(16√3 + 24√35) cm²",
            "(12√3 + 24√35) cm²",
        ],
        "(16√3 + 48√35) cm²",
        "Base area = (√3/4)(64) = 16√3 cm².\n"
        "Each lateral face has base 8 and equal sides 24, so its height is √(576 − 16) = 4√35 and its area is 16√35.\n"
        "TSA = 16√3 + 3(16√35) = (16√3 + 48√35) cm²",
    ),
    (
        "The base of a right pyramid is an equilateral triangle with area 16√3 cm². If the area of one of its lateral faces is 30 cm², then its height (in cm) is:",
        ["√(739/12)", "√(611/12)", "√(209/12)", "√(643/12)"],
        "√(611/12)",
        "(√3/4)a² = 16√3 gives a = 8 cm, and (1/2)(8)l = 30 gives the face slant height l = 7.5 cm.\n"
        "The inradius is 4/√3, so h² = 56.25 − 16/3 = 611/12.\n"
        "Answer: √(611/12)",
    ),
    (
        "The base of a right pyramid is an equilateral triangle of side 4 cm. The height of the pyramid is half of its slant height. Find the length of a slant edge and the volume of the pyramid.",
        [
            "2√13/3 cm & 8√3/9 cm³",
            "4√13/3 cm & 12√3/5 cm³",
            "5√13/3 cm & 10√3/9 cm³",
            "None",
        ],
        "2√13/3 cm & 8√3/9 cm³",
        "The inradius is 2/√3, so l² = h² + 4/3 with h = l/2 gives (3/4)l² = 4/3, l = 4/3 and h = 2/3 cm.\n"
        "The circumradius is 4/√3, so the slant edge is √(4/9 + 16/3) = 2√13/3 cm.\n"
        "Volume = (1/3)(4√3)(2/3) = 8√3/9 cm³, i.e. 2√13/3 cm & 8√3/9 cm³",
    ),
    (
        "The height of a pyramid is 6 m and the base of the pyramid is a square whose diagonal is √1152 m. Find the volume of the pyramid.",
        ["144", "288", "576", "1152"],
        "1152",
        "For a square, diagonal² = 2a², so a² = 1152/2 = 576 m².\n"
        "V = (1/3)(576)(6) = 1152",
    ),
    (
        "What is the total surface area of a pyramid whose base is a square of side 8 cm and the height of the pyramid is 3 cm?",
        ["121 cm²", "144 cm²", "169 cm²", "184 cm²"],
        "144 cm²",
        "The apothem of the base is 4 cm, so the face slant height is √(3² + 4²) = 5 cm.\n"
        "TSA = 64 + (1/2)(32)(5) = 64 + 80 = 144 cm²",
    ),
    (
        "The base of a right pyramid is a square whose diagonal is 20 cm. The height of the pyramid is 20 cm. The lateral surface area of the pyramid is:",
        ["450 cm²", "500 cm²", "600 cm²", "720 cm²"],
        "600 cm²",
        "Side = 20/√2 = 10√2 cm, so the apothem is 5√2 cm and the face slant height is √(400 + 50) = 15√2 cm.\n"
        "LSA = (1/2)(40√2)(15√2) = 600 cm²",
    ),
    (
        "The base of a pyramid is a square whose area is 324 sq cm. If the volume of the pyramid is 1296 cm³, then find the area of its lateral surface.",
        ["432", "540", "1080", "360"],
        "540",
        "Side = 18 cm and (1/3)(324)h = 1296 gives h = 12 cm.\n"
        "The apothem is 9 cm, so the face slant height is √(144 + 81) = 15 cm.\n"
        "LSA = (1/2)(72)(15) = 540",
    ),
    (
        "The volume of a pyramid with a square base is 200 cm³. The height of the pyramid is 13 cm. What will be the length of the edges (i.e. the distance between the apex and any other vertex), rounded to the nearest integer?",
        ["12 cm", "13cm", "14 cm", "15 cm"],
        "14 cm",
        "Base area = 600/13 = 46.15 cm², so the side is 6.79 cm and half the diagonal is 4.80 cm.\n"
        "Edge = √(13² + 4.80²) = √192.1 = 13.86, i.e. 14 cm",
    ),
    (
        "A right pyramid has a square base with side of base 12 cm and the height of the pyramid is 40 cm. The pyramid is cut into four parts of equal heights by three planes parallel to its base. What is the ratio of the volume of the four parts?",
        ["1:8:27:70", "1:7:19:47", "1:8:27:64", "1:7:19:37"],
        "1:7:19:37",
        "Measured from the apex the cumulative volumes are as 1³ : 2³ : 3³ : 4³ = 1 : 8 : 27 : 64.\n"
        "Taking differences, the four slices are 1:7:19:37",
    ),
    (
        "A pyramid has a square base. The side of the square is 12 cm and the height of the pyramid is 21 cm. The pyramid is cut into 3 parts by 2 cuts parallel to its base. The cuts are at heights of 7 cm and 14 cm respectively from the base. What is the difference (in cm³) in the volume of the topmost and bottommost parts?",
        ["672", "944", "427", "756"],
        "672",
        "V = (1/3)(144)(21) = 1008 cm³.\n"
        "The top piece is (1/3)³V = V/27; the bottom piece is V − (2/3)³V = 19V/27.\n"
        "Difference = 18V/27 = (2/3)(1008) = 672",
    ),
    (
        "Find the TSA of a pyramid whose base is a hexagon with side 8√3 cm and height 16 cm.",
        ["762√3 cm²", "720√3 cm²", "768√3 cm²", "794√3 cm²"],
        "768√3 cm²",
        "Base area = (3√3/2)(8√3)² = (3√3/2)(192) = 288√3 cm², and the apothem is (√3/2)(8√3) = 12 cm.\n"
        "Face slant height = √(16² + 12²) = 20 cm, so the lateral area is (1/2)(48√3)(20) = 480√3 cm².\n"
        "TSA = 288√3 + 480√3 = 768√3 cm²",
    ),
    (
        "There is a pyramid on a base which is a regular hexagon of side 2a. If every slant edge of this pyramid is of length 5a/2, then the volume of this pyramid must be:",
        ["3a³", "3a³√2", "3a³√3", "6a³"],
        "3a³√3",
        "In a regular hexagon the circumradius equals the side, 2a, so h = √(25a²/4 − 4a²) = 3a/2.\n"
        "Base area = (3√3/2)(2a)² = 6√3a².\n"
        "V = (1/3)(6√3a²)(3a/2) = 3a³√3",
    ),
    (
        "Find the TSA of a tetrahedron whose height is 4√2 cm.",
        ["42√3 cm²", "48√3 cm²", "32√3 cm²", "36√3 cm²"],
        "48√3 cm²",
        "For a regular tetrahedron h = a√(2/3), so a = 4√2 × √(3/2) = 4√3 cm.\n"
        "TSA = √3a² = √3(48) = 48√3 cm²",
    ),
    (
        "Find the volume of a tetrahedron with side 3√2 cm.",
        ["12 cm³", "9 cm³", "9√2 cm³", "6√2 cm³"],
        "9 cm³",
        "V = a³/(6√2) with a = 3√2, so a³ = 54√2.\n"
        "V = 54√2/(6√2) = 9 cm³",
    ),
    (
        "The volume of a tetrahedron is 18√2. Then find its TSA.",
        ["18√3", "27√3", "36√3", "45√3"],
        "36√3",
        "a³/(6√2) = 18√2 gives a³ = 18 × 6 × 2 = 216, so a = 6.\n"
        "TSA = √3a² = 36√3",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-6")
