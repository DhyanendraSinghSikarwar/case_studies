# Book 13 — Logical Reasoning & Analytical Thinking | Part 3: Inequalities, Comparison, Ranking and Order Puzzles 🟢🟡

**Target:** 50 questions | **Actual:** 51 questions
**Scope:** Direct and coded inequalities, either-or cases, comparison and ranking (ties, percentiles, rank arithmetic), order and position puzzles on queues, schedules and races, and counting of possible orders; seating and arrangements are in Part 4.

### Q1 ⭐⭐⭐ 🟢 How do you test whether a conclusion follows from a direct inequality chain such as P > Q >= R = S, and when do you say "cannot be determined"?
**Asked at:** commonly asked (no company-specific report found); inequality questions are said to appear in placement reasoning sections (prep-site claim, unverified).
**What the interviewer is checking:** Whether you know that a relation holds only if the chain connects the two letters with arrows that all point the same way.
**Say this in the interview:** "I walk along the chain from one letter to the other. If every step points the same way, I combine them; if the direction changes anywhere, or the two letters are not linked, the answer is cannot be determined."
**Answer:** **A conclusion follows only if one unbroken same-direction path joins the two letters; otherwise say "cannot be determined" (the conclusion is not definite).**
**Explain simply:**
- A "chain" is the statement written in a line, for example P > Q >= R = S. Each symbol compares only its two neighbours.
- Combining rule: all steps "greater" (> or >=, or =) give a "greater or equal" result; if at least one step is strict (>), the result is strict (>). Equal signs just pass the value along.
- Worked example on P > Q >= R = S: P to S goes > then >= then =, all pointing the same way and one step strict, so P > S definitely. S to P is the same fact reversed, so S < P. But "P = S" is definitely false, and "Q > S" is not definite (Q >= R = S allows Q = S).
- Say "cannot be determined" when the path turns around (for example > then <) or when no path exists.
**Likely follow-ups:** 1) *What if the chain were P > Q <= R?* The direction changes at Q, so P and R cannot be compared. 2) *Is Q >= S true in the example?* Yes, Q >= R = S gives Q >= S.
**Common mistakes / traps:** Upgrading ">=" to ">" because "it looks bigger"; assuming a relation between two letters that merely share a neighbour. (Reasoning checked by brute force over small integer values in related items Q2 to Q4.)

### Q2 ⭐⭐⭐ 🟢 Statement: R > S >= T = U < V. Conclusions: I. R > U. II. V > T. III. S > V. Which conclusion(s) definitely follow?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Reading a mixed chain and spotting which pairs are actually connected.
**Say this in the interview:** "I check each pair along the chain. I holds, II holds, III has no connecting path. So I and II follow, III does not."
**Answer:** **Only I and II follow (III does not).**
**Step-by-step reasoning:**
1. I. R to U: R > S, S >= T, T = U. All point downward and one is strict, so R > U. True.
2. II. V to T: U < V, and T = U, so T < V, which is V > T. True.
3. III. S and V: S sits on the left side going down to U; V sits above U. The path S, T, U, V goes >= then = then <, a turn, so S and V cannot be compared. Not definite.
**Fast method (30 seconds):** Mark the lowest point of the chain (T = U) and see which letters are above it: R, S and V are all above it, but R and S are not linked to V, because both are "above" the same bottom point, not above each other.
**Check:** Brute-forced over all integer assignments 1 to 7: I and II hold in every model; III holds in some models and fails in others, so it is not definite.
**Explain simply:**
- Two letters that are both bigger than the same third letter cannot be compared with each other.
- "Definitely follows" means true in every possible assignment of numbers.
**Likely follow-ups:** 1) *Does S >= U follow?* Yes (S >= T = U). 2) *Does R > V follow?* No, R and V are both above U, not linked.
**Common mistakes / traps:** Marking III true because S and V "look" like they are on the same side of the sign.

### Q3 ⭐⭐⭐ 🟢 A candidate reads "P >= Q >= R" and concludes "P > R". Why is this conclusion wrong, and what is the strongest correct conclusion about P and R?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice that "greater or equal" steps can all be equalities.
**Say this in the interview:** "Both signs allow equality, so P, Q and R could all be the same number. P > R is not guaranteed; the strongest safe statement is P >= R."
**Answer:** **P > R is wrong; the strongest correct conclusion is P >= R.**
**Step-by-step reasoning:**
1. Strict (>) means "definitely bigger"; non-strict (>=) means "bigger or equal".
2. Try P = Q = R = 5. Both statements are true (5 >= 5 and 5 >= 5), but P > R is false.
3. So P > R fails in at least one case and is not definite.
4. In every case P >= R holds, because bigger-or-equal chained with bigger-or-equal stays bigger-or-equal.
**Fast method (30 seconds):** The result is strict only if at least one step in the chain is strict. No strict step means the result is non-strict.
**Check:** Brute force over integers 1 to 7: P > R is sometimes true, sometimes false; P >= R is always true.
**Explain simply:**
- A single counterexample (one set of numbers that fits the statement but breaks the conclusion) is enough to reject a conclusion.
- Strongest conclusion means the most precise one that is still always true.
**Likely follow-ups:** 1) *What if it were P >= Q > R?* Then P > R definitely (one strict step). 2) *Is P = R possible?* Yes, but not forced, so "P = R" does not definitely follow either.
**Common mistakes / traps:** Treating >= as >; or saying P = R follows because the symbol "contains" an equal sign.

### Q4 ⭐⭐⭐ 🟢 From the statement "P > Q < R", what can you conclude about the relation between P and R, and why does the chain break at Q?
**Asked at:** commonly asked (no company-specific report found); a Testbook worked example makes the same point with P < S < R < T > Q (no P-Q relation), prep-site claim.
**What the interviewer is checking:** Recognising a "valley": two letters above the same smaller letter cannot be compared.
**Say this in the interview:** "Q is smaller than both P and R, but that tells me nothing about P versus R. They could be equal, or either could be larger. So no relation can be concluded."
**Answer:** **No definite relation between P and R (cannot be determined).**
**Step-by-step reasoning:**
1. Pick Q = 1. Then P and R are each any number above 1.
2. P = 3, R = 5 gives P < R. P = 5, R = 3 gives P > R. P = R = 4 gives P = R.
3. All three outcomes fit the statement, so none is definite.
**Fast method (30 seconds):** Look at the arrows. A "peak or valley" at the middle letter (> then <, or < then >) breaks the chain; a chain only carries a relation when it keeps going one way.
**Check:** Brute force over integers 1 to 7: P > R, P < R and P = R each hold in some models and fail in others.
**Explain simply:**
- The chain breaks at Q because both arrows point at Q, so Q only tells you about itself.
- Everyone in a class is taller than the shortest student, but that does not rank them against each other.
**Likely follow-ups:** 1) *What can you say about P and R in P < Q > R?* Also nothing (Q is above both). 2) *What is definite in P > Q < R?* P > Q and R > Q.
**Common mistakes / traps:** Concluding "P > R" because P is written first; reading left to right as if it were one direction.

### Q5 ⭐⭐⭐ 🟢 In a ranking of n people with no ties, how are the rank from the top and the rank from the bottom related, and how do you count the people between two ranked positions?
**Asked at:** commonly asked (no company-specific report found); ranking variants (rank from top/bottom, total, people between) are standard prep-site topics (unverified).
**What the interviewer is checking:** Whether you know the n + 1 rule and the "minus one" in counting between.
**Say this in the interview:** "Rank from top plus rank from bottom equals total plus one. People between two ranks are the difference of the ranks minus one."
**Answer:** **Rank from top + rank from bottom = n + 1. People between positions a and b (a < b) = b - a - 1.**
**Explain simply:**
- Why n + 1: a person at rank t from the top has t - 1 people above and, if the bottom rank is b, b - 1 people below. Add herself: (t - 1) + (b - 1) + 1 = n, so t + b = n + 1.
- Why minus one when counting between: positions 5 and 9 are 4 apart, but the people strictly between are at positions 6, 7, 8, which is 3.
- Worked mini-example with n = 30: 4th from the top is 30 + 1 - 4 = 27th from the bottom. People between the 7th and 15th: 15 - 7 - 1 = 7.
- Ties are excluded here; with ties the rank rules change.
**Likely follow-ups:** 1) *Total from two ranks?* If someone is 10th from top and 15th from bottom, n = 10 + 15 - 1 = 24. 2) *If two people are on the same side and you want the people between inclusive of both?* Use b - a + 1.
**Common mistakes / traps:** Using n - rank instead of n + 1 - rank; forgetting the minus one, or subtracting two when it should be one.

### Q6 ⭐⭐⭐ 🟢 In a hiring test, all candidates are ranked by score with no ties. Dev is 9th from the top. After a re-evaluation Dev moves down 6 places and is now 20th from the bottom. How many candidates took the test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Updating a rank after a move, then applying the n + 1 rule.
**Say this in the interview:** "Moving down 6 places makes Dev 15th from the top. 15th from the top and 20th from the bottom means 15 + 20 - 1 = 34 candidates."
**Answer:** **34 candidates.**
**Step-by-step reasoning:**
1. New rank from the top = 9 + 6 = 15 (moving down increases the rank number).
2. Rank from top + rank from bottom = n + 1, so 15 + 20 = n + 1.
3. n = 34.
**Fast method (30 seconds):** Take the final position only: new top rank plus bottom rank minus 1.
**Check:** Verified by script: 9 + 6 + 20 - 1 = 34. Dev has 14 above and 19 below; 14 + 19 + 1 = 34.
**Explain simply:**
- Moving down means more people are ahead of you, so your rank from the top goes up.
- The rank "now" is the only one that pairs with the bottom rank.
**Likely follow-ups:** 1) *If Dev had moved up 6 places and was 20th from the bottom?* Then top rank 3, n = 3 + 20 - 1 = 22. 2) *What was Dev's original rank from the bottom?* 34 + 1 - 9 = 26.
**Common mistakes / traps:** Using 9 + 20 - 1 = 28 (ignoring the move), or subtracting 6 instead of adding.

### Q7 ⭐⭐⭐ 🟢 Five regions sold different amounts last quarter. East sold more than South but less than North. West sold more than North. Central sold less than South. Which region sold the second-lowest amount?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chaining comparisons into one full order.
**Say this in the interview:** "Chaining the clues gives West > North > East > South > Central, so the second-lowest is South."
**Answer:** **South.**
**Step-by-step reasoning:**
1. East > South and East < North, so North > East > South.
2. West > North, so West > North > East > South.
3. Central < South, so Central goes at the very bottom.
4. Order high to low: West, North, East, South, Central. Second-lowest = South.
**Fast method (30 seconds):** Write the symbols as a chain (W > N > E > S > C), because every clue links two neighbours and there are no gaps.
**Check:** Verified by script over all 120 orderings: exactly one satisfies all clues.
**Explain simply:**
- The order is unique because each region is linked to the next by a clue, so there is only one way to line them up.
- "Second-lowest" means second from the bottom, not second in the list.
**Likely follow-ups:** 1) *Who sold the third most?* East. 2) *If a clue said "Central sold more than South"?* The clues would clash (Central would need to be above South and below South), so no valid order.
**Common mistakes / traps:** Counting from the top (answering East) or placing Central above South.

