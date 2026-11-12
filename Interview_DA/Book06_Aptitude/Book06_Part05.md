# Book 6 — Aptitude & Business Maths | Part 5: Number Series & Number System 🟢🟡🔴

**Target:** 50 questions | **Actual:** 70 questions
**Scope:** number series (arithmetic, geometric, difference, alternating, wrong-term, missing-term) and number system (divisibility, primes, HCF/LCM, remainders, unit digits, factors) as asked in analyst online aptitude gates.

### Q1 ⭐⭐⭐ 🟢 What are the divisibility rules for 2, 3, 4, 5, 6, 8, 9 and 11?
**Asked at:** commonly asked (no company-specific report found); divisibility is listed in prep-site syllabi for TCS NQT numerical ability (unverified prep-site claim).
**What the interviewer is checking:** Whether you can test a number quickly without long division.
**Say this in the interview:** "Each rule looks at only part of the number: last digit for 2 and 5, last two digits for 4, last three for 8, digit sum for 3 and 9, and the alternating digit sum for 11. 6 needs both 2 and 3."
**Answer:** **The rules are in the list below.**
**Explain simply:**
- 2: last digit is 0, 2, 4, 6 or 8. 5: last digit is 0 or 5.
- 4: the last two digits form a number divisible by 4. 8: the last three digits form a number divisible by 8. (Because 100 is divisible by 4 and 1000 by 8, the front part never matters.)
- 3 and 9: add all digits ("digit sum"); if the sum is divisible by 3 (or 9), so is the number. (Because 10, 100, 1000... each leave remainder 1 when divided by 3 or 9.)
- 6: divisible by both 2 and 3.
- 11: add the digits in odd places, add the digits in even places, subtract. If the difference is 0 or a multiple of 11, the number is divisible by 11.
**Worked mini-example:** 5,346: even (so by 2); digit sum 5+3+4+6 = 18 (so by 3, 9 and, being even, by 6); odd-place digits from the right 6+3 = 9, even-place 4+5 = 9, difference 0 (so by 11). Last three digits 346 are not divisible by 8 (346 / 8 = 43.25), so it is not.
**Check:** verified by script (5,346 = 2 x 3 x 3 x 3 x 99 = 9 x 594 = 11 x 486 checks).
**Likely follow-ups:** 1) *Rule for 12?* Divisible by both 3 and 4. 2) *Rule for 7?* No short rule; just divide.
**Common mistakes / traps:** Saying "divisible by 6" after checking only 2 or only 3; testing 4 with the last digit only; forgetting that a difference of 0 counts as divisible by 11.

### Q2 ⭐⭐⭐ 🟢 How do you approach a number series question when the pattern is not obvious (first differences, second differences, ratios, squares/cubes, primes, alternating series)?
**Asked at:** commonly asked (no company-specific report found); prep sites (FACE Prep, JobCannon) describe first differences as the first thing to try, and claim 5-8 series items in Infosys aptitude (unverified).
**What the interviewer is checking:** A calm, ordered method rather than guessing.
**Say this in the interview:** "I try a fixed checklist: differences, differences of differences, ratios, squares and cubes, primes, then two interleaved series. I stop at the first rule that fits every term."
**Answer:** **Work through the checklist in order and confirm the rule on all terms, not just the first two.**
**Explain simply:**
- Step 1, first differences (term minus previous term). Constant gives an arithmetic series: 3, 7, 11, 15 (+4).
- Step 2, differences of differences. If the differences are 1, 2, 4, 8 they double (add a power of 2); if 2, 4, 6, 8 they grow by 2 (second difference constant).
- Step 3, ratios. Same multiplier each time is geometric: 3, 6, 12, 24.
- Step 4, compare with squares (1, 4, 9, 16...), cubes (1, 8, 27, 64...) and primes (2, 3, 5, 7...). Often the terms are n squared plus or minus a small number.
- Step 5, alternating: if odd and even positions behave differently, split into two series (4, 6, 12, 14: +2, x2, +2...).
- Step 6, mixed rules: multiply then add a growing number (see Q21).
**Worked mini-example:** 2, 3, 5, 9, 17: differences 1, 2, 4, 8, so the next gap is 16 and the next term is 33.
**Likely follow-ups:** 1) *Which series has first differences 5, 7, 9?* Second difference 2 (a squares-type series). 2) *What if nothing fits?* Recheck arithmetic, then try product-then-add.
**Common mistakes / traps:** Fitting a rule to the first three terms only; forgetting to test the alternating split; not re-verifying the rule on the last term.

### Q3 ⭐⭐⭐ 🟢 Find the missing number in the series 2, 5, 8, 11, 14, ?
**Asked at:** commonly asked (no company-specific report found); this is the basic arithmetic-series type in every prep source.
**What the interviewer is checking:** Spotting a constant step.
**Say this in the interview:** "The gap is a constant 3, so the next term is 14 + 3 = 17."
**Answer:** **17**
**Step-by-step working:**
1. Differences: 5-2 = 3, 8-5 = 3, 11-8 = 3, 14-11 = 3.
2. Constant difference 3, so add 3 again: 14 + 3 = 17.
**Check:** the nth term is 3n - 1; for n = 6 it gives 18 - 1 = 17.
**Explain simply:**
- A series with a constant gap is an arithmetic progression (AP).
**Likely follow-ups:** *What is the 20th term?* 3 x 20 - 1 = 59.
**Common mistakes / traps:** Overthinking a very easy question.

### Q4 ⭐⭐⭐ 🟢 Find the next number in the series 1, 4, 9, 16, 25, ?
**Asked at:** commonly asked (no company-specific report found); squares appear in the series taxonomy of practice vendors.
**What the interviewer is checking:** Recognising perfect squares.
**Say this in the interview:** "These are 1 squared, 2 squared and so on, so the next is 6 squared, 36."
**Answer:** **36**
**Step-by-step working:**
1. 1 = 1x1, 4 = 2x2, 9 = 3x3, 16 = 4x4, 25 = 5x5.
2. Next is 6 x 6 = 36.
**Fast method (30 seconds):** the gaps are 3, 5, 7, 9, so the next gap is 11: 25 + 11 = 36. (Squares grow by consecutive odd numbers.)
**Check:** 25 + 11 = 36 = 6 x 6.
**Explain simply:**
- A perfect square is a whole number multiplied by itself.
**Likely follow-ups:** *Next after 36?* 36 + 13 = 49.
**Common mistakes / traps:** Adding 9 (copying the last gap) to get 34.

