**Pattern:** Hash map plus two heaps with lazy deletion. The data changes (a correction replaces an old price), and a heap cannot delete from the middle. So I leave stale entries in the heap and throw them away only when they reach the top (Part 8 Q31; the changing-priority idea is Part 8 Q38).

**Say this first (1 line):** "A dict holds each timestamp's latest price; a min-heap and a max-heap hold every (price, timestamp) ever pushed, and I discard a top entry only when the dict says it is stale."

**Brute force:**
- Keep the dict. `current` = price at `max(dict)`, `maximum` = `max(dict.values())`, `minimum` = `min(dict.values())`.
- Every query rescans, so O(n) per call. With 10^5 queries on 10^5 records that is about 10^10 steps.

**Optimal:**
- `price`: timestamp -> latest price. `latest`: the largest timestamp seen (one integer, updated in `update`). `current()` is `price[latest]`, O(1).
- `update(ts, p)`: set `price[ts] = p`, push `(p, ts)` on the min-heap and `(-p, ts)` on the max-heap. O(log n).
- `maximum()`: look at the max-heap top. If `price[ts]` differs from that entry's price, the record was corrected after it was pushed, so pop it and look again. The first top that matches is the answer.
- `minimum()` is the same on the min-heap.
- Tie rule: equal prices on different timestamps give equal heap keys, and that is fine, because only the price is returned. If the same price is re-sent for a timestamp, two identical entries exist and both are valid; the later one is simply a duplicate.
- Invariant: for every timestamp, the entry holding its current price is in both heaps, so a matching top is always the true extreme.

**Complexity:**
- `update`: O(log n) (two pushes). `current`: O(1).
- `maximum` / `minimum`: O(log n) amortised. Every call does one comparison that succeeds, plus some pops.
- Why amortised: each entry is pushed once and popped at most once, and an entry is popped only when it is stale. Total pops <= total pushes = 2 * updates. So the pop work over any sequence of m calls is O(m log m) in total, which averages to O(log n) per call.
- Space: O(updates), not O(distinct timestamps), because stale entries wait in the heaps until they reach the top.

**Dry run:** the first example.

| call | dict (ts: price) | what happens | returns |
|---|---|---|---|
| update(1, 10) | {1:10} | latest = 1 | None |
| update(2, 5) | {1:10, 2:5} | latest = 2 | None |
| current() | | price[2] | 5 |
| maximum() | | max-heap top (-10, 1): price[1] = 10 matches | 10 |
| update(1, 3) | {1:3, 2:5} | push (3,1) and (-3,1); latest stays 2 | None |
| maximum() | | top (-10, 1) is stale (price[1] = 3): pop; next top (-5, 2) matches | 5 |
| update(4, 2) | {1:3, 2:5, 4:2} | latest = 4 | None |
| minimum() | | min-heap top (2, 4) matches | 2 |
| current() | | price[4] | 2 |
| update(4, 20) | {1:3, 2:5, 4:20} | corrects ts 4 | None |
| maximum() | | top (-20, 4) matches | 20 |
| minimum() | | top (2, 4) is stale: pop; next (3, 1) matches | 3 |
