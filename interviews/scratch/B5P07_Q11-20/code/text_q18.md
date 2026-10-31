**Pattern:** Preorder with explicit null markers (a self-delimiting encoding). Recursion on both sides mirrors the tree.

**Say this first (1 line):** "Write preorder, but write a `#` for every missing child, joined with commas. Then reading is deterministic: read a token, if it is `#` return None, otherwise make a node and read its left then its right subtree."

**Brute force:** Store two traversals (preorder and inorder) and rebuild with Q16. That needs distinct values and two strings. Another option: store the level-order array with Nones, which can be huge for a skewed tree (about 2^h slots if you pad every level). The marker format uses exactly 2n + 1 tokens.

**Optimal:**
- `serialize`: preorder, append `str(val)` for a node and `#` for None. `",".join(tokens)`. Commas are safe because a number never contains one; `-` is part of a number and also cannot be confused with `#`.
- `deserialize`: `toks = iter(s.split(","))`, a recursive `go()` that consumes one token per call. `n.left = go()` must run before `n.right = go()`, since the stream is in preorder.
- Token count: n nodes have 2n child slots. n - 1 of them are filled by the other nodes, so the number of markers is `2n - (n - 1) = n + 1`, and the tokens are `n + (n + 1) = 2n + 1`. For the empty tree that gives 1 (just `#`). The run checks this for every tree shape with 0 to 7 nodes.
- Why markers make preorder enough: the stream is self-delimiting. A subtree ends exactly when its left and right parts have both been consumed, and a marker tells you a part is empty. So there is only one way to parse it.
- Plain preorder without markers is ambiguous: `[1, 2]` could be 2 as a left child or as a right child. The run prints both trees with the same plain preorder `[1, 2]`, and the marker strings `1,2,#,#,#` and `1,#,2,#,#`.
- Recursion depth is the tree height. On a skewed tree of 3000 nodes both recursive functions raise `RecursionError` under the default limit of 1000. Avoid it with an explicit stack: serialize with a stack that pops the left child first; deserialize with a stack of `[node, left_filled]` entries (code above). The iterative round trip works on 3000 nodes (6001 tokens).

**Complexity:** Time O(n) both ways (string building with `join`, not repeated `+`). Space O(n) for the string, plus O(h) for the recursion or stack.

**Dry run:** `[1, 2, 3, null, null, 4, 5]`. Preorder with markers: 1, 2, `#`, `#`, 3, 4, `#`, `#`, 5, `#`, `#` which is `1,2,#,#,3,4,#,#,5,#,#`: 11 tokens, and 2 * 5 + 1 = 11. Read: 1, then left: 2 (left `#`, right `#`), then right: 3 (left: 4 with two markers, right: 5 with two markers).

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Empty tree: `"#"`. Single node: `"1,#,#"`.
- Negative values such as `-1` and `-1000`: fine with the comma delimiter and a marker that is not a digit or `-`.
- Skewed trees: use the iterative functions, as above.
- The rebuilt tree must be a fresh copy (no shared nodes); the run verifies this by node identity on every small shape.

**Follow-ups:**
- BFS (level-order) format instead? Same idea with a queue, with a marker for every missing child (Q38).
- Smaller output for a BST? Preorder alone with no markers is enough, because the values determine the shape (Q44).
- Values may contain commas or be strings? Choose an escape or a length prefix, or use a binary or JSON format.

**Common mistakes:**
- A format without markers (ambiguous) or without delimiters (`12` versus `1,2`).
- Building the right child before the left.
- Using `int(token)` on `#`.
- Repeated string `+=` in a loop (quadratic); collect tokens and join.
- Leaving the recursion limit as is and testing only on small trees.
