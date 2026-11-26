# Book 13 — Logical Reasoning & Analytical Thinking | Part 7: Letter and Alphanumeric Series, Analogy, Classification and Pattern Recognition 🟢🟡

**Target:** 50 questions | **Actual:** 50 questions
**Scope:** Letter and alphanumeric series (including wrap-around and two-track series), analogies, odd-one-out classification and text-described pattern recognition, with method and "why" questions; text-only, no figure questions; pure number series stay in Book 6 Part 5.

### Q1 ⭐⭐⭐ 🟢 How do you find the rule in a letter series quickly: what do you convert the letters into, which patterns do you test first, and when do you give up and move on?
**Asked at:** commonly asked (no company-specific report found); prep sites list letter series in TCS NQT style reasoning (prep-site claim, unverified).
**What the interviewer is checking:** Whether you have a repeatable routine instead of guessing.
**Say this in the interview:** "I turn letters into numbers (A=1 to Z=26), write the gaps between neighbours, and look for a constant gap, a growing gap, or two interleaved series. If nothing shows in about 20 to 30 seconds, I guess sensibly and move on."
**Answer:** **Convert to numbers, write the differences, then test in a fixed order; give up after roughly half a minute (our suggestion).**
**Explain simply:**
- Position value: A=1, B=2, ... Z=26. After Z the count wraps back to A (so 27 is A, 28 is B). Subtracting 26 is the "wrap-around".
- Test order (our suggestion): (1) same gap every step (+2, +2, ...); (2) gap that grows by 1 (+2, +3, +4); (3) two interleaved series (odd places and even places behave differently); (4) letter groups where each position has its own rule.
- Worked example: B, D, G, K, P becomes 2, 4, 7, 11, 16. Gaps: 2, 3, 4, 5. The gaps grow by 1, so the next gap is 6 and the next letter is 22, V.
- Give-up rule (our suggestion, not research): in a timed gate with negative marking, mark it, move on, and return if time is left.
**Likely follow-ups:** 1) *What if the numbers pass 26?* Subtract 26 (29 becomes 3, C). 2) *What if the gaps look random?* Check whether odd and even places are two separate series.
**Common mistakes / traps:** Forgetting to wrap past Z; testing only a constant gap; spending two minutes on one item.

### Q2 ⭐⭐⭐ 🟢 Letter series: B, D, G, K, P, ? What is the next letter?
**Asked at:** commonly asked (no company-specific report found); letter series are a standard reasoning item in prep-site lists (unverified).
**What the interviewer is checking:** Spotting a growing-gap pattern.
**Say this in the interview:** "In numbers it is 2, 4, 7, 11, 16, with gaps 2, 3, 4, 5. The next gap is 6, so 16 plus 6 is 22, which is V."
**Answer:** **V**
**Step-by-step reasoning:**
1. B=2, D=4, G=7, K=11, P=16.
2. Gaps: 4-2=2, 7-4=3, 11-7=4, 16-11=5.
3. Gaps rise by 1 each time, so the next gap is 6.
4. 16 + 6 = 22, the 22nd letter, V.
**Fast method (30 seconds):** Count the alphabet steps between letters on your fingers; if the steps go 2, 3, 4, 5 you have the "gap grows by 1" pattern, the most common after a constant gap.
**Check:** Verified by script; every given term fits (2, 4, 7, 11, 16) and the next is 22 = V.
**Explain simply:**
- A "growing gap" series adds a number that itself goes up by 1 each step.
- Only one simple rule fits all five letters, so V is the answer.
**Likely follow-ups:** *C, E, H, L, Q, ?* Gaps 2, 3, 4, 5, so next gap 6: 17 + 6 = 23, W (hand-checked).
**Common mistakes / traps:** Choosing U (adding 5 again) or assuming a constant gap.

### Q3 ⭐⭐⭐ 🟢 Letter series: Z, X, U, Q, L, ? What is the next letter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Same growing-gap idea, but going backwards.
**Say this in the interview:** "Z, X, U, Q, L is 26, 24, 21, 17, 12. The gaps are minus 2, 3, 4, 5, so next is minus 6: 12 minus 6 is 6, which is F."
**Answer:** **F**
**Step-by-step reasoning:**
1. Z=26, X=24, U=21, Q=17, L=12.
2. Differences: -2, -3, -4, -5.
3. Next difference is -6, so 12 - 6 = 6.
4. The 6th letter is F.
**Fast method (30 seconds):** Letters falling means a minus gap; same test (gaps rising by 1).
**Check:** Verified by script; all given terms fit and the next is 6 = F.
**Explain simply:**
- Backward series follow the same rules, only the gap is subtracted.
- No wrap-around is needed here since 6 is still above 0.
**Likely follow-ups:** *Y, W, T, P, K, ?* Gaps -2 to -5 then -6: 11 - 6 = 5, E (hand-checked).
**Common mistakes / traps:** Adding 6 instead of subtracting, or answering G (gap of 5 again).

### Q4 ⭐⭐⭐ 🟢 Letter series: A, Z, C, X, E, V, ?, ? What are the next two letters?
**Asked at:** commonly asked (no company-specific report found); two-track letter series appear in prep-site material (unverified).
**What the interviewer is checking:** Recognising two interleaved series.
**Say this in the interview:** "Odd places are A, C, E going up by 2; even places are Z, X, V going down by 2. So the next two are G and T."
**Answer:** **G, T**
**Step-by-step reasoning:**
1. Split into places 1, 3, 5: A, C, E (1, 3, 5), gap +2.
2. Places 2, 4, 6: Z, X, V (26, 24, 22), gap -2.
3. Place 7 continues the first track: 5 + 2 = 7, G.
4. Place 8 continues the second: 22 - 2 = 20, T.
**Fast method (30 seconds):** If the neighbour-to-neighbour gaps jump around (here -25, +27, -25...), stop and split into odd and even places; each track is then simple.
**Check:** Verified by script; tracks A, C, E, G and Z, X, V, T fit all six given letters.
**Explain simply:**
- An "interleaved" series is two separate series woven together, one on odd places and one on even places.
- A first and last letter moving toward each other is a classic version.
**Likely follow-ups:** *Continue to the 10th term.* I (odd track) and R (even track): terms 9 and 10 are I, R.
**Common mistakes / traps:** Reading it as one series and chasing the big jumps; giving T, G in the wrong order.

### Q5 ⭐⭐⭐ 🟢 Complete the series: AD, FI, KN, ?, UX.
**Asked at:** commonly asked (no company-specific report found); letter-group series appear in TCS NQT style guides (prep-site claim, unverified).
**What the interviewer is checking:** Applying a rule to each position of a letter pair.
**Say this in the interview:** "First letters A, F, K go up by 5, so the next is P. Second letters D, I, N go up by 5, so S. The missing term is PS, and UX after it confirms it."
**Answer:** **PS**
**Step-by-step reasoning:**
1. First letters: A=1, F=6, K=11, then 16 = P, then U=21 (matches UX).
2. Second letters: D=4, I=9, N=14, then 19 = S, then X=24 (matches).
3. Each pair is also first letter + 3 = second letter.
**Fast method (30 seconds):** Use the last given term (UX) as a free check: your answer must be exactly 5 below it in both letters.
**Check:** Verified by script; P, S fit between KN and UX in both tracks.
**Explain simply:**
- Treat each position as its own mini series.
- The given final term lets you test the rule from the other side.
**Likely follow-ups:** *What comes after UX?* Next first letter 26 = Z, second 29 wraps to 3 = C, so ZC (hand-checked).
**Common mistakes / traps:** Moving the pair by +1 as a block; forgetting that wrap-around occurs after Z.

### Q6 ⭐⭐⭐ 🟢 Complete the series: AAB, BBC, CCD, ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Seeing that every position moves by one step.
**Say this in the interview:** "The first two letters repeat and step A, B, C, so next is D, D. The last letter is one ahead: B, C, D, so E. The answer is DDE."
**Answer:** **DDE**
**Step-by-step reasoning:**
1. Letters 1 and 2: A, B, C, so D, D.
2. Letter 3: B, C, D, so E.
3. Combined: DDE.
**Fast method (30 seconds):** Every position moves +1; just move the whole word one step along the alphabet and keep the pattern "double letter then next letter".
**Check:** Verified by script; AAB, BBC, CCD, DDE each follow "X, X, next of X".
**Explain simply:**
- Each term has the form (letter, same letter, next letter).
- Only one simple rule fits, so the answer is firm.
**Likely follow-ups:** *What is the term after YYZ?* ZZA, because the letter after Z wraps to A (hand-checked).
**Common mistakes / traps:** Writing DDD or CCE by changing only one position.

### Q7 ⭐⭐⭐ 🟢 What are the common relationship types in analogy questions (part and whole, tool and use, measure and quantity, opposites, and so on), and how does the "make a sentence" method help you choose between options?
**Asked at:** commonly asked (no company-specific report found); analogy is listed among TCS NQT reasoning topics in prep guides (unverified).
**What the interviewer is checking:** Whether you name the link before looking at options.
**Say this in the interview:** "I put the first pair into one precise sentence, like 'a page is a part of a book', and then test each option in that same sentence. The option where the sentence stays true in the same direction wins."
**Answer:** **Common types: part and whole, tool and use, measure and quantity, opposites (antonyms), synonyms, cause and effect, category and example, worker and workplace, and degree (warm, hot). Make one precise sentence from the first pair, then fill it with each option.**
**Explain simply:**
- An analogy "A is to B as C is to D" means the relationship between A and B is the same as between C and D.
- Examples: Page : Book (part and whole); Knife : Cut (tool and use); Metre : Length (unit and what it measures); Hot : Cold (opposites); Rain : Flood (cause and effect).
- Make the sentence precise: "a knife is used to cut" beats "a knife and cut go together", because vague sentences let wrong options through.
- Keep the direction: "part of a whole" is not the same as "whole made of parts". If the first pair is part-to-whole, the second must be too.
**Likely follow-ups:** 1) *Two options both fit the sentence?* Tighten the sentence (add size, order, or purpose) until only one stays true. 2) *Which type is commonly tested in data contexts?* Tool and use (formula and task) and part and whole (row and table).
**Common mistakes / traps:** Choosing an option that is merely related to the word (word association) instead of matching the relationship; flipping the direction.

