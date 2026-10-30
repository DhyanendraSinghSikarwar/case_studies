# Illustrative numbers. Brand X margin 3.00 per unit at full price, promotion gives 1.00 off on every unit.
base, m_full, off = 6000, 3.00, 1.00
promo_units, post = 10000, [5000, 5400]
m_promo = m_full - off
print("promo lift", f"{promo_units/base-1:+.1%}")
assert round(promo_units / base - 1, 3) == 0.667
base_margin = base * m_full
wk0 = promo_units * m_promo - base_margin
wk1 = post[0] * m_full - base_margin
wk2 = post[1] * m_full - base_margin
x_net = wk0 + wk1 + wk2
print(f"X promo week {wk0:+,.0f}, week+1 {wk1:+,.0f}, week+2 {wk2:+,.0f}, X net {x_net:+,.0f}")
assert (wk0, wk1, wk2, x_net) == (2000, -3000, -1800, -2800)
y_loss = -1000 * 2.50
total = x_net + y_loss
print(f"Brand Y {y_loss:+,.0f}; total over 3 weeks {total:+,.0f}")
assert (y_loss, total) == (-2500, -5300)
# Unit view
extra = promo_units - base; pull = (base - post[0]) + (base - post[1])
print(f"extra units in promo {extra}, pulled forward {pull}, net extra units for X {extra-pull}")
assert (extra, pull, extra - pull) == (4000, 1600, 2400)
# Break-even in the promo week alone (no halo, no dip): units needed so that units*2 = 6000*3
be = base * m_full / m_promo
print("promo-week break-even units:", be)
assert be == 9000
# Subsidy paid to people who would have bought anyway
print("discount given away on baseline units:", base * off)
assert base * off == 6000
# Break-even if two post weeks dip is as observed and Y loses 1,000: units needed in promo week
need = (base_margin + 3000 + 1800 + 2500) / m_promo
print("promo-week units needed to break even over 3 weeks incl. dips and Y:", need)
assert need == 12650
