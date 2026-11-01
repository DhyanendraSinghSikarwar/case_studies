**Say this first (1 line):** 400 kilobits a second for 3 seconds is 1,200 kilobits = 150 kilobytes, but that is a ceiling with zero overhead, so I would budget about 50 to 75 kB for the first screen, send ranked ids and small text first, and fetch images lazily.

**Clarifying questions:**
- Is "about 400 kilobits per second" the median or a low percentile? If it is the median, half of sessions are slower, so I design for a lower percentile.
- Does "load in 3 seconds" mean first usable content or everything? I would define it as the first screen of ranked items.
- What is cached on the device (app shell, previous feed)? Cached content does not count against the payload.
- Which features need fresh data (price, stock) versus can be a few hours old? It decides what to precompute.
- What share of sessions are new users with no history? They need a non-personalised fallback.

**Approach:**
1. Clarify and frame. Goal: a personalised first screen that is usable in 3 seconds on a slow link. Constraint first: payload ceiling 150 kB, realistic budget 50 to 75 kB.
2. Metrics and guardrails. Time to first usable screen (p75 and p90 on slow links), click and add-to-cart rate, bounce rate, bytes per session. Guardrail: no loss in conversion on fast links.
3. Data and labels. Click, add-to-cart and purchase logs, with network type and bandwidth recorded, so slow-link users can be evaluated separately. Labels from slow users are biased (they see fewer items), so I would check exposure.
4. Baseline first. A popularity-by-city feed cached on the device, then a lightly personalised re-order of the cached list. Measure load time and conversion.
5. Model and trade-offs. Rank on the server with a small model; send only ids, short text and tiny thumbnails; compress with gzip or similar; use a smaller image format and low-resolution placeholders; page the feed 6 items at a time. The trade-off is richness versus speed: each extra 10 kB costs 0.2 s at 400 kbps (see the code). Optionally rank on-device from cached candidates to avoid a round trip.
6. Evaluation. Offline ranking metrics as usual, plus byte and latency accounting per response. Online: A/B test with analysis split by connection speed.
7. Launch and experiment plan. Ship the byte-budgeted feed to slow-link sessions first, since they gain most; then everyone if fast-link conversion holds.
8. Monitoring, retraining and risks. Monitor payload size per response (alert on regressions in CI and in production), time to first screen by network class, conversion by network class.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 10, 7, 5, 5.

**Metrics:**
- Payload ceiling (kB) = bit rate (kbit/s) x seconds / 8 = 400 x 3 / 8 = 150 kB, with 1 kB = 1,000 bytes and no overhead.
- Time to first usable screen = time from tap to first ranked items visible; report p75 and p90 by network class.
- Bytes per session; conversion rate = orders / sessions, by network class.
- Guardrails: fast-link conversion, error rate, stale price or stock complaints.

**Risks:**
- The 150 kB is an upper bound; handshakes, retries and slower phases shrink it (1 second of overhead leaves 100 kB; half the rate leaves 75 kB).
- Averages hide slow tails; many users are slower than the 400 kbps figure.
- Heavy personalisation features can bloat payloads silently.
- Stale cached data (prices, stock) shown as current.
- Collecting device and network data: ask compliance and legal about consent and privacy.

**What the interviewer scores:**
- Strong: 150 kB as a ceiling, then a smaller realistic budget and a plan to hit it.
- Strong: ids first, lazy images, caching, paging, on-device re-ranking.
- Strong: evaluates by network class, not only overall.
- Weak: computes 150 kB and then designs a rich, image-heavy feed anyway.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Use a deep model to personalise and send 40 big product images."
- Strong: "400 kilobits for 3 seconds is 150 kilobytes at most. After connection overhead and slower moments I would budget 60 to 75 kB: ranked ids, short compressed text and small thumbnails for the first 6 items, the rest loaded as the user scrolls. I would test it against the current feed and read conversion separately for slow connections."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Would you rank on the device? For re-ranking a cached candidate list, yes: no round trip and small model; keep the heavy model on the server for the candidate list.
- How do you test improvements for slow users? Randomise by user, record network class at session start, and report the effect within the slow class, with enough users in that class.
- What would you cut first? Images above the fold are largest; shrink or delay them before cutting text signals.

**Common mistakes:**
- Mixing bits and bytes (dividing by 8 is the whole step).
- Treating 150 kB as the budget rather than the ceiling.
- Measuring only on office wifi.
- Reporting averages instead of slow-link percentiles.