### Q8 ⭐⭐⭐ 🟢 Find the odd one out: KMO, EGI, PRT, BDG, WYA.
**Asked at:** commonly asked (no company-specific report found); odd-one-out letter clusters with a +2 rule appear in TCS NQT style prep guides (prep-site claim, unverified).
**What the interviewer is checking:** Testing a rule on every cluster, including a wrap-around one.
**Say this in the interview:** "In KMO, EGI, PRT and WYA each letter is 2 ahead of the last. BDG goes B to D (+2) but D to G (+3), so BDG is the odd one."
**Answer:** **BDG**
**Step-by-step reasoning:**
1. Gaps: KMO 11, 13, 15 (+2, +2); EGI 5, 7, 9 (+2, +2); PRT 16, 18, 20 (+2, +2).
2. BDG: 2, 4, 7 gives +2, +3.
3. WYA: W=23, Y=25, A=27 which wraps to 1, so +2, +2.
4. Only BDG breaks the "every step is +2" rule.
**Fast method (30 seconds):** Compute the two gaps for each cluster; the one that differs is the answer. Do not forget wrap-around for clusters that run past Z.
**Check:** Verified by script; four clusters give gaps (2, 2) and BDG gives (2, 3). No second clean rule was found, so only one rule is defensible.
**Explain simply:**
- "Odd one out" means four items share a rule and one does not.
- Wrap-around: after Z comes A again, so A counts as 27.
**Likely follow-ups:** *Change BDG to BDF?* Then all five fit and there is no odd one out (the question would be invalid).
**Common mistakes / traps:** Calling WYA odd because it ends in A (it does not break the rule once you wrap).

### Q9 ⭐⭐⭐ 🟢 Page is to Book as Row is to what? (a) Table (b) Column (c) Cell (d) Query
**Asked at:** commonly asked (no company-specific report found); data-flavoured analogy written for this book.
**What the interviewer is checking:** Matching the relationship (part to whole) and its direction.
**Say this in the interview:** "A page is a part of a book, so a row is a part of a table. The answer is (a) Table."
**Answer:** **(a) Table**
**Step-by-step reasoning:**
1. Sentence: "A page is one part that makes up a book."
2. Test options in the same sentence: a row is one part that makes up a table. True.
3. Column: a row is not part of a column (same level, a different direction). Cell: a cell is part of a row, so that reverses the direction. Query: unrelated.
**Fast method (30 seconds):** Say the sentence with the first pair, then check direction: small thing first, big thing second.
**Check:** Hand-checked against all four options. A column is also part of a table, but it is a sibling of a row, not a replacement for the "whole"; the intended answer is Table.
**Explain simply:**
- Part-to-whole: the first word is a piece of the second.
- A table is made of rows and columns; each row holds cells.
**Likely follow-ups:** *Cell is to row as ? is to table.* Both row and column are parts of a table, so the item would need options that separate them; the natural reading is row (a cell is part of a row, a row is part of a table). Hand-checked.
**Common mistakes / traps:** Picking Column because it "goes with" row (word association), or Cell by reversing the direction.

### Q10 ⭐⭐⭐ 🟢 Find the odd one out among these Excel functions: COUNTIF, SUMIF, AVERAGEIF, VLOOKUP, SUMIFS.
**Asked at:** commonly asked (no company-specific report found); odd-one-out is a practised company-test topic per prep sites (unverified); data-flavoured version written for this book.
**What the interviewer is checking:** Classifying by what the tool does, not by spelling.
**Say this in the interview:** "COUNTIF, SUMIF, AVERAGEIF and SUMIFS all summarise only the rows that meet a condition. VLOOKUP finds a value and returns something from the same row. So VLOOKUP is the odd one out."
**Answer:** **VLOOKUP**
**Step-by-step reasoning:**
1. COUNTIF counts matching cells, SUMIF adds them, AVERAGEIF averages them, SUMIFS adds with several conditions. All give one summary number from a condition.
2. VLOOKUP looks up a key and fetches a related value; it does not summarise.
3. A second surface clue agrees: four names end in IF or IFS; VLOOKUP does not.
**Fast method (30 seconds):** Ask "what does it return?": a summary (count, total, average) versus a lookup (a value from a table).
**Check:** Hand-checked. Second rules exist (only COUNTIF counts rather than sums or averages; only SUMIFS takes several conditions), but each singles out one function while leaving the other three together with VLOOKUP unexplained, so the lookup-versus-summary rule is preferred. Rule used: what the function returns.
**Explain simply:**
- Conditional aggregation means "summarise only what meets a test".
- Lookup means "find a row by a key and read another column".
**Likely follow-ups:** *Replace VLOOKUP with COUNTA?* Then COUNTA (no condition) would be odd (hand-checked).
**Common mistakes / traps:** Picking COUNTIF because it counts, or SUMIFS because it has more conditions.

### Q11 ⭐⭐⭐ 🟢 Complete the day series: Monday, Thursday, Sunday, Wednesday, ?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Treating days as numbers on a cycle of 7.
**Say this in the interview:** "Each day is 3 days after the last: Monday to Thursday, Thursday to Sunday, Sunday to Wednesday. The next is Wednesday plus 3, which is Saturday."
**Answer:** **Saturday**
**Step-by-step reasoning:**
1. Number the days Monday=1 ... Sunday=7.
2. Sequence: 1, 4, 7, 3 (the 10th day wraps to 3), so every step is +3 with wrap at 7.
3. Next: 3 + 3 = 6, which is Saturday.
**Fast method (30 seconds):** Count forward on your fingers from Monday: Tue, Wed, Thu is 3 steps. Repeat from each term.
**Check:** Verified by script; steps of +3 mod 7 give Mon, Thu, Sun, Wed, Sat. Only this constant-step rule was found.
**Explain simply:**
- A week repeats every 7 days, so counting past Sunday wraps to Monday (like Z to A).
- "Mod 7" just means keep the remainder after dividing by 7.
**Likely follow-ups:** *Next after Saturday?* 6 + 3 = 9, wraps to 2, Tuesday (hand-checked).
**Common mistakes / traps:** Saying Friday (adding 2) or forgetting to wrap after Sunday.

### Q12 ⭐⭐⭐ 🟡 Letter series with wrap-around: T, V, Y, C, H, ? What is the next letter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Growing gaps combined with wrap-around.
**Say this in the interview:** "T, V, Y is 20, 22, 25, then C is 29 after wrapping, H is 34 which is 8. Gaps 2, 3, 4, 5, so next is plus 6. 34 + 6 = 40, minus 26 is 14, which is N."
**Answer:** **N**
**Step-by-step reasoning:**
1. T=20, V=22, Y=25.
2. Next gap +4 gives 29; 29 - 26 = 3 = C. Matches.
3. Next gap +5 gives 8 = H (3 + 5). Matches.
4. Next gap +6 gives 14 = N.
**Fast method (30 seconds):** Whenever letters seem to jump backward in a forward series, add 26 to the later letter before taking the gap. C becomes 29, and the gap from Y (25) to 29 is 4, which fits the growing-gap pattern.
**Check:** Verified by script; the gaps 2, 3, 4, 5 fit all given terms and the next is 14 = N.
**Explain simply:**
- The alphabet is a circle of 26, so passing Z lands you back at A.
- Subtract 26 once the running total goes over 26.
**Likely follow-ups:** *U, W, Z, D, I, ?* Same gaps from 21: 21, 23, 26, 30 (D), 35 (I), then +6 gives 41, minus 26 is 15, O (hand-checked).
**Common mistakes / traps:** Reading C as a drop of 22 and abandoning the pattern; answering M or O from a gap slip.

### Q13 ⭐⭐⭐ 🟡 Alphanumeric series: B2, D6, F12, H20, ? What is the next term?
**Asked at:** commonly asked (no company-specific report found); alphanumeric series are a reported prep-site topic (unverified).
**What the interviewer is checking:** Splitting into a letter track and a number track.
**Say this in the interview:** "Letters B, D, F, H go up by 2, so next is J. Numbers 2, 6, 12, 20 have gaps 4, 6, 8, so next gap is 10 and the number is 30. The term is J30."
**Answer:** **J30**
**Step-by-step reasoning:**
1. Letter track: B, D, F, H (2, 4, 6, 8), +2 each time, so J (10).
2. Number track: 2, 6, 12, 20; differences 4, 6, 8, so next difference 10, giving 30.
3. Link between the tracks: the number equals n times (n + 1) for term n (1x2, 2x3, 3x4, 4x5), so term 5 is 5x6 = 30. This also confirms the gap pattern.
**Fast method (30 seconds):** Do the letters first (they are easy), then the numbers; if the tracks seem unrelated, look at term position n for the number rule.
**Check:** Verified by script; J30 fits both tracks and the n(n+1) rule.
**Explain simply:**
- Two tracks means two separate mini series in one term.
- n(n+1) numbers (2, 6, 12, 20, 30) are called "pronic" or "product of consecutive numbers".
**Likely follow-ups:** *What is the 6th term?* L and 6x7 = 42, so L42 (hand-checked).
**Common mistakes / traps:** Giving J28 by guessing a gap of 8 again; treating the letter and number as one block.