### Q8 ⭐⭐⭐ 🟢 In a row of 50 employees at an induction event, Mira is 17th from the left end and Nikhil is 25th from the right end, with Mira standing to the left of Nikhil. How many employees stand between Mira and Nikhil?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Converting a right-end rank to a left-end position, then counting between.
**Say this in the interview:** "Nikhil is 25th from the right, so he is 50 + 1 - 25 = 26th from the left. Between 17th and 26th there are 26 - 17 - 1 = 8 people."
**Answer:** **8 employees.**
**Step-by-step reasoning:**
1. Nikhil's position from the left = 50 + 1 - 25 = 26.
2. Mira is at position 17, and 17 < 26, which agrees with "Mira is to the left".
3. People between = 26 - 17 - 1 = 8 (positions 18 to 25).
**Fast method (30 seconds):** Total minus the two ranks, minus one: 50 - 17 - 25 = 8. This works when the two ranks are measured from opposite ends and the people do not overlap.
**Check:** Verified by script: both methods give 8; positions 18 to 25 is 8 numbers.
**Explain simply:**
- The 17th from the left has 16 people behind him on his left; the 25th from the right has 24 on his right; 50 - 1 - 1 - 16 - 24 = 8 in the middle (Mira and Nikhil are the two taken out).
**Likely follow-ups:** 1) *How many stand outside the two?* 16 + 24 = 40. 2) *Would Mira at 30th from the left still make sense?* No, then she is to the right of Nikhil (26th), contradicting the statement.
**Common mistakes / traps:** Answering 50 - 17 - 25 + 1 or forgetting to convert; adding the ranks (17 + 25 = 42) as if both counted from the same end.

### Q9 ⭐⭐⭐ 🟢 Sunita is 10th from the top in a list of 40 candidates ranked by score, with no ties. What percentage of the candidates scored below her?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Turning a rank into a count and then a percentage of the whole group.
**Say this in the interview:** "Nine are above her, so 40 - 10 = 30 are below. 30 out of 40 is 75 per cent."
**Answer:** **75% scored below her.**
**Step-by-step reasoning:**
1. Rank from the top is 10, so 9 people are above her.
2. People below = 40 - 10 = 30.
3. Percentage = 30 / 40 x 100 = 75%.
**Fast method (30 seconds):** Below = n - rank. Divide by n.
**Check:** Verified by script: 30/40 = 0.75. 9 above + her + 30 below = 40.
**Explain simply:**
- This is a simple percentile idea (the share of people you beat). Here the denominator is all 40 candidates, as the question asks, and Sunita herself is not counted as "below".
- Some percentile definitions add half of the ties or count the person themselves; with no ties and this question's wording, 75% is the answer.
**Likely follow-ups:** 1) *What share scored above her?* 9/40 = 22.5%. 2) *Percentage of the other 39 who scored below her?* 30/39 = 76.9% (rounded to one decimal).
**Common mistakes / traps:** Using 40 - 10 - 1 = 29 or dividing by 39 without being asked; answering 25% (the share at or above her, rank/n).

### Q10 ⭐⭐⭐ 🟡 Statement: P <= Q < R = S <= T. Conclusions: I. P < T. II. Q < S. III. T = R. IV. T > Q. Which conclusion(s) definitely follow?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Spotting when a strict step upgrades a non-strict chain, and when equality is not forced.
**Say this in the interview:** "The whole chain goes upward, with one strict step, so P < T, Q < S and T > Q all hold. T = R does not, because R <= T allows T to be bigger."
**Answer:** **I, II and IV follow; III does not.**
**Step-by-step reasoning:**
1. The chain runs low to high: P <= Q < R = S <= T. All arrows point the same way, so any two letters are comparable.
2. I. P to T: includes the strict step Q < R, so P < T. True.
3. II. Q < R = S gives Q < S. True.
4. III. R = S <= T gives R <= T, not R = T. Not definite (T could be larger).
5. IV. Q < R <= T gives T > Q. True.
**Fast method (30 seconds):** In a one-direction chain, a relation is strict if the path between the two letters passes a strict step. P to T passes Q < R; Q to S passes Q < R; Q to T passes Q < R; R to T has only = and <=, so it stays non-strict.
**Check:** Brute force over integer assignments 1 to 7: I, II, IV always true; III true only in some models.
**Explain simply:**
- Only the stretch between the two letters matters, not the rest of the chain.
- "<=" means less or equal, so equality is possible but never certain.
**Likely follow-ups:** 1) *Does P <= S follow?* Yes (even P < S). 2) *Does P < Q follow?* No, P <= Q allows P = Q.
**Common mistakes / traps:** Marking III true because R = S and S <= T "feels like" equality; marking P < Q true.

### Q11 ⭐⭐⭐ 🟡 In a certain code, '$' means '>', '#' means '<', '@' means '>=', '%' means '<=' and '*' means '='. Statement: M % N # O * P $ Q. Conclusions: I. M < P. II. N < Q. III. O > Q. IV. M >= Q. Which conclusion(s) definitely follow?
**Asked at:** commonly asked (no company-specific report found); coded inequalities are a named type on prep sites such as Testbook (unverified).
**What the interviewer is checking:** Decoding symbols without slips, then testing each conclusion on the chain.
**Say this in the interview:** "Decoded, the chain is M <= N < O = P > Q. M to P goes upward with a strict step, so I is true. O = P > Q gives III. N versus Q and M versus Q are not linked because P is a peak. So I and III."
**Answer:** **Only I and III follow.**
**Step-by-step reasoning:**
1. Decode: % is <=, # is <, * is =, $ is >. So M <= N < O = P > Q.
2. I. M <= N < O = P: strict step N < O, so M < P. True.
3. II. N < Q? N and Q both sit below the peak O = P, so they cannot be compared. Not definite.
4. III. O = P and P > Q give O > Q. True.
5. IV. M >= Q? M is on the left rising side, Q on the right falling side, joined only through the peak. Not definite.
**Fast method (30 seconds):** Rewrite the code as normal symbols first, mark the peak (O = P), and remember: letters on opposite sides of a peak cannot be compared.
**Check:** Verified by script: brute force over integers 1 to 7 on the decoded chain; I and III always true, II and IV sometimes true.
**Explain simply:**
- A "peak" is a letter or group bigger than both of its neighbours; it separates the chain into two independent sides.
- Decoding first removes the chance of reading the wrong sign mid-solution.
**Likely follow-ups:** 1) *If the statement ended with "$ Q" replaced by "@ Q"?* Then the end is P >= Q, so O = P >= Q; III (O > Q) would no longer be definite, while I (M < P) still follows. (Hand-checked.) 2) *Would M < Q follow?* No.
**Common mistakes / traps:** Mixing up # and $ (reading # as >); picking IV because M "is smaller than P" and Q is smaller than P.

### Q12 ⭐⭐⭐ 🟡 What is the fastest reliable method for solving coded inequalities: how do you decode the symbols, rewrite the chain and check each conclusion, and what usually goes wrong?
**Asked at:** commonly asked (no company-specific report found); Testbook and Unacademy describe the same decode, chain, check approach and call these items harder than direct ones (prep-site claims, unverified).
**What the interviewer is checking:** Whether you have a disciplined routine rather than guessing.
**Say this in the interview:** "First I translate every symbol into normal signs and write the chain. Then for each conclusion I find a one-direction path between the two letters and check strictness. No path, or a turn, means not definite. Last, I look for either-or pairs."
**Answer:** **Decode, rewrite as a normal chain, test each conclusion by path and strictness, then check for either-or.**
**Explain simply:**
- Step 1, decode: write the code key on top ($ = >, # = <, @ = >=, % = <=, * = =) and rewrite the whole statement once in normal signs. Never decode in your head per conclusion.
- Step 2, mark peaks and valleys: where the direction turns, the two sides cannot be compared.
- Step 3, test each conclusion: decode it too, then find the path. Strict only if a strict step lies on the path; equal only if every step is "=".
- Step 4, either-or: if two conclusions are about the same pair of letters, one is ">" and the other "<=" (or "<" and ">="), and neither follows alone, then one of them must be true, so "either I or II follows".
- Worked mini-example: with the key above, A % B * C $ D means A <= B = C > D. "A < D" is not definite (A and D are across the peak at C); "B > D" is true.
**Likely follow-ups:** 1) *How do you check the either-or case?* The two conclusions must cover all possibilities together (P > S and P <= S do). 2) *What if you are unsure?* Substitute small numbers (a quick counterexample test).
**Common mistakes / traps:** Decoding one symbol wrongly, treating "=" in the chain as strict, mixing up conclusion symbols with statement symbols, and forgetting the either-or check when both conclusions fail.

### Q13 ⭐⭐⭐ 🟡 Statement: P >= Q > R <= S. Conclusions: I. P > S. II. P <= S. Choose one: (a) only I follows, (b) only II follows, (c) either I or II follows, (d) neither follows, (e) both follow.
**Asked at:** commonly asked (no company-specific report found); either-or items are a named type on prep sites (unverified).
**What the interviewer is checking:** Recognising the either-or pattern: two conclusions that are exact opposites on the same pair.
**Say this in the interview:** "P and S are on opposite sides of the valley at R, so neither conclusion is definite alone. But P > S and P <= S cover every case, so exactly one of them must be true: option (c)."
**Answer:** **(c) either I or II follows.**
**Step-by-step reasoning:**
1. The chain P >= Q > R <= S has a valley at R (Q > R and S >= R), so P and S have no fixed relation.
2. I. P > S: true in some models, false in others. Not definite alone.
3. II. P <= S: true in some models, false in others. Not definite alone.
4. I and II involve the same two letters, and together they cover every possibility (P is either greater than S or not). So at least one is always true.
5. Neither alone is certain, but one of the two is, which is exactly "either I or II".
**Fast method (30 seconds):** Check (1) neither alone follows, (2) same pair of letters, (3) the two relations are complements, meaning every case falls under one of them (> with <=, or < with >=). Then pick the "either" option.
**Check:** Verified by script: over all integer assignments 1 to 7, I and II are each sometimes true, and in every model at least one of them is true (and never both).
**Explain simply:**
- Either-or only applies when neither conclusion follows by itself and the pair is complete.
- If the pair is not complete (for example P > S and P < S, which leave out P = S), the answer is "neither follows".
**Likely follow-ups:** 1) *What if the conclusions were I. P > S and II. P < S?* Then (d) neither, since P = S is possible. 2) *What if the statement were P >= Q > R >= S?* Then P > S definitely, so only I follows.
**Common mistakes / traps:** Choosing (d) neither because neither alone follows; choosing (e) both, or missing that the conclusions are exact complements.

