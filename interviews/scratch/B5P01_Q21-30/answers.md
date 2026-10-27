### Q21 ⭐⭐ 🟢 Remove element in place. Given list `nums` and a value `val`, remove all occurrences in place and return the new length k, the first k slots holding the kept values in any order. Give the order-preserving write-pointer version and the swap-from-the-end version that does fewer writes when matches are rare. Example: nums=[3,2,2,3], val=3 -> k=2, prefix [2,2].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Read/write pointers (in-place filtering). One pass decides what to keep; a second index decides where it goes. The array is the output.

**Say this first (1 line):** "Walk once, copy every value that is not `val` to the write slot, return the write count; if matches are rare I swap each match with the last live value instead, so I write only once per match."

**Brute force:** Build a new list with a comprehension and copy it back. O(n) time, O(n) extra space. It fails the "in place" ask and the extra list is the whole cost.

**Optimal:** Two versions.
- **Order-preserving write pointer:** `w` is the next free slot. For each `x`, if `x != val`, write `nums[w] = x; w += 1`. Invariant: `nums[:w]` holds the kept values seen so far, in order.
- **Swap from the end:** keep `n` as the live length. If `nums[i] == val`, overwrite it with `nums[n-1]` and shrink `n`. Do not advance `i`, because the value that came in is unchecked. Invariant: `nums[:i]` has no `val`, and `nums[n:]` is dead. Order changes, which the question allows.

**Complexity:**
- Both are O(n) time and O(1) space.
- Writes differ. Write pointer writes once per kept value. Swap writes once per match. So swap wins when matches are rare, write pointer wins when almost everything matches.
- Swap does at most n steps because each step either advances `i` or shrinks `n`.

**Dry run:** `[3,2,2,3]`, `val=3`, swap version.
| step | i | n | array | action |
|---|---|---|---|---|
| 1 | 0 | 4 | [3,2,2,3] | match: nums[0]=nums[3]=3, n=3 |
| 2 | 0 | 3 | [3,2,2,3] | match again: nums[0]=nums[2]=2, n=2 |
| 3 | 0 | 2 | [2,2,2,3] | keep, i=1 |
| 4 | 1 | 2 | [2,2,2,3] | keep, i=2, stop |

Result: k=2, prefix `[2,2]`. Note step 2: the swapped-in value was 3 and had to be rechecked.

The prompt's example is correct, and my run confirms k=2 with prefix [2,2] for both versions.

**Code:**
```python
import random


def remove_brute(nums, val):
    """Build a new list of kept values (extra O(n) space)."""
    return [x for x in nums if x != val]


def remove_stable(nums, val):
    """Write pointer: keeps order. Returns (k, writes)."""
    w = 0
    writes = 0
    for x in nums:
        if x != val:
            nums[w] = x
            w += 1
            writes += 1
    return w, writes


def remove_swap(nums, val):
    """Overwrite a match with the last live value. Order changes.
    Returns (k, writes). Writes == number of matches."""
    i, n = 0, len(nums)
    writes = 0
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1
            writes += 1
            # do NOT advance i: the swapped-in value is unchecked
        else:
            i += 1
    return n, writes


# --- the example from the prompt
a = [3, 2, 2, 3]
k, _ = remove_stable(a, 3)
print("stable  [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and a[:k] == [2, 2]
a = [3, 2, 2, 3]
k, _ = remove_swap(a, 3)
print("swap    [3,2,2,3] val=3 ->", k, a[:k])
assert k == 2 and sorted(a[:k]) == [2, 2]

# --- writes: rare matches
big = list(range(1, 11))          # one match, at the front
s1, s2 = big[:], big[:]
k1, w1 = remove_stable(s1, 1)
k2, w2 = remove_swap(s2, 1)
print("rare match  : stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (9, 1)
# many matches: swap does more writes than stable when matches dominate
mostly = [7] * 9 + [1]
s1, s2 = mostly[:], mostly[:]
k1, w1 = remove_stable(s1, 7)
k2, w2 = remove_swap(s2, 7)
print("many matches: stable writes =", w1, " swap writes =", w2)
assert (w1, w2) == (1, 9)

# --- edge cases
for nums, val in [([], 1), ([1], 1), ([1], 2), ([2, 2, 2], 2),
                  ([2, 2, 2], 3), ([0, 0, 1], 0), ([-1, -1, 5], -1)]:
    want = remove_brute(nums, val)
    a = nums[:]
    k, _ = remove_stable(a, val)
    assert a[:k] == want
    a = nums[:]
    k, _ = remove_swap(a, val)
    assert sorted(a[:k]) == sorted(want)
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(21)
for _ in range(1000):
    n = rng.randint(0, 12)
    nums = [rng.randint(-3, 3) for _ in range(n)]
    val = rng.randint(-3, 3)
    want = remove_brute(nums, val)
    a = nums[:]
    k, wr = remove_stable(a, val)
    assert k == len(want) and a[:k] == want
    a = nums[:]
    k, wr = remove_swap(a, val)
    assert k == len(want) and sorted(a[:k]) == sorted(want)
    assert wr == nums.count(val)
print("1000 random cases OK")
```

**Output (my run):**
```
stable  [3,2,2,3] val=3 -> 2 [2, 2]
swap    [3,2,2,3] val=3 -> 2 [2, 2]
rare match  : stable writes = 9  swap writes = 1
many matches: stable writes = 1  swap writes = 9
edge cases OK
1000 random cases OK
```

**Edge cases:**
- Empty list: k=0.
- No match: nothing changes, k=n.
- All match: k=0.
- `val` equal to the last element: the swap copies a value onto itself, harmless.
- Negative values and 0 are ordinary values.

**Follow-ups:**
- *Why not advance `i` after a swap?* The value copied in from the end has not been tested yet.
- *Which do you ship?* The write pointer: simple and stable. Use the swap when order is free and matches are rare.
- *What if the array is huge and the matches are few?* Swap, since writes can cost more than reads (flash, copy-on-write pages).

**Common mistakes:**
- Using `nums.remove(val)` in a loop, or `del` / `pop(i)` in a loop. Each is O(n), so the total is O(n^2).
- Advancing `i` after a swap, which skips the value just moved in.
- Returning the list instead of k, or checking beyond the first k slots.