### Q5 ⭐⭐⭐ 🟢 Find the HCF and LCM of 24 and 36, and verify that the product of the two numbers equals HCF x LCM.
**Asked at:** commonly asked (no company-specific report found); PrepInsta lists HCF/LCM quizzes tagged for TCS and Infosys (the tagging is the site's, unverified).
**What the interviewer is checking:** Prime factorisation and the HCF x LCM identity.
**Say this in the interview:** "24 = 2^3 x 3 and 36 = 2^2 x 3^2. HCF takes the smaller powers, 12; LCM takes the larger powers, 72. And 12 x 72 = 864 = 24 x 36."
**Answer:** **HCF = 12, LCM = 72; both products equal 864.**
**Step-by-step working:**
1. Factorise: 24 = 2 x 2 x 2 x 3; 36 = 2 x 2 x 3 x 3.
2. HCF (highest common factor, the biggest number dividing both) = common part = 2 x 2 x 3 = 12.
3. LCM (least common multiple, the smallest number both divide into) = 2^3 x 3^2 = 8 x 9 = 72.
4. Product of numbers: 24 x 36 = 864. HCF x LCM = 12 x 72 = 864. Equal.
**Check:** 72 / 24 = 3 and 72 / 36 = 2 (whole numbers), and 12 divides both 24 and 36.
**Explain simply:**
- For any two numbers, HCF x LCM = product of the two numbers.
**Likely follow-ups:** *Find LCM of 24 and 36 using the identity?* 864 / 12 = 72.
**Common mistakes / traps:** Using the larger powers for HCF; swapping HCF and LCM; the identity holds for two numbers only, not three.

### Q6 ⭐⭐⭐ 🟢 How do you check whether 241 is a prime number without a calculator?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing you only test primes up to the square root.
**Say this in the interview:** "The square root of 241 is just under 16, so I test the primes 2, 3, 5, 7, 11 and 13. None divides it, so it is prime."
**Answer:** **Yes, 241 is prime.**
**Step-by-step working:**
1. 15 x 15 = 225 and 16 x 16 = 256, so the square root of 241 lies between 15 and 16. Test primes up to 13.
2. 2: odd, no. 3: digit sum 2+4+1 = 7, no. 5: ends in 1, no.
3. 7: 7 x 34 = 238, remainder 3, no.
4. 11: 11 x 21 = 231, remainder 10, no.
5. 13: 13 x 18 = 234, remainder 7, no.
6. No prime up to 13 divides 241, so it is prime.
**Check:** verified by script (no divisor from 2 to 15).
**Explain simply:**
- If a number had a factor above its square root, the partner factor would be below it, so we would have found it already.
**Likely follow-ups:** *Is 253 prime?* No: 11 x 23 = 253.
**Common mistakes / traps:** Testing every number up to 241; forgetting 11 and 13; assuming odd numbers are prime.

### Q7 ⭐⭐⭐ 🟢 What is the unit digit of the product 13 x 27 x 34?
**Asked at:** commonly asked (no company-specific report found); unit-digit questions appear on prep sites (CCBP).
**What the interviewer is checking:** That only last digits matter in a product.
**Say this in the interview:** "Multiply only the unit digits: 3 x 7 = 21, keep 1; 1 x 4 = 4. The unit digit is 4."
**Answer:** **4**
**Step-by-step working:**
1. Unit digits are 3, 7 and 4.
2. 3 x 7 = 21, unit digit 1.
3. 1 x 4 = 4.
**Check:** full product 13 x 27 x 34 = 11,934, which ends in 4.
**Explain simply:**
- The last digit of a product depends only on the last digits of the factors.
**Likely follow-ups:** *Unit digit of 15 x 22 x 9?* 5 x 2 = 10 gives 0; 0 x 9 = 0.
**Common mistakes / traps:** Carrying the whole 21 forward instead of just the 1.

### Q8 ⭐⭐⭐ 🟢 Is 5,346 divisible by 9? Is it divisible by 11? Show the rule you used for each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Applying the digit-sum and alternating-sum rules correctly.
**Say this in the interview:** "Digit sum is 18, which is a multiple of 9, so yes. Alternating sum is (6+3) - (4+5) = 0, so yes for 11 too."
**Answer:** **Yes to both: divisible by 9 and by 11.**
**Step-by-step working:**
1. By 9: digit sum 5+3+4+6 = 18, and 18 = 9 x 2. Divisible.
2. By 11: digits from the right in odd places: 6 and 3, sum 9. Even places: 4 and 5, sum 9. Difference 9 - 9 = 0. Zero counts as a multiple of 11. Divisible.
**Check:** 9 x 594 = 5,346 and 11 x 486 = 5,346 (verified by script).
**Explain simply:**
- Since 9 and 11 share no factor, being divisible by both means it is divisible by 99: 99 x 54 = 5,346.
**Likely follow-ups:** *Is 2,849 divisible by 11?* (9+8) - (4+2) = 11, yes (11 x 259).
**Common mistakes / traps:** Treating a difference of 0 as "not divisible".

### Q9 ⭐⭐⭐ 🟢 Find the sum of the first 50 natural numbers.
**Asked at:** commonly asked (no company-specific report found); a standard gap-fill formula question.
**What the interviewer is checking:** Knowing n(n+1)/2.
**Say this in the interview:** "Sum of first n natural numbers is n times n+1 over 2: 50 x 51 / 2 = 1,275."
**Answer:** **1,275**
**Step-by-step working:**
1. Formula: n(n+1)/2 with n = 50.
2. 50 x 51 = 2,550.
3. 2,550 / 2 = 1,275.
**Fast method (30 seconds):** pair the numbers: 1+50, 2+49, ... each pair is 51, and there are 25 pairs: 25 x 51 = 1,275.
**Check:** verified by script (sum of 1 to 50 = 1,275).
**Explain simply:**
- Natural numbers are the counting numbers 1, 2, 3, ...
**Likely follow-ups:** *Sum of first 100?* 100 x 101 / 2 = 5,050.
**Common mistakes / traps:** Forgetting to halve (answer 2,550); using n x n / 2.

### Q10 ⭐⭐⭐ 🟢 What is the remainder when 7,893,456 is divided by 9, using the digit-sum method?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using the digit sum as a remainder shortcut.
**Say this in the interview:** "A number leaves the same remainder mod 9 as its digit sum. 7+8+9+3+4+5+6 = 42, and 42 gives remainder 6, so the answer is 6."
**Answer:** **6**
**Step-by-step working:**
1. Digit sum: 7+8+9+3+4+5+6 = 42.
2. Reduce: 4+2 = 6 (or 42 - 36 = 6, as 9 x 4 = 36).
3. Remainder is 6.
**Check:** verified by script (7,893,456 mod 9 = 6).
**Explain simply:**
- Each place value 10, 100, ... leaves remainder 1 when divided by 9, so only the digits matter.
**Likely follow-ups:** *Remainder when divided by 3?* 42 mod 3 = 0.
**Common mistakes / traps:** Answering 42 (not reducing further); answering 0 for any digit sum that merely looks round.

### Q11 ⭐⭐⭐ 🟡 Find the next number in the series 2, 3, 5, 9, 17, 33, ?
**Asked at:** commonly asked (no company-specific report found); growing-difference series appear in practice-vendor material.
**What the interviewer is checking:** Second-level pattern: doubling differences.
**Say this in the interview:** "The differences are 1, 2, 4, 8, 16, doubling each time, so the next gap is 32 and the term is 65."
**Answer:** **65**
**Step-by-step working:**
1. Differences: 3-2 = 1, 5-3 = 2, 9-5 = 4, 17-9 = 8, 33-17 = 16.
2. They double, so the next is 32.
3. 33 + 32 = 65.
**Fast method (30 seconds):** the terms are a power of 2 plus 1: (the terms are 1+1, 2+1, 4+1, 8+1, 16+1, 32+1), so the next is 64 + 1 = 65.
**Check:** 64 + 1 = 65, and 65 - 33 = 32.
**Explain simply:**
- When differences themselves follow a pattern (here powers of 2), extend that pattern.
**Likely follow-ups:** *Next after 65?* 65 + 64 = 129.
**Common mistakes / traps:** Guessing 49 by treating the gaps as +16 again.

### Q12 ⭐⭐⭐ 🟡 Find the next number in the series 4, 6, 12, 14, 28, 30, ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Alternating operations.
**Say this in the interview:** "The rule alternates: add 2, then multiply by 2. After 30 comes the multiply step: 60."
**Answer:** **60**
**Step-by-step working:**
1. 4 + 2 = 6; 6 x 2 = 12; 12 + 2 = 14; 14 x 2 = 28; 28 + 2 = 30.
2. The next operation is x 2: 30 x 2 = 60.
**Check:** verified by script; the pattern fits every term, and 30 x 2 = 60.
**Explain simply:**
- Alternating-operation series repeat a pair of steps.
**Likely follow-ups:** *Next after 60?* 62.
**Common mistakes / traps:** Seeing only "+2, +6, +2, +14" and failing to find the rule.

### Q13 ⭐⭐⭐ 🟡 Find the next number in the series 2, 6, 12, 20, 30, 42, ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Second differences or n(n+1).
**Say this in the interview:** "The terms are 1x2, 2x3, 3x4, ... so the next is 7 x 8 = 56."
**Answer:** **56**
**Step-by-step working:**
1. Differences: 4, 6, 8, 10, 12. They rise by 2.
2. Next difference is 14.
3. 42 + 14 = 56.
**Fast method (30 seconds):** each term is n x (n+1): 2 = 1x2, 6 = 2x3, 12 = 3x4, 42 = 6x7, so the 7th is 7 x 8 = 56.
**Check:** 7 x 8 = 56 = 42 + 14.
**Explain simply:**
- A constant second difference signals an "n squared" type series.
**Likely follow-ups:** *Next after 56?* 8 x 9 = 72.
**Common mistakes / traps:** Adding 12 again (54).

### Q14 ⭐⭐⭐ 🟡 What is the unit digit of 7^45? Explain the cyclicity method.
**Asked at:** CCBP's prep-site article gives a similar unit-digit cyclicity question (unverified claim of company use); otherwise commonly asked.
**What the interviewer is checking:** Cyclicity of last digits.
**Say this in the interview:** "Powers of 7 end in 7, 9, 3, 1 and repeat every 4. 45 leaves remainder 1 on division by 4, so the digit is the first in the cycle: 7."
**Answer:** **7**
**Step-by-step working:**
1. 7^1 = 7, 7^2 = 49 (9), 7^3 = 343 (3), 7^4 = 2401 (1), 7^5 ends in 7 again. Cycle length 4.
2. 45 / 4 = 11 remainder 1.
3. Remainder 1 picks the first digit of the cycle: 7.
**Check:** verified by script (7^45 mod 10 = 7).
**Explain simply:**
- Cyclicity: the unit digit of successive powers repeats in a loop. Divide the exponent by the cycle length; a remainder of 0 means use the last digit in the cycle.
**Likely follow-ups:** *Unit digit of 7^46?* Remainder 2, so 9.
**Common mistakes / traps:** Treating remainder 0 as the first digit; wrong cycle length (digits 2, 3, 7, 8 cycle by 4; 4 and 9 by 2).

### Q15 ⭐⭐⭐ 🟡 What is the remainder when 2^100 is divided by 7?
**Asked at:** CCBP gives a similar "2^100 mod 3" question (prep-site, unverified); otherwise commonly asked.
**What the interviewer is checking:** Finding a short repeating cycle of remainders.
**Say this in the interview:** "2^3 = 8 leaves remainder 1 mod 7, so 2^99 leaves 1, and 2^100 leaves 2."
**Answer:** **2**
**Step-by-step working:**
1. 2^3 = 8 = 7 + 1, so 2^3 leaves remainder 1.
2. 100 = 3 x 33 + 1, so 2^100 = (2^3)^33 x 2.
3. (2^3)^33 leaves remainder 1 (1 raised to any power is 1).
4. So the remainder is 1 x 2 = 2.
**Check:** verified by script (pow(2,100,7) = 2); remainders of 2^1, 2^2, 2^3 are 2, 4, 1 and repeat.
**Explain simply:**
- Remainders of successive powers repeat in a cycle, just like unit digits.
**Likely follow-ups:** *Remainder of 2^101 mod 7?* 4.
**Common mistakes / traps:** Answering 1 by forgetting the leftover single factor of 2.

### Q16 ⭐⭐⭐ 🟡 What is the greatest number that divides 148, 246 and 623 leaving remainders 4, 6 and 11 respectively?
**Asked at:** PrepInsta (TCS Ninja quiz) shows exactly these numbers (prep site, unverified use at TCS).
**What the interviewer is checking:** Subtract the remainders, then take the HCF.
**Say this in the interview:** "Subtract the remainders to get 144, 240 and 612, which the number must divide exactly. Their HCF is 12."
**Answer:** **12**
**Step-by-step working:**
1. 148 - 4 = 144; 246 - 6 = 240; 623 - 11 = 612.
2. HCF of 144 and 240: 240 - 144 = 96; HCF(144, 96) = 48.
3. HCF of 48 and 612: 612 = 48 x 12 + 36; HCF(48, 36) = 12.
4. 12 is bigger than every remainder (4, 6, 11), as required.
**Check:** 148 = 12 x 12 + 4; 246 = 12 x 20 + 6; 623 = 12 x 51 + 11. All match.
**Explain simply:**
- A remainder must be smaller than the divisor, so the divisor must exceed 11.
**Likely follow-ups:** *Same, but all leave remainder 5 for 59, 95, 131?* HCF(54, 90, 126) = 18.
**Common mistakes / traps:** Taking the HCF of the original numbers (gives 1); not checking the divisor exceeds the remainders.

### Q17 ⭐⭐⭐ 🟡 What is the least number which, when divided by 12, 15 and 20, leaves a remainder of 7 in each case?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** LCM plus the common remainder.
**Say this in the interview:** "LCM of 12, 15 and 20 is 60, so the answer is 60 + 7 = 67."
**Answer:** **67**
**Step-by-step working:**
1. 12 = 2^2 x 3; 15 = 3 x 5; 20 = 2^2 x 5.
2. LCM = 2^2 x 3 x 5 = 60.
3. Add the common remainder: 60 + 7 = 67.
**Check:** 67 = 12 x 5 + 7 = 15 x 4 + 7 = 20 x 3 + 7. Also 7 is smaller than 12, 15 and 20.
**Explain simply:**
- A multiple of the LCM divides evenly; adding 7 leaves remainder 7 each time.
**Likely follow-ups:** *Remainder 7 is replaced by "short by 1" each time?* 60 - 1 = 59.
**Common mistakes / traps:** Answering 60 or 7.

### Q18 ⭐⭐⭐ 🟡 The HCF of two numbers is 12 and their LCM is 180. If one number is 36, find the other.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using HCF x LCM = product.
**Say this in the interview:** "Product of the two numbers is 12 x 180 = 2,160, so the other is 2,160 / 36 = 60."
**Answer:** **60**
**Step-by-step working:**
1. HCF x LCM = 12 x 180 = 2,160.
2. 2,160 / 36 = 60.
**Check:** HCF(36, 60) = 12 and LCM(36, 60) = 180 (verified by script).
**Explain simply:**
- For two numbers, HCF x LCM = number 1 x number 2.
**Likely follow-ups:** *Could the LCM be 100 with HCF 12?* No, the LCM must be a multiple of the HCF.
**Common mistakes / traps:** Dividing 180 by 36 (gives 5).

### Q19 ⭐⭐⭐ 🟡 Three payroll batches run every 6, 8 and 12 days respectively, and all three ran together today. After how many days will all three next run on the same day?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured gap-fill of the standard LCM word problem.
**What the interviewer is checking:** Recognising "together again" means LCM.
**Say this in the interview:** "They coincide at common multiples; the first is the LCM of 6, 8 and 12, which is 24 days."
**Answer:** **24 days**
**Step-by-step working:**
1. 6 = 2 x 3; 8 = 2^3; 12 = 2^2 x 3.
2. Highest powers: 2^3 and 3, so LCM = 8 x 3 = 24.
**Check:** 24 / 6 = 4, 24 / 8 = 3, 24 / 12 = 2 runs, all whole numbers; and no smaller number works (12 / 8 is not whole).
**Explain simply:**
- "Meet again" or "together again" problems use LCM; "split into equal groups" or "largest size" use HCF.
**Likely follow-ups:** *Next time after that?* Day 48.
**Common mistakes / traps:** Using HCF (gives 2) or multiplying all (576).

### Q20 ⭐⭐⭐ 🔴 What is the remainder when 17^23 is divided by 18? (Use the negative-remainder shortcut.)
**Asked at:** FACE Prep's remainders guide describes the negative-remainder shortcut (prep site, unverified); otherwise commonly asked.
**What the interviewer is checking:** Writing 17 as -1 modulo 18.
**Say this in the interview:** "17 is one less than 18, so it behaves like -1. (-1) to an odd power is -1, and -1 plus 18 gives remainder 17."
**Answer:** **17**
**Step-by-step working:**
1. 17 = 18 - 1, so 17 leaves remainder -1 when divided by 18.
2. (-1)^23 = -1 because 23 is odd.
3. A remainder of -1 is converted by adding the divisor: -1 + 18 = 17.
**Check:** verified by script (pow(17,23,18) = 17); 17^2 = 289 = 18 x 16 + 1, so even powers give 1, odd powers give 17.
**Explain simply:**
- The negative-remainder shortcut: use the remainder closest to zero, even if negative, as it makes powers easy.
**Likely follow-ups:** *Remainder of 17^24 mod 18?* (-1)^24 = 1.
**Common mistakes / traps:** Answering -1 without converting to a valid remainder; answering 1.

### Q21 ⭐⭐⭐ 🔴 Find the next number in the series 15, 16, 34, 105, 424, ?
**Asked at:** commonly asked (no company-specific report found); a mixed-operation "multiply and add" series.
**What the interviewer is checking:** Persistence beyond simple differences.
**Say this in the interview:** "Each term is the previous times 1, 2, 3, 4 plus 1, 2, 3, 4. Next is 424 x 5 + 5 = 2,125."
**Answer:** **2,125**
**Step-by-step working:**
1. 15 x 1 + 1 = 16.
2. 16 x 2 + 2 = 34.
3. 34 x 3 + 3 = 105.
4. 105 x 4 + 4 = 424.
5. 424 x 5 + 5 = 2,120 + 5 = 2,125.
**Check:** verified by script; the rule fits all four known steps, which makes a coincidence unlikely. Differences (1, 18, 71, 319) show no simple pattern, which is why this test was designed as a trap.
**Explain simply:**
- When differences and ratios fail, test "multiply by a growing number, then add a growing number".
**Likely follow-ups:** *Next after 2,125?* 2,125 x 6 + 6 = 12,756.
**Common mistakes / traps:** Giving up on differences-only thinking; stopping at one example of the rule.

### Q22 ⭐⭐ 🟢 What is the difference between natural numbers, whole numbers, integers, rational numbers and irrational numbers? Give one example of each.
**Asked at:** commonly asked (no company-specific report found); a definitions item.
**What the interviewer is checking:** Clean vocabulary of number types.
**Say this in the interview:** "Each set contains the one before: natural, whole, integers, rational. Irrational numbers sit outside rational ones."
**Answer:** **Definitions and examples below.**
**Explain simply:**
- Natural numbers: counting numbers 1, 2, 3, ... Example: 7 (headcount of a team).
- Whole numbers: natural numbers plus zero. Example: 0 (open vacancies).
- Integers: whole numbers plus negatives. Example: -4 (change in headcount).
- Rational numbers: anything written as a fraction p/q of integers with q not zero; decimals end or repeat. Example: 3/4, or 0.333... = 1/3.
- Irrational numbers: cannot be written as a fraction; decimals never end or repeat. Example: the square root of 2 (1.41421...) or pi.
**Worked mini-example:** -3 is an integer and rational (-3/1) but not natural or whole. 0.5 is rational but not an integer.
**Likely follow-ups:** 1) *Is 0 natural?* In most aptitude books no (it is whole). 2) *Is the square root of 16 irrational?* No, it equals 4.
**Common mistakes / traps:** Calling 22/7 irrational (it is a fraction, so rational); thinking 0 is natural.

