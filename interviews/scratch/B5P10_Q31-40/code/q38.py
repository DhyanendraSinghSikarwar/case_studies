import random
import sys

random.seed(38)

def min_cost(days, costs):
    """dp[d] = minimum cost to cover every travel day <= d. Calendar days 0..last."""
    travel = set(days)
    last = days[-1]
    dp = [0] * (last + 1)                       # dp[0] = 0: nothing to cover yet
    for d in range(1, last + 1):
        if d not in travel:
            dp[d] = dp[d - 1]                   # a non-travel day costs nothing extra
        else:
            dp[d] = min(dp[d - 1] + costs[0],              # 1-day pass covers d only
                        dp[max(0, d - 7)] + costs[1],      # 7-day pass covers d-6..d
                        dp[max(0, d - 30)] + costs[2])     # 30-day pass covers d-29..d
    return dp[last], dp

def rec(days, costs):
    """Plain recursion over the next uncovered travel day (index into days)."""
    n = len(days)
    def f(i):
        if i >= n:
            return 0
        best = float('inf')
        for span, c in zip((1, 7, 30), costs):
            j = i
            while j < n and days[j] < days[i] + span:    # the pass bought on days[i] covers these
                j += 1
            best = min(best, c + f(j))
        return best
    return f(0)

# ---- examples from the prompt
assert min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])[0] == 11
assert min_cost([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])[0] == 17
assert min_cost([5], [3, 2, 1])[0] == 1
assert min_cost([1, 30], [5, 6, 7])[0] == 7
print('examples ok')

# ---- table for the first example
ans, dp = min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])
print('day :', list(range(len(dp))))
print('dp  :', dp)
print('answer', ans)

# ---- seeded cross-check against the plain recursion
cases = 0
for _ in range(600):
    n = random.randint(1, 9)
    days = sorted(random.sample(range(1, random.choice([10, 40, 80]) + 1), n))
    costs = [random.randint(1, 12) for _ in range(3)]          # not forced to be monotone
    assert min_cost(days, costs)[0] == rec(days, costs), (days, costs)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases and full size
assert min_cost([1], [1, 1, 1])[0] == 1
assert min_cost([365], [1000, 1000, 1000])[0] == 1000
full = min_cost(list(range(1, 366)), [2, 7, 15])[0]
print('every day of the year with costs [2, 7, 15]:', full)
assert full == 12 * 15 + 7                                  # twelve 30-day passes (360 days) + one 7-day pass for 5 days
assert min_cost([1, 8, 15], [10, 1, 1])[0] == 1              # one cheap 30-day pass covers all three
assert min_cost([1, 8, 15], [10, 5, 1])[0] == 1
print('edge cases ok')
