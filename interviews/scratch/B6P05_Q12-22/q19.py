# Illustrative numbers.
build, cm, orders = 120_000, 2.50, 30_000
be_orders = build / cm
months = be_orders / orders
print(f"break-even orders {be_orders:,.0f}; months at {orders:,}/month: {months:.2f}")
assert be_orders == 48_000 and round(months, 2) == 1.60
# Sensitivity: monthly extra orders x contribution per order (months to break even)
print("months to break even (rows: extra orders/month; cols: contribution per order)")
cms = [1.50, 2.00, 2.50]
print("orders   " + "  ".join(f"{c:5.2f}" for c in cms))
for o in [10_000, 15_000, 20_000, 30_000]:
    print(f"{o:6,}   " + "  ".join(f"{build/(o*c):5.1f}" for c in cms))
assert round(build / (15_000 * 2.50), 1) == 3.2 and round(build / (10_000 * 1.50), 1) == 8.0
# Cannibalisation: if 40% of the 30,000 would have happened anyway, only 18,000 are incremental
inc = 30_000 * 0.60
print(f"incremental orders {inc:,.0f}; months {build/(inc*cm):.2f}")
assert inc == 18_000 and round(build / (inc * cm), 2) == 2.67
# A ramp: 10,000, 20,000, 30,000 then flat; cumulative contribution
cum, m, vols = 0.0, 0, [10_000, 20_000] + [30_000] * 10
for v in vols:
    m += 1; cum += v * cm
    if cum >= build:
        prev = cum - v * cm
        print(f"with a 3-month ramp break-even falls in month {m} (about {m-1+(build-prev)/(v*cm):.2f} months)")
        break
assert m == 3
# Ongoing run cost: 15,000 a month of upkeep delays things
net_month = 30_000 * cm - 15_000
print(f"with 15,000/month upkeep: {build/net_month:.2f} months")
assert round(build / net_month, 2) == 2.00
