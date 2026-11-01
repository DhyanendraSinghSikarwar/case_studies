import random


class StockSpannerBrute:
    def __init__(self):
        self.prices = []

    def next(self, price):
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):      # walk back while price <= today's
            if p > price:
                break
            span += 1
        return span


class StockSpanner:
    def __init__(self):
        self.stack = []                      # (price, span), prices strictly decreasing bottom to top

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]      # absorb the whole span of a smaller-or-equal price
        self.stack.append((price, span))
        return span


def run(cls, prices):
    s = cls()
    return [s.next(p) for p in prices]


examples = [([100, 80, 60, 70, 60, 75, 85], [1, 1, 1, 2, 1, 4, 6]), ([7, 7, 7], [1, 2, 3])]
for prices, want in examples:
    got = run(StockSpanner, prices)
    assert got == run(StockSpannerBrute, prices) == want, (prices, got)
    print(prices, "->", got)

assert run(StockSpanner, []) == []
assert run(StockSpanner, [5]) == [1]
assert run(StockSpanner, [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]     # increasing: span grows
assert run(StockSpanner, [5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]     # decreasing: always 1
assert run(StockSpanner, [3, 3, 3, 3]) == [1, 2, 3, 4]           # ties are included
n = 10000
assert run(StockSpanner, list(range(n))) == list(range(1, n + 1))  # max calls
assert run(StockSpanner, [10 ** 5] * n)[-1] == n

# the same numbers as "distance to previous strictly greater element"
prices = [100, 80, 60, 70, 60, 75, 85]
prev_greater, st, spans = [], [], []
for i, p in enumerate(prices):
    while st and prices[st[-1]] <= p:
        st.pop()
    prev_greater.append(st[-1] if st else -1)
    st.append(i)
    spans.append(i - prev_greater[-1])
assert spans == run(StockSpanner, prices)
print("span = i - (index of previous strictly greater price):", spans)

rng = random.Random(18)
cases = 0
for _ in range(2000):
    prices = [rng.randint(1, rng.choice([3, 6, 20])) for _ in range(rng.randint(0, 25))]
    assert run(StockSpanner, prices) == run(StockSpannerBrute, prices), prices
    cases += 1
print("random cross-check passed:", cases, "price streams")
