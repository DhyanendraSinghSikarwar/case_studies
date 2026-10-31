import random


def profit_brute(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


def profit_one_pass(prices):
    lowest = prices[0]
    best = 0
    for p in prices[1:]:
        if p < lowest:
            lowest = p             # new buy candidate (left edge jumps here)
        elif p - lowest > best:
            best = p - lowest      # selling today beats the best so far
    return best


print(profit_one_pass([7, 1, 5, 3, 6, 4]))
print(profit_one_pass([7, 6, 4, 3, 1]))
assert profit_one_pass([7, 1, 5, 3, 6, 4]) == 5
assert profit_one_pass([7, 6, 4, 3, 1]) == 0
assert profit_one_pass([5]) == 0                 # single day
assert profit_one_pass([3, 3, 3]) == 0           # all equal
assert profit_one_pass([1, 2]) == 1
assert profit_one_pass([2, 1]) == 0
assert profit_one_pass([2, 4, 1]) == 2           # min comes after the peak: must not use it
assert profit_one_pass(list(range(100000))) == 99999

rng = random.Random(8)
cases = 0
for _ in range(3000):
    n = rng.randint(1, 10)
    prices = [rng.randint(0, 12) for _ in range(n)]
    assert profit_one_pass(prices) == profit_brute(prices), prices
    cases += 1
print("random cross-check passed:", cases, "cases")
