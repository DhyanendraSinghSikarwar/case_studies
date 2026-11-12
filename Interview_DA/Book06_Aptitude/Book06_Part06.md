# Book 6 — Aptitude & Business Maths | Part 6: Permutation, Combination, Probability (Aptitude Style) 🟢🟡🔴

**Target:** 60 questions | **Actual:** 69 questions
**Scope:** counting methods (permutations, combinations, circular and repeated-letter arrangements, selections) and classical aptitude probability (coins, dice, cards, balls, independent events), as seen in online assessments; interview-style probability/Bayes is in Book 5.

### Q1 ⭐⭐⭐ 🟢 What is the difference between a permutation and a combination, and how do you decide which one a question needs?
**Asked at:** commonly asked (no company-specific report found); permutations and combinations are listed under quantitative ability for TCS NQT, Wipro and Infosys style tests (prep-site claims, unverified).
**What the interviewer is checking:** Whether you know that order matters in a permutation and does not in a combination.
**Say this in the interview:** "A permutation counts arrangements where order matters; a combination counts selections where order does not. I ask: if I swap two chosen items, is it a different outcome? If yes, permutation; if no, combination."
**Answer:** **Permutation = order matters (nPr); combination = order does not matter (nCr).**
**Explain simply:**
- Permutation (arrangement): picking a President and a Secretary from 5 people. Ravi-President, Meena-Secretary differs from Meena-President, Ravi-Secretary.
- Combination (selection): picking a 2-person team from 5 people. Ravi and Meena is the same team either way.
- Decision test: do the chosen items get different roles, positions or ranks? Yes means permutation. Are they just a group? Yes means combination.
- Each combination hides several permutations: one group of r items can be ordered in r! ways, so nPr = nCr x r!.
**Worked example:** From 4 people A, B, C, D choose 2. Groups: AB, AC, AD, BC, BD, CD = 6 combinations. Arrangements: each group can be ordered 2 ways, so 6 x 2 = 12 permutations (4P2 = 12, 4C2 = 6).
**Check:** 4P2 = 4 x 3 = 12 and 4C2 = 12 / 2! = 6; verified by listing in a script.
**Likely follow-ups:**
- "Which is it for choosing 3 interview panellists from 7?" Combination, 7C3 = 35, because the panel has no ranking.
- "And for awarding Gold, Silver, Bronze to 3 of 7?" Permutation, 7P3 = 210.
**Common mistakes / traps:** Words like "arrange", "rank", "form a number", "assign posts" signal order; "select", "choose", "committee", "team" signal no order. The classic trap is using nCr when roles differ, giving a much smaller number.

### Q2 ⭐⭐⭐ 🟢 State the formulas for nPr and nCr and the relation between them.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether the formulas are memorised correctly and you see how they connect.
**Say this in the interview:** "nPr = n! / (n-r)! and nCr = n! / (r! (n-r)!). They are related by nPr = nCr x r!, because a combination ignores the r! orderings that a permutation counts."
**Answer:** **nPr = n! / (n-r)!; nCr = n! / (r! x (n-r)!); nPr = r! x nCr.**
**Explain simply:**
- n! (n factorial) means n x (n-1) x ... x 1. So 5! = 120.
- nPr: fill r ordered slots from n items: n x (n-1) x ... for r factors.
- nCr: take those ordered fills and divide by r!, since the order inside the group does not matter.
**Worked example:** 6P2 = 6 x 5 = 30. 6C2 = 30 / 2! = 15. Using the formula: 6! / (2! x 4!) = 720 / 48 = 15.
**Check:** 15 x 2! = 30 = 6P2; verified by script.
**Likely follow-ups:**
- "Fast way for 10C3?" 10 x 9 x 8 / (3 x 2 x 1) = 720 / 6 = 120.
- "What is nC1?" n, and nCn = 1.
**Common mistakes / traps:** Forgetting to divide by r!, or dividing by n! instead. Also writing 10C3 as 10 x 9 x 8 / 3 (dividing by 3 rather than 3!).

### Q3 ⭐⭐⭐ 🟢 How is the probability of an event defined, and what range of values can it take?
**Asked at:** commonly asked (no company-specific report found); basic probability is listed for Wipro, Mu Sigma and TCS style tests (prep-site claims, unverified).
**What the interviewer is checking:** Basic definition and the 0 to 1 range.
**Say this in the interview:** "Probability is favourable outcomes divided by total equally likely outcomes. It lies between 0 and 1: 0 for an impossible event, 1 for a certain one."
**Answer:** **P(E) = (number of favourable outcomes) / (total number of equally likely outcomes), and 0 <= P(E) <= 1.**
**Explain simply:**
- "Equally likely" matters: every outcome must have the same chance (a fair die, a fair coin).
- 0 means it can never happen; 1 means it always happens; 0.5 means a 50% chance. Multiply by 100 for a percentage.
- Favourable can never exceed total, so the fraction cannot exceed 1 or go negative.
- P(E) + P(not E) = 1.
**Worked example:** Of 40 employees in a team, 10 are in HR. A random pick is from HR with probability 10/40 = 1/4 = 0.25 = 25%.
**Check:** 10/40 = 0.25 and 0.25 + 0.75 (non-HR) = 1.
**Likely follow-ups:**
- "Probability of rolling a 7 on one die?" 0, impossible.
- "Can probability be 1.2 or -0.3?" No; check your count.
**Common mistakes / traps:** Counting outcomes that are not equally likely (for example treating "sum = 7" on two dice as one of 11 equal sums, when there are 36 equal pairs). Also giving odds (3 to 1) instead of probability.

### Q4 ⭐⭐⭐ 🟢 State the fundamental counting principle (the multiplication rule) and the addition rule, and when each applies.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can tell AND situations (multiply) from OR situations (add).
**Say this in the interview:** "If a task has steps that all must happen, I multiply the number of choices. If it can be done in one way OR another, mutually exclusive ways, I add."
**Answer:** **Multiplication rule: independent steps in sequence, total = m x n. Addition rule: mutually exclusive alternatives, total = m + n.**
**Explain simply:**
- Multiplication ("and then"): 3 shirts and 2 trousers give 3 x 2 = 6 outfits, because each shirt pairs with each trouser.
- Addition ("or"): travel by 3 bus routes or 2 train routes, but one journey only: 3 + 2 = 5 ways.
- Addition works only when the two options cannot happen together; if they overlap you must subtract the overlap.
**Worked example:** A PIN has 2 digits from 0-9, repeats allowed: 10 x 10 = 100. A person picks one candidate from 4 Analysts OR 3 Managers: 4 + 3 = 7.
**Check:** Listing 3 shirts x 2 trousers gives 6 pairs; verified by script.
**Likely follow-ups:**
- "Outfits if there are also 4 ties?" 3 x 2 x 4 = 24.
- "Multiples of 4 or 6 up to 50?" Overlap exists (multiples of 12), so add then subtract it (see Q26).
**Common mistakes / traps:** Adding when steps are sequential, or multiplying when options are alternatives. Key words: "and", "followed by" mean multiply; "or", "either" mean add.

### Q5 ⭐⭐⭐ 🟢 Why is the complement rule, P(at least one) = 1 - P(none), the standard shortcut for 'at least one' probability questions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you reach for the one-step shortcut instead of listing many cases.
**Say this in the interview:** "'At least one' covers every case except 'none'. Since all probabilities add to 1, P(at least one) = 1 minus P(none), and P(none) is a single easy product."
**Answer:** **Because "at least one" and "none" together cover all outcomes, P(at least one) = 1 - P(none), and P(none) is one simple calculation.**
**Explain simply:**
- Direct way: add P(exactly 1), P(exactly 2), ..., P(all). That is many terms.
- Complement way: only one case, "none", is left out. For independent trials, P(none) = (chance of failing once) multiplied n times.
- Worked example: 3 tosses of a coin. Direct: 7 of 8 outcomes have a head. Complement: P(no head) = (1/2)^3 = 1/8, so answer = 1 - 1/8 = 7/8.
**Check:** 7/8 + 1/8 = 1; verified by listing all 8 outcomes in a script.
**Likely follow-ups:**
- "Each of 4 recruiters independently has a 20% chance to close a vacancy; chance at least one does?" 1 - 0.8^4 = 1 - 0.4096 = 0.5904.
- "Does it work if trials are dependent?" Yes, but P(none) must use conditional probabilities.
**Common mistakes / traps:** Computing P(none) but forgetting the final "1 minus". Also using the shortcut for "exactly one", where it does not apply.

### Q6 ⭐⭐⭐ 🟢 Five candidates are shortlisted for three distinct posts (Analyst, Team Lead, Manager), and each person can get at most one post. In how many ways can the posts be filled?
**Asked at:** commonly asked (no company-specific report found); posts and ranking items are a standard permutation pattern in prep banks.
**What the interviewer is checking:** Recognising that distinct posts mean order matters.
**Say this in the interview:** "Posts are different, so this is a permutation: 5 choices for Analyst, 4 for Team Lead, 3 for Manager, which is 5P3 = 60."
**Answer:** **60 ways**
**Step-by-step working:**
1. Analyst post: any of 5 candidates = 5 choices.
2. Team Lead: one person is gone, so 4 choices.
3. Manager: 3 choices left.
4. Multiply: 5 x 4 x 3 = 60.
**Fast method (30 seconds):** 5P3 means "start at 5, multiply 3 numbers going down": 5 x 4 x 3.
**Check:** 5!/(5-3)! = 120/2 = 60; verified by script (enumerating all ordered triples).
**Explain simply:**
- Each post is a different role, so swapping two people changes the outcome.
- "At most one post each" means no repeats, so choices shrink at each step.
**Likely follow-ups:**
- "If any 3 of the 5 were simply shortlisted, no posts?" 5C3 = 10.
- "If one person may hold several posts?" 5 x 5 x 5 = 125.
**Common mistakes / traps:** Using 5C3 = 10 (ignores which post), or 5^3 = 125 (ignores the "at most one" rule).

### Q7 ⭐⭐⭐ 🟢 A committee of 3 members is to be chosen from 8 employees. In how many ways can this be done?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing combination when there are no roles.
**Say this in the interview:** "A committee has no ranking, so it is a combination: 8C3 = 8 x 7 x 6 / 6 = 56."
**Answer:** **56 ways**
**Step-by-step working:**
1. Order does not matter, so use 8C3.
2. 8C3 = (8 x 7 x 6) / (3 x 2 x 1).
3. Numerator = 336; denominator = 6.
4. 336 / 6 = 56.
**Fast method (30 seconds):** Write r numbers going down from n on top and r! below, then cancel: (8 x 7 x 6) / 6 = 8 x 7 = 56.
**Check:** 8P3 = 336 ordered picks, each group counted 3! = 6 times, so 336 / 6 = 56; verified by script.
**Explain simply:**
- nCr counts groups, not orderings.
- A committee of 3 named A, B, C is the same group as C, B, A.
**Likely follow-ups:**
- "Same committee, but one must be Chairperson?" Choose the group (56) then a chair (3): 168; or 8 x 7C2 = 8 x 21 = 168.
- "8C5?" Same as 8C3 = 56.
**Common mistakes / traps:** Answering 336 (the permutation 8P3).

### Q8 ⭐⭐⭐ 🟢 A fair coin is tossed twice. What is the probability of getting two heads?
**Asked at:** commonly asked (no company-specific report found); coin items are the usual starter in probability sections.
**What the interviewer is checking:** Listing the sample space and using independence.
**Say this in the interview:** "Two tosses give 4 equally likely outcomes, only HH is favourable, so 1/4. Or multiply: 1/2 x 1/2."
**Answer:** **1/4 (0.25, or 25%)**
**Step-by-step working:**
1. All outcomes: HH, HT, TH, TT = 4.
2. Favourable: HH only = 1.
3. Probability = 1/4.
**Fast method (30 seconds):** Tosses are independent, so multiply: 1/2 x 1/2 = 1/4.
**Check:** the four outcome probabilities 1/4 each add to 1; verified by script.
**Explain simply:**
- Independent events: one toss does not affect the next, so probabilities multiply.
- n tosses give 2^n outcomes.
**Likely follow-ups:**
- "Exactly one head in two tosses?" HT and TH = 2/4 = 1/2.
- "Four heads in four tosses?" (1/2)^4 = 1/16.
**Common mistakes / traps:** Thinking there are only 3 outcomes (0, 1 or 2 heads), which are not equally likely, giving 1/3.

