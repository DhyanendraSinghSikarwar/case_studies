**Edge cases:**
- `union(x, x)` is False (already together) and does not change counts.
- `connected(x, x)` is always True.
- n = 1, empty `ops`: largest set is 1, set count is n.
- Many repeated unions of the same pair: only the first returns True.
- Do not mutate sizes on `connected`.

**Follow-ups:**
- Union by rank instead of size? Same bound; size is handy when the question asks for component sizes.
- Path halving (`p[x] = p[p[x]]`) is a one-pass alternative with the same amortised bound.
- Need to undo unions (offline dynamic connectivity)? Drop path compression, keep union by size and a rollback stack, each find is O(log n).

**Common mistakes:**
- A recursive `find` on a chain: RecursionError at depth 1000.
- Comparing nodes instead of roots when deciding union size or equality.
- Reading `size[x]` for a non-root `x` when computing the largest set (use `size[find(x)]`).
- Forgetting to decrement the set count only on a real merge.
- Adding sizes after swapping the roots in the wrong order.
