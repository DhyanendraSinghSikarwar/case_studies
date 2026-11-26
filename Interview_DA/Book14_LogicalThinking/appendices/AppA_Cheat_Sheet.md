# Appendix A: Formula and Rule Cheat Sheet

One compact section per topic, in the order of the book. Every formula, truth table and rule below was checked by a short computer program (all possible truth values, brute-force counting, or a calendar and clock simulation). Where a convention is needed, it is stated, because many puzzles are decided by the convention. Chapter numbers show where to learn the idea.

Symbols: T true, F false, p q r statements, NOT, AND, OR written in capitals.

---

## Part 1: Foundations of Logic

### A1. Arguments (Ch 1)

| Item | Rule |
|---|---|
| Premise | A reason offered |
| Conclusion | The claim the premises support |
| Conclusion clue words | therefore, so, hence, thus, it follows that |
| Premise clue words | because, since, given that, for |
| Deduction | If the premises are true, the conclusion cannot be false |
| Induction | The premises make the conclusion likely, not certain |

### A2. Statements and truth values (Ch 2)

| Sentence type | Statement? |
|---|---|
| Fact claim, true or false or not yet known | Yes (it has a truth value, even if we cannot check it today) |
| Question, command, exclamation, greeting | No |
| Opinion or taste ("best", "nicest") | No |
| Open sentence with a blank ("x + 4 = 10") | No, until the blank is filled |
| "This sentence is false" | No (no consistent value) |

### A3. AND, OR, NOT (Ch 3)

| p | q | NOT p | p AND q | p OR q |
|---|---|---|---|---|
| T | T | F | T | T |
| T | F | F | F | T |
| F | T | T | F | T |
| F | F | T | F | F |

- OR is inclusive: true when at least one is true, including both.
- Rows needed: 1 variable 2, 2 variables 4, 3 variables 8, 4 variables 16 (2 to the power n).
- Standard row order: start with all T and change the last column first.
- De Morgan: NOT (p AND q) = (NOT p) OR (NOT q). NOT (p OR q) = (NOT p) AND (NOT q).
- Distribution: p AND (q OR r) = (p AND q) OR (p AND r).
- Two statements are equivalent if their result columns match in every row.

### A4. If-then and its relatives (Ch 4)

| p | q | If p then q | Converse (if q then p) | Inverse (if NOT p then NOT q) | Contrapositive (if NOT q then NOT p) | p iff q |
|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T |
| T | F | F | T | T | F | F |
| F | T | T | F | F | T | F |
| F | F | T | T | T | T | T |

- The only way "if p then q" is false: p true and q false. So NOT (if p then q) = p AND (NOT q).
- Original and contrapositive always agree. Converse and inverse always agree with each other, but not with the original.
- p iff q means (if p then q) AND (if q then p); true exactly when p and q have the same value.
- Wording translations: "p if q" means if q then p. "p only if q" means if p then q. "p unless q" means if NOT q then p (same as p OR q). "p provided that q" means if q then p. "All A are B" means if it is an A it is a B.

### A5. Quantifiers and their negations (Ch 5)

"Some" means at least one (it can be all). One counterexample breaks an "all" claim.

| Original | Negation |
|---|---|
| All A are B | Some A are not B |
| No A is B | Some A is B |
| Some A are B | No A is B |
| Some A are not B | All A are B |
| X AND Y (inside the claim) | NOT X OR NOT Y |
| X OR Y (inside the claim) | NOT X AND NOT Y |
| If X then Y (inside the claim) | X AND NOT Y |

A real negation can never leave both sentences false. "No employee is present" is the opposite of "All are present", not its negation.

### A6. Valid, invalid, sound (Ch 6)

- Valid: if all premises are true, the conclusion must be true. Validity is about the shape, not the facts.
- Invalid: the premises can be true and the conclusion false (find a counterexample).
- Sound: valid AND all premises actually true. Only this guarantees a true conclusion.