### Q14 ⭐⭐⭐ 🟡 Complete the letter-group series: ABD, EFH, IJL, ?
**Asked at:** commonly asked (no company-specific report found); letter-group series appear in TCS NQT style prep material (prep-site claim, unverified).
**What the interviewer is checking:** Whether you convert letters to numbers and spot a repeating shape inside each group.
**Say this in the interview:** "I turn ABD into 1, 2, 4. EFH is 5, 6, 8 and IJL is 9, 10, 12. Each group starts 4 higher, so the next is 13, 14, 16."
**Answer:** **MNP**
**Step-by-step reasoning:**
1. Convert to positions (A=1, B=2, and so on up to Z=26): ABD = 1, 2, 4; EFH = 5, 6, 8; IJL = 9, 10, 12.
2. Inside every group the shape is the same: first, first+1, first+3.
3. The first letters go 1, 5, 9, so they rise by 4 each time. The next first letter is 13 = M.
4. Apply the shape: 13, 14, 16 = M, N, P.
**Fast method (30 seconds):** Notice the groups are just the alphabet read in blocks of 4 with the 3rd letter of each block skipped (ABCD without C, EFGH without G, IJKL without K). Next block MNOP without O = MNP. It works because the rule is "same gap pattern, block start moves 4".
**Check:** Verified by script: adding 4 to each position of ABD, repeatedly, gives ABD, EFH, IJL, MNP.
**Explain simply:**
- Position value means the letter's place in the alphabet.
- When groups look alike, compare group to group (the first letters) and also inside one group (the gaps).
**Likely follow-ups:** 1) *What comes after MNP?* Add 4 again: 17, 18, 20 = QRT. 2) *What if the groups were ABD, FGI, KLN?* The start moves 5, so the next is PQS (checked by script).
**Common mistakes / traps:** Continuing the alphabet straight on (MNO) instead of applying the skip inside the group.

### Q15 ⭐⭐⭐ 🟡 How do you attack an alphanumeric series: why do you split it into a letter track and a number track, and what do you check if the two tracks seem unrelated?
**Asked at:** commonly asked (no company-specific report found); the letter-track and number-track method is described in prep sites such as CCBP (prep-site claim, unverified).
**What the interviewer is checking:** Whether you break a mixed problem into two simpler ones instead of staring at the whole.
**Say this in the interview:** "I split it into a letter row and a number row, find a rule for each, and then check whether one drives the other, for example the number equals the letter's position times something."
**Answer:** **Solve each track separately; if they look unrelated, test (a) a link between the two, (b) that the two tracks alternate in one series, and (c) wrap-around or a changing step.**
**Explain simply:**
- Letter track: convert letters to positions (A=1 to Z=26) and look at the gaps. Number track: look at differences, ratios, squares and cubes.
- Why split: one rule in two small parts is far easier than one big rule, and a mistake in one part cannot hide behind the other.
- If they seem unrelated, check these in order: does the number equal the letter's position, or a function of it (B2, D4 ...)? Does the number equal the term's place (1st, 2nd, 3rd) times something? Do letters and numbers actually alternate as one series (A 1 B 4 C 9 reads as two interleaved lists)? Does a letter wrap past Z back to A?
- Worked mini-example: B2, D6, F12, H20 (a practice item). Letters B, D, F, H are 2, 4, 6, 8 (step 2). Numbers 2, 6, 12, 20 have differences 4, 6, 8, so the next is 30. Here the number is also the product of neighbouring even numbers (1x2, 2x3, 3x4, 4x5), so the tracks are linked: letter position 2k with number k(k+1).
**Likely follow-ups:** 1) *What if only one track is regular?* Answer from that track, and say the other looks like noise or a distractor. 2) *How long do you spend?* Our suggestion: about 40 to 60 seconds, then guess and move on.
**Common mistakes / traps:** Forcing one rule over the whole term; forgetting that the number track may count the term number, not the letter value.

### Q16 ⭐⭐⭐ 🟡 A hospital rota repeats in a fixed cycle: Morning, Morning, Evening, Night, then starts again. Day 1 is a Morning shift. What shift falls on Day 30?
**Asked at:** commonly asked (no company-specific report found); repeating-cycle questions are a standard pattern-recognition item (prep-site claim, unverified).
**What the interviewer is checking:** Whether you use the remainder after dividing by the cycle length instead of listing 30 days.
**Say this in the interview:** "The cycle has 4 days. 30 divided by 4 leaves remainder 2, so Day 30 sits in position 2 of the cycle, which is Morning."
**Answer:** **Morning**
**Step-by-step reasoning:**
1. One full cycle is Morning, Morning, Evening, Night: 4 days.
2. Day 1 is position 1, Day 5 is position 1 again, and so on.
3. Remainder of 30 divided by 4 is 2 (4 x 7 = 28, leaving 2).
4. Remainder 2 means position 2, which is Morning. (A remainder of 0 would mean position 4, Night.)
**Fast method (30 seconds):** Remainder of day number divided by cycle length gives the position; remainder 0 means the last position. Days 28 (Night), 29 (Morning), 30 (Morning) confirm it.
**Check:** Verified by script: listing 30 days of the cycle gives Morning on Day 30.
**Explain simply:**
- Remainder means what is left after dividing; it tells you how far into the current cycle you are.
- This is the same idea as "what day of the week is it 30 days from now" (30 mod 7).
**Likely follow-ups:** 1) *What shift is Day 100?* 100 divided by 4 leaves 0, so position 4, Night. 2) *What if the cycle were 5 days?* Divide by 5 instead and read the position.
**Common mistakes / traps:** Treating remainder 0 as position 0 (there is none; it is the last position), or starting the count from Day 0.

### Q17 ⭐⭐ 🟢 What position-value facts help you solve letter questions fast (A=1 to Z=26, the opposite-letter rule, the letters E J O T Y)?
**Asked at:** commonly asked (no company-specific report found); position mapping A=1 to Z=26 is listed in letter-series prep material (prep-site claim, unverified).
**What the interviewer is checking:** Whether you have the alphabet numbers memorised well enough to work without counting on your fingers.
**Say this in the interview:** "A is 1 and Z is 26. The letter from the left and its mirror from the right always add to 27. Five anchor letters, E, J, O, T, Y, are positions 5, 10, 15, 20, 25."
**Answer:** **Three facts: A=1 to Z=26; opposite letter = 27 minus position; anchors E=5, J=10, O=15, T=20, Y=25.**
**Explain simply:**
- Position value: the letter's place in the alphabet. Convert to numbers, do the arithmetic, convert back.
- Opposite-letter rule: the letter the same distance from the other end. Position 3 (C) pairs with 27 - 3 = 24 (X). So A-Z, B-Y, C-X ... M-N all add to 27.
- Anchors: remember E J O T Y (the word "EJOTY"). From F to Y every letter is at most 2 steps from an anchor, so M is O minus 2 = 13, and R is T minus 2 = 18. For A to D, count up from A or down from E (A to D are 4 to 1 steps below E), and Z is 1 step above Y.
- Worked mini-example: opposite of K? K = 11, 27 - 11 = 16 = P. Position of V? Anchor T = 20, V is 2 further = 22.
- Useful extra: vowels A E I O U are 1, 5, 9, 15, 21.
**Likely follow-ups:** 1) *Opposite of H?* 27 - 8 = 19 = S. 2) *What is the 10th letter from the right?* 27 - 10 = 17 = Q (the 17th from the left).
**Common mistakes / traps:** Using 26 instead of 27 for the opposite rule (that gives off-by-one errors); counting from 0.

### Q18 ⭐⭐ 🟢 Which letter is exactly midway between G and S in the English alphabet?
**Asked at:** commonly asked (no company-specific report found); alphabet-test position questions appear in prep-site lists (unverified).
**What the interviewer is checking:** Whether you find a midpoint by averaging positions.
**Say this in the interview:** "G is 7 and S is 19. The middle of 7 and 19 is (7+19)/2 = 13, which is M."
**Answer:** **M**
**Step-by-step reasoning:**
1. G = 7, S = 19.
2. Midway means the average: (7 + 19) / 2 = 13.
3. 13 = M.
4. Because 19 - 7 = 12 is even, there is exactly one middle letter (if the gap were odd there would be none).
**Fast method (30 seconds):** Add the two positions, halve. Or count from G: the 6th letter after G is M, and 6 more reaches S.
**Check:** Verified by script: the letters strictly between G and S are H to R (11 letters) and the 6th of them, M, is the middle; 5 letters on each side.
**Explain simply:**
- "Exactly midway" is the same as the average of two numbers.
- It only exists as a real letter when the sum of positions is even.
**Likely follow-ups:** 1) *Midway between G and R?* (7+18)/2 = 12.5, so no single letter; L and M share the middle. 2) *Midway between B and N?* (2+14)/2 = 8 = H.
**Common mistakes / traps:** Counting G or S themselves when counting letters between; answering L or N from a miscount.

### Q19 ⭐⭐ 🟢 CAT is to ECV as DOG is to what?
**Asked at:** commonly asked (no company-specific report found); letter-shift analogies are in TCS NQT style prep material (prep-site claim, unverified).
**What the interviewer is checking:** Whether you find the letter-by-letter shift rule and apply it to a new word.
**Say this in the interview:** "C to E, A to C, T to V: each letter moves 2 forward. So D, O, G become F, Q, I."
**Answer:** **FQI**
**Step-by-step reasoning:**
1. Compare letter by letter: C(3) to E(5) is +2; A(1) to C(3) is +2; T(20) to V(22) is +2.
2. Same shift for every letter, so the rule is "move each letter 2 forward".
3. Apply to DOG: D(4) +2 = F(6); O(15) +2 = Q(17); G(7) +2 = I(9).
4. Answer FQI. This is the only simple rule that fits all three letters (a different rule per letter would be arbitrary).
**Fast method (30 seconds):** Check only the first letter's shift, then confirm on one more letter. A constant shift means the rule is certain.
**Check:** Verified by script: shifting CAT by +2 gives ECV, and DOG gives FQI.
**Explain simply:**
- A "shift" or "Caesar shift" moves every letter the same number of places along the alphabet.
- If a letter would pass Z, it wraps back to A.
**Likely follow-ups:** 1) *What would XYZ become with the same rule?* ZAB (wrap-around). 2) *What if CAT became DBU?* Then it is +1 each, and DOG would be EPH.
**Common mistakes / traps:** Reversing the word, or shifting only the first letter.

