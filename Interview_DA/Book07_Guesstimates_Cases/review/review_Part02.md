# Review: Book 7 Part 02 (market-size guesstimates), Q1 to Q94

## Counts
- Answers checked: 94. Answers whose numbers were recomputed by code: 94 (every chain, range, sensitivity and check; script in scratch folder C07_Part02/v.py).
- Answers with a wrong number or changed content: 40 (79 targeted edits). The rest were arithmetically correct; no headings, stars, order or inline data changed.
- Em dashes in answer text: none. Code fences: none (balanced).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 3 | "4 two-wheelers per car" compared with a different city | Reworded as rough guide from Hyderabad (Q2, Q21), 3 to 4 |
| 6 | Range (28 / 56 lakh) left out the 10% NCR uplift used in the base | Now 31 / 62 lakh |
| 22 | TAM used before explained; sanity check just restated an input | TAM defined; check now per head / per resident, labelled reality check |
| 25 | 4.2 lakh shown but 76.5 lakh needs 4.25 lakh | Step shows 4.25 lakh |
| 26 | "UPI reducing ATMs? Yes" stated as fact | Marked as assumption |
| 35 | Doctor density stated as fact | Marked assumed |
| 37 | Sensitivity said -10% (actual -14%); sanity check circular | -14%; replaced by share-of-white-collar check |
| 40 | Cars 7.5 lakh vs Q2's 6 lakh (inconsistent assumptions) | Uses Q2's 6 lakh: result about 1 lakh (was 1.3), range 70,000 to 1.3 lakh |
| 41 | District count unstated | "about 750 districts (assumed)" |
| 42 | Bengaluru 1.4 crore vs 1.3 crore in Q3/Q4 | 1.3 crore; 3.5 lakh demand vs 4.5 lakh supply |
| 44 | 14.2 kg size unlabelled | Labelled assumed |
| 46 | 150 stores not in assumptions; GMV undefined | Added to table; GMV defined |
| 47 | 8.6 lakh x 15,000 does not give 1,296 | Uses 8.64 lakh |
| 50 | Bengaluru 1.4 crore vs 1.3 crore | 1.3 crore: Rs 273 crore (was 294), range 180 to 400 |
| 51 | Wrong intermediate (9.6 lakh x 600 = 5.76 crore) | Rs 5,760 lakh = Rs 57.6 crore |
| 52 | Mini-example claimed to close "most" of gap (closes about 30%) | Corrected to about a third |
| 56 | Households "second route" same total by construction | Relabelled as plausibility check |
| 57 | Muddled sanity check (1.5 earners per household vs 0.84) | Rewritten: 0.84 daily payers per household |
| 58 | Say-this 65 to 80 lakh vs result 65 to 70; top-down hires conflicted with Q77 | Result aligned; top-down uses Q77's 2.5 lakh freshers at 9 applications per hire (total unchanged 82.5 lakh) |
| 59 | Cohort 1.2 lakh vs Q27's 1.4 lakh; circular check | 1.4 lakh: Rs 1,088 crore (was 947), range 600 to 1,400; check relabelled |
| 60 | TAM/SAM/SOM not explained before use | One-line definitions added |
| 61 | Invented "practice platform" source; loan book/yield unexplained | Source claim removed; terms explained |
| 62 | Hyderabad cars 7 lakh and two-wheelers 50 lakh vs 6 and 20 lakh in Q2/Q21 | Uses Q2/Q21: about 2,200 points (was 4,300), range 1,300 to 3,500 |
| 64 | "Sanity check" was insurer arithmetic, not a check | Affordability check added, insurer view kept as aside |
| 66, 67, 68, 69 | Unlisted assumptions (40 dealers, 7,000 vendors, 20 kg, smoker share) | Labelled assumed; vendor count made consistent (about 7,000) |
| 71 | Autos 1.2 lakh vs Q23's 1.3 lakh; driver range mixed autos and drivers | 1.3 lakh: 14,300 autos, about 20,000 drivers, range 13,000 to 27,000 |
| 72 | Say-this Rs 600 vs result Rs 650 crore; price sensitivity "plus or minus 40%" | Aligned to 650; -29% to +43% |
| 74 | 4.7 household size vs 4.5 elsewhere; mixed 17.4/18 million | 4.5: 18.2 million, Rs 8,190 crore |
| 75 | 25 million / 2 = 1 crore weddings wrong; conflicted with Q28's 90 lakh | Uses 90 lakh: Rs 5.8 lakh crore (was 6.45), range 3.5 to 8 |
| 76 | Sensitivity 1.07 to 1.64 crore wrong | 1.14 to 1.50 crore |
| 79 | Range top 14,000 (actual 14,800); "typical range" claim | 7,400 to 14,800; claim removed |
| 83 | Sample average 80 in step 1 but 88 in step 4 | Strata changed so average is 80; weighted 69; overstates 16% |
| 84 | Household size 4.7 | 4.5 (about 31 crore) |
| 86 | Range 43 / 64 lakh omitted new users | 44 / 66 lakh |
| 87 | 2,700 crore called "platform-addressable" (it is the fee if all trade moved online); mandi unexplained | Reworded; mandi defined |
| 89 | Analysts 15 lakh vs Q37's 5 lakh | 5 lakh: Rs 830 crore (was 1,530), range 415 to 1,245 |
| 90 | Active quick-commerce households 40% vs Q46's 20%; result 200 stores | 20%: about 100 stores, range 80 to 125; links to Q46's 150 stores |
| 92 | "lakh vs crore slip gives 10 times" | Corrected to 100 times |

## Unresolved / report only
- Ordering: no issues found in star/difficulty order. Q89 now far from Q37 only through the shared 5 lakh input.
- Overlap: Q9 and Q18/Q19 repeat the chai example intentionally; Q2/Q10/Q52 share the car chain; Q12 and Q20 share one order-volume build; Q33/Q11 overlap with Q1 chai. Left as is (cross-referenced).
- Household size varies by scope (4 for cities, 4.5 for India or towns); left, but worth a style-wide decision.
- Q1 and Q24 two routes agree closely by design; flagged in text for Q24.
- Q36 uses 20% aged 5 to 17 (district) vs 18% in Q27 (metro); left as a defensible difference.

## Claims left unverified
- All real-world base numbers (populations, households, vehicles, prices, fuel use, users, workforce sizes, company volumes) are labelled assumed and not checked (no web access).
- "Asked at" lines follow research/Book07_Part02_sources.md and research/interview_processes.md (Meesho New Delhi stores confirmed there); company attributions from Dataford or prep sites remain marked unverified.
