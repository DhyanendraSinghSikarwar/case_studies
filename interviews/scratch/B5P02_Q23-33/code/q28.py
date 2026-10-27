import random


def cards_brute(cards, k):
    # i cards from the left, k-i from the right
    best = 0
    for i in range(k + 1):
        left = sum(cards[:i])
        right = sum(cards[len(cards) - (k - i):]) if k - i else 0
        best = max(best, left + right)
    return best


def cards_window(cards, k):
    # view 1: the cards left behind form one window of size n-k; minimise it
    n = len(cards)
    m = n - k
    window = sum(cards[:m])
    low = window
    for r in range(m, n):
        window += cards[r] - cards[r - m]
        low = min(low, window)
    return sum(cards) - low


def cards_split(cards, k):
    # view 2: start with k from the left, then trade one left card for one right card
    cur = sum(cards[:k])
    best = cur
    for i in range(1, k + 1):
        cur += cards[-i] - cards[k - i]
        best = max(best, cur)
    return best


print("[1,2,3,4,5,6,1], 3:", cards_window([1, 2, 3, 4, 5, 6, 1], 3), cards_split([1, 2, 3, 4, 5, 6, 1], 3), "(expected 12)")
print("[2,2,2], 2:", cards_window([2, 2, 2], 2), cards_split([2, 2, 2], 2), "(expected 4)")
print("[9,7,7,9,7,7,9], 7:", cards_window([9, 7, 7, 9, 7, 7, 9], 7), cards_split([9, 7, 7, 9, 7, 7, 9], 7), "(expected 55)")

random.seed(28)
for _ in range(1000):
    n = random.randint(1, 10)
    cards = [random.randint(0, 9) for _ in range(n)]
    k = random.randint(1, n)
    b = cards_brute(cards, k)
    assert cards_window(cards, k) == b == cards_split(cards, k), (cards, k)
print("cross-check: 1000 seeded cases agree")

assert cards_window([5], 1) == 5
assert cards_split([5], 1) == 5
assert cards_window([1, 2, 3], 3) == 6  # k = n: empty middle window, take everything
assert cards_split([1, 2, 3], 3) == 6
assert cards_window([1, 2, 3], 1) == 3
assert cards_window([0, 0, 0], 2) == 0
big = [random.randint(0, 10 ** 4) for _ in range(10 ** 5)]
assert cards_window(big, 10 ** 5) == sum(big)
assert cards_window(big, 5 * 10 ** 4) == cards_split(big, 5 * 10 ** 4)
print("edge asserts passed")
