import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P11_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out) for kw, out in ex)
order = {'🟢': 0, '🟡': 1, '🔴': 2}
QS = sorted([(s, d, key, f"{text.strip()} Example: {example_text(ex)}.", a) for s, d, key, text, ex, a in RAW], key=lambda q: (-q[0], order[q[1]]))   # stable
N = 35
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
    assert 'seeded random cross-check' in q, key
KEYNO = {q[2]: i for i, q in enumerate(QS, 1)}
# within-part references 'Qn' (not preceded by 'Part N ') must point at the intended question
INTRA = {('regex_match', 17): 'wildcard_count'}
for s, d, key, q, a in QS:
    for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', q):
        qn = int(m.group(1)); tgt = INTRA.get((key, qn), 'MISSING')
        assert tgt is not None and tgt != 'MISSING', (key, qn)
        assert KEYNO[tgt] == qn, (key, qn, tgt, KEYNO[tgt])
for (key, qn), tgt in INTRA.items():
    if tgt: assert re.search(rf'\bQ{qn}\b', next(q[3] for q in QS if q[2] == key)), (key, qn)
KW = {(3, 8): 'Longest palindromic substring.', (3, 9): 'Count palindromic substrings.', (3, 34): 'One edit distance.', (3, 35): 'Edit distance and LCS at concept level.',
      (3, 38): 'Wildcard matching.', (9, 40): 'Shortest paths in a DAG with negative weights.',
      (10, 29): 'Best time to buy and sell stock with at most k transactions.', (10, 31): 'The `[[0]*n]*m` aliasing trap.', (10, 39): 'Ones and zeroes'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part{p:02d}.md', encoding='utf-8').read() for p in range(1, 11)}
def check_ref(p, qn):
    assert 1 <= p <= 10 and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
hdr = f"""# Book 5 — Part 11: Dynamic Programming II (2D Grids, Two-String DPs, Intervals and Bitmasks)

**Topic:** Python DSA for product-company interviews: two-dimensional DP states and how to derive the transition, grid DP (unique paths with and without obstacles, minimum path sum with the path recovered under an explicit tie rule, triangle, minimum falling path, counting minimum-cost paths, paths whose sum is divisible by k with a modulus, maximal square, the dungeon game solved backwards, cherry pickup as a two-walker DP), two-sequence string DPs (longest common subsequence as a length and as the lexicographically smallest string, longest common substring, edit distance as a value and as an edit script, shortest common supersequence, minimum ASCII delete sum, interleaving string, distinct subsequences as a counting DP, longest repeating subsequence, regular expression matching, wildcard matching as a counting table), palindromic DPs (longest palindromic subsequence, counting palindromic substrings with a table, palindrome partitioning with minimum cuts), interval DP (burst balloons, matrix chain multiplication with its parenthesisation, minimum cost to cut a stick, minimum score triangulation, strange printer), a DAG DP over a matrix (longest increasing path), bitmask DP at a basic level (assigning tasks, travelling salesman with a small number of cities), space optimisation to one or two rows, reconstruction of solutions with explicit tie rules, counting versus optimising DPs, modulo arithmetic, and Python specifics (memoised recursion on an n x m state grid versus bottom-up, `functools.lru_cache` with tuple keys, cache size and recursion depth)

**Target:** 35  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns two-dimensional DP: grids, two-string tables, interval DP and basic bitmask DP. Part 3 owns the string patterns around it (expand-around-center and the longest palindromic substring are 'Part 3 Q9' and 'Part 3 Q8', the single-edit test is 'Part 3 Q34', edit distance and LCS at concept level with a memoised recursion are 'Part 3 Q35', and the two-pointer boolean wildcard matcher is 'Part 3 Q38'; here the same ideas appear as full tabulated DPs, with space optimisation and reconstruction, and the wildcard question Q17 adds a counting table instead of repeating the boolean matcher; the palindromic-substring question Q12 reuses the Part 3 Q9 problem only to build the interval table and a one-row version), Part 5 owns binary search, Part 9 owns graphs (shortest paths on a DAG as a DP are 'Part 9 Q40'; Q24, the longest increasing path in a matrix, is the matrix version solved bottom-up and does not repeat the graph material), Part 10 owns DP I (the at-most-k stock table is 'Part 10 Q29', the `[[0]*n]*m` aliasing trap is 'Part 10 Q31' and 'ones and zeroes', the two-capacity knapsack, is 'Part 10 Q39'; none of them is duplicated here, Q1 and Q6 only point to Q31 and Q29, and Q39 is named only to mark the edge of this part), Part 12 owns backtracking (enumerating the paths, cuts or orderings instead of counting or optimising them: every question here returns a count, a length, an optimum or one optimal object under a tie rule), and Part 13 owns math. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py, and every within-part reference (Q17 in Q9) was checked by build.py against the final question numbers. Conventions: every question states its constraints, whether the answer is returned exactly (Python integers do not overflow) or modulo 10^9 + 7 (Q27 and Q28 only), and its return value for degenerate input (an empty string, an empty list, a 1 x 1 grid, an impossible or zero-length case as the prompt says). Every prompt asks the answer to include a table walk-through on the first example and a seeded random cross-check of the solution against a brute-force, plain-recursion or standard-library oracle on small inputs. Recursion: the prompts whose natural top-down recursion nests past 1000 say a bottom-up solution is required, because CPython's default recursion limit is 1000 and the call depth of a memoised recursion on a two-sequence or a grid table grows with the sum of the two sizes (demonstrated by running code, an observation and not a rule: a memoised LCS on two 300-letter strings runs and on two 400-letter strings runs, the same recursion raises RecursionError for two disjoint 520-, 600- and 1000-letter strings; a memoised edit distance, ASCII delete sum at 1000 x 1000, a memoised longest palindromic subsequence on 2000 letters and a memoised regular-expression match of 1000 letters against `a*` repeated 500 times all raise RecursionError; memoised grid recursion with the cache key `(i, j)` on a 600 x 600 grid is 1199 deep and raises RecursionError while 400 x 400 is 799 deep and works; a memoised longest-increasing-path DFS on a 61 x 61 winding corridor of increasing values raises RecursionError), and no prompt relies on raising the limit and no claim is made about the C stack. Questions whose answer would not be unique say exactly what is accepted: every reconstruction question fixes an explicit tie rule (minimum path moves: lexicographically smallest string with 'D' < 'R', Q14; LCS string: lexicographically smallest, Q10; edit script: lexicographically smallest over D < I < M < S, Q15; shortest common supersequence: lexicographically smallest, Q16; matrix-chain parenthesisation: smallest split index, applied recursively, Q23; task assignment: lexicographically smallest list, Q31; longest common substring: smallest i then smallest j, Q11), and each rule was verified against an oracle that enumerates every candidate and applies the same rule. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P11_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force, plain recursion, `re.fullmatch` (regular expressions), a breadth-first search over printed states (strange printer) or an instrumented `lru_cache` recursion (cache size and depth) on 300 seeded random small inputs per question (fewer for the slowest oracles), for example all subsequences for the palindromic and common-subsequence questions, every path for the grid questions, every pair of paths for cherry pickup, every permutation for assignment, travelling salesman and cut-a-stick, every parenthesisation for matrix chain and every index combination for distinct subsequences. Claims tested by running code: every pair of strings of length up to 4 over {{a, b}} (961 pairs) agrees with the oracle for the lexicographically smallest LCS, the shortest common supersequence, the edit script (which also turns `a` into `b` and has as many non-match letters as the edit distance), the longest common substring and the ASCII delete sum; every binary-string table up to length 8 gives the longest palindromic subsequence equal to the LCS of the string with its reverse, the one-row interval version and the oracle, and the palindromic-substring count and minimum cuts agree with their oracles; every 2 x 3 grid with values 0..2 and every 3 x 3 grid with values 0..1 (1241 grids) gives the same minimum-path string and minimum-path count as the oracle, and every assignment matrix of 0 and 1 of size 3 x 3 the same assignment; every matrix chain of 4 matrices with dimensions 1..3 agrees with the enumeration; the closed forms C(m + n - 2, m - 1) for unique paths (and for the obstacle-free grid), C(n + k - 1, k - 1) for k stars in the wildcard count, C(50, 25) for distinct subsequences of a^50 equal to a^25 and C(198, 99) for the minimum-cost path count on a zero grid (which exceeds 10^9 + 7, so the modulus matters); a greedy move fails for minimum path sum on 98 of 500 random grids; the maximum-total-sum path needs more health than the optimum on 5 of 500 random dungeon grids (so a forward DP is not enough); a parent-pointer rebuild from a prefix table gives a different minimum path than the suffix tie rule on 244 of 500 and the classic back-pointer LCS walk gives a different string than the lexicographically smallest one on 39 of 500; the order among equal values does not matter for the longest increasing path (300 shuffles); the boolean wildcard result equals a regular-expression translation on 600 random inputs and equals ways > 0; the cache of an `lru_cache` function rejects a list argument with TypeError (unhashable). Both branches of every boolean or sentinel answer occurred in the random tests, and all solutions run at the stated maximum sizes (1000 x 1000 string tables, 2000-letter palindrome tables, 200 x 200 grids, 300 balloons, 200 matrices, 1500 x 1500 grid statistics, 15 tasks, 12 cities) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part11_sources.md). Searches returned DP pattern guides (techinterview.org 2D and interval and advanced DP posts, a LeetCode Discuss 13-patterns post, codemia, a DP pattern cheat sheet) that group LCS, edit distance, regular-expression and wildcard matching, grid paths, burst balloons, matrix chain and bitmask DP, and candidate-reported Flipkart rounds (a 2020 on-campus report with a longest palindromic substring solved by a 2-D boolean table and a 2024 off-campus SDE-1 report with a 2D DP array-splitting question; self-reported, unverified); nothing was found tying edit distance, LCS or any other item to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as dungeon game, distinct subsequences, minimum cost to cut a stick, strange printer, cherry pickup and minimum score triangulation come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
for m in refs_in(hdr): check_ref(*m)
out = [hdr]
for i, (s, d, key, q, a) in enumerate(QS, 1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt = ''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->') == N and txt.count('**Asked at:**') == N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt and "**Target:** 35" in txt
assert txt.count('\n### Q') == N
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0])
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
HQ = {8: 'edit_distance', 9: 'regex_match', 10: 'lcs_recon', 11: 'lcs_substring', 12: 'palin_substr_dp', 14: 'min_path_recon', 15: 'edit_script', 16: 'scs', 17: 'wildcard_count',
      23: 'matrix_chain', 24: 'lis_matrix', 27: 'paths_mod_k', 28: 'count_min_paths', 31: 'assign_tasks', 1: 'unique_paths', 6: 'lcs_length'}
for k, v in HQ.items(): assert KEYNO[v] == k, (k, v, KEYNO[v])
open('Book5_DSA/Book5_DSA_Part11.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P11-Q{i} | 11 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P11_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P11-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