### Q22 ⭐⭐ 🟢 Merge sorted array in place. `a` has length m+n where the first m slots are sorted values and the last n are zeros as placeholders; `b` is a sorted list of n values. Merge b into a in place in O(m+n) time by filling from the back and explain why filling from the front fails. Example: a=[1,2,3,0,0,0], m=3, b=[2,5,6], n=3 -> [1,2,2,3,5,6].
**Asked at:** Indian placement and online-assessment prep sheets (a TCS NQT coding sheet on GitHub, Scribd 'Array Patterns' and TCS NQT Python guides, a Scribd interview preparation guide tagging rotate-array and non-repeating-element tasks to IT-services firms; snippets only, not opened; company tags in these documents contradict each other, so treat as indicative only) | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Two pointers from the back (merge in place). The free space is at the end, so the largest values go there first and nothing unread is overwritten.

**Say this first (1 line):** "I fill `a` from the back: compare the last live value of `a` with the last of `b`, put the larger at the last free slot, and move that pointer left; this never overwrites an unread `a` value."

**Brute force:** Copy `a[:m]` and `b`, concatenate, sort, write back. O((m+n) log(m+n)) time, O(m+n) space. It ignores the fact that both inputs are already sorted.

**Optimal:** Pointers `i = m-1` (last live in `a`), `j = n-1` (last in `b`), `w = m+n-1` (write slot).
- Take the larger of `a[i]` and `b[j]`, write it at `w`, move that pointer and `w` left.
- Loop while `j >= 0`. When `b` is used up, what is left of `a` is already in the right place.
- Invariant: `a[w+1:]` holds the largest values in final order, and `w >= i` always, so a write never lands on an unread `a` value. The gap between `w` and `i` is exactly the number of `b` values still unplaced.

**Why the front fails:** Writing at slot 0 overwrites `a[0]`, `a[1]`, ... before they are read. To go from the front you would need to shift `a` right or copy it, which is extra space or O(n^2). From the back, the free slots are exactly the zeros.

**Complexity:** O(m+n) time, each step moves one pointer. O(1) extra space.

**Dry run:** `a=[1,2,3,0,0,0]`, `b=[2,5,6]`.
| step | i | j | w | compare | write |
|---|---|---|---|---|---|
| 1 | 2 | 2 | 5 | 3 vs 6 | a[5]=6 |
| 2 | 2 | 1 | 4 | 3 vs 5 | a[4]=5 |
| 3 | 2 | 0 | 3 | 3 vs 2 | a[3]=3 |
| 4 | 1 | 0 | 2 | 2 vs 2 (not >) | a[2]=2 from b |
Then `j < 0`, stop. Array: `[1,2,2,3,5,6]`.

The prompt's example is correct. My run also shows a naive front-fill giving a wrong answer on it.

**Code:**
```python
import random


def merge_brute(a, m, b, n):
    """Extra-space version: sort the live parts, copy back."""
    merged = sorted(a[:m] + b)
    a[:] = merged
    return a


def merge_back(a, m, b, n):
    """Fill from the back. i: last live of a, j: last of b, w: write slot."""
    i, j, w = m - 1, n - 1, m + n - 1
    while j >= 0:                      # once b is used up, a's prefix is in place
        if i >= 0 and a[i] > b[j]:
            a[w] = a[i]
            i -= 1
        else:
            a[w] = b[j]
            j -= 1
        w -= 1
    return a


def merge_front_wrong(a, m, b, n):
    """Fill from the front in the same array: overwrites unread a values."""
    i, j = 0, 0
    a_copy_len = m
    for w in range(m + n):
        if j >= n or (i < a_copy_len and a[i] <= b[j]):
            a[w] = a[i]
            i += 1
        else:
            a[w] = b[j]
            j += 1
    return a


a = [1, 2, 3, 0, 0, 0]
print("back-fill  :", merge_back(a[:], 3, [2, 5, 6], 3))
assert merge_back(a[:], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
try:
    bad = merge_front_wrong(a[:], 3, [2, 5, 6], 3)
    print("front-fill :", bad, "(wrong)")
    assert bad != [1, 2, 2, 3, 5, 6]
except IndexError as e:
    print("front-fill : IndexError", e)

# --- edge cases
assert merge_back([0], 0, [1], 1) == [1]            # a empty
assert merge_back([1], 1, [], 0) == [1]             # b empty
assert merge_back([], 0, [], 0) == []               # both empty
assert merge_back([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3) == [1, 2, 3, 4, 5, 6]
assert merge_back([2, 2, 0, 0], 2, [2, 2], 2) == [2, 2, 2, 2]
assert merge_back([-3, -1, 0, 0], 2, [-2, -2], 2) == [-3, -2, -2, -1]
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(22)
for _ in range(1000):
    m, n = rng.randint(0, 8), rng.randint(0, 8)
    live = sorted(rng.randint(-5, 5) for _ in range(m))
    b = sorted(rng.randint(-5, 5) for _ in range(n))
    a1 = live + [0] * n
    a2 = live + [0] * n
    assert merge_back(a1, m, b, n) == merge_brute(a2, m, b, n)
print("1000 random cases OK")
```

**Output (my run):**
```
back-fill  : [1, 2, 2, 3, 5, 6]
front-fill : [1, 2, 2, 2, 5, 6] (wrong)
edge cases OK
1000 random cases OK
```

**Edge cases:**
- `m = 0`: all of `b` copies in.
- `n = 0`: `a` is already done, the loop never runs.
- All of `b` smaller than `a`: `a`'s values shift right one by one.
- All of `b` larger: `b` copies straight over the zeros.
- Duplicates: on a tie the code takes `b`'s value for the later slot, so equal values from `a` stay left of equal values from `b`.

**Follow-ups:**
- *Is it stable?* Yes. Filling from the back, a tie writes `b`'s value at the later slot, so `a`'s equal values stay before `b`'s.
- *What if there is no spare room?* Then you need a gap-method merge or a new list.
- *Linked lists?* Merging from the front is natural there; no trouble with overwriting.

**Common mistakes:**
- Merging from the front and clobbering `a`.
- Looping `while i >= 0 and j >= 0` and then forgetting to copy leftover `b`.
- Using `a[:] = sorted(...)` and calling it O(m+n).

### Q23 ⭐⭐ 🟡 Four sum count (4Sum II). Given four integer lists A, B, C, D each of length n (n <= 200), count tuples (i, j, k, l) with A[i]+B[j]+C[k]+D[l] == 0. Reduce to a two-sum over pair sums to get O(n^2) time and space instead of O(n^4). Example: A=[1,2], B=[-2,-1], C=[-1,2], D=[0,2] -> 2.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Meet in the middle with a hashmap (split a 4-way sum into two pair sums). Count what you need to find, then look it up.

