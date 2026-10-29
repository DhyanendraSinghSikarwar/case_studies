import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B5P12_wavea')
from qs import QS as RAW
def render(v): return repr(v).replace('None', 'null')
def example_text(ex):
    return '; '.join(', '.join(f"{k}={render(v)}" for k, v in kw.items()) + ' -> ' + render(out) for kw, out in ex)
order = {'🟢': 0, '🟡': 1, '🔴': 2}
QS = sorted([(s, d, key, f"{re.sub(r' +', ' ', text.strip())} Example: {example_text(ex)}.", a) for s, d, key, text, ex, a in RAW], key=lambda q: (-q[0], order[q[1]]))   # stable
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
    assert 'seeded random cross-check' in q or 'seeded random cross-check' in q.replace('\n', ' '), key
KEYNO = {q[2]: i for i, q in enumerate(QS, 1)}
# within-part references 'Qn' (not preceded by 'Part N ') must point at the intended question
INTRA = {('word_search', 32): 'iter_ws', ('word_search2', 9): 'word_search', ('replace_words', 3): 'trie_ops', ('subsets_dup', 4): 'subsets',
         ('permutations_dup', 6): 'permutations', ('comb_sum2', 8): 'comb_sum', ('map_sum', 3): 'trie_ops', ('iter_ws', 9): 'word_search', ('trie_memory', 3): 'trie_ops'}
for s, d, key, q, a in QS:
    for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', q):
        qn = int(m.group(1)); tgt = INTRA.get((key, qn), 'MISSING')
        assert tgt != 'MISSING', (key, qn)
        assert KEYNO[tgt] == qn, (key, qn, tgt, KEYNO[tgt])
for (key, qn), tgt in INTRA.items():
    assert re.search(rf'\bQ{qn}\b', next(q[3] for q in QS if q[2] == key)), (key, qn)
KW = {(1, 8): 'Missing number.', (1, 15): 'Valid Sudoku.', (1, 34): 'Next permutation.', (1, 35): 'Randomised set with O(1) operations.', (1, 36): 'Subarray XOR equals k.',
      (1, 42): 'Bloom filter at concept level.', (1, 47): 'Insert, delete and getRandom with duplicates.',
      (3, 2): 'Longest common prefix.', (3, 36): 'Prefix queries: sorted list versus trie, at concept level.',
      (6, 30): 'LRU cache: the linked-list idea (concept only).', (7, 41): 'A trie as a tree, at concept level.',
      (9, 13): 'Union-find with path compression and union by size.', (10, 10): 'Coin change II, number of combinations.',
      (11, 19): 'Palindrome partitioning II: minimum cuts.'}
def refs_in(t):
    return {(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'Part (\d+) Q(\d+)', t)}
refs = set()
for s, d, key, q, a in QS: refs |= refs_in(q)
print('refs in prompts', sorted(refs))
files = {p: open(f'Book5_DSA/Book5_DSA_Part{p:02d}.md', encoding='utf-8').read() for p in range(1, 12)}
def check_ref(p, qn):
    assert 1 <= p <= 11 and (p, qn) in KW, (p, qn)
    m = re.search(rf'^### Q{qn} \S+ \S+ (.*)$', files[p], re.M)
    assert m and m.group(1).startswith(KW[(p, qn)]), (p, qn, m and m.group(1)[:50])
