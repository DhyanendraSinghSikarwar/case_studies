# Q29 price increase and churn: DiD and 12-month revenue (illustrative numbers)
subs0 = 100_000
old_price, new_price = 199, 249
# difference-in-differences: treated users saw the new price, a control region still on old price
treated_before, treated_after = 0.030, 0.045
control_before, control_after = 0.030, 0.034
did = (treated_after - treated_before) - (control_after - control_before)
print("raw churn change pts:", round((treated_after - treated_before) * 100, 2), " DiD price effect pts:", round(did * 100, 2))
assert round(did * 100, 2) == 1.10

def year_revenue(price, churn_by_month, subs=subs0):
    total = 0.0
    for c in churn_by_month:
        total += subs * price          # revenue from subscribers active this month
        subs *= (1 - c)                # churn at month end (closed cohort, no new adds)
    return total

old = year_revenue(old_price, [0.03] * 12)
persist = year_revenue(new_price, [0.045] * 12)
# price effect only: churn at 4.5% for 3 months then back to 3%
revert = year_revenue(new_price, [0.045] * 3 + [0.03] * 9)
# DiD view: only 3.0% + 1.1 pts = 4.1% is due to price; the rest is seasonality that hits old price too
did_view = year_revenue(new_price, [0.041] * 12)
old_season = year_revenue(old_price, [0.034] * 12)
for name, v in [("old price, 3.0% churn", old), ("new price, 4.5% persists", persist),
                ("new price, 4.5% for 3 months then 3.0%", revert),
                ("new price, 4.1% (DiD price effect)", did_view), ("old price, 3.4% (seasonal baseline)", old_season)]:
    print(f"{name:42} Rs {v/1e6:8.2f} m   vs old {v/old - 1:+.1%}")
assert persist > old and revert > persist and did_view > persist
assert round(persist / old - 1, 3) == 0.157 and round(revert / old - 1, 3) == 0.205
assert round(did_view / old - 1, 3) == 0.181 and round(old_season / old - 1, 3) == -0.021
# breakeven constant monthly churn at which 12-month revenue equals the old plan
lo, hi = 0.03, 0.30
for _ in range(60):
    mid = (lo + hi) / 2
    if year_revenue(new_price, [mid] * 12) > old:
        lo = mid
    else:
        hi = mid
print("breakeven monthly churn at new price:", round(lo, 4))
assert 0.07 < lo < 0.10

# lifetime view (simple geometric lifetime = price / churn, per subscriber, undiscounted)
ltv_old, ltv_new = old_price / 0.03, new_price / 0.045
print("LTV old:", round(ltv_old), " LTV new:", round(ltv_new), " change:", round(ltv_new / ltv_old - 1, 3))
assert round(ltv_old) == 6633 and round(ltv_new) == 5533 and round(ltv_new / ltv_old - 1, 3) == -0.166
