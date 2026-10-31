**Edge cases:**
- One record: all three queries return that price.
- Correcting the only record (or the current latest timestamp): `current` follows the new price.
- A late (older) timestamp never changes `current`, but it can change `maximum` and `minimum`.
- The same price re-sent for a timestamp: duplicate heap entry, both valid, no bug.
- Correcting a record down and then back to its old price makes the old stale entry valid again. That is correct: validity is checked against the dict, not stored on the entry.
- Heap entries are tuples `(price, ts)`, so equal prices fall back to comparing timestamps (ints, always comparable).

**Follow-ups:**
- *Why not a `SortedList` of prices?* It also works (remove the old price, add the new one, O(log n) with a real balanced structure), but it is not in the standard library; lazy deletion needs only `heapq`.
- *Can the heaps grow without bound?* Yes, if nobody calls `maximum` or `minimum`, stale entries sit there. Rebuild a heap from the dict when it exceeds twice the number of live timestamps (O(n) per rebuild, amortised O(1) per update).
- *Thread-safety (stated concept only):* the dict write and the two pushes must look atomic to readers, so one lock around each method body; the heaps' lazy pops mutate state even inside a "read".
- *Scoring note [Set D, Q1 of 4, 8 min, 15 pts]:* about 4.5 points for stating the rules first (correction replaces, current = latest timestamp not latest call, stale means price differs from the dict), 4.5 for a correct solution that passes the example and a random check, 3 for O(log n) amortised with the "each entry popped once" reason, 1.5 for the edge cases above, 1.5 for a crisp under-60-second summary. Partial credit: a working O(n)-per-query version with correct rules earns most of the first two parts (about 6 of 15), but nothing for the complexity part. How I would pace this: 1.5 minutes to restate rules and pick dict plus two heaps, 4 minutes to code, 1.5 minutes to run the example, 1 minute for complexity and the stale-entry argument.

**Common mistakes:**
- Taking `current` from the last call instead of the largest timestamp.
- Forgetting that a correction leaves the old entry in the heap, then returning a stale maximum.
- Deleting by value when a different timestamp has the same price (check the timestamp's own latest price, not "does this price exist").
- Using `heapq` for the max without negating.
- Popping a valid top entry "to be safe" and so losing a live record.
