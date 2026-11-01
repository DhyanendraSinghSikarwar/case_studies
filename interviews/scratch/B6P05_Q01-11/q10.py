T = 60_000
human, ai, esc, reopen_cost, fee = 5.00, 0.20, 5.50, 5.00, 40_000
res_rate, reopen = 0.40, 0.15
base = T * human
resolved = T * res_rate
reopened = resolved * reopen
escalated = T - resolved
print(f"baseline {base:,.0f}; resolved {resolved:,.0f}; reopened {reopened:,.0f}; escalated {escalated:,.0f}")
assert base == 300000 and resolved == 24000 and reopened == 3600 and escalated == 36000
parts = dict(ai=T * ai, reopened=reopened * reopen_cost, escalated=escalated * esc, fee=fee)
for k, v in parts.items(): print(f"  {k:10s} {v:>10,.0f}")
total = sum(parts.values())
print(f"AI-assisted total {total:,.0f}; monthly saving {base-total:,.0f} ({(base-total)/base:.1%})")
assert total == 268000 and base - total == 32000
print(f"human-touched tickets {escalated+reopened:,.0f} of {T:,}; truly resolved {resolved-reopened:,.0f} ({(resolved-reopened)/T:.0%})")
assert escalated + reopened == 39600 and (resolved - reopened) / T == 0.34
# if reopened tickets also cost 5.50 (human must read the failed chat)
alt = parts["ai"] + reopened * esc + parts["escalated"] + fee
print(f"if reopened tickets cost 5.50 too: saving {base-alt:,.0f}")
assert base - alt == 30200
def saving(r, rp=reopen):
    return base - (T*ai + T*r*rp*reopen_cost + T*(1-r)*esc + fee)
be = next(r/10000 for r in range(0, 10001) if saving(r/10000) >= 0)
print(f"break-even resolution rate {be:.1%}; at 0% resolution the saving is {saving(0):,.0f}; at 60% {saving(0.6):,.0f}")
assert abs(be - 0.2878) < 0.0002
for rp in (0.15, 0.30, 0.50):
    print(f"  reopen rate {rp:.0%}: saving at 40% resolution {saving(0.4, rp):,.0f}")
assert saving(0.4, 0.50) < saving(0.4, 0.15)
# cost per AI-resolved-and-stayed-resolved ticket
print(f"AI-side cost per truly resolved ticket: {(T*ai+fee)/(resolved-reopened):.2f}")