### Q23 ⭐⭐ 🟢 Find the next number in the Fibonacci-type series 0, 1, 1, 2, 3, 5, 8, ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Recognising "each term is the sum of the previous two".
**Say this in the interview:** "Each term is the sum of the two before it, so 5 + 8 = 13."
**Answer:** **13**
**Step-by-step working:**
1. 0 + 1 = 1; 1 + 1 = 2; 1 + 2 = 3; 2 + 3 = 5; 3 + 5 = 8.
2. Next: 5 + 8 = 13.
**Check:** 13 - 8 = 5, the term before 8.
**Explain simply:**
- This is the Fibonacci sequence; differences (1, 0, 1, 1, 2, 3) are the series itself.
**Likely follow-ups:** *Next after 13?* 8 + 13 = 21.
**Common mistakes / traps:** Looking for a constant difference and guessing 11 or 12.

### Q24 ⭐⭐ 🟢 Find the next number in the series 11, 13, 17, 19, 23, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Spotting a non-arithmetic pattern.
**Say this in the interview:** These are consecutive prime numbers, numbers with exactly two factors, 1 and themselves. After 23 the next prime is 29.
**Answer:** **29**
**Step-by-step working:**
1. Look at the series: 11, 13, 17, 19, 23. None can be split into smaller whole-number factors, so they are primes.
2. The next candidate after 23 is 24. It is even, so it is divisible by 2: not prime.
3. 25 = 5 x 5: not prime. 26 is even. 27 = 3 x 9. 28 is even.
4. 29 has no divisor other than 1 and itself (not divisible by 2, 3 or 5; 7 x 7 = 49 is already above 29): prime.
**Fast method (30 seconds):** Skip even numbers and anything ending in 5; test only 3 and 7 for the rest.
**Check:** The next prime after 23 is 29; 24 to 28 each have a divisor (24, 25, 26, 27, 28 all fail), verified by script.
**Explain simply:**
- A prime is a number above 1 that only 1 and itself divide exactly.
- The gaps (2, 4, 2, 4, 6) are irregular, so a difference method fails; that irregularity is the clue it is a prime series.
**Likely follow-ups:** Next after 29? 31. Is 1 prime? No, it has only one factor.
**Common mistakes / traps:** Looking for a pattern in differences (2, 4, 2, 4) and answering 25 (add 2). 25 is 5 x 5, so it is not prime.

### Q25 ⭐⭐ 🟢 Find the next number in the series 1, 8, 27, 64, 125, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Recognising squares/cubes.
**Say this in the interview:** The terms are perfect cubes: 1^3, 2^3, 3^3, 4^3, 5^3. The next is 6^3 = 216.
**Answer:** **216**
**Step-by-step working:**
1. 1 = 1x1x1, 8 = 2x2x2, 27 = 3x3x3, 64 = 4x4x4, 125 = 5x5x5.
2. The next base is 6.
3. 6 x 6 = 36; 36 x 6 = 216.
**Fast method (30 seconds):** Learn cubes 1 to 10: 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000. Cubes end in the digit pattern 1, 8, 7, 4, 5, 6, 3, 2, 9, 0.
**Check:** 6 x 6 x 6 = 36 x 6 = 216; difference method also gives 91 (125 + 91) = 216, verified by script.
**Explain simply:**
- A cube is a number multiplied by itself three times.
- Quick signal: when the terms grow fast and look familiar (8, 27, 64), test cubes before differences.
**Likely follow-ups:** What is the next term after 216? 343 (7^3). What if the series was 2, 9, 28, 65, 126? Cubes plus 1 (n^3 + 1), so the next term is 6^3 + 1 = 217.
**Common mistakes / traps:** Taking differences (7, 19, 37, 61) and getting lost; they form a second-level pattern, so cubes are the quick route. Another trap is answering 189 (adding 64 to 125).

### Q26 ⭐⭐ 🟢 Find the sum of the first 10 even natural numbers.
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Sum-of-series formula.
**Say this in the interview:** Add 2 + 4 + ... + 20. Use the pattern: sum of first n even numbers = n x (n + 1).
**Answer:** **110**
**Step-by-step working:**
1. The first 10 even natural numbers are 2, 4, 6, 8, 10, 12, 14, 16, 18, 20.
2. Pair first and last: 2 + 20 = 22, 4 + 18 = 22, and so on: 5 pairs.
3. 5 x 22 = 110.
**Fast method (30 seconds):** Formula n x (n + 1) = 10 x 11 = 110. It works because the sum is 2 x (1 + 2 + ... + n) = 2 x n(n+1)/2.
**Check:** Reverse: 110 / 10 = 11 = average of 2 and 20; verified by script.
**Explain simply:**
- Natural numbers are the counting numbers 1, 2, 3...; even ones are divisible by 2.
- Pairing the ends is the trick used by the maths student Gauss: every pair adds to the same total.
**Likely follow-ups:** Sum of first 10 odd numbers? 10 x 10 = 100. Sum of first 50 even numbers? 50 x 51 = 2,550.
**Common mistakes / traps:** Using n x n (the formula for odd numbers, giving 100).

### Q27 ⭐⭐ 🟢 Convert the recurring decimal 0.363636... into a fraction in its lowest terms.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Fractions from recurring decimals.
**Say this in the interview:** Let x = 0.3636.... The repeating block is 2 digits, so multiply by 100, subtract, and simplify. Answer 4/11.
**Answer:** **4/11**
**Step-by-step working:**
1. Let x = 0.363636...
2. Two digits repeat, so multiply by 100: 100x = 36.363636...
3. Subtract: 100x - x = 36, so 99x = 36.
4. x = 36/99.
5. Divide top and bottom by 9 (the highest common factor): 36/9 = 4, 99/9 = 11. So x = 4/11.
**Fast method (30 seconds):** Repeating block over as many 9s as the block has digits: 36 over 99, then reduce. HCF of 36 and 99 is 9.
**Check:** Reverse: 4 / 11 = 0.363636..., since 11 x 0.363636 = 4.0; verified by script with exact fractions.
**Explain simply:**
- A recurring decimal repeats a block forever; every such decimal is a fraction.
- Multiplying by 10, 100, ... (as many zeros as repeating digits) moves the decimal point so the infinite tail cancels on subtraction.
- Lowest terms means no further common factor.
**Likely follow-ups:** 0.272727... as a fraction? 27/99 = 3/11. 0.1666...? (mixed repeat) 1/6.
**Common mistakes / traps:** Leaving the answer as 36/99, or putting 36/100. Test setters offer 36/99 as a trap option.

### Q28 ⭐⭐ 🟢 What is the largest 4-digit number divisible by 16?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Largest multiple below a limit.
**Say this in the interview:** Take the largest 4-digit number 9999, divide by 16, and subtract the remainder.
**Answer:** **9,984**
**Step-by-step working:**
1. Largest 4-digit number is 9,999.
2. 16 x 624 = 9,984 and 16 x 625 = 10,000 (too big).
3. Remainder of 9,999 / 16 = 9,999 - 9,984 = 15.
4. 9,999 - 15 = 9,984.
**Fast method (30 seconds):** Largest number below a limit divisible by d: limit minus (limit mod d). Here 9,999 mod 16 = 15, so 9,999 - 15.
**Check:** 9984 / 16 = 624 exactly; 9984 + 16 = 10,000, which has 5 digits, verified by script.
**Explain simply:**
- Divisible means leaves remainder 0.
- Subtracting the remainder moves you down to the nearest multiple.
**Likely follow-ups:** Largest 4-digit number divisible by 25? 9,975. Smallest 4-digit divisible by 16? 1,008.
**Common mistakes / traps:** Subtracting 16 from 9,999 or forgetting that 9,999 itself is not a multiple.