**Say this first (1 line):** "Count every sum `a+b` in a Counter, then for every `c+d` add how many times `-(c+d)` was counted: O(n^2) instead of O(n^4)."

**Brute force:** Four nested loops (or `itertools.product`) testing the sum. O(n^4). For n=200 that is 1.6 billion tuples, too slow.

**Optimal:**
- Build `ab = Counter(a+b)` over all n^2 pairs.
- For each of the n^2 pairs `(c, d)`, add `ab[-(c+d)]`.
- The count of matching `(a, b)` pairs for one `(c, d)` is the number of tuples it completes, so the answer is the sum. Duplicates are handled for free because the Counter stores multiplicities.
- Use `.get(key, 0)` on the lookup, not `ab[key]` on a plain `defaultdict`, so the lookup does not insert keys.

**Complexity:** Time O(n^2) (n^2 inserts plus n^2 lookups, average O(1) each). Space O(n^2) for up to n^2 distinct sums: 40,000 at n=200, which is fine.

**Dry run:** `A=[1,2]`, `B=[-2,-1]`, `C=[-1,2]`, `D=[0,2]`.
- A+B sums: 1-2=-1, 1-1=0, 2-2=0, 2-1=1. Counter: {-1:1, 0:2, 1:1}.
- C+D sums: -1+0=-1 (need 1: count 1), -1+2=1 (need -1: count 1), 2+0=2 (need -2: 0), 2+2=4 (need -4: 0).
- Total = 1 + 1 = 2.

The prompt's example is correct (my run prints 2, and brute force agrees).

**Code:**
```python
import random
from collections import Counter
from itertools import product


def four_sum_brute(A, B, C, D):
    return sum(1 for a, b, c, d in product(A, B, C, D) if a + b + c + d == 0)


def four_sum_count(A, B, C, D):
    ab = Counter(a + b for a in A for b in B)      # O(n^2) time and space
    total = 0
    for c in C:
        for d in D:
            total += ab.get(-(c + d), 0)           # .get: no key inserted
    return total


A, B, C, D = [1, 2], [-2, -1], [-1, 2], [0, 2]
print("example:", four_sum_count(A, B, C, D))
assert four_sum_count(A, B, C, D) == 2 == four_sum_brute(A, B, C, D)

# --- edge cases
assert four_sum_count([0], [0], [0], [0]) == 1
assert four_sum_count([1], [1], [1], [1]) == 0
assert four_sum_count([0] * 5, [0] * 5, [0] * 5, [0] * 5) == 5 ** 4   # all equal
assert four_sum_count([-1, -1], [1, 1], [-1, -1], [1, 1]) == 16
assert four_sum_count([10 ** 9], [-10 ** 9], [10 ** 9], [-10 ** 9]) == 1  # no overflow
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(23)
for _ in range(500):
    n = rng.randint(1, 5)
    lists = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(4)]
    assert four_sum_count(*lists) == four_sum_brute(*lists)
print("500 random cases OK")

# --- size note: n=200 -> 40,000 pair sums stored, 40,000 lookups
n = 200
rng = random.Random(1)
big = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(n)] for _ in range(4)]
print("n=200 result runs fine, pair sums stored <=", n * n, "; n^4 =", n ** 4)
four_sum_count(*big)
```

**Output (my run):**
```
example: 2
edge cases OK
500 random cases OK
n=200 result runs fine, pair sums stored <= 40000 ; n^4 = 1600000000
```

**Edge cases:**
- All zeros: every tuple counts, n^4.
- No solution: 0.
- Big values: Python ints do not overflow.
- Unequal list lengths would also work with the same code.

**Follow-ups:**
- *Four sum (return the quadruples)?* A different problem: sort plus two pointers, O(n^3), with dedupe care.
- *Can you cut space?* Not easily; you can store only the smaller side, but both sides are n^2 here.
- *k lists?* Split in half: O(n^(k/2)) time and space.

**Common mistakes:**
- Using a set of sums, which loses multiplicity.
- Counting `(i, j)` pairs once and forgetting `(k, l)` multiplicity, or the reverse.
- Reading `defaultdict` on lookup and bloating memory.

### Q24 ⭐⭐ 🟡 Encode and decode a list of strings. Design `encode(strs) -> str` and `decode(s) -> list` so that any list of strings, including empty strings and strings containing your delimiter or digits, round-trips exactly. Use a length-prefix scheme and justify why a plain separator character is unsafe. Example: ['we','say',':','yes'] encodes to one string that decodes back to the same four items.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Length-prefix framing (a self-describing serialisation). It is a design question dressed as a hashing-section problem: the key idea is that the format must be unambiguous for every possible string.

**Say this first (1 line):** "I write each string as its length, a `#`, then the string itself; the decoder reads the length, then takes exactly that many characters without looking at them, so content can never be confused with structure."

**Brute force:** Join with a delimiter (a comma) and split on decode. It breaks as soon as a string contains the delimiter, and `[]` and `['']` both encode to `''`. Escaping the delimiter works but needs a careful two-sided scheme.

**Optimal:**
- `encode`: `"".join(f"{len(s)}#{s}" for s in strs)`.
- `decode`: from position `i`, find the next `#` (the length field is digits only, so the first `#` after `i` is ours), parse the number, slice exactly that many characters, jump `i` past them.
- Why it is safe: the decoder never inspects payload characters, only counts them. A payload `'3#abc'` or `'1#1#1'` is just data.
- `[]` encodes to `''`; `['']` encodes to `'0#'`. Different, so empty cases round-trip.

**Complexity:** Encode and decode are O(total characters). Space O(total characters) for the output. Each character is touched a constant number of times; `str.index` scans only the short length field.

**Dry run:** `['we','say',':','yes']` encodes to `2#we3#say1#:3#yes`.
Decode: i=0, `#` at 1, length 2, take `we`, i=4. `#` at 5, length 3, take `say`, i=9. `#` at 10, length 1, take `:`, i=13. Then length 3, `yes`. Done.

The prompt's example round-trips in my run, as the output shows.