### Q9 ⭐⭐⭐ 🟢 A fair six-sided die is rolled once. What is the probability that the number is a prime number?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing that 1 is not prime.
**Say this in the interview:** "Primes on a die are 2, 3 and 5, so 3 favourable out of 6, which is 1/2."
**Answer:** **1/2 (50%)**
**Step-by-step working:**
1. Sample space: 1, 2, 3, 4, 5, 6 = 6 outcomes.
2. A prime has exactly two factors, 1 and itself: 2, 3, 5.
3. 1 is not prime (only one factor); 4 and 6 are composite.
4. Probability = 3/6 = 1/2.
**Check:** the three non-primes are 1, 4, 6, so 3/6 + 3/6 = 1; verified by script.
**Explain simply:**
- Prime number: a number greater than 1 divisible only by 1 and itself.
- Fair die: each face has chance 1/6.
**Likely follow-ups:**
- "Prime on a die numbered 1 to 12?" Primes 2, 3, 5, 7, 11 = 5/12.
- "Even number?" 3/6 = 1/2.
**Common mistakes / traps:** Counting 1 as prime (answer 4/6 = 2/3).

### Q10 ⭐⭐⭐ 🟢 Two fair dice are rolled together. What is the probability that the sum is 7?
**Asked at:** commonly asked (no company-specific report found); sum-of-two-dice is the classic dice item in prep banks.
**What the interviewer is checking:** Using all 36 equally likely pairs, not 11 sums.
**Say this in the interview:** "There are 36 equally likely pairs, and 6 of them sum to 7, so 6/36 = 1/6."
**Answer:** **1/6**
**Step-by-step working:**
1. Total outcomes: 6 x 6 = 36 pairs.
2. Pairs summing to 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6.
3. Probability = 6/36 = 1/6.
**Fast method (30 seconds):** Whatever the first die shows, exactly one value on the second die makes 7. So the chance is 1/6. This is why 7 is the most likely sum.
**Check:** the counts of sums 2 to 12 are 1,2,3,4,5,6,5,4,3,2,1 and add to 36; verified by script.
**Explain simply:**
- The two dice are treated as different (first and second), so (1,6) and (6,1) are separate outcomes.
**Likely follow-ups:**
- "Sum of 4?" (1,3), (2,2), (3,1) = 3/36 = 1/12.
- "Sum of 12?" 1/36.
**Common mistakes / traps:** Using 11 possible sums as the denominator (answer 1/11), or counting (3,4) and (4,3) once.

### Q11 ⭐⭐⭐ 🟢 A bag has 5 red and 3 blue balls. One ball is drawn at random. What is the probability that it is red?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Favourable over total with balls as the equally likely items.
**Say this in the interview:** "8 balls in total, 5 red, so 5/8."
**Answer:** **5/8 (0.625, or 62.5%)**
**Step-by-step working:**
1. Total balls = 5 + 3 = 8.
2. Red balls = 5.
3. Probability = 5/8.
**Check:** P(blue) = 3/8 and 5/8 + 3/8 = 1; verified by script.
**Explain simply:**
- Each ball is equally likely to be drawn, so count balls, not colours.
- The total is the sum of all colours, not just the other colour.
**Likely follow-ups:**
- "Probability the ball is not red?" 3/8.
- "If 2 more blue balls are added?" Red = 5/10 = 1/2.
**Common mistakes / traps:** Dividing by 3 (the blue count), giving 5/3, which exceeds 1 and cannot be a probability.

### Q12 ⭐⭐⭐ 🟢 How many different arrangements can be made from the letters of the word DATA?
**Asked at:** commonly asked (no company-specific report found); repeated-letter arrangements are a standard pattern in prep banks.
**What the interviewer is checking:** Dividing by the factorial of repeated letters.
**Say this in the interview:** "DATA has 4 letters with A repeated twice, so 4! / 2! = 12."
**Answer:** **12 arrangements**
**Step-by-step working:**
1. If all 4 letters were different: 4! = 24.
2. The two A's look identical, so swapping them gives nothing new. Each real arrangement was counted 2! = 2 times.
3. Divide: 24 / 2 = 12.
**Fast method (30 seconds):** Total letters factorial over the factorial of each repeat: 4!/2! = 24/2 = 12.
**Check:** listing all distinct words (ADAT, ADTA, AADT, ...) gives 12; verified by script.
**Explain simply:**
- Repeated letters are indistinguishable, so we remove the duplicate counting.
- General rule: n! / (p! x q! x ...) where p, q are the counts of each repeated letter.
**Likely follow-ups:**
- "Arrangements of BANANA?" 6!/(3! x 2!) = 720/12 = 60.
- "DATA with the two A's at the ends?" A _ _ A: the middle 2 letters D, T can be arranged in 2 ways.
**Common mistakes / traps:** Answering 24 (4!) by ignoring the repeat.

### Q13 ⭐⭐⭐ 🟢 How many 4-digit PINs can be formed using the digits 1 to 9 if no digit may be repeated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Permutation without repetition, filling slots.
**Say this in the interview:** "Four slots: 9 choices, then 8, 7, 6, since no digit repeats. 9 x 8 x 7 x 6 = 3024."
**Answer:** **3024 PINs**
**Step-by-step working:**
1. First digit: 9 choices (digits 1 to 9).
2. Second digit: 8 left.
3. Third: 7 left.
4. Fourth: 6 left.
5. 9 x 8 = 72; 72 x 7 = 504; 504 x 6 = 3024.
**Fast method (30 seconds):** This is 9P4: four numbers going down from 9.
**Check:** 9!/5! = 362880/120 = 3024; verified by script.
**Explain simply:**
- Order matters (1234 is not 4321), so permutation.
- The digit 0 is not allowed here, so all 9 digits are valid in every slot.
**Likely follow-ups:**
- "If digits can repeat?" 9^4 = 6561.
- "If 0 is also allowed, no repeats?" 10P4 = 5040.
**Common mistakes / traps:** Using 9C4 = 126 (ignores order) or 9^4 (ignores the no-repeat rule).

### Q14 ⭐⭐⭐ 🟢 At a team meeting, each of the 10 people shakes hands exactly once with every other person. How many handshakes take place?
**Asked at:** commonly asked (no company-specific report found); handshake items are a standard combination pattern.
**What the interviewer is checking:** Seeing a handshake as an unordered pair.
**Say this in the interview:** "Each handshake is a pair of people and A-B is the same as B-A, so 10C2 = 45."
**Answer:** **45 handshakes**
**Step-by-step working:**
1. A handshake needs 2 people, order does not matter: 10C2.
2. 10C2 = (10 x 9) / (2 x 1) = 90 / 2 = 45.
**Fast method (30 seconds):** n(n-1)/2 = 10 x 9 / 2 = 45. Each of 10 people shakes 9 hands = 90, but every handshake is counted twice (once per person), so halve it.
**Check:** 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 = 45 (first person shakes 9, next new 8, and so on); verified by script.
**Explain simply:**
- Pair counting appears for handshakes, matches in a league, and lines between points.
**Likely follow-ups:**
- "20 people?" 20 x 19 / 2 = 190.
- "10 teams each play each other twice?" 45 x 2 = 90.
**Common mistakes / traps:** Answering 90 (counting each handshake twice).

### Q15 ⭐⭐⭐ 🟢 A fair coin is tossed three times. What is the probability of getting at least one head?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using the complement for "at least one".
**Say this in the interview:** "Easier to find no heads: all tails is 1/8. So at least one head is 1 - 1/8 = 7/8."
**Answer:** **7/8 (0.875, or 87.5%)**
**Step-by-step working:**
1. Total outcomes: 2 x 2 x 2 = 8.
2. "No head" means TTT only: 1 outcome, probability 1/8.
3. At least one head = 1 - 1/8 = 7/8.
**Check:** direct count: outcomes with 1, 2, 3 heads = 3 + 3 + 1 = 7 out of 8; verified by script.
**Explain simply:**
- Complement rule: P(at least one) = 1 - P(none) (see Q5).
**Likely follow-ups:**
- "At least one head in 5 tosses?" 1 - (1/2)^5 = 31/32.
- "Exactly two heads in 3 tosses?" 3/8.
**Common mistakes / traps:** Forgetting the "1 minus" and answering 1/8, or answering 1/2 by thinking only about one toss.

### Q16 ⭐⭐⭐ 🟢 How many 3-digit numbers can be formed using the digits 1, 2, 3, 4, 5 if no digit may be repeated?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Slot-filling with no repetition (each digit in a different position gives a different number).
**Say this in the interview:** "Hundreds place 5 choices, tens 4, units 3: 5 x 4 x 3 = 60."
**Answer:** **60 numbers**
**Step-by-step working:**
1. Hundreds digit: any of 5.
2. Tens digit: 4 remaining.
3. Units digit: 3 remaining.
4. 5 x 4 x 3 = 60.
**Fast method (30 seconds):** This is 5P3 = 60. No 0 among the digits, so no leading-zero problem.
**Check:** 5!/2! = 120/2 = 60; verified by script.
**Explain simply:**
- 123 and 321 are different numbers, so order matters.
**Likely follow-ups:**
- "How many are even?" Units digit 2 or 4 (2 ways), then 4 x 3 = 12: 24 numbers.
- "If repetition is allowed?" 5^3 = 125.
**Common mistakes / traps:** Using 5C3 = 10.

### Q17 ⭐⭐⭐ 🟡 How many distinct arrangements are possible from the letters of the word SALARY?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Spotting the repeated A before applying 6!.
**Say this in the interview:** "SALARY has 6 letters with A twice, so 6! / 2! = 360."
**Answer:** **360 arrangements**
**Step-by-step working:**
1. Letters: S, A, L, A, R, Y = 6; only A repeats (twice).
2. 6! = 720.
3. Divide by 2! = 2 for the repeated A: 720 / 2 = 360.
**Check:** verified by script (360 distinct permutations of the letters); also 6P6/2 = 360.
**Explain simply:**
- Same rule as Q12: divide by the factorial of each repeated letter's count.
**Likely follow-ups:**
- "Arrangements of ASSESS?" 6!/(4! x 1! x 1!) = 30.
- "SALARY starting with S?" Remaining 5 letters (A twice): 5!/2! = 60.
**Common mistakes / traps:** Answering 720 because the repeat was missed; the trap is that S-A-L-A-R-Y looks like six different letters at a glance.

### Q18 ⭐⭐⭐ 🟡 In how many ways can the letters of the word LEADER be arranged so that all the vowels stay together?
**Asked at:** commonly asked (no company-specific report found); "vowels together" is a standard restricted-arrangement pattern (prep-site claim).
**What the interviewer is checking:** The "glue" method plus handling repeated letters twice.
**Say this in the interview:** "I glue the vowels E, A, E into one block. Then there are 4 units, 4! = 24 ways, and inside the block the vowels can arrange in 3!/2! = 3 ways. 24 x 3 = 72."
**Answer:** **72 arrangements**
**Step-by-step working:**
1. LEADER has 6 letters: L, E, A, D, E, R. Vowels: E, A, E (3 of them, E repeated twice). Consonants: L, D, R.
2. Treat the vowels as one block. Units to arrange: L, D, R, [block] = 4 distinct units: 4! = 24.
3. Inside the block, arrange E, A, E: 3!/2! = 3 (EAE, EEA, AEE).
4. Multiply: 24 x 3 = 72.
**Check:** total arrangements of LEADER = 6!/2! = 360; brute-force count of those with vowels adjacent = 72; verified by script.
**Explain simply:**
- Gluing items turns "must stay together" into an ordinary arrangement of fewer units.
- Always multiply by the internal arrangements of the glued block, and remember the repeat adjustment there.
**Likely follow-ups:**
- "Vowels together in DESIGN?" Vowels E, I: 5! x 2! = 240.
- "LEADER with no restriction?" 360.
**Common mistakes / traps:** Using 3! = 6 inside the block (ignores the repeated E), giving 144; or forgetting the block's internal order, giving 24.

