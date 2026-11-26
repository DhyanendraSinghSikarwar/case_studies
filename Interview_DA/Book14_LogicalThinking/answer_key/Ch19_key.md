# Chapter 19 answer key: Truth-Teller and Liar Puzzles

Every puzzle in the chapter (all 5 solved examples, both scenarios and all 20 practice questions) was checked by script that tried every possible labelling of truth-tellers and liars (together with every possible version of the facts, such as culprit, day or number) and confirmed that exactly one combination fits. Q19 was checked over all 3 x 3 x 3 = 27 assignments of the three kinds, and Q13 and Q20 over all 7 days. Short notation below: T = truth-teller, L = liar.

## Self-check answers

1. A liar's statement is false. "It rained yesterday" is false, so it **did not rain** yesterday.
2. Tomas tells the truth, so "Uma is a liar" is true and Uma is a liar. A liar's statement is false, so "The shop opens at 8" is false: the shop **does not open at 8**.
3. It is a **contradiction**, so the assumption "Ravi is a truth-teller" was wrong. (If nothing else could be wrong, Ravi must be a liar, but you still check that.)

## Easy

**Q1** 🟢 Omar is a liar, so his statement is false. "The refund was paid twice" is false. **No, it was not paid twice.**

**Q2** 🟢 Chen says Divya and he are both T.
- If Chen is T, then Divya is T too. But Divya says "Chen is a liar", which would then be false, and a T cannot say a false statement. Contradiction.
- So Chen is L. His statement "we are both truth-tellers" is then false, which fits (Chen is an L). Divya says "Chen is a liar", and Chen is an L, so this is true, so Divya is T.
**Chen is a liar and Divya is a truth-teller.**

**Q3** 🟢 Kiran says "Lena is a liar". Lena says "Exactly one of the two of us is a liar."
- Assume Kiran is T. Then Lena is L. Lena's statement "exactly one of us is a liar" would be true (Lena only), but an L cannot say something true. Contradiction.
- So Kiran is L. His statement is false, so Lena is T. Check Lena: Kiran is L and Lena is T, so exactly one is a liar: true. Fits a T.
**Lena is the truth-teller (Kiran is the liar).**

