# Chapter 31 Answer Key: Intro to Mathematical Induction

All formulas below were re-checked by code for n from 1 to 299, and the voucher results (Example 4, Q9) were found by exhaustive search of all combinations. The Example 5 "flawed" formula was confirmed to be exactly 1 more than the true sum for n = 1 to 4.

## Self-check answers

1. You need the passing-along rule: "whenever any domino falls, it knocks over the next one". Then domino 1 falls, which makes 2 fall, and so on.
2. **No.** Five matching cases are evidence, not a proof. Induction (or another full argument) is needed to be sure about n = 6 and beyond. (Example 5 shows a rule that fails at n = 1 even though its step works; Chapter 30 Example 3 shows a pattern that held for ten values and then failed.)
3. Because without the first fall, nothing ever starts. Dominoes that would pass the fall along are useless if nobody pushes the first one.

---

## Practice answers

**Q1** 🟢
1. Fact (A) "you can stand on step 1" is the **base case** (the first domino).
2. Fact (B) "from any step you can climb to the next" is the **inductive step** (each domino knocks over the next).
3. Together: you reach step 1, so step 2, so step 3, and so on up to step 40. **Conclusion:** you can reach step 40 (and any step on the staircase).

**Q2** 🟢 Nothing can be concluded about reaching any particular step. Fact (B) only says "if you are on a step, you can go to the next"; without (A) you never get onto the first step, so the chain never starts. (You might reach step 40 for some other reason, but this reasoning does not show it.)

**Q3** 🟢

| n | Sum added by hand | n(n + 1) / 2 |
|---|---|---|
| 1 | 1 | 1 × 2 / 2 = 1 |
| 2 | 1 + 2 = 3 | 2 × 3 / 2 = 3 |
| 3 | 1 + 2 + 3 = 6 | 3 × 4 / 2 = 6 |
| 4 | 1 + 2 + 3 + 4 = 10 | 4 × 5 / 2 = 10 |
| 5 | 1 + 2 + 3 + 4 + 5 = 15 | 5 × 6 / 2 = 15 |

All five rows agree. This is only a check of five cases; it does not show the formula works for n = 6 or 6,000. An induction proof also needs the step "if it works for k then it works for k + 1" for a general k.

**Q4** 🟡 **Claim:** 1 + 4 + 7 + ... + (3n minus 2) = n(3n minus 1) / 2.
1. **Base case (n = 1):** left side is 3 × 1 minus 2 = 1. Right side: 1 × (3 minus 1) / 2 = 1 × 2 / 2 = 1. Match.
2. **Assume** the claim for k: 1 + 4 + ... + (3k minus 2) = k(3k minus 1) / 2.
3. **Next term:** the term after (3k minus 2) is 3(k + 1) minus 2 = 3k + 1.
4. **Add it:** sum to k + 1 = k(3k minus 1) / 2 + (3k + 1) = (3k² minus k + 6k + 2) / 2 = (3k² + 5k + 2) / 2. *Why:* write 3k + 1 as (6k + 2) / 2 to share the denominator.
5. **Factor:** 3k² + 5k + 2 = (k + 1)(3k + 2). Check: (k + 1)(3k + 2) = 3k² + 2k + 3k + 2. Yes.
6. **Target for n = k + 1:** (k + 1)(3(k + 1) minus 1) / 2 = (k + 1)(3k + 2) / 2. It matches step 5.
7. By induction the claim is true for every n. (Quick check: n = 4 gives 1 + 4 + 7 + 10 = 22 and 4 × 11 / 2 = 22.)

**Q5** 🟡 **Claim:** handshakes among n people = n(n minus 1) / 2.
1. **Base case (n = 1):** one person has 0 handshakes; formula 1 × 0 / 2 = 0. Match. (n = 2 gives 1 handshake and 2 × 1 / 2 = 1, also fine.)
2. **Assume** k people have k(k minus 1) / 2 handshakes.
3. **New arrival:** the (k + 1)-th person shakes hands with each of the k people already there: k new handshakes. *Why:* every earlier handshake is still counted once; the newcomer only adds handshakes involving themselves.
4. **Total:** k(k minus 1) / 2 + k = (k² minus k + 2k) / 2 = (k² + k) / 2 = k(k + 1) / 2.
5. **Target for n = k + 1:** (k + 1)((k + 1) minus 1) / 2 = (k + 1) × k / 2. It matches.
6. Proved. Example: 10 people give 10 × 9 / 2 = 45 handshakes.

