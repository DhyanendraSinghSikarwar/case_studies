# Book 13 — Logical Reasoning & Analytical Thinking | Part 6: Deeper Blood Relations, Direction & Distance, Coding-Decoding, Input-Output and Machine Logic 🟡

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** multi-step blood relations and coded relations, direction and distance with turns and coordinates, letter, number, table and word coding-decoding, and input-output machine and process-tracing questions; fully specified problems with single answers plus method questions.

### Q1 ⭐⭐⭐ 🟢 Pointing to a photograph, Rohit says, "She is the daughter of the only son of my father's mother." How is the girl in the photograph related to Rohit?
**Asked at:** commonly asked (no company-specific report found); blood relations appear in prep-site topic lists for TCS NQT, Infosys, Cognizant and Mu Sigma (reported by prep sites, unverified).
**What the interviewer is checking:** Whether you can unpack a nested "of ... of ..." phrase from the inside out.
**Say this in the interview:** "My father's mother is my grandmother. Her only son must be my father. His daughter is my sister. So she is Rohit's sister."
**Answer:** **The girl is Rohit's sister.**
**Step-by-step reasoning:**
1. Innermost phrase: "my father's mother" is Rohit's paternal grandmother.
2. "The only son" of the grandmother: the grandmother's children include Rohit's father, and the word "only" says she has just one son. So that son is Rohit's father.
3. "Daughter of" Rohit's father is a girl with the same father as Rohit, so she is his sister (or half-sister; the question assumes full siblings, the normal convention).
```
Grandmother
   |
 Father ---- Rohit
   |
 Girl (photo)   -> sister
```
**Fast method (30 seconds):** Collapse the phrase: "only son of my father's mother" = "my father". Then "daughter of my father" = sister. The word "only" is what lets you collapse it.
**Check:** Reverse it: Rohit is a child of the girl's father, so Rohit is her sibling. Hand-checked.
**Explain simply:**
- "Only son" means exactly one son, so it points to one named person in the tree.
- The only son of your father's mother has to be your father, since he is one of her children.
- Children of the same father are siblings.
**Likely follow-ups:** 1) *What if the word "only" were removed?* Then the son could be Rohit's father or a paternal uncle, so the girl could be a sister or a cousin; the question would be unsolvable. 2) *Is Rohit male or female?* Not stated; the answer "sister" does not need it.
**Common mistakes / traps:** Answering "cousin" or "niece" by treating "the only son" as a different person from the father.

### Q2 ⭐⭐⭐ 🟢 Each of four brothers in a family has exactly one sister, and there are no other children. How many children does the family have?
**Asked at:** commonly asked (no company-specific report found); a classic "shared sister" puzzle.
**What the interviewer is checking:** Whether you notice that the same person can be counted for several people.
**Say this in the interview:** "Each brother has exactly one sister, and the sisters are shared, so there is one girl. Four boys plus one girl is five children."
**Answer:** **5 children (4 sons and 1 daughter).**
**Step-by-step reasoning:**
1. Let b be the number of boys and g the number of girls. Every brother's sisters are all the girls in the family, so each brother has g sisters.
2. "Exactly one sister" gives g = 1.
3. b = 4, so the total is 4 + 1 = 5.
**Fast method (30 seconds):** Siblings are shared. If every boy has one sister, it is the same girl for all of them. Do not multiply 4 by 1.
**Check:** Brute force over b and g from 0 to 7 found only b = 4, g = 1 meeting the clue (total 5), verified by script.
**Explain simply:**
- A brother's sisters are all the girls in the family, not private to him.
- So "each has exactly one sister" is a statement about the whole family: one girl.
**Likely follow-ups:** 1) *Each of 4 sisters has exactly 2 brothers?* Then 2 boys are shared by 4 girls: 6 children. 2) *Each of 3 brothers has 2 sisters?* 3 + 2 = 5 children.
**Common mistakes / traps:** Answering 8 (4 brothers + 4 sisters) by giving every boy his own sister.

### Q3 ⭐⭐⭐ 🟢 A group contains 2 mothers, 2 daughters and 1 grandmother. What is the minimum number of people in the group, and how do you show it?
**Asked at:** commonly asked (no company-specific report found); a classic "one person plays two roles" riddle.
**What the interviewer is checking:** Whether you see that one person can hold two relations at once (a middle generation is both mother and daughter).
**Say this in the interview:** "Three people: grandmother, her daughter, and that daughter's daughter. The middle woman is both a mother and a daughter, and the grandmother is also a mother."
**Answer:** **3 people (grandmother, mother, granddaughter).**
**Step-by-step reasoning:**
1. Call them G (oldest), M (middle), D (youngest). G is M's mother; M is D's mother.
2. Mothers: G and M, so there are 2 mothers.
3. Daughters: M (G's daughter) and D (M's daughter), so there are 2 daughters.
4. Grandmother: G, so there is 1 grandmother.
5. Two people cannot work: the two mothers would both need a child, but with only two people at most one of them can be a parent of the other.
```
G (grandmother, mother)
 |
M (mother, daughter)
 |
D (daughter)
```
**Fast method (30 seconds):** Count generations. A grandmother needs three generations, and three people in a line already supply every role.
**Check:** Brute force over all sex and mother assignments for 1 to 5 people found 3 is the smallest group that works (all female, a chain), verified by script. This reads "2 mothers, 2 daughters, 1 grandmother" as "at least these roles"; the usual reading.
**Explain simply:**
- A relation is a role, not a person: one woman can be a mother and a daughter at the same time.
- Minimum counts come from reusing people across roles.
**Likely follow-ups:** 1) *2 fathers, 2 sons and 1 grandfather?* Same logic: 3 men. 2) *3 mothers, 3 daughters?* A chain of 4 women (the oldest is a mother only, the youngest a daughter only).
**Common mistakes / traps:** Answering 5 by counting each role as a separate person.

### Q4 ⭐⭐⭐ 🟢 Why do blood-relation questions say "only son" or "only daughter", and how does that word change the answer to "the only son of my mother's mother" compared with "a son of my mother's mother"?
**Asked at:** commonly asked (no company-specific report found); a concept check on the wording of kinship questions.
**What the interviewer is checking:** Whether you understand that "only" makes a clue point to exactly one person, which is what allows a chain to continue.
**Say this in the interview:** "'Only' means exactly one, so the clue names one specific person. Both phrases give my maternal uncle, but with 'only' he is the single brother of my mother, so I can safely continue with 'his wife' or 'his son'."
**Answer:** **"Only" fixes the person to exactly one individual. In both phrases the person is a brother of my mother (a maternal uncle, mama), but "only son" says there is just one such uncle, while "a son" leaves it open that there are several.**
**Explain simply:**
- My mother's mother is my maternal grandmother. Her sons are my mother's brothers, so each is my maternal uncle.
- "The only son": she has one son, so the uncle is a single definite man. Any follow-on clue ("his wife", "his daughter") has one answer: aunt (mami) or cousin.
- "A son": she may have several sons, so a later clue could refer to different people. The relation name (uncle) is the same, but the question may become unanswerable.
- Worked contrast with numbers: in Q1, "only son of my father's mother" collapses to my father. Without "only", it could be my father or any of my father's brothers, so the answer could be sister or cousin.
**Likely follow-ups:** 1) *Is "only son of my mother's mother" ever me?* No: I am a son of my mother, not of my mother's mother. 2) *Does "only daughter of my father's father" always mean my father's sister?* Yes, given full siblings: she is my father's only sister, my paternal aunt (bua).
**Common mistakes / traps:** Treating "only" as decoration; also forgetting that the person pointed to by "only son of X's mother" is X's brother, not X.

### Q5 ⭐⭐⭐ 🟢 A courier starts at office O, goes 10 km north, turns right and goes 4 km, turns right again and goes 6 km, turns left and goes 8 km, and finally turns left and goes 5 km. How far is the courier now from O, and in which quadrant (north-east, north-west, south-east or south-west) of O is the courier?
**Asked at:** commonly asked (no company-specific report found); direction sense is on TCS, Infosys, Wipro, Cognizant and Accenture topic lists per prep sites (unverified).
**What the interviewer is checking:** Whether you track facing direction through left and right turns and then use Pythagoras on the net displacement.
**Say this in the interview:** "I track the facing direction at each turn and keep x for east-west and y for north-south. I end at 12 east and 9 north of the start, so the distance is 15 km, north-east."
**Answer:** **15 km from O, in the north-east quadrant (12 km east, 9 km north).**
**Step-by-step reasoning:**
1. Start (0, 0), facing north. x is east, y is north. Walk 10 north: (0, 10).
2. Turn right from north: facing east. 4 km: (4, 10).
3. Turn right from east: facing south. 6 km: (4, 4).
4. Turn left from south: facing east. 8 km: (12, 4).
5. Turn left from east: facing north. 5 km: (12, 9).
6. Distance = square root of (12 squared + 9 squared) = square root of 225 = 15.
**Fast method (30 seconds):** Add all north moves and subtract south moves (10 - 6 + 5 = 9); add east moves and subtract west moves (4 + 8 = 12). Then use the 3-4-5 triple scaled by 3: 9 and 12 give 15.
**Check:** Simulated move by move by script: final position (12, 9), distance 15.0.
**Explain simply:**
- Net displacement is the straight-line gap between start and end, not the path length (33 km walked).
- Left from facing south is east: turning left means counterclockwise, and south turned counterclockwise is east.
- 9, 12, 15 is a right triangle (a 3-4-5 triangle times 3).
**Likely follow-ups:** 1) *What is the total distance walked?* 10 + 4 + 6 + 8 + 5 = 33 km. 2) *If the last turn were right instead of left?* Facing south: (12, -1), distance sqrt(145), about 12.04 km, south-east.
**Common mistakes / traps:** Treating "left" as west regardless of facing direction; answering 33 km.

### Q6 ⭐⭐⭐ 🟢 A trekker walks 3 km north, then 4 km east, then 6 km south, then 4 km west. Where is the trekker now relative to the starting point (distance and direction)?
**Asked at:** commonly asked (no company-specific report found); standard direction-sense item.
**What the interviewer is checking:** Whether you net out opposite moves instead of adding all distances.
**Say this in the interview:** "East 4 and west 4 cancel. North 3 and south 6 leave 3 km south. So 3 km due south of the start."
**Answer:** **3 km due south of the starting point.**
**Step-by-step reasoning:**
1. East-west: +4 east, then 4 west: net 0.
2. North-south: +3 north, then 6 south: net -3, which is 3 km south.
3. With no east-west gap, the position is straight south, 3 km away.
```
start (0,0)
(0,3)--(4,3)
        |
(0,-3)--(4,-3)   end at (0,-3)
```
**Fast method (30 seconds):** Keep two running totals, one per axis. Opposite moves on the same axis subtract.
**Check:** Coordinates by script: (0,3), (4,3), (4,-3), (0,-3). End (0, -3), verified.
**Explain simply:**
- Only the net gap on each axis matters for "where is he now".
- If one net is zero, the answer is a pure compass direction, with no Pythagoras needed.
**Likely follow-ups:** 1) *Total distance walked?* 3 + 4 + 6 + 4 = 17 km. 2) *If the last leg were 3 km west?* Net (1, -3): sqrt(10), about 3.16 km, south-east.
**Common mistakes / traps:** Answering 17 km or 3 km south-west; there is no west component left.

### Q7 ⭐⭐⭐ 🟢 In a certain code, CAT is written as ECV. How is PAYSLIP written in that code? (Wrap around after Z.)
**Asked at:** commonly asked (no company-specific report found); letter-shift coding appears on the Mu Sigma logical-section topic list per a FACE Prep summary (not official) and TCS NQT lists.
**What the interviewer is checking:** Spotting a constant letter shift and handling the wrap-around at the end of the alphabet.
**Say this in the interview:** "C to E, A to C, T to V: each letter moves 2 forward. Apply +2 to PAYSLIP, with Y wrapping to A. Answer: RCAUNKR."
**Answer:** **RCAUNKR**
**Step-by-step reasoning:**
1. Test the rule: C(3) to E(5) is +2; A(1) to C(3) is +2; T(20) to V(22) is +2. All three fit, so the rule is a constant shift of +2.
2. Apply it: P to R, A to C, Y to A (Y is 25, +2 = 27, subtract 26 to get 1 = A), S to U, L to N, I to K, P to R.
3. Join: R C A U N K R.
**Fast method (30 seconds):** Write the shift above the first letter pair, confirm it on the other two, then move straight through the word. Wrap-around only matters for X, Y, Z.
**Check:** Shift applied by script to CAT gives ECV and to PAYSLIP gives RCAUNKR; every given letter fits.
**Explain simply:**
- "Wrap around" means after Z you go back to A, like a clock after 12.
- If a shift is constant, any one pair tells you the rule; the other pairs are confirmation.
**Likely follow-ups:** 1) *Decode ECV?* Shift each letter back 2: CAT. 2) *What if the rule were -1, +2, -1 repeating?* That would be a position-dependent shift; CAT to ECV does not fit it (C to E is +2, A to C is +2).
**Common mistakes / traps:** Writing Y + 2 as "[" instead of wrapping to A; shifting by 3 because of the count of letters.

