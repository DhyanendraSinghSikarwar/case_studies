**Pattern:** Frequency buckets as stacks (O(1) design). Instead of searching for the most frequent element, keep one stack per frequency level, in push order.

**Say this first (1 line):** "A value with count f sits on stacks 1 to f, one entry each; `pop` takes the top of the highest non-empty stack, and that top is exactly the most frequent, most recently pushed value."

**Brute force:**
- Keep the stack as a list. On `pop`, count every value, find the highest count, then scan from the top for the first element with that count and remove it. O(n) per pop.

**Optimal:**
- `count[x]`: how many copies of x are in the stack now.
- `stacks[f]`: values in the order their count REACHED f. `push(x)`: `count[x] += 1`, append x to `stacks[count[x]]`, raise `max_freq` if needed.
- `pop()`: take `x = stacks[max_freq].pop()`, `count[x] -= 1`, and if `stacks[max_freq]` is now empty then `max_freq -= 1`.
- Why one value sits on several stacks: pushing 5 three times puts 5 on stack 1, stack 2 and stack 3. Popping 5 removes it from stack 3 only, so it correctly remains on stacks 1 and 2 as a 2-copy value. The levels peel off from the top, mirroring the order in which the copies were pushed.
- Why this gives exactly the tie rule: the highest non-empty level is the highest frequency. Within that level, the stack order is the order in which values reached that level, and the last one to reach it is the one whose latest push is most recent. That is the topmost occurrence among the tied values (the entry on stack f was placed at the time of the push that made the count f, and a later push of another tied value would have placed that value later on the same stack).
- Invariant: `stacks[f]` is non-empty for every f <= `max_freq`, which is why decreasing `max_freq` by one after a pop is enough.

**Complexity:**
- `push` and `pop`: O(1) average (dict operations and list append/pop).
- Space: O(n), one stack entry per element in the stack (a value with count f has exactly f entries across the stacks).

**Dry run:** the first example.

| push | count | stacks (level: contents) | max_freq |
|---|---|---|---|
| 5 | 5:1 | 1:[5] | 1 |
| 7 | 7:1 | 1:[5,7] | 1 |
| 5 | 5:2 | 1:[5,7] 2:[5] | 2 |
| 7 | 7:2 | 1:[5,7] 2:[5,7] | 2 |
| 4 | 4:1 | 1:[5,7,4] 2:[5,7] | 2 |
| 5 | 5:3 | 1:[5,7,4] 2:[5,7] 3:[5] | 3 |

| pop | step | result |
|---|---|---|
| 1 | top of level 3 is 5; level 3 empties, max_freq = 2; count 5 = 2 | 5 |
| 2 | level 2 is [5,7]: top is 7 (7 reached count 2 after 5 did); count 7 = 1 | 7 |
| 3 | level 2 is [5]: top is 5; level 2 empties, max_freq = 1; count 5 = 1 | 5 |
| 4 | level 1 is [5,7,4]: top is 4 | 4 |

Outputs: 5, 7, 5, 4.