**Code:**
```python
import random


def encode_naive(strs):
    return ",".join(strs)


def decode_naive(s):
    return s.split(",")


def encode(strs):
    """length + '#' + payload, concatenated."""
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)           # first '#' after i ends the length field
        length = int(s[i:j])          # digits only, so the first '#' is ours
        out.append(s[j + 1:j + 1 + length])   # take exactly `length` chars
        i = j + 1 + length            # jump over the payload unread
    return out


ex = ["we", "say", ":", "yes"]
enc = encode(ex)
print("encoded:", repr(enc))
print("decoded:", decode(enc))
assert decode(enc) == ex

# why a separator is unsafe
bad = ["a,b", "c"]
print("naive round trip of", bad, "->", decode_naive(encode_naive(bad)))
assert decode_naive(encode_naive(bad)) != bad
print("naive round trip of [] ->", decode_naive(encode_naive([])), "(wrong: one empty string)")
assert decode_naive(encode_naive([])) != []

# --- edge cases
for case in ([], [""], ["", ""], ["#"], ["3#abc"], ["12", "3"], ["0#"],
             ["a" * 1000], ["héllo", "日本語", "😀"], ["1#1#1"], ["\n", " "]):
    assert decode(encode(case)) == case, case
assert encode([]) == "" and encode([""]) == "0#"
print("edge cases OK")

# --- seeded randomised check (adversarial alphabet: digits, '#', ',', letters)
rng = random.Random(24)
alpha = "#0123456789,ab "
for _ in range(2000):
    strs = ["".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
            for _ in range(rng.randint(0, 6))]
    assert decode(encode(strs)) == strs
print("2000 random round trips OK")
```

**Output (my run):**
```
encoded: '2#we3#say1#:3#yes'
decoded: ['we', 'say', ':', 'yes']
naive round trip of ['a,b', 'c'] -> ['a', 'b', 'c']
naive round trip of [] -> [''] (wrong: one empty string)
edge cases OK
2000 random round trips OK
```

**Edge cases:**
- Empty list versus a list of one empty string.
- Strings that contain `#`, digits or newlines.
- Unicode: lengths count characters, so it works as long as encode and decode both use `str` (if you move to bytes, use byte lengths and keep it consistent).
- Very long strings: the length has more digits, still fine.

**Follow-ups:**
- *Over a network?* Encode to bytes and use a fixed-width length header (4 bytes), so you can read without scanning.
- *Why not JSON?* It is perfectly valid and the sane production answer; the interviewer usually wants you to build the framing yourself.
- *Escaping instead?* Works, but every delimiter and escape character must be handled, and the decoder is a state machine.

**Common mistakes:**
- Splitting on `'#'` in decode, which breaks on payloads that contain `#`.
- Parsing the length with a fixed single digit.
- Not handling `''` (length 0) strings.

### Q25 ⭐⭐ 🟡 Continuous subarray sum multiple of k. Given `nums` (non-negative) and an integer k, return True if some contiguous subarray of length at least 2 has a sum that is a multiple of k (0 counts). Store the first index of each prefix-sum remainder and explain why length at least 2 matters. Example: nums=[23,2,4,6,7], k=6 -> True (2+4); nums=[23,2,6,4,7], k=13 -> False.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Prefix sums with a remainder map (first-seen index). If two prefix sums leave the same remainder mod k, the stretch between them sums to a multiple of k.

**Say this first (1 line):** "Track the prefix sum mod k and store the first index where each remainder appeared; if I see a remainder again at least two positions later, the subarray between them has sum divisible by k."

**Brute force:** Try every start and extend the end, keeping a running sum, test `sum % k == 0` for lengths of at least 2. O(n^2) time, O(1) space.

**Optimal:**
- `prefix[i]` = sum of the first `i` values. Subarray `(a, b]` has sum `prefix[b] - prefix[a]`. It is a multiple of k exactly when both prefixes have equal remainders.
- Seed the map with `{0: -1}` so a prefix that is itself a multiple of k counts (the empty prefix "ends" at -1).
- At index `i`: compute `r = prefix % k`. If `r` is in the map and `i - first[r] >= 2`, return True. If `r` is not in the map, store `first[r] = i`. Never overwrite: the earliest index gives the longest span, the best chance of clearing length 2.
- **Why length at least 2 matters:** for `[6]` with k=6 the prefix remainder 0 repeats at index 0 with the seed at -1, giving a length-1 subarray. The check `i - first[r] >= 2` rejects it.
- **k = 0:** a multiple of 0 means sum exactly 0, so the key is the raw prefix sum (`p % k` would divide by zero). With non-negative values that means a run of zeros, which the same code handles.

**Complexity:** O(n) time, O(min(n, k)) space (at most k remainders).

**Dry run:** `[23,2,4,6,7]`, k=6.
| i | x | prefix | r | map | action |
|---|---|---|---|---|---|
| seed | | 0 | 0 | {0:-1} | |
| 0 | 23 | 23 | 5 | {0:-1,5:0} | store |
| 1 | 2 | 25 | 1 | +{1:1} | store |
| 2 | 4 | 29 | 5 | | seen at 0, 2-0=2 >= 2: True (subarray 2+4=6) |

The prompt's examples are correct: True for the first, False for `[23,2,6,4,7]`, k=13 (my run shows both).

**Code:**
```python
import random


def check_brute(nums, k):
    n = len(nums)
    for i in range(n):
        s = nums[i]
        for j in range(i + 1, n):          # length >= 2
            s += nums[j]
            if (s == 0) if k == 0 else (s % k == 0):
                return True
    return False


def check_hash(nums, k):
    first = {0: -1}                         # empty prefix "ends" at index -1
    p = 0
    for i, x in enumerate(nums):
        p += x
        r = p % k if k else p               # k == 0: need an equal prefix sum
        if r in first:
            if i - first[r] >= 2:           # length at least 2
                return True
        else:
            first[r] = i                    # keep the EARLIEST index only
    return False


print(check_hash([23, 2, 4, 6, 7], 6), check_hash([23, 2, 6, 4, 7], 13))
assert check_hash([23, 2, 4, 6, 7], 6) is True
assert check_hash([23, 2, 6, 4, 7], 13) is False

# --- why length >= 2 matters: without it, one element can qualify
print("[6], k=6 ->", check_hash([6], 6), "(a single 6 is a multiple but length 1)")
assert check_hash([6], 6) is False and check_hash([6, 0], 6) is True

# --- edge cases
assert check_hash([], 5) is False
assert check_hash([0], 1) is False
assert check_hash([0, 0], 1) is True
assert check_hash([0, 0], 0) is True          # k = 0: sum must be exactly 0
assert check_hash([1, 0], 0) is False
assert check_hash([5, 0, 0], 0) is True
assert check_hash([1, 2], 1) is True          # k = 1: every sum qualifies
assert check_hash([23, 2, 6, 4, 7], 6) is True    # whole array sums to 42
assert check_hash([1, 1], 3) is False
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(25)
for _ in range(2000):
    n = rng.randint(0, 8)
    nums = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(0, 9)
    assert check_hash(nums, k) == check_brute(nums, k), (nums, k)
print("2000 random cases OK")
```