**Q4** 🟢 Priya is T, so the shortfall is in Sita's or Tom's ledger (so not Raj's). Quinn is L, so "in Tom's ledger" is false, so not Tom's. The only one left is Sita. **Sita's ledger.**

**Q5** 🟢 Hugo is L. Gita says "Hugo is a truth-teller", which is false, so Gita is L. Farah says "Gita is a liar", which is true, so Farah is T. Emeka says "Farah is a truth-teller", which is true, so Emeka is T. **Emeka and Farah are truth-tellers (Gita and Hugo are liars).**

**Q6** 🟢 Test each possible copier and count the false statements (the liars).

| Copier | Emeka ("Farah") | Farah ("Gita") | Gita ("Farah is lying") | Liars |
|---|---|---|---|---|
| Emeka | false | false | Farah's statement is false, so Farah is lying: true | 2 |
| Farah | true | false | Farah is lying: true | 1 |
| Gita | false | true | Farah is truthful, so "Farah is lying" is false | 2 |

Only the Farah row has exactly one liar (Farah). **Farah copied the file.**

**Q7** 🟢 Exactly two statements are true. The statements are: more than 6; multiple of 3; exactly 12.
- If Chen (exactly 12) is true, then the number is 12. Then "more than 6" is true and "multiple of 3" is true, so all three are true: no liar. Breaks the clue.
- So Chen is the liar and Alma and Bruno are truthful: more than 6 and a multiple of 3, but not 12. The multiples of 3 up to 12 that exceed 6 are 9 and 12, and without 12 we have 9.
- Check: 9 is more than 6 (true), a multiple of 3 (true), not 12 (so Chen's statement is false). Exactly one liar.
**9 invoices.**

## Medium

**Q8** 🟡 Test each possible entrant (the number of false statements must be exactly 1). Lena says "neither Mona nor Nikhil", Mona says "Lena or Nikhil", Nikhil says "not Lena", Ola says "me".

| Entrant | Lena | Mona | Nikhil | Ola | False statements |
|---|---|---|---|---|---|
| Lena | true | true | false | false | 2 |
| Mona | false | false | true | false | 3 |
| Nikhil | false | true | true | false | 2 |
| Ola | true | false | true | true | 1 |

Only the Ola row has exactly one false statement, and it is Mona's. **Ola entered; Mona is the liar.**

**Q9** 🟡 Test each possible person (exactly two liars, so exactly two false statements). Hugo says "Iris", Iris says "Hugo", Jan says "not me", Kiran says "Hugo is telling the truth" (true exactly when Hugo's statement is true).

| Culprit | Hugo | Iris | Jan | Kiran | False |
|---|---|---|---|---|---|
| Hugo | false | true | true | false | 2 |
| Iris | true | false | true | true | 1 |
| Jan | false | false | false | false | 4 |
| Kiran | false | false | true | false | 3 |

Only the Hugo row has exactly 2 false statements, and they are Hugo's and Kiran's. **Hugo altered the payment; Hugo and Kiran are the liars.**

**Q10** 🟡 Remember that a false "X and Y" only needs one false part. Priya and Quinn say "Hugo and Monday" and "Hugo and Tuesday". These cannot both be true (the day cannot be both). So at least one of Priya and Quinn is a liar, and since only one liar exists, Raj is truthful.
- Raj is truthful: "Iris or Monday" is true.
- Case A: Priya is the liar and Quinn is truthful. Then Hugo and Tuesday are true. Raj: "Iris or Monday": Iris is not the forger (it was Hugo), and Monday is not the day (it was Tuesday): false. But Raj must be truthful. Contradiction.
- Case B: Quinn is the liar and Priya is truthful. Then Hugo and Monday are true. Raj: "Iris or Monday": Monday is true, so true. Quinn: "Hugo and Tuesday" is false (Tuesday is wrong), which fits a liar. Consistent.
**Hugo forged it, on Monday; Quinn is the liar.** (Note that Quinn's false statement still had a true part, "Hugo".)

**Q11** 🟡 The statements are "at least k of us are liars" for k = 1, 2, 3, 4. Let L be the number of liars. Statement k is true exactly when k is at most L. So the truth-tellers are the ones with k = 1 up to k = L, which makes L truth-tellers. But there are 4 people, so L liars plus L truth-tellers gives 2L = 4, so L = 2. Then the statements k = 1 and k = 2 are true, and k = 3 and k = 4 are false. Check: Quinn (3) and Raj (4) are liars (2 liars), and Ola and Priya are truth-tellers. Other values of L fail: for L = 1, 1 liar needs 3 truth-tellers but only 1 statement is true; for L = 3, 3 liars need 1 truth-teller but 3 statements are true; L = 0 or 4 fail similarly. **Quinn and Raj are the liars.**

**Q12** 🟡 Whatever anyone is, the honest answer to "Are you a truth-teller?" is yes, and a liar lies about it and also says yes. So nobody could have told the investigator "I am a liar", and Nikhil did not tell Mona that. Mona's statement is false, so Mona is a liar. Nikhil says "Mona is a truth-teller", which is false, so Nikhil is a liar as well. Check: both are liars and both statements are false. **Neither is a truth-teller (both are liars).**

**Q13** 🟡 Gita lies on Mon, Wed, Fri. Her statement "Tomorrow I will tell the truth" is true when tomorrow is a truthful day (Tue, Thu, Sat, Sun) and false when tomorrow is a lying day (Mon, Wed, Fri).

| Day | Gita that day | Tomorrow | Statement is | Needed | Fits? |
|---|---|---|---|---|---|
| Mon | liar | Tue (truth) | true | false | no |
| Tue | truthful | Wed (lie) | false | true | no |
| Wed | liar | Thu (truth) | true | false | no |
| Thu | truthful | Fri (lie) | false | true | no |
| Fri | liar | Sat (truth) | true | false | no |
| Sat | truthful | Sun (truth) | true | true | yes |
| Sun | truthful | Mon (lie) | false | true | no |

**Saturday.**

**Q14** 🟡 Sana says "exactly 2 of Tej, Uma, Vik are liars". Tej says "Sana, Uma and Vik are all truthful". Uma says "Sana, Tej and Vik are all liars". Vik says "exactly 2 of Sana, Tej, Uma are liars".
- Assume Tej is T. Then Uma is T too, but Uma says Tej is a liar. Contradiction. So Tej is L.
- Assume Uma is T. Then Sana, Tej and Vik are all L. Sana is L, so her statement must be false. But among Tej, Uma, Vik the liars are Tej and Vik, exactly 2, so her statement is true. Contradiction. So Uma is L.
- Now Tej and Uma are liars. Sana's statement is true exactly when Vik is T (then the liars among Tej, Uma, Vik are exactly 2). Vik's statement is true exactly when Sana is T. So Sana and Vik are the same kind.
- If Sana and Vik were both L, then Sana, Tej and Vik would all be liars, and Uma's statement would be true. But Uma is L. Contradiction. So Sana and Vik are both T.
- Check: Sana T (Tej and Uma are the 2 liars among Tej, Uma, Vik: true), Tej L (false), Uma L (false), Vik T (true).
**Tej and Uma are the liars (Sana and Vik are truth-tellers).**

## Hard

**Q15** 🔴 Write the statements: Alma (Divya T), Bruno (Chen and Emeka both L), Chen (Bruno T), Divya (Emeka T), Emeka (Alma or Chen is a liar).
- Chen and Bruno vouch for each other, so they are the same kind (Bruno T if and only if Chen T, from both statements). If both were T, Bruno's statement "Chen and Emeka are both liars" would require Chen to be a liar. Contradiction. So Bruno and Chen are both L.
- Bruno is L, so "Chen and Emeka are both liars" is false. Chen is L, so that means Emeka is not an L: Emeka is T.
- Emeka is T and says "at least one of Alma and Chen is a liar": true, because Chen is L. Fine, but it does not decide Alma.
- Divya says "Emeka is a truth-teller", which is true, so Divya is T. Alma says "Divya is a truth-teller", which is true, so Alma is T.
- Check all: Alma T (true), Bruno L (false: Emeka is T), Chen L (false: Bruno is L, not T), Divya T, Emeka T. All fit.
**Alma, Divya and Emeka are truth-tellers (Bruno and Chen are liars).**

**Q16** 🔴 Test each possible person (exactly 2 false statements). Chen says "neither Alma nor Bruno". Divya's statement is true exactly when Chen's is. Emeka's is true exactly when Divya's is.

| Approver | Alma ("Emeka") | Bruno ("Divya") | Chen | Divya (= Chen) | Emeka (= Divya) | False |
|---|---|---|---|---|---|---|
| Alma | false | false | false | false | false | 5 |
| Bruno | false | false | false | false | false | 5 |
| Chen | false | false | true | true | true | 2 |
| Divya | false | true | true | true | true | 1 |
| Emeka | true | false | true | true | true | 1 |

Only the Chen row has exactly 2 false statements. **Chen approved the refund; Alma and Bruno are the liars.**

**Q17** 🔴 Let L be the number of liars. A statement "exactly k are liars" is true only if k = L. So the number of truth-tellers equals the number of people who said k = L, and it must equal 6 minus L.

| L | Who says k = L | Truth-tellers | Needed (6 minus L) | Fits? |
|---|---|---|---|---|
| 0, 1, 2 | nobody | 0 | 6, 5, 4 | no |
| 3 | Alma, Chen, Farah | 3 | 3 | yes |
| 4 | nobody | 0 | 2 | no |
| 5 | Bruno, Emeka | 2 | 1 | no |
| 6 | Divya | 1 | 0 | no |

**3 liars; the truth-tellers are Alma, Chen and Farah** (Bruno, Divya and Emeka are the liars).

**Q18** 🔴 Each pair has one T and one L. Test each possible thief. Statements: Alma "not Iris", Bruno "Hugo", Chen "not Hugo", Emeka "Jan", Divya's statement is true exactly when Farah is T, Farah's is true exactly when Alma is L.
- Billing pair: Alma and Bruno must differ in truth. Alma ("not Iris") and Bruno ("Hugo") are both true if Hugo did it, so Hugo cannot be the thief. If Iris did it, Alma false, Bruno false: both liars, breaks the pair rule. So the thief is Jan: Alma true (so T), Bruno false (so L). The pair is fine.
- Payroll: Chen says "not Hugo", true since Jan did it, so Chen is T and then Divya is L.
- Stores: Emeka says "Jan" which is true, so Emeka is T and Farah is L.
- Check the remaining statements: Divya (L) says "Farah is a truth-teller", which is false (Farah is L). Farah (L) says "Alma is a liar", which is false (Alma is T). All fit.
**Jan committed the theft. Alma T, Bruno L, Chen T, Divya L, Emeka T, Farah L.**

**Q19** 🔴 Exactly one person is each kind. Try each kind for Alma and read Bruno's statements: (1) "Alma is a switcher", (2) "Alma is not a truth-teller".
- Alma is a truth-teller: Bruno's (1) is false and (2) is false. Two false statements means Bruno is a liar, so Chen is the switcher. But Alma, a truth-teller, says "Bruno is a truth-teller", which is false. Contradiction.
- Alma is a liar: Bruno's (1) is false and (2) is true, a mixed pattern, so Bruno is a switcher and Chen is the truth-teller. But Chen says "Alma is a truth-teller", which is false. Contradiction.
- Alma is a switcher: Bruno's (1) and (2) are both true, so Bruno is a truth-teller and Chen is the liar.
- Check Chen (liar): "Alma is a truth-teller" is false and "Bruno is not a truth-teller" is false. Both false, fits. Check Alma (switcher): (1) "Bruno is a truth-teller" is true and (2) "Chen is a switcher" is false (true then false: opposite values, fits). Check Bruno: both true, fits.
**Alma is the switcher, Bruno the truth-teller, Chen the liar. Alma's first statement is true (her second is false).**

**Q20** 🔴 A day fits if both statements match the kind of day: on a truthful day both statements are true, on a lying day both are false. The lying days are Mon, Tue and Fri.

| Day | Kind of day | Yesterday was a lying day? | Tomorrow is a lying day? | Both statements | Needed | Fits? |
|---|---|---|---|---|---|---|
| Mon | lying | Sun: no | Tue: yes | false, true | both false | no |
| Tue | lying | Mon: yes | Wed: no | true, false | both false | no |
| Wed | truthful | Tue: yes | Thu: no | true, false | both true | no |
| Thu | truthful | Wed: no | Fri: yes | false, true | both true | no |
| Fri | lying | Thu: no | Sat: no | false, false | both false | yes |
| Sat | truthful | Fri: yes | Sun: no | true, false | both true | no |
| Sun | truthful | Sat: no | Mon: yes | false, true | both true | no |

**Friday.**
