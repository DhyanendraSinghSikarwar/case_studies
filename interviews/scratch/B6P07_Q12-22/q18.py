import math
def two_prop(p1, n1, p2, n2):
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    return d, se, d / se, d - 1.96 * se, d + 1.96 * se
d, se, z, lo, hi = two_prop(0.61, 20_000, 0.615, 20_000)
print(f"online: +{d*100:.1f} pts, SE {se*100:.2f}, z {z:.2f}, 95% CI {lo*100:.2f} to {hi*100:.2f} pts (assumes independent conversations)")
assert round(se * 100, 2) == 0.49 and round(z, 2) == 1.03 and (round(lo * 100, 2), round(hi * 100, 2)) == (-0.45, 1.45)
d2, se2, z2, lo2, hi2 = two_prop(0.82, 1000, 0.86, 1000)
print(f"offline (unpaired view): +{d2*100:.0f} pts, SE {se2*100:.2f}, z {z2:.2f}, 95% CI {lo2*100:.1f} to {hi2*100:.1f} pts")
assert round(z2, 2) == 2.44 and (round(lo2 * 100, 1), round(hi2 * 100, 1)) == (0.8, 7.2)
print(f"offline +4 sits above the online upper limit +{hi*100:.2f}: {0.04 > hi}")
assert 0.04 > hi
# Mix effect: offline set 50% hard / 50% easy, gain only on hard items (+8). Online traffic is 10% hard.
gain_hard = 8.0
off = 0.5 * gain_hard; on = 0.1 * gain_hard
print(f"mix effect: offline gain {off:.1f} pts, online gain {on:.1f} pts")
assert off == 4.0 and abs(on - 0.8) < 1e-9
# Clustering: conversations come from users; a design effect of 2 inflates the online SE by sqrt(2).
deff = 2.0
print(f"with design effect {deff:.0f}: online SE {se*math.sqrt(deff)*100:.2f} pts, CI upper {(d+1.96*se*math.sqrt(deff))*100:.2f}")
assert round(se * math.sqrt(deff) * 100, 2) == 0.69