### Q14 ⭐⭐⭐ 🟡 A is taller than B. C is shorter than B. D is taller than A but shorter than E. F is shorter than C. All six heights are different. Who is the third tallest?
**Asked at:** commonly asked (no company-specific report found); comparison and ordering items appear in prep-site reasoning lists (unverified).
**What the interviewer is checking:** Whether you can merge several "taller than" clues into one single line.
**Say this in the interview:** "I chain the clues: E > D > A > B > C > F. Counting from the tallest, the third is A."
**Answer:** **A is the third tallest.**
**Step-by-step reasoning:**
1. "A taller than B" and "C shorter than B": A > B > C.
2. "F shorter than C": A > B > C > F.
3. "D taller than A but shorter than E": E > D > A.
4. Join the two pieces at A: E > D > A > B > C > F.
5. Counting from the tallest: E (1st), D (2nd), A (3rd).
The line is complete (every neighbouring pair is linked), so the order is unique.
**Fast method (30 seconds):** Write each clue as a short arrow chain, then join chains on a shared letter (A and B appear twice). Once all six letters sit on one line, just count.
**Check:** Verified by script over all 720 orderings: exactly one, E D A B C F.
**Explain simply:**
- "Taller than" is transitive: if X is taller than Y and Y is taller than Z, then X is taller than Z.
- A single line of six letters is a full ranking; no guessing is needed.
**Likely follow-ups:** 1) *Who is the shortest?* F. 2) *If the clue "F is shorter than C" were removed, who is third?* It could not be determined: F would be unlinked, and checking all orders gives A, D or F as third tallest depending on where F fits.
**Common mistakes / traps:** Putting D below A because D is mentioned later, or stopping when two chains exist and guessing how they join.

### Q15 ⭐⭐⭐ 🟡 A weighs 4 kg more than B. B weighs 3 kg less than C. D weighs 2 kg more than C. E weighs 2 kg less than A. Who is the heaviest and who is the lightest of the five?
**Asked at:** commonly asked (no company-specific report found); topic seen in prep-site lists (unverified).
**What the interviewer is checking:** Turning "x kg more or less" clues into numbers measured from one reference person.
**Say this in the interview:** "I call C's weight w and express everyone relative to C. D is w+2, A is w+1, E is w-1, B is w-3. So D is heaviest and B is lightest."
**Answer:** **Heaviest: D. Lightest: B.**
**Step-by-step reasoning:**
1. Pick C as the base: C = w.
2. B weighs 3 kg less than C: B = w - 3.
3. A weighs 4 kg more than B: A = w - 3 + 4 = w + 1.
4. D weighs 2 kg more than C: D = w + 2.
5. E weighs 2 kg less than A: E = w + 1 - 2 = w - 1.
Table (relative to C): D +2, A +1, C 0, E -1, B -3.
**Fast method (30 seconds):** Choose the person who appears most often as the base (here C, or B) and give everyone a number such as "+2" or "-3". The biggest and smallest numbers are the answer; you never need the real weights.
**Check:** Verified by script with w = 10 (D 12, A 11, C 10, E 9, B 7): all five differ, and every clue holds.
**Explain simply:**
- "Relative value" means we measure everyone as a gap from one person instead of needing actual kilograms.
- Because the gaps are fixed, the order is the same whatever C really weighs.
**Likely follow-ups:** 1) *By how many kg does D outweigh B?* 5 kg (+2 minus -3). 2) *Who is second heaviest?* A.
**Common mistakes / traps:** Sign slips, for example treating "B is 3 kg less than C" as C = B - 3, or computing E from B instead of A.

### Q16 ⭐⭐⭐ 🟡 In a row of people, Asha is 9th from the left end and Bhaskar is 15th from the right end. Asha stands to the left of Bhaskar and exactly 12 people stand between them. How many people are in the row?
**Asked at:** commonly asked (no company-specific report found); rank/position counting is a standard prep-site topic (unverified).
**What the interviewer is checking:** Placing one person from the left end and using the "between" count correctly.
**Say this in the interview:** "Asha is at position 9. Twelve people between means Bhaskar is at 9 + 12 + 1 = 22 from the left. He is 15th from the right, so the row has 22 + 15 - 1 = 36 people."
**Answer:** **36 people.**
**Step-by-step reasoning:**
1. Asha is at position 9 from the left.
2. The 12 people between them fill positions 10 to 21.
3. So Bhaskar is at position 22 from the left.
4. Left position + right position = total + 1 (the person is counted from both ends). So 22 + 15 = total + 1, giving total = 36.
**Fast method (30 seconds):** Gap between two people = difference of positions minus 1. So Bhaskar = 9 + 12 + 1 = 22. Then total = left position + right position - 1.
**Check:** In a row of 36, the 22nd from the left is 36 + 1 - 22 = 15th from the right. Positions 10 to 21 are 12 people. Verified by script.
**Explain simply:**
- "People between" excludes both named people, so add 1 to get the position difference.
- Counting from the left and from the right counts the same person twice, hence the "- 1".
**Likely follow-ups:** 1) *If only 10 people stood between them?* Bhaskar is 9 + 11 = 20th from the left, so the row has 20 + 15 - 1 = 34. 2) *How many stand to the right of Bhaskar?* 14.
**Common mistakes / traps:** Forgetting the "+1" and getting Bhaskar at 21 (total 35), or adding 9 + 12 + 15 = 36 by luck. (It does work here: 9 counts the people up to and including Asha, 12 are between, and 15 counts Bhaskar and everyone to his right. But it is easy to misapply, so use the position method.)

### Q17 ⭐⭐⭐ 🟡 In a certification batch, Tara is 12th from the top in the Excel test. In the SQL test she drops 10 places and is 27th from the bottom. No ties in either test. How many people are in the batch?
**Asked at:** commonly asked (no company-specific report found); "rank changes between two tests" is a common prep-site variant (unverified).
**What the interviewer is checking:** Updating a rank after a move, then converting top rank and bottom rank into a total.
**Say this in the interview:** "Dropping 10 places moves her from 12th to 22nd from the top. She is also 27th from the bottom, so total = 22 + 27 - 1 = 48."
**Answer:** **48 people.**
**Step-by-step reasoning:**
1. Excel rank from the top: 12.
2. "Drops 10 places" means she moves toward the bottom: 12 + 10 = 22nd from the top in SQL.
3. In the same SQL list she is 27th from the bottom.
4. Total = rank from top + rank from bottom - 1 = 22 + 27 - 1 = 48.
**Fast method (30 seconds):** Drop = add to the top rank; rise = subtract. Then use "top + bottom - 1 = total". The Excel list is only used to get the starting rank.
**Check:** In a list of 48, 22nd from the top is 48 + 1 - 22 = 27th from the bottom. Verified by script.
**Explain simply:**
- Rank from the top gets bigger as you go down the list, so "drops" means a bigger number.
- Top rank and bottom rank in the same list always add to total + 1.
**Likely follow-ups:** 1) *What if she had climbed 10 places instead?* Top rank 2, total 2 + 27 - 1 = 28. 2) *How many scored below her in SQL?* 26.
**Common mistakes / traps:** Subtracting 10 (12 - 10 = 2) because "drop" sounds like a smaller number; and forgetting the "- 1".

### Q18 ⭐⭐⭐ 🟡 Six people P, Q, R, S, T and U stand in a queue (position 1 is the front). R is ahead of Q. S stands immediately behind P. T stands immediately behind R and ahead of P. U is at the back. Q is not 5th. Who is 3rd in the queue?
**Asked at:** commonly asked (no company-specific report found); queue and order puzzles are standard prep-site items (unverified).
**What the interviewer is checking:** Building blocks from "immediately behind" clues and fitting the loose clues around them.
**Say this in the interview:** "R-T is a block, P-S is a block, U is last. T is ahead of P, so R T comes before P S. Q is not 5th and is behind R, which puts Q in 3rd. The queue is R, T, Q, P, S, U, so 3rd is Q."
**Answer:** **Q is 3rd.**
**Step-by-step reasoning:**
1. U is at the back: position 6.
2. Blocks: R then T (T immediately behind R), and P then S (S immediately behind P).
3. T is ahead of P, so block R-T comes before block P-S.
4. Positions 1 to 5 hold R-T, P-S and Q. Q must be behind R, and Q is not 5th.
5. Q must be behind R. Blocks cannot be split, so Q goes before R-T (breaks "R ahead of Q"), between R-T and P-S (3rd), or after P-S (5th, banned).
6. Only one place is left: R, T, Q, P, S, U.
Final queue:

| Position | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | R | T | Q | P | S | U |

**Fast method (30 seconds):** Glue "immediately behind" pairs into blocks first; they remove the most freedom. Then slot the single free person (Q) into the gaps and use the negative clue last.
**Check:** Verified by script over all 720 orders: exactly one satisfies all clues (R T Q P S U).
**Explain simply:**
- "Immediately behind" means adjacent, so the two people travel as one unit.
- A negative clue ("Q is not 5th") is best used at the end to remove the last extra option.
**Likely follow-ups:** 1) *Without the clue "Q is not 5th", how many queues work?* Hand-checked: Q can also be 5th (R T P S Q U), so two. 2) *Who is 4th?* P.
**Common mistakes / traps:** Placing Q before R, or treating "ahead of P" as "immediately ahead of P".

### Q19 ⭐⭐⭐ 🟡 Five candidates A, B, C, D and E are interviewed one per day from Monday to Friday. A is interviewed before C. B is interviewed the day after D. E is interviewed two days after A. C is not interviewed on Friday. D is interviewed after A. Who is interviewed on Friday?
**Asked at:** commonly asked (no company-specific report found); day-scheduling puzzles are a standard prep-site topic (unverified).
**What the interviewer is checking:** Using fixed gaps ("two days after", "the day after") to limit the positions.
**Say this in the interview:** "Number the days 1 to 5. E = A + 2, B = D + 1, and D comes after A. Trying A on day 1 gives E on day 3, so D is on day 4 and B on day 5, leaving C on day 2. Friday is B."
**Answer:** **B is interviewed on Friday.**
**Step-by-step reasoning:**
1. Days: Mon = 1 ... Fri = 5. E = A + 2, so A can only be on day 1, 2 or 3.
2. D is after A and B = D + 1 (a block D-B), so D is at most day 4.
3. Try A = 2: E = 4. Remaining days 1, 3, 5 must hold C, D, B; D-B must be adjacent, but 1, 3, 5 are not consecutive. Fails.
4. Try A = 3: E = 5. Days 1, 2, 4 left; D must be after A, so D = 4 and B = 5, which is taken by E. Fails.
5. Try A = 1: E = 3. Days 2, 4, 5 left. D-B adjacent gives D = 4, B = 5, so C = 2, which is after A and not Friday. Works.
Final schedule:

| Day | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Candidate | A | C | E | D | B |

**Fast method (30 seconds):** Start with the clue that has a fixed gap (E = A + 2) and list the few possible starts for A; test each one. Only A = 1 survives.
**Check:** Verified by script over all 120 orders: exactly one fits all five clues.
**Explain simply:**
- "Exactly two days after" ties two people's days together, so one choice fixes the other.
- Trying every small possibility in turn is a valid proof when there are only three starts.
**Likely follow-ups:** 1) *What if the clue "D is interviewed after A" were removed?* Not unique: a second schedule appears (D, B, A, C, E, which has Friday = E), so the extra clue matters (verified by script). 2) *Who is interviewed on Wednesday?* E.
**Common mistakes / traps:** Reading "two days after" as "the day after tomorrow's slot is free" without checking collisions, and forgetting that the "D after A" clue is what rules out the second schedule.

