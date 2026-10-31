from fractions import Fraction as Fr
import numpy as np

V = 10
win = {4: Fr(20, 100), 6: Fr(45, 100), 7: Fr(60, 100), 8: Fr(75, 100), 9: Fr(88, 100), 10: Fr(95, 100)}
surplus = {b: (V - b) * w for b, w in win.items()}
spend = {b: b * w for b, w in win.items()}
for b in win:
    print(f"bid {b:>2}: win {float(win[b]):.2f} | surplus {float(surplus[b]):.2f} | expected spend per auction {float(spend[b]):.2f} | surplus per unit spend {float(surplus[b]/spend[b]):.3f}")
best = max(surplus.values())
tied = [b for b, s in surplus.items() if s == best]
print("best surplus", float(best), "at bids", tied)
assert best == Fr(18, 10) and tied == [6, 7]
assert surplus[4] == Fr(6, 5) and surplus[8] == Fr(3, 2) and surplus[9] == Fr(22, 25) and surplus[10] == 0
# tie: the step from 6 to 7 buys 0.15 more win probability for 1.5 more spend per auction and adds zero surplus
dw = win[7] - win[6]; ds = spend[7] - spend[6]
print("6 -> 7: extra win prob", float(dw), "| extra spend per auction", float(ds), "| extra surplus", float(surplus[7] - surplus[6]))
assert dw == Fr(3, 20) and ds == Fr(3, 2)
# marginal cost per extra win: (7*0.6 - 6*0.45)/(0.6-0.45) = 10 -> equals the value, so zero surplus
print("marginal cost per extra win going 6 -> 7:", float(ds / dw))
assert ds / dw == 10
# volume view: 1,000 auctions
for b in (6, 7):
    print(f"1,000 auctions at bid {b}: wins {float(win[b]*1000):.0f}, spend {float(spend[b]*1000):.0f}, surplus {float(surplus[b]*1000):.0f}")
# interpolation is a guess, not data: linear win curve between 6 and 7 gives bid 6.5
w65 = (win[6] + win[7]) / 2
print("linear-interpolated bid 6.5:", float(w65), "surplus", float((V - Fr(13, 2)) * w65), "(untested; depends on the curve shape between the points)")
assert (V - Fr(13, 2)) * w65 == Fr(14700, 8000)
# estimating the win curve with noise: how uncertain is each estimate with n logged auctions near the bid?
rng = np.random.default_rng(38)
n = 400
for b in (6, 7):
    p = float(win[b]); se = (p * (1 - p) / n) ** 0.5
    print(f"bid {b}: with {n} auctions per point, win prob {p:.2f} +- {1.96*se:.3f}; surplus +- {1.96*se*(V-b):.3f}")
# drift alarm: a competitor shifts the curve right by 1 unit, so the old bid 7 now wins like the old bid 6
pred = float(win[7]); actual = float(win[6])
z = (actual - pred) / (pred * (1 - pred) / n) ** 0.5
print("bid 7 predicted win", pred, "live win", actual, "| z with", n, "live auctions:", round(z, 1))
assert round(z, 1) == -6.1
# what the shift does to the best bid: shifted curve, same value 10
sh = {b + 1: w for b, w in win.items()}              # bids 5, 7, 8, 9, 10, 11 carry the old win rates
sh_s = {b: (V - b) * w for b, w in sh.items() if b <= V}
print("shifted-curve surplus by bid:", {b: float(s_) for b, s_ in sh_s.items()})
print("best shifted bids:", [b for b, s_ in sh_s.items() if s_ == max(sh_s.values())], "with surplus", float(max(sh_s.values())))
assert max(sh_s.values()) == Fr(27, 20) and [b for b, s_ in sh_s.items() if s_ == Fr(27, 20)] == [7]