| Shape | Verdict |
|---|---|
| If P then Q; P; so Q (modus ponens) | Valid |
| If P then Q; NOT Q; so NOT P (modus tollens) | Valid |
| If P then Q; Q; so P (affirm the result) | Invalid |
| If P then Q; NOT P; so NOT Q (deny the condition) | Invalid |
| If P then Q; if Q then R; so if P then R (chain) | Valid |
| P or Q; NOT P; so Q | Valid |
| P or Q; P; so NOT Q | Invalid (OR allows both) |
| All A are B; x is A; so x is B | Valid |
| All A are B; x is B; so x is A | Invalid |

---

## Part 2: Sets and Classification

### A7. Sets and Venn counting (Ch 7)

Two sets: 4 regions (only A, both, only B, neither). Three sets: 8 regions (3 "only", 3 "exactly two", 1 "all three", 1 "none").

| Quantity | Formula |
|---|---|
| At least one (two sets) | A + B - both |
| Only A | A - both |
| Neither | Total - (A + B - both) |
| At least one (three sets) | A + B + C - (A and B) - (A and C) - (B and C) + (all three) |
| Only A (three sets) | A - (A and B) - (A and C) + (all three) |
| A and B only | (A and B) - (all three) |
| Exactly two | (sum of the three pair totals) - 3 x (all three) |
| Sum check | A + B + C = (exactly one) + 2 x (exactly two) + 3 x (all three) |
| None | Total - at least one |

A circle total includes its overlaps. The "+ all three" is there because people in the centre are added 3 times and removed 3 times. Blank templates are in Appendix B.

### A8. Classification, odd one out, analogies (Ch 8)

- Good groups: no overlap (each item fits one group) and nothing left out.
- Odd one out: find a feature that four items share and one lacks; say the rule in a sentence.
- Analogy A : B :: C : D. Make a sentence for A and B, reuse it for C and the options.
- Keep the order. Doctor : patient is not patient : doctor.
- If two options fit, make the sentence more specific.

---

## Part 3: Patterns and Information

### A9. Series pattern checklist (Ch 9)

Try in this order and stop at the first rule that fits every term:

| Step | Ask | Example |
|---|---|---|
| 1 | Same gap each time? | 7, 12, 17, 22 (add 5) |
| 2 | Same multiplier each time? | 3, 6, 12, 24 (times 2) |
| 3 | Does the gap itself grow in a pattern? | 1, 2, 4, 7, 11 (gaps 1, 2, 3, 4) |
| 4 | Two lists mixed (odd and even places)? | 2, 50, 4, 45, 6, 40 |
| 5 | A known family? | squares 1, 4, 9; cubes 1, 8, 27; triangular 1, 3, 6, 10; primes 2, 3, 5, 7, 11 |
| 6 | Two operations taking turns? | 3, 6, 4, 8, 6, 12 |
| 7 | Built from earlier terms? | 2, 3, 5, 8, 13 |

- Letters: A = 1 to Z = 26. After Z comes A (position 27 is A, position 0 is Z).
- Repeating cycle of length L: the term at position n depends on the remainder of n divided by L.
- A short list never proves a rule; the simplest rule that fits all terms is the intended one.

### A10. Tables, flowcharts and decision trees (Ch 10 and 11)

- Row total adds across; column total adds down; the grand total must agree both ways.
- Grid puzzle rules: one tick per row and column within each pair of categories; after a tick, cross the rest of its row and column; a negative clue is a cross; if a row has one open cell, tick it.
- Flowchart: follow the arrows; a diamond is a yes/no test; test each path with a tiny example.

### A11. Syllogism rules (Ch 12)

Conventions: believe the statements; "some" means at least one; every named group has at least one member; "follows" means true in every legal drawing.

