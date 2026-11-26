# Chapter 17 answer key: Coding-Decoding and Alphabet/Number Logic

All answers were recomputed by script. Rule-finding questions (Q15, Q16, Q31 and examples 1 and 3) were checked against a family of about 1,500 candidate rules (constant, progressive and alternating shifts, with or without reversing the word); every rule that fits the examples gives the same answer. Sentence-code questions (Q18, Q19, Q32, Q38 and example 4) were checked by trying every possible word-to-code matching. Q35 was checked by trying every letter and digit combination.

## Self-check answers

1. CAT: C+1=D, A+1=B, T+1=U. **DBU**.
2. M is the 13th letter, so **13**.
3. B(2) to C(3), O(15) to P(16), X(24) to Y(25): every letter moves **1 place forward**.

## Easy

**Q1** Rule: +3. B(2)+3=5=E, A(1)+3=4=D, D(4)+3=7=G, G(7)+3=10=J, E(5)+3=8=H. **EDGJH**.

**Q2** Rule: -1. A(1)-1=0, which wraps to Z (26). B-1=A, O(15)-1=14=N, U(21)-1=20=T, T(20)-1=19=S. **ZANTS**.

**Q3** Mirror = 27 minus position. N(14) gives 13=M; A(1) gives 26=Z; M(13) gives 14=N; E(5) gives 22=V. **MZNV**.

**Q4** (a) H=8, I=9, R=18, E=5: **8 9 18 5**. (b) 20=T, 5=E, 1=A, 13=M: **TEAM**.

**Q5** Decode by moving back 2. J(10)-2=8=H, G(7)-2=5=E, N(14)-2=12=L, R(18)-2=16=P. **HELP**.

**Q6** First two letters of "chair": CH. Letters in "green": 5. Size: L. **CH5L**.

**Q7** Finance gives F, September is month 09, serial 14 written as 014. **F09014**.

**Q8** Swap the first and last letters. DESK: D and K swap, giving **KESD**. LEAVE: L and E swap, giving **EEAVL**.

**Q9** The thing you sit on is a chair. In this code language a chair is called a desk. **Desk**.

**Q10** Double the position. F(6) gives 12, A(1) gives 2, C(3) gives 6, E(5) gives 10. **12 2 6 10**.

**Q11** (a) LEDGER backwards: **REGDEL**. (b) TNEMYAP backwards: **PAYMENT**.

**Q12** PLANET splits into pairs PL, AN, ET. Swap inside each pair: LP, NA, TE. **LPNATE**.

**Q13** Differences: G(7) to J(10) is +3, A(1) to D(4) is +3, M(13) to P(16) is +3, E(5) to H(8) is +3. Rule +3. F(6)+3=9=I, I(9)+3=12=L, L(12)+3=15=O, E(5)+3=8=H. ILOH, option **(b)**. (Option (a) is +2 and (c) is +4, the typical off-by-one traps; (d) scrambles the last two letters.)

**Q14** Test each against the four conditions.
- KT482: two letters, three digits, first digit 4 (not 0), 4+8+2=14 (even). Valid.
- KT4820: four digits, fails.
- K4T82: a digit sits between the letters, fails the format.
- MP571: 5+7+1=13, odd, fails.
- RD064: first digit 0, fails.
**KT482** is the only valid one.

## Medium

**Q15** Differences for WORD to XQUH: X-W=1, Q-O=2, U-R=3, H-D=4. Progressive +1, +2, +3, +4. PLAN: P(16)+1=17=Q, L(12)+2=14=N, A(1)+3=4=D, N(14)+4=18=R. **QNDR**.

**Q16** STAFF to USCEH: S(19) to U(21) is +2; T(20) to S(19) is -1; A(1) to C(3) is +2; F(6) to E(5) is -1; F(6) to H(8) is +2. Alternating +2, -1, +2, -1, +2. CHART: C(3)+2=5=E, H(8)-1=7=G, A(1)+2=3=C, R(18)-1=17=Q, T(20)+2=22=V. **EGCQV**.

