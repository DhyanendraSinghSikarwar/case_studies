tasks, capped, cap, avg_other = 20_000, 600, 25, 6
other = tasks - capped
assert other == 19_400 and capped / tasks == 0.03
s_cap, s_oth = capped * cap, other * avg_other
share = s_cap / (s_cap + s_oth)
print(f"steps: capped {s_cap:,}, others {s_oth:,}, total {s_cap+s_oth:,}; capped share {share*100:.1f}%")
assert (s_cap, s_oth) == (15_000, 116_400) and round(share * 100, 1) == 11.4
# If every step re-sends the whole history (equal tokens added per step), input tokens of a k-step task ~ k(k+1)/2 units.
tri = lambda k: k * (k + 1) // 2
c_cap, c_oth = capped * tri(cap), other * tri(6)
sh2 = c_cap / (c_cap + c_oth)
print(f"history-resend model: capped task {tri(cap)} units vs 6-step task {tri(6)} units = {tri(cap)/tri(6):.1f}x")
print(f"capped share of input tokens <= {sh2*100:.1f}% (treats 'average 6' as exactly 6; spread would lower this share)")
assert (tri(25), tri(6)) == (325, 21) and round(tri(25) / tri(6), 1) == 15.5 and round(sh2 * 100, 1) == 32.4
# Convexity check: spreading steps around a mean of 6 raises others' cost, so the capped share only falls.
import numpy as np
rng = np.random.default_rng(3)
steps = rng.poisson(6, other)
steps = np.clip(steps, 1, 24)
c_oth2 = float((steps * (steps + 1) // 2).sum())
sh3 = c_cap / (c_cap + c_oth2)
print(f"with Poisson(6) spread: others' mean steps {steps.mean():.2f}, capped share {sh3*100:.1f}%")
assert sh3 < sh2
