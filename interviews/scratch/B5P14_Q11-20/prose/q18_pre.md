**Pattern:** Persistent per-index history plus binary search. Do not copy the array on `snap`; record only the changes, tagged with the epoch, and binary search the epoch at query time.

**Say this first (1 line):** "For each index I keep a sorted list of (snap id, value) pairs written only when it is set, and `get` is a `bisect_right` on the snap ids."

**Brute force:**
- `snap` copies the whole array, `get` reads `snaps[snap_id][index]`. `snap` costs O(length), so 5*10^4 snaps on a 5*10^4 array is 2.5*10^9 stored integers. Too much memory and time.

**Optimal:**
- `sid`: the id the NEXT `snap()` will return (the current epoch, starting at 0).
- Per index two parallel lists, `ids[i]` (epochs) and `vals[i]` (values), starting with the pair `(0, 0)`.
- `set(i, v)`: if the last epoch recorded for `i` equals `sid`, overwrite the last value (set twice before a snapshot); otherwise append `(sid, v)`.
- `snap()`: `sid += 1`, return the old `sid`. O(1), nothing copied.
- `get(i, s)`: `bisect_right(ids[i], s) - 1` is the last pair with epoch <= `s`; return its value. The initial pair guarantees the position is >= 0.
- Why that pair is right: a pair stamped epoch e means "set during epoch e", i.e. before snapshot e was taken (snapshot e freezes everything written in epochs 0..e). So the value at snapshot s is the newest write with epoch <= s.

**Complexity:**
- `set` O(1), `snap` O(1), `get` O(log k) where k is the number of recorded epochs for that index.
- Space O(length + number of sets), not O(length * snaps).

**Dry run:** first example, `length = 3`. `sid` starts 0; `ids[0] = [0]`, `vals[0] = [0]` etc.

| call | action | returns |
|---|---|---|
| set(0, 5) | last epoch of index 0 is 0 = sid: overwrite: vals[0] = [5] | None |
| snap() | sid becomes 1 | 0 |
| set(0, 6) | last epoch 0 != 1: append: ids [0,1], vals [5,6] | None |
| get(0, 0) | bisect_right([0,1], 0) = 1, pair 0: 5 | 5 |
| set(1, 9) | append (1, 9): ids[1] = [0,1], vals [0,9] | None |
| set(1, 8) | same epoch: overwrite: vals [0,8] | None |
| snap() | sid becomes 2 | 1 |
| get(1, 0) | bisect_right([0,1], 0) = 1, pair 0: 0 | 0 |
| get(1, 1) | bisect_right([0,1], 1) = 2, pair 1: 8 | 8 |
| get(0, 1) | bisect_right([0,1], 1) = 2, pair 1: 6 | 6 |
| get(2, 1) | ids[2] = [0], bisect_right = 1, pair 0: 0 | 0 |
