import math
def wil(k, n, z=1.96):
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h
k, n, N = 78, 100, 500
lo, hi = wil(k, n)
print(f"valid rate {k/n:.2f}, Wilson 95% {lo:.4f} to {hi:.4f}")
assert 0.688 < lo < 0.690 and 0.849 < hi < 0.851
print(f"naive projection over 500: {N*lo:.0f} to {N*hi:.0f} valid")
assert round(N*lo) == 345 and round(N*hi) == 425
rest = N - n
a, b = k + rest*lo, k + rest*hi
print(f"reviewed 100 are known: 78 + {rest} x interval = {a:.0f} to {b:.0f} valid")
assert round(a) == 354 and round(b) == 418
fpc = math.sqrt(1 - n/N)
print(f"finite-population factor on the standard error = {fpc:.3f}")
assert abs(fpc - 0.894) < 0.001
# how many more to review to halve the interval width roughly
w = hi - lo
for m in (100, 200, 400):
    l2, h2 = wil(round(0.78*m), m)
    print(f"n={m}: width {h2-l2:.3f}")
assert (wil(312, 400)[1]-wil(312, 400)[0]) < 0.6*w
# invalid questions to drop if used as a test set
print(f"expected invalid among 500: {N*(1-k/n):.0f} (range {N*(1-hi):.0f} to {N*(1-lo):.0f})")
assert round(N*(1-k/n)) == 110