| Statement | Drawing | Can you swap X and Y? |
|---|---|---|
| All X are Y | X inside Y | No |
| No X are Y | Circles apart | Yes |
| Some X are Y | Circles overlap | Yes |
| Some X are not Y | A mark in X, outside Y | No |

Wordings: "Only X are Y" means All Y are X. "None but X are Y" means All Y are X. "Not all X are Y" means Some X are not Y. "X is never Y" means No X are Y.

Two statements (X and Z are the outer groups):

| Statement 1 | Statement 2 | Certain about X and Z |
|---|---|---|
| All X are Y | All Y are Z | All X are Z; Some X are Z; Some Z are X |
| Some X are Y | All Y are Z | Some X are Z; Some Z are X |
| All X are Y | No Y are Z | No X are Z; Some X are not Z |
| Some X are Y | No Y are Z | Some X are not Z |
| No X are Y | All Z are Y | No X are Z; Some X are not Z |
| All X are Y | Some Y are Z | Nothing |
| Some X are Y | Some Y are Z | Nothing |
| No X are Y | No Y are Z | Nothing |
| All X are Y | All Z are Y | Nothing |
| Some X are not Y | All Y are Z | Nothing |

In every row, "Some" and "No" statements can be swapped (Some X are Z = Some Z are X). Verdicts: Follows (true in every legal picture), Possible (true in some), False (false in all). Either-or: choose "either I or II" only when neither follows alone and the two are a claim and its negation. Always try to break the conclusion with another legal drawing.

---

## Part 4: Position, Relations and Puzzles

### A12. Direction and distance conventions (Ch 13)

- Map: North up, East right, South down, West left.
- Clockwise order: N, NE, E, SE, S, SW, W, NW. Each step is 45 degrees; a quarter turn is 90; a half turn is 180.
- Right turn is a quarter turn clockwise; left turn is a quarter turn anticlockwise.

| You face | Turn left | Turn right | Behind |
|---|---|---|---|
| North | West | East | South |
| East | North | South | West |
| South | East | West | North |
| West | South | North | East |

- Coordinates (across, up): East plus across, West minus across, North plus up, South minus up. Start at (0, 0).
- Distance travelled = sum of all legs. Distance from the start = straight line = square root of (across squared + up squared).
- Triples: 3-4-5, 6-8-10, 5-12-13, 8-15-17, 20-21-29, and multiples of these.
- Direction of the end point from the start: signs of (across, up): (+,+) NE, (-,+) NW, (+,-) SE, (-,-) SW; a zero means due N, S, E or W.

### A13. Blood relations: symbols and conventions (Ch 14)

- Four basic links: parent, child, sibling, spouse. Longer words are paths through the tree.
- Gender comes only from gender words: father, mother, son, daughter, brother, sister, husband, wife, uncle, aunt, nephew, niece. The words parent, child, sibling, spouse, cousin do not say gender; write "?".
- Assumptions: siblings are full siblings; one marriage per person; nobody marries a blood relative; the family described is the whole story.
- Tree drawing: line up for parent, sideways for sibling, "=====" for married, down for child; M, F, or ? beside each name.
- Paternal means father's side; maternal means mother's side.
- Uncle/aunt: parent's sibling (or that sibling's spouse). Cousin: child of a parent's sibling. In-law: spouse's relative, or relative's spouse.
- "Only" fixes one person ("my father's only brother").
- Read a chain one link at a time from "my". Check by reading it backwards. Symbol questions (such as "P & Q means P is the mother of Q"): translate each symbol into a link and draw.

### A14. Ranking formulas (Ch 15)

| Quantity | Formula |
|---|---|
| Rank from top + rank from bottom | Total + 1 |
| People above you | Rank from top - 1 |
| People below you | Rank from bottom - 1 |
| Total | People above + 1 + people below |
| Between two ranks a < b (same end) | b - a - 1 |
| Counting a to b including both ends | b - a + 1 |