### Q20 ⭐⭐ 🟢 Expand is to Contract as Inflate is to what?
**Asked at:** commonly asked (no company-specific report found); opposites analogies appear in TCS NQT style prep material (prep-site claim, unverified).
**What the interviewer is checking:** Whether you name the relationship (antonym, meaning opposite) and apply it.
**Say this in the interview:** "Expand and contract are opposites. The opposite of inflate (fill with air) is deflate."
**Answer:** **Deflate**
**Step-by-step reasoning:**
1. Make a sentence: "Contract is the opposite of expand."
2. Use the same sentence: "___ is the opposite of inflate."
3. Inflate means fill with air or make bigger; its opposite is deflate (let air out, make smaller).
4. Only one rule is defensible here: antonym. Both pairs also describe size or volume change, which supports it.
**Fast method (30 seconds):** Say the sentence aloud with the first pair, then swap in the new word. If two options both fit, pick the one with the closest degree and type of meaning.
**Check:** Hand-checked: expand to contract is bigger to smaller, inflate to deflate is bigger to smaller.
**Explain simply:**
- Antonym means a word with the opposite meaning; synonym means the same meaning.
- Spot the relationship type first (opposite, part and whole, tool and use), then find the word.
**Likely follow-ups:** 1) *What if the first pair were Expand and Enlarge?* Then it is synonyms and the answer would be a synonym of inflate, such as swell. 2) *Opposite of Increase?* Decrease.
**Common mistakes / traps:** Choosing "burst" (a result of inflating too much, not the opposite action) or "empty".

### Q21 ⭐⭐ 🟢 Find the odd one out: CF, GJ, KN, PR, TW.
**Asked at:** commonly asked (no company-specific report found); odd-one-out letter clusters are described in TCS NQT guides (prep-site claim, unverified).
**What the interviewer is checking:** Whether you measure the gap inside each pair and spot the one that breaks the pattern.
**Say this in the interview:** "I convert each pair to numbers and check the gap. CF is 3 to 6, GJ 7 to 10, KN 11 to 14, TW 20 to 23: all gap 3. PR is 16 to 18, a gap of 2. So PR is odd."
**Answer:** **PR**
**Step-by-step reasoning:**
1. Positions: CF = 3, 6; GJ = 7, 10; KN = 11, 14; PR = 16, 18; TW = 20, 23.
2. Gap inside each pair (second minus first): 3, 3, 3, 2, 3.
3. Four pairs have gap 3; PR has gap 2, so PR is the odd one.
4. A second rule on the first letters (C, G, K, P, T = 3, 7, 11, 16, 20, steps 4, 4, 5, 4) is not clean: removing any one item does not leave a constant step, so it does not point to a different answer. The gap-inside-the-pair rule is the one used.
**Fast method (30 seconds):** Check the gap inside each item first; it is the quickest test and usually reveals the intruder.
**Check:** Verified by script: gaps 3, 3, 3, 2, 3.
**Explain simply:**
- Odd one out: find the rule that most items follow, then pick the one that breaks it.
- Test the gap inside the item before testing gaps between items.
**Likely follow-ups:** 1) *If PR were OR, would it fit?* O is 15, R is 18, gap 3 and the starts C, G, K, O, T go 4, 4, 4, 5 (the last would be S). So the gap rule fits but the start rule does not. 2) *What if the intruder shows two rules?* Say the primary rule and mention the second.
**Common mistakes / traps:** Counting letters in between instead of the difference (gap 3 means 2 letters between); picking TW because it follows the odd step in the starts.

### Q22 ⭐⭐ 🟢 Find the odd one out among these SQL keywords: INNER JOIN, LEFT JOIN, FULL JOIN, CROSS JOIN, UNION.
**Asked at:** commonly asked (no company-specific report found); SQL-themed classification is our own data-analyst flavour of the standard odd-one-out item.
**What the interviewer is checking:** Whether you know the difference between joining tables and stacking result sets.
**Say this in the interview:** "Four of these are joins that combine columns from two tables side by side. UNION is different: it stacks rows from two queries on top of each other. UNION is the odd one."
**Answer:** **UNION**
**Step-by-step reasoning:**
1. INNER JOIN, LEFT JOIN, FULL JOIN and CROSS JOIN are all join types: they place columns of two tables side by side, matching rows.
2. UNION is a set operator: it appends the rows of one query under another and removes duplicates; it needs matching column counts, not matching keys.
3. A second rule exists: CROSS JOIN is the only join with no ON condition (it pairs every row with every row). That would make CROSS JOIN odd. But UNION is preferred because it is not a join at all, which is the more basic difference.
**Fast method (30 seconds):** Ask "is the word JOIN in the name?" and then "what does it do to the data, widen or lengthen?" UNION lengthens; joins widen.
**Check:** Hand-checked against standard SQL definitions (not run here).
**Explain simply:**
- Join: combine two tables column-wise using a matching key.
- Set operator (UNION, INTERSECT, EXCEPT): combine query results row-wise.
- UNION removes duplicates; UNION ALL keeps them.
**Likely follow-ups:** 1) *Which of the five has no ON clause?* CROSS JOIN. 2) *Odd one among INNER, LEFT, FULL, UNION ALL, INTERSECT?* Then the joins are the INNER, LEFT, FULL group and the other two are set operators, so the grouping changes.
**Common mistakes / traps:** Picking CROSS JOIN because of the ON clause; the item asks for the biggest category split.

### Q23 ⭐⭐ 🟢 Find the odd one out in a salary structure: Basic pay, HRA, Special allowance, Provident fund deduction, Conveyance allowance.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured classification item written for this book's reader.
**What the interviewer is checking:** Whether you separate earnings from deductions, a distinction every HR professional already knows.
**Say this in the interview:** "Basic, HRA, special allowance and conveyance allowance are earnings that add to gross salary. Provident fund deduction is taken out of pay. So the deduction is the odd one."
**Answer:** **Provident fund deduction**
**Step-by-step reasoning:**
1. Earnings (components added to gross pay): basic pay, HRA (house rent allowance), special allowance, conveyance allowance.
2. Provident fund deduction is the employee's contribution subtracted from gross to reach net pay.
3. So four items are earnings and one is a deduction.
4. A second grouping exists: HRA, special and conveyance are all "allowances", and basic pay is not. That would make Basic pay odd. We prefer the earnings versus deduction split because the item names a "deduction" explicitly and the salary-structure frame invites it.
**Fast method (30 seconds):** Look for words that signal direction: "deduction" subtracts, everything else adds.
**Check:** Hand-checked; no calculation involved.
**Explain simply:**
- Gross pay: total earnings before deductions. Net pay: take-home after deductions.
- Allowance: an extra amount paid on top of basic for a stated purpose.
**Likely follow-ups:** 1) *Where does the employer's PF share go?* It is usually shown in the cost to company (CTC) but not as a deduction from the employee's pay; this varies by company, so check the structure. 2) *Add "Professional tax" to the list: which group?* A deduction.
**Common mistakes / traps:** Choosing Basic pay because it is not called an allowance, when the clearer split is earnings versus deductions.

### Q24 ⭐⭐ 🟢 Find the odd one out: February, April, June, September, November.
**Asked at:** commonly asked (no company-specific report found); calendar-based odd-one-out is a standard classification item (prep-site claim, unverified).
**What the interviewer is checking:** Whether you use a factual property (days in the month) rather than a surface feature like spelling.
**Say this in the interview:** "April, June, September and November all have 30 days. February has 28 or 29. February is the odd one out."
**Answer:** **February**
**Step-by-step reasoning:**
1. Days: February 28 (29 in a leap year), April 30, June 30, September 30, November 30.
2. Four months share 30 days; February does not.
3. Spelling-based rules do not separate one month cleanly (letter counts are 8, 5, 4, 9, 8), so the days rule is the only defensible one.
**Fast method (30 seconds):** Use the knuckle rhyme: "30 days has September, April, June and November."
**Check:** Hand-checked against the calendar.
**Explain simply:**
- Leap year: a year with an extra day in February, roughly every 4 years.
- Prefer facts that split the set 4 to 1 over cute wordplay.
**Likely follow-ups:** 1) *Add July to the list?* It has 31 days, so then two groups appear and the item is no longer a clean odd-one-out. 2) *Which months have 31 days?* January, March, May, July, August, October, December.
**Common mistakes / traps:** Choosing September because it is the longest word.

### Q25 ⭐⭐ 🟢 ACE is to 9 as BDF is to what? (Use the same rule for both.)
**Asked at:** commonly asked (no company-specific report found); letter-to-number analogies appear in TCS NQT style prep material (prep-site claim, unverified).
**What the interviewer is checking:** Whether you test a rule on the first pair, then apply the same rule to the second.
**Say this in the interview:** "ACE is 1 + 3 + 5 = 9, so the rule is the sum of letter positions. BDF is 2 + 4 + 6 = 12."
**Answer:** **12**
**Step-by-step reasoning:**
1. Convert ACE: A = 1, C = 3, E = 5.
2. The sum is 1 + 3 + 5 = 9, which matches the given number.
3. Apply the same rule to BDF: B = 2, D = 4, F = 6; sum = 12.
4. The product rule fails (1 x 3 x 5 = 15, not 9), and a "number of letters" rule would give 3 for both, so the sum is the only simple rule that fits.
**Fast method (30 seconds):** Convert to numbers, then try sum first, because it is the most common rule. BDF is ACE with every letter 1 higher, so the sum rises by 3: 9 + 3 = 12.
**Check:** Verified by script: sums are 9 and 12; products 15 and 48 (the product does not give 9).
**Explain simply:**
- Letter-to-number analogy: letters stand for their alphabet positions.
- Test one rule on the known pair. If it matches, use it on the new one.
**Likely follow-ups:** 1) *CEG would be?* 3 + 5 + 7 = 15. 2) *What if ACE were 15?* Then the rule would be the product, and BDF would be 48.
**Common mistakes / traps:** Answering 9 again because the letters "look similar", or using the first letter only.

