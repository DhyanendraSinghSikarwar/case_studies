# review_Book06.md — Book 6 (Aptitude & Business Maths) review summary (Wave C, plan.md Section 8.6)

Date: 2026-11-12. One reviewer per part (11 parts) independently re-solved every numeric, probability, puzzle, data-interpretation and data-sufficiency question in code (exact fractions, brute force over arrangements and orders, enumeration of models for syllogisms and data sufficiency, sqlite3 for SQL), compared with the written answers, fixed errors in place and wrote `review/review_PartNN.md` (per-fix detail there). Three reviewers (Parts 2, 7, 10) were interrupted by a usage limit and resumed after the reset. Reviewer counts are the reviewers' own and approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 724 of 724 answered; 0 `ANSWER_PENDING` (script check) |
| Count | 724 vs target 600 (met) |
| Ordering / numbering | Continuous Q1..Qn in all 11 parts (script check). Part 10 stars/difficulty are not monotone (mock items interleaved); left as is |
| Template fields | Asked at, interviewer check, Say this, follow-ups present in all 724 (script check) |
| Markdown / style | Code fences balanced; no em dashes in answers (script check) |
| Accuracy | Every headline answer matched the reviewers' independent re-solve (0 wrong final answers in Parts 1-6, 8, 9, 11; Part 7 and 10 main answers matched too); errors found were in follow-up variants, Check lines, intermediate steps, assumptions and wording |

## Per part
| Part | Answers | Answers edited | Main fix types |
|---|---|---|---|
| 1 | 82 | 14 | wrong follow-ups (Q2, Q59, Q28), Check line added to all; unproven "verified by script" claims removed |
| 2 | 67 | 12 | circular fast routes (Q18, Q19), wrong trap text (Q42), unsupported "Asked at" |
| 3 | 65 | 26 | Q11 Check, harmonic-mean limits, missing assumptions, unsupported "Asked at" |
| 4 | 52 | 9 | wrong follow-ups (Q27 Rs 740.14, Q36 difference Rs 25), garbled Q19 |
| 5 | 70 | 15 | unsupported claims, muddled shortcuts, Q64 table assumption stated |
| 6 | 69 | 12 | unsupported "Asked at" (Q60-69), missing Check lines, Q65 vowel list |
| 7 | 80 | ~16 | wrong follow-ups (Q20, Q72), wrong "unique arrangement" Check lines (Q23, Q33), Fractal puzzle claim removed |
| 8 | 94 | 12 | Q20 rate 17.02%, Q82 median follow-up, Q37 follow-up, assumptions stated |
| 9 | 49 | 17 | all option letters correct; Check wording corrected (infinite domains), shortcut limits |
| 10 | 63 | ~28 | wrong figures in Q35, Q52, Q28, Q63; Q51 contradicted Q23; shortcut limits added |
| 11 | 33 | ~17 | Q6/Q12/Q15 figures and samples, Q18 gaps, asked-at wording; SQL re-run on sqlite3 |

## Known limits (not fixed; honest status)
- **Sources:** all "Asked at" claims rest on search-snippet prep-site material and stay marked unverified; company-specific frequency claims (TCS NQT, Infosys, Wipro, Accenture, Mu Sigma, Fractal) are third-party and unconfirmed. `research/Book06_Part07_sources.md` still repeats the Fractal puzzle-round claim that `research/interview_processes.md` does not support (answers were corrected).
- **Rules of thumb:** time-per-question, mock counts, pass-mark and negative-marking guidance are labelled rule of thumb, not official figures; test patterns differ between prep sites and companies.
- **Not provable by code:** a few classic results (Part 7 Q79 minimum 7 races) are standard published answers; Excel formulas (Part 3 Q37) were not run in Excel; non-SQLite database behaviour (TRUNCATE rollback, SQL Server NULLs) not run.
- **Puzzle assumptions** (burn-time, circular-table direction, "at least one member" for syllogisms, calendar spans) are stated in the answers; a few puzzles have unique rings but not unique seat labels (stated).
- **Overlap:** many deliberate near-duplicates inside parts (+x% then -x%, false weight, MISSISSIPPI Q31/Q46 in Part 6, average speed Q11/Q24/Q43 in Part 3) and a few across parts (Part 2 Q47, Part 3 Q16 and Part 10 Q16 repeat the 60/40 round-trip average); kept and cross-referenced; not removed.
- Part header counts differ from targets (all parts exceed target by design).
- A human read-through by a non-technical reader is still advisable.
