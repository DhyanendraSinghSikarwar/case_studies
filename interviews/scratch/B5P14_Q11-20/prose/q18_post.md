**Edge cases:**
- `get` on an index never set: the initial `(0, 0)` pair answers 0.
- Snapshot of an untouched array: id 0, every get returns 0 (tested).
- Setting the same value again in a new epoch still appends a pair; it is harmless (tested), and skipping it when the value equals the last one is an optional saving.
- Two sets of one index before a snapshot keep only the last (tested; pair count printed).
- `bisect_right` (not `bisect_left`): the pair stamped exactly `snap_id` must be included.
- `length = 1` and up to 5*10^4 operations: fine.

**Follow-ups:**
- *Could I store the full array only every k snaps?* Yes, but per-index change lists are simpler and already optimal for sparse updates.
- *Worst case:* every index changes every epoch, so memory is O(length * snaps) anyway; that is inherent to storing the history.
- *Thread-safety (stated concept only):* `set` and `snap` must not interleave in a way that lets a set land in the wrong epoch; a lock around both, or a copy-on-write structure.

**Common mistakes:**
- Copying the array on every `snap`.
- Using `bisect_left` and missing the pair equal to `snap_id`.
- Appending a duplicate pair for the same epoch, so `bisect` finds the older value.
- Returning `snap_id` as `len(snaps)` after incrementing (off by one).