### Q8 ⭐⭐⭐ 🟢 In a code, the alphabet is reversed (A = Z, B = Y, ...) and each letter is then shifted 2 places forward. How is ROW written?
**Asked at:** commonly asked (no company-specific report found); a two-step coding rule, common in prep-site practice sets (unverified).
**What the interviewer is checking:** Applying two rules in the stated order without mixing them.
**Say this in the interview:** "First reverse: R to I, O to L, W to D. Then shift each 2 forward: I to K, L to N, D to F. Answer: KNF."
**Answer:** **KNF**
**Step-by-step reasoning:**
1. Reverse step: a letter at position p becomes position 27 - p. R is 18, so 27 - 18 = 9 = I. O is 15, so 12 = L. W is 23, so 4 = D.
2. Shift step: I(9) + 2 = 11 = K; L(12) + 2 = 14 = N; D(4) + 2 = 6 = F.
3. Result: K N F.
**Fast method (30 seconds):** Pairs sum to 27 (A+Z = 1 + 26), so the mirror of a letter is 27 minus its position. Then add 2.
**Check:** Computed by script: reversal gives I, L, D; shift gives KNF.
**Explain simply:**
- Order matters: shifting first and then reversing gives a different word (shifting R, O, W forward gives T, Q, Y; reversing gives G, J, B).
- The mirror of position p is 27 - p because first and last positions add to 27.
**Likely follow-ups:** 1) *Shift first, then reverse: ROW?* GJB (hand-checked: T=20 mirror 7 = G, Q=17 mirror 10 = J, Y=25 mirror 2 = B). 2) *Decode KNF?* Shift back 2 to get I, L, D, then reverse to R, O, W.
**Common mistakes / traps:** Doing the steps in the wrong order, or shifting backward instead of forward.

### Q9 ⭐⭐⭐ 🟢 In a code, each letter is replaced by its mirror position in the alphabet (A = 26, B = 25, ..., Z = 1). How are the words SQL and DATA written as numbers?
**Asked at:** commonly asked (no company-specific report found); number-value coding, same family as Mu Sigma-style letter tests (prep-site summary, unverified).
**What the interviewer is checking:** Converting a letter to a reverse position using the 27 minus position rule.
**Say this in the interview:** "Code = 27 minus the normal position. S is 19, so 8; Q is 17, so 10; L is 12, so 15. SQL is 8 10 15. DATA is 23 26 7 26."
**Answer:** **SQL = 8, 10, 15; DATA = 23, 26, 7, 26.**
**Step-by-step reasoning:**
1. Check the rule from the given examples: A is position 1, code 26 = 27 - 1; B is 2, code 25 = 27 - 2; Z is 26, code 1 = 27 - 26.
2. SQL: S = 19 gives 8; Q = 17 gives 10; L = 12 gives 15.
3. DATA: D = 4 gives 23; A = 1 gives 26; T = 20 gives 7; A = 1 gives 26.
**Fast method (30 seconds):** Memorize "27 minus position". Repeated letters (the two A's in DATA) must give the same number: a built-in check.
**Check:** Computed by script: [8, 10, 15] and [23, 26, 7, 26].
**Explain simply:**
- A code is a lookup that always gives the same output for the same letter.
- The sum of a letter's position and its code is always 27.
**Likely follow-ups:** 1) *Decode 8 10 15?* 27 - 8 = 19 = S, and so on back to SQL. 2) *If the code were 26 minus position starting at A = 25?* Then add 1 less: SQL becomes 7, 9, 14.
**Common mistakes / traps:** Using 26 minus position (off by one) or mixing normal and mirror positions in one word.

### Q10 ⭐⭐⭐ 🟢 Letters A to Y are placed in a 5 x 5 table, row by row (row 1 is A B C D E, row 2 is F G H I J, row 3 is K L M N O, row 4 is P Q R S T, row 5 is U V W X Y). Each letter is coded as its row number followed by its column number (for example, B = 12). How is QUERY written in this code?
**Asked at:** commonly asked (no company-specific report found); table-coordinate coding appears in prep-site coding-decoding lists (unverified).
**What the interviewer is checking:** Reading a grid as row then column, in the order the question states.
**Say this in the interview:** "Row first, then column. Q is row 4, column 2, so 42. U is 51, E is 15, R is 43, Y is 55. QUERY is 42 51 15 43 55."
**Answer:** **42 51 15 43 55**
**Step-by-step reasoning:**
1. Row 4 is P Q R S T: Q is the 2nd, so 42; R is the 3rd, so 43.
2. Row 5 is U V W X Y: U is the 1st, so 51; Y is the 5th, so 55.
3. Row 1 is A B C D E: E is the 5th, so 15.
4. Join in order Q, U, E, R, Y: 42, 51, 15, 43, 55.
```
     c1 c2 c3 c4 c5
 r1   A  B  C  D  E
 r2   F  G  H  I  J
 r3   K  L  M  N  O
 r4   P  Q  R  S  T
 r5   U  V  W  X  Y
```
**Fast method (30 seconds):** Rewrite the grid once and read off each letter. Check the given example: B is row 1, column 2, so 12.
**Check:** Computed by script from letter index: [42, 51, 15, 43, 55].
**Explain simply:**
- Row-then-column is the same idea as a cell reference such as B3 in Excel, except the order is swapped (Excel gives column first).
- The grid has 25 cells, so J stays in and Z is left out.
**Likely follow-ups:** 1) *Decode 33 11 24?* 33 is row 3, column 3 = M; 11 = A; 24 is row 2, column 4 = I. The word is MAI. 2) *How would Z be coded?* It cannot; the table stops at Y.
**Common mistakes / traps:** Reading column first (giving 24 for Q); forgetting that the table skips Z.

### Q11 ⭐⭐⭐ 🟢 What are the main families of coding-decoding rules (constant shift, position-dependent shift, reversal, substitution, number value, language word-matching), and in what order do you test them on an unfamiliar question?
**Asked at:** commonly asked (no company-specific report found); coding-decoding is on TCS NQT, AMCAT, Infosys, Wipro and Mu Sigma topic lists per prep sites (unverified). The test order below is our suggestion, not a research finding.
**What the interviewer is checking:** Whether you have a systematic method rather than guessing.
**Say this in the interview:** "I compare letters one by one. First a constant shift, then a shift that changes with position, then reversal, then substitution by fixed symbols or numbers, and for word-matching I compare across sentences to find which code word belongs to which word."
**Answer:** **Six families; test the cheapest checks first (our suggested order: constant shift, then position-dependent shift, reversal, number value, substitution, language word-matching).**
**Explain simply:**
- Constant shift: every letter moves the same number of places (CAT to ECV is +2 each).
- Position-dependent shift: the shift changes by letter position (for example +1, +2, +3 along the word). Signal: the differences are not all equal but form a pattern.
- Reversal (mirror): A and Z swap, B and Y swap; position p becomes 27 - p. Signal: the sum of old and new positions is always 27.
- Number value: letters replaced by positions, by mirror positions, or by a table of coordinates. Signal: output is numbers.
- Substitution: a fixed dictionary (for example, each vowel replaced by a symbol). Signal: no arithmetic pattern; the mapping is read from examples.
- Language word-matching: invented words stand for real words; find the common code word between sentences that share one real word, then eliminate.
- Worked mini-example: CAT to ECV: differences +2, +2, +2, so constant shift. Test the same on DOG to FQI (+2, +2, +2); then apply to the new word.
**Likely follow-ups:** 1) *What if two rules combine (reverse then shift)?* Test reversal first with the sum-to-27 check; the leftover constant difference is the shift (as in Q8). 2) *How do you decode instead of encode?* Undo the steps in reverse order.
**Common mistakes / traps:** Assuming one pair proves the rule (use at least two letters); forgetting wrap-around; mixing the order of combined rules.

### Q12 ⭐⭐⭐ 🟡 Pointing to a woman, Ajay says, "She is the mother-in-law of my wife's brother's wife." How is the woman related to Ajay? Assume all siblings mentioned are full siblings.
**Asked at:** commonly asked (no company-specific report found); multi-step blood-relation chains appear in prep-site lists for TCS, Infosys and Cognizant (unverified).
**What the interviewer is checking:** Reading a chain from the inside out and noticing a "round trip" that lands back on a close relative.
**Say this in the interview:** "My wife's brother's wife: her mother-in-law is her husband's mother. Her husband is my wife's brother, so his mother is my wife's mother. That is my mother-in-law."
**Answer:** **She is Ajay's mother-in-law (his wife's mother).**
**Step-by-step reasoning:**
1. Innermost: Ajay's wife's brother is Ajay's brother-in-law. Call him B.
2. B's wife is the person whose mother-in-law we want.
3. A mother-in-law of B's wife is the mother of B's wife's husband, that is, the mother of B.
4. B is Ajay's wife's brother, and with full siblings, B's mother is also Ajay's wife's mother.
5. Ajay's wife's mother is Ajay's mother-in-law.
```
Woman ---- (husband)
   |
 Wife(Ajay's) ---- Ajay
   |
 B ---- B's wife
```
**Fast method (30 seconds):** "Mother-in-law of X's wife" always means X's mother (the husband's mother). X here is Ajay's wife's brother, whose mother is Ajay's wife's mother.
**Check:** Reverse: Ajay's mother-in-law is the mother of his wife, and that woman is also the mother of her son B, who is the husband of "B's wife". Consistent; hand-checked.
**Explain simply:**
- Your spouse's mother is your mother-in-law; your son's wife's mother is not.
- The mother-in-law of a woman is her husband's mother.
- "Full siblings" matters: with half-siblings, B's mother might not be Ajay's wife's mother.
**Likely follow-ups:** 1) *Who is Ajay's wife's brother's wife herself?* Ajay's sister-in-law. 2) *If the clue said "father-in-law of my wife's brother's wife"?* Then he is Ajay's father-in-law (wife's father).
**Common mistakes / traps:** Answering "mother" or "wife's grandmother"; treating the mother-in-law as belonging to Ajay's side.

### Q13 ⭐⭐⭐ 🟡 Pointing to a man, Anita says, "His mother's husband is my father's only brother." How is the man related to Anita?
**Asked at:** commonly asked (no company-specific report found); topic seen in prep-site blood-relation lists (unverified).
**What the interviewer is checking:** Turning "mother's husband" into "father" and following the clue to the cousin.
**Say this in the interview:** "His mother's husband is his father, and that man is my father's only brother, my uncle. So the man is my uncle's son, my cousin brother."
**Answer:** **The man is Anita's cousin (a male cousin, "cousin brother"), the son of her paternal uncle (chacha).**
**Step-by-step reasoning:**
1. "His mother's husband" is the man's father (standard reading: the mother's husband is the child's father).
2. This father is Anita's father's only brother, that is, Anita's paternal uncle.
3. So the man is the child of Anita's uncle: Anita's first cousin.
4. The pointing phrase says "a man", so he is male.
```
Anita's father ---- his only brother (= man's father)
      |                      |
    Anita                  Man   -> cousin
```
**Fast method (30 seconds):** "Mother's husband" = father. Then "my father's brother" = uncle. The man is that uncle's son.
**Check:** Reverse: Anita is the daughter of the man's father's brother, so Anita is his cousin. Hand-checked.
**Explain simply:**
- Assumption: the mother's husband is also the man's father (not a step-father). If he were a step-father, the man would be a step-cousin; blood-relation questions never intend this.
- A cousin is the child of a parent's sibling.
**Likely follow-ups:** 1) *If the clue read "his mother is my father's only sister"?* Then he is her cousin on the aunt's side (bua's son). 2) *Could the man be Anita's brother?* No: his father is her uncle, not her father.
**Common mistakes / traps:** Answering "uncle" because the clue names an uncle; the uncle is the man's father, not the man.