**Output (my run):**
```
True False
[6], k=6 -> False (a single 6 is a multiple but length 1)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty or one element: False.
- `[0, 0]`: True for any k (sum 0 is a multiple of anything, including 0 as the problem allows).
- `k = 1`: any pair works.
- `k = 0`: need a zero-sum subarray of length at least 2.
- `k` larger than every sum: only a zero-sum run works.

**Follow-ups:**
- *Negative numbers?* Python's `%` already returns a non-negative remainder for positive k, so the idea still holds. Without that guarantee, normalise with `((p % k) + k) % k`.
- *Count them instead of existence?* Count remainder frequencies and add `c*(c-1)/2` per remainder (this is a later question in this part).
- *Why a dict and not a set?* You need the index, to enforce length at least 2.

**Common mistakes:**
- Overwriting the stored index with the latest one, which loses long spans.
- Forgetting the `{0: -1}` seed.
- Dividing by `k = 0`.
- Accepting length-1 subarrays.

### Q26 ⭐⭐ 🟡 Contiguous array. Given a list of 0s and 1s, return the length of the longest contiguous subarray with equally many 0s and 1s. Map 0 to -1 and use first-seen prefix sums. Example: [0,1] -> 2; [0,1,0] -> 2; [0,0,1,0,0,0,1,1] -> 6.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Prefix sums with a first-seen map after a transform (0 becomes -1). Equal count of 0s and 1s means a net balance of zero.

**Say this first (1 line):** "Treat 0 as -1, keep a running balance, and remember the first index of each balance; whenever a balance repeats, the stretch between has equal 0s and 1s, so I take the longest such gap."

**Brute force:** For each start, extend the end with a running balance, record the length when it hits 0. O(n^2) time, O(1) space.

**Optimal:**
- Balance after index `i` is `#1s - #0s` so far.
- Same balance at positions `a < b` means the subarray `(a, b]` has net zero.
- Store only the first index of each balance (seed `{0: -1}`), since the earliest occurrence gives the longest span.
- Answer is the maximum `i - first[balance]`.

**Complexity:** O(n) time. Space O(n) worst case (balances range within [-n, n], so at most 2n+1 keys).

**Dry run:** `[0,0,1,0,0,0,1,1]`.
| i | x | balance | first seen? | length |
|---|---|---|---|---|
| seed | | 0 | at -1 | |
| 0 | 0 | -1 | store 0 | |
| 1 | 0 | -2 | store 1 | |
| 2 | 1 | -1 | seen at 0 | 2 |
| 3 | 0 | -2 | seen at 1 | 2 |
| 4 | 0 | -3 | store 4 | |
| 5 | 0 | -4 | store 5 | |
| 6 | 1 | -3 | seen at 4 | 2 |
| 7 | 1 | -2 | seen at 1 | 6 |
Answer 6.

All three examples in the prompt are correct; my run matches each and the brute force.

**Code:**
```python
import random


def longest_brute(nums):
    best = 0
    for i in range(len(nums)):
        bal = 0
        for j in range(i, len(nums)):
            bal += 1 if nums[j] == 1 else -1
            if bal == 0:
                best = max(best, j - i + 1)
    return best


def longest_hash(nums):
    first = {0: -1}               # balance 0 before index 0
    bal = best = 0
    for i, x in enumerate(nums):
        bal += 1 if x == 1 else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i        # earliest index gives the longest span
    return best


for arr, want in [([0, 1], 2), ([0, 1, 0], 2), ([0, 0, 1, 0, 0, 0, 1, 1], 6)]:
    got = longest_hash(arr)
    print(arr, "->", got)
    assert got == want == longest_brute(arr)

# --- edge cases
assert longest_hash([]) == 0
assert longest_hash([0]) == 0 and longest_hash([1]) == 0
assert longest_hash([0, 0, 0]) == 0
assert longest_hash([1, 1, 1, 1]) == 0
assert longest_hash([1, 0, 1, 0, 1, 0]) == 6
assert longest_hash([1, 1, 0, 0]) == 4
assert longest_hash([0, 0, 0, 1, 1]) == 4
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(26)
for _ in range(2000):
    arr = [rng.randint(0, 1) for _ in range(rng.randint(0, 14))]
    assert longest_hash(arr) == longest_brute(arr), arr
print("2000 random cases OK")
```

**Output (my run):**
```
[0, 1] -> 2
[0, 1, 0] -> 2
[0, 0, 1, 0, 0, 0, 1, 1] -> 6
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty list: 0.
- All 0s or all 1s: 0 (the balance never repeats).
- Whole array balanced: the answer is n.
- A single element: 0.

**Follow-ups:**
- *Why not a sliding window?* A window cannot decide when to shrink: a balance can go down and come back up, so there is no monotone signal.
- *Generalise?* Subarray with sum k, or equal counts of three kinds (use a tuple of differences as the key).
- *Space?* Can use an array of size 2n+1 offset by n instead of a dict.

**Common mistakes:**
- Forgetting the `{0: -1}` seed, which loses prefixes that start at index 0.
- Updating the stored index on every repeat (shortens the answer).
- Mapping 0 to 0 instead of -1.

### Q27 ⭐⭐ 🟡 Find all duplicates in place. A list of n integers has every value in 1..n, each value appearing once or twice. Return all values that appear twice in O(n) time and O(1) extra space (output excluded) by using the sign or index of the array itself as a marker, and say what you do to restore the input. Example: [4,3,2,7,8,2,3,1] -> [2,3].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Use the array itself as a hash set (index marking). Because every value is in 1..n, value `v` has a home slot `v-1`, and a sign bit on that slot records "seen".

**Say this first (1 line):** "For each value I flip the sign of the slot at its own index; if that slot is already negative, I have seen the value before, so it is a duplicate; at the end I take absolute values to restore the input."

**Brute force:** Counter or set: O(n) time and O(n) space. Or sort and compare neighbours: O(n log n) and it modifies the input. Both miss the O(1) extra space ask (sorting mutates).

**Optimal:**
- For each `x`, take `v = abs(x)` (the slot may have been negated earlier, but the value stored there still identifies a real value).
- If `nums[v-1] < 0`, then `v` was seen: add `v` to the answer.
- Otherwise negate `nums[v-1]`.
- Each duplicate is reported exactly once because a value appears at most twice. A third visit would break the guarantee.
- **Restore** with a final pass that sets every cell to its absolute value. Without it, the caller's data is corrupted, so state this out loud.

**Complexity:** O(n) time (two passes). O(1) extra space excluding the output. It does temporarily mutate the input.

**Dry run:** `[4,3,2,7,8,2,3,1]`.
- Marks negate slots 3, 2, 1, 6, 7 (values 4, 3, 2, 7, 8).
- Next x=2: slot 1 is already negative: report 2.
- Next x=3: slot 2 negative: report 3.
- x=1: slot 0 positive, negate. Final abs pass restores. Answer `[2,3]`.

The prompt's example is correct and the output order [2,3] is what this method produces (order of the second occurrence).

**Code:**
```python
import random
from collections import Counter


