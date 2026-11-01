**Pattern:** Interval DP, concept level. State is a substring i..j; the transition either prints the last letter separately, or lets the print of that letter be shared with an equal letter earlier in the range.

**Say this first (1 line):** "Merge equal neighbours first, then `dp[i][j]` is the fewest turns for t[i..j]: either `dp[i][j-1] + 1` (print t[j] alone) or, for each k with t[k] == t[j], print t[k] and t[j] with one wide stroke: `dp[i][k] + dp[k+1][j-1]`; O(n^3)."

**Brute force:** Breadth-first search over strip states: start from all blanks, each move overwrites any range with one letter, stop when the strip equals `s`. The number of states grows like 4^n for the alphabet a-c (4 symbols with the blank), each with up to n(n+1)/2 * 3 moves. It is the oracle for len <= 6 over a, b, c.

**Optimal:**
- Collapse first: `aaabbb` is the same job as `ab`, because one stroke can cover a whole run of equal letters at no extra cost. The code checks that the DP gives the same answers with and without the collapse for all 255 strings up to length 7 over {a, b}; collapsing just shrinks n.
- State: `dp[i][j]` = minimum turns to print `t[i..j]` onto a blank strip (t is the collapsed string).
- Base: `dp[i][i] = 1`; an empty string needs 0 turns.
- Transition: first candidate `dp[i][j-1] + 1`: print the first j - i letters, then one more stroke for t[j]. Second candidate for every k in [i, j) with `t[k] == t[j]`: print t[j] with the same stroke as t[k]. That stroke is laid down while printing `t[i..k]` (so cost `dp[i][k]`, the stroke simply extends to column j) and then everything between, `t[k+1..j-1]`, is printed on top afterwards (cost `dp[k+1][j-1]`, 0 if that range is empty). Take the minimum.
- Why the answer needs only "the first letter can be printed across a wider range": in an optimal plan, the stroke that paints the leftmost position can be extended to the right, to cover another equal letter, without ever hurting, because every later stroke over that range overwrites it anyway. So, the leftmost letter is either printed alone or together with an equal letter; the code's DP states the mirror form (last letter t[j]), which is the same argument read right to left. An exchange argument, checked rather than proved here: the DP equals the BFS for all 364 strings of length <= 5 over a, b, c and 60 random strings of length 6.
- Wrong version: only splitting into two independent parts (`dp[i][k] + dp[k+1][j]`) never shares a stroke, so `aba` costs 3 instead of 2; it is wrong on 864 strings of length <= 6 in the code.
- Memoised version: `f(i, j)` with `lru_cache`, depth <= n <= 100 (each call shrinks the range), so there is no recursion-limit problem at this size; bottom-up is shown as the main solution.
- Space: `dp` reads cells inside `[i, j]` for the same i and larger i, so the full triangle is kept: O(n^2).

**Complexity:** Time O(n^3): n^2/2 cells, each scanning up to n values of k (at n = 100 that is about 166,000 inner steps). Space O(n^2). The code's random 26-letter string of length 100 runs in a blink (sandbox only).

**Dry run:**
- `aaabbb` collapses to `ab`: `dp[0][0] = 1`, `dp[1][1] = 1`, `dp[0][1] = dp[0][0] + 1 = 2` (the letters differ, so no sharing). Answer 2.
- `aba`, the interesting one (upper triangle, rows i):

| i \ j | 0 (a) | 1 (b) | 2 (a) |
|---|---|---|---|
| 0 (a) | 1 | 2 | 2 |
| 1 (b) |  | 1 | 2 |
| 2 (a) |  |  | 1 |

`dp[0][2]`: candidate one is `dp[0][1] + 1 = 3`. Candidate two uses k = 0 (t[0] == t[2] == a): `dp[0][0] + dp[1][1] = 1 + 1 = 2`. So print `aaa` first, then `b` over the middle. Answer 2.
- `abcabc` -> 5 (the run prints that 6 x 6 table; `dp[0][5] = 5`: printing the last c alone gives `dp[0][4] + 1 = 5`, sharing it with the c at k = 2 gives `dp[0][2] + dp[3][4] = 3 + 2 = 5`, a tie).

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- Empty string: 0.
- One letter, or a single repeated letter (`aaa`, 100 a's): 1.
- All letters different (26 distinct): n turns, nothing to share.
- Alternating `abab...` of length 100: 51 (the code asserts it): one stroke of a across everything, then 50 strokes of b.

**Follow-ups:**
- Why O(n^3) and not better? n^2 states with O(n) transitions each; with n <= 100 that is about 166,000 steps, so nothing faster is needed.
- How would you recover the strokes? Store which candidate won per cell and replay: stroke (k..j) of letter t[j] first, then the middle.
- How does it differ from burst balloons / cut a stick? Same interval shape; here the split condition is "equal letters" instead of "any split point", so only the matching k are tried.

**Common mistakes:**
- Skipping the collapse (not wrong for correctness, but it blows up the table with redundant cells).
- Using `dp[k+1][j]` instead of `dp[k+1][j-1]`: the letter t[j] is already painted by the shared stroke.
- Forgetting the base for an empty middle range (`k + 1 > j - 1` must give 0).
- Only splitting into independent halves: it never shares a stroke and is wrong on `aba`.
