**Pattern:** BFS on an implicit, unweighted graph. Words are nodes, two words are linked if they differ in exactly one letter. Shortest path in edges plus 1 equals the word count.

**Say this first (1 line):** "BFS from `begin`, generating neighbours by changing one letter at a time, with a visited set; the first time I pop `end` I have the shortest ladder."

**Brute force:** Build the whole graph by comparing every pair of words (L letters each): O(N^2 * L) = 5000^2 * 10 / 2 = about 1.25 * 10^8 character comparisons, then BFS. It works and is my checker, but it is too slow for the upper bound in Python.

**Optimal:** Two ways to get neighbours without comparing all pairs.
- Letters: for each position try the 26 letters, keep candidates that are in the word set. Cost per word: L * 26 string builds, each O(L) to build and hash, so O(26 * L^2) per word. Total O(N * 26 * L^2) = 5000 * 26 * 100 = 1.3 * 10^7.
- Buckets: map `h*t`-style patterns to the words that match. A word has L patterns; neighbours are the words in its L buckets. Build cost O(N * L^2) (L patterns of length L), BFS cost O(sum of bucket sizes touched) with no factor 26. Worst case a bucket is large, but each word is enqueued once, and each bucket is scanned once per word that contains that pattern.
- BFS invariant: nodes are dequeued in order of distance, so the first time `end` comes out its depth is minimal. Mark visited when enqueuing so nothing is queued twice.
- Return 0 at once when `end` is not in the list.

**Complexity:**
- Letters: O(N * 26 * L^2) time, O(N * L) space.
- Buckets: O(N * L^2) time to build and to search (a bucket of size B visited from each of its members costs B per member in the worst case, but the visited check keeps the queue at N), O(N * L^2) space for the pattern strings.
- All pairs: O(N^2 * L) time. For N = 5000 and L = 10 it is the slowest by far.

**Dry run:** `hit -> cog`, list `hot dot dog lot log cog`.
- Level 1: hit. Neighbours in the list: hot (hit -> hot).
- Level 2: hot. Neighbours: dot, lot. Level 3: dot -> dog; lot -> log. Level 4: dog -> cog; log -> cog (cog already queued).
- Pop cog at depth 5: hit, hot, dot, dog, cog. Answer 5.
