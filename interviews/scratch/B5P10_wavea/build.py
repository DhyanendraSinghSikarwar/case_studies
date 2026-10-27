import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P10_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out) for kw, out in ex)
order = {'🟢': 0, '🟡': 1, '🔴': 2}
QS = sorted([(s, d, key, f"{text.strip()} Example: {example_text(ex)}.", a) for s, d, key, text, ex, a in RAW], key=lambda q: (-q[0], order[q[1]]))   # stable
N = 40
n = len(QS)
c = [sum(1 for q in QS if q[0] == s) for s in (3, 2, 1)]
print(n, c)
assert n == N, n
assert [q[0] for q in QS] == sorted([q[0] for q in QS], reverse=True)
assert sum(c) == N and all(q[1] in order for q in QS)
assert len({q[3] for q in QS}) == N and len({q[2] for q in QS}) == N
assert len({q[3].split('.')[0] for q in QS}) == N   # unique titles
for s in (3, 2, 1):
    d = [order[q[1]] for q in QS if q[0] == s]
    assert d == sorted(d), (s, d)
for s, d, key, q, a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
    assert 'seeded random cross-check' in q or key in ('alias_trap',), key
KEYNO = {q[2]: i for i, q in enumerate(QS, 1)}
# within-part references 'Qn' (not preceded by 'Part N ') must point at the intended question
INTRA = {('coin_ways', 6): 'coin_min', ('coin_ways', 10): None, ('comb_sum4', 10): 'coin_ways', ('knapsack01', 20): 'unbounded_knapsack', ('unbounded_knapsack', 17): 'knapsack01',
         ('perfect_squares', 6): 'coin_min', ('stock_cooldown', 4): 'stock_once', ('delete_earn', 5): 'house_robber', ('count_lis', 7): 'lis_length', ('lis_recon', 7): 'lis_length'}
for s, d, key, q, a in QS:
    for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', q):
        qn = int(m.group(1)); tgt = INTRA.get((key, qn), 'MISSING')
        assert tgt is not None and tgt != 'MISSING', (key, qn)
        assert KEYNO[tgt] == qn, (key, qn, tgt, KEYNO[tgt])
for (key, qn), tgt in INTRA.items():
    if tgt: assert re.search(rf'\bQ{qn}\b', next(q[3] for q in QS if q[2] == key)), (key, qn)
KW = {(4, 35): 'Maximum score with jumps of at most k (monotonic deque for DP).', (5, 11): 'Lower and upper bound semantics and the bisect module.',
      (7, 35): 'Deep skewed trees and the recursion limit.', (7, 45): 'House Robber III, at concept level.', (7, 50): 'Binary tree cameras, at concept level.',
      (8, 12): 'Jump game (can you reach the end).', (8, 13): 'Jump game II (minimum jumps).', (8, 18): 'Last stone weight.', (8, 33): 'When greedy fails: coins.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part0{p}.md', encoding='utf-8').read() for p in (1, 2, 3, 4, 5, 6, 7, 8, 9)}
def check_ref(p, qn):
    assert p in files and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
