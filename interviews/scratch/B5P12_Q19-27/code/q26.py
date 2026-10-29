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
