# Book 13 — Logical Reasoning & Analytical Thinking | Part 2: Deductive Logic and Conditional Reasoning 🟡

**Target:** 70 questions | **Actual:** 73 questions
**Scope:** Deductive logic: syllogisms (Venn and possibility cases, either-or), "only/all/some/none" statements, conditional logic (if-then, converse, inverse, contrapositive, unless, only if), and common fallacies; syllogism conventions: "some" means at least one and every named group is non-empty.

### Q1 ⭐⭐⭐ 🟢 Statements: Some analysts are auditors. Some auditors are lawyers. Conclusions: I. Some analysts are lawyers. II. Some lawyers are analysts. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); syllogisms appear in prep-site lists for TCS NQT, Infosys, Wipro and Mu Sigma (prep-site claim, unverified).
**What the interviewer is checking:** Whether you know that two "some" statements never link the outer groups.
**Say this in the interview:** "Two 'some' statements give no definite connection between analysts and lawyers, because the auditors who are analysts may be different people from the auditors who are lawyers. So neither conclusion follows."
**Answer:** **Neither I nor II follows.**
**Step-by-step reasoning:**
1. Convention: "some" means at least one; every named group (analysts, auditors, lawyers) has at least one member.
2. Draw Auditors as a circle. Analysts overlap it somewhere; Lawyers overlap it somewhere.
3. Nothing forces the two overlaps to be in the same place. Draw Analysts and Lawyers as two separate circles that each touch Auditors in different spots.
4. In that drawing no analyst is a lawyer, so I is false, and II (the same claim reversed) is false too.
5. A conclusion "follows" only if it is true in every possible drawing. One counter-drawing is enough to reject it.
**Fast method (30 seconds):** If both statements are "some" (no "all" or "no"), nothing follows about the two outer groups. Try the separate-circles drawing first.
**Check:** Verified by script: I enumerated all 160 ways of filling the 8 Venn regions that satisfy the convention; I and II are each false in some of them.
**Explain simply:**
- A Venn diagram is overlapping circles; each circle is a group.
- "Some" only guarantees an overlap exists, never which people are in it.
- "Follows" means true in every possible drawing, not just in one you like.
**Likely follow-ups:** 1) *Does "Some analysts are auditors" let you say "Some auditors are analysts"?* Yes, "some" statements can be reversed. 2) *What if the second statement were "All auditors are lawyers"?* Then I follows: the analyst-auditors are lawyers (hand-checked).
**Common mistakes / traps:** Chaining the two "some" statements like a relay (analysts to auditors to lawyers). That works for "all", not for "some".

### Q2 ⭐⭐⭐ 🟢 Statements: All reports are dashboards. Some dashboards are charts. Conclusions: I. Some reports are charts. II. Some charts are dashboards. III. No reports are charts. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); statement-conclusion items are reported for Mu Sigma and TCS NQT by prep sites (unverified).
**What the interviewer is checking:** Reversing a "some" statement correctly and not over-reading it.
**Say this in the interview:** "Only II follows. 'Some dashboards are charts' reverses to 'some charts are dashboards'. The reports sit inside dashboards, but the chart overlap could be in a different part of the dashboards, so I and III are only possible."
**Answer:** **Only II follows.**
**Step-by-step reasoning:**
1. Draw Reports fully inside Dashboards.
2. Charts overlap Dashboards. The overlap may be in the part outside Reports, or may include some Reports.
3. II is the same fact as the second statement read backwards, so it is always true.
4. I fails in the drawing where the chart overlap lies outside Reports.
5. III fails in the drawing where charts overlap Reports. So both I and III are possible but not certain.
**Fast method (30 seconds):** Reverse each "some" statement; those reversals follow automatically. Then test every other conclusion by looking for one drawing that breaks it.
**Check:** Verified by script over all 40 models: II is true in all; I and III are true in some and false in others (I and III are direct opposites, so exactly one of them is always true, but neither is certain).
**Explain simply:**
- "All X are Y" puts X inside Y.
- "Some" can be flipped; "all" cannot be flipped.
- A "possible" conclusion is not a "follows" conclusion.
**Likely follow-ups:** 1) *Does "Some dashboards are reports" follow?* Yes, all reports are dashboards and reports exist, so at least one dashboard is a report. 2) *Does "All dashboards are reports" follow?* No (the reverse of "all" is not valid).
**Common mistakes / traps:** Picking I because reports are "inside" dashboards, which feels connected to charts. Being inside the bigger circle does not mean touching the chart circle.

### Q3 ⭐⭐⭐ 🟢 What is the contrapositive of "if a payment is late, a fee applies", and is it equivalent to the original statement?
**Asked at:** commonly asked (no company-specific report found); the contrapositive is listed as the one valid rewrite of an if-then in prep sites (unverified).
**What the interviewer is checking:** Whether you can flip and negate both parts correctly.
**Say this in the interview:** "The contrapositive is: if no fee applies, then the payment is not late. It is exactly equivalent to the original, because if lateness always brings a fee, a missing fee proves there was no lateness."
**Answer:** **Contrapositive: "If no fee applies, the payment is not late." Yes, it is logically equivalent to the original.**
**Step-by-step reasoning:**
1. Original has the form "If P then Q", with P = payment is late, Q = a fee applies.
2. Contrapositive = "If not Q then not P": swap the two parts and negate both.
3. So: if no fee applies, the payment is not late.
4. Why equivalent: the original says "late" never occurs without a fee. If there is no fee, "late" cannot have occurred.
**Check:** Verified by script: the truth tables of "P then Q" and "not Q then not P" match in all four P/Q combinations.
**Explain simply:**
- Contrapositive means "turn it around and negate both parts".
- Equivalent means the two statements are true or false together in every situation.
- Only the contrapositive keeps the meaning; reversing or negating alone does not.
**Likely follow-ups:** 1) *Is "If a fee applies, the payment is late" equivalent?* No, that is the converse; the fee could apply for another reason. 2) *Is "If the payment is not late, no fee applies" equivalent?* No, that is the inverse.
**Common mistakes / traps:** Only swapping (that is the converse) or only negating (that is the inverse). Both are not equivalent to the original.

### Q4 ⭐⭐⭐ 🟢 For the statement "If P then Q", what are its converse, inverse and contrapositive, and which of them are logically equivalent to the original?
**Asked at:** commonly asked (no company-specific report found); a standard topic in deductive-reasoning prep material (unverified).
**What the interviewer is checking:** Precise vocabulary for the three rewrites and which one preserves meaning.
**Say this in the interview:** "Converse swaps: if Q then P. Inverse negates: if not P then not Q. Contrapositive does both: if not Q then not P. Only the contrapositive is equivalent to the original; the converse and the inverse are equivalent to each other but not to the original."
**Answer:** **Converse: if Q then P. Inverse: if not P then not Q. Contrapositive: if not Q then not P. Only the contrapositive is equivalent to the original.**
**Explain simply:**
- Converse = swap the parts. Inverse = negate the parts. Contrapositive = swap and negate.
- Worked example: "If it is a square (P), it has four sides (Q)." Converse: if it has four sides, it is a square (false, a rectangle). Inverse: if it is not a square, it does not have four sides (false, same rectangle). Contrapositive: if it does not have four sides, it is not a square (true).
- The converse and inverse are contrapositives of each other, so they always have the same truth value, but that value can differ from the original.
**Check:** Verified by script for original versus contrapositive (and versus converse, inverse); converse equals inverse hand-checked (they are each other's contrapositive). The original differs from the converse when P is false and Q is true.
**Likely follow-ups:** 1) *What name has the mistake of treating the converse as true?* Affirming the consequent. 2) *And treating the inverse as true?* Denying the antecedent.
**Common mistakes / traps:** Thinking "converse" or "inverse" keep the meaning because they "sound the same". A true statement can have a false converse (square and rectangle).

### Q5 ⭐⭐⭐ 🟢 What does "Only A are B" mean, how does it differ from "All A are B", and which Venn diagram does it give?
**Asked at:** commonly asked (no company-specific report found); "only" statements are listed as a standard syllogism variant on prep sites (unverified).
**What the interviewer is checking:** Whether you reverse "only" correctly.
**Say this in the interview:** "'Only A are B' means every B is an A, so B sits inside A. 'All A are B' is the opposite way round: A sits inside B. 'Only' reverses the direction."
**Answer:** **"Only A are B" means "All B are A": the B circle lies inside the A circle (some A may be outside B). It is not the same as "All A are B".**
**Explain simply:**
- "Only A are B": nobody outside A can be a B, so B is the small circle inside A.
- "All A are B": A is the small circle inside B.
- Worked example: "Only analysts are managers" gives "every manager is an analyst". It does not say every analyst is a manager.
- A trick: "only A are B" is like "B only if A".
**Check:** Hand-checked with a 60-person example: if 36 are managers and all of them are analysts, then at most 36 of the 45 analysts are managers, which is consistent; the reverse reading would force 45 managers.
**Likely follow-ups:** 1) *What does "Only A are B" say about people who are not A?* None of them is B. 2) *Is "Only A are B" the same as "No non-A is B"?* Yes.
**Common mistakes / traps:** Reading "only A are B" as "all A are B". This is the most common slip in "only" questions.

### Q6 ⭐⭐⭐ 🟢 What is the difference between a conclusion that "follows" (definitely true) and one that is only "possible", and how do you decide in a Venn diagram?
**Asked at:** commonly asked (no company-specific report found); the follows/possible distinction is core to statement-conclusion items reported for Mu Sigma (prep-site claim, unverified).
**What the interviewer is checking:** Whether you understand "true in every case" versus "true in some case".
**Say this in the interview:** "A conclusion follows only if it is true in every diagram that fits the statements. If I can draw one fitting diagram where it is false, it does not follow; if it is true in some diagrams and false in others, it is only possible."
**Answer:** **Follows = true in every valid diagram. Possible only = true in some valid diagrams and false in others. A conclusion false in every diagram is contradicted.**
**Explain simply:**
- Draw the statements in the most spread-out way and in the most overlapping way. Test the conclusion in both.
- Worked example: "Some analysts are auditors; some auditors are lawyers." "Some analysts are lawyers" is true if the overlaps coincide and false if they do not, so it is only possible.
- Statement-conclusion questions ask "follows", never "possible", so only keep conclusions true in every diagram.
**Check:** Verified by script: for Q1, Q2 and Q11 I counted, over every model, whether each conclusion was true always, sometimes or never.
**Likely follow-ups:** 1) *Is "all" stronger than "some"?* Yes; "all A are B" guarantees an overlap, so "some A are B" follows (given A is not empty). 2) *Can a conclusion be neither follows nor possible?* Yes: contradicted ones, where it is false in every diagram.
**Common mistakes / traps:** Choosing a conclusion because it matches the diagram you drew first. Always try to break it with a second diagram.

### Q7 ⭐⭐⭐ 🟢 Statement: "If the audit is passed, the licence is renewed." Which of these is logically equivalent to it? (a) If the licence is renewed, the audit was passed. (b) If the audit is not passed, the licence is not renewed. (c) If the licence is not renewed, the audit was not passed. (d) The licence is renewed only if the audit is not passed.
**Asked at:** commonly asked (no company-specific report found); equivalence-spotting among converse/inverse/contrapositive is the typical conditional item (prep-site topic, unverified).
**What the interviewer is checking:** Spotting the contrapositive among look-alike options.
**Say this in the interview:** "The original is P then Q, with P = audit passed and Q = licence renewed. The contrapositive is not Q then not P: if the licence is not renewed, the audit was not passed. That is option (c)."
**Answer:** **(c)**
**Step-by-step reasoning:**
1. (a) is "if Q then P": the converse, not equivalent.
2. (b) is "if not P then not Q": the inverse, not equivalent.
3. (c) is "if not Q then not P": the contrapositive, equivalent.
4. (d) says "Q only if not P": "if Q then not P", which contradicts the original idea; not equivalent.
**Fast method (30 seconds):** Look for the option that swaps the two parts and negates both.
**Check:** Verified by script: only (c) has the same truth table as P then Q.
**Explain simply:**
- Contrapositive is the only valid rewrite of an if-then.
- Converse and inverse look natural but are different claims.
- "Q only if R" means "if Q then R".
**Likely follow-ups:** 1) *If the licence was renewed, can you say the audit was passed?* No, the licence could be renewed another way. 2) *Which option is a fallacy named "affirming the consequent"?* (a).
**Common mistakes / traps:** Picking (a) because it "feels like the same story reversed", or (d) because it contains "only if" and sounds formal.

### Q8 ⭐⭐⭐ 🟢 Rule: "If a number is divisible by 6, it is divisible by 3." Which number is a counter-example to the converse? (a) 9 (b) 12 (c) 18 (d) 24
**Asked at:** commonly asked (no company-specific report found); a standard converse/counter-example item (unverified).
**What the interviewer is checking:** Writing the converse correctly and then hunting for a case that breaks it.
**Say this in the interview:** "The converse is: if a number is divisible by 3, it is divisible by 6. A counter-example must be divisible by 3 but not by 6. 9 works."
**Answer:** **(a) 9**
**Step-by-step reasoning:**
1. Converse of "if 6 then 3" is "if divisible by 3 then divisible by 6".
2. Check each number: 9 is divisible by 3 but not by 6, so it breaks the converse.
3. 12, 18 and 24 are all divisible by both 3 and 6, so they agree with the converse and are not counter-examples.
**Check:** Verified by script: among 9, 12, 18, 24 only 9 is divisible by 3 and not by 6.
**Explain simply:**
- A counter-example is one case that makes the "if" part true and the "then" part false.
- One counter-example is enough to prove a statement false.
- The original rule has no counter-example (every multiple of 6 is a multiple of 3), but its converse does.
**Likely follow-ups:** 1) *Give another counter-example.* 15 or 21. 2) *Is the original rule true for all numbers?* Yes, since 6 = 2 x 3.
**Common mistakes / traps:** Choosing a number divisible by 6, because it fits the original rule and not the converse.

### Q9 ⭐⭐⭐ 🟢 Statement: "All invoices in the batch are valid." Which of these is its negation? (a) No invoice in the batch is valid. (b) Some invoice in the batch is not valid. (c) All invoices in the batch are invalid. (d) Some invoices in the batch are valid.
**Asked at:** commonly asked (no company-specific report found); negation of "all" is a standard trap in deductive tests (unverified).
**What the interviewer is checking:** Negating "all" properly.
**Say this in the interview:** "To deny 'all are valid' I only need one invalid invoice. So the negation is 'at least one invoice is not valid', option (b)."
**Answer:** **(b)**
**Step-by-step reasoning:**
1. "All are valid" is broken by a single invalid invoice.
2. So its negation is "some invoice is not valid".
3. (a) and (c) are far too strong: they say every invoice is invalid. If one invoice is valid and one is not, "all valid" is false, but (a) and (c) are also false.
4. (d) is compatible with "all valid", so it cannot be its negation.
**Check:** Hand-checked with a batch of two invoices (one valid, one invalid): "all valid" is false, (b) is true, (a), (c) are false.
**Explain simply:**
- The negation of a statement is true exactly when the statement is false.
- Negation of "all" is "some not"; negation of "some" is "none".
**Likely follow-ups:** 1) *Negate "Some invoices are valid".* No invoice is valid. 2) *Negate "No invoice is valid".* Some invoice is valid.
**Common mistakes / traps:** Choosing "none are valid" (the opposite, not the negation).

