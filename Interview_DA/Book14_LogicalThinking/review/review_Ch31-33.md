# Review Ch31-33 (Book 14, Wave C)

Scratch: scratchpad/C14_Ch31-33/v.py (independent re-solve by code, run before comparing with keys).

## Counts
| Ch | Practice re-solved by code / total | Self-check | Examples + scenarios recomputed | Wrong or changed answers |
|---|---|---|---|---|
| 31 | 10 / 10 (Q4-Q8 formulas checked for n=1..299; voucher puzzles Q9 and Ex 4 by exhaustive search; Q1-Q3, Q10 are reasoning items, checked by hand) | 3 / 3 | 5 + 2 | 0 wrong |
| 32 | 20 / 20 (every sample traced with an equivalent program: halving-search guess counts, reconcile, averages, runs, merge, discount table) | 3 / 3 | 5 + 2 | 0 wrong |
| 33 | 20 / 20 (all arithmetic recomputed) | 3 / 3 | 5 + 2 | 0 wrong |

Template checks passed: 5 examples, 2 scenarios labelled illustrative, 10/20/20 practice questions (match index), 3 to 5 mistakes, 5-line recap, keys cover every question and self-check, no answers in chapter files, no em or en dashes, fences balanced, blank line after every table.

## Fixes
| Ch | Item | Problem | Fix |
|---|---|---|---|
| 31 key | Q10 point 3 | Wording muddled about why the step cannot go from 1 to 2 | Reworded |
| 31 key | Q9(b) | Uses "assume all earlier amounts" (step reaches back 4) without saying it is the same idea | Added one explanatory sentence |
| 32 | Scenario 2 table header | "Over 1,000?" contradicts the rule "1,000 or more" | Header now "1,000 or more?" |
| 32 | Pseudocode table | Keys use `ELSE IF` and "table" but the building-block table did not define them | Added two rows (extra choice, list and table) |
| 32 key | Q10 | Text says 0 or 1 items give "yes" but pseudocode took "the first value" of a possibly empty list | Added a guard IF and a note |
| 33 | Q10 | Spreadsheet row limit used unlabelled | Added "(from memory, unverified)" (same label as Scenario 2) |

## Overlaps
- Greps of Book13 and Book06 Part07 (induction, handshake, vouchers, chai, reconcile, algorithm, reams, loaves, lifts): none close. Q5 (Ch31) handshakes-by-induction differs from Book13 handshake counting (pairs, different structure). Book07 chai/guesstimate topics are by the user's design; Ch33 numbers and structure are new.
- Inside Book 14: no duplicate questions found for these topics (Ch34 Q8 is unrelated tea/coffee Venn item).

## Cross-references checked
Ch31 refers to Ch30 Example 3 (exists: ten true cases then n=10 fails) and Ch1 (title covers induction vs deduction); Book 1, 2, 6 Part 7, 7, 13 all exist.

## Unresolved / unverified
- Excel row limit 1,048,576 (Ch33 Scenario 2, Q10) is from memory, unverified, labelled.
- Ch32 Q6 (tea) is a free-form daily-life item with no single checkable answer; model answer is one acceptable version.
- Ch33 sanity remarks such as "plausible for a bakery" are illustrative judgement, not facts.
- Word counts 2,790 to 3,231 (within range).
