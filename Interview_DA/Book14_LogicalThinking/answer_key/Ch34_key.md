# Chapter 34 answer key: Debugging Your Reasoning

All results recomputed by code (Q13 checked by listing every possible height order).

## Self-check answers

1. The faulty step is "total discount is 30%". The second 10% is taken off the already reduced price, not the original. Price: 500 x 0.80 = 400; 400 x 0.90 = 360. Correct price 360 (a 28% total discount). Wrong base.
2. The final answer is wrong, because it is built on step 2's wrong number. Report step 2, the first faulty step, as the fault; steps 3 and 4 are correct but carry the damage.
3. Any two of: plug in simple numbers (for example 100); check units; put the answer back into the problem; test whether it is possible or reasonable (for example a share above 100% is impossible).

## Practice answers

**Q1.** First faulty step: Step 1. 90 / 12 = 7.5, not 8.5. Bug: arithmetic slip. Correct: 7 x 7.5 = 52.5. Reverse check: 12 pens at 7.5 = 90.

**Q2.** First faulty step: Step 2 ("a 10% cut cancels a 10% raise"; step 1 is right). The cut is 10% of 44,000, not of 40,000. Bug: wrong base. Correct: 44,000 x 0.90 = 39,600 (down 400).

**Q3.** First faulty step: Step 1. 2 hours 30 minutes is 2.5 hours (30 minutes is half an hour), not 2.30. Bug: unit mismatch (clock time versus decimal hours). Correct: 150 / 2.5 = 60 km per hour.

**Q4.** First faulty step: Step 1. Counting inclusive from 5 to 20 means 20 - 5 + 1 = 16 steps. Bug: off-by-one. Check with a tiny case: steps 5 to 6 are 2 steps, but 6 - 5 = 1.

**Q5.** First faulty step: Step 2. Rice per person is 75 g, so 10 people need 75 x 10, not 75 + 10. Bug: wrong operation. Correct: 750 g. Check: 10 people is 2.5 times 4 people; 300 x 2.5 = 750.

**Q6.** First faulty step: Step 1 (weights ignored). Total pay: 4 x 50,000 = 200,000; 16 x 30,000 = 480,000; sum 680,000 over 20 people = 34,000. Bug: average of averages. Reasonableness: most staff are in Y (30,000), so the overall figure should be nearer 30,000 than 40,000.

**Q7.** First faulty step: Step 2. The rule is: priority implies answered within 2 hours. Being answered in 1 hour does not show the ticket was priority; non-priority tickets may also be answered fast. Bug: converse error. Correct conclusion: nothing can be concluded about T-17's priority.

**Q8.** First faulty step: Step 4 (steps 1 to 3 are right: both 5, tea only 30, coffee only 25). The sum must include the both group: 30 + 25 + 5 = 60, which equals the class, so nobody likes neither. Bug: double counting setup / forgetting a group. Answer: 0 like neither (consistent with "everyone likes at least one").

**Q9.** First faulty step: Step 2. A percentage change uses the starting value (80) as base: 20 / 80 = 25% fall, not 20 / 60. Bug: wrong base. Check: 25% of 80 is 20, and 80 - 20 = 60.

**Q10.** First faulty step: Step 2. More workers means less time, not more. Total work = 5 x 6 = 30 worker-days; with 10 workers: 30 / 10 = 3 days. Bug: wrong direction (inverse relationship treated as direct). Check: 10 workers x 3 days = 30 worker-days.

**Q11.** First faulty step: Step 3. 6 x 5 = 30 counts ordered pairs, so "Asha then Ravi" and "Ravi then Asha" are counted as two teams but are the same team. Each team is counted twice: 30 / 2 = 15. Bug: double counting. Check by listing: 6 people give 5 + 4 + 3 + 2 + 1 = 15 distinct pairs.

**Q12.** First faulty step: Step 2 (generalising from 10 people in one office to 4,000). Bug: hasty generalisation. The answers alone allow: lowest 10 / 4,000 = 0.25% (only those 10 prefer remote work), highest (10 + 3,990) / 4,000 = 100%. So the sample says almost nothing about the whole company. A fair statement: "All 10 people asked in the Pune office prefer remote work."

**Q13.** First faulty step: Step 2. Knowing D > C and B > C does not order D and B; C is below both. Bug: unsupported step. Listing all 24 height orders that satisfy A > B > C and D > C, D is taller than A in some and shorter in others, so it cannot be decided. Correct answer: cannot tell whether A or D is taller (A is taller than B and C; D is only known to be taller than C).

**Q14.** First faulty step: Step 1. Successive discounts apply to the reduced price. 2,000 x 0.80 = 1,600; 1,600 x 0.70 = 1,120. Bug: wrong base. Correct price 1,120 (a 44% total discount, not 50%).

**Q15.** First faulty step: Step 2. The problem says rent is 30% of the original salary: 0.30 x 60,000 = 18,000, not 30% of 54,000. Bug: misread condition. Correct: after tax 54,000; after rent 54,000 - 18,000 = 36,000; savings 20% of 36,000 = 7,200. (Step 1 is right; steps 3 and 4 were calculated correctly from the wrong rent figure, giving 7,560 instead of 7,200.)