### Q10 ⭐⭐⭐ 🟢 In a firm of 60 employees, 36 are managers, 45 are analysts, and the rule "Only analysts are managers" holds. How many analysts are not managers?
**Asked at:** commonly asked (no company-specific report found); set-and-count with an "only" statement is a typical gate item (unverified).
**What the interviewer is checking:** Turning "only" into "all managers are analysts" and then counting.
**Say this in the interview:** "'Only analysts are managers' means every manager is an analyst. So all 36 managers are among the 45 analysts, which leaves 45 minus 36 = 9 analysts who are not managers."
**Answer:** **9 analysts are not managers.**
**Step-by-step reasoning:**
1. "Only analysts are managers" = "All managers are analysts".
2. So the manager circle sits fully inside the analyst circle.
3. Analysts who are managers = 36.
4. Analysts who are not managers = 45 - 36 = 9.
5. The total of 60 is not needed for this; it just tells us there are 60 - 45 = 15 non-analysts.
**Check:** Verified by arithmetic script and by hand: 36 + 9 + 15 = 60, consistent.
**Explain simply:**
- "Only" reverses the direction (see Q5).
- When one group is inside another, the difference of the counts is the leftover.
**Likely follow-ups:** 1) *If the rule were "All analysts are managers", what would happen?* 45 analysts would all be managers, and there would be 36 managers in total, which is impossible (45 > 36). 2) *How many employees are neither analysts nor managers?* 15.
**Common mistakes / traps:** Answering 60 - 36 = 24 or 60 - 45 = 15, or letting the 60 mislead you.

### Q11 ⭐⭐⭐ 🟡 Statements: No testers are developers. Some developers are managers. Conclusions: I. Some managers are not testers. II. Some managers are not developers. III. No managers are testers. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); prep sites report syllogisms in TCS NQT, Infosys and Wipro papers (unverified).
**What the interviewer is checking:** Mixing a "no" statement with a "some" statement and deriving a "some not" conclusion.
**Say this in the interview:** "The managers who are developers cannot be testers, because no tester is a developer. So some managers are not testers, which is I. II and III can fail, so they only might be true."
**Answer:** **Only I follows.**
**Step-by-step reasoning:**
1. At least one developer is a manager (second statement).
2. No developer is a tester, so that manager is not a tester.
3. Hence some managers are not testers: I follows.
4. II: all managers could be developers, so it can fail.
5. III: some other managers might be testers (they do not have to be developers), so it can fail.
**Fast method (30 seconds):** "Some" plus "no" gives a "some not". Take the "some" overlap and push it away from the "no" group.
**Check:** Verified by script over all 24 models.
**Explain simply:**
- "No X are Y" means the circles do not touch.
- If managers who are developers exist, they sit outside the tester circle.
**Likely follow-ups:** 1) *Does "No managers are developers" follow?* No, it contradicts the second statement. 2) *Does "Some managers are testers" follow?* No, only possible.
**Common mistakes / traps:** Choosing III because "no testers are developers" sounds like it should extend to managers.

### Q12 ⭐⭐⭐ 🟡 Statements: All clerks are staff. No staff are trainees. Conclusions: I. No clerks are trainees. II. Some trainees are not clerks. III. Some staff are not trainees. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); an "all plus no" chain is a standard syllogism pattern (prep-site topic, unverified).
**What the interviewer is checking:** Chaining "all" into "no", then using the non-empty convention for "some not".
**Say this in the interview:** "Clerks are inside staff and staff do not touch trainees, so clerks do not touch trainees: I. By the convention trainees exist, and none of them is a clerk, so II. Staff exist and none is a trainee, so III. All three follow."
**Answer:** **I, II and III all follow.**
**Step-by-step reasoning:**
1. All clerks are staff; no staff are trainees, so no clerk is a trainee: I.
2. Trainees exist (convention) and none of them is staff, so none of them is a clerk, so some trainees are not clerks: II.
3. Staff exist and none of them is a trainee, so some staff are not trainees: III.
**Fast method (30 seconds):** Draw clerks inside staff, and trainees as a separate circle. Everything in the conclusions can be read from this picture.
**Check:** Verified by script: all conclusions true in all 4 models.
**Explain simply:**
- "No" statements make "some not" conclusions work once the groups are non-empty.
- The convention that every group has a member is what makes II and III follow.
**Likely follow-ups:** 1) *What if trainees could be an empty group?* Then II would not be guaranteed. 2) *Does "Some staff are clerks" follow?* Yes (clerks exist and are all staff).
**Common mistakes / traps:** Accepting I but rejecting II and III as "not stated". Under the convention they are valid.

### Q13 ⭐⭐⭐ 🟡 Statements: Some stores are warehouses. All warehouses are depots. Conclusions: I. All stores are depots. II. Some stores are not depots. Which is correct: (a) only I follows, (b) only II follows, (c) either I or II follows, (d) neither follows and there is no either-or? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); the either-or case is a standard syllogism item (prep-site topic, unverified).
**What the interviewer is checking:** Recognising a complementary pair of conclusions where neither is certain alone.
**Say this in the interview:** "The statements tell us nothing about the stores that are not warehouses. 'All stores are depots' and 'some stores are not depots' are direct opposites, so exactly one of them is true in every picture. That is the either-or case."
**Answer:** **(c) either I or II follows.**
**Step-by-step reasoning:**
1. The warehouse stores are depots, but other stores may or may not be depots; the statements do not say.
2. If all other stores are depots, I is true (and II false). If some other store is not a depot, II is true (and I false).
3. Neither is true in every picture, so neither follows alone.
4. I and II are contradictory: one of them is always true and they are never both true. So "either I or II" follows.
**Fast method (30 seconds):** Check whether the two conclusions share the same subject and predicate and are opposites (all versus some-not). If neither follows alone, the answer is either-or.
**Check:** Verified by script over all 32 models: I or II is true in every one, and never both together.
**Explain simply:**
- Either-or applies when two conclusions are complete opposites and neither can be proven alone.
- Together they cover all cases, so one must hold.
**Likely follow-ups:** 1) *What if one conclusion already followed?* Then pick that conclusion; either-or is not used. 2) *Does "Some stores are depots" follow?* Yes.
**Common mistakes / traps:** Picking (d) because you cannot prove either alone; this misses the either-or rule.

### Q14 ⭐⭐⭐ 🟡 Statements: Some pens are files. No files are boxes. Conclusions: I. Some pens are not boxes. II. No pens are boxes. III. Some pens are boxes. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); a "some plus no" pattern is standard (prep-site topic, unverified).
**What the interviewer is checking:** Getting the guaranteed "some not" and rejecting the tempting "no" conclusion.
**Say this in the interview:** "The pens that are files cannot be boxes, so some pens are not boxes: I follows. II and III are opposites and either could be true, so neither follows. Since I follows, I do not need an either-or."
**Answer:** **Only I follows.**
**Step-by-step reasoning:**
1. A pen that is a file exists, and no file is a box. So that pen is not a box: I follows.
2. Other pens, not files, might or might not be boxes. So "no pens are boxes" (II) and "some pens are boxes" (III) are both possible.
3. II and III are opposite statements, so one of them is always true, but neither is certain alone.
4. The either-or rule is used only when no conclusion follows on its own; here I already does.
**Fast method (30 seconds):** Use "some pens are files" to build a guaranteed "some not". For the rest, ask whether another group of pens could break it.
**Check:** Verified by script over all 24 models: I always true; II and III never both true, and one of them always true.
**Explain simply:**
- Only the pens that are files are controlled by the statements.
- Other pens are free to be boxes or not.
**Likely follow-ups:** 1) *Would "Some files are pens" follow?* Yes (reversing "some"). 2) *Would "Some boxes are not pens" follow?* No, possible only.
**Common mistakes / traps:** Choosing II because "no files are boxes" feels like it spreads to pens.

### Q15 ⭐⭐⭐ 🟡 Statements: Some bags are not cups. All cups are plates. Conclusions: I. Some bags are not plates. II. Some bags are plates. III. Some plates are bags. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); "some not plus all" items are a known trap (prep-site topic, unverified).
**What the interviewer is checking:** Not turning "some bags are not cups" into anything about plates.
**Say this in the interview:** "The bags that are not cups may or may not be plates, since the 'all' statement only covers cups. So I, II and III each fail in some picture. No single conclusion follows."
**Answer:** **None of I, II, III follows by itself.** (Remark: I and II are the opposite-type pair for bags and plates; at least one of "some bags are not plates" or "some bags are plates" is always true, but both can be true together, so this is not a strict either-or.)
**Step-by-step reasoning:**
1. Cups are inside plates. The bags that are not cups sit outside the cup circle.
2. They may be inside the plate circle (then I could be false) or outside it (then II could be false).
3. III needs a bag that is a plate; no bag is forced to be a plate, so it can fail.
4. So none is certain.
**Fast method (30 seconds):** A "some not" statement cannot be pushed through an "all" statement. Test each conclusion with one drawing that breaks it.
**Check:** Verified by script over all 36 models: I, II and III each false in some model. In every model at least one of I and II holds, but both are true in some.
**Explain simply:**
- "All cups are plates" only controls cups.
- A conclusion about plates and bags needs a link through cups, and the statements do not give one.
**Likely follow-ups:** 1) *Does "Some bags are not cups" reverse?* No, a "some not" statement cannot be reversed. 2) *Would "Some plates are not bags" follow?* No (check by drawing).
**Common mistakes / traps:** Choosing I because "not cups" feels like "not plates". Or marking II/III as true because plates are a big group.

### Q16 ⭐⭐⭐ 🟡 How do you test whether a conclusion follows from two "some" statements, for example "Some analysts are auditors" and "Some auditors are lawyers"?
**Asked at:** commonly asked (no company-specific report found); statement-and-conclusion syllogisms are reported on prep sites for TCS NQT, Infosys, Wipro and Mu Sigma (prep-site claims, unverified).
**What the interviewer is checking:** Whether you know that two "some" statements never chain, and that you test by trying to break the conclusion rather than by feel.
**Say this in the interview:** "Two 'some' statements give no link between the outer groups. Analysts and lawyers can overlap or not, so 'some analysts are lawyers' is only possible, not certain. Only the direct restatements follow."
**Answer:** **Draw the smallest picture that makes the conclusion false. If one exists, the conclusion does not follow. For these two statements, nothing about analysts and lawyers follows; only "Some auditors are analysts" and "Some lawyers are auditors" (the reversed statements) follow.**
**Step-by-step reasoning:**
1. Convention: "some" means at least one, and every named group has at least one member.
2. Draw Auditors as a circle. "Some analysts are auditors" puts at least one analyst inside it; "Some auditors are lawyers" puts at least one lawyer inside it.
3. Model 1: the analyst and the lawyer are two different people, both auditors. Then no analyst is a lawyer. So "Some analysts are lawyers" can fail.
4. Model 2: one person is analyst, auditor and lawyer. Then "Some analysts are lawyers" is true. So "No analysts are lawyers" can fail too.
5. A conclusion follows only if it is true in every model. Both "Some A are C" and "No A are C" fail somewhere, so neither follows. The same holds for "Some A are not C" and "All A are C".
**Fast method (30 seconds):** Rule of thumb: a middle term (here "auditors") must be *covered* by at least one "all" or "no" statement to carry a link. With two "some" statements it is not covered, so say "no conclusion about the outer groups" at once.
**Check:** verified by script: I enumerated every way of filling the 8 Venn regions of three groups (160 models satisfy the statements and non-emptiness); "Some A are C" is true in some and false in others; "Some A are B" is true in all 160.
**Explain simply:**
- A conclusion "follows" only if it holds in every possible picture, not just the one you drew.
- A "middle term" is the group that appears in both statements (auditors); it can only pass information on if it is fully pinned down.
- Two "some" statements are like two partial overlaps: the overlaps may or may not touch.
**Likely follow-ups:** 1) *What if the second statement were "All auditors are lawyers"?* Then the analyst auditor is also a lawyer, so "Some analysts are lawyers" follows (script-verified). 2) *Does "Some lawyers are analysts" follow in the original?* No, same reasoning with the letters swapped.
**Common mistakes / traps:** Reading "some A are B, some B are C" as "so some A are C" (it feels like a chain, but it is not). Also, rejecting the conclusion as "false": it is only *not certain* (possible).

### Q17 ⭐⭐⭐ 🟡 When does the "either-or" case apply in a syllogism question, and how do you check it quickly?
**Asked at:** commonly asked (no company-specific report found); the either-or option appears in statement-conclusion items on Indian prep sites (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can spot a complementary pair of conclusions and avoid wrongly saying "neither follows".
**Say this in the interview:** "Either-or applies when neither conclusion follows alone, both are about the same two groups, and between them they cover every case, so one of them must be true. Typical pairs are 'Some' with 'No', and 'All' with 'Some not'."
**Answer:** **The either-or case applies when (1) neither conclusion follows on its own, (2) both have the same subject and the same predicate, and (3) they are contradictories (one is the exact negation of the other), so exactly one is true in every possible picture.**
**Step-by-step reasoning:**
1. First test each conclusion alone. If one definitely follows, you are done; no either-or.
2. If neither follows, check the pair has the same two groups in the same order.
3. Check the pair is a contradictory pair: "Some A are B" with "No A is B", or "All A are B" with "Some A are not B".
4. If yes, answer "either I or II follows". If the pair is "All" with "No" (both can be false) or the groups differ, answer "neither".
**Fast method (30 seconds):** Ask: "Can both be false?" For a contradictory pair it never happens. Example: Statements "Some A are B; some B are C". I. Some A are C. II. No A is C. Neither is certain, and one of them must be true, so it is either-or. Script check: in all 160 models one of the two holds.
**Check:** verified by script: "Some A are C or No A are C" holds in all 160 models; "All A are C or No A are C" fails in some (so no either-or there).
**Explain simply:**
- Contradictory means "exact opposite": if one is true the other is false, and vice versa.
- Many exams also treat "Some A are B" with "Some A are not B" as either-or because with A non-empty at least one of them is always true (script-verified); they can both be true, so say which reading your test uses.
**Likely follow-ups:** 1) *Does either-or apply to "All A are B" and "No A are B"?* No: both are false when A partly overlaps B. 2) *If conclusion I already follows, is it either-or?* No, then I alone is the answer.
**Common mistakes / traps:** Picking either-or when the two conclusions involve different groups; choosing "neither" when the pair is complementary; forgetting to check each one alone first.

### Q18 ⭐⭐⭐ 🟡 Rule: "If a record has a missing customer ID, it is flagged. If a record is flagged, it is sent to manual review. A record sent to manual review is not loaded to the warehouse." Record X was loaded to the warehouse. Which of these must be true: I. X has no missing customer ID. II. X was flagged. III. X was sent to manual review?
**Asked at:** commonly asked (no company-specific report found); chained rules like this mirror data-validation logic and prep-site "conditional chain" items (unverified).
**What the interviewer is checking:** Can you run a chain backwards using the contrapositive, and avoid concluding things the rules do not force.
**Say this in the interview:** "Forward the chain is missing ID, flagged, manual review, not loaded. X was loaded, so working backwards X was not reviewed, so not flagged, so no missing ID. Only statement I must be true."
**Answer:** **Only I: X has no missing customer ID. (II and III are false.)**
**Step-by-step reasoning:**
1. Chain: missing ID then flagged; flagged then review; review then not loaded.
2. X was loaded. "Review then not loaded" has the contrapositive "loaded then not reviewed". So III (sent to review) is false.
3. "Flagged then review" has the contrapositive "not reviewed then not flagged". So X was not flagged: II is false.
4. "Missing ID then flagged" has the contrapositive "not flagged then no missing ID". So I is true.
**Fast method (30 seconds):** Start from the fact and walk the arrows backwards, flipping each into "not B then not A". Everything upstream of the known fact is denied.
**Check:** verified by script: of the 16 true/false combinations of the four facts, exactly 1 fits the rules with X loaded; in it, missing ID is false, flagged is false, review is false.
**Explain simply:**
- Contrapositive: "If P then Q" is equivalent to "If not Q then not P". It is the only safe way to reverse a rule.
- Denying the end of the chain (loaded means not reviewed) lets you deny every earlier link.
**Likely follow-ups:** 1) *Record Y was flagged: what follows?* Y was sent to review and not loaded; whether it had a missing ID is unknown (a record could be flagged for another reason). 2) *Record Z has no missing ID: can it be loaded?* Not decided by these rules.
**Common mistakes / traps:** Saying "loaded, so it was never flagged" is right, but also claiming "no missing ID means loaded" is wrong; and thinking II or III is "possibly true" (they are definitely false here).

