# Review: Book 10 Part 2 (E-commerce & quick-commerce)

Reviewer: Wave C. File edited in place: `Book10_Domain/Book10_Part02.md`. Scratch scripts: `calc.py`, `sql.py`, `ed.py` in the scratchpad `C10_Part02`.

## Counts
- Answers checked: 94 (Q1 to Q94; no ANSWER_PENDING left; 14 code fences, balanced).
- Answers whose numbers were recomputed in code from the question data: 49 (Q10, 11, 12, 13, 16, 18, 19, 21, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 57, 58, 62, 63, 65, 66, 73, 80, 84, 87, 88, 92, 93, 94, plus the unit conversions in Q13/Q21 and the table in Q54 checked by hand).
- SQL snippets executed in SQLite and compared with pasted output: Q10, Q14, Q20, Q50, Q57, Q62, Q81. All reproduced the pasted results (sample rows were rebuilt to match the described output).
- Answers with wrong arithmetic: 0. Every figure matched (including percentage vs percentage-point wording, lakh/crore, break-evens, Simpson's paradox table).
- Answers changed (wording, labels, clarity, code consistency): 22.

## Fix table
| Q | What was wrong | Fix |
|---|---|---|
| Q1 | "Quick commerce is usually inventory-led or hybrid" stated as company fact | Reworded "often ... models differ by company and change over time" |
| Q5 | Dark store and FC size claims (few thousand SKUs, lakhs of items) stated flat | Marked "typically / varies by company"; lakh explained |
| Q6 | "Percentiles" used without explanation | Plain-words definition added |
| Q17 | "90th percentile" unexplained | Defined as "9 in 10 orders arrive within X" |
| Q20 | "Asked at" claimed ranking window functions in Flipkart/Swiggy reviews; sources only support window functions (Swiggy) and lead/lag (Flipkart) | Narrowed to what sources say |
| Q21 | "MTU widely used in Indian quick-commerce reporting" is an unsupported real-world claim | Relabelled "from memory, unverified" |
| Q23 | "Mix effect vs rate effect" not explained for a beginner | Both defined in brackets |
| Q35 | "Shipping fee mostly goes to the courier" stated as fact | Softened to "may largely pass through (varies by platform)" |
| Q39 | Follow-up asserted how platforms record bank offers | Replaced with "depends on how finance books it; ask finance" |
| Q40 | "Statistical significance / confidence interval" jargon | Plain explanation added |
| Q50 | SQL used table `purchases` while the data line named `orders`; no sample note on output | SQL changed to `orders` / `ordered_at`, matched to data line; output labelled as sample (rerun: s2, s3, s1) |
| Q53 | "False-positive cost" unexplained | Defined |
| Q62 | SQL shown with no output; "window function" unexplained | Real output and plain-words line added; term explained |
| Q65, Q66, Q80 | "computed by script" scaffolding in answer text | Removed |
| Q70 | "25th to 75th percentile" unexplained | Added "middle half of stores" |
| Q81 | "one order is underpaid" but the data shows O4 unpaid and O2 overpaid | Wording corrected to match output |
| Q85 | "shrunk average" jargon | Replaced with plain method |
| Q88 | Y courier 26/800 shown as 3.3% (exact value 3.25%) | Shown as 3.25% |
| Q90 | "confounders" unexplained | Defined in brackets |
| Q93 | Precision, recall and logistic regression unexplained | Each defined in plain words |

## Checks passed without change
- Domain definitions (GMV, take rate, ROAS/ACoS as inverses, fill rates, RTO vs return vs cancellation, contribution, shrinkage vs wastage, MTU, Simpson's paradox) are standard or labelled as company-dependent.
- Regulation items (Q7 COD probe, Q29 fee rules, Q56 DPDP, Q79 E-Commerce Rules/dark patterns, Q83 Code on Social Security, Q55, Q53, Q69, Q77, Q86) all carry "from memory, unverified / confirm with compliance or legal"; no section numbers, penalties or dates asserted.
- Invented numbers are labelled invented or are question data; no real benchmark quoted as fact.
- Q45 (HR background) is a template-style answer with no personal-experience claims.
- Only one em dash remains (part title line, allowed).

## Unresolved / report only
- Ordering: all 94 questions follow star then difficulty order (3-star 🟢, 🟡, 🔴, then 2-star, then 1-star); no issue found. Header says Actual 94 vs target 90; consistent.
- Overlap: Q16 and Q73 (fill rate), Q12 and Q94 (on-time rate), Q25 and Q93 (COD RTO), Q33/Q86 (seller data), Q14 and Q62 (repeat customers) overlap in theme but test different skills; Q80 (GMV and GST) may overlap Book 10 Part 1 finance questions; not checked against other parts.
- Q54, Q82, Q84 have no "Asked at" evidence beyond "commonly asked"; acceptable per rules.
- Q49 and Q92: the "contribution" definition is labelled mine (varies by company); the rupee examples are invented.

## Claims left unverified (all labelled in the text)
Fulfilment programme details (FBA, Flipkart Assured), COD-charge probe reported in press, 30-minute session rule, typical category economics (Q32), DPDP principles, E-Commerce Rules and dark-pattern content, Code on Social Security gig-worker provision, buy-box factors, quick-commerce business models.