**Q17** Check the rule on TEAM: reverse gives MAET; mirror: M(13) to N(14), A to Z, E(5) to V(22), T(20) to G(7): NZVG. Matches. BONDS reversed is SDNOB. Mirrors: S(19) to 8=H, D(4) to 23=W, N(14) to 13=M, O(15) to 12=L, B(2) to 25=Y. **HWMLY**.

**Q18** "office closed today" and "closed holiday tomorrow" share "closed"; the code words they share are "ma", so closed = ma. "closed holiday tomorrow" and "tomorrow office open" share "tomorrow"; shared code "du", so tomorrow = du. The first and third sentences share "office"; shared code "fi", so office = fi. In sentence 2 the codes are du, ma, ve; closed = ma and tomorrow = du are used, so holiday = **ve**.

**Q19** Shared words and shared codes:
- Sentences 1 and 2 share "staff"; shared code ti, so staff = ti.
- Sentences 1 and 3 share "joined"; shared code ba, so joined = ba.
- Sentences 1 and 4 share "new"; shared code mo, so new = mo.
- Sentences 2 and 3 share "team"; shared code ru, so team = ru.
- Sentences 2 and 4 share "today"; shared code ne, so today = ne.
- Sentence 3: joined = ba, team = ru, so "hired" is the leftover code **pa**.
- Sentence 4: new = mo, today = ne, so "left" is the leftover code **ko**.

**Q20** HIRE: 8+9+18+5=40. FIRE: 6+9+18+5=38. WAGE: 23+1+7+5=36. LATE: 12+1+20+5=38. Largest: **HIRE (40)**. Equal: **FIRE and LATE (38 each)**. (Different words can have the same value, a first look at collisions.)

**Q21** Surname first two letters, birth month (2 digits), last letter of first name.
- Rohan Menon: ME, 03, N: **ME03N**.
- Anita Pandey: PA, 11, A: **PA11A**.
- Karan Mehta: ME, 03, N: **ME03N**.
- Priya Rao: RA, 07, A: **RA07A**.
Rohan and Karan clash (**ME03N** twice), so the ID cannot tell them apart. One fix: add a serial number at the end (ME03N01, ME03N02).

**Q22** (a) WL = wallet, S = small, GN = green, 120 grams: **a small green wallet of 120 grams**. (b) Bag = BK, large = L, blue = BL, weight 400: **BK-L-BL-400**.

**Q23** Try squares: 2 squared is 4, plus 1 is 5; 3 squared is 9, plus 1 is 10; 5 squared is 25, plus 1 is 26; 6 squared is 36, plus 1 is 37. The rule "square then add 1" fits all four. For 9: 81+1=**82**. (A computer check of all rules of the form a x n squared + b x n + c shows this rule is the only one that fits the four examples.)

**Q24** C stays a consonant: C to D. U is a vowel: *. S to T. T to U. O is a vowel: *. M to N. **D*TU*N**.

**Q25** HIRE to KLUH: H(8) to K(11), I(9) to L(12), R(18) to U(21), E(5) to H(8): +3 each. To decode, go back 3. Z(26)-3=23=W, R(18)-3=15=O, U(21)-3=18=R, N(14)-3=11=K. **WORK**.

**Q26** Sum of first five digits, then units digit:
- 483925: 4+8+3+9+2=26, units 6, sixth digit 5. Not valid.
- 120744: 1+2+0+7+4=14, units 4, sixth digit 4. Valid.
- 907651: 9+0+7+6+5=27, units 7, sixth digit 1. Not valid.
- 555550: 5+5+5+5+5=25, units 5, sixth digit 0. Not valid.
- 341682: 3+4+1+6+8=22, units 2, sixth digit 2. Valid.
**2 are valid** (120744 and 341682).

