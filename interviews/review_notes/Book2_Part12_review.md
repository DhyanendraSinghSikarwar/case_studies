# Book 2 Part 12 review (Wave C) and Book 2 final pass

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 40 questions, Q1-Q40. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (40 of 40 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q40 | pass |
| Star order and counts 13 / 15 / 12 | pass (matches header) |
| Required fields incl. Example, Output (my run) | pass |
| Salary / LPA claims | none (the word "salary" appears only inside toy HR data in code) |

## Code
40 Python blocks extracted with the line-start fence rule and run standalone with `python3 -I`: all exit 0; agents confirmed each pasted output equals a fresh run (two runs identical where timing was involved). All LLMs, ASR, OCR and embeddings are mocked or toy. Checked against closed forms or brute force: Wilson vs exact Clopper-Pearson, Wilson vs z-score equation, Verhoeff over all single-digit errors and adjacent swaps, Monte Carlo vs closed form for the degradation ladder (0.9441 vs 0.9440), bootstrap SE vs closed form, WER on known cases, 300-conversation property test of the memory manager, leak fuzz with a mutant store (0 leaks vs 751). Honest weak results kept: Q3 no model clears the in-country bars at n=150; Q4 learning curve flattens; Q6 semantic-layer win is circular; Q7 LLM normaliser worsens a field with no checksum (8.05% silent wrong); Q9 no relevance floor; Q10 keyword intent model misses a paraphrased payment request; Q13 mini-RAG over-abstains (6 of 9 answerable answered); Q16 thresholds do not transfer between embeddings (0.99 vs 0.9 for zero false hits); Q21 comment cap drops a real finding; Q22 Hinglish confirmation missed; Q24 spam precision 0.76; Q26 offline replay underestimates true lift (1.035 and 1.065 vs 2.346); Q33 hybrid below dense and indistinguishable at n=60; Q11 gate returns NO-GO on a sample-size problem.

## Facts verified from sources
BIRD and Spider dataset sizes (abstracts opened in Wave A; BIRD 40.08% vs human 92.96% is a dated 2023 figure, labelled), RouteLLM "more than 2x" (authors' abstract claim), RBI FREE-AI press release facts (13 Aug 2025, seven Sutras, 26 recommendations, six pillars; the full report was not read). Everything else is the answers' own arithmetic or labelled ASSUMED/synthetic.

## Not verified (hedged in the text)
DPDP Rules specifics, RBI video-KYC and deepfake directions, e-invoice IRN threshold (none stated; defer to counsel); Stanford legal-RAG hallucination rates (described qualitatively only, no figures); voice-latency stage figures and turn-taking thresholds; leaderboard numbers; semantic-cache published thresholds; IDP vendor accuracy claims; Hinglish WER ranges; prices, GPU throughput; SSE proxy buffering (from memory); provider idempotency-key support; PAN and IFSC layouts (check issuer specs).

## Book 2 final pass
- 12 parts, 558 questions (47, 44, 44, 47, 41, 53, 50, 52, 46, 49, 45, 40), inside the plan's 520-600 range.
- Headers: every part's Actual count equals the number of `### Q` headings and the star counts match; zero ANSWER_PENDING in all 12 files; all Status lines read review done.
- Cross-references: every "Part N Qm" reference in Parts 1-12 points to an existing question heading (scripted, 0 out-of-range). Topical correctness was checked per part at review time.
- question_index.md has the expected number of B2PNN rows per part.
- Rupee mentions are in code or data (crore revenue examples, lakh as a unit); no salary figures or LPA claims appear as facts.

## Evidence limits (unchanged, stated in every part)
No candidate-reported questions were found for any company; evidence is papers, vendor docs, OWASP, regulator press releases and prep guides. No source states a salary band. Stars and "Asked at" tags are indicative.