### Q14 ⭐⭐⭐ 🟡 Pointing to a boy, a woman says, "He is the son of the only daughter-in-law of my mother-in-law." How is the boy related to the woman?
**Asked at:** commonly asked (no company-specific report found); in-law chains are a standard blood-relation variant on prep-site lists (unverified).
**What the interviewer is checking:** Recognising that a clue can loop back to the speaker herself.
**Say this in the interview:** "My mother-in-law's daughter-in-law is a son's wife. 'Only' means there is exactly one, and I am one, so it is me. The boy is my son."
**Answer:** **The boy is the woman's own son.**
**Step-by-step reasoning:**
1. The woman's mother-in-law is her husband's mother.
2. The daughter-in-law of that mother-in-law is the wife of one of her sons.
3. The speaker herself is the wife of one of that lady's sons (her husband), so she is a daughter-in-law of her mother-in-law.
4. "Only daughter-in-law" says there is exactly one such woman. So the daughter-in-law is the speaker.
5. The boy is the son of the speaker: her son.
**Fast method (30 seconds):** Spot "my mother-in-law's only daughter-in-law": the only daughter-in-law of my husband's mother is me.
**Check:** Reverse: the speaker's mother-in-law has one daughter-in-law (the speaker), whose son is the boy: the speaker. Hand-checked.
**Explain simply:**
- "Daughter-in-law" means a son's wife.
- "Only" collapses the clue to one person, here the speaker.
**Likely follow-ups:** 1) *Without "only"?* The boy could be her son or a nephew (the child of her husband's brother's wife); the question would be ambiguous. 2) *What if the clue said "daughter of my mother-in-law's only daughter-in-law"?* Then the girl is her daughter.
**Common mistakes / traps:** Answering "nephew" or "cousin" because "my mother-in-law's daughter-in-law" sounds like someone else.

### Q15 ⭐⭐⭐ 🟡 Pointing to a lady, a man says, "She is the wife of the only son of my mother's mother." How is the lady related to the man? (Use the Indian-English kinship terms or describe the relation in words.)
**Asked at:** commonly asked (no company-specific report found); topic seen in prep-site blood-relation lists (unverified).
**What the interviewer is checking:** Collapsing "only son of my mother's mother" to a maternal uncle and then taking his wife.
**Say this in the interview:** "My mother's mother's only son is my mother's brother, my maternal uncle (mama). His wife is my maternal aunt, my mami. The lady is my aunt by marriage."
**Answer:** **The lady is the man's maternal aunt by marriage (his mother's brother's wife: mami).**
**Step-by-step reasoning:**
1. "My mother's mother" is the man's maternal grandmother.
2. Her only son is the brother of the man's mother, so he is the man's maternal uncle (mama). He cannot be the man's father, because the father is not a child of the maternal grandmother.
3. The lady is this uncle's wife, so she is the man's mami, the wife of his mother's brother.
```
Maternal grandmother
   |            |
 Mother      Her only son ---- Lady
   |
  Man
```
**Fast method (30 seconds):** Same pattern as Q1, but through the mother: "only son of my mother's mother" = "my mother's only brother". Then "his wife" = mami.
**Check:** Reverse: the man is the nephew (sister's son) of the lady's husband, so she is his aunt by marriage. Hand-checked.
**Explain simply:**
- An aunt by marriage is the wife of your uncle; she is not a blood relative.
- "Only" makes the uncle unique, so "his wife" has a single answer.
**Likely follow-ups:** 1) *What if the clue said "daughter of the only son of my mother's mother"?* Then she is the man's cousin (maternal uncle's daughter). 2) *Wife of the only son of my father's mother?* That is the man's mother.
**Common mistakes / traps:** Answering "mother" (confusing mother's side with father's side); calling her a blood aunt (maasi) when maasi is the mother's sister.

### Q16 ⭐⭐⭐ 🟡 In a family, each daughter has as many brothers as sisters, and each son has twice as many sisters as brothers. How many sons and how many daughters does the family have?
**Asked at:** commonly asked (no company-specific report found); a classic counting form of blood-relation items in prep-site lists (unverified).
**What the interviewer is checking:** Whether you remember that a person does not count themselves as their own brother or sister.
**Say this in the interview:** "Let sons be s and daughters be d. A daughter sees s brothers and d-1 sisters; a son sees d sisters and s-1 brothers. Two equations give 3 sons and 4 daughters."
**Answer:** **3 sons and 4 daughters (7 children).**
**Step-by-step reasoning:**
1. Let s = number of sons, d = number of daughters.
2. A daughter's brothers = s; her sisters = d - 1 (not herself). Clue 1: s = d - 1.
3. A son's sisters = d; his brothers = s - 1 (not himself). Clue 2: d = 2(s - 1).
4. Put s = d - 1 into clue 2: d = 2(d - 2) = 2d - 4, so d = 4 and s = 3.
5. It is unique: two straight-line equations in two unknowns with different slopes have one solution.
**Fast method (30 seconds):** Say "a daughter has one fewer sister than the girls in the family, a son has one fewer brother than the boys." Try small values: d = 4, s = 3 fits at once.
**Check:** Daughter: 3 brothers, 3 sisters (equal). Son: 4 sisters, 2 brothers (4 = 2 x 2). Also checked by script over all s, d from 1 to 29: only (3, 4) works.
**Explain simply:**
- "Brothers of X" means the other boys in the family; X is never counted as their own sibling.
- Girls and boys see different counts, so you need one equation for each.
**Likely follow-ups:** 1) *What if each son had three times as many sisters as brothers?* Then d = 3(s - 1) with d = s + 1 gives s = 2, d = 3 (hand-checked: son has 3 sisters and 1 brother). 2) *Why can the answer not be 0 sons?* Then a daughter would have 0 brothers, so she would need 0 sisters, meaning one daughter only; but then the second clue has no son to apply to. That is a degenerate case, not the intended family.
**Common mistakes / traps:** Counting the person themselves as a sibling, which gives d = s and nonsense; mixing up which group is "doubled".

### Q17 ⭐⭐⭐ 🟡 Six people are described: (i) Arun is the husband of Bela. (ii) Chetan is the son of Bela. (iii) Divya is the only sister of Chetan. (iv) Esha is the wife of Chetan. (v) Farah is the daughter of Esha and Chetan. How is Divya related to Farah?
**Asked at:** commonly asked (no company-specific report found); chain-style relation sets appear in prep-site lists for TCS, Infosys and Cognizant (unverified).
**What the interviewer is checking:** Ignoring distractors and finding the shared parent.
**Say this in the interview:** "Divya is Chetan's sister, and Chetan is Farah's father. So Divya is Farah's father's sister, her paternal aunt (bua)."
**Answer:** **Divya is Farah's paternal aunt (father's sister, "bua").**
**Step-by-step reasoning:**
1. Draw the tree: Arun + Bela are the parents; their children are Chetan and Divya (Divya is a sister of Chetan, so same parents).
2. Chetan + Esha are a couple; Farah is their daughter.
3. Farah's father is Chetan. Divya is Chetan's sister, so she is Farah's father's sister.
**Check:** Reverse: Farah is Divya's brother's daughter, i.e. Divya's niece. The two readings agree.
**Explain simply:**
- Your parent's sister is your aunt; on the father's side she is the paternal aunt (bua).
- Husband and wife clues (Arun, Esha) are bridges, not the answer.
**Likely follow-ups:** 1) *How is Arun related to Farah?* Paternal grandfather. 2) *How is Esha related to Divya?* Sister-in-law (brother's wife).
**Common mistakes / traps:** Calling Divya "maternal aunt" (that would be Esha's sister) or "sister"; wasting time on Arun.

### Q18 ⭐⭐⭐ 🟡 In a coded relation, A + B means A is the mother of B, A - B means A is the brother of B, A x B means A is the sister of B and A / B means A is the father of B. What does P / Q x R + S mean, i.e. how is P related to S?
**Asked at:** commonly asked (no company-specific report found); coded relations appear on prep-site lists (unverified).
**What the interviewer is checking:** Translating symbols to words and carrying gender through a chain.
**Say this in the interview:** "P is father of Q; Q is sister of R; R is mother of S. So R is also P's daughter, and S is P's grandchild: P is S's maternal grandfather."
**Answer:** **P is S's maternal grandfather (mother's father).**
**Step-by-step reasoning:**
1. P / Q: P is the father of Q (male).
2. Q x R: Q is the sister of R, so Q is female and R is Q's sibling; both are P's children.
3. R + S: R is the mother of S, so R is female, a daughter of P.
4. P is father of R, R is mother of S: P is S's mother's father.
**Fast method (30 seconds):** Write each pair as words under the symbols: P (father) Q (sister) R (mother) S. Link the first and last through the shared parent.
**Check:** Reverse: S is the child of R, and R is P's daughter, so S is P's daughter's child (a grandchild through the daughter). Gender of S is not given, so "grandchild".
**Explain simply:**
- Each symbol is a rule about the pair on either side of it, not about the chain as a whole.
- Siblings (Q, R) share parents, so what is true of P and Q is true of P and R.
**Likely follow-ups:** 1) *How is S related to P?* Daughter's child (grandchild; gender not given). 2) *Change R + S to R / S?* Then R is S's father, but R was Q's sister (female), so the chain is contradictory.
**Common mistakes / traps:** Answering "paternal grandfather" (forgetting R is a woman, so the link is through the mother); reading P and R as unrelated.

### Q19 ⭐⭐⭐ 🟡 In a coded relation, A + B means A is the mother of B, A - B means A is the brother of B, A x B means A is the sister of B and A / B means A is the father of B. How is M related to T in M x N / O - T?
**Asked at:** commonly asked (no company-specific report found); same coded-relation family as Q18 (prep-site lists, unverified).
**What the interviewer is checking:** Reading siblings through a parent link and not over-claiming gender.
**Say this in the interview:** "M is sister of N; N is father of O; O is brother of T. So O and T are N's children, and M is their father's sister: T's paternal aunt."
**Answer:** **M is T's paternal aunt (father's sister).**
**Step-by-step reasoning:**
1. M x N: M is the sister of N, so M is female and N is her sibling; N is male (next step shows he is a father).
2. N / O: N is the father of O.
3. O - T: O is the brother of T, so T is also N's child (siblings share parents).
4. M is the sister of T's father N, so she is T's paternal aunt. T's gender is not given.
**Check:** Reverse: T is M's brother's child, so T is M's niece or nephew. Consistent (gender of T unknown).
**Explain simply:**
- "A x B" says only that A is female and a sibling of B; "/" and "+" give the parent's gender.
- A parent's sister is an aunt.
**Likely follow-ups:** 1) *How is M related to O?* Paternal aunt too. 2) *Change O - T to O x T?* Same answer for M (T is still N's child).
**Common mistakes / traps:** Answering "mother" or "sister"; or "maternal aunt" (aunt on the mother's side) when she is the father's sister.

### Q20 ⭐⭐⭐ 🟡 In the coded relation A $ B means A is the mother of B, A # B means A is the sister of B and A @ B means A is the father of B. If X # Y $ Z @ W, how is X related to W?
**Asked at:** commonly asked (no company-specific report found); coded relations (prep-site lists, unverified).
**What the interviewer is checking:** Chaining three generations and naming a "grand" relation correctly.
**Say this in the interview:** "X is sister of Y; Y is mother of Z; Z is father of W. So Y is W's paternal grandmother, and X is her sister: W's paternal grandmother's sister, a grand-aunt."
**Answer:** **X is W's grand-aunt (father's mother's sister).**
**Step-by-step reasoning:**
1. X # Y: X is the sister of Y (X is female).
2. Y $ Z: Y is the mother of Z, so Y is female.
3. Z @ W: Z is the father of W.
4. Y is W's father's mother, W's paternal grandmother. X is Y's sister, so she is W's grandmother's sister, a grand-aunt (great-aunt).
**Check:** Reverse: W is the child of X's sister's son, i.e. X's grand-nephew or grand-niece. Consistent (W's gender not given).
**Explain simply:**
- A grand-aunt is a sister of one of your grandparents.
- Count generations: X's generation = Y's; Z is one below; W is two below.
**Likely follow-ups:** 1) *How is Y related to W?* Paternal grandmother. 2) *Change Z @ W to Z $ W?* Z is then W's mother, so W would then be a child of mother Z, so X would be W's maternal grandmother's sister, a maternal grand-aunt (hand-checked, assuming Y is still Z's mother and Z is female).
**Common mistakes / traps:** Answering "aunt" or "grandmother" (one generation off).