### Q19 ⭐⭐⭐ 🟡 Two cards are drawn one after the other, without replacement, from a well-shuffled pack of 52 cards. What is the probability that both are aces?
**Asked at:** commonly asked (no company-specific report found); card items are listed among typical probability styles (prep blogs).
**What the interviewer is checking:** Dependent events: the second draw changes after the first.
**Say this in the interview:** "First ace is 4/52. With one ace gone, second ace is 3/51. Multiply: 12/2652 = 1/221."
**Answer:** **1/221 (about 0.0045, or 0.45%)**
**Step-by-step working:**
1. A pack has 52 cards, 4 aces. P(first is ace) = 4/52 = 1/13.
2. No replacement: 51 cards left, 3 aces. P(second is ace) = 3/51 = 1/17.
3. Multiply: 1/13 x 1/17 = 1/221.
**Fast method (30 seconds):** Combination route: 4C2 / 52C2 = 6 / 1326 = 1/221.
**Check:** both routes give 1/221; verified by script (exact fractions).
**Explain simply:**
- Without replacement, the draws depend on each other, so use 3/51 not 4/52 for the second draw.
- Drawing 2 cards one after another without replacement has the same probability as drawing 2 together.
**Likely follow-ups:**
- "With replacement?" 4/52 x 4/52 = 1/169.
- "Both cards are hearts?" 13C2 / 52C2 = 78/1326 = 1/17.
**Common mistakes / traps:** Using 4/52 x 4/52 = 1/169 (that is the with-replacement answer).

### Q20 ⭐⭐⭐ 🟡 A bag has 4 red, 6 green and 5 yellow balls. Three balls are drawn together at random. What is the probability that all three are of the same colour?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Combination counting with an OR over three colours.
**Say this in the interview:** "Total ways to pick 3 of 15 balls is 15C3 = 455. Same colour: 4C3 + 6C3 + 5C3 = 4 + 20 + 10 = 34. So 34/455."
**Answer:** **34/455 (about 0.0747, or 7.5%)**
**Step-by-step working:**
1. Total balls = 4 + 6 + 5 = 15. Three drawn together (order irrelevant): 15C3 = (15 x 14 x 13) / 6 = 2730 / 6 = 455.
2. All red: 4C3 = 4.
3. All green: 6C3 = 20.
4. All yellow: 5C3 = 10.
5. Add (the colours are mutually exclusive): 4 + 20 + 10 = 34.
6. Probability = 34/455. (34 = 2 x 17 and 455 = 5 x 7 x 13 share no factor, so this is already simplest.)
**Check:** 34 / 455 = 0.0747; verified by script with exact fractions.
**Explain simply:**
- "Drawn together" means no order, so use combinations in both numerator and denominator.
- Add the three cases because the ball set is all one colour OR another, never two at once.
**Likely follow-ups:**
- "At least one red?" 1 - 11C3/455 = 1 - 165/455 = 290/455 = 58/91.
- "All three different colours?" 4 x 6 x 5 / 455 = 120/455 = 24/91.
**Common mistakes / traps:** Forgetting to add all three colours, or mixing permutations in the numerator with combinations in the denominator.

### Q21 ⭐⭐⭐ 🟡 A committee of 5 is to be chosen from 6 men and 4 women so that it has at least 2 women. In how many ways can this be done?
**Asked at:** commonly asked (no company-specific report found); "at least" committee selections are a standard pattern (prep-site claim).
**What the interviewer is checking:** Splitting "at least 2 women" into cases, or using the complement.
**Say this in the interview:** "At least 2 women means 2, 3 or 4 women. I add 3 cases, or take all 252 committees and subtract those with 0 or 1 woman. Both give 186."
**Answer:** **186 ways**
**Step-by-step working:**
1. Total committees of 5 from 10 people: 10C5 = 252.
2. Case 2 women, 3 men: 4C2 x 6C3 = 6 x 20 = 120.
3. Case 3 women, 2 men: 4C3 x 6C2 = 4 x 15 = 60.
4. Case 4 women, 1 man: 4C4 x 6C1 = 1 x 6 = 6.
5. Add: 120 + 60 + 6 = 186.
**Fast method (30 seconds):** Complement: subtract 0 women (6C5 = 6) and 1 woman (4C1 x 6C4 = 4 x 15 = 60) from 252: 252 - 6 - 60 = 186.
**Check:** both routes give 186; verified by script.
**Explain simply:**
- Choose the men and women separately, then multiply (a "and" step); add the cases (an "or" step).
- Only 4 women exist, so 5 women is impossible.
**Likely follow-ups:**
- "At most 1 woman?" 6 + 60 = 66.
- "Exactly 3 men?" 6C3 x 4C2 = 120.
**Common mistakes / traps:** Treating "at least 2" as "exactly 2" (120), or forgetting a case.

### Q22 ⭐⭐⭐ 🟡 Two fair dice are rolled together. What is the probability that the sum is greater than 9?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Listing favourable pairs in a 36-outcome space.
**Say this in the interview:** "Sums of 10, 11 or 12: 3 + 2 + 1 = 6 pairs out of 36, so 1/6."
**Answer:** **1/6**
**Step-by-step working:**
1. Total pairs = 36.
2. "Greater than 9" means 10, 11 or 12.
3. Sum 10: (4,6), (5,5), (6,4) = 3.
4. Sum 11: (5,6), (6,5) = 2.
5. Sum 12: (6,6) = 1.
6. Favourable = 3 + 2 + 1 = 6. Probability = 6/36 = 1/6.
**Check:** by symmetry, P(sum > 9) equals P(sum < 5) = (1 + 2 + 3)/36 = 6/36; verified by script.
**Explain simply:**
- "Greater than 9" excludes 9, so start from 10.
**Likely follow-ups:**
- "Sum at least 9?" Add 4 pairs for sum 9: 10/36 = 5/18.
- "Sum less than 5?" 6/36 = 1/6.
**Common mistakes / traps:** Including sum 9 (giving 10/36), which is "at least 9" or "greater than 8".

### Q23 ⭐⭐⭐ 🟡 A fair die is rolled 3 times. What is the probability of getting at least one six?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Complement rule with repeated independent trials.
**Say this in the interview:** "No six in a roll is 5/6. Three rolls: (5/6)^3 = 125/216. So at least one six = 1 - 125/216 = 91/216."
**Answer:** **91/216 (about 0.4213, or 42.1%)**
**Step-by-step working:**
1. Total outcomes: 6 x 6 x 6 = 216.
2. No six on any roll: 5 x 5 x 5 = 125 outcomes.
3. At least one six = 216 - 125 = 91 outcomes.
4. Probability = 91/216 (91 = 7 x 13 and 216 = 2^3 x 3^3, so it is in lowest terms).
**Fast method (30 seconds):** 1 - (5/6)^3 = 1 - 125/216 = 91/216. Rounded to 4 decimal places: 0.4213.
**Check:** brute-force enumeration of all 216 outcomes gives 91 containing a six; verified by script.
**Explain simply:**
- Rolls are independent, so the "no six" chances multiply.
- Adding 1/6 + 1/6 + 1/6 = 1/2 is wrong because it double counts outcomes with two or three sixes.
**Likely follow-ups:**
- "At least one six in 4 rolls?" 1 - (5/6)^4 = 1 - 625/1296 = 671/1296, about 0.518.
- "Exactly one six in 3 rolls?" 3 x (1/6) x (5/6)^2 = 75/216 = 25/72.
**Common mistakes / traps:** Answering 3/6 = 1/2 by adding the chances, or forgetting the final "1 minus".

### Q24 ⭐⭐⭐ 🟡 In how many ways can 5 people sit around a circular table?
**Asked at:** commonly asked (no company-specific report found); circular arrangement is a standard item in P&C prep lists (PapersAdda, unverified).
**What the interviewer is checking:** Whether you know that rotations of a circle count as the same seating.
**Say this in the interview:** "In a circle only relative positions matter, so I fix one person and arrange the other 4: (5-1)! = 24."
**Answer:** **24 ways**
**Step-by-step working:**
1. In a row, 5 people can be arranged in 5! = 120 ways.
2. In a circle, turning everyone one seat to the right gives the same seating. There are 5 such turns for each arrangement.
3. So circular arrangements = 120 / 5 = 24.
**Fast method (30 seconds):** Seat person 1 anywhere (this fixes the "start"), then arrange the remaining 4 in 4! = 4 x 3 x 2 x 1 = 24 ways.
**Check:** Verified by script (brute force over all 120 orders, merging rotations, gives 24).
**Explain simply:**
- A circle has no "first seat", so a rotation of the same group is not a new arrangement.
- Formula for n distinct people around a table: (n-1)!.
**Likely follow-ups:** 7 people round a table? 6! = 720.
**Common mistakes / traps:** Answering 5! = 120 (treating the table like a row).

### Q25 ⭐⭐⭐ 🟡 Seven people stand in a row. In how many ways can they be arranged if two particular people must always stand together?
**Asked at:** commonly asked (no company-specific report found); the "keep together" pattern appears in P&C prep guides (Toprankers, FACE Prep; unverified).
**What the interviewer is checking:** The "glue them into one block" method and remembering the block's internal order.
**Say this in the interview:** "Treat the two as one block, so 6 units arrange in 6! = 720 ways, and the pair can swap inside the block in 2 ways: 1,440."
**Answer:** **1,440 ways**
**Step-by-step working:**
1. Glue the two people into one block. Now there are 6 units (the block plus 5 others).
2. 6 units can be arranged in 6! = 720 ways.
3. Inside the block the two can stand as (X, Y) or (Y, X): 2 ways.
4. Total = 720 x 2 = 1,440.
**Check:** Verified by script (counting all 5,040 orders where the two are adjacent gives 1,440). Estimate: pair is adjacent in 6 of the 21 possible seat pairs, 6/21 x 5,040 = 1,440.
**Explain simply:**
- "Together" means a block; the block is moved around like one person.
- The multiplication rule joins the two independent choices: outer arrangement x inner arrangement.
**Likely follow-ups:** Not together? 5,040 - 1,440 = 3,600.
**Common mistakes / traps:** Stopping at 720 and forgetting the x 2 for the pair's internal order.

### Q26 ⭐⭐⭐ 🟡 A number is chosen at random from 1 to 50. What is the probability that it is a multiple of 4 or a multiple of 6?
**Asked at:** commonly asked (no company-specific report found); "multiple of A or B" is a standard inclusion-exclusion probability item (unverified).
**What the interviewer is checking:** Inclusion-exclusion: do not double-count numbers that are multiples of both.
**Say this in the interview:** "Multiples of 4: 12; of 6: 8; of both means multiples of 12: 4. So 12 + 8 - 4 = 16 out of 50, which is 8/25."
**Answer:** **8/25 (0.32)**
**Step-by-step working:**
1. Multiples of 4 up to 50: 4, 8, ..., 48. Count = 50/4 = 12 (whole part).
2. Multiples of 6 up to 50: 6, 12, ..., 48. Count = 50/6 = 8 (whole part).
3. Multiples of both are multiples of the LCM (least common multiple) 12: 12, 24, 36, 48. Count = 4.
4. Numbers that are a multiple of 4 or 6 = 12 + 8 - 4 = 16.
5. Probability = 16/50 = 8/25.
**Check:** Verified by script (listing 1 to 50 gives 16 qualifying numbers).
**Explain simply:**
- P(A or B) = P(A) + P(B) - P(A and B). The overlap is counted twice, so subtract it once.
- "Both 4 and 6" means a multiple of 12, not 24 (4 x 6 would be wrong because 4 and 6 share a factor 2).
**Likely follow-ups:** Multiple of 3 or 5 from 1 to 30? 10 + 6 - 2 = 14, so 14/30 = 7/15.
**Common mistakes / traps:** Giving 20/50 (12 + 8) without subtracting the 4 overlaps; or using 24 as the overlap.