### Q29 ⭐⭐ 🟢 How many prime numbers are there below 50? List them.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Prime-number facts.
**Say this in the interview:** I cross out multiples of 2, 3, 5 and 7, because any composite number below 50 has a factor up to 7. 15 numbers survive.
**Answer:** **15 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47**
**Step-by-step working:**
1. Prime: only factors are 1 and itself. 1 is not prime.
2. Only test divisors up to 7, since 7 x 7 = 49 and the next prime 11 squared is 121.
3. Under 10: 2, 3, 5, 7 (4 primes).
4. 10-19: 11, 13, 17, 19 (4).
5. 20-29: 23, 29 (2).
6. 30-39: 31, 37 (2).
7. 40-49: 41, 43, 47 (3).
8. Total 4 + 4 + 2 + 2 + 3 = 15.
**Fast method (30 seconds):** Remember: 4, 4, 2, 2, 3 across the decades below 50. Only 2 is an even prime.
**Check:** Counted: 15 primes; sieve of Eratosthenes (crossing out multiples of 2, 3, 5, 7) verified by script.
**Explain simply:**
- The sieve method means striking out multiples of each prime in turn.
- You need to test only primes up to the square root of the number.
**Likely follow-ups:** How many primes below 100? 25. Is 51 prime? No, 3 x 17.
**Common mistakes / traps:** Calling 1, 9, 15, 21, 27, 33, 39, 49 prime; 49 = 7 x 7 is the classic trap.

### Q30 ⭐⭐ 🟢 Monthly sales are Rs 5,000, Rs 5,500, Rs 6,050 and Rs 6,655 in four consecutive months. If the same pattern continues, what are the sales in the fifth month?
**Asked at:** commonly asked (no company-specific report found); compounding-growth pattern also appears in business series.
**What the interviewer is checking:** Spotting growth rate / GP.
**Say this in the interview:** The sales grow by 10% each month (multiplying by 1.1), so month 5 is 6,655 x 1.1 = Rs 7,320.50.
**Answer:** **Rs 7,320.50** (rounded to the paisa; about Rs 7,321)
**Step-by-step working:**
1. Differences: 500, 550, 605. They are not equal, so it is not a fixed addition.
2. Ratios: 5,500/5,000 = 1.1, 6,050/5,500 = 1.1, 6,655/6,050 = 1.1. Constant ratio.
3. Each month is 10% above the last.
4. 6,655 x 1.1 = 6,655 + 665.5 = 7,320.5.
**Fast method (30 seconds):** 10% of 6,655 is 665.5 (move the decimal one place). Add it on.
**Check:** 5,500 / 5,000 = 1.1; 6,050 / 5,500 = 1.1; 6,655 / 6,050 = 1.1; 6,655 x 1.1 = 7,320.50, verified by script.
**Explain simply:**
- This is a geometric progression (GP): each term is the previous one times a fixed ratio.
- The differences also grow by 10% (500, 550, 605), which is a hint.
**Likely follow-ups:** Month 6? 7,320.5 x 1.1 = Rs 8,052.55. If the growth were a fixed Rs 500 each month? That would be an AP: month 5 = Rs 7,000 (but the data shows 550 and 605, so no).
**Common mistakes / traps:** Adding the latest difference (605 + 55 = 660 gives 7,315) or adding Rs 600, instead of using the ratio. 7,315 is the trap.

### Q31 ⭐⭐ 🟢 Find the 25th term of the series 4, 7, 10, 13, ...
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** AP nth term formula.
**Say this in the interview:** It is an arithmetic progression with first term 4 and common difference 3, so term n = 4 + (n - 1) x 3. The 25th term is 76.
**Answer:** **76**
**Step-by-step working:**
1. Differences: 7 - 4 = 3, 10 - 7 = 3, 13 - 10 = 3: constant.
2. nth term = first term + (n - 1) x difference.
3. 25th term = 4 + 24 x 3 = 4 + 72 = 76.
**Fast method (30 seconds):** Shortcut: the rule is 3n + 1 (difference times n plus an offset: 3 x 1 + 1 = 4). 3 x 25 + 1 = 76.
**Check:** Term 25 = 4 + 24 x 3 = 76; also 3 x 25 + 1 = 76, verified by script.
**Explain simply:**
- An arithmetic progression (AP) adds the same number each step.
- You take (n - 1) steps to reach term n, because the first term needs no steps.
**Likely follow-ups:** 50th term? 4 + 49 x 3 = 151. Sum of first 25 terms? 25/2 x (4 + 76) = 1,000.
**Common mistakes / traps:** Using 25 x 3 + 4 = 79, forgetting that only 24 steps are taken. 79 is the trap.

### Q32 ⭐⭐ 🟢 How many terms are there in the series 2, 4, 8, 16, ..., 1024?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** GP term counting.
**Say this in the interview:** This is a doubling series: term k is 2^k. Since 1,024 = 2^10, there are 10 terms.
**Answer:** **10 terms**
**Step-by-step working:**
1. Each term is double the one before, so term k = 2^k.
2. Powers: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1,024.
3. Count them: 10.
**Fast method (30 seconds):** Know 2^10 = 1,024 by heart (the famous 'kilobyte' number). The power equals the number of terms when the series starts at 2^1.
**Check:** 2^10 = 1,024 (2 x 2 x ... ten times), and 2^1 = 2 is the first term, so 10 terms; listed in a script.
**Explain simply:**
- A geometric progression (GP) multiplies by a fixed ratio (here 2).
- If the first term is 2 and the ratio 2, term n = 2 x 2^(n-1) = 2^n.
**Likely follow-ups:** Terms in 3, 9, 27, ..., 729? 3^6 = 729, so 6 terms. If the series began at 1 (1, 2, 4...1024)? 11 terms.
**Common mistakes / traps:** Dividing 1,024 by 2 (512 terms) as if it were an AP, or answering 9 by confusing 2^10 with the number of doublings.

### Q33 ⭐⭐ 🟢 Find the square root of 5,929 without a calculator.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Mental square-root estimation.
**Say this in the interview:** The root is between 70 and 80 and ends in 3 or 7; comparing with 75^2 = 5,625 picks 77.
**Answer:** **77**
**Step-by-step working:**
1. 70 x 70 = 4,900 and 80 x 80 = 6,400. So the root is between 70 and 80.
2. The last digit is 9. Squares ending in 9 come from numbers ending in 3 or 7 (3 x 3 = 9, 7 x 7 = 49).
3. Candidates: 73 and 77.
4. Compare with 75^2 = 5,625. 5,929 is above this, so the root is the larger one: 77.
5. Verify: 77 x 77 = 5,390 + 539 = 5,929.
**Fast method (30 seconds):** Bracket with tens, use the last digit for the units, then use the midpoint (75^2 = 5,625) to choose.
**Check:** 77 x 77 = 5,929 (77 x 70 = 5,390; 77 x 7 = 539; 5,390 + 539 = 5,929), verified by script.
**Explain simply:**
- The square root is the number that multiplied by itself gives the original.
- The last digit of a square limits the possible last digits of the root.
**Likely follow-ups:** Square root of 4,761? Between 60 and 70, ends in 1, so 61 or 69; 65^2 = 4,225 lower, so 69. Square root of 7,921? 89.
**Common mistakes / traps:** Picking 73 without the midpoint check. 73^2 = 5,329.

### Q34 ⭐⭐ 🟢 What does the Excel formula =MOD(5346, 9) return, and how would you use MOD to test divisibility across a column of employee IDs?
**Asked at:** commonly asked (no company-specific report found); Excel MOD is an analyst-flavoured gap-fill, not sourced to a company.
**What the interviewer is checking:** Excel MOD and divisibility tests.
**Say this in the interview:** MOD returns the remainder after division. 5,346 divided by 9 leaves nothing, so the result is 0. To test a column, I use =MOD(A2, n)=0 and filter for TRUE.
**Answer:** **0** (5,346 is exactly divisible by 9)
**Step-by-step working:**
1. =MOD(number, divisor) gives the remainder.
2. 9 x 594 = 5,346, so remainder = 0.
3. Test by digit sum: 5 + 3 + 4 + 6 = 18, and 18 is divisible by 9.
4. For a column of employee IDs in A2:A100, put in B2: =MOD(A2, 5)=0 and fill down. TRUE means the ID is divisible by 5. Use =IF(MOD(A2,5)=0,"Yes","No") for words.
**Fast method (30 seconds):** Rule for 9: a number is divisible by 9 if its digit sum is divisible by 9 (remainder of the digit sum gives the remainder).
**Check:** Digit sum of 5,346 = 5 + 3 + 4 + 6 = 18, which is a multiple of 9, so remainder 0; 9 x 594 = 5,346, verified by script.
**Explain simply:**
- Remainder is what is left over after dividing as many whole times as possible.
- Equal to 0 means exactly divisible, which is how MOD is used in checks such as every 5th row or even/odd IDs (MOD(id, 2)).
- The result keeps the sign of the divisor in Excel.
**Likely follow-ups:** MOD(5347, 9)? 1. How do I highlight every 3rd employee? =MOD(ROW(),3)=0 in conditional formatting.
**Common mistakes / traps:** Writing =MOD(A2,5) alone (gives remainders, not a test) or swapping the arguments: MOD(9, 5346) = 9.

### Q35 ⭐⭐ 🟡 Find the next number in the series 1, 3, 7, 13, 21, 31, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Difference-of-differences pattern.
**Say this in the interview:** The differences are 2, 4, 6, 8, 10, growing by 2 each time, so the next difference is 12 and the next term is 31 + 12 = 43.
**Answer:** **43**
**Step-by-step working:**
1. Differences: 3 - 1 = 2, 7 - 3 = 4, 13 - 7 = 6, 21 - 13 = 8, 31 - 21 = 10.
2. The differences themselves go up by 2: next difference 12.
3. 31 + 12 = 43.
**Fast method (30 seconds):** Second-level difference is constant (2); extend the difference list by one.
**Check:** Each term = n x n - n + 1 (n = 7 gives 49 - 7 + 1 = 43), verified by script.
**Explain simply:**
- If first differences are not constant, take differences of differences.
- A constant second difference means a quadratic pattern (involving n squared).
**Likely follow-ups:** Next after 43? 43 + 14 = 57. Rule check: n = 6 gives 36 - 6 + 1 = 31, good.
**Common mistakes / traps:** Adding 10 again (41) because you stop at the first differences.

### Q36 ⭐⭐ 🟡 Find the next number in the series 2, 12, 30, 56, 90, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Product pattern.
**Say this in the interview:** The terms are products of consecutive odd and even numbers: 1x2, 3x4, 5x6, 7x8, 9x10. The next is 11 x 12 = 132.
**Answer:** **132**
**Step-by-step working:**
1. 2 = 1 x 2, 12 = 3 x 4, 30 = 5 x 6, 56 = 7 x 8, 90 = 9 x 10.
2. Next pair: 11 and 12.
3. 11 x 12 = 132.
**Fast method (30 seconds):** Check by differences: 10, 18, 26, 34 (up by 8), so the next difference is 42, and 90 + 42 = 132.
**Check:** Each term = (2n - 1) x 2n: 1x2, 3x4, 5x6, 7x8, 9x10, so the next is 11x12 = 132; differences 10, 18, 26, 34, 42 also give 90 + 42 = 132, verified by script.
**Explain simply:**
- Two routes agree: factor pattern and difference pattern.
- When terms look like products of nearby numbers, try factor pairs.
**Likely follow-ups:** Next after 132? 13 x 14 = 182. If the first term was 6 (2x3, 4x5, 6x7)? Next 8x9 = 72.
**Common mistakes / traps:** Not trying factor pairs and guessing from differences alone, which needs a second level of differences.