### Q21 ⭐⭐⭐ 🟡 A blood-relation question gives the clue "P is the cousin of Q" and asks for the gender of P. How do you decide whether a question has enough information, and what do you answer here?
**Asked at:** commonly asked (no company-specific report found); "data inadequate" blood-relation items are common in prep-site sets (unverified).
**What the interviewer is checking:** Whether you know which words fix gender and which leave it open.
**Say this in the interview:** "I check whether any word in the chain fixes gender: son, daughter, brother, sister, father, mother, husband, wife. 'Cousin' does not, so the answer is: cannot be determined."
**Answer:** **Cannot be determined (data inadequate).** A cousin can be a male or a female.
**Explain simply:**
- Gender-fixing words: son, daughter, brother, sister, father, mother, uncle, aunt, husband, wife, nephew, niece, grandfather, grandmother.
- Gender-neutral words: cousin, child, parent, sibling, spouse, friend, grandchild, in-law (alone), "person".
- Decision method: (1) name the person asked about; (2) walk the chain to that person; (3) if you reach a gender-fixing word for them, answer; if only a neutral word, say "cannot be determined".
- Worked mini-example: "P is the cousin of Q, and P is the sister of R." Now "sister" fixes P as female, so the answer is female.
**Likely follow-ups:** 1) *Is "spouse" enough?* No, unless the person is named husband or wife (or the other person's gender is given in a traditional-marriage setting, which exam questions usually do not assume). 2) *And "P is the father of Q's cousin"?* Father fixes P as male.
**Common mistakes / traps:** Guessing "male" from a name like Rahul; real exams say gender only through relation words, and the "cannot be determined" option is often the intended one.

### Q22 ⭐⭐⭐ 🟡 How do you decode a coded-relation question (symbols for mother, father, brother, sister): what is the step-by-step method, and how do you read a chain like A + B x C / D from left to right without losing the gender?
**Asked at:** commonly asked (no company-specific report found); symbol-decoding method on prep sites (unverified).
**What the interviewer is checking:** A repeatable method rather than guesswork.
**Say this in the interview:** "I write each symbol as a word, note the gender of the left person, then read each adjacent pair and keep a small tree. A pair's left letter gets the gender of its symbol."
**Answer:** **Method:** translate symbols, mark genders, read pairs left to right, join through shared parents.
**Explain simply:**
- Step 1: write the legend once (+ mother, - brother, x sister, / father in this book's style). The left letter of every pair has the gender the symbol shows.
- Step 2: rewrite the chain in words with arrows: A (mother) B (sister) C (father) D.
- Step 3: read each pair and note what it fixes: A is female, B is female, C is male; D is unknown.
- Step 4: sibling symbols (- and x) mean both people share parents, so link the parents of one to the other.
- Worked mini-example, A + B x C / D: A is mother of B; B is sister of C, so C is also A's child; C is father of D. So A is D's grandmother (A is C's mother, C is D's father, so paternal grandmother) and B is D's paternal aunt. No gender of D is claimed.
**Likely follow-ups:** 1) *How is C related to A in that chain?* C is A's child (son, because C is a father). 2) *Why can a symbol give only the left person's gender?* Because the symbol describes what the left person is to the right person, and says nothing about the right person.
**Common mistakes / traps:** Giving the right-hand person the gender (e.g. calling C "female" because of x); forgetting that siblings share parents; skipping the order of pairs.

### Q23 ⭐⭐⭐ 🟡 Asha starts at a point and walks 9 km west and then 12 km north. Bala starts at the same point, walks 3 km east and then 4 km south. How far apart are Asha and Bala now?
**Asked at:** commonly asked (no company-specific report found); direction-distance on TCS, Infosys, Wipro, Cognizant prep lists (unverified).
**What the interviewer is checking:** Coordinates and the Pythagoras formula.
**Say this in the interview:** "Put the start at (0,0). Asha is at (-9, 12), Bala at (3, -4). The gaps are 12 east-west and 16 north-south: 12-16-20, a 3-4-5 triangle times 4. So 20 km."
**Answer:** **20 km.**
**Step-by-step reasoning:**
1. Take east as +x, north as +y. Start (0,0).
2. Asha: 9 west gives (-9, 0), 12 north gives (-9, 12).
3. Bala: 3 east gives (3, 0), 4 south gives (3, -4).
4. East-west gap = 3 - (-9) = 12; north-south gap = 12 - (-4) = 16.
5. Distance = square root of (12^2 + 16^2) = square root of 400 = 20.
**Fast method (30 seconds):** Recognise 12 and 16 as 4 times (3, 4); the third side is 4 x 5 = 20. Pythagoras says the straight-line distance in a right angle is the square root of the two squares added.
**Check:** Computed by script: 20.0.
**Explain simply:**
- Opposite directions on the same line add (west 9 + east 3 = 12 gap); same-line moves in the same direction subtract.
- Pythagorean triples (3,4,5), (5,12,13), (7,24,25), (8,15,17) save time.
**Likely follow-ups:** 1) *If Bala had gone 3 west instead?* Gap 6 east-west, 16 north-south: square root of 292, about 17.09 km (hand-checked). 2) *Direction of Asha from Bala?* North-west.
**Common mistakes / traps:** Subtracting 9 and 3 (gap 6) or adding the two distances 12 + 4 = 16; the east-west gap must add because the two walks are on opposite sides of the start.

### Q24 ⭐⭐⭐ 🟡 Town P is 8 km due north of town Q, and town R is 6 km due east of Q. How far is R from P, and in which direction is R from P?
**Asked at:** commonly asked (no company-specific report found); direction-distance (prep-site lists, unverified).
**What the interviewer is checking:** Right-angled triangle plus naming the direction from the right reference point.
**Say this in the interview:** "Q is the corner of a right angle: P is 8 north, R is 6 east. PR is the hypotenuse, 10 km (6-8-10). From P, R is to the south-east."
**Answer:** **10 km, south-east of P.**
**Step-by-step reasoning:**
1. Q = (0,0), P = (0,8), R = (6,0).
2. Distance PR = square root of (6^2 + 8^2) = 10.
3. From P to R: x increases (east) and y decreases (south), so south-east. (Exactly, the bearing is about 36.9 degrees east of south; exam answers just say south-east.)
**Check:** Script gave 10.0; direction by coordinates (R is east and south of P).
**Explain simply:**
- "A from B" means stand at B and look at A; swap the order and the direction flips.
- From R, P would be north-west.
**Likely follow-ups:** 1) *Direction of P from R?* North-west. 2) *If R were 6 km west of Q?* Still 10 km, but R is south-west of P.
**Common mistakes / traps:** Giving the direction of P from R (north-west) instead of R from P.

### Q25 ⭐⭐⭐ 🟡 Point C is 24 km due north of point A, and point B is 7 km due east of A. How far is C from B, and in which direction is B from C?
**Asked at:** commonly asked (no company-specific report found); direction-distance (prep-site lists, unverified).
**What the interviewer is checking:** Recognising the 7-24-25 triple and reading direction in the right order.
**Say this in the interview:** "A is the corner. 7 east and 24 north give 25 km (the 7-24-25 triple). B is south-east of C."
**Answer:** **25 km; B is south-east of C.**
**Step-by-step reasoning:**
1. A = (0,0), C = (0,24), B = (7,0).
2. CB = square root of (7^2 + 24^2) = square root of 625 = 25.
3. From C to B: 7 east and 24 south, so B lies south-east of C.
**Check:** Script: 25.0.
**Explain simply:**
- 7, 24, 25 is a whole-number right triangle, like 3, 4, 5.
- A far-from-square direction is named by the two compass sides, here south then east, so south-east.
**Likely follow-ups:** 1) *Direction of C from B?* North-west. 2) *Distance if B were 10 km east and C 24 north?* Square root of 676 = 26 (5-12-13 times 2; verified by hand).
**Common mistakes / traps:** Saying "north-east" or "north-west" (C is north-west of B, which is the reverse question); mixing the order of the two points.

### Q26 ⭐⭐⭐ 🟡 Point P is 12 km due north of Q and R is due east of Q. If the distance PR is 13 km, how far is R from Q, and in which direction is P from R?
**Asked at:** commonly asked (no company-specific report found); direction-distance (prep-site lists, unverified).
**What the interviewer is checking:** Using Pythagoras backwards to find a leg.
**Say this in the interview:** "The hypotenuse is 13 and one leg is 12, so the other leg is 5 (the 5-12-13 triple). R is 5 km east of Q. P is north-west of R."
**Answer:** **5 km; P is north-west of R.**
**Step-by-step reasoning:**
1. Q = (0,0), P = (0,12), R = (x, 0) with x > 0 (due east).
2. x^2 + 12^2 = 13^2, so x^2 = 169 - 144 = 25, x = 5.
3. From R at (5,0) to P at (0,12): 5 west, 12 north, so P is north-west of R.
**Check:** Script found only r = 5 for positive r with r^2 + 144 = 169.
**Explain simply:**
- Leg = square root of (hypotenuse squared minus other leg squared).
- "Due east" fixes x as positive, so only one answer.
**Likely follow-ups:** 1) *If R were due west of Q?* Still 5 km, and P would be north-east of R. 2) *If PR were 15 and PQ 9?* QR = 12 (hand-checked: 81 + 144 = 225).
**Common mistakes / traps:** Adding 12 + 13 or 12 + 5; naming P as north-east of R.

### Q27 ⭐⭐⭐ 🟡 A rider leaves a warehouse W and goes 11 km north, then 24 km east, then 4 km south, and then returns to W in a straight line. What is the total distance travelled?
**Asked at:** commonly asked (no company-specific report found); delivery-route direction items (prep-site lists, unverified).
**What the interviewer is checking:** Net displacement before applying Pythagoras, and adding all legs for total distance.
**Say this in the interview:** "Net position: 24 east, 11 - 4 = 7 north. The straight return is the square root of (24^2 + 7^2) = 25. Total travelled is 11 + 24 + 4 + 25 = 64 km."
**Answer:** **64 km.**
**Step-by-step reasoning:**
1. W = (0,0). After 11 north: (0,11). After 24 east: (24,11). After 4 south: (24,7).
2. Return leg from (24,7) to (0,0): square root of (24^2 + 7^2) = 25 km.
3. Total distance = 11 + 24 + 4 + 25 = 64 km (distance counts every leg; displacement would be 0 because the rider ends at W).
**Check:** Script: 64.0.
**Explain simply:**
- Distance travelled adds the length of every leg; displacement is the straight line start-to-end.
- The 7-24-25 triple appears again here.
**Likely follow-ups:** 1) *Displacement before the return?* 25 km (to the point 24 east, 7 north). 2) *If the third leg were 6 south?* Net 5 north, return = 24.52 km (square root of 601), total 65.52 km (hand-checked).
**Common mistakes / traps:** Giving 25 km (only the return) or 39 km (the three legs without the return); subtracting 4 from the total instead of from the north position.

### Q28 ⭐⭐⭐ 🟡 Two cars leave the same junction at the same time. Car A drives north at 40 km/h and car B drives east at 30 km/h. How far apart are they after 90 minutes, assuming they keep driving at those speeds in straight lines?
**Asked at:** commonly asked (no company-specific report found); speed plus direction items (prep-site lists, unverified).
**What the interviewer is checking:** Converting minutes to hours before multiplying.
**Say this in the interview:** "90 minutes is 1.5 hours. A goes 60 km north, B goes 45 km east. 45-60-75 is 15 times (3, 4, 5). Answer 75 km."
**Answer:** **75 km.**
**Step-by-step reasoning:**
1. 90 minutes = 1.5 hours.
2. Distances: A = 40 x 1.5 = 60 km north; B = 30 x 1.5 = 45 km east.
3. They are at right angles, so gap = square root of (60^2 + 45^2) = square root of 5625 = 75 km.
**Fast method (30 seconds):** Speeds 40 and 30 are 10 x (4, 3), so the closing speed apart is 10 x 5 = 50 km/h; in 1.5 hours that is 75 km.
**Check:** Script: 75.0.
**Explain simply:**
- Perpendicular directions form a right angle, so Pythagoras applies.
- The gap grows at a steady 50 km/h, so you can scale by time.
**Likely follow-ups:** 1) *After 2 hours?* 100 km. 2) *If B drove west instead?* Still 75 km (hand-checked; the angle is still 90 degrees).
**Common mistakes / traps:** Using 90 hours or 0.9 hours; adding 60 + 45 = 105.

### Q29 ⭐⭐⭐ 🟡 Kiran faces south-west. He turns 135 degrees anticlockwise, then 90 degrees clockwise, and then 90 degrees clockwise again. In which direction is he facing now?
**Asked at:** commonly asked (no company-specific report found); turning-angle items in direction-sense sets (prep-site lists, unverified).
**What the interviewer is checking:** Working in degrees with clockwise as the positive direction.
**Say this in the interview:** "Measure compass bearings clockwise from north: south-west is 225. Anticlockwise 135 gives 90 (east). Clockwise 90 gives 180 (south). Clockwise 90 gives 270 (west). West."
**Answer:** **West.**
**Step-by-step reasoning:**
1. Compass angles: N = 0, E = 90, S = 180, W = 270, SW = 225.
2. 225 - 135 = 90, which is east.
3. 90 + 90 = 180, south.
4. 180 + 90 = 270, west.
**Fast method (30 seconds):** Net turn = -135 + 90 + 90 = +45 degrees clockwise. From south-west (225), 225 + 45 = 270 = west. Adding all the turns first is quicker and avoids mistakes.
**Check:** Script: final heading 270 (west).
**Explain simply:**
- Clockwise adds, anticlockwise subtracts; wrap around at 360 (so 360 = 0, north).
- Anticlockwise 135 from south-west passes south, south-east and ends at east.
**Likely follow-ups:** 1) *If the first turn were clockwise 135?* 225 + 135 = 360 = north; +90 = east; +90 = south. Final heading south (hand-checked). 2) *Net turn when facing the same way again?* A multiple of 360.
**Common mistakes / traps:** Treating anticlockwise as clockwise; forgetting that 135 is not a quarter turn.