### Q26 ⭐⭐ 🟢 7 is to 343 as 5 is to what?
**Asked at:** commonly asked (no company-specific report found); number-pair analogies are a standard item (prep-site claim, unverified).
**What the interviewer is checking:** Whether you recognise the power relationship between the numbers.
**Say this in the interview:** "7 x 7 x 7 is 343, so the rule is the cube. The cube of 5 is 125."
**Answer:** **125**
**Step-by-step reasoning:**
1. Test squares first: 7 squared is 49, not 343.
2. Test cubes: 7 x 7 x 7 = 343. It matches.
3. Apply to 5: 5 x 5 x 5 = 125.
4. Other rules like "multiply by 49" would give 245, but 49 appears nowhere in the pair, so the cube is the one defensible rule.
**Fast method (30 seconds):** Know the cubes of 1 to 10: 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000. Seeing 343 you know it is 7 cubed at once.
**Check:** Verified by script: 7 cubed is 343 and 5 cubed is 125.
**Explain simply:**
- Cube of a number: the number multiplied by itself three times.
- When the output is much bigger than the input, test squares and cubes before anything else.
**Likely follow-ups:** 1) *6 is to what, by the same rule?* 216. 2) *What if 7 is to 49 as 5 is to what?* The square, 25.
**Common mistakes / traps:** Squaring (25) or tripling (15).

### Q27 ⭐⭐ 🟢 Why can the same short series, such as 2, 4, 8, ?, have more than one defensible next term, and how should you choose the answer in a timed test?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know a few terms never prove a rule, and whether you choose the simplest rule that fits all terms.
**Say this in the interview:** "Three terms fit several rules. Doubling gives 16; adding 2, 4, 6 gives 14. In a test I pick the simplest rule that fits every term and, if the options allow, the one that appears there."
**Answer:** **Several rules fit 2, 4, 8; the default pick is 16 (multiply by 2), the main rival is 14 (differences 2, 4, 6).** Choose by simplicity plus the answer options.
**Explain simply:**
- A "rule" is just a recipe that produces the terms. With only three terms, more than one recipe can produce them. Rule A: multiply by 2 gives 2, 4, 8, 16. Rule B: add 2, then 4, then 6 (the added amount grows by 2 each time) gives 2, 4, 8, 14.
- In fact any fourth number can be forced by some formula (a polynomial, i.e. a formula made of powers of n, can be drawn through any set of points), so "fits" alone is not enough. You need the simplest rule.
- Simplest means fewest steps and no strange constants. Doubling is one step; rule B needs two layers.
- Tie-breakers: (1) check the answer options, because often only one of the rival values is offered (our suggestion, not a guarantee); (2) a longer given series removes the ambiguity, so more terms mean less doubt; (3) if still tied, take the simplest rule and move on.
**Worked mini-example:** 2, 4, 8, 16, 32 (doubling) and 2, 4, 8, 14, 22 (differences 2, 4, 6, 8) agree on three terms and split on the fourth. Shown by script.
**Likely follow-ups:** If the options are 14, 16 and 18, which? Both 14 and 16 fit, so look for the setter's intent: doubling is the simplest, so 16; say you assumed the simplest rule. If the series is 2, 4, 8, 14, ? then rule B is now forced, next is 22.
**Common mistakes / traps:** Spending two minutes proving the rule is the only one. Also picking a clever, complicated rule when a plain one fits.

### Q28 ⭐⭐ 🟢 A test gives 20 series, analogy and classification questions in 15 minutes. How many seconds can you spend per question, and what is your rule for skipping?
**Asked at:** commonly asked (no company-specific report found); the timing here is arithmetic only, and test formats reported by prep sites are unverified
**What the interviewer is checking:** Time budgeting under pressure and discipline to skip.
**Say this in the interview:** "Fifteen minutes is 900 seconds, divided by 20 is 45 seconds each. If I have no rule after about 30 to 40 seconds I mark it and move on, and come back if time remains."
**Answer:** **45 seconds per question on average.**
**Step-by-step reasoning:**
1. 15 minutes x 60 = 900 seconds.
2. 900 / 20 = 45 seconds per question (computed by script).
3. These are short questions, so many take 15 to 20 seconds. Those fast ones bank time for harder ones.
**Fast method (30 seconds):** Our suggestion (not a research finding): give every question a first look of about 30 seconds. If you have found no rule by then, mark it, guess if there is no negative marking, and move on. Return at the end with the saved time.
**Check:** 20 x 45 = 900 seconds = 15 minutes.
**Explain simply:**
- "Average" means some questions take less and some more; you do not have to stop at 45 on each.
- Skipping is a score tool: one stuck question at 3 minutes costs about four easy ones.
- If the test has negative marking (a penalty for wrong answers) check the rule before guessing; if not, always guess before time ends.
**Likely follow-ups:** What if there are 25 questions in 15 minutes? 900 / 25 = 36 seconds each, so skip even sooner (around 25 seconds).
**Common mistakes / traps:** Stubbornly staying on one series; leaving blanks when there is no penalty; forgetting to leave about a minute at the end to fill guesses.

### Q29 ⭐⭐ 🟢 Pivot table is to summarising as filter is to what? (a) Selecting (b) Sorting (c) Deleting (d) Joining
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Tool and purpose analogy: matching a spreadsheet feature to its main job.
**Say this in the interview:** "A pivot table's job is to summarise data; a filter's job is to select the rows you want to see. So (a) Selecting."
**Answer:** **(a) Selecting**
**Step-by-step reasoning:**
1. Make a sentence: "A pivot table is used for summarising, and a filter is used for ___."
2. A filter shows only the rows that meet a condition, which is selecting.
3. Check each option: Sorting only reorders rows, and every row stays visible. Deleting removes data, while a filter only hides rows and does not erase them. Joining combines two tables, which a filter does not do.
**Fast method (30 seconds):** Use "tool and its main purpose" and write the sentence. Eliminate options that describe a different tool (sort, join).
**Check:** Hand-checked. Rule used: tool to purpose. No second defensible rule exists; "sorting" fails because sorting keeps all rows.
**Explain simply:**
- A filter hides the rows you do not want and keeps the rows you do. That keeping is "selecting".
- A pivot table turns many rows into a short summary (totals, counts).
**Likely follow-ups:** Chart is to visualising as sort is to what? Ordering (arranging rows in a sequence).
**Common mistakes / traps:** Choosing "Deleting" because filtered-out rows disappear from view; they are only hidden.

### Q30 ⭐⭐ 🟡 Complete the series: A1Z, B4Y, C9X, D16W, ?
**Asked at:** commonly asked (no company-specific report found); the split-into-tracks method is described by prep sites (unverified)
**What the interviewer is checking:** Three tracks at once: forward letters, square numbers, backward letters.
**Say this in the interview:** "First letters go A, B, C, D, E; the numbers are 1, 4, 9, 16, so 25; the last letters go backward Z, Y, X, W, so V. Answer E25V."
**Answer:** **E25V**
**Step-by-step reasoning:**
1. Split each term into three parts: first letter, number, last letter.
2. First letters: A, B, C, D go forward by 1, so next is E.
3. Numbers: 1, 4, 9, 16 are 1x1, 2x2, 3x3, 4x4 (squares), so next is 5x5 = 25.
4. Last letters: Z, Y, X, W go backward by 1 (26, 25, 24, 23), so next is V (22).
5. Join: E25V.
**Fast method (30 seconds):** Treat each part as its own mini-series. Positions also help: first letter at position n, last letter at position 27 minus n, and the number is n squared.
**Check:** Verified by script: term n = (letter n, n squared, letter 27 minus n) reproduces A1Z, B4Y, C9X, D16W and gives E25V.
**Explain simply:**
- A square number is a number multiplied by itself (4 = 2x2).
- Mirror letters: the pair of letters at positions n and 27 minus n are opposite ends of the alphabet.
**Likely follow-ups:** What is the 6th term? F36U.
**Common mistakes / traps:** Reading 1, 4, 9, 16 as +3, +5, +7 (this also gives 25, but squares tell you why). Forgetting the last letter runs backward.

### Q31 ⭐⭐ 🟡 Complete the series: ZYX, VUT, RQP, ?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Group series where letters inside a group and between groups both move backward.
**Say this in the interview:** "Each group is three letters going backward, and each group starts 4 letters before the last one started: Z, V, R, so N. The group is NML."
**Answer:** **NML**
**Step-by-step reasoning:**
1. Convert to numbers: ZYX = 26, 25, 24; VUT = 22, 21, 20; RQP = 18, 17, 16.
2. Inside each group the letters step down by 1.
3. The first letters 26, 22, 18 drop by 4 each time, so the next first letter is 14 = N.
4. Group: 14, 13, 12 = N, M, L.
**Fast method (30 seconds):** Look only at the first letters of each group, find their step (-4), then write the rest of the group by the inside rule.
**Check:** Verified by script (groups generated from start 26 - 4g with step -1 reproduce all three given groups).
**Explain simply:**
- Two-level pattern: one rule inside a group, another rule from group to group.
- Between groups: X (24) to V (22) is a step of 2, so one letter (W) is skipped. That is why first letters drop by 4: 3 letters are used and 1 is skipped.
**Likely follow-ups:** The group after NML? JIH (10, 9, 8).
**Common mistakes / traps:** Continuing alphabetically from the last letter (X, W, V, ...) and getting WVU.

### Q32 ⭐⭐ 🟡 In the series B, E, H, K, N, Q, S, W, one term is wrong. Which term is it, and what should it be?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Spotting the wrong term (an anomaly) by finding the dominant rule first.
**Say this in the interview:** "The rule is plus 3. B, E, H, K, N, Q, then T, W. The S is wrong and should be T."
**Answer:** **S is wrong; it should be T.**
**Step-by-step reasoning:**
1. Positions: B=2, E=5, H=8, K=11, N=14, Q=17, S=19, W=23.
2. Differences: +3, +3, +3, +3, +3, +2, +4. Most steps are +3.
3. If the 7th term were T (20) the steps would be +3 then +3 (T to W = 20 to 23), so the rest of the series is saved by changing one term.
4. Changing only S to T makes every step +3, so S is the single wrong term (W is consistent with T + 3).
**Fast method (30 seconds):** Find the step that most pairs share, extend the series from the first term, and see where it first disagrees.
**Check:** Verified by script: B plus 3 each time generates B, E, H, K, N, Q, T, W; only the 7th term differs from the given one.
**Explain simply:**
- This is like spotting an outlier: first learn the normal pattern, then see what breaks it.
- The two odd differences (+2, +4) are a signature of one swapped term, since they add up to 6 = 2 x 3.
**Likely follow-ups:** In B, E, H, L, N, Q, T which is wrong? L (12) should be K (11).
**Common mistakes / traps:** Blaming W because it is the last term, or saying two terms are wrong.

