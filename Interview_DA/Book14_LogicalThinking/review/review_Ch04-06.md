# Review Ch04-06 (Book 14, Wave C)

Scope: Ch04, Ch05, Ch06 chapter files and answer keys. Scratch: C14_Ch04-06 (verification script v.py).

## Counts
| Chapter | Practice re-solved by code or exhaustive check / total | Wrong answers | Changed |
|---|---|---|---|
| Ch04 (20) | 20 / 20 (Q20 over all 16 attendance combos: unique; Q11, Q17 tables; truth-table columns for Ex 1, Q4, Q12) | 0 | 1 key note |
| Ch05 (25) | 25 / 25 (all negation rules over every group of 0-4 items; Q7, Q15, Q19, Q22 tables recomputed) | 0 | 2 wording fixes |
| Ch06 (20) | 20 / 20 (if-then shapes by truth table; all/some/no arguments over every 3-person group; Q17 gives exactly 2 combos) | 0 | 2 wording fixes |

Also re-solved: all 15 solved examples (5 per chapter), all 6 scenarios, all 9 self-check questions. All agree with the written answers. Counts, tags (green/yellow/red order), 5 examples, 2 scenarios, 5-line recaps, 5-item mistake logs, self-check answers in keys: all present and correct. Word counts about 2,600 to 3,100 per chapter. No em or en dashes, no code fences, tables followed by blank lines.

## Fixes
| Chapter | Item | Problem | Fix |
|---|---|---|---|
| Ch04 key | Q17 | Correct answer (S2, S4, S6), but the rule is self-contradictory for anyone with score at least 40 and attendance below 75; unexplained | Added a note saying S2 and S4 can never satisfy the rule |
| Ch04 | Spreadsheet pointer | Excel formula shown without the "from memory" label; arguments were vague | Wrote `=IF(condition, value_if_true, value_if_false)` and labelled "from memory, not run here" |
| Ch05 | Quantifier table | "any" listed under "All"; ambiguous for beginners ("any" can mean "some") | Removed "any" |
| Ch05 | Memory trick | Sentence was garbled and contradicted itself | Rewritten to say which rule flips the property and which keeps it |
| Ch06 | Recap line 4 | Ungrammatical ("If P then Q, with P is valid...") | Reworded |
| Ch06 key | Q19 | Non-standard term "valid by emptiness" | Changed to "vacuously valid" |

No puzzle was wrong, non-unique or ambiguous; no question numbers, tags or counts changed.

## Overlaps
- Book 13 Part 2 and Book 6 Part 7 grepped for all Ch04-06 topics (only if, unless, converse, negation of all/some, leap year, penguins/birds, helmets, encryption, expense claims, and so on). Only generic concept overlap (the same rules must be taught); no question, scenario, names or numbers copied or lightly reworded. Book 13 items use audit/licence, refund/manager approval, bonus table, policy/claim; Book 14 uses different scenarios.
- Inside Book 14: Ch06 Q9 (Priya, long-service award) shares a scenario theme with Ch01 Q11 (different task: unstated premise vs invalid denial). Ch06 Scenario 1 loyalty-card theme also appears in Ch21 item 40 (different structure). Left as is; low risk. Self-check Ch05 Q1 mirrors Example 1 in style (intended warm-up).

## Cross-references checked
Ch06 "Chapter 1" (argument, premise) and "Chapter 12" (syllogisms) exist and match; Ch04 key "Chapter 3" (NOT of AND) matches; "Book 13 Part 2" (deductive logic and conditional reasoning) exists and covers conditionals and negation. Definitions of converse, inverse, contrapositive, counterexample and "unless" are consistent across the three chapters.

## Unresolved / notes
- Ch04 "unless" is taught as "if not" (one-way); stated explicitly as the book's convention, consistent with Book 13 Part 2 Q27. No change needed.
- Ch05 mentions Excel COUNTIF and SQL NOT EXISTS by name only (no formulas shown); nothing to label.
- De Morgan "19th century logician" is common knowledge from memory, unverified (no web access).
- I did not re-check Ch01 to Ch03 or Ch12 content beyond the greps above.