### Q30 ⭐⭐⭐ 🟡 A drone faces north and makes this sequence of 90-degree turns: right, left, left, right, right, right, left. Which direction does it face at the end?
**Asked at:** commonly asked (no company-specific report found); turn-sequence items (prep-site lists, unverified).
**What the interviewer is checking:** Turning a long list of left and right turns into one net number.
**Say this in the interview:** "Right is +1 quarter turn and left is -1. Sum: +1 -1 -1 +1 +1 +1 -1 = +1. One net right turn from north is east."
**Answer:** **East.**
**Step-by-step reasoning:**
1. Heading after each turn (R = clockwise): R gives east, L gives north, L gives west, R gives north, R gives east, R gives south, L gives east.
2. Final heading: east.
**Fast method (30 seconds):** Count rights (4) minus lefts (3) = 1 net right turn. Net quarter turns mod 4: 1 = east (0 = north, 1 = east, 2 = south, 3 = west).
**Check:** Script: final heading 90 degrees (east), matching the step list.
**Explain simply:**
- A right turn cancels a left turn.
- Only the net count mod 4 matters, because four quarter turns bring you back to the start.
**Likely follow-ups:** 1) *What if the last turn were right instead of left?* Rights 5, lefts 2: net 3, west... check: 5 - 2 = 3, so west (hand-checked). 2) *What if there were 4 rights and 4 lefts?* Net 0, so still north.
**Common mistakes / traps:** Treating left and right as fixed compass sides; they are always relative to the drone's current heading, which the net-count trick respects.

### Q31 ⭐⭐⭐ 🟡 How do you solve a direction-and-distance question reliably: how do you set up coordinates, how do you handle left and right turns relative to the current heading, and what is the most common error?
**Asked at:** commonly asked (no company-specific report found); direction and distance appear in prep-site topic lists for TCS NQT, Cognizant and others (prep-site claim, unverified).
**What the interviewer is checking:** Whether you track a changing heading step by step instead of guessing from a mental picture.
**Say this in the interview:** "I put the start at (0, 0) with north as up and east as right. I keep a 'facing' note, and each turn changes that note: a right turn moves it clockwise, a left turn anticlockwise. Then I add up the east-west and north-south moves and use Pythagoras for the straight-line distance."
**Answer:** **Fix a grid (north = +y, east = +x), track the current facing, update it at every turn relative to that facing, add the moves to get the final (x, y), then find distance = sqrt(x squared + y squared) and the quadrant from the signs.**
**Explain simply:**
- Turns are relative to where you face now, not to the map. Facing north, right = east. Facing east, right = south. Facing south, right = west. Facing west, right = north (the clockwise cycle N, E, S, W). Left is the same cycle backwards.
- The final distance is the straight-line gap (displacement), not the length walked.
- A 3-4-5, 5-12-13, 8-15-17 or 9-12-15 pair of legs gives a whole-number distance, a quick sanity signal.
**Worked mini-example (verified by script):** Go 10 north, turn right 4, right 6, left 8, left 5. Facing: N (0,10); right is E, so (4,10); right again is S, so (4,4); left from S is E, so (12,4); left from E is N, so (12,9). Distance = sqrt(144 + 81) = **15 km**, north-east of the start.
**Likely follow-ups:** 1) *What if every left and right were swapped?* The path is mirrored: the end is (-12, 9), still 15 km away but north-west (checked by script). 2) *Does the distance depend on how far was walked in total?* No, only on the end point; total walked here is 33 km.
**Common mistakes / traps:** Treating "right" as always east (it depends on the current heading), and reporting the total path length instead of the straight-line distance. Also forgetting that a 180-degree turn is two turns.

### Q32 ⭐⭐⭐ 🟡 In a certain code, REPORT is written as SGSSWZ. How is ANALYSIS written in that code?
**Asked at:** commonly asked (no company-specific report found); letter-shift coding appears on TCS NQT, Infosys, Wipro and Mu Sigma prep-site topic lists (unverified).
**What the interviewer is checking:** Spotting a position-dependent letter shift.
**Say this in the interview:** "Each letter moves forward by its own position number: first letter by 1, second by 2, and so on. REPORT checks out. Applying it to ANALYSIS gives BPDPDYPA."
**Answer:** **BPDPDYPA**
**Step-by-step reasoning:**
1. Compare REPORT with SGSSWZ letter by letter: R to S is +1, E to G is +2, P to S is +3, O to S is +4, R to W is +5, T to Z is +6. The shift equals the position number.
2. Apply to ANALYSIS (8 letters, shifts +1 to +8): A+1 = B; N+2 = P; A+3 = D; L+4 = P; Y+5 = 25+5 = 30, subtract 26 to wrap round = D; S+6 = Y; I+7 = P; S+8 = 27, wrap to A.
3. Result: B P D P D Y P A.
**Fast method (30 seconds):** Write the alphabet numbers under each letter, subtract (code minus original) and look at the differences; if they read 1, 2, 3 ... you are done. Wrap rule: if the number goes above 26, subtract 26.
**Check:** Verified by script (the same rule reproduces SGSSWZ and gives BPDPDYPA).
**Explain simply:**
- A "shift" means moving along the alphabet by a fixed number of places; Z followed by A is the wrap-around.
- Here the shift grows by 1 each position, so the same letter (the two S's in ANALYSIS, or the two A's) becomes different letters.
**Likely follow-ups:** 1) *Code for DATA?* ECWE (D+1, A+2, T+3, A+4; checked by script). 2) *Why can't the shift be a single fixed number?* In REPORT the two R's became S and W, so the shift depends on position.
**Common mistakes / traps:** Forgetting to wrap after Z (Y+5 is D, not a symbol), and counting positions from 0.

### Q33 ⭐⭐⭐ 🟡 In a certain code, FRIEND is written as HUMJTK. How is CANDLE written in that code?
**Asked at:** commonly asked (no company-specific report found); letter-shift coding is on TCS NQT, AMCAT, Infosys and Wipro prep-site lists (unverified).
**What the interviewer is checking:** Detecting a shift that starts at +2 and grows.
**Say this in the interview:** "The shifts are +2, +3, +4, +5, +6, +7 for the six letters. CANDLE becomes EDRIRL."
**Answer:** **EDRIRL**
**Step-by-step reasoning:**
1. F to H is +2; R to U is +3; I to M is +4; E to J is +5; N to T is +6; D to K is +7.
2. The shift starts at 2 and rises by 1 each place.
3. CANDLE: C+2 = E; A+3 = D; N+4 = R; D+5 = I; L+6 = R; E+7 = L.
**Fast method (30 seconds):** Compute only the first two differences. If they are +2 and +3, test the "rising by 1" idea on the third letter before doing the rest.
**Check:** Verified by script (the rule reproduces HUMJTK and gives EDRIRL).
**Explain simply:**
- Look for the pattern in the differences, not in the letters themselves.
- This is a "position + 1" shift: position number plus a constant 1.
**Likely follow-ups:** 1) *What is XYZ under the same rule?* X+2 = Z, Y+3 = B (wrap), Z+4 = D, so ZBD (checked by script). 2) *What if the rule were position + 2?* Then the first shift would be +3, which does not fit FRIEND.
**Common mistakes / traps:** Reusing the Q32 rule (shift = position), which would turn F into G instead of H.

### Q34 ⭐⭐⭐ 🟡 In a certain code, SALARY is written as TZMZSX. How is BONUS written in that code?
**Asked at:** commonly asked (no company-specific report found); alternating-shift coding is a standard variant on prep-site lists (unverified).
**What the interviewer is checking:** Seeing an alternating forward and backward shift.
**Say this in the interview:** "Odd-numbered letters go one forward and even-numbered letters go one back. BONUS becomes CNOTT."
**Answer:** **CNOTT**
**Step-by-step reasoning:**
1. S to T is +1 (1st letter), A to Z is -1 (2nd), L to M is +1 (3rd), A to Z is -1 (4th), R to S is +1 (5th), Y to X is -1 (6th).
2. So odd positions shift +1, even positions shift -1.
3. BONUS: B+1 = C; O-1 = N; N+1 = O; U-1 = T; S+1 = T.
**Fast method (30 seconds):** Look at the repeated letter. The two A's in SALARY (2nd and 4th places, both even) both became Z, which hints that the rule depends on odd or even place, not on the exact position number.
**Check:** Verified by script (rule reproduces TZMZSX; BONUS gives CNOTT).
**Explain simply:**
- Parity means odd or even; the rule depends only on whether the position is odd or even.
- Going "one back" from A would wrap to Z; no wrap was needed here.
**Likely follow-ups:** 1) *If the rule started with a backward shift instead?* BONUS would become APMVR (checked by script). 2) *Is there a second rule that fits SALARY?* Not a simple one; the +1/-1 alternation fits all six letters.
**Common mistakes / traps:** Applying the shift to every letter in the same direction, or counting even positions as odd.

### Q35 ⭐⭐⭐ 🟡 Using the rule in which SALARY is written as TZMZSX (odd-numbered letters shifted 1 forward, even-numbered letters shifted 1 back), which word is written as EZUZTDU?
**Asked at:** commonly asked (no company-specific report found); reverse (decoding) versions of coding items are common on prep-site lists (unverified).
**What the interviewer is checking:** Whether you can run a rule backwards.
**Say this in the interview:** "To decode, I undo each shift: odd positions go one back, even positions go one forward. EZUZTDU decodes to DATASET."
**Answer:** **DATASET**
**Step-by-step reasoning:**
1. Encoding did +1 at odd places and -1 at even places, so decoding does -1 at odd places and +1 at even places.
2. E (1st) -1 = D; Z (2nd) +1 = A (wrap past Z); U (3rd) -1 = T; Z (4th) +1 = A; T (5th) -1 = S; D (6th) +1 = E; U (7th) -1 = T.
3. D A T A S E T reads DATASET, a real word, which supports the decoding.
**Fast method (30 seconds):** Decode the first three letters; if a real word starts to appear, trust the rule and finish.
**Check:** Verified by script: encoding DATASET with the rule gives EZUZTDU. Decoding is one-to-one (each coded letter comes from exactly one original letter), so the answer is unique.
**Explain simply:**
- To reverse a rule, apply the opposite operation at each step.
- Z+1 wraps to A, because the alphabet is treated as a circle.
**Likely follow-ups:** 1) *Code for PAYROLL?* QZZQPKM (checked by script). 2) *What if only the word was given with no rule?* You would compare letter pairs, as in Q34.
**Common mistakes / traps:** Applying the encoding rule again instead of its opposite (the result would not be a real word, a quick warning sign).

### Q36 ⭐⭐⭐ 🟡 In a code language, "tax rule filed" is written "ka mo zi", "rule filed late" is written "zi mo bu" and "late tax audit" is written "ka bu pe". What is the code for "audit"?
**Asked at:** commonly asked (no company-specific report found); word-coding from overlapping sentences is on TCS NQT and AMCAT prep-site lists (unverified).
**What the interviewer is checking:** Using common words across sentences to isolate one word.
**Say this in the interview:** "Tax is in sentences 1 and 3, and the only code shared by those is ka, so tax is ka. Late is in sentences 2 and 3 and the shared code is bu. Sentence 3 has ka bu pe, so audit is pe."
**Answer:** **pe**
**Step-by-step reasoning:**
1. Common word tax (sentences 1 and 3) and common code ka (codes 1 and 3): tax = ka.
2. Common word late (sentences 2 and 3) and common code bu (codes 2 and 3): late = bu.
3. In "late tax audit" = "ka bu pe", the remaining code is pe, so audit = pe.
4. For rule and filed, mo and zi appear in both sentences 1 and 2, so we cannot say which is which. We are not asked, and it does not change audit.
**Fast method (30 seconds):** Look for a code that appears in only one sentence: pe appears only in sentence 3, and audit is the only word appearing only in sentence 3. They must match.
**Check:** Brute force over all 120 assignments of 5 codes to 5 words: exactly 2 fit (rule and filed can swap mo and zi), and audit = pe in both.
**Explain simply:**
- A word that appears in two sentences must have a code that appears in both coded sentences.
- A word and code that appear in only one sentence pair up by elimination.
**Likely follow-ups:** 1) *Can we find the code for "rule"?* No, it is ambiguous (mo or zi). 2) *What would add a sentence to fix that?* One that has rule without filed.
**Common mistakes / traps:** Assuming codes appear in the same order as the words (they usually do not), or claiming a code for rule or filed when the data cannot separate them.