### Q33 ⭐⭐ 🟡 Letter series with wrap-around: A, B, D, H, P, ? What is the next letter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Doubling rule plus wrap-around past Z.
**Say this in the interview:** "Positions are 1, 2, 4, 8, 16, doubling. Next is 32, which is past 26, so subtract 26 to get 6, which is F."
**Answer:** **F**
**Step-by-step reasoning:**
1. A=1, B=2, D=4, H=8, P=16.
2. Each is double the one before.
3. Next is 32. The alphabet has only 26 letters, so wrap around: 32 - 26 = 6.
4. Position 6 is F.
**Fast method (30 seconds):** Convert to numbers; when the number passes 26, subtract 26 (the alphabet restarts after Z, so 27 is A again).
**Check:** Verified by script: powers of 2 mapped to letters give A, B, D, H, P, then 32 maps to F.
**Explain simply:**
- Wrap-around means after Z you go back to A, like a clock after 12.
- A second reading: differences 1, 2, 4, 8, 16 (also doubling) lead to the same value, 16 + 16 = 32.
**Likely follow-ups:** The term after F? Double 32 gives 64; 64 - 52 = 12, which is L.
**Common mistakes / traps:** Stopping at 32 and saying "no such letter"; or subtracting 26 only when the result is above 52.

### Q34 ⭐⭐ 🟡 Complete the mixed series: Z, 1, Y, 4, X, 9, W, ?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Two interleaved series (alternate terms) that follow separate rules.
**Say this in the interview:** "Odd positions are letters going backward: Z, Y, X, W. Even positions are squares: 1, 4, 9, so next is 16."
**Answer:** **16**
**Step-by-step reasoning:**
1. Pull out the terms in odd positions: Z, Y, X, W (backward by 1).
2. Pull out even positions: 1, 4, 9, ? (squares 1x1, 2x2, 3x3).
3. The missing term is in position 8 (even), so it is 4x4 = 16.
**Fast method (30 seconds):** When letters and numbers alternate, split them into two series. Then ask which track the question mark sits on.
**Check:** Verified by script (squares 1, 4, 9, 16 and the letters Z, Y, X, W fit every given term).
**Explain simply:**
- Interleaved means two series woven together, term by term.
- Differences 3, 5, 7 between the squares confirm the pattern.
**Likely follow-ups:** What comes after 16? The letter V.
**Common mistakes / traps:** Looking for one rule across all terms; or answering a letter (V) when the missing position is a number.

### Q35 ⭐⭐ 🟡 In the table below, each row follows the same rule. Find the missing number.

| Row | Col 1 | Col 2 | Col 3 |
|---|---|---|---|
| 1 | 2 | 3 | 6 |
| 2 | 4 | 5 | 20 |
| 3 | 6 | 7 | ? |
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Finding a row rule that works for the complete rows, then applying it.
**Say this in the interview:** "Column 3 is Column 1 times Column 2: 2x3=6, 4x5=20, so 6x7=42."
**Answer:** **42**
**Step-by-step reasoning:**
1. Try the simplest operation on row 1: 2 and 3 give 6. Sum is 5, product is 6, so product fits.
2. Test on row 2: 4 x 5 = 20 matches.
3. Apply to row 3: 6 x 7 = 42.
**Fast method (30 seconds):** Try add, subtract, multiply on the first row, and confirm on the second row before using it. Two rows both matching removes most doubts.
**Check:** Verified by script: products of Col 1 and Col 2 are 6, 20, 42. No other simple rule (sum, difference, square of one column) fits both rows; the natural variants Col 1 x (Col 1 + 1) and Col 2 x (Col 2 - 1) also give 42 (only two complete rows exist, so very contrived formulas could differ).
**Explain simply:**
- A row rule must work for every row that has all its numbers.
- Product means multiplication.
**Likely follow-ups:** If row 4 is 8, 9, ? it is 72.
**Common mistakes / traps:** Stopping after one row; a rule like "Col 2 squared minus 3" fits row 1 (9 - 3 = 6) but fails row 2 (25 - 3 = 22).

### Q36 ⭐⭐ 🟡 The letters of the word REPORTING are arranged in alphabetical order (repeated letters kept). Which letter is fourth from the right end?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Careful sorting and counting from the right, keeping repeats.
**Say this in the interview:** "Sorted, REPORTING is E, G, I, N, O, P, R, R, T. Fourth from the right is P."
**Answer:** **P**
**Step-by-step reasoning:**
1. Letters of REPORTING: R, E, P, O, R, T, I, N, G (9 letters, R appears twice).
2. Alphabetical order: E, G, I, N, O, P, R, R, T.
3. From the right: 1st T, 2nd R, 3rd R, 4th P.
**Fast method (30 seconds):** Count the letters first (9) so you do not drop the repeated R. Fourth from the right is position 9 - 4 + 1 = 6 from the left, and the 6th letter is P.
**Check:** Verified by script: sorted list has 9 letters and the 4th from the end is P.
**Explain simply:**
- "Repeated letters kept" means the two Rs both stay, and both take a place.
- From the right to from the left: position from left = total + 1 - position from right.
**Likely follow-ups:** Which letter is second from the left? G.
**Common mistakes / traps:** Dropping one R (then the answer shifts to N or O); counting from the left.

### Q37 ⭐⭐ 🟡 Find the odd one out: B2, D8, F18, H32, J49.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Two-track odd-one-out: split letter and number, find the rule, spot the break.
**Say this in the interview:** "Letters go up by 2 positions each time. The numbers are 2 times the square of 1, 2, 3, 4, 5, which is 2, 8, 18, 32, 50. So J49 is the odd one; it should be J50."
**Answer:** **J49**
**Step-by-step reasoning:**
1. Letters: B, D, F, H, J = positions 2, 4, 6, 8, 10 (steps of 2). All fit.
2. Numbers: 2, 8, 18, 32, 49. Each of the first four is 2 x n squared: 2x1, 2x4, 2x9, 2x16.
3. The fifth should be 2 x 25 = 50, but the term shows 49.
4. So J49 breaks the rule.
**Fast method (30 seconds):** Number = 2 x (n squared), where n is the term's place (1 to 5). A quick tell: the first four numbers are even and 49 is odd.
**Check:** Verified by script: terms for n = 1 to 5 are B2, D8, F18, H32, J50. Only the last differs. A second view, "odd number among evens", also picks J49, so the two views agree.
**Explain simply:**
- Odd one out means the one item that does not follow the pattern the others share.
- The letter track is fine for all five, so the oddity is only in the number track.
**Likely follow-ups:** What is the next term after J50? L72 (letter position 12, 2 x 36 = 72).
**Common mistakes / traps:** Looking at the letters, which are all regular, and concluding there is no odd one.

### Q38 ⭐⭐ 🟡 In the word PIVOTS, how many pairs of letters have as many letters between them in the word as they have between them in the English alphabet? (Count each pair of positions once.)
**Asked at:** commonly asked (no company-specific report found); alphabet-test counting questions are a prep-site topic (unverified)
**What the interviewer is checking:** Systematic pair counting without missing or double counting.
**Say this in the interview:** "There are 15 pairs in PIVOTS. Comparing the gap in the word with the gap in the alphabet for each, four match: P-T, V-T, V-S and T-S. Answer 4."
**Answer:** **4 pairs**
**Step-by-step reasoning:**
1. Alphabet positions: P=16, I=9, V=22, O=15, T=20, S=19. Word positions: P1, I2, V3, O4, T5, S6.
2. 6 letters give 6 x 5 / 2 = 15 pairs. "Letters between" matches exactly when the gap in word positions equals the gap in alphabet positions (the number between is the gap minus 1 in both cases).
3. Matching pairs:
   - P and T: word gap 4 (1 to 5), alphabet gap 4 (16 to 20). Match, 3 letters between.
   - V and T: word gap 2, alphabet gap 2 (22 to 20). Match, 1 between.
   - V and S: word gap 3, alphabet gap 3 (22 to 19). Match, 2 between.
   - T and S: word gap 1, alphabet gap 1 (20 to 19). Match, 0 between.
4. The other 11 pairs do not match, for example I and O: word gap 2, alphabet gap 6.
**Fast method (30 seconds):** Write the alphabet number under each letter and list the 15 pairs in order (P with five others, I with four, and so on) so none is missed. Compare the two gaps for each.
**Check:** Verified by script over all 15 pairs: exactly 4 match.
**Explain simply:**
- "Pairs" means any two different letters; order does not matter, so P-T and T-P are the same pair.
- Between-count is the gap minus 1 on both sides, so comparing gaps is enough.
- Adjacent pairs (nothing between) count too: T-S has none between in both.
**Likely follow-ups:** If the pairs must have at least one letter between them? Remove T-S, giving 3.
**Common mistakes / traps:** Counting adjacent letters only in the word but forgetting the alphabet check; counting both P-T and T-P; missing pairs when listing by eye.