- Chains: A > B and B > C give A > C. A > B and A > C say nothing about B versus C.
- Ties: standard competition ranking skips numbers (90, 80, 80, 70 gives 1, 2, 2, 4); dense ranking does not (1, 2, 2, 3). The question says which.
- Row positions: from left + from right = total + 1.

### A15. Seating conventions (used in Appendix B)

- These are the conventions of Chapter 16 (and Chapters 17, 18 and 36 follow them). Left and right always belong to the person sitting there.
- Straight row: everyone faces north (the top of the page), so right is east, the right side of the drawing. Seat 1 is the west end (left end).
- Circle or rectangular table, facing the centre: your left neighbour is the next seat clockwise; your right is the next seat anticlockwise.
- Circle, facing outside: reversed (left is anticlockwise, right is clockwise).
- Two rows facing each other: the top (north) row faces south, so its right is west (the left side of the drawing); the bottom (south) row faces north, so its right is east. Seats are numbered from the west, and "opposite" means the same seat number in the other row.
- Opposite seat in a circle of n seats (n even): k + n/2.
- Distinct circular arrangements of n people: (n - 1) factorial. Always say whether the question counts rotations as different.
- "Neighbour" means directly adjacent; "second to the left" skips one person.

### A16. Coding-decoding checklist (Ch 17)

1. Write the plain and coded words one under the other.
2. Convert both to positions (A = 1 to Z = 26).
3. Subtract coded minus plain for every letter: all equal means constant shift; climbing by 1 means progressive; taking turns means alternating.
4. If random, test reversal, position values, rearranging, substitution table.
5. Test the rule on every example. Mirror letters add to 27 (A and Z, M and N). Alphabet wraps after Z.
6. Word codes: find the word shared by two sentences, then eliminate.

### A17. Puzzle-solving order (Ch 18)

1. List the things and the places. 2. Read all clues; underline order words. 3. Draw a grid or strip. 4. Place exact facts first, then linked pairs. 5. Eliminate; write a value when only one choice remains. 6. If stuck, try cases and look for a contradiction. 7. Check every clue against the final answer.

| Wording (floors 1 to 5) | Meaning |
|---|---|
| A directly above B | A = B + 1 |
| A above B | A higher by any amount |
| Adjacent | Differ by exactly 1 |
| Not adjacent | Do not differ by exactly 1 |
| Exactly two floors above | A = B + 2 |

Critical path = longest chain of waiting tasks; the finish time cannot be shorter. Total work divided by helpers (rounded up) is another lower limit.

### A18. Clock angles and calendar rules (Ch 20)

Clock (12-hour dial):

| Fact | Value |
|---|---|
| Degrees per hour mark | 30 |
| Minute hand speed | 6 degrees per minute |
| Hour hand speed | 0.5 degrees per minute |
| Minute hand gains | 5.5 degrees per minute |
| Angle at H hours M minutes | absolute value of (30 H - 5.5 M); if above 180, subtract from 360 |
| Hands overlap at | M = 60 H / 11 minutes past H |
| In 12 hours: overlaps / opposite / right angles | 11 / 11 / 22 |

Fast and slow clocks: compare "minutes shown" to "true minutes" and scale.

Calendar:

- Odd days = remainder when days are divided by 7. Weekday after N days moves forward by N mod 7.
- Ordinary year: 365 days = 52 weeks + 1 odd day. Leap year: 366 days = 2 odd days.
- Leap year: divisible by 4, except century years, which must be divisible by 400 (2000 and 2028 yes; 1900 and 2100 no).
- Month odd days: 31-day month 3; 30-day month 2; February 28 days 0; February 29 days 1.
- Extra (not taught in Chapter 20, checked by code): 100 years have 5 odd days; 200 have 3; 300 have 1; 400 have 0 (counted from a century year start, such as 1601 to 1701).
- The same date next year moves 1 weekday, or 2 if a 29 February lies in between.
- Months with 31 days: Jan, Mar, May, Jul, Aug, Oct, Dec. Financial year: check the convention (India commonly 1 April to 31 March).