### Q37 ⭐⭐⭐ 🟡 In a code language, "sales up today" is written "pa ni su", "today report due" is written "su ro ve" and "due sales call" is written "ve pa ti". What is the code for "report"?
**Asked at:** commonly asked (no company-specific report found); same overlapping-sentence format as other word-coding prep items (unverified).
**What the interviewer is checking:** Finding common words and eliminating step by step.
**Say this in the interview:** "Today is in sentences 1 and 2, the shared code is su. Due is in sentences 2 and 3, shared code ve. So in sentence 2, 'su ro ve', the leftover ro must be report."
**Answer:** **ro**
**Step-by-step reasoning:**
1. today appears in sentences 1 and 2; the only common code is su, so today = su.
2. due appears in sentences 2 and 3; the common code is ve, so due = ve.
3. Sentence 2 is "today report due" = "su ro ve". Remove su (today) and ve (due); report = ro.
4. For completeness: sales (sentences 1 and 3) = pa, so up = ni and call = ti. All six words are fixed.
**Fast method (30 seconds):** Only sentence 2 has "report" and only code string 2 has "ro". A word and a code that each occur once pair up.
**Check:** Brute force over all 720 assignments of 6 codes to 6 words: exactly 1 fits, and report = ro.
**Explain simply:**
- Overlap between sentences is what gives the information; each shared word narrows the codes.
- Here every word is fully determined, which does not always happen (see Q36).
**Likely follow-ups:** 1) *Code for "call"?* ti. 2) *Code for "up"?* ni.
**Common mistakes / traps:** Matching words and codes in written order (report is the 2nd word and ro the 2nd code only by luck here).

### Q38 ⭐⭐⭐ 🟡 A code works as follows: the letters of the word are first reversed, then every vowel (A, E, I, O, U) is replaced by the next letter in the alphabet. How is DATABASE written in this code?
**Asked at:** commonly asked (no company-specific report found); multi-step letter coding is a common variant in prep-site lists (unverified).
**What the interviewer is checking:** Applying a two-step rule in the stated order.
**Say this in the interview:** "Reverse DATABASE to ESABATAD, then change each vowel to the next letter: A to B and E to F. The result is FSBBBTBD."
**Answer:** **FSBBBTBD**
**Step-by-step reasoning:**
1. Reverse DATABASE: E S A B A T A D.
2. Vowels are E, A, A, A (positions 1, 3, 5, 7). Next letters: E to F, A to B.
3. Consonants S, B, T, D stay the same.
4. Result: F S B B B T B D.
**Fast method (30 seconds):** Here the two steps commute: replacing vowels first and then reversing gives the same string, since the vowel replacement looks at each letter alone, not its position.
**Check:** Verified by script.
**Explain simply:**
- Vowels are A, E, I, O, U; everything else is a consonant.
- Order of steps matters only when a step depends on position (as in shifts by place number).
**Likely follow-ups:** 1) *Does the answer change if you replace vowels first and then reverse?* No, same output. 2) *What if "next letter" for U?* V.
**Common mistakes / traps:** Replacing vowels but forgetting to reverse (the reverse step matters for the order of letters), or changing consonants too.

### Q39 ⭐⭐⭐ 🟡 In a code, the value of a word equals the sum of the alphabet positions of its consonants minus the sum of the alphabet positions of its vowels (A = 1, ..., Z = 26; treat Y as a consonant). What is the value of ANALYTICS?
**Asked at:** commonly asked (no company-specific report found); number-value coding appears in prep-site lists (unverified).
**What the interviewer is checking:** Careful arithmetic with a clear classification of letters.
**Say this in the interview:** "Vowels A, A, I sum to 11. Consonants N, L, Y, T, C, S sum to 93. The value is 93 minus 11, which is 82."
**Answer:** **82**
**Step-by-step reasoning:**
1. Letters: A N A L Y T I C S.
2. Vowels: A = 1, A = 1, I = 9; total 11.
3. Consonants: N = 14, L = 12, Y = 25, T = 20, C = 3, S = 19; total 93.
4. Value = 93 - 11 = 82.
**Fast method (30 seconds):** Compute the vowel total first (small), then the consonant total. Check by adding all letters (93 + 11 = 104) and confirming 104 as the full sum of positions.
**Check:** Verified by script: 82; the full-word sum is 104.
**Explain simply:**
- The question tells you to treat Y as a consonant, so Y is added (25), not subtracted.
- The word-value is "consonants minus vowels", not the other way round.
**Likely follow-ups:** 1) *Value of BONUS?* Consonants B 2 + N 14 + S 19 = 35; vowels O 15 + U 21 = 36; value = -1 (checked by script). 2) *If Y were a vowel?* ANALYTICS would be (93 - 25) - (11 + 25) = 32 (checked by hand).
**Common mistakes / traps:** Counting Y as a vowel, or subtracting in the wrong order and answering -82.

### Q40 ⭐⭐⭐ 🟡 In a code, + means x, x means -, - means / and / means +. What is the value of 12 / 6 - 3 + 4 x 2?
**Asked at:** commonly asked (no company-specific report found); symbol-substitution arithmetic is a standard prep-site format (unverified).
**What the interviewer is checking:** Substituting symbols correctly before applying BODMAS.
**Say this in the interview:** "I swap the symbols first: / becomes +, - becomes /, + becomes x, x becomes -. The sum is 12 + 6 / 3 x 4 - 2, which is 18."
**Answer:** **18**
**Step-by-step reasoning:**
1. Replace each symbol using the code: 12 / 6 - 3 + 4 x 2 becomes 12 + 6 / 3 x 4 - 2.
2. Use BODMAS (the usual order: brackets, orders, division and multiplication left to right, then addition and subtraction): 6 / 3 = 2, then 2 x 4 = 8.
3. Now 12 + 8 - 2 = 18.
**Fast method (30 seconds):** Rewrite the whole line with true symbols before calculating anything; mixing the two meanings is how errors happen.
**Check:** Verified by script: 18.
**Explain simply:**
- BODMAS means do multiplication and division before addition and subtraction.
- The code changes only what the signs mean, not the order rules.
**Likely follow-ups:** 1) *What is 20 / 4 - 2 + 3 x 1?* 20 + 4 / 2 x 3 - 1 = 25 (checked by script). 2) *What if you calculated strictly left to right?* You would get a different number, so always apply BODMAS.
**Common mistakes / traps:** Calculating with the original signs (the ordinary value of 12 / 6 - 3 + 4 x 2 is 7, not 18), or swapping only some of the four symbols.

### Q41 ⭐⭐⭐ 🟡 Why does a word-coding question sometimes give two or three different sentences with overlapping words, and how do you find the code of one word from them without trying every combination?
**Asked at:** commonly asked (no company-specific report found); overlapping-sentence word coding is on TCS NQT, AMCAT and Infosys prep-site lists (unverified).
**What the interviewer is checking:** Whether you reason with common elements instead of guessing.
**Say this in the interview:** "The overlap is the information. A word that appears in two sentences must have a code that appears in both coded sentences, so I find the shared word, find the shared code, and match them. Then I use elimination for the rest."
**Answer:** **Find a word common to two sentences and the one code common to the same two coded sentences; they match. Remove matched pairs and repeat. A word and a code that each appear only once pair up by elimination.**
**Explain simply:**
- One sentence alone gives only a set of words and a set of codes, with no order (the codes do not follow the word order). Overlaps break that deadlock.
- Each shared word narrows its code to the single code shared between the two coded sentences.
- Sometimes two words always appear together (like rule and filed in Q36); then they cannot be separated, which is fine if the question does not ask for them.
**Worked mini-example (hand-checked):** "red car fast" = "ab cd ef", "fast car blue" = "ef cd gh". Common word car and fast; common codes cd and ef: ambiguous between the two, but red (only in sentence 1) = ab and blue (only in sentence 2) = gh pair by elimination. In Q37, "today" is in two sentences and su is the shared code, so today = su immediately.
**Likely follow-ups:** 1) *Can you always decode every word?* No; two words that always appear together stay ambiguous (Q36 gives 2 valid assignments, but audit is the same in both). 2) *How do you check?* Rebuild each sentence with your codes and compare as sets.
**Common mistakes / traps:** Matching by position, and over-claiming a code that the data cannot fix.

### Q42 ⭐⭐⭐ 🟡 Meena's father's father has only one son. How is that son's wife's mother related to Meena?
**Asked at:** commonly asked (no company-specific report found); the "only son" trick is a common blood-relation format (prep-site, unverified).
**What the interviewer is checking:** Whether you use the word "only" to identify a person already named.
**Say this in the interview:** "Meena's father's father is her paternal grandfather. His only son must be Meena's father. His wife is Meena's mother, and her mother is Meena's maternal grandmother."
**Answer:** **Meena's maternal grandmother (nani, her mother's mother).**
**Step-by-step reasoning:**
1. Meena's father's father = paternal grandfather.
2. He has only one son, and Meena's father is his son, so the son is Meena's father.
3. The son's wife = Meena's mother (assuming a standard marriage and no step-relations).
4. Mother's mother = maternal grandmother.
**Fast method (30 seconds):** When the chain turns back on itself ("grandfather's only son"), it returns to the parent: collapse that part first.
**Check:** Hand-checked (family tree).
**Explain simply:**
- "Only son" means there is exactly one, so it cannot be an uncle.
- If it said "a son" instead of "only son", it could be Meena's uncle and the answer would be different (her aunt's mother).
**Likely follow-ups:** 1) *What if the question said "a son of Meena's father's father"?* Then we do not know whether he is her father or an uncle; the question would not have a single answer. 2) *Meena's father's father's only son's mother?* Meena's paternal grandmother.
**Common mistakes / traps:** Treating the "only son" as a different person (uncle) and answering "great-grandmother" or "aunt's mother".

### Q43 ⭐⭐⭐ 🔴 A family has three generations. Anil and Bharti are husband and wife. Chitra is the daughter of Anil and Bharti. Dev is the husband of Chitra. Esha is the daughter of Dev and Chitra. Farid is the brother of Bharti. How is Farid related to Esha?
**Asked at:** commonly asked (no company-specific report found); family-tree blood-relation questions are on TCS, Infosys and Accenture prep-site lists (unverified).
**What the interviewer is checking:** Drawing a tree and counting generations to name a grand-uncle correctly.
**Say this in the interview:** "Bharti is Esha's mother's mother, so Esha's maternal grandmother. Farid is Bharti's brother, so he is Esha's maternal grandmother's brother, her maternal great-uncle."
**Answer:** **Farid is Esha's maternal great-uncle (her mother's mother's brother).**
**Step-by-step reasoning:**
1. Tree: Anil + Bharti (top generation) have daughter Chitra, who with husband Dev has daughter Esha (bottom generation).
2. Chitra is Esha's mother; Bharti is Chitra's mother, so Bharti is Esha's maternal grandmother.
3. Farid is Bharti's brother, so he is a brother of Esha's grandmother: a great-uncle.
4. He is on the mother's side, so "maternal great-uncle".
**Note on the premise:** The question says "three generations"; Farid sits in the top generation beside Bharti, so the count still holds. We assume Farid and Bharti are full siblings.
**Fast method (30 seconds):** Climb up from Esha: mother Chitra, then grandmother Bharti. Then step sideways to the sibling Farid: sibling of a grandparent = great-uncle.
**Check:** Hand-checked on the tree. This relies on Bharti and Farid being full siblings (stated "brother").
**Explain simply:**
- A great-uncle (or grand-uncle) is the brother of a grandparent.
- "Maternal" means on the mother's side, "paternal" on the father's.
- Sibling of a grandparent is two steps up, one step sideways.
**Likely follow-ups:** 1) *If Farid were Dev's brother instead?* He would be Esha's father's brother, her paternal uncle. 2) *If Farid were Anil's brother?* He would be Esha's maternal great-uncle too (mother's father's brother).
**Common mistakes / traps:** Calling Farid her "maternal uncle" (that would be her mother Chitra's brother, not Bharti's), or "grandfather".

### Q44 ⭐⭐ 🟢 A machine applies this rule to every number: an odd number is doubled and an even number is halved, and then all numbers are arranged in ascending order. Input: 18 7 24 13 10. What is the output of Step II (after the rule has been applied twice)?
**Asked at:** commonly asked (no company-specific report found); input-output machine questions are claimed for TCS NQT and Infosys by one prep site (unverified).
**What the interviewer is checking:** Applying a repeated rule carefully and re-sorting after each step.
**Say this in the interview:** "Step I: apply the rule and sort, giving 5 9 12 14 26. Step II: do it again, giving 6 7 10 13 18."
**Answer:** **6 7 10 13 18**
**Step-by-step reasoning:**
1. Step I: 18 is even, halved to 9; 7 is odd, doubled to 14; 24 is even, halved to 12; 13 is odd, doubled to 26; 10 is even, halved to 5. Sorted ascending: 5 9 12 14 26.
2. Step II: 5 odd, doubled to 10; 9 odd, doubled to 18; 12 even, halved to 6; 14 even, halved to 7; 26 even, halved to 13. Sorted ascending: 6 7 10 13 18.
**Fast method (30 seconds):** Do not skip the re-sorting; the rule changes the order, so each step ends with a sort.
**Check:** Verified by script.
**Explain simply:**
- "Odd" means leaves a remainder of 1 when divided by 2; "even" means it divides exactly.
- A step is one full pass: apply the rule to every number, then sort.
**Likely follow-ups:** 1) *Step III?* 3 5 9 14 26 (checked by script). 2) *Would sorting only at the end change the answer?* No for this rule (it acts on each number alone), but it is safer to follow the stated order.
**Common mistakes / traps:** Forgetting that 9 (odd) is doubled again in Step II, or skipping the re-sort after Step I.

