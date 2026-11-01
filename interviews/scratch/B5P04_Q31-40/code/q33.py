import itertools
import random


def valid_fast(pushed, popped):
    st, j = [], 0
    for v in pushed:
        st.append(v)
        while st and j < len(popped) and st[-1] == popped[j]:
            st.pop()
            j += 1
    return not st            # same length is given, so empty stack means all matched


def valid_brute(pushed, popped):
    # exhaustive search over every interleaving of pushes and pops
    n = len(pushed)
    def go(i, st, j):
        if j == n:
            return True
        if i < n and go(i + 1, st + (pushed[i],), j):
            return True
        if st and st[-1] == popped[j] and go(i, st[:-1], j + 1):
            return True
        return False
    return go(0, (), 0)


cases = [
    ([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
    ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False),
    ([], [], True),
    ([7], [7], True),
    ([1, 2], [1, 2], True),
    ([1, 2], [2, 1], True),
    ([1, 2, 3], [3, 1, 2], False),
    ([2, 1, 0], [1, 2, 0], True),
]
for a, b, want in cases:
    assert valid_fast(a, b) == valid_brute(a, b) == want, (a, b)
print("valid_fast([1,2,3,4,5],[4,5,3,2,1]) ->", valid_fast([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]))
print("valid_fast([1,2,3,4,5],[4,3,5,1,2]) ->", valid_fast([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]))

# exhaustive: every popped permutation for every n <= 7 (values 0..n-1 pushed in order)
tot = ok = 0
for n in range(0, 8):
    pushed = list(range(n))
    cnt = 0
    for perm in itertools.permutations(pushed):
        a = valid_fast(pushed, list(perm))
        tot += 1
        ok += a
        cnt += a
        if n <= 6:
            assert a == valid_brute(pushed, list(perm))
    print(f"n={n}: valid pop orders = {cnt}")
# the counts are the Catalan numbers 1,1,2,5,14,42,132,429 (checked via the printed rows)

# seeded random distinct values, shuffled pushed order, including popped that is not a permutation-checked case
rng = random.Random(33)
for _ in range(400):
    n = rng.randint(0, 6)
    vals = rng.sample(range(-20, 20), n)
    popped = vals[:]
    rng.shuffle(popped)
    assert valid_fast(vals, popped) == valid_brute(vals, popped)
print("400 seeded random cases agree with the exhaustive interleaving search")
