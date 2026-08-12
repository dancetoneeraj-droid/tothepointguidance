"""3D Mensuration Sheet-4 (Sphere and Hemisphere) -> maths_mensuration_3d_189 onward.

The sheet highlights an answer for only about a third of its questions, so every
answer below was worked out from scratch; where a highlight exists it agrees
with the derivation.

Q16 is the one item the sheet cannot satisfy geometrically: r1 + r2 = 10 with a
combined volume of 880 cm3 forces r1r2 = 26 1/3, which makes the radii complex.
The standard identity answer, 26 1/3, is stored.
"""

from mensuration3d_import_lib import import_sheet

START_INDEX = 187  # maths_mensuration_3d_189

QUESTIONS = [
    (
        "The volumes of two spheres are in the ratio of 512 : 3375. The ratio of their surface areas is:",
        ["64:225", "49:325", "27:144", "68:125"],
        "64:225",
        "Volumes go as the cube of the radius: (r₁/r₂)³ = 512/3375, so r₁ : r₂ = 8 : 15.\n"
        "Surface areas go as the square of the radius: 8² : 15² = 64 : 225.\n"
        "Answer: 64:225",
    ),
    (
        "A sphere and a cube have equal surface areas. The ratio of the volume of the sphere to that of the cube is:",
        ["√3 : √π", "√6 : √π", "√π : √8", "√2 : √π"],
        "√6 : √π",
        "Equal areas: 4πr² = 6a², so a = r√(2π/3).\n"
        "Ratio = (4/3)πr³ ÷ r³(2π/3)^(3/2) = 2 ÷ √(2π/3) = √(6/π).\n"
        "Answer: √6 : √π",
    ),
    (
        "Find the surface area of the sphere whose radius is 112 cm and π = 22/7 (in cm²).",
        ["177696", "187696", "157696", "167696"],
        "157696",
        "Surface area = 4πr² = 4 × (22/7) × 112².\n"
        "112²= 12544 and (22/7) × 12544 = 39424, so the area is 4 × 39424 = 157696 cm².\n"
        "Answer: 157696",
    ),
    (
        "The curved surface area of a sphere is 9856 cm². Find its diameter in m.",
        ["2.8", "0.28", "5.6", "0.56"],
        "0.56",
        "4 × (22/7) × r² = 9856 gives r² = 9856 × 7/88 = 784, so r = 28 cm.\n"
        "Diameter = 56 cm = 0.56 m.\n"
        "Answer: 0.56",
    ),
    (
        "The cost of painting a spherical vessel of radius 7 cm is ₹18,480. What is the cost of painting per square centimetre? (use π = 22/7)",
        ["₹33", "₹32", "₹30", "₹31"],
        "₹30",
        "Surface area = 4 × (22/7) × 7² = 616 cm².\n"
        "Rate = 18480/616 = ₹30 per cm².\n"
        "Answer: ₹30",
    ),
    (
        "The diameter of a sphere is 14.7 m. What will be the volume of the sphere?",
        ["1663.893 m³", "1873.487 m³", "1693.563 m³", "1783.723 m³"],
        "1663.893 m³",
        "r = 14.7/2 = 7.35 m, so r³ = 397.065375.\n"
        "V = (4/3)(22/7)(397.065375) = 88 × 397.065375 ÷ 21 = 1663.893 m³.\n"
        "Answer: 1663.893 m³",
    ),
    (
        "The volume of the hemisphere (to the nearest integer) with a radius of 5.5 cm is (use π = 3.14):",
        ["378 cm³", "325 cm³", "348 cm³", "362 cm³"],
        "348 cm³",
        "V = (2/3)πr³ = (2/3)(3.14)(166.375) = 348.3 cm³.\n"
        "Rounded to the nearest integer this is 348 cm³.\n"
        "Answer: 348 cm³",
    ),
    (
        "What will be the volume of a sphere with radius 65 cm? (approximately)",
        ["4.5 × 10⁶ cm³", "6 × 10⁶ cm³", "1.15 × 10⁶ cm³", "2 × 10⁶ cm³"],
        "1.15 × 10⁶ cm³",
        "V = (4/3)π(65)³ = (4/3)π(274625) ≈ 1150347 cm³.\n"
        "That is about 1.15 × 10⁶ cm³.\n"
        "Answer: 1.15 × 10⁶ cm³",
    ),
    (
        "What is the radius of a sphere having a volume of 38808 cm³?",
        ["27 cm", "21 cm", "24 cm", "18 cm"],
        "21 cm",
        "(4/3)(22/7)r³ = 38808 gives r³ = 38808 × 21/88 = 9261.\n"
        "r = ∛9261 = 21 cm.\n"
        "Answer: 21 cm",
    ),
    (
        "If the volume of a sphere is 4851 cm³, then its surface area (in cm²) is: (Take π = 22/7)",
        ["1323", "2772", "1337", "1386"],
        "1386",
        "(88/21)r³ = 4851 gives r³ = 1157.625, so r = 10.5 cm.\n"
        "Surface area = 4 × (22/7) × 110.25 = 1386 cm².\n"
        "Answer: 1386",
    ),
    (
        "The surface area of a sphere is 2464 cm². Calculate its volume. (Use π = 22/7)",
        ["11598.67 cm³", "11498.67 cm³", "11488.67 cm³", "11478.67 cm³"],
        "11498.67 cm³",
        "4 × (22/7) × r² = 2464 gives r² = 196, so r = 14 cm.\n"
        "V = (4/3)(22/7)(2744) = 241472/21 = 11498.67 cm³.\n"
        "Answer: 11498.67 cm³",
    ),
    (
        "The cost of painting the surface of a large spherical ball at the rate of ₹2.40 per sq cm is ₹9240. What is the radius (in cm) of the ball? (Take π = 22/7)",
        ["16.5", "21", "18.5", "17.5"],
        "17.5",
        "Painted area = 9240/2.40 = 3850 cm².\n"
        "4 × (22/7) × r² = 3850 gives r² = 306.25, so r = 17.5 cm.\n"
        "Answer: 17.5",
    ),
    (
        "If the radius of a sphere is increased by 2 cm, its surface area increases by 704 cm². What was the radius of the sphere before the increase? (Use π = 22/7)",
        ["12 cm", "11 cm", "13 cm", "14 cm"],
        "13 cm",
        "4π[(r + 2)² − r²] = 704 becomes (88/7)(4r + 4) = 704.\n"
        "4r + 4 = 56, so r = 13 cm.\n"
        "Answer: 13 cm",
    ),
    (
        "Three solid metallic spheres of radii 1 cm, 6 cm and 8 cm, respectively, are melted and recast into a single solid sphere. The radius of the new sphere so formed is:",
        ["9.0 cm", "5.9 cm", "7.7 cm", "8.5 cm"],
        "9.0 cm",
        "Volume adds, so R³ = 1³ + 6³ + 8³ = 1 + 216 + 512 = 729.\n"
        "R = 9.0 cm.\n"
        "Answer: 9.0 cm",
    ),
    (
        "A metallic solid spherical ball of radius 3 cm is melted and recast into three spherical balls. The radii of two of these balls are 2 cm and 1.5 cm. What is the surface area (in cm²) of the third ball?",
        ["25π/2", "25π/4", "50π", "25π"],
        "25π",
        "27 = 8 + 3.375 + r³ gives r³ = 15.625, so r = 2.5 cm.\n"
        "Surface area = 4π(2.5)² = 25π cm².\n"
        "Answer: 25π",
    ),
    (
        "The sum of the radii of two spheres is 10 cm and the sum of their volumes is 880 cm³. What will be the product of their radii?",
        ["25 2/3 cm²", "26 1/3 cm²", "33 1/3 cm²", "27 1/3 cm²"],
        "26 1/3 cm²",
        "(4/3)(22/7)(r₁³ + r₂³) = 880 gives r₁³ + r₂³ = 210.\n"
        "(r₁ + r₂)³ − 3r₁r₂(r₁ + r₂) = 210 becomes 1000 − 30r₁r₂ = 210.\n"
        "r₁r₂ = 790/30 = 26 1/3 cm²\n"
        "Answer: 26 1/3 cm²",
    ),
    (
        "Air is leaking from a spherical-shaped advertising balloon at the rate of 24 cubic feet per minute. If the radius of the balloon is 8 feet, how long would it take for the balloon to empty? Round your answer to the nearest minute. (Use π = 3.14)",
        ["89 minutes", "80 minutes", "65 minutes", "94 minutes"],
        "89 minutes",
        "V = (4/3)(3.14)(512) = 2143.6 cubic feet.\n"
        "Time = 2143.6/24 = 89.3 minutes, i.e. 89 minutes to the nearest minute.\n"
        "Answer: 89 minutes",
    ),
    (
        "The length of the side of a cube is 5.6 cm. What is the volume of the largest sphere that can be taken out of the cube?",
        ["91.98 cm³", "99.96 cm³", "96.98 cm³", "90.69 cm³"],
        "91.98 cm³",
        "The largest sphere has diameter equal to the edge, so r = 2.8 cm.\n"
        "V = (4/3)(22/7)(21.952) = 91.98 cm³.\n"
        "Answer: 91.98 cm³",
    ),
    (
        "The length of the largest possible rod that can be placed in a cubical room is 42√3 m. The surface area (in sq m) of the largest possible sphere that fits within the cubical room is:",
        ["3590", "4589", "2564", "5544"],
        "5544",
        "The rod is the cube's diagonal: a√3 = 42√3, so a = 42 m.\n"
        "The largest sphere has r = 21 m and area 4 × (22/7) × 441 = 5544 sq m.\n"
        "Answer: 5544",
    ),
    (
        "There is a wooden sphere of radius 15√3 cm. The total surface area of the largest possible cube cut from the sphere will be:",
        ["540 cm²", "600 cm²", "5400 cm²", "900 cm²"],
        "5400 cm²",
        "The cube's diagonal equals the sphere's diameter: a√3 = 30√3, so a = 30 cm.\n"
        "TSA = 6a² = 6 × 900 = 5400 cm².\n"
        "Answer: 5400 cm²",
    ),
    (
        "What is the radius of the sphere passing through the corners of the cuboid with edges 8 cm, 12 cm and 24 cm?",
        ["10.5 cm", "14 cm", "21 cm", "28 cm"],
        "14 cm",
        "The sphere's diameter is the cuboid's diagonal = √(64 + 144 + 576) = √784 = 28 cm.\n"
        "Radius = 14 cm.\n"
        "Answer: 14 cm",
    ),
    (
        "The ratio between the volume of a sphere and the volume of a circumscribing right circular cylinder is:",
        ["1 : 1", "2 : 1", "1 : 2", "2 : 3"],
        "2 : 3",
        "The circumscribing cylinder has the same radius r and height 2r.\n"
        "Ratio = (4/3)πr³ : 2πr³ = 2 : 3.\n"
        "Answer: 2 : 3",
    ),
    (
        "A metallic sphere of diameter 40 cm is melted into smaller spheres of radius 0.5 cm. How many such small balls can be made?",
        ["6400", "64,000", "32,000", "3200"],
        "64,000",
        "Big radius = 20 cm, so the count is (20/0.5)³ = 40³.\n"
        "40³ = 64000 balls.\n"
        "Answer: 64,000",
    ),
    (
        "A spherical ball of radius 35 cm is melted to form 8000 small balls of equal size. In this process the surface area of the solid is increased by:",
        ["1900%", "19900%", "190%", "900%"],
        "1900%",
        "8000r³ = 35³ gives r = 35/20 = 1.75 cm.\n"
        "New area ÷ old area = 8000 × 1.75²/35² = 20, so the area becomes 20 times.\n"
        "Increase = 19 times = 1900%.\n"
        "Answer: 1900%",
    ),
    (
        "If 2744 identical small spheres are made out of a big sphere of radius 7 cm, then what is the surface area of each small sphere?",
        ["2π cm²", "3π cm²", "π cm²", "4π cm²"],
        "π cm²",
        "2744r³ = 7³ and ∛2744 = 14, so r = 7/14 = 0.5 cm.\n"
        "Surface area = 4π(0.5)² = π cm².\n"
        "Answer: π cm²",
    ),
    (
        "The diameter of a solid sphere is 3 cm. It is melted and drawn into a wire of diameter 8 mm. The length of the wire is:",
        ["25 1/4 cm", "26 3/8 cm", "28 1/8 cm", "32 1/4 cm"],
        "28 1/8 cm",
        "Sphere volume = (4/3)π(1.5)³ = 4.5π cm³, and the wire radius is 0.4 cm.\n"
        "π(0.4)²h = 4.5π gives h = 4.5/0.16 = 28.125 cm = 28 1/8 cm\n"
        "Answer: 28 1/8 cm",
    ),
    (
        "A solid metallic sphere of radius 8.4 cm is melted and recast into a right circular cylinder of radius 12 cm. What is the height of the cylinder?",
        ["6.5 cm", "7.0 cm", "5.5 cm", "6.0 cm"],
        "5.5 cm",
        "(4/3)π(8.4)³ = π(12)²h gives 4 × 592.704 = 3 × 144h.\n"
        "h = 2370.816/432 = 5.488 ≈ 5.5 cm.\n"
        "Answer: 5.5 cm",
    ),
    (
        "A solid sphere of radius 3 cm is melted to form a hollow cylinder of height 4 cm and external diameter 10 cm. What is the thickness of the cylinder?",
        ["0.42 cm", "0.46 cm", "0.50 cm", "1.00 cm"],
        "1.00 cm",
        "Sphere volume = (4/3)π(27) = 36π cm³.\n"
        "π(5² − r²)(4) = 36π gives 25 − r² = 9, so r = 4 cm.\n"
        "Thickness = 5 − 4 = 1.00 cm.\n"
        "Answer: 1.00 cm",
    ),
    (
        "Two metallic right circular cones having their heights of 5.2 cm and 6 cm and the radii of their bases 2.8 cm each, have been melted together and recast into a sphere. The diameter of the sphere is:",
        ["6.4 cm", "5.0 cm", "6.2 cm", "5.6 cm"],
        "5.6 cm",
        "Cones together: (1/3)π(2.8)²(5.2 + 6) = (1/3)π(87.808).\n"
        "(4/3)πR³ = (1/3)π(87.808) gives R³ = 21.952, so R = 2.8 cm.\n"
        "Diameter = 5.6 cm.\n"
        "Answer: 5.6 cm",
    ),
    (
        "Some marbles, each of diameter 4.2 cm, are dropped into a cylindrical beaker containing some water and are fully submerged. The diameter of the beaker is 28 cm. Find how many marbles have been dropped in it if the water rises by 15.75 cm.",
        ["225", "275", "250", "290"],
        "250",
        "Water displaced = π(14)²(15.75) = 3087π cm³.\n"
        "Each marble = (4/3)π(2.1)³ = 12.348π cm³.\n"
        "Number = 3087/12.348 = 250.\n"
        "Answer: 250",
    ),
    (
        "The largest sphere is to be carved out of a right circular cylinder of radius 8 cm and height 16 cm. Find the volume of the sphere. (Take π = 22/7)",
        ["2200.50 cm³", "2321.63 cm³", "2140.70 cm³", "2145.52 cm³"],
        "2145.52 cm³",
        "The largest sphere takes the cylinder's radius, r = 8 cm (its diameter 16 cm equals the height).\n"
        "V = (4/3)(22/7)(512) = 45056/21 = 2145.52 cm³.\n"
        "Answer: 2145.52 cm³",
    ),
    (
        "A cylindrical can whose base is horizontal and is of internal radius 3.5 cm contains sufficient water so that when a solid sphere is placed inside it, the water just covers the sphere. The sphere fits in the can exactly. What was the depth (in cm) of water in the can before the sphere was put in?",
        ["25/3", "17/3", "7/3", "14/3"],
        "7/3",
        "The sphere fits exactly, so r = 3.5 cm and the water finally stands at 2r = 7 cm.\n"
        "Water volume = π(3.5)²(7) − (4/3)π(3.5)³ = 85.75π − 57.1667π = 28.5833π.\n"
        "Depth before = 28.5833π ÷ 12.25π = 7/3 cm.\n"
        "Answer: 7/3",
    ),
    (
        "The inner and outer radii of a hollow metal cylinder are 1.1 cm and 4.3 cm respectively, and its height is 16 2/3 cm. It is melted and made into a sphere. What will be the surface area (in cm²) of the sphere?",
        ["196π", "100π", "256π", "144π"],
        "144π",
        "Metal volume = π(4.3² − 1.1²)(50/3) = π(17.28)(50/3) = 288π cm³.\n"
        "(4/3)πR³ = 288π gives R³ = 216, so R = 6 cm.\n"
        "Surface area = 4π(36) = 144π\n"
        "Answer: 144π",
    ),
    (
        "A hollow metal sphere of internal and external radii 5 cm and 6 cm, respectively, is melted into a solid cone of base radius 5.2 cm. What is the height (in cm, rounded off to 1 decimal place) of the cone?",
        ["11.8", "12.8", "13.5", "14.5"],
        "13.5",
        "Shell volume = (4/3)π(6³ − 5³) = (4/3)π(91).\n"
        "(1/3)π(5.2)²h = (4/3)π(91) gives h = 4 × 91/27.04 = 13.46.\n"
        "Rounded to one decimal place, h = 13.5\n"
        "Answer: 13.5",
    ),
    (
        "A hollow spherical shell is made of a metal of density 36 g/cm³. Its internal and external radii are 9 cm and 11 cm, respectively. What is the weight (in kg) of the shell? (Take π = 22/7)",
        ["92.52", "90.816", "87.816", "92.75"],
        "90.816",
        "Volume = (4/3)(22/7)(11³ − 9³) = (88/21)(602) = 2522.667 cm³.\n"
        "Weight = 2522.667 × 36 = 90816 g = 90.816 kg.\n"
        "Answer: 90.816",
    ),
    (
        "A spherical metallic shell with 6 cm external radius weighs 6688 g. What is the thickness of the shell if the density of the metal is 10.5 g per cm³? (Take π = 22/7)",
        ["2 cm", "3 cm", "2 1/2 cm", "4 cm"],
        "2 cm",
        "Metal volume = 6688/10.5 = 636.95 cm³.\n"
        "(88/21)(216 − r³) = 636.95 gives 216 − r³ = 152, so r = 4 cm.\n"
        "Thickness = 6 − 4 = 2 cm.\n"
        "Answer: 2 cm",
    ),
    (
        "A solid rubber sphere weighs 40 kg when its diameter is 8 cm. Using the same material, a hollow sphere is made with an outer diameter of 16 cm and inner diameter of 12 cm. What is its weight?",
        ["80 kg", "240 kg", "185 kg", "120 kg"],
        "185 kg",
        "Weight is proportional to volume, i.e. to the cube of the radius.\n"
        "Solid: 4³ = 64 corresponds to 40 kg; hollow: 8³ − 6³ = 296.\n"
        "Weight = 40 × 296/64 = 185 kg.\n"
        "Answer: 185 kg",
    ),
    (
        "The total surface area of a solid hemisphere is 166.32 sq cm. Find its curved surface area.",
        ["55.44 sq cm", "110.88 sq cm", "221.76 sq cm", "196.96 sq cm"],
        "110.88 sq cm",
        "TSA = 3πr² while CSA = 2πr², so CSA is two-thirds of the TSA.\n"
        "CSA = (2/3) × 166.32 = 110.88 sq cm.\n"
        "Answer: 110.88 sq cm",
    ),
    (
        "Find the total surface area of the hemisphere whose radius is 27 cm and π = 3.14.",
        ["6567.18", "6667.18", "6867.18", "6767.18"],
        "6867.18",
        "TSA = 3πr² = 3 × 3.14 × 729.\n"
        "3 × 3.14 = 9.42 and 9.42 × 729 = 6867.18 cm².\n"
        "Answer: 6867.18",
    ),
    (
        "A hemispherical bowl has radius 7.7 cm. It is to be painted from inside as well as outside. Find the cost of painting (in ₹) the bowl at ₹17 per 7 cm². (Take π = 22/7)",
        ["1810.16", "745.36", "1025.24", "1620.35"],
        "1810.16",
        "Painted area = 2 × 2πr² = 4 × (22/7) × 59.29 = 745.36 cm².\n"
        "Cost = (745.36/7) × 17 = 106.48 × 17 = ₹1810.16.\n"
        "Answer: 1810.16",
    ),
    (
        "If the diameter of a hemisphere is 63 cm, then what is the volume of the hemisphere?",
        ["72654.5 cm³", "61324.5 cm³", "65488.5 cm³", "69246.5 cm³"],
        "65488.5 cm³",
        "r = 31.5 cm, so r³ = 31255.875.\n"
        "V = (2/3)(22/7)(31255.875) = (44/21)(31255.875) = 65488.5 cm³.\n"
        "Answer: 65488.5 cm³",
    ),
    (
        "The volume of a hemisphere is 2425 1/2 cm³. Find its radius. (Take π = 22/7)",
        ["10 cm", "9.5 cm", "12 cm", "10.5 cm"],
        "10.5 cm",
        "(2/3)(22/7)r³ = 2425.5 gives r³ = 2425.5 × 21/44 = 1157.625.\n"
        "r = ∛1157.625 = 10.5 cm.\n"
        "Answer: 10.5 cm",
    ),
    (
        "How many litres of water can a hemispherical bowl of diameter 21 m hold? (1 m³ = 1000 L)",
        ["2100000 L", "2425500 L", "2322500 L", "2250500 L"],
        "2425500 L",
        "r = 10.5 m, so V = (2/3)(22/7)(1157.625) = 2425.5 m³.\n"
        "2425.5 × 1000 = 2425500 litres.\n"
        "Answer: 2425500 L",
    ),
    (
        "The volume of a solid hemisphere is 19,404 cm³. Its total surface area (in cm²) is: (Take π = 22/7)",
        ["2079", "3465", "2772", "4158"],
        "4158",
        "(44/21)r³ = 19404 gives r³ = 9261, so r = 21 cm.\n"
        "TSA = 3πr² = 3 × (22/7) × 441 = 4158 cm².\n"
        "Answer: 4158",
    ),
    (
        "The total surface area of a solid hemisphere is 1039.5 cm². The volume of the hemisphere is:",
        ["2225.5", "2530.6", "2425.5", "2525.6"],
        "2425.5",
        "3 × (22/7) × r² = 1039.5 gives r² = 110.25, so r = 10.5 cm.\n"
        "V = (2/3)(22/7)(1157.625) = 2425.5 cm³.\n"
        "Answer: 2425.5",
    ),
    (
        "A hemispherical solid of radius 21 cm is melted and made into a cylinder whose height is 14 cm. The volume of the cylinder is given by (a × bᵃ × c^b)π where a, b and c are prime. Then the value of (a + b)c is:",
        ["66", "42", "54", "35"],
        "35",
        "Hemisphere volume = (2/3)π(9261) = 6174π, so π R²(14) = 6174π and R = 21 cm.\n"
        "6174 = 2 × 3² × 7³, which matches a × bᵃ × c^b with a = 2, b = 3, c = 7.\n"
        "(a + b)c = 5 × 7 = 35.\n"
        "Answer: 35",
    ),
    (
        "20 identical solid hemispheres of radius 3 cm are melted to form a big solid hemisphere. What is the radius (in cm) of the biggest hemisphere formed, if 20% of the solid is wasted during the process?",
        ["3√2", "6", "6∛2", "3"],
        "6∛2",
        "Usable volume = 0.8 × 20 × (2/3)π(27) = (2/3)π(432).\n"
        "R³ = 432 = 216 × 2, so R = 6∛2 cm.\n"
        "Answer: 6∛2",
    ),
    (
        "Three toys are in the shape of a cylinder, a hemisphere and a cone. The three toys have the same base. The height of each toy is 2√2 cm. What is the ratio of the total surface areas of the cylinder, hemisphere and cone respectively?",
        ["4:3:(√2+1)", "4:3:(2+√2)", "2:1:(1+√2)", "4:3:2√2"],
        "4:3:(√2+1)",
        "A hemisphere's height is its radius, so r = 2√2 cm and every height is 2√2 cm.\n"
        "Cylinder TSA = 2πr(h + r) = 32π; hemisphere TSA = 3πr² = 24π.\n"
        "Cone: l = √(8 + 8) = 4, so TSA = πr(l + r) = 8π(√2 + 1).\n"
        "Ratio = 32 : 24 : 8(√2 + 1) = 4:3:(√2+1)",
    ),
    (
        "A hemispherical tank full of water is emptied by a pipe at the rate of 7.7 litres per second. How much time (in hours) will it take to empty 2/3 part of the tank, if the internal radius of the tank is 10.5 m?",
        ["185/6", "175/3", "185/3", "175/2"],
        "175/3",
        "Tank volume = (2/3)(22/7)(1157.625) = 2425.5 m³ = 2425500 litres.\n"
        "Two-thirds of it is 1617000 litres, emptied in 1617000/7.7 = 210000 seconds.\n"
        "210000/3600 = 175/3 hours.\n"
        "Answer: 175/3",
    ),
    (
        "A hemispherical bowl is made of 1 cm thick steel. The inside radius of the bowl is 4 cm. The volume of the steel (in cm³) used in making the bowl is:",
        ["41 4/3 π", "27 1/3 π", "35 1/3 π", "40 2/3 π"],
        "40 2/3 π",
        "Outer radius = 4 + 1 = 5 cm.\n"
        "Steel volume = (2/3)π(5³ − 4³) = (2/3)π(61) = 122π/3.\n"
        "122/3 = 40 2/3, so the volume is 40 2/3 π",
    ),
    (
        "The internal and external radii of a hollow hemispherical vessel are 6 cm and 7 cm respectively. What is the total surface area (in cm²) of the vessel?",
        ["177π", "174π", "183π", "189π"],
        "183π",
        "TSA = outer curved + inner curved + rim = 2πR² + 2πr² + π(R² − r²).\n"
        "= 2π(49) + 2π(36) + π(13) = 98π + 72π + 13π.\n"
        "Total = 183π",
    ),
    (
        "A metallic hemispherical bowl is made up of steel. The total steel used in making the bowl is 342π cm³. The bowl can hold 144π cm³ of water. What is the thickness (in cm) of the bowl and the curved surface area (in cm²) of the outer side?",
        ["6, 162π", "3, 162π", "6, 81π", "3, 81π"],
        "3, 162π",
        "(2/3)πr³ = 144π gives r³ = 216, so the inner radius is 6 cm.\n"
        "(2/3)π(R³ − 216) = 342π gives R³ = 729, so R = 9 cm and the thickness is 3 cm.\n"
        "Outer CSA = 2π(81) = 162π, so the pair is 3, 162π",
    ),
    (
        "The internal and external diameters of a hollow hemispherical vessel are 28 cm and 32 cm, respectively. The cost incurred to paint 1 sq cm of the vessel surface is ₹2.50. Find the total cost incurred to paint the vessel all over, correct to two decimals.",
        ["Rs 7,574.28", "Rs 7,745.28", "Rs 5774.28", "Rs 7547.28"],
        "Rs 7,574.28",
        "r = 14 cm and R = 16 cm.\n"
        "Painted area = 2πR² + 2πr² + π(R² − r²) = π(512 + 392 + 60) = 964π = 3029.71 cm².\n"
        "Cost = 3029.71 × 2.50 = Rs 7,574.28",
    ),
    (
        "A solid cone of base radius 7 cm and height 18 cm is melted and recast into a hollow metal hemisphere of internal and external radii 20 cm and R cm, respectively. What is the value of R (in cm)?",
        ["∛8144", "∛8441", "∛8448", "∛8568"],
        "∛8441",
        "Cone volume = (1/3)π(49)(18) = 294π cm³.\n"
        "(2/3)π(R³ − 8000) = 294π gives R³ − 8000 = 441, so R³ = 8441.\n"
        "Answer: ∛8441",
    ),
    (
        "A toy is in the form of a cone mounted on a hemisphere. The radius of the hemisphere and that of the cone is 36 cm and the height of the cone is 105 cm. The total surface area (in cm²) of the toy is:",
        ["6588 π", "5240 π", "6025 π", "5799 π"],
        "6588 π",
        "Slant height = √(36² + 105²) = √12321 = 111 cm.\n"
        "TSA = πrl + 2πr² = π(36)(111) + 2π(1296) = 3996π + 2592π.\n"
        "Total = 6588 π",
    ),
    (
        "To make a toy, a hemisphere is attached to one end of a cylinder and a cone is attached to the other end of the cylinder. The common radius of the cylinder, cone and hemisphere is 4.2 cm. The height of the cylinder and the height of the cone are 7 cm each. Find the volume (in cubic cm) of the toy.",
        ["863.25", "358.8", "672.672", "762.255"],
        "672.672",
        "Volume = (2/3)πr³ + πr²h + (1/3)πr²h with r = 4.2 cm and h = 7 cm.\n"
        "= π(49.392 + 123.48 + 41.16) = 214.032π.\n"
        "214.032 × 22/7 = 672.672",
    ),
    (
        "The radius of the base of a solid cylinder is 7 cm and its height is 21 cm. It is melted and converted into small bullets of the same size. Each bullet consists of two parts, a cylinder and a hemisphere on one of its bases. The total height of a bullet is 3.5 cm and the radius of its base is 2.1 cm. Approximately how many complete bullets can be obtained?",
        ["83", "89", "74", "79"],
        "83",
        "Cylinder volume = π(49)(21) = 1029π cm³.\n"
        "Bullet = π(2.1)²(3.5 − 2.1) + (2/3)π(2.1)³ = 6.174π + 6.174π = 12.348π.\n"
        "1029/12.348 = 83.3, so only 83 complete bullets are possible.\n"
        "Answer: 83",
    ),
    (
        "A solid top is in the form of a cone surmounted by a hemisphere. If the volume of the solid is 2816 cubic cm and the radius of the hemispherical part is 8 cm, then the height of the top is: (Take π = 22/7)",
        ["26 cm", "50 cm", "34 cm", "42 cm"],
        "34 cm",
        "(1/3)π(64)h + (2/3)π(512) = 2816 gives (22/21)(64h + 1024) = 2816.\n"
        "64h + 1024 = 2688, so the cone's height is h = 26 cm.\n"
        "Total height = 26 + 8 = 34 cm",
    ),
    (
        "A medicine capsule is shaped like a cylinder with two hemispheres attached to each of its ends. The length of the entire capsule is 15 mm, and its diameter is 6 mm. Calculate the surface area (in sq mm) of the capsule. (Take π = 22/7)",
        ["286", "283", "280", "289"],
        "283",
        "r = 3 mm, so the cylindrical part is 15 − 6 = 9 mm long.\n"
        "Surface area = 2πrh + 4πr² = 54π + 36π = 90π = 282.86 sq mm.\n"
        "To the nearest whole number this is 283",
    ),
    (
        "The inside of a bowl is part of a sphere. When water is put into the bowl to a depth d, the water surface becomes a circle of radius 2d. What is the radius of the sphere?",
        ["2.5d", "2.75d", "3d", "3.25 d"],
        "2.5d",
        "From the centre, R² = (2d)² + (R − d)².\n"
        "R² = 4d² + R² − 2Rd + d² gives 2Rd = 5d², so R = 2.5d",
    ),
]

if __name__ == "__main__":
    import_sheet(START_INDEX, QUESTIONS, "Sheet-4")