### Q45 ⭐⭐ 🟢 A machine arranges numbers by the sum of their digits in ascending order, and numbers with the same digit sum by value in ascending order. Input: 47 92 35 18 63. What is the output?
**Asked at:** commonly asked (no company-specific report found); sort-by-key machine items are standard on prep sites (unverified).
**What the interviewer is checking:** Sorting by a key with a tie-break.
**Say this in the interview:** "Digit sums are 11, 11, 8, 9, 9. Order by digit sum: 35, then 18 and 63, then 47 and 92. Ties go by value: 18 before 63 and 47 before 92."
**Answer:** **35 18 63 47 92**
**Step-by-step reasoning:**
1. Digit sums: 47 gives 4 + 7 = 11; 92 gives 11; 35 gives 8; 18 gives 9; 63 gives 9.
2. Sort ascending by digit sum: 35 (8), then 18 and 63 (9), then 47 and 92 (11).
3. Tie-break by value ascending: 18 < 63 and 47 < 92.
**Fast method (30 seconds):** Write each number with its digit sum in brackets, then sort in two passes: first by value, then (keeping that order) by digit sum.
**Check:** Verified by script.
**Explain simply:**
- A tie-break is a second rule used only when the first rule gives equal results.
- The digit sum is the "key"; the number itself is the tie-breaker.
**Likely follow-ups:** 1) *If digit sums were descending and ties ascending by value?* 47 92 18 63 35 (checked by script). 2) *Where would 29 go if added?* Its digit sum is 11, and 29 < 47, so the order is 35 18 63 29 47 92 (hand-checked).
**Common mistakes / traps:** Sorting by value first (18 35 47 63 92), or putting 92 before 47 because of the tens digit.

### Q46 ⭐⭐ 🟢 How do you solve an input-output (machine) question with unknown rules: what do you compare between consecutive steps, how many steps do you check before trusting a rule, and how do you avoid computing every step when a later step is asked?
**Asked at:** commonly asked (no company-specific report found); one prep site claims input-output questions appear in TCS NQT and Infosys (unverified).
**What the interviewer is checking:** Whether you find a rule by comparing before and after, test it on more than one example, and then use shortcuts instead of brute repetition.
**Say this in the interview:** "I compare Step 0 with Step I and ask what moved or changed. I write a guess, test it on Step II and Step III, and only then apply it. If a late step is asked, I look for a final or repeating state."
**Answer:** **Compare neighbouring steps, test the rule on at least two transitions (three is safer), and look for a finished or repeating state before computing a late step.**
**Explain simply:**
- What to compare: (a) positions (did the same item move to a new place, and by how many places?), (b) values (is each number changed by the same add, multiply, square or digit rule?), (c) order (is it sorting by size, by alphabet, by digit sum, by number of vowels?). Check one of these at a time.
- How many steps: one pair of steps can fit many rules. A rule that fits Step I to II AND Step II to III is rarely a coincidence. If a rule fails on any step, throw it out; do not bend the data. (Our suggestion: two confirmations minimum, three if time allows.)
- Avoid computing every step: (1) sorting machines stop changing once everything is placed; every later step repeats the last one. (2) Rotation or reversal machines repeat after a fixed number of steps (the "period"); use Step number divided by the period, keep the remainder. (3) A "k-th step places the k-th item" pattern lets you write step k directly.
**Worked mini-example:** Input 4 9 16 gives 7 13 21 (Q51 style). Test "add 3": 4+3=7 but 9+3=12, not 13, so rejected. Test "add the square root plus 1": 4+2+1=7, 9+3+1=13, 16+4+1=21, so it fits all three.
**Likely follow-ups:** 1) *A machine reverses the whole list each step; what is Step 9?* Period 2 (odd steps reversed, even steps original), so Step 9 is reversed. 2) *What if two rules fit your data?* Test the next step; if still tied, say so and give the simpler one.
**Common mistakes / traps:** Trusting a rule that fits only the first pair; mixing two changes (position and value) into one guess; computing Step VII by hand when the list became fixed at Step IV.

### Q47 ⭐⭐ 🟢 A machine takes a number x. If x is a multiple of 5 the output is x / 5, otherwise the output is x + 3. The machine is applied again and again to its own output, starting with 22. After how many applications is the output first below 5?
**Asked at:** commonly asked (no company-specific report found); the rule is our own variant.
**What the interviewer is checking:** Careful step-by-step tracing of a conditional rule.
**Say this in the interview:** "22 is not a multiple of 5, so add 3 to get 25. 25 is a multiple of 5, so divide to get 5. 5 is again a multiple of 5, so divide to get 1. That is three applications."
**Answer:** **3 applications** (22 to 25 to 5 to 1).
**Step-by-step reasoning:**
1. Application 1: 22 is not a multiple of 5, so 22 + 3 = 25. (25 is not below 5.)
2. Application 2: 25 is a multiple of 5, so 25 / 5 = 5. (5 is not below 5; "below" means strictly less.)
3. Application 3: 5 / 5 = 1, which is below 5.
**Check:** Verified by script: the sequence is 22, 25, 5, 1, first value below 5 after 3 applications.
**Explain simply:**
- "Multiple of 5" means it ends in 0 or 5.
- Each step needs a fresh test of the new number, not the old one.
**Likely follow-ups:** 1) *Start at 23?* 23, 26, 29, 32, 35, 7, 10, 2: 7 applications (hand-checked).
**Common mistakes / traps:** Stopping at 5 (it equals 5, not below it); forgetting to re-test after adding 3.

### Q48 ⭐⭐ 🟡 A machine rearranges words in increasing order of the number of vowels (a, e, i, o, u), and words with the same number of vowels alphabetically. Input: region sales profit margin units. What is the output?
**Asked at:** commonly asked (no company-specific report found); word-sorting machines are a standard input-output type (prep-site topic lists, unverified).
**What the interviewer is checking:** Applying a two-level sort key (primary count, then alphabet).
**Say this in the interview:** "I count vowels in each word, sort by that count, and break ties alphabetically. Only 'region' has 3 vowels, so it goes last."
**Answer:** **margin profit sales units region**
**Step-by-step reasoning:**
1. Vowel counts: region = e, i, o = 3; sales = a, e = 2; profit = o, i = 2; margin = a, i = 2; units = u, i = 2.
2. Count 2 group: margin, profit, sales, units. Alphabetical order: margin, profit, sales, units.
3. Count 3 group: region, placed after them.
**Check:** Verified by script with the sort key (vowel count, word).
**Explain simply:**
- A two-level sort first orders by the main key, and the second key only matters inside ties.
**Likely follow-ups:** 1) *Count the letter y as a vowel?* Then profit still 2, region 3 (y is not in these words), same output. 2) *Sort in decreasing vowel order?* region first, then the four 2-vowel words alphabetically (if the tie rule is unchanged).
**Common mistakes / traps:** Sorting only alphabetically; miscounting the vowels in "region" or "profit".

### Q49 ⭐⭐ 🟡 A machine takes a string of digits and works as follows. Step 1: reverse the string. Step 2: replace each digit d by (d + 3) modulo 10. Step 3: delete any digit that already appeared earlier (keep the first occurrence). What is the output for the input 2 7 4 7 9 2?
**Asked at:** commonly asked (no company-specific report found); our own variant mixing coding and deduplication, which is close to data-cleaning logic.
**What the interviewer is checking:** Applying a pipeline in the stated order, and understanding "modulo 10" as wrap-around.
**Say this in the interview:** "Reverse, shift each digit by 3 with wrap-around at 10, then remove repeats keeping the first. The result is 5 2 0 7."
**Answer:** **5 2 0 7**
**Step-by-step reasoning:**
1. Reverse 2 7 4 7 9 2: 2 9 7 4 7 2.
2. Add 3 and wrap (modulo 10 means keep the remainder after dividing by 10; 9 + 3 = 12 gives 2, 7 + 3 = 10 gives 0): 5 2 0 7 0 5.
3. Remove repeats, keeping the first: 5, 2, 0, 7 stay; the second 0 and second 5 go. Output 5 2 0 7.
**Check:** Verified by script.
**Explain simply:**
- Modulo 10 gives the last digit of the sum, so digits wrap round like a clock.
- Order matters: deduplicating is the last step, because two different digits can never become equal after the shift, but reversing first decides which copy counts as the "first occurrence".
**Likely follow-ups:** 1) *Keep the last occurrence instead?* From 5 2 0 7 0 5 keep last: 2 7 0 5.
**Common mistakes / traps:** Writing 10 instead of 0; keeping the first occurrence of the original (unreversed) string; removing both copies of a repeat.

### Q50 ⭐⭐ 🟡 A machine takes a two-digit number and does this: Step 1: swap the digits. Step 2: take the positive difference between the original number and the swapped number. Step 3: add the digits of that difference. For the input 83 the output is 9. For which two-digit inputs is the output not 9, and what is the output then?
**Asked at:** commonly asked (no company-specific report found); our own variant based on a classic number property.
**What the interviewer is checking:** Generalising from one example to all cases and spotting the edge case.
**Say this in the interview:** "For digits a and b the difference is 9 times (a minus b), a multiple of 9 up to 81, and its digit sum is 9. The only exception is when both digits are equal, giving difference 0 and output 0."
**Answer:** **Output is not 9 only for 11, 22, 33, 44, 55, 66, 77, 88, 99 (equal digits); the output is 0 for them.**
**Step-by-step reasoning:**
1. Number = 10a + b, swapped = 10b + a. Difference = 9 x |a - b|.
2. |a - b| can be 1 to 9 when digits differ, giving 9, 18, 27, 36, 45, 54, 63, 72, 81.
3. Digit sums of these are all 9.
4. If a = b the difference is 0 and the digit sum is 0.
5. Numbers ending in 0 (such as 40): swapped is 04 = 4, difference 36, digit sum 9, so they still give 9.
**Check:** Verified by brute force over all 90 two-digit numbers: 81 give 9, the 9 repeated-digit numbers give 0.
**Explain simply:**
- Any multiple of 9 up to 81 (and not 0) has a digit sum of 9.
**Likely follow-ups:** 1) *Three-digit version?* Not asked; test it by code before claiming a pattern.
**Common mistakes / traps:** Missing repeated-digit numbers; treating 10, 20, ... as special (they are not).

### Q51 ⭐⭐ 🟡 Input: 4 9 16 25 36. Output: 7 13 21 31 43. What output does the machine give for the input 64?
**Asked at:** commonly asked (no company-specific report found); number-pattern machines are a standard type (prep-site claim, unverified).
**What the interviewer is checking:** Finding a rule that fits every pair, not just the first.
**Say this in the interview:** "The inputs are perfect squares. Each output is the number plus its square root plus 1. For 64: 64 + 8 + 1 = 73."
**Answer:** **73**
**Step-by-step reasoning:**
1. Differences output minus input: 3, 4, 5, 6, 7.
2. Square roots of the inputs: 2, 3, 4, 5, 6. Each difference is the root plus 1.
3. So output = n + sqrt(n) + 1. For 64, root 8, output 64 + 8 + 1 = 73.
**Fast method (30 seconds):** Subtract input from output for every pair; if the gaps grow by 1 each time, link the gap to the root.
**Check:** All five given pairs fit (7, 13, 21, 31, 43), checked by script.
**Explain simply:**
- Look at the difference first; a steadily growing difference points to a link with the position or the root.
**Likely follow-ups:** 1) *Input 100?* 100 + 10 + 1 = 111.
**Common mistakes / traps:** "Add 3" (fits only the first); using the position in the list instead of the root (gives a wrong answer for 64, which is not the 6th item).

### Q52 ⭐⭐ 🟡 A machine sorts numbers as follows. Input: 47 19 82 36 63 25. Step I: 19 47 82 36 63 25. Step II: 19 82 47 36 63 25. Step III: 19 82 25 47 36 63. Step IV: 19 82 25 63 47 36. Each step moves the smallest or largest number of the remaining unsorted part to the next free place from the left, alternately, starting with the smallest. What is Step V?
**Asked at:** commonly asked (no company-specific report found); our own variant of the usual "alternate smallest and largest" machine.
**What the interviewer is checking:** Tracking which part is "placed" and which is "remaining", and reading an alternating rule.
**Say this in the interview:** "Step V is an odd step, so it takes the smallest of the remaining numbers, 47 and 36, which is 36, and puts it in place 5. The output is 19 82 25 63 36 47."
**Answer:** **19 82 25 63 36 47**
**Step-by-step reasoning:**
1. Placed after Step IV: 19, 82, 25, 63 (smallest, largest, next smallest, next largest). Remaining: 47, 36.
2. Odd step means smallest: 36 goes to place 5.
3. Then 47 is left in place 6.
**Check:** The same rule reproduces Steps I to IV exactly; verified by script. Step VI would be unchanged.
**Explain simply:**
- Steps I and II are for the whole list, then the unsorted part shrinks by one each time.
**Likely follow-ups:** 1) *How many steps until nothing changes?* Step V already gives the final order (with 6 items, the last place has only one candidate).
**Common mistakes / traps:** Sorting the whole list instead of only the remaining part; going back to look for the next-smallest among already placed numbers.

