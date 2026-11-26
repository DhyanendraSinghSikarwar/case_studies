# Book 13 — Logical Reasoning & Analytical Thinking | Part 5: Multi-Attribute Puzzles, Constraint Puzzles and Truth-Teller/Liar 🔴

**Target:** 70 questions | **Actual:** 70 questions
**Scope:** Who-owns-what grids, schedules and sessions, selection and constraint puzzles, digit and code puzzles, tournaments and points tables, and knight/knave (truth-teller and liar) puzzles, plus method questions; sorted by stars then difficulty; seating, floor and month/day arrangements belong to Part 4.

### Q1 ⭐⭐⭐ 🟢 Four new joiners Esha, Farid, Gita and Hari are each hired into a different role: Analyst, Auditor, Recruiter and Trainer (one role each). Clues: (1) Esha is neither Analyst nor Auditor. (2) Farid is neither Recruiter nor Trainer. (3) Gita is not Analyst, not Trainer and not Auditor. (4) Hari is not Auditor. Who is the Auditor?
**Asked at:** commonly asked (no company-specific report found); matching-grid puzzles are listed in prep-site topic lists for TCS, Infosys, Wipro, Accenture and Cognizant (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can use "is not" clues to eliminate until one option is left.
**Say this in the interview:** "Gita can only be Recruiter. That leaves Esha as Trainer, Farid as Analyst or Auditor, and Hari not Auditor, so Farid is the Auditor and Hari is the Analyst."
**Answer:** **Farid is the Auditor.** (Esha = Trainer, Farid = Auditor, Gita = Recruiter, Hari = Analyst.)
**Step-by-step reasoning:**
1. Gita is not Analyst, Trainer or Auditor, so Gita = Recruiter.
2. Recruiter is now taken. Esha is not Analyst or Auditor, so Esha = Trainer.
3. Farid is not Recruiter or Trainer, so Farid is Analyst or Auditor.
4. Left roles for Farid and Hari: Analyst and Auditor. Hari is not Auditor, so Hari = Analyst and Farid = Auditor.

| Person | Role |
|---|---|
| Esha | Trainer |
| Farid | Auditor |
| Gita | Recruiter |
| Hari | Analyst |

The answer is unique because every step above was forced; there was never a choice.
**Fast method (30 seconds):** Start with the person who has the fewest allowed roles (Gita, only one left). Then repeat with whoever is now down to one option.
**Check:** Re-read the four clues against the table: all hold. Checked by brute force over all 24 assignments; exactly one fits.
**Explain simply:**
- A "grid puzzle" gives each person exactly one item from each list, so crossing out one option often forces another.
- A clue that says "not X" is a cross in the grid; a person with only one uncrossed cell is decided.
**Likely follow-ups:** 1) *What if clue 4 were removed?* Then Farid and Hari could swap Analyst and Auditor, so there would be 2 solutions (by script); clue 4 is needed. 2) *How many arrangements exist with no clues?* 4! = 24.
**Common mistakes / traps:** Starting with Esha or Hari (each has two options) and guessing; or forgetting that the role Gita gets is removed from everyone else.

### Q2 ⭐⭐⭐ 🟢 On an island every inhabitant is either a knight (always tells the truth) or a knave (always lies). A says: "B is a knave." B says: "A and I are of the same type." What are A and B?
**Asked at:** commonly asked (no company-specific report found); a knights-and-knaves item appears in an interview-question bank (unverified summary, page not read).
**What the interviewer is checking:** Testing both assumptions for one speaker and following the consequence.
**Say this in the interview:** "Suppose A is a knight. Then B is a knave, so B's claim 'we are the same type' is false, which fits a knave. So A is a knight and B is a knave. The other assumption breaks, so this is the only answer."
**Answer:** **A is a knight and B is a knave.**
**Step-by-step reasoning:**
1. A knight tells the truth; a knave lies. So whatever a speaker says must be true if he is a knight and false if he is a knave.
2. Assume A is a knight. Then "B is a knave" is true, so B is a knave.
3. Check B: B says "A and I are the same type." A is a knight and B a knave, so the statement is false. A knave lies, so this is consistent.
4. Assume instead A is a knave. Then "B is a knave" is false, so B is a knight. A knight's statement must be true, but "A and I are the same type" is false (knave and knight). Contradiction.
5. So only "A knight, B knave" survives.
**Fast method (30 seconds):** Test the two assumptions about A and stop at the first contradiction. "A is a knave" fails quickly, so A is a knight and everything else follows.
**Check:** Brute force over all 4 type assignments: only (A knight, B knave) is consistent.
**Explain simply:**
- Knight: every statement is true. Knave: every statement is false.
- "Assume then check" means pick a type for one person, follow the consequences, and see whether anyone is forced to contradict their own type.
**Likely follow-ups:** 1) *What if B said "A and I are of different types"?* Then A knight gives B knave, and B's statement "different" is true, which a knave cannot say; A knave gives B knight and B's "different" is true, which fits. So A knave, B knight (checked by hand). 2) *Could both be knights?* No: A would be saying a false thing.
**Common mistakes / traps:** Stopping after the first assumption works without realising you should also confirm the other fails (uniqueness); treating a knave's statement as "unreliable" instead of exactly false.

### Q3 ⭐⭐⭐ 🟢 On the same island, A says: "At least one of us two is a knave." B says nothing. What are A and B?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Seeing that a statement can contradict its own speaker's type.
**Say this in the interview:** "If A were a knave, 'at least one of us is a knave' would be true, but a knave cannot say something true. So A is a knight, the statement is true, and since A is not the knave, B must be."
**Answer:** **A is a knight and B is a knave.**
**Step-by-step reasoning:**
1. Assume A is a knave. Then A's statement must be false, so "at least one of us is a knave" must be false, meaning both are knights. But A is a knave. Contradiction.
2. So A is a knight and the statement is true.
3. At least one of the two is a knave, and A is a knight, so B is the knave.
4. B's silence does not matter; the answer comes from A alone.
**Fast method (30 seconds):** A statement that is automatically true if the speaker is a knave ("at least one of us is a knave") cannot come from a knave. So the speaker is a knight and the other person is the knave.
**Check:** Brute force over 4 combinations: only (knight, knave) works.
**Explain simply:**
- "At least one" means one or more; it is true as soon as one person is a knave.
- A knave must say only false things, so any statement that would be true because of his own type is impossible for him.
**Likely follow-ups:** 1) *If A said "both of us are knaves"?* A knight cannot say it (false), so A is a knave; the statement is then false, so B is not a knave, i.e. B is a knight (hand-checked). 2) *If A said "at least one of us is a knight"?* A knight (true, B can be either) and A knave with B knave (statement false) both fit, so the puzzle would not decide (hand-checked).
**Common mistakes / traps:** Thinking B's silence means B is missing information, or that the puzzle has no answer without B speaking.

### Q4 ⭐⭐⭐ 🟢 A hiring panel of exactly 3 people is chosen from Asha, Bimal, Chitra, Dev, Esha and Farah. (1) Asha and Bimal cannot both be on the panel. (2) If Chitra is on the panel, Dev must also be on it. (3) At least one of Esha and Farah must be on the panel. (4) Dev and Farah cannot both be on the panel. Which one of these panels is valid? (a) Asha, Bimal, Esha (b) Chitra, Esha, Farah (c) Bimal, Dev, Farah (d) Asha, Dev, Esha (e) Chitra, Dev, Farah
**Asked at:** commonly asked (no company-specific report found); selection puzzles appear in prep-site lists (unverified).
**What the interviewer is checking:** Testing each option against every rule, rather than hunting for the answer by feel.
**Say this in the interview:** "I check each option against the four rules and cross it out at the first rule it breaks. Only (d) passes all four."
**Answer:** **(d) Asha, Dev, Esha.**
**Step-by-step reasoning:**
1. (a) Asha and Bimal both present: breaks rule 1.
2. (b) Chitra present but Dev absent: breaks rule 2.
3. (c) Dev and Farah both present: breaks rule 4.
4. (d) Asha without Bimal (rule 1 ok); no Chitra (rule 2 not triggered); Esha present (rule 3 ok); Dev without Farah (rule 4 ok). Valid.
5. (e) Dev and Farah both present: breaks rule 4.
**Fast method (30 seconds):** Scan for "forbidden pairs" first: rule 1 pair (Asha, Bimal) and rule 4 pair (Dev, Farah) knock out (a), (c), (e) instantly. Then rule 2 knocks out (b).
**Check:** Brute force over all 20 possible 3-person panels: 5 are valid and (d) is the only one among the options.
**Explain simply:**
- "If Chitra, then Dev" only bites when Chitra is on the panel. A panel without Chitra never breaks it.
- "At least one of Esha and Farah" means Esha, or Farah, or both.
**Likely follow-ups:** 1) *How many panels are valid in all?* 5 (see Q12). 2) *Would (d) stay valid if Dev and Esha could not both serve?* No.
**Common mistakes / traps:** Reading rule 2 as "Chitra and Dev go together" (if Dev is on, Chitra need not be); marking (d) wrong because Asha seems unrelated.

### Q5 ⭐⭐⭐ 🟢 In a league, 8 teams play each other twice (home and away). How many matches are played in total?
**Asked at:** commonly asked (no company-specific report found); league and round-robin counting is a listed reasoning topic on prep sites (unverified).
**What the interviewer is checking:** Counting pairs correctly and then doubling for two legs.
**Say this in the interview:** "Each team has 7 opponents, so 8 times 7 is 56 ordered pairings, and with home and away that is exactly 56 matches. Another way: 28 pairs, played twice, is 56."
**Answer:** **56 matches.**
**Step-by-step reasoning:**
1. Number of different pairs of teams: 8 x 7 / 2 = 28 (the division by 2 is because "A vs B" and "B vs A" are the same pair).
2. Each pair plays twice (home and away): 28 x 2 = 56.
3. Same result: each of 8 teams hosts 7 opponents, 8 x 7 = 56.
**Fast method (30 seconds):** Double round robin = n x (n - 1). For 8 teams, 8 x 7 = 56. A single round robin is half of that.
**Check:** Counted by script (pairs and home-away listing): 28 pairs, 56 matches.
**Explain simply:**
- A "round robin" means everyone plays everyone.
- Dividing by 2 removes double counting of a pair; playing twice puts the 2 back, so they cancel.
**Likely follow-ups:** 1) *10 teams, play each other once?* 10 x 9 / 2 = 45. 2) *10 teams, twice?* 90.
**Common mistakes / traps:** Answering 28 (forgetting the second leg) or 64 (8 x 8, counting a team playing itself).

### Q6 ⭐⭐⭐ 🟢 How do you solve a "who owns what" logic-grid puzzle systematically: how do you set up the table, which clues do you use first, and how do you record negative clues?
**Asked at:** commonly asked (no company-specific report found); the grid method is described in public tutorials such as Brilliant's elimination-grid page, and an analyst-role grid puzzle appears in a 2025 Australian government recruitment challenge (snippet-level sources).
**What the interviewer is checking:** Whether you have a repeatable method, not guesswork.
**Say this in the interview:** "I draw a table with people as rows and each attribute as columns, mark positive clues with a tick and negative clues with a cross, use direct clues first, and keep crossing out until each row and column has exactly one tick."
**Answer:** **Set up one grid (people x each attribute), use direct "is" clues first, cross out for every "is not", and apply the "one tick per row and column" rule until all cells are decided.**
**Explain simply:**
- Setup: list people down the side; across the top list every option of every attribute (for example city and tool). Each person gets exactly one option of each attribute, and no option is used twice.
- Order of clues: first the direct ones ("Jay is the Tableau user"), then the chains ("the Excel user is in Kolkata", which links two attributes), then the negative ones, last the vague ones ("earlier than").
- Negative clues: put a cross in the cell. A cross is information: when a row has all crosses but one, that cell must be a tick.
- Two shortcuts: "last remaining cell" (one uncrossed cell in a row or column is the answer) and "pair elimination" (if two people can only take the same two options, nobody else can take them).
- Merge clues about two attributes as soon as you can ("the Excel user" and "the person in Kolkata" are the same person), so you track one row, not two.
**Worked mini-example:** Roles Analyst, Auditor for X and Y. Clue: "X is not Auditor." Cross X-Auditor, so X = Analyst, then Y = Auditor in one step.
**Likely follow-ups:** 1) *What if no direct clue exists?* Start with the attribute pair that appears in the most clues. 2) *How do you know the answer is unique?* Every tick was forced, or you tried the alternative and met a contradiction (see Q14).
**Common mistakes / traps:** Recording only ticks and forgetting crosses; failing to link two attributes that clues say are the same person; guessing early.

### Q7 ⭐⭐⭐ 🟢 What is a reliable step-by-step method for truth-teller and liar (knight and knave) puzzles, and why does the "assume one person is a knight, then check" method work?
**Asked at:** commonly asked (no company-specific report found); the assume-and-check method is the standard tutorial approach (Brilliant, Wikipedia on Knights and Knaves; snippet-level), and such an item appears in an interview-question bank (unverified).
**What the interviewer is checking:** That you reason by consistency, not by trusting what is said.
**Say this in the interview:** "I let each person be either knight or knave, translate each statement into 'true if knight, false if knave', try one assumption, follow it through, and if no one contradicts their own type it is a solution. If it contradicts, the opposite must hold."
**Answer:** **Pick a person, assume knight, derive everyone's type from the statements, check every statement against the types; if a contradiction appears, the person is a knave. Repeat until only consistent assignments remain.**
**Explain simply:**
- Rule: a knight's statement is true; a knave's statement is false. So each statement ties the speaker's type to the truth of the statement.
- Method: (1) write each statement in symbols or plain words; (2) assume A is a knight, so A's statement is true; (3) work out what that says about B and C; (4) test every other statement; (5) if all fit, record the solution; (6) if not, try A as a knave; (7) count the solutions.
- Why it works: every person is exactly one of two types, so the two assumptions cover all cases. If "A knight" fails, "A knave" is the only way left. If both work, the puzzle has two answers; if neither, the puzzle is flawed.
- A shortcut: a statement that can only be true (or only false) fixes the speaker at once (see Q3).
**Worked mini-example:** A says "I am a knave." If A is a knight, the statement is true, so A is a knave: contradiction. If A is a knave, the statement is true, so a knave said something true: contradiction. No one can say it (see Q19).
**Likely follow-ups:** 1) *With 3 people, how many cases?* 2 x 2 x 2 = 8, and you can test all 8 if you must. 2) *What if the answer depends on the starting guess?* Then there are several solutions; say so.
**Common mistakes / traps:** Treating a knave's statement as "can be anything"; stopping at the first consistent assignment without checking the other.

### Q8 ⭐⭐⭐ 🟡 Four analysts Ira, Jay, Kim and Lee each work in a different city (Pune, Delhi, Chennai, Kolkata) and each uses a different main tool (Excel, SQL, Python, Tableau). Clues: (1) Jay is the Tableau user. (2) The Excel user is the person in Kolkata. (3) The Python user is not the person in Chennai. (4) Lee is not the person in Pune. (5) Kim is not the Excel user. (6) Lee is not the person in Kolkata. (7) The SQL user is the person in Delhi. Which tool does Kim use, and in which city does Ira work?
**Asked at:** commonly asked (no company-specific report found); two-attribute matching grids are listed in prep-site topics (unverified).
**What the interviewer is checking:** Merging linked clues ("Excel user = Kolkata") and then eliminating.
**Say this in the interview:** "Excel is Kolkata and SQL is Delhi, so Python and Tableau are Pune and Chennai. Python is not Chennai, so Python is Pune and Tableau is Chennai. Jay is Tableau, so Jay is in Chennai. Lee is not Pune or Kolkata or Chennai, so Lee is Delhi with SQL. Kim is not Excel, so Kim is Python in Pune, and Ira is Excel in Kolkata."
**Answer:** **Kim uses Python; Ira works in Kolkata.**
**Step-by-step reasoning:**
1. Clues 2 and 7 give two tool-city links: Excel = Kolkata, SQL = Delhi.
2. So Python and Tableau take Pune and Chennai. Clue 3 says Python is not Chennai, so Python = Pune, Tableau = Chennai.
3. Clue 1: Jay uses Tableau, so Jay is in Chennai.
4. Lee is not in Pune (4), not in Kolkata (6), not in Chennai (Jay is), so Lee = Delhi = SQL.
5. Remaining: Ira and Kim for Kolkata/Excel and Pune/Python. Clue 5: Kim is not Excel, so Kim = Pune = Python and Ira = Kolkata = Excel.

| Person | City | Tool |
|---|---|---|
| Ira | Kolkata | Excel |
| Jay | Chennai | Tableau |
| Kim | Pune | Python |
| Lee | Delhi | SQL |

The solution is unique: each step was forced.
**Fast method (30 seconds):** Fuse city and tool into one "slot" (Kolkata-Excel, Delhi-SQL) first; then only two free slots remain to place.
**Check:** All 7 clues re-read against the table hold. Checked by brute force over all 24 x 24 = 576 city and tool assignments; exactly one fits.
**Explain simply:**
- When a clue says "the Excel user is the person in Kolkata", those two options belong to the same person, so treat them as one item.
- Counting remaining slots (here two cities, two tools) makes the final deduction easy.
**Likely follow-ups:** 1) *What if clue 3 (Python is not Chennai) were dropped?* There would be 3 solutions, so clue 3 is needed (by script). 2) *What if clue 5 (Kim is not Excel) were dropped?* 2 solutions, so Ira and Kim could not be told apart (by script).
**Common mistakes / traps:** Treating the city and tool tables as independent and guessing, instead of merging linked clues.

### Q9 ⭐⭐⭐ 🟡 Four colleagues Meena, Naveen, Omkar and Pooja work in four different departments (HR, Finance, IT, Sales) and each commutes by a different mode (bus, metro, bike, car). Clues: (1) The IT employee is the bus commuter. (2) Naveen is the IT employee. (3) The Sales employee is the bike commuter. (4) Meena is not the Finance employee. (5) Pooja is not the Finance employee. (6) The HR employee is the car commuter. (7) Meena is not the bike commuter. Who works in Finance, and how does that person commute?
**Asked at:** commonly asked (no company-specific report found); matching-grid puzzles are listed for several Indian service firms on prep sites (unverified).
**What the interviewer is checking:** Chaining department-mode links and using the leftover option.
**Say this in the interview:** "Naveen is IT and so takes the bus. Meena and Pooja are not Finance, so Omkar is Finance. HR drives, Sales bikes, so Finance gets the remaining mode, metro. Meena is not on the bike, so she is HR (car) and Pooja is Sales (bike)."
**Answer:** **Omkar works in Finance and commutes by metro.**
**Step-by-step reasoning:**
1. Naveen = IT (clue 2), and IT = bus (clue 1), so Naveen takes the bus.
2. Meena and Pooja are not Finance (4, 5) and Naveen is IT, so Omkar = Finance.
3. Mode links: IT-bus, Sales-bike, HR-car. The only mode left is metro, which therefore belongs to Finance.
4. So Omkar commutes by metro.
5. Meena and Pooja share HR and Sales. Meena is not on the bike (7), so Meena = HR (car), Pooja = Sales (bike).

