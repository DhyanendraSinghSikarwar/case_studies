# Book 5 Part 7 review (Wave C)

Date: 2026-10-27. Reviewer: lead session (independent of the five answer agents). Scope: 50 questions, Q1-Q50 (DSA in Python: trees and BST). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Five agents answered Q1-10, Q11-20, Q21-30, Q31-40, Q41-50; merged by heading: 50 of 50 merged, 0 skipped, 0 pending. No spend-limit stops. Wave A rendered each of 210 examples from the same data that `check_examples.py` runs and cross-checked reference solutions over all 626 tree shapes up to 7 nodes, all small BST shapes and seeded random cases; each answer agent re-ran the examples and tested stated bounds and uniqueness claims exhaustively over small shapes.

## Checks (scripted by the lead, `scratch/B5_check.py`)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q50; star order and counts 18 / 21 / 11 | pass |
| All 11 template labels present and in order; code fences balanced | pass for all 50 |
| One python block per answer, re-run standalone with `python3 -I` by the lead | 50 of 50 exit 0 |
| Cross-references (Part 1 Q13, Part 3 Q36, Part 4 Q25 and Q30, Part 6 Q2, Q17, Q26) | verified by Wave A's build.py |

Every block builds trees from level-order arrays with None, guards against cycles and shared nodes, runs the question's own examples and cross-checks against an independent brute force.

## Correction made during review
Q35 (deep skewed trees and the recursion limit) said raising `sys.setrecursionlimit` is not a fix for 10^5 nodes "because the C stack can overflow". The Q31-40 agent refuted that for pure-Python recursion on Python 3.13.17: with the limit raised, a 10^5-node recursive depth succeeded (about 10 MB extra) and 10^6 nodes succeeded (about 107 MB extra, sandbox-only), while recursion through an `lru_cache` wrapper still raised RecursionError at depth 10^5 because C-level calls have a separate fixed limit. The prompt sentence now says raising the limit is version and call-path dependent (some call paths such as `lru_cache` have a separate C-level limit, older interpreters can crash, memory still grows with depth). The lead applied the same wording to the part file, the agent's answer heading, the Wave A source (`qs.py`) and the question_index rows. The answer still recommends the explicit stack.

## Prompt notes handled in the answers (frozen prompts otherwise unchanged)
- Recursion limit versus stated sizes: Q7, Q10 (n up to 5,000), Q11, Q12 (10^4), Q16 (3,000), Q18 (10^4), Q20 (10^5), Q22 (2*10^4), Q26 (5,000), Q27 (1,000), Q29 (3,000), Q31, Q44 (3,000), Q45, Q46, Q49 (10^4) and Q50 (1,000): a skewed tree at these limits raises RecursionError under the default limit of 1,000; each answer demonstrates it and gives an iterative version.
- Q10: the example `[1,2,2,3,3,null,null,4,4]` does not show why checking only the root's two heights is not enough (root heights are 3 and 1); the answer uses `[1,2,2,3,null,null,3,4,null,null,4]` and the searched smallest counter-example `[0,1,3,null,2,null,4,null,null,null,5]`. Top-down cost is O(n*h): a perfect tree of 4,095 nodes took 40,962 visits against 4,095 for the single pass.
- Q24: "measured after each append" gives 0 for a single node; the answer counts the initial `deque([root])` (single node gives 1; perfect k-level tree gives 2^(k-1)); all four examples still match. Q34: step bounds tested exactly (at most 2h^2; exactly 2h on a perfect tree; h(2h-1) at n = 2^(h+1)-2), after the Wave A draft's (h+1)^2 was refuted at n = 22.
- Q44: the upper-bound builder does not validate input (`[1,2,0]` builds a garbage tree); the uniqueness claim holds for valid preorders (exactly Catalan(n) of n <= 7). Q49: "one pass" is the recursive flagged DFS; the iterative answer is a leaf pass plus two O(h) edge walks, stated in a follow-up. Q48: the n+L loop count holds on every shape up to 9 nodes; an exception in the visit callback leaves a thread behind (demonstrated). Q36: the first recursive splice was O(n^2) on a left-skewed tree and was rewritten to return the tail. Q23: the prompt excludes duplicates; the iterative code would send a duplicate right. Outputs print `None` where prompts write `null`.

## Findings kept in the text (observed)
Diameter, validate-BST, LCA, right view, max path sum, serialisation (exactly 2n+1 tokens for n = 0..8, 2,056 shapes) and minimum depth all match brute force on tens of thousands of cases; the early-return LCA is wrong in all 4,081 missing-value cases; starting max-path-sum at 0 or skipping the clamp gives wrong answers; preorder+postorder is ambiguous from n = 2 and a pair identifies a tree exactly when it is full (Q29); (preorder, inorder) pairs are distinct across 625 shapes (Q16); the swap-back pair in recover-BST is unique across 51,550 cases (Q39); a level-parity house-robber greedy is wrong on 640 of 1,878 trees, e.g. `[2,1,3,null,4]` gives 6 against 7 (Q45); a camera on every leaf is never needed for n >= 2 (Q50); chains of k nodes need ceil(k/3) cameras (tested to k = 39 and 1,000).

## Not run / sandbox-only
Memory figures (Q35, Q16, Q43) are sandbox-only. Concept-level questions Q41 (trie), Q45 (house robber III) and Q50 (binary tree cameras) keep full treatment for Parts 12 and 10.

## Evidence limits
No company-reported problems verified; snippets support Flipkart and Amazon candidate-reported entries (vertical order, LCA), a Glassdoor Flipkart LCA report and a Facebook intern report; every WebFetch failed (8 searches, snippets only). See research_notes/Book5_Part07_sources.md.
