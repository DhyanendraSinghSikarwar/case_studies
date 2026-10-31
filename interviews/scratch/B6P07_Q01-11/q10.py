PIN, POUT = 3.0, 15.0          # illustrative, per million tokens
tin, tout = 2000, 400          # millions of tokens per month
api = tin*PIN + tout*POUT
print(f"API bill: input {tin*PIN:,.0f} + output {tout*POUT:,.0f} = {api:,.0f} per month")
assert (tin*PIN, tout*POUT, api) == (6000, 6000, 12000)
fixed, cap = 15_000, 2.0
be = fixed / api
print(f"break-even volume: {fixed:,}/{api:,} = {be:.2f}x today's; capacity limit {cap:.0f}x")
assert be == 1.25 and be < cap
print(f"today: self-host costs {fixed-api:,} more than API; at 2x volume API would cost {2*api:,} vs {fixed:,} -> saves {2*api-fixed:,}")
assert fixed - api == 3000 and 2*api - fixed == 9000
# Sensitivity: API price falls 30% (illustrative)
cut = 0.30; api_cut = api*(1-cut); be_cut = fixed/api_cut
print(f"if API prices fall {cut:.0%}: bill {api_cut:,.0f}, break-even {be_cut:.2f}x (above the {cap:.0f}x capacity? {be_cut > cap})")
assert round(api_cut) == 8400 and round(be_cut, 2) == 1.79 and be_cut < cap
# Peak vs average: if peak traffic is 3x average, capacity '2x current volume' (average) may not cover peaks
avg_cap_ok = 2.0; peak_ratio = 3.0
print(f"capacity covers {avg_cap_ok:.0f}x of today's average; if peak/average is {peak_ratio:.0f}x, today's peak already uses {peak_ratio/avg_cap_ok:.0%} of it")
assert peak_ratio/avg_cap_ok == 1.5
# Utilisation view: self-host only wins above 1.25x; what share of the 2x capacity is that?
print(f"break-even utilisation of capacity: {be/cap:.1%}"); assert round(be/cap, 4) == 0.625
# Cost per million tokens at various volumes (blended: 2400 M tokens => 12000, 5.0 per M)
blend = api/(tin+tout); print(f"API blended price {blend:.2f} per million; self-host at 1x: {fixed/(tin+tout):.2f}, at 2x: {fixed/(2*(tin+tout)):.2f}")
assert blend == 5.0 and round(fixed/(tin+tout), 2) == 6.25 and round(fixed/(2*(tin+tout)), 2) == 3.12