| Person | Department | Mode |
|---|---|---|
| Meena | HR | car |
| Naveen | IT | bus |
| Omkar | Finance | metro |
| Pooja | Sales | bike |

**Fast method (30 seconds):** Three departments are tied to three modes by the clues, so the fourth department takes the fourth mode. No need to touch the person-mode clue to answer the question.
**Check:** All 7 clues hold. Checked by brute force over 24 x 24 assignments; exactly one fits.
**Explain simply:**
- When every department except one is tied to a mode, the leftover department gets the leftover mode.
- Clue 7 is only needed to separate Meena and Pooja; the question itself does not need it.
**Likely follow-ups:** 1) *Who is the bike commuter?* Pooja. 2) *If clue 7 were dropped?* Meena and Pooja could swap (HR/Sales), so who rides the bike would be open, but the Finance answer stays Omkar-metro.
**Common mistakes / traps:** Guessing that Meena is Finance because the name comes first; forgetting that Finance's mode is whatever is left.

### Q10 ⭐⭐⭐ 🟡 Six one-hour training sessions (Excel, SQL, Python, Power BI, Statistics, Reporting) are held one after another in six slots, each topic exactly once. Clues: (1) Python is held earlier than Power BI. (2) SQL is held earlier than Reporting. (3) Reporting is held immediately before Statistics. (4) Reporting is held earlier than Python. (5) Excel is held immediately before Reporting. Which session is held 4th, and which is held last (6th)?
**Asked at:** commonly asked (no company-specific report found); scheduling and ordering puzzles are common on prep sites (unverified).
**What the interviewer is checking:** Building one ordered chain from "before" and "immediately before" clues.
**Say this in the interview:** "Excel, Reporting, Statistics come as a block of three in that order. SQL is before that block. Python and Power BI come after Reporting, with Python before Power BI. So the order is SQL, Excel, Reporting, Statistics, Python, Power BI."
**Answer:** **4th is Statistics; 6th (last) is Power BI.**
**Step-by-step reasoning:**
1. "Immediately before" glues sessions together: Excel, Reporting, Statistics form a block E-R-S (clues 5 and 3).
2. SQL is before Reporting (2), and Excel is right before Reporting, so SQL is before Excel.
3. Python is after Reporting (4); Statistics is right after Reporting, so Python is after Statistics. Power BI is after Python (1).
4. The full chain: SQL, Excel, Reporting, Statistics, Python, Power BI.

| Slot | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Session | SQL | Excel | Reporting | Statistics | Python | Power BI |

It is unique because the chain is complete: every pair is ordered.
**Fast method (30 seconds):** Write the glued block first, then hang each "earlier than" clue off its ends. When the chain has a clue for every neighbour, the order is forced.
**Check:** Checked by brute force over all 720 orderings: exactly one satisfies all five clues.
**Explain simply:**
- "Earlier than" only says relative order; "immediately before" means adjacent, with no gap.
- A block of glued items behaves like one item when you place others around it.
**Likely follow-ups:** 1) *If clue 2 (SQL before Reporting) were dropped?* 4 orders fit, so the answer would no longer be forced (by script). 2) *Which slot is Reporting?* 3rd.
**Common mistakes / traps:** Treating "earlier than" as "immediately before"; putting Python between Reporting and Statistics (they are adjacent).

### Q11 ⭐⭐⭐ 🟡 Three interview-panel members A, B and C are each a knight (always truthful) or a knave (always lying). A says: "Exactly one of us three is a knave." B says: "Exactly two of us three are knaves." C says: "All three of us are knaves." How many knights are on the panel, and who are they?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Counting-statement puzzles: at most one "exactly k" claim can be true.
**Say this in the interview:** "The three claims say 1, 2 and 3 knaves, so at most one can be true. C's claim cannot be true (a knight cannot be among 'all knaves'), so C is a knave. If A were the knight there would be 2 knaves, not 1. If B is the only knight there are exactly 2 knaves, matching B. So B is the only knight."
**Answer:** **One knight: B. A and C are knaves.**
**Step-by-step reasoning:**
1. The statements give three different counts of knaves, so at most one statement is true. So at most one knight.
2. If C were a knight, "all three are knaves" would be true, but C is a knight: contradiction. So C is a knave.
3. If there were no knights, all three are knaves, and C's statement would be true: a knave cannot say that. So there is exactly one knight, A or B.
4. If A is the knight: knaves = 2, but A says exactly 1. False. Contradiction.
5. If B is the knight: knaves = 2 (A and C), B says exactly 2. True. A's claim (exactly 1) is false and C's claim (3) is false, as knaves require.
**Fast method (30 seconds):** Count-claims that differ cannot both hold, so at most one is true; then test who the one true speaker could be by matching "number of knaves" with "number of liars".
**Check:** Checked by brute force over all 8 type assignments: only (A knave, B knight, C knave).
**Explain simply:**
- "Exactly k are knaves" is true for only one value of k, so different values contradict each other.
- If knights = 1, knaves = 2, so the claim "exactly two" is the true one.
**Likely follow-ups:** 1) *If there were four members each claiming exactly 1, 2, 3, 4 knaves?* The only knight would be the one saying "exactly 3" (3 knaves, 1 knight); same pattern (by hand). 2) *Why can nobody say "all are knaves"?* If a knight says it, it is false; if a knave says it, it is true.
**Common mistakes / traps:** Thinking that if all three statements are different, all are false; forgetting that the number of knaves is 3 minus the number of knights.

### Q12 ⭐⭐⭐ 🟡 A hiring panel of exactly 3 people is to be chosen from Asha, Bimal, Chitra, Dev, Esha and Farah. (1) Asha and Bimal cannot both be on the panel. (2) If Chitra is on the panel, Dev must also be on it. (3) At least one of Esha and Farah must be on the panel. (4) Dev and Farah cannot both be on the panel. How many different panels are possible?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Systematic counting under constraints, without missing or double counting.
**Say this in the interview:** "Without rules there are 20 panels. I split by whether Esha is in. I list the valid panels case by case and get 5."
**Answer:** **5 panels.**
**Step-by-step reasoning:**
1. All 3-person panels from 6: C(6,3) = 6 x 5 x 4 / (3 x 2 x 1) = 20.
2. Case 1: Farah is on the panel. Then Dev is out (rule 4), so Chitra is out (rule 2). The other two come from Asha, Bimal, Esha but not both Asha and Bimal: Asha+Esha, Bimal+Esha. Panels: (Asha, Esha, Farah), (Bimal, Esha, Farah). (Asha+Bimal is banned.)
3. Case 2: Farah is out. Then Esha must be in (rule 3). Choose two more from Asha, Bimal, Chitra, Dev: Chitra needs Dev; Asha and Bimal not together. Valid pairs: Asha+Dev, Bimal+Dev, Chitra+Dev. (Asha+Chitra, Bimal+Chitra fail rule 2; Asha+Bimal fails rule 1.)
4. Total 2 + 3 = 5.

| Panel |
|---|
| Asha, Dev, Esha |
| Asha, Esha, Farah |
| Bimal, Dev, Esha |
| Bimal, Esha, Farah |
| Chitra, Dev, Esha |

**Fast method (30 seconds):** Split on the most restrictive person (Farah). Each case collapses quickly, so you list, not count blindly.
**Check:** Checked by script: all 20 panels enumerated, exactly 5 pass.
**Explain simply:**
- C(6,3) means "6 choose 3": the number of groups of 3 when order does not matter.
- Splitting into cases that cannot overlap (Farah in versus out) ensures no double counting.
**Likely follow-ups:** 1) *Without rule 4?* 9 panels (by script). 2) *Panels of 4 under all four rules?* 2: (Asha, Chitra, Dev, Esha) and (Bimal, Chitra, Dev, Esha) (by script).
**Common mistakes / traps:** Counting (Asha, Chitra, Esha) because "Chitra and Dev" is only one rule; forgetting Esha is forced when Farah is out.

### Q13 ⭐⭐⭐ 🟡 A hiring panel of exactly 3 people is to be chosen from Asha, Bimal, Chitra, Dev, Esha and Farah. (1) Asha and Bimal cannot both be on the panel. (2) If Chitra is on the panel, Dev must also be on it. (3) At least one of Esha and Farah must be on the panel. (4) Dev and Farah cannot both be on the panel. Which person must be on every valid panel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The idea of "forced" membership: appears in all valid cases.
**Say this in the interview:** "The five valid panels all contain Esha: when Farah is in, Dev and Chitra are out and the rest needs Esha; when Farah is out, rule 3 forces Esha."
**Answer:** **Esha.**
**Step-by-step reasoning:**
1. Suppose Esha is not on the panel. Rule 3 then forces Farah in. Rule 4 removes Dev, and rule 2 then removes Chitra.
2. That leaves only Asha, Bimal and Farah to fill 3 seats, so the panel would be Asha, Bimal, Farah, which breaks rule 1.
3. So Esha must be on every valid panel.
4. Confirm: each of the 5 valid panels (Q12) contains Esha, while no one else is in all five (Asha is missing from 3, Dev from 2, Farah from 3, Bimal from 3, Chitra from 4).
**Fast method (30 seconds):** Try removing a person and see whether any panel survives. Removing Esha kills them all, so Esha is forced.
**Check:** Checked by script: intersection of all valid panels is exactly {Esha}.
**Explain simply:**
- "Must be on every panel" means the person is in the overlap (intersection) of all valid panels.
- A proof by contradiction: assume the person is absent and show no valid panel is left.
**Likely follow-ups:** 1) *Is Dev always in?* No: (Asha, Esha, Farah) has no Dev. 2) *Which person can never be on a valid panel?* Nobody; every person appears in at least one valid panel (by script).
**Common mistakes / traps:** Picking Dev because rule 2 mentions him, or Chitra because she is mentioned first; reading "at least one of Esha and Farah" as forcing Farah.

### Q14 ⭐⭐⭐ 🟡 A multi-attribute puzzle seems stuck after the direct clues are used. What do you do next (case split, indirect clues, skip), and how do you decide how long to spend before moving on in a timed test?
**Asked at:** commonly asked (no company-specific report found); time management is general advice, not a company-specific finding.
**What the interviewer is checking:** Whether you have a plan when direct deduction runs out, and good time sense.
**Say this in the interview:** "First I re-read the unused clues and merge any that link two attributes. If still stuck, I make a two-way case split on the person or item with the fewest options and follow each branch; a branch that contradicts is eliminated. If I have spent about twice the average time per question and have no progress, I mark it and move on."
**Answer:** **Order of attack: (1) re-read every clue for hidden links, (2) apply negatives and counting (last remaining cell, pair elimination), (3) case split on the most constrained cell, (4) skip and return if time is short.**
**Explain simply:**
- Indirect clues are clues like "X is not Pune" or "the SQL user is older than Ira"; they do not fix a cell but remove options, and several together can force one.
- Case split (guess and check): pick a cell with two possibilities, assume one, follow the chain; a contradiction proves the other. This is fully valid logic, not guessing, because you cover both cases.
- Time rule of thumb (our suggestion, not a research finding): divide the test time by the number of questions, allow about double that for a puzzle you have started, and skip if no new cell has been filled for a couple of minutes.
- Keep a mark on skipped questions so you can return with leftover time.
**Worked mini-example:** Two options remain for Kim: Pune or Delhi. Assume Pune; if that makes Lee have no city, Kim must be Delhi. One branch usually dies in a few lines.
**Likely follow-ups:** 1) *How many cases can you afford?* Two (one split); if you need nested splits, skip. 2) *If you are in an interview, not a test?* Say your reasoning aloud; interviewers watch the approach, and an honest "here is where I would split" counts.
**Common mistakes / traps:** Splitting before finishing the simple eliminations; continuing a branch after it has already contradicted; spending five minutes on a 1-mark question.

### Q15 ⭐⭐ 🟢 A knockout cricket tournament (single elimination, one loser out per match, no byes needed) has 37 teams. How many matches are played in total to decide the champion, and why?
**Asked at:** commonly asked (no company-specific report found); knockout counting is a games-and-tournaments topic on prep sites (unverified).
**What the interviewer is checking:** Whether you count eliminations instead of drawing the whole bracket.
**Say this in the interview:** "Every match knocks out exactly one team, and 36 of the 37 teams must be knocked out, so there are 36 matches."
**Answer:** **36 matches.**
**Step-by-step reasoning:**
1. Only one team ends as champion, so 37 - 1 = 36 teams must lose.
2. Each match produces exactly one loser (no draws, one team out per match).
3. So the number of matches = the number of losers = 36.
**Fast method (30 seconds):** Matches = teams - 1, for any knockout, even or odd team count. It works because we count losers, which does not care how the bracket is drawn.
**Check:** Small case: 4 teams give 2 semi-finals + 1 final = 3 = 4 - 1. Also, the formula was confirmed by script for 37 teams.
**Explain simply:**
- "Single elimination" means one defeat and you are out.
- Counting what each match produces (one loser) is easier than counting rounds.
**Likely follow-ups:** 1) *What if there are 64 teams?* 63 matches. 2) *How many rounds for 37 teams?* With byes it is 6 rounds (ceiling of log base 2 of 37 is 6); the match total is still 36.
**Common mistakes / traps:** Halving repeatedly (37/2 is not whole) and getting stuck; or using n(n-1)/2, which is the round robin formula.

### Q16 ⭐⭐ 🟢 In a single round robin of 10 players (every pair plays exactly once), every player has so far played exactly 6 matches. How many matches are still to be played?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The handshake idea: each match involves two players, so divide by 2.
**Say this in the interview:** "Total matches are 45. Played so far: 10 players times 6 games, divided by 2 because each match has two players, is 30. So 15 remain."
**Answer:** **15 matches.**
**Step-by-step reasoning:**
1. Total matches in a single round robin of 10 = 10 x 9 / 2 = 45.
2. Each player has played 6, so the "player-appearances" total 10 x 6 = 60.
3. Each match uses two appearances, so matches played = 60 / 2 = 30.
4. Remaining = 45 - 30 = 15. (Same view: each player has 9 - 6 = 3 opponents left, 10 x 3 / 2 = 15.)
**Fast method (30 seconds):** Remaining per player = 9 - 6 = 3; total = 10 x 3 / 2 = 15.
**Check:** Verified by script that a situation where everyone has played 6 exists (every player faces the 3 players on each side in a circle of 10), leaving each with 3 opponents; 15 matches.
**Explain simply:**
- A "round robin" is a format where every pair meets once.
- Counting each match twice (once per player) and then halving is called the handshake method.
**Likely follow-ups:** 1) *Could 10 players each have played exactly 5 matches?* Yes, 25 played. 2) *Could 9 players each have played exactly 5?* No: 9 x 5 = 45 is odd, so it cannot be halved.
**Common mistakes / traps:** Forgetting to halve (answer 30 or 60), or subtracting 6 from 45.

### Q17 ⭐⭐ 🟢 Among 25 employees, what is the largest number you can guarantee shares the same birth month (that is, at least how many must share a month), whatever the birthdays are?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The pigeonhole principle: spreading things evenly to find the worst case.
**Say this in the interview:** "12 months, 25 people. Even spreading gives 2 per month with 1 left over, so some month must have at least 3."
**Answer:** **At least 3 employees share a birth month (guaranteed); 4 is not guaranteed.**
**Step-by-step reasoning:**
1. Suppose no month had 3 or more. Then each month holds at most 2.
2. 12 months x 2 = 24 people at most.
3. We have 25, which is more, so that is impossible; some month has at least 3.
4. 4 is not guaranteed: 1 month with 3 and 11 months with 2 gives 3 + 22 = 25 with no month above 3.
**Fast method (30 seconds):** Guaranteed number = ceiling of 25 / 12 = ceiling of 2.08 = 3. "Ceiling" means round up to the next whole number.
**Check:** Verified by script (ceiling 25/12 = 3, and the 3 + 11 x 2 example reaches 25 with maximum 3).
**Explain simply:**
- Pigeonhole principle: if more items than boxes, some box holds more than one; in general some box holds at least the ceiling of items / boxes.
- It talks about the worst case, not the typical case.
**Likely follow-ups:** 1) *How many people guarantee 4 in one month?* 12 x 3 + 1 = 37. 2) *How many guarantee two share a month?* 13.
**Common mistakes / traps:** Answering 2 (rounding 25/12 down) or 4.

### Q18 ⭐⭐ 🟢 In constraint puzzles, what is the difference between "at least one", "exactly one" and "at most one" of two people, and how should you read "either A or B" when the puzzle does not say "but not both"?
**Asked at:** commonly asked (no company-specific report found); wording of selection clues is a standard trap in panel puzzles (our observation, not a source claim).
**What the interviewer is checking:** Precise reading of conditions before solving.
**Say this in the interview:** "At least one allows both; exactly one forbids both and neither; at most one forbids both but allows neither. For a bare 'either A or B' I state my assumption, and if it changes the answer I say so."
**Answer:** **At least one = 1 or 2 of them. Exactly one = precisely 1. At most one = 0 or 1. A bare "either A or B" is ambiguous; in puzzles treat it as "at least one" (inclusive) unless the text says "but not both", and always state that choice.**
**Explain simply:**
| Of A and B | Neither | Only A | Only B | Both |
|---|---|---|---|---|
| At least one | no | yes | yes | yes |
| Exactly one | no | yes | yes | no |
| At most one | yes | yes | yes | no |
- "Either ... or ..." in everyday speech often means exactly one; in formal logic "or" is inclusive. Puzzle setters differ, so check whether the puzzle has a solution under both readings.
- Worked mini-example: "at least one of Esha and Farah" accepts a panel that contains both; "exactly one" rejects it. So the reading changes which panels are valid.
**Likely follow-ups:** 1) *"A and B cannot both be on the panel" is which one?* At most one. 2) *What is the negation of "at least one is a knave"?* Both are knights.
**Common mistakes / traps:** Treating "at least one" as "exactly one", or forgetting that "at most one" allows nobody.

### Q19 ⭐⭐ 🟢 Why can no inhabitant of a knights-and-knaves island say "I am a knave", and what would any inhabitant answer to the question "Are you a knight?"
**Asked at:** commonly asked (no company-specific report found); a knights-and-knaves item is reported in an interview-question bank (unverified, page not read).
**What the interviewer is checking:** Whether you can test a statement against both types of speaker.
**Say this in the interview:** "A knight cannot say it, because it would be false. A knave cannot say it, because a lie that 'I am a knave' would mean he is a knight. And everyone answers 'yes' to 'Are you a knight?'"
**Answer:** **Nobody can say "I am a knave"; and every inhabitant answers "Yes" to "Are you a knight?"**
**Step-by-step reasoning:**
1. Knight says "I am a knave": a knight must tell the truth, but the sentence is false for a knight. Impossible.
2. Knave says "I am a knave": a knave must lie, but the sentence is true for a knave. Impossible.
3. "Are you a knight?": a knight truthfully says yes; a knave lies about "no" and so says yes.
**Fast method (30 seconds):** "I am a knight" or "I am a knave" tests: the knight's truth and knave's lie both produce the same word, so such a question tells you nothing about the type.
**Check:** Verified by enumeration of both types against both statements.
**Explain simply:**
- A knight always tells the truth; a knave always lies (Smullyan's convention).
- A statement that gives the same answer for both types carries no information.
**Likely follow-ups:** 1) *How would you learn a person's type with one question?* Ask something whose truth you know, e.g. "Is 2 + 2 = 4?": yes means knight. 2) *What if someone says "I am a knight"?* No information, he could be either.
**Common mistakes / traps:** Thinking a knave can call himself a knave.