### Q37 ⭐⭐ 🟡 Find the next number in the series 6, 11, 21, 36, 56, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Growing-difference series.
**Say this in the interview:** The differences are 5, 10, 15, 20, so the next is 25. The next term is 56 + 25 = 81.
**Answer:** **81**
**Step-by-step working:**
1. 11 - 6 = 5, 21 - 11 = 10, 36 - 21 = 15, 56 - 36 = 20.
2. These increase by 5 each time, so the next difference is 25.
3. 56 + 25 = 81.
**Fast method (30 seconds):** The differences are multiples of 5 (5 x 1, 5 x 2, 5 x 3, ...): quick to see.
**Check:** Differences 5, 10, 15, 20, 25 add up: 6 + 75 = 81, verified by script.
**Explain simply:**
- The first differences form an arithmetic progression, giving a quadratic-type series.
- This is a triangular-number pattern scaled by 5: 6 + 5 x (1 + 2 + ... ).
**Likely follow-ups:** Next term after 81? 81 + 30 = 111.
**Common mistakes / traps:** Adding 20 again (76) or adding 5 (61).

### Q38 ⭐⭐ 🟡 Find the next number in the series 2, 10, 4, 20, 6, 30, 8, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Alternating series.
**Say this in the interview:** This is two series woven together. The 1st, 3rd, 5th, 7th terms are 2, 4, 6, 8. The 2nd, 4th, 6th terms are 10, 20, 30. The 8th term is 40.
**Answer:** **40**
**Step-by-step working:**
1. Split the odd places: 2, 4, 6, 8 (adding 2 each).
2. Split the even places: 10, 20, 30, ? (adding 10 each).
3. The question asks for position 8, which belongs to the second series.
4. 30 + 10 = 40.
**Fast method (30 seconds):** If the series zig-zags (small, big, small, big), split it into two.
**Check:** Odd positions 2, 4, 6, 8 (+2); even positions 10, 20, 30, next 40; verified by script.
**Explain simply:**
- An alternating series is two separate patterns shared across odd and even positions.
- Check which position you need: the ? is the 8th term, an even position.
**Likely follow-ups:** The 9th term? The first series continues (8 + 2), giving 10.
**Common mistakes / traps:** Continuing the first series instead (answering 10) because you forgot which series the 8th place belongs to. 10 is the trap.

### Q39 ⭐⭐ 🟡 Find the next number in the series 2, 5, 11, 23, 47, ?
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Multiply-and-add series.
**Say this in the interview:** Each term is double the previous plus 1. 47 x 2 + 1 = 95.
**Answer:** **95**
**Step-by-step working:**
1. 2 x 2 + 1 = 5.
2. 5 x 2 + 1 = 11.
3. 11 x 2 + 1 = 23.
4. 23 x 2 + 1 = 47.
5. 47 x 2 + 1 = 94 + 1 = 95.
**Fast method (30 seconds):** Differences are 3, 6, 12, 24, which double: next 48, 47 + 48 = 95. Doubling differences signal a x2 rule.
**Check:** 2 x 2 + 1 = 5; 5 x 2 + 1 = 11; 11 x 2 + 1 = 23; 23 x 2 + 1 = 47; 47 x 2 + 1 = 95, verified by script.
**Explain simply:**
- The rule has two parts: multiply by 2 and add 1.
- If differences double, the series is multiply-and-add.
**Likely follow-ups:** Next after 95? 191. If the rule was x2 - 1 starting from 2? 3, 5, 9, 17.
**Common mistakes / traps:** Using only doubling (94) and forgetting the + 1; 94 is the trap.

### Q40 ⭐⭐ 🟡 Find the wrong number in the series 2, 5, 10, 17, 26, 37, 50, 64, 82.
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Wrong-term series.
**Say this in the interview:** Each term is a perfect square plus 1 (1+1, 4+1, 9+1, ...). The 8th term should be 8^2 + 1 = 65, so 64 is the wrong number.
**Answer:** **64** (it should be 65)
**Step-by-step working:**
1. Write the squares: 1, 4, 9, 16, 25, 36, 49, 64, 81.
2. Add 1 to each: 2, 5, 10, 17, 26, 37, 50, 65, 82.
3. Compare: the 8th term is 65 but the series shows 64.
4. Everything else matches, so 64 is wrong.
**Fast method (30 seconds):** The differences should be 3, 5, 7, 9, 11, 13, 15, 17. From 50, adding 15 gives 65.
**Check:** Rule n^2 + 1: 2, 5, 10, 17, 26, 37, 50, 65, 82; the 8th term should be 65, not 64, verified by script.
**Explain simply:**
- A wrong-number question has one term that breaks an otherwise clean rule.
- Find the rule from the first few terms, then check each one.
- Note that 82 matches the rule, which confirms 64 is the only fault.
**Likely follow-ups:** Wrong number in 1, 4, 9, 16, 24, 36? 24 (should be 25). Wrong number in 3, 6, 12, 24, 40, 96? 40 (should be 48).
**Common mistakes / traps:** Picking 82 because the end looks unusual, or answering 65 (the correct value, not the wrong number).

### Q41 ⭐⭐ 🟡 Find the wrong number in the series 3, 7, 15, 31, 63, 127, 256.
**Asked at:** Number-series items are a standard part of service-company online aptitude rounds (prep sites such as FACE Prep claim 5-8 per Infosys paper; unverified); no company-specific report of this exact item found.
**What the interviewer is checking:** Wrong-term series.
**Say this in the interview:** Each term is double the previous plus 1 (or 2^n - 1). Following 127 the term should be 255, so 256 is wrong.
**Answer:** **256** (it should be 255)
**Step-by-step working:**
1. 3 x 2 + 1 = 7.
2. 7 x 2 + 1 = 15.
3. 15 x 2 + 1 = 31.
4. 31 x 2 + 1 = 63.
5. 63 x 2 + 1 = 127.
6. 127 x 2 + 1 = 255, but 256 is given, so 256 is wrong.
**Fast method (30 seconds):** Every term must be odd (double plus one). 256 is even, so it stands out immediately.
**Check:** Rule 2^n - 1: 3, 7, 15, 31, 63, 127, 255. The last term should be 255, not 256, verified by script.
**Explain simply:**
- Parity (odd or even) is a quick filter: all other terms are odd.
- 2^n - 1 values are 1 less than powers of 2.
**Likely follow-ups:** Wrong number in 2, 6, 14, 30, 62, 125? 125 (should be 126). Note 255 + 256 = 511 is the next.
**Common mistakes / traps:** Choosing 127 because it looks large, or trusting 256 because it is a well-known power of 2.

### Q42 ⭐⭐ 🟡 What is the smallest 4-digit number exactly divisible by 12, 15 and 18?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** LCM and ceiling to a range.
**Say this in the interview:** Find the LCM (lowest common multiple) of 12, 15 and 18, which is 180, then take the first multiple of 180 that reaches 1,000.
**Answer:** **1,080**
**Step-by-step working:**
1. Prime factors: 12 = 2 x 2 x 3, 15 = 3 x 5, 18 = 2 x 3 x 3.
2. LCM uses the highest power of each prime: 2^2 x 3^2 x 5 = 4 x 9 x 5 = 180.
3. Multiples of 180: 180, 360, 540, 720, 900, 1,080.
4. 900 is 3-digit; the first 4-digit multiple is 1,080 (180 x 6).
**Fast method (30 seconds):** 1,000 / 180 = 5.55, so round up to 6; 6 x 180 = 1,080.
**Check:** 1,080 / 12 = 90, / 15 = 72, / 18 = 60; 1,080 - 180 = 900, which has 3 digits, verified by script.
**Explain simply:**
- A number divisible by several numbers must be a multiple of their LCM.
- LCM takes each prime at its highest count; multiplying all three (3,240) would be too big.
**Likely follow-ups:** Smallest 4-digit divisible by 12, 15, 20? LCM 60, answer 1,020. Largest 4-digit divisible by 180? 9,900.
**Common mistakes / traps:** Multiplying the numbers, or answering 1,000 or 1,008 (divisible by 12 and 18 but not 15).

### Q43 ⭐⭐ 🟡 How many numbers from 1 to 200 are divisible by 3 or 5?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Inclusion-exclusion counting.
**Say this in the interview:** I count multiples of 3, add multiples of 5, and subtract multiples of 15 so numbers divisible by both are not counted twice.
**Answer:** **93**
**Step-by-step working:**
1. Multiples of 3 up to 200: 200 / 3 = 66.67, so 66.
2. Multiples of 5: 200 / 5 = 40.
3. Multiples of both (15): 200 / 15 = 13.33, so 13.
4. Total = 66 + 40 - 13 = 93.
**Fast method (30 seconds):** Divide, drop the decimal, then add and subtract. This is the inclusion-exclusion rule (add the groups, subtract the overlap).
**Check:** By listing: 66 multiples of 3 plus 40 of 5 minus 13 of 15 = 93, verified by script.
**Explain simply:**
- Or means divisible by 3, or by 5, or by both.
- Overlap is counted twice in 66 + 40, so subtract it once.
- Both 3 and 5 means divisible by 15 (their LCM).
**Likely follow-ups:** 3 or 5 up to 100? 33 + 20 - 6 = 47. Neither 3 nor 5 up to 200? 200 - 93 = 107.
**Common mistakes / traps:** Answering 106 (66 + 40) and forgetting the overlap, or rounding 66.67 up to 67.

### Q44 ⭐⭐ 🟡 How many numbers from 1 to 500 are divisible by both 4 and 6?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** LCM versus product.
**Say this in the interview:** Divisible by both 4 and 6 means divisible by their LCM, 12. Count multiples of 12 up to 500: 500 / 12 = 41.67, so 41.
**Answer:** **41**
**Step-by-step working:**
1. LCM of 4 and 6: 4 = 2 x 2, 6 = 2 x 3, LCM = 2 x 2 x 3 = 12.
2. Numbers divisible by 12 up to 500: 500 / 12 = 41.67.
3. Take the whole part: 41.
4. Check: 12 x 41 = 492 and 12 x 42 = 504 which is over 500.
**Fast method (30 seconds):** Do not multiply 4 x 6 = 24; that gives 20 and is wrong, because 12 is also divisible by both.
**Check:** Multiples of 12: 12, 24, ..., 492 (41 numbers), next is 504 > 500, verified by script.
**Explain simply:**
- LCM = smallest number both divide into exactly.
- Divisible by both 4 and 6 means divisible by 12, not by 24.
**Likely follow-ups:** Divisible by both 6 and 8 up to 500? LCM 24, so 20. Divisible by 4 or 6? 125 + 83 - 41 = 167.
**Common mistakes / traps:** Using 24 (the product), giving 20. That is the trap.

