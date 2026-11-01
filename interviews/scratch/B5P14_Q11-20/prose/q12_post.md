**Edge cases:**
- A key is alive at T + ttl - 1 and gone at T + ttl (tested).
- `get` right before expiry does not extend life (tested).
- Re-`put` of a key restarts life from now and replaces value and ttl (tested).
- Capacity 1: every new key evicts the previous one.
- A put when every entry is expired: purge empties the cache first, nothing is evicted.
- Stale heap entries (replaced or evicted keys) must be ignored on pop, otherwise the new entry for the same key would be deleted early. That is why `version` exists.
- Same timestamp for many calls (non-decreasing, not strictly increasing) works because nothing depends on distinct times.

**Follow-ups:**
- *Why `version` and not just the key?* After `put(k)` twice, the heap holds two entries for `k`. The old one fires first (if its ttl was shorter) and must not delete the new value.
- *Thread-safety (stated concept only):* a single lock around the whole body of `put`, `get` and `size`. The purge, the capacity check and the insert must happen as one step, and even `get` mutates recency order and the heap, so there are no read-only methods.
- *Could a background thread do the purging?* It could free memory sooner, but correctness must not depend on it: every call still purges lazily, so results are identical with or without the thread.
- *Scoring note [Set A, Q4 of 5, 12 min, 25 pts]:* 7.5 points for stating the rules (expiry boundary, purge before evict, get does not extend life, put-replace restarts life), 7.5 for a correct solution that passes the example and a random timed check against the naive version, 5 for O(log n) amortised and why each entry is popped once, 2.5 for edge cases, 2.5 for a crisp spoken summary. Partial credit: a correct list-based O(n) version gets about 12 of 25; a correct LRU with no expiry handled gets about 8. How I would pace this: 2 minutes for rules, 3 minutes to sketch OrderedDict plus heap and the version trick, 5 minutes to code, 2 minutes to run the example and test.

**Common mistakes:**
- Evicting the LRU key before purging expired ones.
- Treating the expiry as inclusive (`now <= T + ttl`) instead of `now < T + ttl`.
- Letting `get` refresh the expiry.
- Deleting by key alone from stale heap entries, killing a freshly replaced value.
- Reading `time.time()` inside the class instead of `clock()`.
- `size()` returning `len(od)` without purging.
