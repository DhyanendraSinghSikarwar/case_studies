**Pattern:** Hash map of last PRINT time. The only subtle point is what gets stored when a message is refused: nothing.

**Say this first (1 line):** "I store the time a message was last printed; print again when now minus that is at least 10; a refusal does not touch the stored time."

**Brute force:**
- Keep every print time of every message and compare against the last one. Same answers, unbounded memory. (It is the oracle in the code.)

**Optimal:**
- `last[message]`: time of the last successful print.
- `shouldPrint(m)`: if `m` is unseen, or `now - last[m] >= 10`, set `last[m] = now` and return True. Otherwise return False and leave `last` alone.
- Boundary rule: exactly 10 seconds later is allowed again. This is the same family as the hit counter of Q1, where an item exactly 300 seconds old has already expired: an interval of length L is half-open, so age L means "over".
- Tie rule: two identical messages at the same second: first prints, second is refused (age 0).

**Complexity:**
- O(1) per call (one dict lookup and one compare).
- Memory O(distinct messages seen). For an unbounded stream of distinct messages (stated concept): periodically drop entries older than 10 seconds, or keep a deque of `(time, message)` in arrival order and pop from the left while the head is older than 10 (each entry is dropped once, so O(1) amortised). Dropping an entry older than 10 is safe because the message would be allowed anyway.

**Dry run:** the example.

| t | message | last | now - last | result |
|---|---|---|---|---|
| 1 | foo | none | | True (last = 1) |
| 2 | bar | none | | True (last = 2) |
| 3 | foo | 1 | 2 | False |
| 8 | bar | 2 | 6 | False |
| 10 | foo | 1 | 9 | False |
| 11 | foo | 1 | 10 | True (last = 11) |
| 12 | bar | 2 | 10 | True (last = 12) |
| 21 | foo | 11 | 10 | True |

The "steady stream every 3 seconds" claim: arrivals at 0, 3, 6, 9 are refused after the print at 0; 12 is the first arrival with age >= 10, so it prints; then 15, 18, 21 are refused (ages 3, 6, 9) and 24 prints. Prints at 0, 12, 24 (and 36), as the code confirms.
