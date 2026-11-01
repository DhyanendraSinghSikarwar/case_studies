**Edge cases:**
- Exactly 10 seconds apart: allowed (tested).
- 9 seconds apart: refused.
- Same message twice in one second: second refused.
- First message ever, at time 0: allowed (the unseen check is `is None`, not falsy on the time, because 0 is a legal time).
- An empty-string message is still a message.
- A refused message must NOT refresh its time; the buggy version prints once at time 0 and then never again on a steady stream (tested).

**Follow-ups:**
- *Memory bound (stated concept only):* see the complexity section; a deque in arrival order plus the dict, popping while `now - head_time >= 10` and deleting from the dict only if the dict still holds that same time.
- *Compare with the hit counter of Q1:* the same half-open boundary, but the logger keeps one timestamp per message, while the hit counter keeps counts per second in a window.
- *Thread-safety (stated concept only):* check-then-set on `last[m]` must be atomic, or two threads could both print the same message; a lock, or an atomic "set if absent or older" in a shared store.

**Common mistakes:**
- Updating the stored time on a refusal.
- Using `> 10` instead of `>= 10`.
- Using `if not last.get(m)` and mishandling a last time of 0.
- Reading `time.time()` instead of `clock()`.
