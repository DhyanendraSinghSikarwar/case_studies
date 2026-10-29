**Pattern:** Coordinate compression. Replace big or sparse values by their order-preserving small ranks, so array-indexed structures (Fenwick tree, counting array) can be used.

**Say this first (1 line):** "Sort the distinct values once, give them ranks 1, 2, 3, and look each element up: O(n log n)."

**Brute force:**
- For each value, count how many distinct values are smaller and add 1. O(n^2). It is the oracle in the code.

**Optimal:**
- `uniq = sorted(set(values))`: O(n log n).
- `rank = {v: i + 1}`: the dict maps each value to its 1-based dense rank. Or use `bisect_left(uniq, v) + 1` (no dict, O(log n) per lookup; same answer).
- Return `[[rank[v] for v in values], len(uniq)]`.
- Dense rank means equal values share a rank, the smallest is 1 and there are no gaps; the largest rank equals `distinct`.
- Why Fenwick trees and counting arrays need this: they index by position, and a value like 10^18 cannot be an array index. Ranks keep the index range at most n.
- Why start at 1: a Fenwick tree is 1-indexed. Index 0 is unused (the update loop `i += i & -i` would never leave 0 and the query loop would not stop correctly).
- Difference from competition ranking ("1224"): there, ties share the first position and the next rank skips numbers, so the largest rank can exceed `distinct`. Dense ranking gives "1223".

**Complexity:**
- Time O(n log n) for the sort; building the dict and mapping is O(n). `bisect_left` version: O(n log n) for lookups too.
- Space O(n).
- Python integers have no overflow, so 10^18 is no problem, and sorting compares them exactly.

**Dry run:** `values = [40, -5, 40, 7]`.
- `set` gives {40, -5, 7}; sorted: `[-5, 7, 40]`.
- Ranks: -5 -> 1, 7 -> 2, 40 -> 3.
- Map the input: 40 -> 3, -5 -> 1, 40 -> 3, 7 -> 2. Result `[[3, 1, 3, 2], 3]`.
