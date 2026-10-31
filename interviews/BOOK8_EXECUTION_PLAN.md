# BOOK8_EXECUTION_PLAN.md — How Book 8 (Region-wise Interview Processes versus India, 3 parts, 13 profiles) will be built

Follows plan.md §2 (Book 8), §4, §11 and style_guide.md, and reuses Book 7's evidence method (see BOOK7_EXECUTION_PLAN.md). Books 1-7 are complete. Output files: `Book8_Regions/Book8_Regions_PartNN.md`. Audience: data science, ML engineer and GenAI candidates in India, or based elsewhere, who are considering roles in other markets.

## What Book 8 is
Region profiles built from live research: how hiring for data and ML roles tends to run in each market, how that differs from the Indian process, and how to use Books 1-7 to prepare. The risks are stereotyping, false precision and legal/immigration misstatements, so the book is built around evidence tags, process-level (not person-level) comparisons and pointers to official sources.

Environment limits: WebFetch does not work here (every fetch fails with ENOTFOUND), so research is WebSearch result snippets only. Every statement is labelled by how it is supported.

## Hard rules (the checker enforces what it can)
1. NO pay figures or pay-norm statements of any kind. plan.md's "salary norms" field is replaced by a one-line note that pay is out of scope. The checker flags LPA, lakh, crore, CTC, salary, compensation, base pay, per annum, currency symbols and currency codes with digits.
2. NO visa, work-permit, immigration, tax or employment-law claims stated as fact: no eligibility rules, thresholds, fees, processing times, quotas or sponsorship practices. The "Work authorisation: where to check" section names the official government source(s) to consult (and the URL only if it appeared in a search result), says what a candidate should verify there (route type, employer requirements, timelines), and uses `[U]`/`[G]` honestly. The checker flags digits near the words visa, permit or sponsorship for manual review.
3. Every factual claim carries `[S#]` (a numbered source in the profile: URL as seen in a search result, what the snippet supports, date seen, snippet only), `[G]` (a general convention, not specific to the country, stated as a pattern) or `[U]` (unverified or weakly sourced). No bare claims. Never invent URLs, stages, durations or customs.
4. "How candidates coming from India's process commonly differ" is a PROCESS comparison (formats, conventions, paperwork, timing), never a statement about people or nationalities: no stereotypes, no culture generalisations about Indians or the host country's people. Frame as: what a candidate used to the Indian process should expect to look different, each point tagged. If a source makes a stereotyped claim, discard it.
5. Anecdotes are labelled anecdotal; a single anecdote is never the norm. Mark recent versus older evidence; AI-era changes are labelled by source quality.
6. Company examples may reference Book 7 profiles (by company name and Part) but must not contradict them; do not repeat company-specific claims without their tags.
7. Commit and push WIP often (stop hook); plain push, never force; never create PRs; if git add crashes remove a stale `.git/index.lock`; resume spend-limited agents with SendMessage.

## Region profile template (labels in this order, exactly)
`### Rn <Country or region> (<region group>)` / `**Evidence level:**` (High | Medium | Thin plus a line why) / `**Market snapshot for data and ML roles (as reported):**` (employer types present, hiring season or hubs only if sourced, no pay) / `**Hiring process norms (as reported):**` (typical stages and any sourced timelines) / `**Round formats:**` (a table: Format | How common as reported | What is tested | Evidence; take-home versus live coding versus case versus system design versus behavioural) / `**Culture and communication style in interviews:**` / `**CV and application format:**` (length, photo, cover letter, references, local conventions, only if sourced) / `**Language and location notes:**` / `**Work authorisation: where to check:**` (official sources only, what to verify, no claims) / `**Process differences for candidates coming from India's process:**` (process-level, tagged) / `**How to use Books 1-7 for this market:**` (mapped by part topic names, checked against plan.md titles) / `**Preparation checklist (2 weeks):**` / `**Common mistakes:**` / `**Recent changes and AI-era notes:**` / `**Sources:**` (numbered S1..) / `**Confidence and what to verify:**`. Spoken, plain language; bullets and tables.

## Part layout
Header (title, scope, target, actual, date, status, evidence limits, how to read tags) then `---`, then a comparison table written by the lead from the profiles (process features only, only where sourced, otherwise "not found"), then the profiles R1..Rn. Part 3 additionally holds an India baseline profile (the reference point for all comparisons) and a closing section "India comparison and relocation preparation guide" written by the lead from the profiles (process-level preparation steps, with every official-source pointer and no immigration claims).

## Pipeline
1. **Research and write (agents, own folders `scratch/B8PNN_Rxx-yy/`):** each agent researches its regions with WebSearch (6-10 searches per region from different angles: data/ML interview process in that country, take-home versus live coding, CV format and conventions, local-language expectations, hiring hubs, AI-era changes, official government job-seeker pages, candidate reports) and writes `profiles.md`, `sources.md` and per-region progress files early. Brief: `scratch/B8_brief.md`.
2. **Merge (lead):** `scratch/B8_merge.py N`.
3. **Wave C (lead):** `scratch/B8_check.py <part file>` (labels, tags, tag-to-source integrity, sources, salary patterns, visa-digit flags), mapping scan of every `Book N Part M (topic)` against plan.md titles, spot-check, comparison table, review note `review_notes/Book8_PartNN_review.md`, tracker and checklist updates, commit and push.

## Part checklist
| Part | Coverage | Profiles | Status |
|---|---|---|---|
| 1 | Europe: Sweden, Germany, Netherlands, Ireland, UK, Switzerland | 6 | ✅ (evidence: 1 Medium, 1 Medium-Thin, 1 Thin-Medium, 3 Thin) |
| 2 | North America: USA, Canada | 2 | ⬜ |
| 3 | SEA and Middle East: Singapore, Malaysia, Indonesia, UAE, plus the India baseline and the India comparison and relocation preparation guide | 5 | ⬜ |

## Next step
Part 2: two agents (USA; Canada), one region each because the US is broad (note employer types: big tech, finance, startups, healthcare; do not generalise one segment to the whole market). Part 1 lessons: the checker flags false positives for visa-digit near source tags (review manually); Book 9 is planned and not written, so any reference to it must say so; discard national-character claims; record conflicting CV conventions as disagreements; aim for 8-10 searches per region from different angles. Part 3 afterwards: Singapore, Malaysia, Indonesia, UAE plus the India baseline and the closing India comparison and relocation preparation guide (lead-written, process-level, official-source pointers only).
