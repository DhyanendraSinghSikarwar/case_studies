# Q40: what does 148/200 really say? Wilson interval + routing example (illustrative)
from math import sqrt
def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 148, 200
lo, hi = wilson(k, n)
print(f"overall {k}/{n} = {k/n:.0%}, 95% Wilson CI [{lo:.3f}, {hi:.3f}]")
assert k / n == 0.74 and hi < 0.95            # even the top of the interval misses 95%
print("wrong answers per 1,000 questions: tool", round(1000*(1-k/n)), "vs target", round(1000*0.05))
# by tier (invented split that adds up to 148/200)
simple_k, simple_n = 114, 120
hard_k, hard_n = 34, 80
assert simple_k + hard_k == k and simple_n + hard_n == n
for name, kk, nn in [("simple/certified-metric", simple_k, simple_n), ("open-ended", hard_k, hard_n)]:
    l, h = wilson(kk, nn)
    print(f"{name:24} {kk}/{nn} = {kk/nn:.1%}  CI [{l:.3f}, {h:.3f}]")
# how many all-correct trials would prove >=95% lower bound? smallest n with 0 errors
m = 1
while wilson(m, m)[0] < 0.95: m += 1
print("smallest all-correct run whose lower bound reaches 95% =", m)
assert wilson(m, m)[0] >= 0.95 > wilson(m-1, m-1)[0]
