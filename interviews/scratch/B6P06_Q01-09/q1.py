# Q1: cumulative lift by end of week 12 (illustrative numbers; lift counted per full week after launch)
full, base = 100_000, 60_000          # weekly lift: full model, rules baseline
wait = full * (12 - 10)               # full model live after week 10 -> weeks 11, 12
plan = base * (12 - 6)                # baseline live after week 6 -> weeks 7..12; swap lands in week 12, full from week 13
print("wait for full model:", wait)
print("baseline first     :", plan, " difference:", plan - wait)
assert wait == 200_000 and plan == 360_000 and plan - wait == 160_000

# long run: after week 12 both earn 100k a week, so the 160k lead stays
for wk in (12, 16, 20):
    w = full * (wk - 10)
    p = base * 6 + full * (wk - 12)
    print(f"week {wk}: wait {w:,} vs baseline-first {p:,}  (lead {p-w:,})")
    assert p - w == 160_000

# how weak can the baseline be before waiting wins at week 12?
be = wait / 6
print(f"break-even baseline lift per week: {be:,.0f}")
assert round(be) == 33_333
# if the swap slips a further 4 weeks (to week 16) the baseline plan still leads at week 16?
p16 = base * (16 - 6)
w16 = full * (16 - 10)
print("swap slips to week 16: baseline-first at wk16", p16, "vs wait", w16)
assert p16 == 600_000 and w16 == 600_000   # exactly level at week 16
