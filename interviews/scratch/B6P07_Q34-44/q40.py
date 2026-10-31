import math

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

# Illustrative numbers from the prompt
k, n, monthly = 20, 500, 30_000
p = k / n
lo, hi = wilson(k, n)
print(f"rate {p:.1%}; Wilson 95% [{lo:.2%}, {hi:.2%}]")
assert p == 0.04 and 0.0259 < lo < 0.0262 and 0.0609 < hi < 0.0612

print(f"monthly wrong writes: point {p*monthly:.0f}, range {lo*monthly:.0f} to {hi*monthly:.0f}")
assert round(p * monthly) == 1200 and 780 < lo * monthly < 783 and 1828 < hi * monthly < 1831

# Normal-approximation interval for comparison (it is similar here, but worse for small rates)
se = math.sqrt(p * (1 - p) / n)
print(f"Wald 95% [{p-1.96*se:.2%}, {p+1.96*se:.2%}]")
assert round(p - 1.96 * se, 4) == 0.0228 and round(p + 1.96 * se, 4) == 0.0572

# Even the lowest end of the interval is hundreds of wrong writes a month. Layered controls (illustrative):
approve_catch = 0.90     # human approval catches 90% of wrong writes it is shown (invented)
residual = p * monthly * (1 - approve_catch)
print(f"if approval catches 90%, residual point estimate: {residual:.0f} a month")
assert round(residual) == 120

# How many clean staged runs would you need to claim the rate is below 0.1% (rule of three)?
need = math.ceil(3 / 0.001)
print("clean runs needed for a 95% upper bound of 0.1%:", need)
assert need == 3000

# Chance of at least one wrong write in a week of 7,000 writes at the lower bound (independence assumed)
week = 7_000
print("P(at least one wrong write in a week at 2.6%):", 1 - (1 - lo) ** week)
assert 1 - (1 - lo) ** week > 0.999999

# Example numbers quoted in the text (illustrative cost of 20 per wrong write)
assert round(p * monthly) * 20 == 24_000 and round(residual) * 20 == 2_400