---

## Part 5: Reasoning for Real Decisions

### A19. Statement-assumption, conclusion, course of action (Ch 21)

| Type | Test |
|---|---|
| Assumption | Negation test: flip it; if the statement becomes pointless, it is an implicit assumption. Not assumptions: new facts, extreme words (always, never, only, everyone), hoped-for results. |
| Conclusion | Must be true in every situation where the statement is true. Beware reversal, causation, and numbers ("most" means more than half). |
| Course of action | Relevant, practicable, proportionate, no new harm. Judge only from the statement. |

### A20. Data sufficiency verdict table (Ch 22)

Sufficient means exactly one answer (for yes/no questions: always yes or always no; a firm "no" is sufficient). Test I alone, then II alone (do not carry over), and together only if both fail.

| I alone | II alone | Together | Choice |
|---|---|---|---|
| sufficient | not | not needed | A |
| not | sufficient | not needed | B |
| not | not | sufficient | C |
| sufficient | sufficient | not needed | D |
| not | not | not sufficient | E |

Show "not sufficient" with two cases that both obey the statement but give different answers. Background facts count. Repeated facts add nothing.

### A21. Fallacy list with one-line tests (Ch 23)

A fallacy only means this argument fails; the conclusion may still be true.

| Fallacy | One-line test |
|---|---|
| Ad hominem | Is the person attacked instead of the argument? |
| Straw man | Was the view twisted into a weaker one first? |
| False cause | Is "after" treated as "because"? |
| Bandwagon | Is "many do it" the only reason? |
| False authority | Is the expert outside their field? |
| False dilemma | Are there more than two options? |
| Slippery slope | Is a chain of disasters claimed without evidence? |
| Hasty generalisation | Too few or unrepresentative cases? |
| Circular reasoning | Is the conclusion hidden in the premise? |
| Appeal to emotion | Is pity or fear replacing evidence? |
| Red herring | Does the point change the subject? |
| Appeal to tradition | Is "always done" the only reason? |
| Appeal to ignorance | "Not disproved" taken as proved? |
| Loaded question | Does the question hide an unfair assumption? |
| Tu quoque | Is advice dismissed because the speaker does not follow it? |

Routine: find the conclusion, list the reasons, ask whether the reasons support it.

### A22. Correlation vs causation checklist (Ch 24)

Two things moving together may be explained by one of four stories: P (A really causes B), R (reverse: B causes A), T (a third factor causes both), C (coincidence or shared trend). Checks that move toward causation: random assignment to groups, a fair comparison group, correct time order, dose and response, a believable mechanism, repeats elsewhere. Safe wording: "is linked with", "goes together with", not "causes", unless a fair experiment supports it.

### A23. Cognitive bias list (Ch 25)

| Bias | One-line antidote |
|---|---|
| Confirmation | Look for one fact that would prove you wrong |
| Anchoring | Decide your own number first |
| Survivorship | Ask who is missing from the data |
| Sunk cost | Count only future costs and benefits |
| Availability | Look up the real count or rate |
| Halo | Score each trait separately |
| Recency | Look at the full period, then the latest |
| Framing | Restate the claim in the opposite wording |
| Hindsight and outcome | Judge the decision by what was known then |
| Base-rate neglect | Ask: out of how many cases? |
| Overconfidence | Give a range and check later |

### A24. Claim-evaluation questions (Ch 26)

1. WHO says it, and do they gain? 2. WHAT evidence is given? 3. HOW was it measured (who, how many, when, what counted)? 4. WHAT is missing (comparison group, denominator, time period, opposite cases)? 5. CAN I CHECK it elsewhere, from the original source?

Evidence ladder, weak to strong: anecdote, expert opinion without data, survey, comparison in existing data, controlled test with random assignment. Relative change needs the starting numbers ("reduced by 50%" may be 2 in 1,000 to 1 in 1,000).

