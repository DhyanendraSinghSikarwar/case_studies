### Q20 ⭐⭐ 🟢 Pascal's triangle. `num_rows` is an integer with 0 <= num_rows <= 30 and `row_index` is an integer with 0 <= row_index <= 200. Return `[triangle, row]`: `triangle` is the first `num_rows` rows as lists (row i has i + 1 entries, starts and ends with 1, and every inner entry is the sum of the two above it; `num_rows = 0` gives an empty list), and `row` is row number `row_index` (0-indexed) alone, built with only O(row_index) extra space by updating one list from right to left. Explain why the right-to-left order matters, give the closed form C(n, k) = n! / (k! (n - k)!) and the recurrence C(n, k) = C(n, k-1) * (n - k + 1) / k that is always an exact integer step, and say from which row on the entries stop fitting in a signed 32-bit integer (the largest entry of row 33 is below 2^31 - 1 and row 34 has an entry above it) while Python needs no change. In the answer include a dry run on the first example and a seeded random cross-check of your solution against math.comb on small inputs. Example: num_rows=5, row_index=4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]; num_rows=0, row_index=0 -> [[], [1]]; num_rows=1, row_index=1 -> [[[1]], [1, 1]]; num_rows=3, row_index=10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Dynamic programming on a triangle (Pascal), with a one-row, right-to-left update for O(row) space.

**Say this first (1 line):** "Each entry is the sum of the two above it, edges are 1. For a single row I keep one list and update it from right to left, so the value I read from the left is still last row's value. That is O(row_index) space."

**Brute force:** Use the closed form C(n, k) = n! / (k! (n-k)!) per entry. Correct, but computing factorials per entry wastes work; `math.comb` is the checked reference here (`math.comb` exists since 3.8, editor knowledge).

**Optimal:**
- Triangle: row i = [1] + [prev[j-1] + prev[j] for j in 1..i-1] + [1]; row 0 is [1]; `num_rows = 0` returns [].
- Single row without keeping rows: start with row = [1] * (n + 1). For i from 1 to n, update j = i-1 down to 1 with `row[j] += row[j-1]`. Right to left: `row[j-1]` has not been touched in this round yet, so it still holds last round's value. Left to right would add an already-updated neighbour: for row 4 it gives [1, 4, 8, 9, 1] (shown in the output).
- Multiplicative recurrence: C(n, k) = C(n, k-1) * (n - k + 1) / k. Multiply first, then use integer `//`: the division is always exact (checked for every row below 200), so no floats are needed.
- Overflow: Python ints do not overflow. In a signed 32-bit integer the largest entry of row 33 is 1,166,803,110 (fits under 2,147,483,647) and row 34 has an entry 2,333,606,220 (does not), so from row 34 on you need 64 bits in other languages.

**Complexity:** Triangle: O(num_rows^2) time and space (it is the output). One row: O(n^2) time for the nested loop, O(n) space. The multiplicative way is O(n) time for the row (n big-int multiplications), also O(n) space.

**Dry run:** row_index 4: row = [1,1,1,1,1]. i=1: nothing to update. i=2: j=1: row[1] = 1 + 1 = 2 -> [1,2,1,1,1]. i=3: j=2: row[2] = 1 + 2 = 3; j=1: row[1] = 2 + 1 = 3 -> [1,3,3,1,1]. i=4: j=3: 1+3 = 4; j=2: 3+3 = 6; j=1: 3+1 = 4 -> [1,4,6,4,1].