def dups_brute(nums):
    c = Counter(nums)
    return sorted(v for v, cnt in c.items() if cnt == 2)


def dups_inplace(nums):
    """Mark value v by negating nums[v-1]. A second visit sees a negative."""
    out = []
    for x in nums:
        v = abs(x)                      # x may already be negated by a marker
        if nums[v - 1] < 0:
            out.append(v)               # seen before
        else:
            nums[v - 1] = -nums[v - 1]
    for i in range(len(nums)):          # restore the input
        nums[i] = abs(nums[i])
    return out


a = [4, 3, 2, 7, 8, 2, 3, 1]
orig = a[:]
res = dups_inplace(a)
print("duplicates:", res, "| input restored:", a == orig)
assert res == [2, 3] and a == orig

# --- edge cases
assert dups_inplace([]) == []
assert dups_inplace([1]) == []
assert dups_inplace([1, 1]) == [1]
assert dups_inplace([1, 2, 3]) == []
assert dups_inplace([2, 2]) == [2]
assert sorted(dups_inplace([1, 1, 2, 2])) == [1, 2]   # stays valid: 3, 4 missing
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(27)
for _ in range(2000):
    n = rng.randint(0, 10)
    pool = list(range(1, n + 1)) * 2     # each value at most twice
    rng.shuffle(pool)
    nums = pool[:n]
    before = nums[:]
    got = sorted(dups_inplace(nums))
    assert got == dups_brute(before), before
    assert nums == before                # restored
print("2000 random cases OK")
```

**Output (my run):**
```
duplicates: [2, 3] | input restored: True
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty or single value: nothing.
- `[1,1]`: reports 1.
- A value that is a duplicate and also the slot that was negated: `abs(x)` handles it.
- Input already containing negatives or 0 or values out of range: the trick does not apply; state the precondition.

**Follow-ups:**
- *Could you do it without mutating?* Not in O(1) space for this problem in general; with the mutation you must restore. Cyclic sort is the other in-place option.
- *Multi-threaded callers?* The temporary mutation is not safe to share; copy first or take a lock.
- *Related?* Find all numbers missing from 1..n: the slots still positive after marking.

**Common mistakes:**
- Forgetting `abs()` when reading `x`, giving a negative index.
- Not restoring the input.
- Using the trick when values can be 0 or above n.

### Q28 ⭐⭐ 🟡 Find the duplicate number. A list of n+1 integers holds values in 1..n and exactly one value is repeated (possibly many times). Find it without modifying the list and using O(1) extra space. Compare a set (O(n) space), sorting (modifies), binary search on value range and Floyd cycle detection treating values as next pointers. Example: [1,3,4,2,2] -> 2; [3,1,3,4,2] -> 3.
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Pigeonhole plus Floyd's cycle detection on an implicit linked list. Treat each index `i` as a node pointing to `nums[i]`. Two indices with the same value mean two edges into one node, which is where the cycle begins.

**Say this first (1 line):** "With n+1 values in 1..n, I treat `nums` as next pointers; the repeated value is the entrance of the cycle, so I find it with tortoise and hare without touching the array and with O(1) space."

**Brute force / alternatives (compared):**
| Method | Time | Extra space | Modifies input |
|---|---|---|---|
| Set of seen values | O(n) | O(n) | no |
| Sort and scan neighbours | O(n log n) | O(1) if in place, O(n) for a copy | yes if in place |
| Binary search on value range | O(n log n) | O(1) | no |
| Floyd cycle detection | O(n) | O(1) | no |

**Optimal (Floyd):**
- Start both pointers at node 0. Node 0 is never a value, so nothing points back to it, and it is outside the cycle: the head.
- Phase 1: slow moves one step (`nums[slow]`), fast moves two. They meet inside the cycle.
- Phase 2: put slow back at node 0 and move both one step at a time. They meet at the cycle entrance, which is the duplicate.
- Why: let `a` be the tail length and `c` the cycle length. At the meeting, slow has walked `s` steps and fast `2s`; both are in the cycle, so `s` is a multiple of `c`. The meeting point is `x = s - a` steps past the entrance, so walking `a` more steps from it gives `s` steps total, a multiple of `c`, which is the entrance. Walking `a` steps from the head also reaches the entrance. So the two pointers meet there.

**Binary search on values (the alternative):** for a candidate `mid`, count values `<= mid`. If the count exceeds `mid`, the duplicate is in `[lo, mid]`; otherwise in `[mid+1, hi]`. Pigeonhole guarantees the sign. O(n log n), O(1) space, simpler to defend.

**Complexity:** Floyd: O(n) time, O(1) space. Each phase walks at most a small constant times n steps.

**Dry run:** `[1,3,4,2,2]`. Edges: 0→1, 1→3, 3→2, 2→4, 4→2. The cycle is 2→4→2, entrance 2.
- Phase 1 (slow, fast): (1,3), (3,4), (2,4), (4,4). They meet at node 4.
- Phase 2 (slow from 0, fast from 4): (1,2), (3,4), (2,2). They meet at 2, the answer.

The prompt's examples are correct; all four methods agree on both in my run.