for r in refs: check_ref(*r)
hdr = f"""# Book 5 — Part 12: Backtracking, Tries, Bit Manipulation and DS-flavoured DSA

**Topic:** Python DSA for product-company interviews: backtracking as choose, explore, undo (subsets and permutations with and without duplicates and the skip rule that removes the repeats, combinations with a pruning bound, combination sum with unlimited reuse and with each element once, generate parentheses, letter combinations of a phone number, restore IP addresses, palindrome partitioning, word search on a grid, N-Queens, the Sudoku solver with bitmasks and a most-constrained-cell rule, expression add operators), measuring and pruning the cost of backtracking by counting calls, iterative backtracking with an explicit stack and the recursion limit; tries (insert, search and startsWith, replace words, autocomplete with counts stored per node, map sum, word search II with a trie, maximum XOR with a binary trie, memory of a trie against a dict of sets and arrays of 26); bit manipulation (single number I, II and III, Brian Kernighan's set-bit count with `int.bit_count` and `bit_length`, power of two and of four, Hamming distance and the total over all pairs, XOR for the repeated and the missing number and the XOR swap, `x & -x`, reverse bits, sum of two integers without `+`, enumerating subsets and submasks with a bitmask, and Python's arbitrary-precision integers and negative numbers with `& ~ >>`: no fixed width, so mask to 32 bits explicitly and convert back to signed yourself); and DS-flavoured items at concept level (a minimal skip list), with the output order of every enumeration stated in the prompt

**Target:** 35  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns backtracking enumeration, the trie data structure as an API, and bit manipulation. Part 1 owns hashing; it already has the single missing number as 'Part 1 Q8' (hash set, sort, sum), the XOR-prefix subarray count 'Part 1 Q36', the validity check of a partly filled Sudoku board 'Part 1 Q15', next permutation 'Part 1 Q34', the randomised set with O(1) insert, delete and getRandom 'Part 1 Q35' and its duplicate version 'Part 1 Q47', and the Bloom filter 'Part 1 Q42'; none of these is repeated here (the randomised set and the Bloom filter have no question in this part for that reason; Q15 handles a different XOR task, a repeated and a missing number together; Q25 solves the Sudoku board instead of validating it). Part 3 owns strings ('Part 3 Q2' longest common prefix, 'Part 3 Q36' prefix queries with a sorted list against a trie at concept level), Part 6 owns the LRU idea at concept level ('Part 6 Q30'; the design of the whole cache is Part 14's), Part 7 owns trees and the trie as a tree at concept level ('Part 7 Q41', which counts words per prefix; here Q3 builds the full insert, search and prefix API and Q33 measures its memory), Part 9 owns graphs and union-find ('Part 9 Q13'; no question here repeats it), Parts 10 and 11 own the counting and optimising DP versions of these enumeration problems (counting combinations is 'Part 10 Q10' and the minimum cuts for palindrome partitioning is 'Part 11 Q19'; every question here lists or measures the objects instead), Part 13 owns math, randomised algorithms and sorting internals, and Part 14 owns design problems and advanced structures (segment and Fenwick trees, the full LRU design). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py (it asserts that every reference resolves to the expected heading, including this paragraph), and every within-part reference (Q9 in Q11, Q3 in Q14, and so on) was checked by build.py against the final question numbers. Conventions: every enumeration question states the order of the returned list (the outer list sorted with Python's list comparison, or sorted strings, or ascending by the queen columns for N-Queens, or increasing mask order for the bitmask question) and how duplicates are treated (the subset and permutation questions with duplicates return each distinct result once; combination sum II returns each distinct combination once), and states the return value for degenerate input (the empty input returns `[[]]` for subsets and permutations, an empty list for the phone keypad, for no solution and for no combination, False for no path, 0 for a missing key in the sum store). Recursion: backtracking depth equals the number of choices made, and every enumeration prompt keeps that at most 41 (the combination-sum prompts with the candidate 1 and target 40 are the deepest; at most 81 for Sudoku), far below CPython's default recursion limit of 1000, and says so. The one exception is deliberate: the iterative-backtracking question (Q32) asks for an explicit stack because the recursion of Q9 nests one frame per letter of the word (shown by running code, an observation and not a rule: a single-row board of 300 letters with a word of 300 letters runs, and a single-row board of 1500 letters with a word of 1500 letters raises RecursionError; a winding one-cell corridor on a 43 x 43 board with a path of 967 cells ran with the plain recursion in this sandbox, which is why the prompt names the 1 x 1500 row and not the corridor as the failing case), no prompt relies on raising the limit and no claim is made about the C stack. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P12_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run (142 examples in 35 prompts, each also compared with an independent oracle). Cross-checks: each reference against an independent brute force on seeded random small inputs (300 per question; 150 for word search II, 120 for expression operators, 60 for permutations, 40 for Sudoku with puzzles whose solution was verified unique by a plain solver, 7 sizes for N-Queens), for example every bitmask over the elements for subsets and combination sum II, `itertools.permutations` and `itertools.combinations`, all 2^(2n) strings for parentheses, every choice of three cut positions for IP addresses, every cut set for palindrome partitioning, every 4^(n-1) filling evaluated with `eval` for the expression operators, a path search with an immutable visited tuple for word search, a ripple-carry adder for the sum of two integers, a `Counter` for the single-number questions and the repeated and missing number, and a set of strings for the trie questions. Claims tested by running code: the outer lists are sorted and free of duplicates for every enumeration question (60 random inputs each); the N-Queens counts for n = 1..9 are 1, 0, 0, 2, 10, 4, 40, 92, 352 and the solutions for n = 1..8 equal the permutation oracle and are ascending by queen columns; subsets give 2^n, permutations n!, distinct permutations the multinomial (all 243 multisets of five values from {{1, 2, 3}}), parentheses the Catalan numbers for n = 1..8, combinations C(n, k) with C(20, 10) = 184756, the phone keypad at most 4^6 = 4096; palindrome partitions of a^n number 2^(n-1) for n <= 12; the IP search has 3^4 = 81 leaf choices; the skip test `i > 0` instead of `i > start` loses a subset for [1, 2, 2]; both permutation skip rules (left twin not used, left twin used) return the right set but the second makes more calls on all 243 multisets; the pruned combination loop makes no more calls than the unpruned one; every visited parentheses prefix extends to an answer; the sorted-with-break version of combination sum never makes more calls than the unsorted one (400 random cases) and the two hit counts agree with the combination-sum list; leaving a word-search cell marked on the way back gives a wrong answer on 23 of 400 random boards; `n & (n - 1)` equals `n - (n & -n)` for n < 3000; the Kernighan count, the naive count and `bit_length` agree with `bin` for every n < 5000; the power-of-four mask is right for every power of four in range and for every n in -70..299 and the extremes; `x & -x` isolates the lowest set bit of negative numbers and a ^ b is negative for a = -1, b = 1; the XOR swap sets a value to 0 when both names are the same slot; a negative number never reaches 0 under `>>=` (it stays -1); the 32-step loop, the five-step mask version and the string reversal agree on 2000 random 32-bit patterns; the unmasked carry loop does not stop for a = -1, b = 1 (1000 rounds without ending) while the masked one stopped within 32 rounds on 20000 random pairs and the extremes; the bit-count method without the sign conversion returns 2^32 - 8 for the single value -8 while the converted value is -8, and the `ones`/`twos` machine needs no conversion (500 random lists); the submask loop visits every non-empty submask once in decreasing order (all masks below 128) and the pair count equals 3^n - 2^n for n = 0..12; the trie node count never exceeds the dict-of-sets pair count and the two are equal exactly when no two distinct words share a first letter (400 random word lists; the dict of sets has exactly one key per trie node); the skip list returns the same results for five different seeds on 100 random operation lists and holds 500 sorted keys in at most 16 levels; the maximum XOR of [7, 7] is 0 because the pair needs i < j. All solutions run at the stated maximum sizes (3000 words on a 10 x 10 board, 30000 trie operations, 10^5-element XOR lists, 3 * 10^4 numbers for maximum XOR, C(20, 10) combinations, 9-queens, a 2000-cell board for the iterative search) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems, named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part12_sources.md). Searches returned backtracking pattern guides (techinterview.org, designgurus, a DEV Community post) that group subsets, permutations, combination sum, N-Queens, Sudoku and word search, trie pattern guides (techinterview.org: autocomplete, word search II, wildcard search, replace words, maximum XOR) and bit manipulation lists (Techie Delight, Interview Cake, Interview Kickstart, a Devinterview GitHub list, a Teamblind thread); nothing was found tying any single item to a named company, so 'Asked at' tags name source types, not verified company reports, and no India-specific company report was found for this part. Items such as the skip list, expression add operators, map sum, single number II and the sum of two integers come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page; that `int.bit_count` first appeared in Python 3.10 is editor knowledge and was not checked against documentation. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

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
assert not re.search(r'(?i)\blpa\b|salary|\brs \d', txt.split('Evidence limits')[0].replace('No salary figures', ''))
assert '\n' not in ''.join(q for _, _, _, q, _ in QS)
HQ = {3: 'trie_ops', 4: 'subsets', 6: 'permutations', 8: 'comb_sum', 9: 'word_search', 11: 'word_search2', 14: 'replace_words', 15: 'dup_missing', 25: 'sudoku', 32: 'iter_ws', 33: 'trie_memory',
      1: 'single_number', 18: 'subsets_dup', 19: 'permutations_dup', 21: 'comb_sum2', 27: 'map_sum'}
for k, v in HQ.items(): assert KEYNO[v] == k, (k, v, KEYNO[v])
# every header 'Qn' claim (without 'Part') resolves: check the ones used in the header explicitly
for m in re.finditer(r'(?<!Part \d )(?<!Part \d\d )\bQ(\d+)\b', hdr.split('Scope note')[1].split('Evidence limits')[0]):
    assert int(m.group(1)) in {3, 9, 11, 14, 15, 25, 32, 33}, m.group(0)
open('Book5_DSA/Book5_DSA_Part12.md', 'w', encoding='utf-8', newline='\n').write(txt)
rows_i = ''.join(f"| B5P12-Q{i} | 12 | {q.strip()} |\n" for i, (s, d, key, q, a) in enumerate(QS, 1))
open('scratch/B5P12_wavea/index_rows.txt', 'w', encoding='utf-8', newline='\n').write(rows_i)
idx = open('question_index.md', encoding='utf-8').read()
if 'B5P12-Q1 ' not in idx:
    if not idx.endswith('\n'): idx += '\n'
    open('question_index.md', 'w', encoding='utf-8', newline='\n').write(idx + rows_i)
print('built', n, c)
for i, (s, d, key, q, a) in enumerate(QS, 1): print(i, s, d, key)