**Q6** 🟡 **Claim:** 5 + 10 + ... + 5n = 5n(n + 1) / 2.
1. **Base case (n = 1):** left is 5; right is 5 × 1 × 2 / 2 = 5. Match.
2. **Assume** 5 + 10 + ... + 5k = 5k(k + 1) / 2.
3. **Add the next week's saving,** 5(k + 1): total = 5k(k + 1) / 2 + 5(k + 1).
4. **Pull out 5(k + 1):** = 5(k + 1) × (k / 2 + 1) = 5(k + 1)(k + 2) / 2.
5. **Target for n = k + 1:** 5(k + 1)((k + 1) + 1) / 2 = 5(k + 1)(k + 2) / 2. Match.
6. Proved. **After 12 weeks:** 5 × 12 × 13 / 2 = 780 / 2 = **390 rupees**.

**Q7** 🟡 **Claim:** 2^n is bigger than n.
1. **Base case (n = 1):** 2^1 = 2, which is bigger than 1. True.
2. **Assume** 2^k is bigger than k.
3. **Step:** 2^(k+1) = 2 × 2^k. Since 2^k is bigger than k, 2 × 2^k is bigger than 2k.
4. For k at least 1, 2k is at least k + 1 (because k is at least 1, so 2k = k + k is at least k + 1).
5. Chain: 2^(k+1) is bigger than 2k, and 2k is at least k + 1, so 2^(k+1) is bigger than k + 1. That is the claim for k + 1.
6. Proved. (Values: 2, 4, 8, 16, 32 against 1, 2, 3, 4, 5.)

**Q8** 🔴 **Claim:** 4^n minus 1 is a multiple of 3.
1. **Check the hint's identity:** 4 × (4^k minus 1) + 3 = 4^(k+1) minus 4 + 3 = 4^(k+1) minus 1. Correct.
2. **Base case (n = 1):** 4 minus 1 = 3, a multiple of 3.
3. **Assume** 4^k minus 1 = 3m for some whole number m.
4. **Step:** 4^(k+1) minus 1 = 4 × (3m) + 3 = 12m + 3 = 3(4m + 1). *Why:* this is 3 times a whole number.
5. So 4^(k+1) minus 1 is a multiple of 3. Proved. (Values: 3, 15, 63, 255 are 3 × 1, 3 × 5, 3 × 21, 3 × 85.)

**Q9** 🔴
**(a)** Trying every combination of 4s and 7s, the amounts from 1 to 17 that **cannot** be paid are **1, 2, 3, 5, 6, 9, 10, 13, 17**. (For example, 17 would need 4a + 7b = 17: b = 0 gives 17 not a multiple of 4; b = 1 gives 10, no; b = 2 gives 3, no.) The payable ones are 4, 7, 8, 11, 12, 14, 15, 16.
**(b)** Base cases (four in a row, because the step reaches back 4):
- 18 = 4 + 7 + 7
- 19 = 4 + 4 + 4 + 7
- 20 = 4 × 5
- 21 = 7 × 3

Step: take any amount n of 22 or more and assume every amount from 18 up to n minus 1 can be paid. Then n minus 4 is at least 18 and below n, so it can be paid. Add one 4-rupee voucher and n is paid. So every amount from 18 on can be paid. (This is the same domino idea, except that each domino is knocked over by the one four places back, and we assume all earlier amounts, not only the one just before.) *Why four base cases:* the step uses the amount four earlier, so we must have started the chain at four different amounts.

**Q10** 🔴 The step fails when k = 1, going from groups of 1 to groups of 2.
1. With 2 employees, A and B: remove A, the remaining group is just {B}; remove B, the remaining group is just {A}.
2. The argument says "the two groups of k overlap, so A, B and everyone else share a size". For k = 1 the two groups {B} and {A} do **not** overlap at all, so there is nothing linking A's size to B's.
3. For k at least 2 the overlap argument is fine, but it needs "every group of 2 shares a size" as its starting point, and that was never proved. So the chain breaks at the first link: the base case n = 1 does not lead to n = 2. The step is valid only when the overlap exists (k at least 2), so it cannot be used to get from 1 to 2.
4. The conclusion is plainly false (two people can have different shoe sizes). **Lesson:** the step must work for *every* k from the base case on, including the first one.