### Q19 ⭐⭐⭐ 🟡 Statement: "A claim is paid only if the policy is active." Which of these is equivalent? (a) If the policy is active, the claim is paid. (b) If the claim is paid, the policy is active. (c) If the policy is not active, the claim is paid. (d) The claim is paid if and only if the policy is active.
**Asked at:** commonly asked (no company-specific report found); "only if" wording is a standard trap in prep-site deductive sections (unverified).
**What the interviewer is checking:** Whether you put the arrow the right way round for "only if".
**Say this in the interview:** "'A only if B' means A needs B. A claim being paid requires an active policy, so: if paid, then active. That is option (b)."
**Answer:** **(b) If the claim is paid, the policy is active.**
**Step-by-step reasoning:**
1. "Only if" introduces the necessary condition: "A claim is paid only if the policy is active" means active is needed for payment.
2. Write it as: paid then active.
3. (a) is the converse (active then paid): an active policy does not guarantee payment. Wrong.
4. (c) says an inactive policy leads to payment, the opposite of the rule. Wrong.
5. (d) "if and only if" adds (a) as well, which is stronger than given. Wrong.
**Fast method (30 seconds):** Ask "what is the thing that must hold?" The word after "only if" is the requirement and goes on the right side of the arrow.
**Check:** verified by script: over all four true/false cases, (b) matches "paid then active" exactly; (a), (c), (d) each disagree in at least one case.
**Explain simply:**
- "A if B" means B then A. "A only if B" means A then B. They are reverses of each other.
- Necessary condition: you must have it, but having it alone is not enough.
**Likely follow-ups:** 1) *Policy active, claim not paid: does this break the rule?* No. 2) *Policy inactive: what follows?* The claim is not paid (contrapositive of (b)).
**Common mistakes / traps:** Reading "only if" as "if" and picking (a); picking (d) because "only if" sounds like "exactly when".

### Q20 ⭐⭐⭐ 🟡 Rule: "Unless the manager approves, the refund is not processed." The refund was processed. Which of these must be true: I. The manager approved. II. Every request the manager approves is processed. III. The customer was eligible for the refund?
**Asked at:** commonly asked (no company-specific report found); "unless" wording is a standard conditional trap on prep sites (unverified).
**What the interviewer is checking:** Translating "unless" correctly and not over-reading the rule.
**Say this in the interview:** "'Unless the manager approves, no refund' means: if not approved, then not processed. Contrapositive: if processed, then approved. So I is certain. II is the reverse and III is never mentioned."
**Answer:** **Only I must be true.**
**Step-by-step reasoning:**
1. Rewrite: not approved then not processed.
2. Contrapositive: processed then approved.
3. The refund was processed, so the manager approved: I is true.
4. II says approval always leads to processing. The rule only says approval is needed, not enough. So II does not follow (a manager can approve and the refund can still fail for another reason).
5. III (customer eligible) is not mentioned in the rule, so it cannot be deduced.
**Fast method (30 seconds):** "Unless X, not Y" is the same as "Y only if X": if Y happened, X happened.
**Check:** verified by script: "not approved then not processed" is equivalent to "processed then approved" in all 4 cases; among cases with processed = true, approved is always true, while approved-with-not-processed also exists (so II fails).
**Explain simply:**
- "Unless" introduces the one exception that makes the thing allowed. It states a necessary condition, not a guarantee.
- Do not add facts the rule does not contain (eligibility).
**Likely follow-ups:** 1) *Manager did not approve: was it processed?* No. 2) *Manager approved: was it processed?* Unknown.
**Common mistakes / traps:** Treating "unless" as "if and only if" and ticking II; assuming a processed refund must have been eligible.

### Q21 ⭐⭐⭐ 🟡 Rule: "A bonus is paid only if the employee has rating 4 or 5 and zero warnings." How many employees in the table below violate the rule?

| Emp | Rating | Warnings | Tenure (yrs) | Bonus paid |
|---|---|---|---|---|
| E1 | 5 | 0 | 4 | Yes |
| E2 | 4 | 1 | 3 | Yes |
| E3 | 3 | 0 | 5 | No |
| E4 | 4 | 0 | 1 | Yes |
| E5 | 2 | 0 | 6 | Yes |
| E6 | 5 | 0 | 3 | No |
| E7 | 4 | 0 | 2 | Yes |
| E8 | 3 | 2 | 1 | No |
**Asked at:** commonly asked (no company-specific report found); rule-violation checks on tables are a typical analyst-style reasoning item (unverified).
**What the interviewer is checking:** Whether you test the rule only where it can be broken (bonus paid), not where it is silent.
**Say this in the interview:** "'Only if' means a paid bonus needs rating 4 or 5 and no warnings. So I look only at rows with Bonus paid = Yes and check both conditions. E2 has a warning and E5 has rating 2. Two violations."
**Answer:** **2 employees violate the rule: E2 and E5.**
**Step-by-step reasoning:**
1. Rule: bonus paid then (rating 4 or 5 and zero warnings).
2. Filter to Bonus paid = Yes: E1, E2, E4, E5, E7.
3. E1: 5, 0 warnings, fine. E2: rating 4 but 1 warning, violation. E4: 4, 0, fine. E5: rating 2, violation. E7: 4, 0, fine.
4. Rows with Bonus paid = No (E3, E6, E8) cannot violate an "only if" rule: it never promises a bonus. E6 looks like it deserved one, but that is not a violation.
**Fast method (30 seconds):** Cover the "No" rows. Check the paid rows against the condition.
**Check:** verified by script: filtering paid rows and testing the condition gives exactly E2 and E5.
**Explain simply:**
- A rule "X only if Y" is broken only by a case with X true and Y false.
- A violation is a case that contradicts the rule, not a case that "feels unfair".
**Likely follow-ups:** 1) *If the rule were "if and only if", how many violations?* 3 (E2, E5 and E6). Script-verified. 2) *Which rows would break "If rating 5 then bonus"?* E6 (rating 5, no bonus).
**Common mistakes / traps:** Counting E6 (good rating, no bonus) as a violation; forgetting that both conditions (rating and warnings) must hold; checking tenure, which is irrelevant here.

### Q22 ⭐⭐⭐ 🟡 Rule: "If tenure is more than 2 years and rating is at least 4, a bonus is paid." Which employee(s) in the table below violate it?

| Emp | Rating | Warnings | Tenure (yrs) | Bonus paid |
|---|---|---|---|---|
| E1 | 5 | 0 | 4 | Yes |
| E2 | 4 | 1 | 3 | Yes |
| E3 | 3 | 0 | 5 | No |
| E4 | 4 | 0 | 1 | Yes |
| E5 | 2 | 0 | 6 | Yes |
| E6 | 5 | 0 | 3 | No |
| E7 | 4 | 0 | 2 | Yes |
| E8 | 3 | 2 | 1 | No |
**Asked at:** commonly asked (no company-specific report found); same family as the "only if" table item above (unverified).
**What the interviewer is checking:** That you test the rule exactly where its "if" part is satisfied and the "then" part fails.
**Say this in the interview:** "A violation needs tenure over 2, rating at least 4, and no bonus. Only E6 fits: 3 years, rating 5, bonus not paid."
**Answer:** **E6 is the only violation.**
**Step-by-step reasoning:**
1. Rule: (tenure > 2 and rating >= 4) then bonus paid.
2. Find rows where both conditions hold: E1 (4 yrs, 5), E2 (3 yrs, 4), E6 (3 yrs, 5). E7 has tenure exactly 2, which is not "more than 2"; E4 has tenure 1; E3 and E5 and E8 have rating below 4.
3. Among those three, E1 and E2 were paid (fine), E6 was not paid: violation.
4. Rows where the condition is not met (such as E5, rating 2, paid) do not break this rule; the rule says nothing about them.
**Fast method (30 seconds):** Look for "condition met, outcome missing". Do not hunt for odd-looking paid rows.
**Check:** verified by script: rows with condition true and bonus No are exactly [E6].
**Explain simply:**
- An "if A then B" rule fails only when A is true and B is false.
- "More than 2" excludes 2; "at least 4" includes 4. Read boundaries carefully.
**Likely follow-ups:** 1) *If the rule said "tenure of 2 years or more", who violates it?* Still only E6, because E7 (tenure 2) now qualifies and was paid (script-verified). 2) *Does E5 (rating 2, bonus paid) violate it?* No, the rule does not forbid bonuses for others.
**Common mistakes / traps:** Flagging E5 or E4 (paid without meeting the condition); treating "more than 2" as including 2 and flagging E7 (E7 was paid, so no harm here, but the habit costs marks elsewhere).

### Q23 ⭐⭐⭐ 🟡 Statement: "Only certified analysts can sign off a report." Priya signed off a report. Rahul is a certified analyst. Sana is an analyst but not certified. Which of these must be true: I. Priya is a certified analyst. II. Rahul signed off a report. III. Sana did not sign off a report?
**Asked at:** commonly asked (no company-specific report found); "only" statements are a standard item type on prep sites (unverified).
**What the interviewer is checking:** Direction of an "only" statement and what it does and does not allow.
**Say this in the interview:** "'Only certified analysts can sign off' means signing off requires certification. Priya signed off, so she is certified. Sana is not certified, so she cannot sign off. Rahul being certified does not mean he signed off. So I and III."
**Answer:** **I and III must be true; II does not follow.**
**Step-by-step reasoning:**
1. Translate: signed off then certified analyst.
2. I: Priya signed off, so she is certified. True.
3. II: Rahul is certified, but certification is only needed, not enough to sign off; whether he signed is unknown. Not forced.
4. III: contrapositive: not certified then did not sign off. Sana is not certified, so she did not sign off. True.
**Fast method (30 seconds):** "Only X can do Y": Y-doers are inside X. If you are inside X it does not mean you did Y; if you are outside X you did not.
**Check:** verified by script: with signed-then-certified, every case where Priya signed has certified true; every case where the person is not certified has signed false; Rahul's signing can be either.
**Explain simply:**
- "Only A are B" means every B is an A (B is a subset of A), same direction as "if B then A".
- Being allowed to do something is not the same as having done it.
**Likely follow-ups:** 1) *Sana is certified: did she sign off?* Unknown. 2) *Nobody signed off: is the statement false?* No, it is still true (nothing broke it).
**Common mistakes / traps:** Reversing it into "all certified analysts sign off" and ticking II; forgetting III follows by contrapositive.

### Q24 ⭐⭐ 🟢 Statements: All rows are columns. All tables are columns. Conclusions: I. All rows are tables. II. Some rows are tables. III. Some columns are rows. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); the "two All statements share the predicate" pattern is a standard syllogism trap on prep sites (unverified).
**What the interviewer is checking:** Spotting that two groups both inside a third group have no forced link to each other.
**Say this in the interview:** "Rows and tables both sit inside columns, but they may or may not overlap. So I and II are only possible. III follows because rows are a non-empty part of columns."
**Answer:** **Only III follows.**
**Step-by-step reasoning:**
1. Convention: "some" means at least one; all named groups are non-empty.
2. Draw a big circle for Columns. Draw Rows inside it and Tables inside it. Nothing says how Rows and Tables relate.
3. I (all rows are tables): can fail when Rows and Tables are separate circles. Does not follow.
4. II (some rows are tables): can fail in the same picture. Does not follow.
5. III (some columns are rows): rows are non-empty and all are columns, so at least one column is a row. Follows.
**Fast method (30 seconds):** "All A are B" and "All C are B" (middle term is the *predicate* of both): no link between A and C. Only the reversed statements ("Some B are A", "Some B are C") are safe.
**Check:** verified by script over Venn-region models (20 models fit): I and II are true in some, false in others; III is true in all 20.
**Explain simply:**
- Undistributed middle: the shared group (columns) is not fully covered by either statement, so it cannot connect the others.
- "Some columns are rows" is the safe reverse of "All rows are columns", valid because rows are assumed non-empty.
**Likely follow-ups:** 1) *Does "Some tables are columns" follow?* Yes, same reason as III. 2) *Does "No rows are tables" follow?* No, equally uncertain (possible).
**Common mistakes / traps:** Thinking "both are columns, so rows are tables"; ticking II because it "looks mild".

### Q25 ⭐⭐ 🟢 Does "All A are B" logically imply "Some A are B"? Explain why the answer depends on whether the group A may be empty, and what convention reasoning tests usually assume.
**Asked at:** commonly asked (no company-specific report found); the empty-group convention matters in reasoning-test instructions (unverified).
**What the interviewer is checking:** Whether you know the hidden assumption behind "All implies Some".
**Say this in the interview:** "In modern logic 'All A are B' is true even if A is empty, so it does not imply 'Some A are B'. Reasoning tests assume every named group has members, so under that convention it does. Check the test's instructions."
**Answer:** **Not necessarily. It implies "Some A are B" only if A is assumed non-empty. Reasoning tests normally state or assume that, so there the answer is yes.**
**Step-by-step reasoning:**
1. "All A are B" says: no A lies outside B.
2. If A has no members, that is true automatically (nothing can lie outside B). Yet "Some A are B" needs at least one A, so it is false.
3. So with empty groups allowed, "All" does not imply "Some". With non-empty groups assumed, it does.
4. Real-world example: "All employees with more than 10 warnings are on a watch list" can be true in a firm where nobody has more than 10 warnings; it does not mean such an employee exists.
**Explain simply:**
- Vacuous truth: a rule about "all X" is automatically true when there is no X.
- Existential import: the assumption that named groups have at least one member. Most aptitude tests use it; formal logic software often does not.
**Check:** verified by script: over all models of two groups with empty groups allowed (8 models fit "All A are B"), "Some A are B" is false in some; over models with both groups non-empty (4 models), it is true in all.
**Likely follow-ups:** 1) *Does "No A is B" imply "Some A are not B"?* Same story: yes if A is non-empty. 2) *What should you do if the test does not say?* Ask or follow the stated convention; in the usual aptitude format assume non-empty.
**Common mistakes / traps:** Saying "yes always" without the convention, or "never" without noting that tests assume non-empty groups.

### Q26 ⭐⭐ 🟢 What is the correct negation of each of the four statement forms: "All A are B", "No A is B", "Some A are B" and "Some A are not B"?
**Asked at:** commonly asked (no company-specific report found); negation of quantified statements is core to deductive prep and to SQL filter logic (unverified).
**What the interviewer is checking:** Whether you separate a true negation from a mere opposite.
**Say this in the interview:** "The negation flips truth in every case. All A are B negates to Some A are not B; No A is B negates to Some A are B; and the other two are the reverse."
**Answer:**
| Statement | Negation |
|---|---|
| All A are B | **Some A are not B** |
| No A is B | **Some A are B** |
| Some A are B | **No A is B** |
| Some A are not B | **All A are B** |
**Step-by-step reasoning:**
1. A negation must be true exactly when the original is false.
2. "All A are B" fails the moment one A is outside B, which is "Some A are not B".
3. "No A is B" fails the moment one A is inside B, which is "Some A are B".
4. The other two are the same pairs read backwards.
**Check:** verified by script: over all 8 Venn models of two groups (empty groups allowed), each pair always has opposite truth values.
**Explain simply:**
- "All" and "No" are opposites but not negations: both are false when A partly overlaps B (for example some analysts are managers, some are not). The negation of "All" is "Some not", not "No".
- Negating "all" gives "some not": one counter-example kills a universal claim.
- Data link: a filter "NOT (all rows pass)" means at least one row fails.
**Likely follow-ups:** 1) *Negate "Some invoices are paid".* No invoice is paid. 2) *Negate "All invoices are valid".* Some invoice is not valid.
**Common mistakes / traps:** Choosing "No A is B" as the negation of "All A are B" (the classic wrong option in Q9 style questions).