### Q20 ⭐⭐⭐ 🟡 In a ranked list of 15 employees (no ties), C is 5th from the bottom. B ranks 3 places above C, and A ranks 4 places above B. What is A's rank from the top?
**Asked at:** commonly asked (no company-specific report found); top/bottom rank conversion is a standard prep-site item (unverified).
**What the interviewer is checking:** Converting bottom rank to top rank, then moving up the list by subtraction.
**Say this in the interview:** "5th from the bottom in a list of 15 is 15 + 1 - 5 = 11th from the top. B is 3 places above, so 8th. A is 4 places above B, so 4th."
**Answer:** **A is 4th from the top.**
**Step-by-step reasoning:**
1. Rank from top = total + 1 - rank from bottom = 15 + 1 - 5 = 11. So C is 11th from the top.
2. "Above" means closer to the top, so subtract: B = 11 - 3 = 8.
3. A = 8 - 4 = 4.
**Fast method (30 seconds):** Convert once to top rank, then total shift = 3 + 4 = 7 places up: 11 - 7 = 4.
**Check:** From the bottom, A is 15 + 1 - 4 = 12th; C is 5th, and 12 - 5 = 7 = 3 + 4. Verified by script.
**Explain simply:**
- Higher in the ranking means a smaller top-rank number.
- Top rank + bottom rank = total + 1 because the person is counted from both ends.
**Likely follow-ups:** 1) *If C were 6th from the bottom?* C is 10th from top, A is 3rd (verified). 2) *How many employees are between A and C?* 6.
**Common mistakes / traps:** Using 15 - 5 = 10 for C's top rank, and adding instead of subtracting when moving "above".

### Q21 ⭐⭐ 🟢 Six scores were recorded: Ana 82, Bo 91, Cy 82, Di 75, Ed 91 and Fay 68. Using standard competition ranking (tied people share a rank and the next rank is skipped), what is Di's rank, and what rank does Di get under dense ranking (no ranks skipped)?
**Asked at:** commonly asked (no company-specific report found); the same RANK versus DENSE_RANK idea is a classic analyst topic.
**What the interviewer is checking:** Whether you know that ties change the numbering, and the two common conventions.
**Say this in the interview:** "Sorted high to low: 91, 91, 82, 82, 75, 68. Competition ranking gives Di 5th (four people score higher). Dense ranking gives 3rd (three distinct scores, 91, 82, 75, are at or above hers)."
**Answer:** **Competition rank: 5. Dense rank: 3.**
**Step-by-step reasoning:**
1. Sort descending: Bo 91, Ed 91, Ana 82, Cy 82, Di 75, Fay 68.
2. Competition ("1224") ranking: rank = 1 + number of people with a strictly higher score. For Di: higher scores are 91, 91, 82, 82, so 4 people; rank = 5.
3. Dense ranking ("1223"): rank = 1 + number of distinct higher scores. Distinct higher scores are 91 and 82, so rank = 3.
Table:

| Person | Score | Competition | Dense |
|---|---|---|---|
| Bo, Ed | 91 | 1 | 1 |
| Ana, Cy | 82 | 3 | 2 |
| Di | 75 | 5 | 3 |
| Fay | 68 | 6 | 4 |

**Fast method (30 seconds):** Competition: count people strictly above, add 1. Dense: count distinct scores strictly above, add 1.
**Check:** Verified by script; the two formulas give Di 5 and 3. In SQL these correspond to RANK() and DENSE_RANK() (named from memory; not run here).
**Explain simply:**
- Competition ranking leaves gaps after ties (like a race: two golds, no silver, the next person gets bronze).
- Dense ranking never leaves gaps, so the top rank number equals the number of distinct scores.
**Likely follow-ups:** 1) *What are Ana's ranks?* Competition 3, dense 2 (verified). 2) *What is a third option?* Ordinal ranking gives every person a different number, breaking ties arbitrarily (e.g. by name); say which you use.
**Common mistakes / traps:** Giving Di 4 (counting the tie pairs once under competition), or 3 under both conventions.

### Q22 ⭐⭐ 🟢 A manager says, "My team's rank in the company quiz went from 10th to 5th, so our score improved." Why does this not necessarily follow, and what data would you ask for?
**Asked at:** commonly asked (no company-specific report found); a standard "rank versus score" critical-thinking probe for analysts.
**What the interviewer is checking:** Whether you separate relative position (rank) from absolute performance (score).
**Say this in the interview:** "Rank only says where you stand against others. The team could have scored lower but other teams fell more, or the field changed. I would ask for the actual scores in both rounds, the number of teams, and the spread."
**Answer:** **It does not follow: a better rank can come with the same or even a lower score. I would ask for raw scores for both rounds, the number of teams in each, the maximum possible score and the score gaps between neighbouring teams.**
**Explain simply:**
- Rank is relative: it depends on everyone else, not only on you.
- Worked mini-example: Round 1, team score 70, nine teams above it score 71 to 90, so it is 10th. Round 2, the team scores 65 (lower), but five of those teams are absent or score under 65; it can now be 5th. Rank improved, score fell.
- Other things that can change: number of teams, a different quiz with different difficulty, ties, or someone else's disqualification.
- Better evidence: score as a percentage of the maximum, or a percentile among the same group, alongside raw scores.
**Likely follow-ups:** 1) *Does an improved score guarantee an improved rank?* No; others may improve more. 2) *What measure would you report?* Raw score plus percentile, with the group size.
**Common mistakes / traps:** Treating rank as a score, and ignoring that the group or test may differ between the two rounds.

### Q23 ⭐⭐ 🟢 How do you handle negative clues such as "A is not first" or "B does not finish last" in an order puzzle: when do you use them and when do you hold them back?
**Asked at:** commonly asked (no company-specific report found); a common puzzle-technique question.
**What the interviewer is checking:** Whether you have a sensible order of attack: strong clues first, weak clues to prune.
**Say this in the interview:** "Negative clues rule out only one slot, so they are weak. I first use the positive clues, such as 'immediately behind' or a fixed gap, to build blocks and a short list of possible arrangements. Then I use each negative clue to delete the options it forbids."
**Answer:** **Use positive, tight clues first to build the structure; hold negative clues until you have a few candidate arrangements, then use them to eliminate. Use a negative clue early only when it directly settles a small choice.**
**Explain simply:**
- Positive clue ("A is immediately before C") cuts many arrangements; a negative clue ("A is not first") cuts only some.
- Worked mini-example: 4 people, "A not first" and "B not last". With no other clue there are 24 orders; inclusion-exclusion gives 24 - 6 - 6 + 2 = 14 left (checked by script). Two negatives alone barely help.
- In Q18, "Q is not 5th" was the last clue used: it chose between two surviving queues.
- Good habit: keep a small grid of people against positions and cross out the banned cell the moment you read a negative clue; that costs nothing and prevents later mistakes.
**Likely follow-ups:** 1) *Can a negative clue ever be the key one?* Yes, as the final tie-break (Q18; in Q19 the plain clue "D is interviewed after A" played the same last-step role). 2) *What if all clues are negative?* Count: the arrangements left after the exclusions; use a grid.
**Common mistakes / traps:** Forgetting a negative clue after using it once, or trying to start the puzzle from a negative clue and guessing.

### Q24 ⭐⭐ 🟢 A is older than B. C is older than B. Can you say who is the oldest of the three? Explain why or why not.
**Asked at:** commonly asked (no company-specific report found); a classic "cannot be determined" check.
**What the interviewer is checking:** Whether you can tell when two clues point at the same person and give no link between the others.
**Say this in the interview:** "Both A and C are older than B, so B is the youngest. But nothing compares A and C, so either could be oldest. The oldest cannot be determined."
**Answer:** **No. The oldest is A or C (cannot be determined); the only sure fact is that B is the youngest.**
**Explain simply:**
- Both arrows point down at B: A > B and C > B. There is no arrow between A and C, so no chain joins them.
- Checked by script: the consistent orders are C > A > B and A > C > B. So both A and C can be oldest.
- A single linear order needs every neighbouring pair linked; here the link A to C is missing.
- Worked mini-example: ages A 30, C 25, B 20 (A oldest) and A 25, C 30, B 20 (C oldest) both obey the two clues.
**Likely follow-ups:** 1) *Who is the youngest?* B, for sure. 2) *What one extra clue would settle it?* Any clue comparing A and C, such as "A is older than C".
**Common mistakes / traps:** Picking A because it is named first, or answering "C" from the order in the sentence.

### Q25 ⭐⭐ 🟢 You get about 45 seconds for each inequality or ranking question in an online assessment. How do you decide the order of attempt, when do you skip, and how do you avoid sign mistakes?
**Asked at:** commonly asked (no company-specific report found); the 45-second budget is the question's own assumption, not a reported test timing.
**What the interviewer is checking:** Whether you manage time and accuracy sensibly under a clock.
**Say this in the interview:** "I do the quick direct items first, skip anything that stalls after about 45 seconds and return later. For signs I rewrite the chain on paper, mark the direction, and check each conclusion by tracing a path."
**Answer:** **Our suggestion (a rule of thumb, not a research finding): attempt direct inequality and simple rank-count items first, then coded and multi-clue puzzles; skip when you are stuck at about the time budget; and protect accuracy with one fixed routine for signs.**
**Explain simply:**
- Order of attempt (our suggestion): (1) direct inequality, (2) single-formula rank counts (top + bottom = total + 1), (3) coded inequality, (4) puzzles with many clues.
- Skip rule (our suggestion): if you have no chain after about 30 to 45 seconds, mark it and move on; if negative marking applies, guess only when you can drop at least one option (check the test's own rules).
- Sign routine: decode symbols first and write the chain in one line; a conclusion is sure only if a continuous path of same-direction signs joins the two letters; if the path needs a reversal (> then <), say "cannot be determined".
- Worked mini-example (Q13 style): P >= Q > R <= S; P and S are not on one directional path, so neither "P > S" nor "P <= S" is sure.
- Useful sanity test: try two sets of numbers; if both conclusions can hold, it is "not determined".
**Likely follow-ups:** 1) *How many ranking questions could you do in 10 minutes?* About 13 at 45 seconds each, arithmetic only (600 / 45 = 13.3); real speed varies. 2) *What if you finish early?* Re-check signs on the items you did fastest.
**Common mistakes / traps:** Spending 3 minutes on one hard puzzle, and reading ">=" as ">" in the conclusion.

### Q26 ⭐⭐ 🟢 What does "transitive" mean for a comparison, and which of >, >=, = and != can be chained to give a sure conclusion?
**Asked at:** commonly asked (no company-specific report found); the rule underlying every inequality item.
**What the interviewer is checking:** Whether you know exactly which signs carry a conclusion through a middle term.
**Say this in the interview:** "Transitive means if a relates to b and b relates to c in the same way, then a relates to c. Greater than, at least and equals are transitive. Not equal is not; it only chains through an equals sign."
**Answer:** **Transitive: (a R b and b R c) implies a R c. >, >= and = are transitive; != is not. Same-direction chains keep the strict sign if at least one link is strict; mixing > or >= with < or <= gives no sure conclusion.**
**Explain simply:**
- Chaining table, enumerated by script over integers (the sure result for a ? c):

| a ? b, b ? c | Sure conclusion |
|---|---|
| > and > | a > c |
| > and >= | a > c |
| > and = | a > c |
| >= and >= | a >= c |
| >= and = | a >= c |
| = and = | a = c |
| = and != | a != c |
| > and !=, >= and !=, != and !=, != and > | nothing sure |

