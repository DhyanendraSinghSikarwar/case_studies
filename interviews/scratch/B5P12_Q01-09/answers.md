# Book 5 Part 12, answers Q1-Q9 (Wave B)

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