### Q45 ⭐⭐ 🟡 How many numbers between 100 and 300 are divisible by 7?
**Asked at:** commonly asked (no company-specific report found); 'between' wording is a known ambiguity in these tests.
**What the interviewer is checking:** Counting multiples in a range.
**Say this in the interview:** Multiples of 7 form an AP: the first above 100 is 105, the last below 300 is 294, so (294 - 105) / 7 + 1 = 28.
**Answer:** **28**
**Step-by-step working:**
1. First multiple of 7 above 100: 7 x 14 = 98 (too low), 7 x 15 = 105.
2. Last multiple of 7 below 300: 7 x 42 = 294 (7 x 43 = 301 is too high).
3. Numbers are 7 x 15 up to 7 x 42.
4. Count = 42 - 15 + 1 = 28.
5. Check: (294 - 105) / 7 + 1 = 27 + 1 = 28.
**Fast method (30 seconds):** Count of multiples to 300 minus count to 100: 300 / 7 = 42 (whole part), 100 / 7 = 14, 42 - 14 = 28.
**Check:** Both ends: 100 and 300 are not multiples of 7, so including or excluding them gives the same count; 28 numbers listed by script.
**Explain simply:**
- Counting a list from first to last: (last - first) / step + 1.
- The +1 is needed because both end terms are counted.
- The wording is safe here because neither 100 nor 300 is a multiple of 7; with other limits you must state whether ends are included.
**Likely follow-ups:** Between 100 and 300 divisible by 5 (inclusive)? 41. Divisible by 7 between 1 and 100? 14.
**Common mistakes / traps:** Forgetting the + 1 (27), or including 98.

### Q46 ⭐⭐ 🟡 How many trailing zeros does 50! have?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Trailing zeros of factorial.
**Say this in the interview:** Each trailing zero needs one 10 = 2 x 5. There are always more 2s than 5s, so count the 5s in 50!. That is 10 + 2 = 12.
**Answer:** **12**
**Step-by-step working:**
1. A zero at the end appears for each factor of 10, and 10 = 2 x 5.
2. In 50! factors of 2 are plentiful, so the 5s decide.
3. Multiples of 5 up to 50: 50 / 5 = 10.
4. Multiples of 25 (which carry a second 5): 50 / 25 = 2.
5. Total 5s = 10 + 2 = 12, so 12 trailing zeros.
**Fast method (30 seconds):** Keep dividing by 5 and add the whole parts: 50 / 5 = 10, 10 / 5 = 2. 10 + 2 = 12.
**Check:** 5s: 10 + 2 = 12 factors of 5; there are more than enough 2s; verified by exact factorial in a script (12 trailing zeros).
**Explain simply:**
- n! (factorial) is 1 x 2 x 3 x ... x n.
- Trailing zeros are the zeros at the very end of the number.
- Numbers like 25 and 50 count extra because 25 = 5 x 5.
**Likely follow-ups:** Trailing zeros in 100!? 20 + 4 = 24. In 30!? 6 + 1 = 7.
**Common mistakes / traps:** Answering 10 (counting only multiples of 5 and forgetting 25 and 50).

### Q47 ⭐⭐ 🟡 How many factors does 360 have?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Number of divisors.
**Say this in the interview:** Prime factorise 360 = 2^3 x 3^2 x 5. Add 1 to each power and multiply: 4 x 3 x 2 = 24.
**Answer:** **24 factors**
**Step-by-step working:**
1. 360 = 36 x 10 = (2 x 2 x 3 x 3) x (2 x 5) = 2^3 x 3^2 x 5^1.
2. A factor takes 2 to the power 0 to 3 (4 choices), 3 to the power 0 to 2 (3 choices), 5 to the power 0 or 1 (2 choices).
3. Total = 4 x 3 x 2 = 24.
**Fast method (30 seconds):** Add 1 to each exponent and multiply: (3 + 1)(2 + 1)(1 + 1) = 24.
**Check:** Counted divisors of 360 one by one: 24, verified by script.
**Explain simply:**
- A factor (divisor) divides the number exactly, including 1 and the number itself.
- Each factor is a choice of how many of each prime to include.
- The same method shows only perfect squares have an odd number of factors.
**Likely follow-ups:** Factors of 100? 2^2 x 5^2, so 9. Sum of factors of 360? (1+2+4+8)(1+3+9)(1+5) = 15 x 13 x 6 = 1,170.
**Common mistakes / traps:** Counting only prime factors (3) or forgetting the +1 for the power 0 (2 x 2 x 1 = 4).

### Q48 ⭐⭐ 🟡 A two-digit number is 4 times the sum of its digits, and when its digits are reversed the number increases by 27. Find the number.
**Asked at:** commonly asked (no company-specific report found); digit puzzles are standard service-company aptitude material (prep-site claim, unverified).
**What the interviewer is checking:** Can you turn a word puzzle into two simple equations using place value.
**Say this in the interview:** "Write the number as 10a + b. The two conditions give b = 2a and b - a = 3, so a = 3, b = 6, and the number is 36."
**Answer:** **36**
**Step-by-step working:**
1. Let the tens digit be a and the units digit be b. The number is 10a + b.
2. Condition 1: 10a + b = 4(a + b), so 6a = 3b, so b = 2a.
3. Condition 2: reversed number 10b + a is 27 more: (10b + a) - (10a + b) = 9(b - a) = 27, so b - a = 3.
4. Put b = 2a: 2a - a = 3, so a = 3 and b = 6.
**Fast method (30 seconds):** Reversal always changes the number by 9 times the digit gap, so the gap is 27 / 9 = 3. Digits that differ by 3 and where one is double the other: 3 and 6. Tens digit is the smaller (number increases on reversal), so 36.
**Check:** 36 = 4 x (3 + 6) = 36; reversed 63 - 36 = 27. Verified by script (36 is the only two-digit solution).
**Explain simply:**
- Place value: a digit in the tens place is worth 10 times its face value, so 10a + b.
- Swapping digits changes the number by 9 x (difference of digits), a useful fact on its own.
**Likely follow-ups:** If the reversed number were 18 more? Gap = 2, and 10a + b = 4(a+b) forces b = 2a, so a = 2, b = 4: number 24 (24 = 4 x 6; 42 - 24 = 18).
**Common mistakes / traps:** Answering 63, the reversed number (check: 4 x 9 = 36, not 63). Also forgetting that "increases" means the units digit is the larger one.

### Q49 ⭐⭐ 🟡 A number leaves a remainder of 29 when divided by 56. What is the remainder when the same number is divided by 8?
**Asked at:** commonly asked (no company-specific report found); remainder questions are in every prep-site syllabus (unverified).
**What the interviewer is checking:** Whether you know that a remainder carries over to a divisor that is a factor of the original one.
**Say this in the interview:** "56 is a multiple of 8, so the number is 56k + 29, and 56k is clean for 8. The remainder is just 29 divided by 8, which leaves 5."
**Answer:** **5**
**Step-by-step working:**
1. Write the number as N = 56k + 29 for some whole number k.
2. 56 = 8 x 7, so 56k is exactly divisible by 8.
3. So the remainder of N by 8 is the remainder of 29 by 8.
4. 29 = 3 x 8 + 5, so the remainder is 5.
**Fast method (30 seconds):** If the new divisor divides the old one, reduce the old remainder by the new divisor. Works here because 8 divides 56.
**Check:** Take k = 1: N = 85, and 85 = 10 x 8 + 5. Verified by script for many values of k (always 5).
**Explain simply:**
- Dividend = divisor x quotient + remainder; this is the only formula you need.
- The trick only works if the new divisor is a factor of the old one (8 divides 56). It would fail for 9.
**Likely follow-ups:** Same number divided by 7? 56 is a multiple of 7, and 29 = 4 x 7 + 1, so 1.
**Common mistakes / traps:** Answering 29 (not reduced), or dividing 29 by 56 again. Remember a remainder must be smaller than the divisor.

### Q50 ⭐⭐ 🟡 What is the remainder when 123,456 is divided by 11?
**Asked at:** commonly asked (no company-specific report found); divisibility rules are standard TCS/Infosys-style syllabus items (prep-site claim, unverified).
**What the interviewer is checking:** Do you know the divisibility rule for 11 instead of doing long division.
**Say this in the interview:** "Alternate plus and minus the digits from the right: 6 - 5 + 4 - 3 + 2 - 1 = 3. That is the remainder, 3."
**Answer:** **3**
**Step-by-step working:**
1. Write digits from the right: 6, 5, 4, 3, 2, 1.
2. Alternate signs: +6 - 5 + 4 - 3 + 2 - 1.
3. Add up: 6 - 5 = 1; 1 + 4 = 5; 5 - 3 = 2; 2 + 2 = 4; 4 - 1 = 3.
4. The result 3 is between 0 and 10, so it is the remainder.
**Fast method (30 seconds):** The alternating sum above is the whole method. If the sum is negative, add 11 until it is between 0 and 10.
**Check:** 11 x 11,223 = 123,453, and 123,456 - 123,453 = 3. Verified by script.
**Explain simply:**
- Powers of 10 leave remainder 1, then -1, then 1, -1 when divided by 11, which is why signs alternate.
- If the alternating sum is 0 or a multiple of 11, the number is divisible by 11.
**Likely follow-ups:** Is 918,082 divisible by 11? 2 - 8 + 0 - 8 + 1 - 9 = -22, a multiple of 11, so yes.
**Common mistakes / traps:** Starting the signs from the left (this can flip the sign of the result, so you get 11 minus the true remainder); forgetting to add 11 to a negative result.

### Q51 ⭐⭐ 🟡 What is the smallest number that must be added to 5,000 to make it exactly divisible by 13?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Remainder thinking: how far is the number from the next multiple.
**Say this in the interview:** "Divide 5,000 by 13, find the remainder 8, and add the gap 13 - 8 = 5."
**Answer:** **5**
**Step-by-step working:**
1. 13 x 384 = 4,992.
2. 5,000 - 4,992 = 8, so the remainder is 8.
3. Next multiple is 13 x 385 = 5,005.
4. Number to add = 5,005 - 5,000 = 5 (same as 13 - 8).
**Fast method (30 seconds):** Add = divisor - remainder (if remainder is not 0). To subtract instead, subtract the remainder itself.
**Check:** 5,005 / 13 = 385 exactly. Verified by script.
**Explain simply:**
- The remainder tells how far you are above the last multiple; the gap to the next is divisor minus remainder.
**Likely follow-ups:** Smallest number to subtract from 5,000 for divisibility by 13? The remainder, 8 (gives 4,992).
**Common mistakes / traps:** Answering 8 (that is what to subtract, not add).

### Q52 ⭐⭐ 🟡 What is the smallest number that must be subtracted from 1,000 to make it a perfect square?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing squares near 1,000 and picking the one below, not above.
**Say this in the interview:** "30 squared is 900 and 31 squared is 961, 32 squared is 1,024 which is too big. So the nearest square below is 961, and I subtract 39."
**Answer:** **39**
**Step-by-step working:**
1. 31 x 31 = 961.
2. 32 x 32 = 1,024, which is above 1,000, so it cannot be reached by subtracting.
3. 1,000 - 961 = 39.
**Fast method (30 seconds):** Take the square root approximately: root of 1,000 is about 31.6. Round down to 31, square it (961), subtract.
**Check:** 1,000 - 39 = 961 = 31 squared. Verified by script.
**Explain simply:**
- A perfect square is a whole number times itself (like 961 = 31 x 31).
- Subtracting means we go down to the closest square below.
**Likely follow-ups:** Smallest number to add to 1,000 for a perfect square? 1,024 - 1,000 = 24.
**Common mistakes / traps:** Using 1,024 and answering 24, which is the "add" version.

