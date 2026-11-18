# Review report: Book 10 Part 5 (Supply chain & operations)

## Counts
- Answers checked: 85 (Q1-Q85). Zero ANSWER_PENDING; 10 code fences, balanced; no em dashes in answer text.
- Answers with numbers recomputed by code (independently, in scratch `C10_Part05/v.py`): 36 (Q7, Q11, Q13-Q17, Q19, Q31 illustrative, Q38-Q47, Q49, Q50, Q60-Q62, Q68, Q69, Q71, Q73, Q74, Q76, Q77, Q81, Q83). Pasted code/SQL outputs (Q19, Q50, Q71, Q73) were re-run.
- Answers with wrong arithmetic: 0. All recomputed figures matched.
- Answers changed: 8 (Q47, Q49, Q50, Q57, Q64, Q67, Q71, Q73), for incomplete code, jargon, labelling or overclaims.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q50 | SQL shown without the input table; pasted output headers did not match the column aliases | Added the 3-order sample (as day offsets); re-ran in SQLite; pasted real output with the true headers (avg 37.3 days confirmed) |
| Q71 | pandas snippet had no data; output (8.6%, 9.6%, 1 of 6 closer, 4 worse, 1 tied) could not be reproduced | Constructed a 6-SKU sheet that reproduces exactly those outputs, added the DataFrame to the code, labelled it separate from the 18/22/25% inputs |
| Q73 | pandas snippet used `spend` without defining it | Added import and the 8-supplier DataFrame; cumulative output re-verified (40, 65, 77, 85, 91, 95, 98, 100) |
| Q49 | Lead-time-variability safety stock (about 900) shown with no formula; "sample 5.5" and CV unexplained | Added formula in plain words (variance explained) and CV definition; both 123 and 900 reproduced (900.4 using mean 18.4) |
| Q47 | "Inventory cost = holding cost x (cycle stock + safety stock)" mixed a yearly cost with a stock figure | Reworded to yearly holding cost per unit x (average cycle stock + safety stock) |
| Q57 | "Asked at" cited Flipkart supply-chain prompts, which the sources file ties to a different prompt (Tier 2 network design), not dark-store replenishment | Removed the Flipkart claim; kept "no company-specific report found" |
| Q64 | FOB and CIF details stated as fact; only the CIF risk point was labelled | Added a "from memory, unverified, confirm with the official ICC text" line covering both |
| Q67 | "tax-time of supply" is jargon a non-technical reader cannot follow | Replaced with plain words (invoice date versus physical arrival date) |

## Unresolved / report-only
- Overlap within the part: ABC and Pareto appear in Q11, Q41, Q48 and Q73; WMS/TMS/ERP in Q23 and Q30; OTIF in Q2, Q13, Q18, Q62; safety stock in Q5, Q40, Q47. Intentional gradation, but the reader meets near-repeats.
- Overlap with other books (from sources notes, not re-checked here): Book 8 B8P06Q69 (inventory turnover) vs Q3/Q17; B8P06Q41 (MAPE) vs Q19; Book 7 B7P03Q32 (picker roster) vs Q60 and Q79.
- Ordering: star/difficulty order is correct as numbered. Q60's heading ("A plant uses workforce planning like a warehouse does") is awkward but headings may not be changed.
- Q43/Q44 and others have a "Worked example" folded into Explain simply (no separate heading); content is complete, left as is.
- Q71 sample sheet WAPE (8.6%/9.6%) is deliberately a different dataset from the 18/22/25% inputs; stated in the answer.

## Claims left unverified (labelled "from memory, unverified" or generic in the answers)
- z values 1.28/1.65/2.33; textbook safety-stock formulas (Q5, Q40, Q47, Q49); EOQ assumptions.
- Incoterms FOB/CIF (Q64); bill of lading as title document (Q65); GST, e-way bill, eInvoicing, DPDP Act 2023 (Q67, Q78), landed-cost duty base and GST credit (Q74).
- "Above roughly 85-90% storage utilisation hurts" (Q76) and similar rules of thumb, labelled unverified.
- All "Asked at" lines say "commonly asked (no company-specific report found)"; the prep-site and vendor-blog attributions are from the sources file (snippet level) and stay marked unverified.
