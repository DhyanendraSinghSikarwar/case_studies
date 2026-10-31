**Edge cases:**
- First request of a user: no state, treat as a fresh window.
- Window 1: every second is its own window, so each request is a new window and always accepted when limit >= 1.
- Skipping whole windows (t jumps from 3 to 57): the stored index is stale, so reset; no need to "tick" the empty windows.
- Different users are independent.
- Rejected requests do not consume quota, so a client hammering the limiter in one window cannot lock itself out of the next.
- Same second repeated: windows depend on the integer time only.

**Follow-ups:**
- *Distributed version (stated concept only):* store the count under a key like `user:window_index` in a shared store, use an atomic increment, and set an expiry of one window so old keys vanish. Any server that sees the same key sees the same count. Note that this version counts every attempt, including rejected ones, unless you decrement.
- *How do I fix the boundary burst?* Sliding window log (exact, O(limit) memory per user, Q7), sliding window counter (weighted blend of two adjacent windows, approximate, O(1)), or token bucket (Q8).
- *Thread-safety (stated concept only):* the read-compare-increment must be one atomic step, so a lock per user or around the method.

**Common mistakes:**
- Counting rejected requests (a client over the limit stays blocked for no reason).
- Using `t % window` as the window id (that is the offset inside the window).
- Forgetting to reset when the index changes.
- Claiming fixed window is "accurate": it is exact per window but allows up to `2 * limit` across a boundary.
