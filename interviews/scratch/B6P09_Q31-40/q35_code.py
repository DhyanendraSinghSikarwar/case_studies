items_n, subs_n = 1000, 4000
p0, p1, ps = 500, 450, 500
u0, u1 = 100_000, 120_000
s0, s1 = 240_000, 228_000
assert p1 == p0 * 0.9 and u1 == u0 * 1.2 and s1 == s0 * 0.95
rev_i0, rev_i1 = u0 * p0, u1 * p1
rev_s0, rev_s1 = s0 * ps, s1 * ps
d_i, d_s = rev_i1 - rev_i0, rev_s1 - rev_s0
print("test items revenue/day", rev_i0, "->", rev_i1, "change", d_i, f"({d_i/rev_i0:+.1%})")
print("substitutes revenue/day", rev_s0, "->", rev_s1, "change", d_s, f"({d_s/rev_s0:+.1%})")
print("category change", d_i + d_s, f"({(d_i+d_s)/(rev_i0+rev_s0):+.2%} of {rev_i0+rev_s0})")
assert d_i == 4_000_000 and d_s == -6_000_000 and d_i + d_s == -2_000_000
assert rev_i0 + rev_s0 == 170_000_000 and rev_i1 + rev_s1 == 168_000_000
# decomposition of the item-level change
price_effect = u0 * (p1 - p0)            # old units at the new price
volume_effect = (u1 - u0) * p1           # extra units at the new price
print("price effect on old units", price_effect, "| revenue from extra units", volume_effect)
assert price_effect == -5_000_000 and volume_effect == 9_000_000 and price_effect + volume_effect == d_i
# units
extra, lost = u1 - u0, s0 - s1
print("extra units on test items", extra, "| units lost on substitutes", lost, "| share of extra units that is cannibalised", lost / extra, "| net category units", extra - lost)
assert extra == 20000 and lost == 12000 and lost / extra == 0.6 and extra - lost == 8000
elas = (u1 / u0 - 1) / (p1 / p0 - 1)
cross = (s1 / s0 - 1) / (p1 / p0 - 1)
print("own elasticity", round(elas, 2), "| cross elasticity", round(cross, 2))
assert round(elas, 2) == -2.0 and round(cross, 2) == 0.5
# break-even: what substitute loss makes the category revenue-neutral?
lost_even = d_i / ps
print("category revenue-neutral if substitutes lose", lost_even, "units/day (", round(lost_even / s0 * 100, 2), "% of their units )")
assert lost_even == 8000
# margin view: invented unit cost 300 (illustrative)
c = 300
m0 = u0 * (p0 - c) + s0 * (ps - c)
m1 = u1 * (p1 - c) + s1 * (ps - c)
print("margin/day at unit cost", c, ":", m0, "->", m1, "change", m1 - m0)
assert (m1 - m0) == -4_400_000

# why item-level randomisation overstates: toy logit-share category (invented), half the items get -10%
e, eta = 2.0, 0.3                     # item share elasticity, category elasticity to the price index
def category(frac_treated, n=2000, Q0=200_000):
    w_t, w_c = 0.9 ** (-e), 1.0
    nt = int(n * frac_treated); nc = n - nt
    W = nt * w_t + nc * w_c
    pidx = (nt * 0.9 + nc * 1.0) / n   # simple average price index
    Q = Q0 * pidx ** (-eta)
    ut = Q * w_t / W if nt else 0; uc = Q * w_c / W if nc else 0
    return nt, nc, ut, uc, Q
nt, nc, ut, uc, Q = category(0.5)
base_u = 200_000 / 2000
print("item-randomised: treated item units", round(ut, 1), "control item units", round(uc, 1), "baseline", base_u)
naive = ut / uc - 1
print("naive treated-vs-control unit lift", round(naive, 3))
nt2, nc2, ut2, uc2, Q2 = category(1.0)
true_all = Q2 / 200_000 - 1
print("true category unit lift if every item were cut by 10%", round(true_all, 3), "| control items vs their own baseline", round(uc / base_u - 1, 3))
assert round(naive, 3) == 0.235 and round(true_all, 3) == 0.032 and uc / base_u - 1 < 0
