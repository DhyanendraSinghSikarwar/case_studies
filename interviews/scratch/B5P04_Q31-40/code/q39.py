import random


def visible_fast(h):
    n, ans, st = len(h), [0] * len(h), []
    for i in range(n - 1, -1, -1):
        c = 0
        while st and st[-1] < h[i]:
            st.pop()
            c += 1                  # a shorter person that i sees
        if st:
            c += 1                  # the first taller person, who blocks the rest
        ans[i] = c
        st.append(h[i])
    return ans


def visible_brute(h):
    n, ans = len(h), []
    for i in range(n):
        c = 0
        for j in range(i + 1, n):
            if all(h[m] < min(h[i], h[j]) for m in range(i + 1, j)):
                c += 1
        ans.append(c)
    return ans


a = visible_fast([10, 6, 8, 5, 11, 9])
b = visible_fast([5, 1, 2, 3, 10])
print(a, b)
assert a == visible_brute([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
assert b == visible_brute([5, 1, 2, 3, 10]) == [4, 1, 1, 1, 0]

# edge cases
assert visible_fast([]) == [] and visible_fast([7]) == [0]
assert visible_fast([1, 2]) == [1, 0] and visible_fast([2, 1]) == [1, 0]
assert visible_fast([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 0]       # decreasing: only the neighbour
assert visible_fast([1, 2, 3, 4, 5]) == [1, 1, 1, 1, 0]       # increasing: only the neighbour
assert visible_fast(list(range(100000, 0, -1)))[:2] == [1, 1]  # large input, no quadratic blow-up

# seeded random check; distinct integers as the prompt states
rng = random.Random(39)
for _ in range(2000):
    n = rng.randint(0, 9)
    h = rng.sample(range(1, 30), n)
    assert visible_fast(h) == visible_brute(h), h
print("2000 seeded random permutations agree with the O(n^3) definition")

# each person is popped at most once: count pops on a random input
h = rng.sample(range(1, 10**6), 50000)
st, pops = [], 0
for x in reversed(h):
    while st and st[-1] < x:
        st.pop(); pops += 1
    st.append(x)
assert pops <= len(h)
print("n=50000: pops =", pops, "<= n")