### Q27 ⭐⭐ 🟢 How do you translate "A if B", "A only if B", "A if and only if B" and "A unless B" into if-then form?
**Asked at:** commonly asked (no company-specific report found); translating if/only if/unless is a standard prep item (unverified).
**What the interviewer is checking:** Writing the arrow in the right direction for each wording.
**Say this in the interview:** "'A if B' is B then A. 'A only if B' is A then B. 'A if and only if B' is both directions. 'A unless B' is: if not B, then A."
**Answer:**
| Wording | If-then form |
|---|---|
| A if B | **If B then A** |
| A only if B | **If A then B** (same as: if not B then not A) |
| A if and only if B | **If A then B, and if B then A** |
| A unless B | **If not B then A** (same as: if not A then B) |
**Step-by-step reasoning:**
1. "If" points to the sufficient condition: the part after "if" goes on the left.
2. "Only if" points to the necessary condition: the part after "only if" goes on the right.
3. "If and only if" combines both, so A and B are always true together or false together.
4. "Unless B" means "if B does not happen": so not B then A.
**Worked example:** "The report is sent if it is approved": approved then sent. "The report is sent only if it is approved": sent then approved. "The report is sent unless it is blocked": not blocked then sent.
**Check:** verified by script: truth tables confirm "A only if B" equals "not B then not A", and "A unless B" equals "A or B", equal to both "not B then A" and "not A then B".
**Explain simply:**
- Sufficient: enough by itself. Necessary: required but maybe not enough.
- "Unless" is usually read as one-way (only the exception is guaranteed to allow it); some writers mean "if and only if", so look at context.
**Likely follow-ups:** 1) *"Refund is not processed unless manager approves"?* Processed then approved (Q20). 2) *Is "A if B" the same as "A only if B"?* No, they are converses.
**Common mistakes / traps:** Treating "only if" like "if"; treating "unless" as "if" without the "not".

### Q28 ⭐⭐ 🟢 Which of the four statement forms can be converted simply ("All", "No", "Some", "Some not"), and which cannot? Give one example where the reversed statement is wrong.
**Asked at:** commonly asked (no company-specific report found); conversion is core syllogism theory on prep sites (unverified).
**What the interviewer is checking:** Whether you know which reversals are safe.
**Say this in the interview:** "'No' and 'Some' reverse safely. 'All' and 'Some not' do not. All A are B does not give All B are A."
**Answer:**
| Form | Reverse safe? |
|---|---|
| All A are B | **No** (only "Some B are A" follows, if A is non-empty) |
| No A is B | **Yes** (No B is A) |
| Some A are B | **Yes** (Some B are A) |
| Some A are not B | **No** |
**Worked example of a wrong reversal:** Analysts = {Ann, Bob}, managers = {Ann}. "Some analysts are not managers" is true (Bob). Reversed, "Some managers are not analysts" is false (the only manager is an analyst). Likewise "All managers are analysts" is true but "All analysts are managers" is false.
**Check:** verified by script over Venn models with non-empty groups: reversing "No" and "Some" never fails; reversing "All" or "Some not" fails in some models; "All A are B" always gives "Some B are A".
**Explain simply:**
- "Some" and "No" are symmetric: overlap or no overlap between A and B is the same fact from either side.
- "All" and "Some not" are one-way: they describe A relative to B only.
**Likely follow-ups:** 1) *Reverse "All dogs are animals".* Some animals are dogs (safe), not "All animals are dogs". 2) *Reverse "No A is B".* No B is A.
**Common mistakes / traps:** Reversing "All A are B" into "All B are A"; assuming "Some not" is symmetric.

### Q29 ⭐⭐ 🟢 You get a set of 4 statements and 5 conclusions in a syllogism question and about 90 seconds. What is a time-efficient step-by-step method, and when should you skip?
**Asked at:** commonly asked (no company-specific report found); prep sites report about 2 syllogisms in a 20-question, 25-minute TCS NQT reasoning section (prep-site claim, unverified); timings below are our suggestion, not a research finding.
**What the interviewer is checking:** Structured, calm method under time pressure, and judgement about when to move on.
**Say this in the interview:** "I draw one combined diagram, then test each conclusion by asking whether I can make it false. About 15 to 18 seconds each. If the diagram needs more than three groups and I am stuck, I guess and move on."
**Answer:** **Our suggested 90-second routine: 20 seconds to build the diagram, about 14 seconds per conclusion, and a skip rule for tangled sets.**
**Step-by-step reasoning:**
1. Read all statements; note the convention (some = at least one; groups non-empty).
2. Combine statements with the quick rules (below) and draw the *most spread-out* picture, where nothing overlaps unless forced.
3. For each conclusion, ask "Is it true in every picture?" Try to break it by moving circles apart or together.
4. Tick conclusions that survive; mark the rest.
5. Check the either-or case for any untouched pair of conclusions about the same two groups (Q17).
6. Pick the option that matches the ticked set.
**Fast method (quick rules, each verified by script):**
- All A are B + All B are C gives All A are C.
- Some A are B + All B are C gives Some A are C.
- All A are B + No B is C gives No A is C.
- Some A are B + No B is C gives Some A are not C.
- No A is B + All B are C gives Some C are not A.
- Two "some", two "no", or "All A are B + All C are B" give no link.
**Worked example:** All A are B; Some B are C; All C are D; No D is E. Script-checked: "Some B are D", "No C is E", "Some B are not E" and "Some D are not E" follow; "Some A are C" and "All A are D" do not.
**When to skip (our suggestion):** More than three groups with several "some" statements, or you are past 30 seconds on one conclusion. Guess and return if time remains. If there is negative marking, weigh the guess first.
**Check:** the rules and the worked example were verified by script over Venn-region models; the timings are a rule of thumb.
**Explain simply:**
- Drawing the loosest picture forces you to see what is *not* guaranteed.
- A conclusion is certain only if no valid picture breaks it.
**Likely follow-ups:** 1) *Which conclusion do you test first?* The one that uses the fewest groups. 2) *What if two conclusions are complementary?* Check either-or.
**Common mistakes / traps:** Drawing one picture and accepting every conclusion true in it; spending 60 seconds on one conclusion; forgetting the either-or check.

### Q30 ⭐⭐ 🟢 What is the negation of "If a ticket is closed, the customer has confirmed"? (a) If a ticket is not closed, the customer has not confirmed. (b) A ticket is closed and the customer has not confirmed. (c) If the customer has confirmed, the ticket is closed. (d) A ticket is not closed and the customer has confirmed.
**Asked at:** commonly asked (no company-specific report found); negating an if-then is a standard trap on prep sites (unverified).
**What the interviewer is checking:** Knowing that the negation of a rule is a counter-example, not another rule.
**Say this in the interview:** "A rule 'if P then Q' is broken only when P is true and Q is false. So the negation is: the ticket is closed and the customer has not confirmed. That is (b)."
**Answer:** **(b) A ticket is closed and the customer has not confirmed.**
**Step-by-step reasoning:**
1. "If closed then confirmed" is false in exactly one situation: closed but not confirmed.
2. So its negation is "closed and not confirmed".
3. (a) is the inverse (if not closed, then not confirmed). It is not equivalent to the negation.
4. (c) is the converse (if confirmed then closed). Also not the negation.
5. (d) is "not closed and confirmed". That case does not break the rule.
**Fast method (30 seconds):** The negation of an if-then is "P and not Q": keep the first part, flip the second, join with "and".
**Check:** verified by script: over all four true/false combinations, only option (b) is true exactly when the original rule is false.
**Explain simply:**
- Negation: the statement that is true precisely when the original is false.
- Inverse and converse are different if-then rules, not negations.
**Likely follow-ups:** 1) *Negate "If an order ships, an invoice is sent".* An order ships and no invoice is sent. 2) *Is the inverse of the rule equivalent to its converse?* Yes (both are the same rule logically), but neither is equivalent to the original.
**Common mistakes / traps:** Choosing (a) the inverse because it "sounds opposite"; writing a new if-then as the negation.

### Q31 ⭐⭐ 🟢 "Our five top-selling reps all attend the 8 a.m. huddle, so the huddle makes people top sellers." Which fallacy is this? (a) affirming the consequent (b) false cause (confusing correlation with causation) (c) circular reasoning (d) false dilemma
**Asked at:** commonly asked (no company-specific report found); named fallacies appear in prep-site deductive-reasoning topic lists (unverified).
**What the interviewer is checking:** Whether you separate "two things go together" from "one causes the other", the core habit of a good analyst.
**Say this in the interview:** "Five top sellers attending is a correlation. It does not show the huddle caused their sales; keen people may simply be the ones who attend. That is false cause. Answer (b)."
**Answer:** **(b) false cause (correlation mistaken for causation).**
**Step-by-step reasoning:**
1. The evidence is only "top sellers attend the huddle". That is an association.
2. The conclusion is "the huddle makes people top sellers". That is a cause claim.
3. Other explanations fit the same evidence: motivated people choose to attend (reverse direction), or a third factor such as a good territory or manager drives both.
4. Jumping from association to cause is the false cause fallacy (also called "post hoc" or "correlation is not causation").
**Fast method (30 seconds):** Ask "is a cause claimed from a pattern alone?" If yes, think false cause. Then rule out the others by their definitions: no if-then form (a), the conclusion is not a restatement of the premise (c), no "only two choices" (d).
**Check:** Option (a) needs a rule "if X then Y" plus "Y, so X"; no rule is given. (c) needs the conclusion to repeat the premise; it does not. (d) needs a forced either-or; none appears. Hand-checked.
**Explain simply:**
- Correlation means two things move or appear together; causation means one produces the other.
- To show cause you need more: a comparison group, timing (cause first), and ruling out other explanations.
**Likely follow-ups:** 1) *What data would help?* Compare sales of similar reps who attend and who do not, before and after they start attending. 2) *Could the huddle still help?* Yes; the argument is not proved, not disproved.
**Common mistakes / traps:** Picking (a) because the sentence sounds like "top sellers, so huddle" (reversed logic). The tempting label is right only for if-then rules; here the error is about cause.

### Q32 ⭐⭐ 🟢 "If an employee is a data analyst, she knows Excel. Kavya knows Excel, so Kavya is a data analyst." What is the error, and is the conclusion valid?
**Asked at:** commonly asked (no company-specific report found); the converse trap is named in conditional-reasoning prep pages (unverified).
**What the interviewer is checking:** Whether you can spot a reversed if-then rule.
**Say this in the interview:** "The rule runs analyst to Excel, not Excel to analyst. Knowing Excel is the result, and many non-analysts know it. This is affirming the consequent, so the conclusion is not valid."
**Answer:** **The error is affirming the consequent (treating the converse as if it were the rule). The conclusion is NOT valid; it may be true, but it does not follow.**
**Step-by-step reasoning:**
1. Write the rule as "If A then E": A = is a data analyst, E = knows Excel.
2. The fact given is E (Kavya knows Excel).
3. The argument concludes A. That is going from the consequent (E) back to the antecedent (A), which the rule never allows.
4. Counter-example: Kavya is an HR executive who knows Excel. Rule holds, fact holds, conclusion fails. One such case is enough to make the argument invalid.
**Fast method (30 seconds):** Valid forms point forward from A ("A, so E") or are the contrapositive ("not E, so not A"). Any "E, so A" is the reverse and is wrong.
**Check:** In a small model with 3 people (analyst who knows Excel, HR person who knows Excel, person who knows neither), the rule is true and Kavya (HR) knows Excel but is not an analyst. Hand-checked.
**Explain simply:**
- Antecedent is the "if" part; consequent is the "then" part.
- Affirming the consequent means asserting the "then" part and concluding the "if" part.
- "Invalid" means the conclusion is not forced by the premises; it does not mean the conclusion is false.
**Likely follow-ups:** 1) *What can we conclude if Kavya does not know Excel?* She is not a data analyst (contrapositive, valid). 2) *What if the rule said "if and only if"?* Then the reverse would hold too.
**Common mistakes / traps:** Saying "the conclusion is false". It is unproven, not disproved.

### Q33 ⭐⭐ 🟢 "Do not trust the churn analysis; its author was reprimanded last year." Which fallacy is this? (a) ad hominem (b) straw man (c) circular reasoning (d) hasty generalisation
**Asked at:** commonly asked (no company-specific report found); named fallacies appear in prep-site lists (unverified).
**What the interviewer is checking:** Whether you judge the analysis on its evidence rather than on the person.
**Say this in the interview:** "It attacks the author, not the analysis. Whether the numbers are right does not depend on a past reprimand. That is ad hominem, option (a)."
**Answer:** **(a) ad hominem (attacking the person instead of the argument).**
**Step-by-step reasoning:**
1. The claim being judged is "the churn analysis is reliable".
2. The reason offered is about the author's past conduct, not about data, method or results.
3. Dismissing a claim because of who made it is ad hominem (Latin for "to the person").
4. Other options: a straw man misrepresents someone's argument (none is described); circular reasoning repeats the claim as its own proof; hasty generalisation draws a wide rule from too few cases.
**Fast method (30 seconds):** Ask "does the reason talk about the person or about the evidence?" Person means ad hominem.
**Check:** Replace the author with a different person and keep the same numbers; the analysis is equally right or wrong. So the reprimand is irrelevant to its quality. Hand-checked.
**Explain simply:**
- A fallacy is a faulty reasoning pattern that sounds convincing but does not support the conclusion.
- Past conduct can justify extra checking, but it is not proof the work is wrong.
**Likely follow-ups:** 1) *Is it ever fair to doubt a source?* Yes, to check more carefully (for example a conflict of interest), but you still test the evidence. 2) *Is "ignore him, he is junior" the same?* Yes, ad hominem.
**Common mistakes / traps:** Choosing (d) because one reprimand is "one case"; the sentence does not generalise to a rule.

### Q34 ⭐⭐ 🟢 "Either we hire ten more analysts or the project will fail." Which fallacy is this (assuming other options exist)? (a) false dilemma (b) ad hominem (c) undistributed middle (d) equivocation
**Asked at:** commonly asked (no company-specific report found); named fallacies appear in prep-site lists (unverified).
**What the interviewer is checking:** Whether you notice when only two choices are presented but more exist.
**Say this in the interview:** "It offers two options only. Other routes exist: hire fewer, automate, cut scope, extend the deadline. That is a false dilemma, (a)."
**Answer:** **(a) false dilemma (false dichotomy, "either-or" fallacy).**
**Step-by-step reasoning:**
1. The statement says exactly two outcomes: hire ten, or fail.
2. The question tells us other options exist (for example, hire three, automate reporting, reduce scope).
3. Presenting two options as if they were the only ones is a false dilemma.
4. Other options do not fit: no person is attacked (b); no syllogism with a shared middle term (c); no word changes meaning mid-argument (d).
**Fast method (30 seconds):** Spot "either...or" and ask "are there really only two?" If a third option exists, it is a false dilemma.
**Check:** List one more option, "hire four and automate"; if the project can succeed under it, the either-or is broken. Hand-checked.
**Explain simply:**
- A dilemma is a choice between two options; it is "false" when more options exist.
- Either-or is only valid when the two options truly cover every possibility.
**Likely follow-ups:** 1) *When is "either-or" fine?* When it is exhaustive, such as "the customer is either active or churned" under a clear definition. 2) *How would you reply in a meeting?* "What are the other ways to get this done?"
**Common mistakes / traps:** Treating every "either...or" sentence as a fallacy; it is one only when the options are not exhaustive.