**Code:**
```python
import random


def find_set(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)


def find_sort(nums):
    s = sorted(nums)                     # copy: the input stays untouched
    for a, b in zip(s, s[1:]):
        if a == b:
            return a


def find_binary(nums):
    """Binary search on the VALUE range 1..n using the pigeonhole count."""
    lo, hi = 1, len(nums) - 1            # values are in 1..n, len = n+1
    while lo < hi:
        mid = (lo + hi) // 2
        cnt = sum(1 for x in nums if x <= mid)
        if cnt > mid:                    # too many values <= mid: dup is in [lo, mid]
            hi = mid
        else:
            lo = mid + 1
    return lo


def find_floyd(nums):
    """Index i points to nums[i]. The repeated value is the cycle entrance."""
    slow = fast = 0                      # node 0 is the head: no value equals 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                             # phase 2: restart one pointer at the head
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


for arr, want in [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]:
    r = (find_set(arr), find_sort(arr), find_binary(arr), find_floyd(arr))
    print(arr, "->", r)
    assert r == (want,) * 4

# --- edge cases
assert find_floyd([1, 1]) == 1 and find_binary([1, 1]) == 1
assert find_floyd([2, 2, 2, 2, 2]) == 2           # many copies
assert find_binary([2, 2, 2, 2, 2]) == 2
assert find_floyd([1, 1, 2]) == 1 and find_binary([1, 1, 2]) == 1
assert find_floyd([2, 1, 2]) == 2
big = list(range(1, 100001)) + [77777]
assert find_floyd(big) == find_binary(big) == find_set(big) == 77777
keep = [3, 1, 3, 4, 2]
find_floyd(keep); find_binary(keep); find_sort(keep)
assert keep == [3, 1, 3, 4, 2]                    # not modified
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(28)
for _ in range(2000):
    n = rng.randint(1, 12)
    c = rng.randint(2, n + 1)                      # copies of the repeated value
    d = rng.randint(1, n)
    others = rng.sample([v for v in range(1, n + 1) if v != d], n + 1 - c)
    nums = [d] * c + others
    rng.shuffle(nums)
    assert len(nums) == n + 1
    want = find_set(nums)
    assert want == d
    assert find_sort(nums) == find_binary(nums) == find_floyd(nums) == d, nums
print("2000 random cases OK")
```

**Output (my run):**
```
[1, 3, 4, 2, 2] -> (2, 2, 2, 2)
[3, 1, 3, 4, 2] -> (3, 3, 3, 3)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- `[1,1]`: n=1, answer 1.
- The duplicate appears many times: fine, the argument only needs one repeated target.
- The duplicate is the first element (`[2,1,2]` etc.): node 0 still sits outside the cycle.
- The values are never 0 and never above n: this precondition is what keeps the walk inside the array.

**Follow-ups:**
- *Why start at node 0?* No value equals 0, so nothing points back to node 0. It is outside the cycle, which the proof needs.
- *What if values include 0?* The walk could loop on node 0 and the proof breaks; use another method.
- *How is this related to linked list cycle detection?* It is the same two phases, with `nums[i]` as the `next` pointer.

**Common mistakes:**
- Sorting the input, which breaks the "do not modify" rule.
- Starting phase 1 at `nums[0]` but restarting phase 2 at node 0. The two phases must share the same head, or the loop may never end.
- Returning the meeting point of phase 1 instead of the phase-2 meeting.

### Q29 ⭐⭐ 🟡 Sort by frequency. Given a list of integers, return it sorted by frequency in descending order, ties broken by smaller value first. Show Counter plus sorted with a tuple key and explain stability of sorted and why tie-breaking must be explicit. Example: [1,1,2,2,2,3] -> [2,2,2,1,1,3]; [2,3,1,3,2] -> [2,2,3,3,1].
**Asked at:** Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports | Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports
**Pattern:** Frequency counting plus a composite sort key (a tuple key). Count once, then sort by `(-count, value)`.

**Say this first (1 line):** "Counter for frequencies, then `sorted(nums, key=lambda x: (-cnt[x], x))`; the tuple makes the tie-break explicit: higher count first, smaller value first."

**Brute force:** Key by `nums.count(x)` inside the sort. Each call is O(n), so O(n^2) overall. Correct but slow.

**Optimal:**
- `cnt = Counter(nums)`, O(n).
- `sorted(nums, key=lambda x: (-cnt[x], x))`. Negating the count sorts descending without `reverse`, so the value part still sorts ascending. (`reverse=True` would flip both.)
- Equal values come out together because they share the same key.

**Stability, and why the tie-break must be explicit:** `sorted` is stable: items with equal keys keep their input order. If you key only on `-cnt[x]`, tied values keep first-position order, and worse, the tied values interleave. On `[3,2,2,3,1]` that gives `[3,2,2,3,1]`: 3s and 2s are not grouped. Adding `x` to the key groups them and orders them as required.

**Complexity:** Time O(n log n) for the sort plus O(n) counting. Space O(n) for the counter and the output list. Sorting the n elements rather than the d distinct values costs a bit more than needed; you can instead sort the distinct values and expand with `[v] * c`, giving O(n + d log d).

**Dry run:** `[2,3,1,3,2]`. Counts: 2→2, 3→2, 1→1. Keys: 2→(-2,2), 3→(-2,3), 1→(-1,1). Sorted by key: 2,2 then 3,3 then 1 = `[2,2,3,3,1]`.

Both prompt examples are correct and my run reproduces them.

**Code:**
```python
import random
from collections import Counter


def sort_brute(nums):
    return sorted(nums, key=lambda x: (-nums.count(x), x))      # O(n^2) counts


def sort_freq(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: (-cnt[x], x))


def sort_freq_no_tiebreak(nums):
    cnt = Counter(nums)
    return sorted(nums, key=lambda x: -cnt[x])      # relies on stability only


print(sort_freq([1, 1, 2, 2, 2, 3]), sort_freq([2, 3, 1, 3, 2]))
assert sort_freq([1, 1, 2, 2, 2, 3]) == [2, 2, 2, 1, 1, 3]
assert sort_freq([2, 3, 1, 3, 2]) == [2, 2, 3, 3, 1]

# stability alone keeps first-position order inside a tie: equal-count values interleave
t = [3, 2, 2, 3, 1]
print("explicit tie-break  :", sort_freq(t))
print("stability only      :", sort_freq_no_tiebreak(t), "(tied values interleaved: wrong)")
assert sort_freq(t) == [2, 2, 3, 3, 1]
assert sort_freq_no_tiebreak(t) == [3, 2, 2, 3, 1]

# --- edge cases
assert sort_freq([]) == []
assert sort_freq([5]) == [5]
assert sort_freq([4, 4, 4]) == [4, 4, 4]
assert sort_freq([3, 2, 1]) == [1, 2, 3]            # all frequency 1: by value
assert sort_freq([-1, -1, 2, 2, 0]) == [-1, -1, 2, 2, 0]
assert sort_freq([2, 2, -3, -3]) == [-3, -3, 2, 2]  # tie: smaller value first
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(29)
for _ in range(2000):
    nums = [rng.randint(-4, 4) for _ in range(rng.randint(0, 14))]
    assert sort_freq(nums) == sort_brute(nums), nums
