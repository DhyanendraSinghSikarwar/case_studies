# Q39: host-level pricing tool in a market with roughly fixed guest demand. Illustrative, seeded.
import numpy as np

print("relative lift:", round(10.8 / 10.0 - 1, 3))
assert round(10.8 / 10.0 - 1, 3) == 0.08
tot = 5000 * 10.8 + 5000 * 10.0
print("if demand is fixed, everyone-treated or nobody-treated average =", tot / 10_000)
assert tot / 10_000 == 10.4            # market average bookings per listing is 10.4 either way
print(f"treated gain over market average {10.8-10.4:+.1f}, control loss {10.0-10.4:+.1f}: the gap of 0.8 is all redistribution")

rng = np.random.default_rng(39)
C, N_PER = 40, 250                      # 40 cities, 250 listings each = 10,000 hosts
gamma = np.log(1.08)                    # treated listings are 8% more attractive to guests

def city_bookings(frac_treated, eps, Dper, treated_mask):
    """Guests split across listings in proportion to attractiveness w; city demand grows with mean w**eps."""
    w = np.where(treated_mask, np.exp(gamma), 1.0)
    D = Dper * N_PER * (w.mean() ** eps)
    return rng.poisson(D * w / w.sum())

def host_level(eps):
    diffs = []
    for _ in range(30):
        c = []; t = []
        for _ in range(C):
            m = np.zeros(N_PER, bool); m[: N_PER // 2] = True
            b = city_bookings(0.5, eps, 10.4 * rng.lognormal(0, 0.3), m)
            t.append(b[m].mean()); c.append(b[~m].mean())
        diffs.append(np.mean(t) / np.mean(c) - 1)
    return np.mean(diffs)

def city_level(eps, reps=400):
    est, adj = [], []
    for _ in range(reps):
        treated_city = rng.permutation(C) < C // 2
        tt, cc, tt2, cc2 = [], [], [], []
        for i in range(C):
            Dper = 10.4 * rng.lognormal(0, 0.3)
            m = np.full(N_PER, bool(treated_city[i]))
            b = city_bookings(1.0, eps, Dper, m)
            pre = rng.poisson(Dper * N_PER) / N_PER          # same city, month before launch
            (tt if treated_city[i] else cc).append(b.mean())
            (tt2 if treated_city[i] else cc2).append(b.mean() / pre)
        est.append(np.mean(tt) / np.mean(cc) - 1)
        adj.append(np.mean(tt2) / np.mean(cc2) - 1)
    return np.mean(est), np.std(est), np.mean(adj), np.std(adj)

for eps in (0.0, 0.25):
    h = host_level(eps)
    m, s, ma, sa = city_level(eps)
    print(f"demand elasticity {eps}: host-level estimate {h:+.1%};  city-level estimate {m:+.1%} (sd {s:.1%});  city-level vs own pre-period {ma:+.1%} (sd {sa:.1%})")
    assert sa < s / 3
    assert abs(ma - (1.08 ** eps - 1)) < 0.01
    if eps == 0.0:
        assert abs(h - 0.08) < 0.01 and abs(m) < 0.03
    else:
        assert abs(h - 0.08) < 0.01 and 0.0 < m < 0.06      # true market effect is 1.08**0.25 - 1
print("true market effect with elasticity 0.25:", f"{1.08**0.25-1:+.1%}")