- Rule of thumb: one strict link makes the whole chain strict; a weak link (>=) alone keeps it weak.
- Worked mini-example: 5 >= 3 >= 3 gives 5 >= 3 (not strict); 5 > 3 >= 3 gives 5 > 3 (strict).
- Why != breaks: a != b and b != c still allows a = c (for example 1, 2, 1).
**Likely follow-ups:** 1) *Does a > b and a > c tell you b versus c?* No. 2) *Is "greater than" for a chain of three always safe?* Yes, a > b > c gives a > c.
**Common mistakes / traps:** Concluding P > R from P >= Q >= R (only P >= R is sure), and chaining != through a middle term.

### Q27 ⭐⭐ 🟢 For integer x, how many values satisfy both 3x - 7 > 11 and 2x + 5 <= 25?
**Asked at:** commonly asked (no company-specific report found); the sources file gives no report for this item.
**What the interviewer is checking:** Whether you can solve two linear inequalities and count the whole numbers in the overlap.
**Say this in the interview:** "First inequality gives x > 6, second gives x <= 10. Integers from 7 to 10, so 4 values."
**Answer:** **4 values (x = 7, 8, 9, 10).**
**Step-by-step reasoning:**
1. 3x - 7 > 11, so 3x > 18, so x > 6.
2. 2x + 5 <= 25, so 2x <= 20, so x <= 10.
3. Both must hold: 6 < x <= 10.
4. The integers are 7, 8, 9, 10, which is 4 numbers.
**Fast method (30 seconds):** Solve each inequality for x like an equation, then put the two limits on a number line. Count integers with (upper limit - lower limit) when one end is open and the other is closed: 10 - 6 = 4.
**Check:** Verified by script over every integer from -100 to 99: exactly 7, 8, 9, 10. For x = 7: 14 > 11 and 19 <= 25. For x = 11: 26 > 25 fails.
**Explain simply:**
- Solving an inequality is like solving an equation; the only special rule is that the sign flips when you multiply or divide by a negative number (not needed here).
- "Both conditions" means the overlap of the two ranges.
- ">" leaves the end value out; "<=" keeps it in.
**Likely follow-ups:** 1) *What if the first condition were 3x - 7 >= 11?* Then x >= 6, so 6 to 10 gives 5 values (verified by script). 2) *What if x could be any real number?* Infinitely many.
**Common mistakes / traps:** Including x = 6 (it gives exactly 11, not greater than 11) or forgetting x = 10 (it gives exactly 25, which is allowed).

### Q28 ⭐⭐ 🟡 Statement: A > B >= C < D = E, and F <= B. Which of the following is definitely true? (a) F < D (b) A > D (c) E > C (d) F <= C.
**Asked at:** commonly asked (no company-specific report found); direct inequality items are a staple of placement reasoning lists (prep-site claim, unverified).
**What the interviewer is checking:** Whether you only link letters through a chain that runs one way, and refuse to link across a "valley" or "peak".
**Say this in the interview:** "Only option (c) is forced: C < D and D = E, so C < E. The others need a link through B or C that the chain does not give."
**Answer:** **(c) E > C.**
**Step-by-step reasoning:**
1. Write the chain: A > B >= C < D = E. Extra clue: F <= B (F hangs under B).
2. (c) E = D and C < D, so C < E, which means E > C. Definitely true.
3. (a) F < D: F <= B and C < D, but B and D are linked only through C, and the chain goes B >= C then C < D (down, then up). B versus D is open. Not definite.
4. (b) A > D: A is above B, but B and D are not comparable. Not definite.
5. (d) F <= C: F is below B, C is also below B. F and C are two items under the same top; their order is unknown. Not definite.
**Fast method (30 seconds):** Look for an option where the arrows all point the same direction between the two letters. Between E and C they do (both ">" direction reading E = D > C). For the others, spot the place where the direction flips (B >= C < D).
**Check:** Verified by brute-force enumeration of all integer assignments 0 to 5: (c) was true in every case; (a), (b), (d) each came out both true and false in some case.
**Explain simply:**
- A conclusion "definitely follows" only if it is true in every possible set of numbers that fits the statement.
- You can chain two comparisons only when they point the same way (or are "=").
- A flip such as ">= then <" is a break: the two ends are unrelated.
**Likely follow-ups:** 1) *What if the statement had C <= D instead of C < D? Would (c) still hold?* No, E >= C only. 2) *What would make (a) definite?* A strict link such as B < D (then F <= B < D gives F < D). B <= D alone gives only F <= D.
**Common mistakes / traps:** Treating B >= C < D as "B and D are comparable", and choosing (a) or (b) from the order of letters on the page.

### Q29 ⭐⭐ 🟡 Statement: K >= L > M >= N, and K = P. Which of the following is definitely false? (a) K > N (b) P > M (c) L > P (d) N < L.
**Asked at:** commonly asked (no company-specific report found); direct inequality items are a staple of placement reasoning lists (prep-site claim, unverified).
**What the interviewer is checking:** Reading "definitely false" correctly: the conclusion must be impossible, not just unproven.
**Say this in the interview:** "K = P and K >= L, so L <= P. That makes 'L > P' impossible. The other three are all forced true."
**Answer:** **(c) L > P.**
**Step-by-step reasoning:**
1. The chain is K >= L > M >= N, all going downward, so every pair is comparable.
2. (a) K >= L > M >= N, so K > N (one strict step is enough). True.
3. (b) P = K >= L > M, so P > M. True.
4. (c) P = K >= L, so L <= P. "L > P" is therefore always false.
5. (d) L > M >= N, so L > N, i.e. N < L. True.
**Fast method (30 seconds):** Replace P by K. Then read the chain: the top item K cannot be smaller than L. Any option that claims L is above K or P is false for sure.
**Check:** Verified by brute-force enumeration: (a), (b), (d) true in every case; (c) false in every case.
**Explain simply:**
- Three kinds of answers exist for a conclusion: definitely true, definitely false, or undetermined.
- If one ">" appears anywhere on a one-direction chain, the two ends are strictly ordered.
- "=" lets you swap letters (P for K).
**Likely follow-ups:** 1) *Is "L >= P" true?* Not definite (L could be smaller than K). Only L <= P is definite. 2) *Is "K >= N" true?* Yes, and even K > N.
**Common mistakes / traps:** Picking an option that is merely "not proven" (for instance L >= P, which is possible but not forced) instead of one that is impossible.

### Q30 ⭐⭐ 🟡 In a certain code, '+' means '>', '-' means '<', 'x' means '>=', '/' means '<=' and '=' means equal. Statement: J x K + L / M - N. Conclusions: I. J > L. II. L < N. III. K > M. IV. J > N. Which conclusion(s) definitely follow?
**Asked at:** commonly asked (no company-specific report found); coded inequalities are described as a standard type by prep sites (unverified).
**What the interviewer is checking:** Accurate decoding of symbols, then the same chain rules as a plain inequality.
**Say this in the interview:** "Decoded, it reads J >= K > L <= M < N. J >= K > L gives J > L, and L <= M < N gives L < N. III and IV need a link across L, so they fail. Answer: I and II."
**Answer:** **Only I and II follow.**
**Step-by-step reasoning:**
1. Decode: J x K becomes J >= K; K + L becomes K > L; L / M becomes L <= M; M - N becomes M < N.
2. Chain: J >= K > L <= M < N.
3. I. J >= K > L gives J > L. True.
4. II. L <= M < N gives L < N. True.
5. III. K > M: K is above L and M is above or equal to L, so K and M are both above L but not related to each other. Not definite.
6. IV. J > N: the chain goes down to L and then up to N. Not definite.
**Fast method (30 seconds):** Write the decoded chain on rough paper first; never work from the symbols. The lowest item here is L (arrows come into L from both sides), so any conclusion that compares two items on opposite sides of L is a trap.
**Check:** Verified by brute-force enumeration: I and II true in every case; III and IV each true in some cases and false in others.
**Explain simply:**
- A "code" question only changes the symbols, not the logic. Decode once, carefully.
- The smallest element (the "valley") separates the chain: items on its two sides cannot be compared.
**Likely follow-ups:** 1) *Does "J > M" follow?* No: J is above L and M is above L, so they are unrelated. 2) *Does "J >= L" follow?* Yes, but it is weaker than the true "J > L".
**Common mistakes / traps:** Mixing up '+' and 'x' (the code uses '+' for ">" and 'x' for ">="), and picking IV because J is "first" and N is "last".

### Q31 ⭐⭐ 🟡 Five runners A, B, C, D and E finish a race with no ties. A finishes two places ahead of B. C finishes immediately after D. E does not finish first or last. B does not finish last. Who finishes third?
**Asked at:** commonly asked (no company-specific report found); order-and-ranking puzzles appear in prep-site topic lists (unverified).
**What the interviewer is checking:** Placing a fixed-gap pair (A _ B) and a glued pair (D C) into five slots, then using the "not" clues.
**Say this in the interview:** "A and B take slots two apart, D and C are neighbours with D first. Only A E B D C fits, so third is B."
**Answer:** **B finishes third.**
**Step-by-step reasoning:**
1. Slots 1 to 5, first place is slot 1. A is two ahead of B, so (A, B) is (1,3), (2,4) or (3,5).
2. B is not last, so (3,5) is out. Left: (1,3) or (2,4).
3. D and C take adjacent slots with D first.
4. If A=1, B=3: the free slots are 2, 4, 5. Adjacent pair D,C must be 4 and 5, leaving E in 2. E is not first or last, so fine.
5. If A=2, B=4: free slots are 1, 3, 5. No two adjacent slots free, so D,C cannot fit. Out.
6. Final order: 1 A, 2 E, 3 B, 4 D, 5 C.
**Final arrangement:**

| Place | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| Runner | A | E | B | D | C |

**Fast method (30 seconds):** Place the rigid blocks first (the "A _ B" block and the "D C" block), and use "not last" to kill options. The glued pair needs two empty neighbouring slots, which only one case leaves.
**Check:** Brute force over all 120 orders found exactly one that satisfies all clues: A E B D C. Re-reading clues: A is 1st, B 3rd (two apart); C 5th right after D 4th; E is 2nd (not first or last); B is not last.
**Explain simply:**
- "Immediately after" means the two are neighbours with no gap.
- "Two places ahead" means a gap of exactly one person between them.
- Try the possible positions of the most restricted pair first; most cases die quickly.
**Likely follow-ups:** 1) *If B could finish last, would the answer stay unique?* No; A=3, B=5 then D,C would take 1,2 or... D C must be neighbours among 1,2,4: slots 1,2, leaving E at 4, so another order D C A E B appears (checked by hand). 2) *Who finishes second?* E.
**Common mistakes / traps:** Reading "two places ahead" as "immediately ahead", or forgetting that D must come before C, not after.