### Q20 ⭐⭐ 🟢 How many matches are played in a single round robin with n teams, and how many rounds are needed if every team plays at most once per round (what changes when n is odd)?
**Asked at:** commonly asked (no company-specific report found); n(n-1)/2 is the standard prep-site formula (unverified).
**What the interviewer is checking:** Knowing the formula and reasoning about scheduling.
**Say this in the interview:** "n times (n-1) over 2 matches. If n is even it takes n-1 rounds; if n is odd it takes n rounds because one team sits out each round."
**Answer:** **Matches = n(n-1)/2. Rounds = n - 1 if n is even; n if n is odd.**
**Step-by-step reasoning:**
1. Each team meets n - 1 others; n teams x (n - 1) counts each match twice, so divide by 2.
2. A team plays at most once per round, and it has n - 1 opponents, so at least n - 1 rounds are needed.
3. Even n: every round can have n/2 matches with everyone playing, so n - 1 rounds suffice (7 rounds for 8 teams: 28 matches = 7 x 4).
4. Odd n: one team must rest in each round, so a round has (n - 1)/2 matches. Total n(n-1)/2 divided by (n-1)/2 gives n rounds (5 teams: 10 matches, 2 per round, 5 rounds).
**Fast method (30 seconds):** Add a dummy "bye" team when n is odd; it becomes even, giving n + 1 - 1 = n rounds.
**Check:** Formulas hand-checked on 4, 5 and 8 teams; the round counts for n = 2 to 10 were also confirmed by script (n - 1 rounds for even n, n for odd n, after adding a dummy team).
**Explain simply:**
- A "round robin" means every team plays every other team once.
- A "bye" is a round where a team does not play.
**Likely follow-ups:** 1) *10 teams, home and away?* 90 matches over 18 rounds. 2) *How many matches does 11 teams give?* 55.
**Common mistakes / traps:** Saying n - 1 rounds for odd n, and doubling the count (n(n-1)) for a single round robin.

### Q21 ⭐⭐ 🟢 In grid puzzles, why are negative clues ("X is not in Pune") often as useful as positive ones, and what are the "last remaining cell" and "pair elimination" shortcuts?
**Asked at:** commonly asked (no company-specific report found); the elimination-grid method is described in tutorials such as Brilliant's (unverified snippet).
**What the interviewer is checking:** Whether you have a disciplined way to record and use information.
**Say this in the interview:** "Each negative clue crosses out a cell, and every crossed cell shrinks the choices. When a row has one open cell left, that is forced, and then I cross out the rest of its column."
**Answer:** **Negative clues are crossed-out cells, and enough crosses force the answer; "last remaining cell" = the only open cell in a row or column must be the match; "pair elimination" = if two people share the same two possible options, those two options belong to them, so cross those options out for everyone else.**
**Explain simply:**
- Each person matches exactly one item and each item exactly one person, so every X in a row or column also helps its neighbours.
- Last remaining cell: if Ira can be only Excel, mark Excel for Ira and cross out Excel for the others.
- Pair elimination: if Jay and Kim can each only be Pune or Delhi, then nobody else can be Pune or Delhi.
- Mini-example: 3 people, Pune/Delhi/Kolkata. "A is not Pune", "B is not Pune", so C = Pune (last cell). If "A is not Delhi", A = Kolkata, and B = Delhi.
**Likely follow-ups:** 1) *What if no row has a single cell left?* Make a case split: try one option and see if it leads to a contradiction. 2) *Why record negatives at all?* They are half of the clues in most puzzles.
**Common mistakes / traps:** Only marking the positive ticks and forgetting the crosses in the matching row and column.

### Q22 ⭐⭐ 🟡 A workshop has six sessions (Excel, SQL, Python, Power BI, Statistics, Reporting), one per slot from 1st to 6th, each topic exactly once. Clues: (1) Power BI is held immediately before Statistics. (2) Python is held earlier than Reporting. (3) SQL is held earlier than Python. (4) Reporting is held earlier than Statistics. (5) Excel is held immediately before Reporting. In which slot is the Reporting session held?
**Asked at:** commonly asked (no company-specific report found); ordering puzzles appear in prep-site lists for TCS, Infosys and similar (unverified).
**What the interviewer is checking:** Chaining "before" clues into one order.
**Say this in the interview:** "SQL, Python, then Excel and Reporting together, then Power BI and Statistics together. Reporting is the 4th session."
**Answer:** **Slot 4 (Reporting). Full order: 1 SQL, 2 Python, 3 Excel, 4 Reporting, 5 Power BI, 6 Statistics.**
**Step-by-step reasoning:**
1. Glue the "immediately before" pairs: [Excel, Reporting] and [Power BI, Statistics].
2. Clues 2 and 3 give SQL < Python < Reporting, so SQL and Python come before the Excel-Reporting block.
3. So the order so far: SQL, Python, then Excel then Reporting (Python must be before Reporting; Excel sits directly before Reporting).
4. Clue 4: Reporting is earlier than Statistics, so the [Power BI, Statistics] block comes after Reporting.
5. That gives SQL, Python, Excel, Reporting, Power BI, Statistics.
```
Slot:  1    2       3      4          5         6
       SQL  Python  Excel  Reporting  Power BI  Statistics
```
**Why unique:** Reporting has 3 sessions before it (SQL, Python, Excel) and 2 after (Power BI, Statistics); Python can only be in slot 1 or 2 and SQL must precede it, which fixes slots 1 and 2.
**Fast method (30 seconds):** Count how many sessions must come before and after Reporting: 3 before, 2 after, so slot 4.
**Check:** Verified by brute force over all 720 orders: exactly one satisfies all five clues.
**Explain simply:**
- "Immediately before" means next to each other; treat the pair as one block.
- "Earlier than" only needs the order, not neighbours.
**Likely follow-ups:** 1) *If clue 5 were dropped?* More than one order fits, so the answer would no longer be unique. 2) *Which slot is Python?* 2nd.
**Common mistakes / traps:** Treating "earlier than" as "immediately before".

### Q23 ⭐⭐ 🟡 Five employees Anu, Bala, Chitra, Dev and Esha, from five different departments (HR, Finance, IT, Ops, Sales), each take their weekly day off on a different weekday from Monday to Friday (one person per day). Clues: (1) The HR employee has the day off the day immediately before Dev. (2) Esha has the day off the day immediately before the IT employee. (3) Chitra has the day off earlier in the week than Bala. (4) Dev has the day off the day immediately before the Finance employee. (5) Chitra has the day off the day immediately before Dev. (6) The Sales employee has the day off earlier in the week than Chitra. (7) Dev has the day off earlier in the week than the IT employee. Who is off on Wednesday, and from which department?
**Asked at:** commonly asked (no company-specific report found); multi-person matching grids are listed for TCS, Accenture, Wipro and Cognizant on prep sites (unverified).
**What the interviewer is checking:** Chaining adjacent-day clues and combining two attributes (day and department).
**Say this in the interview:** "Chitra is just before Dev, and HR is just before Dev, so Chitra is HR. That locks the days one by one. Wednesday is Dev, from Ops."
**Answer:** **Dev is off on Wednesday, from Ops.**
**Step-by-step reasoning:**
1. Clues 1 and 5: both the HR employee and Chitra are the day before Dev, so Chitra is HR.
2. Clue 6: Sales is before Chitra, so Chitra is not Monday; clue 4: Finance is the day after Dev. So days run Sales ... Chitra, Dev, Finance. Chitra, Dev, Finance are three consecutive days with Sales earlier, so Chitra is Tue, Dev Wed, Finance Thu, Sales Mon.
3. Clue 7: IT is after Dev, so IT is Thursday or Friday; Thursday is Finance, so IT is Friday.
4. Clue 2: Esha is the day before IT, so Esha is Thursday (Finance).
5. Clue 3: Chitra before Bala, so Bala is Friday (IT), leaving Anu for Monday (Sales). Dev is Ops by elimination.
```
Day:  Mon    Tue    Wed   Thu      Fri
Who:  Anu    Chitra Dev   Esha     Bala
Dept: Sales  HR     Ops   Finance  IT
```
**Why unique:** the chain Sales, Chitra, Dev, Finance, IT leaves no alternative placement.
**Fast method (30 seconds):** Find the clue that pins two things to the same position (1 + 5), then build a block of consecutive days.
**Check:** Verified by brute force over all 120 day orders x 120 department assignments: exactly one solution; every clue was also re-read against the table.
**Explain simply:**
- If two different clues say "the day before Dev", they describe the same person.
- A block of consecutive days is placed first, then the rest filled by elimination.
**Likely follow-ups:** 1) *Who is off on Thursday?* Esha (Finance). 2) *Which clue is needed to separate Anu and Bala?* Clue 3 together with clue 2.
**Common mistakes / traps:** Missing that clues 1 and 5 identify Chitra as HR; leaving Sales in the wrong spot.

### Q24 ⭐⭐ 🟡 A support team of five (Anu, Bala, Chitra, Dev, Esha) belongs to five different departments (HR, Finance, IT, Ops, Sales). Each person has a different weekday off, Monday to Friday, one person per day. Clues: (1) Bala has the day off the day immediately before Chitra. (2) The Sales employee has the day off earlier in the week than the IT employee. (3) The Finance employee has the day off the day immediately before the HR employee. (4) The Ops employee has the day off earlier in the week than the HR employee. (5) The Finance employee has the day off earlier in the week than Chitra. (6) Dev has the day off the day immediately before Anu. (7) Bala has the day off the day immediately before the Sales employee. Who is off on Thursday, and from which department?
**Asked at:** commonly asked (no company-specific report found); multi-person matching grids are listed on prep sites (unverified).
**What the interviewer is checking:** Placing blocks of adjacent days and then using the "earlier than" clues to fit them.
**Say this in the interview:** "Bala, Chitra is a block; Bala is also just before Sales, so Chitra is Sales. Then the blocks fall into place: Thursday is Chitra, Sales."
**Answer:** **Chitra is off on Thursday, from Sales.**
**Step-by-step reasoning:**
1. Clues 1 and 7: Chitra and the Sales employee are both the day after Bala, so Chitra is Sales.
2. Clue 5: Finance is earlier than Chitra; clue 3: HR is right after Finance; clue 4: Ops is earlier than HR; clue 2: IT is after Sales (Chitra), so IT is after Chitra.
3. Chitra (Sales) must be before IT, so she is not on Friday. Try Chitra on Thursday: IT is then Friday, and Bala is Wednesday. Monday to Wednesday must hold Ops, Finance, HR (Finance immediately before HR, Ops before HR), which forces Ops Monday, Finance Tuesday, HR Wednesday, so Bala is HR.
4. The block [Dev, Anu] then takes Monday and Tuesday (Dev Mon, Anu Tue), and Esha takes Friday (IT). Chitra on Tuesday or Wednesday fails some clue (checked by script, not shown here).
```
Day:  Mon   Tue      Wed   Thu     Fri
Who:  Dev   Anu      Bala  Chitra  Esha
Dept: Ops   Finance  HR    Sales   IT
```
**Why unique:** the brute force below found only one arrangement; the Finance-HR pair must sit before Chitra and be adjacent to each other, and Ops must be before HR, which leaves only this layout.
**Fast method (30 seconds):** Identify who is the same person from two "the day after X" clues, then list which blocks must fit before and after.
**Check:** Verified by brute force over all 120 x 120 assignments: exactly one solution.
**Explain simply:**
- Two clues pointing to "the day after Bala" mean they name the same person.
- "Earlier than" clues restrict which blocks can sit before or after others.
**Likely follow-ups:** 1) *Who is off on Monday?* Dev (Ops). 2) *Which department is Esha?* IT.
**Common mistakes / traps:** Not noticing that clues 1 and 7 give Chitra as Sales; placing Anu on Tuesday as Ops.

### Q25 ⭐⭐ 🟡 Three colleagues A, B and C are each a knight (always truthful) or a knave (always lying). A says: "B and C are of the same type." B says: "A is a knight." C says: "Both A and B are knaves." Who is the knight?
**Asked at:** commonly asked (no company-specific report found); a knights-and-knaves item is reported in an interview-question bank (unverified).
**What the interviewer is checking:** Assume a type, follow the consequences, spot contradictions.
**Say this in the interview:** "If A were a knight, B would be a knight, so C would be one too, but C's statement would then be false. So A is a knave. Then B lies, so B is a knave, and C is the knight."
**Answer:** **C is the knight; A and B are knaves.**
**Step-by-step reasoning:**
1. Assume A is a knight. Then B and C are the same type. B says "A is a knight", which is true, so B is a knight, so C is a knight. But C says "A and B are knaves", which is false for a knight. Contradiction.
2. So A is a knave. B says "A is a knight", which is false, so B is a knave.
3. A's statement is a lie, so B and C differ; B is a knave, so C is a knight.
4. Check C: "A and B are both knaves" is true, as a knight must say.
**Fast method (30 seconds):** Start with B's statement, because it points straight at A; B and A match or differ in a way that forces the rest.
**Check:** Verified by script over all 8 type assignments: exactly one consistent.
**Explain simply:**
- A knight's statement must be true; a knave's must be false. Test each full assignment against all three.
**Likely follow-ups:** 1) *If C said "Both A and B are knights"?* Verified by script: then all three are knights (A's claim true, B's true, C's true). 2) *What if only B and C spoke?* Fewer clues may leave more than one answer.
**Common mistakes / traps:** Stopping when the first assumption looks fine, without checking every statement.

### Q26 ⭐⭐ 🟡 Three clerks A, B and C are each a knight (always truthful) or a knave (always lying). A says: "C is a knave." B says: "A and I are of the same type." C says: "Exactly two of the three of us are knaves." Who are the knaves?
**Asked at:** commonly asked (no company-specific report found); knights-and-knaves items are reported in an interview-question bank (unverified).
**What the interviewer is checking:** Handling counting statements ("exactly two") together with type statements.
**Say this in the interview:** "If A is a knight, C is a knave and B, same as A, is a knight. Then there is just one knave, so C's claim is false, which fits. Only C is a knave."
**Answer:** **Only C is a knave; A and B are knights.**
**Step-by-step reasoning:**
1. Assume A is a knight. A's statement is true, so C is a knave. B says "A and I are the same type"; since A is a knight, B's statement is true only if B is a knight, so B is a knight (a knave B would be telling the truth, impossible).
2. Knaves are then just C: one knave. C says "exactly two are knaves", false, as a knave must say. Consistent.
3. Assume A is a knave. Then C is a knight, and "exactly two knaves" must be true. B must then be a knave, but then B's statement ("A and I same type") is true, which a knave cannot say; and a knight B would also be false. Contradiction.
**Fast method (30 seconds):** Try the assumption that gives a quick contradiction first; here A knave breaks on B.
**Check:** Verified by script over all 8 assignments: exactly one consistent.
**Explain simply:**
- A knave who says something true would break the rule, so every knave statement must come out false.
- Counting claims need the whole assignment checked, not one person at a time.
**Likely follow-ups:** 1) *If C said "Exactly one of us is a knave"?* Verified by script: A is a knight, B and C are knaves. 2) *How many knaves in the original?* One (C).
**Common mistakes / traps:** Accepting "C is a knave" without checking that C's own statement is false.

### Q27 ⭐⭐ 🟡 Three managers A, B and C are each a knight (always truthful) or a knave (always lying). A says: "C and I are of different types." B says: "At least one of A and C is a knave." C says: "Exactly one of the three of us is a knave." What is each person?
**Asked at:** commonly asked (no company-specific report found); knights-and-knaves items are reported in an interview-question bank (unverified).
**What the interviewer is checking:** Systematic case testing of a three-person statement set.
**Say this in the interview:** "If A were a knight, C would be a knave, and C's claim 'exactly one knave' would be true, contradiction. So A is a knave, which makes C a knave too; B is the knight."
**Answer:** **A is a knave, B is a knight, C is a knave.**
**Step-by-step reasoning:**
1. Assume A is a knight. Then C is a knave (different type). C says "exactly one knave"; with C the only possible knave if B is a knight, the claim would be true, which a knave cannot say. If B is a knave, B says "at least one of A and C is a knave", which is true (C is a knave), impossible for a knave. Contradiction.
2. So A is a knave. A's statement is false, so C is the same type as A: a knave.
3. B says "at least one of A and C is a knave": true, so B is a knight.
4. Check C (a knave): "exactly one knave" is false because there are two (A and C). Correct.
```
A  B  C
knave  knight  knave
```
**Fast method (30 seconds):** A self-referential-style claim (C says "exactly one of us") is quickest to test: count knaves in each scenario.
**Check:** Verified by script over all 8 assignments: exactly one is consistent.
**Explain simply:**
- Test each possible assignment against all statements; the one with no clash is the answer.
**Likely follow-ups:** 1) *If C said "exactly two of us are knaves"?* The script gives A knight, B knight, C knave. 2) *Why is the answer unique?* Seven assignments each break at least one statement.
**Common mistakes / traps:** Reading B's "at least one" as "exactly one".

### Q28 ⭐⭐ 🟡 A sheet has five numbered statements. Statement 1: "Exactly one statement on this sheet is false." Statement 2: "Exactly two statements on this sheet are false." Statement 3: "Exactly three statements on this sheet are false." Statement 4: "Exactly four statements on this sheet are false." Statement 5: "Exactly five statements on this sheet are false." Which statement(s) are true?
**Asked at:** commonly asked (no company-specific report found); self-referential counting puzzles are a classic.
**What the interviewer is checking:** Spotting mutually exclusive statements and testing the only consistent count.
**Say this in the interview:** "The statements contradict each other, so at most one is true. Zero true would make statement 5 true, a contradiction. So exactly one is true, which means four are false, and that is statement 4."
**Answer:** **Only statement 4 is true.**
**Step-by-step reasoning:**
1. Each statement names a different number of false statements, so no two can be true together: at most one is true.
2. If none were true, all five would be false, but then "exactly five are false" (statement 5) would be true. Contradiction.
3. So exactly one is true, hence exactly four are false.
4. The statement that says "exactly four are false" is statement 4, so it is the true one; check the other four are false: yes, each names the wrong count.
**Fast method (30 seconds):** Say the number of true statements is t; then false = 5 - t. Only t = 1 makes a matching statement ("exactly four false") true, with the others wrong.
**Check:** Verified by brute force over all 32 true/false assignments: only "statement 4 true, rest false" is consistent.
**Explain simply:**
- A self-referential statement talks about the sheet that contains it, so we test whole assignments.
- Mutually exclusive means they cannot all hold at once.
**Likely follow-ups:** 1) *With only three statements (1, 2, 3 false-counts)?* The brute-force result is: statement 2 is true (exactly one true, two false). 2) *Could the answer be none true?* No: that makes statement 5 true.
**Common mistakes / traps:** Answering "statement 5" or "none".