### Q53 ⭐⭐ 🟡 An employee's monthly salary is Rs 30,000 in month 1 and rises by a fixed Rs 2,500 every month. What is the salary in month 12, and the total paid over the 12 months?
**Asked at:** commonly asked (no company-specific report found); a business-flavoured arithmetic progression (gap-fill question, not from a source).
**What the interviewer is checking:** Arithmetic progression: nth term and sum.
**Say this in the interview:** "It is an arithmetic progression, first term 30,000, difference 2,500. Month 12 is 30,000 + 11 x 2,500 = 57,500, and total is 12 x average of first and last = 12 x 43,750 = Rs 5,25,000."
**Answer:** **Month 12 salary: Rs 57,500; total over 12 months: Rs 5,25,000 (525,000).**
**Step-by-step working:**
1. nth term = first + (n - 1) x difference.
2. Month 12 = 30,000 + 11 x 2,500 = 30,000 + 27,500 = 57,500.
3. Sum = n x (first + last) / 2 = 12 x (30,000 + 57,500) / 2.
4. 87,500 / 2 = 43,750; 12 x 43,750 = 525,000.
**Fast method (30 seconds):** Total = number of months x average salary; in a steady rise the average is the midpoint of first and last.
**Check:** Adding all 12 salaries one by one in a script gives 525,000. Hand check: months 6 and 7 are 42,500 and 45,000, average 43,750, and 43,750 x 12 = 525,000.
**Explain simply:**
- Arithmetic progression (AP): each term is the previous plus a fixed amount.
- Counting trap: month 12 has 11 raises, not 12.
**Likely follow-ups:** If the raise were Rs 2,000? Month 12 = 52,000; total = 12 x 41,000 = 4,92,000.
**Common mistakes / traps:** Using 12 raises (giving 60,000), or multiplying 12 by the last salary.

### Q54 ⭐⭐ 🟡 Why is the product of any three consecutive integers always divisible by 6?
**Asked at:** commonly asked (no company-specific report found); a classic number-theory reasoning question.
**What the interviewer is checking:** Can you justify a general claim, not just test examples.
**Say this in the interview:** "Among any three consecutive integers, at least one is even and exactly one is a multiple of 3. Since 2 and 3 share no factor, the product is divisible by 2 x 3 = 6."
**Answer:** **Because the product always contains a factor of 2 and a factor of 3.**
**Step-by-step working:**
1. Take n, n + 1, n + 2.
2. Even numbers come every 2nd number, so at least one of the three is even: product divisible by 2.
3. Multiples of 3 come every 3rd number, so exactly one of the three is a multiple of 3: product divisible by 3.
4. 2 and 3 have no common factor (they are coprime), so the product is divisible by 2 x 3 = 6.
**Check:** Examples: 1 x 2 x 3 = 6; 4 x 5 x 6 = 120 = 6 x 20; 7 x 8 x 9 = 504 = 6 x 84. Verified by script for n from 1 to 1,000.
**Explain simply:**
- Coprime means the two numbers share no factor other than 1; if a number is divisible by both, it is divisible by their product.
- The same idea shows that four consecutive integers give a multiple of 24.
**Likely follow-ups:** Is the product of 3 consecutive integers always divisible by 12? No: 1 x 2 x 3 = 6.
**Common mistakes / traps:** Just listing examples (not a proof), or claiming divisibility by 4 or 12.

### Q55 ⭐ 🟢 Convert the binary number 1101 to decimal and the decimal number 45 to binary.
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Understanding of place value in base 2.
**Say this in the interview:** "Binary place values are 1, 2, 4, 8, 16, 32. 1101 is 8 + 4 + 1 = 13. For 45, divide repeatedly by 2 and read remainders upward: 101101."
**Answer:** **1101 (binary) = 13 (decimal); 45 (decimal) = 101101 (binary).**
**Step-by-step working:**
1. Binary to decimal: digits 1, 1, 0, 1 have place values 8, 4, 2, 1.
2. 1 x 8 + 1 x 4 + 0 x 2 + 1 x 1 = 13.
3. Decimal to binary: 45 / 2 = 22 r 1; 22 / 2 = 11 r 0; 11 / 2 = 5 r 1; 5 / 2 = 2 r 1; 2 / 2 = 1 r 0; 1 / 2 = 0 r 1.
4. Read remainders from last to first: 1 0 1 1 0 1.
**Fast method (30 seconds):** Subtract the biggest power of 2 each time: 45 = 32 + 8 + 4 + 1, so put 1s at 32, 8, 4, 1 and 0s at 16 and 2: 101101.
**Check:** 32 + 0 + 8 + 4 + 0 + 1 = 45. Verified by script.
**Explain simply:**
- Binary uses only 0 and 1; each place is worth double the one on its right.
**Likely follow-ups:** Binary of 20? 16 + 4 = 10100.
**Common mistakes / traps:** Reading the remainders top to bottom instead of bottom to top. For 20 the correct answer is 10100, while the wrong order gives 00101.

### Q56 ⭐ 🟢 Simplify sqrt(50) + sqrt(18) and state whether the result is rational or irrational.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Pulling perfect squares out of roots and spotting like terms.
**Say this in the interview:** "sqrt(50) is 5 sqrt(2) and sqrt(18) is 3 sqrt(2). Together 8 sqrt(2), which is irrational."
**Answer:** **8 sqrt(2) (about 11.31); irrational.**
**Step-by-step working:**
1. sqrt(50) = sqrt(25 x 2) = 5 sqrt(2).
2. sqrt(18) = sqrt(9 x 2) = 3 sqrt(2).
3. Add like terms: 5 sqrt(2) + 3 sqrt(2) = 8 sqrt(2).
4. sqrt(2) is irrational (it cannot be written as a fraction), and 8 times an irrational number stays irrational.
**Check:** 7.0711 + 4.2426 = 11.3137 and 8 x 1.4142 = 11.3137. Verified by script.
**Explain simply:**
- Rational means it can be written as a fraction of whole numbers; irrational means it cannot (decimals never end or repeat).
- Roots with the same inside number add like terms (like 5 apples + 3 apples).
**Likely follow-ups:** sqrt(50) x sqrt(18)? = 15 x 2 = 30, which is rational.
**Common mistakes / traps:** Writing sqrt(68) (you cannot add numbers under roots).

### Q57 ⭐ 🟢 Find the sum 5 + 10 + 15 + ... + 100.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Counting terms and using the AP sum formula.
**Say this in the interview:** "There are 20 terms. Sum = 20 x (5 + 100) / 2 = 1,050."
**Answer:** **1,050**
**Step-by-step working:**
1. Number of terms = (last - first) / step + 1 = (100 - 5) / 5 + 1 = 20.
2. Sum = n x (first + last) / 2 = 20 x 105 / 2.
3. 20 x 105 = 2,100; half is 1,050.
**Fast method (30 seconds):** Take 5 out: 5 x (1 + 2 + ... + 20) = 5 x 210 = 1,050.
**Check:** Pairing: 5 + 100 = 105, 10 + 95 = 105, and so on; 10 pairs x 105 = 1,050. Verified by script.
**Explain simply:**
- Pair the first and last terms; each pair gives the same total.
**Likely follow-ups:** Sum of 7 + 14 + ... + 98? 14 terms, 14 x 105 / 2 = 735.
**Common mistakes / traps:** Using 19 terms (forgetting the +1), or 100 terms.

### Q58 ⭐ 🟡 Find the next number in the series 4, 9, 25, 49, 121, 169, ?
**Asked at:** commonly asked (no company-specific report found); squares and primes are standard series types in prep material.
**What the interviewer is checking:** Spotting a two-layer pattern (squares of primes).
**Say this in the interview:** "These are squares of prime numbers: 2, 3, 5, 7, 11, 13. The next prime is 17, so 289."
**Answer:** **289**
**Step-by-step working:**
1. Take square roots: 2, 3, 5, 7, 11, 13.
2. These are consecutive primes (4 skipped, 6, 8, 9, 10, 12 are not prime).
3. The next prime after 13 is 17.
4. 17 x 17 = 289.
**Check:** Differences of terms do not follow a simple pattern, but the prime-square rule fits all six terms. Verified by script.
**Explain simply:**
- When first differences look random, check squares, cubes and primes.
- A prime has exactly two factors: 1 and itself.
**Likely follow-ups:** What comes after 289? 19 squared = 361.
**Common mistakes / traps:** Picking 225 (15 squared), because 15 is not prime.

### Q59 ⭐ 🟡 Find the sum 3 + 6 + 12 + ... for 10 terms.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Recognising a geometric series (doubling) and using the GP sum.
**Say this in the interview:** "Each term doubles, so ratio 2. Sum = 3 x (2^10 - 1) / (2 - 1) = 3 x 1,023 = 3,069."
**Answer:** **3,069**
**Step-by-step working:**
1. First term a = 3, ratio r = 2 (6 / 3 = 2, 12 / 6 = 2).
2. GP sum = a x (r^n - 1) / (r - 1).
3. 2^10 = 1,024, so 2^10 - 1 = 1,023.
4. Sum = 3 x 1,023 / 1 = 3,069.
**Fast method (30 seconds):** For ratio 2 the sum of n terms is first x (2^n - 1). Know that 2^10 = 1,024.
**Check:** Last term is 3 x 512 = 1,536; adding the 10 terms (3, 6, 12, 24, 48, 96, 192, 384, 768, 1,536) gives 3,069. Verified by script.
**Explain simply:**
- Geometric progression (GP): each term is the previous times a fixed ratio.
**Likely follow-ups:** What is the 10th term? 3 x 2^9 = 1,536.
**Common mistakes / traps:** Using 2^10 instead of 2^10 - 1, or treating it as an AP.

### Q60 ⭐ 🟡 Find the sum of the squares of the first 10 natural numbers.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing the sum-of-squares formula.
**Say this in the interview:** "n(n+1)(2n+1)/6 with n = 10: 10 x 11 x 21 / 6 = 385."
**Answer:** **385**
**Step-by-step working:**
1. Formula: n(n + 1)(2n + 1) / 6.
2. n = 10: 10 x 11 x 21 = 2,310.
3. 2,310 / 6 = 385.
**Check:** 1 + 4 + 9 + 16 + 25 + 36 + 49 + 64 + 81 + 100 = 385. Verified by script.
**Explain simply:**
- Natural numbers are 1, 2, 3, and so on.
- Related formulas: sum of first n numbers = n(n+1)/2 (55 here); sum of cubes = that, squared (3,025).
**Likely follow-ups:** Sum of squares of the first 20? 20 x 21 x 41 / 6 = 2,870.
**Common mistakes / traps:** Squaring the simple sum (3,025 is the sum of cubes, not squares).

### Q61 ⭐ 🟡 What is the sum of all the factors of 28? What is special about this number?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Listing factors systematically and knowing perfect numbers.
**Say this in the interview:** "Factors are 1, 2, 4, 7, 14, 28, total 56. Without 28 itself they add to 28, so it is a perfect number."
**Answer:** **56; 28 is a perfect number.**
**Step-by-step working:**
1. Factor pairs: 1 x 28, 2 x 14, 4 x 7.
2. Factors: 1, 2, 4, 7, 14, 28.
3. Sum = 1 + 2 + 4 + 7 + 14 + 28 = 56.
4. Excluding 28: 1 + 2 + 4 + 7 + 14 = 28, equal to the number itself.
**Fast method (30 seconds):** 28 = 2^2 x 7, so sum = (1 + 2 + 4)(1 + 7) = 7 x 8 = 56.
**Check:** Both routes give 56. Verified by script.
**Explain simply:**
- A perfect number equals the sum of its proper factors (all factors except itself). The first is 6, then 28, then 496.
**Likely follow-ups:** Sum of factors of 6? 12; and 1 + 2 + 3 = 6, so it is perfect.
**Common mistakes / traps:** Leaving out 1 or 28; answering 28 for the total.