### Q27 ⭐⭐⭐ 🟡 How many 4-digit numbers can be formed using the digits 0, 1, 2, 3, 4, 5 if no digit may be repeated?
**Asked at:** commonly asked (no company-specific report found); the "0 cannot lead" digit-forming pattern is standard in P&C lists (unverified).
**What the interviewer is checking:** Handling the restricted first digit first.
**Say this in the interview:** "First digit cannot be 0, so 5 choices; then 5, 4 and 3 choices for the rest: 5 x 5 x 4 x 3 = 300."
**Answer:** **300 numbers**
**Step-by-step working:**
1. Thousands place: any of 1 to 5 (not 0) = 5 choices.
2. Hundreds place: 5 digits remain (including 0) = 5 choices.
3. Tens place: 4 choices.
4. Units place: 3 choices.
5. Total = 5 x 5 x 4 x 3 = 300.
**Check:** Verified by script. Hand check: all 4-digit strings without repeat = 6 x 5 x 4 x 3 = 360; those starting with 0 = 5 x 4 x 3 = 60; 360 - 60 = 300.
**Explain simply:**
- Fill the restricted place first, then the others; multiply the choices.
- A number cannot start with 0 or it becomes a 3-digit number.
**Likely follow-ups:** How many of these are even? Units 0: 5x4x3 = 60; units 2 or 4: 2 x (4 x 4 x 3) = 96; total 156.
**Common mistakes / traps:** 6 x 5 x 4 x 3 = 360 (allowing a leading zero).

### Q28 ⭐⭐⭐ 🔴 In how many ways can 5 men and 4 women be seated in a row so that no two women sit next to each other?
**Asked at:** commonly asked (no company-specific report found); the "gap method" is a standard harder P&C pattern (unverified).
**What the interviewer is checking:** The gap method: seat the unrestricted group first, then slot the restricted group into gaps.
**Say this in the interview:** "Seat the 5 men first: 5! = 120. That creates 6 gaps (including both ends). Choose and arrange 4 of them for the women: 6P4 = 360. Total 120 x 360 = 43,200."
**Answer:** **43,200 ways**
**Step-by-step working:**
1. Seat the 5 men in a row: 5! = 120 ways.
2. Gaps for women: before the first man, between men (4), after the last man = 6 gaps. Women in separate gaps cannot touch each other.
3. Put the 4 distinct women into 4 different gaps out of 6, order matters: 6 x 5 x 4 x 3 = 360 ways.
4. Total = 120 x 360 = 43,200.
**Check:** Verified by script (brute force over all 9! = 362,880 seatings gives 43,200). Cross-check: 9! = 362,880 total, and 43,200/362,880 = 5/42, about 12% have no two women adjacent, which is plausible.
**Explain simply:**
- Why men first? Once men stand, the gaps are fixed, so "no two women adjacent" becomes "at most one woman per gap".
- Choosing gaps then ordering women: 6C4 x 4! = 15 x 24 = 360, the same as 6P4.
**Likely follow-ups:** 3 men and 4 women, no two women adjacent? 3 men leave 4 gaps; women fill all: 3! x 4! = 144.
**Common mistakes / traps:** Counting only 5 gaps (forgetting the two ends), or using 6C4 without multiplying by 4! for the women's order.

### Q29 ⭐⭐ 🟢 What are the values of 0!, nC0 and nCn, and why is nCr equal to nC(n-r)?
**Asked at:** commonly asked (no company-specific report found); concept check in P&C basics (unverified).
**What the interviewer is checking:** Whether you understand the definitions behind the formula, not only the formula.
**Say this in the interview:** "0! = 1, nC0 = 1 and nCn = 1. nCr = nC(n-r) because choosing r people to include is the same as choosing n-r people to leave out."
**Answer:** **0! = 1; nC0 = 1; nCn = 1; nCr = nC(n-r)**
**Explain simply:**
- 0! = 1 by definition: there is exactly one way to arrange nothing (the empty arrangement). It also keeps the formula nCr = n!/(r!(n-r)!) working: nC0 = n!/(0! x n!) = 1 only if 0! = 1.
- nC0 = 1: there is one way to pick nobody. nCn = 1: one way to pick everybody.
- Symmetry: nCr = n!/(r!(n-r)!) and nC(n-r) = n!/((n-r)! x r!) are the same expression.
**Worked mini-example:** From 8 employees choose 3 for a team: 8C3 = 56. Equivalent to choosing the 5 who stay out: 8C5 = 56. Check: 8C3 = (8 x 7 x 6)/6 = 56; 8C5 = (8 x 7 x 6 x 5 x 4)/120 = 56.
**Check:** 8C3 = 8C5 = 56 (worked above); 0! = 1 is what makes nC0 = n!/(0! x n!) equal 1, as shown.
**Likely follow-ups:** Use the symmetry to find 50C48: equals 50C2 = (50 x 49)/2 = 1,225.
**Common mistakes / traps:** Saying 0! = 0. Also computing 10C8 the long way instead of using 10C2 = 45.

### Q30 ⭐⭐ 🟢 What is the difference between selecting with replacement and without replacement, and how does it change the probability calculation?
**Asked at:** commonly asked (no company-specific report found); a standard concept in ball and card probability (unverified).
**What the interviewer is checking:** Whether you know when the denominator and the favourable count change between draws.
**Say this in the interview:** "With replacement, the item goes back, so every draw has the same probability and draws are independent. Without replacement, the pool shrinks, so later probabilities change."
**Answer:** **With replacement: same probability every draw (independent). Without replacement: probabilities change after each draw (dependent).**
**Explain simply:**
- With replacement: multiply the same fraction each time.
- Without replacement: reduce both the favourable count and the total as items are removed.
**Worked mini-example:** A bag has 3 red and 2 blue balls; draw two reds. With replacement: 3/5 x 3/5 = 9/25. Without: 3/5 x 2/4 = 6/20 = 3/10.
**Check:** 9/25 = 0.36 and 3/10 = 0.30; without replacement is smaller because a red has been removed. Also 3C2/5C2 = 3/10, verified by script.
**Likely follow-ups:** "Drawn together" means? Treat as without replacement; use combinations on top and bottom: (favourable selections) / (total selections), as in 3C2/5C2 above.
**Common mistakes / traps:** Using the same fraction (3/5) for the second draw when the first ball is not returned.

### Q31 ⭐⭐ 🟢 How do you count arrangements of n letters when some letters repeat, for example the word MISSISSIPPI?
**Asked at:** commonly asked (no company-specific report found); MISSISSIPPI is a named example in prep guides (Toprankers, FACE Prep; unverified).
**What the interviewer is checking:** The divide-by-repeats rule.
**Say this in the interview:** "Arrange as if all letters were different, n!, then divide by the factorial of each repeat count. MISSISSIPPI has 11 letters: I x4, S x4, P x2, M x1, so 11!/(4! x 4! x 2!) = 34,650."
**Answer:** **n!/(p! x q! x r! ...); for MISSISSIPPI, 34,650**
**Explain simply:**
- If all letters were different there would be n! orders. Swapping two identical letters does not create a new word, so each real word is counted p! times for p copies; divide by p!.
- Do this for each repeated letter.
**Worked mini-example:** DATA: 4 letters, A twice: 4!/2! = 24/2 = 12 arrangements.
**Check:** MISSISSIPPI: 11! = 39,916,800; 4! x 4! x 2! = 1,152; 39,916,800/1,152 = 34,650. Verified by script.
**Likely follow-ups:** BOOKKEEPER? 10 letters, O x2, K x2, E x3: 10!/(2! x 2! x 3!) = 151,200.
**Common mistakes / traps:** Forgetting letters that appear once (harmless, 1! = 1) or dividing by the number of repeated letters (4+4+2) instead of the product of factorials.

### Q32 ⭐⭐ 🟢 Calculate 12C4 by cancelling terms, without expanding the full factorials.
**Asked at:** commonly asked (no company-specific report found); a calculation-speed item (unverified).
**What the interviewer is checking:** Fluency in cancelling factorials.
**Say this in the interview:** "12C4 = (12 x 11 x 10 x 9)/(4 x 3 x 2 x 1). Cancel to get 495."
**Answer:** **495**
**Step-by-step working:**
1. Write only 4 terms on top, starting at 12 and going down, and 4! below: (12 x 11 x 10 x 9)/(4 x 3 x 2 x 1).
2. 12/(4 x 3) = 1, leaving (11 x 10 x 9)/2.
3. 10/2 = 5, leaving 11 x 5 x 9.
4. 11 x 5 = 55; 55 x 9 = 495.
**Check:** Verified by script. Reverse: 12C8 should equal 12C4 by symmetry, and 495 is a known Pascal's triangle value.
**Explain simply:**
- nCr = (r terms counting down from n)/(r!), because the long factorial parts cancel.
- Cancel before multiplying to keep numbers small.
**Likely follow-ups:** 10C3? (10 x 9 x 8)/6 = 120.
**Common mistakes / traps:** Using 4 terms on top but forgetting that 4! = 24 (not 4) below; or multiplying everything out first and making errors.

### Q33 ⭐⭐ 🟢 Two fair dice are rolled together. What is the probability that the product of the two numbers is even?
**Asked at:** commonly asked (no company-specific report found); dice-product items are standard in basic probability banks (unverified).
**What the interviewer is checking:** Using the complement: product is odd only if both numbers are odd.
**Say this in the interview:** "Product is odd only when both dice are odd: 1/2 x 1/2 = 1/4. So even is 1 - 1/4 = 3/4."
**Answer:** **3/4 (0.75)**
**Step-by-step working:**
1. Total outcomes = 6 x 6 = 36.
2. Odd product needs both dice odd: 3 x 3 = 9 outcomes.
3. Even product = 36 - 9 = 27 outcomes.
4. Probability = 27/36 = 3/4.
**Check:** Verified by script (counting all 36 products gives 27 even).
**Explain simply:**
- Even x anything = even; the only way to get odd is odd x odd.
- Complement rule: count the easy opposite case and subtract from 1.
**Likely follow-ups:** Product odd? 1/4. Sum even? Both same parity: 18/36 = 1/2.
**Common mistakes / traps:** Answering 1/2 (assuming even and odd products are equally likely).

### Q34 ⭐⭐ 🟢 A fair die is rolled twice. What is the probability that both numbers are the same?
**Asked at:** commonly asked (no company-specific report found); a standard two-dice item (unverified).
**What the interviewer is checking:** Counting favourable outcomes out of 36, or the "first roll is free" idea.
**Say this in the interview:** "Six matching pairs out of 36: 6/36 = 1/6."
**Answer:** **1/6 (about 0.167)**
**Step-by-step working:**
1. Total outcomes = 6 x 6 = 36.
2. Matching pairs: (1,1), (2,2), (3,3), (4,4), (5,5), (6,6) = 6.
3. Probability = 6/36 = 1/6.
**Fast method (30 seconds):** The first roll can be anything. The second must match it: 1 face out of 6 = 1/6.
**Check:** Verified by script (6 of 36 outcomes).
**Explain simply:**
- Rolls are independent, so the second roll does not care what the first was.
**Likely follow-ups:** Three dice all the same? First free, then 1/6 x 1/6 = 1/36.
**Common mistakes / traps:** Multiplying 1/6 x 1/6 = 1/36 (that is the chance of a specific pair such as two sixes).

### Q35 ⭐⭐ 🟢 What is the minimum number of employees you must pick to guarantee that at least two of them have their birthday in the same calendar month?
**Asked at:** commonly asked (no company-specific report found); pigeonhole items appear in aptitude banks (unverified).
**What the interviewer is checking:** The pigeonhole principle and worst-case thinking.
**Say this in the interview:** "There are 12 months. In the worst case the first 12 people each have a different month. The 13th must repeat one: 13."
**Answer:** **13 employees**
**Step-by-step working:**
1. Boxes = 12 months.
2. Worst case: 12 people, each in a different month. No pair yet.
3. The 13th person must land in a month already used. So 13 guarantees a pair.
**Check:** With 12 people it is possible to have 12 different months (no guarantee), so 12 is not enough; 13 is the minimum.
**Explain simply:**
- Pigeonhole principle: if you put more than k items into k boxes, some box has at least 2 items.
- "Guarantee" means plan for the worst case, not the likely case.
**Likely follow-ups:** Guarantee 3 people in the same month? Worst case 2 per month = 24, so 25.
**Common mistakes / traps:** Answering 12 (just the number of months) or 2 (the group size asked for).

