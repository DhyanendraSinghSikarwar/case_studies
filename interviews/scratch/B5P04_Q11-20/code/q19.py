import random


def prev_next_brute(a):
    n = len(a)
    prev, nxt = [], []
    for i in range(n):
        j = i - 1
        while j >= 0 and not a[j] < a[i]:     # nearest strictly smaller on the left
            j -= 1
        prev.append(j)
        k = i + 1
        while k < n and not a[k] < a[i]:      # nearest strictly smaller on the right
            k += 1
        nxt.append(k)
    return prev, nxt


def prev_next(a):
    n = len(a)
    prev = [-1] * n
    nxt = [n] * n                 # elements never popped keep n
    link = [-1] * n               # for an equal-value pop: "my answer is the same as that index's"
    stack = []                    # indices, values strictly increasing bottom to top
    for i, x in enumerate(a):
        while stack and a[stack[-1]] >= x:
            j = stack.pop()
            if a[j] > x:
                nxt[j] = i        # x is strictly smaller than a[j]: first one to its right
            else:
                link[j] = i       # equal: j's next strictly smaller is i's next strictly smaller
        prev[i] = stack[-1] if stack else -1   # top is strictly smaller than x
        stack.append(i)
    for j in range(n - 1, -1, -1):             # resolve links right to left (link[j] > j)
        if link[j] != -1:
            nxt[j] = nxt[link[j]]
    return prev, nxt


examples = [([4, 5, 2, 10, 8], ([-1, 0, -1, 2, 2], [2, 2, 5, 4, 5])), ([3, 3, 3], ([-1, -1, -1], [3, 3, 3]))]
for a, want in examples:
    got = prev_next(a)
    assert got == prev_next_brute(a) == want, (a, got)
    print(a, "-> prev", got[0], "nxt", got[1])

assert prev_next([]) == ([], [])
assert prev_next([7]) == ([-1], [1])
assert prev_next([1, 2, 3, 4]) == ([-1, 0, 1, 2], [4, 4, 4, 4])      # increasing
assert prev_next([4, 3, 2, 1]) == ([-1, -1, -1, -1], [1, 2, 3, 4])   # decreasing
assert prev_next([2, 2, 1, 2]) == prev_next_brute([2, 2, 1, 2])      # duplicates around a smaller value
assert prev_next([5] * 100000) == ([-1] * 100000, [100000] * 100000)  # max size, all equal
assert prev_next(list(range(100000))) == (list(range(-1, 99999)), [100000] * 100000)

# the tie rule used for "sum of subarray minimums": left strict, right non-strict (<=)
def next_smaller_or_equal(a):
    n, res, st = len(a), [len(a)] * len(a), []
    for i, x in enumerate(a):
        while st and a[st[-1]] >= x:
            res[st.pop()] = i
        st.append(i)
    return res

print("next strictly smaller        for [3,3,3]:", prev_next([3, 3, 3])[1])
print("next smaller-or-equal        for [3,3,3]:", next_smaller_or_equal([3, 3, 3]))

rng = random.Random(19)
cases = 0
for _ in range(4000):
    a = [rng.randint(0, rng.choice([2, 4, 9])) for _ in range(rng.randint(0, 16))]
    assert prev_next(a) == prev_next_brute(a), a
    cases += 1
print("random cross-check passed:", cases, "cases")
