import bisect
import random

random.seed(40)

def lis_strict(heights):
    tails = []
    for h in heights:
        p = bisect.bisect_left(tails, h)       # strict: an equal height replaces, never extends
        if p == len(tails):
            tails.append(h)
        else:
            tails[p] = h
    return len(tails)

def russian_doll(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))     # width up, height DOWN on equal width
    return lis_strict([h for _, h in order])

def ascending_tiebreak_bug(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], e[1]))      # WRONG tie-break
    return lis_strict([h for _, h in order])

def brute(envelopes):
    """O(n^2) DP over pairs, checking BOTH dimensions strictly."""
    es = sorted(envelopes)
    n = len(es)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if es[j][0] < es[i][0] and es[j][1] < es[i][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)

# ---- examples from the prompt
assert russian_doll([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
assert russian_doll([[1, 1], [1, 1], [1, 1]]) == 1
assert russian_doll([]) == 0
assert russian_doll([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]) == 4
print('examples ok')

# ---- walk-through of the first example
env = [[5, 4], [6, 4], [6, 7], [2, 3]]
order = sorted(env, key=lambda e: (e[0], -e[1]))
print('sorted (w asc, h desc):', order)
tails = []
for _, h in order:
    p = bisect.bisect_left(tails, h)
    tails[p:p + 1] = [h]
    print(f'  h={h}: position {p}, tails = {tails}')
print('answer', len(tails))

# ---- why descending: with an ascending tie-break equal widths chain
E2 = [[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]
print('ascending tie-break on', E2, '->', ascending_tiebreak_bug(E2), '| correct', russian_doll(E2))
assert ascending_tiebreak_bug(E2) == 5 and brute(E2) == 4

# ---- seeded cross-check against the O(n^2) pair DP
cases = bad_asc = 0
for _ in range(600):
    n = random.randint(0, 14)
    es = [[random.randint(1, 6), random.randint(1, 6)] for _ in range(n)]
    got = russian_doll(es)
    assert got == brute(es), es
    if ascending_tiebreak_bug(es) != got:
        bad_asc += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the ascending tie-break was wrong on', bad_asc)

# ---- edge cases and full size
assert russian_doll([[3, 3]]) == 1
assert russian_doll([[1, 5], [1, 6], [1, 7]]) == 1             # same width never nests
assert russian_doll([[1, 5], [2, 5], [3, 5]]) == 1             # same height never nests
assert russian_doll([[i, i] for i in range(1, 101)]) == 100
big = [[random.randint(1, 10**9), random.randint(1, 10**9)] for _ in range(10**5)]
print('n = 10**5 random envelopes, chain length:', russian_doll(big))
print('edge cases ok')