### Q36 ⭐⭐ 🟢 A team has 5 men and 4 women. Three people are chosen at random for a training programme. What is the probability that all three are women?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured version of the standard "all same type" selection item (unverified).
**What the interviewer is checking:** Favourable combinations divided by total combinations.
**Say this in the interview:** "4C3 = 4 ways to pick three women out of 9C3 = 84 total groups: 4/84 = 1/21."
**Answer:** **1/21 (about 0.048)**
**Step-by-step working:**
1. Total ways to choose 3 from 9 = 9C3 = (9 x 8 x 7)/6 = 84.
2. Ways to choose 3 women from 4 = 4C3 = 4.
3. Probability = 4/84 = 1/21.
**Fast method (30 seconds):** Pick one by one: 4/9 x 3/8 x 2/7 = 24/504 = 1/21.
**Check:** Both routes give 1/21; verified by script.
**Explain simply:**
- Choosing "together" does not depend on order, so use combinations on top and bottom.
- Step-by-step fractions give the same answer because the pool shrinks each time.
**Likely follow-ups:** At least one man? 1 - 1/21 = 20/21.
**Common mistakes / traps:** Using 4/9 x 4/9 x 4/9 (that assumes replacement).

### Q37 ⭐⭐ 🟡 What is the difference between mutually exclusive events and independent events, and can two events with non-zero probability be both?
**Asked at:** commonly asked (no company-specific report found); a classic concept trap (unverified).
**What the interviewer is checking:** Whether you separate "cannot happen together" from "do not influence each other".
**Say this in the interview:** "Mutually exclusive means P(A and B) = 0. Independent means P(A and B) = P(A) x P(B). If both have non-zero probability, they cannot be both."
**Answer:** **No. Two events with non-zero probabilities cannot be both mutually exclusive and independent.**
**Explain simply:**
- Mutually exclusive: if one happens, the other cannot (rolling a 2 and a 5 on one throw). Then P(A and B) = 0.
- Independent: one happening does not change the chance of the other (two separate coin tosses). Then P(A and B) = P(A) x P(B).
- If both held, then P(A) x P(B) = 0, so at least one probability must be 0.
- Mutually exclusive events with non-zero probability are in fact dependent: knowing A happened tells you B did not.
**Worked mini-example:** Die: A = "even" (1/2), B = "odd" (1/2). Exclusive: P(A and B) = 0, but P(A) x P(B) = 1/4, not 0, so not independent. Two coin tosses: P(H1 and H2) = 1/4 = 1/2 x 1/2, independent, but both can happen, so not exclusive.
**Check:** Die example: P(even and odd) = 0 but 1/2 x 1/2 = 1/4, so exclusive events with non-zero chances fail the independence test. (Edge case: an event with probability 0 is trivially both, which is why the question says non-zero.)
**Likely follow-ups:** For exclusive events, P(A or B)? P(A) + P(B) (no subtraction).
**Common mistakes / traps:** Treating the two words as the same idea.

### Q38 ⭐⭐ 🟡 What is the formula for the number of circular arrangements of n distinct objects, and how does it change when clockwise and anticlockwise arrangements are treated as the same (a necklace or garland)?
**Asked at:** commonly asked (no company-specific report found); a standard circular-permutation concept (unverified).
**What the interviewer is checking:** Rotation versus reflection symmetry.
**Say this in the interview:** "Circular arrangements are (n-1)!. For a necklace, where flipping it over gives the same arrangement, divide by 2: (n-1)!/2."
**Answer:** **(n-1)! for a circular table; (n-1)!/2 for a necklace or garland (n of at least 3)**
**Explain simply:**
- Table: rotations are the same, so fix one person and arrange the other n-1.
- Necklace: you can also flip it over, so each arrangement and its mirror image are the same. Every arrangement pairs up with a different mirror image (when n is at least 3), so halve.
**Worked mini-example:** 5 people at a table: 4! = 24. 5 different beads on a necklace: 24/2 = 12.
**Check:** n = 3: table gives 2! = 2 (ABC and ACB); necklace gives 2/2 = 1, correct since ABC flipped is ACB.
**Likely follow-ups:** 6 different flowers in a garland? 5!/2 = 60.
**Common mistakes / traps:** Halving for a seating table (people cannot be flipped, so clockwise and anticlockwise differ).

### Q39 ⭐⭐ 🟡 If P(A) = 0.5, P(B) = 0.4 and P(A and B) = 0.2, what is P(A or B)?
**Asked at:** commonly asked (no company-specific report found); direct use of the addition rule (unverified).
**What the interviewer is checking:** The addition rule with overlap.
**Say this in the interview:** "P(A or B) = 0.5 + 0.4 - 0.2 = 0.7."
**Answer:** **0.7**
**Step-by-step working:**
1. P(A or B) = P(A) + P(B) - P(A and B).
2. = 0.5 + 0.4 - 0.2 = 0.9 - 0.2 = 0.7.
**Check:** Here P(A) x P(B) = 0.5 x 0.4 = 0.2 = P(A and B), so A and B are independent; also 1 - (1-0.5)(1-0.4) = 1 - 0.3 = 0.7. Verified by script.
**Explain simply:**
- Adding P(A) and P(B) counts the overlap twice, so subtract it once.
**Likely follow-ups:** P(neither)? 1 - 0.7 = 0.3.
**Common mistakes / traps:** Answering 0.9 (not subtracting the overlap).

### Q40 ⭐⭐ 🟡 Two analysts check a report independently. Analyst A catches a particular error with probability 1/3 and Analyst B with probability 1/4. What is the probability that exactly one of them catches it?
**Asked at:** commonly asked (no company-specific report found); a standard independent-events item in a workplace setting (unverified).
**What the interviewer is checking:** Splitting "exactly one" into two cases and multiplying independent probabilities.
**Say this in the interview:** "A catches and B misses: 1/3 x 3/4 = 1/4. B catches and A misses: 2/3 x 1/4 = 1/6. Add: 5/12."
**Answer:** **5/12 (about 0.417)**
**Step-by-step working:**
1. P(A catches, B misses) = 1/3 x (1 - 1/4) = 1/3 x 3/4 = 3/12.
2. P(B catches, A misses) = 1/4 x (1 - 1/3) = 1/4 x 2/3 = 2/12.
3. The two cases cannot happen together, so add: 3/12 + 2/12 = 5/12.
**Check:** Both catch = 1/3 x 1/4 = 1/12; neither = 2/3 x 3/4 = 6/12; 1/12 + 5/12 + 6/12 = 1. Verified by script.
**Explain simply:**
- Independent means multiply for "and"; separate cases that cannot overlap are added for "or".
**Likely follow-ups:** At least one catches it? 1 - 6/12 = 1/2.
**Common mistakes / traps:** Answering 1/3 + 1/4 = 7/12 (that includes the both-catch case) or 1/12 (only both).

### Q41 ⭐⭐ 🟡 What is the rank of the word RATE if all arrangements of its letters are listed in dictionary (alphabetical) order?
**Asked at:** commonly asked (no company-specific report found); "rank of a word" is a standard P&C pattern (unverified).
**What the interviewer is checking:** Counting all words that come before, letter by letter.
**Say this in the interview:** "Alphabetical letters: A, E, R, T. Words starting with A or E come first: 6 + 6 = 12. Then RAET is 13th and RATE is 14th. Rank 14."
**Answer:** **14**
**Step-by-step working:**
1. Letters in order: A, E, R, T. Total words = 4! = 24.
2. First letter A: remaining 3 letters arrange in 3! = 6 ways. First letter E: 6 ways. That is 12 words before any word beginning with R.
3. Now first letter R. Remaining letters A, E, T. Second letter A (smallest): words RAET, RATE. RAET comes first (E before T).
4. So RAET = 13th, RATE = 14th.
**Check:** Verified by script (sorting all 24 arrangements, RATE is at position 14). Also R begins words 13 to 18, and RATE is the 2nd of the RA- block.
**Explain simply:**
- For each position, count the words that start with a smaller available letter, multiply by the factorial of letters left, then add 1 for the word itself.
- Here: first letter R has 2 smaller letters (A, E): 2 x 3! = 12; second letter A has 0 smaller left: 0 x 2! = 0; third letter T has 1 smaller left (E): 1 x 1! = 1; total before = 13; rank = 13 + 1 = 14.
**Likely follow-ups:** Rank of TEAR? Smaller first letters A, E, R: 3 x 3! = 18; second letter E has 1 smaller left (A): 1 x 2! = 2; third letter A has 0 smaller left; total before = 20, so rank 21.
**Common mistakes / traps:** Forgetting the "+1" for the word itself, or not sorting the letters alphabetically first.

### Q42 ⭐⭐ 🟡 In how many ways can 5 distinct bonus vouchers be distributed among 3 employees if any employee may receive any number of vouchers, including none?
**Asked at:** commonly asked (no company-specific report found); a standard "distribution" item (unverified).
**What the interviewer is checking:** Choosing the right viewpoint: voucher chooses employee, not the reverse.
**Say this in the interview:** "Each voucher can go to any of 3 employees, independently, so 3 x 3 x 3 x 3 x 3 = 3^5 = 243."
**Answer:** **243 ways**
**Step-by-step working:**
1. Voucher 1 has 3 choices of employee; so do vouchers 2, 3, 4 and 5.
2. By the multiplication rule: 3 x 3 x 3 x 3 x 3 = 243.
**Check:** Verified by script (all assignments counted by brute force: 243). Estimate: 3^5 = 9 x 27 = 243.
**Explain simply:**
- Look at the object being placed: each voucher has 3 options, and its choice does not affect the others.
- Do not count from the employee side ("each employee picks vouchers"), which becomes messy.
**Likely follow-ups:** Each employee must get at least one? Count of onto assignments = 3^5 - 3 x 2^5 + 3 = 243 - 96 + 3 = 150.
**Common mistakes / traps:** Answering 5^3 = 125 (swapping the base and exponent).

### Q43 ⭐⭐ 🟡 A committee of 4 is to be chosen from 10 people, two of whom are A and B. In how many ways can it be chosen if A and B must not both be on the committee?
**Asked at:** commonly asked (no company-specific report found); a standard "restriction by complement" selection item (unverified).
**What the interviewer is checking:** Total minus the forbidden case.
**Say this in the interview:** "Total committees 10C4 = 210. Committees with both A and B: choose the other 2 from 8 = 8C2 = 28. So 210 - 28 = 182."
**Answer:** **182 ways**
**Step-by-step working:**
1. Total ways without any restriction = 10C4 = (10 x 9 x 8 x 7)/24 = 210.
2. Forbidden committees have both A and B. Two seats are taken, so choose the other 2 from the remaining 8: 8C2 = 28.
3. Allowed = 210 - 28 = 182.
**Check:** Direct count: neither A nor B: 8C4 = 70; exactly one of them: 2 x 8C3 = 2 x 56 = 112; 70 + 112 = 182. Verified by script.
**Explain simply:**
- "Not both" = everything except "both", so subtract.
- "Not both" still allows only A, only B, or neither.
**Likely follow-ups:** A and B must both be on? 28.
**Common mistakes / traps:** Subtracting 8C3 or removing A and B altogether (8C4 = 70), which wrongly bans each of them individually.

### Q44 ⭐⭐ 🟡 How many rectangles (of all sizes) are there on a standard 8 x 8 chessboard?
**Asked at:** commonly asked (no company-specific report found); a classic geometry-counting item (unverified).
**What the interviewer is checking:** Seeing a rectangle as a choice of 2 horizontal and 2 vertical lines.
**Say this in the interview:** "The board has 9 horizontal and 9 vertical grid lines. A rectangle needs 2 of each: 9C2 x 9C2 = 36 x 36 = 1,296."
**Answer:** **1,296 rectangles (squares are included)**
**Step-by-step working:**
1. An 8 x 8 board has 8 rows of squares, so 9 horizontal lines; similarly 9 vertical lines.
2. Choose 2 horizontal lines: 9C2 = (9 x 8)/2 = 36.
3. Choose 2 vertical lines: 9C2 = 36.
4. Rectangles = 36 x 36 = 1,296.
**Check:** Verified by script. Also, squares alone = 1^2 + 2^2 + ... + 8^2 = 204, which is less than 1,296, as it should be.
**Explain simply:**
- Each pair of horizontal lines and each pair of vertical lines encloses exactly one rectangle.
- A square is a special rectangle, so 1,296 includes the 204 squares.
**Likely follow-ups:** Rectangles that are not squares? 1,296 - 204 = 1,092.
**Common mistakes / traps:** Using 8C2 x 8C2 = 784 (counting squares instead of lines) or counting only the 204 squares.

