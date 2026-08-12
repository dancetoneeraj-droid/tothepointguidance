"""Mensuration Sheet-5 (Prism) -> maths_mensuration_3d_249 onward.

The sheet highlights answers for 13 of its 18 questions; each highlight matches
the derivation below, and the remaining five were solved from scratch.
"""

from mensuration3d_import_lib import import_sheet

START_INDEX = 247  # maths_mensuration_3d_249

QUESTIONS = [
    (
        "The base area, height and volume of a prism are (3√3/2)p² cm², 100√3 cm and 7200 cm³ respectively. Then find the value of p.",
        ["√3", "3/2", "2/√3", "4"],
        "4",
        "Volume = base area × height: (3√3/2)p² × 100√3 = 7200.\n"
        "√3 × √3 = 3, so (3 × 3/2)(100)p² = 450p² = 7200 and p² = 16.\n"
        "Answer: 4",
    ),
    (
        "A right prism has a triangular base with sides 13 cm, 20 cm and 21 cm. If the height of the prism is 9 cm, then find the volume of the prism.",
        ["1314 cm³", "1134 cm³", "1413 cm³", "1143 cm³"],
        "1134 cm³",
        "s = (13 + 20 + 21)/2 = 27, so the base area is √(27 × 14 × 7 × 6) = 126 cm².\n"
        "Volume = 126 × 9 = 1134 cm³",
    ),
    (
        "The base of a prism is a triangle with sides 4 cm, 13 cm and 15 cm. If the volume of the right triangular prism is 480 cm³, then find the total surface area of the prism.",
        ["688 cm²", "568 cm²", "752 cm²", "664 cm²"],
        "688 cm²",
        "s = 16, so the base area is √(16 × 12 × 3 × 1) = 24 cm² and the height is 480/24 = 20 cm.\n"
        "TSA = 2(24) + (4 + 13 + 15)(20) = 48 + 640 = 688 cm²",
    ),
    (
        "The base of a right prism is a triangle of perimeter 90 cm and its inradius is 4 cm. If the volume of the prism is 1200 cm³, then find its total surface area.",
        ["840", "960", "1200", "900"],
        "960",
        "Base area = r × s = 4 × 45 = 180 cm², so the height is 1200/180 = 20/3 cm.\n"
        "TSA = 2(180) + 90(20/3) = 360 + 600 = 960",
    ),
    (
        "The base of a right prism is a triangle with sides 16 cm, 30 cm and 34 cm. Its height is 32 cm. The lateral surface area (in cm²) and the volume (in cm³) are, respectively:",
        ["2688 and 7680", "2624 and 7040", "2560 and 6400", "2560 and 7680"],
        "2560 and 7680",
        "16² + 30² = 34², so the base is right angled with area (1/2)(16)(30) = 240 cm².\n"
        "LSA = perimeter × height = 80 × 32 = 2560 cm² and volume = 240 × 32 = 7680 cm³.\n"
        "Answer: 2560 and 7680",
    ),
    (
        "The base of a right prism is a triangle with sides 20 cm, 21 cm and 29 cm. If its volume is 7560 cm³, then its lateral surface area (in cm²) is:",
        ["2520", "2448", "2556", "2484"],
        "2520",
        "20² + 21² = 29², so the base area is (1/2)(20)(21) = 210 cm² and the height is 7560/210 = 36 cm.\n"
        "LSA = 70 × 36 = 2520",
    ),
    (
        "The base of a right prism is an equilateral triangle whose side is 10 cm. If the height of this prism is 10√3 cm, then what is its total surface area?",
        ["150√3 cm²", "125√3 cm²", "350√3 cm²", "325√3 cm²"],
        "350√3 cm²",
        "Each base has area (√3/4)(100) = 25√3 cm².\n"
        "TSA = 2(25√3) + 3(10)(10√3) = 50√3 + 300√3 = 350√3 cm²",
    ),
    (
        "The base of a right prism is an equilateral triangle with each side measuring 4 cm. If the lateral surface area is 120 cm², find the volume (in cm³) of the prism.",
        ["30√3", "40√3", "10√3", "20√3"],
        "40√3",
        "LSA = perimeter × height: 12h = 120, so h = 10 cm.\n"
        "Volume = (√3/4)(16)(10) = 40√3",
    ),
    (
        "The total surface area of a triangular prism of height 6 cm is 162√3 cm². If the base of the prism is an equilateral triangle, find its volume.",
        ["162√3 cm³", "180√3", "216√3", "144√3"],
        "162√3 cm³",
        "2(√3/4)a² + 3a(6) = 162√3 is satisfied by a = 6√3, since 54√3 + 108√3 = 162√3.\n"
        "Volume = (√3/4)(108)(6) = 162√3 cm³",
    ),
    (
        "Let ABCDEF be a prism whose base is a right triangle whose perpendicular sides are 9 cm and 12 cm. If the cost of painting the prism is ₹151.20 at the rate of 20 paise/cm², then find the height of the prism.",
        ["17 cm", "15 cm", "16 cm", "18 cm"],
        "18 cm",
        "Painted area = 151.20/0.20 = 756 cm²; the base area is 54 cm² and the perimeter is 9 + 12 + 15 = 36 cm.\n"
        "2(54) + 36h = 756 gives 36h = 648, so h = 18 cm",
    ),
    (
        "The base of a right prism is an equilateral triangle. If the lateral surface area and volume are 120 cm² and 40√3 cm³ respectively, then the side of the base of the prism is:",
        ["4cm", "5cm", "6cm", "3cm"],
        "4cm",
        "LSA gives 3ah = 120, i.e. ah = 40; volume gives (√3/4)a²h = 40√3, i.e. a²h = 160.\n"
        "Dividing the two, a = 160/40 = 4cm",
    ),
    (
        "The base of a solid right prism of height 10 cm is a square and its volume is 160 cm³. What is the total surface area of the prism (in cm²)?",
        ["200", "192", "180", "176"],
        "192",
        "Base area = 160/10 = 16 cm², so the square's side is 4 cm.\n"
        "TSA = 2(16) + 4(4)(10) = 32 + 160 = 192",
    ),
    (
        "The base of a right prism is a square having a side of 15 cm. If its height is 8 cm, then find the total surface area.",
        ["920 cm²", "930 cm²", "900 cm²", "940 cm²"],
        "930 cm²",
        "TSA = 2a² + 4ah = 2(225) + 4(15)(8).\n"
        "= 450 + 480 = 930 cm²",
    ),
    (
        "The height of a right prism with a square base is 15 cm. If the area of the total surface of the prism is 608 sq cm, its volume is:",
        ["910", "920", "960", "980"],
        "960",
        "2a² + 4a(15) = 608 gives a² + 30a − 304 = 0, so a = 8 cm.\n"
        "Volume = 64 × 15 = 960",
    ),
    (
        "A prism has a square base whose side is 8 cm. The height of the prism is 80 cm. The prism is cut into 10 identical parts by 9 cuts which are parallel to the base of the prism. What is the total surface area (in cm²) of all the 10 parts together?",
        ["4260", "2560", "3840", "3220"],
        "3840",
        "Original TSA = 2(64) + 4(8)(80) = 128 + 2560 = 2688 cm².\n"
        "Each cut exposes two fresh 64 cm² faces, so 9 cuts add 9 × 128 = 1152 cm².\n"
        "Total = 2688 + 1152 = 3840",
    ),
    (
        "The base of a right prism is a rectangle in which the ratio of length to breadth is 3 : 2. If the height of the prism is 12 cm and the total surface area is 288 cm², then what is the volume of the prism?",
        ["291 cm³", "288 cm³", "290 cm³", "286 cm³"],
        "288 cm³",
        "With sides 3x and 2x: 2(6x²) + 2(5x)(12) = 288, i.e. x² + 10x − 24 = 0, so x = 2.\n"
        "The base is 6 cm by 4 cm, so the volume is 6 × 4 × 12 = 288 cm³",
    ),
    (
        "The base of a right prism is a trapezium whose parallel sides are 11 cm and 15 cm and the distance between them is 9 cm. If the volume of the prism is 1731.6 cm³, then the height (in cm) of the prism will be:",
        ["15.2", "14.2", "15.6", "14.8"],
        "14.8",
        "Base area = (1/2)(11 + 15)(9) = 117 cm².\n"
        "Height = 1731.6/117 = 14.8",
    ),
    (
        "The base of a right prism is a quadrilateral ABCD, given that AB = 9 cm, BC = 14 cm, CD = 13 cm, DA = 12 cm and ∠DAB = 90°. If the volume of the prism is 2070 cm³, then the area of the lateral surface is:",
        ["720 cm²", "810 cm²", "1260 cm²", "2070 cm²"],
        "720 cm²",
        "BD = √(9² + 12²) = 15 cm, so area(ABD) = 54 cm²; triangle BCD with sides 13, 14, 15 has area 84 cm².\n"
        "Base area = 138 cm², so the height is 2070/138 = 15 cm.\n"
        "LSA = (9 + 14 + 13 + 12)(15) = 720 cm²",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-5")
