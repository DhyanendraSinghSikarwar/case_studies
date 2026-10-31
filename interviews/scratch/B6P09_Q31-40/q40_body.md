**Say this first (1 line):** About 24,000 of the 60,000 zero-result searches a day are spelling or synonym problems and about 12,000 are products the catalogue lacks (projections from a 500-search review); I would build spelling and synonym handling first because it is the largest fixable group, measure it with an A/B test on those searches, and give sellers an aggregated, privacy-safe demand report for the missing products.

**Clarifying questions:**
- Were the 500 searches sampled at random from the 60,000 searches, or from distinct queries? Sampling searches weights head queries correctly; sampling queries does not.
- What are the other 200 (40%): filters too narrow, out of stock, ambiguous, junk? That group is as large as the spelling group and may be cheap to fix.
- How does the current search handle typos and synonyms (any correction, stemming, a synonym list)? It sets how much is new.
- Can a search that returns results still be bad? Fixing zero results should not just replace "no results" with irrelevant results.
- Which sellers can add listings, and is there a policy team for restricted items? It shapes what we can pass on.

**Approach:**
1. Projections: 6% x 1,000,000 = 60,000 zero-result searches. Spelling or synonym: 200 / 500 = 40% x 60,000 = 24,000 a day (95% range about 21,400 to 26,600). Genuinely missing: 100 / 500 = 20% x 60,000 = 12,000 a day (range about 9,900 to 14,100). Other: 40% = 24,000.
2. Build first: query understanding for spelling and synonyms. Start from logs: zero-result queries that users reformulate within the session into a query with clicks give pairs (typo to fixed query, trainers to sneakers). Combine with a vocabulary-based corrector. In a small test, string similarity fixed "runing shoes", "wireles headphones" and "fone charger" but could not fix "kettlebell" (missing) or "trainers" (a synonym), so synonyms need a separate dictionary or learned model.
3. Roll out safely: auto-correct only above a confidence threshold, otherwise show "did you mean"; always keep the user's original query visible.
4. Size the benefit: fixing half the spelling group puts 12,000 searches a day back to having results and lowers the zero-result rate from 6.0% to 4.8%; fixing 80% gives 4.08%.
5. Measure with an A/B test on searches that would have returned zero results: randomise users, compare search-to-click, add-to-cart and orders per search, revenue per search. Zero-result rate alone is a vanity metric because a correction that returns junk lowers it too.
6. Guardrails: relevance judged by a labelled sample of corrected searches (wrong correction rate), reformulation rate, latency, and bounce or exit rate.
7. Missing-product signal for sellers: normalise and cluster the 12,000-a-day group by intent, publish only terms searched by at least K distinct users (K = 20 in my toy example, which kept three terms and dropped a one-user term that looked like a person's name), exclude personal or sensitive queries and prohibited items, and verify the product is truly missing (not out of stock or mis-categorised).
8. Present to sellers as weekly demand gaps: term cluster, searches per day, trend, and the category. Check with the trust and policy team and legal or privacy about what can be shown to sellers. Measure the effect by gaps filled and sales on newly listed items.

**Metrics:**
- Zero-result rate = searches with no results / all searches (6%).
- Recovered searches = zero-result searches that now return results and get a click / zero-result searches.
- Search-to-click rate and orders per search on the treated group; revenue per search.
- Wrong-correction rate = corrections judged irrelevant / corrections shown.
- Seller side: gaps published, gaps filled, sales on filled gaps.

**Risks:**
- Auto-correcting a rare, correct word into a common one (a brand name) hurts users.
- Sampling searches versus queries changes the shares.
- The missing-product group may include illegal, restricted or irrelevant demand.
- Small counts in seller reports can expose individual users.
- 500 reviewed searches are a sample; ranges are about +/- 4 points.

**What the interviewer scores:**
- Strong: 24,000 and 12,000, labelled projections, and notices the other 24,000.
- Strong: builds query understanding first, with confidence thresholds and an A/B test on the affected searches.
- Strong: measures revenue or conversion, not only the zero-result rate; privacy threshold for the seller report.
- Weak: "build a bigger index"; "reduce the zero-result rate" as the only goal.

**Example:** Illustrative numbers from the run. 60,000 zero-result searches; 24,000 spelling or synonym, 12,000 missing, 24,000 other. Fixing half the spelling group moves the zero-result rate from 6.0% to 4.8%.
- Weak: "We should add more products so people find results."
- Strong: "About 24,000 a day are typos or synonyms and 12,000 are real catalogue gaps, so I would build spelling and synonym handling first, with a confidence threshold, and A/B test on those searches measuring orders per search. For the 12,000 I would send sellers a weekly list of terms searched by at least 20 users, after the policy team checks the list."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Why not use a language model for every query?* It may help synonyms, but latency, cost and wrong corrections need an A/B test; start with logs and a dictionary.
- *How do you handle the 40% other?* Sample and classify them; filters and stock issues may need product changes rather than ML.
- *What if sellers game the demand report?* Use distinct users, a minimum history and a review step.

**Common mistakes:**
- Reporting shares from 500 searches as exact.
- Celebrating a lower zero-result rate without checking relevance.
- Publishing rare queries.
- Treating missing products and typos as the same problem.
