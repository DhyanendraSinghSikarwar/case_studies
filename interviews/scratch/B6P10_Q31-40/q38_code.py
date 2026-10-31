import math
from statistics import NormalDist
save, loss, k, n = 800, 20_000, 388, 400
p_be = loss / (save + loss)
acc = k / n
print("break-even accuracy", round(p_be, 5), "sample accuracy", acc)
assert round(p_be, 5) == 0.96154 and acc == 0.97
ev = lambda p: save * p - loss * (1 - p)
print("EV per incident at 97%", ev(0.97), "at break-even", round(ev(p_be), 6))
assert round(ev(0.97), 2) == 176.0 and abs(ev(p_be)) < 1e-9
# Wilson 95% interval for 388/400
z = NormalDist().inv_cdf(0.975)
c = (acc + z * z / (2 * n)) / (1 + z * z / n)
h = z * math.sqrt(acc * (1 - acc) / n + z * z / (4 * n * n)) / (1 + z * z / n)
lo, hi = c - h, c + h
print("Wilson 95%", round(lo, 4), round(hi, 4), "EV at lower end", round(ev(lo), 1))
assert lo < p_be < hi and ev(lo) < 0
# exact binomial: chance of seeing >= 388 right if the true accuracy were exactly break-even
def sf(n, k, p):
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))
pv = sf(n, k, p_be)
print("P(>=388 of 400 | p=break-even)", round(pv, 3))
assert 0.2 < pv < 0.4
# errors budget: at 97%, 12 wrong of 400; each costs 20,000
print("wrong in sample", n - k, "cost", (n - k) * loss, "savings", k * save, "net", k * save - (n - k) * loss)
assert (n - k) * loss == 240_000 and k * save == 310_400 and k * save - (n - k) * loss == 70_400
# accuracy needed if the loss were capped at 5,000 by a guardrail (e.g. blast-radius limit)
print("break-even if wrong costs 5,000:", round(5000 / (save + 5000), 4))
assert round(5000 / 5800, 4) == 0.8621
# sample size to put the lower bound above break-even if true accuracy is 0.98 (rough)
for m in (400, 1000, 2000):
    c = (0.98 + z * z / (2 * m)) / (1 + z * z / m)
    h = z * math.sqrt(0.98 * 0.02 / m + z * z / (4 * m * m)) / (1 + z * z / m)
    print("n", m, "lower bound at 98% observed", round(c - h, 4), "above break-even:", c - h > p_be)