### Q53 ⭐⭐ 🟡 A machine rearranges words step by step. Input: tax audit rule bonus claim fund. Step 1 moves the alphabetically first word to the left end. Step 2 moves the alphabetically last word to the right end. Step 3 moves the alphabetically first of the remaining unplaced words to the second place from the left, Step 4 moves the alphabetically last of the remaining unplaced words to the second place from the right, and so on in the same pattern. All other words keep their relative order. In how many steps is the output fully in alphabetical order for the first time?
**Asked at:** commonly asked (no company-specific report found); our own variant.
**What the interviewer is checking:** Careful tracking of placed and unplaced words, and noticing when the list is already sorted before the pattern finishes.
**Say this in the interview:** "I write out each step. After Step 4 the list is audit bonus claim fund rule tax, which is fully alphabetical, so the answer is 4 steps."
**Answer:** **4 steps** (output: audit bonus claim fund rule tax).
**Step-by-step reasoning:**
1. Alphabetical order of the words: audit, bonus, claim, fund, rule, tax.
2. Step 1 (first = audit to left end): audit tax rule bonus claim fund.
3. Step 2 (last = tax to right end): audit rule bonus claim fund tax.
4. Step 3 (first of the unplaced = bonus to place 2): audit bonus rule claim fund tax. Not sorted (rule is before claim).
5. Step 4 (last of the unplaced = rule to second from right): audit bonus claim fund rule tax. Sorted.
**Check:** Verified by script; Steps 1 to 3 were not sorted, Step 4 was.
**Explain simply:**
- Words not yet moved keep their relative order, so claim and fund slide into place by themselves.
**Likely follow-ups:** 1) *Would a Step 5 change anything?* No, the list is final from Step 4 on.
**Common mistakes / traps:** Counting all 6 words as steps; moving a word that was already placed.

### Q54 ⭐⭐ 🟡 A payroll machine takes hours worked h. Gross pay is 20 x h for h up to 40, and 800 + 30 x (h - 40) beyond 40 hours. If the gross pay is more than 1,000, a 10% deduction is applied. What is the net pay for h = 48?
**Asked at:** commonly asked (no company-specific report found); a payroll-flavoured variant of our own for an HR background.
**What the interviewer is checking:** Applying a piecewise rule, then a threshold rule on the result.
**Say this in the interview:** "48 hours is beyond 40, so gross is 800 + 30 x 8 = 1,040. That is above 1,000, so deduct 10%, which is 104, and net is 936."
**Answer:** **Net pay = 936**
**Step-by-step reasoning:**
1. 40 hours at 20 = 800.
2. Overtime hours 48 - 40 = 8, at 30 each = 240. Gross = 1,040.
3. Gross exceeds 1,000, so net = 1,040 x 0.90 = 936.
**Check:** Verified by script (gross 1,040, net 936.0).
**Explain simply:**
- Piecewise means different formulas for different ranges of h; the 800 is the pay for the first 40 hours only.
- The 10% applies to the whole gross, not only to the part above 1,000 (as the question is worded).
**Likely follow-ups:** 1) *h = 46?* Gross 800 + 180 = 980, not above 1,000, so net 980 (hand-checked).
**Common mistakes / traps:** Applying 30 to all 48 hours; taking 10% only of the excess over 1,000.

### Q55 ⭐⭐ 🟡 A machine reverses the first k elements in Step k, starting with k = 2. Input: 5 3 8 1 9 2. What is the output of Step 5?
**Asked at:** commonly asked (no company-specific report found); our own variant (a pancake-flip style machine).
**What the interviewer is checking:** Applying each step to the result of the previous step, not to the original input.
**Say this in the interview:** "Step 2 flips the first 2, Step 3 the first 3, and so on, always on the latest list. Step 5 gives 9 8 5 3 1 2."
**Answer:** **9 8 5 3 1 2**
**Step-by-step reasoning:**
1. Start: 5 3 8 1 9 2.
2. Step 2 (reverse the first 2): 3 5 8 1 9 2.
3. Step 3 (first 3): 8 5 3 1 9 2.
4. Step 4 (first 4): 1 3 5 8 9 2.
5. Step 5 (first 5): 9 8 5 3 1 2.
**Check:** Verified by script (Step 6 would give 2 1 3 5 8 9).
**Explain simply:**
- Each step uses the previous output as its input, so one slip carries forward.
**Likely follow-ups:** 1) *Step 6?* 2 1 3 5 8 9.
**Common mistakes / traps:** Reversing from the original input each time.

### Q56 ⭐⭐ 🟡 A machine performs one left-to-right bubble pass per step: it compares each pair of neighbours and swaps them if the left one is larger. Input: 6 2 9 4 1 7. After how many steps is the list first fully in ascending order, and what is the list after Step 2?
**Asked at:** commonly asked (no company-specific report found); bubble sort is a standard algorithm-trace item.
**What the interviewer is checking:** Tracing an algorithm pass by pass, and knowing when it is done.
**Say this in the interview:** "One pass carries the largest remaining number to the end. After Step 2 the list is 2 4 1 6 7 9, and it becomes fully sorted after Step 4."
**Answer:** **4 steps; after Step 2 the list is 2 4 1 6 7 9.**
**Step-by-step reasoning:**
1. Pass 1: 6 2 9 4 1 7 becomes 2 6 4 1 7 9 (9 bubbles to the end, passing 4, 1 and 7).
2. Pass 2: 2 6 4 1 7 9 becomes 2 4 1 6 7 9.
3. Pass 3: becomes 2 1 4 6 7 9.
4. Pass 4: becomes 1 2 4 6 7 9, which is sorted.
**Check:** Verified by script; after Steps 1 to 3 the list is not sorted.
**Explain simply:**
- After k passes the largest k numbers sit in their final places. A small number far to the right (here 1) moves left only one place per pass, which is why 4 passes are needed.
**Likely follow-ups:** 1) *If the smallest number is at the far right of n numbers?* It needs n - 1 passes.
**Common mistakes / traps:** Doing a full sort in one step; counting an extra "check" pass as a step.

### Q57 ⭐⭐ 🟡 A machine question asks for "Step VII" of an input where steps I to III are shown. What are the two signs that the pattern has a cycle or that the arrangement is already final, and how do they save time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Efficiency: you do not blindly compute seven steps.
**Say this in the interview:** "I look for a step that repeats an earlier one, which means a cycle, or a step that equals the one before it, which means it is final. Either way I can jump straight to Step VII."
**Answer:** **Sign 1: a step equals the one before it (or the list is fully sorted by the rule), so every later step is the same. Sign 2: a step equals an earlier arrangement, so the steps cycle and Step VII is found by remainder after dividing by the cycle length.**
**Explain simply:**
- Final state: a sorting machine that has placed everything cannot change further.
- Cycle: if Step IV looks like the input (Step 0), the period is 4, and Step VII equals Step III (7 divided by 4 leaves remainder 3).
- Also check whether the rule is "pure" (the same operation every step); if the operation depends on the step number (like reversing the first k elements), a cycle needs more care.
**Worked mini-example:** Rule: move the first number to the end. Input 1 2 3 4. Step 4 gives 1 2 3 4 again, so period 4. Step VII is the same as Step 3: 4 1 2 3 (hand-checked).
**Likely follow-ups:** 1) *Reverse the list each step, which step is Step VII?* Period 2, odd step, so reversed. 2) *Rule that changes with step number?* Compute until it stabilises; do not assume a cycle.
**Common mistakes / traps:** Forgetting that remainder 0 means the last arrangement of the cycle (for period 4, Step 8 equals Step 4, which is also Step 0 here); assuming a cycle after only one repeated value.

### Q58 ⭐⭐ 🔴 In a payroll machine (gross = 20h up to 40 hours, 800 + 30(h - 40) beyond; a 10% deduction if gross exceeds 1,000), a net pay of 1,017 was recorded. How many hours were worked?
**Asked at:** commonly asked (no company-specific report found); a reverse (inverse) problem built on our own payroll variant.
**What the interviewer is checking:** Working backwards through a piecewise rule and a threshold, and checking which branch is possible.
**Say this in the interview:** "Without the deduction the most anyone could take home at gross 1,000 is 1,000, so 1,017 must be after the deduction. Gross is 1,017 / 0.9 = 1,130, and 800 + 30(h - 40) = 1,130 gives h = 51."
**Answer:** **51 hours**
**Step-by-step reasoning:**
1. Branch A (no deduction): net = gross, which must be 1,000 or less. 1,017 is above that, so this is impossible.
2. Branch B (with deduction): net = 0.9 x gross, so gross = 1,017 / 0.9 = 1,130 (which is above 1,000, consistent).
3. 1,130 is above 800, so overtime applies: 800 + 30(h - 40) = 1,130, so 30(h - 40) = 330 and h = 51.
**Check:** Forward: h = 51 gives gross 800 + 330 = 1,130 and net 1,017. Brute force over h = 0 to 99 finds 51 only; net pay rises with h, so no other value matches.
**Explain simply:**
- Undoing a deduction means dividing by 0.9 (not adding 10%).
- Always test the branch you assumed.
**Likely follow-ups:** 1) *Net 936?* Gross 1,040 and h = 48.
**Common mistakes / traps:** Adding 10% (1,017 x 1.1 = 1,118.7), which gives a wrong gross; forgetting the 800 base.

### Q59 ⭐ 🟡 A stack machine reads tokens left to right. A number is pushed onto the stack. D duplicates the top item. S swaps the top two items. + and x pop two items and push their sum or product. - pops the top item as b, then the next item as a, and pushes a - b. What is the final stack for the tokens: 3 4 + D x 5 S -?
**Asked at:** commonly asked (no company-specific report found); no source names stack machines, so this is a differentiator item for analyst roles.
**What the interviewer is checking:** Mechanical, careful state tracking and understanding of last-in-first-out order.
**Say this in the interview:** "A stack is a pile where only the top is touched. I write the pile after every token. 3 4 + gives 7, D gives 7 7, x gives 49, 5 pushes, S swaps to 5 under 49 on top, and minus gives 5 - 49 = -44."
**Answer:** **The stack holds a single item: -44.**
**Step-by-step reasoning (bottom to top):**
1. 3: [3]
2. 4: [3, 4]
3. +: [7]
4. D: [7, 7]
5. x: [49]
6. 5: [49, 5]
7. S: [5, 49] (top is now 49)
8. -: b = 49 (top), a = 5, push 5 - 49 = -44. Final [-44].
**Check:** Verified by script.
**Explain simply:**
- Stack: last item in is first item out; the "top" is the last item added.
- The order for minus matters: top is b, the one below is a, and the answer is a - b.
**Likely follow-ups:** 1) *Remove S?* Then - gives 49 - 5 = 44 (hand-checked).
**Common mistakes / traps:** Computing top minus next (49 - 5 = 44, wrong sign).

### Q60 ⭐ 🟡 A queue machine processes commands in order. ENQ x puts x at the back, and DEQ removes the item at the front and prints it. Commands: ENQ 4, ENQ 7, DEQ, ENQ 9, DEQ, ENQ 2, DEQ. What is printed, and what remains in the queue?
**Asked at:** commonly asked (no company-specific report found); no source names queue machines, so this is a differentiator item for analyst roles.
**What the interviewer is checking:** First-in-first-out order, as opposed to the stack's last-in-first-out.
**Say this in the interview:** "A queue is a line: first in, first out. The printed items are 4, 7, 9 in that order, and 2 is left waiting."
**Answer:** **Printed: 4, 7, 9. Remaining queue: [2].**
**Step-by-step reasoning (front on the left):**
1. ENQ 4: [4]
2. ENQ 7: [4, 7]
3. DEQ: prints 4, queue [7]
4. ENQ 9: [7, 9]
5. DEQ: prints 7, queue [9]
6. ENQ 2: [9, 2]
7. DEQ: prints 9, queue [2]
**Check:** Verified by script.
**Explain simply:**
- Queue is like a ticket line; a stack is like a pile of plates.
**Likely follow-ups:** 1) *If it were a stack (DEQ removes the latest)?* Printed 7, 9, 2 and remaining [4] (hand-checked).
**Common mistakes / traps:** Removing from the back; printing the item just added.