### Q35 ⭐⭐ 🟢 "The vendor is reliable because it says it is reliable." Which fallacy is this? (a) circular reasoning (b) false cause (c) appeal to ignorance (d) slippery slope
**Asked at:** commonly asked (no company-specific report found); named fallacies appear in prep-site lists (unverified).
**What the interviewer is checking:** Whether you can see that a reason merely repeats the claim.
**Say this in the interview:** "The reason and the conclusion are the same claim. The vendor's own word is used to prove the vendor is trustworthy. That is circular reasoning, (a)."
**Answer:** **(a) circular reasoning (begging the question).**
**Step-by-step reasoning:**
1. Conclusion: the vendor is reliable.
2. Reason: the vendor says it is reliable.
3. The reason only has weight if we already trust the vendor, which is exactly what we are trying to decide. The argument assumes its own conclusion.
4. Independent evidence (delivery records, references, audits) would break the circle.
**Fast method (30 seconds):** Ask "would I accept the reason only if I already accepted the conclusion?" If yes, it is circular.
**Check:** If the vendor said "we are unreliable", the same logic would "prove" the opposite; a reason that can prove anything proves nothing. Hand-checked.
**Explain simply:**
- Circular reasoning means the premise and conclusion rest on each other.
- Evidence must come from outside the claim being tested.
**Likely follow-ups:** 1) *What counts as independent evidence?* On-time delivery rate from past orders, customer references. 2) *Is a vendor's self-report useless?* It is a claim to verify, not proof.
**Common mistakes / traps:** Choosing (c) appeal to ignorance ("no one proved it unreliable"); that is not what the sentence says.

### Q36 ⭐⭐ 🟡 Statements: All leads are seniors. Some agents are not seniors. Conclusions: I. Some agents are not leads. II. No agents are leads. III. Some seniors are not agents. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); syllogisms appear in prep-site lists for TCS, Infosys, Wipro and Mu Sigma (unverified).
**What the interviewer is checking:** Whether you can derive only what is forced, no more.
**Say this in the interview:** "Some agents are outside seniors, and every lead is inside seniors, so those agents are outside leads. Only conclusion I follows."
**Answer:** **Only I follows.**
**Step-by-step reasoning:**
1. Draw a big circle for seniors; draw leads fully inside it.
2. Some agents are not seniors: those agents sit outside the senior circle.
3. Leads are all inside seniors, so those outside agents cannot be leads. So some agents are not leads: I follows.
4. II says no agent is a lead. The statements do not exclude other agents who are also seniors and leads. Counter-model: one agent who is a lead plus one agent who is not a senior; both statements hold, II fails.
5. III says some seniors are not agents. A model where every senior is also an agent satisfies both statements, so III is not forced.
**Fast method (30 seconds):** "All A are B" plus "some C are not B" gives "some C are not A" (what is outside the bigger group is outside the smaller group). Then test each remaining conclusion with one counter-model.
**Check:** Verified by script: all 24 possible region-occupancy models (every group non-empty) were enumerated. I true in 24 of 24; II true in 8 of 24; III true in 20 of 24.
**Explain simply:**
- "Follows" means true in every possible picture that fits the statements.
- One picture where the conclusion fails is enough to reject it.
**Likely follow-ups:** 1) *If the second statement were "Some agents are seniors", what follows?* Nothing about leads; leads could be none of those agents. 2) *What is "some not" in plain words?* At least one is outside.
**Common mistakes / traps:** Accepting III or II because they "sound" compatible; possible is not the same as forced.

### Q37 ⭐⭐ 🟡 Statements: All vendors are suppliers. Some suppliers are partners. No partners are buyers. Conclusions: I. Some vendors are partners. II. Some suppliers are not buyers. III. No vendors are buyers. IV. Some suppliers are vendors. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); multi-statement syllogisms appear in prep-site lists (unverified).
**What the interviewer is checking:** Handling a three-statement chain without over-reading "some".
**Say this in the interview:** "Some suppliers are partners, and partners are never buyers, so those suppliers are not buyers: II. Vendors are all suppliers and non-empty, so some suppliers are vendors: IV. I and III are not forced."
**Answer:** **II and IV follow.**
**Step-by-step reasoning:**
1. IV: all vendors are suppliers and vendors exist, so at least one supplier is a vendor. Follows.
2. II: take a supplier who is a partner (statement 2). Partners are not buyers (statement 3), so that supplier is not a buyer. Follows.
3. I: the partner-suppliers might all be non-vendor suppliers. Not forced.
4. III: a vendor could also be a buyer (nothing links vendors to partners), so "no vendors are buyers" is not forced.
**Fast method (30 seconds):** Look for a chain where a "some" statement meets an "all" or "no" statement on the same group; those give conclusions (here: partners link to buyers). Anything that needs two "some" groups to overlap is not forced.
**Check:** Verified by script over all 312 valid region-occupancy models (4 groups, every group non-empty). II and IV true in 312 of 312; I true in 224; III true in 120.
**Explain simply:**
- "All vendors are suppliers" lets us reverse to "some suppliers are vendors" only because every group is assumed non-empty.
- A "some" statement never grows into an "all".
**Likely follow-ups:** 1) *If vendors could be empty, does IV still follow?* No; it would then fail. 2) *Would "Some partners are vendors" follow?* No.
**Common mistakes / traps:** Accepting I because vendors and partners are both "inside suppliers"; sharing a big group does not make two small groups overlap.

### Q38 ⭐⭐ 🟡 Statements: No kit is a tool. No tool is a box. Conclusions: I. No kit is a box. II. Some kits are boxes. Which is correct: (a) only I follows, (b) only II follows, (c) either I or II follows, (d) neither follows and there is no either-or? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); "either-or" syllogism items are a standard prep-site pattern (unverified).
**What the interviewer is checking:** Whether you recognise two negative premises give nothing, and that two opposite conclusions together cover everything.
**Say this in the interview:** "Two negative premises force nothing about kits and boxes. But 'no kit is a box' and 'some kits are boxes' are exact opposites, so one of them must be true. Answer (c)."
**Answer:** **(c) either I or II follows.**
**Step-by-step reasoning:**
1. Draw three separate-looking circles: kits do not meet tools, tools do not meet boxes.
2. Kits and boxes may overlap or may not; both pictures obey the statements. So neither I nor II is forced.
3. I ("No kit is a box") and II ("Some kits are boxes") are contradictories: exactly one is true in any picture.
4. So at least one of them always holds, which is the "either-or" case.
**Fast method (30 seconds):** Both premises negative means no definite conclusion. If the two conclusions are "No A is B" and "Some A is B", pick "either-or" (when the statements leave the pair undecided).
**Check:** Verified by script over 10 valid models: I true in 2, II true in 8, and I or II true in all 10. Neither alone is always true.
**Explain simply:**
- "Either-or" is correct only when the two conclusions are contradictories (one must be true) and neither is forced alone.
- A contradictory pair covers all cases: "none" versus "at least one".
**Likely follow-ups:** 1) *Would it still be either-or if the conclusions were "No kit is a box" and "All kits are boxes"?* No; both could be false (some kits are boxes and some are not). 2) *What if the first statement were "All kits are tools"?* Then I follows (kits inside tools, tools outside boxes).
**Common mistakes / traps:** Choosing (a) because "no, no" feels like it chains; two negatives prove nothing.

### Q39 ⭐⭐ 🟡 Statements: All juniors are analysts. Some analysts are interns. Conclusions: I. Some juniors are interns. II. Some analysts are not juniors. III. Some interns are analysts. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); syllogisms appear in prep-site lists for TCS, Infosys and Wipro (unverified).
**What the interviewer is checking:** Telling a simple reversal of "some" (valid) from a link through a shared group (invalid).
**Say this in the interview:** "Some analysts are interns, which reverses to some interns are analysts: III. The interns might not be the juniors, and the analysts might all be juniors, so I and II are not forced."
**Answer:** **Only III follows.**
**Step-by-step reasoning:**
1. "Some analysts are interns" means at least one person is in both groups, so "some interns are analysts" follows: III. ("Some" statements can be turned around.)
2. I: juniors sit inside analysts, but the analyst-interns may be outside the juniors. Not forced.
3. II: all analysts could be juniors (the juniors circle could fill the analysts circle). Not forced.
**Fast method (30 seconds):** Reverse the "some" statement first; those are the safe conclusions. For the rest ask "can I draw it so it fails?"
**Check:** Verified by script over 40 valid models: I true in 32, II true in 32, III true in 40.
**Explain simply:**
- "All juniors are analysts" says juniors are a part of analysts, not that they are all of them.
- A "some" link between analysts and interns says nothing about the juniors part.
**Likely follow-ups:** 1) *Would "Some juniors are not interns" follow?* No; all juniors could be interns. 2) *If the second statement were "All analysts are interns", what follows?* All juniors are interns.
**Common mistakes / traps:** Accepting I by chaining juniors to analysts to interns; the "some" breaks the chain.

### Q40 ⭐⭐ 🟡 Statements: Some alpha are beta. All alpha are gamma. Conclusions: I. Some beta are gamma. II. Some gamma are beta. III. All beta are gamma. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); this some-plus-all pattern is the most common valid pair in prep-site syllogism sets (unverified).
**What the interviewer is checking:** Recognising the valid "some + all gives some" pattern and refusing the "all" overreach.
**Say this in the interview:** "The alpha that are beta are also gamma, so some beta are gamma and some gamma are beta. 'All beta' is not forced. I and II follow."
**Answer:** **I and II follow (III does not).**
**Step-by-step reasoning:**
1. Pick one alpha that is also beta (statement 1 guarantees one).
2. All alpha are gamma, so that one is also gamma.
3. So that single item is beta and gamma: some beta are gamma (I) and some gamma are beta (II).
4. III: beta may contain items outside alpha, and those need not be gamma. Counter-model: a beta that is not gamma. Fails.
**Fast method (30 seconds):** "Some A are B" plus "All A are C" gives "Some B are C" (and its reverse). Pick the A that is B; it inherits C.
**Check:** Verified by script over 32 valid models: I and II true in 32 of 32; III true in 16.
**Explain simply:**
- Every alpha is gamma, so the alpha-beta overlap sits inside gamma.
- "Some X are Y" and "Some Y are X" are the same fact stated two ways.
**Likely follow-ups:** 1) *Would "Some beta are not gamma" follow?* No; that is possible but not forced. 2) *If statement 2 were "Some alpha are gamma"?* Nothing follows about beta and gamma.
**Common mistakes / traps:** Choosing III because beta "looks" tied to gamma through alpha.

### Q41 ⭐⭐ 🟡 Statements: No clients are buyers. Some sellers are not buyers. Conclusions: I. Some sellers are not clients. II. Some sellers are clients. III. Some buyers are sellers. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); "none follow" items appear in prep-site syllogism sets (unverified).
**What the interviewer is checking:** Realising that two statements which both exclude "buyers" give no link between the other two groups.
**Say this in the interview:** "Both statements are negative about buyers, so they give no link between clients and sellers. The sellers who are not buyers could be clients or not. None of the three follows."
**Answer:** **None of I, II, III follows.**
**Step-by-step reasoning:**
1. Statement 1 keeps clients and buyers apart. Statement 2 says some sellers are outside buyers.
2. The sellers outside buyers could all be clients (clients are outside buyers, so that fits). Then I fails.
3. Or they could all be non-clients. Then II fails.
4. III: all sellers could be non-buyers (statement 2 only needs one), so no buyer need be a seller; III fails.
5. So each conclusion is possible but none is forced.
**Fast method (30 seconds):** The middle group (buyers) is excluded in both statements: negative plus negative gives nothing. Say "none follow" unless an either-or pair is offered. Here I and II are not contradictories (both can be true together), so no either-or applies.
**Check:** Verified by script over 30 valid models: I true in 26, II true in 24, III true in 20; none true in all.
**Explain simply:**
- A group named in both statements (the "middle" term) must connect them; here it is excluded in both, so no link.
- "Possible" is not "follows".
**Likely follow-ups:** 1) *Is this an either-or case?* No: I says some sellers are non-clients, II says some are clients; both can be true or only one, and neither is forced. 2) *If statement 1 were "All clients are buyers"?* Then the sellers who are not buyers cannot be clients, so "Some sellers are not clients" would follow (hand-checked).
**Common mistakes / traps:** Picking I because "sellers are not buyers and clients are not buyers, so sellers are not clients"; that is the undistributed-middle trap.

### Q42 ⭐⭐ 🟡 Statements: Some tools are macros. No macro is a script. For each statement, say whether it is definitely true, possibly true but not certain, or definitely false: I. Some tools are not scripts. II. Some tools are scripts. III. All tools are scripts. (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); possibility-classification items are a differentiator at analytics firms (our judgement; no source gives frequency).
**What the interviewer is checking:** Three-way thinking: certain, possible, impossible.
**Say this in the interview:** "A tool that is a macro is not a script, so some tools are not scripts: I is certain. Other tools could be scripts: II is possible. All tools being scripts would break that macro tool: III is false."
**Answer:** **I: definitely true. II: possibly true but not certain. III: definitely false.**
**Step-by-step reasoning:**
1. At least one tool is a macro; no macro is a script, so that tool is not a script. I is certain.
2. Tools beyond that macro tool could be scripts or not; both pictures fit. II is possible, not certain.
3. III says every tool is a script, but we have one tool that is not. Impossible.
**Fast method (30 seconds):** Find the guaranteed member (the macro tool). What is true of it is certain; its opposite is impossible; everything else is "possible".
**Check:** Verified by script over 24 valid models: I true in 24 of 24, II true in 16 (not all), III true in 0.
**Explain simply:**
- Certain means true in every picture; impossible means true in none; possible means true in some pictures and false in others.
- III is the contradiction of I ("all are" against "some are not").
**Likely follow-ups:** 1) *Does "Some scripts are tools" follow?* It is possible, not certain. 2) *Does "No tool is a script" hold?* It is possible, not certain: it is the opposite of II, which is also only possible.
**Common mistakes / traps:** Calling II "false" because macros are not scripts; macros are only some of the tools.

### Q43 ⭐⭐ 🟡 What are the rules that make a two-premise syllogism valid (for example: what goes wrong with two negative premises, two "some" premises, or an undistributed middle term)?
**Asked at:** commonly asked (no company-specific report found); the rules are standard textbook logic, and syllogisms recur in prep-site lists (unverified).
**What the interviewer is checking:** Whether you understand why the shortcuts work, not only the shortcuts.
**Say this in the interview:** "A valid pair needs a middle group that links both statements. Two negatives, two 'some' statements, or a middle term that never covers its whole group give no safe link."
**Answer:** **Rules of thumb for a valid conclusion from two premises (three groups, with a middle group in both):**
1. **Two negative premises give no conclusion.**
2. **Two "some" premises give no conclusion.**
3. **The middle group must be "fully covered" (distributed) in at least one premise.** Otherwise it is an undistributed middle.
4. **If one premise is negative, the conclusion must be negative; if the conclusion is negative, one premise must be negative.**
5. **If one premise is "some", the conclusion must be "some".**
6. **A group covered fully in the conclusion must be covered fully in a premise.**
**Explain simply:**
- "Covered fully" (distributed) means the statement talks about every member: "All A are B" covers A (not B); "No A is B" covers both; "Some A are B" covers neither; "Some A are not B" covers only B.
- Example, two negatives: "No cats are fish; no fish are cars" says nothing about cats and cars.
- Example, two "some": "Some analysts are managers; some managers are tall": the managers who are tall may not be analysts.
- Example, undistributed middle: "All dogs are animals; all cats are animals; so all dogs are cats" fails, because "animals" is the right-hand term in both "All" statements and is never fully covered, so the two groups need not meet.
**Worked mini-example (numbers):** Verified by script: all 256 combinations of two premises (each of the 4 types) in the 4 standard arrangements of the middle group, tested against conclusions linking the two end groups with every group non-empty, gave 24 valid forms; none had two negative premises or two "some" premises.
**Likely follow-ups:** 1) *Why does "All A are B, all C are B" fail?* Middle B is never fully covered. 2) *Is "All A are B, all B are C, so all A are C" valid?* Yes; B is fully covered in the second premise.
**Common mistakes / traps:** Treating "All A are B" as meaning "all B are A", and forgetting that these rules assume every group has members (the convention here).