### Q29 ⭐⭐ 🟡 A laptop was stolen from the office by exactly one of five employees: Anil, Bina, Chetan, Divya or Esha. Their statements: Anil: "It was not Esha." Bina: "It was Divya." Chetan: "It was Bina." Divya: "It was not Chetan." Esha: "It was Divya." Exactly two of the five statements are true. Who stole the laptop?
**Asked at:** commonly asked (no company-specific report found); "who is the culprit" statement puzzles are a standard analytics-interview type (prep-site claim, unverified).
**What the interviewer is checking:** Whether you can test each suspect against a counting condition ("exactly two true") instead of guessing.
**Say this in the interview:** "I assume each person is the thief in turn and count how many statements come out true. Only Anil gives exactly two. Answer: Anil."
**Answer:** **Anil stole the laptop.**
**Step-by-step reasoning:**
1. Assume the thief is X and count true statements for each X.
2. Anil is the thief: Anil's "not Esha" is true; Bina "Divya" false; Chetan "Bina" false; Divya "not Chetan" true; Esha "Divya" false. Total 2. Fits.
3. Bina is the thief: Anil true, Bina false, Chetan true, Divya true, Esha false. Total 3. No.
4. Chetan is the thief: only Anil's statement is true. Total 1. No.
5. Divya is the thief: Anil, Bina, Divya, Esha true; Chetan false. Total 4. No.
6. Esha is the thief: only Divya's statement is true. Total 1. No.
7. Only one suspect gives exactly two, so the answer is unique.
**Fast method (30 seconds):** Note that Bina and Esha say the same thing ("Divya"), so they are both true or both false. Two true statements with a matching pair means either that pair is the two true ones (thief Divya, but then Anil and Divya are also true, giving 4) or the pair is false (thief is not Divya). Then the two true ones come from Anil, Chetan, Divya, and only "Anil is the thief" leaves exactly Anil and Divya true.
**Check:** Verified by script over all 5 possible thieves; only Anil gives a count of 2.
**Explain simply:**
- Statement puzzles with a count are solved by "assume, then count"; there are only as many cases as suspects.
- A statement like "It was not Esha" is true for every suspect except Esha, so negative statements are true most of the time.
**Likely follow-ups:** What if exactly three statements were true? Then only Bina fits (3 true), checked by script.
**Common mistakes / traps:** Treating "exactly two true" as "at least two true" (Bina would then also fit with 3, and Divya with 4); or assuming the thief must be lying.

### Q30 ⭐⭐ 🟡 Two guards stand before two doors, one leading to the exit and one to a trap. One guard always tells the truth and the other always lies, but you do not know which is which. You may ask exactly one question (any wording) to one guard of your choice. What single question lets you identify the exit door for certain?
**Asked at:** commonly asked (no company-specific report found); a classic that Analytics India Magazine lists among standard analytics-interview puzzles (media claim, not verified in detail).
**What the interviewer is checking:** Whether you can build a question whose answer is wrong in the same way for both guards.
**Say this in the interview:** "I ask either guard: 'If I asked the other guard which door leads to the exit, what would he say?' Then I take the opposite door, because that answer is always a lie."
**Answer:** **Ask one guard: "If I asked the other guard which door is the exit, which door would he point to?" Then go through the other door.**
**Step-by-step reasoning:**
1. Suppose the exit is the left door.
2. You ask the truth-teller. The liar would point to the trap (right door). The truth-teller reports this honestly: "right".
3. You ask the liar. The truth-teller would point to the exit (left door). The liar lies about it: "right".
4. Either way the answer is "right", the trap. So you choose the opposite, the left door.
5. If the exit were the right door, both guards would say "left", and you again take the opposite.
**Fast method (30 seconds):** One lie plus one truth always gives a lie. Whoever you ask, the reply is the wrong door, so flip it.
**Check:** Hand-checked over the four cases (2 guard identities x 2 exit positions); all give the trap door as the reply.
**Explain simply:**
- A question about what the other guard would say combines two statements: one truthful and one false. Truth then lie, or lie then truth, always ends as a lie.
- "Any wording" lets you ask about another person, which cancels the uncertainty about who is who.
**Likely follow-ups:** Can you ask "Are you the liar?" No: both guards answer "no", so it tells you nothing. Can you ask "Which door would you say is the exit?" No: both say the exit, since the liar lies about what he would say.
**Common mistakes / traps:** Asking a direct question ("Which door is the exit?"), whose answer depends on which guard you picked; or forgetting to flip the answer at the end.

### Q31 ⭐⭐ 🟡 A 4-digit employee code has four different digits. The digits add up to 20. The first digit is twice the last digit. The second digit is the average of the first and third digits. What is the code?
**Asked at:** commonly asked (no company-specific report found); digit and code puzzles are listed in prep-site topic lists (unverified).
**What the interviewer is checking:** Turning word clues into small equations and searching a short list.
**Say this in the interview:** "Call the digits a, b, c, d. a = 2d and b = (a + c)/2. With sum 20 only d = 2 works, giving 4682."
**Answer:** **4682**
**Step-by-step reasoning:**
1. Let the code be a b c d. Then a = 2d, so d is at most 4 (a must be one digit, and a cannot be 0).
2. b = (a + c)/2 means a + c = 2b, so a + b + c = 3b. Total sum: 3b + d = 20.
3. So 20 - d must be a multiple of 3. With d = 1, 2, 3, 4: only d = 2 gives 18, so b = 6. (d = 1 gives 19, d = 3 gives 17, d = 4 gives 16; none divisible by 3.)
4. d = 2 means a = 4. Then c = 2b - a = 12 - 4 = 8.
5. Code 4, 6, 8, 2: all digits different.
**Fast method (30 seconds):** "b is the average of a and c" means a + b + c = 3b. So the sum becomes 3b + d = 20, and divisibility by 3 picks d at once.
**Check:** 4 + 6 + 8 + 2 = 20; 4 = 2 x 2; 6 = (4 + 8)/2; all different. Verified by script over all 4-digit codes with distinct digits; only 4682.
**Explain simply:**
- The average of two numbers is the middle number of an evenly spaced trio, so a, b, c form an even step (4, 6, 8).
- Always use a "can this be divided by 3" test to cut the search.
**Likely follow-ups:** What if the sum were 17? Then 3b = 17 - d must be a multiple of 3, so d = 2, b = 5, a = 4, c = 6: code 4562. Checked by script (the only code).
**Common mistakes / traps:** Allowing a first digit of 0 (then a = 2d forces d = 0 too, breaking "different digits"); forgetting that all four digits must differ.

### Q32 ⭐⭐ 🟡 The numbers 1 to 9 are each used exactly once to fill a 3 x 3 grid. The three row sums, from top to bottom, are 21, 10 and 14. The three column sums, from left to right, are 20, 13 and 12. The number in row 2, column 1 is 5, the number in row 1, column 2 is 7 and the number in row 3, column 3 is 3. What number is in the centre cell (row 2, column 2)?
**Asked at:** commonly asked (no company-specific report found); number-grid puzzles are a standard analytics-puzzle type (unverified).
**What the interviewer is checking:** Using row and column sums together, filling the grid cell by cell.
**Say this in the interview:** "Given cells first, then use the row sums to find the two unknowns in each row. The centre comes out as 4."
**Answer:** **4**
**Step-by-step reasoning:**
1. Known: R1C2 = 7, R2C1 = 5, R3C3 = 3.
2. Column 1 sums to 20 and holds 5, so R1C1 + R3C1 = 15. Two different digits from 1 to 9 adding to 15: (6, 9) or (7, 8). 7 is already used, so (6, 9).
3. Row 1 sums to 21 and holds 7, so R1C1 + R1C3 = 14. R1C1 is 6 or 9: 6 gives R1C3 = 8; 9 gives R1C3 = 5, but 5 is already used. So R1C1 = 6, R1C3 = 8, and R3C1 = 9.
4. Row 3 sums to 14: 9 + R3C2 + 3 = 14, so R3C2 = 2.
5. Column 2 sums to 13: 7 + R2C2 + 2 = 13, so R2C2 = 4. Then row 2: 5 + 4 + R2C3 = 10, so R2C3 = 1.
```
6 7 8 | 21
5 4 1 | 10
9 2 3 | 14
```
Digits used: 6,7,8,5,4,1,9,2,3, each once.
**Fast method (30 seconds):** Start with the column or row that already has a given cell, list the digit pairs for that sum, and cross out used digits.
**Check:** Columns: 6 + 5 + 9 = 20, 7 + 4 + 2 = 13, 8 + 1 + 3 = 12. Verified by script over all 362,880 arrangements; this is the only grid that fits.
**Explain simply:**
- Each sum is a small equation; one given number turns a 3-term sum into a 2-term sum, which has few options.
- "Each digit once" lets you cross out repeated digits.
**Likely follow-ups:** Why is the given 7 needed? It removes the pair (7, 8) in step 2; without it that step would have two options (not re-run without the clue).
**Common mistakes / traps:** Forgetting that digits cannot repeat (accepting 5 in R1C3), or using a pair like (7, 8) that includes a digit already placed.

### Q33 ⭐⭐ 🟡 A 4 x 4 grid must be filled with the digits 1 to 4 so that every row, every column and each of the four 2 x 2 corner boxes (rows 1-2 x columns 1-2, rows 1-2 x columns 3-4, rows 3-4 x columns 1-2, rows 3-4 x columns 3-4) contains each digit exactly once. A dot means empty.

| | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| R1 | 3 | 1 | · | · |
| R2 | · | · | 3 | · |
| R3 | · | · | 2 | 3 |
| R4 | · | · | · | 4 |

What is the sum of the four digits on the main diagonal (R1C1, R2C2, R3C3, R4C4) of the completed grid?
**Asked at:** commonly asked (no company-specific report found); mini-sudoku is a common puzzle-round format (prep-site claim, unverified).
**What the interviewer is checking:** Placing digits with "last remaining" and row/column/box elimination.
**Say this in the interview:** "I fill the forced cells one by one. The completed diagonal is 3, 2, 2, 4, sum 11."
**Answer:** **11**
**Step-by-step reasoning:**
1. Top-left box has 3 and 1, so R2C1 and R2C2 are {2, 4}. Row 2 has 3 at C3, so R2C4 = 1 (the only digit left: row needs 1, 2, 4 in C1, C2, C4, and C1, C2 take 2 and 4).
2. Top-right box has 3 (R2C3) and 1 (R2C4), so R1C3 and R1C4 are {2, 4}. Row 1 already has 3 and 1, so that works. Column 4 has 1 (R2) and 3 and 4 below, so R1C4 = 2. Then R1C3 = 4.
3. Column 3 now has 4, 3, 2, so R4C3 = 1. Row 4 has 1 and 4; R4C1, R4C2 are {2, 3}.
4. Bottom-right box: 2, 3, 1, 4 all present, good. Column 1 has 3 on top, so R4C1 = 2 and R4C2 = 3.
5. Column 2 has 1 (R1) and 3 (R4); R2C2 and R3C2 are {2, 4}. Row 3 needs 1, 4 in C1, C2 (it has 2, 3). Column 2 cannot take 1, so R3C2 = 4, R3C1 = 1. Then R2C2 = 2 and R2C1 = 4.
```
3 1 4 2
4 2 3 1
1 4 2 3
2 3 1 4
```
**Fast method (30 seconds):** Look for a box or row with three cells filled; the fourth is forced. Work from the most filled boxes outward.
**Check:** Every row, column and box holds 1 to 4 once. Verified by script over all grids: exactly one solution; diagonal 3 + 2 + 2 + 4 = 11.
**Explain simply:**
- In a 1-to-4 grid, each row, column and box must hold each digit once; "what is missing here?" fills cells.
- A puzzle designed with one solution is solved without guessing.
**Likely follow-ups:** What is the sum of the other diagonal (R1C4, R2C3, R3C2, R4C1)? 2 + 3 + 4 + 2 = 11, read from the grid above.
**Common mistakes / traps:** Placing a digit that fits the row but repeats in the column; forgetting the 2 x 2 box rule.

### Q34 ⭐⭐ 🟡 A payroll run has seven tasks: P (pull attendance), V (validate attendance), L (apply leave adjustments), T (update tax slabs), C (compute pay), A (approve) and D (disburse). Order rules: P comes before V and before L; V, L and T all come before C; C comes before A; A comes before D. Tasks are done one at a time. In how many different orders can the seven tasks be completed?
**Asked at:** commonly asked (no company-specific report found); counting valid orders is a topic in prep-site puzzle collections (unverified).
**What the interviewer is checking:** Splitting a precedence problem into a fixed part and a free part, then counting.
**Say this in the interview:** "C, A, D are always last, in that order. The first four are P, V, L, T with P before V and L. That gives 8 orders."
**Answer:** **8 orders**
**Step-by-step reasoning:**
1. C needs V, L and T done; A and D follow C in a fixed order. So the last three positions are C, A, D.
2. The first four slots hold P, V, L, T, with P before V and before L. T has no rule among them.
3. Order P, V, L only: P first, then V and L in either order, so 2 ways (PVL or PLV).
4. Insert T into any of the 4 gaps (before, between, after): 2 x 4 = 8.
5. Total orders: 8.
**Fast method (30 seconds):** Of the 3! = 6 orders of P, V, L, P is first in exactly 1 of 3 (the fraction 1/3), giving 2. Inserting one free task into 3 items multiplies by 4. Result 2 x 4 = 8.
**Check:** Verified by script over all 5,040 orderings; 8 satisfy every rule.
**Explain simply:**
- A "linear extension" is just a full order that respects every "must come before" rule. We count those.
- Free tasks (T) can slide anywhere before their successor, multiplying the count.
**Likely follow-ups:** If T had to come after P as well? T after P: P first, then V, L, T in any order = 6 orders. Hand-checked.
**Common mistakes / traps:** Counting 7! / something loosely; forgetting T is free (answering 2); treating V before L as a rule.

### Q35 ⭐⭐ 🟡 Seven interviews need meeting rooms: I1 09:00-10:30, I2 09:30-11:00, I3 10:00-11:30, I4 10:30-12:00, I5 11:00-12:30, I6 11:30-13:00, I7 12:00-13:00. A room becomes free the moment an interview in it ends, so an interview may start in a room at the exact time another ends. What is the minimum number of rooms needed?
**Asked at:** commonly asked (no company-specific report found); meeting-room scheduling is a classic (the "meeting rooms II" family) in analytics and coding interviews (prep-site claim, unverified).
**What the interviewer is checking:** Recognising that rooms needed equals the largest number of overlapping interviews at one moment.
**Say this in the interview:** "I find the busiest moment. At 11:00 to 11:30 interviews I3, I4 and I5 overlap, and no moment has four. So 3 rooms."
**Answer:** **3 rooms**
**Step-by-step reasoning:**
1. Count interviews running at each interesting time (a start counts after an end at the same minute).
2. 09:30: I1, I2 (2). 10:00: I1, I2, I3 (3). 10:30 (I1 ends, I4 starts): I2, I3, I4 (3). 11:00 (I2 ends, I5 starts): I3, I4, I5 (3). 11:30 (I3 ends, I6 starts): I4, I5, I6 (3). 12:00 (I4 ends, I7 starts): I5, I6, I7 (3).
3. The maximum is 3, so 3 rooms are needed at least.
4. 3 are enough: Room A: I1, I4, I7 (ends 10:30, 12:00); Room B: I2, I5 (ends 11:00); Room C: I3, I6 (ends 11:30).
```
Room A: I1 09:00-10:30 | I4 10:30-12:00 | I7 12:00-13:00
Room B: I2 09:30-11:00 | I5 11:00-12:30
Room C: I3 10:00-11:30 | I6 11:30-13:00
```
**Fast method (30 seconds):** Sweep line: list all starts (+1) and ends (-1) in time order, ends first on ties, and track the running total; its maximum is the answer.
**Check:** Verified by script (sweep line gives maximum 3); the schedule above has no clash in any room.
**Explain simply:**
- Two interviews can share a room only if one ends before or when the other starts.
- At the busiest moment every interview running then needs its own room, so that count is a floor; here it can also be met.
**Likely follow-ups:** If a room were not free until after the end minute (an interview could not start the moment another ends)? Then 4 rooms are needed (at 10:30, I1, I2, I3 and I4 would all count); verified by script.
**Common mistakes / traps:** Counting a back-to-back end and start as an overlap (answering 4); counting all 7 interviews.

### Q36 ⭐⭐ 🟡 A migration project has seven tasks with durations (days) and prerequisites: A (3 days, none), B (2 days, needs A), C (4 days, needs A), D (3 days, needs B), E (2 days, needs C and D), F (1 day, needs E), G (5 days, needs B). Tasks with no dependency between them can run in parallel, and there are enough people for that. What is the minimum number of days to finish the whole project?
**Asked at:** commonly asked (no company-specific report found); critical-path scheduling is a common project-analyst topic (prep-site claim, unverified).
**What the interviewer is checking:** Finding the longest chain of dependent tasks (the critical path).
**Say this in the interview:** "Earliest finish of each task is its duration plus the latest finish of its prerequisites. F ends at day 11, G at day 10, so the project takes 11 days."
**Answer:** **11 days**
**Step-by-step reasoning:**
1. A: no prerequisite, finishes at day 3.
2. B (needs A): 3 + 2 = 5. C (needs A): 3 + 4 = 7.
3. D (needs B): 5 + 3 = 8. G (needs B): 5 + 5 = 10.
4. E (needs C and D): starts when the later of 7 and 8 is done, so day 8; ends 8 + 2 = 10.
5. F (needs E): 10 + 1 = 11.
6. The project ends when all tasks end: max(F = 11, G = 10) = 11.
7. Critical path: A, B, D, E, F = 3 + 2 + 3 + 2 + 1 = 11.
**Fast method (30 seconds):** Write the earliest finish beside each task from left to right, using the maximum over prerequisites. The largest finish is the project length.
**Check:** Verified by script (earliest-finish calculation); the chain A-B-D-E-F also adds to 11 by hand.
**Explain simply:**
- The critical path is the longest chain of tasks that each wait for the previous one; speeding anything off it does not shorten the project.
- A task with two prerequisites waits for the slower one.
**Likely follow-ups:** If D took 1 day instead of 3? D ends 6, E starts at 7 (after C), E ends 9, F 10; project 10 days, and C-E-F becomes critical. Computed by hand.
**Common mistakes / traps:** Adding all durations (20 days); forgetting G can run alongside D and still must finish; taking only one prerequisite of E.

### Q37 ⭐⭐ 🟡 Four auditors must each take exactly one of four audits. The table gives the hours each auditor needs for each audit.

| Auditor | Audit 1 | Audit 2 | Audit 3 | Audit 4 |
|---|---|---|---|---|
| Auditor 1 | 9 | 2 | 7 | 8 |
| Auditor 2 | 6 | 4 | 3 | 7 |
| Auditor 3 | 5 | 8 | 1 | 8 |
| Auditor 4 | 7 | 6 | 9 | 4 |