### Q39 ⭐⭐ 🟡 In the sequence R 4 K 7 M 2 T 9 L 5 D 3 A 8 N 6 E, how many consonants are immediately followed by an even digit?
**Asked at:** commonly asked (no company-specific report found); alphabet-test counting items appear in prep-site lists (unverified).
**What the interviewer is checking:** Careful scanning against two conditions at once (letter type and the next item's type).
**Say this in the interview:** "I go left to right, and for each consonant I look only at the very next symbol. R then 4, M then 2 and N then 6 qualify. The answer is 3."
**Answer:** **3** (R-4, M-2, N-6).
**Step-by-step reasoning:**
1. A consonant is any letter that is not A, E, I, O, U. An even digit is 0, 2, 4, 6 or 8.
2. Walk through each letter and its right-hand neighbour: R→4 (even, count), K→7 (odd), M→2 (even, count), T→9 (odd), L→5 (odd), D→3 (odd), A→8 (A is a vowel, so skip), N→6 (even, count). E is last and has nothing after it.
3. Total = 3.
**Fast method (30 seconds):** Circle the even digits (4, 2, 6, 8) first, then look at the symbol just before each: R, M, A, N. Drop the vowel A. That leaves 3.
**Check:** Verified by script.
**Explain simply:**
- "Immediately followed by" means the very next symbol, not somewhere later.
- Starting from the digits you want is faster than starting from every letter.
**Likely follow-ups:** 1) *How many vowels are followed by an even digit?* One (A-8). 2) *How many digits are immediately preceded by a consonant?* Seven (4, 7, 2, 9, 5, 3, 6); A is the only letter before a digit that is not a consonant (8), (verified by script).
**Common mistakes / traps:** Counting A-8 because the digit is even; counting "next even digit anywhere later"; forgetting that the sequence ends on E with no follower.

### Q40 ⭐⭐ 🟡 Find the odd one out: CEG, HJL, MOQ, RTU, WYA.
**Asked at:** commonly asked (no company-specific report found); odd-one-out letter clusters are listed in TCS NQT prep material (unverified).
**What the interviewer is checking:** Converting letters to positions (A=1 to Z=26) and testing a gap rule on every group.
**Say this in the interview:** "Each group should jump by 2 and then by 2. RTU is 18, 20, 21, so its second jump is 1. RTU is the odd one out."
**Answer:** **RTU** (the pattern would need RTV).
**Step-by-step reasoning:**
1. Convert to positions: CEG = 3, 5, 7; HJL = 8, 10, 12; MOQ = 13, 15, 17; RTU = 18, 20, 21; WYA = 23, 25, 1.
2. Gaps inside each group: 2 and 2, 2 and 2, 2 and 2, 2 and 1, 2 and 2.
3. WYA looks strange but wraps round: after Z (26) comes A (1), so 25 to 27 is 1, and the gap is still 2.
4. The first letters C, H, M, R, W step by 5 each time, which RTU also fits, so only its last letter breaks the rule.
**Fast method (30 seconds):** Say "every other letter" under your breath: C-(D)-E-(F)-G. Check each group the same way and stop at the group that does not fit.
**Check:** Verified by script (gaps modulo 26). Only one rule is defensible here.
**Explain simply:**
- Wrap-around means the alphabet is a circle: Z is followed by A.
- Compare the pattern inside each group and also between groups.
**Likely follow-ups:** 1) *If the odd group were fixed, what would replace it?* RTV. 2) *What would the next group after WYA be?* BDF (first letter +5 wraps to B).
**Common mistakes / traps:** Picking WYA because it contains Y and A far apart; forgetting the wrap.

### Q41 ⭐⭐ 🟡 A pattern is written in groups: A, BB, CCC, DDDD, and so on up to Z. What is the 50th letter written?
**Asked at:** commonly asked (no company-specific report found); grouped-letter patterns are a standard series format.
**What the interviewer is checking:** Turning a pattern into a running total (triangular numbers) rather than writing everything out.
**Say this in the interview:** "The nth letter appears n times, so after n letters I have written 1+2+...+n. That is 45 after I, and 55 after J. The 50th falls inside the J group, so it is J."
**Answer:** **J**
**Step-by-step reasoning:**
1. The k-th letter of the alphabet is written k times (A once, B twice, and so on).
2. Running totals: after A 1, B 3, C 6, D 10, E 15, F 21, G 28, H 36, I 45, J 55.
3. Position 50 is more than 45 and at most 55, so it lies in the J group (positions 46 to 55). I is letter 9, J is letter 10.
**Fast method (30 seconds):** The sum 1+2+...+n equals n(n+1)/2. Try n = 9: 45 (too small), n = 10: 55 (enough). Letter number 10 is J. This works because the groups get longer by one each time.
**Check:** Verified by script (full string of 351 letters, 50th is J).
**Explain simply:**
- Numbers like 1, 3, 6, 10, 15 are called triangular numbers (dots stacked in a triangle).
- You find the group by asking which running total first reaches 50.
**Likely follow-ups:** 1) *What is the 100th letter?* Totals: N=105, M=91, so the 100th is N (checked by hand). 2) *How many letters are written in all?* 26 x 27 / 2 = 351.
**Common mistakes / traps:** Dividing 50 by 2 or 5 and guessing; stopping at 45 and answering I.

### Q42 ⭐⭐ 🟡 Find the missing number in the table. All rows follow the same rule.

| Row | Col 1 | Col 2 | Col 3 |
|---|---|---|---|
| 1 | 5 | 3 | 22 |
| 2 | 6 | 4 | 32 |
| 3 | 7 | 2 | 47 |
| 4 | 8 | 5 | ? |
**Asked at:** commonly asked (no company-specific report found); row-rule grids are a standard reasoning format.
**What the interviewer is checking:** Hypothesis testing: try a rule on one row, then confirm it on all the others.
**Say this in the interview:** "The third column is 22, 32, 47, which sit just below the squares 25, 36, 49. The gaps are 3, 4, 2, exactly Col 2. So Col 3 = Col 1 squared minus Col 2. For row 4: 64 minus 5 is 59."
**Answer:** **59**
**Step-by-step reasoning:**
1. Look for a big number near a simple function of Col 1. 5 gives 22, 6 gives 32, 7 gives 47. Squares are 25, 36, 49.
2. Differences: 25 - 22 = 3, 36 - 32 = 4, 49 - 47 = 2. These equal Col 2 in each row.
3. So the rule is Col 1 x Col 1 - Col 2.
4. Row 4: 8 x 8 = 64; 64 - 5 = 59.
**Fast method (30 seconds):** Numbers that grow faster than steadily (22, 32, 47 for inputs 5, 6, 7) hint at squares. Compare to squares, then see what is left over.
**Check:** Rule re-applied to rows 1 to 3 (22, 32, 47, all match). A script search over formulas with small whole coefficients (squares and product of the columns, each column, and a constant) found two other fits, but each needs six non-zero terms and they give 56 and 62; Col 1 squared minus Col 2 is by far the simplest, so it is the rule used.
**Explain simply:**
- Three rows that fit one rule give good evidence; the fourth row is the prediction.
- "Squared" means a number multiplied by itself.
**Likely follow-ups:** 1) *If row 4 were 9 and 6?* 81 - 6 = 75. 2) *Why not guess a pattern in Col 3 alone?* Gaps 10 then 15 give no clean rule, so the columns must be used together.
**Common mistakes / traps:** Treating Col 3 as its own number series; testing the rule on only one row.

### Q43 ⭐ 🟢 Why does the question "Find the odd one out: 2, 3, 5, 9, 11" feel ambiguous at first, and what is the standard way to decide the answer?
**Asked at:** commonly asked (no company-specific report found); odd-one-out is a practised company-test topic per prep sites (unverified).
**What the interviewer is checking:** Whether you can list competing rules and choose the best one with a reason, not by gut feel.
**Say this in the interview:** "At least three rules each isolate one number: 2 is the only even, 9 is the only non-prime, 11 is the only two-digit number. The standard choice is the rule that splits the set into a named mathematical class versus one outsider, which is prime versus not prime, so 9."
**Answer:** **9 is the intended answer** (the only number that is not prime), but 2 and 11 are also defensible under other rules.
**Explain simply:**
- Odd-one-out means find the item that fails a property all the others share. Many properties exist, so first list them.
- Properties found: parity (only 2 is even), primality (only 9 is not prime), digit count (only 11 has two digits).
- Choosing rule: prefer the property with a standard name (prime), where the four majority items form a recognised group. "Two-digit" is a surface feature, and "even" would make 2 odd one out even though 2 is prime and belongs to the prime group with 3, 5 and 11.
- In a real test the option list or the question's topic often decides; if you can ask, ask.
**Worked mini-example:** Test the set {2, 3, 5, 9, 11} against each rule: prime? yes, yes, yes, NO, yes (one outsider, 9). Even? YES, no, no, no, no (one outsider, 2). Verified by script for the prime test.
**Likely follow-ups:** 1) *What if the list were 2, 3, 5, 7, 9?* Still 9 (non-prime), and now 2 is the only even as well; two rules, two answers again. 2) *What if the options did not include 9?* Then fall back to the next rule that points to an option present.
**Common mistakes / traps:** Stopping at the first rule you notice; picking 2 because "even" is easy to see; not saying out loud which rule you used.

### Q44 ⭐ 🟡 How does the skill of spotting patterns in series connect to analyst work such as finding trends, seasonality and anomalies, and where does the analogy break down?
**Asked at:** commonly asked (no company-specific report found); this is a "why does this test matter" style question, and no source reports it at a specific company.
**What the interviewer is checking:** Whether you see reasoning drills as practice for real data work, and know the difference between a puzzle and real data.
**Say this in the interview:** "Both ask what rule produces these values. A series puzzle has one exact rule; real data has trend, repeating seasonality and noise, and I must test a pattern, not just spot it."
**Answer:** **Series puzzles train the same habits as trend, seasonality and anomaly spotting, but real data is noisy, has no guaranteed single rule, and needs checking before you trust a pattern.**
**Explain simply:**
- Trend means a steady drift up or down; seasonality means a pattern that repeats on a calendar cycle (like weekly sales peaks). An anomaly is a point that breaks the pattern, like the wrong term in "B, E, H, K, N, Q, S, W" (S should be T).
- Same moves: split into tracks (a letter track and a number track is like separating trend from seasonal part), compare each term with the previous one (differences), and check the rule against every point.
- Where it breaks down: a puzzle has exactly one intended rule and no errors; data has randomness, missing values and several rules that fit equally well. A fitted pattern can be a coincidence, so we validate on held-back data and ask the business whether a cause exists.
- An outlier in data may be a real event or a data entry error; the puzzle never makes you decide that.
**Worked mini-example:** Weekly sales: 100, 120, 100, 121, 100, 119. Rule: alternating. Differences: +20, -20, +21, -21, +19. The pattern fits within small noise (+/-1), which a puzzle would not have. Hand-checked.
**Likely follow-ups:** 1) *How would you tell a seasonal spike from an anomaly?* See whether it repeats at the same calendar point in other cycles. 2) *Is an exact-rule fit proof of the rule?* No: with few points many rules fit.
**Common mistakes / traps:** Claiming a pattern from three points; treating every outlier as an error; forgetting that cause needs business context.