hdr = f"""# Book 5 — Part 10: Dynamic Programming I (1D DP and Knapsack)

**Topic:** Python DSA for product-company interviews: how to define a DP state and derive the transition, base cases, counting versus optimising DPs, memoisation versus tabulation versus space optimisation, climbing stairs and Fibonacci (call counts of plain recursion, a cache and a bottom-up loop), min cost climbing stairs, house robber (linear and circular), maximum subarray (Kadane, with indices and a tie rule, and the circular variant), maximum product subarray, best time to buy and sell stock as a state machine (one transaction, cooldown, at most k transactions), decode ways, coin change (minimum coins, number of combinations, and recovering the coins), perfect squares, word break, longest increasing subsequence (O(n^2) table, O(n log n) with bisect and the patience-sorting argument, recovering one, the non-decreasing variant with bisect_right, counting all of them, Russian doll envelopes), 0/1 knapsack (1D table and why the capacity loop runs downward, recovering the items), subset sum with a table and a big-int bitset, partition equal subset sum, target sum, last stone weight II, unbounded knapsack, combination sum IV (order matters versus not), ones and zeroes (a two-capacity knapsack at the edge of 2D DP), delete and earn, jump game as DP versus greedy, paint fence and dice-roll counting with a modulus, minimum cost for tickets, and Python specifics (recursion limit versus bottom-up, `functools.cache` and `lru_cache` with mutable arguments and `cache_clear`, the `[[0]*n]*m` aliasing trap)

**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns one-dimensional DP and knapsack-style tables. Part 5 owns binary search (the bisect semantics used by the patience-sorting LIS are cross-referenced as 'Part 5 Q11'), Part 7 owns trees (tree DP stays there: House Robber III is 'Part 7 Q45' and binary tree cameras 'Part 7 Q50'; the deep-recursion limit on skewed trees is 'Part 7 Q35'; nothing from them is duplicated here, and Q5 only points to Part 7 Q45), Part 8 owns greedy (jump game and jump game II are 'Part 8 Q12' and 'Part 8 Q13', the greedy-fails-for-coins counter-example is 'Part 8 Q33' and the heaviest-two stone smashing is 'Part 8 Q18'; here the same problems are the DP side of the greedy-versus-DP contrast), Part 4 owns monotonic stacks and deques (a DP over jumps of at most k with a monotonic deque is 'Part 4 Q35'), Part 9 owns graphs (shortest paths on a DAG as a DP are handed off by part number only), Part 11 owns DP II (two-dimensional grids, string DPs such as edit distance and longest common subsequence, interval DP and palindromic subsequences; this part has only the two-capacity knapsack of Q39, 'ones and zeroes', at the concept edge, and the aliasing trap of Q31, whose 2D table appears everywhere in Part 11), Part 12 owns backtracking (enumerating the combinations, orderings or paths instead of counting them: the counting questions here, Q10, Q19, Q21 and Q28, return counts only), and Part 13 owns math and prefix sums. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py, and every within-part reference (Q6, Q10 and so on) was checked by build.py against the final question numbers. Conventions: every question states its constraints, whether an answer is returned exactly (Python integers do not overflow) or modulo 10^9 + 7, and its return value for degenerate input (an empty list, a zero target or amount, an impossible case returns -1 or null as the prompt says). Every prompt asks the answer to include a table walk-through on the first example and a seeded random cross-check of the optimal solution against a brute-force or plain-recursion oracle on small inputs. Recursion: every prompt whose size passes 1000 for a natural top-down recursion says a bottom-up solution is required, because a memoised recursion nests about n deep and CPython's default recursion limit is 1000 (demonstrated by running code: memoised recursions at the quoted sizes for climbing stairs, house robber, coin change, perfect squares, combination sum IV, coin change II, paint fence and the cooldown stock problem each raise RecursionError at the default limit, and a 3-step stair recursion succeeds at n = 500 and fails at n = 2000), while no prompt relies on raising the limit and no claim is made about the C stack. Questions whose answer would not be unique say exactly what is accepted: reconstruction questions fix an explicit tie rule (maximum subarray position: smallest start, then smallest end; coin change recovery: the lexicographically smallest list among minimum-size multisets; LIS recovery and knapsack item recovery: the lexicographically smallest list of indices), and the reachable set in the jump game, the `tails` array of patience sorting and the call counts of Q14 are defined step by step so their outputs are unique. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P10_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force or plain recursion on 400 seeded random small inputs per question (15612 in all), for example subset enumeration for house robber, partition, knapsack, subset sum, ones and zeroes and delete and earn; all 2^n sign assignments for target sum; plain recursion without a memo for climbing stairs, coin change, perfect squares, unbounded knapsack and tickets; all subsequences for the LIS family (length, smallest last value per length, count, lexicographic recovery, non-decreasing variant); all colourings for paint fence; all outcomes for dice rolls; all multisets for coin recovery; every smash order for last stone weight II; and counted-call and dict-memo models for the cache questions. Claims tested by running code: the maximum subarray tie rule agrees with the O(n^2) enumeration on every list of length up to 6 with values in -2..2 (19530 lists); the reachable set in the jump game is a prefix of the indices on all 5460 lists of length up to 6 with values 0..3; the circular-array maximum equals the circular enumeration on every list of length up to 5 with values -3..3 and the naive formula max(Kadane, total - minimum subarray) is wrong on some of them; the upward-loop 0/1 knapsack equals the unbounded knapsack on 1000 random inputs and differs from the true 0/1 answer on some of them; the bitset and the boolean table agree for subset sum; target sum with z zeros is 2^z times the count without them; in combination sum IV the swapped loop order yields the unordered count and the ordered count is never smaller; the plain parent-pointer rebuild of coin change differs from the lexicographic tie rule on some inputs; bisect_left used for the non-decreasing LIS computes the strict length and is wrong on some inputs, the number of greedy patience piles equals the LIS length and `tails` is not itself an LIS; sorting equal widths by ascending height is wrong for Russian dolls on some inputs; the at-most-k stock table with k capped at n // 2 equals the full table; the fence count modulo 10^9 + 7 equals the exact big-integer count modulo; `[[0]*n]*m` has exactly one distinct row object while the comprehension has m; a list argument to a `functools.cache` function raises TypeError (unhashable type: 'list'); naive Fibonacci calls equal 2 fib(n + 1) - 1 and memoised calls equal 2n - 1 for n >= 1. Both branches of every boolean or sentinel answer occurred in the random tests, and all solutions run at the stated maximum sizes (10^5-element lists, 10^4 amounts, 200 items with 10^4 targets) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part10_sources.md). Searches returned DP pattern guides (techinterview.org, DesignGurus, IGotAnOffer, labuladong, system.design), candidate-reported Flipkart rounds that mention coin change, a longest decreasing subsequence assessment, a 0-1 knapsack with a space-optimisation follow-up and an unbounded-knapsack-like question (LeetCode Discuss, Naukri Code360, GeeksforGeeks and Taro, self-reported, spanning 2017 to 2025 and mixing intern and SDE-1 roles), and stock state-machine write-ups; nothing was found tying the other items to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as delete and earn, last stone weight II, ones and zeroes, Russian doll envelopes, minimum cost for tickets and number of longest increasing subsequences come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
for q in re.findall(r"\b(Q\d+)\b", hdr.split('Evidence limits')[0]): pass
out = [hdr]
for i, (s, d, key, q, a) in enumerate(QS, 1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt = ''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->') == N and txt.count('**Asked at:**') == N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 40" in txt
assert txt.count('\n### Q') == N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0])
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
# header Q-number claims: Q5, Q10, Q14, Q19, Q21, Q28, Q31, Q39 named in the scope note
HQ = {5: 'house_robber', 10: 'coin_ways', 14: 'fib_three', 19: 'target_sum', 21: 'comb_sum4', 28: 'count_lis', 31: 'alias_trap', 39: 'ones_zeroes'}
for k, v in HQ.items(): assert KEYNO[v] == k, (k, v, KEYNO[v])
open('Book5_DSA/Book5_DSA_Part10.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P10-Q{i} | 10 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P10_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P10-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