What is the minimum possible total number of hours?
**Asked at:** commonly asked (no company-specific report found); assignment problems appear in operations-research style prep (unverified).
**What the interviewer is checking:** Trying all one-to-one matchings, not just picking each row's cheapest cell.
**Say this in the interview:** "There are only 4! = 24 ways to assign. The cheapest is Auditor 1 to Audit 2, 2 to Audit 1, 3 to Audit 3, 4 to Audit 4, total 13 hours."
**Answer:** **13 hours**
**Step-by-step reasoning:**
1. Each auditor gets a different audit, so there are 4! = 24 assignments.
2. Row minimums: Auditor 1 best at Audit 2 (2), Auditor 2 at Audit 3 (3), Auditor 3 at Audit 3 (1), Auditor 4 at Audit 4 (4). Audit 3 is wanted twice, so a conflict.
3. Give Audit 3 to Auditor 3 (saves most; 1 hour). Auditor 2 then takes Audit 1 (6; the next-best, Audit 2 at 4, is needed by Auditor 1).
4. Assignment: A1 to Audit 2 (2), A2 to Audit 1 (6), A3 to Audit 3 (1), A4 to Audit 4 (4). Total 2 + 6 + 1 + 4 = 13.
5. The next-best assignments total 14 and 17 (the other 21 are higher).
**Fast method (30 seconds):** Take the cheapest cell, then the cheapest in the remaining rows and columns, then check swaps of two people. For 4 x 4, listing all 24 is also quick. (Greedy is not safe in general; here the result was confirmed by full enumeration.)
**Check:** Verified by script over all 24 assignments; the minimum 13 is reached by one assignment only, the next best is 14.
**Explain simply:**
- This is the "assignment problem": match people to jobs one-to-one at minimum total cost.
- Picking each person's own best job can clash; a swap check fixes it.
**Likely follow-ups:** What is the maximum total? 33 hours (computed by script over all 24 assignments).
**Common mistakes / traps:** Adding row minimums 2 + 3 + 1 + 4 = 10 (invalid, Audit 3 used twice); picking cheapest per column.

### Q38 ⭐⭐ 🟡 Four teams A, B, C and D play a single round robin (each pair plays once). A win earns 3 points, a draw 1 point and a loss 0. Final points: A 6, B 4, C 1, D 5. Which matches were drawn, and who won the match between A and D?
**Asked at:** commonly asked (no company-specific report found); points-table reconstruction is a standard games-and-tournaments item (prep-site claim, unverified).
**What the interviewer is checking:** Using total points and win counts to rebuild match results.
**Say this in the interview:** "Total points are 16 across 6 matches, so 4 matches had a winner and 2 were draws. The draws are B v D and C v D, and D beat A."
**Answer:** **Drawn matches: B v D and C v D. D won the match against A.**
**Step-by-step reasoning:**
1. There are 4 x 3 / 2 = 6 matches. Total points = 6 + 4 + 1 + 5 = 16. A win match gives 3 points, a draw gives 2. With w wins and d draws, w + d = 6 and 3w + 2d = 16, so w = 4, d = 2.
2. A has 6 points: with 3 matches, options are two wins and a loss (6) or one win and three draws (impossible with only 3 matches). So A: 2 wins, 1 loss, 0 draws.
3. C has 1 point: exactly one draw and two losses.
4. B has 4 = one win and one draw and a loss. D has 5 = one win and two draws.
5. The 2 draws touch 4 team slots: C has one draw, B has one, D has two. So the draws are B v D and C v D.
6. Then the wins: A beat B and C (A's wins), A lost to D (D's win). B beat C. Check D: win vs A, draws with B and C = 5. B: beat C, draw D, lost A = 4. C: lost to A, lost to B, drew D = 1.
```
A beat B, A beat C, D beat A, B beat C, B draw D, C draw D
```
**Fast method (30 seconds):** Use the points total (16) to count draws, then each team's points decompose into wins and draws in few ways (a team on 1 point has exactly 1 draw).
**Check:** Verified by script over all 3^6 = 729 result combinations; exactly one gives A 6, B 4, C 1, D 5.
**Explain simply:**
- A decisive match gives out 3 points, a draw gives out 2, so the total points reveal the number of draws.
- A team's points often split into wins and draws in only one way.
**Likely follow-ups:** How many points are handed out in total? Each decisive match gives 3 and each draw gives 2, so 4 x 3 + 2 x 2 = 16, matching 6 + 4 + 1 + 5.
**Common mistakes / traps:** Assuming A beat D because A has the most points; forgetting each team plays exactly 3 matches.

### Q39 ⭐⭐ 🟡 A knockout tournament has 22 players. In round 1 some players get a bye (advance without playing) so that exactly 16 players remain for round 2, and no byes are given after round 1. How many players get a bye in round 1, how many matches are played in round 1, and how many matches are played in the whole tournament?
**Asked at:** commonly asked (no company-specific report found); knockout and bye counting is a standard games-and-tournaments item (prep-site claim, unverified).
**What the interviewer is checking:** Bye arithmetic and the "one loser per match" rule.
**Say this in the interview:** "To reach 16 we must remove 6 players, one per match, so 6 matches in round 1 with 12 players, and 10 byes. Total matches are 22 - 1 = 21."
**Answer:** **10 byes, 6 matches in round 1, 21 matches in total.**
**Step-by-step reasoning:**
1. Round 1 must cut 22 down to 16, a loss of 6 players. Each match eliminates exactly one player, so 6 matches.
2. 6 matches use 12 players. The other 22 - 12 = 10 players get a bye.
3. Check survivors: 6 winners + 10 byes = 16.
4. After that, 16 to 8 to 4 to 2 to 1: 8 + 4 + 2 + 1 = 15 matches.
5. Total = 6 + 15 = 21 = 22 - 1.
**Fast method (30 seconds):** Total matches = players - 1, because each match removes one player and only the champion is left. Byes = 2 x 16 - 22 = 10 (the 16 slots in round 2 each need one winner or one bye).
**Check:** Verified by script (round-by-round simulation: 6 + 8 + 4 + 2 + 1 = 21).
**Explain simply:**
- A bye means a free pass into the next round; it is not a match, so it removes nobody.
- With 21 eliminations needed to leave one champion, there are 21 matches, however the byes are given.
**Likely follow-ups:** 37 players to reach 32: 5 matches, 27 byes, 36 matches in total; by hand.
**Common mistakes / traps:** Counting a bye as a match; saying 11 matches in round 1 (22 / 2) and ignoring byes.

### Q40 ⭐⭐ 🟡 Six players play a chess round robin (each pair plays once; a win scores 1 point, a draw 0.5 and a loss 0). Five players finish with 4, 3.5, 3, 2.5 and 1.5 points. How many points did the sixth player score?
**Asked at:** commonly asked (no company-specific report found); score-total shortcut questions are common in games-and-tournaments sets (prep-site claim, unverified).
**What the interviewer is checking:** Seeing that every game hands out exactly 1 point in total.
**Say this in the interview:** "Six players play 15 games, each worth 1 point, so the total is 15. The five known scores add to 14.5, so the sixth scored 0.5."
**Answer:** **0.5 points**
**Step-by-step reasoning:**
1. Number of games = 6 x 5 / 2 = 15.
2. Each game gives out exactly 1 point (1 + 0, or 0.5 + 0.5). Total points = 15.
3. Known scores: 4 + 3.5 + 3 + 2.5 + 1.5 = 14.5.
4. Sixth player = 15 - 14.5 = 0.5.
**Fast method (30 seconds):** Total = number of games. Subtract the known scores.
**Check:** Computed by script (15 - 14.5 = 0.5); a maximum for any one player is 5, so 0.5 is feasible. Whether the full table is achievable was not separately enumerated.
**Explain simply:**
- A round robin with n players has n(n - 1)/2 games.
- In chess, every game hands out exactly 1 point in total, so the total of all scores equals the number of games.
**Likely follow-ups:** What if football scoring (3-1-0) were used? The total then depends on how many draws there were, so the shortcut does not work.
**Common mistakes / traps:** Using 6 x 5 = 30 games (double counting); thinking you need the individual results.

### Q41 ⭐⭐ 🟡 A 3-digit locker number has three different digits and is divisible by 9. Its middle digit equals the sum of its first and last digits. It is greater than 500, its first digit is odd and its last digit is greater than 3. What is the number?
**Asked at:** commonly asked (no company-specific report found); digit puzzles are listed in prep-site topic lists (unverified).
**What the interviewer is checking:** Combining the divisibility-by-9 rule with digit conditions to shrink the search.
**Say this in the interview:** "If the middle digit is the sum of the outer two, the digit sum is twice the middle digit, so for divisibility by 9 the middle digit must be 9. Then 5 + 9 + ... gives 594."
**Answer:** **594**
**Step-by-step reasoning:**
1. A number is divisible by 9 if its digit sum is a multiple of 9.
2. Digit sum = first + middle + last = 2 x middle (since middle = first + last). So 2 x middle is a multiple of 9; middle is 9 (or 0, impossible here).
3. Middle = 9, so first + last = 9.
4. First digit is odd and above 5 or equal to 5 (number > 500): 5, 7 or 9. Last digit = 9 - first: 4, 2, 0. Last digit must be above 3, so first = 5, last = 4.
5. The number is 594; first 5 is odd, last 4 > 3, digits different, 594 = 9 x 66.
**Fast method (30 seconds):** "Middle = first + last" gives digit sum 2 x middle, so "divisible by 9" means middle = 9. Then only first + last = 9 remains.
**Check:** Verified by script over every number from 501 to 999; only 594 qualifies.
**Explain simply:**
- Divisibility by 9: add the digits; if the sum is in the 9 times table, the number is too.
- When a clue links digits, use it before trying numbers.
**Likely follow-ups:** If the number had to be above 700? Then no number qualifies: first digit 7 gives last digit 2, first digit 9 gives last digit 0, both fail "last digit above 3" (hand-checked).
**Common mistakes / traps:** Ignoring "greater than 500" and offering 693 or 396; forgetting the last digit must exceed 3.

### Q42 ⭐⭐ 🟡 Meena, Naveen, Omkar and Pooja are four newly hired employees placed in four different departments (HR, Finance, IT, Sales); each travels to the office by a different mode (bus, metro, bike, car). Clues: (1) Pooja is the Finance employee. (2) The Finance employee is not the metro commuter. (3) Meena is not the HR employee. (4) The IT employee is the bus commuter. (5) Omkar is not the HR employee. (6) The HR employee is the car commuter. (7) Omkar is not the bus commuter. Who is placed in IT, and how does that person travel?
**Asked at:** commonly asked (no company-specific report found); matching grids are listed for TCS, Infosys, Wipro and Accenture in prep-site topic lists (unverified).
**What the interviewer is checking:** Filling a who-owns-what grid with positive clues first, then eliminating.
**Say this in the interview:** "Pooja is Finance. HR is not Meena or Omkar, so HR is Naveen. Omkar is not IT (IT travels by bus and Omkar does not), so Omkar is Sales and Meena is IT, travelling by bus."
**Answer:** **Meena is in IT and travels by bus.**
**Step-by-step reasoning:**
1. Clue 1: Pooja = Finance.
2. HR candidates: not Pooja (Finance), not Meena (3), not Omkar (5). So Naveen = HR, and clue 6 gives Naveen = car.
3. Left: Meena and Omkar for IT and Sales. IT travels by bus (4) and Omkar is not a bus commuter (7), so Omkar is not IT. Omkar = Sales, Meena = IT, Meena = bus.
4. Modes left: metro and bike for Pooja (Finance) and Omkar (Sales). Finance is not metro (2), so Pooja = bike, Omkar = metro.
```
Meena  IT      bus
Naveen HR      car
Omkar  Sales   metro
Pooja  Finance bike
```
**Fast method (30 seconds):** Start with the elimination "HR is none of Pooja, Meena, Omkar"; a person is forced. Then link department to mode through the clues (IT = bus, HR = car).
**Check:** Re-read all 7 clues against the table: all hold. Verified by script over all 576 department-and-mode combinations; this is the only solution.
**Explain simply:**
- Clues like "the IT employee is the bus commuter" glue two columns of the grid together, so solving one fills the other.
- When three of four people are ruled out of a slot, the fourth must fill it.
**Likely follow-ups:** If clue 7 were removed, would the answer stay unique? No: a second solution appears with Omkar in IT (bus) and Meena in Sales (metro); verified by script, 2 solutions.
**Common mistakes / traps:** Forgetting clue 6 gives Naveen's mode; assigning Pooja metro because it remains, though clue 2 forbids it.

### Q43 ⭐⭐ 🟡 How do you check that a round-robin points table is internally consistent (total points, total wins and losses, number of draws) before trying to find the individual results?
**Asked at:** commonly asked (no company-specific report found); round-robin and points-table items are listed under "games and tournaments" in prep-site reasoning topics (unverified).
**What the interviewer is checking:** Whether you test the data for sense with totals before hunting for results.
**Say this in the interview:** "A round robin of n teams has n(n-1)/2 matches. A decisive match hands out 3 points, a draw hands out 2, so total points = 3 x (matches) - d, where d is the number of draws. I check that the totals fit before I solve anything."
**Answer:** **Count the matches, then compare the points total with 3 x matches. The gap is exactly the number of draws, and it must be a whole number between 0 and the number of matches.**
**Step-by-step reasoning:**
1. Matches = n(n-1)/2 (each pair plays once).
2. Add all the points in the table. Call this S.
3. If every match were decisive, S would be 3 x matches. Each draw loses one point (2 given out instead of 3). So draws d = 3 x matches - S.
4. Sanity: d must be a whole number and 0 <= d <= matches. Decisive matches = matches - d, and total wins = total losses = decisive matches.
5. Each team's wins, draws and losses must add up to the games it played, and each team's points = 3W + D.
**Worked example (numbers verified by script):** 4 teams, points 6, 4, 1, 5. Matches = 6. S = 16. d = 18 - 16 = 2 draws, so 4 decisive matches: 4 wins and 4 losses in total. Another table: 5 teams, 10 matches, points total 20. Then draws = 30 - 20 = 10, so every match was drawn and every team has exactly 4 points; any other table with total 20 is inconsistent. In a chess table (1 point per match shared as 1 or 0.5 + 0.5), total points must equal the number of matches exactly: 5 known scores 4, 3.5, 3, 2.5, 1.5 sum to 14.5, so the sixth player has 15 - 14.5 = 0.5.
**Explain simply:**
- Round robin: every team plays every other team once.
- The total is a check, not an answer: it only says the table could be real.
- With 3-1-0 scoring, a draw "costs" one point of the pool.
**Likely follow-ups:** 1) *Could a 4-team table total 19 points?* No: 3 x 6 = 18 is the maximum. 2) *Table total 17?* Then d = 1, which is fine.
**Common mistakes / traps:** Using n(n-1) instead of n(n-1)/2; forgetting that a draw gives 2 points in total; assuming draws count as decisive matches.

### Q44 ⭐⭐ 🟡 What is the difference between "must be true", "could be true" and "cannot be true" questions in a constraint puzzle, and how do you answer each one efficiently?
**Asked at:** commonly asked (no company-specific report found); this question style is the standard format of constraint-puzzle sets (prep-site material, unverified).
**What the interviewer is checking:** Whether you treat the answer as a property of ALL valid solutions, not of the one you happened to find.
**Say this in the interview:** "Must be true means true in every valid arrangement. Could be true means true in at least one. Cannot be true means false in every one. So I first list all valid arrangements, then check each option against the whole list."
**Answer:** **Must = true in all valid solutions; could = true in at least one; cannot = true in none. Build the full list of valid solutions once, then test each option against it.**
**Step-by-step reasoning:**
1. List every arrangement that obeys all the rules (or the compact set of cases).
2. "Must be true": look for the option that appears in every case. One counterexample kills an option.
3. "Could be true": find one valid case where the option holds. One example is enough to prove it.
4. "Cannot be true": show that adding the option breaks a rule in every case.
5. Note: "must" implies "could" (if the list is non-empty), and "cannot" is the opposite of "could".
**Worked example (verified by script):** Panel of 3 from Asha, Bimal, Chitra, Dev, Esha, Farah with the rules from Q12. Valid panels: {Asha, Dev, Esha}, {Asha, Esha, Farah}, {Bimal, Dev, Esha}, {Bimal, Esha, Farah}, {Chitra, Dev, Esha}. Esha is in all five, so "Esha must be on the panel". Chitra is in one, so "Chitra could be on it". Asha with Bimal appears in none, so "Asha and Bimal both on the panel cannot be true".
**Explain simply:**
- Think of the valid arrangements as a list of "possible worlds"; the question word tells you how many worlds must agree.
- Disproving "must" needs just one counterexample; proving "could" needs just one example.
**Likely follow-ups:** 1) *Which person cannot be on a panel with Chitra?* Farah (Chitra needs Dev, and Dev and Farah cannot be together). 2) *Is "not Farah" a must when Chitra is chosen?* Yes.
**Common mistakes / traps:** Picking an option because it is true in the one solution you found; confusing "could be true" with "must be true".

### Q45 ⭐⭐ 🟡 A selection puzzle says "If Chitra is chosen, Dev must be chosen." What does this rule tell you when Chitra is not chosen, what does it tell you when Dev is not chosen, and how do you use it to list all valid teams?
**Asked at:** commonly asked (no company-specific report found); conditional selection rules are a standard constraint-puzzle form (prep-site material, unverified).
**What the interviewer is checking:** Correct use of an "if-then" rule: the forward direction and the contrapositive, and not the converse.
**Say this in the interview:** "If Chitra is out, the rule says nothing about Dev. If Dev is out, then Chitra must be out too, because Chitra would force Dev in. So Chitra never appears without Dev."
**Answer:** **Chitra not chosen: the rule tells you nothing (Dev may be in or out). Dev not chosen: Chitra cannot be chosen (the contrapositive). Valid teams are only those with Chitra absent, or with Chitra AND Dev both present.**
**Step-by-step reasoning:**
1. Write the rule as C -> D (C = Chitra chosen, D = Dev chosen).
2. Contrapositive: not D -> not C. This is always logically equivalent to the original rule.
3. Converse (D -> C) and inverse (not C -> not D) are NOT implied. Dev can be chosen alone.
4. To list teams, split into two cases: Chitra in (then Dev is in too, fill the rest) and Chitra out (ignore the rule, apply the other rules).
5. Apply the other rules inside each case.
**Worked example (verified by script):** Panel of 3 from the six, with Q12's rules. Chitra in: Dev in; the third must be Esha (Farah is blocked by Dev): {Chitra, Dev, Esha}, 1 panel. Chitra out: 4 panels from the other five people ({Asha, Dev, Esha}, {Asha, Esha, Farah}, {Bimal, Dev, Esha}, {Bimal, Esha, Farah}). Total 5.
**Explain simply:**
- "If A then B" only promises something when A happens.
- The contrapositive ("if not B then not A") is the same rule seen from the other side.
- Converse and inverse are different statements and may be false.
**Likely follow-ups:** 1) *Name the fallacy of reading C -> D as D -> C.* Affirming the consequent. 2) *Reading it as not C -> not D?* Denying the antecedent.
**Common mistakes / traps:** Thinking that "Chitra is out" forces Dev out, or that "Dev is in" forces Chitra in.

