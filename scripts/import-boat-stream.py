"""Import the 54 Boat and Stream questions from datas/maths/Boat-and-Stream-Sheet.pdf
into data/maths/time-speed-distance.json, filling the placeholder slots that start at
maths_time_speed_distance_223. No other entry in the bank is touched.

The sheet highlights its own answers; every one was re-derived here. Two of the
sheet's highlights are arithmetically wrong and the correct option is used instead:
  Q23 - sheet highlights 10.4 h, but upstream speed is 8 km/h so 41.6/8 = 5.2 h.
  Q38 - sheet highlights 2 km/h, but 28/4 + 40/10 = 11 and 16/4 + 30/10 = 7 give
        upstream 4, downstream 10, hence a stream speed of 3 km/h.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "data" / "maths" / "time-speed-distance.json"
START_INDEX = 222  # maths_time_speed_distance_223

# (question, [options], correct answer, solution)
QUESTIONS = [
    (
        "The effective speed of a boat is 15.2 km/h against the stream and 20.8 km/h along the stream. Find the speed of the stream.",
        ["18 km/h", "1.8 km/h", "2.8 km/h", "3 km/h"],
        "2.8 km/h",
        "Speed of stream = (downstream − upstream)/2.\n"
        "= (20.8 − 15.2)/2 = 5.6/2 = 2.8 km/h.\n"
        "Answer: 2.8 km/h",
    ),
    (
        "A boat covers a certain distance downstream with speed 33 km/hr and upstream at 14 km/hr. Then find the speed of the boat in still water and also find the speed of the current.",
        [
            "9.5 km/hr and 23.5 km/hr",
            "23.5 km/hr and 9.5 km/hr",
            "28.5 km/hr and 4.5 km/hr",
            "4.5 km/hr and 28.5 km/hr",
        ],
        "23.5 km/hr and 9.5 km/hr",
        "Boat in still water = (33 + 14)/2 = 23.5 km/hr.\n"
        "Speed of current = (33 − 14)/2 = 9.5 km/hr.\n"
        "Answer: 23.5 km/hr and 9.5 km/hr",
    ),
    (
        "Rahul covers 734 km in a boat in 30 hours against the stream and he takes 12 hours with the stream. Then find the speed of the stream.",
        ["18.35 km/h", "11.88 km/h", "19.07 km/h", "28.44 km/h"],
        "18.35 km/h",
        "Upstream speed = 734/30 = 24.4667 km/h.\n"
        "Downstream speed = 734/12 = 61.1667 km/h.\n"
        "Stream = (61.1667 − 24.4667)/2 = 36.7/2 = 18.35 km/h.\n"
        "Answer: 18.35 km/h",
    ),
    (
        "A man rows 25.8 km upstream in 8.6 hours and a distance of 20 km downstream in 4 hours. Then the speed of the man in still water is:",
        ["2 km/h", "4 km/h", "6 km/h", "5 km/h"],
        "4 km/h",
        "Upstream speed = 25.8/8.6 = 3 km/h.\n"
        "Downstream speed = 20/4 = 5 km/h.\n"
        "Still water = (5 + 3)/2 = 4 km/h.\n"
        "Answer: 4 km/h",
    ),
    (
        "A person rows a boat 11 km in 5 hours downstream and returns upstream in 7 hours. What is the speed of the stream in km/h?",
        ["11/35 km/h", "11/27 km/h", "11/38 km/h", "11/28 km/h"],
        "11/35 km/h",
        "Downstream speed = 11/5 km/h and upstream speed = 11/7 km/h.\n"
        "Stream = (11/5 − 11/7)/2 = ((77 − 55)/35)/2 = (22/35)/2 = 11/35 km/h.\n"
        "Answer: 11/35 km/h",
    ),
    (
        "A man wishes to cover 1 km distance in river water. In still water he takes 12 minutes to cover it, but in the flowing river he takes 13 minutes. The speed of the flowing water of the river is:",
        ["25 km/h", "5/13 km/h", "22 km/h", "7/12 km/h"],
        "5/13 km/h",
        "Still water speed = 1 km in 12 min = 60/12 = 5 km/h.\n"
        "Against the flow = 1 km in 13 min = 60/13 km/h.\n"
        "Stream = 5 − 60/13 = (65 − 60)/13 = 5/13 km/h.\n"
        "Answer: 5/13 km/h",
    ),
    (
        "A man's speed in still water is 4 km/h more than the speed of the current. If the man takes a total of 10 h to cover 45 km downstream and 35 km upstream, then the speed of the man in still water is:",
        ["20 km/h", "18 km/h", "15 km/h", "22 km/h"],
        "20 km/h",
        "Let the current be c, so the boat in still water is c + 4.\n"
        "Downstream = 2c + 4 and upstream = (c + 4) − c = 4 km/h.\n"
        "45/(2c + 4) + 35/4 = 10 ⇒ 45/(2c + 4) = 10 − 8.75 = 1.25 ⇒ 2c + 4 = 36 ⇒ c = 16.\n"
        "Still water speed = 16 + 4 = 20 km/h.\n"
        "Answer: 20 km/h",
    ),
    (
        "The speed of a boat in still water is 15 km/h and the speed of the current is 9 km/h. The distance travelled by the boat downstream in 25 minutes is:",
        ["8 km", "10 km", "12 km", "9 km"],
        "10 km",
        "Downstream speed = 15 + 9 = 24 km/h.\n"
        "Distance in 25 min = 24 × 25/60 = 10 km.\n"
        "Answer: 10 km",
    ),
    (
        "A person rows a distance of 3 3/4 km upstream in 1 1/2 hours and a distance of 13 km downstream in 2 hours. How much time (in hours) will the person take to row a distance of 90 km in still water?",
        ["15", "20", "18", "24"],
        "20",
        "Upstream speed = 3.75/1.5 = 2.5 km/h.\n"
        "Downstream speed = 13/2 = 6.5 km/h.\n"
        "Still water = (6.5 + 2.5)/2 = 4.5 km/h.\n"
        "Time for 90 km = 90/4.5 = 20 hours.\n"
        "Answer: 20",
    ),
    (
        "A person can row a boat at 10 km/h in still water. If the speed of the stream is 7 km/h, what is the time taken to row a distance of 85 km down the stream?",
        ["5 hours", "4 hours", "6 hours", "3 hours"],
        "5 hours",
        "Downstream speed = 10 + 7 = 17 km/h.\n"
        "Time = 85/17 = 5 hours.\n"
        "Answer: 5 hours",
    ),
    (
        "A boat can travel at a speed of 15.5 km/h in still water. If speed of the stream is 4.5 km/h, then how much time will it take to go 76 km downstream and 104.5 km upstream?",
        [
            "15 hours 20 minutes",
            "13 hours 18 minutes",
            "12 hours 30 minutes",
            "18 hours 13 minutes",
        ],
        "13 hours 18 minutes",
        "Downstream = 15.5 + 4.5 = 20 km/h; upstream = 15.5 − 4.5 = 11 km/h.\n"
        "Time = 76/20 + 104.5/11 = 3.8 + 9.5 = 13.3 hours.\n"
        "0.3 hour = 18 minutes, so the total is 13 hours 18 minutes.\n"
        "Answer: 13 hours 18 minutes",
    ),
    (
        "A boat can travel 16.9 km downstream in 52 min. If the speed of the current is 3 km/h, then how much time (in hours) will the boat take to travel 84 km upstream?",
        ["6", "13.5", "6.22", "7.5"],
        "6.22",
        "Downstream speed = 16.9 × 60/52 = 19.5 km/h.\n"
        "Boat in still water = 19.5 − 3 = 16.5 km/h, so upstream = 16.5 − 3 = 13.5 km/h.\n"
        "Time = 84/13.5 = 6.22 hours.\n"
        "Answer: 6.22",
    ),
    (
        "Two boats A and B start moving towards each other from two places, 272 km apart. The speed of the boat A and B in still water are 32 km/h and 36 km/h, respectively. If A moves downstream and B moves upstream, then in how much time will they meet each other?",
        ["4 hours", "3 hours", "5 hours", "6 hours"],
        "4 hours",
        "Let the stream be s. A moves downstream at 32 + s and B upstream at 36 − s.\n"
        "Relative speed = (32 + s) + (36 − s) = 68 km/h, so the stream cancels out.\n"
        "Time = 272/68 = 4 hours.\n"
        "Answer: 4 hours",
    ),
    (
        "The ratio of the speed of a boat to that of the current water is 35 : 8. The boat goes along with the current in 5 hours 10 minutes. What will be the time taken by the boat to come back?",
        [
            "5 hours 15 minutes 58 seconds",
            "6 hours 45 minutes 10 seconds",
            "8 hours 13 minutes 48 seconds",
            "9 hours 30 minutes 49 seconds",
        ],
        "8 hours 13 minutes 48 seconds",
        "Downstream : upstream speed = (35 + 8) : (35 − 8) = 43 : 27.\n"
        "Time is inversely proportional to speed, so upstream time = 310 min × 43/27 ≈ 493.7 min.\n"
        "493.7 min ≈ 8 hours 13.7 minutes, matching the option 8 hours 13 minutes 48 seconds.\n"
        "Answer: 8 hours 13 minutes 48 seconds",
    ),
    (
        "The speed of a boat in still water is 25 km/hr and the speed of the current is 7 km/hr. If a boat goes from place A to place B and returns from B to A and it takes 6 hours 40 minutes in total, find the time taken by the boat to cover twice the distance of AB downstream.",
        [
            "3 hours 36 minutes",
            "4 hours 16 minutes",
            "5 hours 12 minutes",
            "4 hours 48 minutes",
        ],
        "4 hours 48 minutes",
        "Downstream = 32 km/h and upstream = 18 km/h.\n"
        "d/32 + d/18 = 20/3 ⇒ d × 25/288 = 20/3 ⇒ d = 76.8 km.\n"
        "Twice AB downstream = 153.6/32 = 4.8 hours = 4 hours 48 minutes.\n"
        "Answer: 4 hours 48 minutes",
    ),
    (
        "A boat covers a distance of 375 metres upstream in 30 min, and returns back to the starting point in 18 min. Find the ratio of the speed of the boat in still water and the speed of the stream.",
        ["5 : 6", "7 : 13", "13 : 7", "4 : 1"],
        "4 : 1",
        "For the same distance, speed is inversely proportional to time.\n"
        "Upstream : downstream = 18 : 30 = 3 : 5, so take upstream = 3k and downstream = 5k.\n"
        "Boat = (5k + 3k)/2 = 4k and stream = (5k − 3k)/2 = k.\n"
        "Ratio = 4 : 1.\n"
        "Answer: 4 : 1",
    ),
    (
        "A boat running upstream takes 8 hours and 48 mins to cover a certain distance, while it takes 4 hours to cover the same distance running downstream. The speed of the current is how much percentage less than the speed of the boat in still water?",
        ["62.5%", "60%", "66.66%", "58.33%"],
        "62.5%",
        "Upstream : downstream time = 8.8 : 4, so speeds are in the ratio 4 : 8.8 = 5 : 11.\n"
        "Boat = (11 + 5)/2 = 8 units and current = (11 − 5)/2 = 3 units.\n"
        "Required % = (8 − 3)/8 × 100 = 62.5%.\n"
        "Answer: 62.5%",
    ),
    (
        "A boat takes one fourth time in moving a certain distance downstream than upstream. The speed of the boat in still water is how much percentage more than the speed of current?",
        ["40%", "66.66%", "60%", "75%"],
        "66.66%",
        "Downstream time = (1/4) × upstream time, so downstream speed = 4 × upstream speed.\n"
        "Take upstream = 1 and downstream = 4: boat = 2.5 and current = 1.5.\n"
        "Required % = (2.5 − 1.5)/1.5 × 100 = 66.66%.\n"
        "Answer: 66.66%",
    ),
    (
        "The speed of a boat in still water is 5 1/3 km/h. It is found that the boat takes thrice as much time to row up than it does to row down the same distance in the river stream. Find the speed of the river stream.",
        ["23/27 m/sec", "22/27 m/sec", "20/27 m/sec", "19/27 m/sec"],
        "20/27 m/sec",
        "Upstream time = 3 × downstream time ⇒ downstream speed = 3 × upstream speed.\n"
        "Let upstream = u, downstream = 3u. Boat = (3u + u)/2 = 2u = 16/3 ⇒ u = 8/3.\n"
        "Stream = (3u − u)/2 = u = 8/3 km/h.\n"
        "In m/sec: (8/3) × (5/18) = 40/54 = 20/27 m/sec.\n"
        "Answer: 20/27 m/sec",
    ),
    (
        "A boat starting from point P goes downstream to point Q in 3 hours and returns back from point Q to point P in 4 hours. If the speed of the water is 3 km/h, find the speed (km/h) of the boat in still water.",
        ["12", "20", "21", "32"],
        "21",
        "Distance is the same both ways: 3(b + 3) = 4(b − 3).\n"
        "3b + 9 = 4b − 12 ⇒ b = 21 km/h.\n"
        "Answer: 21",
    ),
    (
        "A boat takes 60% more time to cover a certain distance upstream than downstream. If speed of current is 9 km/hr, then in how much time will it cover 504 km downstream?",
        ["10 hr", "10.5 hr", "12 hr", "12.5 hr"],
        "10.5 hr",
        "Upstream : downstream time = 160 : 100 = 8 : 5, so speeds are in the ratio 5 : 8.\n"
        "Upstream = 5k, downstream = 8k ⇒ current = (8k − 5k)/2 = 1.5k = 9 ⇒ k = 6.\n"
        "Downstream speed = 48 km/h, so time = 504/48 = 10.5 hr.\n"
        "Answer: 10.5 hr",
    ),
    (
        "The time taken by a boat to go a certain distance downstream is two-third of the time taken by the boat to go the same distance upstream. If two times the speed of the boat in still water is 10 km/h more than 7 times the speed of the stream, then what is the speed (in km/h) of the stream?",
        ["3 1/3", "2 1/2", "4", "2"],
        "3 1/3",
        "Downstream time = (2/3) upstream time ⇒ speeds are in the ratio 3 : 2.\n"
        "Let upstream = 2k and downstream = 3k: boat = 2.5k, stream = 0.5k.\n"
        "2(2.5k) = 7(0.5k) + 10 ⇒ 5k = 3.5k + 10 ⇒ k = 20/3.\n"
        "Stream = 0.5 × 20/3 = 10/3 = 3 1/3 km/h.\n"
        "Answer: 3 1/3",
    ),
    (
        "A boat can cover a distance of 56 km downstream in 3.5 hours. The ratio of the speed of the boat in still water and the speed of stream is 3 : 1. How much time (in hours) will the boat take to cover a distance of 41.6 km upstream?",
        ["9.1", "10.5", "10.4", "5.2"],
        "5.2",
        "Downstream speed = 56/3.5 = 16 km/h.\n"
        "Boat : stream = 3 : 1, so downstream = 3x + x = 4x = 16 ⇒ x = 4.\n"
        "Boat = 12 km/h and stream = 4 km/h, so upstream = 12 − 4 = 8 km/h.\n"
        "Time = 41.6/8 = 5.2 hours.\n"
        "Answer: 5.2",
    ),
    (
        "A man can row a boat at a speed of 10 km/h in still water. If the river is flowing at 4.5 km/h, it takes 2 hours to go to a point and come back to the starting point. At what distance (in km) is the place located (rounded off to two decimal places)?",
        ["6.25", "5.50", "7.98", "8.98"],
        "7.98",
        "Downstream = 14.5 km/h and upstream = 5.5 km/h.\n"
        "d/14.5 + d/5.5 = 2 ⇒ d(0.068966 + 0.181818) = 2 ⇒ d × 0.250784 = 2.\n"
        "d = 7.975 ≈ 7.98 km.\n"
        "Answer: 7.98",
    ),
    (
        "A boat's speed in still water is 22 km/h, while the river is flowing with a speed of 8 km/h and the time taken to cover a certain distance upstream is 4 hours more than the time taken to cover the same distance downstream. Find the distance.",
        ["105 km", "110 km", "115 km", "125 km"],
        "105 km",
        "Downstream = 30 km/h and upstream = 14 km/h.\n"
        "d/14 − d/30 = 4 ⇒ d(30 − 14)/420 = 4 ⇒ 16d = 1680 ⇒ d = 105 km.\n"
        "Answer: 105 km",
    ),
    (
        "The speed of a boat in still water is 15 km/h. If it can travel 42 km downstream and 28 km upstream in the same time, then what is the speed of the stream?",
        ["2.5 km/h", "3 km/h", "4.5 km/h", "6 km/h"],
        "3 km/h",
        "42/(15 + s) = 28/(15 − s).\n"
        "630 − 42s = 420 + 28s ⇒ 210 = 70s ⇒ s = 3 km/h.\n"
        "Answer: 3 km/h",
    ),
    (
        "The time taken by a boat to travel 13 km downstream is the same as time taken by it to travel 7 km upstream. If the speed of the stream is 3 km/h, then how much time will it take to travel a distance of 44.8 km in still water?",
        ["4 12/25", "5 3/5", "5 2/5", "4 13/25"],
        "4 12/25",
        "13/(b + 3) = 7/(b − 3) ⇒ 13b − 39 = 7b + 21 ⇒ 6b = 60 ⇒ b = 10 km/h.\n"
        "Time = 44.8/10 = 4.48 hours = 4 12/25 hours.\n"
        "Answer: 4 12/25",
    ),
    (
        "A man rows to a place at a distance of 72 km and comes back in 36 hours. He finds that he can row 12 km with the stream in the same time as 4 km against the stream. The speed (in km/h) of the stream is:",
        ["3.75", "2.45", "2.67", "2.33"],
        "2.67",
        "12/(b + s) = 4/(b − s) ⇒ 12b − 12s = 4b + 4s ⇒ 8b = 16s ⇒ b = 2s.\n"
        "So downstream = 3s and upstream = s.\n"
        "72/3s + 72/s = 36 ⇒ 24/s + 72/s = 36 ⇒ 96/s = 36 ⇒ s = 2.67 km/h.\n"
        "Answer: 2.67",
    ),
    (
        "A man rows 48 km and back in 48 hours. He can row 4 km with the stream in the same time as 3 km against the stream. The speed of the stream (in km/h) is:",
        ["5/21", "7/21", "7/24", "3/29"],
        "7/24",
        "4/(b + s) = 3/(b − s) ⇒ 4b − 4s = 3b + 3s ⇒ b = 7s.\n"
        "Downstream = 8s and upstream = 6s.\n"
        "48/8s + 48/6s = 48 ⇒ 6/s + 8/s = 48 ⇒ 14/s = 48 ⇒ s = 7/24 km/h.\n"
        "Answer: 7/24",
    ),
    (
        "The speed of a boat downstream is 150% more than its speed upstream. If the time taken by the boat for going 80 km downstream and 50 km upstream is 8.2 hours, then what is the speed (in km/h) of the boat downstream?",
        ["16", "30", "24", "25"],
        "25",
        "Downstream = 2.5 × upstream, so take upstream = 2k and downstream = 5k.\n"
        "80/5k + 50/2k = 8.2 ⇒ 16/k + 25/k = 8.2 ⇒ 41/k = 8.2 ⇒ k = 5.\n"
        "Downstream speed = 5 × 5 = 25 km/h.\n"
        "Answer: 25",
    ),
    (
        "A boat takes total 10 hr to cover 102 km downstream and 63 km upstream. The time spent to cover 34 km downstream is equal to the time taken to cover 24 km in still water. The speed of the boat upstream is how much greater than the speed of current?",
        ["4 km/hr", "3 km/hr", "4.5 km/hr", "5 km/hr"],
        "3 km/hr",
        "34/(b + s) = 24/b ⇒ 34b = 24b + 24s ⇒ 10b = 24s ⇒ b = 2.4s.\n"
        "So downstream = 3.4s and upstream = 1.4s.\n"
        "102/3.4s + 63/1.4s = 10 ⇒ 30/s + 45/s = 10 ⇒ 75/s = 10 ⇒ s = 7.5 km/h.\n"
        "Upstream = 1.4 × 7.5 = 10.5, so the difference = 10.5 − 7.5 = 3 km/hr.\n"
        "Answer: 3 km/hr",
    ),
    (
        "The speed of a boat downstream is 2.5 times the speed of the boat upstream. If the time taken by the boat for going 30 km downstream and the same distance upstream is 7 hours, then what is the speed (in km/h) of the boat downstream?",
        ["12.5", "9", "15", "7.5"],
        "15",
        "Take upstream = 2k and downstream = 5k.\n"
        "30/5k + 30/2k = 7 ⇒ 6/k + 15/k = 7 ⇒ 21/k = 7 ⇒ k = 3.\n"
        "Downstream speed = 5 × 3 = 15 km/h.\n"
        "Answer: 15",
    ),
    (
        "A boat goes 112 km downstream and comes back to the starting point in 11.5 hours. If the speed of the current is 9 km/hr, then the speed (in km/hr) of the boat in still water is:",
        ["17 km/h", "19 km/h", "29 km/h", "23 km/h"],
        "23 km/h",
        "112/(b + 9) + 112/(b − 9) = 11.5.\n"
        "224b = 11.5(b² − 81) ⇒ 23b² − 448b − 1863 = 0.\n"
        "Discriminant = 448² + 4 × 23 × 1863 = 372100, √372100 = 610.\n"
        "b = (448 + 610)/46 = 23 km/h.\n"
        "Answer: 23 km/h",
    ),
    (
        "The speed of a stream is 6 km/h. A boat can go 56 km downstream and 39 km upstream in 7 hours. What is the speed (in km/h) of the boat in still water?",
        ["22", "15", "7", "13"],
        "15",
        "56/(b + 6) + 39/(b − 6) = 7.\n"
        "Testing b = 15: 56/21 + 39/9 = 2.667 + 4.333 = 7. ✓\n"
        "Answer: 15",
    ),
    (
        "In a stream running at 3 km/h, a motorboat goes 12 km upstream and back to the starting point in 60 min. Find the speed of the motorboat in still water.",
        ["2(2+√17)", "2(4+√15)", "3(4+√17)", "3(2+√17)"],
        "3(4+√17)",
        "12/(b − 3) + 12/(b + 3) = 1 ⇒ 24b = b² − 9 ⇒ b² − 24b − 9 = 0.\n"
        "b = (24 + √(576 + 36))/2 = (24 + √612)/2 = 12 + 3√17 = 3(4 + √17).\n"
        "Check: (12 + 3√17)² − 24(12 + 3√17) − 9 = 297 + 72√17 − 288 − 72√17 − 9 = 0. ✓\n"
        "Answer: 3(4+√17)",
    ),
    (
        "The speed of a motorboat in still water is 20 km/h. It travels 150 km downstream and then returns to the starting point. If the round trip takes a total of 16 hours, what is the speed (in km/h) of the flow of river?",
        ["6", "4", "8", "5"],
        "5",
        "150/(20 + s) + 150/(20 − s) = 16.\n"
        "150 × 40 = 16(400 − s²) ⇒ 6000 = 6400 − 16s² ⇒ 16s² = 400 ⇒ s = 5 km/h.\n"
        "Answer: 5",
    ),
    (
        "A motorboat's speed is 16 km/h in still water. It takes 72 minutes more to go 36 km upstream than to return downstream to the same spot. The speed (in km/h) of the stream is:",
        ["8", "10", "4", "5"],
        "4",
        "36/(16 − s) − 36/(16 + s) = 72/60 = 1.2 hours.\n"
        "36(2s) = 1.2(256 − s²) ⇒ 1.2s² + 72s − 307.2 = 0 ⇒ s² + 60s − 256 = 0.\n"
        "s = (−60 + √4624)/2 = (−60 + 68)/2 = 4 km/h.\n"
        "Answer: 4",
    ),
    (
        "A motorboat travelling at some speed can cover 28 km upstream and 40 km downstream in 11 hours. At the same speed it can travel 30 km downstream and 16 km upstream in 7 hours, then the speed of the stream is:",
        ["2 km/h", "4 km/h", "3 km/h", "1 km/h"],
        "3 km/h",
        "Let u = 1/(upstream speed) and d = 1/(downstream speed).\n"
        "28u + 40d = 11 and 16u + 30d = 7.\n"
        "Multiplying by 3 and 4 and subtracting: 20u = 5 ⇒ u = 0.25 ⇒ upstream = 4 km/h.\n"
        "Then 40d = 11 − 7 = 4 ⇒ d = 0.1 ⇒ downstream = 10 km/h.\n"
        "Check: 16/4 + 30/10 = 4 + 3 = 7. ✓\n"
        "Stream = (10 − 4)/2 = 3 km/h.\n"
        "Answer: 3 km/h",
    ),
    (
        "A man covers 39 km upstream and 116 km downstream in 7 hrs. He also covers 65 km upstream and 87 km downstream in 8 hrs. Find the speed of boat in still water.",
        ["21 km/hr", "27 km/hr", "18 km/hr", "29 km/hr"],
        "21 km/hr",
        "Let u = 1/(upstream speed) and d = 1/(downstream speed).\n"
        "39u + 116d = 7 and 65u + 87d = 8.\n"
        "Multiplying by 5 and 3 and subtracting: 319d = 11 ⇒ d = 1/29 ⇒ downstream = 29 km/h.\n"
        "39u = 7 − 116/29 = 3 ⇒ u = 1/13 ⇒ upstream = 13 km/h.\n"
        "Still water = (29 + 13)/2 = 21 km/hr.\n"
        "Answer: 21 km/hr",
    ),
    (
        "A boat can go 40 km downstream and 25 km upstream in 7 hours 30 minutes. It can go 48 km downstream and 36 km upstream in 10 hours. What is the speed (in km/h) of the boat in still water?",
        ["6", "12", "9", "15"],
        "9",
        "Let d = 1/(downstream speed) and u = 1/(upstream speed).\n"
        "40d + 25u = 7.5 and 48d + 36u = 10.\n"
        "Multiplying by 6 and 5 and subtracting: 30u = 5 ⇒ u = 1/6 ⇒ upstream = 6 km/h.\n"
        "40d = 7.5 − 25/6 = 10/3 ⇒ d = 1/12 ⇒ downstream = 12 km/h.\n"
        "Still water = (12 + 6)/2 = 9 km/h.\n"
        "Answer: 9",
    ),
    (
        "A boat can go 30 km downstream and 24 km upstream in 2 hours 27 minutes. Also, it can go 10 km downstream and 4 km upstream in 37 minutes. What is the speed of the boat upstream (in km/hr)?",
        ["20", "24", "22", "18"],
        "20",
        "Let d = 1/(downstream speed) and u = 1/(upstream speed).\n"
        "30d + 24u = 2.45 hours and 10d + 4u = 37/60 hour.\n"
        "Multiplying the second by 3: 30d + 12u = 1.85.\n"
        "Subtracting: 12u = 0.6 ⇒ u = 0.05 ⇒ upstream speed = 20 km/hr.\n"
        "Answer: 20",
    ),
    (
        "A boat can go 3 km upstream and 5 km downstream in 55 minutes. It can also go 4 km upstream and 9 km downstream in 1 hour 25 minutes. In how much time (in hours) will it go 43.2 km downstream?",
        ["4.8", "5.4", "3.6", "4.4"],
        "3.6",
        "Let u = 1/(upstream speed) and d = 1/(downstream speed).\n"
        "3u + 5d = 11/12 and 4u + 9d = 17/12.\n"
        "Multiplying by 4 and 3 and subtracting: 7d = 17/4 − 11/3 = 7/12 ⇒ d = 1/12 ⇒ downstream = 12 km/h.\n"
        "Time = 43.2/12 = 3.6 hours.\n"
        "Answer: 3.6",
    ),
    (
        "A motorboat can go 8.4 km downstream and 4.8 km upstream in 1 hour. It can go 17.5 km downstream and 9 km upstream in 2 hours. How much time (in hours) will it take to go 31.2 km in still water?",
        ["2.4", "1.3", "3.9", "1.2"],
        "2.4",
        "Let d = 1/(downstream speed) and u = 1/(upstream speed).\n"
        "8.4d + 4.8u = 1 and 17.5d + 9u = 2.\n"
        "Solving: d = 1/14 ⇒ downstream = 14 km/h, and u = 1/12 ⇒ upstream = 12 km/h.\n"
        "Still water = (14 + 12)/2 = 13 km/h, so time = 31.2/13 = 2.4 hours.\n"
        "Answer: 2.4",
    ),
    (
        "A boat covers 24 km upstream and 36 km downstream in 10 hours, and 36 km upstream and 24 km downstream in 12 hours. The speed of the current is:",
        ["26/9 km/h", "33/13 km/h", "25/8 km/h", "24/7 km/h"],
        "25/8 km/h",
        "Let u = 1/(upstream speed) and d = 1/(downstream speed).\n"
        "24u + 36d = 10 and 36u + 24d = 12.\n"
        "Adding: 60u + 60d = 22 ⇒ u + d = 11/30. Subtracting: u − d = 1/6.\n"
        "u = 4/15 ⇒ upstream = 3.75 km/h; d = 1/10 ⇒ downstream = 10 km/h.\n"
        "Current = (10 − 3.75)/2 = 3.125 = 25/8 km/h.\n"
        "Answer: 25/8 km/h",
    ),
    (
        "A boat can go 3.6 km upstream and 5.4 km downstream in 54 minutes, while it can go 5.4 km upstream and 3.6 km downstream in 58.5 minutes. The time taken by the boat in going 10 km downstream is:",
        ["48 minutes", "50 minutes", "45 minutes", "54 minutes"],
        "50 minutes",
        "Let u = 1/(upstream speed) and d = 1/(downstream speed), with times in hours.\n"
        "3.6u + 5.4d = 0.9 and 5.4u + 3.6d = 0.975.\n"
        "Adding: u + d = 0.208333. Subtracting: u − d = 0.0416667.\n"
        "u = 0.125 ⇒ upstream = 8 km/h; d = 0.083333 ⇒ downstream = 12 km/h.\n"
        "Time for 10 km downstream = 10/12 hour = 50 minutes.\n"
        "Answer: 50 minutes",
    ),
    (
        "On a river, Q is the mid-point between two points P and R on the same bank of the river. A boat can go from P to Q and back in 12 hours, and from P to R in 16 hours 40 min. How long would it take to go from R to P?",
        ["3 3/7 h", "5 h", "6 2/3 h", "7 1/3 h"],
        "7 1/3 h",
        "P to R takes 50/3 hours; since it is slower it must be the upstream direction.\n"
        "PQ is half of PR, so P to Q upstream = (50/3)/2 = 25/3 hours.\n"
        "Q to P downstream = 12 − 25/3 = 11/3 hours.\n"
        "R to P is downstream over twice that distance = 2 × 11/3 = 22/3 = 7 1/3 hours.\n"
        "Answer: 7 1/3 h",
    ),
    (
        "X, Y are two points in a river. Points P and Q divide the straight line XY into three equal parts. The river flows along XY and the time taken by a boat to row from X to Q and from Y to Q are in the ratio 4 : 5. The ratio of the speed of the boat downstream to that of the river current is equal to:",
        ["3 : 10", "3 : 4", "10 : 3", "4 : 3"],
        "10 : 3",
        "Taking each part as 1 unit, XQ = 2 units (downstream) and YQ = 1 unit (upstream).\n"
        "(2/D) : (1/U) = 4 : 5 ⇒ 2U/D = 4/5 ⇒ U/D = 2/5, so take U = 2 and D = 5.\n"
        "Current = (5 − 2)/2 = 1.5 units.\n"
        "Downstream : current = 5 : 1.5 = 10 : 3.\n"
        "Answer: 10 : 3",
    ),
    (
        "A boat takes 20 hours for travelling downstream from point A to point B and comes back to a midpoint C between A and B. The speed of the stream is 5 km/h and the speed of the boat in still water is 10 km/h. Find the distance between A and B (in km).",
        ["100", "120", "150", "75"],
        "120",
        "Downstream = 15 km/h and upstream = 5 km/h.\n"
        "d/15 + (d/2)/5 = 20 ⇒ d/15 + d/10 = 20.\n"
        "d(2 + 3)/30 = 20 ⇒ d = 120 km.\n"
        "Answer: 120",
    ),
    (
        "A man travels by a motor boat down a river to his office and back. With the speed of the river unchanged, if he doubles the speed of his motor boat, then his travel time gets reduced by 75%. The ratio of the original speed of the motor boat to the speed of the river is:",
        ["√6 : √2", "√7 : 2", "2√5 : 3", "3 : 2"],
        "√7 : 2",
        "Round trip time T = 2bd/(b² − r²); after doubling, T' = 4bd/(4b² − r²).\n"
        "T' = 0.25T ⇒ 4/(4b² − r²) = 0.5/(b² − r²) ⇒ 4b² − 4r² = 2b² − 0.5r².\n"
        "2b² = 3.5r² ⇒ b²/r² = 7/4 ⇒ b : r = √7 : 2.\n"
        "Answer: √7 : 2",
    ),
    (
        "A boat covers a round trip journey between two points A and B in a river in T hours. If its speed in still water becomes 2 times, it would take (80/161)T hours for the same journey. Find the ratio of its speed in still water to the speed of the river.",
        ["11 : 1", "161 : 40", "1 : 11", "2 : 1"],
        "11 : 1",
        "T = 2bd/(b² − r²) and the new time = 4bd/(4b² − r²) = (80/161)T.\n"
        "4/(4b² − r²) = (160/161)/(b² − r²) ⇒ 644(b² − r²) = 160(4b² − r²).\n"
        "644b² − 644r² = 640b² − 160r² ⇒ 4b² = 484r² ⇒ b/r = 11.\n"
        "Answer: 11 : 1",
    ),
    (
        "A man swims from A to B and back in 4 1/2 hours. A block of wood when allowed to go with the stream from A to B takes 6 hours. What is the ratio of the speed of the man in still water to that of the stream?",
        ["2:1", "4:3", "3:1", "4:1"],
        "3:1",
        "A block of wood drifts at the speed of the stream, so d/r = 6 ⇒ d = 6r.\n"
        "2bd/(b² − r²) = 4.5 ⇒ 12br = 4.5(b² − r²).\n"
        "Dividing by r² with k = b/r: 4.5k² − 12k − 4.5 = 0 ⇒ 3k² − 8k − 3 = 0 ⇒ (3k + 1)(k − 3) = 0.\n"
        "k = 3, so man : stream = 3 : 1.\n"
        "Answer: 3:1",
    ),
    (
        "A swimmer swims from a point P against the current for 6 min and then swims back along the current for next 6 min and reaches a point Q. If the distance between P and Q is 120 m then the speed of the current (in km/h) is:",
        ["0.4", "0.2", "1", "0.6"],
        "0.6",
        "Net displacement = 6(b + r) − 6(b − r) = 12r, where speeds are per minute.\n"
        "12r = 120 m ⇒ r = 10 m/min.\n"
        "In km/h: 10 × 60/1000 = 0.6 km/h.\n"
        "Answer: 0.6",
    ),
    (
        "A ship is 77 km from the shore, springs a leak which admits 2 1/4 ton of water in every 5 1/2 min. An outlet tank can throw out 12 tons of water per hour. Find at what speed it should move such that when it begins to sink a rescue ship moving with 6 km/hr escapes the passengers of the ship, if 69 ton of water is enough to sink it.",
        ["6 km/hr", "8 km/hr", "10 km/hr", "12 km/hr"],
        "8 km/hr",
        "Leak rate = (9/4) ÷ (11/2) = 9/22 ton/min = 270/11 ton/hour.\n"
        "Net inflow = 270/11 − 12 = 138/11 ton/hour.\n"
        "Time to take in 69 tons = 69 ÷ (138/11) = 5.5 hours.\n"
        "The two ships must close 77 km in 5.5 hours: v + 6 = 77/5.5 = 14 ⇒ v = 8 km/hr.\n"
        "Answer: 8 km/hr",
    ),
    (
        "A man rows a boat a certain distance downstream in 9 hours, while it takes 18 hours to row the same distance upstream. How many hours will it take him to row three-fifth of the same distance in still water?",
        ["9.5", "7.2", "10", "12"],
        "7.2",
        "Downstream speed = d/9 and upstream speed = d/18.\n"
        "Still water speed = (d/9 + d/18)/2 = (3d/18)/2 = d/12.\n"
        "Time for (3/5)d = (3d/5) ÷ (d/12) = 36/5 = 7.2 hours.\n"
        "Answer: 7.2",
    ),
]


def main() -> None:
    bank = json.loads(BANK.read_text(encoding="utf-8"))

    end = START_INDEX + len(QUESTIONS)
    if end > len(bank):
        raise SystemExit(f"bank has only {len(bank)} entries, need {end}")

    for offset, entry in enumerate(bank[START_INDEX:end]):
        text = entry.get("question") or ""
        if "add real content" not in text and "[Add content]" not in text:
            raise SystemExit(f"index {START_INDEX + offset} ({entry['id']}) is not a placeholder")

    for offset, (question, options, answer, solution) in enumerate(QUESTIONS):
        if answer not in options:
            raise SystemExit(f"Q{offset + 1}: answer {answer!r} missing from options")
        if len(set(options)) != 4:
            raise SystemExit(f"Q{offset + 1}: options are not 4 distinct values")
        if not solution.rstrip().endswith(answer):
            raise SystemExit(f"Q{offset + 1}: solution does not end with the answer")

        index = START_INDEX + offset
        bank[index] = {
            "id": bank[index]["id"],
            "question": question,
            "options": options,
            "correctAnswer": answer,
            "solution": solution,
        }

    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {len(QUESTIONS)} questions: {bank[START_INDEX]['id']} .. {bank[end - 1]['id']}")


if __name__ == "__main__":
    main()
