# Q40: sessions/user +10%, revenue/session -4%, revenue/user +5.6%. Illustrative, seeded.
import numpy as np

print("1.10 x 0.96 =", round(1.10 * 0.96, 3))
assert round(1.10 * 0.96, 3) == 1.056

rng = np.random.default_rng(40)
U = 100_000
def arm(mean_sessions, rev_per_session):
    # users differ in activity (gamma), sessions ~ Poisson; each session's revenue is zero-inflated and skewed
    act = rng.gamma(2.0, mean_sessions / 2.0, U)
    s = rng.poisson(act)
    rev = np.array([0.0] * U)
    tot = s.sum()
    per = np.where(rng.random(tot) < 0.1, rng.exponential(rev_per_session * 10, tot), 0.0)
    idx = np.repeat(np.arange(U), s)
    rev = np.bincount(idx, weights=per, minlength=U)
    return s, rev
sc, rc = arm(5.0, 2.00)
st, rt = arm(5.5, 1.92)

spu = st.mean() / sc.mean() - 1
rps = (rt.sum() / st.sum()) / (rc.sum() / sc.sum()) - 1
rpu = rt.mean() / rc.mean() - 1
print(f"sessions/user {spu:+.1%}   revenue/session (ratio of sums) {rps:+.1%}   revenue/user {rpu:+.1%}")
assert abs(spu - 0.10) < 0.02 and abs(rps + 0.04) < 0.03
# identity: revenue/user = sessions/user x revenue/session when the ratio is a ratio of sums
assert abs((1 + rpu) - (1 + spu) * (1 + rps)) < 1e-9

# interval for revenue per user: difference in means, user is the unit
d = rt.mean() - rc.mean()
se = np.sqrt(rt.var(ddof=1) / U + rc.var(ddof=1) / U)
print(f"revenue/user diff {d:.3f}, 95% CI [{d-1.96*se:.3f}, {d+1.96*se:.3f}]  = [{(d-1.96*se)/rc.mean():+.1%}, {(d+1.96*se)/rc.mean():+.1%}] relative")
assert d - 1.96 * se > 0
# delta-method SE of the ratio-of-sums revenue/session vs naive per-session SE
def ratio_se(num, den):
    r = num.sum() / den.sum(); m = den.mean()
    z = (num - r * den) / m
    return r, np.sqrt(z.var(ddof=1) / len(num))
rr, se_delta = ratio_se(rc, sc)
# naive: treat sessions as independent draws: need per-session values
print(f"control revenue/session {rr:.3f}, delta-method SE {se_delta:.4f}")
# mean of per-user ratios is a different quantity
mask_c, mask_t = sc > 0, st > 0
mor_c = (rc[mask_c] / sc[mask_c]).mean(); mor_t = (rt[mask_t] / st[mask_t]).mean()
print(f"mean of per-user ratios: {mor_t/mor_c-1:+.1%} (a different number from the ratio of sums {rps:+.1%})")
# a mix-shift check: the extra sessions are lower value than the existing ones
extra_sessions = st.sum() - sc.sum(); extra_rev = rt.sum() - rc.sum()
print(f"extra sessions {extra_sessions:,.0f}, extra revenue {extra_rev:,.0f} -> {extra_rev/extra_sessions:.2f} per extra session vs {rc.sum()/sc.sum():.2f} existing average")
assert extra_rev > 0