### Q46 ⭐⭐ 🟡 A set of questions shares one puzzle, and one question begins "If Esha is on the panel, which of the following must be true?" Does that extra condition carry over to the other questions in the set, and how should you work such a question?
**Asked at:** commonly asked (no company-specific report found); "if ... then which must be true" sub-questions are a common set format (prep-site material, unverified).
**What the interviewer is checking:** Whether you keep the base rules fixed and treat each "if" as a temporary, local assumption.
**Say this in the interview:** "No, the extra 'if' applies only to that question. The original rules stay for every question. I add the new condition, redo the possible cases, and then see what holds in all of them."
**Answer:** **No. The new condition applies only to that one question; the base rules apply to all questions in the set.**
**Step-by-step reasoning:**
1. Copy the base rules to a fresh scratch area for this question.
2. Add the new condition ("Esha is on the panel") as an extra fact.
3. List the cases that satisfy the base rules and the new fact (the list is usually shorter).
4. Pick the option that is true in all of these cases (must), or in at least one (could).
5. For the next question, throw the extra fact away and go back to the base rules.
**Worked example (verified by script):** Base rules are those in Q12. With the added fact "Farah is on the panel", the valid panels shrink to {Asha, Esha, Farah} and {Bimal, Esha, Farah}, so "Esha must be on the panel" is true for that question. Without the extra fact, a different question may allow {Chitra, Dev, Esha}, where Farah is absent. Esha is in all five base panels, so here the "if Esha" condition removes nothing; this is allowed, and it just means the condition was not restrictive.
**Explain simply:**
- A "what if" question explores a smaller world; it does not rewrite the puzzle.
- Reusing an earlier "if" by mistake is the most common way to lose marks in a set.
**Likely follow-ups:** 1) *If Dev is on the panel, can Farah be?* No (rule 4). 2) *What if the extra condition contradicts the base rules?* Then the question has no valid case; recheck for an error.
**Common mistakes / traps:** Carrying a previous question's condition into the next; ignoring a base rule in the "if" world.

### Q47 ⭐⭐ 🟡 What is the difference between the minimum time to finish a project with prerequisite tasks (critical path) and the number of valid orders in which the tasks can be done one at a time, and how do you compute each?
**Asked at:** commonly asked (no company-specific report found); scheduling and precedence items appear in puzzle collections (prep-site material, unverified).
**What the interviewer is checking:** Whether you separate "how long" (parallel work) from "in what sequence" (one at a time).
**Say this in the interview:** "Minimum time assumes people work in parallel, so it is the longest chain of dependent tasks, the critical path. The number of orders assumes one task at a time and counts every sequence that respects the prerequisites."
**Answer:** **Critical path = the longest total duration along a chain of dependent tasks (this is the minimum project time with enough workers). Number of orders = the count of one-at-a-time sequences that put every prerequisite before its task. They answer different questions.**
**Step-by-step reasoning:**
1. Critical path: for each task, finish time = its duration + the latest finish time among its prerequisites. The largest finish time is the project length.
2. Orders: count the sequences (topological orders) where each task comes after its prerequisites. For small cases, build the order by choosing at each step any task whose prerequisites are done.
3. Duration does not matter for the order count; the arrows do not matter for ordinary "choose any" counting except through the rules.
**Worked example (verified by script):** Migration project (Q36): finish times A 3, B 5, C 7, D 8, E 10, F 11, G 10. The longest chain A-B-D-E-F is 3+2+3+2+1 = 11 days. For the payroll tasks of Q34 (P, V, L, T, C, A, D), brute force over all 5040 permutations gives 8 valid orders.
**Explain simply:**
- Parallel work: several people work at once, so you only wait for the longest chain.
- One at a time: a valid order is any list in which no task appears before its prerequisites.
- A task that is on the critical path is one where delay delays the whole project.
**Likely follow-ups:** 1) *Does adding a short side task change the project time?* Not if it fits inside slack and is not on the critical path. 2) *Can two projects have the same orders but different times?* Yes, change the durations only.
**Common mistakes / traps:** Adding all durations (28 days in Q36 instead of 11); counting orders as if all tasks were free (7! = 5040).

### Q48 ⭐⭐ 🔴 Five colleagues Anu, Bala, Chitra, Dev and Esha work in five different departments (HR, Finance, IT, Ops, Sales) and each uses a different way to get to office (bus, metro, bike, car, walk). Clues: (1) The Sales employee is the metro commuter. (2) The Finance employee is the bike commuter. (3) Anu is the HR employee. (4) The IT employee is the bus commuter. (5) The Ops employee is the car commuter. (6) Dev is not the Finance employee. (7) Bala is not the bike commuter. (8) Bala is not the Ops employee. (9) Dev is not the car commuter. (10) Dev is not the IT employee. (11) Chitra is not the bike commuter. Who works in Ops, and how does that person commute?
**Asked at:** commonly asked (no company-specific report found); matching grids are listed for TCS, Infosys, Wipro, Accenture and Cognizant in prep-site pages (unverified).
**What the interviewer is checking:** Merging two attributes into one (department fixes mode) and then eliminating.
**Say this in the interview:** "Clues 1, 2, 4, 5 tie each department to a mode, so HR must take the leftover mode, walk. Then I eliminate people. Chitra is the Ops employee, and she travels by car."
**Answer:** **Chitra works in Ops and commutes by car.**
**Step-by-step reasoning:**
1. Departments link to modes: Sales = metro, Finance = bike, IT = bus, Ops = car. The only mode left is walk, so HR = walk.
2. Anu is HR (clue 3), so Anu walks.
3. Dev is not Finance (6), not IT (10), not HR (Anu) and not Ops (Ops = car, clue 9 says Dev is not car). So Dev is Sales (metro).
4. Bala is not bike, so not Finance (7); not Ops (8); HR and Sales are taken. So Bala is IT (bus).
5. Chitra and Esha share Finance and Ops. Chitra is not the bike commuter (11), so she is not Finance. Chitra = Ops (car), Esha = Finance (bike).
```
Anu   HR      walk
Bala  IT      bus
Chitra Ops    car
Dev   Sales   metro
Esha  Finance bike
```
Unique because every step above was forced; a brute force over all 120 x 120 assignments found exactly 1 solution.
**Fast method (30 seconds):** First merge the "department = mode" clues so that only one attribute remains; then fill the most restricted person (Dev) first.
**Check:** Verified by script (all clues satisfied; exactly one solution).
**Explain simply:**
- When two attributes are tied together by clues, treat them as one column.
- The leftover value goes to the only unlinked item (HR takes walk).
- Work from the person with the most "not" clues.
**Likely follow-ups:** 1) *If clue 11 were dropped, would the answer stay unique?* No (checked by script): Chitra and Esha could swap, so Ops could be either of them. 2) *Who walks?* Anu.
**Common mistakes / traps:** Forgetting that HR gets walk by elimination; ignoring that clue 9 (not car) bars Dev from Ops.

### Q49 ⭐⭐ 🔴 Four analysts Ira, Jay, Kim and Lee differ in tool (Excel, SQL, Python, Tableau), city (Pune, Delhi, Chennai, Kolkata) and department (HR, Finance, IT, Sales); every value is used exactly once. Clues: (1) Kim is the person in Chennai. (2) The Python user is the Finance employee. (3) The Excel user is the Sales employee. (4) Ira is the person in Delhi. (5) The person in Delhi is the Sales employee. (6) The Tableau user is the IT employee. (7) The person in Pune is the Finance employee. (8) Jay is not the Python user. (9) Jay is not the SQL user. Who is in the Sales department, which tool does that person use, and in which city?
**Asked at:** commonly asked (no company-specific report found); three-attribute grids are in the style of analyst-role logic puzzles (a government recruitment puzzle and prep pages show the format; no company report found).
**What the interviewer is checking:** Chaining linked clues across three attributes.
**Say this in the interview:** "Ira is in Delhi, Delhi is Sales, Sales uses Excel. So the Sales person is Ira, using Excel, in Delhi."
**Answer:** **Ira is in Sales, uses Excel and is in Delhi.**
**Step-by-step reasoning:**
1. Clue 4 + 5: Ira is in Delhi and Delhi is Sales, so Ira is Sales.
2. Clue 3: Sales uses Excel, so Ira uses Excel.
3. Clue 2 + 7: Python = Finance = Pune. Clue 6: Tableau = IT. SQL is left with HR.
4. Jay is not Python and not SQL, and Excel is Ira's, so Jay uses Tableau (IT).
5. Kim is in Chennai, so not Pune, so not the Python/Finance person. Kim is not Excel or Tableau, so Kim uses SQL (HR). Lee gets Python (Finance, Pune). Jay gets the last city, Kolkata.
```
Ira  Excel   Sales   Delhi
Jay  Tableau IT      Kolkata
Kim  SQL     HR      Chennai
Lee  Python  Finance Pune
```
Unique: brute force over all 24 x 24 x 24 assignments gave exactly one that meets every clue.
**Fast method (30 seconds):** Look for a name attached to a position (Ira = Delhi) and follow the chain of "is" clues from it.
**Check:** Verified by script.
**Explain simply:**
- Several "is" clues make one chain; once you reach a name, the whole chain belongs to that person.
- Negative clues finish the rest by elimination.
**Likely follow-ups:** 1) *Who is in Pune?* Lee. 2) *If clue 8 were removed?* The puzzle stops being unique: script finds 3 consistent solutions, so clue 8 is needed.
**Common mistakes / traps:** Treating "the person in Pune is Finance" as a name; forgetting that Kim's city rules out Pune.

### Q50 ⭐⭐ 🔴 Four analysts Rhea, Sameer, Tara and Uday differ in tool (Excel, SQL, Python, Tableau), city (Pune, Delhi, Chennai, Kolkata) and department (HR, Finance, IT, Sales); every value is used exactly once. Clues: (1) The person in Delhi is the Finance employee. (2) Tara is the HR employee. (3) The person in Chennai is the IT employee. (4) The Tableau user is the person in Pune. (5) The Python user is the Sales employee. (6) The Excel user is the IT employee. (7) Uday is not the Finance employee. (8) Uday is not the Excel user. (9) Sameer is not the IT employee. Who uses Python, in which city, and in which department?
**Asked at:** commonly asked (no company-specific report found); three-attribute grid, a format shown in analyst-role puzzles (no company report found).
**What the interviewer is checking:** Linking attributes before names, then using "not" clues to place people.
**Say this in the interview:** "Chennai is IT, and IT uses Excel. Python is Sales. Pune uses Tableau, so Pune is not Sales, so Pune is HR and Kolkata is Sales. Tara is HR, and Uday cannot be Finance or IT, so Uday is Sales. Uday uses Python in Kolkata."
**Answer:** **Uday uses Python, works in Kolkata, in the Sales department.**
**Step-by-step reasoning:**
1. Clue 3 + 6: Chennai = IT = Excel. Clue 1: Delhi = Finance. Clue 4: Pune = Tableau. Clue 5: Python = Sales.
2. Python user is not in Pune (Pune uses Tableau), not Chennai (Excel), not Delhi (Finance, not Sales). So Python is in Kolkata, and Kolkata is Sales.
3. Pune is then HR (Tableau). Delhi is Finance (SQL, the remaining tool).
4. Tara is HR, so Tara is in Pune with Tableau.
5. Uday is not Finance (7), not Excel/IT (8), not HR (Tara). So Uday is Sales: Python, Kolkata.
6. Sameer is not IT (9), so Sameer is Finance (Delhi, SQL); Rhea is IT (Chennai, Excel).
```
Rhea   Excel   IT      Chennai
Sameer SQL     Finance Delhi
Tara   Tableau HR      Pune
Uday   Python  Sales   Kolkata
```
Unique: brute force over all 24^3 assignments found exactly one.
**Fast method (30 seconds):** Fuse the clues so each city has a tool and a department; only then use the name clues.
**Check:** Verified by script.
**Explain simply:**
- Build "bundles" (city + tool + department) first, names last.
- The bundle that cannot fit any named exclusion goes to the last person.
**Likely follow-ups:** 1) *Who uses SQL?* Sameer. 2) *Which city has the HR person?* Pune.
**Common mistakes / traps:** Giving Python to the HR person in Pune because Tara is named; mixing up the "not" clues.

### Q51 ⭐⭐ 🔴 Four team leads A, B, C and D are each a knight (always truthful) or a knave (always lying). A says: "C is a knave." B says: "A and D are of different types." C says: "Exactly three of the four of us are knaves." D says: "C is a knight." How many of the four are knaves, and who are they?
**Asked at:** commonly asked (no company-specific report found); a knights-and-knaves item appears in an interview-question bank (page not read, unverified).
**What the interviewer is checking:** Assume-and-check on a four-person puzzle with a count statement.
**Say this in the interview:** "I assume C is a knight and see if it breaks. If C were a knight, D is a knight, A is a knave, B is a knight, so 1 knave, but C says 3: contradiction. So C is a knave, D is a knave, A is a knight and B is a knight. Two knaves: C and D."
**Answer:** **2 knaves: C and D (A and B are knights).**
**Step-by-step reasoning:**
1. Assume C is a knight. Then D (who says C is a knight) is truthful, so D is a knight. A says "C is a knave", which is false, so A is a knave. B says A and D differ: knave vs knight is true, so B is a knight. Knaves = {A} only, but C (a knight) said there are exactly three. Contradiction.
2. So C is a knave. D says "C is a knight", which is false, so D is a knave.
3. A says "C is a knave", which is true, so A is a knight.
4. B says A (knight) and D (knave) differ: true, so B is a knight.
5. Check C's lie: knaves = {C, D} = 2, not 3, so "exactly three" is false, as a knave must say.
```
A knight   B knight   C knave   D knave
```
Unique: all 16 type combinations were enumerated and only this one is consistent.
**Fast method (30 seconds):** Start with the person whose statement is about a count or about one other person (C), since a wrong guess collapses quickly.
**Check:** Verified by script (16 combinations).
**Explain simply:**
- A knight's statement must be true; a knave's statement must be false.
- Knowing C settles D, then A, then B in a chain.
**Likely follow-ups:** 1) *If C had said "exactly two of us are knaves"?* No consistent assignment exists (checked by script), so the puzzle would be flawed. 2) *If D had said "C is a knave" instead?* Two solutions exist (A, D knights and B, C knaves; or only C a knight), so it is no longer unique.
**Common mistakes / traps:** Treating a knave's statement as "partly false"; the whole statement must be false.

### Q52 ⭐⭐ 🔴 Four analysts A, B, C and D are each a knight (always truthful) or a knave (always lying). A says: "D and I are of the same type." B says: "Exactly two of the four of us are knaves." C says: "B and I are of the same type." D says: "At least one of the other three is a knight." Who are the knights?
**Asked at:** commonly asked (no company-specific report found); knights-and-knaves items appear in an interview-question bank (page not read, unverified).
**What the interviewer is checking:** Systematic case analysis where "same type" statements are used.
**Say this in the interview:** "D must be a knight, because if D were a knave, all three others would be knaves and A's 'same type' statement would be true, which a knave cannot say. Then I test A. The only consistent case is B and D knights, A and C knaves."
**Answer:** **B and D are knights (A and C are knaves).**
**Step-by-step reasoning:**
1. If D were a knave, his statement is false, so A, B, C are all knaves. But then A (a knave) says "D and I are the same type", which is true. A knave cannot say something true. So D is a knight.
2. Suppose A is a knight (so A and D are both knights). Then the knaves are among B and C. B says "exactly two knaves", so B knave means B and C are both knaves, making B's statement true: contradiction. So B is a knight, and then exactly two knaves is needed, but only C can be a knave: contradiction. So A is a knave.
3. A is a knave and D is a knight, so A's statement "D and I are the same type" is false, as a knave must say.
4. Now B. If B were a knave, C's statement "B and I are the same type" would be true if C were a knave (not allowed) and false if C were a knight (not allowed). So B is a knight.
5. B (knight) says exactly two knaves. A is one; C must be the other. Check C: B is a knight, C is a knave, so "B and I are the same" is false, as it must be.
```
A knave   B knight   C knave   D knight
```
Unique: all 16 combinations were enumerated by script.
**Fast method (30 seconds):** Look for the person whose being a knave would force a true statement from someone else. That gives D quickly.
**Check:** Verified by script (16 combinations).
**Explain simply:**
- "Same type" statements are easy to test: two knaves would be telling the truth when they say "same".
- A statement about a count must match the final count if the speaker is a knight.
**Likely follow-ups:** 1) *How many knaves are there?* Two. 2) *If B said "exactly three of us are knaves"?* No consistent assignment exists (checked by script).
**Common mistakes / traps:** Forgetting that a knave must say a completely false statement; stopping after finding one consistent branch without testing the others.

### Q53 ⭐⭐ 🔴 A project team of exactly 4 is chosen from seven people: Arun, Bhavna, Chandra, Deepak, Esha, Farid and Geeta. Rules: (1) If Arun is chosen, Chandra must be chosen. (2) Bhavna and Deepak cannot both be chosen. (3) At least one of Esha and Farid must be chosen. (4) Esha and Geeta cannot both be chosen. (5) Geeta can be chosen only if Arun or Bhavna is chosen. (6) At least one of Chandra and Deepak must be chosen. (7) Chandra and Farid cannot both be chosen. (8) If Esha is chosen, Bhavna must be chosen. Who is on the team?
**Asked at:** commonly asked (no company-specific report found); selection puzzles are a standard constraint-puzzle form (prep-site material, unverified).
**What the interviewer is checking:** Case splitting on the person who appears in the most rules.
**Say this in the interview:** "I split on Farid. If Farid is in, Chandra is out, so Deepak is in, so Bhavna is out, and then I cannot find a fourth member. So Farid is out, Esha is in, and the rest follows: Esha, Bhavna, Chandra and Arun."
**Answer:** **The team is Arun, Bhavna, Chandra and Esha.**
**Step-by-step reasoning:**
1. Case Farid in: rule 7 puts Chandra out; rule 6 puts Deepak in; rule 2 puts Bhavna out; rule 1 puts Arun out (he would need Chandra); rule 5 puts Geeta out (no Arun or Bhavna); rule 8 puts Esha out (she would need Bhavna). Only Farid and Deepak remain, so a team of 4 is impossible.
2. So Farid is out. Rule 3 puts Esha in. Rule 8 puts Bhavna in. Rule 4 puts Geeta out. Rule 2 puts Deepak out. Rule 6 puts Chandra in.
3. That gives Esha, Bhavna, Chandra, and one more place. The remaining people are Arun only (Deepak, Farid, Geeta are out). Arun needs Chandra (rule 1), who is in. So the fourth is Arun.
```
In: Arun, Bhavna, Chandra, Esha     Out: Deepak, Farid, Geeta
```
Unique: all 35 teams of 4 from 7 were enumerated; exactly one passes all 8 rules.
**Fast method (30 seconds):** Split on the person tied to the most "cannot both" rules, and let the chain of forced decisions run.
**Check:** Verified by script (35 teams).
**Explain simply:**
- A case split tries both answers for one person; if one branch fails, the other must hold.
- "If X then Y" rules (1, 8) are chains: chosen people pull others in.
**Likely follow-ups:** 1) *If rule 7 were dropped?* The answer stops being unique: six teams fit (checked by script), including some with Farid. 2) *Which rule did most of the work?* Rule 8.
**Common mistakes / traps:** Stopping after Esha, Bhavna, Chandra without counting to 4; forgetting rule 1 when adding Arun.