### Q62 ⭐ 🟡 How many perfect squares are there from 101 to 999 inclusive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Boundary handling when counting.
**Say this in the interview:** "10 squared is 100, which is out. The first square in range is 11 squared = 121, the last is 31 squared = 961. That is 11 to 31, so 21 squares."
**Answer:** **21**
**Step-by-step working:**
1. 10^2 = 100, which is below 101, so excluded.
2. 11^2 = 121 is the first square in range.
3. 31^2 = 961 is in range; 32^2 = 1,024 is above 999.
4. Count of integers from 11 to 31 = 31 - 11 + 1 = 21.
**Check:** 31 squares up to 999 minus 10 squares up to 100 = 21. Verified by script.
**Explain simply:**
- Count the roots, not the squares: each whole number from 11 to 31 gives exactly one square in range.
**Likely follow-ups:** Squares from 100 to 999 inclusive? 22.
**Common mistakes / traps:** Answering 22 (including 100) or 20 (31 - 11).

### Q63 ⭐ 🟡 Find the LCM of the fractions 2/3, 4/9 and 5/6.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing the fraction rule: LCM of numerators over HCF of denominators.
**Say this in the interview:** "For fractions in lowest terms, LCM = LCM of numerators / HCF of denominators = 20 / 3."
**Answer:** **20/3 (about 6.67)**
**Step-by-step working:**
1. All three fractions are already in lowest terms.
2. Numerators 2, 4, 5: LCM = 20.
3. Denominators 3, 9, 6: HCF = 3.
4. LCM of fractions = 20 / 3.
**Check:** 20/3 divided by 2/3 = 10, by 4/9 = 15, by 5/6 = 8, all whole numbers, and 20/3 is the smallest such value. Verified by script.
**Explain simply:**
- LCM of fractions is the smallest number that each fraction fits into a whole number of times.
- HCF of fractions is HCF of numerators / LCM of denominators (here 1/18).
**Likely follow-ups:** HCF of the same fractions? 1/18.
**Common mistakes / traps:** Taking LCM of denominators too (18, giving 20/18). Also forgetting to reduce fractions first.

### Q64 ⭐ 🟡 In the grid below, each row follows the same rule. Find the missing number.

| A | B | C |
|---|---|---|
| 2 | 3 | 13 |
| 3 | 4 | 25 |
| 5 | 6 | ? |
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Testing a rule against every row, not just the first.
**Say this in the interview:** "C is A squared plus B squared. 4 + 9 = 13, 9 + 16 = 25, so 25 + 36 = 61."
**Answer:** **61**
**Step-by-step working:**
1. Row 1: 2 and 3 give 13. Try 2^2 + 3^2 = 4 + 9 = 13. Fits.
2. Row 2: 3^2 + 4^2 = 9 + 16 = 25. Fits.
3. Row 3: 5^2 + 6^2 = 25 + 36 = 61.
**Check:** The rule fits both complete rows; the alternative A x B + A + B (11, 19) does not, so only the squares rule works. Verified by script.
**Explain simply:**
- In grid puzzles, look for a rule combining the first two columns; test one idea on all known rows before trusting it.
**Likely follow-ups:** If the row were 4, 7, ? Then 16 + 49 = 65.
**Common mistakes / traps:** Settling on a rule after checking only one row. Note 2AB + 1 also fits all rows (13, 25, 61), because A squared plus B squared equals 2AB + 1 when B = A + 1; both rules give 61, so the answer is safe.

### Q65 ⭐ 🟡 What is the remainder when 3^50 is divided by 8?
**Asked at:** commonly asked (no company-specific report found); the cycle-of-remainders method appears in prep guides on remainders (unverified).
**What the interviewer is checking:** Finding a repeating cycle instead of computing a huge power.
**Say this in the interview:** "3 squared is 9, which leaves 1 when divided by 8. So 3^50 = (3^2)^25 leaves 1 to the power 25, which is 1."
**Answer:** **1**
**Step-by-step working:**
1. 3^1 = 3 leaves remainder 3.
2. 3^2 = 9 leaves remainder 1 (9 = 8 + 1).
3. So 3^50 = (3^2)^25 = 9^25.
4. 9 leaves remainder 1, so 9^25 leaves 1^25 = 1.
**Fast method (30 seconds):** Remainders cycle 3, 1, 3, 1. Even power gives 1, odd power gives 3. 50 is even, so 1.
**Check:** pow(3, 50, 8) = 1 by script.
**Explain simply:**
- Remainder of a product = product of the remainders (reduced again). So remainders can be raised to powers.
**Likely follow-ups:** 3^51 mod 8? 3 x 1 = 3.
**Common mistakes / traps:** Trying to compute 3^50 directly, or answering 3.

### Q66 ⭐ 🟡 What is the smallest 3-digit number that leaves a remainder of 3 when divided by 4, 5 and 6?
**Asked at:** commonly asked (no company-specific report found); LCM-with-same-remainder is a stock prep-site pattern (unverified).
**What the interviewer is checking:** Same remainder rule: LCM times k plus the remainder.
**Say this in the interview:** "LCM of 4, 5, 6 is 60. Numbers are 60k + 3. 63 is two digits, so the next is 123."
**Answer:** **123**
**Step-by-step working:**
1. LCM(4, 5, 6) = 60.
2. A number leaving 3 in each case is 60k + 3.
3. k = 1: 63 (only 2 digits). k = 2: 123 (3 digits).
**Check:** 123 = 4 x 30 + 3 = 5 x 24 + 3 = 6 x 20 + 3. Verified by script.
**Explain simply:**
- Subtract the common remainder and the number must be divisible by all divisors, so it is a multiple of the LCM.
**Likely follow-ups:** Largest 3-digit such number? 60 x 16 + 3 = 963.
**Common mistakes / traps:** Answering 63 (ignores "3-digit") or 60 (forgets to add 3).

### Q67 ⭐ 🟡 What does =MOD(-7, 3) return in Excel, and why is the result not -1?
**Asked at:** commonly asked (no company-specific report found); an analyst-flavoured gap-fill question.
**What the interviewer is checking:** Knowing Excel's MOD takes the sign of the divisor.
**Say this in the interview:** "It returns 2. Excel defines MOD so the result has the sign of the divisor: -7 = 3 x (-3) + 2."
**Answer:** **2**
**Step-by-step working:**
1. Excel's rule: MOD(n, d) = n - d x INT(n / d), where INT rounds down.
2. -7 / 3 = -2.33; rounding down gives -3.
3. MOD = -7 - 3 x (-3) = -7 + 9 = 2.
4. The remainder is never negative when the divisor is positive.
**Check:** 3 x (-3) + 2 = -7. Python's -7 % 3 also gives 2 (verified by script).
**Explain simply:**
- Rounding down (floor) on negatives goes away from zero, so the leftover is positive.
- -1 would come from rounding toward zero, which some languages do (the % operator in C or Java gives -1).
- HR use: rotating shifts with MOD to wrap around a week.
**Likely follow-ups:** =MOD(7, -3)? Sign follows the divisor: -2.
**Common mistakes / traps:** Answering -1 by dropping the sign.

### Q68 ⭐ 🟡 Is 0.999... equal to 1? Justify your answer.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Comfort with recurring decimals and a clean argument.
**Say this in the interview:** "Yes, exactly equal. Let x = 0.999..., then 10x = 9.999..., subtract: 9x = 9, so x = 1."
**Answer:** **Yes, 0.999... = 1 exactly.**
**Step-by-step working:**
1. Let x = 0.999... (nines going on forever).
2. Then 10x = 9.999...
3. Subtract: 10x - x = 9.999... - 0.999... = 9, so 9x = 9.
4. x = 1.
**Check:** 1/3 = 0.333..., and 3 x 0.333... = 0.999..., while 3 x (1/3) = 1.
**Explain simply:**
- There is no number between 0.999... and 1; two different numbers always have one between them, so they must be the same.
- Same reason 0.5 can be written 0.4999...: two spellings of one number.
**Likely follow-ups:** What fraction is 0.272727...? 27/99 = 3/11.
**Common mistakes / traps:** Saying "it gets close but never reaches 1"; that confuses the process of writing digits with the value.

### Q69 ⭐ 🔴 What is the remainder when 3^100 is divided by 7? (State Fermat's little theorem and use it.)
**Asked at:** commonly asked (no company-specific report found); Euler/Fermat for large powers appears in prep guides (unverified).
**What the interviewer is checking:** Applying Fermat's little theorem to reduce an exponent.
**Say this in the interview:** "If p is prime and does not divide a, then a^(p-1) leaves remainder 1 mod p. So 3^6 leaves 1 mod 7. 100 = 6 x 16 + 4, so 3^100 behaves like 3^4 = 81, which leaves 4."
**Answer:** **4**
**Step-by-step working:**
1. Fermat's little theorem: for a prime p and a not a multiple of p, a^(p-1) leaves remainder 1 when divided by p.
2. Here p = 7, a = 3, so 3^6 leaves remainder 1.
3. 100 = 6 x 16 + 4, so 3^100 = (3^6)^16 x 3^4.
4. (3^6)^16 leaves 1, so the remainder equals that of 3^4 = 81.
5. 81 = 7 x 11 + 4, so the remainder is 4.
**Check:** pow(3, 100, 7) = 4 by script. Also the cycle of 3^n mod 7 is 3, 2, 6, 4, 5, 1 (length 6), position 100 mod 6 = 4 gives 4.
**Explain simply:**
- Prime means divisible only by 1 and itself.
- The theorem lets you shrink the exponent by its remainder when divided by p - 1.
**Likely follow-ups:** 2^100 mod 7? 2^3 = 8 leaves 1; 100 = 3 x 33 + 1, so 2.
**Common mistakes / traps:** Dividing the exponent by 7 instead of 6.

### Q70 ⭐ 🔴 What are the last two digits of 7^2025?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Last two digits means remainder modulo 100; find the cycle.
**Say this in the interview:** "7^4 = 2,401, which ends in 01. So the cycle length is 4. 2025 leaves 1 when divided by 4, so the answer matches 7^1: last two digits 07."
**Answer:** **07**
**Step-by-step working:**
1. Last two digits = remainder when divided by 100.
2. 7^2 = 49; 7^4 = 49 x 49 = 2,401, remainder 1 mod 100.
3. 2025 = 4 x 506 + 1, so 7^2025 = (7^4)^506 x 7.
4. (7^4)^506 leaves 1, so the result leaves the same as 7, which is 07.
**Check:** pow(7, 2025, 100) = 7 by script.
**Explain simply:**
- Once a power ends in 01, powers repeat from there.
- Write single-digit results with a leading zero: 07.
**Likely follow-ups:** Last two digits of 7^2026? 7 x 7 = 49.
**Common mistakes / traps:** Answering 7 (should be shown as 07), or using the unit-digit cycle only, which gives the last digit but not the second-last.

