"""Fill maths_compound_interest_159 onward from datas/maths/ci.pdf (37 questions).

Replaces only the placeholder entries at indices 158..194; every other entry
in data/maths/compound-interest.json is left untouched.

Run: python scripts/import-ci-pdf.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "maths" / "compound-interest.json"
START_INDEX = 158  # maths_compound_interest_159

Q: list[dict] = [
    {
        "question": "If the rate of interest is 20% per annum compounded yearly and the interest on a certain sum in the second year is Rs 250, then what will be the interest on the same sum in the 5th year?",
        "options": ["Rs 518", "Rs 360", "Rs 400", "Rs 432"],
        "correctAnswer": "Rs 432",
        "solution": "**Step 1:** Interest of the nth year $= P \\cdot r \\cdot (1+r)^{n-1}$, so successive yearly interests form a GP with ratio $(1+r)$.\n\n**Step 2:** From year 2 to year 5 there are 3 steps.\n$I_5 = I_2 \\times (1.2)^3 = 250 \\times 1.728$\n\n**Step 3:** $I_5 = 432$\n\n**Answer: Rs 432**",
    },
    {
        "question": "The compound interest of the 13th year is 1024. Find the compound interest of the 10th year if the rate of interest is 14(2/7)%.",
        "options": ["443", "512", "343", "686"],
        "correctAnswer": "686",
        "solution": "**Step 1:** $r = 14\\frac{2}{7}\\% = \\frac{100}{7}\\% = \\frac{1}{7}$, so $1 + r = \\frac{8}{7}$.\n\n**Step 2:** Yearly interests form a GP with ratio $\\frac{8}{7}$.\n$I_{13} = I_{10} \\times \\left(\\frac{8}{7}\\right)^3 = I_{10} \\times \\frac{512}{343}$\n\n**Step 3:** $I_{10} = 1024 \\times \\frac{343}{512} = 2 \\times 343 = 686$\n\n**Answer: 686**",
    },
    {
        "question": "If at the same rate of interest, in 2 years the simple interest is ₹42 and the compound interest is ₹51, then what is the principal (in ₹)?",
        "options": ["44", "49", "42", "53"],
        "correctAnswer": "49",
        "solution": "**Step 1:** SI for 2 years = 42, so SI per year = 21.\n\n**Step 2:** CI − SI = 51 − 42 = 9. This is the interest earned on the first year's interest.\n$21 \\times r = 9 \\Rightarrow r = \\frac{9}{21} = \\frac{3}{7}$\n\n**Step 3:** $P \\times r = 21 \\Rightarrow P = 21 \\times \\frac{7}{3} = 49$\n\n**Answer: 49**",
    },
    {
        "question": "On a certain sum, simple interest for 2 years is ₹9,600 whereas the compound interest compounded annually is ₹10,176. What is the rate of interest per annum?",
        "options": ["9%", "12%", "10%", "15%"],
        "correctAnswer": "12%",
        "solution": "**Step 1:** SI per year $= \\frac{9600}{2} = 4800$.\n\n**Step 2:** CI − SI for 2 years = 10176 − 9600 = 576, which is the interest on the first year's interest.\n$4800 \\times r = 576$\n\n**Step 3:** $r = \\frac{576}{4800} = 0.12 = 12\\%$\n\n**Answer: 12%**",
    },
    {
        "question": "What is the rate of interest (in %) if the simple interest earned on a certain sum for 5 years is Rs 45,000 and the compound interest earned for 2 years is Rs 18,630?",
        "options": ["5", "7", "8", "6"],
        "correctAnswer": "7",
        "solution": "**Step 1:** SI for 5 years = 45000, so $P \\cdot r = \\frac{45000}{5} = 9000$ per year.\n\n**Step 2:** CI for 2 years $= P(2r + r^2) = 2Pr + (Pr)r = 18000 + 9000r$.\n\n**Step 3:** $18000 + 9000r = 18630 \\Rightarrow 9000r = 630 \\Rightarrow r = 0.07$\n\n**Answer: 7**",
    },
    {
        "question": "The compound interest and the simple interest for two years on a certain sum of money at a certain rate of interest are Rs.2257.5 and Rs.2100 respectively. Find the principal and rate percent.",
        "options": ["6000, 7%", "7500, 8%", "14000, 10%", "7000, 15%"],
        "correctAnswer": "7000, 15%",
        "solution": "**Step 1:** SI per year $= \\frac{2100}{2} = 1050$.\n\n**Step 2:** CI − SI = 2257.5 − 2100 = 157.5, the interest on the first year's interest.\n$1050 \\times r = 157.5 \\Rightarrow r = 0.15 = 15\\%$\n\n**Step 3:** $P \\times 0.15 = 1050 \\Rightarrow P = 7000$\n\n**Answer: 7000, 15%**",
    },
    {
        "question": "If the interest earned during the 2nd year on a certain sum is ₹3726, and the rate of interest is 15% per annum compounded annually, then the sum is: (RRB JE 2024)",
        "options": ["₹21600", "₹20885", "₹21185", "₹20835"],
        "correctAnswer": "₹21600",
        "solution": "**Step 1:** Interest of the 2nd year $= P \\cdot r \\cdot (1+r)$.\n\n**Step 2:** $P \\times 0.15 \\times 1.15 = 3726$\n$0.1725P = 3726$\n\n**Step 3:** $P = \\frac{3726}{0.1725} = 21600$\n\n**Answer: ₹21600**",
    },
    {
        "question": "The compound interest on a certain principal at the rate of 12.5% per annum compounded annually is Rs.1215 in the third year. Then find the principal.",
        "options": ["Rs.7680", "Rs.8640", "Rs.6912", "Rs.9216"],
        "correctAnswer": "Rs.7680",
        "solution": "**Step 1:** $r = 12.5\\% = \\frac{1}{8}$, so $1 + r = \\frac{9}{8}$.\n\n**Step 2:** Interest of the 3rd year $= P \\cdot r \\cdot (1+r)^2 = P \\times \\frac{1}{8} \\times \\frac{81}{64} = \\frac{81P}{512}$.\n\n**Step 3:** $\\frac{81P}{512} = 1215 \\Rightarrow P = 1215 \\times \\frac{512}{81} = 15 \\times 512 = 7680$\n\n**Answer: Rs.7680**",
    },
    {
        "question": "A sum of Rs 20000 is invested for three years at compound interest. The rate of interest for the first year is 20 percent per annum, for the second year it is 15 percent per annum and for the third year it is 10 percent per annum. Find the interest for the third year.",
        "options": ["Rs 2190", "Rs 2620", "Rs 2760", "Rs 2340"],
        "correctAnswer": "Rs 2760",
        "solution": "**Step 1:** Amount after year 1 $= 20000 \\times 1.20 = 24000$.\n\n**Step 2:** Amount after year 2 $= 24000 \\times 1.15 = 27600$.\n\n**Step 3:** Interest for the 3rd year $= 27600 \\times 0.10 = 2760$\n\n**Answer: Rs 2760**",
    },
    {
        "question": "The compound interest on a certain sum of money for 1 year 146 days at 14.28% per annum is Rs.408. Then find the principal.",
        "options": ["Rs.1920", "Rs.2040", "Rs.1960", "Rs.1880"],
        "correctAnswer": "Rs.1960",
        "solution": "**Step 1:** $14.28\\% = \\frac{1}{7}$ and 146 days $= \\frac{146}{365} = \\frac{2}{5}$ year.\n\n**Step 2:** Growth factor $= \\left(\\frac{8}{7}\\right) \\times \\left(1 + \\frac{2}{5} \\cdot \\frac{1}{7}\\right) = \\frac{8}{7} \\times \\frac{37}{35} = \\frac{296}{245}$.\n\n**Step 3:** $CI = P\\left(\\frac{296}{245} - 1\\right) = \\frac{51P}{245} = 408$\n$P = 408 \\times \\frac{245}{51} = 8 \\times 245 = 1960$\n\n**Answer: Rs.1960**",
    },
    {
        "question": "The difference between C.I. and S.I. on a certain sum of money at 15% per annum for 2 years 219 days is Rs.2061. Then find the principal.",
        "options": ["Rs.40000", "Rs.48000", "Rs.36000", "Rs.32000"],
        "correctAnswer": "Rs.40000",
        "solution": "**Step 1:** 219 days $= \\frac{219}{365} = 0.6$ year, so total time = 2.6 years and the part-year rate is $0.6 \\times 15\\% = 9\\%$.\n\n**Step 2:** CI factor $= (1.15)^2 \\times 1.09 - 1 = 1.3225 \\times 1.09 - 1 = 0.441525$.\nSI factor $= 0.15 \\times 2.6 = 0.39$.\n\n**Step 3:** Difference factor $= 0.441525 - 0.39 = 0.051525$.\n$P = \\frac{2061}{0.051525} = 40000$\n\n**Answer: Rs.40000**",
    },
    {
        "question": "The simple interest on a certain sum at the end of three years at 5% p.a. is 1200 rupees. The compound interest on the same sum for the same period at the same rate is (interest compounded yearly):",
        "options": ["1273", "1261", "1272", "1260"],
        "correctAnswer": "1261",
        "solution": "**Step 1:** $P \\times 0.05 \\times 3 = 1200 \\Rightarrow P = 8000$.\n\n**Step 2:** $CI = 8000\\left[(1.05)^3 - 1\\right] = 8000\\,[1.157625 - 1]$.\n\n**Step 3:** $CI = 8000 \\times 0.157625 = 1261$\n\n**Answer: 1261**",
    },
    {
        "question": "The compound interest on a certain sum of money at 8% per annum for 3 years is ₹4,058. Find the simple interest on the same sum for 4 years at 10% p.a. (DP CONSTABLE 2023)",
        "options": ["Rs 6520", "Rs 6025", "Rs 6250", "Rs 6052"],
        "correctAnswer": "Rs 6250",
        "solution": "**Step 1:** $(1.08)^3 = 1.259712$, so the CI factor is $0.259712$.\n\n**Step 2:** $P = \\frac{4058}{0.259712} = 15625$.\n\n**Step 3:** $SI = 15625 \\times 0.10 \\times 4 = 6250$\n\n**Answer: Rs 6250**",
    },
    {
        "question": "When the difference between compound and simple interest for three years is ₹228 at 4% interest per annum, the principal is ₹______ (SSC GD 2025)",
        "options": ["46875", "48075", "47295", "46300"],
        "correctAnswer": "46875",
        "solution": "**Step 1:** For 3 years, $CI - SI = P r^2 (3 + r)$.\n\n**Step 2:** $P (0.04)^2 (3.04) = 228$\n$P \\times 0.0016 \\times 3.04 = P \\times 0.004864$\n\n**Step 3:** $P = \\frac{228}{0.004864} = 46875$\n\n**Answer: 46875**",
    },
    {
        "question": "If the difference between C.I and S.I for three years is Rs.840 and the rate of interest is 11(1/9)%, then find the principal.",
        "options": ["Rs.21870", "Rs.20780", "Rs.18225", "Rs.24300"],
        "correctAnswer": "Rs.21870",
        "solution": "**Step 1:** $r = 11\\frac{1}{9}\\% = \\frac{100}{9}\\% = \\frac{1}{9}$.\n\n**Step 2:** $CI - SI = P r^2 (3 + r) = P \\times \\frac{1}{81} \\times \\frac{28}{9} = \\frac{28P}{729}$.\n\n**Step 3:** $\\frac{28P}{729} = 840 \\Rightarrow P = 840 \\times \\frac{729}{28} = 30 \\times 729 = 21870$\n\n**Answer: Rs.21870**",
    },
    {
        "question": "If the difference between C.I and S.I for one and a half years is Rs.1500 and the rate of interest is 25% compounded half yearly, then find the principal.",
        "options": ["Rs.30720", "Rs.20480", "Rs.28800", "Rs.36000"],
        "correctAnswer": "Rs.30720",
        "solution": "**Step 1:** Half-yearly rate $= 12.5\\% = \\frac{1}{8}$ for 3 periods.\n$CI$ factor $= \\left(\\frac{9}{8}\\right)^3 - 1 = \\frac{729}{512} - 1 = \\frac{217}{512}$\n\n**Step 2:** $SI$ factor $= 25\\% \\times 1.5 = 37.5\\% = \\frac{3}{8} = \\frac{192}{512}$.\n\n**Step 3:** Difference factor $= \\frac{25}{512}$.\n$P = 1500 \\times \\frac{512}{25} = 60 \\times 512 = 30720$\n\n**Answer: Rs.30720**",
    },
    {
        "question": "If the difference between the compound interest, compounded annually, and the simple interest on a certain sum of money at 5% per annum for 3 years is Rs.183, then what is the sum of money invested? (SSC GD 2022)",
        "options": ["Rs. 20,000", "Rs. 28,000", "Rs. 24,000", "Rs. 16,000"],
        "correctAnswer": "Rs. 24,000",
        "solution": "**Step 1:** For 3 years, $CI - SI = P r^2 (3 + r)$.\n\n**Step 2:** $P (0.05)^2 (3.05) = P \\times 0.0025 \\times 3.05 = P \\times 0.007625$.\n\n**Step 3:** $P = \\frac{183}{0.007625} = 24000$\n\n**Answer: Rs. 24,000**",
    },
    {
        "question": "A person lent a certain sum on simple interest and the same sum on compound interest at a certain rate of interest per annum. If the ratio between the difference of compound interest and simple interest of 2 years and that of 3 years is 25 : 78, then what is the rate of interest per annum?",
        "options": ["16%", "15%", "10%", "12%"],
        "correctAnswer": "12%",
        "solution": "**Step 1:** For 2 years, $CI - SI = P r^2$. For 3 years, $CI - SI = P r^2 (3 + r)$.\n\n**Step 2:** $\\frac{P r^2}{P r^2 (3+r)} = \\frac{25}{78} \\Rightarrow \\frac{1}{3+r} = \\frac{25}{78}$.\n\n**Step 3:** $3 + r = \\frac{78}{25} = 3.12 \\Rightarrow r = 0.12 = 12\\%$\n\n**Answer: 12%**",
    },
    {
        "question": "The difference between compound interest and simple interest on a certain sum at a certain rate for 3 years is Rs. 2541 and for 2 years it is Rs 840. Find the rate of interest per annum.",
        "options": ["4%", "2.5%", "7.5%", "3.33%"],
        "correctAnswer": "2.5%",
        "solution": "**Step 1:** $D_2 = P r^2 = 840$ and $D_3 = P r^2 (3 + r) = 2541$.\n\n**Step 2:** $\\frac{D_3}{D_2} = 3 + r = \\frac{2541}{840} = 3.025$.\n\n**Step 3:** $r = 0.025 = 2.5\\%$\n\n**Answer: 2.5%**",
    },
    {
        "question": "A sum of money is accumulating at compound interest at a certain rate of interest. If simple interest instead of compound were reckoned, the interest for the first two years would be diminished by Rs.70 and that for the first three years by Rs.213.5. Find the sum.",
        "options": ["21000 Rs.", "28000 Rs.", "24500 Rs.", "35000 Rs."],
        "correctAnswer": "28000 Rs.",
        "solution": "**Step 1:** $D_2 = P r^2 = 70$ and $D_3 = P r^2 (3 + r) = 213.5$.\n\n**Step 2:** $3 + r = \\frac{213.5}{70} = 3.05 \\Rightarrow r = 0.05$.\n\n**Step 3:** $P = \\frac{70}{(0.05)^2} = \\frac{70}{0.0025} = 28000$\n\n**Answer: 28000 Rs.**",
    },
    {
        "question": "The compound interest on a sum of money for 2 years is Rs.832 and the simple interest on the same sum for the same period is Rs.800. The difference between the compound interest and the simple interest for 3 years at the same rate will be:",
        "options": ["Rs.92.36", "Rs.75.64", "Rs.98.56", "Rs.106.56"],
        "correctAnswer": "Rs.98.56",
        "solution": "**Step 1:** SI per year $= \\frac{800}{2} = 400$. Difference for 2 years = 832 − 800 = 32.\n\n**Step 2:** $400 \\times r = 32 \\Rightarrow r = 0.08$, and $P = \\frac{400}{0.08} = 5000$.\n\n**Step 3:** $D_3 = P r^2 (3 + r) = 5000 \\times 0.0064 \\times 3.08 = 32 \\times 3.08 = 98.56$\n\n**Answer: Rs.98.56**",
    },
    {
        "question": "The ratio of the compound interest earned over 2 years when compounding a principal annually to the simple interest earned for the same principal at the same rate for the same duration is 25:24. Find the ratio of the compound interest earned over 3 years when compounding the same principal annually to the simple interest earned for the same principal at the same rate for 3 years.",
        "options": ["625:576", "79:72", "301:288", "469:432"],
        "correctAnswer": "469:432",
        "solution": "**Step 1:** $\\frac{CI_2}{SI_2} = \\frac{P(2r + r^2)}{2Pr} = \\frac{2 + r}{2} = \\frac{25}{24}$.\n\n**Step 2:** $2 + r = \\frac{25}{12} \\Rightarrow r = \\frac{1}{12}$.\n\n**Step 3:** $CI_3 = P\\left[\\left(\\frac{13}{12}\\right)^3 - 1\\right] = P \\cdot \\frac{469}{1728}$ and $SI_3 = 3P \\cdot \\frac{1}{12} = P \\cdot \\frac{432}{1728}$.\n\n**Step 4:** Ratio $= 469 : 432$\n\n**Answer: 469:432**",
    },
    {
        "question": "The difference between the compound interest and the simple interest on a principal of ₹54,000 is ₹1,215 at the same yearly rate of interest for a period of 2 years. Find the rate of interest. (DP CONSTABLE 2023)",
        "options": ["12%", "15%", "18%", "10%"],
        "correctAnswer": "15%",
        "solution": "**Step 1:** For 2 years, $CI - SI = P r^2$.\n\n**Step 2:** $54000 \\, r^2 = 1215 \\Rightarrow r^2 = \\frac{1215}{54000} = 0.0225$.\n\n**Step 3:** $r = 0.15 = 15\\%$\n\n**Answer: 15%**",
    },
    {
        "question": "The difference between the compound interest and the simple interest on ₹80,000 at the same rate of interest per annum for 2 years is ₹98. What is the rate of interest per annum? (DP CONSTABLE 2023)",
        "options": ["3(1/2)%", "5(1/2)%", "2(1/2)%", "7(1/2)%"],
        "correctAnswer": "3(1/2)%",
        "solution": "**Step 1:** For 2 years, $CI - SI = P r^2$.\n\n**Step 2:** $80000 \\, r^2 = 98 \\Rightarrow r^2 = \\frac{98}{80000} = 0.001225$.\n\n**Step 3:** $r = 0.035 = 3.5\\% = 3\\frac{1}{2}\\%$\n\n**Answer: 3(1/2)%**",
    },
    {
        "question": "If the difference between CI and SI on a certain sum of money of Rs.25200 for 2 years is Rs.700, find the rate of interest.",
        "options": ["14(1/7)%", "16(2/3)%", "15%", "13%"],
        "correctAnswer": "16(2/3)%",
        "solution": "**Step 1:** For 2 years, $CI - SI = P r^2$.\n\n**Step 2:** $25200 \\, r^2 = 700 \\Rightarrow r^2 = \\frac{700}{25200} = \\frac{1}{36}$.\n\n**Step 3:** $r = \\frac{1}{6} = 16\\frac{2}{3}\\%$\n\n**Answer: 16(2/3)%**",
    },
    {
        "question": "Amit borrowed a sum of 25000 rupees on simple interest. Bhola borrowed the same amount on compound interest (compounded yearly). At the end of 2 years, Bhola had to pay 160 rupees more interest than Amit. The rate of interest charged per annum is:",
        "options": ["6.4%", "8%", "4%", "4.8%"],
        "correctAnswer": "8%",
        "solution": "**Step 1:** For 2 years, $CI - SI = P r^2$.\n\n**Step 2:** $25000 \\, r^2 = 160 \\Rightarrow r^2 = \\frac{160}{25000} = 0.0064$.\n\n**Step 3:** $r = 0.08 = 8\\%$\n\n**Answer: 8%**",
    },
    {
        "question": "A borrowed ₹58,000 from B at 8% per annum simple interest for 2 years. He lent the same sum to C at 10% per annum compound interest, compounded annually for 2 years. How much did he gain (in ₹) in the transaction at the end of 2 years?",
        "options": ["3,000", "2,800", "2,900", "2,750"],
        "correctAnswer": "2,900",
        "solution": "**Step 1:** Interest paid to B $= 58000 \\times 0.08 \\times 2 = 9280$.\n\n**Step 2:** Interest received from C $= 58000\\left[(1.1)^2 - 1\\right] = 58000 \\times 0.21 = 12180$.\n\n**Step 3:** Gain $= 12180 - 9280 = 2900$\n\n**Answer: 2,900**",
    },
    {
        "question": "A money-lender borrows money at 6% per annum and pays the interest at the end of the year. He lends it at 8% per annum compound interest compounded half-yearly and receives the interest at the end of the year. In this way, he gains Rs.1512 a year. The amount of money he borrows is:",
        "options": ["Rs. 60,000", "Rs. 50,000", "Rs. 55,000", "Rs. 70,000"],
        "correctAnswer": "Rs. 70,000",
        "solution": "**Step 1:** Lending at 8% compounded half-yearly means 4% for 2 periods.\nEffective rate $= (1.04)^2 - 1 = 0.0816 = 8.16\\%$\n\n**Step 2:** Net gain rate $= 8.16\\% - 6\\% = 2.16\\%$.\n\n**Step 3:** $P \\times 0.0216 = 1512 \\Rightarrow P = 70000$\n\n**Answer: Rs. 70,000**",
    },
    {
        "question": "Akhilesh borrowed ₹50,000 at a certain rate on simple interest and lent the same sum to Rakesh on compound interest, compounded annually at the same rate of interest. At the end of 2 years, Rakesh cleared his loan and then Akhilesh also cleared his loan. In the process, Akhilesh earned ₹180. What was the rate of interest charged per annum?",
        "options": ["8%", "6%", "7.5%", "5%"],
        "correctAnswer": "6%",
        "solution": "**Step 1:** The gain is exactly the 2-year difference, $CI - SI = P r^2$.\n\n**Step 2:** $50000 \\, r^2 = 180 \\Rightarrow r^2 = \\frac{180}{50000} = 0.0036$.\n\n**Step 3:** $r = 0.06 = 6\\%$\n\n**Answer: 6%**",
    },
    {
        "question": "Sudha invested her savings in schemes A and B in the ratio 3:5, each for 1(1/2) years. Scheme A offers interest at a rate of 20% per annum compounded 6-monthly, whereas scheme B offers interest at a rate of 10% per annum compounded annually. If the difference between the interests received from A and B is Rs 152.60, then the money invested in scheme B is: (ICAR Assistant 2022)",
        "options": ["Rs 4000", "Rs 4500", "Rs 3000", "Rs 3500"],
        "correctAnswer": "Rs 3500",
        "solution": "**Step 1:** Let the investments be $3x$ in A and $5x$ in B.\n\n**Step 2:** Scheme A: 10% per half-year for 3 periods.\n$I_A = 3x\\left[(1.1)^3 - 1\\right] = 3x \\times 0.331 = 0.993x$\n\n**Step 3:** Scheme B: 10% for 1 year then 5% for the half year.\n$I_B = 5x\\,[1.1 \\times 1.05 - 1] = 5x \\times 0.155 = 0.775x$\n\n**Step 4:** $0.993x - 0.775x = 0.218x = 152.60 \\Rightarrow x = 700$.\nMoney in B $= 5x = 3500$\n\n**Answer: Rs 3500**",
    },
    {
        "question": "Rs.8454 is invested in two parts at the rate of 12% per annum compounded annually for 13 years and 15 years respectively. If the amount received on both investments is equal, then find the difference between both investments.",
        "options": ["Rs.954", "Rs.894", "Rs.1014", "Rs.1272"],
        "correctAnswer": "Rs.954",
        "solution": "**Step 1:** $A(1.12)^{13} = B(1.12)^{15} \\Rightarrow \\frac{A}{B} = (1.12)^2 = \\frac{784}{625}$.\n\n**Step 2:** Let $A = 784k$ and $B = 625k$, so $1409k = 8454 \\Rightarrow k = 6$.\n\n**Step 3:** $A = 4704$, $B = 3750$, difference $= 954$\n\n**Answer: Rs.954**",
    },
    {
        "question": "Ashok has ₹1612 with him. He divided it amongst his sons Raj and Varun and asked them to invest it at 8% rate of interest compounded annually. It was seen that Raj and Varun got the same amount after 15 and 16 years respectively. How much (in ₹) did Ashok give to Raj? (SSC GD 2025)",
        "options": ["687", "837", "875", "775"],
        "correctAnswer": "837",
        "solution": "**Step 1:** $R(1.08)^{15} = V(1.08)^{16} \\Rightarrow \\frac{R}{V} = 1.08 = \\frac{27}{25}$.\n\n**Step 2:** Let $R = 27k$ and $V = 25k$, so $52k = 1612 \\Rightarrow k = 31$.\n\n**Step 3:** $R = 27 \\times 31 = 837$\n\n**Answer: 837**",
    },
    {
        "question": "A man wants to invest Rs.1,34,470 in bank accounts of his two sons whose ages are 12 years and 16 years in such a way that they will get equal amounts at the age of 21 years at the rate of 20% per annum compounded annually. Find the share of the younger brother.",
        "options": ["Rs.43750", "Rs.90720", "Rs.97200", "Rs.42250"],
        "correctAnswer": "Rs.43750",
        "solution": "**Step 1:** The younger son invests for $21 - 12 = 9$ years, the elder for $21 - 16 = 5$ years.\n\n**Step 2:** $Y(1.2)^9 = E(1.2)^5 \\Rightarrow \\frac{Y}{E} = \\frac{1}{(1.2)^4} = \\frac{625}{1296}$.\n\n**Step 3:** $625k + 1296k = 1921k = 134470 \\Rightarrow k = 70$.\nYounger's share $= 625 \\times 70 = 43750$\n\n**Answer: Rs.43750**",
    },
    {
        "question": "A person deposits a certain amount of money at the start of each year. If the rate of interest is 12.5% per annum compounded annually and the compound interest of the third year is Rs.13020, find how much money is deposited each year.",
        "options": ["40960 Rs.", "25600 Rs.", "38400 Rs.", "30720 Rs."],
        "correctAnswer": "30720 Rs.",
        "solution": "**Step 1:** Let the yearly deposit be $D$ and $r = \\frac{1}{8}$, so the growth factor is $\\frac{9}{8}$.\n\n**Step 2:** Balance at the start of year 3:\n$\\left(D \\cdot \\frac{9}{8} + D\\right)\\frac{9}{8} + D = D \\cdot \\frac{153}{64} + D = \\frac{217D}{64}$\n\n**Step 3:** Interest of the 3rd year $= \\frac{217D}{64} \\times \\frac{1}{8} = \\frac{217D}{512} = 13020$.\n$D = 13020 \\times \\frac{512}{217} = 60 \\times 512 = 30720$\n\n**Answer: 30720 Rs.**",
    },
    {
        "question": "A man borrowed a sum of money and agreed to pay it off by paying Rs 4200 at the end of the first year and Rs 4410 at the end of the second year. If the rate of compound interest was 5% per annum, find the sum borrowed. (DP CONSTABLE 2023)",
        "options": ["Rs 7500", "Rs 8000", "Rs 8500", "Rs 7000"],
        "correctAnswer": "Rs 8000",
        "solution": "**Step 1:** The sum borrowed is the present value of both instalments.\n\n**Step 2:** $\\frac{4200}{1.05} = 4000$ and $\\frac{4410}{(1.05)^2} = \\frac{4410}{1.1025} = 4000$.\n\n**Step 3:** Sum $= 4000 + 4000 = 8000$\n\n**Answer: Rs 8000**",
    },
    {
        "question": "A person borrows some money at 10% per annum compound interest for three years. At the end of the second year he deposits Rs. 8470 and at the end of the third year he clears all his debt by paying Rs.13310. What was the money he borrowed?",
        "options": ["Rs. 16000", "Rs. 17000", "Rs. 18000", "Rs. 16997.7"],
        "correctAnswer": "Rs. 17000",
        "solution": "**Step 1:** After 2 years the debt is $P(1.1)^2 = 1.21P$. After paying 8470 the balance is $1.21P - 8470$.\n\n**Step 2:** This balance grows for one more year and equals 13310.\n$(1.21P - 8470) \\times 1.1 = 13310$\n\n**Step 3:** $1.21P - 8470 = 12100 \\Rightarrow 1.21P = 20570 \\Rightarrow P = 17000$\n\n**Answer: Rs. 17000**",
    },
    {
        "question": "A person borrowed a sum of ₹30800 at 10% p.a. for 3 years, interest compounded annually. At the end of two years, he paid a sum of ₹13268. At the end of the 3rd year, he paid ₹x to clear off the debt. What is the value of x?",
        "options": ["26200", "26620", "26400", "26510"],
        "correctAnswer": "26400",
        "solution": "**Step 1:** Debt after 2 years $= 30800 \\times (1.1)^2 = 30800 \\times 1.21 = 37268$.\n\n**Step 2:** After paying 13268, the balance is $37268 - 13268 = 24000$.\n\n**Step 3:** $x = 24000 \\times 1.1 = 26400$\n\n**Answer: 26400**",
    },
]


def main() -> None:
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    original_len = len(data)

    errors: list[str] = []
    for offset, q in enumerate(Q):
        idx = START_INDEX + offset
        entry = data[idx]
        qid = entry["id"]
        expected = f"maths_compound_interest_{START_INDEX + offset + 1:03d}"
        if qid != expected:
            errors.append(f"index {idx}: id {qid} != expected {expected}")
            continue
        if q["correctAnswer"] not in q["options"]:
            errors.append(f"{qid}: correctAnswer not in options")
            continue
        data[idx] = {
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "correctAnswer": q["correctAnswer"],
            "solution": q["solution"],
        }

    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))

    assert len(data) == original_len, "entry count changed"
    TARGET.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    last = START_INDEX + len(Q)
    print(f"Filled {len(Q)} questions")
    print(f"IDs: {data[START_INDEX]['id']} .. {data[last - 1]['id']}")
    print(f"Next placeholder still at: {data[last]['id']}")


if __name__ == "__main__":
    main()
