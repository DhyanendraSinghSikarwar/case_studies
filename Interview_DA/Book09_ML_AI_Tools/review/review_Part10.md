# Review: Book 9 Part 10 (LLM/RAG basics), Wave C

**Counts:** 22 answers checked; 8 Python/SQL code blocks run (Q4, Q8, Q11, Q13, Q16, Q17, Q19, Q20) on Python 3.13, pandas 3.0.5, numpy 2.5.3, sqlite3; 8 of 8 outputs matched the pasted Output exactly; 8 answers edited for wording/clarity (Q6, Q7, Q8, Q13, Q12, Q19 twice, Q20); 0 answers had wrong code, output or numbers. Other 14 are concept-only, unchanged.

## Figures recomputed
- Q4: 12,000 x 1.3 = 15,600 tokens vs 8,000 window = 1.95x ("about twice" correct).
- Q8: softmax probabilities at T=0.2/1/2 match.
- Q11: 60-character split cuts "30" into "3" and "0" (confirmed).
- Q13: 4 of 5 hits = 0.8 (confirmed).
- Q19: generated N=400, S=300 (sum 700) vs base N=300, S=300 (total 600); overstatement of 100 from order 1 duplicated by two return rows (confirmed).
- Q20: seeds 1,2,3 give low, high, high with numpy 2.5.3 default_rng (seed-dependent, already stated); greedy = high.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q6 | "cosine similarity" used before defined | Added one-clause gloss (near 1 similar, near 0 unrelated) |
| Q7 | "chunks" undefined at first use here | Gloss added (small pieces of text, Q11) |
| Q8 | Output shown without explaining the formula | What it means now says divide by temperature, convert to percentages (softmax) |
| Q12 | "in my experience-based view" is a personal-experience claim | Reworded to "named as usual suspects in prep material (unverified, not a measured statistic)" |
| Q13 | "top k" / "k" unexplained | Added k definition |
| Q19 | Prose cited "grand total 700 vs 600" but code never prints 700; jargon (grain, join keys, NULLs) | Explained 700 as sum of the generated query's regions; glossed jargon |
| Q20 | "seed" unexplained | One-line definition added |

## Checks with no change needed
- Headers (Asked at, checker, Say this), Explain simply, Likely follow-ups, Common mistakes present in all 22; Code/Output present in code questions.
- "Asked at" claims match research/Book09_Part10_sources.md (no company-specific reports; Infosys review marked unverified).
- No em dashes in answer text (only the part-title line has one); code fences balanced (32 fences); no live LLM calls; all "mock" code is offline toy code and says so (Q8, Q16, Q19, Q20). Example prompts are text only.

## Report-only
- Ordering/numbering: no problem. Part header says Target 20, Actual 22 (consistent with task).
- Overlap: Q5 and Q15 (RAG vs fine-tuning) overlap deliberately; Q8 and Q20 (temperature/randomness) overlap; Q9 and Q21 privacy repeat. Possible overlap with other Book 9 AI-tools parts (not compared).

## Unresolved / left unverified
- Token rule of thumb (1 word ~ 1.3 tokens), context-window behaviour, vendor data retention and training use, DPDP/GDPR duties, hybrid search, LLM-as-judge, temperature-0 determinism, prompt-injection controls: all already labelled "from memory, unverified" in the answers; not checkable offline.
- Prep-site/Glassdoor claims remain unverified snippets per the sources file.
