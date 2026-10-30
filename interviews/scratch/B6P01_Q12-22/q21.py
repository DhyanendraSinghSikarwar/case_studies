# Illustrative: 100,000 orders per fortnight. Cancellation counts by initiator and stage.
rows = [  # (initiator, stage, before, after)
 ("customer",   "before restaurant accepts",       1_300, 1_350),
 ("customer",   "after pickup (wrong/late)",         400,   450),
 ("restaurant", "after accept (item out of stock)",  900,   950),
 ("system",     "no delivery partner assigned",      900, 2_650),
 ("support",    "payment/other",                     500,   600),
]
n = 100_000
b = sum(r[2] for r in rows); a = sum(r[3] for r in rows)
print(f"cancel rate {b / n:.1%} -> {a / n:.1%}")
assert b == 4_000 and a == 6_000
print(f"{'initiator / stage':<46}{'before':>8}{'after':>8}{'delta pts':>10}{'share of rise':>15}")
for who, stage, x, y in rows:
    print(f"{who + ' / ' + stage:<46}{x / n:>8.1%}{y / n:>8.1%}{(y - x) / n * 100:>+10.2f}{(y - x) / (a - b):>15.0%}")
assert (2_650 - 900) / (a - b) == 0.875
# second cut: same orders by partner supply at the time of order (orders per available partner in zone-hour)
cut = {"tight supply (>=3 orders/partner)": (20_000, 1_500, 3_800),
       "balanced (<3)":                    (80_000, 2_500, 2_200)}   # (orders in each period, cancels before, cancels after); 20k/80k split assumed same both periods
for k, (m, c0, c1) in cut.items():
    print(f"{k:<36} orders {m:>6,}  cancel rate {c0 / m:.1%} -> {c1 / m:.1%}")
assert sum(v[1] for v in cut.values()) == 4_000 and sum(v[2] for v in cut.values()) == 6_000
assert round(1_500 / 20_000, 3) == 0.075 and round(3_800 / 20_000, 3) == 0.190 and round(2_200 / 80_000, 4) == 0.0275
