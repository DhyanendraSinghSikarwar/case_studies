# Chapter 5 answer key: Quantifiers and Negation

Every negation below was checked by computer against all small groups (0 to 3 items, and up to 5 for counting statements) with every combination of properties; in each group exactly one of the statement and its negation is true. Nested statements were checked against all small tables.

## Self-check answers

1. "Some stall in the market is not open." (At least one stall is closed.) One closed stall is enough to break "all open".
2. **False.** One customer who did not pay is a counterexample, and a counterexample defeats "every".
3. **Yes.** "Some" means "at least one", so it is still true when all products are on sale.

## Practice answers

**Q1** Negation: **Some intern did not attend the orientation.** Why: "all" is broken by one exception; the property flips to "did not attend". (Not "No intern attended", which is much stronger.)

**Q2** Negation: **Some parcel arrived damaged.** Why: "no" means zero damaged; it fails when there is at least one.

**Q3** Negation: **No staff member works night shifts.** Why: "some" (at least one) fails only when there are zero.

**Q4** Negation: **Some bus on route 12 did not run on time today** (at least one bus was late). Why: "every" fails with one exception.

**Q5** Negation: **Every candidate scored 90 or below** (no candidate scored above 90). Why: "at least one scored above 90" fails only when none did, so everyone is at 90 or below. Note: "below 90" would be wrong; a candidate with exactly 90 is not above 90.

**Q6** Answer: **(b)**. The original is "at least one driver has no licence". It fails only if every driver has a licence. (a) can be true together with the original (one licensed, one unlicensed). (c) is much stronger than needed. (d) is just a copy of the original with an extra condition. Checked: only (b) always disagrees with the original.

**Q7**
- (a) False: Bilal (Night) and Esha (Night) work nights. Negation: **Some employee does not work the day shift.**
- (b) True: Esha lives in Bengaluru.
- (c) True: the night-shift employees are Bilal (Pune) and Esha (Bengaluru); neither is in Hyderabad.
- (d) False: Bilal is in Pune and works nights. Negation: **Some Pune employee does not work the day shift.**

**Q8** Negation: **Every seller offers free delivery.** Why: "Not every" already is the negation of "every"; negating it again removes the "not" (double negation cancels).

**Q9** Negation: **At least one of the three test cases failed.** Why: "none failed" means zero failures; it fails when there is one or more.

**Q10** Negation: **Some new joiner does not have a laptop or does not have an ID card** (lacks at least one of them). Why: "every" becomes "some"; the "and" inside becomes "or" once negated, because one missing item breaks the "and".

**Q11** Negation: **No report is both accurate and on time**, which means every report is inaccurate or late (or both). Why: "some" becomes "none"; "none are accurate-and-on-time" means each report fails at least one of the two. Trap: "No report is accurate and no report is on time" is too strong; a report that is accurate but late is allowed.

**Q12** Negation: **Some customer neither paid in cash nor used a card.** Why: "every" becomes "some"; the inside "cash or card" becomes "not cash and not card" (both fail).

**Q13** Negation: **At most 2 of the 10 trainees passed** (fewer than 3). Why: 3 or more fails only when the number is 0, 1 or 2.

**Q14** Negation: **Either no machine is faulty, or two or more machines are faulty.** Why: "exactly one" is false for every count except 1, which means 0 or 2 or more. Trap: "No machine is faulty" alone ignores the "two or more" case.

**Q15**
- (a) Orders above 500: O2, O3, O4. O3 was not delivered. **False**; counterexample **O3**.
- (b) Orders above 1,000: O2 (paid), O4 (unpaid). **True**; **O4** proves it.
- (c) Orders below 500: O1 and O5, both delivered. **True** (no order below 500 is undelivered).
- (d) Delivered orders: O1, O2, O4, O5. O4 is unpaid. **False**; counterexample **O4**.

**Q16** Negation: **Some manager has no employee reporting to them.** Why: outer "every manager" becomes "some manager"; inner "at least one employee reports" becomes "no employee reports".

**Q17** Negation: **Every employee has missed at least one course on the list** (nobody has completed all of them). Why: "some employee completed every course" becomes "no employee completed every course"; "not every course completed" is "at least one course missed". Trap: "No employee has completed any course" is too strong.

**Q18** The statement is "For every order above 500, it gets free delivery". Negation: **Some order above 500 does not get free delivery.** Why: "every" becomes "some"; the property flips to "does not get free delivery". Orders at or below 500 do not matter here.

**Q19** The true negation pairs are **(ii) and (iii)**.
- (i) No: both are false if the menu has a mix of vegetarian and non-vegetarian dishes.
- (ii) Yes: "some vegetarian" and "none vegetarian" always disagree.
- (iii) Yes: "every dish is under 200" fails exactly when some dish is 200 or more.
- (iv) No: both are true on a mixed menu.

**Q20** Negation: **There is a product for which no supplier can deliver within 2 days.** Why: outer "for every product" becomes "for some product"; inner "there is a supplier who can" becomes "no supplier can".

**Q21** Negation: **On every day of the week, at least one shop in the market was closed.** Why: outer "there is a day" becomes "for every day"; inner "every shop was open" becomes "some shop was closed". Trap: "On every day, every shop was closed" is much too strong.

**Q22**
(a) Teams with a senior member that missed target: **T2 and T6**.
(b) Teams without a senior member (**T3 and T5**) can never refute the claim, whether they met target or not, because the claim says nothing about them. (T5 met target and T3 did not; neither matters.)
(c) The claim is **false**, since counterexamples exist. Its negation, "Some team with a senior member did not meet its target", is true.

**Q23**
(a) **Yes.** If the folder holds two files, one encrypted and one not, S1 is false (one is unencrypted) and S2 is false (one is encrypted).
(b) **Only if the folder is empty.** With no files, neither statement can be broken, so both are (vacuously) true. With at least one file they cannot both be true.
(c) **No**, because a negation can never leave both false, and here both can be false (mixed folder). The true negation of S1 is "Some file is not encrypted".

**Q24**
(a) **No.** 3 claims remain unchecked; any of them could be fraudulent. A "none" claim can only be confirmed by checking all 8.
(b) **A single fraudulent claim** among the remaining 3 would prove the manager wrong.
(c) Checking all remaining 3 and finding no fraud among them would confirm the manager is right (all 8 clean).

**Q25** The negation is **Bob's**: "Some employee who completed the training did not pass the test." Why: "every ... passed" becomes "some ... did not pass".
- Alice is wrong. Group: two trainees who completed the training, one passed and one failed. The original is false (one failed). Alice's "none passed" is also false (one passed). A negation can never leave both false.
- Carol is wrong. Same group: Carol's "every one failed" is false (one passed), and the original is false too.
- Bob in the same group: true (one failed) while the original is false: they disagree, as a negation must.
