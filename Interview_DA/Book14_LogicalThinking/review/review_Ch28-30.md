# Review Ch28-30 (Book 14) 

Method: every example, scenario, self-check and practice item re-solved by Python (brute force over arrangements, schedules, codes, digits, game states, timer flips) before comparing with chapter and key. Scratch: scratchpad/C14_Ch28-30.

## Counts
| Chapter | Practice re-solved / total | Answers wrong | Items changed |
|---|---|---|---|
| 28 (Polya) | 10 / 10 (plus 5 examples, 2 scenarios, 3 self-checks) | 0 | 0 (key wording only) |
| 29 (Strategies) | 25 / 25 (plus 5 examples, 2 scenarios, 3 self-checks) | 0 | 0 (key wording only) |
| 30 (Proofs) | 20 / 20 (plus 5 examples, 2 scenarios, 3 self-checks) | 0 | 2 rewritten (Q14, Q20) |

All answers, unique solutions (Ch28 Q5, Q8, Q9, Q10; Ch29 Q11, Q15, Q18, Q20, Q21, Q23) and counterexamples (n=10 for n^2+n+11, n=16 for n^2+n+17) confirmed. Q19 timer flips (4, 7, 8) confirmed as the only routes to minute 9 in the search. Practice counts match index (10, 25, 20). No em/en dashes, no code fences, tables followed by blank lines.

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| 30 | Q20 | Near copy of Book 13 Part 5 Q17 (25 people, same birth month, at least 3) | Rewritten: 19 trainees in 9 batches, at least 3 share a batch; key updated |
| 30 | Q14 | Same numbers and argument as Scenario 2 (8 people, 7 days), duplicate inside the chapter | Rewritten: 7 employees, 6 lunch menus; key updated |
| 30 | Terms | "divisible by" and "remainder" used (Q13, Q16, Q18) but never defined | Added two short entries to the word list |
| 30 | Pointer | "Book 13 Part 5 ... must be true questions" mismatched Part 5 content | Now Part 2 (deductive logic) and Part 5 (constraint puzzles) |
| 28 | Pointer | "Book 13 Part 10" for timed reasoning (Part 10 is brain teasers; timed sets are Part 11) | Now Part 10 and Part 11 |
| 28 key | Q9 review | Garbled aside "H = 4 = 2 x 2?" | Rewritten clearly; 462 shown as the extra solution without the odd clue |
| 28 key | Q4 | Redundant wording in the 1-pack case | Tidied, result unchanged (11) |
| 29 key | Q21 verification | Garbled check line ("gives 8?") | Rewritten as clean hit/near counts for 2158 |

## Overlaps
- Ch30 Q20 vs Book 13 Part 5 Q17: fixed (above). Ch30 Example 4 (13 employees, birth month) is the same principle as Book 13 Part 5 Q17 and Part 10 Q18 (85 employees) but a different task (a written proof, different numbers); left, flagged as acceptable.
- Ch29 Example 3 (pairs playing games) and Book 13 Part 5 Q16 / Part 10 Q28 (round robin, handshakes) share the counting idea only; scenario and numbers differ; left.
- Grepped Book 13 and Book 6 Part 7 for muffin/bakery, lamps, lift, stamps, tokens game, sand timers, matchsticks, passcode, committee, notes: no matches. No other duplicates within Book 14 found for these topics (birth-month items appear only in Ch30).

## Honesty and conventions
Scenario numbers are labelled illustrative. Pólya is a real historical figure named only as the method's source (no statistic or claim). No effectiveness claims. No spreadsheet formulas shown. Key statements "A computer count agrees" are now true (all rerun).

## Unresolved / unverified
- Ch29 Q19 assumes both timers are started together at minute 0 (implicit in the puzzle); left as is.
- Ch28/29 cross-references to "Book 1" for formulas were not opened (Book01_Excel exists); topic coverage unchecked.
