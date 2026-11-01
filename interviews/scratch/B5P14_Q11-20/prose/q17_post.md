**Edge cases:**
- Empty list: `[[], 0]`.
- Single element: `[[1], 1]`.
- All equal: all ranks 1, distinct 1.
- Negatives and +-10^18: handled by sort (tested).
- Strictly decreasing input: ranks decreasing from n to 1.
- n = 10^5 with random huge values: ranks span exactly 1 to `distinct` (tested).

**Follow-ups:**
- *Where do I use it?* Counting smaller numbers after self and inversions with a Fenwick tree (inversions with a BIT is Q25 in this part; the merge sort version is Part 13 Q17), and any sweep over coordinates.
- *Why `sorted(set(...))` and not `sorted(values)`?* The set removes duplicates first, so the rank table has no gaps. Sorting with duplicates and enumerating would give gaps.
- *Do I need the dict?* No; `bisect_left` on `uniq` avoids it and keeps memory at one list, at O(log n) per lookup instead of O(1).

**Common mistakes:**
- 0-based ranks passed to a Fenwick tree.
- Enumerating the sorted list WITH duplicates, producing gaps.
- Mixing up dense ranking with competition ranking.
- Compressing the queries and the data separately, so the same value gets different ranks (compress them together).