### Q45 ⭐⭐ 🟡 There are 10 points on a plane, of which 4 lie on one straight line and no other three are collinear. How many triangles can be formed using these points as vertices?
**Asked at:** commonly asked (no company-specific report found); a standard collinear-points item (unverified).
**What the interviewer is checking:** Subtracting the groups of 3 that cannot form a triangle.
**Say this in the interview:** "Any 3 points make a triangle except 3 on the same line: 10C3 - 4C3 = 120 - 4 = 116."
**Answer:** **116 triangles**
**Step-by-step working:**
1. Ways to choose any 3 points from 10: 10C3 = (10 x 9 x 8)/6 = 120.
2. Three points on the same line give no triangle. Choose 3 from the 4 collinear points: 4C3 = 4.
3. Triangles = 120 - 4 = 116.
**Check:** Direct count: 0 collinear points: 6C3 = 20; 1 collinear point: 4 x 6C2 = 60; 2 collinear points: 4C2 x 6 = 36; total 116. Verified by script.
**Explain simply:**
- A triangle needs 3 non-collinear points. Count all triples, then remove the "flat" ones.
**Likely follow-ups:** If 5 points were collinear? 120 - 5C3 = 120 - 10 = 110.
**Common mistakes / traps:** Answering 120, or subtracting 4C2 = 6 (wrong group size).

### Q46 ⭐⭐ 🟡 How many distinct arrangements are there of the letters of the word MISSISSIPPI?
**Asked at:** commonly asked (no company-specific report found); named as a standard example in P&C prep guides (Toprankers, FACE Prep; unverified).
**What the interviewer is checking:** Repeated-letter arrangements (this repeats the method of Q31 with the final number).
**Say this in the interview:** "11 letters: I four times, S four times, P twice, M once. 11!/(4! x 4! x 2!) = 34,650."
**Answer:** **34,650 arrangements**
**Step-by-step working:**
1. Count letters: M = 1, I = 4, S = 4, P = 2; total 1 + 4 + 4 + 2 = 11.
2. Arrangements = 11!/(1! x 4! x 4! x 2!).
3. Cancel: 11! = 11 x 10 x 9 x 8 x 7 x 6 x 5 x 4!, so the 4! cancels: (11 x 10 x 9 x 8 x 7 x 6 x 5)/(4! x 2!) = 1,663,200/48 = 34,650.
**Fast method (30 seconds):** Choose positions: put the 4 S's in 11C4 = 330 ways, the 4 I's in the remaining 7 places 7C4 = 35 ways, the 2 P's in the remaining 3 places 3C2 = 3 ways, M takes the last place: 330 x 35 x 3 = 34,650.
**Check:** Both routes give 34,650. Verified by script.
**Explain simply:**
- Identical letters cannot be told apart, so divide by the ways to shuffle each identical group among itself.
**Likely follow-ups:** How many start with M? Remaining 10 letters I4 S4 P2: 10!/(4! x 4! x 2!) = 3,150.
**Common mistakes / traps:** Forgetting to divide, giving 11! = 39,916,800, or dividing by 4! only once.

### Q47 ⭐⭐ 🟡 Two cards are drawn together from a pack of 52 cards. What is the probability that both are spades?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Combinations in probability: favourable selections over total selections.
**Say this in the interview:** "Choose 2 spades out of 13 and divide by choosing any 2 out of 52. It simplifies to 1/17."
**Answer:** **1/17 (about 0.0588)**
**Step-by-step working:**
1. Ways to pick any 2 cards: 52C2 = 52 x 51 / 2 = 1326.
2. Ways to pick 2 spades: 13C2 = 13 x 12 / 2 = 78.
3. Probability = 78 / 1326 = 1/17.
**Fast method (30 seconds):** Card by card: 13/52 x 12/51 = 1/4 x 4/17 = 1/17. Drawing 'together' is the same as drawing one after another without replacement.
**Check:** 1/4 x 12/51 = 12/204 = 1/17, same answer by the sequential route (also verified by script).
**Explain simply:**
- nCr (combination) counts selections where order does not matter, which is right for 'drawn together'.
- Probability = favourable outcomes / total equally likely outcomes.
**Likely follow-ups:** 1) Both red? 26C2/52C2 = 325/1326 = 25/102. 2) Both kings? 6/1326 = 1/221.
**Common mistakes / traps:** Using 13/52 x 13/52 (that is with replacement) gives 1/16, the tempting wrong option.

### Q48 ⭐⭐ 🟡 Two fair dice are rolled. Given that the first die shows 3, what is the probability that the sum is 8?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Conditional probability: shrink the sample space to what is given.
**Say this in the interview:** "Once the first die is 3, only the second die is random. I need a 5, so the answer is 1/6."
**Answer:** **1/6**
**Step-by-step working:**
1. Given: first die = 3. The sample space is now just the second die: 6 outcomes.
2. Sum 8 needs second die = 8 - 3 = 5: 1 outcome.
3. Probability = 1/6.
**Fast method (30 seconds):** Formula check: P(sum 8 and first 3) = 1/36; P(first 3) = 6/36; divide: (1/36)/(6/36) = 1/6.
**Check:** verified by script (listing all 36 pairs, 6 have first die 3, 1 of them sums to 8).
**Explain simply:**
- Conditional probability P(A|B) = P(A and B) / P(B): 'out of the cases where B happened, how many also have A'.
- Given information removes outcomes from the sample space.
**Likely follow-ups:** 1) Given first die is 3, probability sum is at least 8? Second die 5 or 6: 2/6 = 1/3. 2) Probability of sum 8 with no condition? 5/36.
**Common mistakes / traps:** Answering 5/36 (the unconditional chance of sum 8) ignores the given information.

### Q49 ⭐⭐ 🟡 A family has two children. Assuming each child is equally likely to be a boy or a girl, independently, what is the probability that both are boys given that at least one is a boy?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** The classic 'at least one' conditional trap: list equally likely cases.
**Say this in the interview:** "List the four equally likely cases: BB, BG, GB, GG. Remove GG, leaving 3. Only 1 is BB, so it is 1/3, not 1/2."
**Answer:** **1/3**
**Step-by-step working:**
1. Equally likely outcomes (older, younger): BB, BG, GB, GG, each 1/4.
2. 'At least one boy' removes GG, leaving BB, BG, GB: 3 cases.
3. Only BB has both boys: 1 case.
4. Probability = 1/3.
**Check:** P(both boys and at least one boy) / P(at least one boy) = (1/4)/(3/4) = 1/3; also verified by script.
**Explain simply:**
- Knowing 'at least one is a boy' is different from knowing 'the first child is a boy' (that gives 1/2).
- Conditional probability = favourable cases among the cases still possible.
**Likely follow-ups:** 1) If we are told the elder child is a boy, chance both are boys? 1/2. 2) Two children, at least one girl, both girls? 1/3.
**Common mistakes / traps:** Saying 1/2 because 'the other child is a boy or girl equally'. That ignores that BG and GB are two separate cases.

### Q50 ⭐⭐ 🟡 What is the probability that a leap year selected at random has 53 Sundays?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Reducing a calendar problem to the 2 extra days.
**Say this in the interview:** "A leap year has 52 full weeks plus 2 extra days. Those two days contain a Sunday in 2 of 7 pairs, so 2/7."
**Answer:** **2/7**
**Step-by-step working:**
1. Leap year = 366 days = 52 weeks (364 days) + 2 extra days.
2. The 52 weeks already give 52 Sundays; we need one more Sunday among the 2 extra days.
3. The 2 extra days are consecutive days. Possible pairs: (Mon,Tue), (Tue,Wed), (Wed,Thu), (Thu,Fri), (Fri,Sat), (Sat,Sun), (Sun,Mon): 7 equally likely pairs.
4. Pairs containing Sunday: (Sat,Sun) and (Sun,Mon) = 2.
5. Probability = 2/7.
**Check:** an ordinary year (365 days, 1 extra day) gives 1/7; a leap year has one more extra day, so 2/7 is consistent. Verified by script.
**Explain simply:**
- The extra days left after full weeks decide everything; 366 mod 7 = 2.
- The pair is decided by which day the year starts on, and each start day is equally likely.
**Likely follow-ups:** 1) Non-leap year with 53 Sundays? 1/7. 2) Leap year with 53 Mondays? 2/7.
**Common mistakes / traps:** Saying 1/7 (the non-leap answer) or forgetting that two days, not one, are left over.

### Q51 ⭐⭐ 🟡 A fair coin is tossed 4 times. What is the probability of getting exactly 2 heads?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Binomial counting: arrangements of heads among tosses.
**Say this in the interview:** "There are 2^4 = 16 equally likely sequences, and 4C2 = 6 of them have exactly two heads. So 6/16 = 3/8."
**Answer:** **3/8 (0.375)**
**Step-by-step working:**
1. Total sequences = 2 x 2 x 2 x 2 = 16.
2. Choose which 2 of the 4 tosses are heads: 4C2 = 4 x 3 / 2 = 6 (HHTT, HTHT, HTTH, THHT, THTH, TTHH).
3. Probability = 6/16 = 3/8.
**Fast method (30 seconds):** Row 4 of Pascal's triangle is 1, 4, 6, 4, 1; the middle 6 over the total 16.
**Check:** probabilities for 0 to 4 heads are 1+4+6+4+1 = 16 over 16, which equals 1. Verified by script.
**Explain simply:**
- Each toss is independent with chance 1/2, so every one of the 16 sequences is equally likely.
- nCr counts positions of heads without caring about order of choosing them.
**Likely follow-ups:** 1) At least 3 heads? (4+1)/16 = 5/16. 2) Exactly 3 heads in 6 tosses? 20/64 = 5/16.
**Common mistakes / traps:** Answering 1/2 because 2 heads out of 4 'feels' even; or using 1/4 by forgetting the arrangements.

### Q52 ⭐⭐ 🟡 A batch has 10 items, of which 3 are defective. Two items are chosen at random without replacement for inspection. What is the probability that neither is defective?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Probability without replacement using combinations.
**Say this in the interview:** "Seven items are good. Choose 2 good from 7 over choose 2 from 10: 21/45 = 7/15."
**Answer:** **7/15 (about 0.467)**
**Step-by-step working:**
1. Good items = 10 - 3 = 7.
2. Ways to pick 2 good: 7C2 = 7 x 6 / 2 = 21.
3. Ways to pick any 2: 10C2 = 10 x 9 / 2 = 45.
4. Probability = 21/45 = 7/15.
**Fast method (30 seconds):** Sequentially: 7/10 x 6/9 = 42/90 = 7/15.
**Check:** 7/10 x 6/9 = 7/15, matches. Verified by script.
**Explain simply:**
- 'Without replacement' means the second pick has one fewer item to choose from, so probabilities change.
- Two routes (combinations or multiply fractions) must agree.
**Likely follow-ups:** 1) Exactly one defective? 7 x 3 / 45 = 21/45 = 7/15. 2) At least one defective? 1 - 7/15 = 8/15.
**Common mistakes / traps:** Using 7/10 x 7/10 = 0.49, which is the with-replacement answer.

