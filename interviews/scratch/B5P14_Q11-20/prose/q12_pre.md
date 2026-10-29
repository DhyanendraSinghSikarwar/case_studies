**Pattern:** LRU recency (OrderedDict) plus expiry (min-heap of expiry times with lazy deletion, Part 8 Q31). Two different orders on the same keys: "least recently used" and "expires soonest". One structure each.

**Say this first (1 line):** "Rules first: alive while now < T + ttl, so expiry at exactly T + ttl; purge every expired entry before I look at capacity; a get refreshes recency but never life."

**Brute force:**
- A list of `[key, value, expiry]` in recency order. On every call filter out expired entries (O(n)), then find or insert (O(n)).
- O(n) per operation, n <= 1000 here so it passes, but it is the oracle, not the answer.

**Optimal:**
- `od`: OrderedDict key -> (value, version), oldest first, so the left end is the LRU key.
- `heap`: entries `(expiry, key, version)`. `version` increases on every `put`, so an entry for an overwritten key is recognised as stale (the stored version no longer matches).
- `_purge()`: while the heap top has `expiry <= now`, pop it. If that key is still in `od` with the same version, delete it. Otherwise the entry was stale (key replaced or already evicted): ignore it. "`<=`" is the exactly-at-expiry rule.
- `put(key, value, ttl)`: purge; then if the key exists, remove it (it will be reinserted fresh, so new value, new ttl, new expiry, most recent); else if `len(od) == capacity`, `popitem(last=False)` evicts the LRU live key; then insert at the right end and push `(now + ttl, key, version)`.
- `get(key)`: purge; if absent return -1; else `move_to_end` and return the value. The heap is untouched, so life is not extended.
- `size()`: purge, then `len(od)`.
- Tie rules: LRU order is the only tie-break for eviction (an entry is never evicted because it is "nearly expired"; only expired entries disappear for that reason). Two entries with the same expiry are both purged in one pass; the heap's secondary comparison on `key` only matters for ordering inside the heap, and the unique `version` stops comparisons ever reaching the value (keys must be comparable with each other, true for the strings and ints used here).
- Why purge first: if an expired entry is still in `od` while the cache is at capacity, the LRU victim could be a live key even though a dead entry was holding the slot. The cache would shrink its live content for nothing.

**Complexity:**
- Each call: O(log n) amortised. Every heap entry is pushed once and popped at most once, so total purge pops <= total puts.
- OrderedDict `move_to_end`, `popitem`, delete and insert are O(1).
- Space: O(capacity) live keys, plus stale heap entries that wait until their expiry time passes; at most one per `put`, so O(puts in the last max-ttl seconds).

**Dry run:** the first example, capacity 2. Notation: `od` is listed LRU first.

| time | call | purge | od after | returns |
|---|---|---|---|---|
| 0 | put a=1 ttl 10 | nothing | a (exp 10) | None |
| 1 | put b=2 ttl 3 | nothing | a, b (exp 4) | None |
| 2 | get a | nothing | b, a | 1 |
| 3 | put c=3 ttl 10 | nothing (b expires at 4) | full, evict LRU b: a, c (exp 13) | None |
| 3 | get b | nothing | a, c | -1 |
| 4 | size | pop (4, b): b not in od, ignore | a, c | 2 |
| 10 | get a | pop (10, a): delete a | c | -1 |
| 10 | size | | c | 1 |
| 11 | put c=9 ttl 5 | nothing | c replaced, exp 16 | None |
| 15 | get c | nothing (16 > 15) | c | 9 |
| 16 | get c | pop (16, c): delete | empty | -1 |
