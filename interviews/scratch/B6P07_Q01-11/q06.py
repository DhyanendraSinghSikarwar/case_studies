import math
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
k, n = 17, 200
lo, hi = wilson(k, n)
print(f"red-team success {k/n:.1%}, 95% Wilson {lo:.1%} to {hi:.1%}  (rate on PLANTED emails, not production)")
assert k/n == 0.085 and round(lo, 3) == 0.054 and round(hi, 3) == 0.132
# If a prompt fix gives 0 successes in 200 new test emails: rule of three upper bound (95%)
print(f"0 of 200: upper bound about 3/200 = {3/200:.1%}; Wilson upper {wilson(0, 200)[1]:.2%}")
assert 3/200 == 0.015 and round(wilson(0, 200)[1], 4) == 0.0188
# Structural controls cut the blast radius: a hard cap on refund amount and a human approval over it (illustrative)
# 17 bad refunds with illustrative amounts; auto-refunds capped at 50, anything above goes to a human
bad = [20]*5 + [40]*5 + [80]*3 + [150]*2 + [250] + [400]
assert len(bad) == k and sum(bad) == 1490
cap = 50
auto = [a for a in bad if a <= cap]; held = [a for a in bad if a > cap]
print(f"17 bad refunds total {sum(bad)}; paid automatically under cap {cap}: {sum(auto)} ({len(auto)} refunds); sent to a human: {len(held)} refunds worth {sum(held)}")
assert (len(auto), sum(auto), len(held), sum(held)) == (10, 300, 7, 1190)
print(f"worst-case loss falls from {sum(bad)} to {sum(auto)} ({sum(auto)/sum(bad):.0%}) if the human rejects the held ones")
assert round(sum(auto)/sum(bad), 2) == 0.20
# Attempts needed: if each planted email has 8.5% chance, chance an attacker gets at least one refund in m tries
for m in (1, 10, 30):
    print(f"{m:2d} attempts -> {1-(1-0.085)**m:.1%} chance of at least one bad refund")
assert round(1-(1-0.085)**30, 3) == 0.930
