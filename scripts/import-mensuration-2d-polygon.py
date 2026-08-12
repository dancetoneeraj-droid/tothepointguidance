"""Import the 62 POLYGON questions from datas/maths/Mensuration-2d.pdf into
data/maths/mensuration-2d.json, filling the placeholder slots that start at
maths_mensuration_2d_207. No other entry in the bank is touched.

Answers come from the answer key printed on the last page of the PDF; every
answer was re-derived by hand and the worked steps are stored in `solution`.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "mensuration-2d.json"
START_INDEX = 206  # maths_mensuration_2d_207
FIG = "/content/figures/mensuration-2d"

# (question, [options], correct answer, solution, image or None)
QUESTIONS = [
    (
        "Which of the following is NOT a property of a regular polygon?",
        [
            "All sides are of equal length.",
            "Angles at the centre by all sides are equal.",
            "The angle made by each side at the centre is 90°, if it is a regular polygon with four sides.",
            "The angle made by each side at the centre is 60°, if it is a regular polygon with eight sides.",
        ],
        "The angle made by each side at the centre is 60°, if it is a regular polygon with eight sides.",
        "Each side of a regular n-sided polygon subtends an angle of 360°/n at the centre.\n"
        "For n = 4: 360°/4 = 90°, so that statement is a genuine property.\n"
        "For n = 8: 360°/8 = 45°, not 60°.\n"
        "Answer: The angle made by each side at the centre is 60°, if it is a regular polygon with eight sides.",
        None,
    ),
    (
        "Find the number of sides in a regular polygon if its each interior angle is 165°.",
        ["24", "17", "25", "20"],
        "24",
        "Each exterior angle = 180° − 165° = 15°.\n"
        "Sum of exterior angles is always 360°, so n = 360°/15° = 24.\n"
        "Answer: 24",
        None,
    ),
    (
        "If one interior angle of a regular polygon is greater than its exterior angle by 144°, how many sides does the polygon have?",
        ["18", "21", "20", "19"],
        "20",
        "Interior + Exterior = 180° and Interior − Exterior = 144°.\n"
        "Adding the two: 2 × Interior = 324° ⇒ Interior = 162°, so Exterior = 18°.\n"
        "n = 360°/18° = 20.\n"
        "Answer: 20",
        None,
    ),
    (
        "The sum of all interior angles of a regular polygon is 1620°. What is the measure (in degrees) of its each exterior angle?",
        ["33 8/11", "34 8/11", "32 8/11", "31 8/11"],
        "32 8/11",
        "(n − 2) × 180° = 1620° ⇒ n − 2 = 9 ⇒ n = 11.\n"
        "Each exterior angle = 360°/11 = 32 8/11 degrees.\n"
        "Answer: 32 8/11",
        None,
    ),
    (
        "The interior angle between two adjacent sides of a regular n-sided polygon is _______ degrees.",
        ["180 − 90/n", "180 − 180/n", "90 − 90/n", "180 − 360/n"],
        "180 − 360/n",
        "Each exterior angle of a regular n-gon = 360°/n.\n"
        "Interior angle = 180° − exterior angle = 180° − 360°/n.\n"
        "Answer: 180 − 360/n",
        None,
    ),
    (
        "The exterior angle of a regular polygon is one-seventh of its interior angle. How many sides does the polygon have?",
        ["12", "18", "16", "24"],
        "16",
        "Let the exterior angle be E, then the interior angle is 7E.\n"
        "E + 7E = 180° ⇒ 8E = 180° ⇒ E = 22.5°.\n"
        "n = 360°/22.5° = 16.\n"
        "Answer: 16",
        None,
    ),
    (
        "The ratio of sum of interior angles to sum of exterior angles of a regular polygon of n sides is 7/2. What is the measure of an interior angle of polygon?",
        ["110", "120", "130", "140"],
        "140",
        "Sum of exterior angles = 360°, sum of interior angles = (n − 2) × 180°.\n"
        "(n − 2) × 180 / 360 = 7/2 ⇒ (n − 2)/2 = 7/2 ⇒ n = 9.\n"
        "Interior angle = 180° − 360°/9 = 180° − 40° = 140°.\n"
        "Answer: 140",
        None,
    ),
    (
        "For a regular polygon, the sum of the interior angles is 400% more than the sum of its exterior angles. Each interior angle of the polygon measures x°. What is the value of x?",
        ["145", "135", "150", "140"],
        "150",
        "Sum of exterior angles = 360°. '400% more' means sum of interior = 360 + 4 × 360 = 1800°.\n"
        "(n − 2) × 180 = 1800 ⇒ n = 12.\n"
        "Each interior angle = 180° − 360°/12 = 150°.\n"
        "Answer: 150",
        None,
    ),
    (
        "For a regular polygon, the sum of the interior angles is 250% more than the sum of its exterior angles. Each interior angle of the polygon measures x°. What is the value of x?",
        ["140", "150", "145", "120"],
        "140",
        "'250% more' means sum of interior = 360 + 2.5 × 360 = 1260°.\n"
        "(n − 2) × 180 = 1260 ⇒ n = 9.\n"
        "Each interior angle = 180° − 360°/9 = 140°.\n"
        "Answer: 140",
        None,
    ),
    (
        "The ratio of the numbers of sides of two regular polygons is 5 : 3. If each interior angle of the first polygon is 156°, then the measure of each interior angle of the second polygon is:",
        ["136°", "150°", "140°", "135°"],
        "140°",
        "First polygon: interior 156° ⇒ exterior 24° ⇒ n₁ = 360/24 = 15.\n"
        "Sides are in the ratio 5 : 3, so n₂ = 15 × 3/5 = 9.\n"
        "Interior angle of the second polygon = 180° − 360°/9 = 140°.\n"
        "Answer: 140°",
        None,
    ),
    (
        "A regular polygon has twice the number of sides as another regular polygon. The perimeter of the smaller polygon is 84.8 cm and each of its interior angles measures 140°. The side length of the larger polygon is 1.2 times that of the smaller one. What is the measure of each interior angle of the larger polygon?",
        ["155°", "158°", "160°", "162°"],
        "160°",
        "Smaller polygon: interior 140° ⇒ exterior 40° ⇒ n = 360/40 = 9.\n"
        "The larger polygon has twice as many sides, i.e. 18.\n"
        "Interior angle = 180° − 360°/18 = 180° − 20° = 160°.\n"
        "(The perimeter and side-length data are not needed here.)\n"
        "Answer: 160°",
        None,
    ),
    (
        "If the exterior angle of a regular polygon is 18°, then what will be the number of diagonals in this polygon?",
        ["180", "170", "140", "150"],
        "170",
        "n = 360°/18° = 20.\n"
        "Number of diagonals = n(n − 3)/2 = 20 × 17/2 = 170.\n"
        "Answer: 170",
        None,
    ),
    (
        "The sum of interior angles of a regular polygon is 1260°. Find the number of diagonals of this regular polygon.",
        ["35", "27", "44", "20"],
        "27",
        "(n − 2) × 180 = 1260 ⇒ n − 2 = 7 ⇒ n = 9.\n"
        "Diagonals = n(n − 3)/2 = 9 × 6/2 = 27.\n"
        "Answer: 27",
        None,
    ),
    (
        "Find the number of diagonals of a regular polygon whose interior angles sum to 2700°.",
        ["127", "121", "119", "117"],
        "119",
        "(n − 2) × 180 = 2700 ⇒ n − 2 = 15 ⇒ n = 17.\n"
        "Diagonals = 17 × 14/2 = 119.\n"
        "Answer: 119",
        None,
    ),
    (
        "If the sum of the interior angles of a regular polygon is 2520°, determine the number of sides and the total number of diagonals of the polygon.",
        [
            "16 sides, 104 diagonals",
            "14 sides, 94 diagonals",
            "18 sides, 104 diagonals",
            "14 sides, 84 diagonals",
        ],
        "16 sides, 104 diagonals",
        "(n − 2) × 180 = 2520 ⇒ n − 2 = 14 ⇒ n = 16.\n"
        "Diagonals = 16 × 13/2 = 104.\n"
        "Answer: 16 sides, 104 diagonals",
        None,
    ),
    (
        "In a regular polygon, any interior angle exceeds the exterior angle by 120 degrees. Then, the number of diagonals of this polygon is:",
        ["54", "55", "56", "60"],
        "54",
        "Interior − Exterior = 120° and Interior + Exterior = 180° ⇒ Exterior = 30°.\n"
        "n = 360/30 = 12.\n"
        "Diagonals = 12 × 9/2 = 54.\n"
        "Answer: 54",
        None,
    ),
    (
        "If a regular polygon has 65 diagonals, then the number of sides this polygon has is:",
        ["12", "14", "13", "10"],
        "13",
        "n(n − 3)/2 = 65 ⇒ n² − 3n − 130 = 0 ⇒ (n − 13)(n + 10) = 0.\n"
        "n = 13.\n"
        "Answer: 13",
        None,
    ),
    (
        "If a regular polygon has 35 diagonals, then the sum of its interior angles is:",
        ["1620°", "1440°", "1980°", "1800°"],
        "1440°",
        "n(n − 3)/2 = 35 ⇒ n² − 3n − 70 = 0 ⇒ (n − 10)(n + 7) = 0 ⇒ n = 10.\n"
        "Sum of interior angles = (10 − 2) × 180° = 1440°.\n"
        "Answer: 1440°",
        None,
    ),
    (
        "In a polygon, the number of diagonals is 12 more than the number of sides. Find the number of sides in polygon.",
        ["8", "6", "5", "10"],
        "8",
        "n(n − 3)/2 = n + 12 ⇒ n² − 3n = 2n + 24 ⇒ n² − 5n − 24 = 0.\n"
        "(n − 8)(n + 3) = 0 ⇒ n = 8.\n"
        "Answer: 8",
        None,
    ),
    (
        "If the sum of the interior angles of a regular polygon is equal to four times the sum of its exterior angles, then what is the number of diagonals in the polygon?",
        ["35", "30", "25", "40"],
        "35",
        "Sum of interior = 4 × 360° = 1440° ⇒ (n − 2) × 180 = 1440 ⇒ n = 10.\n"
        "Diagonals = 10 × 7/2 = 35.\n"
        "Answer: 35",
        None,
    ),
    (
        "If the interior angle of a regular polygon is k times its exterior angle, express the number of sides (n) of the polygon in terms of k.",
        ["2k+4", "2k−4", "2k+2", "4k−3"],
        "2k+2",
        "Interior = k × Exterior and Interior + Exterior = 180°.\n"
        "Exterior × (k + 1) = 180° ⇒ Exterior = 180/(k + 1).\n"
        "n = 360/Exterior = 360(k + 1)/180 = 2(k + 1) = 2k + 2.\n"
        "Answer: 2k+2",
        None,
    ),
    (
        "If each interior angle of a regular polygon is (128 4/7)°, then what is the sum of the number of its diagonals and the number of its sides?",
        ["15", "21", "17", "19"],
        "21",
        "Interior angle = 128 4/7 = 900/7 degrees.\n"
        "Exterior = 180 − 900/7 = 360/7 ⇒ n = 360 ÷ (360/7) = 7.\n"
        "Diagonals = 7 × 4/2 = 14.\n"
        "Diagonals + sides = 14 + 7 = 21.\n"
        "Answer: 21",
        None,
    ),
    (
        "If the measure of exterior angle of a regular polygon is (25 5/7)°, then the ratio of its diagonals to the number of its sides is:",
        ["11 : 2", "14 : 3", "7 : 1", "10 : 1"],
        "11 : 2",
        "Exterior angle = 25 5/7 = 180/7 degrees ⇒ n = 360 ÷ (180/7) = 14.\n"
        "Diagonals = 14 × 11/2 = 77.\n"
        "Diagonals : sides = 77 : 14 = 11 : 2.\n"
        "Answer: 11 : 2",
        None,
    ),
    (
        "The ratio of the sum of all interior angles and the measure of an exterior angle of a regular polygon is 6 : 0.1. Find the number of sides of the polygon.",
        ["16", "12", "10", "15"],
        "12",
        "6 : 0.1 = 60 : 1, so (n − 2) × 180 ÷ (360/n) = 60.\n"
        "n(n − 2)/2 = 60 ⇒ n² − 2n − 120 = 0 ⇒ (n − 12)(n + 10) = 0.\n"
        "n = 12.\n"
        "Answer: 12",
        None,
    ),
    (
        "If one of the interior angles of a regular polygon is 15/16 times one of the interior angles of a regular decagon, then find the number of diagonals of the polygon.",
        ["20", "14", "2", "35"],
        "20",
        "Interior angle of a regular decagon = 180° − 360°/10 = 144°.\n"
        "Required interior angle = (15/16) × 144° = 135° ⇒ exterior = 45° ⇒ n = 360/45 = 8.\n"
        "Diagonals = 8 × 5/2 = 20.\n"
        "Answer: 20",
        None,
    ),
    (
        "The interior angle of a regular polygon is 36° more than 5 times of its one exterior angle. Find the number of diagonals in this polygon.",
        ["77", "119", "104", "90"],
        "90",
        "Interior = 5 × Exterior + 36° and Interior + Exterior = 180°.\n"
        "6 × Exterior = 144° ⇒ Exterior = 24° ⇒ n = 360/24 = 15.\n"
        "Diagonals = 15 × 12/2 = 90.\n"
        "Answer: 90",
        None,
    ),
    (
        "A₁ and A₂ are two regular polygons. The sum of all the interior angles of A₁ is 1080°. Each interior angle of A₂ exceeds its exterior angle by 132°. The sum of the number of sides A₁ and A₂ is:",
        ["21", "22", "23", "24"],
        "23",
        "A₁: (n − 2) × 180 = 1080 ⇒ n₁ = 8.\n"
        "A₂: Interior − Exterior = 132° with Interior + Exterior = 180° ⇒ Exterior = 24° ⇒ n₂ = 360/24 = 15.\n"
        "n₁ + n₂ = 8 + 15 = 23.\n"
        "Answer: 23",
        None,
    ),
    (
        "P1 and P2 are two regular polygons. If the ratio of one of the internal angles to that of an external angle of P1 is 7 : 2 and the number of diagonals of P2 is 65, then find the sum of the number of sides of P1 and P2.",
        ["20", "21", "22", "23"],
        "22",
        "P1: interior : exterior = 7 : 2, so exterior = 180 × 2/9 = 40° ⇒ n₁ = 360/40 = 9.\n"
        "P2: n(n − 3)/2 = 65 ⇒ n² − 3n − 130 = 0 ⇒ n₂ = 13.\n"
        "n₁ + n₂ = 9 + 13 = 22.\n"
        "Answer: 22",
        None,
    ),
    (
        "Number of sides of two regular polygons are in ratio 2 : 3 and each of their interior angles are in ratio 9 : 10. The number of sides of these two polygons are:",
        ["8, 12", "6, 9", "4, 6", "10, 15"],
        "8, 12",
        "Let the sides be 2k and 3k.\n"
        "Interior angles are 180 − 360/(2k) = 180 − 180/k and 180 − 360/(3k) = 180 − 120/k.\n"
        "10(180 − 180/k) = 9(180 − 120/k) ⇒ 1800 − 1800/k = 1620 − 1080/k ⇒ 180 = 720/k ⇒ k = 4.\n"
        "Sides = 8 and 12.\n"
        "Answer: 8, 12",
        None,
    ),
    (
        "There are two regular polygons with number of sides in the ratio 4 : 5, and interior angles are in the ratio 25 : 26. Find number of sides in both polygons.",
        ["8, 10", "20, 25", "12, 15", "16, 20"],
        "12, 15",
        "Let the sides be 4k and 5k.\n"
        "Interior angles are 180 − 90/k and 180 − 72/k.\n"
        "26(180 − 90/k) = 25(180 − 72/k) ⇒ 4680 − 2340/k = 4500 − 1800/k ⇒ 180 = 540/k ⇒ k = 3.\n"
        "Sides = 12 and 15.\n"
        "Answer: 12, 15",
        None,
    ),
    (
        "8 interior angles of a polygon are 165° each and the remaining interior angles are 168° each. Find the number of diagonals in the polygon.",
        ["350", "464", "275", "405"],
        "350",
        "8 × 165 + (n − 8) × 168 = (n − 2) × 180.\n"
        "1320 + 168n − 1344 = 180n − 360 ⇒ 168n − 24 = 180n − 360 ⇒ 12n = 336 ⇒ n = 28.\n"
        "Diagonals = 28 × 25/2 = 350.\n"
        "Answer: 350",
        None,
    ),
    (
        "If the sum of all interior angles except one of a polygon is 2730°, then the number of sides must be? (All interior angles are less than 180°)",
        ["19", "17", "18", "20"],
        "18",
        "(n − 2) × 180 = 2730 + x, where x is the left-out interior angle and 0° < x < 180°.\n"
        "For n = 18: (18 − 2) × 180 = 2880 ⇒ x = 2880 − 2730 = 150°, which is valid.\n"
        "For n = 17 the total 2700° is already less than 2730°, so it is impossible.\n"
        "Answer: 18",
        None,
    ),
    (
        "The interior angles of a polygon are in AP, the smallest interior angle is 100°, and common difference is 4°, then find the number of sides.",
        ["5", "20", "12", "8"],
        "5",
        "Sum of the AP = n/2 [2(100) + (n − 1)4] = 2n² + 98n.\n"
        "This must equal (n − 2) × 180 ⇒ 2n² + 98n = 180n − 360 ⇒ n² − 41n + 180 = 0.\n"
        "(n − 5)(n − 36) = 0 ⇒ n = 5 or 36.\n"
        "n = 36 gives a largest angle of 100 + 35 × 4 = 240° (> 180°), so it is rejected.\n"
        "Answer: 5",
        None,
    ),
    (
        "A closed polygon has six sides and one of its angles is 30° greater than each of the other five equal angles. What is the value of one of the equal angles?",
        ["55°", "115°", "125°", "110°"],
        "115°",
        "Sum of interior angles of a hexagon = (6 − 2) × 180° = 720°.\n"
        "Let each equal angle be x: 5x + (x + 30) = 720 ⇒ 6x = 690 ⇒ x = 115°.\n"
        "Answer: 115°",
        None,
    ),
    (
        "If a star figure is formed by elongating the sides of a regular pentagon, then the measure of each angle at the angular points of the star figure is:",
        ["36°", "48°", "32°", "30°"],
        "36°",
        "Each interior angle of a regular pentagon = 108°, so each base angle of a point-triangle of the star = 180° − 108° = 72°.\n"
        "Angle at each point of the star = 180° − 2 × 72° = 36°.\n"
        "Answer: 36°",
        None,
    ),
    (
        "ABCDE is a regular pentagon. O is a point inside the pentagon such that AOB is an equilateral triangle. What is ∠OEA?",
        ["66°", "48°", "54°", "72°"],
        "66°",
        "Each interior angle of a regular pentagon = 108°, so ∠EAB = 108°.\n"
        "△AOB is equilateral ⇒ ∠OAB = 60° and OA = AB = AE (all equal to the side).\n"
        "∠EAO = 108° − 60° = 48°.\n"
        "In isosceles △AEO (AE = AO): ∠OEA = (180° − 48°)/2 = 66°.\n"
        "Answer: 66°",
        None,
    ),
    (
        "One angle of a pentagon is 140°. If the remaining angles are in the ratio 1 : 2 : 3 : 4, the size of the greatest angle is:",
        ["150°", "180°", "160°", "170°"],
        "160°",
        "Sum of interior angles of a pentagon = 540°.\n"
        "Remaining four angles total 540° − 140° = 400°, shared in the ratio 1 : 2 : 3 : 4 (10 parts) ⇒ 1 part = 40°.\n"
        "Greatest angle = 4 × 40° = 160°.\n"
        "Answer: 160°",
        None,
    ),
    (
        "The area of a regular polygon with a side of 8 cm is 112 cm². If the perpendicular distance from the centre to the side of the polygon is 7 cm, then the number of sides of the polygon is:",
        ["7", "4", "6", "5"],
        "4",
        "Area = (1/2) × perimeter × apothem = (1/2) × (8n) × 7 = 28n.\n"
        "28n = 112 ⇒ n = 4.\n"
        "Answer: 4",
        None,
    ),
    (
        "Find the apothem of a regular pentagon with side length 10 cm and area 172 cm².",
        ["6.8 cm", "7.5 cm", "6.2 cm", "7.0 cm"],
        "6.8 cm",
        "Area = (1/2) × perimeter × apothem, and perimeter = 5 × 10 = 50 cm.\n"
        "172 = (1/2) × 50 × a = 25a ⇒ a = 6.88 ≈ 6.8 cm.\n"
        "Answer: 6.8 cm",
        None,
    ),
    (
        "The area of a regular hexagon is made of how many equilateral triangles?",
        ["3", "4", "5", "6"],
        "6",
        "Joining the centre of a regular hexagon to all six vertices splits it into 6 congruent equilateral triangles, each with side equal to the side of the hexagon.\n"
        "Answer: 6",
        None,
    ),
    (
        "A regular hexagon has a perimeter of 72 cm. What is its area?",
        ["374.12 cm²", "449.76 cm²", "670.32 cm²", "748.15 cm²"],
        "374.12 cm²",
        "Perimeter 72 cm ⇒ side = 72/6 = 12 cm.\n"
        "Area = (3√3/2)a² = (3√3/2) × 144 = 216√3 = 216 × 1.732 = 374.12 cm².\n"
        "Answer: 374.12 cm²",
        None,
    ),
    (
        "If the area of a regular hexagon is 4860√3 cm², find the length of each side.",
        ["18√10 cm", "44.2 cm", "6√6 cm", "11√4 cm"],
        "18√10 cm",
        "(3√3/2)a² = 4860√3 ⇒ (3/2)a² = 4860 ⇒ a² = 3240.\n"
        "a = √3240 = √(324 × 10) = 18√10 cm.\n"
        "Answer: 18√10 cm",
        None,
    ),
    (
        "A regular hexagonal mirror has a side of 18 cm. If 12% of the mirror area is covered by the frame, what is the visible glass area?",
        ["690.2 cm²", "710.5 cm²", "740.7 cm²", "758.6 cm²"],
        "740.7 cm²",
        "Area of the hexagon = (3√3/2) × 18² = 486√3 = 486 × 1.732 = 841.75 cm².\n"
        "The frame covers 12%, so the visible glass = 88% of 841.75 = 740.7 cm².\n"
        "Answer: 740.7 cm²",
        None,
    ),
    (
        "A field whose area is 2400√3 sq. m is in the shape of a regular hexagon. If the cost of fencing the field is Rs. 16.80/m, then find the total cost required to completely fence the field.",
        ["4032", "2212", "4872", "2864"],
        "4032",
        "(3√3/2)a² = 2400√3 ⇒ a² = 1600 ⇒ a = 40 m.\n"
        "Perimeter = 6 × 40 = 240 m.\n"
        "Cost = 240 × 16.80 = Rs. 4032.\n"
        "Answer: 4032",
        None,
    ),
    (
        "A regular hexagon is inscribed inside a circle of radius 14 cm. Find the area of the hexagon.",
        ["438.54 cm²", "509.21 cm²", "598.45 cm²", "638.76 cm²"],
        "509.21 cm²",
        "For a regular hexagon inscribed in a circle, side = radius = 14 cm.\n"
        "Area = (3√3/2) × 196 = 294√3 = 294 × 1.732 = 509.21 cm².\n"
        "Answer: 509.21 cm²",
        None,
    ),
    (
        "If the area of a regular hexagon is equal to the area of an equilateral triangle of side 12 cm, then the length, in cm, of each side of the hexagon is:",
        ["4√6", "2√6", "√6", "6√6"],
        "2√6",
        "Area of the equilateral triangle = (√3/4) × 12² = 36√3.\n"
        "(3√3/2)a² = 36√3 ⇒ a² = 24 ⇒ a = 2√6 cm.\n"
        "Answer: 2√6",
        None,
    ),
    (
        "The area of a regular hexagon is equal to the area of a square. What is the ratio of the perimeter of the regular hexagon to the perimeter of the square?",
        ["√(6√3) : √(3√6)", "2√3 : √(6√2)", "√(6√3) : 2", "√(6√3) : 2√3"],
        "√(6√3) : 2√3",
        "Let the hexagon side be h and the square side be s. Equal areas: (3√3/2)h² = s² ⇒ s = h√(3√3/2).\n"
        "Ratio of perimeters = 6h : 4s = 6 : 4√(3√3/2) = 3 : 2√(3√3/2) = √(6√3) : 2√3.\n"
        "Numerically 6 : 6.447 ≈ 1 : 1.075, and √(6√3) : 2√3 = 3.224 : 3.464 ≈ 1 : 1.075.\n"
        "Answer: √(6√3) : 2√3",
        None,
    ),
    (
        "Two similar hexagons have their perimeters in the ratio 5 : 7. If the smaller hexagon has an area of 75 cm², what is the area of the larger hexagon?",
        ["147 cm²", "125 cm²", "130 cm²", "159 cm²"],
        "147 cm²",
        "For similar figures, ratio of areas = (ratio of perimeters)² = (5/7)² = 25/49.\n"
        "Larger area = 75 × 49/25 = 147 cm².\n"
        "Answer: 147 cm²",
        None,
    ),
    (
        "In the given figure, PQRSTU is a regular hexagon of side 12 cm. What is the area (in cm²) of triangle SQU?",
        ["162√3", "144√3", "108√3", "54√3"],
        "108√3",
        "Q, S and U are alternate vertices of the regular hexagon, so △SQU is equilateral with side = √3 × 12 = 12√3 cm.\n"
        "Area = (√3/4)(12√3)² = (√3/4) × 432 = 108√3 cm².\n"
        "Answer: 108√3",
        f"{FIG}/q49.png",
    ),
    (
        "ABCDEF is a regular hexagon with side 12 cm. P, Q and R are the midpoints of AF, ED and BC respectively. Find the area of ∆PQR.",
        ["72√3 cm²", "81√3 cm²", "54√3 cm²", "90√3 cm²"],
        "81√3 cm²",
        "Place the hexagon with centre at the origin and circumradius 12:\n"
        "A(6, 6√3), B(12, 0), C(6, −6√3), D(−6, −6√3), E(−12, 0), F(−6, 6√3).\n"
        "P = midpoint of AF = (0, 6√3); Q = midpoint of ED = (−9, −3√3); R = midpoint of BC = (9, −3√3).\n"
        "QR = 18 and the height from P to QR = 6√3 + 3√3 = 9√3.\n"
        "Area = (1/2) × 18 × 9√3 = 81√3 cm².\n"
        "Answer: 81√3 cm²",
        f"{FIG}/q50.png",
    ),
    (
        "Let PQRSTU be a regular hexagon. The ratio of the area of the triangle PRT to that of the hexagon PQRSTU is:",
        ["0.4", "0.5", "0.75", "0.625"],
        "0.5",
        "P, R and T are alternate vertices, so △PRT is equilateral with side √3·a.\n"
        "Area of △PRT = (√3/4)(3a²) = (3√3/4)a², while the hexagon = (3√3/2)a².\n"
        "Ratio = (3√3/4) ÷ (3√3/2) = 1/2 = 0.5.\n"
        "Answer: 0.5",
        None,
    ),
    (
        "In the given figure, the side of the regular hexagon is 12 cm. Find the area of ∆ECD.",
        ["33√3 cm²", "36√3 cm²", "35√3 cm²", "32√3 cm²"],
        "36√3 cm²",
        "From the figure E, D and C are three consecutive vertices of the regular hexagon, so ED = DC = 12 cm and ∠EDC = 120°.\n"
        "Area of △ECD = (1/2) × 12 × 12 × sin120° = 72 × (√3/2) = 36√3 cm².\n"
        "Answer: 36√3 cm²",
        f"{FIG}/q52.png",
    ),
    (
        "In the given figure, ABCDEF is a regular hexagon whose side is 12 cm. What is the shaded area (in cm²)?",
        ["54√3", "36√3", "48√3", "52√3"],
        "54√3",
        "Take the hexagon with centre at the origin and circumradius 12:\n"
        "A(−12, 0), B(−6, 6√3), C(6, 6√3), D(12, 0), E(6, −6√3), F(−6, −6√3).\n"
        "The shaded piece is the trapezium B(−6, 6√3), C(6, 6√3), the point where CF meets AD i.e. (0, 0), and the foot of B on AD i.e. (−6, 0).\n"
        "Parallel sides are BC = 12 and the lower side = 6, with height 6√3.\n"
        "Area = (1/2)(12 + 6)(6√3) = 54√3 cm².\n"
        "Answer: 54√3",
        f"{FIG}/q53.png",
    ),
    (
        "A is the centre of the given regular hexagon. Find the area of the shaded region.",
        ["430√3 cm²", "434√3 cm²", "432√3 cm²", "440√3 cm²"],
        "432√3 cm²",
        "The side of the regular hexagon PQRSTU is 24 cm, so its area = (3√3/2) × 24² = 864√3 cm².\n"
        "The lines drawn through the centre A cut the hexagon into congruent pieces and, by symmetry, the shaded pieces make up exactly half of the figure.\n"
        "Shaded area = (1/2) × 864√3 = 432√3 cm².\n"
        "Answer: 432√3 cm²",
        f"{FIG}/q54.png",
    ),
    (
        "ABCDEF is a regular hexagon whose area is 180 cm². Find the area of the shaded region.",
        ["9 cm²", "10 cm²", "12 cm²", "15 cm²"],
        "10 cm²",
        "Joining the centre to the vertices splits the hexagon into 6 equal triangles, so each has area 180/6 = 30 cm².\n"
        "The shaded triangle in the figure is one-third of one such triangle (the cevians of that triangle cut it into 3 equal parts).\n"
        "Shaded area = 30/3 = 10 cm².\n"
        "Answer: 10 cm²",
        f"{FIG}/q55.png",
    ),
    (
        "In the given figure, find the ratio of the shaded area to the un-shaded area.",
        ["1/8", "1/9", "1/10", "1/12"],
        "1/8",
        "The diagonals drawn in the figure cut the hexagon into 9 equal parts, of which the shaded triangle is 1 part.\n"
        "So shaded : un-shaded = 1 : (9 − 1) = 1 : 8.\n"
        "Answer: 1/8",
        f"{FIG}/q56.png",
    ),
    (
        "ABCDEF is a regular hexagon. Find the ratio of the area of the shaded region to the area of hexagon ABCDEF.",
        ["1/3", "3/10", "2/5", "1/2"],
        "1/3",
        "Joining alternate vertices of ABCDEF gives two overlapping equilateral triangles (a Star of David); the shaded part is the small regular hexagon common to both.\n"
        "If the hexagon side is a, each triangle has side a√3, and the inner hexagon of such a star has side (a√3)/3 = a/√3.\n"
        "Ratio of areas = (a/√3)² : a² = 1 : 3.\n"
        "Answer: 1/3",
        f"{FIG}/q57.png",
    ),
    (
        "An equilateral triangle of area 300 cm² is cut from its three vertices to form a regular hexagon. The area of the hexagon is what % of the area of the triangle?",
        ["66.66%", "33.33%", "83.33%", "56.41%"],
        "66.66%",
        "Cutting the three corners of an equilateral triangle to leave a regular hexagon removes 3 small equilateral triangles, each of side one-third of the original side.\n"
        "Each small triangle = (1/3)² = 1/9 of the original area, so the removed part = 3/9 = 1/3.\n"
        "Hexagon = 1 − 1/3 = 2/3 = 66.66% of the triangle.\n"
        "Answer: 66.66%",
        None,
    ),
    (
        "ABCDEF is a regular polygon. Two poles at C and D are standing vertically and subtend angles of elevation 30° and 60° at A respectively. What is the ratio of the height of the pole at C to that of the pole at D?",
        ["1 : √3", "1 : 2√3", "2√3 : 1", "2 : √3"],
        "1 : 2√3",
        "Let the side of the regular hexagon ABCDEF be a. Then AC = √3·a (short diagonal) and AD = 2a (long diagonal).\n"
        "Height of the pole at C = AC × tan30° = √3a × (1/√3) = a.\n"
        "Height of the pole at D = AD × tan60° = 2a × √3 = 2√3a.\n"
        "Ratio = a : 2√3a = 1 : 2√3.\n"
        "Answer: 1 : 2√3",
        None,
    ),
    (
        "A square whose side is 2 cm has its corners cut away so as to form an octagon with all sides equal. Then the length of each side of the octagon is:",
        ["√2/(√2+1)", "2/(√2+1)", "√2/(√2−1)", "2/(√2−1)"],
        "2/(√2+1)",
        "Let x be cut from each end of every side. The slanting side of the octagon = x√2 and the straight side = 2 − 2x.\n"
        "x√2 = 2 − 2x ⇒ x(√2 + 2) = 2 ⇒ x = 2/(√2 + 2).\n"
        "Side = 2 − 2x = 2√2/(√2 + 2) = 2/(√2 + 1).\n"
        "Answer: 2/(√2+1)",
        None,
    ),
    (
        "A regular octagonal stop sign has a side length of 10 cm. Calculate its area.",
        ["482.8 cm²", "72√3 cm²", "363 cm²", "48√3 cm²"],
        "482.8 cm²",
        "Area of a regular octagon = 2(1 + √2)a².\n"
        "= 2(1 + √2) × 100 = 200 × 2.4142 = 482.8 cm².\n"
        "Answer: 482.8 cm²",
        None,
    ),
    (
        "A circle with radius R circumscribes a regular octagon. What is the area of the octagon?",
        ["2√2R²", "2R²", "2(1+√2)R²", "√2R²"],
        "2√2R²",
        "Area of a regular n-gon inscribed in a circle of radius R = (1/2)nR² sin(360°/n).\n"
        "For n = 8: (1/2)(8)R² sin45° = 4R² × (√2/2) = 2√2R².\n"
        "Answer: 2√2R²",
        None,
    ),
]


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))

    end = START_INDEX + len(QUESTIONS)
    if end > len(bank):
        raise SystemExit(f"bank has only {len(bank)} entries, need {end}")

    for offset, entry in enumerate(bank[START_INDEX:end]):
        if "[Add content]" not in (entry.get("question") or ""):
            raise SystemExit(f"index {START_INDEX + offset} ({entry['id']}) is not a placeholder")

    for offset, (question, options, answer, solution, image) in enumerate(QUESTIONS):
        if answer not in options:
            raise SystemExit(f"Q{offset + 1}: answer {answer!r} missing from options")
        if len(set(options)) != 4:
            raise SystemExit(f"Q{offset + 1}: options are not 4 distinct values")

        index = START_INDEX + offset
        new_entry = {"id": bank[index]["id"], "question": question}
        if image:
            new_entry["image"] = image
        new_entry["options"] = options
        new_entry["correctAnswer"] = answer
        new_entry["solution"] = solution
        bank[index] = new_entry

    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {len(QUESTIONS)} questions: {bank[START_INDEX]['id']} .. {bank[end - 1]['id']}")


if __name__ == "__main__":
    main()
