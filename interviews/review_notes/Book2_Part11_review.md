# Book 2 Part 11 review (Wave C)

Date: 2026-10-24. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45. Target band per plan.md: Rs 30-80 LPA.

## Process
Per-agent scratch files merged by heading (45 of 45 merged, 0 skipped, 0 pending). Header status updated after the merge.

## Structure checks (scripted)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45 | pass |
| Star order and counts 12 / 19 / 14 | pass (matches header) |
| Required fields incl. Example, Output (my run) | pass |
| Salary / LPA text | none |

## Code
45 Python blocks extracted with the line-start fence rule and run standalone with `python3 -I`: all exit 0; agents confirmed each pasted output equals a fresh run. All LLMs are mocked, all security demos are defensive toys with benign placeholders and reserved example domains, no payload kits. Checked against closed forms or brute force: binomial alert thresholds vs simulation, KS fast vs brute force, Rogan-Gladen correction, sign test, Wilson intervals (closed form for k=0, bisection, exact coverage sums), Luhn against a known test number, Verhoeff against all single-digit errors and adjacent swaps, trifecta subset counting vs inclusion-exclusion, offset-aligned base64 canary patterns, token-bucket closed form and a 200-thread admission test, storage closed form vs 100k-sample simulation. Honest weak or negative results kept: sequential-test rollbacks of equal candidates (about 5-7%), regex injection detector misses paraphrases and blocks a legitimate request (9/14 caught, 1/14 benign flagged on a hand-made set), French paraphrase evades the canary scan, paraphrased poisoning from an approved source passes ingestion, label-only extraction reaches about 0.99 agreement, per-client rate rule evaded by 20 accounts, base-rate arithmetic gives about 6% precision at 0.1% prevalence, patching to a dev set leaves held-out ASR at 11/12, policy-table test flagged as weak because it restates the rules, PII redactor found 11 of 16 synthetic items.

## Facts verified from sources
OWASP LLM Top 10 2025 names (opened by the Wave A agent; check for a newer edition), OWASP LLM10 mitigations, Willison lethal trifecta post, Greshake abstract, CaMeL abstract (77% vs 84% on AgentDojo is the authors' claim in their setup), NIST AI RMF 1.0 and NIST-AI-600-1 dates (from the sources note, not re-verified), Anthropic and OpenAI guidance pages, Langfuse, LangSmith, Phoenix, Helicone and MLflow docs as summarised in the sources note. arXiv 2506.08837 abstract re-opened by the lead: it names no patterns; the six pattern names in Q45 come from a summarising fetch and are hedged (see the sources note addendum).

## Not verified (hedged in the text)
EU AI Act and India DPDP specifics (kept general, defer to counsel); OpenTelemetry GenAI attribute names (not used; field names illustrative); vendor sampling, masking and budget features; provider data-retention terms; pickle vs safetensors behaviour; ANN-filter recall caveat; provider key scoping; watermarking; Aadhaar Verhoeff checksum (check the spec); `traceparent` header; PSI > 0.2 rule of thumb; markdown-image exfiltration and CSP; Retry-After; garak, PyRIT and HarmBench named only as existing.

## Evidence limits (unchanged)
No candidate-reported LLMOps or security questions were found; evidence is OWASP, papers, vendor docs and prep guides. No source states a salary band. Stars and "Asked at" tags are indicative.