**Q27** Keys: HIRE is 4 (H), 4 (I), 7 (R), 3 (E) = 4473. GIRD is 4 (G), 4 (I), 7 (R), 3 (D) = 4473. BONUS is 26687, STAFF is 78233, PAY is 729, all different. **HIRE and GIRD, code 4473.** (They share a key for every letter, so the keypad code cannot be decoded to one word.)

**Q28** Build the lookup: the cipher alphabet written under A to Z is B U D G E T A C F H I J K L M N O P Q R S V W X Y Z.
(a) N in the cipher line is under the plain letter P (16th), B under A, Y under Y; so NBY = **PAY**. M is under O, L under N, so ML = **ON**. T is under F, P under R, F under I, G under D, B under A, Y under Y; so TPFGBY = **FRIDAY**. Message: **PAY ON FRIDAY**.
(b) S is 19th plain; the 19th cipher letter is Q. E (5th) goes to E (5th cipher letter). N (14th) goes to L. D (4th) goes to G. SEND = **QELG**.

**Q29** (Letters, vowels): PAYMENT (7, 2: A, E); LEAVE (5, 3: E, A, E); RECRUIT (7, 3: E, U, I); TENURE (6, 3: E, U, E); BENEFIT (7, 3: E, E, I); SHIFT (5, 1: I). **RECRUIT and BENEFIT share (7, 3).**

**Q30** (a) B(2) is even, half is 1. A(1) is odd, plus 1 is 2. D(4) is even, half is 2. G(7) is odd, plus 1 is 8. E(5) is odd, plus 1 is 6. **1 2 2 8 6**.
(b) D gives 2. A gives 2 as well (1+1). Any other? Odd n gives n+1 = 2 only for n=1; even n gives n/2 = 2 only for n=4. So **A and D**.
(c) Two different letters can give the same number, so the code cannot be decoded with certainty (for example, 2 could be A or D). An ID code must come from only one source, so this is a poor choice.

## Hard

**Q31** Test the idea "reverse the word, then shift progressively +1, +2, +3, +4". HIRE reversed is ERIH: E(5)+1=6=F, R(18)+2=20=T, I(9)+3=12=L, H(8)+4=12=L: FTLL. Matches. LEAD reversed is DAEL: D(4)+1=5=E, A(1)+2=3=C, E(5)+3=8=H, L(12)+4=16=P: ECHP. Matches. TRAIN reversed is NIART: N(14)+1=15=O, I(9)+2=11=K, A(1)+3=4=D, R(18)+4=22=V, T(20)+5=25=Y. **OKDVY**.

**Q32** Shared words, using the codes:
- Sentences 1 and 2 share two words (budget, review) and two codes (ha, zi), but we do not yet know which is which.
- Sentences 3 and 4 share one code, **ko**, so "urgent" = ko.
- Sentence 4 and sentence 1 share "review", with shared code **ha**. So review = ha.
- Then "budget" is the other shared code of sentences 1 and 2, which is **zi**.
- Sentence 4 has review (ha), urgent (ko), so "final" is the leftover **ro**.
Answer: **final = ro, budget = zi**. (Trying all matchings finds exactly one fit.)

**Q33** (a) LOYAL: L(12), O(15), Y(25), A(1), L(12). Places 1, 3, 5: 12+25+12=49. Places 2, 4: 15+1=16. Value 49-16=**33**.
(b) GRADE: G(7)+A(1)+E(5)=13; R(18)+D(4)=22; 13-22=-9. CADRE: C(3)+D(4)+E(5)=12; A(1)+R(18)=19; 12-19=-7. STAFF: S(19)+A(1)+F(6)=26; T(20)+F(6)=26; 26-26=0. LEAD: L(12)+A(1)=13; E(5)+D(4)=9; 13-9=4. **STAFF** has value 0.