### Q44 ⭐⭐ 🟡 Why is "If it is a bonus month, payroll is late; payroll is late; so it is a bonus month" invalid, and what is the name of the error?
**Asked at:** commonly asked (no company-specific report found); affirming the consequent is named in conditional-reasoning prep pages (unverified).
**What the interviewer is checking:** Spotting the reversed conditional in a workplace setting.
**Say this in the interview:** "The rule says bonus month leads to late payroll, not the other way round. Payroll could be late for other reasons, such as a system fault. This is affirming the consequent, so the conclusion is not valid."
**Answer:** **Invalid; the error is "affirming the consequent" (also called the converse error).**
**Step-by-step reasoning:**
1. Rule: B then L (B = bonus month, L = payroll late).
2. Fact: L is true.
3. Conclusion: B. This reverses the arrow.
4. Counter-example: a month with no bonus where a bank holiday delays payroll. Rule true, L true, B false.
5. Only two moves are safe: B is true so L is true (modus ponens), or L is false so B is false (contrapositive).
**Check:** Truth table by hand: with B false and L true the rule "if B then L" is true, the premise L is true, and the conclusion B is false. That single row proves invalidity.
**Explain simply:**
- The rule gives a sufficient cause (bonus month is enough for late payroll), not a necessary one (late payroll can arise otherwise).
- Related forms: converse "If late then bonus" (not equivalent), inverse "If not bonus then not late" (not equivalent), contrapositive "If not late then not bonus" (equivalent).
**Likely follow-ups:** 1) *What if the payroll is on time?* Then it is not a bonus month (contrapositive). 2) *What if it is not a bonus month?* Nothing follows ("denying the antecedent" would be wrong).
**Common mistakes / traps:** Saying "the conclusion is false"; it may be true, just unproven.

### Q45 ⭐⭐ 🟡 Can a conclusion be logically valid and still false in the real world? Explain the difference between a valid conclusion and a true conclusion, using a small example.
**Asked at:** commonly asked (no company-specific report found); the validity versus truth distinction is standard logic teaching (unverified for specific companies).
**What the interviewer is checking:** Whether you know that logic checks the link between statements and conclusion, not the facts.
**Say this in the interview:** "Yes. Valid means the conclusion must be true IF the statements are true. If a statement is false in the real world, a valid conclusion can still be false. In syllogism tests we accept the statements as given."
**Answer:** **Yes. A valid conclusion is forced by the premises; a true conclusion matches the real world. They are different questions.**
**Explain simply:**
- Valid is about structure: if all premises were true, the conclusion could not be false.
- True is about facts: does it match reality?
- Sound argument = valid structure AND true premises; only then is the conclusion guaranteed true.
**Worked mini-example:** "All cats are dogs. Tom is a cat. So Tom is a dog." The structure is valid (it is "All A are B; x is A; so x is B"). The conclusion is false in the real world because the first premise is false. The reverse also happens: "Some analysts are tall; some tall people are managers; so some analysts are managers" may sound plausible, and may even be true in a real office, but it is invalid because it is not forced. (Hand-checked.)
**Likely follow-ups:** 1) *In a test, should I use real-world knowledge?* No; use only the given statements. 2) *Can an invalid argument have a true conclusion?* Yes, by luck; it just is not proven.
**Common mistakes / traps:** Rejecting a valid conclusion because it sounds silly in real life.

### Q46 ⭐⭐ 🟡 How do you prove that a conclusion does NOT follow from given statements, using a counter-example Venn diagram or a small data set?
**Asked at:** commonly asked (no company-specific report found); the Venn method is described by prep sites (reported, unverified).
**What the interviewer is checking:** whether you know that "follows" means "true in EVERY possible situation", so one bad situation kills a conclusion.
**Say this in the interview:** "A conclusion follows only if it holds in every situation that fits the statements. So I build one small situation where all the statements are true but the conclusion is false. One such example is enough to reject it."
**Answer:** **Build one counter-example: a Venn diagram or tiny table where every statement is true and the conclusion is false. That single case proves the conclusion does not follow.**
**Step-by-step reasoning:**
1. Write each statement as a rule on groups ("All A are B" means every A is also a B).
2. Draw or list a tiny world (2-5 items) that obeys all the statements.
3. Check the conclusion in that world. If it is false there, stop: it does not follow.
4. If you cannot build such a world after trying, the conclusion probably follows; confirm by checking every possible region.
**Worked example:** Statements: Some tasks are jobs; all jobs are shifts; all roles are shifts. Conclusion: "Some shifts are not jobs." Small data set: Task1 = job and shift; Role1 = job and shift (a role that is also a job). Every statement is true, but no shift is outside "job". So the conclusion does not follow (brute force over all Venn-region models confirmed a counter-model exists).
**Check:** the worked example was verified by script (enumeration of all region models).
**Explain simply:**
- "Follows" (valid) means forced in every possible world; "could be true" is weaker.
- A counter-example needs all statements true at once and the conclusion false.
- A counter-example proves "does not follow"; a single example that fits can never prove "follows".
**Likely follow-ups:** Does one example where the conclusion is true prove it follows? No; you must show it holds in all worlds. Can the counter-world be silly? Yes, as long as it obeys every statement and the "every group is non-empty" convention.
**Common mistakes / traps:** Using a world that breaks a statement; testing only one friendly world and declaring the conclusion proven; forgetting that groups must be non-empty.

### Q47 ⭐⭐ 🟡 What are modus ponens and modus tollens, and why is modus tollens valid while "denying the antecedent" is not?
**Asked at:** commonly asked (no company-specific report found); sources list denying the antecedent and affirming the consequent as classic traps (prep sites, reported, unverified).
**What the interviewer is checking:** correct handling of "if P then Q" and its contrapositive.
**Say this in the interview:** "Modus ponens: if P then Q, P is true, so Q. Modus tollens: if P then Q, Q is false, so P is false. Denying the antecedent says P is false so Q is false, which is invalid because Q can be true for another reason."
**Answer:** **Modus ponens (affirm P, get Q) and modus tollens (deny Q, get not-P) are valid. Denying the antecedent (not P, so not Q) is invalid.**
**Explain simply:**
- In "If P then Q", P is the antecedent (the condition) and Q the consequent (the result). Modus ponens means "method of affirming"; modus tollens means "method of denying".
- Modus tollens is the contrapositive in action: "if P then Q" is the same claim as "if not Q then not P". If Q failed, P cannot have been true, or Q would have happened.
- Denying the antecedent uses the inverse "if not P then not Q", which is NOT the same claim. It leaves room for Q to arrive another way.
**Worked mini-example:** Rule: if it is a bonus month (P), payroll is late (Q). Payroll is on time, so it is not a bonus month (valid). It is not a bonus month, so payroll is on time (invalid: payroll can be late for another reason). Truth table check by script: modus ponens and modus tollens have no counter-row; denying the antecedent fails in the row P false, Q true.
**Likely follow-ups:** Name the fallacy "Q is true so P is true". Affirming the consequent (also invalid, same failing row). Which one statement is always equivalent to the rule? Only the contrapositive.
**Common mistakes / traps:** Treating the inverse or converse as equivalent to the rule; thinking "if" means "if and only if".

### Q48 ⭐⭐ 🟡 Rule: "Every invoice above 50,000 must carry two approvals." You see four cards, each showing one side of an invoice: (1) amount 80,000, (2) amount 20,000, (3) two approvals, (4) one approval. Which cards must you turn over to check the rule, and which need not be checked?
**Asked at:** commonly asked (no company-specific report found); this is a Wason-style rule-check, a standard reasoning puzzle.
**What the interviewer is checking:** whether you test for rule violations (P true and Q false) instead of confirming examples.
**Say this in the interview:** "The rule is broken only by a big invoice with fewer than two approvals. So I turn over the 80,000 card and the one-approval card, and nothing else."
**Answer:** **Turn over cards (1) 80,000 and (4) one approval. Cards (2) and (3) need not be checked.**
**Step-by-step reasoning:**
1. The only violation is: amount above 50,000 AND not two approvals.
2. Card 1 (80,000): the hidden side could be one approval, a violation. Check.
3. Card 2 (20,000): the rule says nothing about small invoices, whatever they carry. Skip.
4. Card 3 (two approvals): whatever the amount, the rule is not broken. Skip.
5. Card 4 (one approval): the hidden amount could be above 50,000, a violation. Check.
**Fast method (30 seconds):** ask of each card "could the hidden side make a violation?" Only the cards showing "P" and "not Q" can.
**Check:** verified by script: only cards 1 and 4 have a hidden value that can create a violation.
**Explain simply:**
- A rule "if P then Q" is broken only by P together with not-Q.
- Card 3 feels tempting but "two approvals" with a small amount is perfectly legal; the rule is not "only big invoices have two approvals".
**Likely follow-ups:** If the rule were "if and only if", which cards? All four, since small invoices with two approvals would then also be violations. Which card is the classic mistake? Card 3.
**Common mistakes / traps:** Turning the "two approvals" card (confirming, not testing) and skipping the "one approval" card.

### Q49 ⭐⭐ 🟡 Rule: "If the server is down, the dashboard shows an error." Which argument is valid? (a) The dashboard shows an error, so the server is down. (b) The server is not down, so the dashboard shows no error. (c) The dashboard shows no error, so the server is not down. (d) The server is up, so the dashboard shows an error.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** applying the contrapositive and rejecting the converse and inverse.
**Say this in the interview:** "Only (c) is valid. It is modus tollens: if the server being down forces an error, no error means the server cannot be down."
**Answer:** **(c)**
**Step-by-step reasoning:**
1. P = server down, Q = dashboard shows error. Rule: P then Q.
2. (a) Q so P: the converse (affirming the consequent). Invalid; a bug can also cause an error.
3. (b) not P so not Q: the inverse (denying the antecedent). Invalid.
4. (c) not Q so not P: the contrapositive. Valid.
5. (d) not P so Q: does not even follow the rule's direction; invalid.
**Fast method (30 seconds):** the only valid move after the rule is to affirm the first part or deny the second part; (c) denies the second part.
**Check:** verified by script over all four truth-table rows: only (c) has no counter-row.
**Explain simply:**
- Contrapositive: flip and negate both parts, and it says the same thing as the rule.
- Converse (flip only) and inverse (negate only) are different claims.
**Likely follow-ups:** If the dashboard shows an error, what can you say? Nothing certain about the server. Which fallacy is (a)? Affirming the consequent.
**Common mistakes / traps:** Picking (a) because error and downtime "go together" in real life; logic only uses what the rule states.

### Q50 ⭐⭐ 🟡 Rules: "A candidate is shortlisted if and only if she clears the test and has at least 2 years of experience." Meera cleared the test but was not shortlisted. What follows about Meera, and what would follow if instead Meera had not cleared the test?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** reading "if and only if" with a two-part condition and negating "A and B" correctly.
**Say this in the interview:** "Shortlisted means both conditions hold, and both holding means shortlisted. Meera passed the test but was not shortlisted, so she must lack the 2 years of experience. If she had not cleared the test, she would be not shortlisted, and we would learn nothing about her experience."
**Answer:** **Case 1: Meera has fewer than 2 years of experience. Case 2 (test not cleared): she is not shortlisted, and her experience cannot be determined.**
**Step-by-step reasoning:**
1. "If and only if" works both ways: shortlisted exactly when (test AND experience).
2. Not shortlisted therefore means NOT (test AND experience), i.e. test failed OR experience below 2 years (or both).
3. Meera passed the test, so the "test failed" option is gone; experience must be below 2 years.
4. If she failed the test, the AND is already broken, so not shortlisted regardless of experience.
**Check:** verified by script over all 8 true/false combinations: case 1 forces experience short; case 2 leaves both experience values possible.
**Explain simply:**
- Not (A and B) means at least one is missing, not that both are.
- "If and only if" is "if" plus "only if" combined.
**Likely follow-ups:** If Radha is shortlisted, what follows? She cleared the test and has 2 or more years. If Sam has 3 years and was not shortlisted? He did not clear the test.
**Common mistakes / traps:** Concluding "Meera failed the test" or "Meera has no experience at all"; only "less than 2 years" is certain.

### Q51 ⭐⭐ 🟡 Rule: "If a customer is Gold and has an open ticket, the ticket is prioritised." Customer Z is Gold and none of Z's tickets is prioritised. What follows about Z?
**Asked at:** commonly asked (no company-specific report found); conditional rules underlie data-validation questions (prep-site reasoning, unverified).
**What the interviewer is checking:** applying the contrapositive to a rule with a compound condition.
**Say this in the interview:** "Z is Gold, and no ticket is prioritised, so by contrapositive none of Z's tickets can be open. Z has no open ticket."
**Answer:** **Z has no open ticket (any tickets Z has are closed, or Z has none).**
**Step-by-step reasoning:**
1. Rule: (Gold AND open) leads to prioritised, for each ticket.
2. Contrapositive: not prioritised leads to not (Gold AND open), i.e. not Gold OR not open.
3. Z is Gold, so "not Gold" is out; the ticket must be not open.
4. This holds for every ticket of Z.
**Check:** verified by script over every combination of up to 3 tickets: the only consistent situations have no open ticket.
**Explain simply:**
- You cannot say Z has no tickets at all, only none open.
- The rule only speaks about Gold customers with open tickets.
**Likely follow-ups:** If Z were not Gold, what follows? Nothing about the open tickets. Could Z have a closed ticket? Yes.
**Common mistakes / traps:** Concluding "Z has no ticket" or "Z is not Gold"; Z's Gold status is given, so it cannot be the fact that changes.

### Q52 ⭐⭐ 🟡 Rule: "If a batch is corrupted, the load fails. If the load fails, the alert fires." Today the alert did not fire. Which of these must be true: I. The load did not fail. II. The batch was not corrupted. III. The batch was clean and the load was run?
**Asked at:** commonly asked (no company-specific report found); chained-conditional style appears in prep sites (reported, unverified).
**What the interviewer is checking:** chaining contrapositives backwards and refusing to add unstated facts.
**Say this in the interview:** "Alert did not fire, so the load did not fail, so the batch was not corrupted. That gives I and II. III adds that the load was run, which nothing tells us."
**Answer:** **I and II only.**
**Step-by-step reasoning:**
1. Chain: corrupted, then load fails, then alert fires.
2. Alert did not fire: by contrapositive of rule 2, the load did not fail (I true).
3. Load did not fail: by contrapositive of rule 1, the batch was not corrupted (II true).
4. III says the load was run. "Did not fail" is also true if the load never ran, so III is not forced.
**Check:** verified by script over all 16 combinations of corrupted, failed, alert, run: I and II hold in every consistent one; III fails when the load was not run.
**Explain simply:**
- Run the chain in reverse: the last link missing means every earlier link is missing.
- "Did not fail" is not the same as "ran successfully".
**Likely follow-ups:** If the alert fired, was the batch corrupted? Not necessarily; other causes may fail the load.
**Common mistakes / traps:** Accepting III because "clean batch" sounds right; the "load was run" part is an extra claim.