### Q54 ⭐⭐ 🔴 A 3-digit lock code uses three different digits (0 to 9; a code may start with 0). Hints from five trial codes: Guess 1 (5 7 1) - 1 digit is correct but in the wrong position. Guess 2 (4 8 3) - 2 digits are correct but in the wrong position. Guess 3 (3 7 8) - 1 digit is correct and in the right position. Guess 4 (0 1 2) - no digit is in the code. Guess 5 (9 0 4) - 1 digit is correct but in the wrong position. What is the code?
**Asked at:** commonly asked (no company-specific report found); code-breaking (Mastermind-style) puzzles fit analytics-firm interviews (prep-site material, unverified).
**What the interviewer is checking:** Eliminating digits and positions systematically.
**Say this in the interview:** "Guess 4 removes 0, 1, 2. Guess 3 means just one of 3, 7, 8 is in the code, so guess 2 forces 4 plus one of 3 or 8. Positions then give 3 4 5."
**Answer:** **The code is 3 4 5.**
**Step-by-step reasoning (reading: "1 digit is correct and in the right position" means exactly one digit of that guess is in the code at all, and it sits in the right place):**
1. Guess 4: 0, 1 and 2 are not in the code.
2. Guess 3: exactly one of 3, 7, 8 is in the code, in its guessed place.
3. Guess 2 needs two of 4, 8, 3; at most one of 3 and 8 can be in the code, so 4 is in the code plus exactly one of 3 or 8.
4. 4 is not in position 1 (guess 2) and not in position 3 (guess 5), so 4 is in position 2.
5. Try 3 in position 1: code 3 4 _. Guess 1 needs exactly one of 5 or 7 (1 is out): 7 is barred by step 2, so 5, which is in the wrong place (guess had 5 first, code has it third). Code 3 4 5. Guess 5: 9 is not in the code, 0 not in code, 4 in the wrong place: correct.
6. Try 8 in position 3: code _ 4 8. Guess 1 needs 5 or 7; 7 is barred, 5 would have to go first, but then it is in the right position in guess 1, which is not allowed. So this fails.
**Check:** Verified by script over all 720 codes (exactly one, 345).
**Fast method (30 seconds):** Use the "no digit is correct" guess to delete digits, then the "right position" guess to anchor.
**Explain simply:**
- "Wrong position" means the digit is in the code but not where guessed.
- Counting how many digits each guess shares with the code narrows the choices quickly.
**Likely follow-ups:** 1) *If guess 3 only said "exactly one digit is correct and in the right position", without saying the other digits are absent?* Then 3 4 7 and 7 4 8 also fit (checked by script), so the stricter reading is needed for a unique answer. 2) *Which digits are ruled out outright?* 0, 1, 2 from guess 4, and 9 is not in the code either.
**Common mistakes / traps:** Reading guess 3 loosely and allowing two matching digits; forgetting that a digit repeated in the wrong place may still be wrong.

### Q55 ⭐⭐ 🔴 Five teams A, B, C, D and E play a round robin (every pair plays once, no draws). The numbers of wins are: A 3, B 3, C 2, D 1, E 1. B beat A, and D beat B. Who won the match between C and E, and who won the match between D and E?
**Asked at:** commonly asked (no company-specific report found); round-robin result puzzles appear in prep-site "games and tournaments" topics (unverified).
**What the interviewer is checking:** Using win counts to fix results one team at a time.
**Say this in the interview:** "10 matches, 10 wins, so the table is consistent. B has 3 wins and lost to D, so B beat everyone else. D's only win is B, so D lost to all the rest. Then E's only win is D. C beat E, and A beat C."
**Answer:** **C won the C-E match, and E won the D-E match.**
**Step-by-step reasoning:**
1. Total matches = 5 x 4 / 2 = 10 and total wins = 3+3+2+1+1 = 10. Consistent.
2. B plays 4 matches, has 3 wins, and lost to D. So B beat A, C and E.
3. D has exactly 1 win and it is over B. So D lost to A, C and E. That gives E a win over D.
4. E has exactly 1 win (over D), so E lost to A, B and C. That gives C a win over E.
5. C has 2 wins: over D and E. So C lost to A and to B. A beat C.
6. A: beat C, D, E (3 wins), lost to B. Matches the table.
```
A beat C, D, E   B beat A, C, E   C beat D, E   D beat B   E beat D
```
Unique: all 1024 result sets were enumerated; only one fits.
**Fast method (30 seconds):** Take the team whose win count equals its number of games minus one (B) or whose count is 1 (D, E), and let the "all their wins are used" logic fix the rest.
**Check:** Verified by script (1024 outcomes, 1 fits the wins and the two given results).
**Explain simply:**
- Each team plays 4 matches, so its wins plus losses equal 4.
- A team whose wins are used up must have lost the rest.
**Likely follow-ups:** 1) *Who beat C?* A and B. 2) *If B had 2 wins instead of 3?* The wins would total 9, not 10, so the table is inconsistent: a quick total check catches it.
**Common mistakes / traps:** Giving D a second win; forgetting that D's one win is already used against B.

### Q56 ⭐ 🟢 Why does a single-elimination (knockout) tournament with n teams always need exactly n - 1 matches, and how do you work out byes when n is not a power of two?
**Asked at:** commonly asked (no company-specific report found); knockout match counting is a classic reasoning item (prep-site material, unverified).
**What the interviewer is checking:** The "count losers" insight instead of adding up rounds.
**Say this in the interview:** "Every match eliminates exactly one team, and everyone except the champion must be eliminated, so n - 1 matches. For byes, I round n up to the next power of two, and the difference is the number of byes."
**Answer:** **n - 1 matches. Byes = (next power of two above or equal to n) - n.**
**Step-by-step reasoning:**
1. Each match produces exactly one loser.
2. Everyone except the champion loses exactly once, so there are n - 1 losers, hence n - 1 matches.
3. Byes: let P be the smallest power of two with P >= n (2, 4, 8, 16, 32...). Then byes = P - n so that exactly P/2 teams remain after round 1.
4. Round 1 matches = n - P/2 (the other teams get byes).
**Worked example (verified by script):** n = 13. Next power of two is 16, so byes = 16 - 13 = 3. Round 1 has 13 - 8 = 5 matches (10 teams play); 5 winners + 3 bye teams = 8 teams remain; matches then 4 + 2 + 1. Total = 5 + 4 + 2 + 1 = 12 = 13 - 1.
**Explain simply:**
- Bye: a team advances without playing in that round.
- A power of two (2, 4, 8, 16...) halves cleanly every round, so no more byes are needed afterwards.
**Likely follow-ups:** 1) *37 teams?* 36 matches. 2) *Does the count change if byes are given in later rounds?* No: it is still n - 1.
**Common mistakes / traps:** Counting byes as matches; using n/2 + n/4 + ... and forgetting to round.

### Q57 ⭐ 🟡 Six people sit around a circular table, each a knight or a knave. Each person says: "The person on my left is a knave." How many knights are at the table?
**Asked at:** commonly asked (no company-specific report found); knight and knave puzzles appear in puzzle banks (unverified).
**What the interviewer is checking:** Whether you turn each statement into a rule linking neighbours and then follow the chain round the circle.
**Say this in the interview:** "Each statement links a person to their left neighbour: if I am a knight, my left neighbour is a knave; if I am a knave, my left neighbour is a knight. So types must alternate. Six is even, so it closes up, and exactly 3 are knights."
**Answer:** **3 knights (and 3 knaves), seated alternately.**
**Step-by-step reasoning:**
1. A knight tells the truth, so a knight's left neighbour is a knave.
2. A knave lies, so the claim "my left neighbour is a knave" is false, which means the knave's left neighbour is a knight.
3. So in both cases the neighbour on the left is the opposite type. Types alternate: K, V, K, V, K, V (V = knave).
4. Going round 6 seats, alternation returns to the start correctly because 6 is even.
5. There are two such arrangements (start with a knight, or start with a knave). Both have 3 knights.
**Fast method (30 seconds):** "Statement = my neighbour is the opposite of me", so the pattern alternates; around a circle alternation needs an even count, then half are knights.
**Check:** Verified by script over all 64 type assignments: exactly 2 are consistent (the two alternating ones), both with 3 knights.
**Explain simply:**
- A knight always tells the truth; a knave always lies (so a knave's sentence is false).
- When a sentence about someone is true for a knight and false for a knave, it gives the same link either way: "opposite type".
**Likely follow-ups:** 1) *Can we tell WHO is a knight?* No, the puzzle gives two arrangements; only the count (3) is fixed. 2) *What if the table has 8 people?* 4 knights, same reasoning.
**Common mistakes / traps:** Assuming the first person must be a knight, or forgetting that a knave's false statement still forces information (the neighbour is a knight).

### Q58 ⭐ 🟡 Five people sit around a circular table, each a knight or a knave. Each says: "The person on my left is a knave." Is this situation possible? If yes, how many knights are there; if no, give the reason.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice that a rule can be impossible to satisfy around a circle (parity).
**Say this in the interview:** "The statements force the types to alternate. Around a circle of 5, alternating cannot close up, because the fifth person would have to be the same type as the first and also the opposite. So it is impossible."
**Answer:** **Not possible; no assignment of knights and knaves fits.**
**Step-by-step reasoning:**
1. As in the six-person case, each statement forces the left neighbour to be the opposite type.
2. Starting from person 1 and moving left: types go T, opposite, T, opposite, T for persons 1 to 5.
3. Person 5's left neighbour is person 1. Person 5 has the same type as person 1 (odd position), but the rule demands person 1 be the OPPOSITE of person 5.
4. That is a contradiction whichever type person 1 has, so the situation cannot exist.
**Fast method (30 seconds):** "Opposite neighbour" around a circle needs an even number of seats. Five is odd, so no.
**Check:** Verified by script over all 32 type assignments: none is consistent.
**Explain simply:**
- This is a parity argument: "parity" means odd or even. Switching between two states each step only returns to the start after an even number of steps.
- When a puzzle has no valid arrangement, that is the answer; it does not mean you made an error (see Q70).
**Likely follow-ups:** 1) *Which odd sizes work?* None; any odd circle fails. 2) *What if one person said "The person on my left is a knight"?* Then that one link is "same type" and the other four are "opposite", and the circle of 5 can close; the script finds exactly 2 consistent type assignments.
**Common mistakes / traps:** Answering "2 knights" or "3 knights" by guessing an alternating pattern and ignoring the seam where the circle closes.

### Q59 ⭐ 🟡 Using the same seven interviews (I1 09:00-10:30, I2 09:30-11:00, I3 10:00-11:30, I4 10:30-12:00, I5 11:00-12:30, I6 11:30-13:00, I7 12:00-13:00) and only ONE room, what is the maximum number of interviews that can be held, given that an interview may start the moment the previous one ends?
**Asked at:** commonly asked (no company-specific report found); this is the classic activity-selection (interval scheduling) idea.
**What the interviewer is checking:** The greedy rule "always pick the one that finishes earliest", and being able to justify it.
**Say this in the interview:** "I sort by finishing time and keep taking the earliest finisher that starts after the last one ends: I1, then I4, then I7. That gives 3, and 4 is impossible because the time window is too short."
**Answer:** **3 interviews: I1 (09:00-10:30), I4 (10:30-12:00), I7 (12:00-13:00).**
**Step-by-step reasoning:**
1. Take the earliest finisher: I1 ends 10:30.
2. Next interview starting at or after 10:30 that finishes earliest: I4 (10:30-12:00).
3. Next starting at or after 12:00 that finishes earliest: I7 (12:00-13:00).
4. Nothing starts after 13:00, so we stop with 3.
5. Why not 4: the day runs 09:00 to 13:00 = 240 minutes. Every interview is 90 minutes except I7 (60). Any four would need at least 90 + 90 + 90 + 60 = 330 minutes, more than 240.
**Fast method (30 seconds):** Earliest-finish-first greedy. It works because finishing earlier always leaves at least as much room for the rest.
**Check:** Brute force over all 128 subsets of the 7 interviews: the maximum non-overlapping set has size 3, and I1, I4, I7 is the only set of that size.
**Explain simply:**
- Two interviews "overlap" if they share any time other than an end point; touching at an end point is allowed here.
- A "greedy" method makes the best-looking choice at each step and never looks back; for this problem it is proven to be optimal.
**Likely follow-ups:** 1) *What if an interview must have a 15-minute gap after it?* Then I1 (ends 10:30) allows next start 10:45, so I5 (11:00-12:30) is next; I1 and I5 only gives 2 (script-checked on this data: maximum 2). 2) *How many rooms are needed to hold all seven?* The most overlapping at once is 3 (from 10:30 to 11:00, I2, I3 and I4 run together; script-checked maximum overlap is 3), so 3 rooms.
**Common mistakes / traps:** Choosing the earliest START first (I1, I3, I5, I7 would clash: I3 starts at 10:00 before I1 ends); or picking by shortest length.

### Q60 ⭐ 🟡 A courier van carries at most 10 kg. Eight parcels weigh 7, 6, 5, 4, 4, 3, 3 and 2 kg and cannot be split. What is the minimum number of van trips needed to carry all of them, and why can it not be done in one fewer?
**Asked at:** commonly asked (no company-specific report found); this is a bin-packing item (unverified as asked by any named company).
**What the interviewer is checking:** The two-part habit: find a lower bound, then build a packing that reaches it.
**Say this in the interview:** "Total weight is 34 kg, and 3 trips carry at most 30, so at least 4 trips. Then I show 4 works: 7+3, 6+4, 5+3+2 and 4."
**Answer:** **4 trips.**
**Step-by-step reasoning:**
1. Total = 7 + 6 + 5 + 4 + 4 + 3 + 3 + 2 = 34 kg.
2. Three trips carry at most 3 x 10 = 30 kg, which is less than 34, so 3 trips are impossible. Hence at least 4.
3. A packing with 4 trips: Trip 1: 7 + 3 = 10. Trip 2: 6 + 4 = 10. Trip 3: 5 + 3 + 2 = 10. Trip 4: 4.
4. So 4 is achievable and 3 is impossible: the minimum is 4.
**Fast method (30 seconds):** Lower bound = total weight / capacity, rounded UP (34 / 10 = 3.4, so 4). Then try pairing big with small to hit the bound.
**Check:** Brute force over every way to assign the 8 parcels to 2, 3 or 4 trips: 0 valid ways with 2 or 3 trips, 1920 valid assignments with 4 trips.
**Explain simply:**
- "Bin packing" means fitting items into as few containers as possible; here each trip is a container.
- A "lower bound" is a number you can prove the answer cannot go below; if you find an arrangement that meets it, you are done.
**Likely follow-ups:** 1) *What if capacity were 12 kg?* 34 / 12 = 2.83, so at least 3; for example 7+5, 6+4+2, 4+3+3 works (12, 12, 10), so 3; the script confirms 2 trips are impossible and 3 trips are possible. 2) *Does the bound always give the answer?* No: sometimes the packing needs one more than the bound, so you must show a packing as well.
**Common mistakes / traps:** Stopping at the bound without building a packing; or loading greedily (7, then 6 alone...) and wrongly claiming 5 trips is needed.

### Q61 ⭐ 🟡 Nine teams must play a single round robin, and each team can play at most one match per round. What is the minimum number of rounds needed, and why can it not be fewer?
**Asked at:** commonly asked (no company-specific report found); scheduling is a games-and-tournaments topic on prep sites (unverified).
**What the interviewer is checking:** Counting total matches, bounding matches per round, then showing a schedule exists.
**Say this in the interview:** "There are 36 matches. With 9 teams, at most 4 matches fit in one round because one team must sit out. 36 divided by 4 is 9, so at least 9 rounds, and a standard rotation schedule achieves 9."
**Answer:** **9 rounds.**
**Step-by-step reasoning:**
1. Total matches = 9 x 8 / 2 = 36.
2. Each match uses 2 teams and each team plays at most once per round, so a round holds at most floor(9 / 2) = 4 matches (8 teams play, 1 rests).
3. Rounds needed is at least 36 / 4 = 9.
4. Achievability: the rotation (circle) method adds a dummy 10th team, fixes one team and rotates the other nine. This gives 9 rounds; the team paired with the dummy sits out that round. Each team sits out exactly once.
**Fast method (30 seconds):** For an odd number n of teams the answer is n rounds (each team rests once); for an even n it is n - 1.
**Check:** Verified by script: the rotation gives 9 rounds of 4 matches, all 36 pairs appear exactly once, and no team plays twice in any round.
**Explain simply:**
- A "round robin" is a format where every pair meets exactly once.
- With an odd number of teams someone always has no opponent in a round (a "bye"), which is why odd n needs n rounds, not n - 1.
**Likely follow-ups:** 1) *And for 8 teams?* 28 matches, 4 per round, so 7 rounds. 2) *And 10 teams?* 45 matches, 5 per round, so 9 rounds.
**Common mistakes / traps:** Saying 8 rounds because "everyone plays 8 opponents"; that ignores that one team must rest in every round when n is odd.

### Q62 ⭐ 🟡 How would a data analyst check a logic puzzle by brute force in Python or SQL (for example with all permutations or a cross join with filters), and why is that a useful way to test whether a puzzle has exactly one solution?
**Asked at:** commonly asked (no company-specific report found); brute-force checking is our suggestion for analysts, not a reported test format.
**What the interviewer is checking:** Whether you can turn clues into filters and use counting to prove uniqueness, which links puzzles to analyst skills.
**Say this in the interview:** "I list every possible arrangement, apply each clue as a filter, and count what survives. If exactly one row survives, the solution exists and is unique; zero means the clues contradict; more than one means the puzzle is ambiguous."
**Answer:** **Generate all candidates, filter by every clue, count survivors: 1 = unique, 0 = contradictory, 2 or more = ambiguous.**
**Explain simply:**
- Candidates: a "permutation" is one ordering of items. For 4 people and 4 roles there are 4 x 3 x 2 x 1 = 24 permutations; for a 3-digit code with different digits there are 10 x 9 x 8 = 720.
- Filters: each clue becomes a True/False test on a candidate. In Python, `itertools.permutations` makes the candidates and `all(...)` applies the clues. In SQL, a CROSS JOIN of small tables makes the candidates and the clues go in a WHERE clause.
- Why it proves uniqueness: you checked every possibility, so nothing was missed, unlike a hand deduction that may have skipped a branch.
**Worked mini-example:** Q67 (the safe code): 720 candidate codes; after filtering by the five hints, exactly 1 remains (738). Q68 (DATA + DATA = SMART): 10 x 9 x 8 x 7 x 6 x 5 = 151,200 letter-to-digit assignments for six letters; exactly one satisfies the sum (6989 + 6989 = 13978). Both were run by script.
**Likely follow-ups:** 1) *What if there are too many candidates?* Prune early: reject partial arrangements the moment a clue fails (called backtracking). 2) *Can the check be wrong?* Yes, if a clue is coded wrongly; so test the code on a known valid answer and read each filter against the sentence.
**Common mistakes / traps:** Coding a clue loosely (for example "not next to" versus "not the same"), and treating "found one solution" as "the only solution".