**Q34** The shift: S(19) to Z(26) is +7. Checking the rest of SEND: E(5) to L(12) is +7, N(14) to U(21) is +7, D(4) to K(11) is +7. So the rule is a constant +7 (checked against all 26 possible shifts: only +7 turns SEND into ZLUK). To decode, move back 7 (wrapping before A to Z).
- AOL: A(1)-7 wraps to 20=T, O(15)-7=8=H, L(12)-7=5=E. THE.
- VMMLY: V(22)-7=15=O, M(13)-7=6=F, M gives F, L(12)-7=5=E, Y(25)-7=18=R. OFFER.
- SLAALY: S(19)-7=12=L, L(12)-7=5=E, A gives T, A gives T, L gives E, Y gives R. LETTER.
- AVKHF: A gives T, V(22)-7=15=O, K(11)-7=4=D, H(8)-7=1=A, F(6)-7 wraps to 25=Y. TODAY.
Message: **SEND THE OFFER LETTER TODAY**.

**Q35** Clue 2: vowels are A, E, I, O, U with positions 1, 5, 9, 15, 21; multiples of 5 are E (5) and O (15) only. Clue 1: the mirror of E is V (22), which is later in the alphabet, fine; the mirror of O is L (12), which is earlier, so O fails clue 2. So the letters are **EV**. Digits: equal gaps with a sum of 18 means the middle digit is 18/3=6. First digit a, last digit 12-a. Clue 5: last = 3 x first, so 12-a=3a, a=3, last 9. Digits: 3, 6, 9 (all different, increasing, gaps of 3). Code: **EV369**. (Checked by trying every letter and every digit combination: this is the only code fitting all five clues.)

**Q36** Subtract the place from each number. 19-1=18=R, 17-2=15=O, 22-3=19=S, 24-4=20=T, 10-5=5=E, 24-6=18=R. **ROSTER**.

**Q37** Rules: R1 region in N, S, E, W. R2 category in T, B, F. R3 size 28 to 46. R4 check digit = units digit of 3 x (sum of size digits).
- NT367: N ok, T ok, size 36 ok, check: (3+6) x 3=27, units 7, given 7. **Valid.**
- QT325: Q is not a region letter. Breaks **R1** (the size 32 and check digit 5 are fine: (3+2) x 3=15).
- EK367: K is not a category. Breaks **R2** (size 36 and check 7 are fine).
- WB505: size 50 is outside 28 to 46. Breaks **R3** (the check digit is fine: (5+0) x 3=15, units 5).
- NF395: size 39 is fine, check should be (3+9) x 3=36, units 6, but the code shows 5. Breaks **R4**.
Only **NT367** is valid.

**Q38** Sentences 1 and 2 share two words (grade, band) and two codes (ju, ki). Nothing in the three sentences separates them: grade and band appear together in exactly the same sentences. So "grade" is either ju or ki and **cannot be determined**. Check by trying all matchings: two different matchings fit (grade = ju, band = ki, or the other way round). For "cap": sentence 3 has ta, wo, re. The code ta is shared by sentences 1 and 3, so pay = ta; the code wo is shared by sentences 2 and 3, so bonus = wo. That leaves re for cap, so "cap" = **re**, which is certain in both matchings.

**Q39** (a) CLAIM has 5 letters, so +5. C(3)+5=8=H, L(12)+5=17=Q, A(1)+5=6=F, I(9)+5=14=N, M(13)+5=18=R. **HQFNR**.
(b) The coded word has 4 letters, so the plain word was shifted by 4. Go back 4. X(24)-4=20=T, I(9)-4=5=E, E(5)-4=1=A, Q(17)-4=13=M. **TEAM**.

**Q40** (a) First letters A and V. Mirrors: A(1) to Z(26); V(22) to 27-22=5=E. So ZE. Year 2021 gives 21. Finance is 3. Check: 2+1+3=6, units 6. ID: **ZE2136**.
(b) Rahul Singh: R(18) mirrors to 9=I; S(19) mirrors to 8=H. IH. Year 2019 gives 19. Sales is 2. Check: 1+9+2=12, units 2. Correct ID: **IH1922**. The sheet shows IH1923, whose check digit is 3, so it is **not correct**; it should be IH1922.