### Q32 ⭐⭐ 🟡 Out of 30 candidates ranked by score with no ties, Tej scored higher than at least 8 candidates and lower than at least 5. What is the best and the worst rank (from the top) that Tej can have?
**Asked at:** commonly asked (no company-specific report found); rank-range items are a variant of standard ranking questions (prep-site topic lists, unverified).
**What the interviewer is checking:** Turning "at least" into limits on the rank, and using the "rank from top = people above + 1" idea.
**Say this in the interview:** "At least 5 above him means rank 6 or worse. At least 8 below him means at most 22 people are at or above him (himself included), so rank 22 or better. Range 6 to 22."
**Answer:** **Best rank 6th, worst rank 22nd.**
**Step-by-step reasoning:**
1. A candidate with rank r has r - 1 people above and 30 - r below.
2. "Lower than at least 5" means at least 5 above: r - 1 >= 5, so r >= 6.
3. "Higher than at least 8" means at least 8 below: 30 - r >= 8, so r <= 22.
4. So the rank can be any value from 6 to 22 (17 values).
**Fast method (30 seconds):** Best (smallest) rank = (number above at least) + 1 = 6. Worst (largest) rank = total - (number below at least) = 30 - 8 = 22.
**Check:** Verified by script listing all ranks 1 to 30 that satisfy both conditions: 6 through 22. Ranks 6 and 22 both satisfy and 5 and 23 both fail.
**Explain simply:**
- Rank from top = (people scoring higher) + 1.
- "At least" gives a lower limit on a count, which pushes the rank in one direction only.
- Both conditions together make a range, not a single number.
**Likely follow-ups:** 1) *What if it said "exactly 8 below"?* Then rank 22 only. 2) *How many different ranks are possible?* 17.
**Common mistakes / traps:** Answering 5 and 23 (forgetting the +1 / the person himself), or treating "at least" as "exactly".

### Q33 ⭐⭐ 🟡 In the statement P >= Q ? R = S, which one of the signs >, >=, =, <, <= placed at '?' makes the conclusion P > S definitely true?
**Asked at:** commonly asked (no company-specific report found); "fill the sign" is a variant of the standard inequality chain (prep-site type, unverified).
**What the interviewer is checking:** That you know a strict ">" is needed somewhere on a same-direction chain to get a strict conclusion.
**Say this in the interview:** "I need the whole chain to run downward from P to S with at least one strict step. P >= Q is non-strict, R = S is just an equality, so the middle sign must be strict '>'."
**Answer:** **The sign ">" (strictly greater than).**
**Step-by-step reasoning:**
1. Put each sign in and ask whether P is certainly above S.
2. With ">": P >= Q > R = S. One strict step, all downward, so P > S. True.
3. With ">=": P >= Q >= R = S gives only P >= S (they could all be equal). Not definite.
4. With "=": P >= Q = R = S gives P >= S only.
5. With "<" or "<=": the chain turns upward (Q < R) after going down, so P and S are not linked.
**Fast method (30 seconds):** A strict conclusion needs (a) all signs pointing the same way and (b) at least one of them strict. Only ">" at the question mark satisfies both.
**Check:** Verified by brute-force enumeration: with ">" the conclusion P > S is true in every case; with each of the other four signs it is false in at least one case.
**Explain simply:**
- ">=" means "greater than or equal to"; it allows equality, so chaining only ">=" and "=" never gives a strict ">".
- One strict sign is enough to make the whole chain strict.
**Likely follow-ups:** 1) *Which signs make P >= S definite?* ">", ">=" and "=" (all keep the downward direction). 2) *Which sign makes P > S definite if the first sign were ">" instead of ">="?* Then ">", ">=" or "=" all work.
**Common mistakes / traps:** Choosing ">=" because it "looks like" greater than, or choosing "=" thinking equals can be substituted freely (it can, but it does not create strictness).

### Q34 ⭐⭐ 🟡 The digits of the number 82459361 are rearranged in descending order. How many digits keep their original position?
**Asked at:** commonly asked (no company-specific report found); "rearrange and count unchanged positions" is a standard placement item (prep-site claim, unverified).
**What the interviewer is checking:** Careful, position-by-position comparison after sorting.
**Say this in the interview:** "Descending order is 98654321. Comparing position by position with 82459361, the 4th, 6th and 8th digits match. So 3."
**Answer:** **3 digits (the 5, the 3 and the 1).**
**Step-by-step reasoning:**
1. Original digits by position: 8, 2, 4, 5, 9, 3, 6, 1.
2. Sort largest to smallest: 9, 8, 6, 5, 4, 3, 2, 1 (all digits are different).
3. Compare:

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Original | 8 | 2 | 4 | 5 | 9 | 3 | 6 | 1 |
| Descending | 9 | 8 | 6 | 5 | 4 | 3 | 2 | 1 |
| Same? | no | no | no | yes | no | yes | no | yes |

4. Three matches.
**Fast method (30 seconds):** Write the sorted row under the original row and tick matches. Do not sort in your head and count; the table avoids slips.
**Check:** Verified by script: sorted string 98654321, 3 matching positions.
**Explain simply:**
- "Position" means place in the number counted from the left, so the same digit in a different place does not count.
- A digit matching its place is a "fixed point" of the sorting.
**Likely follow-ups:** 1) *What if the digits were arranged in ascending order?* Ascending is 12345689; compared with 82459361 only position 2 (the digit 2) matches, so 1 (verified by script). 2) *What if digits repeat?* Compare place by place the same way.
**Common mistakes / traps:** Counting digits that appear in both numbers (all 8 do), or sorting incorrectly by missing the 6.

### Q35 ⭐⭐ 🟡 The letters of the word DATABASE are rearranged in alphabetical order. How many letters stay in their original position?
**Asked at:** commonly asked (no company-specific report found); a standard placement item (prep-site claim, unverified).
**What the interviewer is checking:** Handling repeated letters in a sort and comparing positions carefully.
**Say this in the interview:** "Alphabetical is A A A B D E S T. Against D A T A B A S E, the 2nd letter A and the 7th letter S match. Answer 2."
**Answer:** **2 letters (A in position 2 and S in position 7).**
**Step-by-step reasoning:**
1. DATABASE has 8 letters: D, A, T, A, B, A, S, E (three A's).
2. Alphabetical order: A, A, A, B, D, E, S, T.
3. Compare:

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Original | D | A | T | A | B | A | S | E |
| Sorted | A | A | A | B | D | E | S | T |
| Same? | no | yes | no | no | no | no | yes | no |

4. Two matches. The 4th and 6th letters are also A in the original, but the sorted word has B and E there.
**Fast method (30 seconds):** Sort the letters first (count the A's: three), write both words one under the other, and tick matching places.
**Check:** Verified by script: sorted word AAABDEST, matches at positions 2 and 7.
**Explain simply:**
- Alphabetical order means A to Z; repeated letters sit together.
- Only the letter at the same place counts, not the letter's presence in the word.
**Likely follow-ups:** 1) *Reverse alphabetical order?* Sorted is T S E D B A A A; positions 5 (B) and 6 (A) match, so 2 (verified by script). 2) *What if the question asked for the letters that move?* 8 - 2 = 6.
**Common mistakes / traps:** Forgetting that there are three A's (sorting to ABADEST-style errors), or counting the A's at positions 4 and 6 because "A is still an A".

### Q36 ⭐⭐ 🟡 How many sets of three different positive integers have a sum of 12 (order does not matter)?
**Asked at:** commonly asked (no company-specific report found); counting-sets items appear as differentiators in puzzle rounds (unverified).
**What the interviewer is checking:** Systematic listing without duplicates (smallest number first, then increasing).
**Say this in the interview:** "I list a < b < c with sum 12 starting from the smallest number: 1 gives four sets, 2 gives two, 3 gives one. That is 7."
**Answer:** **7 sets.**
**Step-by-step reasoning:**
1. Write each set as a < b < c, so every set is counted once (order does not matter).
2. a = 1: b + c = 11 with 1 < b < c: (2,9), (3,8), (4,7), (5,6), which is 4 sets.
3. a = 2: b + c = 10 with 2 < b < c: (3,7), (4,6), which is 2 sets. (5,5) is out since the numbers must differ.
4. a = 3: b + c = 9 with 3 < b < c: (4,5), 1 set.
5. a = 4: b + c = 8 with b >= 5 and c > b: b = 5 gives c = 3, impossible. Zero.
6. Total 4 + 2 + 1 = 7.
**Fast method (30 seconds):** Fix the smallest number and list the pairs in order; stop when a + (a+1) + (a+2) exceeds 12 (that is when a = 4).
**Check:** Verified by script (itertools combinations): (1,2,9), (1,3,8), (1,4,7), (1,5,6), (2,3,7), (2,4,6), (3,4,5), so 7.
**Explain simply:**
- A "set" has no order, so (1,2,9) and (9,2,1) are the same set.
- Listing smallest first is a standard way to avoid counting the same set twice.
**Likely follow-ups:** 1) *If order mattered?* Each set can be arranged in 3! = 6 ways, so 7 x 6 = 42 ordered triples. 2) *If repeats were allowed?* More sets would appear, such as (2,5,5) and (4,4,4).
**Common mistakes / traps:** Counting (2,5,5) or (4,4,4), or counting both (1,2,9) and (2,1,9).

### Q37 ⭐⭐ 🟡 Three interviewers rank four candidates. Interviewer 1: A, B, C, D. Interviewer 2: B, C, A, D. Interviewer 3: C, B, D, A (each list is best to worst). Using Borda scoring (4 points for first place, 3 for second, 2 for third, 1 for fourth), which candidate wins and with how many points?
**Asked at:** commonly asked (no company-specific report found); rank-aggregation is a differentiator item (unverified).
**What the interviewer is checking:** Whether you can convert ranks to points and add them up without slips.
**Say this in the interview:** "Borda gives 4, 3, 2, 1 points by place. B scores 3 + 4 + 3 = 10, C scores 2 + 3 + 4 = 9, A scores 7, D scores 4. B wins with 10."
**Answer:** **Candidate B wins with 10 points.**
**Step-by-step reasoning:**
1. A: 4 (first) + 2 (third) + 1 (fourth) = 7.
2. B: 3 (second) + 4 (first) + 3 (second) = 10.
3. C: 2 (third) + 3 (second) + 4 (first) = 9.
4. D: 1 + 1 + 2 = 4.
5. Check the total: 7 + 10 + 9 + 4 = 30 = 3 interviewers x (4+3+2+1).

| Candidate | Int. 1 | Int. 2 | Int. 3 | Total |
|---|---|---|---|---|
| A | 4 | 2 | 1 | 7 |
| B | 3 | 4 | 3 | 10 |
| C | 2 | 3 | 4 | 9 |
| D | 1 | 1 | 2 | 4 |

**Fast method (30 seconds):** Add the points and test that the grand total is 30 (each interviewer hands out 10 points). Any slip shows immediately.
**Check:** Verified by script: A 7, B 10, C 9, D 4.
**Explain simply:**
- Borda count is a voting method: each rank earns points, and the totals decide the winner.
- It rewards steady good placing, not only first places: B wins by being first or second with every interviewer.
**Likely follow-ups:** 1) *Who wins by "most first places"?* A, B and C each have one first place, so it is a three-way tie; Borda breaks it. 2) *What if points were 3, 2, 1, 0?* Each candidate loses 1 point per interviewer, so totals drop by 3 and the winner stays B (7 points).
**Common mistakes / traps:** Giving 1 point for first place, or mixing up which end of the list is "best".

