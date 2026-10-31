# BOOK7_EXECUTION_PLAN.md — How Book 7 (Company Interview Processes, 4 parts, 40 companies) will be built

Follows plan.md §2 (Book 7), §4, §11 and style_guide.md. Books 1-6 are complete. Output files: `Book7_Companies/Book7_Companies_PartNN.md`. Audience: Data Scientist / ML Engineer / GenAI Engineer candidates preparing loops at product, unicorn, GCC and European/global companies.

## What is different about Book 7
Books 1-6 are question banks with runnable code. Book 7 is a set of company PROFILES built from live research. The risk is false precision: a wrong round count, duration or question attributed to a company misleads a candidate. So the book is organised around evidence labelling, not around volume.

Environment limits: WebFetch does not work here (every fetch fails with ENOTFOUND, including from the web-fetch agent type), so research is WebSearch result snippets only. Every statement about a company is therefore labelled by how it is supported. Nothing is presented as current fact beyond what a snippet supports.

## Hard rules (the checker enforces what it can)
1. NO salary or compensation figures anywhere, and no pay-band words with numbers (plan.md's "level/salary band" field becomes "Level notes": level names and what is expected, never pay). The checker flags LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and USD/EUR/INR followed by digits.
2. Every factual claim about a company's process carries an evidence tag: `[S1]`, `[S2]`... pointing to the profile's Sources list (each source: URL as seen in a search result, what the snippet supports, date seen, snippet-only), or `[G]` for a stable, general convention of the company type that is not specific to the company (stated as a pattern, never as "X does this"), or `[U]` for unverified/uncertain. No bare claims.
3. Never invent rounds, durations, team names, interviewers, recruiter practices or specific questions. If sources do not give round durations, write "duration not found in sources". Candidate-reported content (forums, blogs, review sites) is labelled as anecdotal; a single anecdote is never presented as the process.
4. Sample questions are ILLUSTRATIVE (editor-written to match the question types the sources describe) unless a snippet supports a specific question; each is tagged `[illustrative]` or `[S#]`, and mapped to the book and part where practice material exists (cross-reference by part topic names, e.g. "Book 5 Part 9 graphs", not by guessed question numbers).
5. State confidence and what to verify on the company's own careers page; processes change often (AI-era: more live-coding scrutiny, some companies allowing or banning AI tools, onsite versus virtual). Label what is recent and what is older.
6. No claims about visa, legal or immigration rules (Book 8 covers regions and will say "check official sources").
7. No disparagement; no insider/confidential material; no claims that a question "will be asked".
8. Commit and push WIP often (a stop hook demands it); plain push, never force; never create PRs; if git add crashes (bus error) remove a stale `.git/index.lock` and retry; spend-limit stops happen: resume the agent with SendMessage (finished work on disk is kept).

## Company profile template (labels in this order, exactly)
`### Cn <Company> (<type>)` / `**Evidence level:** High | Medium | Thin` plus one line why / `**Roles seen in sources:**` / `**Process overview (as reported):**` (numbered rounds with format, duration only if sourced, each tagged) / `**Round by round:**` (a table: Round | Format | What is tested | Evidence) / `**Question types:**` / `**Sample questions (illustrative):**` (5-8, each tagged and mapped to Books 1-6) / `**What they score:**` / `**Level notes:**` (level names and expectations only) / `**Preparation plan (2 weeks):**` (day-block plan mapped to Books 1-6 by part topic) / `**Common mistakes:**` / `**Recent changes and AI-era notes:**` / `**Sources:**` (numbered; URL, supports what, date seen) / `**Confidence and what to verify:**`. Spoken, plain language; bullets and tables; no filler.

## Part file layout
Header (title, scope, target, actual, date, status, evidence limits, how to read the evidence tags) then `---`, then a company comparison table written by the lead from the profiles (rounds as reported, coding emphasis, ML depth, case or product round, system design, behavioural emphasis; each cell only where sourced, otherwise "not found"), then the profiles C1..C10.

## Pipeline
1. **Wave A+B (5 agents per part, 2 companies each, own folder `scratch/B7PNN_Cxx-yy/`):** each agent researches its companies with WebSearch (aim for 6-10 searches per company: official careers/interview-process pages, engineering blogs, candidate-experience pages, prep guides, recent AI-era changes) and writes `profiles.md` (the two profiles), `sources.md` and per-company progress files to disk early. Brief: `scratch/B7_brief.md`.
2. **Merge (lead):** `scratch/B7_merge.py N` builds the part file from the agents' profiles in company order and adds the header.
3. **Wave C (lead):** `scratch/B7_check.py <part file>` (labels, order, evidence tags on claims, salary patterns, source counts, URLs only as seen), spot-check three profiles against their sources, write the comparison table, `review_notes/Book7_PartNN_review.md`, update plan.md tracker and this checklist, commit and push.

## Part checklist
| Part | Coverage | Companies | Status |
|---|---|---|---|
| 1 | Big Tech: Google, Microsoft, Amazon, Meta, Apple, Netflix, Uber, LinkedIn, Adobe, Salesforce | 10 | ✅ (evidence: 7 Medium, 3 Thin) |
| 2 | Indian product/unicorns: Flipkart, Swiggy, Zomato, PhonePe, Razorpay, CRED, Meesho, Ola, Paytm, Myntra | 10 | ⬜ |
| 3 | GCCs/MNCs in India: Walmart, Target, JPMorgan, Goldman Sachs, American Express, Visa, Mastercard, Intuit, Atlassian, Optum | 10 | ⬜ |
| 4 | Europe/global: Spotify, Zalando, Booking.com, Klarna, SAP, Delivery Hero, Revolut, Wise, Grab, Shopee | 10 | ⬜ |

## Next step
Part 2 Wave A+B: five agents (Flipkart+Swiggy, Zomato+PhonePe, Razorpay+CRED, Meesho+Ola, Paytm+Myntra); Zomato's listed parent is Eternal, say so in the profile if sources do. Part 1 lessons: no company got a High evidence rating because official pages appear only as snippets; every claim needs a tag that exists in the profile's source list; the checker now enforces that; keep India-specific evidence separate from global process claims; label candidate AI-tool policies by source quality; use the same source-list format as Part 1 (`- S1: URL . Supports: ... Seen date. Snippet only.`); where sources are thin say so rather than pad.
