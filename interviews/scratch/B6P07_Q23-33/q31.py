# Model upgrade: cost per call and cost per resolution. Illustrative prices (3 in, 15 out per million), not vendor prices.
pin, pout = 3.0, 15.0
tin, told, tnew = 2000, 400, 280
assert round(1 - tnew/told, 2) == 0.30
old = tin*pin/1e6 + told*pout/1e6
new = tin*pin*1.5/1e6 + tnew*pout*1.5/1e6
print("old per call", round(old, 6), "new per call", round(new, 6), "change", f"{new/old-1:+.1%}", "abs", round(new-old, 6))
assert round(old, 6) == 0.012 and round(new, 6) == 0.0153 and round(new/old-1, 3) == 0.275
# Per 1,000,000 calls a month
print("monthly per 1M calls: old", old*1e6, "new", new*1e6)
assert round(old*1e6) == 12000 and round(new*1e6) == 15300
# Split: input unchanged in tokens, so input cost +50%; output cost = 1.5 x 0.7 = 1.05
print("input part", 0.006, "->", 0.009, "output part", 0.006, "->", round(280*22.5/1e6, 6))
assert round(280*22.5/1e6, 6) == 0.0063
# Incremental cost per extra resolved case: extra cost per call / extra resolution rate
dc, dr = new-old, 0.02
print("extra cost per extra resolved case", round(dc/dr, 3))
assert round(dc/dr, 3) == 0.165
# Cost per resolved case for a few illustrative baseline resolution rates
for r in (0.40, 0.60, 0.80):
    print(f"baseline {r:.0%}: old {old/r:.5f} new {new/(r+dr):.5f} per resolved")
# The new model is cheaper per resolved case only if baseline resolution is below this:
r_star = dr*old/dc
print("break-even baseline resolution rate", round(r_star, 4))
assert round(r_star, 4) == 0.0727
# Worth it if an extra resolution saves more than 0.165. Illustrative human cost per ticket 2.0 -> yes
print("net per 1,000 calls at human cost 2.0 per resolution:", round(1000*(dr*2.0 - dc), 2))
assert round(1000*(dr*2.0 - dc), 2) == 36.7
