**Pattern:** Fixed-window counter. Cut time into equal windows, count accepted requests per user per window, reset when the window index changes. The simplest limiter, and the one with a known boundary weakness.

**Say this first (1 line):** "Window index is `t // window`; I store one pair `[index, accepted]` per user, reset it when the index changes, and only count accepted requests."

**Brute force:**
- Remember every accepted timestamp per user. On each request, count those with the same `t // window`. O(history) per call and unbounded memory.

**Optimal:**
- `state[user] = [k, count]` where `k = t // window`.
- On `allow`: compute `k` from `clock()`. If the user has no state or the stored index differs, reset to `[k, 0]`. If `count < limit`, increment and return True. Else return False without incrementing (rejected requests do not count).
- Boundary rule: window `k` is `[k*window, (k+1)*window)`, so `t = 10` with window 10 is the FIRST second of window 1.
- Tie rule: two requests in the same second are just two requests in the same window; the first ones accepted take the quota.

**Complexity:**
- Time O(1) per call (one dict lookup and integer arithmetic).
- Memory O(1) per user (two integers), O(users) in total. Old users' entries can be dropped when their window index is behind the current one (a sweep every so often).

**Dry run:** limit 2, window 10 (the example).

| t | user | window k | count before | decision |
|---|---|---|---|---|
| 8 | u | 0 | 0 | True (count 1) |
| 9 | u | 0 | 1 | True (count 2) |
| 9 | u | 0 | 2 | False (not counted) |
| 10 | u | 1 | reset to 0 | True (count 1) |
| 11 | u | 1 | 1 | True (count 2) |
| 11 | u | 1 | 2 | False |
| 20 | u | 2 | reset | True |
| 20 | v | 2 | no state | True |

The weakness is visible in rows 1, 2, 4, 5: accepted at t = 8, 9, 10, 11. That is four requests inside four seconds with a limit of 2 per 10 seconds, double the intended rate, because the window boundary at 10 resets the count. The sliding window log of Q7 would accept 8 and 9, and refuse 10 and 11 (the code below shows both). In the worst case a client can send `limit` requests at the end of one window and `limit` at the start of the next, so up to `2 * limit` in a span of two seconds. The token bucket of Q8 smooths this with a burst allowance plus a steady refill.