### Q53 ⭐⭐ 🟡 A two-digit number is chosen at random from all two-digit numbers (10 to 99). What is the probability that it is divisible by 7?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Counting multiples in a range carefully.
**Say this in the interview:** "Multiples of 7 from 14 to 98 number 13, out of 90 two-digit numbers, so 13/90."
**Answer:** **13/90 (about 0.144)**
**Step-by-step working:**
1. Two-digit numbers: 10 to 99, so 99 - 10 + 1 = 90.
2. Smallest two-digit multiple of 7 is 14 (7 x 2); largest is 98 (7 x 14).
3. Multiples: 7 x 2 up to 7 x 14, that is 14 - 2 + 1 = 13.
4. Probability = 13/90.
**Fast method (30 seconds):** Count = floor(99/7) - floor(9/7) = 14 - 1 = 13. Always subtract the multiples below the range.
**Check:** 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98 is 13 numbers. Verified by script.
**Explain simply:**
- Count of multiples of k up to N is floor(N/k).
- Range count = last - first + 1 (inclusive).
**Likely follow-ups:** 1) Divisible by 5? 18/90 = 1/5. 2) Divisible by 7 among 1 to 100? 14/100 = 7/50.
**Common mistakes / traps:** Dividing 14 by 100 or counting 7 itself (a single digit) or using 99/7 = 14 without removing 7.

### Q54 ⭐⭐ 🟡 A card is drawn from a standard pack of 52. What is the probability that it is a red card or a face card (J, Q, K)?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Union of events with overlap handled correctly (addition rule).
**Say this in the interview:** "Red cards are 26. Face cards that are not red are the 6 black J, Q, K. So 26 + 6 = 32 out of 52, which is 8/13."
**Answer:** **8/13 (about 0.615)**
**Step-by-step working:**
1. Red cards: 26 (13 hearts + 13 diamonds).
2. Face cards (J, Q, K): 3 x 4 = 12; of these 6 are red and 6 are black.
3. Red and face (overlap): 6.
4. Red or face = 26 + 12 - 6 = 32.
5. Probability = 32/52 = 8/13.
**Check:** P = 26/52 + 12/52 - 6/52 = 32/52 = 8/13. Verified by script.
**Explain simply:**
- Addition rule: P(A or B) = P(A) + P(B) - P(A and B).
- Subtract the overlap because those cards were counted twice.
**Likely follow-ups:** 1) Red or king? 26 + 4 - 2 = 28, so 28/52 = 7/13. 2) Spade or face card (J, Q, K)? 13 + 12 - 3 = 22, so 22/52 = 11/26.
**Common mistakes / traps:** Adding 26 + 12 = 38 (38/52 = 19/26) without removing the 6 overlapping red face cards.

### Q55 ⭐⭐ 🟡 A fair die is rolled twice. What is the probability that the second number is greater than the first?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Using symmetry to avoid listing.
**Say this in the interview:** "Equal, less and greater are the only options. 6 of 36 pairs are equal, leaving 30, and half of those have second greater: 15/36 = 5/12."
**Answer:** **5/12 (about 0.417)**
**Step-by-step working:**
1. Total outcomes: 6 x 6 = 36.
2. Equal pairs (1,1) to (6,6): 6.
3. The other 30 split evenly between second greater and second smaller (symmetry): 15 each.
4. Probability = 15/36 = 5/12.
**Fast method (30 seconds):** Direct count: if first is 1, second can be 2 to 6 (5 ways); first 2: 4; 3: 3; 4: 2; 5: 1; 6: 0. Total 15.
**Check:** 5+4+3+2+1+0 = 15, matching (36 - 6)/2 = 15. Verified by script.
**Explain simply:**
- Symmetry: swapping the two dice turns 'second greater' into 'first greater', so those two are equally likely.
- Remove the ties first, then halve.
**Likely follow-ups:** 1) Probability the numbers are equal? 1/6. 2) Second at least the first? 21/36 = 7/12.
**Common mistakes / traps:** Answering 1/2 by forgetting that ties exist.

### Q56 ⭐⭐ 🟡 Six people stand in a row. In how many ways can they be arranged so that two particular people, A and B, are not next to each other?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Complement counting in permutations (total minus together).
**Say this in the interview:** "Total arrangements 6! = 720. Treat A and B as one block: 5! x 2 = 240 arrangements where they sit together. 720 - 240 = 480."
**Answer:** **480 ways**
**Step-by-step working:**
1. All arrangements of 6 people: 6! = 720.
2. Together: glue A and B into one block. Now 5 units arrange in 5! = 120 ways.
3. Inside the block A and B can swap: 2 ways, so 120 x 2 = 240.
4. Not together = 720 - 240 = 480.
**Fast method (30 seconds):** Another route: place the other 4 people first (4! = 24), which makes 5 gaps; choose 2 different gaps for A and B in order: 5 x 4 = 20; 24 x 20 = 480.
**Check:** the gap method gives 24 x 20 = 480, same. Verified by script.
**Explain simply:**
- 'Not next to each other' is easiest as total minus 'next to each other' (complement).
- Gluing people into a block is the standard 'together' trick; remember the block can be ordered internally.
**Likely follow-ups:** 1) Same question for 7 people? 5040 - 1440 = 3600. 2) A, B must be together among 6? 240.
**Common mistakes / traps:** Forgetting the factor 2 inside the block (giving 720 - 120 = 600).

### Q57 ⭐⭐ 🟡 A company has 120 employees: 70 men and 50 women. 20 men and 10 women resigned this year. If one employee is picked at random, what is the probability that the person resigned or is a woman?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Addition rule for 'or' with an overlap, from a two-way table.
**Say this in the interview:** "Resigned = 30, women = 50, women who resigned = 10. Union is 30 + 50 - 10 = 70 out of 120, so 7/12."
**Answer:** **7/12 (about 0.583)**
**Step-by-step working:**
1. Resigned = 20 men + 10 women = 30.
2. Women = 50.
3. Women who resigned (counted in both groups) = 10.
4. Resigned or woman = 30 + 50 - 10 = 70.
5. Probability = 70/120 = 7/12.
**Fast method (30 seconds):** Count the people who are neither: men who stayed = 70 - 20 = 50. So 120 - 50 = 70, and 70/120 = 7/12.
**Check:** complement route gives 120 - 50 = 70 people, same. Verified by script.
**Explain simply:**
- 'Or' in probability means at least one of the two conditions holds.
- Subtract the overlap (resigned women) so no one is counted twice.
**Likely follow-ups:** 1) Probability a man who stayed is picked? 50/120 = 5/12. 2) Probability the picked person is a woman given she resigned? 10/30 = 1/3.
**Common mistakes / traps:** Adding 30 + 50 = 80 and answering 2/3, double counting the 10 women who resigned.

### Q58 ⭐⭐ 🟡 Each of 3 employees independently stays with the company for the full year with probability 0.8. What is the probability that at least one of them leaves during the year?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Complement rule with independent events.
**Say this in the interview:** "'At least one leaves' is 1 minus 'nobody leaves'. Nobody leaves = 0.8 x 0.8 x 0.8 = 0.512, so the answer is 0.488."
**Answer:** **0.488 (48.8%)**
**Step-by-step working:**
1. Probability one person stays = 0.8.
2. All 3 stay (independent, so multiply) = 0.8 x 0.8 x 0.8 = 0.512.
3. At least one leaves = 1 - 0.512 = 0.488.
**Fast method (30 seconds):** 0.8 cubed: 0.8 x 0.8 = 0.64; 0.64 x 0.8 = 0.512. Subtract from 1.
**Check:** probabilities of 0, 1, 2, 3 leavers (0.512 + 0.384 + 0.096 + 0.008) add to 1, and the last three add to 0.488. Verified by script.
**Explain simply:**
- Independent means one person's decision does not change another's, so probabilities multiply.
- 'At least one' is hard to list directly; 'none' is a single case, so use the complement.
**Likely follow-ups:** 1) Probability exactly one leaves? 3 x 0.2 x 0.8 x 0.8 = 0.384. 2) With 5 employees, at least one leaves? 1 - 0.8^5 = 1 - 0.32768 = 0.67232.
**Common mistakes / traps:** Computing 3 x 0.2 = 0.6 (adding), which is not a valid probability rule here.

### Q59 ⭐⭐ 🟡 In how many ways can 8 employees be split into two unlabelled teams of 4 each?
**Asked at:** commonly asked (no company-specific report found); probability and P&C items are listed for TCS, Infosys, Wipro and Mu Sigma style tests in prep sites (unverified).
**What the interviewer is checking:** Dividing by symmetry when groups are unlabelled.
**Say this in the interview:** "Choose 4 of 8 for one team: 70 ways. But each split is counted twice (team and its mirror), so 70 / 2 = 35."
**Answer:** **35 ways**
**Step-by-step working:**
1. Choose 4 people out of 8: 8C4 = 8 x 7 x 6 x 5 / 24 = 70.
2. The remaining 4 form the other team automatically.
3. Teams are unlabelled, so choosing group X first and Y second is the same split as the reverse: divide by 2! = 2.
4. 70 / 2 = 35.
**Fast method (30 seconds):** Fix one person (say the first) in team 1; choose his 3 teammates from the other 7: 7C3 = 35. No halving needed.
**Check:** 7C3 = 7 x 6 x 5 / 6 = 35, matches. Verified by script.
**Explain simply:**
- Labelled groups (Team A, Team B) give 70; unlabelled groups divide by the number of ways to shuffle equal-sized groups.
- Equal sizes are what create the double counting.
**Likely follow-ups:** 1) 8 employees into Team A and Team B of 4 each? 70. 2) 6 employees into 3 unlabelled pairs? 6!/(2!^3 x 3!) = 15.
**Common mistakes / traps:** Answering 70 and missing that (X,Y) and (Y,X) are the same split.

### Q60 ⭐ 🟢 A fair die is rolled once and you are paid as many rupees as the number shown. What is the expected payout?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Expected value: probability-weighted average.
**Say this in the interview:** "Each number 1 to 6 has chance 1/6, so the expected payout is (1+2+3+4+5+6)/6 = 21/6 = 3.5 rupees."
**Answer:** **Rs 3.5**
**Step-by-step working:**
1. Outcomes 1 to 6, each with probability 1/6.
2. Expected value = sum of (value x probability) = (1 + 2 + 3 + 4 + 5 + 6) x 1/6.
3. Sum = 21; 21/6 = 3.5.
**Fast method (30 seconds):** Average of first and last of an evenly spaced list: (1 + 6)/2 = 3.5.
**Check:** (1+6)/2 = 3.5. Verified by script.
**Explain simply:**
- Expected value is the long-run average payout if you repeated the game many times.
- It need not be a value you can actually roll (you never roll 3.5).
**Likely follow-ups:** 1) Expected total of two dice? 7. 2) If you pay Rs 4 to play, expected profit? 3.5 - 4 = -0.5 rupees per play.
**Common mistakes / traps:** Thinking the answer must be a whole number, or picking the median-looking value 3.

### Q61 ⭐ 🟡 Four people are chosen at random. Assuming each of the 7 days of the week is equally likely as a birthday and independence, what is the probability that no two of them were born on the same day of the week?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Counting non-matching assignments (birthday-problem style).
**Say this in the interview:** "First person has 7 choices of day, second 6, third 5, fourth 4 for all-different, out of 7^4 total. 840/2401 = 120/343."
**Answer:** **120/343 (about 0.350)**
**Step-by-step working:**
1. Total ways for 4 people to have birth-days: 7 x 7 x 7 x 7 = 2401.
2. All different: 7 x 6 x 5 x 4 = 840.
3. Probability = 840/2401. Divide top and bottom by 7: 120/343.
**Fast method (30 seconds):** Multiply chances person by person: 1 x 6/7 x 5/7 x 4/7 = 120/343.
**Check:** 120/343 = 0.3499; 6/7 x 5/7 x 4/7 = 120/343, same. Verified by script.
**Explain simply:**
- This is the birthday problem with 7 'days' instead of 365.
- Each later person must avoid every day already taken, so choices shrink: 7, 6, 5, 4.
**Likely follow-ups:** 1) At least two share a day? 1 - 120/343 = 223/343. 2) With 8 people, a shared day is guaranteed (pigeonhole), since 8 > 7.
**Common mistakes / traps:** Using 7C4 / 7^4 or forgetting that the people are distinguishable (order matters).

