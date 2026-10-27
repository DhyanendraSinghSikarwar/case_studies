import itertools
import random


def has132_fast(nums):
    third = float("-inf")          # largest valid '2' found so far (it has a bigger '3' left of it)
    st = []                        # decreasing from bottom to top, scanning right to left
    for x in reversed(nums):
        if x < third:
            return True            # x plays the '1'
        while st and st[-1] < x:
            third = st.pop()       # popped value has x (bigger) to its left: a valid '2'
        st.append(x)
    return False


def has132_n2(nums):
    n = len(nums)
    lo = float("inf")              # smallest value strictly before j
    for j in range(n):
        for k in range(j + 1, n):
            if lo < nums[k] < nums[j]:
                return True
        lo = min(lo, nums[j])
    return False


def has132_n3(nums):
    return any(nums[i] < nums[k] < nums[j]
               for i, j, k in itertools.combinations(range(len(nums)), 3))


for a, want in [([1, 2, 3, 4], False), ([3, 1, 4, 2], True), ([-1, 3, 2, 0], True)]:
    assert has132_fast(a) == has132_n2(a) == has132_n3(a) == want, a
    print(a, "->", has132_fast(a))

# edge cases
assert has132_fast([]) is False and has132_fast([1]) is False and has132_fast([1, 2]) is False
assert has132_fast([2, 2, 2, 2]) is False          # equal values never satisfy strict <
assert has132_fast([1, 3, 2]) is True              # the minimal pattern
assert has132_fast([3, 2, 1]) is False             # strictly decreasing
assert has132_fast([1, 4, 2, 3]) is True and has132_fast([3, 4, 3, 3]) is False  # 3 is not < 3
assert has132_fast([-5, -1, -3]) is True           # negatives
assert has132_fast(list(range(200000))) is False   # increasing, max size
assert has132_fast(list(range(200000, 0, -1))) is False

# exhaustive over all sequences of length <= 6 on values 0..3, then seeded random
for n in range(0, 7):
    for t in itertools.product(range(4), repeat=n):
        assert has132_fast(list(t)) == has132_n3(list(t)), t
print("exhaustive: every sequence up to length 6 over values 0..3 agrees with the triple loop")
rng = random.Random(40)
hits = 0
for _ in range(3000):
    n = rng.randint(0, 12)
    a = [rng.randint(-5, 5) for _ in range(n)]
    r = has132_fast(a)
    assert r == has132_n2(a) == has132_n3(a), a
    hits += r
print(f"3000 seeded random arrays agree; {hits} contained a 132 pattern")