### Q53 ⭐⭐ 🟡 Statement: "None but data staff attended the workshop." Neha is data staff. Ravi attended the workshop. Which of these must be true: I. Ravi is data staff. II. Neha attended the workshop. III. Anyone who is not data staff did not attend?
**Asked at:** commonly asked (no company-specific report found); "only" statements are a standard 3-star topic in the sources (prep-site judgement).
**What the interviewer is checking:** decoding "none but" as "only", which points from attended to data staff.
**Say this in the interview:** "'None but data staff attended' means attendance requires being data staff. Ravi attended, so he is data staff (I). Neha being data staff does not mean she attended, so II fails. III is the same rule said backwards, so it holds."
**Answer:** **I and III.**
**Step-by-step reasoning:**
1. "None but X did Y" equals "only X did Y": if attended, then data staff.
2. I: Ravi attended, so Ravi is data staff. True.
3. II: the rule does not say all data staff attended. Not forced.
4. III: not data staff leads to did not attend; that is the contrapositive. True.
**Fast method (30 seconds):** write "attended leads to data staff" and use only that arrow: forward use (I) and contrapositive (III) are fine; reversed use (II) is not.
**Check:** hand-checked (II verified false by a quick enumeration where Neha did not attend).
**Explain simply:**
- "Only" names a necessary condition, not a guarantee.
- Contrapositive: the same rule, flipped and negated.
**Likely follow-ups:** What if the statement were "All data staff attended"? Then II would follow, I would not.
**Common mistakes / traps:** Reading "only data staff" as "all data staff attended".

### Q54 ⭐⭐ 🟡 Of 25 invoices, all but three carry a purchase order (PO), and the rule "Only invoices with a PO are paid" holds. If 19 invoices are paid, how many invoices with a PO are unpaid?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** translating "all but three" and "only" into set sizes.
**Say this in the interview:** "22 invoices have a PO. Only PO invoices are paid, so all 19 paid ones are inside the 22. That leaves 3 PO invoices unpaid."
**Answer:** **3**
**Step-by-step reasoning:**
1. All but three carry a PO: 25 - 3 = 22 with a PO.
2. "Only PO invoices are paid": paid is a subset of PO.
3. So all 19 paid invoices have a PO; 22 - 19 = 3 PO invoices are unpaid.
4. Total unpaid is 25 - 19 = 6: the 3 without PO plus these 3.
**Check:** verified by script (22 - 19 = 3) and by 25 - 19 = 6 unpaid in total, 3 of them without PO.
**Explain simply:**
- "All but three" means exactly three lack the property.
- "Only A are B" means B is inside A.
**Likely follow-ups:** If 23 were paid? Impossible: only 22 can be paid.
**Common mistakes / traps:** Answering 6 (all unpaid) or 25 - 19 without removing the non-PO invoices.

### Q55 ⭐⭐ 🟡 Of 15 analysts, 9 use SQL and 8 use Excel ("most" means more than half). Every analyst uses at least one of the two tools. What is the smallest and what is the largest possible number who use both?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** inclusion-exclusion and noticing when a range collapses to one value.
**Say this in the interview:** "Both = SQL + Excel - total when everyone uses at least one: 9 + 8 - 15 = 2. The count is forced, so smallest and largest are both 2."
**Answer:** **Smallest = 2 and largest = 2 (exactly 2 use both).**
**Step-by-step reasoning:**
1. Union = SQL + Excel - both.
2. Everyone uses at least one tool, so union = 15.
3. 15 = 9 + 8 - both, so both = 2.
4. Nothing is left free, so no range exists. Premise note: the question suggests a range, but the "everyone uses a tool" condition pins the answer.
**Check:** verified by script over every possible overlap from 0 to 15: only 2 gives a union of 15.
**Explain simply:**
- Adding 9 and 8 counts the overlap twice; subtracting the total removes that double-count.
- A range appears only if some analysts could use neither tool.
**Likely follow-ups:** If analysts could use neither, what is the range of "both"? the overlap runs from at least 2 up to at most 8 (smallest 2, largest 8; verified by script).
**Common mistakes / traps:** Giving 0 to 8 without using the "at least one" condition.

### Q56 ⭐⭐ 🟡 "If a model is overfit, its training accuracy is high. Model Y is not overfit, so its training accuracy is not high." Is this valid? Name the error or the rule.
**Asked at:** commonly asked (no company-specific report found); analytics-flavoured version of a classic fallacy.
**What the interviewer is checking:** spotting denying the antecedent in a data-science setting.
**Say this in the interview:** "Not valid. It denies the antecedent: the rule says overfit leads to high training accuracy, not that high training accuracy happens only when overfit. A good model can also have high training accuracy."
**Answer:** **Invalid; the error is denying the antecedent (also called the inverse error).**
**Step-by-step reasoning:**
1. P = overfit, Q = high training accuracy. Rule: P then Q.
2. The argument says: not P, therefore not Q.
3. That form fails when P is false and Q is true: a well-fitted model with high training accuracy.
4. The valid partner would be modus tollens: training accuracy not high, so not overfit.
**Check:** verified by script: the form fails in the row P false, Q true.
**Explain simply:**
- The rule gives overfit a consequence; it does not say only overfit models score high.
- Overfitting is really judged by a gap between training and test accuracy, but logic only needs the rule as stated.
**Likely follow-ups:** What valid conclusion can you draw if training accuracy is low? Model is not overfit.
**Common mistakes / traps:** Calling it modus tollens because it "looks negative".

### Q57 ⭐⭐ 🟡 "All auditors are careful. All pilots are careful. So all pilots are auditors." Which error is this? (a) undistributed middle (b) ad hominem (c) false cause (d) hasty generalisation
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** recognising the middle-term error in a syllogism.
**Say this in the interview:** "It is (a), undistributed middle. 'Careful' is the middle term and neither premise says it covers all careful people, so auditors and pilots can be separate groups inside it."
**Answer:** **(a) undistributed middle**
**Step-by-step reasoning:**
1. Middle term = "careful", present in both premises but absent from the conclusion.
2. In both premises it is the predicate of an "All" statement, so neither premise talks about ALL careful people.
3. Counter-world: auditors and pilots are two separate groups, both inside "careful". Both premises hold, conclusion false.
4. Other options: ad hominem attacks a person; false cause confuses correlation with cause; hasty generalisation draws a broad rule from too few cases.
**Check:** verified by script: a model exists with both premises true and the conclusion false.
**Explain simply:**
- Being in the same bigger group does not make two groups the same group.
- Same shape: "All dogs are animals; all cats are animals; so all cats are dogs".
**Likely follow-ups:** What would make it valid? "All auditors are careful; all careful people are pilots" gives all auditors are pilots.
**Common mistakes / traps:** Choosing false cause because of the "so".

### Q58 ⭐⭐ 🔴 Statements: Some tasks are jobs. All jobs are shifts. All roles are shifts. Conclusions: I. Some tasks are shifts. II. All tasks are shifts. III. Some shifts are roles. IV. Some shifts are not jobs. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); statement-conclusion items are reported for Mu Sigma and Indian campus tests by prep sites (unverified).
**What the interviewer is checking:** separating "must be true" from "could be true", including a conclusion that uses the non-empty convention.
**Say this in the interview:** "I follows by chaining: a task that is a job is a shift. III follows because roles exist and all of them are shifts. II and IV only might be true, so they do not follow."
**Answer:** **Only I and III follow.**
**Step-by-step reasoning:**
1. Some task is a job; every job is a shift; so that task is a shift. I follows.
2. II: only the job-tasks are guaranteed to be shifts; other tasks are unconstrained. Fails.
3. III: roles are non-empty by convention and all roles are shifts, so at least one shift is a role. Follows.
4. IV: shifts could all be jobs (roles that are also jobs, nothing else). A counter-world exists, so it fails.
**Fast method (30 seconds):** draw jobs inside shifts, roles inside shifts, and one task dot in jobs. Then test each conclusion by moving things around: II and IV break easily.
**Check:** checked by brute force over all 736 region-occupancy models (every group non-empty): I and III hold in all, II and IV fail in some.
**Explain simply:**
- Follows = true in every model; II and IV are possible but not certain.
- "All roles are shifts" plus a non-empty roles group gives "some shifts are roles".
**Likely follow-ups:** Does "some roles are jobs" follow? No; roles and jobs may not overlap. Does "some tasks are not roles" follow? No (checked: possible but not forced).
**Common mistakes / traps:** Accepting II by reading "some tasks are jobs, jobs are shifts" as a rule for all tasks; rejecting III because "no statement links roles to anything else", forgetting the convention.

### Q59 ⭐⭐ 🔴 Statements: All phones are tablets. No tablets are cables. Some screens are phones. Conclusions: I. Some screens are not cables. II. No phones are cables. III. Some screens are tablets. IV. Some cables are not screens. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** chaining three statements and handling a negative "some not" conclusion.
**Say this in the interview:** "Phones are tablets and tablets are never cables, so phones are never cables (II). A screen that is a phone is then a tablet (III) and not a cable (I). IV is about cables outside screens, which nothing forces."
**Answer:** **I, II and III follow; IV does not.**
**Step-by-step reasoning:**
1. All phones are tablets, no tablets are cables, so no phones are cables. II follows.
2. Some screen is a phone; that phone is a tablet. So some screens are tablets. III follows.
3. That same screen is a phone, hence not a cable. So some screens are not cables. I follows.
4. IV: all cables could be screens too (cables that are screens, not phones). Nothing prevents it. IV fails.
**Fast method (30 seconds):** build the chain screens (some) -> phones -> tablets, with cables sitting outside tablets. Everything on the chain inherits "not a cable"; cables themselves are unconstrained relative to screens.
**Check:** checked by brute force over all 96 region-occupancy models: I, II, III hold in all; IV fails in some.
**Explain simply:**
- "No" statements pass down to subsets: if tablets are never cables, phones (a subset) are never cables.
- A "some" statement can be carried along an "all" chain, so the screen-phone overlap becomes a screen-tablet overlap.
**Likely follow-ups:** What if the third statement were "All screens are phones"? Then IV would follow: cables exist, cannot be tablets, so cannot be phones or screens, so some cables are not screens (verified by script).
**Common mistakes / traps:** Marking IV true because cables "feel" different from screens; marking I false because the statements never mention screens and cables together.

### Q60 ⭐⭐ 🔴 Statements: All engineers are analysts. All coders are engineers. No analysts are testers. Conclusions: I. All coders are analysts. II. No coders are testers. III. Some testers are not coders. IV. Some analysts are coders. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); syllogism and statement-conclusion items are listed on prep sites for TCS NQT, Infosys, Wipro and Mu Sigma (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can chain "all" statements and use the non-empty convention to get "some" conclusions.
**Say this in the interview:** "Coders sit inside engineers, engineers sit inside analysts, and analysts do not overlap testers. So all four conclusions follow."
**Answer:** **All four, I, II, III and IV, follow.**
**Step-by-step reasoning:**
1. Draw nested circles: coders inside engineers inside analysts. Testers is a separate circle outside analysts.
2. I (All coders are analysts): coders are in engineers, engineers are in analysts, so coders are in analysts. Follows.
3. II (No coders are testers): coders are inside analysts, and analysts never touch testers. Follows.
4. III (Some testers are not coders): testers has at least one member, and none of them can be a coder (step 3). So those testers are "not coders". Follows.
5. IV (Some analysts are coders): coders has at least one member and every coder is an analyst, so at least one analyst is a coder. Follows, but only because of the stated convention that every group is non-empty.
**Fast method (30 seconds):** Draw nested circles first. A conclusion that follows must be true in the one picture that the statements allow. Here the picture is forced, so you only read off the answers.
**Check:** Verified by script: all 8 non-empty-region models consistent with the statements make I to IV true.
**Explain simply:**
- "Syllogism" means a conclusion drawn from two or more statements about groups.
- "Follows" means true in every possible picture, not just the one you drew.
- A "some" conclusion needs the non-empty convention; without it, IV and III would not be guaranteed.
**Likely follow-ups:** *If the non-empty convention were dropped, which conclusions survive?* I and II (pure "all" and "no" chains). IV and III need a member to exist.
**Common mistakes / traps:** Rejecting IV because no statement says "some". Also testing only the pictures you like instead of asking whether any allowed picture breaks the conclusion.

### Q61 ⭐⭐ 🔴 Statements: Some cats are dogs. All dogs are birds. No birds are fish. Conclusions: I. Some cats are birds. II. Some cats are not fish. III. No dogs are fish. IV. Some fish are not cats. Which conclusion(s) follow? (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); syllogism and statement-conclusion items are listed on prep sites for TCS NQT, Infosys, Wipro and Mu Sigma (prep-site claim, unverified).
**What the interviewer is checking:** Separating what is forced (through a chain) from what is merely possible.
**Say this in the interview:** "The cats that are dogs are birds, and birds are not fish. So I, II and III follow. IV is only possible, because every fish might also be a cat."
**Answer:** **I, II and III follow. IV does not.**
**Step-by-step reasoning:**
1. Draw: dogs inside birds; fish outside birds; cats overlap dogs.
2. I (Some cats are birds): the cat that is a dog is a bird. Follows.
3. II (Some cats are not fish): that same cat is a bird, and birds are not fish. Follows.
4. III (No dogs are fish): dogs are birds and birds are not fish. Follows.
5. IV (Some fish are not cats): in one allowed picture every fish is also a cat (cats can be a big circle covering the dogs and the fish), so "some fish are not cats" is not forced. Does not follow; it is only possible.
**Fast method (30 seconds):** For each conclusion try to build a legal picture where it is false. For IV that is easy; for I to III it is impossible.
**Check:** Verified by script over all legal region models (96 models): I, II, III true in all 96; IV true in 64 of 96.
**Explain simply:**
- "Follows" = true in all legal pictures; "possible" = true in some.
- The word "some" in a premise only guarantees one member, it says nothing about the leftover members.
**Likely follow-ups:** *Does "Some fish are cats" follow?* No, it is false in a picture where cats and fish are separate.
**Common mistakes / traps:** Treating "possibly true" as "follows" for IV.

### Q62 ⭐⭐ 🔴 Five tasks A, B, C, D and E are available and exactly three must be selected. Rules: (1) If A is selected, B is selected. (2) C and D are not both selected. (3) If E is selected, A is not selected. (4) B is selected only if C is selected. How many valid selections are there, and what are they?
**Asked at:** commonly asked (no company-specific report found); constraint-selection puzzles are a standard reasoning-gate format (prep-site claim, unverified).
**What the interviewer is checking:** Turning rules into if-then chains and pruning combinations systematically.
**Say this in the interview:** "Rule 4 says B needs C and rule 1 says A needs B, so A drags in B and C. That gives {A,B,C}. Without A, the only clean trio is {B,C,E}. Two selections."
**Answer:** **2 valid selections: {A, B, C} and {B, C, E}.**
**Step-by-step reasoning:**
1. Rewrite the rules: A leads to B (1); not both C and D (2); E leads to not A (3); B leads to C (4). So A leads to B leads to C.
2. Case A selected: B and C must be in. That is already three, so D and E are out. Check rule 2 (no D) and rule 3 (no E): fine. {A,B,C}.
3. Case A not selected: choose 3 of B, C, D, E. {B,C,D} breaks rule 2. {C,D,E} breaks rule 2. {B,D,E} breaks rule 4 (B without C). {B,C,E} satisfies all.
4. Unique count: 10 possible trios exist; only these 2 survive.
**Fast method (30 seconds):** Build the chain A to B to C first; it tells you how large the A group is. Then split on A in or out.
**Check:** Verified by script: all C(5,3) = 10 trios tested; only ABC and BCE pass.
**Explain simply:**
- "B is selected only if C is selected" means B leads to C, not C leads to B.
- Counting combinations: C(5,3) = 5x4x3 / (3x2x1) = 10 trios in total.
**Likely follow-ups:** *If rule 3 were dropped, how many?* Still 2: {A,B,C} and {B,C,E} (verified by script; {A,B,E} still fails rule 4).
**Common mistakes / traps:** Reading rule 4 backwards (C leads to B), which wrongly lets in {A,B,D} (B without C) and changes the count.

