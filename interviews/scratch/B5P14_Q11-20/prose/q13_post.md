**Edge cases:**
- All values distinct: every element has frequency 1, so it behaves as a normal LIFO stack.
- One value repeated: pops return it every time and `max_freq` drops 3, 2, 1, 0.
- Tie at the top frequency (1,1,2,2): the value pushed last pops first (2), then the other (1), then the same again.
- Pushing, popping to empty, then pushing again: `max_freq` returns to 0 and then grows again correctly.
- `pop` is never called on an empty stack (stated by the prompt), so no error handling is needed.

**Follow-ups:**
- *Relation to earlier designs:* the min stack (Part 4 Q2) keeps a parallel stack of minimums and the max stack (Part 4 Q38) needs lazy deletion or a linked list for `popMax`; here the bucket-per-frequency idea gives O(1) with no heap. Top-k frequencies by counting is Part 1 Q10.
- *What if `pop` had to remove the least frequent element?* Keep a `min_freq` too; but then raising it after a pop is harder (levels can become empty in the middle), so a doubly linked list of levels is needed (the same idea as the all-O(1) data structure).
- *Thread-safety (stated concept only):* `push` and `pop` each touch `count`, a stack and `max_freq`, so a lock around each method makes them atomic; without it a pop could see a `max_freq` that no longer matches the stacks.
- *Scoring note [Set D, Q3 of 4, 13 min, 30 pts]:* 9 points for stating the tie rule and an example before coding, 9 for a correct O(1) solution that passes the example and a random check, 6 for the complexity and the "value on several stacks" explanation, 3 for edge cases, 3 for a crisp summary. Partial credit: a correct O(n)-per-pop scan solution earns about 12 of 30; a heap of (-freq, -time, value) with lazy deletion gets about 20 (it is O(log n) and correct, only not O(1)). How I would pace this: 2 minutes for rules and an example, 3 minutes to find the per-frequency stacks, 5 minutes to code, 3 minutes to test and explain.

**Common mistakes:**
- Using one stack per VALUE instead of per frequency, losing the global push order.
- Removing the value from every level on pop instead of only the top level.
- Forgetting to lower `max_freq` when its stack empties (the next pop hits an empty list).
- Pushing the value only on stack `count` but pulling `count` from the stale value after a pop (update `count` on every pop).
- Breaking ties by smallest value or by insertion order of first appearance instead of the most recent push.
