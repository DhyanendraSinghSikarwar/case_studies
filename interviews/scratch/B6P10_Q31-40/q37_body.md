**Say this first (1 line):** 4,000 searches a second at 3 requests each is 12,000 suggestion calls a second, and at 2,500 per instance run at 60% I need 12,000 / 1,500 = 8 instances.

**Clarifying questions:**
- Is the 4,000 searches per second the peak for the whole app or per region? It sets the number to size to.
- Is the 3 requests per search measured, and does it include debouncing? Typing behaviour changes it a lot.
- Is the 2,500 per second per instance measured at the 50 ms p99 budget? Throughput without a latency condition is meaningless.
- What query mix: Hinglish in Latin script, native scripts, and mixed? It drives normalisation and the index.
- How fresh must trending and new product terms be? It sets the rebuild cadence.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 6, baseline 5, model 8, evaluation 7, launch 5, monitoring and cost 5):**
1. Clarify and frame: a very low latency suggestion service, with a ranking quality bar.
2. Metrics and guardrails: suggestion acceptance (clicks on a suggestion / sessions with suggestions shown), keystrokes saved, p99 latency, zero-result rate per language.
3. Data and labels: query logs, clicked suggestions, product titles; transliteration variants map Hinglish spellings to one form.
4. Baseline first: a prefix trie ranked by popularity per language, with a spelling-variant table. It is fast and is hard to beat on latency.
5. Model and trade-offs: add a light reranker on personal and recent signals only for the top candidates; keep the heavy model offline. Sizing: 12,000 per second; one instance at 60% gives 1,500; 8 instances; with one down, 7 instances run at 68.6%, so I would plan 9. A prefix cache with a 30% hit rate drops backend load to 8,400 per second, 6 instances; with 50% hits, 4 (cache hit rates are assumptions to measure). Budget for 50 ms p99, illustrative split: 10 network, 5 normalise, 15 retrieve, 15 rank, 5 slack.
6. Evaluation: offline mean reciprocal rank on logged completions per language; then an A/B on search success and time to first result.
7. Launch: one language group at a time, with the old autocomplete as fallback; client debouncing so requests per search falls.
8. Monitoring and cost: p99 and error rate per region, quality per language (small languages get their own dashboard), index refresh age.

**Metrics:**
- Acceptance rate = searches where a suggestion was selected / searches where suggestions were shown, per language.
- Suggestion requests per second = searches per second x requests per search (12,000 here).
- Guardrails: p99 latency at most 50 ms, zero-result rate, offensive-suggestion reports.

**Risks:**
- Average quality hides small languages; report per language.
- Offensive or sensitive suggestions from raw logs; filter and review (ask the policy team).
- Typing bursts exceed the 3 average; peak per second may be higher.
- Transliteration errors send Hinglish users to empty results.

**What the interviewer scores:**
- Strong: 12,000, 1,500, 8, plus N+1 and a latency condition on the throughput.
- Strong: trie baseline first, rerank only a few candidates, per-language measurement.
- Weak: a large neural model on the hot path; sizing at 100% utilisation.

**Example:** Illustrative numbers. 4,000 x 3 = 12,000; 2,500 x 0.6 = 1,500; 12,000 / 1,500 = 8.
- Weak: "Use a transformer to generate completions for every keystroke."
- Strong: "That is 12,000 calls a second and 8 instances at 60% load. I would serve a trie per language with transliteration variants, rerank the top 20 with a light model, and cut load with debouncing and a prefix cache, then check the cache hit rate before shrinking the fleet."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if requests per search is really 4?* 16,000 per second, 11 instances (10.67 rounded up).
- *Why 60% utilisation?* Headroom for bursts and for one node loss while holding the p99; the number should come from a load test.

**Common mistakes:** Forgetting the 3x multiplier. Using 100% utilisation. One quality number for all 8 languages. Putting the heavy model on the hot path.
