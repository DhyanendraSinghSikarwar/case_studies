# Book 7 Part 2 review (Wave C)

Date: 2026-10-31. Reviewer: lead session (independent of the five research agents). Scope: 10 company profiles (Flipkart, Swiggy, Zomato, PhonePe, Razorpay, CRED, Meesho, Ola, Paytm, Myntra). No pay figures; no visa or legal claims.

## Process
Five agents researched two companies each (4 to 13 WebSearch searches per company, snippet-only) and wrote profiles, source logs and per-company progress files; merged in company order with `scratch/B7_merge.py 2`; the lead wrote the header (including entity notes) and the comparison table from the profiles. No spend-limit stops.

## Checks (`scratch/B7_check.py`, now including tag-to-source integrity)
| Check | Result |
|---|---|
| Profile numbering C1-C10 and all 13 template labels present and in order | pass for all 10 |
| At least 8 evidence tags per profile; at least 2 source URLs per profile; every `[S#]` used exists in that profile's Sources list | pass |
| 5 to 8 sample questions per profile, each tagged `[illustrative]` or `[S#]` | pass |
| Pay patterns (LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and codes with digits) | 0 hits |
| Cross-references to Books 1-6 (39 distinct Book/Part pairs) | all resolve to real parts; five topic parentheticals were wrong and were corrected in the profiles and the merged part (Razorpay: "Book 2 Part 9 (RAG)" became Part 6 RAG basics plus Part 9 LLM evaluation; CRED: "Book 6 Part 6 (product and stakeholder framing)" became Part 1 plus Part 6; Paytm: "Book 4 Part 12 (production ML monitoring)" became Book 4 Part 8 monitoring and Book 6 Part 2; Paytm: "Book 6 Part 10 (project narratives)" became end-to-end open scenarios) |
| Part 1 re-check of the same parentheticals | all matched the plan.md part titles |

## Findings and honest limits
- Every profile is rated Thin. No company's own data science or ML interview page surfaced; the closest official content is a company representative quoted in an Analytics India Magazine piece (Razorpay, CRED, PhonePe), which the snippets cut off before the round list.
- Indian-company evidence is mostly small candidate-report samples (some from 2020 to 2023); the profiles label them anecdotal and keep conflicting round counts side by side.
- Entity handling: Zomato (listed parent Eternal, renamed March 2025), Paytm (listed parent One 97 Communications), and Ola (ride-hailing versus Ola Electric versus Krutrim) are separated; the Paytm Labs Toronto report is flagged as a different entity and a weak signal.
- Myntra's membership of the Flipkart group was not confirmed by any result and is tagged [G] in the profile.
- Four agents ran fewer than the 6 to 10 searches per company that the brief asked for because results repeated (Razorpay, CRED, Flipkart, Swiggy); the profiles state "not found" instead of filling gaps.
- Pay content seen in results was discarded (Meesho, Myntra, Paytm snippets).
- AI-tool policy for candidates: no company statement found for any of the ten; company hiring-AI statements (Razorpay, CRED, Paytm) are about the company's own recruiting, not candidates.

## Not done
No page was opened (WebFetch fails in this environment). Nothing here replaces the company's careers page or the recruiter's description of the current process.
