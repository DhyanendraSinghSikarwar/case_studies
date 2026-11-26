# Chapter 30 Answer Key: Proof Techniques

All results were re-checked by code (brute force over ranges of whole numbers for the true statements, and a direct search for the counterexamples).

## Self-check answers

1. **False.** The claim is a "for all" claim ("every employee"). One employee without a laptop is a counterexample, and one counterexample is enough to make it false.
2. **No.** Three examples cannot cover all numbers. The claim is in fact false: 4 is a number you could have picked and it is even.
3. Checking examples looks at some cases and can only suggest a pattern or find a counterexample. A proof is an argument that covers every case.

---

## Practice answers

**Q1** 🟢 **True (direct proof).**
1. Write the two odd numbers as 2a + 1 and 2b + 1. *Why:* that is the definition of odd.
2. Add: (2a + 1) + (2b + 1) = 2a + 2b + 2. *Why:* the two 1s combine into 2.
3. Pull out 2: 2(a + b + 1). *Why:* each part has a factor 2.
4. a + b + 1 is a whole number, so the result is 2 times a whole number, which is even. Proved.

**Q2** 🟢 **True (direct proof).**
1. A multiple of 4 is 4m for some whole number m.
2. 4m = 2 × (2m). *Why:* 4 is 2 times 2.
3. 2m is a whole number, so 4m is 2 times a whole number: a multiple of 2. Proved.

**Q3** 🟢 **False.** Counterexample: 2 is prime and even (its only divisors are 1 and 2). One case is enough to kill "every prime is odd".

**Q4** 🟢 **True, and yes, here checking is a proof.**
1. The statement is about a finite, complete list of five employees.
2. Check each row: 74, 88, 71, 92, 70 are all 70 or more.
3. Since every case on the list was checked, nothing is left uncovered. (This works only because the list is the *whole* group and is finite.)

**Q5** 🟢 **False.** Lata works the evening shift. She is a Support team member who does not work mornings, so she is a counterexample.

**Q6** 🟢 **False.** Counterexample: 2 and 3 are both prime and 2 + 3 = 5, which is odd. (Other examples: 2 + 5 = 7, 2 + 7 = 9.)

**Q7** 🟢 **False.** Counterexample: 3 is a multiple of 3 but not a multiple of 6 (3 is not 6 times a whole number). Another: 9.

**Q8** 🟡 **True (direct proof).**
1. Write the odd number as n = 2k + 1.
2. n² = (2k + 1)(2k + 1) = 4k² + 4k + 1. *Why:* expand the brackets: 2k times 2k is 4k², then 2k and 2k give 4k, then 1.
3. 4k² + 4k + 1 = 2(2k² + 2k) + 1. *Why:* pull a 2 out of the first two parts.
4. That is "2 times a whole number, plus 1": odd. Proved.

**Q9** 🟡 **True (direct proof, two cases).**
1. Split into cases because every whole number is even or odd.
2. **Case n even.** n² is even (even times even is even, since n × n = 2k × n = 2(kn)) and n is even; even + even is even (Example 1).
3. **Case n odd.** n² is odd (Q8) and n is odd; odd + odd is even (Q1).
4. Both cases give even. Proved. (A shorter route: n² + n = n(n + 1), and one of two consecutive numbers is always even, so the product is even.)

**Q10** 🟡 **False.** Counterexample: n = 1. Then n² = 1 and 2n = 2, and 1 is less than 2. (It works for n = 0, 2, 3, ... which is why the failing case is easy to miss.)

**Q11** 🟡 **True (direct proof by elimination).**
1. Two whole numbers are (even, even), (odd, odd) or (even, odd) in some order.
2. (even, even) gives an even sum (Example 1), so it cannot give an odd sum.
3. (odd, odd) gives an even sum (Q1), so it cannot either.
4. The only case left is one even and one odd. Proved.

**Q12** 🟡 **True (direct proof).**
1. Call the numbers n, n + 1, n + 2.
2. Sum = n + n + 1 + n + 2 = 3n + 3. *Why:* three n's make 3n, and 1 + 2 makes 3.
3. 3n + 3 = 3(n + 1), which is 3 times a whole number. Proved.

**Q13** 🟡 **False.** Counterexample: 12 is divisible by 4 (12 = 4 × 3) and by 6 (12 = 6 × 2), but not by 24. (36 also works.) The correct statement is that it must be divisible by 12.

**Q14** 🟡 **True (proof by contradiction).**
1. Assume no two of the 8 employees were hired on the same weekday.
2. Then the 8 employees have 8 different weekdays.
3. There are only 7 weekdays. Impossible.
4. So at least two share a hiring weekday. Proved.

**Q15** 🔴 **False.** Test n = 0, 1, 2, ...: the values 17, 19, 23, 29, 37, 47, 59, 73, 89, 107, 127, 149, 173, 199, 227, 257 are all prime, but n = 16 gives 256 + 16 + 17 = 289 = 17 × 17, not prime. Counterexample: n = 16. (Sixteen agreeing cases, still false.)

**Q16** 🔴 **True (proof by contradiction).**
1. Assume n² is a multiple of 3 but n is **not** a multiple of 3.
2. Then n leaves remainder 1 or 2 when divided by 3: n = 3k + 1 or n = 3k + 2.
3. If n = 3k + 1: n² = 9k² + 6k + 1 = 3(3k² + 2k) + 1. Remainder 1.
4. If n = 3k + 2: n² = 9k² + 12k + 4 = 3(3k² + 4k + 1) + 1. Remainder 1.
5. In both cases n² leaves remainder 1, so it is not a multiple of 3. That contradicts our assumption.
6. So n is a multiple of 3. Proved.

**Q17** 🔴 **True (proof by contradiction).**
1. Assume 4k + 2 equals n × n for some whole number n.
2. n is even or odd.
3. **If n is even**, n = 2m, so n² = 4m², a multiple of 4. But 4k + 2 leaves remainder 2 when divided by 4, so it is not a multiple of 4. Clash.
4. **If n is odd**, n² is odd (Q8). But 4k + 2 = 2(2k + 1) is even. Clash.
5. Both cases are impossible, so no number of the form 4k + 2 is a perfect square. Proved.

**Q18** 🔴 **True (proof by contradiction).**
1. Dividing by 4, the remainder is 0, 1, 2 or 3: four possible remainders.
2. Assume no two of the five numbers share a remainder. Then the five numbers have five different remainders.
3. Only four remainders exist. Impossible.
4. So two numbers have the same remainder r: a = 4p + r and b = 4q + r.
5. a minus b = 4p minus 4q = 4(p minus q), a multiple of 4. Proved.

**Q19** 🔴 **False.** Counterexample: 2 and 3. Their product is 6, which is even, but 3 is not even. (Also 1 and 4: product 4.)

**Q20** 🔴 **True (proof by contradiction).**
1. Assume that in every month at most 2 of the 25 people were born.
2. Then the total is at most 12 months times 2 people = 24 people.
3. But there are 25 people. Impossible.
4. So some month has at least 3 of them. Proved.