### Q38 ⭐⭐ 🟡 In a certain code, '$' means '>', '#' means '<', '@' means '>=', '%' means '<=' and '*' means '='. Statement: A $ B * C % D # E. Conclusions: I. A > C. II. E > B. III. D >= B. IV. A is not equal to E. How many of the four conclusions definitely follow?
**Asked at:** commonly asked (no company-specific report found); coded inequalities are described as a standard type by prep sites (unverified).
**What the interviewer is checking:** Decoding, then testing each conclusion, including the weaker "not equal" type.
**Say this in the interview:** "Decoded: A > B = C <= D < E. I, II and III follow. IV needs a link between A and E across the valley at B and C, so it does not. Answer: 3."
**Answer:** **3 conclusions (I, II and III).**
**Step-by-step reasoning:**
1. Decode: A $ B becomes A > B; B * C becomes B = C; C % D becomes C <= D; D # E becomes D < E.
2. Chain: A > B = C <= D < E.
3. I. A > B = C, so A > C. True.
4. II. B = C <= D < E, so B < E, i.e. E > B. True.
5. III. B = C <= D, so D >= B. True.
6. IV. A and E are on opposite sides of the lowest group (B = C). A can be bigger than E or smaller than E, or equal to it, so "not equal" is not forced. Not definite.
**Fast method (30 seconds):** Find the lowest element (here B = C). Items on the same side of it, reading away from it, can be compared; items on opposite sides cannot.
**Check:** Verified by brute-force enumeration: I, II, III true in every case; IV true in some cases and false in others (for example A = E = 5 is allowed).
**Explain simply:**
- "A is not equal to E" is a claim about every possible case; one case where they are equal breaks it.
- "=" lets you merge B and C into one item in the chain.
**Likely follow-ups:** 1) *Does "A <= E" or "A >= E" follow?* Neither; both are open. 2) *Does "E > C" follow?* Yes, same reason as II since B = C.
**Common mistakes / traps:** Saying IV "follows" because the two ends look different, or misreading '%' as a percent sign instead of "<=".

### Q39 ⭐⭐ 🟡 Among 50 candidates ranked by test score with no ties, 18 scored more than Zoya. Yash scored less than Zoya, and 12 candidates scored less than Yash. How many candidates scored between Zoya and Yash?
**Asked at:** commonly asked (no company-specific report found); "people between two ranks" is a listed ranking variant on prep sites (unverified).
**What the interviewer is checking:** Converting counts above and below into ranks, then subtracting.
**Say this in the interview:** "Zoya is 19th from the top. Yash has 12 below, so he is 50 - 12 = 38th. People strictly between are 38 - 19 - 1 = 18."
**Answer:** **18 candidates.**
**Step-by-step reasoning:**
1. Zoya has 18 above her, so her rank from the top is 18 + 1 = 19.
2. Yash has 12 below him, so his rank from the bottom is 13 and his rank from the top is 50 + 1 - 13 = 38.
3. Yash is below Zoya (38 > 19), which matches the statement.
4. Between them: 38 - 19 - 1 = 18 candidates.
**Fast method (30 seconds):** Count the whole list as three blocks: 18 above Zoya, Zoya, the "between" block, Yash, 12 below Yash. Then between = 50 - 18 - 1 - 1 - 12 = 18.
**Check:** Computed by script both ways (rank difference and block subtraction), both 18.
**Explain simply:**
- Rank from top + rank from bottom = total + 1, because the person is counted in both.
- People strictly between two ranks = (difference of ranks) - 1.
**Likely follow-ups:** 1) *What if 18 scored more than Zoya and 12 scored less than her?* The counts would then need to fit the total of 50 (18 above, Zoya, 12 below makes 31, leaving 19 unplaced), so always check the totals match before answering. 2) *How many scored below Zoya?* The 18 between, Yash and the 12 below Yash: 18 + 1 + 12 = 31 (also 50 - 19 = 31).
**Common mistakes / traps:** Answering 19 (38 - 19) by forgetting to remove the two endpoints, or treating "18 scored more than Zoya" as Zoya's rank 18.

### Q40 ⭐⭐ 🟡 State the conditions under which an "either I or II follows" answer is correct in inequality questions, and show them on a short example.
**Asked at:** commonly asked (no company-specific report found); either-or items are listed among the harder coded-inequality types on prep sites (unverified).
**What the interviewer is checking:** Whether you know that "either-or" is a statement about two conclusions together, not about one of them alone.
**Say this in the interview:** "I use either-or only when both conclusions compare the same two things, neither is definitely true on its own, and between them they cover every possible case. Then one of them must be true, so I answer 'either I or II'."
**Answer:** **All three conditions must hold: (1) both conclusions involve the same pair of elements; (2) neither conclusion follows by itself; (3) the two together are exhaustive, so at least one of them is true in every possible case.**
**Step-by-step reasoning:**
1. Check each conclusion alone first. If one already follows, answer that one; either-or is for when neither does.
2. Check that both name the same pair, for example A and C.
3. Ask: can I find a case where both are false? If not, they are exhaustive.
4. Example: Statement A >= B <= C. Conclusions I. A > C, II. A <= C. B is the smallest, so A and C are not linked: A may be bigger, smaller or equal to C. I alone is not sure, II alone is not sure. But "A > C" or "A <= C" covers every case, so the answer is **either I or II**.
Common exhaustive pairs: (> and <=), (>= and <), (< and >=), (<= and >). The pair (> and <) is not exhaustive because "=" is left out.
**Check:** Enumerated all values 0 to 3 for A, B, C with A >= B <= C: A > C, A < C and A = C all occur, and "A > C or A <= C" is true in every case (verified by script).
**Explain simply:**
- "Exhaustive" means the two statements together leave no gap.
- "Either-or" does not mean both are possible; it means one of them is certainly true, you just cannot say which.
**Likely follow-ups:** 1) *Conclusions are A > C and A < C, what now?* "A = C" is still possible, so neither follows (answer "neither"). 2) *Conclusions are A >= C and A <= C?* They cover every case, so either-or is the usual exam answer (A = C makes both true, so strictly one-and-only-one is not guaranteed; how an exam treats this varies, so say your reading aloud. The usual rule of thumb is from memory, unverified).
**Common mistakes / traps:** Using either-or when the conclusions involve different pairs; using it for > and < and forgetting that equality is a third case; picking either-or when one conclusion is already definitely true.

### Q41 ⭐⭐ 🔴 Four trainees A, B, C and D finish a certification in different positions (1st to 4th, no ties). Exactly two of these five statements are true: (1) A finished immediately ahead of C. (2) A finished ahead of C. (3) A finished ahead of B. (4) B finished ahead of C. (5) C finished last. In what order did they finish?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Handling "exactly k statements are true" by case testing and spotting hidden links between clues.
**Say this in the interview:** "Statement 1 implies statement 2, so they are linked. I test the cases and find only one order that gives exactly two true statements: A, D, C, B."
**Answer:** **A finished 1st, D 2nd, C 3rd, B 4th.**
**Step-by-step reasoning:**
1. Note (1) "immediately ahead" implies (2) "ahead". So if (1) is true, (2) is true too, and then (3), (4), (5) must all be false.
2. Try that: (3) false means B is ahead of A; (4) false means C is ahead of B; so C is ahead of B, B ahead of A, but (2) says A is ahead of C. Contradiction. So (1) is false.
3. With (1) false, exactly two of (2), (3), (4), (5) are true. Of the 18 orders in which (1) is false, only one gives exactly two true (checked by script).
4. Final order and truth table:
 Position: 1 A, 2 D, 3 C, 4 B
 (1) false (D sits between A and C); (2) true; (3) true; (4) false (B is behind C); (5) false (B is last, not C). Two true.
**Fast method (30 seconds):** Spot the implication (1) then (2): it removes a whole case, then check the rest.
**Check:** Brute force over all 24 orders: exactly one order has exactly two true statements (verified by script).
**Explain simply:**
- "Exactly two true" means you must also confirm the other three are false, not just find two true ones.
- Linked statements (one implying another) shrink the cases you must try.
**Likely follow-ups:** 1) *Why is the answer unique?* The brute force over all 24 orders found just one. 2) *Which statements are true in it?* (2) and (3).
**Common mistakes / traps:** Stopping when two statements are true without checking the rest; treating (1) and (2) as independent.

### Q42 ⭐⭐ 🔴 From the statement A > B >= C = D < E <= F, for how many of the 15 pairs of letters can you say for sure which letter of the pair is strictly greater?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Telling a sure comparison from an unknown one across a mixed chain with "=" and ">=" signs.
**Say this in the interview:** "A sure strict comparison needs a path through the chain with at least one strict sign and all signs pointing the same way. Counting pairs gives 7 of 15."
**Answer:** **7 pairs**
**Step-by-step reasoning:**
1. Chain: A > B >= C = D < E <= F. Left of D the chain goes down from A; right of D it goes up to F.
2. A is strictly above B (>), and B >= C = D, so A is strictly above B, C, D: pairs AB, AC, AD.
3. D < E and C = D, so E and F are strictly above C and D: pairs CE, CF, DE, DF.
4. Pairs left unsure: AE, AF (A is above D, E is above D, no link), BC (only >=, may be equal), BD (same), BE, BF (B and E both sit above C/D with no link), CD (equal, not strictly greater), EF (only <=, may be equal). That is 8.
5. 15 - 8 = 7.
**Check:** Enumerated all assignments of values 0 to 5 to the six letters that fit the chain (371 of them) and counted pairs where one letter is strictly greater in every one: AB, AC, AD, CE, CF, DE, DF = 7 (verified by script).
**Explain simply:**
- "Strictly greater" means greater with no chance of equal.
- A path of ">=" and "=" alone can only give "greater or equal", never strict.
**Likely follow-ups:** 1) *Is B > E for sure?* No: B and E both sit above C and D with no path between them. 2) *If B >= C became B > C?* BC, BD become sure too: 9 pairs.
**Common mistakes / traps:** Counting BC or BD as strict; counting CD (they are equal); counting pairs across the "valley" (A with E) that have no path.

### Q43 ⭐⭐ 🔴 Eight reports A to H are reviewed one at a time in positions 1 to 8. Exactly two reports are reviewed between C and D, with C reviewed before D. A is reviewed immediately after F. G is reviewed after D. B is reviewed immediately after G. H is reviewed before C. A is reviewed before D. E is reviewed after B. Which report is reviewed 3rd?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Building one long order from many clues by chaining fixed-gap pairs first.
**Say this in the interview:** "I bind the glued pairs (F-A and G-B), use the gap of two between C and D, then fit everyone. The only order is H, C, F, A, D, G, B, E, so F is 3rd."
**Answer:** **F is reviewed 3rd.**
**Step-by-step reasoning:**
1. Glue pairs: F A (A right after F) and G B (B right after G). C _ _ D (two between, so D is 3 places after C).
2. Clues in order: H before C; C is 3 places before D; A before D; D before G; G B glued; E after B. So G, B, E come after D (3 reports), and H, C come before D.
3. H is before C, so C is at position 2 or later, so D is at position 5 or later. G, B, E need 3 positions after D, so D is at position 5 or earlier. Hence D = 5, C = 2, H = 1.
4. Remaining: F A glued (A before D), so F A fill 3 and 4. After D: G 6, B 7, E 8.
5. Every clue checks (see Check).
Final arrangement: 1 H, 2 C, 3 F, 4 A, 5 D, 6 G, 7 B, 8 E.
**Fast method (30 seconds):** Find the most constrained report (D: needs C, H, F, A before it and G, B, E after it, so it must be 5th: 4 before, 3 after).
**Check:** Tested all 40320 orders: exactly one satisfies every clue (verified by script).
**Explain simply:**
- "Immediately after" glues two reports into one block.
- Counting how many reports must come before and after a report can pin it down.
**Likely follow-ups:** 1) *Which report is 6th?* G. 2) *Which report is reviewed last?* E (8th).
**Common mistakes / traps:** Reading "two between" as "two places apart" (it is a gap of 3); forgetting H must be before C.

