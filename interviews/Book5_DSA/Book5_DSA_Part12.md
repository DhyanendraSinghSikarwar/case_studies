# Book 5 — Part 12: Backtracking, Tries, Bit Manipulation and DS-flavoured DSA

**Topic:** Python DSA for product-company interviews: backtracking as choose, explore, undo (subsets and permutations with and without duplicates and the skip rule that removes the repeats, combinations with a pruning bound, combination sum with unlimited reuse and with each element once, generate parentheses, letter combinations of a phone number, restore IP addresses, palindrome partitioning, word search on a grid, N-Queens, the Sudoku solver with bitmasks and a most-constrained-cell rule, expression add operators), measuring and pruning the cost of backtracking by counting calls, iterative backtracking with an explicit stack and the recursion limit; tries (insert, search and startsWith, replace words, autocomplete with counts stored per node, map sum, word search II with a trie, maximum XOR with a binary trie, memory of a trie against a dict of sets and arrays of 26); bit manipulation (single number I, II and III, Brian Kernighan's set-bit count with `int.bit_count` and `bit_length`, power of two and of four, Hamming distance and the total over all pairs, XOR for the repeated and the missing number and the XOR swap, `x & -x`, reverse bits, sum of two integers without `+`, enumerating subsets and submasks with a bitmask, and Python's arbitrary-precision integers and negative numbers with `& ~ >>`: no fixed width, so mask to 32 bits explicitly and convert back to signed yourself); and DS-flavoured items at concept level (a minimal skip list), with the output order of every enumeration stated in the prompt

**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 11, ⭐⭐ 15, ⭐ 9)  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns backtracking enumeration, the trie data structure as an API, and bit manipulation. Part 1 owns hashing; it already has the single missing number as 'Part 1 Q8' (hash set, sort, sum), the XOR-prefix subarray count 'Part 1 Q36', the validity check of a partly filled Sudoku board 'Part 1 Q15', next permutation 'Part 1 Q34', the randomised set with O(1) insert, delete and getRandom 'Part 1 Q35' and its duplicate version 'Part 1 Q47', and the Bloom filter 'Part 1 Q42'; none of these is repeated here (the randomised set and the Bloom filter have no question in this part for that reason; Q15 handles a different XOR task, a repeated and a missing number together; Q25 solves the Sudoku board instead of validating it). Part 3 owns strings ('Part 3 Q2' longest common prefix, 'Part 3 Q36' prefix queries with a sorted list against a trie at concept level), Part 6 owns the LRU idea at concept level ('Part 6 Q30'; the design of the whole cache is Part 14's), Part 7 owns trees and the trie as a tree at concept level ('Part 7 Q41', which counts words per prefix; here Q3 builds the full insert, search and prefix API and Q33 measures its memory), Part 9 owns graphs and union-find ('Part 9 Q13'; no question here repeats it), Parts 10 and 11 own the counting and optimising DP versions of these enumeration problems (counting combinations is 'Part 10 Q10' and the minimum cuts for palindrome partitioning is 'Part 11 Q19'; every question here lists or measures the objects instead), Part 13 owns math, randomised algorithms and sorting internals, and Part 14 owns design problems and advanced structures (segment and Fenwick trees, the full LRU design). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py (it asserts that every reference resolves to the expected heading, including this paragraph), and every within-part reference (Q9 in Q11, Q3 in Q14, and so on) was checked by build.py against the final question numbers. Conventions: every enumeration question states the order of the returned list (the outer list sorted with Python's list comparison, or sorted strings, or ascending by the queen columns for N-Queens, or increasing mask order for the bitmask question) and how duplicates are treated (the subset and permutation questions with duplicates return each distinct result once; combination sum II returns each distinct combination once), and states the return value for degenerate input (the empty input returns `[[]]` for subsets and permutations, an empty list for the phone keypad, for no solution and for no combination, False for no path, 0 for a missing key in the sum store). Recursion: backtracking depth equals the number of choices made, and every enumeration prompt keeps that at most 41 (the combination-sum prompts with the candidate 1 and target 40 are the deepest; at most 81 for Sudoku), far below CPython's default recursion limit of 1000, and says so. The one exception is deliberate: the iterative-backtracking question (Q32) asks for an explicit stack because the recursion of Q9 nests one frame per letter of the word (shown by running code, an observation and not a rule: a single-row board of 300 letters with a word of 300 letters runs, and a single-row board of 1500 letters with a word of 1500 letters raises RecursionError; a winding one-cell corridor on a 43 x 43 board with a path of 967 cells ran with the plain recursion in this sandbox, which is why the prompt names the 1 x 1500 row and not the corridor as the failing case), no prompt relies on raising the limit and no claim is made about the C stack. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P12_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run (142 examples in 35 prompts, each also compared with an independent oracle). Cross-checks: each reference against an independent brute force on seeded random small inputs (300 per question; 150 for word search II, 120 for expression operators, 60 for permutations, 40 for Sudoku with puzzles whose solution was verified unique by a plain solver, 7 sizes for N-Queens), for example every bitmask over the elements for subsets and combination sum II, `itertools.permutations` and `itertools.combinations`, all 2^(2n) strings for parentheses, every choice of three cut positions for IP addresses, every cut set for palindrome partitioning, every 4^(n-1) filling evaluated with `eval` for the expression operators, a path search with an immutable visited tuple for word search, a ripple-carry adder for the sum of two integers, a `Counter` for the single-number questions and the repeated and missing number, and a set of strings for the trie questions. Claims tested by running code: the outer lists are sorted and free of duplicates for every enumeration question (60 random inputs each); the N-Queens counts for n = 1..9 are 1, 0, 0, 2, 10, 4, 40, 92, 352 and the solutions for n = 1..8 equal the permutation oracle and are ascending by queen columns; subsets give 2^n, permutations n!, distinct permutations the multinomial (all 243 multisets of five values from {1, 2, 3}), parentheses the Catalan numbers for n = 1..8, combinations C(n, k) with C(20, 10) = 184756, the phone keypad at most 4^6 = 4096; palindrome partitions of a^n number 2^(n-1) for n <= 12; the IP search has 3^4 = 81 leaf choices; the skip test `i > 0` instead of `i > start` loses a subset for [1, 2, 2]; both permutation skip rules (left twin not used, left twin used) return the right set but the second makes more calls on all 243 multisets; the pruned combination loop makes no more calls than the unpruned one; every visited parentheses prefix extends to an answer; the sorted-with-break version of combination sum never makes more calls than the unsorted one (400 random cases) and the two hit counts agree with the combination-sum list; leaving a word-search cell marked on the way back gives a wrong answer on 23 of 400 random boards; `n & (n - 1)` equals `n - (n & -n)` for n < 3000; the Kernighan count, the naive count and `bit_length` agree with `bin` for every n < 5000; the power-of-four mask is right for every power of four in range and for every n in -70..299 and the extremes; `x & -x` isolates the lowest set bit of negative numbers and a ^ b is negative for a = -1, b = 1; the XOR swap sets a value to 0 when both names are the same slot; a negative number never reaches 0 under `>>=` (it stays -1); the 32-step loop, the five-step mask version and the string reversal agree on 2000 random 32-bit patterns; the unmasked carry loop does not stop for a = -1, b = 1 (1000 rounds without ending) while the masked one stopped within 32 rounds on 20000 random pairs and the extremes; the bit-count method without the sign conversion returns 2^32 - 8 for the single value -8 while the converted value is -8, and the `ones`/`twos` machine needs no conversion (500 random lists); the submask loop visits every non-empty submask once in decreasing order (all masks below 128) and the pair count equals 3^n - 2^n for n = 0..12; the trie node count never exceeds the dict-of-sets pair count and the two are equal exactly when no two distinct words share a first letter (400 random word lists; the dict of sets has exactly one key per trie node); the skip list returns the same results for five different seeds on 100 random operation lists and holds 500 sorted keys in at most 16 levels; the maximum XOR of [7, 7] is 0 because the pair needs i < j. All solutions run at the stated maximum sizes (3000 words on a 10 x 10 board, 30000 trie operations, 10^5-element XOR lists, 3 * 10^4 numbers for maximum XOR, C(20, 10) combinations, 9-queens, a 2000-cell board for the iterative search) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems, named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part12_sources.md). Searches returned backtracking pattern guides (techinterview.org, designgurus, a DEV Community post) that group subsets, permutations, combination sum, N-Queens, Sudoku and word search, trie pattern guides (techinterview.org: autocomplete, word search II, wildcard search, replace words, maximum XOR) and bit manipulation lists (Techie Delight, Interview Cake, Interview Kickstart, a Devinterview GitHub list, a Teamblind thread); nothing was found tying any single item to a named company, so 'Asked at' tags name source types, not verified company reports, and no India-specific company report was found for this part. Items such as the skip list, expression add operators, map sum, single number II and the sum of two integers come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page; that `int.bit_count` first appeared in Python 3.10 is editor knowledge and was not checked against documentation. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

### Q1 ⭐⭐⭐ 🟢 Single number. `nums` has an odd number of integers (1 <= len <= 10^5, any sign): every value appears exactly twice except one value that appears once. Return that value in O(n) time and O(1) extra space. Explain which three properties of XOR make a plain left-to-right XOR work (a ^ a = 0, a ^ 0 = a, commutative and associative), and why a hash-set or Counter solution is correct but uses O(n) space. Also state why Python needs no masking here (integers are arbitrary precision and negative values XOR correctly). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter-based brute force on small inputs. Example: nums=[6, 3, 9, 3, 6] -> 9; nums=[7] -> 7; nums=[-3, -3, 5] -> 5; nums=[0, 1, 0] -> 1; nums=[-8, 2, 2, -8, -1] -> -1.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation (bit manipulation). Pairs cancel, the odd one out is left.

**Say this first (1 line):** "XOR everything. a ^ a = 0 and a ^ 0 = a, XOR is commutative and associative, so every pair cancels and the single value survives. O(n) time, O(1) space."

**Brute force:** Count with a `Counter` (or toggle values in a set) and return the key with count 1. Correct, O(n) time, but O(n) extra space. Sorting and scanning pairs is O(n log n) time.

**Optimal:**
- Keep one running value `x = 0` and do `x ^= v` for every value.
- Three properties make this work:
  - `a ^ a = 0`: two equal values wipe each other out.
  - `a ^ 0 = a`: zero is the identity, so the start value and the cancelled pairs add nothing.
  - Commutative and associative: the order and the grouping do not matter, so we may mentally regroup the list as (all pairs together) ^ (the single one), even though the pairs are not next to each other.
- Result: `(a ^ a) ^ (b ^ b) ^ ... ^ s = 0 ^ ... ^ s = s`.
- Why not masking: Python ints are arbitrary precision. A negative number behaves like an infinite string of leading 1 bits (two's complement), so `-3 ^ -3 == 0` and `-8 ^ 2 ^ 2 == -8` with no overflow and no `& 0xFFFFFFFF`. I ran both on Python 3.13 (output below). In C or Java the same loop works on fixed width; here you simply do not need a mask.

**Complexity:** Time O(n), one pass. Space O(1) (one int; the values are small, so one int is constant size). The hash-set or Counter version is also correct but stores up to about n/2 + 1 distinct values: O(n) space.

**Dry run:** `[6, 3, 9, 3, 6]`. In binary: 6 = 0110, 3 = 0011, 9 = 1001.
- x = 0 ^ 6 = 0110 (6)
- ^ 3 = 0101 (5)
- ^ 9 = 1100 (12)
- ^ 3 = 1111 (15). The 3 came back, so its bits are restored on top of 9 and 6.
- ^ 6 = 1001 (9). Answer 9.

**Code:**
```python
import random
from collections import Counter

random.seed(1201)

def single_xor(nums):
    x = 0
    for v in nums:
        x ^= v          # a ^ a = 0, 0 ^ b = b; order does not matter
    return x

def single_counter(nums):          # brute force: O(n) extra space
    return next(k for k, c in Counter(nums).items() if c == 1)

def single_set(nums):              # another O(n)-space version: toggle membership
    seen = set()
    for v in nums:
        seen.symmetric_difference_update({v})
    return next(iter(seen))

examples = [([6, 3, 9, 3, 6], 9), ([7], 7), ([-3, -3, 5], 5), ([0, 1, 0], 1), ([-8, 2, 2, -8, -1], -1)]
for nums, want in examples:
    got = single_xor(nums)
    assert got == want == single_counter(nums) == single_set(nums)
    print(nums, '->', got)

# dry run trace of the first example
x = 0
for v in [6, 3, 9, 3, 6]:
    x ^= v
    print(f'  x ^= {v:>2} -> {x:>2}  ({x:04b})')

# seeded cross-check: 3000 random inputs, negatives included, big magnitudes included
for _ in range(3000):
    pairs = random.sample(range(-50, 50), random.randint(0, 6))
    odd = random.choice([v for v in range(-60, 60) if v not in pairs] + [10**12, -10**12])
    nums = [odd] + pairs * 2
    random.shuffle(nums)
    assert single_xor(nums) == single_counter(nums) == odd
print('random cross-check ok: 3000 cases')

# Python specifics: no mask needed, negatives XOR like infinite two's complement
assert -3 ^ -3 == 0 and -3 ^ 0 == -3 and (-8 ^ 2) ^ 2 == -8
assert single_xor([-(2**70), 5, 5]) == -(2**70)
print('-8 ^ 2 =', -8 ^ 2, ' (-8 ^ 2) ^ 2 =', (-8 ^ 2) ^ 2)
print('big:', single_xor([2**100, 7, 2**100, 7, -(2**90)]) == -(2**90))
print('edge asserts ok')
```

**Output (my run):**
```
[6, 3, 9, 3, 6] -> 9
[7] -> 7
[-3, -3, 5] -> 5
[0, 1, 0] -> 1
[-8, 2, 2, -8, -1] -> -1
  x ^=  6 ->  6  (0110)
  x ^=  3 ->  5  (0101)
  x ^=  9 -> 12  (1100)
  x ^=  3 -> 15  (1111)
  x ^=  6 ->  9  (1001)
random cross-check ok: 3000 cases
-8 ^ 2 = -6  (-8 ^ 2) ^ 2 = -8
big: True
edge asserts ok
```

**Edge cases:**
- Single element `[7]` returns 7.
- Negatives and zero: `[-3, -3, 5]`, `[0, 1, 0]` (a 0 pair cancels like any other).
- Huge magnitudes (I tested 10**12 and 2**100): no overflow in Python.
- Input is guaranteed to have exactly one single value. If it may have none or two, XOR gives garbage (XOR of the two, see the follow-up).

**Follow-ups:**
- Two single values (Single number III, Q16): XOR gives a ^ b; split by a set bit of it.
- Every value three times except one (Q28): bit-by-bit count mod 3; XOR alone fails.
- Why does a hash set solution not violate the question? It does not: it is correct, only O(n) space. The interviewer asks for O(1).

**Common mistakes:**
- Adding a `& 0xFFFFFFFF` "to be safe" and then returning a large positive number for a negative answer.
- Using `sum(set(nums)) * 2 - sum(nums)`: correct but O(n) space for the set and can be called out; also not an XOR answer.
- Assuming the pairs must be adjacent. XOR does not care about order.

### Q2 ⭐⭐⭐ 🟢 Number of 1 bits. `n` is an integer with 0 <= n < 2^32. Return `[popcount, naive_iterations, kernighan_iterations]`: the number of 1 bits in `n`; the number of times the loop `while m: m >>= 1` runs (examining one bit per round, starting from m = n); and the number of times the loop `while m: m &= m - 1` runs. Explain why `m & (m - 1)` clears exactly the lowest set bit, why the Kernighan loop count equals the popcount, and why the naive count equals `n.bit_length()`. Also compare with `bin(n).count('1')` and `int.bit_count()` (added in Python 3.10; on older versions it does not exist) and say which one you would write in an interview and why you still need to know the loop. In the answer include a dry run on the first example and a seeded random cross-check of your solution against bin(n).count('1') and n.bit_length() on small inputs. Example: n=11 -> [3, 4, 3]; n=0 -> [0, 0, 0]; n=2147483648 -> [1, 32, 1]; n=4294967295 -> [32, 32, 32]; n=1 -> [1, 1, 1].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit counting with the lowest-set-bit trick (Brian Kernighan).

**Say this first (1 line):** "m & (m - 1) clears exactly the lowest set bit, so looping until m is 0 runs once per set bit. Shift-and-test runs once per bit position up to the highest set bit, which is bit_length. Return [popcount, naive, kernighan]."

**Brute force:** Shift right one bit at a time and test the low bit (or `bin(n).count('1')`). The loop `while m: m >>= 1` runs `bit_length` times: up to 32 for a 32-bit input.

**Optimal:**
- Kernighan: `m &= m - 1` per round. Subtracting 1 flips the lowest set bit to 0 and every 0 below it to 1; the bits above are unchanged. AND-ing with the original keeps the bits above, and the flipped region becomes all 0 (the lowest set bit was 1 in m but 0 in m - 1, and the lower bits were 0 in m). So exactly one set bit disappears per round.
- So the iteration count equals the popcount: each round removes one set bit and nothing else, and the loop stops at 0.
- Naive count: `m >>= 1` drops the lowest bit each time, and m reaches 0 exactly when all `bit_length` bits are gone. So the count is `n.bit_length()` (0 for n = 0).
- Compare: `bin(n).count('1')` is simple and fine. `int.bit_count()` is the one I write in an interview: it is a one-call popcount, written in C. It was added in Python 3.10 (editor knowledge, not checked against the docs); on an older version it raises AttributeError. I ran it on 3.13 and it matches in every test below. I still need the loop: interviewers ask "do it without the built-in", and the loop is the base of other tricks (power of two is `n & (n - 1) == 0`).
- Python note: the input is 0 <= n < 2**32 for a reason. For a negative number both loops never terminate, because Python ints have infinitely many leading 1 bits (shown capped at 100 rounds below). If you must handle negatives, mask first: `n & 0xFFFFFFFF`.

**Complexity:** Naive: O(bit_length), at most 32 rounds. Kernighan: O(popcount), at most 32 rounds, best on sparse numbers. Space O(1). With a fixed 32-bit bound both are O(1); the difference matters for sparse or big values (for example 2**1000 + 1 needs 2 Kernighan rounds, about 1000 naive rounds).

**Dry run:** `n = 11 = 1011`.
- m = 1011, m - 1 = 1010, m & (m - 1) = 1010 (lowest 1 gone). Round 1.
- m = 1010, m - 1 = 1001, AND = 1000. Round 2.
- m = 1000, m - 1 = 0111, AND = 0000. Round 3. Stop. Popcount 3.
- The shift loop: 1011 -> 101 -> 10 -> 1 -> 0, 4 rounds = bit_length. Result `[3, 4, 3]`.

**Code:**
```python
import random

random.seed(1202)

def naive_loop(n):
    m, it = n, 0
    while m:
        m >>= 1
        it += 1
    return it

def kernighan_loop(n):
    m, it = n, 0
    while m:
        m &= m - 1       # clears the lowest set bit
        it += 1
    return it

def solve(n):
    k = kernighan_loop(n)
    return [k, naive_loop(n), k]    # popcount == kernighan iterations

def brute(n):
    s = bin(n)[2:]
    return [s.count('1'), len(s) if n else 0, s.count('1')]

examples = [(11, [3, 4, 3]), (0, [0, 0, 0]), (2147483648, [1, 32, 1]), (4294967295, [32, 32, 32]), (1, [1, 1, 1])]
for n, want in examples:
    assert solve(n) == want == brute(n)
    print(n, '->', solve(n))

# dry run of n = 11 = 0b1011
m = 11
while m:
    print(f'  m={m:04b}  m-1={m-1:04b}  m&(m-1)={m & (m-1):04b}')
    m &= m - 1

# seeded cross-check against bin().count and bit_length (and int.bit_count, present on this Python 3.13)
for _ in range(5000):
    n = random.choice([random.randrange(2**32), random.randrange(40), 2**random.randrange(32), 2**random.randrange(1, 33) - 1])
    r = solve(n)
    assert r == brute(n)
    assert r[0] == bin(n).count('1') == n.bit_count()
    assert r[1] == n.bit_length()
print('random cross-check ok: 5000 cases')
# exhaustive on 0..2**16
for n in range(2**16):
    assert solve(n) == brute(n) and n.bit_length() == solve(n)[1] and n.bit_count() == solve(n)[0]
print('exhaustive 0..65535 ok')

# why the 0 <= n < 2**32 bound matters: both loops never end for negative n in Python.
# Bounded demonstration (stop after 100 rounds):
def rounds_capped(n, step, cap=100):
    m, it = n, 0
    while m and it < cap:
        m = step(m); it += 1
    return it, m
print('naive on -1, capped at 100:', rounds_capped(-1, lambda m: m >> 1))
print('kernighan on -1, capped at 100:', rounds_capped(-1, lambda m: m & (m - 1)))
print('masked version of -1 :', kernighan_loop(-1 & 0xFFFFFFFF))
print('edge asserts ok')
```

**Output (my run):**
```
11 -> [3, 4, 3]
0 -> [0, 0, 0]
2147483648 -> [1, 32, 1]
4294967295 -> [32, 32, 32]
1 -> [1, 1, 1]
  m=1011  m-1=1010  m&(m-1)=1010
  m=1010  m-1=1001  m&(m-1)=1000
  m=1000  m-1=0111  m&(m-1)=0000
random cross-check ok: 5000 cases
exhaustive 0..65535 ok
naive on -1, capped at 100: (100, -1)
kernighan on -1, capped at 100: (100, -1267650600228229401496703205376)
masked version of -1 : 32
edge asserts ok
```

**Edge cases:**
- n = 0: both loops run 0 times, popcount 0.
- n = 2**31 (a single high bit): 1 Kernighan round, 32 naive rounds. This is the case that shows the difference.
- n = 2**32 - 1 (all ones): all three numbers are 32.
- Negative input: infinite loop (shown capped). Mask to 32 bits first if the contract allows negatives.

**Follow-ups:**
- Power of two (Q12)? `n > 0 and n & (n - 1) == 0` (one set bit).
- Count set bits for 0..n? DP: `bits[i] = bits[i >> 1] + (i & 1)`, or `bits[i & (i - 1)] + 1`.
- Hamming distance of two numbers (Q13)? `(x ^ y).bit_count()`.

**Common mistakes:**
- Writing `m & m - 1`: precedence is fine in Python (`-` binds tighter than `&`), but it reads as a bug, so use brackets.
- Looping `for _ in range(32)` and testing `(n >> i) & 1` and calling that Kernighan.
- Running either loop on a negative number.
- Claiming `bit_count` exists "in all Python 3": it does not before 3.10.

### Q3 ⭐⭐⭐ 🟡 Implement a trie (prefix tree) over lowercase words. `ops` is a list of operations (1 <= len <= 3*10^4), each `['insert', w]`, `['search', w]` or `['startsWith', p]` with 1 <= len(w), len(p) <= 20. Return one result per operation in order: `null` (Python None) for insert, True or False for search (True only if exactly that whole word was inserted before) and True or False for startsWith (True if some inserted word begins with p, including a word equal to p). Duplicate inserts are allowed and change nothing. Build nodes as dicts of children plus an end-of-word flag, and compare with a list of 26 children per node. State the cost of each operation in terms of the word length L (not the number of words). Part 7 Q41 builds a trie at concept level to count words per prefix; here you write the full insert, search and prefix API as a reusable class. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain set of inserted words with `startswith` on small inputs. Example: ops=[['insert', 'apple'], ['search', 'apple'], ['search', 'app'], ['startsWith', 'app'], ['insert', 'app'], ['search', 'app']] -> [null, True, False, True, null, True]; ops=[['startsWith', 'a']] -> [False]; ops=[['insert', 'to'], ['insert', 'to'], ['search', 't'], ['startsWith', 'to'], ['startsWith', 'top']] -> [null, null, False, True, False].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie (prefix tree). Shared prefixes share nodes, so cost depends on the word length, not on the number of words.

**Say this first (1 line):** "Each node maps a letter to a child and has an end-of-word flag. insert, search and startsWith all walk one node per letter: O(L) time each, independent of how many words are stored. search needs the flag, startsWith does not."

**Brute force:** Keep a set of words. search is O(L) (hash), but startsWith must scan all words with `startswith`: O(N * L). Sorting the words and using bisect makes prefix queries O(L log N) but insertions O(N) in a list.

**Optimal:**
- Node = children map + `is_end`. The root represents the empty string.
- insert(w): walk from the root, create missing children, set `is_end = True` on the last node. A duplicate insert walks existing nodes and sets the flag to True again: no change.
- search(w): walk; if a letter is missing return False; at the end return `is_end`. So 'app' is not found after inserting only 'apple' (the node exists but is_end is False).
- startsWith(p): walk; return True if you reach a node, ignoring the flag. A word equal to p counts, because that node exists.
- Node representations:
  - dict of children: only the letters actually used are stored, any alphabet, small for sparse tries.
  - list of 26: O(1) index with no hashing and no key objects, but 26 pointers per node even if only one child is used, and it only works for lowercase letters.
  - In my run (sandbox only, `sys.getsizeof` summed over node containers, so a rough guide) 1000 random 8-letter words gave about 6500 nodes, about 1.56 MB with dicts and 2.04 MB with 26-slot lists. Random words share little, and the dict trie was still smaller. For dense tries on a small alphabet the list can win on speed.

**Complexity:** insert, search and startsWith are O(L) time each, where L is the length of the word or prefix (at most 20). Space O(total letters in the distinct words) nodes in the worst case, times the node size: dict nodes are proportional to the children present, list nodes are 26 slots each. Total time for q operations: O(q * L).

**Dry run:** first example. insert 'apple' creates a -> p -> p -> l -> e, `e.is_end = True`. search 'apple': walk 5 nodes, flag True, so True. search 'app': node exists but flag False, so False. startsWith 'app': reaches the node, True. insert 'app': flag on the third node set. search 'app': True. Output `[None, True, False, True, None, True]` (`null` is Python None). The program also prints the node chain after inserting apple and app: 'app' and 'apple' end flags are True, 'a', 'ap', 'appl' are False.

**Code:**
```python
import random
import sys

random.seed(1203)

class TrieDict:
    """Nodes are dicts: children by letter; the key '$' is NOT used, the flag is a separate tuple slot."""
    __slots__ = ('root',)
    def __init__(self):
        self.root = [{}, False]            # [children, is_end]
    def insert(self, w):
        node = self.root
        for ch in w:
            nxt = node[0].get(ch)
            if nxt is None:
                nxt = node[0][ch] = [{}, False]
            node = nxt
        node[1] = True                      # duplicate insert just sets True again
    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node[0].get(ch)
            if node is None:
                return None
        return node
    def search(self, w):
        node = self._walk(w)
        return node is not None and node[1]
    def startsWith(self, p):
        return self._walk(p) is not None

class TrieArray:
    """Same API, 26-slot list per node (lowercase only)."""
    __slots__ = ('kids', 'end')
    def __init__(self):
        self.kids = [None] * 26
        self.end = False
    def insert(self, w):
        node = self
        for ch in w:
            i = ord(ch) - 97
            if node.kids[i] is None:
                node.kids[i] = TrieArray()
            node = node.kids[i]
        node.end = True
    def _walk(self, s):
        node = self
        for ch in s:
            node = node.kids[ord(ch) - 97]
            if node is None:
                return None
        return node
    def search(self, w):
        node = self._walk(w)
        return node is not None and node.end
    def startsWith(self, p):
        return self._walk(p) is not None

def run(ops, cls=TrieDict):
    t, out = cls(), []
    for op, arg in ops:
        if op == 'insert':
            t.insert(arg); out.append(None)
        elif op == 'search':
            out.append(t.search(arg))
        else:
            out.append(t.startsWith(arg))
    return out

def brute(ops):                      # plain set + startswith
    words, out = set(), []
    for op, arg in ops:
        if op == 'insert':
            words.add(arg); out.append(None)
        elif op == 'search':
            out.append(arg in words)
        else:
            out.append(any(w.startswith(arg) for w in words))
    return out

examples = [
    ([['insert', 'apple'], ['search', 'apple'], ['search', 'app'], ['startsWith', 'app'], ['insert', 'app'], ['search', 'app']],
     [None, True, False, True, None, True]),
    ([['startsWith', 'a']], [False]),
    ([['insert', 'to'], ['insert', 'to'], ['search', 't'], ['startsWith', 'to'], ['startsWith', 'top']],
     [None, None, False, True, False]),
]
for ops, want in examples:
    for cls in (TrieDict, TrieArray):
        assert run(ops, cls) == want == brute(ops)
    print(run(ops))

# dry run: structure after inserting apple then app
t = TrieDict(); t.insert('apple'); t.insert('app')
node, path = t.root, ''
while node[0]:
    ch = next(iter(node[0])); node = node[0][ch]; path += ch
    print(f'  node {path!r:8} end={node[1]}')

# seeded random cross-check
for _ in range(2000):
    ops = [[random.choice(['insert', 'search', 'startsWith']), ''.join(random.choice('abc') for _ in range(random.randint(1, 4)))]
           for _ in range(random.randint(1, 30))]
    want = brute(ops)
    assert run(ops, TrieDict) == want and run(ops, TrieArray) == want
print('random cross-check ok: 2000 cases')

# edge cases: length-20 words, whole alphabet, prefix equal to a word
w = 'z' * 20
assert run([['insert', w], ['search', w], ['startsWith', w[:7]], ['search', w[:7]]]) == [None, True, True, False]
alpha = 'abcdefghijklmnopqrstuvwxyz'
assert run([['insert', alpha], ['startsWith', alpha[:13]], ['startsWith', alpha[:13] + 'z']], TrieArray) == [None, True, False]

# memory comparison for 1000 random 8-letter words (sys.getsizeof counts only the container itself: a rough guide)
words = [''.join(random.choice(alpha) for _ in range(8)) for _ in range(1000)]
td, ta = TrieDict(), TrieArray()
for x in words:
    td.insert(x); ta.insert(x)
def size_dict(node):
    return sys.getsizeof(node) + sys.getsizeof(node[0]) + sum(size_dict(c) for c in node[0].values())
def size_arr(node):
    return sys.getsizeof(node) + sys.getsizeof(node.kids) + sum(size_arr(c) for c in node.kids if c)
def count(node):
    return 1 + sum(count(c) for c in node[0].values())
print('nodes:', count(td.root), ' dict-trie bytes:', size_dict(td.root), ' array-trie bytes:', size_arr(ta))
print('edge asserts ok')
```

**Output (my run):**
```
[None, True, False, True, None, True]
[False]
[None, None, False, True, False]
  node 'a'      end=False
  node 'ap'     end=False
  node 'app'    end=True
  node 'appl'   end=False
  node 'apple'  end=True
random cross-check ok: 2000 cases
nodes: 6531  dict-trie bytes: 1563528  array-trie bytes: 2037672
edge asserts ok
```

**Edge cases:**
- search for a proper prefix of an inserted word is False; startsWith is True.
- A prefix longer than any word (startsWith 'top' after 'to') is False.
- Duplicate inserts change nothing.
- Length 20 words, and the full alphabet `abcdefghijklmnopqrstuvwxyz` as one word.
- Never share a mutable default child dict between nodes (see mistakes).

**Follow-ups:**
- Delete a word? Clear the flag, then walk back and remove nodes that have no children and no flag.
- Autocomplete with counts or top-k? Store a count (or a cached top-k list) per node; writes cost more, reads become O(L).
- Why not a hash set of all prefixes? That is O(L^2) space per word and does not help with enumeration.

**Common mistakes:**
- Returning True from search when only the node exists (forgetting `is_end`): then 'app' would be found after inserting 'apple'.
- Making startsWith check the flag.
- `children = {}` as a class-level or default-argument attribute, so all nodes share one dict.
- Stating the cost as O(N) or O(number of words); it is O(L).

### Q4 ⭐⭐⭐ 🟡 Subsets (power set) of distinct integers. `nums` has 0 <= len <= 10 distinct integers in any order. Return every subset exactly once. Each subset is a list that keeps the relative order of `nums`; the outer list must be sorted ascending with Python's list comparison (so the empty list comes first and `[1]` comes before `[1, 2]`). `nums = []` returns `[[]]`. Solve it with the include-or-exclude recursion and say how many leaves it has (2^n) and why the total work is O(n * 2^n). Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a bitmask loop over 0..2^n - 1 on small inputs. Example: nums=[4, 1, 7] -> [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]; nums=[] -> [[]]; nums=[5] -> [[], [5]]; nums=[3, 1] -> [[], [1], [3], [3, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking, include-or-exclude (choose, explore, undo). One binary decision per element.

**Say this first (1 line):** "At each index I either skip the element or take it, then recurse on the next index. That is a binary tree of depth n with 2^n leaves, each leaf is one subset, and copying a leaf costs O(n), so O(n * 2^n) overall."

**Brute force:** Loop `mask` from 0 to 2^n - 1 and build the subset from the set bits. Same O(n * 2^n), no recursion, and it is the oracle in the cross-check. Sorting the outer list at the end costs O(2^n * n log 2^n) comparisons of lists, fine for n <= 10.

**Optimal:**
- `go(i)`: if `i == n`, append a copy of `cur`. Otherwise: first go(i+1) without nums[i] (exclude), then `cur.append(nums[i])`, `go(i+1)`, `cur.pop()` (include, then undo).
- The undo `cur.pop()` restores `cur` so the sibling branch starts clean. Append `cur[:]`, not `cur`, or every answer becomes the same list that ends up empty.
- Each subset keeps the order of `nums` because we decide elements left to right.
- The outer list is sorted at the end with Python's list comparison: `[]` < `[1]` < `[1, 7]` < `[4]` ...
- Pruning rule: there is none. Every branch ends in a valid answer, so there is nothing to cut. The only saving is the start-index variant, where every node (not only the leaf) is an answer: it makes 2^n calls instead of 2^(n+1) - 1. Measured below for n = 0..10: include/exclude makes exactly 2^(n+1) - 1 calls (2047 for n = 10), the start-index version exactly 2^n (1024).
- Recursion depth is n <= 10 frames plus one, far below CPython's default limit of 1000.

**Complexity:** 2^n leaves; each leaf copies a list of up to n items. Time O(n * 2^n) (calls are 2^(n+1) - 1, the copying dominates). Extra space O(n) for the recursion and `cur`, plus the output itself, which is O(n * 2^n) (average n/2 items per subset).

**Dry run:** `nums = [4, 1]` (the program prints the full tree).
- at 4: exclude -> at 1: exclude -> leaf `[]`; include -> leaf `[1]`.
- at 4: include -> at 1: exclude -> leaf `[4]`; include -> leaf `[4, 1]`.
- For `[4, 1, 7]` the same tree has 8 leaves. After sorting: `[[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]`.

**Code:**
```python
import random

random.seed(1204)

def subsets_inc_exc(nums):
    """Include-or-exclude: one yes/no decision per element. Returns (sorted result, number of calls)."""
    out, cur, calls = [], [], [0]
    def go(i):
        calls[0] += 1
        if i == len(nums):
            out.append(cur[:])             # copy: cur keeps changing
            return
        go(i + 1)                           # exclude nums[i]
        cur.append(nums[i])                 # choose
        go(i + 1)                           # explore
        cur.pop()                           # undo
    go(0)
    return sorted(out), calls[0]

def subsets_start_index(nums):
    """Start-index version: every node is an answer, so only 2^n calls."""
    out, cur, calls = [], [], [0]
    def go(start):
        calls[0] += 1
        out.append(cur[:])
        for j in range(start, len(nums)):
            cur.append(nums[j]); go(j + 1); cur.pop()
    go(0)
    return sorted(out), calls[0]

def brute(nums):                           # bitmask loop
    n = len(nums)
    return sorted([nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n))

examples = [([4, 1, 7], [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]), ([], [[]]), ([5], [[], [5]]), ([3, 1], [[], [1], [3], [3, 1]])]
for nums, want in examples:
    assert subsets_inc_exc(nums)[0] == want == brute(nums) == subsets_start_index(nums)[0]
    print(nums, '->', subsets_inc_exc(nums)[0])

# decision tree for [4, 1] (E = exclude, I = include); leaf = subset
def tree(nums, i=0, cur=(), depth=0):
    pad = '  ' * depth
    if i == len(nums):
        print(f'{pad}leaf {list(cur)}'); return
    print(f'{pad}at {nums[i]}:')
    print(f'{pad} exclude'); tree(nums, i + 1, cur, depth + 1)
    print(f'{pad} include'); tree(nums, i + 1, cur + (nums[i],), depth + 1)
tree([4, 1])

# call counts: 2^(n+1)-1 for include/exclude, 2^n for start-index; there is nothing to prune (every leaf is an answer)
for n in range(0, 11):
    nums = list(range(n))
    assert subsets_inc_exc(nums)[1] == 2 ** (n + 1) - 1
    assert subsets_start_index(nums)[1] == 2 ** n
    assert len(subsets_inc_exc(nums)[0]) == 2 ** n
print('calls for n=10: include/exclude', subsets_inc_exc(list(range(10)))[1], ' start-index', subsets_start_index(list(range(10)))[1])

# seeded cross-check
for _ in range(1500):
    nums = random.sample(range(-9, 10), random.randint(0, 8))
    r = subsets_inc_exc(nums)[0]
    assert r == brute(nums) == subsets_start_index(nums)[0]
    assert len(r) == 2 ** len(nums) and len({tuple(s) for s in r}) == len(r)
print('random cross-check ok: 1500 cases')

# edge: negative and unordered input; n = 10 gives 1024 subsets
assert subsets_inc_exc([-1, 0])[0] == [[], [-1], [-1, 0], [0]]
assert len(subsets_inc_exc(list(range(10)))[0]) == 1024
print('edge asserts ok')
```

**Output (my run):**
```
[4, 1, 7] -> [[], [1], [1, 7], [4], [4, 1], [4, 1, 7], [4, 7], [7]]
[] -> [[]]
[5] -> [[], [5]]
[3, 1] -> [[], [1], [3], [3, 1]]
at 4:
 exclude
  at 1:
   exclude
    leaf []
   include
    leaf [1]
 include
  at 1:
   exclude
    leaf [4]
   include
    leaf [4, 1]
calls for n=10: include/exclude 2047  start-index 1024
random cross-check ok: 1500 cases
edge asserts ok
```

**Edge cases:**
- `[]` returns `[[]]` (one empty subset), not `[]`.
- One element: `[[], [5]]`.
- Negative or unordered input: the elements are in input order inside each subset, only the outer list is sorted.
- n = 10 gives 1024 subsets, which the code asserts.

**Follow-ups:**
- Duplicates in the input (Q18): sort, then skip a value equal to the previous one at the same level.
- Return subsets of size k only (Q20): add a length bound and prune when too few elements remain.
- Count the subsets that sum to a target: that is the knapsack DP (Parts 10 and 11 own counting); here we list them.

**Common mistakes:**
- Appending `cur` instead of `cur[:]`.
- Forgetting the undo, so `cur` keeps growing.
- Returning `[]` for empty input.
- Saying the work is O(2^n): the copying makes it O(n * 2^n).

### Q5 ⭐⭐⭐ 🟡 Letter combinations of a phone number. `digits` is a string (0 <= len <= 6) of characters from '2' to '9' on a phone keypad (2 abc, 3 def, 4 ghi, 5 jkl, 6 mno, 7 pqrs, 8 tuv, 9 wxyz). Return every string you can type, one letter per digit, in ascending alphabetical order (which is the order a recursion that tries letters in keypad order produces). An empty `digits` returns an empty list (not `['']`). State the number of results as the product of the key sizes (3 or 4 per digit, at most 4^6 = 4096) and the cost of building each string. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.product over the key letters on small inputs. Example: digits='27' -> ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']; digits='9' -> ['w', 'x', 'y', 'z']; digits='' -> []; digits='78' -> ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over a product of choices: one letter per digit, a fixed-depth tree.

**Say this first (1 line):** "Recurse digit by digit, try each letter of that key in keypad order, undo after. Letters in keypad order give ascending output for free. Results are the product of the key sizes, at most 4^6 = 4096, and each string costs O(L) to build."

**Brute force:** `itertools.product(*keys)` and join. Same count, no recursion. That is the oracle in the cross-check. Naive string concatenation at each level also works but copies prefixes.

**Optimal:**
- `go(i)`: if `i == len(digits)`, join `cur` and append. Else for each letter in `KEYS[digits[i]]` in order: `cur.append(ch)`, `go(i + 1)`, `cur.pop()`.
- Keys are stored in alphabetical order, and the first digit is the most significant "digit" of the result, so the output comes out sorted: no final sort needed. The tests check this against a sorted `itertools.product` result.
- Empty `digits` returns `[]`, not `['']`: special-case it first (otherwise the recursion would hit the leaf at once and return one empty string).
- Pruning rule: none exists. Every path of length L is an answer, so the tree has no dead end. The call count is 1 + k1 + k1*k2 + ... + (k1*...*kL), shown below (for '999999' it is 5461 calls for 4096 results, so the internal nodes add only about 33 per cent).
- Recursion depth is L <= 6.

**Complexity:** Results R = product of the key sizes (3 or 4 each), at most 4096. Each result is a string of L characters built with `join`: O(L). Time O(L * R) (plus the calls, which are O(R) in total because the tree is bushy). Space O(L) for the recursion and `cur`, plus the output O(L * R).

**Dry run:** `'27'`. Level 0 digit 2 ('abc'): choose 'a'. Level 1 digit 7 ('pqrs'): choose p, q, r, s, producing `ap aq ar as`. Undo to the prefix `''`, choose 'b', again four leaves, then 'c'. 3 * 4 = 12 results, in the order shown. The program prints the first lines of this tree.

**Code:**
```python
import itertools
import random

random.seed(1205)
KEYS = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}

def letter_combos(digits):
    """Returns (list in ascending order, number of recursive calls)."""
    if not digits:
        return [], 1                        # empty input -> [] (not [''])
    out, cur, calls = [], [], [0]
    def go(i):
        calls[0] += 1
        if i == len(digits):
            out.append(''.join(cur))        # O(L) to build each string
            return
        for ch in KEYS[digits[i]]:          # keypad order => ascending output
            cur.append(ch)                  # choose
            go(i + 1)                       # explore
            cur.pop()                       # undo
    go(0)
    return out, calls[0]

def brute(digits):
    if not digits:
        return []
    return sorted(''.join(p) for p in itertools.product(*(KEYS[d] for d in digits)))

examples = [('27', ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']),
            ('9', ['w', 'x', 'y', 'z']), ('', []),
            ('78', ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv'])]
for d, want in examples:
    assert letter_combos(d)[0] == want == brute(d)
    print(repr(d), '->', letter_combos(d)[0])

# decision tree for '9' then '2' is wide; show the tree for '27' as calls with depth (first 8 lines)
lines = []
def show(i, cur, digits='27'):
    if i == len(digits):
        lines.append('  ' * i + 'leaf ' + cur); return
    lines.append('  ' * i + f'digit {digits[i]} ({KEYS[digits[i]]}), prefix {cur!r}')
    for ch in KEYS[digits[i]]:
        show(i + 1, cur + ch, digits)
show(0, '')
print('\n'.join(lines[:9])); print('  ...', len(lines), 'lines in all')

# no pruning exists: every path of length L is an answer. Calls = 1 + k1 + k1*k2 + ...
def expected_calls(digits):
    total, prod = 1, 1
    for d in digits:
        prod *= len(KEYS[d]); total += prod
    return total
for d in ['', '2', '27', '7979', '999999', '234567']:
    r, c = letter_combos(d)
    assert c == (1 if not d else expected_calls(d))
    print(f'digits={d!r:10} results={len(r):5} calls={c}')

# seeded cross-check
for _ in range(2000):
    d = ''.join(random.choice('23456789') for _ in range(random.randint(0, 5)))
    assert letter_combos(d)[0] == brute(d)
print('random cross-check ok: 2000 cases')

# edge: max size 4^6 = 4096 results, all of length 6, sorted and distinct
r = letter_combos('777777')[0]
assert len(r) == 4096 and r == sorted(set(r)) and all(len(s) == 6 for s in r)
assert letter_combos('')[0] == [] and letter_combos('2')[0] == ['a', 'b', 'c']
print('edge asserts ok')
```

**Output (my run):**
```
'27' -> ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']
'9' -> ['w', 'x', 'y', 'z']
'' -> []
'78' -> ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv']
digit 2 (abc), prefix ''
  digit 7 (pqrs), prefix 'a'
    leaf ap
    leaf aq
    leaf ar
    leaf as
  digit 7 (pqrs), prefix 'b'
    leaf bp
    leaf bq
  ... 16 lines in all
digits=''         results=    0 calls=1
digits='2'        results=    3 calls=4
digits='27'       results=   12 calls=16
digits='7979'     results=  256 calls=341
digits='999999'   results= 4096 calls=5461
digits='234567'   results=  972 calls=1336
random cross-check ok: 2000 cases
edge asserts ok
```

**Edge cases:**
- `''` returns `[]`.
- A single digit returns that key's letters, in order.
- '7' and '9' have four letters; '777777' gives 4096 strings, all distinct and sorted (asserted).
- Input never contains '0' or '1' by the prompt. If it could, you would have to define what they mean.

**Follow-ups:**
- Iterative version: start with `['']` and for each digit replace the list with every `p + ch`. Same output order, O(R * L) time, no recursion.
- Count only: the product of key sizes, no enumeration.
- Dictionary words only: prune a prefix that is not in a trie (Q11 uses this idea).

**Common mistakes:**
- Returning `['']` for empty input.
- Using a list for `cur` and forgetting `cur.pop()` (passing an immutable string `prefix + ch` down needs no undo, a shared list does).
- Assuming 3 letters per digit: 7 and 9 have 4.

### Q6 ⭐⭐⭐ 🟡 Permutations of distinct integers. `nums` has 0 <= len <= 8 distinct integers. Return all n! orderings, each as a list, with the outer list sorted ascending with Python's list comparison (lexicographic order by value; so the order of `nums` itself does not matter). `nums = []` returns `[[]]` (one empty permutation). Use a `used` array and say how the swap-in-place variant differs; the cost is O(n * n!). Part 1 Q34 (next permutation) steps from one permutation to the next in this same order without recursion; mention that as a follow-up. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.permutations sorted on small inputs. Example: nums=[3, 1, 2] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]; nums=[] -> [[]]; nums=[9] -> [[9]]; nums=[2, 1] -> [[1, 2], [2, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking, ordering a set: choose an unused element for each position.

**Say this first (1 line):** "Fill the positions left to right; at each position try every element not yet used, mark it, recurse, unmark. There are n! leaves and each costs O(n) to copy: O(n * n!). Sort the outer list at the end."

**Brute force:** `itertools.permutations(nums)` sorted. Or the unpruned recursion that tries all n values at every position and rejects repeats only at the leaves: n^n leaves. For n = 6 that is 55987 calls against 1957 for the used-array version (measured below).

**Optimal:**
- `used[i]` marks nums[i] as already on the path. `go()`: if `len(cur) == n`, append a copy. Else for every i not used: mark, push, recurse, pop, unmark.
- Pruning rule: skip any element that is in use. That cuts the n^n tree down to the tree that has n choices at depth 0, n-1 at depth 1, and so on. Number of calls = sum over k of n!/(n-k)!, which I checked equals 1, 2, 5, 16, 65, 326, 1957 for n = 0..6.
- Swap-in-place variant: no `used` array. Keep `a[:k]` as the fixed prefix; for each i >= k swap `a[k]` and `a[i]`, recurse on k + 1, swap back. It saves the array and the membership test but does not produce the lexicographic order, so you would still sort the result (the code does, and the cross-check compares it).
- Input order does not matter for the answer because the outer list is sorted at the end; the used-array version with input order `[3, 1, 2]` first produces `[3, 1, 2]`.
- Recursion depth is n <= 8 frames plus one.

**Complexity:** n! leaves, each a copy of n items: O(n * n!) time (the internal calls add at most a constant factor: sum of n!/(n-k)! is at most e * n!). Extra space O(n) plus the output O(n * n!). For n = 8 that is 40320 permutations.

**Dry run:** `[3, 1, 2]` (first lines of the tree are printed). place 3 -> place 1 -> place 2 -> leaf `[3, 1, 2]`; back, place 2 -> place 1 -> leaf `[3, 2, 1]`; then place 1 first: `[1, 3, 2]`, `[1, 2, 3]`; then 2 first: `[2, 3, 1]`, `[2, 1, 3]`. Six leaves in tree order; sorted: `[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]`. The `skip x (used)` lines are the pruned choices.

**Code:**
```python
import itertools
import math
import random

random.seed(1206)

def permutations_used(nums):
    """used-array version. Returns (sorted result, calls)."""
    n = len(nums); out, cur, used, calls = [], [], [False] * n, [0]
    def go():
        calls[0] += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]:
                continue                    # pruning rule: an element can be placed once
            used[i] = True; cur.append(nums[i])     # choose
            go()                                    # explore
            cur.pop(); used[i] = False              # undo
    go()
    return sorted(out), calls[0]

def permutations_swap(nums):
    """Swap-in-place variant: no used array; the prefix nums[:k] is fixed. Output order is NOT sorted, so we sort."""
    a, out, calls = list(nums), [], [0]
    def go(k):
        calls[0] += 1
        if k == len(a):
            out.append(a[:]); return
        for i in range(k, len(a)):
            a[k], a[i] = a[i], a[k]
            go(k + 1)
            a[k], a[i] = a[i], a[k]
    go(0)
    return sorted(out), calls[0]

def unpruned(nums):
    """No used check: try every element at every position, filter at the leaves. Counts calls only (n <= 6 here)."""
    n = len(nums); calls = [0]; good = [0]
    def go(seq):
        calls[0] += 1
        if len(seq) == n:
            good[0] += len(set(seq)) == n; return
        for i in range(n):
            go(seq + (i,))
    go(())
    return calls[0], good[0]

def brute(nums):
    return sorted(map(list, itertools.permutations(nums)))

examples = [([3, 1, 2], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), ([], [[]]), ([9], [[9]]), ([2, 1], [[1, 2], [2, 1]])]
for nums, want in examples:
    assert permutations_used(nums)[0] == want == brute(nums) == permutations_swap(nums)[0]
    print(nums, '->', permutations_used(nums)[0])

# decision tree for [3, 1, 2] (used-array order = input order; the final list is then sorted)
lines = []
def tree(nums, cur=(), depth=0):
    if len(cur) == len(nums):
        lines.append('  ' * depth + 'leaf ' + str(list(cur))); return
    for v in nums:
        if v in cur:
            lines.append('  ' * depth + f'skip {v} (used)'); continue
        lines.append('  ' * depth + f'place {v}')
        tree(nums, cur + (v,), depth + 1)
tree([3, 1, 2])
print('\n'.join(lines[:13])); print('  ...', len(lines), 'lines in all')

# node counts: used array = sum n!/(n-k)!, unpruned = sum n^k
for n in range(0, 7):
    calls = permutations_used(list(range(n)))[1]
    assert calls == sum(math.factorial(n) // math.factorial(n - k) for k in range(n + 1))
    un, good = unpruned(list(range(n))) if n else (1, 1)
    assert good == math.factorial(n) and un == sum(n ** k for k in range(n + 1))
    print(f'n={n} used-array calls={calls:6} unpruned calls={un:6} results={good}')

# seeded cross-check
for _ in range(1000):
    nums = random.sample(range(-9, 10), random.randint(0, 6))
    r = permutations_used(nums)[0]
    assert r == brute(nums) == permutations_swap(nums)[0]
print('random cross-check ok: 1000 cases')

# edge: n = 8 gives 40320 permutations, sorted, all distinct; sorted(nums) first, reversed last
r = permutations_used([5, 3, 8, 1, 9, 2, 7, 4])[0]
assert len(r) == 40320 and r[0] == sorted(r[0]) and r[-1] == sorted(r[0], reverse=True)
assert permutations_used([])[0] == [[]] and permutations_used([-1, 0])[0] == [[-1, 0], [0, -1]]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 1, 2] -> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
[] -> [[]]
[9] -> [[9]]
[2, 1] -> [[1, 2], [2, 1]]
place 3
  skip 3 (used)
  place 1
    skip 3 (used)
    skip 1 (used)
    place 2
      leaf [3, 1, 2]
  place 2
    skip 3 (used)
    place 1
      leaf [3, 2, 1]
    skip 2 (used)
place 1
  ... 36 lines in all
n=0 used-array calls=     1 unpruned calls=     1 results=1
n=1 used-array calls=     2 unpruned calls=     2 results=1
n=2 used-array calls=     5 unpruned calls=     7 results=2
n=3 used-array calls=    16 unpruned calls=    40 results=6
n=4 used-array calls=    65 unpruned calls=   341 results=24
n=5 used-array calls=   326 unpruned calls=  3906 results=120
n=6 used-array calls=  1957 unpruned calls= 55987 results=720
random cross-check ok: 1000 cases
edge asserts ok
```

**Edge cases:**
- `[]` returns `[[]]` (one empty permutation).
- One element returns `[[9]]`.
- Negative values: fine, the used array tracks indexes, not values.
- n = 8: 40320 lists, first one ascending, last one descending (asserted).
- Duplicates are out of scope for this prompt; with duplicates this code would print repeats (Q19 handles them).

**Follow-ups:**
- Next permutation (Part 1 Q34) steps from one permutation to the next in this same sorted order with O(1) extra space and no recursion: start at the sorted array and call it n! - 1 times.
- Duplicates (Q19): sort and skip `nums[i] == nums[i-1]` when `nums[i-1]` is not used.
- The k-th permutation without listing all: factorial number system, O(n^2).

**Common mistakes:**
- Marking by value (`if v in cur`) with duplicates, or O(n) membership tests inside the loop.
- Forgetting to unmark `used[i]` after the recursive call.
- Appending `cur` instead of a copy.
- Claiming the swap variant is lexicographic.

### Q7 ⭐⭐⭐ 🟡 Generate parentheses. `n` is an integer with 1 <= n <= 8. Return every balanced string of n pairs of '(' and ')', sorted ascending as Python strings (so '(' sorts before ')' and `'((()))'` comes first). Build them by recursion with two counters (open used, close used) and justify the two pruning rules: you may add '(' while open < n and ')' while close < open. State that the number of results is the n-th Catalan number and that no invalid prefix is ever extended (so every call leads to at least one answer). Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against filtering all 2^(2n) strings of '(' and ')' for balance on small inputs. Example: n=1 -> ['()']; n=2 -> ['(())', '()()']; n=3 -> ['((()))', '(()())', '(())()', '()(())', '()()()'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a validity invariant: only extend a prefix that can still be completed.

**Say this first (1 line):** "Build the string left to right with two counters. Add '(' while open < n. Add ')' while close < open. Those two rules keep every prefix valid, so nothing is ever thrown away. The count is the n-th Catalan number."

**Brute force:** Generate all 2^(2n) strings of '(' and ')' and keep the balanced ones. For n = 8 that is 65536 strings to test (131071 calls in the tree) for 1430 answers.

**Optimal:**
- State: `o` = '(' used, `c` = ')' used, `cur` = the string so far.
- Rule 1: add '(' only if `o < n` (we have only n pairs).
- Rule 2: add ')' only if `c < o` (there must be an unmatched '(' to close; otherwise the prefix is already unbalanced and no suffix can fix it).
- Stop when `len(cur) == 2n`; then `o == n` and `c == n`, hence balanced.
- Order: try '(' before ')'. Since '(' < ')' as characters, the leaves come out in ascending order, and the code also sorts (cheap) so the claim is by test, not trust.
- "No invalid prefix is ever extended": by induction, every prefix has `c <= o <= n`. Such a prefix can always be completed (add the missing '(' then close everything, or just close). I tested this: for n = 1..8, every prefix visited by the recursion is the prefix of at least one returned answer. So every call leads to at least one answer, and the work per answer is O(n).
- Call counts, pruned against the unpruned tree (which has 2^(2n+1) - 1 calls): n = 3: 22 against 127; n = 6: 625 against 8191; n = 8: 6917 against 131071.
- Recursion depth is 2n <= 16.

**Complexity:** Number of results is Catalan(n) = C(2n, n) / (n + 1): 1, 2, 5, 14, 42, 132, 429, 1430 for n = 1..8, checked by code. Time O(n * Catalan(n)) (every call is on a path to an answer, there are at most 2n calls per answer, and building each string costs O(n)). Asymptotically Catalan(n) ~ 4^n / (n^1.5 * sqrt(pi)). Space O(n) for the recursion plus the output.

**Dry run:** `n = 2`. The program prints the tree:
- empty -> '(' (o=1) -> '((' (o=2): '(' is blocked because o == n; ')' allowed -> '(()' -> '(())' answer.
- '(' -> '()' (o=1, c=1) -> '()(' -> '()()' answer; at '()' the ')' is blocked because c == o.
- At the root ')' is blocked because c == o == 0.
Result `['(())', '()()']`.

**Code:**
```python
import itertools
import math
import random

random.seed(1207)

def gen_parens(n):
    """Returns (sorted list, number of calls, list of every prefix visited)."""
    out, cur, calls, prefixes = [], [], [0], []
    def go(o, c):
        calls[0] += 1
        prefixes.append(''.join(cur))
        if len(cur) == 2 * n:
            out.append(''.join(cur)); return
        if o < n:                           # rule 1: may open while fewer than n opens used
            cur.append('('); go(o + 1, c); cur.pop()
        if c < o:                           # rule 2: may close only if an unmatched '(' exists
            cur.append(')'); go(o, c + 1); cur.pop()
    go(0, 0)
    return sorted(out), calls[0], prefixes

def gen_unpruned_calls(n):
    """Try '(' and ')' at every position, test balance at the leaves: calls = 2^(2n+1) - 1."""
    return 2 ** (2 * n + 1) - 1

def brute(n):
    def ok(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == '(' else -1
            if bal < 0:
                return False
        return bal == 0
    return sorted(''.join(t) for t in itertools.product('()', repeat=2 * n) if ok(t))

examples = [(1, ['()']), (2, ['(())', '()()']), (3, ['((()))', '(()())', '(())()', '()(())', '()()()'])]
for n, want in examples:
    assert gen_parens(n)[0] == want == brute(n)
    print(n, '->', gen_parens(n)[0])

# decision tree for n = 2: which branches the two rules allow
def tree(n, s='', o=0, c=0, d=0):
    if len(s) == 2 * n:
        print('  ' * d + f'{s}  (answer)'); return
    print('  ' * d + f'{s or "(empty)"}  open={o} close={c}')
    if o < n: tree(n, s + '(', o + 1, c, d + 1)
    else: print('  ' * (d + 1) + "'(' blocked: open == n")
    if c < o: tree(n, s + ')', o, c + 1, d + 1)
    else: print('  ' * (d + 1) + "')' blocked: close == open")
tree(2)

# Catalan counts, calls pruned vs unpruned, and the claim 'no dead branch': every visited prefix begins some answer
for n in range(1, 9):
    res, calls, prefixes = gen_parens(n)
    assert len(res) == math.comb(2 * n, n) // (n + 1)
    assert all(any(r.startswith(p) for r in res) for p in prefixes), 'dead branch found'
    print(f'n={n} results={len(res):5} pruned calls={calls:6} unpruned calls={gen_unpruned_calls(n):7}')
    if n <= 6:
        assert res == brute(n)

# seeded cross-check (n up to 5, plus random ids)
for _ in range(100):
    n = random.randint(1, 5)
    assert gen_parens(n)[0] == brute(n)
print('random cross-check ok: 100 cases (n in 1..5; the oracle is exhaustive)')
# edge: n = 1, n = 8 (1430 = Catalan(8)), first and last strings
r = gen_parens(8)[0]
assert len(r) == 1430 and r[0] == '(' * 8 + ')' * 8 and r[-1] == '()' * 8
assert gen_parens(1)[0] == ['()']
print('edge asserts ok')
```

**Output (my run):**
```
1 -> ['()']
2 -> ['(())', '()()']
3 -> ['((()))', '(()())', '(())()', '()(())', '()()()']
(empty)  open=0 close=0
  (  open=1 close=0
    ((  open=2 close=0
      '(' blocked: open == n
      (()  open=2 close=1
        '(' blocked: open == n
        (())  (answer)
    ()  open=1 close=1
      ()(  open=2 close=1
        '(' blocked: open == n
        ()()  (answer)
      ')' blocked: close == open
  ')' blocked: close == open
n=1 results=    1 pruned calls=     3 unpruned calls=      7
n=2 results=    2 pruned calls=     8 unpruned calls=     31
n=3 results=    5 pruned calls=    22 unpruned calls=    127
n=4 results=   14 pruned calls=    64 unpruned calls=    511
n=5 results=   42 pruned calls=   196 unpruned calls=   2047
n=6 results=  132 pruned calls=   625 unpruned calls=   8191
n=7 results=  429 pruned calls=  2055 unpruned calls=  32767
n=8 results= 1430 pruned calls=  6917 unpruned calls= 131071
random cross-check ok: 100 cases (n in 1..5; the oracle is exhaustive)
edge asserts ok
```

**Edge cases:**
- n = 1 returns `['()']`.
- n = 8: 1430 strings; the first is `'(((((((())))))))'` and the last is `'()()()()()()()()'` (asserted).
- The oracle test is exhaustive (all 2^(2n) strings for n <= 6), so the "random" loop only repeats small n; it adds no variety. I say that plainly.
- Prompt claims checked: Catalan count (n = 1..8), no dead prefix (n = 1..8): both true.

**Follow-ups:**
- Count only: Catalan DP, `C(n) = sum C(i) * C(n-1-i)`, O(n^2), no listing.
- Several bracket types: add a stack of open brackets instead of counters; the pruning changes (close only the matching top).
- Longest valid parentheses (a DP/stack problem, not enumeration).

**Common mistakes:**
- Pruning only at the end (test balance at leaves): that is the 2^(2n) brute force.
- Rule 2 written as `c < n` instead of `c < o`: then ')' can come first and invalid strings appear.
- Forgetting to pop after the recursive call (with a list buffer).

### Q8 ⭐⭐⭐ 🟡 Combination sum with unlimited reuse. `candidates` has 1 <= len <= 8 distinct positive integers (each <= 40) and `target` is 1 <= target <= 40. Return every combination of candidates (each candidate may be used any number of times) that sums to `target`. A combination is a list in non-decreasing order, two combinations that contain the same numbers the same number of times are the same one (list it once), and the outer list is sorted ascending with Python's list comparison. Return an empty list if none exists. Explain the start-index trick that prevents permutations of the same combination (recurse with the same index, not index + 1) and the sort-then-break pruning. Counting instead of listing is the coin-change-II DP of Part 10 Q10. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.combinations_with_replacement over every length on small inputs. Example: candidates=[3, 4, 5], target=12 -> [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]; candidates=[3, 5], target=2 -> []; candidates=[2], target=8 -> [[2, 2, 2, 2]]; candidates=[1], target=3 -> [[1, 1, 1]]; candidates=[7, 2, 4], target=11 -> [[2, 2, 7], [4, 7]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over combinations with reuse: a start index stops permutations, sorting plus break stops overshoot.

**Say this first (1 line):** "Sort the candidates. Recurse with the remaining sum and a start index. Pick candidate i, then recurse with the same i (reuse is allowed) so order is always non-decreasing and a combination appears once. Break as soon as a candidate exceeds what is left."

**Brute force:** `itertools.combinations_with_replacement` over every length 1..target / min(candidates), keep those that sum to the target. Exponential, and it generates many sums that overshoot. Or the version without a start index that tries every order (compositions) and deduplicates by sorting at the end: for `[1, 2]`, target 12 it makes 753 calls against 49.

**Optimal:**
- `go(start, remain)`: if `remain == 0`, record `cur[:]`. Else for `i` from `start`: if `cs[i] > remain`, break; push `cs[i]`, `go(i, remain - cs[i])`, pop.
- Start-index trick: passing `i` (not `0`, and not `i + 1`) means the next pick is `cs[i]` or a larger candidate. Same index gives reuse; never going back gives each multiset exactly once, in non-decreasing order. Without it `[3, 4, 5]`, 12 would reach `[4, 3, 5]` and `[5, 4, 3]` as well.
- Sort-then-break: the candidates are ascending, so once `cs[i] > remain` every later candidate is too big too: break, not continue. Without the break the code makes a call that returns at once on an overshoot: 28 calls against 17 for `[3, 4, 5]`, target 12 (measured below).
- Recursion depth: the most numbers in one combination is target / min = 40 (candidate 1, target 40), so at most 41 frames: far below 1000 (checked: depth 40 for `[1..8]`, target 40; that case has 9749 answers and 73056 calls).
- Counting instead of listing is the coin-change-II DP (Part 10 Q10).

**Complexity:** Let T be the target and m the smallest candidate. Depth is at most T/m. The number of nodes is bounded by the number of non-decreasing sequences with sum at most T; there is no neat closed form. A loose bound is O(n^(T/m)) calls, each answer costs O(T/m) to copy. Space O(T/m) for the recursion plus the output. I give this as a bound from reasoning, not a tight one; the measured counts show how much the break and the start index cut.

**Dry run:** `[2, 3]`, target 5 (the program prints this tree).
- take 2 (remain 3), take 2 (remain 1): 2 > 1 so break.
- back at remain 3: take 3 (remain 0): answer `[2, 3]`.
- back at the root: take 3 (remain 2): 3 > 2, break.
So one answer `[2, 3]`. For the first example `[3, 4, 5]`, 12: `[3, 3, 3, 3]`, `[3, 4, 5]`, `[4, 4, 4]`.

**Code:**
```python
import itertools
import random

random.seed(1208)

def comb_sum(candidates, target):
    """Sorted candidates, start index, break when too big. Returns (list, calls, max depth)."""
    cs = sorted(candidates)
    out, cur, st = [], [], {'calls': 0, 'depth': 0}
    def go(start, remain):
        st['calls'] += 1
        st['depth'] = max(st['depth'], len(cur))
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            if cs[i] > remain:
                break                       # sorted: every later candidate is too big as well
            cur.append(cs[i])               # choose
            go(i, remain - cs[i])           # explore: SAME index i => reuse allowed, no reordering
            cur.pop()                       # undo
    go(0, target)
    return sorted(out), st['calls'], st['depth']

def comb_sum_no_break(candidates, target):
    """Start index but no break: overshoots are visited and rejected one call later."""
    cs = sorted(candidates); out, cur, calls = [], [], [0]
    def go(start, remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            cur.append(cs[i]); go(i, remain - cs[i]); cur.pop()
    go(0, target)
    return sorted(out), calls[0]

def comb_sum_ordered(candidates, target):
    """No start index: every ORDER is explored (permutations); dedupe by sorting at the end."""
    cs = sorted(candidates); out, cur, calls = set(), [], [0]
    def go(remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.add(tuple(sorted(cur))); return
        for v in cs:
            cur.append(v); go(remain - v); cur.pop()
    go(target)
    return sorted(map(list, out)), calls[0]

def brute(candidates, target):
    out = set()
    for length in range(1, target // min(candidates) + 1):
        for combo in itertools.combinations_with_replacement(sorted(candidates), length):
            if sum(combo) == target:
                out.add(combo)
    return sorted(map(list, out))

examples = [(([3, 4, 5], 12), [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]), (([3, 5], 2), []), (([2], 8), [[2, 2, 2, 2]]),
            (([1], 3), [[1, 1, 1]]), (([7, 2, 4], 11), [[2, 2, 7], [4, 7]])]
for (c, t), want in examples:
    assert comb_sum(c, t)[0] == want == brute(c, t) == comb_sum_no_break(c, t)[0] == comb_sum_ordered(c, t)[0]
    print(c, t, '->', comb_sum(c, t)[0])

# decision tree for candidates [2, 3], target 5 (sorted). 'X' = pruned by the break
def tree(cs, start, remain, d, cur):
    if remain == 0:
        print('  ' * d + f'{cur} sum hit: answer'); return
    for i in range(start, len(cs)):
        if cs[i] > remain:
            print('  ' * d + f'{cs[i]} > remain {remain}: break'); break
        print('  ' * d + f'take {cs[i]} (remain {remain - cs[i]}, next index {i})')
        tree(cs, i, remain - cs[i], d + 1, cur + [cs[i]])
tree([2, 3], 0, 5, 0, [])

# calls: break vs no break vs no start index (small cases; the ordered version explodes)
print('case                      answers  break  no-break  ordered')
for c, t in [([3, 4, 5], 12), ([2, 3, 6, 7], 7), ([2, 3, 5], 10), ([1, 2], 12)]:
    a, ca, _ = comb_sum(c, t); b, cb = comb_sum_no_break(c, t); o, co = comb_sum_ordered(c, t)
    assert a == b == o
    print(f'{str(c):12} t={t:<3}        {len(a):7} {ca:6} {cb:9} {co:8}')

# seeded cross-check
for _ in range(1500):
    c = random.sample(range(1, 13), random.randint(1, 5)); t = random.randint(1, 20)
    assert comb_sum(c, t)[0] == brute(c, t)
print('random cross-check ok: 1500 cases')

# edge: depth bound. candidate 1, target 40 -> 40 chosen numbers, 41 frames: far below the recursion limit of 1000
r, calls, depth = comb_sum([1], 40)
assert r == [[1] * 40] and depth == 40
r2, calls2, depth2 = comb_sum([1, 2, 3, 4, 5, 6, 7, 8], 40)
assert depth2 == 40 and all(sum(x) == 40 and x == sorted(x) for x in r2)
print('max depth (chosen numbers):', depth2, ' answers for [1..8], 40:', len(r2), ' calls:', calls2)
assert comb_sum([5], 3)[0] == [] and comb_sum([40], 40)[0] == [[40]]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 4, 5] 12 -> [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]
[3, 5] 2 -> []
[2] 8 -> [[2, 2, 2, 2]]
[1] 3 -> [[1, 1, 1]]
[7, 2, 4] 11 -> [[2, 2, 7], [4, 7]]
take 2 (remain 3, next index 0)
  take 2 (remain 1, next index 0)
    2 > remain 1: break
  take 3 (remain 0, next index 1)
    [2, 3] sum hit: answer
take 3 (remain 2, next index 1)
  3 > remain 2: break
case                      answers  break  no-break  ordered
[3, 4, 5]    t=12               3     17        28       70
[2, 3, 6, 7] t=7                2     10        28       37
[2, 3, 5]    t=10               4     20        34       85
[1, 2]       t=12               7     49        55      753
random cross-check ok: 1500 cases
max depth (chosen numbers): 40  answers for [1..8], 40: 9749  calls: 73056
edge asserts ok
```

**Edge cases:**
- No combination: `[3, 5]`, target 2 returns `[]`.
- Candidate equal to target: `[40]`, 40 returns `[[40]]`.
- A candidate larger than the target: skipped by the break.
- Candidate 1 with target 40: depth 40, one answer `[1] * 40`.
- The input need not be sorted (`[7, 2, 4]`): sort first.

**Follow-ups:**
- Each number used once, duplicates in input (Q21): recurse with `i + 1` and skip equal neighbours at the same level.
- Count the ways: DP over coins (Part 10 Q10).
- Fewest numbers: coin change minimum (a DP, not enumeration).

**Common mistakes:**
- Recursing with `0` instead of `i`: you get permutations of the same combination.
- Recursing with `i + 1`: no reuse.
- Using `continue` instead of `break` (correct but slower), or not sorting and then using `break` (wrong answers).
- Appending `cur` instead of a copy.

### Q9 ⭐⭐⭐ 🟡 Word search in a grid. `board` is a list of 1 to 6 strings of equal length 1 to 6 (letters), and `word` is a string of 1 to 12 letters. Return True if `word` can be spelled by walking to horizontally or vertically adjacent cells, never using the same cell twice in one spelling. Mark a cell as used while it is on the current path and restore it on the way back (state exactly where the undo goes). Say why the worst case is about R * C * 3^(L-1) and why the check `board[r][c] != word[k]` first prunes almost everything on real inputs. Backtracking depth is at most the word length L <= 12. Q32 revisits this with a word length that no longer fits in the recursion limit. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursion that carries the visited cells as an immutable tuple on small inputs. Example: board=['CATS', 'OXAT', 'DOGS'], word='CATS' -> True; board=['CATS', 'OXAT', 'DOGS'], word='TACO' -> True; board=['CATS', 'OXAT', 'DOGS'], word='SAT' -> False; board=['AA'], word='AAA' -> False; board=['Z'], word='Z' -> True.
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking on a grid (DFS with a visited mark): choose a neighbour, explore, undo the mark.

**Say this first (1 line):** "Try every cell as the start. From a cell, if the letter does not match word[k], stop; if it is the last letter, success; otherwise mark the cell as used, try the four neighbours, and restore the cell after all four have been tried."

**Brute force:** Carry the visited cells as an immutable tuple (copied per step) so nothing needs undoing. Same search, O(L) extra work per step for the tuple. It is the oracle in the cross-check.

**Optimal:**
- Copy the board into lists (strings are immutable), loop over every cell as a start.
- `go(r, c, k)`: if `g[r][c] != word[k]` return False (this also rejects a cell currently marked '#', since the board has only letters). If `k == L - 1` return True. Set `saved = g[r][c]`, mark `g[r][c] = '#'`, try the four neighbours, then restore `g[r][c] = saved`.
- Where the undo goes: after the loop over all four neighbours, and it must run on every way out of the function except the success return (which ends the search; the board is a copy so nothing leaks). If you restore too early, the cell is free while its descendants are still running, and the path can reuse it. If you never restore, other paths see a blocked cell. In the cross-check, the never-restore version gave a wrong answer on 95 of 2000 seeded random boards (boards up to 4 x 4 over 'a','b').
- Why about R * C * 3^(L-1): R * C choices of start, then at most 3 moves per step (one of the four neighbours is the cell you came from, which is marked). Worst case is a board of all 'A' and a word of 'A's ending in a missing letter, where no letter prunes early. On 6 x 6 all 'A' with `'A' * 11 + 'B'` the search made 1,069,612 calls (every attempt counted, including those rejected at once), under the bound 36 * 3^11 = 6,377,292.
- Why the letter check prunes almost everything on real boards: a cell survives a step only if it equals the next letter. On 'CATS/OXAT/DOGS' with 'SAT' the search made 16 calls against 114 for a letter-blind walk of all self-avoiding paths of 3 cells; for 'CATSX' 22 against 472.
- Recursion depth is L <= 12, far below 1000. (Q32 handles a word too long for recursion.)

**Complexity:** Time O(R * C * 3^(L-1)) worst case, typically far less because of the letter check. Space O(L) for the recursion, plus O(R * C) for the board copy (the mark is in place, no visited set). The counts above are calls, not timings.

**Dry run:** `CATS/OXAT/DOGS`, word `TACO`. Start at (0,2) 'T' (matches). Neighbour (1,2) 'A' matches word[1]; its neighbours (2,2) 'G', (1,3) 'T', (1,1) 'X' are not 'C': pruned. Back to (0,2): (0,3) 'S' is not 'A': pruned; (0,1) 'A' matches; (1,1) 'X' is not 'C'; (0,0) 'C' matches word[2]; (1,0) 'O' matches word[3], the last letter: True. The program prints this trace. 'SAT' is False: the S cells (0,3) and (2,3) have neighbours T, T and T, G, so no S touches an A. `['AA']`, `'AAA'` is False: only two cells.

**Code:**
```python
import random

random.seed(1209)

def exists(board, word, stats=None):
    """Grid backtracking. The mark '#' is safe because boards hold letters only."""
    g = [list(r) for r in board]            # strings are immutable: work on a copy
    R, C = len(g), len(g[0])
    if stats is None:
        stats = {}
    stats['calls'] = 0
    def go(r, c, k):
        stats['calls'] += 1
        if g[r][c] != word[k]:              # prune first: wrong letter (or the '#' mark) ends this branch
            return False
        if k == len(word) - 1:
            return True
        saved, g[r][c] = g[r][c], '#'       # choose: mark the cell as on the current path
        found = False
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                found = True
                break
        g[r][c] = saved                     # undo: restore on EVERY way out, after the neighbours were tried
        return found
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def exists_no_restore(board, word):
    """WRONG on purpose: the cell is marked and never restored."""
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k):
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1): return True
        return False                                # the undo line is missing
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, word):
    """Visited cells carried as an immutable tuple; nothing to undo."""
    R, C = len(board), len(board[0])
    def go(r, c, k, seen):
        if board[r][c] != word[k] or (r, c) in seen: return False
        if k == len(word) - 1: return True
        seen = seen + ((r, c),)
        return any(0 <= r + dr < R and 0 <= c + dc < C and go(r + dr, c + dc, k + 1, seen)
                   for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return any(go(r, c, 0, ()) for r in range(R) for c in range(C))

B0 = ['CATS', 'OXAT', 'DOGS']
examples = [(B0, 'CATS', True), (B0, 'TACO', True), (B0, 'SAT', False), (['AA'], 'AAA', False), (['Z'], 'Z', True)]
for b, w, want in examples:
    assert exists(b, w) == want == brute(b, w)
    print(b, repr(w), '->', exists(b, w))

# decision tree for TACO on B0: starting cells that pass the first-letter check, then the path
def trace(board, word):
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k, d):
        if g[r][c] != word[k]:
            print('  ' * d + f'({r},{c}) {g[r][c]!r} != {word[k]!r}: prune'); return False
        print('  ' * d + f'({r},{c}) {g[r][c]!r} matches word[{k}]')
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] != '#':
                if go(nr, nc, k + 1, d + 1): return True
        g[r][c] = board[r][c]
        return False
    for r in range(R):
        for c in range(C):
            if board[r][c] == word[0]:
                print(f'start ({r},{c})')
                if go(r, c, 0, 1): return True
    return False
print('found:', trace(B0, 'TACO'))

# calls with the first-letter check vs searching every self-avoiding path without any letter pruning
def count_paths(R, C, L):
    """Number of calls if letters are ignored: every self-avoiding walk of up to L cells is expanded."""
    seen = [[False] * C for _ in range(R)]; tot = [0]
    def go(r, c, k):
        tot[0] += 1
        if k == L - 1: return
        seen[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc]: go(nr, nc, k + 1)
        seen[r][c] = False
    for r in range(R):
        for c in range(C): go(r, c, 0)
    return tot[0]
st = {}
exists(B0, 'SAT', st); print('SAT on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 3))
exists(B0, 'CATSX', st); print('CATSX on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 5))
# adversarial: all 'A' and a word that ends in a letter that never appears: no letter prunes anything until the very end
st = {}
b6 = ['A' * 6] * 6
assert exists(b6, 'A' * 11 + 'B', st) is False
bound = 36 * 3 ** 11
print('worst-ish 6x6 all A, L=12: calls', st['calls'], ' R*C*3^(L-1) =', bound, ' within bound:', st['calls'] <= bound)

# seeded cross-check, and how often forgetting the undo is wrong
def rand_board():
    C = random.randint(1, 4)
    return [''.join(random.choice('ab') for _ in range(C)) for _ in range(random.randint(1, 4))]
bad = 0
for _ in range(2000):
    b = rand_board(); w = ''.join(random.choice('ab') for _ in range(random.randint(1, 7)))
    r = exists(b, w); assert r == brute(b, w)
    bad += exists_no_restore(b, w) != r
print('random cross-check ok: 2000 cases; no-restore variant wrong on', bad, 'of them')

# edge asserts
assert exists(['A'], 'AA') is False and exists(['AB'], 'BA') is True and exists(['A', 'B'], 'BA') is True
assert exists(['ABA'], 'ABA') is True and exists(['AB'], 'ABA') is False   # no cell reuse
assert exists(['ABCDEF'] * 1, 'F') and exists(['AAAAAA'] * 6, 'A' * 12) is True
print('edge asserts ok')
```

**Output (my run):**
```
['CATS', 'OXAT', 'DOGS'] 'CATS' -> True
['CATS', 'OXAT', 'DOGS'] 'TACO' -> True
['CATS', 'OXAT', 'DOGS'] 'SAT' -> False
['AA'] 'AAA' -> False
['Z'] 'Z' -> True
start (0,2)
  (0,2) 'T' matches word[0]
    (1,2) 'A' matches word[1]
      (2,2) 'G' != 'C': prune
      (1,3) 'T' != 'C': prune
      (1,1) 'X' != 'C': prune
    (0,3) 'S' != 'A': prune
    (0,1) 'A' matches word[1]
      (1,1) 'X' != 'C': prune
      (0,0) 'C' matches word[2]
        (1,0) 'O' matches word[3]
found: True
SAT on 3x4: pruned calls 16  letter-blind calls 114
CATSX on 3x4: pruned calls 22  letter-blind calls 472
worst-ish 6x6 all A, L=12: calls 1069612  R*C*3^(L-1) = 6377292  within bound: True
random cross-check ok: 2000 cases; no-restore variant wrong on 95 of them
edge asserts ok
```

**Edge cases:**
- 1 x 1 board: `['Z']`, 'Z' is True; word longer than the number of cells is False (`['AA']`, 'AAA').
- A path may go in any of the four directions, including up and left.
- No cell reuse in one spelling (`['ABA']` with 'ABA' is True, `['AB']` with 'ABA' is False), but every start cell is a fresh search because the mark is restored.
- All-same-letter boards are the slow case.

**Follow-ups:**
- Many words at once: put the words in a trie and walk it during one DFS (Q11).
- Word longer than the recursion limit: explicit stack (Q32).
- Cheap speed-ups: if the board's letter counts cannot cover the word, answer False; search from the rarer end of the word.

**Common mistakes:**
- Not restoring the cell (or restoring before the neighbours are tried).
- Marking with a character that can occur on the board.
- Checking the bounds after indexing (negative indexes wrap around in Python: `g[-1][c]` silently reads the last row).
- Starting the search from only (0, 0).

### Q10 ⭐⭐⭐ 🔴 N-Queens: list every solution. `n` is an integer with 1 <= n <= 9. Place n queens on an n x n board so that no two share a row, a column or a diagonal. Return every solution as a list of n strings of length n (`'Q'` for the queen, `'.'` for empty), ordered so that the solutions are ascending by the tuple of queen columns row by row (row 0 first), which is the order a recursion that tries columns left to right produces. Return an empty list when there is no solution (n = 2 and n = 3). Use three sets (columns, `r - c` diagonals, `r + c` diagonals) and explain why one queen per row is not a restriction. Recursion depth is n <= 9. State, without proving it, that the number of solutions for n = 1..9 is 1, 0, 0, 2, 10, 4, 40, 92, 352 and show that your program prints exactly these counts. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying every permutation of columns and testing the diagonals on small inputs. Example: n=4 -> [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]; n=1 -> [['Q']]; n=3 -> [].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with constraint sets (choose a column for this row, explore, undo). It is a constraint-satisfaction search: the three sets are the pruning rule.

**Say this first (1 line):** "One queen per row, columns left to right, three sets for column, `r - c` and `r + c`; skip an attacked square, recurse, undo. Solutions come out in ascending column-tuple order for free."

**Brute force:** Try every permutation of columns (one queen per row and per column) and test every pair for a shared diagonal. That is n! permutations times O(n^2) pair checks. Fine as an oracle for n <= 8. Even more naive: any column in any row, which is n^n placements (n = 9: 387,420,489 leaves).

**Optimal:**
- Row-by-row recursion `go(r)`. At row `r` try columns `0..n-1` in order.
- Why one queen per row is not a restriction: two queens in the same row attack each other, and there are n queens and n rows, so every row holds exactly one. Same for columns, which is why the column set exists.
- Diagonals: cells on one `\` diagonal share `r - c`; cells on one `/` diagonal share `r + c`. Three sets give an O(1) "is this square attacked" test.
- Pruning rule: only recurse into a square that no earlier queen attacks. A partial board with an attacked pair can never become a solution, so the whole subtree is dead.
- Undo: remove the column and both diagonals from the sets when you come back.
- Order: columns are tried 0, 1, 2, ... so the first queen's column is the outermost sort key, then the second, and so on. That is exactly "ascending by the tuple of queen columns". The code asserts it for n = 1..9.
- Recursion depth is n <= 9, nowhere near CPython's default limit of 1000.

**Complexity:** Time: no polynomial bound; the search is exponential. A loose upper bound is the permutation tree, O(n!) leaves, and pruning cuts far below it. What I can state is measured: 8,394 calls for n = 9, against 986,410 calls for a columns-only search and 435,848,050 for the tree with no test at all. Building each solution's strings costs O(n^2). Space: O(n) for the recursion and the three sets, plus the output (352 boards of 81 characters for n = 9).

**Dry run:** n = 4. Each line is one call; "safe columns" are the squares the sets allow.
```
[]  row 0: safe columns [0, 1, 2, 3]
  [0]  row 1: safe columns [2, 3]
    [0, 2]  row 2: safe columns []  DEAD END
    [0, 3]  row 2: safe columns [1]
      [0, 3, 1]  row 3: safe columns []  DEAD END
  [1]  row 1: safe columns [3]
    ... [1, 3] -> [1, 3, 0] -> [1, 3, 0, 2]  SOLUTION
  [2]  row 1: safe columns [0] ... [2, 0, 3, 1]  SOLUTION
  [3]  row 1: safe columns [0, 1]  both end in DEAD END
```
The full tree is in the output below: 17 calls. The unpruned row-by-row tree (every column tried in every row) has 1 + 4 + 16 + 64 + 256 = 341 nodes. The two solutions are `[1, 3, 0, 2]` and `[2, 0, 3, 1]` (queen columns per row), which render as `['.Q..', '...Q', 'Q...', '..Q.']` and `['..Q.', 'Q...', '...Q', '.Q..']`.

**Code:**
```python
import itertools
import random

random.seed(1210)

def solve_queens(n, trace=None):
    """Backtracking, one queen per row. cols / (r-c) / (r+c) sets give O(1) conflict tests.
    Returns (solutions as strings, number of recursive calls). Columns tried left to right => ascending order."""
    out, placed = [], []
    cs, d1, d2 = set(), set(), set()
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n:
            out.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in placed])
            if trace is not None: trace.append('  ' * r + str(placed) + '  SOLUTION')
            return
        safe = [c for c in range(n) if c not in cs and (r - c) not in d1 and (r + c) not in d2]
        if trace is not None:
            trace.append('  ' * r + str(placed) + '  row %d: safe columns %s%s' % (r, safe, '  DEAD END' if not safe else ''))
        for c in safe:
            cs.add(c); d1.add(r - c); d2.add(r + c); placed.append(c)
            go(r + 1)
            placed.pop(); cs.discard(c); d1.discard(r - c); d2.discard(r + c)
    go(0)
    return out, calls

def unpruned_calls(n):
    """Same row-by-row tree but with NO conflict test: every column is tried in every row. Closed form: 1 + n + n^2 + ... + n^n."""
    return sum(n ** k for k in range(n + 1))

def unpruned_measured(n):
    """Count the calls of the unpruned row-by-row tree by actually running it (n <= 6)."""
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n: return
        for _ in range(n): go(r + 1)
    go(0); return calls

def perm_tree_calls(n):
    """Calls of the 'one queen per row and per column' tree (no diagonal test): 1 + n + n(n-1) + ... + n!."""
    t, f = 0, 1
    for k in range(n + 1):
        t += f; f *= (n - k)
    return t

def brute(n):
    """Oracle: every permutation of columns (one queen per row AND per column), test diagonals pairwise.
    itertools.permutations yields lexicographic order, i.e. ascending column tuples."""
    res = []
    for p in itertools.permutations(range(n)):
        if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            res.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in p])
    return res

# prompt examples
assert solve_queens(4)[0] == [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
assert solve_queens(1)[0] == [['Q']]
assert solve_queens(3)[0] == [] and solve_queens(2)[0] == []
print("3 prompt examples ok")

# decision tree for n = 4
tr = []
sols, calls = solve_queens(4, tr)
print("--- decision tree, n=4 ---")
print("\n".join(tr))
print("calls with pruning:", calls, "| unpruned row-by-row tree:", unpruned_calls(4))
for n in range(1, 7):
    assert unpruned_measured(n) == unpruned_calls(n), n
print("closed form 1+n+...+n^n matches a measured run for n=1..6")

# counts for n = 1..9 and node-visit comparison
print("--- counts and calls ---")
counts = []
for n in range(1, 10):
    s, c = solve_queens(n)
    counts.append(len(s))
    assert s == sorted(s, key=lambda sol: [row.index('Q') for row in sol])   # ascending by queen columns
    print("n=%d solutions=%d calls=%d columns-only=%d unpruned=%d" % (n, len(s), c, perm_tree_calls(n), unpruned_calls(n)))
assert counts == [1, 0, 0, 2, 10, 4, 40, 92, 352]
print("counts n=1..9:", counts)

# seeded random cross-check against the permutation oracle (n = 1..8)
for _ in range(300):
    n = random.randint(1, 8)
    assert solve_queens(n)[0] == brute(n), n
print("300 seeded random sizes (1..8) agree with the permutation oracle")
# edge asserts
assert solve_queens(2) == ([], 3)          # root + two row-0 placements; every row-1 try is attacked
assert all(len(s) == 4 and all(len(row) == 4 for row in s) for s in solve_queens(4)[0])
print("edge asserts ok")
```

**Output (my run):**
```text
3 prompt examples ok
--- decision tree, n=4 ---
[]  row 0: safe columns [0, 1, 2, 3]
  [0]  row 1: safe columns [2, 3]
    [0, 2]  row 2: safe columns []  DEAD END
    [0, 3]  row 2: safe columns [1]
      [0, 3, 1]  row 3: safe columns []  DEAD END
  [1]  row 1: safe columns [3]
    [1, 3]  row 2: safe columns [0]
      [1, 3, 0]  row 3: safe columns [2]
        [1, 3, 0, 2]  SOLUTION
  [2]  row 1: safe columns [0]
    [2, 0]  row 2: safe columns [3]
      [2, 0, 3]  row 3: safe columns [1]
        [2, 0, 3, 1]  SOLUTION
  [3]  row 1: safe columns [0, 1]
    [3, 0]  row 2: safe columns [2]
      [3, 0, 2]  row 3: safe columns []  DEAD END
    [3, 1]  row 2: safe columns []  DEAD END
calls with pruning: 17 | unpruned row-by-row tree: 341
closed form 1+n+...+n^n matches a measured run for n=1..6
--- counts and calls ---
n=1 solutions=1 calls=2 columns-only=2 unpruned=2
n=2 solutions=0 calls=3 columns-only=5 unpruned=7
n=3 solutions=0 calls=6 columns-only=16 unpruned=40
n=4 solutions=2 calls=17 columns-only=65 unpruned=341
n=5 solutions=10 calls=54 columns-only=326 unpruned=3906
n=6 solutions=4 calls=153 columns-only=1957 unpruned=55987
n=7 solutions=40 calls=552 columns-only=13700 unpruned=960800
n=8 solutions=92 calls=2057 columns-only=109601 unpruned=19173961
n=9 solutions=352 calls=8394 columns-only=986410 unpruned=435848050
counts n=1..9: [1, 0, 0, 2, 10, 4, 40, 92, 352]
300 seeded random sizes (1..8) agree with the permutation oracle
edge asserts ok
```

**Edge cases:**
- n = 1 gives `[['Q']]`; n = 2 and n = 3 give `[]` (the search makes 3 calls for n = 2 and 6 for n = 3).
- Counts for n = 1..9 are 1, 0, 0, 2, 10, 4, 40, 92, 352; the program prints exactly these and asserts them. I state them, I do not prove them.
- Return a list of boards (list of list of strings), not one flat list; an empty result is `[]`, not `[[]]`.

**Follow-ups:**
- *Count only, n up to 14?* Use three bitmasks (columns, left diagonals shifted left, right diagonals shifted right) and `avail & -avail` to pick the lowest free column. No board strings, so it is much faster.
- *Use the symmetry?* Solve the left half of row 0 and mirror, about half the work; the odd-n middle column needs care.
- *Why not itertools.permutations?* It is correct (that is my oracle) but it never prunes: it builds all n! orders before testing.

**Common mistakes:**
- Forgetting to undo one of the three sets (usually a diagonal), which silently loses solutions.
- Using `r - c` for both diagonals; the second one must be `r + c`.
- Appending the same mutable list of columns to the output instead of building strings or copying.
- Claiming a time complexity like "O(n!)" as the exact cost; say it is an upper bound and quote the measured calls instead.

---

### Q11 ⭐⭐⭐ 🔴 Word search II with a trie. `board` is a list of 1 to 10 strings of equal length 1 to 10 (lowercase) and `words` is a list of 1 to 3000 distinct lowercase words (each 1 to 10 letters). Return the sorted list (ascending strings) of the words that can be spelled by a path of adjacent (horizontal or vertical) cells that uses no cell twice in one path; a word that cannot be spelled is not returned and the result is empty if none can. Build a trie of the words, run one DFS from each cell that walks the board and the trie together, store the whole word at the end node so you do not rebuild it, and prune: stop when the next letter is not a child, and (as an improvement) delete trie branches that no longer hold words. Explain why running the single-word search of Q9 once per word is too slow when there are thousands of words. Depth is at most 10. In the answer include a dry run on the first example and a seeded random cross-check of your solution against running the single-word search of Q9 once per word on small inputs. Example: board=['cats', 'xaot', 'dgsr'], words=['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot'] -> ['cat', 'cats']; board=['ab'], words=['ab', 'ba', 'aba'] -> ['ab', 'ba']; board=['a'], words=['b'] -> [].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened) | Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Trie plus grid DFS backtracking. The trie is the pruning rule: a path is only extended while it is a prefix of some word.

**Say this first (1 line):** "Put all words in a trie, run one DFS per start cell that walks the board and the trie together, stop when the next letter is not a child, store the whole word at the end node, and delete exhausted branches."

**Brute force:** For every word run the single-word search of Q9 (DFS from every cell, mark, recurse, unmark). With W words that repeats the same board walks W times and never shares a prefix: `cat` and `cats` explore the same cells twice.

**Optimal:**
- Build: for each word walk/create child dicts; at the last node store `node['$'] = word`. The key `'$'` cannot clash with a lowercase letter.
- Search: for each start cell whose letter is a child of the root, call `dfs(r, c, parent)`. Inside: take `nd = parent[ch]`; if `'$'` is in `nd`, record the word and `pop` it (so it is reported once, even if two paths spell it).
- Backtracking: write `'#'` into the cell (it is never a trie key, so the neighbour test `g[nr][nc] in nd` fails for it), recurse into neighbours whose letter is a child, then restore the letter.
- Pruning 1: no child for the next letter means no call at all.
- Pruning 2 (the improvement): after exploring, if `nd` has no children and no word left, delete it from its parent. Later starts then fail at the first letter instead of re-walking dead ground. Observed: same answer, 516 visits against 36,796 without it on one 8 x 8 random board.
- Depth is at most 10 (the longest word), so plain recursion is safe.
- Why per-word search is too slow: it costs W times a full search (up to 100 start cells and about 4 * 3^9 paths of length 10 each), while the trie search shares every common prefix and only follows letters that start some word. The trie cost does not multiply by W.

**Complexity:** Build O(total letters), at most about 30,000 for 3000 words of up to 10 letters. Search: each start cell explores at most 4 * 3^(L - 1) paths for the longest word length L, so a loose bound is R * C * 4 * 3^9, about 7.9 million for a 10 x 10 board and L = 10; in practice the trie cuts this to the prefixes that exist. Space O(total letters) for the trie plus O(L) recursion. Measured on a random 10 x 10 board over {a, b, c} with 3000 distinct words: 24,917 (cell, trie node) visits for the trie against 638,891 recursive calls for 3000 single-word searches (different units, a call is a smaller step, but the gap is the point).

**Dry run:** `board = ['cats','xaot','dgsr']`, words `cat, cats, tar, dog, sat, star, cot`. The program prints every (cell, trie node) visit; here is the story in order.
- Start (0,0) `c` (visit 1): child of the root. Neighbour (0,1) `a` fits `ca` (visit 2); (1,0) `x` does not. From `a`, neighbour (0,2) `t` fits `cat` (visit 3): the node holds `'$'`, so record `cat`. From `t`, neighbour (0,3) `s` fits `cats` (visit 4): record `cats`.
- The `cats` node has no children left, so it is deleted from its parent; then `cat` is empty and deleted, then `ca`. The `c` node stays because `cot` is still below it.
- Start (0,2) `t` (visits 5-6): `t` then `a` at (0,1) fits `ta`, but `tar` needs an `r` next to (0,1) and there is none: dead end.
- Start (0,3) `s` (visits 7-10): the neighbour `t` at (1,3) fits `st` but `star` needs an `a` next to it: dead. The neighbour `t` at (0,2) then `a` at (0,1) fits `sta`, but there is no `r` next to (0,1): dead.
- Starts (1,3) `t`, (2,0) `d`, (2,2) `s` (visits 11-13): one visit each, no neighbour continues any word. The other cells hold letters that are not children of the root (`x`, `a`, `o`, `g`, `r`), so they are skipped without a call.
- Total 13 visits; sorted result `['cat', 'cats']`. One single-word search per word needs 104 calls on the same input.

**Code:**
```python
import random

random.seed(1211)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def find_words(board, words, stats=None, prune=True, log=None):
    """Trie of all words + ONE DFS per start cell. The word is stored at its end node; found leaves are pruned."""
    R, C = len(board), len(board[0])
    root = {}
    for w in words:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = w                                   # whole word stored at the end node
    g = [list(r) for r in board]
    found = []
    visits = 0
    def dfs(r, c, parent):
        nonlocal visits
        ch = g[r][c]
        nd = parent[ch]
        visits += 1                                   # one visit = one (cell, trie node) pair entered
        if log is not None: log.append('visit (%d,%d) %r%s' % (r, c, ch, '  -> found ' + nd['$'] if '$' in nd else ''))
        if '$' in nd:
            found.append(nd.pop('$'))                 # report once; pop so it cannot be reported twice
        g[r][c] = '#'                                 # mark the cell used on this path
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] in nd:   # '#' and '$' are never children letters
                dfs(nr, nc, nd)
        g[r][c] = ch                                  # undo
        if prune and not nd:                          # no words left below: cut the branch
            del parent[ch]
    for r in range(R):
        for c in range(C):
            if g[r][c] in root:
                dfs(r, c, root)
    if stats is not None: stats.append(visits)
    return sorted(found)

def single_word(board, word, counter=None):
    """Q9-style search for ONE word (recursive, marks and unmarks the cell)."""
    R, C = len(board), len(board[0])
    g = [list(r) for r in board]
    def go(r, c, k):
        if counter is not None: counter[0] += 1
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                g[r][c] = word[k]; return True
        g[r][c] = word[k]
        return False
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, words, counter=None):
    return sorted(w for w in words if single_word(board, w, counter))

for b, ws, want in [(['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot'], ['cat', 'cats']),
                    (['ab'], ['ab', 'ba', 'aba'], ['ab', 'ba']), (['a'], ['b'], [])]:
    assert find_words(b, ws) == brute(b, ws) == want, (b, ws)
print("3 prompt examples ok")

# dry run: which words the trie DFS reports on the first example, and how many (cell, node) visits it needs
b, ws = ['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot']
st = []
print("first example:", find_words(b, ws, st), "trie visits:", st[0])
cnt = [0]; brute(b, ws, cnt)
lg = []; find_words(b, ws, [], log=lg)
print("\n".join(lg))
print("same example, one search per word: calls =", cnt[0])

# seeded random cross-check
for _ in range(400):
    R_, C_ = random.randint(1, 4), random.randint(1, 4)
    board = [''.join(random.choice('abc') for _ in range(C_)) for _ in range(R_)]
    words = list({''.join(random.choice('abc') for _ in range(random.randint(1, 6))) for _ in range(random.randint(1, 15))})
    assert find_words(board, words) == brute(board, words), (board, words)
print("400 seeded random boards agree with one single-word search per word")

# why the trie wins: many words, shared prefixes (10 x 10 board, 3000 words, alphabet 'abc')
board = [''.join(random.choice('abc') for _ in range(10)) for _ in range(10)]
words = set()
while len(words) < 3000:
    words.add(''.join(random.choice('abc') for _ in range(random.randint(1, 10))))
words = sorted(words)
st = []; a = find_words(board, words, st)
cnt = [0]; b2 = brute(board, words, cnt)
assert a == b2
print("10x10 board, 3000 words: found %d words | trie visits %d | single-word calls %d" % (len(a), st[0], cnt[0]))
# effect of deleting exhausted branches: same answer, fewer visits when many words are found
board = [''.join(random.choice('ab') for _ in range(8)) for _ in range(8)]
words = sorted({''.join(random.choice('ab') for _ in range(random.randint(1, 8))) for _ in range(300)})
s1, s2 = [], []
assert find_words(board, words, s1, prune=True) == find_words(board, words, s2, prune=False)
print("8x8 board, %d words: visits with branch deletion %d, without %d" % (len(words), s1[0], s2[0]))
assert s1[0] <= s2[0]
# max-size edge cases
assert find_words(['a' * 10] * 10, ['a' * 10]) == ['a' * 10]
assert find_words(['a'], ['a']) == ['a']
assert find_words(['ab'], ['abc']) == []
assert find_words(['aa'], ['aaa']) == []                  # a cell may not be reused in one path
assert find_words(['ab', 'cd'], ['abdc', 'acdb', 'ad']) == ['abdc', 'acdb']   # 'ad' is diagonal
print("edge asserts ok")
```

**Output (my run):**
```text
3 prompt examples ok
first example: ['cat', 'cats'] trie visits: 13
visit (0,0) 'c'
visit (0,1) 'a'
visit (0,2) 't'  -> found cat
visit (0,3) 's'  -> found cats
visit (0,2) 't'
visit (0,1) 'a'
visit (0,3) 's'
visit (1,3) 't'
visit (0,2) 't'
visit (0,1) 'a'
visit (1,3) 't'
visit (2,0) 'd'
visit (2,2) 's'
same example, one search per word: calls = 104
400 seeded random boards agree with one single-word search per word
10x10 board, 3000 words: found 2592 words | trie visits 24917 | single-word calls 638891
8x8 board, 153 words: visits with branch deletion 516, without 36796
edge asserts ok
```

**Edge cases:**
- Board 1 x 1: `['a']` with word `a` is found; word `b` gives `[]`.
- A cell may not repeat inside one path: `['aa']` cannot spell `aaa`.
- Diagonal neighbours do not count (`ad` on `['ab','cd']` is not found).
- Two paths for the same word must still report it once: `pop('$')` guarantees it.
- A word that is a prefix of another (`cat`, `cats`) must record both: check `'$'` before going deeper, do not stop at the first one.

**Follow-ups:**
- *Why delete trie nodes?* It makes the cost shrink as words are found; without it the same dead prefixes are walked again from every start cell (516 against 36,796 visits in my run).
- *Memory?* A dict per node is heavy; for 3000 short words it is fine. Q33 measures dict-of-dicts against arrays of 26.
- *Many queries on one board?* Build the trie once per word list; if the board changes and words are fixed, only the DFS repeats.

**Common mistakes:**
- Not unmarking the cell after recursion (a leftover `'#'` breaks later paths).
- Returning duplicates because the word is recorded on every path that spells it.
- Rebuilding the word by string concatenation along the path instead of storing it at the end node.
- Deleting from a dict you are iterating over (here the delete happens after the neighbour loop, which is safe).

---

### Q12 ⭐⭐ 🟢 Power of two and power of four. `n` is an integer with -2^31 <= n < 2^31 (negatives and zero included). Return `[is_power_of_two, is_power_of_four]`, where a power of two is 2^k for some integer k >= 0 (so 1 counts, 0 and negatives do not). Use `n > 0 and n & (n - 1) == 0` for the first, explain why it works (a power of two has exactly one set bit, and `n & (n - 1)` clears it), and add one more mask for the second (the single bit must sit at an even position: `n & 0x55555555 != 0`), justify the mask for the 31-bit range, and say why a loop that divides by 2 works too but costs O(log n). In the answer include a dry run on the first example and a seeded random cross-check of your solution against membership in the explicit sets {2^k} and {4^k} on small inputs. Example: n=16 -> [True, True]; n=8 -> [True, False]; n=0 -> [False, False]; n=-4 -> [False, False]; n=1 -> [True, True]; n=1073741824 -> [True, True].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bit manipulation: one-set-bit test with `n & (n - 1)` plus a position mask.

**Say this first (1 line):** "A power of two has exactly one set bit, and `n & (n - 1)` clears the lowest set bit, so it is zero only for powers of two (and 0, which I exclude with `n > 0`); for four, the single bit must sit at an even position: `n & 0x55555555 != 0`."

**Brute force:** Divide by 2 (or 4) while the remainder is 0 and see if you end at 1. Correct, O(log n) steps. Or test membership in the explicit set of 31 powers of two and 16 powers of four (my oracle).

**Optimal:**
- `n > 0`: negatives and 0 are not powers of two. The guard matters only for 0 (`0 & -1 == 0`); a negative number has infinitely many 1 bits in Python, so `n & (n - 1)` is never 0 for it. Observed over -1000..1000: without the guard the test is wrong for exactly `[0]`.
- `n & (n - 1) == 0`: subtracting 1 flips the lowest set bit and every zero below it, so the AND clears that one bit. If it was the only bit, the result is 0.
- Precedence, Python 3.13: `&` binds tighter than `==` and `!=`, so `n & (n - 1) == 0` is `(n & (n - 1)) == 0`. In C it would not be; in Python you do not need extra brackets.
- Power of four: 4^k = 2^(2k), the bit sits at an even position. For 1 <= n < 2^31 the largest power of four is 4^15 = 2^30, positions 0, 2, ..., 30. `0x55555555` is `0101...0101` with set bits at exactly those positions (the code prints and asserts that). So for a power of two, `n & 0x55555555 != 0` says the bit is at an even position.
- The mask alone is not enough: it accepts 3, 5, 6, 7, 9, 11 and so on. You need both tests.
- Outside the stated range the mask breaks: 4^16 = 2^32 has its bit at position 32, which `0x55555555` does not cover. A range-free alternative is `n.bit_length() % 2 == 1` for a power of two (2^k has `bit_length` k + 1); I checked it for k = 0..199.

**Complexity:** O(1) time and space for the bit tests (the word size is fixed by the stated range). The division loop is O(log n) divisions.

**Dry run:** n = 16 = `0b10000`: `n - 1` = `0b01111`, AND is 0, so a power of two. Mask: `16 & 0x55555555` = `0x10` (bit 4, even), non-zero, so a power of four: `[True, True]`. n = 8 = `0b1000`: AND with 7 is 0; `8 & 0x55555555` = 0 (bit 3 is odd), so `[True, False]`. n = 0: `n > 0` fails, `[False, False]`. n = -4: `n > 0` fails.

**Code:**
```python
import random

random.seed(1212)

def power_two_four(n):
    p2 = n > 0 and n & (n - 1) == 0          # '&' binds tighter than '==' in Python, so no extra brackets needed
    p4 = p2 and (n & 0x55555555) != 0
    return [p2, p4]

def power_by_division(n):
    """Loop version, O(log n): keep halving (quartering) while the remainder is zero."""
    def pw(n, base):
        if n <= 0: return False
        while n % base == 0: n //= base
        return n == 1
    return [pw(n, 2), pw(n, 4)]

POW2 = {2 ** k for k in range(31)}
POW4 = {4 ** k for k in range(16)}
def brute(n): return [n in POW2, n in POW4]

for n, want in [(16, [True, True]), (8, [True, False]), (0, [False, False]), (-4, [False, False]), (1, [True, True]),
                (1073741824, [True, True])]:
    assert power_two_four(n) == power_by_division(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=16:  bin", bin(16), " n-1 =", bin(15), " n & (n-1) =", 16 & 15, " n & 0x55555555 =", hex(16 & 0x55555555))
print("dry run n=8 :  bin", bin(8), " n & (n-1) =", 8 & 7, " n & 0x55555555 =", 8 & 0x55555555)

# the mask: 4^k for k = 0..15 are exactly the powers of two in 1..2^30 at an even bit position
assert {4 ** k for k in range(16)} == {1 << i for i in range(0, 31, 2)}
print("mask 0x55555555 = %s ; its set bits are the even positions 0..30: %s" % (bin(0x55555555), [i for i in range(32) if 0x55555555 >> i & 1] == list(range(0, 32, 2))))

# exhaustive check over a wide window and over every power of two and its neighbours in range
window = list(range(-70000, 70001))
special = [s * (2 ** k + d) for k in range(31) for d in (-1, 0, 1) for s in (1, -1)] + [-2 ** 31, 2 ** 31 - 1]
for n in window + special:
    assert power_two_four(n) == power_by_division(n) == brute(n), n
print("exhaustive: %d values in [-70000, 70000] plus %d special values agree" % (len(window), len(special)))

# seeded random over the full 32-bit signed range
for _ in range(3000):
    n = random.randint(-2 ** 31, 2 ** 31 - 1)
    assert power_two_four(n) == brute(n)
print("3000 seeded random values over the full range agree with the explicit sets")

# why each part of the test is there
no_guard = [n for n in range(-1000, 1001) if (n & (n - 1) == 0) != (n in POW2)]
print("without 'n > 0', n & (n-1) == 0 is wrong for exactly:", no_guard)
mask_only = [n for n in range(1, 200) if bool(n & 0x55555555) != (n in POW4)]
print("mask alone (no power-of-two test) wrongly accepts, e.g.:", mask_only[:6], "-> you need BOTH tests")
print("outside the stated range: 4**16 =", 4 ** 16, "has the single bit at position 32; n & 0x55555555 =", (4 ** 16) & 0x55555555, "-> would report False")
# alternative for the second test that needs no mask and works for any size: a power of two 2^k has bit_length k+1
assert all(power_two_four(2 ** k)[1] == (k % 2 == 0) == ((2 ** k).bit_length() % 2 == 1) for k in range(0, 31))
assert all(((1 << k).bit_length() % 2 == 1) == (k % 2 == 0) for k in range(0, 200))
print("bit_length alternative: 2^k is a power of 4 exactly when its bit_length is odd (checked k = 0..199)")
assert all(((n - 1) % 3 == 0) == (n in POW4) for n in sorted(POW2))
assert all((1 << (n - 1).bit_length()) >= n and (1 << (n - 1).bit_length()) // 2 < n for n in range(1, 5000))
print("follow-up claims ok: (n-1) % 3 == 0 separates 4^k from 2*4^k; 1 << (n-1).bit_length() is the next power of two >= n")
edge = [(2 ** 31 - 1, [False, False]), (-2 ** 31, [False, False]), (2 ** 30, [True, True]), (2 ** 29, [True, False])]
for n, want in edge: assert power_two_four(n) == want
print("edge asserts ok")
```

**Output (my run):**
```text
6 prompt examples ok
dry run n=16:  bin 0b10000  n-1 = 0b1111  n & (n-1) = 0  n & 0x55555555 = 0x10
dry run n=8 :  bin 0b1000  n & (n-1) = 0  n & 0x55555555 = 0
mask 0x55555555 = 0b1010101010101010101010101010101 ; its set bits are the even positions 0..30: True
exhaustive: 140001 values in [-70000, 70000] plus 188 special values agree
3000 seeded random values over the full range agree with the explicit sets
without 'n > 0', n & (n-1) == 0 is wrong for exactly: [0]
mask alone (no power-of-two test) wrongly accepts, e.g.: [3, 5, 6, 7, 9, 11] -> you need BOTH tests
outside the stated range: 4**16 = 4294967296 has the single bit at position 32; n & 0x55555555 = 0 -> would report False
bit_length alternative: 2^k is a power of 4 exactly when its bit_length is odd (checked k = 0..199)
follow-up claims ok: (n-1) % 3 == 0 separates 4^k from 2*4^k; 1 << (n-1).bit_length() is the next power of two >= n
edge asserts ok
```

**Edge cases:**
- 0 and negatives: always `[False, False]`.
- 1 = 2^0 = 4^0: `[True, True]`.
- 2^30 = 1073741824: `[True, True]`; 2^29: `[True, False]`.
- 2^31 - 1 (all ones, not a power) and -2^31 (a negative): `[False, False]`.

**Follow-ups:**
- *Another test for power of four without a mask?* `(n - 1) % 3 == 0` on a power of two (4^k - 1 is divisible by 3, 2 * 4^k - 1 is not); or the `bit_length` parity above.
- *Power of two with a popcount?* `n > 0 and n.bit_count() == 1` (`int.bit_count` needs Python 3.10 or newer, editor knowledge); `bin(n).count('1') == 1` on older versions.
- *Next power of two at or above n?* `1 << (n - 1).bit_length()` for n >= 1.

**Common mistakes:**
- Dropping `n > 0` and returning True for 0.
- Using only the mask for the four test.
- Using `n & (n - 1) == 0` in C-style precedence worries and adding wrong brackets like `n & ((n - 1) == 0)`, which is a different expression.
- Testing the mask on a wider range without widening it.

---

### Q13 ⭐⭐ 🟢 Hamming distance and total Hamming distance. The Hamming distance of two integers is the number of bit positions at which they differ. Given integers `x`, `y` (0 <= x, y < 2^31) and a list `nums` of 2 <= len <= 10^4 integers in 0..2^31 - 1, return `[hamming(x, y), total]` where `total` is the sum of the Hamming distances over all unordered pairs i < j of `nums`. Compute the first as the popcount of `x ^ y`, and the second in O(31 * n) by counting, for each bit position, how many numbers have the bit set (`ones`) and adding `ones * (n - ones)`; explain why that equals the pair count. In the answer include a dry run on the first example and a seeded random cross-check of your solution against comparing every pair bit by bit on small inputs. Example: x=1, y=4, nums=[5, 9, 12, 3] -> [2, 14]; x=0, y=0, nums=[7, 7] -> [0, 0]; x=2147483647, y=0, nums=[0, 2147483647] -> [31, 31]; x=6, y=5, nums=[1, 2, 4] -> [2, 6].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bit manipulation, per-bit counting (contribution technique): count pairs by bit position instead of by pair.

**Say this first (1 line):** "Pair distance is popcount of `x ^ y`. For the total over all pairs, for each of the 31 bits count how many numbers have it set, `ones`, and add `ones * (n - ones)`, because only a (1, 0) pair differs at that bit."

**Brute force:** For every unordered pair i < j compare all 31 bits: O(n^2 * 31). With n = 10^4 that is about 50 million pairs times 31, far too slow for Python.

**Optimal:**
- `hamming(x, y) = bin(x ^ y).count('1')`: XOR has a 1 exactly where the bits differ, so its popcount is the distance. (`(x ^ y).bit_count()` also works on Python 3.10 or newer; that version is editor knowledge.)
- Total: the distance of a pair is the sum over bits of "do they differ here". Swap the sums: for each bit, count the pairs that differ at it, then add over bits.
- At bit b let `ones` numbers have 1 and `n - ones` have 0. A pair differs at b exactly when one is from each group, and every such pair is counted once as an unordered pair: `ones * (n - ones)` pairs. Pairs with both 1 or both 0 contribute 0.
- 31 bits because every value is below 2^31 (no sign bit, no masking needed for non-negative inputs).

**Complexity:** Time O(31 * n) for the total, O(1) for the pair; space O(1). For n = 10^4 that is 310,000 bit tests instead of about 50 million pair comparisons. The maximum total is 31 * 5000 * 5000 = 775,000,000 (half 0, half 2^31 - 1); Python ints never overflow, but in a 32-bit language this would be a point to mention.

**Dry run:** `nums = [5, 9, 12, 3]` = `0101, 1001, 1100, 0011`.

| bit | numbers with the bit set | ones | zeros | pairs |
|---|---|---|---|---|
| 0 | 5, 9, 3 | 3 | 1 | 3 |
| 1 | 3 | 1 | 3 | 3 |
| 2 | 5, 12 | 2 | 2 | 4 |
| 3 | 9, 12 | 2 | 2 | 4 |

Total 3 + 3 + 4 + 4 = 14. Bits 4..30 are zero everywhere, so they add 0. Pair part: `1 ^ 4` = `0b101`, popcount 2. Answer `[2, 14]`.

**Code:**
```python
import itertools
import random

random.seed(1213)
BITS = 31

def hamming_pair(x, y):
    return bin(x ^ y).count('1')

def hamming_total(nums):
    n, total = len(nums), 0
    for b in range(BITS):
        ones = sum((v >> b) & 1 for v in nums)
        total += ones * (n - ones)                # pairs that differ at bit b: one with 1, one with 0
    return total

def solve(x, y, nums):
    return [hamming_pair(x, y), hamming_total(nums)]

def brute(x, y, nums):
    h = lambda a, b: sum(1 for i in range(BITS) if ((a >> i) & 1) != ((b >> i) & 1))
    return [h(x, y), sum(h(a, b) for a, b in itertools.combinations(nums, 2))]

for (x, y, nums), want in [((1, 4, [5, 9, 12, 3]), [2, 14]), ((0, 0, [7, 7]), [0, 0]),
                           ((2147483647, 0, [0, 2147483647]), [31, 31]), ((6, 5, [1, 2, 4]), [2, 6])]:
    assert solve(x, y, nums) == brute(x, y, nums) == want, (x, y, nums)
print("4 prompt examples ok")

print("dry run nums = [5, 9, 12, 3]:")
nums = [5, 9, 12, 3]
tot = 0
for b in range(4):
    ones = sum((v >> b) & 1 for v in nums)
    tot += ones * (len(nums) - ones)
    print("  bit %d: set in %s -> ones=%d zeros=%d pairs=%d" % (b, [v for v in nums if v >> b & 1], ones, len(nums) - ones, ones * (len(nums) - ones)))
print("  total", tot, "| popcount(1 ^ 4) = popcount(%s) = %d" % (bin(1 ^ 4), hamming_pair(1, 4)))

for _ in range(500):
    nums = [random.randint(0, 2 ** random.randint(1, 31) - 1) for _ in range(random.randint(2, 8))]
    x, y = random.randint(0, 2 ** 31 - 1), random.randint(0, 2 ** 31 - 1)
    assert solve(x, y, nums) == brute(x, y, nums), (x, y, nums)
print("500 seeded random cases agree with the pairwise bit-by-bit brute force")

# edge / size asserts
assert hamming_total([7, 7, 7]) == 0
assert hamming_total([0, 2 ** 31 - 1]) == 31
assert hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000) == 31 * 5000 * 5000      # n = 10^4, max total
assert solve(0, 0, [0, 0]) == [0, 0]
print("max case n=10^4 total:", hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000), "| fits easily: Python ints do not overflow")
print("edge asserts ok")
```

**Output (my run):**
```text
4 prompt examples ok
dry run nums = [5, 9, 12, 3]:
  bit 0: set in [5, 9, 3] -> ones=3 zeros=1 pairs=3
  bit 1: set in [3] -> ones=1 zeros=3 pairs=3
  bit 2: set in [5, 12] -> ones=2 zeros=2 pairs=4
  bit 3: set in [9, 12] -> ones=2 zeros=2 pairs=4
  total 14 | popcount(1 ^ 4) = popcount(0b101) = 2
500 seeded random cases agree with the pairwise bit-by-bit brute force
max case n=10^4 total: 775000000 | fits easily: Python ints do not overflow
edge asserts ok
```

**Edge cases:**
- All numbers equal: total 0 (every bit has `ones` = 0 or n).
- n = 2 reduces to a single pair distance.
- Values using all 31 bits: `[0, 2147483647]` gives 31.
- x = y gives 0.

**Follow-ups:**
- *Sum over all ordered pairs?* Double the total.
- *Count by character instead of bit (strings of equal length)?* Same idea with 26 counters per position.
- *Hamming weight of one number faster?* Brian Kernighan's `m &= m - 1` loop, one round per set bit (Q2).

**Common mistakes:**
- Using `ones * (n - ones)` and then halving; that formula already counts unordered pairs once.
- Looping over 32 bits and treating bit 31 as a sign bit; the input range stops at bit 30.
- Doing the O(n^2) pair loop and calling it "fine" at n = 10^4.

---

### Q14 ⭐⭐ 🟢 Replace words with their shortest root. `roots` is a list of 1 to 1000 lowercase strings (length 1 to 100) and `sentence` is a string of 1 to 1000 lowercase words separated by single spaces (no leading or trailing space, word length 1 to 100). Replace each word by the shortest root that is a prefix of it; if no root is a prefix, keep the word. Return the new sentence. Build a trie of the roots and walk each word until the first end-of-root flag; explain why the first flag you meet is the shortest root and why duplicate roots do not matter. The same trie shape as Q3. Cost: O(total root length + sentence length). In the answer include a dry run on the first example and a seeded random cross-check of your solution against scanning every root for every word on small inputs. Example: roots=['to', 'tra', 'a'], sentence='tomorrow a train travels to tokyo' -> 'to a tra tra to to'; roots=['ab'], sentence='cab ab abc' -> 'cab ab ab'; roots=['b', 'be'], sentence='best bee ace' -> 'b b ace'.
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie prefix walk, stopping at the first end-of-word flag.

**Say this first (1 line):** "Insert all roots in a trie with an end flag; for each word walk letter by letter and stop at the first flag, which is the shortest root; if you fall off the trie first, keep the word."

**Brute force:** For each word test every root with `startswith` and keep the shortest hit: O(words * roots * root length). With 1000 words and 1000 roots of length 100 that is about 10^8 character steps in the worst case.

**Optimal:**
- Build the trie: dict per node, `'$'` marks "a root ends here" (`'$'` cannot be a lowercase letter).
- For each word: `nd = root`, `k = 0`; while `k < len(word)`, no flag at `nd`, and `word[k]` is a child: step. Afterwards, if the current node has a flag, the answer is `word[:k]`; otherwise keep the word.
- Why the first flag is the shortest root: the walk visits the prefixes of the word in increasing length, so the first node with a flag is the shortest prefix that is a root. Longer roots below it are never reached.
- Duplicate roots do not matter: inserting the same root twice sets the same flag on the same node.
- Same trie shape as the insert/search/startsWith API of Q3.

**Complexity:** Build O(total root length), at most 1000 * 100 = 100,000 steps. Each word costs at most its own length, so the sentence costs O(total sentence length). Space O(total root length) for the trie nodes. (A word equal to or shorter than a root is simply not replaced.)

**Dry run:** roots `to, tra, a`; trie: `t -> {o*, r -> a*}`, `a*` (a star marks the flag).
- `tomorrow`: `t`, `o` reaches a flag: `to`.
- `a`: `a` has a flag: `a`.
- `train`: `t`, `r`, `a` has a flag: `tra` (the program prints this walk).
- `travels`: same path: `tra`. `to`: `to`. `tokyo`: `to`.
Result `to a tra tra to to`. Second example: roots `ab`, `cab ab abc` gives `cab ab ab`: `cab` starts with `c`, which is not in the trie, so it stays.

**Code:**
```python
import random

random.seed(1214)

def build_trie(roots):
    root = {}
    for w in roots:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = True                               # end-of-root flag ('$' can never be a lowercase letter)
    return root

def replace_words(roots, sentence):
    trie = build_trie(roots)
    out = []
    for word in sentence.split(' '):
        nd, k = trie, 0
        while k < len(word) and '$' not in nd and word[k] in nd:   # stop at the FIRST flag: it is the shortest root
            nd = nd[word[k]]
            k += 1
        out.append(word[:k] if '$' in nd else word)
    return ' '.join(out)

def brute(roots, sentence):
    out = []
    for word in sentence.split(' '):
        c = [r for r in roots if word.startswith(r)]
        out.append(min(c, key=len) if c else word)
    return ' '.join(out)

for roots, s, want in [(['to', 'tra', 'a'], 'tomorrow a train travels to tokyo', 'to a tra tra to to'),
                       (['ab'], 'cab ab abc', 'cab ab ab'), (['b', 'be'], 'best bee ace', 'b b ace')]:
    assert replace_words(roots, s) == brute(roots, s) == want, (roots, s)
print("3 prompt examples ok")

# dry run: roots = ['to','tra','a'], word 'train'
t = build_trie(['to', 'tra', 'a'])
print("trie top level:", sorted(k for k in t), "| under 't':", sorted(k for k in t['t']), "| under 'tr':", sorted(t['t']['r']))
w = 'train'; nd = t; path = ''
for ch in w:
    if '$' in nd or ch not in nd: break
    nd = nd[ch]; path += ch
    print("  read %r -> node for %r, end flag here: %s" % (ch, path, '$' in nd))
print("  result:", path if '$' in nd else w)

for _ in range(500):
    roots = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 6))]
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 8))]
    s = ' '.join(words)
    assert replace_words(roots, s) == brute(roots, s), (roots, s)
print("500 seeded random cases agree with scanning every root for every word")

# duplicate roots and ordering do not matter; a longer root never wins over a shorter prefix root
assert replace_words(['ab', 'ab', 'a'], 'abc') == 'a' == replace_words(['a', 'ab', 'ab'], 'abc')
assert replace_words(['abc'], 'ab') == 'ab'              # root longer than the word: no replacement
assert replace_words(['a'], 'a') == 'a'                  # word equal to a root
assert replace_words(['z'], 'a') == 'a'                  # no root matches
assert replace_words(['a'], 'aaa a aa') == 'a a a'
print("edge asserts ok")

# max-size shape: 1000 roots of length 100 and a 1000-word sentence of length-100 words
roots = [''.join(random.choice('ab') for _ in range(100)) for _ in range(1000)]
sent = ' '.join(''.join(random.choice('ab') for _ in range(100)) for _ in range(1000))
assert replace_words(roots, sent) == brute(roots, sent)
print("max-size shape ok (1000 roots x 100 letters, 1000 words x 100 letters)")
```

**Output (my run):**
```text
3 prompt examples ok
trie top level: ['a', 't'] | under 't': ['o', 'r'] | under 'tr': ['a']
  read 't' -> node for 't', end flag here: False
  read 'r' -> node for 'tr', end flag here: False
  read 'a' -> node for 'tra', end flag here: True
  result: tra
500 seeded random cases agree with scanning every root for every word
edge asserts ok
max-size shape ok (1000 roots x 100 letters, 1000 words x 100 letters)
```

**Edge cases:**
- Word equal to a root: unchanged.
- Root longer than the word: no flag reached, word kept.
- No root matches: word kept.
- Roots `['ab', 'a']` and word `abc`: `a` wins (shortest), whatever the insert order.
- One word only; single-letter roots.

**Follow-ups:**
- *Why not a set of roots and test every prefix of the word?* Works: for each word build prefixes of length 1, 2, ... and look up in a set, stopping at the first hit. Cost is O(L^2) per word because each prefix slice and hash costs O(L); the trie walk is O(L).
- *Longest root instead of shortest?* Keep walking and remember the last flag.
- *Memory of the trie?* Up to one dict per root character (100,000 nodes here); a sorted list of roots with `bisect` is a lighter alternative (Part 3 Q36 compares the two at concept level).

**Common mistakes:**
- Checking the flag after stepping past it, so the walk continues into longer roots and returns the longest.
- Using `str.replace`, which replaces anywhere in the word, not only at the start.
- Splitting with `split()` and rejoining with single spaces when the problem fixes single spaces (here `split(' ')` matches the input format exactly).

---

### Q15 ⭐⭐ 🟡 Repeated and missing number by XOR. `nums` has n integers (2 <= n <= 10^5) from 1..n in which exactly one value appears twice and exactly one value of 1..n is absent. Return `[duplicate, missing]`. Solve it in O(n) time and O(1) extra space with XOR: XOR every `nums[i]` with every `i` from 1..n to get `duplicate ^ missing`, take its lowest set bit with `x & -x`, split all numbers and indices into two groups by that bit, and XOR within each group; then decide which of the two results is the duplicate. Explain why the two values must differ in some bit and why the groups separate them. Also show the XOR swap `a ^= b; b ^= a; a ^= b` and say why `a, b = b, a` is what you write in Python (and why the XOR swap breaks if both names point at the same list slot). The single-missing-number version (hash set, sorted, sum) is Part 1 Q8. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter and a membership scan on small inputs. Example: nums=[1, 3, 3, 4] -> [3, 2]; nums=[2, 2] -> [2, 1]; nums=[1, 1, 3, 4, 5] -> [1, 2]; nums=[3, 1, 2, 5, 5] -> [5, 4].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation plus partition by a differing bit (`x & -x`).

**Say this first (1 line):** "XOR all numbers with all indices 1..n: everything cancels except `duplicate ^ missing`; take its lowest set bit, split numbers and indices by that bit, XOR inside each group, and one scan tells you which result is the duplicate."

**Brute force:** A `Counter` for the value seen twice, then a scan of 1..n for the absent one. O(n) time but O(n) space. Or sort and compare neighbours: O(n log n), and it changes the input.

**Optimal:**
- Consider the multiset `nums` plus the indices 1..n. A normal value appears once in each: twice in total, it cancels. The duplicate appears three times (twice in `nums`, once as an index): it survives. The missing value appears once (only as an index): it survives. So `x = duplicate ^ missing`.
- `x != 0` because the duplicate is present and the missing value is absent, so they are different numbers. Different numbers differ in some bit.
- `low = x & -x` is the lowest set bit of `x`, a bit where the two differ.
- Split every number and every index into two groups by `value & low`. The duplicate and the missing value land in different groups. Inside each group every other value still shows up an even number of times (once as a number, once as an index, or twice as the duplicate's pair), so it cancels. One group XORs to the duplicate (it has 3 copies), the other to the missing value (1 copy).
- Which is which: one more pass, `nums.count(a) == 2`, decides. That is one O(n) scan and O(1) space.
- XOR swap: `a ^= b; b ^= a; a ^= b` swaps two ints without a temporary. In Python you write `a, b = b, a`: it is clearer, works for any type, and needs no trick. The XOR swap breaks when both names refer to the same slot: `lst[i] ^= lst[j]` with `i == j` makes the slot 0 (a ^ a = 0), and the value is lost. (Two separate variables that merely hold equal numbers swap fine.)

**Complexity:** Time O(n): one pass for `x`, one for the groups, one `count`. Space O(1). Input values and indices are at most 10^5, so no masking is needed; all values are positive.

**Dry run:** `nums = [1, 3, 3, 4]`, n = 4. `x` = (1^1) ^ (2^3) ^ (3^3) ^ (4^4) = 2 ^ 3 = 1 (binary `1`), so `low = 1` (the program prints `x`).
- Bit-set group (odd): numbers `1, 3, 3`, indices `1, 3`: 1 ^ 3 ^ 3 ^ 1 ^ 3 = 3.
- Bit-clear group (even): numbers `4`, indices `2, 4`: 4 ^ 2 ^ 4 = 2.
- `nums.count(3) == 2`, so the duplicate is 3 and the missing value is 2: `[3, 2]`.

**Code:**
```python
import collections
import random

random.seed(1215)

def dup_missing(nums):
    n = len(nums)
    x = 0
    for i, v in enumerate(nums, 1):          # x = dup ^ missing: every value that is both present and in 1..n cancels
        x ^= i ^ v
    low = x & -x                              # a bit where dup and missing differ (x != 0 because dup != missing)
    a = b = 0
    for i, v in enumerate(nums, 1):
        if i & low: a ^= i
        else: b ^= i
        if v & low: a ^= v
        else: b ^= v
    # a and b are {dup, missing} in some order; one more O(n) pass tells which is which
    return [a, b] if nums.count(a) == 2 else [b, a]

def brute(nums):
    c = collections.Counter(nums)
    return [[k for k, v in c.items() if v == 2][0], [i for i in range(1, len(nums) + 1) if i not in c][0]]

for nums, want in [([1, 3, 3, 4], [3, 2]), ([2, 2], [2, 1]), ([1, 1, 3, 4, 5], [1, 2]), ([3, 1, 2, 5, 5], [5, 4])]:
    assert dup_missing(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [1, 3, 3, 4]
nums = [1, 3, 3, 4]
x = 0
for i, v in enumerate(nums, 1): x ^= i ^ v
low = x & -x
print("dry run [1,3,3,4]: x = dup ^ missing =", x, bin(x), "| low bit =", low)
print("  group with bit set   : numbers", [v for v in nums if v & low], "indices", [i for i in range(1, 5) if i & low])
print("  group with bit clear : numbers", [v for v in nums if not v & low], "indices", [i for i in range(1, 5) if not i & low])
print("  results:", dup_missing(nums), "(duplicate, missing)")

for _ in range(500):
    n = random.randint(2, 12)
    dup, miss = random.sample(range(1, n + 1), 2)
    nums = [v for v in range(1, n + 1) if v != miss] + [dup]
    random.shuffle(nums)
    assert dup_missing(nums) == brute(nums) == [dup, miss], nums
print("500 seeded random cases agree with Counter + membership scan")
# every possible (dup, missing) pair for n = 2..7, exhaustively
for n in range(2, 8):
    for dup in range(1, n + 1):
        for miss in range(1, n + 1):
            if dup == miss: continue
            nums = [v for v in range(1, n + 1) if v != miss] + [dup]
            assert dup_missing(nums) == [dup, miss]
print("exhaustive: every (duplicate, missing) pair for n = 2..7 correct")

# XOR swap
a, b = 5, 9
a ^= b; b ^= a; a ^= b
assert (a, b) == (9, 5)
lst = [4, 7]
i = j = 0                                     # both names point at the same slot
lst[i] ^= lst[j]; lst[j] ^= lst[i]; lst[i] ^= lst[j]
print("XOR swap on 5, 9 ->", (a, b), "| same slot [4, 7] with i == j ->", lst, "(slot zeroed, value lost)")
assert lst == [0, 7]
# edge asserts
assert dup_missing([2, 2]) == [2, 1]
assert dup_missing([1, 1]) == [1, 2]
assert dup_missing([2, 3, 3]) == [3, 1]
n = 10 ** 5
big = list(range(1, n + 1)); big[-1] = 1                  # drop n, duplicate 1
assert dup_missing(big) == [1, n]
print("edge asserts ok (including n = 10^5)")
```

**Output (my run):**
```text
4 prompt examples ok
dry run [1,3,3,4]: x = dup ^ missing = 1 0b1 | low bit = 1
  group with bit set   : numbers [1, 3, 3] indices [1, 3]
  group with bit clear : numbers [4] indices [2, 4]
  results: [3, 2] (duplicate, missing)
500 seeded random cases agree with Counter + membership scan
exhaustive: every (duplicate, missing) pair for n = 2..7 correct
XOR swap on 5, 9 -> (9, 5) | same slot [4, 7] with i == j -> [0, 7] (slot zeroed, value lost)
edge asserts ok (including n = 10^5)
```

**Edge cases:**
- n = 2, `[2, 2]` gives `[2, 1]`; `[1, 1]` gives `[1, 2]`.
- Missing value is n: the largest index only appears once.
- Duplicate is 1 and missing is n at n = 10^5: checked.
- Do not rely on the sum trick for both numbers at once (it gives only two equations; sum and sum of squares works but can get large; XOR avoids that).

**Follow-ups:**
- *Why not in-place sign marking?* It also gives O(1) space but it mutates (or temporarily corrupts) the input; XOR leaves it untouched.
- *Single missing number?* XOR of all values and indices, or the sum formula; see Part 1 Q8 for the hash-set, sort and sum versions.
- *Three differing values?* XOR alone is not enough; use counting or sorting.

**Common mistakes:**
- Forgetting to XOR in the indices 1..n (then the missing value is not in the XOR).
- Reporting `[a, b]` without the final check and getting the pair the wrong way round half the time.
- Using the XOR swap on two list slots that may be the same slot.
- Computing `x & -x` and then comparing with `== 1` instead of testing `value & low`.

---

### Q16 ⭐⭐ 🟡 Single number III. `nums` has 2 <= len <= 10^5 integers (any sign, |value| < 2^31): exactly two values appear once and every other value appears exactly twice. Return the two single values as a list sorted ascending. Use O(n) time and O(1) extra space: XOR everything to get `a ^ b`, isolate one bit in which they differ with `x & -x`, and XOR separately the numbers that have that bit. Show that `x & -x` also works for a NEGATIVE `x` in Python (integers behave as two's complement with infinitely many sign bits; the result is the lowest set bit), and give a small case where `a ^ b` is negative. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter on small inputs. Example: nums=[4, 9, 4, -6, 2, 9] -> [-6, 2]; nums=[1, 2] -> [1, 2]; nums=[-1, 1, 3, 3] -> [-1, 1]; nums=[0, 5, 0, 7, 7, -2] -> [-2, 5].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation plus partition by a differing bit; the lowest set bit via `x & -x`.

**Say this first (1 line):** "XOR everything to get `a ^ b`; it is non-zero, so take its lowest set bit `x & -x`; numbers with that bit set go to one group, the rest to the other; pairs stay together and cancel, each group leaves one single."

**Brute force:** `Counter` and keep the two keys with count 1: O(n) time, O(n) space. Sorting also works but is O(n log n).

**Optimal:**
- XOR of all numbers: pairs cancel (`a ^ a = 0`), leaving `x = a ^ b` where `a` and `b` are the singles. `a != b` so `x != 0`.
- Pick any set bit of `x`, here the lowest, `low = x & -x`. At that bit `a` and `b` differ.
- Split by `v & low`. Two equal numbers have the same bit, so each pair lands in the same group and cancels there. `a` and `b` land in different groups.
- XOR the group with the bit set to get one single, `a`. The other is `x ^ a`. Sort the pair for the required output order.
- `x & -x` for a NEGATIVE `x` in Python 3.13 (observed): Python integers behave as two's complement with infinitely many sign bits, and `-x == ~x + 1`. Above the lowest set bit `-x` is the complement of `x`, at and below it they agree, so the AND keeps only the lowest set bit. The output shows `-12 & 12`, i.e. `x & -x` is 4 for both 12 and -12, and a loop over every non-zero x in [-2000, 2000] confirms the result is a positive power of two equal to the lowest set bit.
- Small case with a negative `a ^ b`: in `[4, 9, 4, -6, 2, 9]` the singles -6 and 2 give `-6 ^ 2 = -8`; in `[-1, 1, 3, 3]` the singles give `-1 ^ 1 = -2`. Python needs no masking here: values are below 2^31 in absolute value, so the XOR of two of them stays in the signed 32-bit range, and `x & -x` is exact.

**Complexity:** Time O(n) (two passes). Space O(1). No hash table.

**Dry run:** `nums = [4, 9, 4, -6, 2, 9]`. XOR of all: 4^9^4^(-6)^2^9 = (-6) ^ 2 = -8 (`...11111000`). `low = -8 & 8 = 8`. Numbers with bit 8 set: 9, -6, 9 (-6 is `...11111010`, bit 3 is 1): XOR = -6. Numbers with it clear: 4, 4, 2: XOR = 2. Answer sorted: `[-6, 2]`.

**Code:**
```python
import collections
import functools
import random

random.seed(1216)

def single_number_iii(nums):
    x = 0
    for v in nums:
        x ^= v                                # x = a ^ b: all pairs cancel
    low = x & -x                              # lowest set bit of x; x != 0 because a != b
    a = 0
    for v in nums:
        if v & low:                           # group 1: numbers with that bit set (a pair always lands in one group together)
            a ^= v
    return sorted([a, x ^ a])

def brute(nums):
    return sorted(k for k, v in collections.Counter(nums).items() if v == 1)

for nums, want in [([4, 9, 4, -6, 2, 9], [-6, 2]), ([1, 2], [1, 2]), ([-1, 1, 3, 3], [-1, 1]), ([0, 5, 0, 7, 7, -2], [-2, 5])]:
    assert single_number_iii(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [4, 9, 4, -6, 2, 9]
nums = [4, 9, 4, -6, 2, 9]
x = 0
for v in nums: x ^= v
low = x & -x
print("dry run:", nums)
print("  x = a ^ b =", x, "(-6 ^ 2) | low = x & -x =", low, bin(low))
print("  numbers with that bit set  :", [v for v in nums if v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if v & low]))
print("  numbers with that bit clear:", [v for v in nums if not v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if not v & low]))
print("  answer:", single_number_iii(nums))

# Python 3.13 behaviour with negatives, as observed
print("--- negatives in Python 3.13 (observed) ---")
for v in (12, -12, -2, -1, -8):
    print("x = %3d  -x = %3d  x & -x = %2d  ~x + 1 = %3d  bin(x & -x) = %s" % (v, -v, v & -v, ~v + 1, bin(v & -v)))
print("-6 ^ 2 =", -6 ^ 2, "(a negative XOR: the two singles have different signs, so the sign 'bit' differs)")
print("-1 ^ 1 =", -1 ^ 1, "| (-1 ^ 1) & -(-1 ^ 1) =", (-1 ^ 1) & -(-1 ^ 1))
for v in range(-2000, 2001):
    if v:
        low = v & -v
        assert low > 0 and low & (low - 1) == 0 and v & (low - 1) == 0 and v & low        # power of two, and the lowest set bit of v
print("x & -x is the lowest set bit (a positive power of two) for every nonzero x in [-2000, 2000]")

# seeded random cross-check, values of both signs up to 2^31
for _ in range(500):
    k = random.randint(2, 7)
    vals = random.sample(range(-2 ** 31 + 1, 2 ** 31), k)
    singles, pairs = vals[:2], vals[2:]
    nums = singles + [p for p in pairs for _ in range(2)]
    random.shuffle(nums)
    assert single_number_iii(nums) == brute(nums) == sorted(singles), nums
print("500 seeded random cases (values of both signs) agree with Counter")
# exhaustive: every pair of distinct singles in -4..4 with one extra pair value
for a in range(-4, 5):
    for b in range(-4, 5):
        if a >= b: continue
        for p in range(-4, 5):
            if p in (a, b): continue
            assert single_number_iii([p, a, p, b]) == [a, b]
print("exhaustive small values ok")
# edge asserts
assert single_number_iii([0, 1]) == [0, 1]
assert single_number_iii([-2 ** 31 + 1, 2 ** 31 - 1]) == [-2 ** 31 + 1, 2 ** 31 - 1]
big = [1, 2] + [v for v in range(3, 50003) for _ in range(2)]
assert single_number_iii(big) == [1, 2]
print("edge asserts ok (including 10^5 numbers)")
```

**Output (my run):**
```text
4 prompt examples ok
dry run: [4, 9, 4, -6, 2, 9]
  x = a ^ b = -8 (-6 ^ 2) | low = x & -x = 8 0b1000
  numbers with that bit set  : [9, -6, 9] -> XOR = -6
  numbers with that bit clear: [4, 4, 2] -> XOR = 2
  answer: [-6, 2]
--- negatives in Python 3.13 (observed) ---
x =  12  -x = -12  x & -x =  4  ~x + 1 = -12  bin(x & -x) = 0b100
x = -12  -x =  12  x & -x =  4  ~x + 1 =  12  bin(x & -x) = 0b100
x =  -2  -x =   2  x & -x =  2  ~x + 1 =   2  bin(x & -x) = 0b10
x =  -1  -x =   1  x & -x =  1  ~x + 1 =   1  bin(x & -x) = 0b1
x =  -8  -x =   8  x & -x =  8  ~x + 1 =   8  bin(x & -x) = 0b1000
-6 ^ 2 = -8 (a negative XOR: the two singles have different signs, so the sign 'bit' differs)
-1 ^ 1 = -2 | (-1 ^ 1) & -(-1 ^ 1) = 2
x & -x is the lowest set bit (a positive power of two) for every nonzero x in [-2000, 2000]
500 seeded random cases (values of both signs) agree with Counter
exhaustive small values ok
edge asserts ok (including 10^5 numbers)
```

**Edge cases:**
- `[1, 2]`: no pairs at all; the answer is the sorted pair.
- A single equal to 0: `[0, 1]`; the XOR is non-zero because the singles differ.
- Singles of opposite sign: `a ^ b` is negative; works unchanged.
- Extremes `-2^31 + 1` and `2^31 - 1`: checked, as is a 10^5-element input.

**Follow-ups:**
- *Why does the lowest bit work and not any bit?* Any set bit of `x` works. The lowest is convenient: `x & -x`.
- *Every other number three times and one single?* Q28: count bits modulo 3.
- *In a fixed-width language?* `x & -x` can overflow for `INT_MIN` in C; Python has no such case.

**Common mistakes:**
- Splitting by `v > something` instead of by a bit.
- Forgetting to sort the pair when the order is specified.
- Believing `x & -x` fails for negatives in Python; it does not, as shown.
- Writing the lowest-bit trick as `x & ~x + 1` and being surprised: `+` binds tighter than `&`, so it parses as `x & ((~x) + 1)`, which equals `x & -x`. Fine, but write `x & -x`.

---

### Q17 ⭐⭐ 🟡 Reverse bits of a 32-bit integer. `n` is an integer with -2^31 <= n < 2^32. Treat it as a 32-bit pattern (a negative `n` is read as its two's-complement pattern, so -1 is 32 ones and -2^31 is a one followed by 31 zeros), reverse the order of the 32 bits and return the result as a non-negative integer in 0..2^32 - 1. Python integers have no fixed width, so mask explicitly with `n & 0xFFFFFFFF` before looping and explain what goes wrong without the mask (a negative n never becomes 0 under `n >>= 1`; it stays -1, so a loop that waits for zero never ends). Give the 32-step loop, and the divide-and-conquer version that swaps halves with masks (16, 8, 4, 2, 1 bit groups) in five steps. In the answer include a dry run on the first example and a seeded random cross-check of your solution against reversing the 32-character binary string on small inputs. Example: n=1 -> 2147483648; n=6 -> 1610612736; n=-1 -> 4294967295; n=-2147483648 -> 1; n=0 -> 0; n=4294967295 -> 4294967295.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit manipulation with an explicit 32-bit mask (Python has no fixed width).

**Say this first (1 line):** "Mask to 32 bits first, `n & 0xFFFFFFFF`, then 32 times: shift the result left, append the lowest bit of `n`, shift `n` right. The mask matters because Python's negative integers never reach 0 under `>>`."

**Brute force:** Format as a 32-character binary string with `format(n & 0xFFFFFFFF, '032b')`, reverse it, parse with `int(s, 2)`. Correct and short (my oracle), but it builds strings; interviewers usually want the bit loop.

**Optimal:**
- Loop version: `n &= M32`; repeat 32 times `r = (r << 1) | (n & 1); n >>= 1`. Fixed 32 rounds, so leading zeros of `n` become trailing zeros of the result, as the problem wants.
- Mask, Python 3.13 as observed: `-1 & 0xFFFFFFFF` is 4294967295 and `-2147483648 & 0xFFFFFFFF` is 2147483648, i.e. the two's-complement 32-bit pattern as a non-negative number. That also gives the required reading of negative inputs.
- Without the mask: `-1 >> 1` is -1, and `-1 >> 100` is -1. Every negative number ends at -1 under repeated `>>=` and never reaches 0 (the code checks every n in [-3000, -1]), so a loop `while n:` never ends. A fixed 32-round loop with no mask does still stop and, observed, gives the right answer for negatives (`n & 1` and `>>` are arithmetic on the infinite two's-complement form), but it hides the fact that you rely on that; the mask makes the 32-bit reading explicit, and the five-step version needs it for real.
- Divide and conquer in five steps (swap 16-bit halves, then bytes, nibbles, bit pairs, single bits): `((n >> 16) | (n << 16)) & M32`, then `((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)`, then the same with `0xF0F0F0F0 / 0x0F0F0F0F` and shift 4, `0xCCCCCCCC / 0x33333333` and shift 2, `0xAAAAAAAA / 0x55555555` and shift 1. The first step needs the `& M32` because `n << 16` grows past 32 bits in Python (no overflow); the later steps stay inside 32 bits by construction.
- Result is always in 0..2^32 - 1, a non-negative int. Reversing twice returns the masked pattern (checked on 500 random values).

**Complexity:** Time O(32) = O(1) for the loop, 5 steps for the mask version. Space O(1).

**Dry run:** `n = 6` = `00000000000000000000000000000110`. The loop reads bits 0, 1, 2, ... = 0, 1, 1, 0, 0, ... and pushes them in front-first, so the result is `01100000000000000000000000000000` = 1610612736. Mask version, hex after each step: `00060000`, `06000000`, `60000000`, `90000000`, `60000000` = 1610612736.

**Code:**
```python
import random

random.seed(1217)
M32 = 0xFFFFFFFF

def reverse_loop(n):
    n &= M32                                  # read the 32-bit two's-complement pattern; makes n non-negative
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1)                # append the lowest bit of n to r
        n >>= 1
    return r

def reverse_dc(n):
    n &= M32
    n = ((n >> 16) | (n << 16)) & M32                                   # swap 16-bit halves (mask: << 16 grows past 32 bits)
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)               # swap bytes in each half
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)               # swap nibbles
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)               # swap bit pairs
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)               # swap adjacent bits
    return n

def brute(n):
    return int(format(n & M32, '032b')[::-1], 2)

for n, want in [(1, 2147483648), (6, 1610612736), (-1, 4294967295), (-2147483648, 1), (0, 0), (4294967295, 4294967295)]:
    assert reverse_loop(n) == reverse_dc(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=6 as 32 bits:", format(6, '032b'))
print("  reversed             :", format(reverse_loop(6), '032b'), "=", reverse_loop(6))
print("divide-and-conquer on n=6, value after each of the five steps (32-bit hex):")
n = 6 & M32
steps = []
n = ((n >> 16) | (n << 16)) & M32; steps.append(n)
n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8); steps.append(n)
n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4); steps.append(n)
n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2); steps.append(n)
n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1); steps.append(n)
print("  ", ["%08x" % s for s in steps], "-> final", n)
assert n == 1610612736

# Python 3.13 behaviour without the mask (observed)
print("--- why the mask (Python 3.13, observed) ---")
print("-1 >> 1 =", -1 >> 1, "| -1 >> 100 =", -1 >> 100, "| -2147483648 >> 40 =", -2147483648 >> 40)
def reverse_no_mask_while(n, cap=40):
    steps = 0
    while n and steps < cap:                  # 'while n:' style loop on a negative n; capped so this demo stops
        n >>= 1; steps += 1
    return steps
print("loop 'while n: n >>= 1' on n=-1 stopped only because of the cap of 40 steps; after the cap n is still", end=' ')
m = -1
for _ in range(40): m >>= 1
print(m)
print("without the mask, -1 << 16 =", -1 << 16, "(no 32-bit wrap) ; with the mask, (-1 << 16) & 0xFFFFFFFF =", (-1 << 16) & M32)
print("-1 & 0xFFFFFFFF =", -1 & M32, "| -2147483648 & 0xFFFFFFFF =", -2147483648 & M32)

for n in range(-3000, 0):
    m = n
    for _ in range(64): m >>= 1
    assert m == -1                              # every negative n ends at -1, never at 0
print("every negative n in [-3000, -1] is -1 after 64 shifts: a 'while n' loop would never end")
def reverse_loop_nomask(n):
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1); n >>= 1
    return r
assert all(reverse_loop_nomask(n) == brute(n) for n in range(-5000, 5000))
print("a fixed 32-round loop with no mask also gives the right answer on [-5000, 5000] (n & 1 and >> are arithmetic); the mask makes it explicit")
# seeded random + exhaustive-style checks
for _ in range(2000):
    n = random.choice([random.randint(-2 ** 31, 2 ** 32 - 1), random.randint(-8, 8), 1 << random.randint(0, 31)])
    assert reverse_loop(n) == reverse_dc(n) == brute(n), n
print("2000 seeded random values agree with the string-reversal oracle")
for n in range(-3000, 3001):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
for n in range(0, 2 ** 32, 2 ** 32 // 1000 + 1):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
print("exhaustive window [-3000, 3000] and a 1000-point sweep of 0..2^32 agree")
# involution and range
for _ in range(500):
    n = random.randint(0, M32)
    assert reverse_loop(reverse_loop(n)) == n and 0 <= reverse_loop(n) <= M32
print("reversing twice gives the original pattern (500 random), result always in 0..2^32-1")
# edge asserts
assert reverse_loop(2 ** 31) == 1 and reverse_loop(0) == 0 and reverse_dc(-1) == M32
assert reverse_loop(-2 ** 31) == 1
print("edge asserts ok")
```

**Output (my run):**
```text
6 prompt examples ok
dry run n=6 as 32 bits: 00000000000000000000000000000110
  reversed             : 01100000000000000000000000000000 = 1610612736
divide-and-conquer on n=6, value after each of the five steps (32-bit hex):
   ['00060000', '06000000', '60000000', '90000000', '60000000'] -> final 1610612736
--- why the mask (Python 3.13, observed) ---
-1 >> 1 = -1 | -1 >> 100 = -1 | -2147483648 >> 40 = -1
loop 'while n: n >>= 1' on n=-1 stopped only because of the cap of 40 steps; after the cap n is still -1
without the mask, -1 << 16 = -65536 (no 32-bit wrap) ; with the mask, (-1 << 16) & 0xFFFFFFFF = 4294901760
-1 & 0xFFFFFFFF = 4294967295 | -2147483648 & 0xFFFFFFFF = 2147483648
every negative n in [-3000, -1] is -1 after 64 shifts: a 'while n' loop would never end
a fixed 32-round loop with no mask also gives the right answer on [-5000, 5000] (n & 1 and >> are arithmetic); the mask makes it explicit
2000 seeded random values agree with the string-reversal oracle
exhaustive window [-3000, 3000] and a 1000-point sweep of 0..2^32 agree
reversing twice gives the original pattern (500 random), result always in 0..2^32-1
edge asserts ok
```

**Edge cases:**
- `n = -1` reads as 32 ones: result 4294967295.
- `n = -2147483648` reads as `1` followed by 31 zeros: result 1.
- `n = 0` gives 0; `n = 4294967295` gives itself.
- `n = 1` gives 2^31 = 2147483648, which is NOT a negative number here: the answer is unsigned.

**Follow-ups:**
- *Called millions of times?* Precompute the reversal of every byte (256 entries) and combine four lookups with shifts.
- *Reverse only the used bits (not 32)?* Use `n.bit_length()` rounds; that is a different question.
- *Return a signed 32-bit result?* Convert: `r - (1 << 32) if r >= 1 << 31 else r`.

**Common mistakes:**
- No mask on a negative input with a `while n:` loop (never ends), or with the five-step version (wider than 32 bits).
- Stopping the loop when `n == 0`: the trailing zeros must still be shifted in. 32 rounds always.
- Forgetting `& M32` after `n << 16` in the mask version.
- Treating the output as signed.

---

### Q18 ⭐⭐ 🟡 Subsets with duplicates. `nums` has 0 <= len <= 10 integers and may repeat values. Return every DISTINCT subset (as a multiset: [1, 2] and [2, 1] are the same subset, and two subsets with the same values are the same subset) once. Each subset is a list in ascending order and the outer list is sorted ascending with Python's list comparison; `nums = []` returns `[[]]`. Sort first and skip a value equal to its left neighbour when it is at the same recursion level (`i > start and a[i] == a[i-1]`); explain why the skip must test `i > start` and not `i > 0`, with a small case where `i > 0` loses a subset. The distinct-values version is Q4. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of sorted tuples from a bitmask loop on small inputs. Example: nums=[3, 1, 3] -> [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]; nums=[] -> [[]]; nums=[2, 2, 2] -> [[], [2], [2, 2], [2, 2, 2]]; nums=[1, 2, 2, 1] -> [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 2], [1, 2], [1, 2, 2], [2], [2, 2]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index (subsets) and a sort-then-skip rule for duplicates.

**Say this first (1 line):** "Sort, then loop from `start`; every call is one answer; skip `a[i]` when `i > start` and it equals `a[i - 1]`, because that value was already tried as the next pick at this level."

**Brute force:** Enumerate all 2^n bitmasks, build each subset of the sorted input as a tuple, put them in a set to drop repeats, then sort. Correct (my oracle) but always does 2^n work even when there are few distinct subsets: `[2, 2, 2, 2, 2, 2]` has only 7 distinct subsets and 64 masks.

**Optimal:**
- Sort a copy of `nums` so equal values are neighbours and each subset comes out in ascending order.
- `go(start)`: append a copy of `cur` (every node of the tree is an answer), then for `i` in `start..n-1` add `a[i]`, recurse with `i + 1`, remove it.
- Skip rule: `if i > start and a[i] == a[i - 1]: continue`. At one level of the tree the loop chooses "which value is the next element". Picking the second `2` after the first `2` at the same level would just produce the same set again.
- Why `i > start` and not `i > 0`: when `i == start`, `a[i - 1]` is the element already chosen at the PARENT level (it is in `cur`), so using an equal `a[i]` is allowed and is how `[2, 2]` is built. `i > 0` wrongly skips it. On `[1, 2, 2]` it loses `[1, 2, 2]` and `[2, 2]`, and on 300 seeded random inputs it is wrong 178 times (output below).
- Output order: the DFS visits a node before its children and siblings in ascending order, which is exactly Python's list comparison order (a prefix comes before its extensions). The code asserts the raw list is already sorted. `nums = []` returns `[[]]`.
- Recursion depth is at most 10 (the number of elements), far below 1000.
- The distinct-values version is Q4.

**Complexity:** Time O(n * D) where D is the number of distinct subsets (each is copied, up to n items): at most O(n * 2^n), about 10 * 1024 steps for n = 10. D equals the product over distinct values of (count + 1); the code checks it. Space O(n) recursion plus the output. Node visits: the skip version makes exactly D calls (one per answer, no wasted calls); the no-skip version makes 2^n calls and dedupes at the end.

**Dry run:** `[1, 2, 2]`, tree (each line is a call and an answer):
```
[]
  [1]
    [1, 2]
      [1, 2, 2]
    skip index 2 (second 2 at this level)
  [2]
    [2, 2]
  skip index 2 (second 2 at this level)
```
6 calls, 6 subsets. Without the skip there would be 8 calls and `[1, 2]` and `[2]` would appear twice. For `[3, 1, 3]` the sorted input is `[1, 3, 3]` and the answer is `[[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]`.

**Code:**
```python
import random

random.seed(1218)

def subsets_dup(nums, stats=None):
    """Sort, then loop from `start`; skip a value equal to its left neighbour at the SAME level (i > start)."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(cur[:])                      # every node of this tree is one answer
        for i in range(start, len(a)):
            if i > start and a[i] == a[i - 1]:
                continue                        # same value already tried as the next element at this level
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    if stats is not None: stats.append(calls)
    assert out == sorted(out)                   # the DFS preorder is already the required order (prefix before extension, siblings ascending)
    return out

def subsets_no_skip(nums):
    """Same tree without the skip: 2^n calls, then dedupe at the end. Shows the waste."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(tuple(cur))
        for i in range(start, len(a)):
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(map(list, set(out))), calls

def subsets_wrong_skip(nums):
    """WRONG on purpose: i > 0 instead of i > start."""
    a = sorted(nums)
    out, cur = [], []
    def go(start):
        out.append(cur[:])
        for i in range(start, len(a)):
            if i > 0 and a[i] == a[i - 1]:
                continue
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(out)

def brute(nums):
    n = len(nums)
    return sorted(map(list, {tuple(sorted(nums[i] for i in range(n) if m >> i & 1)) for m in range(1 << n)}))

for nums, want in [([3, 1, 3], [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]), ([], [[]]),
                   ([2, 2, 2], [[], [2], [2, 2], [2, 2, 2]]),
                   ([1, 2, 2, 1], [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 2], [1, 2], [1, 2, 2], [2], [2, 2]])]:
    assert subsets_dup(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# decision tree on [1, 2, 2]
print("--- decision tree for [1, 2, 2] (a node = a call = one answer) ---")
a = [1, 2, 2]
def show(start, cur, depth):
    print("  " * depth + str(cur))
    for i in range(start, len(a)):
        if i > start and a[i] == a[i - 1]:
            print("  " * (depth + 1) + "skip index %d (value %d equals its left neighbour at this level)" % (i, a[i]))
            continue
        show(i + 1, cur + [a[i]], depth + 1)
show(0, [], 0)

# the wrong skip
print("--- i > 0 instead of i > start ---")
good, bad = subsets_dup([1, 2, 2]), subsets_wrong_skip([1, 2, 2])
print("correct:", good)
print("i > 0  :", bad, "| lost:", [s for s in good if s not in bad])
wrong_cases = 0
for _ in range(300):
    nums = [random.randint(1, 3) for _ in range(random.randint(0, 6))]
    if subsets_wrong_skip(nums) != brute(nums): wrong_cases += 1
print("i > 0 wrong on", wrong_cases, "of 300 seeded random inputs")
assert wrong_cases > 0

# node counts
print("--- calls (nodes) ---")
for nums in ([1, 2, 2], [1, 2, 2, 1], [2, 2, 2, 2, 2, 2], [1, 1, 2, 2, 3, 3, 4, 4], list(range(8))):
    st = []
    res = subsets_dup(nums, st)
    _, plain = subsets_no_skip(nums)
    print("%-26s distinct=%3d calls with skip=%3d calls without skip=%3d" % (nums, len(res), st[0], plain))
    assert st[0] == len(res)

# seeded random cross-check
for _ in range(300):
    nums = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    assert subsets_dup(nums) == brute(nums) == subsets_no_skip(nums)[0], nums
print("300 seeded random inputs agree with the bitmask-set oracle")
# the count of distinct subsets is the product of (multiplicity + 1)
import collections, math
for _ in range(200):
    nums = [random.randint(1, 4) for _ in range(random.randint(0, 9))]
    assert len(subsets_dup(nums)) == math.prod(c + 1 for c in collections.Counter(nums).values())
print("200 seeded random inputs: number of distinct subsets = product of (multiplicity + 1)")
# edge asserts
assert subsets_dup([]) == [[]]
assert subsets_dup([5]) == [[], [5]]
assert len(subsets_dup(list(range(10)))) == 1024
assert len(subsets_dup([7] * 10)) == 11
x = [3, 1, 3]; subsets_dup(x); assert x == [3, 1, 3]       # input not mutated (we sort a copy)
print("edge asserts ok")
```

**Output (my run):**
```text
4 prompt examples ok
--- decision tree for [1, 2, 2] (a node = a call = one answer) ---
[]
  [1]
    [1, 2]
      [1, 2, 2]
    skip index 2 (value 2 equals its left neighbour at this level)
  [2]
    [2, 2]
  skip index 2 (value 2 equals its left neighbour at this level)
--- i > 0 instead of i > start ---
correct: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
i > 0  : [[], [1], [1, 2], [2]] | lost: [[1, 2, 2], [2, 2]]
i > 0 wrong on 178 of 300 seeded random inputs
--- calls (nodes) ---
[1, 2, 2]                  distinct=  6 calls with skip=  6 calls without skip=  8
[1, 2, 2, 1]               distinct=  9 calls with skip=  9 calls without skip= 16
[2, 2, 2, 2, 2, 2]         distinct=  7 calls with skip=  7 calls without skip= 64
[1, 1, 2, 2, 3, 3, 4, 4]   distinct= 81 calls with skip= 81 calls without skip=256
[0, 1, 2, 3, 4, 5, 6, 7]   distinct=256 calls with skip=256 calls without skip=256
300 seeded random inputs agree with the bitmask-set oracle
200 seeded random inputs: number of distinct subsets = product of (multiplicity + 1)
edge asserts ok
```

**Edge cases:**
- `[]` gives `[[]]`; one element gives `[[], [x]]`.
- All equal (`[2, 2, 2]`): n + 1 subsets.
- All distinct: 2^n subsets, and the skip never fires (256 calls for 8 distinct values, same as without it).
- The input list must not be mutated: sort a copy (checked).

**Follow-ups:**
- *Iterative version?* Start with `[[]]`; for each distinct value with count c, extend every existing subset with 1..c copies. Same output set; sort at the end if the order must match.
- *Permutations with duplicates?* Different skip rule; see Q19 (the skip rule there is about a used array, not a start index).
- *Count only?* Multiply (count + 1) over distinct values; no enumeration needed (the code checks this identity).

**Common mistakes:**
- Using `i > 0` instead of `i > start`.
- Not sorting first, so equal values are not neighbours and the skip does nothing.
- Appending `cur` instead of `cur[:]`, so every answer ends up the same empty list.
- Returning duplicates and "fixing" it with a set of lists (lists are unhashable; convert to tuples) instead of preventing them.

---

### Q19 ⭐⭐ 🟡 Permutations with duplicates. `nums` has 0 <= len <= 8 integers and may repeat values. Return every DISTINCT arrangement once, as lists, with the outer list sorted ascending with Python's list comparison; `nums = []` returns `[[]]`. State the number of results as n! divided by the product of the factorials of the multiplicities. Sort first, keep a `used` array and skip a value when it equals its left neighbour and that neighbour is NOT used (`not used[i-1]`); explain why that rule keeps equal values in their original relative order, and why testing `used[i-1]` instead gives the same count but is a different (wasteful) pruning. The distinct-values version is Q6. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of tuples from itertools.permutations on small inputs. Example: nums=[2, 1, 2] -> [[1, 2, 2], [2, 1, 2], [2, 2, 1]]; nums=[5] -> [[5]]; nums=[] -> [[]]; nums=[3, 3, 1, 1] -> [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over positions with a `used` array, plus a sort-then-skip rule to stop equal values from producing the same arrangement twice. Same skeleton as Q6 (distinct values); only the skip line is new.

**Say this first (1 line):** "Sort, then at each position try each unused value, but skip a value if its equal left neighbour is not used: that forces equal values to be placed in their original left-to-right order, so each distinct arrangement appears exactly once."

**Brute force:** Generate all `n!` permutations with `itertools.permutations`, drop repeats with a set, sort. Time O(n * n!) even when there are few distinct results (for `[1]*8` it builds 40320 tuples to return one). Used as the oracle.

**Optimal:**
- Sort `nums`. Keep `used[i]` and a `cur` list. At each level loop over indices `i` in order.
- Skip rule: `if i and a[i] == a[i-1] and not used[i-1]: continue`.
- Why it works: call equal values twins, tagged in sorted order (1a, 1b). The rule lets 1b be placed only when 1a is already placed. So in every leaf 1a sits to the left of 1b, 1b left of 1c, and so on. Each distinct arrangement corresponds to exactly one tagged arrangement with the twins in that order, so it is produced once. Tested in the code by tagging the twins.
- Count of results: `n! / (m1! * m2! * ...)` where `m` are the multiplicities (a multinomial). `[3,3,1,1]` gives `4!/(2!*2!) = 6`.
- The other rule, `used[i-1]` (skip when the twin IS used), is also correct: it forces the reverse order (1b before 1a). The count is the same. But it only notices the clash after the twin has already been placed, so it walks into whole sub-trees and cuts them late. On `[1,1,2,2]` it makes 33 calls against 19. Correct, but wasteful.

**Complexity:** Output size alone is `n!/prod(m!)` lists of length `n`, so time is O(n * n!/prod(m!)) for the copies; the work inside the tree is within a factor of `n` of that because with the tight rule every call leads to at least one result (no dead branches). Extra space O(n) for `cur`, `used`, and the recursion (depth `n <= 8`, far below CPython's limit of 1000). The sorted-input trick makes the outer list come out in ascending list order without a final sort.

**Dry run:** `nums = [2, 1, 2]`, sorted `[1, 2, 2]` at indices 0, 1, 2. The code prints this tree (indent is depth).
- Level 1: pick index 0 (value 1) -> `[1]`; pick index 1 (value 2) -> `[2]`; index 2 is skipped: its twin at index 1 is not used.
- Under `[1]`: pick index 1 -> `[1,2]`, then index 2 -> leaf `[1,2,2]`. Index 2 at that level is skipped (twin 1 not used).
- Under `[2]` (index 1): pick index 0 -> `[2,1]` -> pick index 2 -> leaf `[2,1,2]`; pick index 2 -> `[2,2]` -> pick index 0 -> leaf `[2,2,1]`. Here index 2 is allowed because its twin (index 1) IS used.
- Three leaves, in ascending order: `[1,2,2]`, `[2,1,2]`, `[2,2,1]`. Multinomial `3!/2! = 3`.
- Node counts (calls): plain `used`-array search 16 for 6 leaves (3 distinct after dedupe); tight rule 9; the other rule 12.

**Code:**
```python
import itertools, random, math, collections

random.seed(19)

def perms_dup(nums, rule='left_unused'):
    """Distinct permutations. rule 'left_unused': skip a[i] if a[i]==a[i-1] and NOT used[i-1] (correct, tight).
    rule 'left_used': skip if a[i]==a[i-1] and used[i-1] (also correct, but prunes late). Returns (result, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n:
            out.append(cur[:]); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1]:
                if rule == 'left_unused' and not used[i - 1]: continue
                if rule == 'left_used' and used[i - 1]: continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go()
    return out, calls

def no_skip(nums):
    """Plain permutations with a used array and no duplicate rule: n! leaves, many repeated. Returns (list, calls)."""
    a = sorted(nums); n = len(a); used = [False] * n; cur = []; out = []; calls = 0
    def go():
        nonlocal calls
        calls += 1
        if len(cur) == n: out.append(cur[:]); return
        for i in range(n):
            if not used[i]:
                used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return out, calls

def permutations_dup(nums):
    return perms_dup(nums)[0]          # already in ascending order because the input is sorted and we try indices in order

def brute(nums):
    return sorted(map(list, set(itertools.permutations(nums))))

def multinomial(nums):
    c = collections.Counter(nums); r = math.factorial(len(nums))
    for v in c.values(): r //= math.factorial(v)
    return r

# examples
for nums, exp in [([2, 1, 2], [[1, 2, 2], [2, 1, 2], [2, 2, 1]]), ([5], [[5]]), ([], [[]]),
                  ([3, 3, 1, 1], [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]])]:
    got = permutations_dup(nums)
    assert got == exp == brute(nums), nums
    print('example', nums, '->', got)

# decision tree of [1, 1, 2] under the correct rule (indent = depth; X = skipped by the rule)
def show_tree(nums):
    a = sorted(nums); n = len(a); used = [False] * n; cur = []
    def go(d):
        if len(cur) == n:
            print('  ' * d + '-> leaf', cur); return
        for i in range(n):
            if used[i]: continue
            if i and a[i] == a[i - 1] and not used[i - 1]:
                print('  ' * d + f'skip index {i} (value {a[i]}): twin at {i-1} not used'); continue
            used[i] = True; cur.append(a[i]); print('  ' * d + f'pick index {i} -> {cur}'); go(d + 1); cur.pop(); used[i] = False
    go(0)
print('decision tree for [2, 1, 2] (sorted: [1, 2, 2]):')
show_tree([2, 1, 2])

# node counts: no rule vs correct rule vs the other rule, on [1, 1, 2, 2]
for nums in ([1, 2, 2], [1, 1, 2, 2], [1, 1, 1, 2, 2, 3]):
    r0, c0 = no_skip(nums); r1, c1 = perms_dup(nums, 'left_unused'); r2, c2 = perms_dup(nums, 'left_used')
    assert sorted(r1) == brute(nums) and sorted(r2) == brute(nums)
    print(f'{nums}: results={len(r1)} (multinomial {multinomial(nums)}); calls no-rule={c0} (leaves {len(r0)}), left-unused rule={c1}, left-used rule={c2}')

# claim 1: count = multinomial; both rules correct and left-unused never more calls (all multisets of 5 values from {1,2,3}, plus length 0..4)
worse = 0; total = 0
for L in range(0, 7):
    for nums in itertools.product([1, 2, 3], repeat=L):
        if L > 5 and sum(nums) % 7: continue       # thin the length-6 family to keep it quick
        total += 1
        r1, c1 = perms_dup(list(nums), 'left_unused'); r2, c2 = perms_dup(list(nums), 'left_used')
        assert len(r1) == multinomial(nums) and r1 == sorted(r1) and len(set(map(tuple, r1))) == len(r1)
        assert sorted(r2) == r1
        assert c1 <= c2
        worse += c1 < c2
print('inputs checked', total, '| count == multinomial and both rules right on all; left-unused fewer calls on', worse)

# claim 2: equal values keep their ORIGINAL relative order (tag the twins and look at the generated order)
a = [(1, 'a'), (1, 'b'), (2, 'c')]
tagged = []
used = [False] * 3; cur = []
def go():
    if len(cur) == 3: tagged.append([t[1] for t in cur]); return
    for i in range(3):
        if used[i]: continue
        if i and a[i][0] == a[i - 1][0] and not used[i - 1]: continue
        used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
go()
print('tagged twins 1a, 1b, 2c; each leaf lists tags in order:', tagged)
assert all(t.index('a') < t.index('b') for t in tagged)

# seeded random cross-check against set(itertools.permutations)
for _ in range(400):
    n = random.randint(0, 7); nums = [random.randint(0, 3) for _ in range(n)]
    assert permutations_dup(nums) == brute(nums), nums
print('400 seeded random cases agree')

# edge asserts
assert permutations_dup([]) == [[]] and permutations_dup([7, 7, 7]) == [[7, 7, 7]]
assert permutations_dup([-1, 0, -1]) == [[-1, -1, 0], [-1, 0, -1], [0, -1, -1]]
assert len(permutations_dup([1, 2, 3, 4, 5, 6, 7, 8])) == 40320 and len(permutations_dup([1] * 8)) == 1
print('edge asserts passed; 8 distinct values ->', len(permutations_dup(list(range(8)))), 'results; recursion depth <= 8')
```

**Output (my run):**
```
example [2, 1, 2] -> [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
example [5] -> [[5]]
example [] -> [[]]
example [3, 3, 1, 1] -> [[1, 1, 3, 3], [1, 3, 1, 3], [1, 3, 3, 1], [3, 1, 1, 3], [3, 1, 3, 1], [3, 3, 1, 1]]
decision tree for [2, 1, 2] (sorted: [1, 2, 2]):
pick index 0 -> [1]
  pick index 1 -> [1, 2]
    pick index 2 -> [1, 2, 2]
      -> leaf [1, 2, 2]
  skip index 2 (value 2): twin at 1 not used
pick index 1 -> [2]
  pick index 0 -> [2, 1]
    pick index 2 -> [2, 1, 2]
      -> leaf [2, 1, 2]
  pick index 2 -> [2, 2]
    pick index 0 -> [2, 2, 1]
      -> leaf [2, 2, 1]
skip index 2 (value 2): twin at 1 not used
[1, 2, 2]: results=3 (multinomial 3); calls no-rule=16 (leaves 6), left-unused rule=9, left-used rule=12
[1, 1, 2, 2]: results=6 (multinomial 6); calls no-rule=65 (leaves 24), left-unused rule=19, left-used rule=33
[1, 1, 1, 2, 2, 3]: results=60 (multinomial 60); calls no-rule=1957 (leaves 720), left-unused rule=189, left-used rule=517
inputs checked 460 | count == multinomial and both rules right on all; left-unused fewer calls on 444
tagged twins 1a, 1b, 2c; each leaf lists tags in order: [['a', 'b', 'c'], ['a', 'c', 'b'], ['c', 'a', 'b']]
400 seeded random cases agree
edge asserts passed; 8 distinct values -> 40320 results; recursion depth <= 8
```

Reading the output:
- All four examples match the `set(itertools.permutations)` oracle.
- Calls on `[1,1,1,2,2,3]`: 1957 with no rule (720 leaves, 60 distinct), 517 with the `used[i-1]` rule, 189 with the tight rule. The tight rule's calls scale with the answer, not with `n!`.
- Over 460 small inputs (every list of values from {1,2,3} of length 0 to 5, plus a thinned set of length 6) the count equals the multinomial, both rules return the right set, and the tight rule never makes more calls (fewer on 444; equal on the all-distinct ones).
- Tagged twins: every leaf has `a` before `b`, as the argument says.
- 400 seeded random lists agree with the oracle.

**Edge cases:**
- `[]` returns `[[]]`.
- One value, or all values equal: one result.
- Negative numbers and zero: sorting handles them.
- 8 distinct values: 40320 results, the largest output here.

**Follow-ups:**
- "Swap-in-place variant?" Possible, but sorting plus a `used` array is simpler for duplicates. In-place swapping needs a per-level set of values already tried at that position.
- "Next permutation instead of listing?" Part 1 Q34 steps to the next arrangement in this same order in O(n) with no recursion; it also handles duplicates.
- "Count only?" Use the multinomial formula, no search.

**Common mistakes:**
- Not sorting first: equal values are then not adjacent and the neighbour test misses them.
- Testing `a[i] == a[i-1]` without the `used` condition: kills valid results such as `[2,2,1]`.
- Using `i > 0` with `used[i-1]` backwards and thinking it is wrong: both directions are correct, one is just slower.
- Appending `cur` instead of a copy `cur[:]`.
- Putting the results in a set of tuples to dedupe afterwards: correct, but it throws away the pruning.

### Q20 ⭐⭐ 🟡 Combinations n choose k. `n` and `k` are integers with 1 <= k <= n <= 20. Return every k-element subset of 1..n as an ascending list; the outer list is sorted ascending with Python's list comparison (so the first is [1, 2, ..., k]). The number of results is C(n, k) (at most 184756). Use a start index so each combination is built once, and add the pruning bound: from start `s` you need at least `k - len(path)` more numbers, so the loop can stop at `n - (k - len(path)) + 1`; explain how much work this saves with a node count on one example. Depth is k <= 20. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.combinations on small inputs. Example: n=5, k=3 -> [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]; n=3, k=3 -> [[1, 2, 3]]; n=4, k=1 -> [[1], [2], [3], [4]]; n=1, k=1 -> [[1]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index (choose in increasing order, so each subset is built once) and a feasibility bound on the loop (do not start a branch that cannot finish).

**Say this first (1 line):** "Build the subset in ascending order with a start index; and stop the loop early at `n - (k - len(path)) + 1`, because past that point there are not enough numbers left to reach size `k`."

**Brute force:** `itertools.combinations(range(1, n+1), k)`, which is also the oracle. Or, the unpruned recursion: same start-index tree but the loop always runs to `n`. It finds the same `C(n, k)` answers but visits many dead nodes whose path can never reach length `k`.

**Optimal:**
- `go(start)`: if `len(path) == k`, record a copy. Otherwise loop `v` from `start` to `hi`, push `v`, call `go(v + 1)`, pop.
- Start index: after choosing `v`, only larger numbers follow, so `[1,3]` is built but `[3,1]` never is. Each subset is built exactly once, already ascending, and the outer list comes out in ascending list order for free.
- Pruning rule: we still need `need = k - len(path)` numbers, all from `v..n`. The last value that leaves room is `v = n - need + 1`. So `hi = n - (k - len(path)) + 1`. Every node visited with this rule leads to at least one answer, so there are no dead nodes.
- Node count: the number of nodes at depth `d` is the number of valid prefixes, `C(n-k+d, d)`. So calls are `sum_{d=0..k} C(n-k+d, d)`. Checked for all `1 <= k <= n <= 8` in the code.

**Complexity:** Output is `C(n, k)` lists of length `k`, so time O(k * C(n, k)) for the copies. With pruning, the tree has `sum_d C(n-k+d, d)` nodes, which is O(k * C(n, k)) at worst, no wasted exponential. Without pruning the tree can be far larger than the output (see the table below). Space O(k) for the path and recursion (depth `k <= 20`, far below the limit of 1000), apart from the output. Largest case: `C(20, 10) = 184756` results.

**Dry run:** `n = 5, k = 3`. The bound `hi` is 3 at depth 0, 4 at depth 1, 5 at depth 2.
- Root: `v` runs 1..3 (4 and 5 cannot leave room for two more numbers).
- Pick 1: next `v` runs 2..4. Pick 2, then 3..5 gives `[1,2,3]`, `[1,2,4]`, `[1,2,5]`. Pick 3, then 4..5 gives `[1,3,4]`, `[1,3,5]`. Pick 4, then 5 gives `[1,4,5]`. (5 is not tried at this level: nothing would follow.)
- Pick 2: `[2,3,4]`, `[2,3,5]`, `[2,4,5]`. Pick 3: `[3,4,5]`.
- 10 results. Calls: 1 + 3 + 6 + 10 = 20 nodes (`C(2,0)+C(3,1)+C(4,2)+C(5,3)`). Without the bound the loop runs to 5 everywhere and visits 26 nodes, 6 of them dead (for instance `[4]` and `[5]` at the top, and `[1,5]`).
- The code also prints the full pruned tree for `n=4, k=2`.

**Code:**
```python
import itertools, random, math

random.seed(20)

def combinations(n, k, prune=True):
    """All k-subsets of 1..n ascending. Returns (result, calls). prune=True stops the loop at n-(k-len(path))+1."""
    out = []; path = []; calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        if len(path) == k:
            out.append(path[:]); return
        hi = n - (k - len(path)) + 1 if prune else n      # last value that still leaves room for the rest
        for v in range(start, hi + 1):
            path.append(v); go(v + 1); path.pop()
    go(1)
    return out, calls

def solve(n, k): return combinations(n, k)[0]
def brute(n, k): return sorted(map(list, itertools.combinations(range(1, n + 1), k)))

for n, k, exp in [(5, 3, [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]),
                  (3, 3, [[1, 2, 3]]), (4, 1, [[1], [2], [3], [4]]), (1, 1, [[1]])]:
    got = solve(n, k)
    assert got == exp == brute(n, k)
    print('example', (n, k), '->', got)

# decision tree for n=4, k=2 with pruning (X = value cut by the bound)
def tree(n, k):
    path = []
    def go(start, d):
        if len(path) == k: print('  ' * d + '-> leaf', path); return
        hi = n - (k - len(path)) + 1
        for v in range(start, hi + 1):
            path.append(v); print('  ' * d + f'pick {v} -> {path}'); go(v + 1, d + 1); path.pop()
        if hi < n: print('  ' * d + f'(loop stops at {hi}; values {hi + 1}..{n} cannot leave room for {k - len(path)} number(s))')
    go(1, 0)
print('decision tree n=4, k=2 (pruned):'); tree(4, 2)

# node counts: pruned vs unpruned
print('calls (nodes visited), pruned vs unpruned:')
for n, k in [(5, 3), (6, 4), (10, 8), (12, 10), (20, 19), (20, 10)]:
    r1, c1 = combinations(n, k, True); r0, c0 = combinations(n, k, False)
    assert r1 == r0 and len(r1) == math.comb(n, k)
    print(f'  n={n:2d} k={k:2d}: results={len(r1):6d}  pruned={c1:7d}  unpruned={c0:7d}  dead nodes removed={c0 - c1}')

# claim: pruned search has no dead nodes: every call is on a path to a result, calls = sum over depth of C(n, depth)-ish. Check exact formula
# number of calls at depth d = number of valid prefixes of length d = C(n-k+d, d) ... verify by counting
for n in range(1, 9):
    for k in range(1, n + 1):
        r1, c1 = combinations(n, k, True)
        assert c1 == sum(math.comb(n - k + d, d) for d in range(k + 1)), (n, k)
print('pruned calls == sum_d C(n-k+d, d) for all 1 <= k <= n <= 8')
# and unpruned never fewer than pruned
for n in range(1, 11):
    for k in range(1, n + 1):
        assert combinations(n, k, True)[1] <= combinations(n, k, False)[1]
print('pruned calls <= unpruned calls for all 1 <= k <= n <= 10')

# size claim
big = solve(20, 10)
assert len(big) == 184756 == math.comb(20, 10) and big[0] == list(range(1, 11)) and big[-1] == list(range(11, 21))
print('C(20, 10) =', len(big), ' first', big[0], ' last', big[-1])
assert max(math.comb(20, k) for k in range(1, 21)) == 184756

# seeded random cross-check vs itertools.combinations
for _ in range(300):
    n = random.randint(1, 9); k = random.randint(1, n)
    assert solve(n, k) == brute(n, k) == sorted(solve(n, k))
print('300 seeded random cases agree; also exhaustive over 1 <= k <= n <= 10')
for n in range(1, 11):
    for k in range(1, n + 1): assert solve(n, k) == brute(n, k)
assert solve(1, 1) == [[1]] and solve(4, 4) == [[1, 2, 3, 4]]
print('edge asserts passed; depth is k <= 20, recursion limit 1000 is no problem')
```

**Output (my run):**
```
example (5, 3) -> [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]
example (3, 3) -> [[1, 2, 3]]
example (4, 1) -> [[1], [2], [3], [4]]
example (1, 1) -> [[1]]
decision tree n=4, k=2 (pruned):
pick 1 -> [1]
  pick 2 -> [1, 2]
    -> leaf [1, 2]
  pick 3 -> [1, 3]
    -> leaf [1, 3]
  pick 4 -> [1, 4]
    -> leaf [1, 4]
pick 2 -> [2]
  pick 3 -> [2, 3]
    -> leaf [2, 3]
  pick 4 -> [2, 4]
    -> leaf [2, 4]
pick 3 -> [3]
  pick 4 -> [3, 4]
    -> leaf [3, 4]
(loop stops at 3; values 4..4 cannot leave room for 2 number(s))
calls (nodes visited), pruned vs unpruned:
  n= 5 k= 3: results=    10  pruned=     20  unpruned=     26  dead nodes removed=6
  n= 6 k= 4: results=    15  pruned=     35  unpruned=     57  dead nodes removed=22
  n=10 k= 8: results=    45  pruned=    165  unpruned=   1013  dead nodes removed=848
  n=12 k=10: results=    66  pruned=    286  unpruned=   4083  dead nodes removed=3797
  n=20 k=19: results=    20  pruned=    210  unpruned=1048575  dead nodes removed=1048365
  n=20 k=10: results=184756  pruned= 352716  unpruned= 616666  dead nodes removed=263950
pruned calls == sum_d C(n-k+d, d) for all 1 <= k <= n <= 8
pruned calls <= unpruned calls for all 1 <= k <= n <= 10
C(20, 10) = 184756  first [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  last [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
300 seeded random cases agree; also exhaustive over 1 <= k <= n <= 10
edge asserts passed; depth is k <= 20, recursion limit 1000 is no problem
```

Reading the output:
- All four examples match `itertools.combinations`.
- The pruned tree for `n=4, k=2` shows the bound cutting the top-level loop at 3.
- Node counts are exact counts of calls. For `n=20, k=19` the answer has 20 lists, the pruned search makes 210 calls, the unpruned search makes 1,048,575 (it walks through every ascending subset of 1..20). For `n=20, k=10` the saving is smaller (352,716 against 616,666) because most nodes there are useful anyway.
- The formula for the pruned call count holds for all `k <= n <= 8`, and pruned is never above unpruned for `n <= 10`.
- 300 seeded random cases plus an exhaustive sweep to `n = 10` agree with the oracle.

**Edge cases:**
- `k = n`: one result, `[1..n]`; the loop bound is tight at every level.
- `k = 1`: `n` singletons.
- `n = k = 1`: `[[1]]`.
- Largest outputs: `n = 20`, `k = 10`, 184756 lists. The memory is for the answer itself.

**Follow-ups:**
- "Where does the pruning matter most?" When `k` is close to `n`: the unpruned tree explores every ascending subset (up to `2^n`) while the answer has only `C(n, k)` lists.
- "Do it without recursion?" Keep an index array `c[0..k-1]` and advance it like an odometer (find the rightmost index that can still grow), or use `itertools.combinations`.
- "With duplicates in the input?" Sort and skip equal neighbours at the same level, as in Q21.

**Common mistakes:**
- Recursing with `go(v)` instead of `go(v + 1)`: reuses numbers.
- Looping from 1 each time instead of `start`: builds permutations, each subset `k!` times.
- Bound off by one: `n - need + 1` is inclusive, so the `range` end is `n - need + 2`.
- Appending `path` instead of `path[:]`; every result becomes the same (empty) list.

### Q21 ⭐⭐ 🟡 Combination sum II (each number used once, duplicates in the input). `candidates` has 1 <= len <= 14 positive integers (each <= 30, repeats allowed) and `target` is 1 <= target <= 40. Return every combination that sums to `target` using each INPUT ELEMENT at most once; two combinations with the same values count once. Each combination is a non-decreasing list and the outer list is sorted ascending with Python's list comparison; return an empty list if none exists. Sort, recurse with `start = j + 1`, skip a value equal to its left neighbour at the same level (`j > start and c[j] == c[j-1]`), and break when `c[j] > remaining`. Say how this differs from Q8 (reuse allowed, so recurse with `j`). In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of sorted tuples from a bitmask over all subsets on small inputs. Example: candidates=[3, 1, 1, 2, 4, 2], target=6 -> [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]; candidates=[2, 2, 2], target=4 -> [[2, 2]]; candidates=[5, 6], target=3 -> []; candidates=[4], target=4 -> [[4]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index that moves forward (`j + 1`, each input element at most once), a sort so equal values sit together, a same-level skip for duplicates, and a `break` once the number is too big.

**Say this first (1 line):** "Sort, recurse with `j + 1` because each element is used once, skip a value equal to its left neighbour at the same level (`j > start`), and break when the number exceeds what is left."

**Brute force:** Try all `2^n` subsets with a bitmask (`n <= 14`, at most 16384), keep the ones summing to `target`, put each into a set as a sorted tuple, sort. Correct, always `O(n * 2^n)`. Used as the oracle.

**Optimal:**
- `go(start, rem)`: if `rem == 0`, record. Else for `j` from `start`: if `c[j] > rem` break (sorted, so all later values are too big); if `j > start` and `c[j] == c[j-1]` continue; take `c[j]`, call `go(j + 1, rem - c[j])`, undo.
- Why `j > start` and not `j > 0`: at a given level, the first copy of a value (`j == start`) is allowed, because its left neighbour was used at a shallower level and is legitimately in the path. Only a second copy tried at the SAME level would repeat a combination already found. The code shows that `j > 0` loses `[1,1,2]` for input `[1,1,2]`, target 4.
- Why the skip is right: choosing the first or the second 2 as "the" 2 at one level leads to the same set of combinations below, so one is enough.
- Difference from Q8 (reuse allowed): there the next call is `go(j, ...)` (same index) and the candidates are distinct; here it is `go(j + 1, ...)` and the skip rule is needed because the input has repeats.

**Complexity:** Worst case still exponential, O(2^n) nodes (all elements distinct, target large) with `n <= 14`. The two prunings only cut: the skip removes whole repeated sub-trees (it takes `[1]*7 + [2]*7` with target 14 from 14920 calls to 48) and the break cuts loop steps. Each result costs O(n) to copy. Space O(n) for the path and recursion depth (at most 14, far below the limit of 1000), plus the output.

**Dry run:** sorted candidates `[1, 1, 2, 2, 3, 4]`, target 6. The code prints the whole tree; the main branches:
- Take `c[0]=1` (remaining 5), then `c[1]=1` (remaining 4), then `c[2]=2` (remaining 2), then `c[3]=2`: hit `[1,1,2,2]`. Next `c[4]=3 > 2`: break.
- Back at the level after `[1,1]`: `c[3]=2` is skipped (same as the left neighbour at this level). Take `3` -> remaining 1, break; take `4` -> hit `[1,1,4]`.
- Under `[1]` take `c[2]=2`: `[1,2,2]` has remaining 1, break; `[1,2,3]` hit. Skip `c[3]=2` at that level. Take 3 and 4: no hits.
- Top level: `c[1]=1` is skipped (twin of `c[0]` at the same level). Take `c[2]=2`: `[2,4]` hit. Skip `c[3]`. Take 3 and 4: none.
- Four hits, in ascending order: `[1,1,2,2]`, `[1,1,4]`, `[1,2,3]`, `[2,4]`. Calls: 18 with both rules; 32 with no skip rule (the repeated twins re-explore the same sub-trees).

**Code:**
```python
import itertools, random

random.seed(21)

def comb_sum2(candidates, target, skip=True, brk=True):
    """Each input element at most once; each distinct combination once. Returns (result, calls)."""
    c = sorted(candidates); out = []; cur = []; calls = 0; iters = 0
    def go(start, rem):
        nonlocal calls, iters
        calls += 1
        if rem == 0:
            out.append(cur[:]); return
        for j in range(start, len(c)):
            iters += 1
            if c[j] > rem:
                if brk: break
                continue
            if skip and j > start and c[j] == c[j - 1]: continue     # same value already tried at this level
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target)
    comb_sum2.iters = iters
    return out, calls

def solve(candidates, target): return sorted(comb_sum2(candidates, target)[0])

def brute(candidates, target):
    n = len(candidates); res = set()
    for mask in range(1, 1 << n):
        sub = tuple(sorted(candidates[i] for i in range(n) if mask >> i & 1))
        if sum(sub) == target: res.add(sub)
    return sorted(map(list, res))

for cand, t, exp in [([3, 1, 1, 2, 4, 2], 6, [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]),
                     ([2, 2, 2], 4, [[2, 2]]), ([5, 6], 3, []), ([4], 4, [[4]])]:
    got = solve(cand, t)
    assert got == exp == brute(cand, t)
    print('example', cand, t, '->', got)

def tree(cand, target):
    c = sorted(cand); cur = []
    def go(start, rem, d):
        if rem == 0: print('  ' * d + '-> hit', cur); return
        for j in range(start, len(c)):
            if c[j] > rem: print('  ' * d + f'break: c[{j}]={c[j]} > remaining {rem}'); break
            if j > start and c[j] == c[j - 1]: print('  ' * d + f'skip c[{j}]={c[j]} (same as left neighbour at this level)'); continue
            cur.append(c[j]); print('  ' * d + f'take c[{j}]={c[j]} -> {cur}, remaining {rem - c[j]}'); go(j + 1, rem - c[j], d + 1); cur.pop()
    go(0, target, 0)
print('decision tree, sorted candidates [1, 1, 2, 2, 3, 4], target 6:'); tree([3, 1, 1, 2, 4, 2], 6)

# node counts: all four combinations of the two prunings on the first example and a larger one
def compare(cand, t):
    row = {}
    for skip in (False, True):
        for brk in (False, True):
            r, calls = comb_sum2(cand, t, skip, brk); row[(skip, brk)] = (calls, comb_sum2.iters)
            assert len(set(map(tuple, r))) == len(solve(cand, t)) and sorted(set(map(tuple, r))) == sorted(map(tuple, solve(cand, t)))
    return row
for cand, t in [([3, 1, 1, 2, 4, 2], 6), ([1] * 7 + [2] * 7, 14), ([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5], 20)]:
    row = compare(cand, t)
    print(f'{len(cand)} candidates, target {t}, answers {len(solve(cand, t))}: (calls, loop steps): neither={row[(False, False)]}, break only={row[(False, True)]}, skip only={row[(True, False)]}, both={row[(True, True)]}')

# without the skip rule duplicates appear:
r, _ = comb_sum2([2, 2, 2], 4, skip=False)
print('no skip rule on [2, 2, 2], target 4:', r, '(three copies of [2, 2])')
# with j > 0 instead of j > start the valid [1, 1, 2] is lost for [1, 1, 2], target 4
def wrong_skip(candidates, target):
    c = sorted(candidates); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            if j > 0 and c[j] == c[j - 1]: continue            # WRONG: compares with the global left neighbour
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target); return out
print('wrong test j > 0 on [1, 1, 2], target 4 ->', wrong_skip([1, 1, 2], 4), ' correct ->', solve([1, 1, 2], 4))
assert wrong_skip([1, 1, 2], 4) == [] and solve([1, 1, 2], 4) == [[1, 1, 2]]

# Q8 difference: recursing with j reuses an element
def reuse(candidates, target):
    c = sorted(set(candidates)); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            cur.append(c[j]); go(j, rem - c[j]); cur.pop()
    go(0, target); return out
print('Q8 style (reuse, recurse with j) on [3, 1, 2, 4], target 6:', reuse([3, 1, 2, 4], 6))
print('once-each (this question) on [3, 1, 2, 4], target 6:', solve([3, 1, 2, 4], 6))

# properties and seeded random cross-check vs bitmask
for _ in range(400):
    n = random.randint(1, 10); cand = [random.randint(1, 6) for _ in range(n)]; t = random.randint(1, 20)
    got = solve(cand, t)
    assert got == brute(cand, t), (cand, t)
    assert got == sorted(got) and len({tuple(x) for x in got}) == len(got)
    assert all(x == sorted(x) and sum(x) == t for x in got)
print('400 seeded random cases agree (sorted, no duplicates, each sums to target)')

# edge and max size asserts
assert solve([4], 4) == [[4]] and solve([5, 6], 3) == [] and solve([1], 2) == []
big = solve([1] * 14, 14); assert big == [[1] * 14]
print('14 ones, target 14 ->', len(big), 'combination; depth up to 14, well under the recursion limit of 1000')
print('edge asserts passed')
```

**Output (my run):**
```
example [3, 1, 1, 2, 4, 2] 6 -> [[1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 4]]
example [2, 2, 2] 4 -> [[2, 2]]
example [5, 6] 3 -> []
example [4] 4 -> [[4]]
decision tree, sorted candidates [1, 1, 2, 2, 3, 4], target 6:
take c[0]=1 -> [1], remaining 5
  take c[1]=1 -> [1, 1], remaining 4
    take c[2]=2 -> [1, 1, 2], remaining 2
      take c[3]=2 -> [1, 1, 2, 2], remaining 0
        -> hit [1, 1, 2, 2]
      break: c[4]=3 > remaining 2
    skip c[3]=2 (same as left neighbour at this level)
    take c[4]=3 -> [1, 1, 3], remaining 1
      break: c[5]=4 > remaining 1
    take c[5]=4 -> [1, 1, 4], remaining 0
      -> hit [1, 1, 4]
  take c[2]=2 -> [1, 2], remaining 3
    take c[3]=2 -> [1, 2, 2], remaining 1
      break: c[4]=3 > remaining 1
    take c[4]=3 -> [1, 2, 3], remaining 0
      -> hit [1, 2, 3]
    break: c[5]=4 > remaining 3
  skip c[3]=2 (same as left neighbour at this level)
  take c[4]=3 -> [1, 3], remaining 2
    break: c[5]=4 > remaining 2
  take c[5]=4 -> [1, 4], remaining 1
skip c[1]=1 (same as left neighbour at this level)
take c[2]=2 -> [2], remaining 4
  take c[3]=2 -> [2, 2], remaining 2
    break: c[4]=3 > remaining 2
  take c[4]=3 -> [2, 3], remaining 1
    break: c[5]=4 > remaining 1
  take c[5]=4 -> [2, 4], remaining 0
    -> hit [2, 4]
skip c[3]=2 (same as left neighbour at this level)
take c[4]=3 -> [3], remaining 3
  break: c[5]=4 > remaining 3
take c[5]=4 -> [4], remaining 2
6 candidates, target 6, answers 4: (calls, loop steps): neither=(32, 51), break only=(32, 46), skip only=(18, 32), both=(18, 29)
14 candidates, target 14, answers 4: (calls, loop steps): neither=(14920, 15647), break only=(14920, 15471), skip only=(48, 232), both=(48, 226)
14 candidates, target 20, answers 40: (calls, loop steps): neither=(8728, 12572), break only=(8728, 11041), skip only=(404, 989), both=(404, 890)
no skip rule on [2, 2, 2], target 4: [[2, 2], [2, 2], [2, 2]] (three copies of [2, 2])
wrong test j > 0 on [1, 1, 2], target 4 -> []  correct -> [[1, 1, 2]]
Q8 style (reuse, recurse with j) on [3, 1, 2, 4], target 6: [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2], [1, 1, 1, 3], [1, 1, 2, 2], [1, 1, 4], [1, 2, 3], [2, 2, 2], [2, 4], [3, 3]]
once-each (this question) on [3, 1, 2, 4], target 6: [[1, 2, 3], [2, 4]]
400 seeded random cases agree (sorted, no duplicates, each sums to target)
14 ones, target 14 -> 1 combination; depth up to 14, well under the recursion limit of 1000
edge asserts passed
```

Reading the output:
- All four examples match the bitmask oracle.
- Node counts: "calls" is the number of recursive calls and "loop steps" is how often the inner loop body starts. The skip rule is the big saver in calls (14920 down to 48 on the two-value input); the break only saves loop steps (15647 down to 15471 without the skip rule, 232 down to 226 with it). They do different jobs.
- Without the skip rule `[2,2,2]` target 4 returns `[2,2]` three times; with `j > 0` the valid `[1,1,2]` is lost.
- The Q8 contrast on `[3,1,2,4]`, target 6: reuse gives 9 combinations including `[1,1,1,1,1,1]`; once-each gives only `[1,2,3]` and `[2,4]`.
- 400 seeded random inputs agree, each output sorted, duplicate-free, with every combination summing to the target.

**Edge cases:**
- No combination (`[5,6]`, target 3): `[]`.
- All equal (`[2,2,2]`, target 4): one result.
- A single element equal to the target: one result.
- Target bigger than the total sum: the search ends with no result; a cheap pre-check on the total would skip the search.
- `14` ones with target 14: depth 14, one result.

**Follow-ups:**
- "Why not use a set of tuples to remove duplicates?" It is right but explores every duplicate sub-tree first; the skip rule never builds them.
- "Count instead of list?" Group equal values with counts and do a bounded knapsack DP over the target (Part 10 style); no list needed.
- "Reuse allowed but duplicates in the input?" Deduplicate first, then it is Q8.

**Common mistakes:**
- Forgetting to sort: neighbours are not equal, so the skip never triggers.
- `j > 0` instead of `j > start`.
- `go(j, ...)` instead of `go(j + 1, ...)`: reuses an element.
- Using `continue` instead of `break` on `c[j] > rem`: correct but slower.
- Appending the live `cur` instead of a copy.

### Q22 ⭐⭐ 🟡 Palindrome partitioning (list all). `s` is a lowercase string with 1 <= len <= 16. Return every way to cut `s` into consecutive pieces that are all palindromes: each partition is a list of the pieces in order, and the outer list is sorted ascending with Python's list comparison. For 'aaa' the single piece 'aaa' counts as a partition. Recurse over the cut position and test each piece with `t == t[::-1]`; then precompute an `is_pal[i][j]` table so each test is O(1) and say what that changes (the number of partitions can be 2^(n-1), so listing them stays exponential). Part 11 Q19 asks the optimisation version (fewest cuts) as a DP instead of a list. Depth is at most 16. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying all 2^(n-1) sets of cut positions on small inputs. Example: s='abba' -> [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]; s='xyz' -> [['x', 'y', 'z']]; s='aaa' -> [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]; s='a' -> [['a']].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over cut positions: at position `i`, try every piece `s[i:j]`, and only recurse when the piece is a palindrome. The palindrome test is the pruning.

**Say this first (1 line):** "At each position I try each possible next piece, keep only the palindromic ones, and recurse after it. Dead ends are cut the moment a piece is not a palindrome, and a precomputed table makes that test O(1)."

**Brute force:** Try all `2^(n-1)` sets of cut positions (each gap between letters is cut or not), build the pieces, keep the sets where every piece is a palindrome. `n <= 16` gives at most 32768 sets, each checked in O(n). Used as the oracle. It does the full exponential work even for `'abcdefghijklmnop'`, whose only answer is the all-singles split.

**Optimal:**
- `go(i)`: if `i == n`, record the partition. Else for `j` from `i + 1` to `n`: `t = s[i:j]`; if `t == t[::-1]`, push `t`, call `go(j)`, pop.
- The pruning rule is "only recurse on a palindromic piece". A non-palindromic piece is never extended, so none of the partitions built from it are visited. Every single letter is a palindrome, so every call can finish: no dead nodes beyond the failed piece tests.
- Table version: `is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])`, filled with `i` going down. O(n^2) once. Then each test is one lookup instead of a slice, a reverse and a compare (O(piece length)).
- What the table changes and what it does not: it cuts the cost of each test from O(L) to O(1), so the work between recursive calls drops. It does NOT change how many partitions exist, nor how many calls are made (same counts in the output). For `a^n` the answer has `2^(n-1)` partitions, so listing is exponential whatever the test costs.
- Order: pieces are tried short to long, so the output is already ascending in Python's list order (`['a','b','b','a']` before `['a','bb','a']` before `['abba']`); sorting is only a safety net, and the code checks it is unnecessary.

**Complexity:** Output: up to `2^(n-1)` partitions of total length `n` each, so O(n * 2^(n-1)) in the worst case (`'aaaa...'`). Search with the table: each call does up to `n` constant-time tests, so time is O(n * number of calls) plus the O(n^2) table; calls are at most about `2^n`. Space: table O(n^2) (256 cells here), path and recursion depth at most 16, plus the output.

**Dry run:** `s = 'abba'` (printed as a tree by the code).
- Position 0: piece `'a'` is a palindrome. Position 1: `'b'` ok; position 2: `'b'` ok; position 3: `'a'` ok; position 4 = end: record `['a','b','b','a']`.
- Back at position 2: piece `'ba'` is not a palindrome: pruned.
- Back at position 1: piece `'bb'` ok; position 3: `'a'`: record `['a','bb','a']`. Piece `'bba'`: pruned.
- Back at position 0: `'ab'` and `'abb'` pruned. `'abba'` ok: record `['abba']`.
- Three partitions. The recursion makes 8 calls and 11 piece tests; the unpruned search would try all `2^3 = 8` cut sets and check each one.

**Code:**
```python
import itertools, random

random.seed(22)

def partition_slice(s):
    """Recurse over the cut position; test each piece with t == t[::-1]. Returns (result, calls, piece_tests, char_compares_upper_bound)."""
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == len(s):
            out.append(cur[:]); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]; st['tests'] += 1
            if t == t[::-1]:
                cur.append(t); go(j); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def partition_table(s):
    """Same recursion, but each piece test is a lookup in is_pal[i][j] (inclusive ends), built once in O(n^2)."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1])
    out = []; cur = []; st = {'calls': 0, 'tests': 0}
    def go(i):
        st['calls'] += 1
        if i == n:
            out.append(cur[:]); return
        for j in range(i, n):
            st['tests'] += 1
            if is_pal[i][j]:
                cur.append(s[i:j + 1]); go(j + 1); cur.pop()
    go(0)
    return out, st['calls'], st['tests']

def solve(s): return sorted(partition_table(s)[0])

def brute(s):
    n = len(s); out = []
    for mask in range(1 << (n - 1)):                       # bit i set = cut after position i
        cuts = [i + 1 for i in range(n - 1) if mask >> i & 1]; ed = [0] + cuts + [n]
        parts = [s[ed[i]:ed[i + 1]] for i in range(len(ed) - 1)]
        if all(p == p[::-1] for p in parts): out.append(parts)
    return sorted(out)

for s, exp in [('abba', [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]), ('xyz', [['x', 'y', 'z']]),
               ('aaa', [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]), ('a', [['a']])]:
    got = solve(s)
    assert got == exp == brute(s) == sorted(partition_slice(s)[0])
    print('example', repr(s), '->', got)

def tree(s):
    cur = []
    def go(i, d):
        if i == len(s): print('  ' * d + '-> partition', cur); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if t == t[::-1]:
                cur.append(t); print('  ' * d + f'cut piece {t!r} -> {cur}'); go(j, d + 1); cur.pop()
            else: print('  ' * d + f'piece {t!r} is not a palindrome: pruned')
    go(0, 0)
print("decision tree for 'abba':"); tree('abba')

# node counts: palindrome-pruned search vs trying every cut set (2^(n-1) leaves, each with n-1 cut bits)
print('calls / piece tests for the recursion (slice test vs table), and the unpruned number of cut sets 2^(n-1):')
for s in ['abba', 'aaaaaaaa', 'abcdefgh', 'abababab', 'a' * 16, 'abcdefghijklmnop']:
    r1, c1, t1 = partition_slice(s); r2, c2, t2 = partition_table(s)
    assert r1 == r2 and r1 == sorted(r1)
    print(f'  {s:18s} partitions={len(r1):6d} calls={c1:6d} piece tests={t1:7d} (table: {t2}) unpruned cut sets={2 ** (len(s) - 1)}')

# claim: all-equal letters give 2^(n-1) partitions (n <= 12 exhaustive), so listing stays exponential even with the table
for n in range(1, 13): assert len(solve('a' * n)) == 2 ** (n - 1)
print('a^n has exactly 2^(n-1) partitions for n = 1..12; a^16 ->', len(solve('a' * 16)))

# the table builds in O(n^2) and the recursion does a bounded number of table lookups per call (n at most)
# seeded random cross-check vs all 2^(n-1) cut sets
for _ in range(300):
    n = random.randint(1, 12); s = ''.join(random.choice('ab') if random.random() < .8 else random.choice('abc') for _ in range(n))
    assert solve(s) == brute(s), s
    assert partition_slice(s)[0] == sorted(partition_slice(s)[0]) == solve(s)
print('300 seeded random strings (length 1..12) agree; both versions return the list already sorted')

# edge asserts
assert solve('a') == [['a']] and solve('ab') == [['a', 'b']] and solve('aa') == [['a', 'a'], ['aa']]
assert len(solve('abcdefghijklmnop')) == 1
print('edge asserts passed; depth <= 16, recursion limit 1000 is no issue')
```

**Output (my run):**
```
example 'abba' -> [['a', 'b', 'b', 'a'], ['a', 'bb', 'a'], ['abba']]
example 'xyz' -> [['x', 'y', 'z']]
example 'aaa' -> [['a', 'a', 'a'], ['a', 'aa'], ['aa', 'a'], ['aaa']]
example 'a' -> [['a']]
decision tree for 'abba':
cut piece 'a' -> ['a']
  cut piece 'b' -> ['a', 'b']
    cut piece 'b' -> ['a', 'b', 'b']
      cut piece 'a' -> ['a', 'b', 'b', 'a']
        -> partition ['a', 'b', 'b', 'a']
    piece 'ba' is not a palindrome: pruned
  cut piece 'bb' -> ['a', 'bb']
    cut piece 'a' -> ['a', 'bb', 'a']
      -> partition ['a', 'bb', 'a']
  piece 'bba' is not a palindrome: pruned
piece 'ab' is not a palindrome: pruned
piece 'abb' is not a palindrome: pruned
cut piece 'abba' -> ['abba']
  -> partition ['abba']
calls / piece tests for the recursion (slice test vs table), and the unpruned number of cut sets 2^(n-1):
  abba               partitions=     3 calls=     8 piece tests=     11 (table: 11) unpruned cut sets=8
  aaaaaaaa           partitions=   128 calls=   256 piece tests=    255 (table: 255) unpruned cut sets=128
  abcdefgh           partitions=     1 calls=     9 piece tests=     36 (table: 36) unpruned cut sets=128
  abababab           partitions=    21 calls=    55 piece tests=     87 (table: 87) unpruned cut sets=128
  aaaaaaaaaaaaaaaa   partitions= 32768 calls= 65536 piece tests=  65535 (table: 65535) unpruned cut sets=32768
  abcdefghijklmnop   partitions=     1 calls=    17 piece tests=    136 (table: 136) unpruned cut sets=32768
a^n has exactly 2^(n-1) partitions for n = 1..12; a^16 -> 32768
300 seeded random strings (length 1..12) agree; both versions return the list already sorted
edge asserts passed; depth <= 16, recursion limit 1000 is no issue
```

Reading the output:
- All four examples agree with the cut-set oracle.
- Node counts: on `'abcdefghijklmnop'` the pruned search makes 17 calls (one per position plus the end) against 32768 cut sets unpruned. On `'abababab'`: 55 calls against 128. On `'a'*16` there is no pruning to be had: 65536 calls, 32768 partitions (every cut set is valid).
- The slice test and the table test give identical call and test counts: the table only makes each test cheaper.
- `a^n` gives `2^(n-1)` partitions for `n = 1..12` (exhaustive), and 32768 at `n = 16`.
- 300 seeded random strings of length 1 to 12 over `a`, `b`, `c` agree with the oracle.

**Edge cases:**
- Single letter: `[['a']]`.
- No repeated letters: only the all-singles split.
- All equal letters: `2^(n-1)` partitions, the worst case for output size.
- Whole string a palindrome: the one-piece partition is included (`'aaa'` gives `['aaa']`).

**Follow-ups:**
- "Fewest cuts instead of a list?" That is a DP: Part 11 Q19. It counts in O(n^2) and never lists.
- "Count the partitions?" Also a DP, `ways[i]` over suffixes using the same `is_pal` table.
- "Expand-around-centre instead of the table?" Same O(n^2) total, no table; each centre expands while it matches.

**Common mistakes:**
- Using `i` to `j` inclusive in one place and exclusive in another when building `is_pal`.
- Forgetting the piece of the whole remaining string (`j` must reach `n`).
- Appending `cur` without copying.
- Thinking the table makes the whole thing polynomial. It cannot: the output itself can have `2^(n-1)` lists.

### Q23 ⭐⭐ 🟡 Restore IP addresses. `s` is a string of digits with 0 <= len <= 12. Return every valid IPv4 address (four parts separated by '.') you can make by inserting three dots into `s` without reordering or removing digits. A part is valid if it is an integer 0..255 written without a leading zero ('0' alone is fine, '01' and '00' are not). Return the addresses sorted ascending as strings, an empty list if none exists (also for len < 4 or len > 12). Recurse over the part index with part lengths 1, 2, 3, and say why the search tree has at most 3^4 = 81 leaves, so it is O(1) in the length. In the answer include a dry run on the first example and a seeded random cross-check of your solution against choosing three cut positions with itertools.combinations on small inputs. Example: s='1921681' -> ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']; s='0000' -> ['0.0.0.0']; s='010010' -> ['0.10.0.10', '0.100.1.0']; s='111' -> []; s='' -> [].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Fixed-depth backtracking: four parts, each of length 1, 2 or 3, validity checked per part, so the tree is tiny whatever the input.

**Say this first (1 line):** "Four parts, each 1 to 3 digits, so the tree has at most 3^4 = 81 leaves. I recurse over the part index, reject a part with a leading zero or a value above 255, and accept only when four parts use up the whole string."

**Brute force:** Choose three cut positions from the `n - 1` gaps with `itertools.combinations`, split, and validate all four parts. That is `C(11, 3) = 165` choices at `n = 12`, each checked in constant time. Also O(1) in practice; it is the oracle.

**Optimal:**
- `go(i, parts)`: if four parts are placed, accept only when `i == len(s)`. Else try lengths 1, 2, 3.
- A part `t` is valid when `len(t) == L` (enough characters), it has no leading zero unless it is exactly `'0'` (`L > 1 and t[0] == '0'` rejects `'01'`, `'00'`), and `int(t) <= 255`.
- Extra length prune (optional): with `left` parts to place and `rest` characters, give up unless `left <= rest <= 3 * left`. It cuts the long strings and the short strings at the root.
- Why at most 81 leaves: four levels, three choices at each level, `3^4 = 81`. The whole tree has at most `1 + 3 + 9 + 27 + 81 = 121` calls. This does not grow with `len(s)`; `len(s)` only decides which paths are valid, and a string longer than 12 or shorter than 4 has no address.
- Order: the code sorts the strings at the end, which is the order the question asks for (plain string order, where `'.'` sorts before the digits, so `'1.9.216.81'` comes before `'1.92.16.81'`).

**Complexity:** O(1) with respect to `len(s)`: at most 121 calls, each doing O(1) work (slices of at most 3 characters), plus a sort of the addresses. Since `len(s) <= 12` can give at most 81 leaf choices, there are at most 81 addresses (in fact far fewer: the most in the examples is 11). Space O(1): recursion depth 4.

**Dry run:** `'010010'`; the code prints the tree.
- Part 1 can only be `'0'` (`'01'` and `'010'` have a leading zero).
- After `'0'` the rest is `10010`, so part 2 is `'1'`, `'10'` or `'100'`.
  - `'1'`: then part 3 `'0'`, part 4 `'0'` leaves 2 characters (`'10'`): dead. Part 3 `'00'`/`'001'`: leading zero.
  - `'10'`: part 3 `'0'`: part 4 `'1'` leaves 1 character (dead) or `'10'` finishes: `0.10.0.10`. Part 3 `'01'`, `'010'`: leading zero.
  - `'100'`: part 3 `'1'`: part 4 `'0'` finishes: `0.100.1.0`. Part 3 `'10'`: the length prune stops it (0 characters left for 1 part).
- Two addresses: `0.10.0.10` and `0.100.1.0`.

**Code:**
```python
import itertools, random

random.seed(23)

def restore(s, prune_len=True):
    """Returns (sorted addresses, calls). Part lengths 1, 2, 3 tried in that order; no leading zero; value <= 255.
    prune_len=True also stops when the remaining characters cannot fit the remaining parts."""
    out = []; calls = 0
    def go(i, parts):
        nonlocal calls
        calls += 1
        left = 4 - len(parts)
        if left == 0:
            if i == len(s): out.append('.'.join(parts))
            return
        rest = len(s) - i
        if prune_len and not (left <= rest <= 3 * left): return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L or (L > 1 and t[0] == '0') or int(t) > 255: continue
            go(i + L, parts + [t])
    go(0, [])
    return sorted(out), calls

def solve(s): return restore(s)[0]

def brute(s):
    n = len(s); out = []
    if n < 4: return out
    for cuts in itertools.combinations(range(1, n), 3):
        ps = [s[a:b] for a, b in zip((0,) + cuts, cuts + (n,))]
        if all(str(int(p)) == p and int(p) <= 255 for p in ps): out.append('.'.join(ps))
    return sorted(out)

for s, exp in [('1921681', ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']),
               ('0000', ['0.0.0.0']), ('010010', ['0.10.0.10', '0.100.1.0']), ('111', []), ('', [])]:
    got = solve(s)
    assert got == exp == brute(s)
    print('example', repr(s), '->', got)

def tree(s):
    def go(i, parts, d):
        left = 4 - len(parts)
        if left == 0:
            print('  ' * d + ('-> address ' + '.'.join(parts) if i == len(s) else f'-> parts full but {len(s) - i} char(s) left: dead')); return
        rest = len(s) - i
        if not (left <= rest <= 3 * left): print('  ' * d + f'prune: {rest} char(s) cannot fill {left} part(s)'); return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L: continue
            if L > 1 and t[0] == '0': print('  ' * d + f'{t!r}: leading zero'); continue
            if int(t) > 255: print('  ' * d + f'{t!r}: > 255'); continue
            print('  ' * d + f'part {t!r}'); go(i + L, parts + [t], d + 1)
    go(0, [], 0)
print("decision tree for '010010':"); tree('010010')

# node counts
print('calls: length-pruned vs basic (validity only), 3^4 = 81 leaf choices at most:')
for s in ['1921681', '010010', '0000', '111', '255255255255', '999999999999', '1' * 12, '1' * 13]:
    a, ca = restore(s, True); b, cb = restore(s, False)
    assert a == b
    print(f'  {s:14s} answers={len(a):3d} calls pruned={ca:4d} basic={cb:4d}')

# claim: tree has at most 3^4 = 81 leaves, so at most 1 + 3 + 9 + 27 + 81 = 121 calls
mx = 0; seen = 0
for L in range(0, 9):
    for tup in itertools.product('012', repeat=L):
        s = ''.join(tup); seen += 1
        r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
for _ in range(3000):
    s = ''.join(random.choice('0123456789' if random.random() < .5 else '1250') for _ in range(random.randint(0, 12)))
    r, c = restore(s, False); assert c <= 121 and r == brute(s); mx = max(mx, c)
print('basic search never made more than', mx, 'calls (bound 121) over', seen, 'exhaustive strings (digits 0,1,2, length <= 8) + 3000 random ones')

# seeded random cross-check against three-cut-position oracle, with lengths 0..12
for _ in range(400):
    s = ''.join(random.choice('0012559') for _ in range(random.randint(0, 12)))
    assert solve(s) == brute(s), s
print('400 seeded random strings agree with itertools.combinations of cut positions')

# edge asserts
assert solve('') == [] and solve('111') == [] and solve('1' * 13) == [] and solve('0000') == ['0.0.0.0']
assert solve('25525511135') == ['255.255.11.135', '255.255.111.35']
assert solve('256256256256') == [] and solve('255255255255') == ['255.255.255.255'] and solve('00000') == []
assert solve('101023') == sorted(['1.0.10.23', '1.0.102.3', '10.1.0.23', '10.10.2.3', '101.0.2.3'])
print('edge asserts passed')
```

**Output (my run):**
```
example '1921681' -> ['1.9.216.81', '1.92.16.81', '1.92.168.1', '19.2.16.81', '19.2.168.1', '19.21.6.81', '19.21.68.1', '19.216.8.1', '192.1.6.81', '192.1.68.1', '192.16.8.1']
example '0000' -> ['0.0.0.0']
example '010010' -> ['0.10.0.10', '0.100.1.0']
example '111' -> []
example '' -> []
decision tree for '010010':
part '0'
  part '1'
    part '0'
      part '0'
        -> parts full but 2 char(s) left: dead
      '01': leading zero
      '010': leading zero
    '00': leading zero
    '001': leading zero
  part '10'
    part '0'
      part '1'
        -> parts full but 1 char(s) left: dead
      part '10'
        -> address 0.10.0.10
    '01': leading zero
    '010': leading zero
  part '100'
    part '1'
      part '0'
        -> address 0.100.1.0
    part '10'
      prune: 0 char(s) cannot fill 1 part(s)
'01': leading zero
'010': leading zero
calls: length-pruned vs basic (validity only), 3^4 = 81 leaf choices at most:
  1921681        answers= 11 calls pruned=  51 basic=  55
  010010         answers=  2 calls pruned=  13 basic=  13
  0000           answers=  1 calls pruned=   5 basic=   5
  111            answers=  0 calls pruned=   1 basic=   8
  255255255255   answers=  1 calls pruned=  13 basic=  69
  999999999999   answers=  0 calls pruned=   3 basic=  31
  111111111111   answers=  1 calls pruned=  13 basic= 121
  1111111111111  answers=  0 calls pruned=   1 basic= 121
basic search never made more than 104 calls (bound 121) over 9841 exhaustive strings (digits 0,1,2, length <= 8) + 3000 random ones
400 seeded random strings agree with itertools.combinations of cut positions
edge asserts passed
```

Reading the output:
- All five examples agree with the three-cut oracle.
- Node counts (calls). With the length prune: `'1921681'` takes 51 calls for 11 addresses; `'111'` takes 1 call (rejected at the root) against 8 without it; `'1'*13` takes 1 call against 121. Without the prune the largest tree is 121, the bound derived above; over 9841 exhaustive short strings and 3000 random ones the maximum seen was 104.
- 400 seeded random strings of length 0 to 12 (digits from `0,1,2,5,9`) agree with the oracle.
- Edge asserts include `'25525511135'` (two addresses), `'256256256256'` (none: 256 is too big) and `'00000'` (none: five digits but a `'0'` part uses exactly one).

**Edge cases:**
- `''`, length below 4 or above 12: `[]` straight away.
- `'0000'`: only `0.0.0.0`; every part is `'0'`.
- Leading zeros: `'01'`, `'00'`, `'010'` are rejected, `'0'` is fine.
- `'255255255255'`: one address; `'256256256256'`: none.
- A leading `'0'` forces a one-digit first part.

**Follow-ups:**
- "IPv6?" Eight groups of hex, up to 4 digits: the same shape with 8 levels and 4 choices; still a bounded tree.
- "Count only?" The same recursion with a counter, or a small DP over (position, parts placed).
- "Validate an address instead?" Split on `'.'` and apply the same part test.

**Common mistakes:**
- Rejecting `'0'` itself along with `'00'`.
- Using `int(t) > 255` without the leading-zero test: `'01'` converts to 1.
- Accepting four parts that do not consume the whole string.
- Not checking `len(t) == L`: a slice past the end is shorter and gets accepted as a part.
- Treating this as O(3^n): the depth is fixed at four.

### Q24 ⭐⭐ 🟡 Autocomplete with counts. `entries` is a list of 1 to 2000 pairs `[word, count]` (distinct lowercase words of length 1 to 20, count a positive integer) and `queries` is a list of 1 to 2000 non-empty lowercase prefixes. For each query return up to the 3 best words that start with the prefix, ordered by count descending and, for equal counts, by word ascending; fewer than 3 if fewer words match, an empty list if none. Build the trie once and store at every node the best 3 `(count, word)` pairs of the words below it (updated while inserting), so a query is O(L) plus 3 copies; compare with collecting every word under the prefix and sorting, whose cost grows with the size of the subtree. Say what happens to the stored lists when a count changes later (they must be updated along the whole path). In the answer include a dry run on the first example and a seeded random cross-check of your solution against filtering all words by `startswith` and sorting on small inputs. Example: entries=[['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]], queries=['ca', 'car', 'd', 'x', 'cat'] -> [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]; entries=[['a', 1]], queries=['a', 'ab'] -> [['a'], []]; entries=[['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], queries=['a'] -> [['ab', 'ac', 'ad']].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie with a cached answer at every node: the best 3 `(count, word)` pairs below it. Pay a little on insert to make each query a walk down the prefix plus a copy.

**Say this first (1 line):** "Walk the prefix in O(L), then read the top 3 already stored at that node. Insert pushes each word's (count, word) onto every node of its path and keeps only the best 3 there."

**Brute force:** For each query, filter all words with `startswith(prefix)`, sort by `(-count, word)`, take 3. O(W * L) to filter per query (`W` words) plus the sort of the matches. A trie-only variant (walk to the prefix node, collect every word below it, sort) skips the filter but still touches the whole subtree, which for a short prefix is most of the dictionary.

**Optimal:**
- Node: children dict, optional count of a word ending here, and `top`: a list of at most 3 `(-count, word)` pairs.
- Insert `(word, count)`: walk or create nodes; at every node on the path (not the root: prefixes are non-empty) add `(-count, word)` to `top`, sort, keep 3. Storing `-count` makes the sort order exactly "count descending, then word ascending".
- Query `prefix`: walk; if a step is missing return `[]`; else return the words of `top`.
- Why 3 per node is enough: the best 3 words below a node are the best 3 among the best 3 of its children and the word ending at the node itself. So a node never needs more than the top 3 of each child.
- Count changes later: every node on the word's path holds a copy of the old count, so all of them must be refreshed. A RAISE is a simple merge. A LOWER is harder: the word may drop out of a node's list and a word that was not stored (the fourth best) must come back. Rebuild each list on the path bottom-up from the node's own count and its children's lists. The code does this, and the last demo shows it: lowering `ab` brings back `ae`, which no node stored for `'a'`.

**Complexity:** Query O(L) to walk + O(1) to copy 3 words (against O(subtree size * log) for collect-and-sort, or O(W * L) for the filter). Insert O(L * K log K) with `K = 3`: constant per node. Update O(L * (alphabet * K)) with the rebuild. Space: one node per distinct prefix (5435 nodes for 2000 random words in the run), each with a list of at most 3 pairs: O(total letters * K) in the worst case. Memory is the price of the fast query.

**Dry run:** `entries = car 5, cart 9, care 9, cat 2, dog 7`.
- Insert `car` (5): nodes `c`, `ca`, `car` each get `[(5,'car')]`.
- Insert `cart` (9): `c`, `ca`, `car`, `cart` get it; `car`'s list is now `[(9,'cart'),(5,'car')]`.
- Insert `care` (9): lists at `c`, `ca`, `car` become `[(9,'care'),(9,'cart'),(5,'car')]` (equal counts break by word, `'care' < 'cart'`).
- Insert `cat` (2): `c`'s list is full, `cat` is the 4th best and drops out; `ca` too; node `cat` holds `[(2,'cat')]`. Insert `dog`: node `d` holds `[(7,'dog')]`.
- Queries: `'ca'` reads the list at `ca`: `care, cart, car`. `'car'`: same list. `'d'`: `dog`. `'x'`: no child, `[]`. `'cat'`: `cat`. The code prints the stored lists.

**Code:**
```python
import random, string, heapq

random.seed(24)
K = 3

class AutoTrie:
    """Trie with, at every node, the best K (-count, word) pairs of the words at or below that node."""
    def __init__(self):
        self.root = {'c': {}, 'top': [], 'cnt': None}      # 'cnt' is the count if a word ends here
        self.nodes = 1
    def insert(self, word, count):
        nd = self.root
        path = [nd]
        for ch in word:
            if ch not in nd['c']:
                nd['c'][ch] = {'c': {}, 'top': [], 'cnt': None}; self.nodes += 1
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p in path[1:]:                                  # update the whole path (the root list is never queried: prefixes are non-empty)
            p['top'] = sorted([e for e in p['top'] if e[1] != word] + [(-count, word)])[:K]
    def set_count(self, word, count):
        """Change a count later. Raising is a merge; LOWERING may need words that were not stored, so rebuild each list on the path from the children's lists."""
        nd = self.root; path = [nd]
        for ch in word:
            nd = nd['c'][ch]; path.append(nd)
        nd['cnt'] = count
        for p, w in zip(reversed(path[1:]), reversed(range(1, len(path)))):
            cand = [] if p['cnt'] is None else [(-p['cnt'], word[:w])]
            for child in p['c'].values(): cand += child['top']
            p['top'] = sorted(cand)[:K]
    def query(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd['c'].get(ch)
            if nd is None: return []
        return [w for _, w in nd['top']]

def solve(entries, queries):
    t = AutoTrie()
    for w, c in entries: t.insert(w, c)
    return [t.query(p) for p in queries]

def brute(entries, queries):
    return [[w for c, w in sorted((-c, w) for w, c in entries if w.startswith(p))[:K]] for p in queries]

for ent, qs, exp in [([['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]], ['ca', 'car', 'd', 'x', 'cat'],
                       [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]),
                     ([['a', 1]], ['a', 'ab'], [['a'], []]),
                     ([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a'], [['ab', 'ac', 'ad']])]:
    got = solve(ent, qs)
    assert got == exp == brute(ent, qs)
    print('example', ent, qs, '->', got)

# what is stored along the path for example 1
t = AutoTrie()
for w, c in [['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]]: t.insert(w, c)
print('stored top-3 per node, example 1:')
for pre in ['c', 'ca', 'car', 'cat', 'care', 'cart', 'd']:
    nd = t.root
    for ch in pre: nd = nd['c'][ch]
    print(f'  {pre!r:7}: {[(-c, w) for c, w in nd["top"]]}')

# work comparison on a larger set: words visited by "collect everything under the prefix and sort" versus stored lists
rnd = random.Random(240)
words = set()
while len(words) < 2000: words.add(''.join(rnd.choice('abc') for _ in range(rnd.randint(1, 8))) if rnd.random() < .5 else ''.join(rnd.choice(string.ascii_lowercase) for _ in range(rnd.randint(1, 8))))
big = [[w, rnd.randint(1, 100)] for w in sorted(words)]
def subtree_size(trie, prefix):
    nd = trie.root
    for ch in prefix:
        nd = nd['c'].get(ch)
        if nd is None: return 0
    seen = 0; stack = [nd]
    while stack:
        x = stack.pop(); seen += x['cnt'] is not None; stack += x['c'].values()
    return seen
bt = AutoTrie()
for w, c in big: bt.insert(w, c)
print('2000 words; words below prefix (what the collect-and-sort baseline must examine) versus stored entries read by a query:')
for p in ['a', 'ab', 'abc', 'q', 'zz']:
    print(f'  {p!r:6}: words below = {subtree_size(bt, p):4d}   query reads at most {K} stored entries after {len(p)} steps')
print('trie nodes for the 2000 words:', bt.nodes)

# seeded random cross-check vs startswith + sort
for _ in range(300):
    n = random.randint(1, 25)
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(n)})
    ent = [[w, random.randint(1, 6)] for w in ws]; random.shuffle(ent)
    qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(8)]
    assert solve(ent, qs) == brute(ent, qs), (ent, qs)
print('300 seeded random cases agree with the filter-and-sort baseline (ties by word ascending)')

# later count changes: up and down, rebuilt along the path
bad = 0
for _ in range(200):
    ws = sorted({''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(20)})
    cur = {w: random.randint(1, 6) for w in ws}
    tr = AutoTrie()
    for w, c in cur.items(): tr.insert(w, c)
    for _ in range(15):
        w = random.choice(ws); cur[w] = random.randint(1, 6); tr.set_count(w, cur[w])
        qs = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(5)]
        assert [tr.query(p) for p in qs] == brute(list(cur.items()), qs)
print('200 x 15 random count changes (up and down) keep every answer equal to the baseline')
# showing why only "merge" is not enough when a count goes down
tr = AutoTrie()
for w, c in [['ab', 9], ['ac', 5], ['ad', 4], ['ae', 3]]: tr.insert(w, c)
before = tr.query('a'); tr.set_count('ab', 1); after = tr.query('a')
print("top-3 of 'a' before:", before, " after lowering 'ab' to 1:", after, "(ae was not stored; it had to come back from the children)")
assert before == ['ab', 'ac', 'ad'] and after == ['ac', 'ad', 'ae']

# edge asserts
assert solve([['a', 1]], ['a', 'ab', 'b']) == [['a'], [], []]
assert solve([['z' * 20, 5]], ['z' * 20, 'z' * 19]) == [['z' * 20], ['z' * 20]]
assert solve([['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]], ['a']) == [['ab', 'ac', 'ad']]
print('edge asserts passed')
```

**Output (my run):**
```
example [['car', 5], ['cart', 9], ['care', 9], ['cat', 2], ['dog', 7]] ['ca', 'car', 'd', 'x', 'cat'] -> [['care', 'cart', 'car'], ['care', 'cart', 'car'], ['dog'], [], ['cat']]
example [['a', 1]] ['a', 'ab'] -> [['a'], []]
example [['ab', 3], ['ac', 3], ['ad', 3], ['ae', 3]] ['a'] -> [['ab', 'ac', 'ad']]
stored top-3 per node, example 1:
  'c'    : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'ca'   : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'car'  : [(9, 'care'), (9, 'cart'), (5, 'car')]
  'cat'  : [(2, 'cat')]
  'care' : [(9, 'care')]
  'cart' : [(9, 'cart')]
  'd'    : [(7, 'dog')]
2000 words; words below prefix (what the collect-and-sort baseline must examine) versus stored entries read by a query:
  'a'   : words below =  295   query reads at most 3 stored entries after 1 steps
  'ab'  : words below =   85   query reads at most 3 stored entries after 2 steps
  'abc' : words below =   23   query reads at most 3 stored entries after 3 steps
  'q'   : words below =   47   query reads at most 3 stored entries after 1 steps
  'zz'  : words below =    0   query reads at most 3 stored entries after 2 steps
trie nodes for the 2000 words: 5435
300 seeded random cases agree with the filter-and-sort baseline (ties by word ascending)
200 x 15 random count changes (up and down) keep every answer equal to the baseline
top-3 of 'a' before: ['ab', 'ac', 'ad']  after lowering 'ab' to 1: ['ac', 'ad', 'ae'] (ae was not stored; it had to come back from the children)
edge asserts passed
```

Reading the output:
- All three examples agree with the filter-and-sort oracle; the stored lists printed match the dry run.
- On 2000 random words, the baseline would examine 295 words under `'a'`, 85 under `'ab'`, and 47 under `'q'`; the trie query reads at most 3 stored entries after walking the prefix. (These counts are about work, not timings.)
- 300 seeded random cases (ties included, since counts are drawn from 1..6) agree with the baseline.
- 200 sequences of 15 random count changes, up and down, keep every query equal to the baseline, so the rebuild along the path is right.
- The lowering demo shows why a pure "merge" on the path is not enough.

**Edge cases:**
- Prefix not present: `[]`.
- Prefix equal to a whole word: that word competes with its extensions (`'car'` returns `care, cart, car`).
- Fewer than 3 matches: fewer than 3 returned.
- All counts equal: word order decides (`ab, ac, ad` out of four).
- Length-20 words: depth 20, no recursion used.

**Follow-ups:**
- "Large dictionary memory?" Store word ids (or indexes into a list) instead of strings in the per-node lists, or keep `K` small; a compressed (radix) trie reduces the node count.
- "Counts change often?" Updates cost more than reads here; if writes dominate, compute at query time with a heap over the subtree instead, or batch the rebuilds.
- "Why not a sorted list and `bisect`?" It gives the range of words with the prefix in O(log W) but not the top 3 by count in that range without scanning it (Part 3 Q36 compares those two for prefix queries).

**Common mistakes:**
- Sorting by `(count, word)` ascending: the order is wrong (reversed). Store `-count`.
- Storing only the best 3 at the leaf and forgetting the inner nodes.
- Updating only the leaf when a count changes, leaving stale copies on the path.
- Mutating the stored list when answering (return a copy of the words).
- Keeping every word at every node: that is one entry per word per prefix (about `W * L` entries) instead of at most 3 per node.

### Q25 ⭐⭐ 🔴 Sudoku solver. `board` is a list of 9 strings of 9 characters each: '1'..'9' for a given digit and '.' for an empty cell. The puzzle has exactly one solution. Return the solved board in the same format (list of 9 strings of digits). Fill empty cells by backtracking, keeping a bitmask per row, per column and per 3 x 3 box (`rows[r]`, `cols[c]`, `boxes[(r // 3) * 3 + c // 3]`), compute the candidates of a cell as the digits not set in the OR of its three masks, extract a candidate with `low = m & -m` and its digit with `low.bit_length() - 1`, and choose the empty cell with the fewest candidates first. Explain why the search is exponential in theory but fast on real puzzles, and what each of the three masks prunes. (Part 1 Q15 only validates a partly filled board; this question solves it.) The recursion depth equals the number of empty cells, at most 81. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain cell-by-cell solver without the heuristic, plus a validity check of the result on small inputs. Example: board=['.1....3..', '.586.3.24', '..92..5..', '.4.1...5.', '..6.24.17', '.8...94.2', '8.5...74.', '471...2..', '.....7..5'] -> ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with constraint propagation by bitmasks and a most-constrained-cell-first rule (fail-first). Three integers per row, column and box replace three scans.

**Say this first (1 line):** "One 9-bit mask per row, column and box records the digits used; a cell's candidates are the digits not set in the OR of its three masks; I always fill the empty cell with the fewest candidates, so dead ends show up early."

**Brute force:** Cell by cell in reading order, try `'1'..'9'`, check the row, column and box by scanning (about 27 comparisons per try), recurse, undo on failure. Correct, and exponential in theory. It can run for millions of nodes on a puzzle with few givens. Used as the oracle (it also counts solutions, to check that test puzzles are unique).

**Optimal:**
- Masks: digit `d` is bit `d` (bits 1..9, so `FULL = 0x3FE`). `rows[r]`, `cols[c]`, `boxes[(r // 3) * 3 + c // 3]` hold the digits already placed.
- Candidates of a cell: `~(rows[r] | cols[c] | boxes[b]) & FULL`. Python integers are unbounded and `~x` is `-x - 1`, a NEGATIVE number with infinitely many leading 1 bits (observed: `~m = -39` for `m = 0b100110`). So the `& FULL` mask is not optional: without it you would get candidates for bit 0 and for bits 10 and above, and `while m:` would never terminate on a negative number.
- Extract a candidate: `low = m & -m` isolates the lowest set bit (for positive `m`, `-m` is two's complement in Python's infinite-width view, so `m & -m` is exactly the lowest 1). The digit is `low.bit_length() - 1`. Clear it with `m ^= low`. Place and undo by `|= low` and `^= low`.
- Choose the empty cell with the fewest candidates (`m.bit_count()`; `bin(m).count('1')` on older Python; `int.bit_count` was added in 3.10, editor knowledge). Stop scanning at a cell with 0 or 1 candidates. Zero candidates means this branch is dead: return at once.
- What each mask prunes: the row mask removes digits already in that row, the column mask the same for the column, the box mask for the 3 x 3 box. A candidate must pass all three, so the OR is the set of forbidden digits.
- Why exponential in theory but fast in practice: Sudoku solving is NP-complete when generalised to `n^2 x n^2` boards, and a 9 x 9 board with few givens can still need many guesses. On real puzzles propagation (forced single candidates) plus fail-first leaves very few real choices: the example below needs 54 calls for 48 empty cells.

**Complexity:** Worst case exponential: up to 9 branches per empty cell, so O(9^k) for `k` empty cells (a loose bound; real puzzles are far smaller). Each call costs O(k) to scan for the best cell (k <= 81) and O(1) for the mask work per candidate. Space O(k) for the recursion (depth = empty cells, at most 81, far below the limit of 1000) and the masks.

**Dry run:** the first example has 48 empty cells. The code prints the first choices:
- Cell `(1, 0)` has exactly one candidate, 7: forced; place it.
- Then `(0, 0)` has candidates 2 and 6 (two options): try 2 first.
- Then `(0, 2)` has one candidate, 4; `(0, 5)` has 5 and 8; `(1, 4)` has 1 and 9; `(1, 6)` has only 9.
- Whenever some cell has no candidate the search backs out immediately (the `bk == 0` return).
- It finishes after 54 calls for 48 empty cells: a call is made per placement plus one at the end, so at most a few calls went into undone guesses. Reading order with the same masks needs 522 calls on the same board.

**Code:**
```python
import random

random.seed(25)
FULL = 0x3FE            # bits 1..9 set: digit d is bit d. Python's ~ gives a NEGATIVE number, so we always mask with FULL.

def digits_of(m):
    return [i for i in range(1, 10) if m >> i & 1]

def solve_mrv(board, trace=None):
    """Bitmask backtracking, most-constrained empty cell first. Returns (solution rows, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def solve():
        nonlocal nodes
        nodes += 1
        if not empties: return True
        best = -1; bm = 0; bk = 10
        for idx, (r, c) in enumerate(empties):
            m = ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & FULL        # candidates of this cell
            k = m.bit_count()
            if k < bk:
                best, bm, bk = idx, m, k
                if k <= 1: break                                                 # a forced cell (or a dead end) cannot be beaten
        if bk == 0: return False                                                 # some cell has no candidate: prune
        empties[best], empties[-1] = empties[-1], empties[best]
        r, c = empties.pop(); bi = r // 3 * 3 + c // 3
        if trace is not None and len(trace) < 6: trace.append(((r, c), digits_of(bm)))
        while bm:
            low = bm & -bm; bm ^= low; v = low.bit_length() - 1                   # lowest candidate bit, then its digit
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if solve(): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low; g[r][c] = 0
        empties.append((r, c)); empties[best], empties[-1] = empties[-1], empties[best]
        return False
    assert solve(), 'no solution'
    return [''.join(map(str, row)) for row in g], nodes

def solve_fixed_order(board, cap=None):
    """Same masks, same candidate extraction, but cells in reading order (no heuristic). Returns (rows or None, nodes)."""
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; boxes[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    nodes = 0
    def go(i):
        nonlocal nodes
        nodes += 1
        if cap and nodes > cap: raise OverflowError
        if i == len(empties): return True
        r, c = empties[i]; bi = r // 3 * 3 + c // 3
        m = ~(rows[r] | cols[c] | boxes[bi]) & FULL
        while m:
            low = m & -m; m ^= low; v = low.bit_length() - 1
            g[r][c] = v; rows[r] |= low; cols[c] |= low; boxes[bi] |= low
            if go(i + 1): return True
            rows[r] ^= low; cols[c] ^= low; boxes[bi] ^= low
        return False
    try: ok = go(0)
    except OverflowError: return None, nodes
    return ([''.join(map(str, row)) for row in g] if ok else None), nodes

def plain(board, limit=1):
    """Oracle: cell by cell, tries '1'..'9', checks row, column and box by scanning; counts solutions up to `limit`."""
    g = [list(r) for r in board]; found = []
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if len(found) >= limit: return
        while pos < 81 and g[pos // 9][pos % 9] != '.': pos += 1
        if pos == 81: found.append([''.join(r) for r in g]); return
        r, c = divmod(pos, 9)
        for ch in '123456789':
            if ok(r, c, ch): g[r][c] = ch; go(pos + 1); g[r][c] = '.'
    go(0); return found

def valid(rows):
    if len(rows) != 9 or any(len(r) != 9 for r in rows): return False
    want = set('123456789')
    for i in range(9):
        if set(rows[i]) != want or set(rows[j][i] for j in range(9)) != want: return False
        if {rows[3 * (i // 3) + a][3 * (i % 3) + b] for a in range(3) for b in range(3)} != want: return False
    return True

EX = ['.1....3..', '.586.3.24', '..92..5..', '.4.1...5.', '..6.24.17', '.8...94.2', '8.5...74.', '471...2..', '.....7..5']
EXP = ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685']
trace = []
sol, n_mrv = solve_mrv(EX, trace)
assert sol == EXP == plain(EX, 2)[0] and len(plain(EX, 2)) == 1 and valid(sol)
print('example solved:', sol)
print('empty cells:', sum(r.count('.') for r in EX), '| search calls with most-constrained cell first:', n_mrv)
for (rc, cands) in trace: print(f'  step: choose cell {rc} with candidates {cands}')

# the Python negative-integer point, as observed on Python 3.13
m = 0b0000100110
print('~m =', ~m, '(negative); ~m & FULL =', bin(~m & FULL), '-> digits', digits_of(~m & FULL))
x = 0b101000
print('x & -x =', bin(x & -x), '(lowest set bit);  (x & -x).bit_length() - 1 =', (x & -x).bit_length() - 1)
print('digit d as a bit: 1 << 7 =', bin(1 << 7), '; row mask with 5 and 9 set =', bin((1 << 5) | (1 << 9)))

# search cost of the heuristic: same masks, reading-order cells
sol2, n_fixed = solve_fixed_order(EX)
assert sol2 == EXP
print('same example, reading-order cells with the same masks:', n_fixed, 'calls (against', n_mrv, 'with the heuristic)')

# a puzzle with 17 givens and an empty first row: hard for reading order
HARD = ['.........', '.....3.85', '..1.2....', '...5.7...', '..4...1..', '.9.......', '5......73', '..2.1....', '....4...9']
h_sol, n_h = solve_mrv(HARD)
assert valid(h_sol) and all(a == '.' or a == b for ra, rb in zip(HARD, h_sol) for a, b in zip(ra, rb))
r_fixed, n_f = solve_fixed_order(HARD, cap=3_000_000)
print('hard puzzle (17 givens):', 'heuristic', n_h, 'calls;', ('reading order ' + str(n_f) + ' calls') if r_fixed else 'reading order gave up after ' + str(n_f) + ' calls (cap 3,000,000)')
assert r_fixed is None or r_fixed == h_sol

# seeded random puzzles with a unique solution; compare with the plain oracle and check validity
def random_full(rnd):
    g = [['.'] * 9 for _ in range(9)]
    def ok(r, c, ch):
        if any(g[r][k] == ch or g[k][c] == ch for k in range(9)): return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        if pos == 81: return True
        r, c = divmod(pos, 9); ds = list('123456789'); rnd.shuffle(ds)
        for ch in ds:
            if ok(r, c, ch):
                g[r][c] = ch
                if go(pos + 1): return True
                g[r][c] = '.'
        return False
    go(0); return [''.join(r) for r in g]
def make_puzzle(rnd, remove):
    full = random_full(rnd); g = [list(r) for r in full]
    cells = [(r, c) for r in range(9) for c in range(9)]; rnd.shuffle(cells); removed = 0
    for r, c in cells:
        if removed >= remove: break
        keep = g[r][c]; g[r][c] = '.'
        if len(plain([''.join(x) for x in g], 2)) == 1: removed += 1
        else: g[r][c] = keep
    return [''.join(x) for x in g], full
rnd = random.Random(250)
nm = []; nf = []
for i in range(40):
    puz, full = make_puzzle(rnd, rnd.randint(30, 50))
    s1, a = solve_mrv(puz); assert s1 == full == plain(puz, 1)[0] and valid(s1)
    assert all(p == '.' or p == q for rp, rq in zip(puz, s1) for p, q in zip(rp, rq))
    s2, b = solve_fixed_order(puz); assert s2 == full
    nm.append(a); nf.append(b)
print('40 seeded random puzzles with a unique solution: all agree with the plain solver and are valid grids')
print('  calls with heuristic: total', sum(nm), 'max', max(nm), '| reading order: total', sum(nf), 'max', max(nf))

# edge asserts: an already solved board, one empty cell
assert solve_mrv(EXP)[0] == EXP
one = [EXP[0][:4] + '.' + EXP[0][5:]] + EXP[1:]
assert solve_mrv(one)[0] == EXP
print('edge asserts passed (solved board; one empty cell); recursion depth = empty cells <= 81')
```

**Output (my run):**
```
example solved: ['214785369', '758693124', '639241578', '342178956', '596324817', '187569432', '865932741', '471856293', '923417685']
empty cells: 48 | search calls with most-constrained cell first: 54
  step: choose cell (1, 0) with candidates [7]
  step: choose cell (0, 0) with candidates [2, 6]
  step: choose cell (0, 2) with candidates [4]
  step: choose cell (0, 5) with candidates [5, 8]
  step: choose cell (1, 4) with candidates [1, 9]
  step: choose cell (1, 6) with candidates [9]
~m = -39 (negative); ~m & FULL = 0b1111011000 -> digits [3, 4, 6, 7, 8, 9]
x & -x = 0b1000 (lowest set bit);  (x & -x).bit_length() - 1 = 3
digit d as a bit: 1 << 7 = 0b10000000 ; row mask with 5 and 9 set = 0b1000100000
same example, reading-order cells with the same masks: 522 calls (against 54 with the heuristic)
hard puzzle (17 givens): heuristic 17918 calls; reading order gave up after 3000001 calls (cap 3,000,000)
40 seeded random puzzles with a unique solution: all agree with the plain solver and are valid grids
  calls with heuristic: total 1629 max 67 | reading order: total 18763 max 9383
edge asserts passed (solved board; one empty cell); recursion depth = empty cells <= 81
```

Reading the output:
- The solved board equals the expected one, and the plain solver finds exactly one solution for it.
- The mask demo shows `~m` negative and the `& FULL` result giving digits 3, 4, 6, 7, 8, 9 for a row that has 1, 2 and 5 placed. `x & -x` isolates bit 3 and `bit_length() - 1` turns it into 3. Observed on Python 3.13.
- Node counts: 54 calls with the heuristic against 522 with the same masks in reading order. On a 17-given puzzle with an empty first row the heuristic needs 17,918 calls while reading order did not finish within a cap of 3,000,000 calls (a limit of the demo, not a proof it could not finish).
- 40 seeded random puzzles (each with a unique solution, checked by the plain solver) give valid grids that keep all the givens and match the oracle. Total calls: 1629 with the heuristic (max 67) against 18,763 in reading order (max 9,383).

**Edge cases:**
- Already solved board: no empties, returns at once.
- One empty cell: forced.
- A puzzle with no solution: the search ends with `False` (the prompt guarantees exactly one solution, so the code asserts).
- Several solutions: returns the first found (the prompt rules this out).
- Contradictory givens: some mask makes a cell's candidates empty and the search fails at the root.

**Follow-ups:**
- "Validity only?" Part 1 Q15 validates a partly filled board with the same row, column and box idea.
- "Count solutions or prove uniqueness?" Do not return at the first solution; stop at two.
- "Faster?" Add naked and hidden singles propagation, or exact cover with dancing links. The idea here is already the dominant gain.

**Common mistakes:**
- Using `~mask` without `& FULL`: negative numbers and bit 0 give phantom candidates and the loop does not end.
- Box index `r // 3 + c // 3` instead of `(r // 3) * 3 + c // 3`.
- Forgetting to undo all three masks and the grid cell on backtrack.
- Mixing digit `d` and bit `d - 1` conventions between placing and reading.
- Picking the first empty cell (no fail-first rule): same answer, far more calls.

### Q26 ⭐⭐ 🔴 Maximum XOR of two numbers (binary trie). `nums` has 2 <= len <= 3*10^4 integers in 0..2^31 - 1. Return the maximum of `nums[i] ^ nums[j]` over pairs i < j. Build a binary trie of the 31-bit patterns (bit 30 first), and for each number walk the trie choosing, at each bit, the child with the OPPOSITE bit when it exists (greedy: a higher bit outweighs all lower bits together). Insert each number after querying so that i < j holds. State the cost O(31 * n) against O(n^2) for all pairs, and the memory of the trie (up to 31 * n nodes). A hash-set-of-prefixes approach is the follow-up. Note that Python integers are not capped at 31 bits, so the bit width is a constraint of this question, not of the language. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an O(n^2) loop over all pairs on small inputs. Example: nums=[12, 5, 9, 21, 7] -> 28; nums=[0, 0] -> 0; nums=[7, 7, 7] -> 0; nums=[2147483647, 0] -> 2147483647; nums=[8, 1] -> 9.
**Asked at:** A Teamblind discussion of a bit-based trie question, plus the techinterview.org trie posts (search snippets only, not opened)

**Pattern:** Binary trie over fixed-width bit patterns, with a greedy walk that prefers the opposite bit at each level.

**Say this first (1 line):** "A higher bit outweighs all the lower bits together, so for each number I walk the trie from bit 30 down and take the child with the opposite bit whenever it exists. That is the best partner among the stored numbers, found in 31 steps."

**Brute force:** XOR every pair `i < j` and take the maximum: O(n^2). At `n = 30000` that is 449,985,000 pairs, far too slow in Python. It is the oracle for small `n`.

**Optimal:**
- The trie has one level per bit, bit 30 first (31 levels, matching values in `0..2^31 - 1`). A number is a path of 31 edges, each labelled 0 or 1. The code stores the two children in parallel lists `c0`, `c1` (index 0 means missing; node 0 is the root).
- Query for `x`: at bit `b`, if the child for `1 - bit_b(x)` exists, go there and set bit `b` of the result; otherwise follow the child for `bit_b(x)`, which must exist (every stored number is a full-length path), and the result bit stays 0.
- Why greedy is right: the XOR bit at position `b` is worth `2^b`, and `2^b` is greater than the sum of all lower bits `2^b - 1`. So whenever a partner can give a 1 at bit `b`, every partner that gives 0 there is worse, whatever happens below.
- Order: for each number, query first, then insert, so only numbers earlier in the list are partners (`i < j`). (Inserting first would also give the correct answer: the extra self-pair gives 0, which never beats a real pair; the code checks this.)
- The bit width: Python integers are not capped at 31 bits. The width 31 is a rule of this question. A negative input would read sign bits forever (`(-1 >> 30) & 1 == 1`, and the same for every higher bit in Python 3.13), so the walk would be meaningless; the constraints rule negatives out. If they were allowed you would have to mask to a width first (`x & 0xFFFFFFFF`).
- Follow-up approach, a hash set of prefixes: build the answer bit by bit from the top; at bit `b` the candidate answer is `ans | 1 << b`; collect the set of all `x >> b`; the candidate is possible if some `p` in the set has `p ^ candidate_prefix` also in the set. 31 passes of O(n), no trie memory. The code implements it and checks it.

**Complexity:** Time O(31 * n) = O(n * B) for `B = 31` bits: one insert and one query per number, 31 steps each. Against O(n^2) for all pairs. Space: up to `31 * n + 1` nodes (930,001 at `n = 30000`; the random test built 516,727 nodes because the top bits are shared). Each node is two list slots in this encoding. The prefix-set approach uses O(n) space.

**Dry run:** `nums = [12, 5, 9, 21, 7]`, 5-bit view so the paths fit on a line (the real code uses 31 bits; the leading zeros do not change the answer).
- Insert 12 (`01100`).
- Query 5 (`00101`) against `{12}`: the only partner is 12, xor 9. Query 9 (`01001`) against `{12, 5}`: at bit 3 take the child with a 0 (that is 5), and at bit 2 take the child with a 1 (5 again), so the xor is `01100` = 12, partner 5.
- Query 21 (`10101`) against `{12, 5, 9}`: bit 4: x has 1, opposite child 0 exists (all three stored numbers have 0 at bit 4), take it; bit 3: x has 0, take 1 (12 and 9 have it); bit 2: x has 1, take 0 (only 9 remains with 0 here); bit 1 and bit 0: no choice. Partner 9, xor `11100` = 28.
- Query 7 (`00111`) against `{12, 5, 9, 21}`: best is 21, xor 18.
- Results 9, 12, 28, 18. Maximum 28.

**Code:**
```python
import random, itertools, time

random.seed(26)
BITS = 31                                   # the question's width: values are in 0..2^31 - 1, bit 30 is the top bit

def max_xor(nums, bits=BITS, stats=None):
    """Binary trie in two parallel lists (child 0, child 1). Query each number, THEN insert it, so only i < j pairs are seen."""
    c0 = [0]; c1 = [0]                      # node 0 is the root; child index 0 means 'missing'
    children = (c0, c1)
    best = 0
    def insert(x):
        nd = 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            nxt = children[bit][nd]
            if not nxt:
                c0.append(0); c1.append(0); nxt = len(c0) - 1; children[bit][nd] = nxt
            nd = nxt
    def query(x):
        nd = 0; got = 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            want = children[bit ^ 1][nd]    # the child with the OPPOSITE bit
            if want: got |= 1 << b; nd = want
            else: nd = children[bit][nd]    # forced to follow the same bit (it must exist: the trie is a union of full paths)
        return got
    insert(nums[0])
    for x in nums[1:]:
        best = max(best, query(x)); insert(x)
    if stats is not None: stats['nodes'] = len(c0)
    return best

def prefix_set(nums, bits=BITS):
    """Follow-up: hash set of prefixes. Grow the answer bit by bit; keep a bit if two prefixes XOR to the candidate."""
    ans = 0
    for b in range(bits - 1, -1, -1):
        pref = {x >> b for x in nums}
        cand = (ans >> b) | 1
        if any(p ^ cand in pref for p in pref): ans |= 1 << b
    return ans

def brute(nums): return max(a ^ b for a, b in itertools.combinations(nums, 2))

for nums, exp in [([12, 5, 9, 21, 7], 28), ([0, 0], 0), ([7, 7, 7], 0), ([2147483647, 0], 2147483647), ([8, 1], 9)]:
    a, b, c = max_xor(nums), brute(nums), prefix_set(nums)
    assert a == b == c == exp, nums
    print('example', nums, '->', a)

# the greedy walk for 21 against {12, 5, 9} using 5 bits so the path fits on a line
def show_walk(x, stored, bits=5):
    print(f'query {x} = {x:0{bits}b}, stored {stored} = {[format(y, "0%db" % bits) for y in stored]}')
    path = 0; got = 0
    for b in range(bits - 1, -1, -1):
        bit = x >> b & 1
        have = {y >> b for y in stored if (y >> (b + 1)) == path}        # next-bit prefixes present below the current node
        want = path << 1 | (bit ^ 1)
        if want in have: got |= 1 << b; path = want; print(f'  bit {b}: x has {bit}, opposite child exists -> take {bit ^ 1}, xor bit = 1')
        else: path = path << 1 | bit; print(f'  bit {b}: x has {bit}, opposite child missing -> take {bit}, xor bit = 0')
    print('  xor =', got, f'= {got:0{bits}b}, partner = {path}')
    return got
show_walk(5, [12], 5); show_walk(9, [12, 5], 5)
g = show_walk(21, [12, 5, 9], 5); assert g == 28
g2 = show_walk(7, [12, 5, 9, 21], 5); assert max(9, 12, 28, 18) == 28; print('results of the four queries: 9, 12, 28, 18 -> maximum 28')

# trie size: nodes <= 31 * n + 1
st = {}; nums = [random.randrange(1 << 31) for _ in range(30000)]
r = max_xor(nums, stats=st)
print('30000 random 31-bit numbers: trie nodes', st['nodes'], '<= bound 31 * 30000 + 1 =', 31 * 30000 + 1)
assert st['nodes'] <= 31 * 30000 + 1
st2 = {}; max_xor(list(range(1000)), stats=st2); print('1000 consecutive numbers 0..999: nodes', st2['nodes'], '(shared prefixes: far fewer than 31000)')
t0 = time.time(); max_xor(nums); t1 = time.time() - t0
t0 = time.time(); r2 = prefix_set(nums); t2 = time.time() - t0
assert r == r2
print(f'sandbox timing only: trie {t1:.2f} s, prefix-set {t2:.2f} s for n = 30000 (not a proof of big-O)')

# n^2 for n = 30000 would be about 4.5 * 10^8 pair XORs: not run
print('pairs at the maximum size:', 30000 * 29999 // 2)

# claim: inserting BEFORE querying would also be right here, because the self-pair x ^ x = 0 never beats a real pair
def insert_first(nums):
    return max(x ^ y for x in nums for y in nums)           # includes i == j pairs
for _ in range(300):
    nums = [random.randrange(64) for _ in range(random.randint(2, 8))]
    assert max_xor(nums) == brute(nums) == insert_first(nums)
print('300 random lists: the maximum over i <= j equals the maximum over i < j (the self-pair only adds 0)')

# negative numbers are outside the constraints; show what Python does so nobody 'fixes' it with a 31-bit loop
print('Python 3.13: (-1 >> 30) & 1 =', (-1 >> 30) & 1, ' (-1 >> 31) & 1 =', (-1 >> 31) & 1, ' -> a negative input reads sign bits forever; the 31-bit width is the question\'s rule, not the language')
print('Python ints are not capped: (2**31 - 1) ^ 0 =', (2**31 - 1) ^ 0, ', 2**40 ^ 1 =', 2**40 ^ 1)

# seeded random cross-check
for _ in range(400):
    n = random.randint(2, 12); hi = random.choice([2, 8, 100, 2 ** 31])
    nums = [random.randrange(hi) for _ in range(n)]
    assert max_xor(nums) == brute(nums) == prefix_set(nums), nums
print('400 seeded random cases agree (trie, prefix-set, O(n^2))')

# edge asserts
assert max_xor([7, 7]) == 0 and max_xor([0, 2147483647]) == 2147483647 and max_xor([5, 5, 5, 5]) == 0
assert max_xor([1, 2]) == 3 and max_xor([2 ** 30, 2 ** 30 - 1]) == 2 ** 31 - 1
print('edge asserts passed')
```

**Output (my run):**
```
example [12, 5, 9, 21, 7] -> 28
example [0, 0] -> 0
example [7, 7, 7] -> 0
example [2147483647, 0] -> 2147483647
example [8, 1] -> 9
query 5 = 00101, stored [12] = ['01100']
  bit 4: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 3: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 2: x has 1, opposite child missing -> take 1, xor bit = 0
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child exists -> take 0, xor bit = 1
  xor = 9 = 01001, partner = 12
query 9 = 01001, stored [12, 5] = ['01100', '00101']
  bit 4: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 3: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 2: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 12 = 01100, partner = 5
query 21 = 10101, stored [12, 5, 9] = ['01100', '00101', '01001']
  bit 4: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 3: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 2: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 1: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 28 = 11100, partner = 9
query 7 = 00111, stored [12, 5, 9, 21] = ['01100', '00101', '01001', '10101']
  bit 4: x has 0, opposite child exists -> take 1, xor bit = 1
  bit 3: x has 0, opposite child missing -> take 0, xor bit = 0
  bit 2: x has 1, opposite child missing -> take 1, xor bit = 0
  bit 1: x has 1, opposite child exists -> take 0, xor bit = 1
  bit 0: x has 1, opposite child missing -> take 1, xor bit = 0
  xor = 18 = 10010, partner = 21
results of the four queries: 9, 12, 28, 18 -> maximum 28
30000 random 31-bit numbers: trie nodes 516727 <= bound 31 * 30000 + 1 = 930001
1000 consecutive numbers 0..999: nodes 2022 (shared prefixes: far fewer than 31000)
sandbox timing only: trie 0.33 s, prefix-set 0.07 s for n = 30000 (not a proof of big-O)
pairs at the maximum size: 449985000
300 random lists: the maximum over i <= j equals the maximum over i < j (the self-pair only adds 0)
Python 3.13: (-1 >> 30) & 1 = 1  (-1 >> 31) & 1 = 1  -> a negative input reads sign bits forever; the 31-bit width is the question's rule, not the language
Python ints are not capped: (2**31 - 1) ^ 0 = 2147483647 , 2**40 ^ 1 = 1099511627777
400 seeded random cases agree (trie, prefix-set, O(n^2))
edge asserts passed
```

Reading the output:
- All five examples agree across the trie, the prefix-set method and the O(n^2) loop. Note `[7, 7, 7]` gives 0: every pair is equal.
- The printed walks follow the dry run bit by bit; the last walk (`21`) shows three consecutive opposite-bit takes giving `11100`.
- Node counts: 516,727 nodes for 30,000 random 31-bit numbers, under the bound of 930,001. For the numbers 0..999 only 2,022 nodes: shared prefixes cost nothing.
- Timings (sandbox only): the trie takes a fraction of a second for `n = 30000`, the prefix-set method is faster in Python because it uses sets and no per-bit node walking. Not a proof of big-O.
- 400 seeded random lists (value ranges 2, 8, 100 and 2^31) agree, and 300 more confirm that the `i <= j` maximum equals the `i < j` maximum.

**Edge cases:**
- Two numbers: one query.
- All equal (`[7,7,7]`, `[0,0]`): answer 0.
- Largest value with 0: `2^31 - 1`.
- Two numbers differing at the top bit only (`2^30` and `2^30 - 1`): all 31 bits set.
- Duplicates inside a larger list: they share the whole path, no extra nodes.

**Follow-ups:**
- "Memory?" Use the prefix-set method, or compress the trie. Or a sorted array with two pointers on the top bit and recursion on groups.
- "Maximum XOR of a number with a subarray XOR?" Combine with prefix XORs (Part 1 Q36 uses prefix XORs for counting).
- "Queries with a limit (XOR with `x` while the partner is at most `m`)?" Offline: sort queries by `m`, insert numbers up to `m`, then query.

**Common mistakes:**
- Starting at bit 31 or at 32: extra levels of zeros, harmless but wasteful; starting at 29 loses the top bit.
- Following the SAME bit by default, which finds the minimum XOR instead of the maximum.
- Taking `bit ^ 1` without checking the child exists (`None` or index 0 error).
- Using the same walk on negative numbers: infinite sign bits (see the output); mask first or rule them out.
- Rebuilding the trie per query.

### Q27 ⭐ 🟡 Map sum pairs. Implement a key-value store over lowercase string keys. `ops` is a list (1 <= len <= 5000) of `['insert', key, val]` (set `key` to the integer `val`, 0 <= val <= 1000, replacing any earlier value of that key, key length 1 to 20) or `['sum', prefix]` (the sum of the values of all keys that currently start with the non-empty `prefix`; 0 if none). Return one entry per operation: `null` (None) for insert and the sum for sum. Keep a running sum at every trie node and, on insert, add `new - old` along the whole path (this is why a replaced key does not double count); compare with scanning every key for every `sum`. State the cost per operation in terms of the key length. The trie itself is Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain dict scanned with `startswith` on small inputs. Example: ops=[['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']] -> [null, 3, null, 5, null, 7, 0]; ops=[['sum', 'a']] -> [0]; ops=[['insert', 'a', 0], ['sum', 'a'], ['insert', 'a', 7], ['sum', 'a']] -> [null, 0, null, 7].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie with an aggregate at every node (a running sum of the values below it), kept right on updates by adding the difference `new - old`. The plain trie is Q3; the new idea is the aggregate.

**Say this first (1 line):** "Each node stores the sum of all values under that prefix. Insert walks the key and adds `new - old` at every node, so replacing a key does not double count; sum walks the prefix and reads one number."

**Brute force:** Keep a dict `key -> value`; for each `sum(prefix)`, scan every key with `startswith(prefix)` and add the values. Insert is O(1), but each sum costs O(K * L) for `K` live keys of length up to `L`, so a few thousand sums over a few thousand keys is millions of comparisons. Used as the oracle.

**Optimal:**
- Keep a plain dict `vals` (key to current value) and a trie whose nodes (dicts of children) carry a `'#'` sum.
- `insert(key, val)`: `delta = val - vals.get(key, 0)`; set `vals[key] = val`; walk the key and add `delta` to the `'#'` of every node on the path (every proper prefix and the whole key). A new key has old value 0, so `delta = val`. A repeated key adds only the change.
- `sum(prefix)`: walk; a missing child gives 0; otherwise return the node's `'#'`.
- Why it is right: node `n` for prefix `p` always holds the sum of `vals[k]` over keys with prefix `p`; an insert changes exactly one key's value by `delta`, and exactly the nodes of the prefixes of that key include that key.
- Value 0 and no-op replacements are fine: a key with value 0 adds 0, and `delta = 0` changes nothing.

**Complexity:** Each insert and each sum is O(L), the key (or prefix) length, independent of the number of keys: at most 20 steps here, 5000 operations at most. A scan costs O(K * L) per sum. Space: one node per distinct prefix, at most the total letters of the distinct keys (20 * 5000 = 100,000 nodes worst case), plus the `vals` dict.

**Dry run:** example 1 (the code prints the node sums after each insert).
- `insert apple 3`: `a`, `ap`, `app`, `appl`, `apple` all become 3. `sum ap` = 3.
- `insert app 2` (new key, delta 2): `a`, `ap`, `app` become 5; `appl` and `apple` stay 3. `sum ap` = 5.
- `insert apple 5` (old value 3, delta +2, not +5): `a`, `ap`, `app` become 7; `appl`, `apple` become 5. `sum app` = 7. `sum b`: no child `b`, so 0.
- Outputs: `[null, 3, null, 5, null, 7, 0]`. The demo of the bug (adding `val` instead of the delta) gives 10 for `sum app`, which counts `apple` as 3 + 5.

**Code:**
```python
import random

random.seed(27)

class MapSum:
    """Trie where every node keeps the sum of the values of all keys at or below it."""
    def __init__(self):
        self.root = {}            # node: dict of child letter -> node, plus the key '#' holding the running sum
        self.vals = {}            # key -> current value (needed to compute new - old)
        self.steps = 0            # trie steps taken, to compare with a scan
    def insert(self, key, val):
        delta = val - self.vals.get(key, 0)           # replacing a key adds only the DIFFERENCE
        self.vals[key] = val
        nd = self.root
        for ch in key:
            nd = nd.setdefault(ch, {}); self.steps += 1
            nd['#'] = nd.get('#', 0) + delta
    def sum(self, prefix):
        nd = self.root
        for ch in prefix:
            nd = nd.get(ch); self.steps += 1
            if nd is None: return 0
        return nd['#']

def solve(ops):
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert': m.insert(op[1], op[2]); res.append(None)
        else: res.append(m.sum(op[1]))
    return res

def brute(ops):
    d = {}; res = []
    for op in ops:
        if op[0] == 'insert': d[op[1]] = op[2]; res.append(None)
        else: res.append(sum(v for k, v in d.items() if k.startswith(op[1])))
    return res

def wrong_add_not_delta(ops):
    """The tempting bug: add val instead of new - old, so a replaced key counts twice."""
    m = MapSum(); res = []
    for op in ops:
        if op[0] == 'insert':
            nd = m.root
            for ch in op[1]:
                nd = nd.setdefault(ch, {}); nd['#'] = nd.get('#', 0) + op[2]
            res.append(None)
        else: res.append(m.sum(op[1]))
    return res

N = None
for ops, exp in [([['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']], [N, 3, N, 5, N, 7, 0]),
                 ([['sum', 'a']], [0]),
                 ([['insert', 'a', 0], ['sum', 'a'], ['insert', 'a', 7], ['sum', 'a']], [N, 0, N, 7])]:
    got = solve(ops)
    assert got == exp == brute(ops)
    print('example ->', got)

# trace of example 1: node sums after each insert
m = MapSum()
def snap(label):
    parts = []
    for pre in ['a', 'ap', 'app', 'appl', 'apple']:
        nd = m.root
        for ch in pre: nd = nd[ch]
        parts.append(f'{pre}={nd["#"]}')
    print(f'  after {label}: ' + ', '.join(parts))
m.insert('apple', 3); snap("insert apple 3")
m.insert('app', 2); snap("insert app 2")
m.insert('apple', 5); snap("insert apple 5 (delta +2, not +5)")
print('  sum(ap) =', m.sum('ap'), ' sum(app) =', m.sum('app'), ' sum(b) =', m.sum('b'))
ops1 = [['insert', 'apple', 3], ['sum', 'ap'], ['insert', 'app', 2], ['sum', 'ap'], ['insert', 'apple', 5], ['sum', 'app'], ['sum', 'b']]
print('the add-val-not-delta bug on example 1 gives', wrong_add_not_delta(ops1), '(expected 3, 5, 7, 0 at the sum positions)')
assert wrong_add_not_delta(ops1) != solve(ops1)

# cost: trie steps vs keys scanned by the baseline
rnd = random.Random(270)
keys = [''.join(rnd.choice('abcd') for _ in range(rnd.randint(1, 12))) for _ in range(1500)]
ops = []
for i in range(5000):
    if rnd.random() < .5: ops.append(['insert', rnd.choice(keys), rnd.randint(0, 1000)])
    else: ops.append(['sum', rnd.choice(keys)[:rnd.randint(1, 6)]])
mm = MapSum(); got = []
scanned = 0; live = {}
for op in ops:
    if op[0] == 'insert': mm.insert(op[1], op[2]); live[op[1]] = op[2]
    else: got.append(mm.sum(op[1])); scanned += len(live)
assert [x for x in solve(ops) if x is not None] == got
print('5000 mixed operations, keys of length <= 12: trie steps in total', mm.steps, '| keys a scan-per-sum would have examined', scanned)

# seeded random cross-check vs dict + startswith, including repeated replacement and value 0
for _ in range(500):
    ks = [''.join(random.choice('ab') for _ in range(random.randint(1, 4))) for _ in range(5)]
    ops = []
    for _ in range(random.randint(1, 30)):
        if random.random() < .55: ops.append(['insert', random.choice(ks), random.randint(0, 5)])
        else: ops.append(['sum', ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))])
    assert solve(ops) == brute(ops), ops
print('500 seeded random operation lists agree with the dict scanned with startswith')

# edge asserts
assert solve([['sum', 'a']]) == [0]
assert solve([['insert', 'a', 5], ['insert', 'a', 5], ['sum', 'a']]) == [None, None, 5]
assert solve([['insert', 'ab', 9], ['insert', 'ab', 0], ['sum', 'a'], ['sum', 'ab'], ['sum', 'abc']]) == [None, None, 0, 0, 0]
assert solve([['insert', 'z' * 20, 1000], ['sum', 'z'], ['sum', 'z' * 20], ['sum', 'z' * 21]]) == [None, 1000, 1000, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example -> [None, 3, None, 5, None, 7, 0]
example -> [0]
example -> [None, 0, None, 7]
  after insert apple 3: a=3, ap=3, app=3, appl=3, apple=3
  after insert app 2: a=5, ap=5, app=5, appl=3, apple=3
  after insert apple 5 (delta +2, not +5): a=7, ap=7, app=7, appl=5, apple=5
  sum(ap) = 7  sum(app) = 7  sum(b) = 0
the add-val-not-delta bug on example 1 gives [None, 3, None, 5, None, 10, 0] (expected 3, 5, 7, 0 at the sum positions)
5000 mixed operations, keys of length <= 12: trie steps in total 23558 | keys a scan-per-sum would have examined 1531573
500 seeded random operation lists agree with the dict scanned with startswith
edge asserts passed
```

Reading the output:
- All three examples match the dict-and-`startswith` oracle (insert prints `None`, the Python form of `null`).
- The printed node sums are the ones in the dry run. The bug demo returns 10 where 7 is right.
- Cost: on 5000 mixed operations over 1500 keys of length up to 12, the trie made 23,558 steps in total; a scan per `sum` would have examined 1,531,573 keys. (Step counts, not timings.)
- 500 seeded random operation lists (small alphabet so keys collide and are replaced often, values 0..5) agree with the oracle.

**Edge cases:**
- `sum` before any insert: 0.
- Insert with value 0, then `sum`: 0, and a later replacement by 7 gives 7.
- Same key inserted twice with the same value: unchanged.
- Prefix longer than any key (`'z' * 21`): 0.
- Prefix equal to a whole key: that key's value counts.
- Replacing a value with a smaller one: `delta` is negative, which is fine.

**Follow-ups:**
- "Delete a key?" `insert(key, 0)` leaves a zero-valued key; to really delete, subtract its value along the path and drop empty nodes.
- "Count of keys under a prefix?" A second counter, or the same code with `val = 1` for new keys (Part 7 Q41 counts words per prefix).
- "Memory of dict nodes?" Each dict is heavy (Q33 measures it); use arrays of 26 or a compressed trie if memory matters.

**Common mistakes:**
- Adding `val` instead of `new - old`: a replaced key counts twice.
- Not storing the old values separately (a trie holds sums, not per-key values), so `old` cannot be found.
- Returning `None` instead of 0 for a missing prefix.
- Scanning all keys for every `sum`.

### Q28 ⭐ 🟡 Single number II (every other value three times). `nums` has 1 <= len <= 10^4 integers with -2^31 <= value < 2^31: one value appears exactly once and every other value appears exactly three times. Return the single value in O(n) time and O(1) extra space: for each of the 32 bit positions count how many numbers have that bit set, take the count modulo 3 and set the bit of the answer. Because Python integers have no fixed width, you must convert the 32-bit result back to a signed value yourself: if bit 31 is set, subtract 2^32 (show a negative answer and what you would get without this step). Mention the two-register `ones`/`twos` state machine as an alternative and why it needs no sign fix in Python. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter on small inputs. Example: nums=[-5, 7, -5, 7, -5, 7, 9] -> 9; nums=[-8, 3, 3, 3] -> -8; nums=[4] -> 4; nums=[1, 1, 1, -2147483648] -> -2147483648.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit counting with modulo 3 (a 32-column counter), the bit-manipulation relative of "count and take the remainder". Every value outside the single one appears 3 times, so in each bit column the number of 1s from the repeated values is a multiple of 3. What is left over after `% 3` is the single value's bit.

**Say this first (1 line):** "For each of the 32 bit positions I count how many numbers have that bit set, take the count mod 3, and that is the bit of the answer; then I fix the sign by hand because Python has no 32-bit width."

**Brute force:** `Counter(nums)` and return the key whose count is 1. Correct, O(n) time, but O(n) space (about n/3 keys). A sort also works at O(n log n) time. Both break the O(1) space ask.

**Optimal:**
- Column rule: a value that appears 3 times adds 0 or 3 to the count of any column, so it vanishes mod 3. The single value adds 0 or 1. So `count % 3` is exactly its bit.
- For `b` in 0..31: `bit = sum((v >> b) & 1 for v in nums) % 3`; if it is 1, set `1 << b` in `ans`.
- Why `(v >> b) & 1` is safe for negatives: Python's `>>` on a negative int copies the sign bit in from the left, so bit `b` for `b <= 31` is the two's-complement bit of a 32-bit value. Values here are in [-2^31, 2^31), so 32 columns see everything.
- The sign fix (the Python-specific step): `ans` is built only from bits 0..31, so it is a non-negative number in [0, 2^32). If bit 31 is set the true answer is negative: `ans - 2**32`. Without it, `-8` comes back as `4294967288` (observed below, Python 3.13).
- State machine alternative: keep `ones` (bits seen 1 mod 3 times) and `twos` (bits seen 2 mod 3 times). For each `x`: `ones = (ones ^ x) & ~twos`, then `twos = (twos ^ x) & ~ones`. At the end `ones` is the answer. It needs no sign fix in Python because Python ints behave as if sign-extended to infinity: a negative `x` already has infinitely many leading 1s, the update rules act on every column the same way, and the final `ones` is the negative number itself. `~twos` is also fine (it is just `-twos - 1`). The column method builds the answer from 32 bits only, so it is the one that needs the fix.
- Space: O(1) in both (32 counters or two integers).

**Complexity:** Time O(32 * n) = O(n) for the column method (32 passes), O(n) for the state machine (one pass). Space O(1).

**Dry run:** `nums = [-5, 7, -5, 7, -5, 7, 9]`. In 32-bit two's complement `-5` is `...11111011`, `7` is `00000111`, `9` is `00001001`.

| bit | set bits (3 x -5, 3 x 7, 1 x 9) | count | count % 3 |
|---|---|---|---|
| 0 | 3 + 3 + 1 | 7 | 1 |
| 1 | 3 + 3 + 0 | 6 | 0 |
| 2 | 0 + 3 + 0 | 3 | 0 |
| 3 | 3 + 0 + 1 | 4 | 1 |
| 4 | 3 + 0 + 0 | 3 | 0 |
| 31 | 3 + 0 + 0 | 3 | 0 |

(Bits 5 to 30 look like bit 4.) The result has bits 0 and 3 set: `0b1001 = 9`, bit 31 is 0, so no sign change. For `[-8, 3, 3, 3]` the single value is `-8`: it is the only one with bit 31 set, so that column counts 1 (mod 3 = 1) and `ans = 4294967288`; bit 31 is set, so `ans - 2**32 = -8`.

**Code:**
```python
import random
from collections import Counter

random.seed(2801)


def single_count_bits(nums):
    """For each of 32 bit positions count the set bits, mod 3, rebuild, then fix the sign."""
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:   # v >> b works for negatives: sign bits are copied in
            ans |= 1 << b
    return ans - (1 << 32) if ans & (1 << 31) else ans   # bit 31 set -> negative in 32-bit two's complement


def no_sign_fix(nums):
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:
            ans |= 1 << b
    return ans


def single_ones_twos(nums):
    """Two registers: ones = bits seen 1 mod 3 times, twos = bits seen 2 mod 3 times."""
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones          # Python ints sign-extend forever, so a negative answer is already negative


def brute(nums):
    return next(k for k, c in Counter(nums).items() if c == 1)


# dry run table for the first example
ex = [-5, 7, -5, 7, -5, 7, 9]
print("bit : count of set bits, count mod 3")
for b in (0, 1, 2, 3, 4, 31):
    c = sum((v >> b) & 1 for v in ex)
    print(f"{b:>3} : {c}, {c % 3}")

# the four prompt examples
for nums, want in [([-5, 7, -5, 7, -5, 7, 9], 9), ([-8, 3, 3, 3], -8), ([4], 4), ([1, 1, 1, -2147483648], -2147483648)]:
    got = single_count_bits(nums)
    assert got == single_ones_twos(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", got)

# the sign fix, shown
raw = no_sign_fix([-8, 3, 3, 3])
print("without the fix:", raw, "= 2^32 - 8 =", 2**32 - 8, "| with the fix:", single_count_bits([-8, 3, 3, 3]))
print("bit 31 of the raw result:", (raw >> 31) & 1, "| 0xFFFFFFF8 as binary:", format(raw, "032b"))

# seeded random cross-check against Counter
done = 0
while done < 500:
    k = random.randint(0, 6)
    triples = random.sample(range(-20, 20), k) if random.random() < 0.7 else random.sample([-2**31, 2**31 - 1, -1, 0, 1, 2**30], min(k, 6))
    single = random.choice([v for v in range(-2**31, -2**31 + 3)] + [2**31 - 1, 0, -1, 5, -7])
    if single in triples:
        continue
    nums = [single] + [t for t in triples for _ in range(3)]
    random.shuffle(nums)
    assert single_count_bits(nums) == single_ones_twos(nums) == brute(nums) == single, nums
    done += 1
print("500 seeded random cases ok (extremes -2^31 and 2^31-1 included)")

# edge asserts
assert single_count_bits([2**31 - 1]) == 2**31 - 1
assert single_count_bits([-1, 0, 0, 0]) == -1
assert single_count_bits([-2**31, 5, 5, 5]) == -2**31
assert single_ones_twos([-2**31, 5, 5, 5]) == -2**31
print("edge asserts ok")
```

**Output (my run):**
```
bit : count of set bits, count mod 3
  0 : 7, 1
  1 : 6, 0
  2 : 3, 0
  3 : 4, 1
  4 : 3, 0
 31 : 3, 0
[-5, 7, -5, 7, -5, 7, 9] -> 9
[-8, 3, 3, 3] -> -8
[4] -> 4
[1, 1, 1, -2147483648] -> -2147483648
without the fix: 4294967288 = 2^32 - 8 = 4294967288 | with the fix: -8
bit 31 of the raw result: 1 | 0xFFFFFFF8 as binary: 11111111111111111111111111111000
500 seeded random cases ok (extremes -2^31 and 2^31-1 included)
edge asserts ok
```

**Edge cases:**
- Single element: `[4]` gives 4 (every other column is 0 mod 3 trivially).
- The smallest value `-2**31` as the single: only bit 31 is set, the fix turns `2**31` into `-2**31`. Checked above.
- The largest value `2**31 - 1`: bit 31 is 0, no fix, checked above.
- `-1` as the single (all 32 bits set) returns `-1` after the fix; `0` as the single works because every column then reads `0 mod 3`.
- Values outside the stated range (for example `2**40`) would be silently truncated to 32 columns by the column method. The `ones`/`twos` method would still work. Say that if the interviewer widens the range, loop to the wider bit length.

**Follow-ups:**
- *Every other value appears 5 times, not 3?* Same column method with `% 5`. The state machine needs three registers instead of two (the number of registers is the number of bits in the modulus counter).
- *Why can't plain XOR do this one?* XOR is addition mod 2, so it cancels pairs. Triples need addition mod 3, which is why you count per column.
- *Why does `ones` update before `twos`?* `twos` must see the new `ones`: a bit that just entered `ones` must not also enter `twos`. Swap the order and the machine miscounts.

**Common mistakes:**
- Forgetting the sign fix and returning `4294967288` for `-8`.
- Looping `range(31)` and missing bit 31 (the sign bit).
- Using `& 0xFFFFFFFF` on the input and then doing the fix on the wrong side: mask once, fix once.
- Writing `ones ^= x` and `twos ^= ones` in the wrong order; the order and the `& ~` terms are what make the machine count mod 3.
- Claiming the `Counter` solution is O(1) space.

### Q29 ⭐ 🟡 Sum of two integers without + or -. `a` and `b` are integers with |a|, |b| <= 10^9. Compute a + b using only bitwise operators and shifts, and return `[sum, rounds]`, where `rounds` is how many times this loop body runs: start with `a &= 0xFFFFFFFF; b &= 0xFFFFFFFF` and while `b` is nonzero, replace `(a, b)` by `((a ^ b) & 0xFFFFFFFF, ((a & b) << 1) & 0xFFFFFFFF)`. When the loop ends convert back to a signed value (if `a > 0x7FFFFFFF` the result is `~(a ^ 0xFFFFFFFF)`). Explain what XOR (sum without carry) and AND shifted left (the carries) mean, why the masking is needed in Python (a negative operand has infinitely many leading 1 bits, so without the mask the loop can fail to terminate, for example for a = -1 and b = 1; show that) and why the result fits in 32 bits for this input range (|a + b| <= 2 * 10^9 < 2^31). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a 32-bit ripple-carry adder built from single bits on small inputs. Example: a=7, b=5 -> [12, 3]; a=-3, b=3 -> [0, 32]; a=1000000000, b=1000000000 -> [2000000000, 2]; a=-1000000000, b=-1000000000 -> [-2000000000, 2]; a=0, b=0 -> [0, 0].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Addition as XOR plus a shifted AND (half-adder loop), with explicit 32-bit masking because Python integers have no fixed width.

**Say this first (1 line):** "XOR is the sum without carries, AND shifted left is the carries; repeat until no carry is left, and mask to 32 bits every step because a negative Python int has infinitely many leading 1s."

**Brute force:** A 32-bit ripple-carry adder: walk bits 0..31, compute `sum = x ^ y ^ carry` and `carry = (x & y) | (carry & (x ^ y))` per bit, then convert the 32-bit result back to signed. It is 32 steps always and is the oracle in the code.

**Optimal:**
- Split `a + b` into two parts: `a ^ b` (the sum of each column ignoring carries) and `(a & b) << 1` (the carries, moved one column up). Then `a + b = (a ^ b) + ((a & b) << 1)`. The new problem is the same shape but the carry part moves left every round.
- Loop `while b:` and replace `(a, b)` by `((a ^ b) & M, ((a & b) << 1) & M)` with `M = 0xFFFFFFFF`. Stop when no carry is left; `a` holds the sum.
- Why the mask (Python only): `-1` is `...1111` with infinitely many 1s. For `a = -1, b = 1` the unmasked loop gives `(a, b) = (-2, 2)`, then `(-4, 4)`, then `(-8, 8)`: the carry never dies, it only moves left forever (shown below, stopped after 40 rounds). Masking to 32 bits drops the carry that falls off the top, so it reaches 0 after at most 32 rounds here (`a = -3, b = 3` takes exactly 32).
- Convert back: after the loop `a` is in [0, 2^32). If `a > 0x7FFFFFFF` bit 31 is set and the value is negative: `~(a ^ 0xFFFFFFFF)`. That equals `a - 2**32` (XOR with all ones flips the 32 bits to get the complement, `~` negates it).
- Why the result fits: `|a + b| <= 2 * 10^9 < 2^31 = 2147483648`, so the true sum is representable as a signed 32-bit number and the conversion is exact. For inputs where the sum overflows 32 bits this method would wrap around silently, like C.
- Invariant: `a + b` (as numbers mod 2^32) is the same before and after each round.

**Complexity:** Time O(w) rounds with w = 32 the word width: the lowest set bit of the carry word moves up at least one column every round (the next carry is a subset of the old carry's columns shifted left), and the mask drops anything past bit 31, so after at most 32 rounds the carry is 0. `-3 + 3` reaches 32; the most rounds in my 20,000 random pairs was 18. Space O(1).

**Dry run:** `a = 7 (0111), b = 5 (0101)`.
- Round 1: `a ^ b = 0010 (2)`, `(a & b) << 1 = (0101) << 1 = 1010 (10)`.
- Round 2: `a = 0010, b = 1010`: `a ^ b = 1000 (8)`, `(a & b) << 1 = (0010) << 1 = 0100 (4)`.
- Round 3: `a = 1000, b = 0100`: `a ^ b = 1100 (12)`, `a & b = 0`, so `b = 0`. Stop: `[12, 3]`.

**Code:**
```python
import random

random.seed(2901)
MASK = 0xFFFFFFFF


def add(a, b):
    """a + b with only ^, &, <<. Returns [sum, rounds]. Everything is masked to 32 bits."""
    a &= MASK
    b &= MASK
    rounds = 0
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK   # sum without carry, carries moved one place left
        rounds += 1
    return [a if a <= 0x7FFFFFFF else ~(a ^ MASK), rounds]   # ~(a ^ MASK) == a - 2**32 for bit 31 set


def add_no_mask(a, b, cap=40):
    """The same loop WITHOUT masking: for a = -1, b = 1 it never ends (we stop it after `cap` rounds)."""
    trace = []
    for _ in range(cap):
        if b == 0:
            return a, trace
        a, b = a ^ b, (a & b) << 1
        trace.append((a, b))
    return None, trace


def ripple(a, b):
    """Brute force: a 32-bit ripple-carry adder built from single bits (full adders)."""
    out, carry = 0, 0
    for i in range(32):
        x, y = (a >> i) & 1, (b >> i) & 1
        out |= (x ^ y ^ carry) << i
        carry = (x & y) | (carry & (x ^ y))
    return out - (1 << 32) if out >> 31 else out


# dry run on a = 7, b = 5
a, b, r = 7, 5, 0
while b:
    a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    r += 1
    print(f"round {r}: a = {a:04b} ({a}), b = {b:04b} ({b})")

for (x, y), want in [((7, 5), [12, 3]), ((-3, 3), [0, 32]), ((10**9, 10**9), [2 * 10**9, 2]),
                     ((-10**9, -10**9), [-2 * 10**9, 2]), ((0, 0), [0, 0])]:
    got = add(x, y)
    assert got == want and got[0] == ripple(x, y) == x + y, (x, y, got)
    print(f"add({x}, {y}) -> {got}")

res, trace = add_no_mask(-1, 1)
print("no mask, a=-1, b=1: result after 40 rounds =", res, "| first states (a, b):", trace[:3], "... last b =", trace[-1][1])

# seeded random cross-check against the ripple-carry adder (sum only) and against +
mx = 0
for _ in range(20000):
    x, y = random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)
    s, rounds = add(x, y)
    assert s == ripple(x, y) == x + y
    mx = max(mx, rounds)
for x in range(-70, 71):
    for y in range(-70, 71):
        assert add(x, y)[0] == ripple(x, y) == x + y
print("20000 random + 141*141 small pairs ok; most rounds seen in the random run:", mx)
assert 2 * 10**9 < 2**31
assert add(10**9, 10**9)[0] == 2 * 10**9 and add(-1, 1) == [0, 32]
print("edge asserts ok")
```

**Output (my run):**
```
round 1: a = 0010 (2), b = 1010 (10)
round 2: a = 1000 (8), b = 0100 (4)
round 3: a = 1100 (12), b = 0000 (0)
add(7, 5) -> [12, 3]
add(-3, 3) -> [0, 32]
add(1000000000, 1000000000) -> [2000000000, 2]
add(-1000000000, -1000000000) -> [-2000000000, 2]
add(0, 0) -> [0, 0]
no mask, a=-1, b=1: result after 40 rounds = None | first states (a, b): [(-2, 2), (-4, 4), (-8, 8)] ... last b = 1099511627776
20000 random + 141*141 small pairs ok; most rounds seen in the random run: 18
edge asserts ok
```

**Edge cases:**
- `a = 0, b = 0`: no round at all, `[0, 0]`.
- `a = -b` (for example `-3 + 3`): the carry runs all the way off the top, 32 rounds, result 0.
- Both negative (`-10^9 + -10^9`): `a` ends above `0x7FFFFFFF`, the conversion gives `-2000000000`.
- Same-sign large values (`10^9 + 10^9`): the sum `2000000000` stays under `0x7FFFFFFF`, no conversion.
- Subtraction: negate with `~b + 1`, then add. Mask it too.

**Follow-ups:**
- *Do it recursively?* `add(a ^ b, (a & b) << 1)` with the same masking; the recursion depth is at most the number of rounds (32), safe under the default limit.
- *Multiply without `*`?* Shift-and-add over the bits of one operand, using this adder.
- *Why not just use `a + b`?* The question is about what carries are, and about Python's missing fixed width.

**Common mistakes:**
- No mask: infinite loop on negative operands, as shown above.
- Masking `a` and `b` at the start but not inside the loop (the shifted carry grows past 32 bits again).
- Converting with `a - 2**32` only when `a > 2**31` (off by one: bit 31 set means `a >= 2**31`, which is `a > 0x7FFFFFFF`).
- Writing `a & b << 1` without brackets: `<<` binds tighter than `&`.

### Q30 ⭐ 🟡 Enumerate subsets with a bitmask, and submasks. `items` has 0 <= len <= 12 distinct integers (any sign, |value| <= 100) and `target` is an integer. Using the mask `m` in 0..2^n - 1 where bit i means 'take items[i]', return `[found, pairs]`: `found` is the list of all subsets (each a list in the order of `items`) whose sum equals `target`, listed in increasing order of the mask value (so the empty subset, mask 0, comes first when target is 0); `pairs` is the number of (mask, submask) pairs visited when, for every mask m, you loop `sub = m; while sub: ...; sub = (sub - 1) & m` (non-empty submasks only). Explain why `(sub - 1) & m` visits every non-empty submask of `m` exactly once in decreasing order, and why `pairs` equals 3^n - 2^n (each item is in the submask, in the mask but not the submask, or in neither; subtract the empty submask of every mask). Say when a bitmask is better than recursion (small n, set as an integer, fast union and test) and when it is not. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a loop over all subsets using list slicing logic and a double loop testing `s & m == s` on small inputs. Example: items=[3, 1, 4, 2], target=5 -> [[[1, 4], [3, 2]], 65]; items=[], target=0 -> [[[]], 0]; items=[1, -1, 2], target=0 -> [[[], [1, -1]], 19]; items=[5], target=3 -> [[], 1].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bitmask enumeration of subsets (mask bit i = take item i) and the submask loop `sub = (sub - 1) & m`. The loop that makes subset DP over masks 3^n instead of 4^n.

**Say this first (1 line):** "Every integer m in 0..2^n - 1 is a subset; bit i says take item i. To list the subsets of a subset, step `sub = (sub - 1) & m`, which visits each non-empty submask once, biggest first."

**Brute force:** For every mask, build the subset with list logic and sum it (`2^n * n`). For the pair count, a double loop over all `m` and all `s` testing `s & m == s` is `4^n` steps. Both are the oracle in the code (n <= 7 there).

**Optimal:**
- Subsets: for `mask` in `range(1 << n)`, collect `items[i]` where `mask >> i & 1`; keep the list if the sum is `target`. Increasing mask order is the output order required: mask 0 (the empty subset) first, and a subset using a higher-index item comes later than any subset using only lower-index items. Cost O(2^n * n), at most 4096 * 12 steps here.
- Submasks: start with `sub = m`, loop `while sub:`, then `sub = (sub - 1) & m`.
- Why it visits every non-empty submask once, in decreasing order: let `p` be the lowest set bit of `sub`. `sub - 1` clears bit `p` and sets every bit below it; AND with `m` keeps only allowed bits. So `(sub - 1) & m` agrees with `sub` above `p`, has 0 at `p`, and has every bit of `m` that lies below `p`. It is smaller than `sub`, and any other submask of `m` that is smaller than `sub` must first differ from `sub` at bit `p` or above (below `p` `sub` has only zeros, so a difference there would make it bigger), so it cannot exceed this number. Hence it is the next smaller submask: the sequence strictly decreases through every submask and ends at 0, where the loop stops. (The code also checks this for every `m < 256`.)
- Why `pairs = 3^n - 2^n`: for a pair `(mask, sub)` with `sub` inside `mask`, each item is in `sub`, or in `mask` but not in `sub`, or in neither: 3 choices, so `3^n` pairs including the empty submask; the empty submask is excluded for each of the `2^n` masks. For n = 12 that is 531,441 - 4,096 = 527,345 (the code runs the real loop for n = 0..12 and checks).
- Bitmask versus recursion: a mask is great when n is small (<= about 20), the set is an integer, so union is `|`, intersection `&`, membership `mask >> i & 1`, and it is a key for a DP array or a dict. It is not great when n is large (2^n states), when you need pruning (a recursion can stop early; a plain mask loop cannot), or when the items are not a small fixed list.
- Negatives and zero are fine here: no bit trick touches the item values, only the mask integers, which are non-negative, so Python's unbounded negative integers never matter in this question.

**Complexity:** Subsets: time O(2^n * n), space O(output). Submask pair loop: time and count exactly 3^n - 2^n (about 5.3 * 10^5 for n = 12). Not polynomial: that is the nature of the problem, not of the code.

**Dry run:** `items = [3, 1, 4, 2], target = 5`. Bit 0 = item 3, bit 1 = item 1, bit 2 = item 4, bit 3 = item 2. Masks with sum 5: `0110` (6) takes items 1 and 4, sum 5; `1001` (9) takes 3 and 2, sum 5. Increasing order gives `[[1, 4], [3, 2]]`. The pair count is `3^4 - 2^4 = 81 - 16 = 65`. For the submask loop on `m = 1011`: `1011, 1010, 1001, 1000, 0011, 0010, 0001`, then `sub = 0001 - 1 = 0000`, stop. That is 7 = 2^3 - 1 non-empty submasks (decreasing, each once).

**Code:**
```python
import random

random.seed(3001)


def solve(items, target):
    n = len(items)
    found = []
    for mask in range(1 << n):                       # increasing mask order
        total = 0
        for i in range(n):
            if mask >> i & 1:                        # bit i set = take items[i]
                total += items[i]
        if total == target:
            found.append([items[i] for i in range(n) if mask >> i & 1])
    pairs = 0
    for mask in range(1 << n):
        sub = mask
        while sub:                                   # non-empty submasks only
            pairs += 1
            sub = (sub - 1) & mask                   # next smaller submask of mask
    return [found, pairs]


def brute(items, target):
    n = len(items)
    all_subsets = [[items[i] for i in range(n) if (m >> i) % 2 == 1] for m in range(1 << n)]
    found = [s for s in all_subsets if sum(s) == target]
    pairs = sum(1 for m in range(1 << n) for s in range(1, 1 << n) if s & m == s)   # double loop
    return [found, pairs]


# dry run: submasks of m = 0b1011 (11) in the order the loop visits them
m, sub, order = 0b1011, 0b1011, []
while sub:
    order.append(format(sub, "04b"))
    sub = (sub - 1) & m
print("submasks of 1011:", order, "count", len(order), "= 2^3 - 1")

# dry run: items [3, 1, 4, 2], target 5 -> which masks hit
items = [3, 1, 4, 2]
for mask in range(16):
    pick = [items[i] for i in range(4) if mask >> i & 1]
    if sum(pick) == 5:
        print(f"mask {mask:>2} = {mask:04b} takes {pick} sum 5")

for it, tg, want in [([3, 1, 4, 2], 5, [[[1, 4], [3, 2]], 65]), ([], 0, [[[]], 0]),
                     ([1, -1, 2], 0, [[[], [1, -1]], 19]), ([5], 3, [[], 1])]:
    got = solve(it, tg)
    assert got == want == brute(it, tg), (it, tg, got)
    print(it, tg, "->", got)

# pairs = 3^n - 2^n for every n up to 12 (runs the real loop)
for n in range(13):
    assert solve(list(range(n)), 10**9)[1] == 3**n - 2**n
print("pairs == 3^n - 2^n for n = 0..12; at n = 12 that is", 3**12 - 2**12)

# submask claim: decreasing order, each exactly once, for every m < 256
for m in range(256):
    seen, sub = [], m
    while sub:
        seen.append(sub)
        sub = (sub - 1) & m
    assert seen == sorted((s for s in range(1, 256) if s & m == s), reverse=True)

# seeded random cross-check
for _ in range(300):
    n = random.randint(0, 7)
    it = random.sample(range(-100, 101), n)
    tg = random.choice([0, random.randint(-20, 20), sum(random.sample(it, random.randint(0, n))) if n else 0])
    assert solve(it, tg) == brute(it, tg)
print("300 seeded random cases ok; submask order claim ok for every m < 256")
assert solve([], 0) == [[[]], 0] and solve([0], 0)[0] == [[], [0]]
print("edge asserts ok")
```

**Output (my run):**
```
submasks of 1011: ['1011', '1010', '1001', '1000', '0011', '0010', '0001'] count 7 = 2^3 - 1
mask  6 = 0110 takes [1, 4] sum 5
mask  9 = 1001 takes [3, 2] sum 5
[3, 1, 4, 2] 5 -> [[[1, 4], [3, 2]], 65]
[] 0 -> [[[]], 0]
[1, -1, 2] 0 -> [[[], [1, -1]], 19]
[5] 3 -> [[], 1]
pairs == 3^n - 2^n for n = 0..12; at n = 12 that is 527345
300 seeded random cases ok; submask order claim ok for every m < 256
edge asserts ok
```

**Edge cases:**
- `items = []`: one mask (0), the empty subset sums to 0. If `target == 0` the answer is `[[]]`, and `pairs = 0`.
- `target` unreachable: `found = []`, but `pairs` is still `3^n - 2^n`.
- Zero in the items (`[0]`, target 0): both `[]` and `[0]` match, in mask order: `[[], [0]]`.
- Negative values: `[1, -1, 2]`, target 0 gives `[[], [1, -1]]`; the empty subset is a legitimate match.
- `n = 12`: 4096 masks, about 4 * 10^3 * 12 steps for the sums, and 527,345 pair steps.

**Follow-ups:**
- *Same problem with meet in the middle?* Split the items in two halves, list the sums of each half (2^(n/2) each), and match with a dict. It beats 2^n for n around 40. Not run here.
- *Where does 3^n show up in a real problem?* Subset DP where `dp[m]` is built from `dp[sub]` and `dp[m ^ sub]` for each submask (partition-into-groups problems). Say it is 3^n, not 4^n.
- *Next larger mask with the same popcount?* Gosper's hack. I would only mention it, not write it from memory.

**Common mistakes:**
- Looping `while sub >= 0`, or forgetting that `sub = 0` must stop the loop (otherwise `(0 - 1) & m = m` and it cycles forever).
- Writing `(sub - 1) | m`, which gives larger numbers, not submasks.
- Counting the empty submask and getting `3^n`.
- Listing subsets in a different order (for example by size) when the prompt asks for increasing mask order.
- Using `1 << n` as the upper bound with `range(1 << n - 1)`: `<<` binds looser than `-` in Python, so that means `1 << (n - 1)`. Bracket it.

### Q31 ⭐ 🟡 Pruning and the cost of backtracking: count the calls. `candidates` has 1 <= len <= 8 distinct positive integers (each <= 20) and `target` is 1 <= target <= 40. Two recursions find the combinations (unlimited reuse) that sum to `target`. Version A keeps the candidates in the given order: `dfs(start, rem)` counts one call, returns if `rem < 0`, records a hit and returns if `rem == 0`, otherwise loops `j` from `start` to the end and calls `dfs(j, rem - c[j])`. Version B sorts the candidates first and also breaks out of the loop as soon as `c[j] > rem` (so it never calls with a negative remainder). Return `[calls_A, calls_B, hits]` (counting the first call `dfs(0, target)`, and `hits` is the same for both). Explain why B never makes more calls than A, why the two hit counts agree, and give one example where B saves a lot and one where it saves nothing. Do not claim a complexity from these counts; they only measure two implementations on inputs. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the same two recursions rewritten with an explicit stack on small inputs. Example: candidates=[5, 2, 3], target=8 -> [19, 13, 3]; candidates=[7], target=1 -> [2, 1, 0]; candidates=[4, 2, 3, 1], target=10 -> [102, 94, 23]; candidates=[1], target=5 -> [6, 6, 1].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking cost measurement: choose, explore, undo, with a pruning rule (sort, then `break` once a candidate is too big) judged by counting recursive calls. Counting calls measures an implementation on an input, it does not prove a big-O.

**Say this first (1 line):** "Both versions explore the same combinations; B sorts and breaks on `c[j] > rem`, so it never makes the call that would only return on `rem < 0`, and I will show the call counts on real inputs, not claim a complexity from them."

**Brute force:** Version A: keep the given order and try every candidate at every node; return at `rem < 0` (wasted call) and record a hit at `rem == 0`. It is correct and is also the unpruned baseline. An explicit-stack rewrite of both versions is the oracle in the code.

**Optimal:** Version B (the pruned one):
- Sort once so candidates ascend.
- In the loop over `j`, `break` when `c[j] > rem`: every later candidate is at least as big, so every later call would have `rem < 0`. This is a safe cut, not a heuristic.
- Decision tree: a node is `dfs(start, rem)`; its children are "take `c[j]`" for `j >= start` (staying on `j` allows reuse, starting at `j` stops order permutations from repeating a combination). Undo is implicit because `rem` is passed by value.
- Why B never makes more calls than A: every call B makes corresponds to a multiset of candidates with total at most `target` (the empty multiset is the root). In A, the same multiset, taken in A's index order, is also a call: all its proper prefixes have a smaller total than the full total, so all have `rem > 0` and none stops early. B visits each such multiset once; A visits all of them as well and also makes the calls with `rem < 0`. So `calls_B <= calls_A`. (The code checks `calls_B` equals the number of multisets with sum at most `target` on random inputs, and the inequality exhaustively on 5,376 cases.)
- Why the hit counts agree: a hit is a multiset with total exactly `target`, and both versions visit each such multiset exactly once.
- Where B saves a lot: candidates that are mostly big compared with the remainder, so many loop iterations are over-shoots (`[3, 5, 7, 11, 13, 17, 19, 20]`, target 40: 2,282 calls against 573). Where it saves nothing: a single candidate of 1 (`[1]`, target 5: every call is useful, 6 and 6), or a list that is already descending such as `[20, 1]` with target 40 (63 and 63 in my run: the 20 is only ever tried at the root and at `rem = 20`, where it fits, so A makes no wasted call).
- Depth: at most `target / min(candidate) + 1`, so 41 at most (candidate 1, target 40), far below the recursion limit of 1000.

**Complexity:** Reasoned, not measured: the number of calls in B is the number of multisets of the candidates with sum at most `target`, which can grow fast with the target; the counts below are examples on inputs, nothing more. Space O(depth) <= 41 frames plus the output counters.

**Dry run:** `candidates = [5, 2, 3]`, target 8. Version A prints a 19-call tree (6 of its calls are `rem < 0` leaves); version B on the sorted `[2, 3, 5]` prints 13 calls and the break removes all 6 over-shoots. Both have the 3 hits `2+2+2+2`, `2+3+3` and `3+5`. The trees are in the output below. Reading A: root `rem=8`; `take 5` leaves 3; from there `take 5` gives `-2` (wasted), `take 2` gives 1, `take 3` gives 0 (hit). In B a node with `rem=2` (after `take 3, take 3`) makes no call at all, because every remaining candidate (3 and 5) is bigger than 2.

**Code:**
```python
import itertools
import random

random.seed(3101)


def run(c, prune, target, trace=None):
    """Version A (prune=False, c as given) or version B (prune=True, c must be sorted).
    Returns (calls, hits). If trace is a list, appends an indented line per call."""
    calls = hits = 0

    def dfs(start, rem, depth, label):
        nonlocal calls, hits
        calls += 1
        note = "rem<0 stop" if rem < 0 else "HIT" if rem == 0 else ""
        if trace is not None:
            trace.append("  " * depth + f"{label}rem={rem} {note}".rstrip())
        if rem < 0:
            return
        if rem == 0:
            hits += 1
            return
        for j in range(start, len(c)):
            if prune and c[j] > rem:
                break                        # sorted: every later candidate is at least as big
            dfs(j, rem - c[j], depth + 1, f"take {c[j]}: ")

    dfs(0, target, 0, "")
    return calls, hits


def solve(candidates, target):
    a, ha = run(list(candidates), False, target)
    b, hb = run(sorted(candidates), True, target)
    assert ha == hb
    return [a, b, ha]


def brute(candidates, target):
    """Same two rules with an explicit stack (no recursion), children pushed in reverse."""
    def go(c, prune):
        calls = hits = 0
        stack = [(0, target)]
        while stack:
            start, rem = stack.pop()
            calls += 1
            if rem < 0:
                continue
            if rem == 0:
                hits += 1
                continue
            for j in range(len(c) - 1, start - 1, -1):
                if prune and c[j] > rem:
                    continue                 # same as 'break' because c is sorted
                stack.append((j, rem - c[j]))
        return calls, hits
    a, ha = go(list(candidates), False)
    b, hb = go(sorted(candidates), True)
    return [a, b, ha]


# decision trees for candidates=[5, 2, 3], target=8
for name, c, prune in [("A (given order 5,2,3)", [5, 2, 3], False), ("B (sorted 2,3,5, with break)", [2, 3, 5], True)]:
    t = []
    calls, hits = run(c, prune, 8, t)
    print(f"--- {name}: {calls} calls, {hits} hits")
    print("\n".join(t))

for c, t, want in [([5, 2, 3], 8, [19, 13, 3]), ([7], 1, [2, 1, 0]), ([4, 2, 3, 1], 10, [102, 94, 23]), ([1], 5, [6, 6, 1])]:
    got = solve(c, t)
    assert got == want == brute(c, t), (c, t, got)
    print(c, t, "->", got)

big = [3, 5, 7, 11, 13, 17, 19, 20]
print("B saves a lot:", big, 40, "->", solve(big, 40))
print("B saves nothing:", [1], 5, "->", solve([1], 5), "| and", [20, 1], 40, "->", solve([20, 1], 40))

# why B <= A: B's calls are exactly the multisets with sum <= target (empty one = root); each also exists in A
def multisets_le(c, target):
    n = 0
    def go(start, total):
        nonlocal n
        n += 1
        for j in range(start, len(c)):
            if total + c[j] <= target:
                go(j, total + c[j])
    go(0, 0)
    return n

for _ in range(300):
    k = random.randint(1, 5)
    c = random.sample(range(1, 21), k)
    t = random.randint(1, 40)
    a, b, h = solve(c, t)
    assert b == multisets_le(sorted(c), t) and b <= a
    assert [a, b, h] == brute(c, t)
print("300 seeded random cases: B == #multisets with sum <= target, B <= A, hits agree, explicit stack agrees")

# exhaustive: every ordering of every 3-subset of 1..8, targets 1..16
cnt = 0
for cs in itertools.combinations(range(1, 9), 3):
    for perm in itertools.permutations(cs):
        for t in range(1, 17):
            a, ha = run(list(perm), False, t)
            b, hb = run(list(cs), True, t)
            assert b <= a and ha == hb
            cnt += 1
print("exhaustive over", cnt, "(ordering, target) cases: calls_B <= calls_A and hits agree")
assert solve([1], 40) == [41, 41, 1]
print("edge asserts ok (depth 41 for candidate 1, target 40)")
```

**Output (my run):**
```
--- A (given order 5,2,3): 19 calls, 3 hits
rem=8
  take 5: rem=3
    take 5: rem=-2 rem<0 stop
    take 2: rem=1
      take 2: rem=-1 rem<0 stop
      take 3: rem=-2 rem<0 stop
    take 3: rem=0 HIT
  take 2: rem=6
    take 2: rem=4
      take 2: rem=2
        take 2: rem=0 HIT
        take 3: rem=-1 rem<0 stop
      take 3: rem=1
        take 3: rem=-2 rem<0 stop
    take 3: rem=3
      take 3: rem=0 HIT
  take 3: rem=5
    take 3: rem=2
      take 3: rem=-1 rem<0 stop
--- B (sorted 2,3,5, with break): 13 calls, 3 hits
rem=8
  take 2: rem=6
    take 2: rem=4
      take 2: rem=2
        take 2: rem=0 HIT
      take 3: rem=1
    take 3: rem=3
      take 3: rem=0 HIT
    take 5: rem=1
  take 3: rem=5
    take 3: rem=2
    take 5: rem=0 HIT
  take 5: rem=3
[5, 2, 3] 8 -> [19, 13, 3]
[7] 1 -> [2, 1, 0]
[4, 2, 3, 1] 10 -> [102, 94, 23]
[1] 5 -> [6, 6, 1]
B saves a lot: [3, 5, 7, 11, 13, 17, 19, 20] 40 -> [2282, 573, 57]
B saves nothing: [1] 5 -> [6, 6, 1] | and [20, 1] 40 -> [63, 63, 3]
300 seeded random cases: B == #multisets with sum <= target, B <= A, hits agree, explicit stack agrees
exhaustive over 5376 (ordering, target) cases: calls_B <= calls_A and hits agree
edge asserts ok (depth 41 for candidate 1, target 40)
```

**Edge cases:**
- `[7]`, target 1: A makes 2 calls (root, then `rem = -6`), B makes 1 (7 > 1 breaks immediately), 0 hits.
- `[1]`, target 5: the tree is a chain of 6 calls in both.
- Target equal to a candidate: one hit, B makes few calls.
- Unsorted input: B sorts first; without sorting, the `break` would be wrong (a later candidate can be smaller). This is the usual bug.
- Candidates are distinct and positive by the prompt; a 0 or negative would break the termination argument and the `break` rule.

**Follow-ups:**
- *Why not memoise?* The question lists the combinations or counts calls; to count them, a DP (Part 10 Q10, coin change II) is O(n * target). The call counts here belong to the enumeration.
- *Does B change the answer order?* The sorted input changes the order of results if you print them; the count of hits is unchanged. Sort the result list if the output order is specified.
- *Is the count of calls a complexity?* No: it is one number for one input. A bound comes from reasoning (multisets with total at most `target`), not from a table of counts.

**Common mistakes:**
- Sorting but forgetting the `break` (the answer is right, the speed gain is gone: the loop still makes the wasted calls).
- Using `continue` instead of `break` after sorting; it works but still scans the whole tail of the loop.
- Breaking without sorting, which skips valid smaller candidates.
- Recursing with `dfs(j + 1, ...)` (each candidate once) when reuse is allowed.
- Saying "pruning makes it polynomial": it only removes dead calls.

### Q32 ⭐ 🟡 Iterative backtracking and the recursion limit. `board` is a list of rows (strings of equal length, lowercase) with 1 <= rows * cols <= 2000, and `word` is a string of length 1 to 2000. Return True if `word` can be spelled along a path of horizontally or vertically adjacent cells that uses no cell twice. The single-word recursion of Q9 nests one frame per letter, so a 1 x 1500 row of 'a' with `word = 'a' * 1500` raises RecursionError under CPython's default limit of 1000 (run it and show the message), while the same recursion on a row of 300 works; in this question your solution must be ITERATIVE: keep an explicit stack of (cell, next-direction-index) frames and a set of cells on the path, push when you extend the path, and pop (removing the cell from the set) when all four directions are tried. The tests are corridor-shaped boards (one row, or a winding one-cell-wide path of 'a' bordered by 'b'), on which the search is fast; on an open board of equal letters the search time is exponential for ANY backtracking solution and is out of scope. Say what an explicit stack costs in Python compared with the call stack, and that raising the limit with sys.setrecursionlimit is an observation about one machine and Python version and not a fix you can promise. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the recursive version of Q9 on boards small enough for its depth on small inputs. Example: board=['aab', 'bba'], word='aba' -> True; board=['abc'], word='cba' -> True; board=['abc'], word='abca' -> False; board=['aaaa'], word='aaaa' -> True; board=['ab', 'ca'], word='acb' -> False.
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with an explicit stack: the call stack is replaced by a list of frames (cell, next direction), plus a set of cells on the path, so the depth is no longer limited by CPython's recursion limit.

**Say this first (1 line):** "Same search as the recursive word search, but each frame is an entry in my own list: I push when I extend the path and pop, removing the cell from the set, when all four directions are tried."

**Brute force:** The recursive word search of Q9: one Python frame per letter, add the cell to a set, try four neighbours, discard on the way back. It is correct, but on a 1 x 1500 row of `'a'` with a 1500-letter word it raises `RecursionError: maximum recursion depth exceeded` under the default limit of 1000 (shown below), and it works on a row of 300.

**Optimal:** The iterative version:
- Frames: `path` is a list of cells, `nxt[k]` is the next direction index (0..4) to try from `path[k]`, and `on_path` is a set of the same cells for O(1) membership.
- Loop `while path`: if `len(path) == L` return True. Take the top cell and its direction `d`. If `d == 4`, all directions are tried: pop the frame and discard the cell from the set (this is the undo). Otherwise increment `nxt[-1]` and look at the neighbour; if it is on the board, not on the path and equals `word[len(path)]`, push it.
- Start the search from every cell equal to `word[0]`; when a start finishes without success, `path` is empty again (every push was matched by a pop), so the next start begins clean.
- Cheap guard: `L > rows * cols` is an immediate False (a path needs L distinct cells).
- Invariant: `path` is a simple path spelling `word[:len(path)]`, `on_path` equals the set of its cells.
- What the explicit stack costs: you write and maintain the frame state by hand (more code, easier to get the undo wrong); the frames are heap objects in lists, which is O(L) memory just as the call stack would be, but with no limit of 1000 and no `RecursionError`; and each step is a loop iteration with list indexing instead of a function call. I did not time it and make no claim about which is faster.
- `sys.setrecursionlimit`: on this machine (Python 3.13) the 1 x 1500 recursive case works after setting the limit to 5000 (shown below). That is an observation about one machine and version. A very deep recursion can still exhaust the memory or the C stack on another build and crash the process rather than raise a clean error, so I would not promise it as the fix; I would use the explicit stack.
- Scope: this is fast on corridor-shaped boards (one row, or a one-cell-wide winding path bordered by other letters). On an open board of equal letters any backtracking solution is exponential in the worst case; that is out of scope.

**Complexity:** On the corridor tests: each start explores one path of at most L cells, with at most 4 neighbour checks per cell, so one start is O(4 * L) and all starts are O(R * C * L) at most (about 1960 * 1025 * 4 for the serpentine); on these boards no sub-search branches, because every `'a'` cell has at most two `'a'` neighbours. In general the worst case is exponential. Space O(L) for `path`, `nxt` and `on_path`.

**Dry run:** `board = ['aab', 'bba'], word = 'aba'` (cells as (row, col)). Directions are tried right, down, left, up.
- Start at (0,0) 'a'. Need 'b': right (0,1) is 'a' no; down (1,0) is 'b' yes, push. Need 'a': right (1,1) is 'b' no; down is off the board; left off; up (0,0) is on the path. Direction 4 reached, pop (1,0). Back at (0,0): left, up are off the board, pop (0,0).
- Start at (0,1) 'a'. Need 'b': right (0,2) is 'b', push. Need 'a': right off the board; down (1,2) is 'a', push. Length 3 equals L: True. The path a-b-a is (0,1), (0,2), (1,2).

**Code:**
```python
import random
import sys

random.seed(3201)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]          # right, down, left, up


def exist_iter(board, word, trace=None):
    """Iterative word search. path = list of cells, nxt = next direction index per frame, on_path = set."""
    R, C, L = len(board), len(board[0]), len(word)
    if L > R * C:
        return False
    for sr in range(R):
        for sc in range(C):
            if board[sr][sc] != word[0]:
                continue
            path, nxt, on_path = [(sr, sc)], [0], {(sr, sc)}
            if trace is not None:
                trace.append(f"start {path[0]}")
            while path:
                if len(path) == L:
                    return True
                r, c = path[-1]
                d = nxt[-1]
                if d == 4:                           # all four directions tried: undo this cell
                    path.pop()
                    nxt.pop()
                    on_path.discard((r, c))
                    if trace is not None:
                        trace.append(f"pop {(r, c)}")
                    continue
                nxt[-1] += 1
                nr, nc = r + DIRS[d][0], c + DIRS[d][1]
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in on_path and board[nr][nc] == word[len(path)]:
                    path.append((nr, nc))
                    nxt.append(0)
                    on_path.add((nr, nc))
                    if trace is not None:
                        trace.append(f"push {(nr, nc)} for '{word[len(path) - 1]}'")
    return False


def exist_rec(board, word):
    """The Q9 style recursion: one frame per letter."""
    R, C = len(board), len(board[0])
    on_path = set()

    def go(r, c, k):
        if board[r][c] != word[k] or (r, c) in on_path:
            return False
        if k == len(word) - 1:
            return True
        on_path.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                return True
        on_path.discard((r, c))                       # undo on the way back
        return False

    return any(go(r, c, 0) for r in range(R) for c in range(C))


def serpentine(rows_of_a, width):
    """One-cell-wide winding corridor of 'a' inside a border of 'b'. Returns (board, number of a cells)."""
    rows = []
    for i in range(2 * rows_of_a - 1):
        if i % 2 == 0:
            rows.append("a" * width)
        elif (i // 2) % 2 == 0:
            rows.append("b" * (width - 1) + "a")
        else:
            rows.append("a" + "b" * (width - 1))
    return rows, sum(r.count("a") for r in rows)


# dry run
tr = []
print("dry run board=['aab','bba'] word='aba':", exist_iter(["aab", "bba"], "aba", tr))
print("\n".join("  " + t for t in tr))

for b, w, want in [(["aab", "bba"], "aba", True), (["abc"], "cba", True), (["abc"], "abca", False),
                   (["aaaa"], "aaaa", True), (["ab", "ca"], "acb", False)]:
    assert exist_iter(b, w) == exist_rec(b, w) == want, (b, w)
    print(b, w, "->", exist_iter(b, w))

# the recursion limit, observed on this machine (Python %s)
print("python", sys.version.split()[0], "default recursion limit", sys.getrecursionlimit())
row = ["a" * 1500]
try:
    exist_rec(row, "a" * 1500)
except RecursionError as e:
    print("recursive, 1 x 1500:", type(e).__name__ + ":", e)
print("recursive, 1 x 300:", exist_rec(["a" * 300], "a" * 300))
print("iterative, 1 x 1500:", exist_iter(row, "a" * 1500), "| 1 x 1500 word of 1501:", exist_iter(row, "a" * 1501))

board, n_a = serpentine(25, 40)
cells = len(board) * len(board[0])
print(f"serpentine {len(board)} x {len(board[0])} = {cells} cells, {n_a} cells of 'a'")
print("iterative, word = 'a' * %d:" % n_a, exist_iter(board, "a" * n_a), "| word = 'a' * %d:" % (n_a + 1), exist_iter(board, "a" * (n_a + 1)))
assert exist_iter(board, "a" * n_a) is True and exist_iter(board, "a" * (n_a + 1)) is False
try:
    exist_rec(board, "a" * n_a)
except RecursionError:
    print("recursive on the same corridor: RecursionError")

# raising the limit: an observation about this machine and version, not a guarantee
old = sys.getrecursionlimit()
sys.setrecursionlimit(5000)
print("recursive, 1 x 1500 with limit 5000:", exist_rec(row, "a" * 1500))
sys.setrecursionlimit(old)

# seeded random cross-check of iterative vs recursive Q9 on small boards
for _ in range(600):
    r, c = random.randint(1, 4), random.randint(1, 4)
    al = random.choice(["ab", "abc", "a"])
    b = ["".join(random.choice(al) for _ in range(c)) for _ in range(r)]
    w = "".join(random.choice(al) for _ in range(random.randint(1, min(8, 2 * r * c))))
    assert exist_iter(b, w) == exist_rec(b, w), (b, w)
print("600 seeded random boards: iterative == recursive")
assert not exist_iter(["abc", "xxx"], "abcb") and not exist_rec(["abc", "xxx"], "abcb")
assert exist_iter(["a"], "a") and not exist_iter(["a"], "aa") and not exist_iter(["ab"], "ba" + "a")
print("edge asserts ok")
```

**Output (my run):**
```
dry run board=['aab','bba'] word='aba': True
  start (0, 0)
  push (1, 0) for 'b'
  pop (1, 0)
  pop (0, 0)
  start (0, 1)
  push (0, 2) for 'b'
  push (1, 2) for 'a'
['aab', 'bba'] aba -> True
['abc'] cba -> True
['abc'] abca -> False
['aaaa'] aaaa -> True
['ab', 'ca'] acb -> False
python 3.13.17 default recursion limit 1000
recursive, 1 x 1500: RecursionError: maximum recursion depth exceeded
recursive, 1 x 300: True
iterative, 1 x 1500: True | 1 x 1500 word of 1501: False
serpentine 49 x 40 = 1960 cells, 1024 cells of 'a'
iterative, word = 'a' * 1024: True | word = 'a' * 1025: False
recursive on the same corridor: RecursionError
recursive, 1 x 1500 with limit 5000: True
600 seeded random boards: iterative == recursive
edge asserts ok
```

**Edge cases:**
- `L > rows * cols`: False at once.
- 1 x 1 board: `['a']` with `'a'` is True, with `'aa'` is False (a cell cannot be reused).
- The word needs the same cell twice (`['abc', 'xxx']`, `'abcb'`): False, because the set blocks it even though L = 4 is below the 6 cells.
- Backtracking undo: forgetting to discard the cell from `on_path` on pop makes later starts see stale cells (wrong answers on some boards).
- The start cell is not unique: `['aab', 'bba']` first start at (0,0) fails and the second one succeeds.

**Follow-ups:**
- *Could you keep the recursion and raise the limit?* On one machine it worked (1500 deep with a limit of 5000 here). I would not rely on it; the limit protects the C stack and the safe value depends on the build.
- *A trick to convert any recursion to a stack?* Put the arguments plus a "which child next" counter into a frame, push for the call, pop for the return; that is exactly `(cell, next direction)` here.
- *Open boards of equal letters?* Exponential for any backtracking; with the word's letter counts or a quick reachability check you can prune, but the worst case stays.

**Common mistakes:**
- Pushing a neighbour but not adding it to `on_path`, or popping without discarding.
- Marking the starting cell on the path only when the first push happens (the start itself is on the path from the start).
- Checking the length only after a push and so missing `L == 1`: here the check is at the top of the loop, so a one-letter word is found at once.
- Raising the recursion limit and calling it solved.
- Testing the recursive version on large boards and believing a `RecursionError` means a wrong answer: it means the depth.

### Q33 ⭐ 🟡 Trie memory versus a dict of sets. `words` has 1 to 5000 lowercase words (length 1 to 20, repeats allowed). Return `[nodes, slots26, pairs, distinct]`: `nodes` is the number of trie nodes excluding the root; `slots26` is `26 * (nodes + 1)`, the number of child slots if every node, root included, holds a fixed array of 26 children; `pairs` is the number of (prefix, word) pairs you would store in a dict that maps every non-empty prefix to the set of distinct words having that prefix (the sum of the lengths of the distinct words); and `distinct` is the number of distinct words. Explain what each number means in memory terms (dict children store only the existing edges, an array of 26 stores empty slots too, the dict of sets repeats every word under each of its prefixes and its keys are exactly the trie's nodes), why `nodes <= pairs` and when they are equal (exactly when no two distinct words share a first letter), and what a trie does NOT save compared with a plain `set` of words. You may measure `sys.getsizeof` on your machine, labelled as a sandbox measurement for one Python version, but do not present sizes as proof. Part 7 Q41 builds the trie at concept level and Part 3 Q36 compares it with a sorted list for prefix counts; the full API is Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against counting the distinct prefixes of the distinct words with a set on small inputs. Example: words=['car', 'cart', 'cat', 'dog', 'do', 'car'] -> [8, 234, 15, 5]; words=['a', 'b', 'c'] -> [3, 104, 3, 3]; words=['aaa'] -> [3, 104, 3, 1]; words=['ab', 'ac'] -> [3, 104, 4, 2].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Trie memory accounting (concept level): count nodes, child slots and stored pairs, and compare three layouts: a trie with dict children, a trie with a fixed array of 26 children, and a dict from every prefix to the set of words that have it.

**Say this first (1 line):** "Nodes are the distinct non-empty prefixes of the distinct words; a 26-array pays for every empty slot, a dict of sets repeats each word under all its prefixes, and a trie still does not beat a plain set of words when prefixes are not shared."

**Brute force:** Put every distinct word into a `set`, collect every non-empty prefix of every distinct word into another `set`, and count: `nodes` = number of distinct prefixes, `pairs` = sum of the distinct words' lengths. This is the oracle in the code.

**Optimal:** Build the dict-of-dicts trie once and count:
- `nodes`: each time an edge `ch` is missing and created, add 1. The root is not counted. Repeats of a word create nothing, so I insert distinct words only.
- `slots26 = 26 * (nodes + 1)`: with an array of 26 child slots per node, the root also holds an array, so there are `nodes + 1` arrays.
- `pairs`: the dict of sets stores `(prefix, word)` once per non-empty prefix of each distinct word, so `pairs = sum(len(w) for w in distinct)`.
- `distinct = len(set(words))`.
- What each number means in memory terms:
  - Dict children store only the edges that exist, so the number of entries is `nodes` (every non-root node has exactly one incoming edge), plus one dict object per node.
  - The array of 26 stores empty slots too: `slots26` is mostly empty for sparse tries, though it gives O(1) indexing by `ord(ch) - 97` and no hashing.
  - The dict of sets repeats every word under each of its prefixes: `pairs` set entries. Its keys are exactly the trie's nodes (the distinct non-empty prefixes), so it has the trie's node count in keys plus the repeated set entries. It answers "all words with this prefix" in O(answer) after one hash lookup, which is its reason to exist.
- Why `nodes <= pairs`: each node is a distinct prefix, and each distinct prefix of a distinct word is one of the `pairs` (prefix, word) pairs, so the number of distinct prefixes cannot exceed the number of pairs.
- When they are equal: exactly when no two distinct words share a first letter. If two words share a first letter they share that first node, so there are fewer nodes than pairs. If all first letters differ, no prefix is shared at all (different first letters mean different prefixes), so every pair is its own node. The code checks this on 1,500 random lists and exhaustively on small ones.
- What a trie does NOT save compared with a plain `set` of words: the set stores each word once (about its length in bytes plus a fixed object overhead) and answers "is this exact word present" in O(L) as well (hashing a word is O(L)). A trie wins only when prefixes are shared heavily or when you need prefix queries, ordered traversal or per-prefix counts; with unshared words it has more objects (one dict or array per node) than the set has strings. Sandbox sizes below agree on this machine.
- Sandbox sizes, labelled: shallow `sys.getsizeof` sums on this machine and Python 3.13. On 5,000 random words (4,582 distinct) with 38,952 nodes, the dict-children trie was about 6.7 MB (about 172 bytes per node), the trie of 26-lists about 10.3 MB, the plain set about 0.37 MB (about 81 bytes per distinct word) and the dict of sets about 12.3 MB. On 16 distinct words that share a 20-letter prefix the trie was smaller than the dict of sets (7.5 KB against 27.6 KB) but the set was smaller still (1.8 KB). These sizes are shallow, one run, one Python version: not a proof of anything.

**Complexity:** Building the trie is O(total length of the distinct words) time (here at most 5000 * 20 = 10^5 steps), with `nodes` <= that total. Memory is proportional to `nodes` (dict children) or `26 * (nodes + 1)` (arrays); the dict of sets is proportional to `pairs`.

**Dry run:** `words = ['car', 'cart', 'cat', 'dog', 'do', 'car']`. Distinct: `car, cart, cat, dog, do`, so `distinct = 5` (the repeated `car` adds nothing). Inserting in sorted order, new nodes (as prefixes): `car` makes `c, ca, car`; `cart` makes `cart`; `cat` makes `cat`; `do` makes `d, do`; `dog` makes `dog`. That is 3 + 1 + 1 + 2 + 1 = 8 nodes. `slots26 = 26 * 9 = 234`. `pairs = 3 + 4 + 3 + 3 + 2 = 15`. So `[8, 234, 15, 5]`. Note `8 < 15`: `car`, `cart`, `cat` share `c` and `ca`.

**Code:**
```python
import itertools
import random
import sys

random.seed(3301)


def trie_numbers(words):
    """Returns [nodes, slots26, pairs, distinct] using a dict-of-dicts trie."""
    distinct = set(words)
    root = {}
    nodes = 0
    for w in distinct:                       # repeats change nothing, so insert each distinct word once
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                nodes += 1
            node = node[ch]
    pairs = sum(len(w) for w in distinct)    # every non-empty prefix of w pairs with w once
    return [nodes, 26 * (nodes + 1), pairs, len(distinct)]


def brute(words):
    distinct = set(words)
    prefixes = {w[:i] for w in distinct for i in range(1, len(w) + 1)}   # distinct non-empty prefixes
    return [len(prefixes), 26 * (len(prefixes) + 1), sum(len(w) for w in distinct), len(distinct)]


# dry run on the first example
words = ["car", "cart", "cat", "dog", "do", "car"]
seen = set()
for w in sorted(set(words)):
    new = [w[:i] for i in range(1, len(w) + 1) if w[:i] not in seen]
    seen.update(new)
    print(f"insert {w!r:7} new nodes: {new}")
print("nodes =", len(seen), "(the distinct non-empty prefixes)")

for ws, want in [(["car", "cart", "cat", "dog", "do", "car"], [8, 234, 15, 5]), (["a", "b", "c"], [3, 104, 3, 3]),
                 (["aaa"], [3, 104, 3, 1]), (["ab", "ac"], [3, 104, 4, 2])]:
    got = trie_numbers(ws)
    assert got == want == brute(ws), (ws, got)
    print(ws, "->", got)

# claim: dict of sets has exactly the trie's nodes as keys; nodes <= pairs; equality iff first letters all differ
for _ in range(1500):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 6))]
    nodes, slots, pairs, distinct = trie_numbers(ws)
    assert [nodes, slots, pairs, distinct] == brute(ws)
    d = {}
    for w in set(ws):
        for i in range(1, len(w) + 1):
            d.setdefault(w[:i], set()).add(w)
    assert len(d) == nodes and sum(len(v) for v in d.values()) == pairs and nodes <= pairs
    firsts = {w[0] for w in set(ws)}
    assert (nodes == pairs) == (len(firsts) == distinct)
print("1500 seeded random word lists: nodes == keys of the dict of sets, nodes <= pairs, equal iff first letters all differ")

# exhaustive: every list of up to 3 words from {a, b, ab, ba, bb, aab}
pool = ["a", "b", "ab", "ba", "bb", "aab"]
for k in (1, 2, 3):
    for ws in itertools.product(pool, repeat=k):
        n, _, p, dct = trie_numbers(list(ws))
        assert n <= p and ((n == p) == (len({w[0] for w in set(ws)}) == dct))
print("exhaustive small lists ok")


# sandbox measurement (this machine and Python version only): shallow sys.getsizeof sums, NOT a proof of anything
def sizes(ws):
    distinct = set(ws)
    root = {}
    node_dicts = [root]
    for w in distinct:
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                node_dicts.append(node[ch])
            node = node[ch]
    trie_dict = sum(sys.getsizeof(d) for d in node_dicts)
    trie_arr = len(node_dicts) * sys.getsizeof([None] * 26)
    plain_set = sys.getsizeof(distinct) + sum(sys.getsizeof(w) for w in distinct)
    dos = {}
    for w in distinct:
        for i in range(1, len(w) + 1):
            dos.setdefault(w[:i], set()).add(w)
    dict_sets = sys.getsizeof(dos) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in dos.items()) \
        + sum(sys.getsizeof(w) for w in distinct)
    return trie_dict, trie_arr, plain_set, dict_sets


print("sandbox sizes, Python", sys.version.split()[0], "(bytes: trie of dicts, trie of 26-lists, plain set, dict of sets)")
for name, ws in [("5000 random words, len 1-20 over 'abcdefghij'",
                  ["".join(random.choice("abcdefghij") for _ in range(random.randint(1, 20))) for _ in range(5000)]),
                 ("5000 words 'internationalisation' + 4 letters over 'ab'",
                  ["internationalisation" + "".join(random.choice("ab") for _ in range(4)) for _ in range(5000)])]:
    r = trie_numbers(ws)
    print(" ", name, "-> [nodes, slots26, pairs, distinct] =", r, "| sizes", sizes(ws))

assert trie_numbers(["a" * 20] * 5000) == [20, 26 * 21, 20, 1]
print("edge asserts ok")
```

**Output (my run):**
```
insert 'car'   new nodes: ['c', 'ca', 'car']
insert 'cart'  new nodes: ['cart']
insert 'cat'   new nodes: ['cat']
insert 'do'    new nodes: ['d', 'do']
insert 'dog'   new nodes: ['dog']
nodes = 8 (the distinct non-empty prefixes)
['car', 'cart', 'cat', 'dog', 'do', 'car'] -> [8, 234, 15, 5]
['a', 'b', 'c'] -> [3, 104, 3, 3]
['aaa'] -> [3, 104, 3, 1]
['ab', 'ac'] -> [3, 104, 4, 2]
1500 seeded random word lists: nodes == keys of the dict of sets, nodes <= pairs, equal iff first letters all differ
exhaustive small lists ok
sandbox sizes, Python 3.13.17 (bytes: trie of dicts, trie of 26-lists, plain set, dict of sets)
  5000 random words, len 1-20 over 'abcdefghij' -> [nodes, slots26, pairs, distinct] = [38952, 1012778, 52379, 4582] | sizes (6683920, 10283592, 371529, 12348642)
  5000 words 'internationalisation' + 4 letters over 'ab' -> [nodes, slots26, pairs, distinct] = [50, 1326, 384, 16] | sizes (7464, 13464, 1768, 27646)
edge asserts ok
```

**Edge cases:**
- Repeated words: counted once in all four numbers.
- A word that is a prefix of another (`do`, `dog`): the shorter word adds no new nodes after the longer one is there, but it still adds its own `len` to `pairs`.
- One word of length 20: `nodes = 20`, `pairs = 20`, equal (no sharing possible).
- Single-letter distinct words (`a, b, c`): `nodes = pairs = 3`, `slots26 = 104`.
- Same word 5,000 times: `[20, 546, 20, 1]` for a 20-letter word.
- 5,000 words of 20 letters, no sharing: up to 10^5 nodes, `slots26` up to 2.6 million slots.

**Follow-ups:**
- *Compact the trie?* A radix (compressed) tree stores a chain of single-child nodes as one edge with a string; it cuts the node count for sparse sets. Concept only here.
- *Where does the trie fit?* Part 7 Q41 builds it at concept level, Part 3 Q36 compares it with a sorted list for prefix counts, and the full API is Q3.
- *Which would you use for autocomplete?* A trie (or a sorted array plus binary search for a static list); the dict of sets is a memory-hungry alternative and fine for small dictionaries.

**Common mistakes:**
- Counting the root as a node, or forgetting the root's array in `slots26`.
- Counting repeated words twice in `pairs`.
- Presenting `sys.getsizeof` totals as proof, or comparing them across Python versions.
- Saying "a trie saves memory" without the condition (shared prefixes).
- Storing the whole word at the end node of every trie node (that is the dict of sets again).

### Q34 ⭐ 🟡 A minimal skip list (concept level). Implement an ordered set of integers as a skip list with up to 16 levels in which a new node gets level 1, and each further level with probability 1/2 (use a seeded `random.Random`). `ops` is a list (1 <= len <= 2000) of `['insert', x]` (True if x was absent and is now inserted, False if already present), `['contains', x]` and `['remove', x]` (True if x was present and is removed, False otherwise), with |x| <= 10^6. Return the list of results. Describe how a search starts at the top level and drops down, why the expected cost is O(log n) per operation with random levels and O(n) in the worst case, and why the results never depend on the random choices (only the speed does). Say one real use (an ordered in-memory index, for instance a sorted-set structure) and why a balanced tree is the alternative; do not build the whole data store. This is a concept-level question; the Bloom filter is Part 1 Q42 and the LRU idea is Part 6 Q30. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Python set tracked next to the skip list on small inputs. Example: ops=[['insert', 3], ['insert', 1], ['contains', 3], ['remove', 3], ['contains', 3], ['insert', 1]] -> [True, True, True, True, False, False]; ops=[['remove', 5]] -> [False]; ops=[['insert', -2], ['insert', -2], ['remove', -2], ['remove', -2]] -> [True, False, True, False].
**Asked at:** Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Skip list (concept level): a sorted linked list with extra "express" levels chosen at random, giving expected O(log n) search without rotations.

**Say this first (1 line):** "Level 0 is a sorted linked list of every key; each higher level is a random sample of the level below, so a search starts at the top, moves right while the next key is smaller, drops down a level, and repeats."

**Brute force:** A Python `set` (the oracle in the code) gives the same results in O(1) average per operation but has no order. A sorted list with `bisect` has O(log n) search but O(n) insert and remove. A plain sorted linked list is O(n) for everything.

**Optimal:** The skip list:
- Node: a key and a list `next` with one pointer per level it belongs to. A head sentinel has all 16 levels.
- Level choice: a new node starts at level 1 and gets one more level per fair coin flip (`rng.random() < 0.5`), up to 16. So about half of the nodes reach level 2, a quarter level 3, and so on.
- Search (`_path`): start at the head on the top level; while the next key on this level is less than `x`, step right; then drop to the level below, keeping the node you stand on. Record the last node before `x` on every level (`update`). At the bottom, the next node is either `x` or something larger.
- `contains(x)`: look at the next node on level 0. `insert(x)`: if it is already there return False; otherwise draw a level and splice the new node after `update[i]` on each of its levels. `remove(x)`: if the node is not there return False, otherwise unlink it on each of its levels using `update[i]`.
- Why expected O(log n): going from the bottom up, a node that has a higher level appears about every 2nd step on the level below, so you walk an expected O(1) steps per level, and with n keys about log2(n) levels are used. In my run, 2,000 sorted keys took about 11 steps per lookup on average with random levels, against about 1,000 when I forced every level to 1 (a plain list); that is one run, an illustration, not a proof.
- Why O(n) in the worst case: the levels are random, so with bad luck (all nodes at level 1, shown below) the structure is a plain linked list and a search walks the whole bottom level.
- Why the results never depend on the random choices: the bottom level always holds exactly the current set of keys in order, whatever the levels are; the levels only decide how many steps it takes to find a place. The code checks that 6 different seeds and forced levels of 1 and 16 give the same results as a set on 300 random operation lists.
- One real use: an ordered in-memory index (a sorted-set structure in a database or cache, for instance) where you need ordered range scans and fast insert. The alternative is a balanced tree (red-black, AVL): O(log n) worst case but rotations are harder to write and to make lock-free; the skip list is simpler to implement and to extend with concurrency, at the price of randomness and about two pointers per node on average.
- Concept scope: no deletion of empty levels, no range queries, no persistence; the Bloom filter is Part 1 Q42 and the LRU idea is Part 6 Q30.

**Complexity:** Expected O(log n) time per operation with n keys (random levels), O(n) in the worst case (all nodes at level 1, or a very unlucky run). Space O(n) expected (about 2 pointers per node on average because the expected level is 2), plus the 16-pointer head.

**Dry run:** `ops = [insert 3, insert 1, contains 3, remove 3, contains 3, insert 1]` with seed 7. The levels printed after each operation (bottom first):
- `insert 3`: True, the tower of 3 has level 3: levels `[[3], [3], [3]]`.
- `insert 1`: True, 1 gets level 2: bottom `[1, 3]`, level 1 `[1, 3]`, level 2 `[3]`. Search for 1 goes from the head at the top level, sees 3 is not smaller than 1, drops, drops, and splices.
- `contains 3`: True. Levels 3 to 15 of the head are empty, so the walk really starts at the top non-empty level (level 2 in 0-based numbering): the next key is 3, not smaller than 3, drop to level 1, next key is 1 < 3, step to 1, then 3 is not smaller, drop to level 0, the next node is 3: found.
- `remove 3`: True, the node is unlinked on all its levels: `[[1], [1]]`.
- `contains 3`: False. `insert 1`: False (already there). Result `[True, True, True, True, False, False]`, as in the prompt.

**Code:**
```python
import random

MAX_LEVEL = 16


class Node:
    __slots__ = ("key", "next")

    def __init__(self, key, level):
        self.key = key
        self.next = [None] * level          # next[i] = successor on level i (0 = bottom, holds every key)


class SkipList:
    """Ordered set of ints. A new node gets level 1, plus one more level per fair coin flip, up to 16."""

    def __init__(self, seed=0, level_fn=None):
        self.rng = random.Random(seed)
        self.level_fn = level_fn             # test hook: force levels (e.g. always 1 = plain linked list)
        self.head = Node(None, MAX_LEVEL)    # sentinel with all 16 levels
        self.steps = 0                       # nodes stepped onto while searching (for the O(log n) vs O(n) demo)

    def _random_level(self):
        if self.level_fn:
            return self.level_fn()
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < 0.5:
            lvl += 1
        return lvl

    def _path(self, x):
        """Start on the top level, move right while the next key is < x, then drop one level. Returns the
        last node before x on every level."""
        update = [None] * MAX_LEVEL
        cur = self.head
        for i in range(MAX_LEVEL - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].key < x:
                cur = cur.next[i]
                self.steps += 1
            update[i] = cur
        return update

    def contains(self, x):
        nxt = self._path(x)[0].next[0]
        return nxt is not None and nxt.key == x

    def insert(self, x):
        update = self._path(x)
        nxt = update[0].next[0]
        if nxt is not None and nxt.key == x:
            return False
        node = Node(x, self._random_level())
        for i in range(len(node.next)):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node
        return True

    def remove(self, x):
        update = self._path(x)
        node = update[0].next[0]
        if node is None or node.key != x:
            return False
        for i in range(len(node.next)):
            update[i].next[i] = node.next[i]
        return True

    def levels(self):
        """Keys on each level, bottom first, for printing."""
        out = []
        for i in range(MAX_LEVEL):
            row, cur = [], self.head.next[i]
            while cur is not None:
                row.append(cur.key)
                cur = cur.next[i]
            if not row:
                break
            out.append(row)
        return out


def run(ops, seed=0, level_fn=None):
    sl = SkipList(seed, level_fn)
    return [getattr(sl, name)(x) for name, x in ops], sl


def brute(ops):
    s, out = set(), []
    for name, x in ops:
        if name == "insert":
            out.append(x not in s)
            s.add(x)
        elif name == "contains":
            out.append(x in s)
        else:
            out.append(x in s)
            s.discard(x)
    return out


# dry run, first example, with the tower shape after every op
ex = [["insert", 3], ["insert", 1], ["contains", 3], ["remove", 3], ["contains", 3], ["insert", 1]]
sl = SkipList(seed=7)
for name, x in ex:
    r = getattr(sl, name)(x)
    print(f"{name:8} {x}: {r!s:5} levels (bottom first): {sl.levels()}")

for ops, want in [(ex, [True, True, True, True, False, False]), ([["remove", 5]], [False]),
                  ([["insert", -2], ["insert", -2], ["remove", -2], ["remove", -2]], [True, False, True, False])]:
    got, _ = run(ops)
    assert got == want == brute(ops), (ops, got)
    print(ops, "->", got)

# results never depend on the coin flips: seeds 0..5 and forced levels (all 1, all 16) agree with a set
random.seed(3401)
for _ in range(300):
    ops = [[random.choice(["insert", "contains", "remove"]), random.randint(-12, 12)] for _ in range(random.randint(1, 60))]
    want = brute(ops)
    for seed in range(6):
        assert run(ops, seed)[0] == want
    assert run(ops, level_fn=lambda: 1)[0] == want and run(ops, level_fn=lambda: 16)[0] == want
    lv = run(ops)[1].levels()
    assert not lv or lv[0] == sorted(set(lv[0])), "bottom level is sorted, no repeats"
print("300 seeded random op lists: same results for 6 seeds and for forced level 1 and 16, equal to a set")

# speed depends on the levels: 2000 inserts in increasing order, then 2000 lookups
keys = list(range(2000))
for name, fn in [("random levels", None), ("all level 1 (a sorted linked list)", lambda: 1)]:
    sl = SkipList(seed=1, level_fn=fn)
    for k in keys:
        sl.insert(k)
    sl.steps = 0
    for k in keys:
        sl.contains(k)
    print(f"{name}: average nodes stepped onto per lookup = {sl.steps / len(keys):.1f}")

# edge asserts
sl = SkipList()
assert sl.insert(0) and not sl.insert(0) and sl.contains(0) and sl.remove(0) and not sl.remove(0) and not sl.contains(0)
assert all(sl.insert(x) for x in (10**6, -10**6, 0)) and sl.levels()[0] == [-10**6, 0, 10**6]
print("edge asserts ok")
```

**Output (my run):**
```
insert   3: True  levels (bottom first): [[3], [3], [3]]
insert   1: True  levels (bottom first): [[1, 3], [1, 3], [3]]
contains 3: True  levels (bottom first): [[1, 3], [1, 3], [3]]
remove   3: True  levels (bottom first): [[1], [1]]
contains 3: False levels (bottom first): [[1], [1]]
insert   1: False levels (bottom first): [[1], [1]]
[['insert', 3], ['insert', 1], ['contains', 3], ['remove', 3], ['contains', 3], ['insert', 1]] -> [True, True, True, True, False, False]
[['remove', 5]] -> [False]
[['insert', -2], ['insert', -2], ['remove', -2], ['remove', -2]] -> [True, False, True, False]
300 seeded random op lists: same results for 6 seeds and for forced level 1 and 16, equal to a set
random levels: average nodes stepped onto per lookup = 10.9
all level 1 (a sorted linked list): average nodes stepped onto per lookup = 999.5
edge asserts ok
```

**Edge cases:**
- `remove` of an absent key: False and no change (`[['remove', 5]]` gives `[False]`).
- Duplicate insert: False and the structure is unchanged.
- Negative keys and keys up to 10^6 in absolute value: only `<` and `==` are used.
- Empty list: the head's pointers are all None; `contains` is False.
- A key that is the new minimum or maximum: `update[i]` is the head on every level for the minimum; the next pointer is None for the maximum.
- Level 16 cap: with up to 2,000 operations the cap is never the limit; it only bounds the head size.

**Follow-ups:**
- *What probability would you choose?* 1/2 is fine; 1/4 gives fewer pointers per node with slightly longer walks; the expected search cost stays O(log n).
- *Why not a balanced tree?* The tree has a worst-case guarantee; the skip list has an expected one, but is easier to code and to make lock-free for concurrent use.
- *Can I use it to get the k-th element?* Not without storing span lengths in the pointers (an "indexable" skip list); not in this question.

**Common mistakes:**
- Not keeping the `update` array, so you cannot splice on the higher levels.
- Forgetting to check whether the key is already present before inserting (duplicates get stored).
- Stepping right on `<=` instead of `<` (you overshoot the position to insert after).
- Saying the worst case is O(log n): it is expected, not worst-case.
- Depending on the random values in the results (a test that compares the levels instead of the answers).

### Q35 ⭐ 🔴 Expression add operators. `num` is a string of 1 to 8 digits and `target` is an integer with |target| <= 10^9. Insert the binary operators '+', '-' and '*' (or nothing, which joins digits into one multi-digit operand) between the digits so that the expression, evaluated with the usual precedence (multiplication first), equals `target`. An operand may not have a leading zero ('0' alone is fine; '05' and '00' are not). Return every such expression as a string, sorted ascending as Python strings, without duplicates; return an empty list if none exists. Recurse over the cut position while carrying the value so far and the last term, and for '*' use `value - last + last * operand` to undo the last addition; explain why that works and why the carried value avoids re-parsing the string at every leaf. State the upper bound of 4^(n-1) candidate fillings (each of the n - 1 gaps gets '+', '-', '*' or nothing), of which the leading-zero rule removes some. Depth is at most 8. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all 4^(n-1) fillings and evaluating each with `eval` on small inputs. Example: num='2345', target=25 -> ['2+3+4*5']; num='105', target=5 -> ['1*0+5', '10-5']; num='00', target=0 -> ['0*0', '0+0', '0-0']; num='9', target=9 -> ['9']; num='9', target=0 -> [].
**Asked at:** Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Backtracking over cut positions with a carried value: choose the next operand (a cut), choose the operator before it, recurse, and undo by returning. The trick is carrying `(value, last)` so `*` can fix up precedence without re-parsing.

**Say this first (1 line):** "At each position I choose how many digits the next operand takes and which operator goes before it; I carry the running value and the last term, and for `*` I use `value - last + last * operand` to take the last term back out and put it back multiplied."

**Brute force:** For all `4^(n-1)` fillings of the `n - 1` gaps with `''`, `'+'`, `'-'`, `'*'`, build the string, drop it if any operand has a leading zero, `eval` it, and keep it when it equals `target`. Correct, and the oracle here (n <= 6 in the cross-check). It builds and parses 16,384 strings for n = 8.

**Optimal:**
- Recursion `dfs(i, expr, val, last)`: `i` is the next unused digit, `expr` the string so far, `val` the value of the expression so far under the usual precedence, `last` the signed last term (the one a following `*` would multiply).
- First operand: no operator before it; `val = last = int(tok)`.
- Later operands, `tok = num[i:j]`, `v = int(tok)`:
  - `+`: `val + v`, `last = v`.
  - `-`: `val - v`, `last = -v` (the subtracted term is the last term with sign).
  - `*`: `val - last + last * v`, `last = last * v`. Why it works: `val` already contains `last` added in, so remove it, then add `last * v`. Multiplication binds tighter, so it applies to the last term only. Example: `1-2*3`: after `1-2` we have `val = -1`, `last = -2`, so `-1 - (-2) + (-2) * 3 = -5 = 1 - 6`.
- Why carry the value: each leaf already has its value, so nothing is re-parsed or evaluated at the leaves; the brute force pays for an `eval` of a whole string per filling.
- Pruning rule (the only one used): an operand may not have a leading zero. When `num[i] == '0'` and the operand is longer than one digit, `break`: `'05'`, `'050'` and every longer operand from that start are illegal. A single `'0'` is fine.
- Undo: strings and numbers are passed by value, so returning from a call is the undo; nothing has to be restored.
- Output: collect leaves with `val == target`, then `sorted(...)`; each filling yields a different string, so there are no duplicates (the code asserts it). If none matches the list is empty.
- Node count compared with the unpruned search: the unpruned search has `4^(n-1)` fillings, 16,384 for n = 8, and `21,846` recursion calls in all. With the leading-zero rule the calls fall to 21,846 for `12345678` (no zeros, nothing to prune), 11,901 for `10203040`, 4,917 for `10000000` and 3,281 for `00000000`. The valid fillings are 16,384, 8,788, 3,280 and 2,187. So the rule never changes the bound, it only helps on inputs with zeros (see the table in the output).
- Depth: at most `n = 8` frames.
- No target-based pruning is used: with `*` the value can swing back (`9*9*9*0`), so a "too large already" cut would be wrong.

**Complexity:** Upper bound `4^(n-1)` leaves (each gap `+`, `-`, `*` or nothing); the leading-zero rule removes some. Each call does O(n) work (slicing and `int` on the operand, string concatenation), so about O(n * 4^(n-1)) worst case. For n = 8 that is about 22,000 calls. Space O(n) depth plus the output.

**Dry run:** `num = '105'`, `target = 5`. The tree is printed below (19 calls). Operands from index 0: `1`, `10`, `105`.
- `1`, then `0` with `+`, `-` or `*` (values `1`, `1`, and `1 - 1 + 1 * 0 = 0`), then `5` with each of the three operators: after `1+0` the totals are 6, -4 and 1; after `1-0` they are 6, -4 and 1; after `1*0` they are 5, -5 and 0. Only `1*0+5` equals 5 (HIT).
- `10`, then `5`: `10+5 = 15`, `10-5 = 5` (HIT), `10*5 = 50`.
- `105` alone: 105.
- No `'05'` operand ever appears: after `1`, a join of `0` and `5` is `05`, which is cut by the rule. Hits sorted: `['1*0+5', '10-5']`.

**Code:**
```python
import itertools
import random
import re

random.seed(3501)


def solve(num, target, zero_rule=True, trace=None):
    """Returns (sorted expressions, calls). calls counts every dfs call. zero_rule=False only exists
    to measure what the leading-zero rule prunes (its answers then include illegal operands)."""
    n = len(num)
    out = []
    calls = 0

    def dfs(i, expr, val, last, depth):
        nonlocal calls
        calls += 1
        if trace is not None:
            trace.append("  " * depth + f"i={i} expr={expr or '-'} val={val} last={last}" + (" HIT" if i == n and val == target else ""))
        if i == n:
            if val == target:
                out.append(expr)
            return
        for j in range(i + 1, n + 1):                 # operand = num[i:j]
            tok = num[i:j]
            if zero_rule and len(tok) > 1 and tok[0] == "0":
                break                                 # '0x...' and every longer operand starting here are illegal
            v = int(tok)
            if i == 0:
                dfs(j, tok, v, v, depth + 1)
            else:
                dfs(j, expr + "+" + tok, val + v, v, depth + 1)
                dfs(j, expr + "-" + tok, val - v, -v, depth + 1)
                dfs(j, expr + "*" + tok, val - last + last * v, last * v, depth + 1)   # undo last term, redo it times v

    dfs(0, "", 0, 0, 0)
    return sorted(out), calls


def brute(num, target):
    out = []
    for ops in itertools.product(["", "+", "-", "*"], repeat=len(num) - 1):
        e = num[0] + "".join(o + d for o, d in zip(ops, num[1:]))
        if any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", e)):
            continue
        if eval(e) == target:                         # eval applies the usual precedence
            out.append(e)
    return sorted(out)


# dry run: decision tree for '105', target 5
tr = []
res, calls = solve("105", 5, trace=tr)
print("\n".join(tr))
print("answer", res, "| dfs calls", calls)

for num, tg, want in [("2345", 25, ["2+3+4*5"]), ("105", 5, ["1*0+5", "10-5"]), ("00", 0, ["0*0", "0+0", "0-0"]),
                      ("9", 9, ["9"]), ("9", 0, [])]:
    got = solve(num, tg)[0]
    assert got == want == brute(num, tg), (num, tg, got)
    print(repr(num), tg, "->", got)

# why value - last + last * v works: '1-2*3' -> val after '1-2' is -1, last is -2
assert eval("1-2*3") == -1 - (-2) + (-2) * 3 == -5

# node counts: with the leading-zero rule against without it, against the 4^(n-1) leaves of the unpruned filling space
print("n  digits      4^(n-1)  calls without rule  calls with rule  valid leaves")
for num in ["12345678", "10203040", "00000000", "10000000", "11111111"]:
    n = len(num)
    c_without = solve(num, 0, zero_rule=False)[1]
    c_with = solve(num, 0)[1]
    leaves = sum(1 for _ in itertools.product(["", "+", "-", "*"], repeat=n - 1)
                 if not any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", num[0] + "".join(o + d for o, d in zip(_, num[1:])))))
    print(f"{n}  {num}  {4 ** (n - 1):>7}  {c_without:>18}  {c_with:>15}  {leaves:>12}")

# seeded random cross-check against eval over all 4^(n-1) fillings
for _ in range(300):
    n = random.randint(1, 6)
    num = "".join(random.choice("0123456789" if random.random() < 0.5 else "0012") for _ in range(n))
    tg = random.choice([0, random.randint(-30, 100), eval(num[0] + "".join(random.choice("+-*") + d for d in num[1:]))])
    got = solve(num, tg)[0]
    assert got == brute(num, tg) and got == sorted(set(got)), (num, tg)
print("300 seeded random cases: same sorted list as the eval enumeration, no duplicates")
assert solve("0", 0)[0] == ["0"] and solve("05", 5)[0] == ["0+5"] and solve("05", 0)[0] == ["0*5"] and solve("00", 0)[0] == ["0*0", "0+0", "0-0"]
assert solve("12345678", 10**9)[0] == [] and solve("99999999", 99999999)[0] == ["99999999"]
print("edge asserts ok")
```

**Output (my run):**
```
i=0 expr=- val=0 last=0
  i=1 expr=1 val=1 last=1
    i=2 expr=1+0 val=1 last=0
      i=3 expr=1+0+5 val=6 last=5
      i=3 expr=1+0-5 val=-4 last=-5
      i=3 expr=1+0*5 val=1 last=0
    i=2 expr=1-0 val=1 last=0
      i=3 expr=1-0+5 val=6 last=5
      i=3 expr=1-0-5 val=-4 last=-5
      i=3 expr=1-0*5 val=1 last=0
    i=2 expr=1*0 val=0 last=0
      i=3 expr=1*0+5 val=5 last=5 HIT
      i=3 expr=1*0-5 val=-5 last=-5
      i=3 expr=1*0*5 val=0 last=0
  i=2 expr=10 val=10 last=10
    i=3 expr=10+5 val=15 last=5
    i=3 expr=10-5 val=5 last=-5 HIT
    i=3 expr=10*5 val=50 last=50
  i=3 expr=105 val=105 last=105
answer ['1*0+5', '10-5'] | dfs calls 19
'2345' 25 -> ['2+3+4*5']
'105' 5 -> ['1*0+5', '10-5']
'00' 0 -> ['0*0', '0+0', '0-0']
'9' 9 -> ['9']
'9' 0 -> []
n  digits      4^(n-1)  calls without rule  calls with rule  valid leaves
8  12345678    16384               21846            21846         16384
8  10203040    16384               21846            11901          8788
8  00000000    16384               21846             3281          2187
8  10000000    16384               21846             4917          3280
8  11111111    16384               21846            21846         16384
300 seeded random cases: same sorted list as the eval enumeration, no duplicates
edge asserts ok
```

**Edge cases:**
- `'00'`, target 0: `['0*0', '0+0', '0-0']`; `'00'` joined is illegal.
- `'05'`, target 5: only `'0+5'` (`'05'` is illegal, `0-5` is -5, `0*5` is 0).
- One digit: `'9'` with 9 gives `['9']`; with 0 gives `[]`.
- Negative or large targets: `'12345678'` and 10^9 gives `[]`; the values stay far below 10^9 anyway.
- All same digits (`'99999999'`): the single join `99999999` matches itself.
- Overflow: Python ints do not overflow. Every term is below 10^8 (its digits are a subset of 8), so the sum of at most 8 terms stays below 8 * 10^8, inside 32 bits anyway.

**Follow-ups:**
- *Add parentheses or division?* The `value - last + last * v` trick no longer works; a recursion over split points returning a set of possible values per substring would be the approach.
- *How slow is the worst input?* About 22,000 calls for 8 digits, instant; the `4^(n-1)` growth only matters for longer strings.
- *Why `last = -v` for minus?* So that a following `*` multiplies the negative term: `1-2*3` is `1 - (2*3)`.

**Common mistakes:**
- Evaluating `'*'` as `val * v` (applies to the whole prefix, wrong precedence).
- Forgetting the sign in `last` after `-`.
- Allowing `'05'`, or breaking out of the whole recursion instead of just the operand loop when seeing a zero.
- Putting an operator before the first operand.
- Returning the list unsorted or with duplicates when the prompt asks for sorted and distinct.