**Code:**
```python
import math
import random

random.seed(1320)

def pascal(num_rows, row_index):
    tri = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    row = [1] * (row_index + 1)
    for i in range(1, row_index + 1):
        for j in range(i - 1, 0, -1):          # RIGHT to LEFT: row[j-1] is still last row's value when we use it
            row[j] += row[j - 1]
    return [tri, row]

def brute(num_rows, row_index):
    return [[[math.comb(i, j) for j in range(i + 1)] for i in range(num_rows)],
            [math.comb(row_index, j) for j in range(row_index + 1)]]

examples = [
    (5, 4, [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]),
    (0, 0, [[], [1]]),
    (1, 1, [[[1]], [1, 1]]),
    (3, 10, [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]),
]
for nr, ri, exp in examples:
    got = pascal(nr, ri)
    print(nr, ri, '->', got)
    assert got == exp and brute(nr, ri) == exp

# left-to-right update is wrong: it re-uses a value already overwritten
def wrong_row(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i):
            row[j] += row[j - 1]
    return row
print('left-to-right row 4:', wrong_row(4), '(correct [1, 4, 6, 4, 1])')
assert wrong_row(4) != [1, 4, 6, 4, 1]

# the multiplicative recurrence C(n,k) = C(n,k-1) * (n-k+1) / k is ALWAYS exact: multiply first, then //
for n in range(0, 200):
    c = 1
    for k in range(1, n + 1):
        assert (c * (n - k + 1)) % k == 0
        c = c * (n - k + 1) // k
        assert c == math.comb(n, k)
print('exact-division recurrence checked for every row n < 200')

# int32 boundary: largest entry of row 33 is below 2^31 - 1, row 34 has an entry above it
mx = lambda n: max(math.comb(n, k) for k in range(n + 1))
print('max entry row 33 =', mx(33), ' row 34 =', mx(34), ' 2^31 - 1 =', 2 ** 31 - 1)
assert mx(33) < 2 ** 31 - 1 < mx(34) and all(mx(n) < 2 ** 31 - 1 for n in range(34))

# row sums are 2^n; symmetry
for n in range(0, 61):
    r = pascal(0, n)[1]
    assert sum(r) == 2 ** n and r == r[::-1]
print('row sums 2^n and symmetry ok for n <= 60')

# seeded random cross-check against math.comb
for _ in range(300):
    nr, ri = random.randint(0, 30), random.randint(0, 200)
    assert pascal(nr, ri) == brute(nr, ri)
print('random cross-check ok: 300 cases')

# edge asserts
assert pascal(0, 0) == [[], [1]] and pascal(2, 0)[1] == [1] and len(pascal(30, 200)[0]) == 30 and len(pascal(30, 200)[1]) == 201
print('edge asserts ok; C(200, 100) has', len(str(math.comb(200, 100))), 'digits')
```

**Output (my run):**
```
5 4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]
0 0 -> [[], [1]]
1 1 -> [[[1]], [1, 1]]
3 10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]
left-to-right row 4: [1, 4, 8, 9, 1] (correct [1, 4, 6, 4, 1])
exact-division recurrence checked for every row n < 200
max entry row 33 = 1166803110  row 34 = 2333606220  2^31 - 1 = 2147483647
row sums 2^n and symmetry ok for n <= 60
random cross-check ok: 300 cases
edge asserts ok; C(200, 100) has 59 digits
```

**Edge cases:**
- num_rows = 0: empty triangle; row_index = 0: [1].
- Rows are symmetric and sum to 2^n (checked for n <= 60).
- Row 200 has entries with up to 59 digits (C(200, 100)); Python handles it.
- `num_rows` and `row_index` are independent inputs here.

**Follow-ups:**
- Why is the sum 2^n? Each element in a set of n is in or out of a subset; C(n, k) counts subsets of size k.
- Row mod a prime for large n? Use the multiplicative recurrence with a modular inverse (modular inverse is another question in this part).
- Only the k-th entry? One loop of the recurrence, O(k) time, O(1) space.

**Common mistakes:**
- Updating left to right and corrupting the row.
- Writing the recurrence with float division (`/`) and getting rounding errors for large rows.
- Off-by-one: row 0 is [1] (row_index is 0-indexed).
- Forgetting that `num_rows = 0` must return `[]`, not `[[]]`.
