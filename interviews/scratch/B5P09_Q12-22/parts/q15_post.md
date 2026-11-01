**Edge cases:**
- `end` not in `word_list`: 0 (even if reachable in the abstract).
- `begin` is not required to be in the list; it is only the start.
- No path: BFS ends with an empty queue, return 0.
- `begin == end`: the prompt does not say. All my methods return 1 when `end` is in the list (a one-word sequence). A checker that expects something else would need that stated.
- L = 1: every pair of different one-letter words is a neighbour.
- Duplicates are excluded by the prompt (distinct words), but a `set` handles them anyway.

**Follow-ups:**
- Print the actual ladder? Store a parent pointer per word and walk back from `end`.
- Faster for huge lists? Bidirectional BFS: expand the smaller frontier each step; roughly cuts the work from b^d to 2 * b^(d/2).
- All shortest ladders (Word Ladder II)? BFS to get levels, then DFS or backtracking over parents; the number of answers can be exponential.

**Common mistakes:**
- Counting edges instead of words (off by one: the answer counts both ends).
- Comparing all pairs; times out.
- Marking visited on dequeue, so the same word is queued many times.
- Using a list for `word_list` membership (O(N) per test); convert to a set.
- Forgetting to check that `end` is in the list.