### A25. Chart red flags (Ch 27)

| Red flag | Fix |
|---|---|
| Truncated bar axis | Start bars at zero |
| Cherry-picked time window | Show the full period |
| Icons scaled in two directions (area grows by the square) | One icon per fixed amount |
| Pie that does not sum to 100% | Check the sum |
| Unequal bins | Plot per unit of width |
| Dual axes | Index to 100 or use two charts |
| Mean hides outliers | Show median and spread |
| Counts instead of rates | Rate = count divided by group size |
| Percent of a tiny base | Show actual numbers |
| Running total line | Also plot daily values |
| Unlabelled log scale, reversed axis, 3D effects | Read the axis numbers; use plain 2D |

Also read: title, axis labels and units, source, denominator.

---

## Part 6: Problem-Solving Methods

### A26. Polya's four steps (Ch 28)

| Step | Ask | Write |
|---|---|---|
| Understand | What is asked? What is given? | Goal, facts, units |
| Plan | Seen something similar? Which method? | One sentence naming the method |
| Execute | Do the plan line by line | Working with reasons |
| Review | Does it fit, is it reasonable, can I check another way? | A check and a final answer |

### A27. Strategy list (Ch 29)

| Strategy | Use when |
|---|---|
| Work backward | End known, start unknown (undo each step with its opposite) |
| Simplify | Numbers big or messy; try 2, 3, 4 first |
| Find patterns | Problem grows step by step; test the rule on one extra case |
| Casework | Answer depends on a small choice; cases must not overlap and must cover everything |
| Elimination | A list of candidates and several clues |

### A28. Proof types (Ch 30)

| Claim | Killed by | Proved by |
|---|---|---|
| For all | One counterexample | An argument covering every case |
| There exists | An argument that none exist | One example |

- Direct proof: from the given, step by step, to the claim.
- Contradiction: assume the claim is false, reach something impossible.
- Counterexample: one failing case disproves a "for all" claim. Examples never prove a "for all" claim.
- Useful forms: even = 2k, odd = 2k + 1, multiple of 3 = 3m.

### A29. Induction idea (Ch 31)

Two parts, like dominoes: (1) base case, the claim holds for the first value (usually n = 1); (2) inductive step, assume it holds for k, show it holds for k + 1. Both are needed; the base case alone or the step alone proves nothing.

### A30. Algorithm checklist (Ch 32)

An algorithm is clear, ordered, finite, gives the same result for the same input, and handles edge cases (empty list, one item, ties). Routine: state input and output; do a tiny example by hand; write plain steps; write pseudocode (SET, IF, FOR EACH, WHILE, SHOW); trace it on a tiny example, an empty input and a tie.

### A31. Fermi steps (Ch 33)

1. Pin down the question (what, where, when). 2. Break into factors. 3. Give each factor a round, labelled assumption. 4. Calculate with units. 5. Sanity-check by a second route (top-down and bottom-up). 6. Give a range and name the most uncertain factor. Aim for the right order of magnitude, not exactness.

### A32. Debugging-reasoning checklist (Ch 34)

Find the FIRST faulty step, name the bug, repair it, recompute everything after it.

| Check | Ask |
|---|---|
| Re-read | Did I answer the question asked? |
| Re-do | Is each calculation right alone? |
| Units | Do units match (2 h 30 min is 2.5 hours)? |
| Base | A percent of WHAT? |
| Simple numbers | Does the method work with 100? |
| Reverse | Does the answer fit back in the problem? |
| Extremes | Is the answer possible? |
| Hidden assumption | Did I assume something never stated? |

Common bugs: arithmetic slip, unit mismatch, wrong base, average of averages (weight by group size), off-by-one (items from a to b is b - a + 1), wrong operation, converse error, double counting, hasty generalisation, unsupported step, misread condition.