### Q63 ⭐ 🟡 After solving a puzzle you get one answer. How do you quickly test that your answer satisfies every clue, and how can you be sure there is no second solution?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Verification discipline: separate "my answer fits" from "my answer is the only one".
**Say this in the interview:** "First I re-read every clue against the finished arrangement, one tick per clue. Then for uniqueness I look at where I made a forced move versus a guess, and for each guess I check the other choice leads to a contradiction."
**Answer:** **Two separate checks: (1) test the answer against every clue; (2) show every alternative branch fails (or enumerate all possibilities).**
**Explain simply:**
- Check 1, fit: write the final table, then go clue by clue and mark each one satisfied. Use the original wording, not your paraphrase, because misreading a clue is the commonest error.
- Check 2, uniqueness: in your working, every time you chose between two options, go back and follow the other option until it breaks a clue. If all alternatives break, the answer is unique. If one survives, there are two solutions.
- Counting method: if the puzzle is small, list all candidates (for example 24 orderings of 4 items) and cross out those that break a clue; one left means unique.
**Worked mini-example:** Q67: the answer 738 fits the five hints (guess 1 has none of 4, 2, 9; guess 2 has 3 in the wrong place; guess 3 has 8 in the wrong place; guess 4 has 8 in the wrong place; guess 5 has 3 in the right place). For uniqueness, the script tried all 720 codes and only 738 survives.
**Likely follow-ups:** 1) *What if you find two solutions?* The puzzle is ambiguous (or you misread a clue); say so and give both. 2) *What if exam time is short?* Check the answer against the clues you used least, since errors hide there (our suggestion).
**Common mistakes / traps:** Checking only the clues you used to build the answer; and claiming uniqueness because "the other option looked unlikely".

### Q64 ⭐ 🟡 How do knights-and-knaves puzzles change if some people are "normal" (may say true or false statements), and which of the previous deductions stop being valid?
**Asked at:** commonly asked (no company-specific report found); the knight, knave and normal-type extension is from Smullyan-style puzzles.
**What the interviewer is checking:** Whether you understand that a statement only forces a deduction when the speaker's truthfulness is known.
**Say this in the interview:** "A normal person can say anything, so their statement tells me nothing about their type. Any deduction of the form 'he said X, so X is true or false' no longer works for them, and many puzzles that had one answer now have several."
**Answer:** **Statements by a "normal" person carry no forced truth value, so deductions that relied on every speaker being a knight or knave break; unique answers often become several possible answers.**
**Explain simply:**
- Knight = always true; knave = always false; normal = sometimes true, sometimes false, unpredictable.
- Still valid: if a statement is made by a known knight, it is true; by a known knave, it is false. Contradiction hunting (assume a type, test it) still rules out types that cannot say that sentence.
- No longer valid: "A is not a knight, so A is a knave" (A might be normal); "this person lied, so the other is a knight"; and counting arguments such as alternation in Q57 (a normal can break the chain).
**Worked mini-example:** Q2 (A: "B is a knave"; B: "A and I are of the same type"). With only knights and knaves the one solution is A knight, B knave. Allowing normals, the script finds 4 consistent cases: (A knight, B knave), (A knave, B normal), (A normal, B knave), (A normal, B normal). The puzzle now needs extra information to pin it down.
**Likely follow-ups:** 1) *How do puzzle-setters restore uniqueness?* They add clues like "exactly one of each type" or a statement that only one type can truthfully make. 2) *Does "normal" ever speak a sentence only a normal could?* Yes: a sentence that a knight cannot say (it would be false) and a knave cannot say (it would be true) such as "I am a knave" reveals a normal.
**Common mistakes / traps:** Carrying over "not a knight means knave"; and forgetting that the puzzle's first line decides which types exist.

### Q65 ⭐ 🔴 Four auditors A, B, C and D are each a knight (always truthful) or a knave (always lying). A says: "B and D are of different types." B says: "Both C and D are knaves." C says: "B and D are of the same type." D says: "At least one of B and C is a knave." Who are the knights?
**Asked at:** commonly asked (no company-specific report found); a knights-and-knaves item is listed in one interview-question bank (unverified, page not read).
**What the interviewer is checking:** Systematic case work: assume a type for one person and propagate, abandoning branches that contradict.
**Say this in the interview:** "I test D first. If D is a knave, 'at least one of B and C is a knave' is false, so B and C are both knights, but a knight B says C is a knave, a clash. So D is a knight. Then B cannot be a knight, because B's claim would make D a knave. With B a knave, A's statement is true and C's is false. Knights: A and D."
**Answer:** **A and D are knights; B and C are knaves.**
**Step-by-step reasoning:**
1. Suppose D is a knave. Then D's statement is false, so B and C are both knights. But B (a knight) says C is a knave, while we just said C is a knight. Contradiction. So D is a knight.
2. D is a knight, so "at least one of B and C is a knave" is true.
3. Suppose B is a knight. Then B's claim "C and D are both knaves" is true, so D is a knave, contradicting step 1. So B is a knave.
4. B is a knave, so B's claim is false: it is not true that both C and D are knaves. D is a knight, so that is already false, which gives no more information about C.
5. A says "B and D are of different types". B is a knave and D is a knight, so this is true; hence A is a knight.
6. C says "B and D are of the same type". They differ, so C's claim is false, so C is a knave.
Final table: A knight, B knave, C knave, D knight.
**Fast method (30 seconds):** Start with D (his false statement would settle two people at once), then use each knave's statement as a negation.
**Check:** Brute force over all 16 type assignments: exactly one is consistent (A and D knights, B and C knaves). Re-reading all four statements against the table also fits.
**Explain simply:**
- Rule: knight's statement is true; knave's statement is false. A knave saying "both are knaves" means "NOT both are knaves", which only needs one of them to be a knight.
- Negating "at least one is a knave" gives "both are knights"; this step trips people up.
**Likely follow-ups:** 1) *What if B had said only "C is a knave"?* Script check: then no assignment is consistent, so the answer is very sensitive to the exact wording. 2) *Why is C's statement false?* Because B and D differ in type.
**Common mistakes / traps:** Negating "both are knaves" as "both are knights" (the true negation is "not both are knaves", meaning at least one is a knight).

### Q66 ⭐ 🔴 Five hats are in a box: three red and two blue. Three people A, B and C each pick one hat without looking and wear it, so that each can see the other two hats but not their own. The two unused hats are hidden. They are asked in order, and every person reasons perfectly and is honest: A says "I do not know my hat colour." Then B says "I do not know my hat colour." Then C says "I know my hat colour." What colour is C's hat?
**Asked at:** commonly asked (no company-specific report found); hat-logic puzzles are a common interview type (unverified for any named company).
**What the interviewer is checking:** Reasoning from what others' answers reveal, not only from what you see.
**Say this in the interview:** "A not knowing means B and C are not both blue, because with two blue hats worn only red is left for A. B then reasons: if C were blue, then B would be sure of red, because B being blue would have let A know. B did not know, so C is not blue. C's hat is red."
**Answer:** **C's hat is red.**
**Step-by-step reasoning:**
1. There are only 2 blue hats. If A saw two blue hats on B and C, A would know their own is red. A did not know, so B and C are NOT both blue.
2. B hears this. If B saw C in blue, then since B and C are not both blue, B's own hat must be red, and B would know. B said "I do not know", so B did NOT see a blue hat on C.
3. So C's hat is red.
4. This holds for every possible case: after A and B both say they do not know, the surviving cases are (A, B, C) = (blue, blue, red), (blue, red, red), (red, blue, red), (red, red, red). C is red in all four.
5. That explains why C can say "I know": whatever A and B wear, C is red.
**Fast method (30 seconds):** Each "I do not know" removes cases. Only two blue hats exist, so "A does not know" means not (B and C both blue); "B does not know" then kills "C blue".
**Check:** Verified by script: listing all 7 possible colour triples, removing those where A would know, then those where B would know, leaves only triples where C is red (4 triples).
**Explain simply:**
- Perfect reasoners use other people's statements as information; silence or "I don't know" tells you which cases are still possible.
- Hats not worn do not matter except that the supply is limited to 3 red and 2 blue.
**Likely follow-ups:** 1) *What would A's "I know" tell us?* That B and C are both blue (A sees two blue hats, so A's own must be red). 2) *Why is the answer independent of A's and B's colours?* The two "don't know" statements already make C red in every surviving case.
**Common mistakes / traps:** Reasoning only from what you can see, or assuming equal chances (this is not a probability question).

### Q67 ⭐ 🔴 A safe uses a 3-digit code with three different digits (0 to 9; a code may start with 0). Hints from five trial codes: Guess 1 (4 2 9) - no digit is in the code. Guess 2 (1 0 3) - 1 digit is correct but in the wrong position. Guess 3 (8 5 6) - 1 digit is correct but in the wrong position. Guess 4 (2 8 0) - 1 digit is correct but in the wrong position. Guess 5 (2 3 9) - 1 digit is correct and in the right position. What is the code?
**Asked at:** commonly asked (no company-specific report found); Mastermind-style code puzzles are a common puzzle type (unverified for any named company).
**What the interviewer is checking:** Eliminating digits first, then using the "right position" clue to fix a slot.
**Say this in the interview:** "Guess 1 removes 4, 2 and 9. Guess 5 then has only 3 left, so 3 is in the code, in the middle. That makes 3 the correct digit in Guess 2, so 1 and 0 are out. Guess 4 leaves 8, and Guess 3 shows 8 is not first, so it is last. The remaining digit is 7. The code is 738."
**Answer:** **738**
**Step-by-step reasoning:**
1. Guess 1 (4 2 9): none of these digits is in the code. Remove 4, 2, 9.
2. Guess 5 (2 3 9): exactly 1 digit is right and in the right place. 2 and 9 are out, so 3 is in the code and sits in position 2.
3. Guess 2 (1 0 3): exactly 1 digit is correct but misplaced. 3 is in the code (guessed in position 3, true position 2, so it is the misplaced one). Hence 1 and 0 are NOT in the code.
4. Guess 4 (2 8 0): 2 and 0 are out, so the one correct digit is 8, and it is not in position 2 (that slot holds 3).
5. Guess 3 (8 5 6): exactly 1 correct digit, misplaced. 8 is in the code, so it is that digit: 5 and 6 are out, and 8 is not in position 1. Position 2 is taken by 3, so 8 is in position 3.
6. The code is _ 3 8. Digits excluded so far: 0, 1, 2, 4, 5, 6, 9 (plus 3 and 8 used), leaving 7 for the first slot.
Final: 7 3 8.
**Fast method (30 seconds):** Use the "none correct" guess to delete digits, find the guess with a right-position digit, then work out which digit in each other guess is the correct one.
**Check:** Brute force over all 720 codes with three different digits: exactly 1 satisfies all five hints, 738. Re-reading each hint against 738 also works.
**Explain simply:**
- "Correct but in the wrong position" means the digit is in the code, just not at that spot.
- "Correct and in the right position" fixes a digit and its slot at the same time, so start with it.
**Likely follow-ups:** 1) *What if Guess 5 said "wrong position" instead?* Re-solve by script, as the answer may no longer be unique. 2) *How many codes are possible before any hint?* 10 x 9 x 8 = 720.
**Common mistakes / traps:** Treating "wrong position" as "digit not in the code", or forgetting a code can contain only the digits of the guess marked correct.

### Q68 ⭐ 🔴 In the addition DATA + DATA = SMART each letter stands for a different digit (0 to 9), the same letter always stands for the same digit, and no number starts with 0. What is the value of SMART?
**Asked at:** commonly asked (no company-specific report found); cryptarithms (letter-digit puzzles) are a classic puzzle type (unverified for any named company).
**What the interviewer is checking:** Column-by-column reasoning with carries, and a clean uniqueness argument.
**Say this in the interview:** "DATA doubled has 5 digits, so S is 1. I work column by column from the right with carries, and the only assignment that fits is DATA = 6989, so SMART = 13978."
**Answer:** **SMART = 13978** (D = 6, A = 9, T = 8, S = 1, M = 3, R = 7).
**Step-by-step reasoning:**
1. DATA + DATA has at most 5 digits, and the leading digit of the 5-digit result can only be 1 (doubling carries at most 1). So S = 1.
2. Columns from the right with carries c1, c2, c3: units A + A = T + 10 c1; tens T + T + c1 = R + 10 c2; hundreds A + A + c2 = A + 10 c3; thousands D + D + c3 = M + 10 (carry 1 into S).
3. Hundreds column simplifies to A + c2 = 10 c3. Since c3 is 0 or 1 and A is a digit, c3 = 1 and c2 = 1 gives A = 9 (c2 = 0 would need A = 10).
4. Units: 9 + 9 = 18, so T = 8 and c1 = 1. Tens: 8 + 8 + 1 = 17, so R = 7 and c2 = 1 (consistent with step 3).
5. Thousands: 2D + 1 = M + 10, so M = 2D - 9, which needs D at least 5. D = 5 gives M = 1, clashing with S. D = 6 gives M = 3, fine. D = 7 gives M = 5 but D = 7 equals R. D = 8 is T and D = 9 is A.
6. So D = 6, M = 3: 6989 + 6989 = 13978, and the letters D 6, A 9, T 8, S 1, M 3, R 7 are all different.
**Fast method (30 seconds):** Leading carry gives S = 1; the column "2A + carry ends in A" pins A = 9; the rest follows with carries.
**Check:** Brute force over all 151,200 assignments of different digits to the six letters (no leading zero): exactly one works, 6989 + 6989 = 13978. Arithmetic check: 2 x 6989 = 13978.
**Explain simply:**
- A "cryptarithm" is arithmetic where letters replace digits; the "carry" is the extra 1 passed to the next column left when a column total reaches 10 or more.
- Doubling a number can never carry more than 1 into the next column, which is why S must be 1.
**Likely follow-ups:** 1) *Can any letter be 0?* Not in this solution; the digit 0 is simply unused. 2) *What about SEND + MORE = MONEY?* A famous cousin with the unique answer 9567 + 1085 = 10652 (from memory, not verified here).
**Common mistakes / traps:** Forgetting carries between columns, or allowing two letters to share a digit (D = 7 and R = 7 is rejected for that reason).

### Q69 ⭐ 🔴 Four teams play a single round robin (each pair once; win 3 points, draw 1, loss 0). The top two teams qualify. If teams level on points are separated by a tie-break that could go against you, what is the minimum number of points that guarantees a team a top-two finish?
**Asked at:** commonly asked (no company-specific report found); a points-table question of this kind is a games-and-tournaments topic on prep sites (unverified).
**What the interviewer is checking:** Worst-case thinking: find the largest total points that cannot guarantee a place, and add one.
**Say this in the interview:** "Six matches, at most 18 points in total. If three teams all had 7 or more, that would be 21 points, more than exist, so at most one other team can reach 7 and you are top two. With 6 points it can fail: three teams can all finish on 6. So the answer is 7."
**Answer:** **7 points.**
**Step-by-step reasoning:**
1. There are 4 x 3 / 2 = 6 matches, each giving at most 3 points, so at most 18 points are shared.
2. A team misses the top two only if at least two other teams have as many or more points (ties are assumed to go against it).
3. With 7 points: two other teams with 7 or more would mean 21 points in total, more than the 18 available. So at most one other team can match or beat 7, and the team finishes in the top two. 7 is enough.
4. With 6 points it can fail: A beats B, B beats C, C beats A, and each of A, B, C beats D. Then A, B and C all have 6 points and D has 0. Ties are against you, so one of the three is third.
5. 6 or fewer can fail, so 7 is the minimum guarantee.
**Fast method (30 seconds):** Use the total-points cap: 3 other teams at the same total as you cannot share more than 18, so find the smallest P with 3P > 18, that is P = 7.
**Check:** Verified by script over all 3^6 = 729 possible sets of results: a team on 7, 8 or 9 points is never outside the top two when ties go against it, but a team on 6 points (and every lower total, 1 to 5) can be.
**Explain simply:**
- "Guarantee" means it works in every possible set of results, so we look at the worst case.
- The total points in the group is capped by the number of matches times 3 (a draw gives only 2 in total, so fewer points).
**Likely follow-ups:** 1) *What if ties were broken in your favour (you miss only if two teams are strictly above you)?* The script gives 5 points. 2) *What is the most points a team can have and still not qualify?* 6 points (as in step 4).
**Common mistakes / traps:** Saying 6 because "two wins out of three should be enough"; and forgetting that three-way ties on 6 are possible.

### Q70 ⭐ 🔴 How can you recognise quickly that a set of puzzle clues is contradictory (no solution), and what does that tell you about your own working versus the puzzle?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can tell "I made a mistake" from "the puzzle has no solution", and test which it is.
**Say this in the interview:** "If a cell ends up with no possible value, or two clues demand opposite things, I stop and re-read my deductions. If a fresh restart from the original clues reaches the same contradiction, or a brute-force search returns zero rows, the puzzle itself is inconsistent."
**Answer:** **Signs: an empty cell, two clues needing opposite things, or a forced chain that returns to break itself. A contradiction in your working is usually your own error first; only if it survives a clean restart and a full check do you conclude the puzzle has no solution.**
**Explain simply:**
- Typical red flags: a person left with no possible role; two people forced into the same unique slot; a total that cannot add up (for example needing 21 points when only 18 exist, as in Q69); or an odd-sized circle needing alternation (Q58).
- Branch contradictions are normal: in "assume X, then derive an impossibility" working, a contradiction in a trial branch just means that branch is wrong (this is how Q65 is solved). A contradiction in ALL branches is what signals a puzzle with no solution.
- A contradiction can come from a misread clue, a wrong negation, or a wrong earlier deduction; the puzzle is flawed only after those are ruled out.
**Worked mini-example:** Q58 (5 people, "left neighbour is a knave"). Chain: alternation is forced, the circle of 5 cannot close, and a script check of all 32 type assignments finds none. The puzzle is impossible, and the answer "not possible, because of odd parity" is correct, not a failure of working.
**Likely follow-ups:** 1) *What do you say in an interview if you find no solution?* Show the contradiction explicitly, state the assumption you tested, and say which clue to change to make it solvable. 2) *How would you test it by script?* Enumerate all candidates; zero survivors confirms the contradiction.
**Common mistakes / traps:** Forcing an answer to satisfy "most" clues, or deciding the puzzle is broken before re-reading the clues; also, calling a puzzle contradictory when it merely has several solutions.
