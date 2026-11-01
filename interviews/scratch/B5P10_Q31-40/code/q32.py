import functools
import random

random.seed(32)

def solve(nums, target):
    ns = tuple(nums)          # hashable, captured by the closure (not a cache key)
    n = len(ns)

    @functools.cache
    def f(i, rem):
        if i == n:
            return 1 if rem == 0 else 0
        return f(i + 1, rem) + f(i + 1, rem - ns[i])

    ans = f(0, target)
    info = f.cache_info()
    entries = info.currsize          # entries held right before the clear
    f.cache_clear()
    return [ans, info.hits, info.misses, f.cache_info().currsize], entries

def oracle(nums, target):
    """Hand-written dict memo that counts hits and misses itself."""
    n = len(nums)
    memo, hits, misses = {}, 0, 0
    def f(i, rem):
        nonlocal hits, misses
        if (i, rem) in memo:
            hits += 1
            return memo[(i, rem)]
        misses += 1
        v = (1 if rem == 0 else 0) if i == n else f(i + 1, rem) + f(i + 1, rem - nums[i])
        memo[(i, rem)] = v
        return v
    a = f(0, target)
    return [a, hits, misses, 0], len(memo)

def brute_count(nums, target):
    n = len(nums)
    return sum(1 for mask in range(1 << n) if sum(nums[i] for i in range(n) if mask >> i & 1) == target)

# ---- examples from the prompt
assert solve([1, 2, 3], 3)[0] == [2, 1, 14, 0]
assert solve([], 0)[0] == [1, 0, 1, 0]
assert solve([0, 0], 0)[0] == [4, 2, 3, 0]
assert solve([2, 2, 2, 2], 4)[0] == [6, 6, 15, 0]
print('examples ok')

# ---- why a list argument cannot be a cache key
@functools.cache
def g(lst):
    return sum(lst)
try:
    g([1, 2])
except TypeError as e:
    print('TypeError:', e)
print('tuple key works:', g((1, 2)))

# ---- misses == entries stored; hits + misses == number of calls
ex, entries = solve([1, 2, 3], 3)
print('example 1: misses', ex[2], 'entries before clear', entries, 'currsize after clear', ex[3])

# ---- seeded cross-check against the dict memo and a plain subset enumeration
cases = 0
for _ in range(500):
    nums = [random.randint(-20, 20) for _ in range(random.randint(0, 9))]
    target = random.randint(-100, 100) if random.random() < 0.3 else sum(random.sample(nums, random.randint(0, len(nums))))
    got, entries = solve(nums, target)
    exp, entries2 = oracle(nums, target)
    assert got == exp, (nums, target, got, exp)
    assert got[2] == entries == entries2          # misses == cached entries
    assert got[0] == brute_count(nums, target)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- cache_clear matters: a closure cache is rebuilt per call here, but a module-level one grows across tests
@functools.cache
def h(i):
    return i * 2
h(1); h(2); h(1)
print('module-level cache:', h.cache_info())
h.cache_clear()
print('after cache_clear:', h.cache_info())
assert h.cache_info().currsize == 0

# ---- edge cases
assert solve([], 5)[0] == [0, 0, 1, 0]
assert solve([20] * 15, 100)[0][0] == 3003          # C(15, 5)
print('edge cases ok')