### Q45 ⭐ 🟡 RISK is to SKVO as DATA is to what? (Use the same rule for both.)
**Asked at:** commonly asked (no company-specific report found); letter-shift analogies appear in TCS NQT style prep material (unverified).
**What the interviewer is checking:** Finding a position-dependent shift rule by comparing letter by letter.
**Say this in the interview:** "R to S is +1, I to K is +2, S to V is +3, K to O is +4. Each letter moves forward by its position number. Apply that to DATA: E, C, W, E."
**Answer:** **ECWE**
**Step-by-step reasoning:**
1. Convert RISK to numbers: R=18, I=9, S=19, K=11. SKVO is 19, 11, 22, 15.
2. Differences: +1, +2, +3, +4. The shift grows by one with each position.
3. DATA is 4, 1, 20, 1. Add 1, 2, 3, 4: 5, 3, 23, 5.
4. Back to letters: E, C, W, E.
**Fast method (30 seconds):** Compare only the first two pairs; if the shifts are 1 then 2, test "position number" on the rest. It then explains all four letters at once.
**Check:** Verified by script (same rule gives SKVO from RISK and ECWE from DATA). A constant shift fails (R to S is +1 but I to K is +2), so only this rule fits.
**Explain simply:**
- "Position-dependent shift" means the first letter moves 1, the second 2, and so on.
- Letters wrap past Z back to A if needed (not needed here).
**Likely follow-ups:** 1) *Apply to LOGIC?* M, Q, J, M, H (verified by hand: L+1, O+2, G+3, I+4, C+5 = M, Q, J, M, H). 2) *What if the shifts went backwards?* Subtract instead.
**Common mistakes / traps:** Using a constant +1 or +2 shift; giving ECUE or similar after miscounting T+3 (T is 20, so 23 is W).

### Q46 ⭐ 🟡 G is to 49 as K is to what?
**Asked at:** commonly asked (no company-specific report found); letter-to-number analogies appear in prep-site lists (unverified).
**What the interviewer is checking:** Mapping letter to position, then spotting the operation (squaring).
**Say this in the interview:** "G is the 7th letter, and 7 squared is 49. K is the 11th letter, so the answer is 121."
**Answer:** **121**
**Step-by-step reasoning:**
1. Count positions: A=1 ... G=7; K=11.
2. Find how 7 becomes 49: 7 x 7. (Other tries like 7 + 42 have no clean link to the letter.)
3. Apply to K: 11 x 11 = 121.
**Fast method (30 seconds):** When the number is a perfect square of the letter position, answer by squaring. Memorise A to M: A1 ... K11 L12 M13.
**Check:** Verified by script (K = 11, 11 squared = 121). A second defensible rule is hard to find; "position squared" is the simple one.
**Explain simply:**
- Letter position means its place in the alphabet.
- Squared means multiplied by itself.
**Likely follow-ups:** 1) *If G were to 14?* Position times 2, so K gives 22. 2) *What is the answer for Z?* 26 x 26 = 676.
**Common mistakes / traps:** Counting K as 10; answering 11 x 7 or 77.

### Q47 ⭐ 🟡 Complete the series: A2C, D6F, G18I, J54L, ?
**Asked at:** commonly asked (no company-specific report found); alphanumeric series are a standard format in prep sites.
**What the interviewer is checking:** Splitting a mixed term into tracks and finding the rule in each.
**Say this in the interview:** "I split each term into first letter, number, last letter. First letters move +3 (A, D, G, J, M), the numbers multiply by 3 (2, 6, 18, 54, 162), and the last letter is always 2 after the first. Answer: M162O."
**Answer:** **M162O**
**Step-by-step reasoning:**
1. First letters: A, D, G, J are positions 1, 4, 7, 10; step +3, so next is 13 = M.
2. Numbers: 2, 6, 18, 54; each is 3 times the last, so next is 162.
3. Last letters: C, F, I, L are positions 3, 6, 9, 12; step +3, so next is 15 = O (also always first letter +2).
4. Join: M, 162, O.
**Fast method (30 seconds):** Treat each track separately; the number track in the middle is the only one that is not a +3 step. Confirm every track fits all four terms.
**Check:** Verified by script (M, 162, O).
**Explain simply:**
- A "track" is one strand of the pattern (letters or numbers) that follows its own rule.
- Multiplying by a constant (x3) is called a geometric pattern; adding a constant is arithmetic.
**Likely follow-ups:** 1) *Next after M162O?* P486R. 2) *What if the numbers went 2, 6, 12, 20?* Differences 4, 6, 8, so the next is 30 (a different rule; verified by hand).
**Common mistakes / traps:** Adding a constant: the differences 4, 12, 36 are not constant, so the rule is multiplying; wrong +3 counting on letters.

### Q48 ⭐ 🟡 Letter series with two tracks: YA, ZC, AE, ?
**Asked at:** commonly asked (no company-specific report found); wrap-around two-track series appear in prep material (unverified).
**What the interviewer is checking:** Tracking two independent letter sequences and handling wrap-around.
**Say this in the interview:** "First letters go Y, Z, A, B (wrapping past Z, +1 each time). Second letters go A, C, E, G (+2 each time). Next term is BG."
**Answer:** **BG**
**Step-by-step reasoning:**
1. First track: Y=25, Z=26, then A=1 (after Z wraps to 1), so +1 each step. Next is B.
2. Second track: A=1, C=3, E=5, step +2. Next is G=7.
3. Join the two: BG.
**Fast method (30 seconds):** Write the first letters on one line and the second letters on another; each line is a simple count, forward by 1 or skipping 1.
**Check:** Hand-checked (Y, Z, A, B and A, C, E, G; both fit all three given terms). Only one rule is defensible.
**Explain simply:**
- Wrap-around means Z is followed by A again.
- Two tracks are solved one at a time, then recombined.
**Likely follow-ups:** 1) *What is the term after BG?* CI. 2) *What if the second track were A, C, F?* Then the gaps would be 2 and 3 (a growing step), and the next would be J (hand-checked); here the gaps are steady at 2.
**Common mistakes / traps:** Forgetting that A follows Z; answering AG or BF by treating both letters with the same step.

### Q49 ⭐ 🟡 The series A, B, C, D, C, B, A, B, C, D, C, B, ... repeats in the same way. What is the 100th term?
**Asked at:** commonly asked (no company-specific report found); repeating-cycle questions are a standard series format.
**What the interviewer is checking:** Finding the length of the repeating block and using remainders instead of writing everything out.
**Say this in the interview:** "The repeating block is A, B, C, D, C, B, which is 6 long. 100 divided by 6 leaves remainder 4, so the 100th term is the 4th item in the block, which is D."
**Answer:** **D**
**Step-by-step reasoning:**
1. Find the block that repeats: A, B, C, D, C, B, then A starts again, so the block has 6 terms.
2. 100 = 6 x 16 + 4. After 16 full blocks (96 terms), 4 more terms are needed.
3. The 4th term of the block is D.
**Fast method (30 seconds):** Use the remainder after dividing by the block length. If the remainder is 0, the answer is the last item of the block (here the 6th, B). This works because every full block puts you back at the start.
**Check:** Verified by script (indexing position 99 in zero-based ABCDCB).
**Explain simply:**
- A "period" is the length of the repeating block.
- The remainder tells you where you are inside the current block.
**Likely follow-ups:** 1) *What is the 102nd term?* 102 is 6 x 17, remainder 0, so the last item, B. 2) *What is the 50th?* 50 = 6 x 8 + 2, so B (hand-checked).
**Common mistakes / traps:** Using 7 as the period (A repeats at the start of the next block, not inside this one); treating remainder 0 as the first item.

### Q50 ⭐ 🟡 If all five vowels are removed from the English alphabet, which letter is 10th from the left in the remaining letters?
**Asked at:** commonly asked (no company-specific report found); alphabet-test counting items appear in prep-site lists (unverified).
**What the interviewer is checking:** Careful counting after deleting items, without overcounting.
**Say this in the interview:** "Vowels are A, E, I, O, U. Remaining letters in order: B, C, D, F, G, H, J, K, L, M. The 10th is M."
**Answer:** **M**
**Step-by-step reasoning:**
1. Remove A, E, I, O, U. Left: B, C, D, F, G, H, J, K, L, M, N, P, and so on.
2. Count: B1, C2, D3, F4, G5, H6, J7, K8, L9, M10.
3. The 10th letter is M.
**Fast method (30 seconds):** M is the 13th letter of the alphabet and three vowels (A, E, I) come before it; 13 - 3 = 10. This is quicker than listing, and it works because each removed letter before the target moves it one place earlier.
**Check:** Verified by script (list of 21 consonants, index 10 is M).
**Explain simply:**
- Only vowels removed before M change its place; O and U come later, so they do not affect it.
- "From the left" means counting from A's end of the alphabet.
**Likely follow-ups:** 1) *Which letter is 10th from the right?* 21 letters remain, so the 10th from the right is the 12th from the left, P (verified by script). 2) *What if only A and E were removed?* The 10th letter becomes L (verified by script).
**Common mistakes / traps:** Counting from 10 in the full alphabet (J); including Y as a vowel.