### Q62 ⭐ 🟡 In how many ways can 10 identical laptops be distributed among 3 teams if any team may receive none?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Stars and bars: identical items into labelled boxes.
**Say this in the interview:** "Identical laptops into 3 teams with zeros allowed: C(10 + 3 - 1, 3 - 1) = C(12,2) = 66."
**Answer:** **66 ways**
**Step-by-step working:**
1. Let the teams get a, b, c laptops with a + b + c = 10 and each 0 or more.
2. Picture 10 stars (laptops) and 2 bars (dividers between 3 teams): 12 symbols in a row.
3. Choose positions of the 2 bars: 12C2 = 12 x 11 / 2 = 66.
**Fast method (30 seconds):** Formula: items n, boxes r gives C(n + r - 1, r - 1) when empty is allowed. Here n = 10, r = 3.
**Check:** counting a = 0 to 10 with b from 0 to 10 - a gives 11 + 10 + ... + 1 = 66. Verified by script.
**Explain simply:**
- Stars and bars counts ways to split identical objects among distinct receivers.
- If each team must get at least one, use C(9,2) = 36 instead.
**Likely follow-ups:** 1) Each team at least 1 laptop? 36. 2) 10 laptops among 4 teams, zeros allowed? C(13,3) = 286.
**Common mistakes / traps:** Using 3^10 (that is for distinct laptops) or 10C3.

### Q63 ⭐ 🔴 Using a shortcut rather than listing, what is the sum of all 3-digit numbers formed from the digits 1, 2, 3 without repetition?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Digit-position shortcut for sums of permutations.
**Say this in the interview:** "Each digit appears in each place 2 times. Sum of digits 6 times 2 times 111 = 1332."
**Answer:** **1332**
**Step-by-step working:**
1. Numbers: 123, 132, 213, 231, 312, 321 (3! = 6 numbers).
2. Each digit appears in each place (units, tens, hundreds) 6/3 = 2 times.
3. Sum of digits = 1 + 2 + 3 = 6. Contribution per place = 6 x 2 = 12.
4. Place values: 12 x 1 + 12 x 10 + 12 x 100 = 12 x 111 = 1332.
**Fast method (30 seconds):** Formula: (sum of digits) x (count / number of digits) x 111 = 6 x 2 x 111 = 1332. Limit: it works when every digit is used exactly once per number, or more generally when all digits are equally often in every place (as in follow-up 1, where each digit appears 6 times per place); it needs adjusting if a digit is repeated or 0 cannot lead.
**Check:** 123+132+213+231+312+321 = 1332 by direct addition. Verified by script.
**Explain simply:**
- By symmetry every digit is equally often in every position.
- 111 = 100 + 10 + 1 gathers all place values at once.
**Likely follow-ups:** 1) Same for digits 1, 2, 3, 4 taking 3 at a time? Each digit appears 6 times per place; 6 x 10 x 111 = 6660. 2) Same for 2, 3, 4? 9 x 2 x 111 = 1998.
**Common mistakes / traps:** Forgetting place values (adding 6 x 6 = 36) or using the wrong repeat count.

### Q64 ⭐ 🔴 How many 4-digit numbers divisible by 5 can be formed using the digits 0 to 9 without repetition?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Case split on the last digit with the 'no leading zero' constraint.
**Say this in the interview:** "A number divisible by 5 ends in 0 or 5. Count each case, taking care that the first digit cannot be 0. 504 + 448 = 952."
**Answer:** **952**
**Step-by-step working:**
1. Case 1, ends in 0: the other 3 places from the 9 remaining digits: 9 x 8 x 7 = 504.
2. Case 2, ends in 5: first digit cannot be 0 or 5, so 8 choices; second digit from the 8 left (0 allowed now): 8; third from 7: 7. Total 8 x 8 x 7 = 448.
3. Add: 504 + 448 = 952.
**Fast method (30 seconds):** Fill the restricted places first (last digit, then the first digit), then the free places.
**Check:** total 4-digit numbers without repetition = 9 x 9 x 8 x 7 = 4536; 952 is the share ending in 0 or 5, consistent. Verified by script by brute force.
**Explain simply:**
- Divisible by 5 means last digit 0 or 5.
- The case split is needed because 0 behaves differently as a last digit than 5 does.
**Likely follow-ups:** 1) Divisible by 2 (4-digit, no repetition)? Ends in 0: 504; ends in 2,4,6,8: 4 x 8 x 8 x 7 = 1792; total 2296. 2) Divisible by 10? 504.
**Common mistakes / traps:** Using 9 x 8 x 7 for both cases (the ends-in-5 case must exclude a leading 0 and the 5 itself), or ignoring the no-leading-zero rule.

### Q65 ⭐ 🔴 How many 5-letter arrangements (meaningful or not, no letter repeated) can be formed from the word EQUATIONS using exactly 3 vowels and 2 consonants?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Select first, then arrange (combination then permutation).
**Say this in the interview:** "EQUATIONS has 5 vowels (E, U, A, I, O) and 4 consonants (Q, T, N, S). Pick 3 vowels and 2 consonants, then arrange the 5 letters."
**Answer:** **7200**
**Step-by-step working:**
1. Letters: E, Q, U, A, T, I, O, N, S: 9 distinct letters.
2. Vowels: E, U, A, I, O = 5. Consonants: Q, T, N, S = 4.
3. Choose 3 vowels: 5C3 = 10. Choose 2 consonants: 4C2 = 6.
4. Arrange the 5 chosen letters in a row: 5! = 120.
5. Total = 10 x 6 x 120 = 7200.
**Check:** 10 x 6 = 60 selections, 60 x 120 = 7200. Verified by script by brute force over all 5-letter arrangements.
**Explain simply:**
- Combination (choose) first because the choosing step ignores order; permutation (arrange) afterwards because position matters.
- 'Exactly 3 vowels' means 3 and no more.
**Likely follow-ups:** 1) Vowels must all be together? Treat the 3 vowels as a block: 10 x 6 x (3! x 3!) = 2160 (block of 3 vowels arranged inside 3!, block plus 2 consonants 3!). 2) Just 5-letter arrangements of any letters? 9P5 = 15120.
**Common mistakes / traps:** Forgetting the arrangement step (answering 60), or miscounting the vowels: here E, U, A, I, O are the 5 vowels and Q, T, N, S are the 4 consonants.

### Q66 ⭐ 🔴 In how many ways can 12 employees be divided into three labelled project groups of 4 each?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Multinomial coefficient for labelled groups.
**Say this in the interview:** "Choose 4 for Group 1 (12C4), then 4 of the remaining 8 for Group 2 (8C4), the last 4 form Group 3. 495 x 70 = 34650."
**Answer:** **34650 ways**
**Step-by-step working:**
1. Group 1: 12C4 = 495.
2. Group 2 from the remaining 8: 8C4 = 70.
3. Group 3 gets the last 4: 4C4 = 1.
4. Total = 495 x 70 x 1 = 34650.
**Fast method (30 seconds):** Formula: 12! / (4! x 4! x 4!) = 479001600 / 13824 = 34650.
**Check:** 12!/(4!)^3 = 479001600/13824 = 34650. Verified by script.
**Explain simply:**
- Groups are labelled (Project A, B, C), so which group a person joins matters.
- If groups were unlabelled, divide by 3! = 6: 34650/6 = 5775.
**Likely follow-ups:** 1) Same but unlabelled groups? 5775. 2) 12 employees into groups of 3, 4, 5 (labelled by size)? 12!/(3! 4! 5!) = 27720.
**Common mistakes / traps:** Dividing by 3! when the groups are labelled (or not dividing when they are not).

### Q67 ⭐ 🔴 If three fair dice are rolled, what is the probability that the sum is 10?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Counting favourable outcomes among 6^3 = 216.
**Say this in the interview:** "Count triples with sum 10: there are 27 of them out of 216, so 27/216 = 1/8."
**Answer:** **1/8 (0.125)**
**Step-by-step working:**
1. Total outcomes = 6 x 6 x 6 = 216.
2. Combinations of three numbers (1 to 6) with sum 10: {1,3,6}, {1,4,5}, {2,2,6}, {2,3,5}, {2,4,4}, {3,3,4}.
3. Orderings: {1,3,6} 6, {1,4,5} 6, {2,3,5} 6 (three distinct numbers: 3! = 6 each) = 18; {2,2,6} 3, {2,4,4} 3, {3,3,4} 3 (two the same: 3 each) = 9.
4. Favourable = 18 + 9 = 27.
5. Probability = 27/216 = 1/8.
**Fast method (30 seconds):** Sums 10 and 11 are the most likely totals (27 ways each); sums 9 and 12 have 25 ways each.
**Check:** counts of sums 3 to 18 are symmetric around 10.5 and total 216; sum 10 gives 27. Verified by script.
**Explain simply:**
- Count by type: three different numbers have 6 orderings, two equal have 3, all equal have 1.
- Listing the number-sets first keeps the count organised.
**Likely follow-ups:** 1) Sum 9? 25/216. 2) Sum 18? 1/216.
**Common mistakes / traps:** Counting only the 6 number-sets (6/216) and forgetting orderings, or missing a set.

### Q68 ⭐ 🔴 In how many ways can 5 men and 5 women be seated around a circular table so that men and women alternate?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Circular arrangement with an alternating constraint.
**Say this in the interview:** "Fix the 5 men around the table first: (5-1)! = 24 ways. That leaves 5 gaps, one for each woman: 5! = 120. 24 x 120 = 2880."
**Answer:** **2880 ways**
**Step-by-step working:**
1. Seat the men around the circle: (5 - 1)! = 24 (rotating everyone gives the same arrangement, so one seat is fixed).
2. The 5 men create 5 gaps between them; each gap takes exactly one woman.
3. Arrange the 5 women in the gaps: 5! = 120.
4. Total = 24 x 120 = 2880.
**Fast method (30 seconds):** Formula: (n - 1)! x n! for n men and n women alternating = 4! x 5!.
**Check:** 24 x 120 = 2880; brute force with one man fixed (4! x 5!) agrees. Verified by script.
**Explain simply:**
- In a circle only relative positions matter, so n people give (n - 1)! arrangements, not n!.
- Alternating forces women into the gaps, which are then distinct seats.
**Likely follow-ups:** 1) 4 men and 4 women alternating? 3! x 4! = 144. 2) 6 people around a table, no restriction? 5! = 120.
**Common mistakes / traps:** Using 5! x 5! = 14400 (forgetting that rotations are identical).

### Q69 ⭐ 🔴 Four employees each hand in a laptop, and the four laptops are returned at random, one to each employee. In how many ways can the laptops be returned so that nobody gets their own (derangements of 4)?
**Asked at:** commonly asked (no company-specific report found); a harder or gap-fill pattern from standard aptitude practice, not tied to any company report.
**What the interviewer is checking:** Derangements: nobody gets their own item.
**Say this in the interview:** "Use inclusion-exclusion (count all 24 returns, subtract those where someone gets their own, add back the overlaps): D4 = 4! (1 - 1 + 1/2 - 1/6 + 1/24) = 9."
**Answer:** **9 ways**
**Step-by-step working:**
1. Total returns: 4! = 24.
2. D4 = 4! x (1/0! - 1/1! + 1/2! - 1/3! + 1/4!).
3. = 24 x (1 - 1 + 0.5 - 0.1667 + 0.0417) = 24 x 0.375 = 9.
**Fast method (30 seconds):** Recurrence: D(n) = (n - 1) x (D(n-1) + D(n-2)). D2 = 1, D3 = 2, so D4 = 3 x (2 + 1) = 9.
**Check:** recurrence gives 3 x (2 + 1) = 9, and brute force of all 24 permutations finds 9 with no fixed point. Verified by script.
**Explain simply:**
- A derangement is a rearrangement where no item stays in its original place.
- D(n) is about n!/e (e = 2.718), so D4 is 24/2.718, about 8.8, rounding to 9.
**Likely follow-ups:** 1) D5? 4 x (9 + 2) = 44. 2) Probability nobody gets their own laptop (4 people)? 9/24 = 3/8.
**Common mistakes / traps:** Stopping the inclusion-exclusion too early, for example removing only the 6 returns where one named employee gets their own (24 - 6 = 18) or removing 4 (24 - 4 = 20); the overlaps must be added back.