### Q44 ⭐⭐ 🔴 Seven people A to G stand in a queue (position 1 is the front). C stands two places behind F. E stands immediately behind C. G stands immediately behind A. D is at the back. A stands ahead of F. B stands behind F. Who stands 4th?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Combining fixed gaps and "ahead/behind" clues in a queue.
**Say this in the interview:** "I make blocks: A G together, and F _ C E (C two behind F, E right behind C). D is last. Then B must fit behind F. The queue is A, G, F, B, C, E, D, so 4th is B."
**Answer:** **B stands 4th.**
**Step-by-step reasoning:**
1. D is at position 7.
2. Block 1: A then G (G right behind A). Block 2: F, one gap, C, E (positions f, f+2, f+3).
3. A is ahead of F; B is behind F. Positions 1 to 6 hold A, G, F, C, E, B.
4. If A G come first (positions 1, 2), F is 3, the gap is 4, C 5, E 6, and B must fill the gap at 4. B is behind F, which is true.
5. Other placements fail: A G cannot sit between F and C without breaking "A ahead of F"; A G after F is also forbidden; and F cannot be later than 3 since C and E need positions up to f+3 <= 6.
Final queue: 1 A, 2 G, 3 F, 4 B, 5 C, 6 E, 7 D.
**Check:** All 5040 orders tested: only one fits (verified by script).
**Explain simply:**
- "Two places behind" means a gap of one person between them.
- The gap person must satisfy the other clues; here B fits exactly.
**Likely follow-ups:** 1) *Who is 5th?* C. 2) *Who stands last but one?* E (6th).
**Common mistakes / traps:** Putting E two places behind C; ignoring that the gap between F and C must be filled by someone.

### Q45 ⭐ 🟡 Five interview slots are filled by candidates A, B, C, D and E, one per slot. A must be interviewed before B, and C before D. E can be anywhere. How many different slot orders are possible?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Counting orders under "before" constraints using symmetry.
**Say this in the interview:** "Each independent pair is in the right order in half of all arrangements. 120 times half times half is 30."
**Answer:** **30 orders**
**Step-by-step reasoning:**
1. Without rules, 5 candidates can be ordered in 5! = 120 ways.
2. For any arrangement, A is before B or after B; swapping them flips this. So exactly half (60) have A before B.
3. C before D is independent of A before B, so half of those again: 120 x 1/2 x 1/2 = 30.
**Check:** Brute force over all 120 permutations gave 30 (verified by script).
**Explain simply:**
- "Independent" here means the two rules involve different people, so each cuts the count in half.
- Factorial (n!) means n x (n-1) x ... x 1.
**Likely follow-ups:** 1) *If A before B and B before C?* 120/6 = 20 (see Q46). 2) *Add D before E too (so C before D before E, and A before B)?* The order of C, D, E is fixed (1 in 6) and A before B is 1 in 2: 120/12 = 10 (brute-forced).
**Common mistakes / traps:** Counting E as restricted; adding instead of multiplying fractions.

### Q46 ⭐ 🟡 Five candidates A to E are interviewed one per slot. A must be interviewed before B and B before C; D and E are unrestricted. How many different orders are possible?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Counting orders where three people must be in a fixed relative order.
**Say this in the interview:** "Three candidates can be ordered 3! = 6 ways but only one of those is allowed, so 120 divided by 6 is 20."
**Answer:** **20 orders**
**Step-by-step reasoning:**
1. All orders: 5! = 120.
2. Look only at the relative order of A, B, C: 6 possibilities, equally common.
3. Only A, B, C in that exact order is allowed: 1 of 6. 120/6 = 20.
Another way: pick 3 of 5 slots for A, B, C (they go in order): C(5,3) = 10; place D and E in the other 2 slots: 2 ways; 10 x 2 = 20.
**Check:** Brute force over 120 permutations gave 20 (verified by script).
**Explain simply:**
- C(5,3) means "5 choose 3", the number of ways to pick 3 items from 5 without caring about order.
- A fixed order of k people divides the count by k!.
**Likely follow-ups:** 1) *If D must also be before E?* 120/(6x2) = 10. 2) *Only A before B?* 60.
**Common mistakes / traps:** Dividing by 3 instead of 3!; thinking D and E can be placed only at the ends.

### Q47 ⭐ 🟡 In how many different orders can four candidates A, B, C and D finish if A does not finish first and D does not finish last (no ties)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Inclusion and exclusion counting for "not" restrictions.
**Say this in the interview:** "Total 24. Subtract orders where A is first (6) and where D is last (6), then add back where both happen (2), since I subtracted those twice. 24 - 6 - 6 + 2 = 14."
**Answer:** **14 orders**
**Step-by-step reasoning:**
1. All orders: 4! = 24.
2. A first: the other 3 arrange in 3! = 6 ways.
3. D last: also 6 ways.
4. Both (A first and D last): B, C in the middle: 2 ways.
5. Bad orders = 6 + 6 - 2 = 10. Good orders = 24 - 10 = 14.
**Check:** Brute force over 24 permutations gave 14 (verified by script).
**Explain simply:**
- Inclusion and exclusion: subtract each bad group, then add back the overlap counted twice.
**Likely follow-ups:** 1) *If B also may not be 2nd?* Re-count by the same method (use brute force to confirm). 2) *With 5 people, A not first, E not last?* 120 - 24 - 24 + 6 = 78.
**Common mistakes / traps:** Subtracting 6 + 6 = 12 and answering 12; forgetting the overlap.

### Q48 ⭐ 🟡 How many comparisons between two salaries are needed, at minimum, to find the highest of 16 different salaries, and why can you not do it with fewer?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can give a lower bound with a clean argument, not just a number.
**Say this in the interview:** "15 comparisons. Every salary except the top one must lose at least one comparison, and each comparison produces only one loser, so 15 comparisons are needed and a knockout tournament does it."
**Answer:** **15 comparisons (n - 1 for n = 16).**
**Step-by-step reasoning:**
1. Achieve it: pair the 16 up (8 comparisons), then 8 winners (4), then 4 (2), then 2 (1)... 8 + 4 + 2 + 1 = 15. The last winner is the maximum.
2. Why not fewer: 15 salaries are not the highest, and each must be seen to lose to someone. A comparison has one loser, so you need at least 15 comparisons.
**Check:** 8 + 4 + 2 + 1 = 15 (hand-checked); n - 1 is the known result for finding a maximum.
**Explain simply:**
- A "knockout" tournament means winners meet winners.
- If only 14 comparisons were made, two values would never have lost, and you could not tell which is bigger.
**Likely follow-ups:** 1) *How many for 100 values?* 99. 2) *Does the order of comparisons matter?* Not for the count; any approach needs n - 1.
**Common mistakes / traps:** Answering 16 or 4 (log2 16); the tournament depth (4 rounds) is not the comparison count.

### Q49 ⭐ 🟡 How many integer triples a < b < c are possible if every value lies between 3 and 9 inclusive?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Recognising that an increasing triple is just a choice of 3 numbers.
**Say this in the interview:** "Values 3 to 9 are 7 numbers. Any 3 different ones can be put in just one increasing order, so it is 7 choose 3 = 35."
**Answer:** **35 triples**
**Step-by-step reasoning:**
1. The numbers available: 3, 4, 5, 6, 7, 8, 9: 7 numbers.
2. Choose any 3 different numbers. Sorted, they form exactly one triple a < b < c.
3. Count: C(7,3) = 7 x 6 x 5 / (3 x 2 x 1) = 35.
**Check:** Listing all combinations of 3 from the 7 numbers gave 35 (verified by script).
**Explain simply:**
- Order does not matter when the order is forced to be increasing.
**Likely follow-ups:** 1) *If values may repeat (a <= b <= c)?* C(9,3) = 84. 2) *Between 1 and 9 inclusive?* C(9,3) = 84 strictly increasing.
**Common mistakes / traps:** Using 7 x 6 x 5 = 210 (counts orderings); using 6 numbers (forgetting that 9 is included).

### Q50 ⭐ 🔴 What is the minimum number of pairwise comparisons needed to find both the highest and the lowest of 8 different values, and how do you achieve it?
**Asked at:** commonly asked (no company-specific report found); the minimum-comparison puzzle is a classic algorithm item (unverified for analyst rounds).
**What the interviewer is checking:** Whether you can improve on the obvious method by a smarter pairing trick.
**Say this in the interview:** "Pair them up: 4 comparisons. Compare the 4 winners to find the max: 3 more. Compare the 4 losers to find the min: 3 more. 4 + 3 + 3 = 10, and this is known to be the minimum."
**Answer:** **10 comparisons** (formula ceil(3n/2) - 2 with n = 8).
**Step-by-step reasoning:**
1. Split 8 values into 4 pairs and compare each pair: 4 comparisons. Now you have 4 winners and 4 losers.
2. The maximum must be among the winners; find it with 3 comparisons.
3. The minimum must be among the losers; find it with 3 comparisons.
4. Total = 4 + 3 + 3 = 10.
5. The naive method (find max in 7, then min in the remaining 7) needs 7 + 6 = 13.
**Check:** Simulated the method on 2000 random orders of 8 values: always 10 comparisons and correct max and min (verified by script). That 10 cannot be beaten is a known result, not re-derived here.
**Explain simply:**
- A "winner" is the larger of a compared pair; the max cannot be a loser, the min cannot be a winner.
- The saving comes from not comparing every value against both extremes.
**Likely follow-ups:** 1) *For 9 values?* ceil(27/2) - 2 = 12. 2) *For 16 values?* 24 - 2 = 22.
**Common mistakes / traps:** Answering 14 (7 + 7) or 13.

### Q51 ⭐ 🔴 What is the minimum number of pairwise comparisons needed in the worst case to find the second-highest of 8 different values, and how do you achieve it?
**Asked at:** commonly asked (no company-specific report found); a classic algorithm puzzle (unverified for analyst rounds).
**What the interviewer is checking:** Seeing that the second-highest must have lost directly to the highest, so you only need to check those losers.
**Say this in the interview:** "Run a knockout tournament: 7 comparisons find the max. The second-best lost only to the winner, and the winner played 3 matches, so compare those 3 losers: 2 more. Total 9."
**Answer:** **9 comparisons** (n + ceil(log2 n) - 2 = 8 + 3 - 2).
**Step-by-step reasoning:**
1. Knockout tournament on 8 values: 4 + 2 + 1 = 7 comparisons. Record who each player beat.
2. The overall winner played 3 matches (log2 8 = 3), so beat 3 values.
3. The second-highest value can only have lost to the winner (otherwise someone else would also be above it), so it is among those 3 values.
4. Find the max of these 3: 2 comparisons.
5. Total 7 + 2 = 9.
**Check:** Simulated on 2000 random orders: always 9 comparisons and the correct second-highest (verified by script). That 9 cannot be beaten is the known result, not re-derived here.
**Explain simply:**
- Only players who lost directly to the champion can be second best.
- Keeping a list of who each winner beat is the trick.
**Likely follow-ups:** 1) *For 16 values?* 16 + 4 - 2 = 18. 2) *Simple method (find max, remove, find max again)?* 7 + 6 = 13.
**Common mistakes / traps:** Answering 13; comparing all other values with the winner.