print("2000 random cases OK")
```

**Output (my run):**
```
[2, 2, 2, 1, 1, 3] [2, 2, 3, 3, 1]
explicit tie-break  : [2, 2, 3, 3, 1]
stability only      : [3, 2, 2, 3, 1] (tied values interleaved: wrong)
edge cases OK
2000 random cases OK
```

**Edge cases:**
- Empty list.
- All equal.
- All distinct: sorted ascending by value.
- Negative values: the tie-break "smaller value first" means -3 before 2.

**Follow-ups:**
- *Return distinct values with counts?* Use `sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))`.
- *Only the top k?* Heap or bucket by frequency (an earlier question in this part).
- *Strings?* The same, which is a common variant.

**Common mistakes:**
- Relying on stability alone and thinking it breaks ties by value.
- Using `reverse=True` with a `(count, value)` key, which sorts values descending too.
- Calling `.count` inside the key (hidden O(n^2)).

### Q30 ⭐⭐ 🟡 Majority element II. Return all values that appear more than n/3 times in a list of integers in O(n) time and O(1) extra space. Generalise Boyer-Moore with two candidates, then add a verification pass and say why it is needed. Example: [3,2,3] -> [3]; [1,2] -> [1,2]; [1] -> [1].
**Asked at:** Public pattern lists (NeetCode 150 / Blind 75 style 'Arrays & Hashing' sections as mirrored on a Scribd copy, a dev.to prep-sheet post and GitHub roadmap repos; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Company-tagged and product-company prep lists (Weekday 'DSA interview questions 2026: 60 must-know problems with patterns' post, Naukri Code360 must-do list for product-based companies; snippets only, not opened); commercial prep content, not verified candidate reports
**Pattern:** Boyer-Moore voting generalised to k = 2 candidates. Cancel off groups of three distinct values; whatever survives is the only possible winners.

**Say this first (1 line):** "At most two values can appear more than n/3 times, so I keep two candidates with counters, cancel triples of distinct values, then run a second pass to verify the survivors really exceed n/3."

**Brute force:** Counter and filter `count > n // 3`. O(n) time, O(n) space. Or sort and scan runs.

**Optimal:**
- Two candidates `c1, c2` with counts `n1, n2`.
- For each `x`: if it equals a candidate, increment that count. Else if a count is 0, adopt `x` there. Else decrement both.
- A decrement of both removes three distinct values from consideration (`x`, one `c1`, one `c2`). A value with more than n/3 occurrences cannot be fully cancelled, since each cancelled triple holds at most one copy of it, and at most n/3 triples can be cancelled.
- **Verification is required:** the survivors are only possible winners. `[1,2,3]` leaves candidates 1 and 2 although neither exceeds n/3 = 1 (each appears once). The second pass counts both candidates: O(n) total, O(1) space.
- Check order matters: test equality with a candidate before testing for a zero count, or a value can be adopted twice.

**Complexity:** O(n) time (two passes), O(1) extra space.

**Dry run:** `[3,2,3]`. 3 becomes c1 (1). 2 becomes c2 (1). 3 matches c1 (2). Candidates {3, 2}. Verify with n//3 = 1: 3 appears 2 > 1 yes, 2 appears 1 > 1 no. Answer `[3]`.

All three prompt examples are correct; `[1,2]` gives both since 1 > 0.67 (n//3 = 0 and counts must exceed it).

**Code:**
```python
import random
from collections import Counter


def maj3_brute(nums):
    n = len(nums)
    c = Counter(nums)
    return sorted(v for v, k in c.items() if k > n // 3)


def candidates(nums):
    """Pass 1: the two survivors of the pairing-off. Only POSSIBLE winners."""
    c1 = c2 = None
    n1 = n2 = 0
    for x in nums:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:                         # three distinct values: cancel one of each
            n1 -= 1
            n2 -= 1
    return {c for c in (c1, c2) if c is not None}


def maj3_vote(nums):
    n = len(nums)
    cand = candidates(nums)
    # pass 2: verify (this is a count, still O(n) for two candidates)
    return sorted(c for c in cand if nums.count(c) > n // 3)


for arr, want in [([3, 2, 3], [3]), ([1, 2], [1, 2]), ([1], [1])]:
    print(arr, "->", maj3_vote(arr))
    assert maj3_vote(arr) == want == maj3_brute(arr)

# why verification: survivors are not always winners
for w in ([1, 2, 3], [1, 2, 3, 4, 5, 6, 7]):
    print(w, "survivors:", sorted(candidates(w)), "-> verified answer:", maj3_vote(w))
    assert maj3_vote(w) == []
assert sorted(candidates([1, 2, 3])) == [1, 2]

# --- edge cases
assert maj3_vote([]) == []
assert maj3_vote([2, 2]) == [2]
assert maj3_vote([0, 0, 0]) == [0]               # candidate value 0 is not None
assert maj3_vote([1, 1, 1, 2, 2, 2, 3]) == [1, 2]
assert maj3_vote([-1, -1, 5, 5, 7, 7]) == maj3_brute([-1, -1, 5, 5, 7, 7])
print("edge cases OK")

# --- seeded randomised cross-check
rng = random.Random(30)
for _ in range(3000):
    nums = [rng.randint(-3, 3) for _ in range(rng.randint(0, 15))]
    assert maj3_vote(nums) == maj3_brute(nums), nums
print("3000 random cases OK")
```

**Output (my run):**
```
[3, 2, 3] -> [3]
[1, 2] -> [1, 2]
[1] -> [1]
[1, 2, 3] survivors: [1, 2] -> verified answer: []
[1, 2, 3, 4, 5, 6, 7] survivors: [5, 7] -> verified answer: []
edge cases OK
3000 random cases OK
```

**Edge cases:**
- Empty list: nothing.
- A candidate value of 0: initialise candidates to `None`, not 0, or a real 0 may be confused with "no candidate".
- Fewer than two distinct values: one candidate only.
- At most two answers exist, so output is size 0, 1 or 2.

**Follow-ups:**
- *More than n/k?* Keep k-1 candidates (Misra-Gries). O(nk) time, O(k) space.
- *Why `> n // 3` and not `> n / 3`?* Counts are integers, so both are equivalent.
- *Streaming?* The first pass works on a stream; verification needs a second pass or a stored sample.

**Common mistakes:**
- Skipping the verification pass.
- Initialising both candidates to the same value, e.g. 0.
- Checking for a zero count before checking equality.
