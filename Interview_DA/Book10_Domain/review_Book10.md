# Book 10 (Domain Knowledge) — Wave C review summary

Reviewed 2026-11-18 to 2026-11-19, one reviewer per part (per-part reports in `review/review_PartNN.md`). Environment: Python 3 (math, numpy, pandas, scipy, sqlite3); no web access. Part 1 and Part 3 reviewers were interrupted by a usage limit and resumed from their saved edits.

## Totals
| Part | Domain | Answers checked | Answers edited | Notable fixes |
|---|---|---|---|---|
| 1 | HR / People Analytics | 150 | 17 | Q108 placeholder data and total tie-out, Q109 count, Q133 hires arithmetic, Q132 compa-ratio vs market ratio |
| 2 | E-commerce & quick-commerce | 94 | 22 | Unsupported business-model claims relabelled, Q50 table name, Q81 wording, jargon glosses |
| 3 | BFSI | 113 | 20 | Q76 KS/AUC/Gini replaced with a reproducible table (KS 46.2, AUC 0.792, Gini 0.584), Q29 test named, four SQL snippets given sample data |
| 4 | Healthcare & pharma | 79 | 14 | Q49 clean-rows wording, SQL sample rows added, definitions and lakh conversions |
| 5 | Supply chain & operations | 85 | 8 | Q50, Q71, Q73 snippets given input data so outputs reproduce, Q57 unsupported claim removed |
| 6 | Marketing & sales | 93 | ~17 | Q55 SQL double-count and integer-division bugs, Q54 unit-cost inconsistency flagged, Q46 and Q16 statements corrected |
| 7 | IT services / GCC / MIS | 76 | 12 | Q31 estimate above contract value fixed, Q72 additivity contradiction fixed, Q33 time-zone claim |
| 8 | Learning a new domain | 28 | 7 | Q10 "Asked at" corrected to the sources, Q21 sample rows added, Section 7 coverage complete |
| **Total** | | **718** | **~117** | |

About 480 answers had their figures recomputed by independent script and compared with the text. No headline arithmetic result was wrong; the fixes were mostly reproducibility (snippets that showed output but no input data), a few internal inconsistencies in worked examples, SQL bugs, overstated "Asked at" and business claims, and plain-words explanations. Final automated check: 718 answers, balanced code fences, zero `ANSWER_PENDING`, zero em dashes outside file titles.

## Still unverified (labelled in the text)
- Every regulation and statutory detail (RBI, IRDAI, CDSCO, HIPAA, DPDP Act, PMLA, GST and e-way bill, PF/ESI/gratuity, labour law) is from memory, awareness level only, with a "confirm with the compliance/legal team" pointer. No legal, medical or financial advice is given.
- Workday and Alteryx feature statements, standards (ICD-10, CDISC, GS1, Incoterms), industry formulas and rules of thumb (HCVA, Bradford factor, PSI cut-offs, safety stock, ABC/XYZ cut-offs) are from memory.
- All "Asked at" lines rest on search snippets; no first-hand Hyderabad or Bengaluru reports were found, so most say "commonly asked (no company-specific report found)".
- All example numbers are invented exercise inputs.
- Resource and dataset names (Part 8) are from memory: check links.

## Open items for a later pass (report-only)
- Several parts repeat a topic from different angles (DPDP awareness in Part 1; ALOS/occupancy in Part 4; SLA/utilisation/Alteryx Join in Part 7; Q46/Q85 and Q2/Q81 in Part 6). Kept because each asks a different angle.
- Part 1 Q86 onwards uses a slightly different follow-up and "Say this" layout from Q1-85; Part 7 header says target 65, actual 76.
- Compa-ratio vs market-ratio wording should stay consistent across Part 1 compensation answers.
- The old chunk file `answers_chunks/B10P06_Q17-32.md` still contains the pre-fix "Q39 area" wording (merged part file is correct).