### Q63 ⭐⭐ 🔴 A panel of exactly three is chosen from six interviewers P, Q, R, S, T and U. Rules: (1) If P is on the panel, Q is not. (2) R is on the panel only if S is. (3) At least one of T and U is on the panel. (4) If S is on the panel, T is not. How many valid panels are there, and what are they?
**Asked at:** commonly asked (no company-specific report found); panel and team selection puzzles are a standard reasoning-gate format (prep-site claim, unverified).
**What the interviewer is checking:** Case splitting on one pivot person and checking every rule.
**Say this in the interview:** "I split on S. If S is on, T is out, so U must be in; if S is off, R is off too. That gives five panels."
**Answer:** **5 valid panels: {P,S,U}, {Q,S,U}, {R,S,U}, {P,T,U}, {Q,T,U}.**
**Step-by-step reasoning:**
1. Rules in if-then form: P leads to not Q (1); R leads to S (2); T or U present (3); S leads to not T (4).
2. Case S on the panel: T is out (4), so U is in (3). The third member comes from P, Q, R: each works (P and Q are not together, R has S). Panels {P,S,U}, {Q,S,U}, {R,S,U}: 3.
3. Case S not on the panel: R is out (2). Choose 3 from P, Q, T, U. {P,Q,T} and {P,Q,U} break rule 1. {P,T,U} and {Q,T,U} pass: 2.
4. Total 3 + 2 = 5.
**Fast method (30 seconds):** Pick the person who appears in most rules (S) and split in and out.
**Check:** Verified by script: all C(6,3) = 20 panels tested; exactly these 5 pass.
**Explain simply:**
- "R only if S" means R leads to S; S can be on without R.
- Total panels without rules: C(6,3) = 6x5x4 / 6 = 20.
**Likely follow-ups:** *If U must not be on the panel?* Zero panels remain: all 5 valid panels contain U (verified by script).
**Common mistakes / traps:** Forgetting that rule 2 only blocks R when S is absent, or missing that rule 4 works backwards too (if T is on, S must be off).

### Q64 ⭐ 🟢 "I interviewed two candidates from college X and both were weak, so graduates of college X are weak." Which fallacy is this? (a) hasty generalisation (b) straw man (c) circular reasoning (d) equivocation
**Asked at:** commonly asked (no company-specific report found); fallacy naming appears in critical-reasoning prep lists (unverified).
**What the interviewer is checking:** Whether you notice a tiny sample used for a sweeping claim.
**Say this in the interview:** "Two people are far too few to judge a whole college. That is hasty generalisation."
**Answer:** **(a) Hasty generalisation.**
**Step-by-step reasoning:**
1. The claim is about all graduates of college X.
2. The evidence is two candidates.
3. A tiny, possibly unrepresentative sample cannot support an "all" claim.
**Check:** Hand-checked: the other options need a misquoted argument (straw man), a conclusion restating the premise (circular) or a word with two meanings (equivocation); none appears.
**Explain simply:**
- A sample is a small group used to learn about a bigger group; it must be large and fair enough.
- Two weak candidates could just be bad luck.
**Likely follow-ups:** *What would fix it?* Look at many more graduates, chosen without bias.
**Common mistakes / traps:** Calling it false cause; nothing here claims the college caused anything.

### Q65 ⭐ 🟡 Why is the conditional "If P then Q" counted as true when P is false (vacuous truth), and for how many of the four true/false combinations of P and Q is it true?
**Asked at:** commonly asked (no company-specific report found); a logic-basics question.
**What the interviewer is checking:** Whether you understand "if-then" as a promise that is only broken by one case.
**Say this in the interview:** "An if-then statement is only false when the condition holds and the result fails. So it is true in three of the four combinations."
**Answer:** **"If P then Q" is true in 3 of the 4 combinations; false only when P is true and Q is false.**
**Explain simply:**
- "Vacuous truth" means a rule is not broken when its condition never happens. "If it rains I carry an umbrella" is not broken on a dry day.
- Truth table:
  | P | Q | If P then Q |
  |---|---|---|
  | T | T | True |
  | T | F | False |
  | F | T | True |
  | F | F | True |
- The statement is a promise about P-cases only. Where P is false, nothing was promised, so there is no broken promise.
**Worked mini-example:** Rule "if a record is flagged, it is reviewed". An unflagged record that is reviewed or not reviewed does not break the rule. Only a flagged, unreviewed record does.
**Likely follow-ups:** *In a table, which rows violate the rule?* Only those with P true and Q false. Table computed by script (3 true, 1 false).
**Common mistakes / traps:** Calling the statement "false" or "unknown" when P is false, or thinking that Q must hold whenever P is false.

### Q66 ⭐ 🟡 How does deductive checking of a rule help in everyday analyst work, for example when validating a business rule against a table, and what is a counter-example record?
**Asked at:** commonly asked (no company-specific report found); relevant to data validation work.
**What the interviewer is checking:** Whether you can connect logic to real checks on data.
**Say this in the interview:** "A business rule is an if-then. I search the table for rows where the condition is true and the result is false. Even one such row proves the rule is violated."
**Answer:** **Checking a rule means hunting for counter-example records: rows where the condition holds but the required result does not.**
**Explain simply:**
- A "counter-example record" is one row that breaks the rule. One is enough to disprove "always"; but no number of confirming rows can prove it for new data you have not seen.
- Rows where the condition is false say nothing about the rule (see vacuous truth).
**Worked mini-example:** Rule: "every invoice above 50,000 has two approvals". Scan invoices with amount above 50,000 and count approvals; any with fewer than two is a counter-example. Invoices of 20,000 with one approval are fine. Hand-checked.
**Likely follow-ups:** *The rule says "only if". What do you filter on?* Look at the "only" side: rows with the result present and the condition false (for example, claims paid with an inactive policy).
**Common mistakes / traps:** Checking rows that satisfy the rule and calling it proven, or checking the converse (rows with approvals) instead of rows with the condition.

### Q67 ⭐ 🟡 List five logical fallacies an analyst might meet in business meetings, with a one-line example of each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Vocabulary for spotting weak arguments, plus the ability to give a business example.
**Say this in the interview:** "I would name five: false cause, hasty generalisation, ad hominem, straw man and false dilemma, each with a meeting example."
**Answer:** **Five fallacies (a fallacy is a flaw in reasoning that makes an argument look stronger than it is):**
1. **False cause:** "Sales rose after we changed the logo, so the logo caused it." (Timing or correlation is not causation.)
2. **Hasty generalisation:** "Two customers complained, so the product is bad." (Sample too small.)
3. **Ad hominem:** "Ignore his forecast, he was wrong last year." (Attacks the person, not the argument.)
4. **Straw man:** "We should review the budget." "So you want to cut every team?" (Distorts the other side's claim.)
5. **False dilemma:** "Either we hire ten analysts or the project fails." (Ignores other options.)
**Explain simply:**
- A fallacy can have a true conclusion; the problem is the support is weak.
- Test: ask "does the evidence actually prove this?"
**Likely follow-ups:** *Which is affirming the consequent?* "Dashboards break when the server is down; the dashboard broke, so the server is down." (Reverses an if-then.)
**Common mistakes / traps:** Mixing up straw man (distorting a view) with ad hominem (attacking the person).

### Q68 ⭐ 🟡 Of 100 employees, 80 know SQL and 70 know Excel. What is the smallest possible and the largest possible number who know both?
**Asked at:** commonly asked (no company-specific report found); overlap-of-sets items appear in aptitude sections.
**What the interviewer is checking:** Bounds on overlap using total headcount.
**Say this in the interview:** "Smallest is 80 + 70 - 100 = 50, because the two groups must overlap that much. Largest is 70, the size of the smaller group."
**Answer:** **Smallest 50, largest 70 know both.**
**Step-by-step reasoning:**
1. Each person who knows SQL or Excel is counted once in the union: SQL + Excel - Both = union.
2. The union cannot exceed 100: 80 + 70 - Both <= 100, so Both >= 50.
3. Both cannot exceed the smaller group: Both <= 70.
4. At Both = 70 all Excel users know SQL and the union is 80 (20 know neither SQL nor Excel); that is allowed.
**Fast method (30 seconds):** Min overlap = sum minus total (if positive); max overlap = smaller group.
**Check:** Verified by script: tried every Both from 0 to 100; valid values are 50 to 70.
**Explain simply:**
- "Union" means people in at least one group.
- Squeezing 150 "skills" into 100 people forces at least 50 doubles.
**Likely follow-ups:** *If every employee knows at least one tool, what is the overlap?* Exactly 50, since 80 + 70 - Both = 100 (hand-checked).
**Common mistakes / traps:** Answering 0 for the smallest, or 80 for the largest.

### Q69 ⭐ 🟡 Manager: "We should review the leave policy." Reply: "So you want to abolish leave altogether?" Which fallacy is this? (a) straw man (b) false cause (c) hasty generalisation (d) circular reasoning
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Spotting a distorted version of someone's claim.
**Say this in the interview:** "Reviewing the policy is not the same as abolishing leave. The reply attacks an exaggerated version, a straw man."
**Answer:** **(a) Straw man.**
**Step-by-step reasoning:**
1. The manager's claim is mild: review the policy.
2. The reply restates it as an extreme: abolish leave.
3. Attacking the extreme version instead of the real claim is a straw man.
**Check:** Hand-checked: no cause is claimed (not false cause), no sample is used (not hasty generalisation), no circular support (not circular reasoning).
**Explain simply:**
- Like beating up a scarecrow instead of the real person.
**Likely follow-ups:** *How do you respond?* "I only said review, not abolish."
**Common mistakes / traps:** Choosing "false dilemma"; it is not offered here and no either-or is given.

### Q70 ⭐ 🟡 Rule: "If a transaction is above 1 lakh, it is reviewed." A review log shows transaction T9 was reviewed. Which statement is justified? (a) T9 was above 1 lakh. (b) T9 may or may not have been above 1 lakh. (c) T9 was not above 1 lakh. (d) All transactions are reviewed.
**Asked at:** commonly asked (no company-specific report found); affirming the consequent is a classic trap on prep sites.
**What the interviewer is checking:** Not reversing an if-then.
**Say this in the interview:** "The rule says above 1 lakh leads to review. It does not say only those are reviewed. So T9 could be either."
**Answer:** **(b) T9 may or may not have been above 1 lakh.**
**Step-by-step reasoning:**
1. Rule: above 1 lakh (P) leads to reviewed (Q).
2. We know Q (reviewed). Going from Q back to P is the converse, which is not guaranteed.
3. A transaction below 1 lakh may be reviewed for other reasons (random sample).
**Check:** Hand-checked with a counter-example: a 50,000 transaction that was reviewed satisfies the rule.
**Explain simply:**
- 1 lakh = 100,000.
- Seeing the result (reviewed) does not tell you the condition happened.
**Likely follow-ups:** *If T9 was not reviewed?* Then it was not above 1 lakh (contrapositive).
**Common mistakes / traps:** Choosing (a); that is affirming the consequent. (d) also overreaches.

### Q71 ⭐ 🔴 Statements: All rows are keys. Some keys are flags. No flag is a date. For each statement, say whether it is definitely true, possibly true but not certain, or definitely false: I. Some rows are flags. II. Some keys are not dates. III. Some rows are dates. IV. No row is a date. (Treat "some" as "at least one" and assume every named group has at least one member.)
**Asked at:** commonly asked (no company-specific report found); possibility classification is a harder syllogism variant (judgement from the sources file, frequency unknown).
**What the interviewer is checking:** Telling definitely true from possible from impossible.
**Say this in the interview:** "Rows are inside keys. Some keys are flags, but those flag-keys need not be rows. So II is definite; I, III and IV are only possible."
**Answer:** **I possibly true; II definitely true; III possibly true; IV possibly true (none is definitely false).**
**Step-by-step reasoning:**
1. Draw rows inside keys. Flags overlap keys somewhere; flags never touch dates.
2. II (Some keys are not dates): the keys that are flags are not dates. Definitely true.
3. I (Some rows are flags): the flag-keys might lie outside rows, or inside; both are allowed. Possible.
4. III (Some rows are dates): a row is a key, and a key can be a date as long as it is not a flag. Allowed, but not forced. Possible.
5. IV (No row is a date): equally allowed (rows and dates may be separate). Possible. III and IV cannot both be true, but each can be true.
**Check:** Verified by script over all 312 legal region models: II true in all 312; I true in 224; III in 192; IV in 120.
**Explain simply:**
- Definitely true = true in every legal picture; definitely false = true in none; possible = true in some.
- III and IV are opposites, so one is always true, yet each is individually uncertain.
**Likely follow-ups:** *Is "Some rows are not flags" definite?* No; all rows could be flags.
**Common mistakes / traps:** Marking I as definite because "some keys are flags" and rows are keys; the overlap may miss rows.

### Q72 ⭐ 🔴 "Most analysts use SQL" and "Most SQL users know Python". Why can we not conclude "Some analysts know Python"? Construct a counter-example with numbers.
**Asked at:** commonly asked (no company-specific report found); a harder "most" trap.
**What the interviewer is checking:** Knowing "most" does not chain.
**Say this in the interview:** "Most analysts use SQL and most SQL users know Python, but the SQL users who know Python can all be non-analysts. Here is a number example."
**Answer:** **The two statements are consistent with zero analysts knowing Python, so the conclusion does not follow.**
**Step-by-step reasoning:**
1. "Most" here means more than half.
2. Take 10 analysts: 6 use SQL (60%, most).
3. Add 8 non-analysts who use SQL and Python. SQL users total 6 + 8 = 14; 8 know Python (57%, most).
4. Give none of the 6 analysts Python. Then analysts who know Python = 0.
5. Both premises hold, yet the conclusion fails. One consistent example is enough to show it does not follow.
**Check:** Verified by script: 6/10 = 60% and 8/14 = 57.1%, both above 50%.
**Explain simply:**
- "Most" talks about a majority of one group; the majority of the second group can come entirely from outside the first.
- A counter-example proves a conclusion does not follow.
**Likely follow-ups:** *Does "Some analysts use SQL" follow?* Yes, 'most' gives at least one (non-empty).
**Common mistakes / traps:** Treating "most" like "all" and chaining it.

### Q73 ⭐ 🔴 In a team of 50, 40 know SQL, 35 know Excel and 30 know Python. What is the smallest possible number who know all three?
**Asked at:** commonly asked (no company-specific report found); inclusion-exclusion with three sets is an aptitude favourite.
**What the interviewer is checking:** Counting the "missing" people in each set.
**Say this in the interview:** "Count who lacks each skill: 10, 15, 20. That is 45 people-gaps. With 50 people, at most 50 gaps could hit different people, so at least 5 have none missing."
**Answer:** **Smallest number who know all three: 5.**
**Step-by-step reasoning:**
1. People who do not know SQL: 50 - 40 = 10; not Excel: 50 - 35 = 15; not Python: 50 - 30 = 20.
2. Total gaps = 10 + 15 + 20 = 45.
3. To minimise people with all three skills, make every gap fall on a different person. Different people means at most 45 distinct people lack something.
4. Then at least 50 - 45 = 5 people lack nothing, i.e. know all three.
**Fast method (30 seconds):** Sum of set sizes minus 2 x total: 40 + 35 + 30 - 2 x 50 = 5.
**Check:** Verified by script (integer programming over all 8 Venn regions): minimum 5, maximum 30.
**Explain simply:**
- A gap is a missing skill; one person can hold several gaps.
- If gaps never overlap, nobody has two missing skills, and exactly 5 are left with none.
**Likely follow-ups:** *Largest?* The smallest set, 30 (checked by script).
**Common mistakes / traps:** Subtracting only once (105 - 50 = 55) or answering 0.
