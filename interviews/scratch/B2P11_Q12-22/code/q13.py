# TOY: per-request cost from a versioned price table. PRICES ARE SYNTHETIC (not any provider's), per 1M tokens.
from decimal import Decimal as D
from collections import defaultdict
PRICES = {  # (model, version_effective_from) -> price per 1M tokens
    ("m-small", "2026-01-01"): {"in": D("1.00"), "cached_in": D("0.10"), "out": D("4.00")},
    ("m-small", "2026-06-01"): {"in": D("0.80"), "cached_in": D("0.08"), "out": D("3.20")},
}
def price_for(model, day):
    cands = sorted(k for k in PRICES if k[0] == model and k[1] <= day)
    return cands[-1][1], PRICES[cands[-1]]
def cost(u, model, day):
    ver, p = price_for(model, day)
    fresh = u["input"] - u["cached"]
    billed_out = u["output"] + u["reasoning"]          # assumption: reasoning tokens billed at output rate (check provider)
    c = (fresh * p["in"] + u["cached"] * p["cached_in"] + billed_out * p["out"]) / D(1_000_000)
    return ver, c
reqs = [  # (day, tenant, feature, prompt_ver, usage)
    ("2026-05-30", "acme", "search", "p3", dict(input=2000, cached=1500, output=300, reasoning=0)),
    ("2026-06-02", "acme", "search", "p4", dict(input=2600, cached=0,    output=900, reasoning=0)),
    ("2026-06-02", "zeta", "agent",  "p4", dict(input=5000, cached=4000, output=400, reasoning=1200)),
    ("2026-06-03", "zeta", "agent",  "p4", dict(input=5200, cached=4000, output=350, reasoning=900)),
]
rows = []
for day, tenant, feat, pv, u in reqs:
    ver, c = cost(u, "m-small", day)
    rows.append(dict(day=day, tenant=tenant, feature=feat, prompt=pv, price_ver=ver, cost=c))
    print(f"{day} {tenant:5} {feat:7} {pv} price_ver={ver} cost=${c:.6f}")
for key in ("tenant", "feature", "prompt"):
    agg = defaultdict(D)
    for r in rows: agg[r[key]] += r["cost"]
    print("by", key, {k: f"{v:.6f}" for k, v in sorted(agg.items())})
# reconciliation against a (synthetic) invoice that was computed on provider-side token counts
mine = sum(r["cost"] for r in rows)
invoice = mine * D("1.012")     # SYNTHETIC: invoice 1.2% higher, e.g. retries or unrecorded calls
gap = (invoice - mine) / invoice
print(f"my total ${mine:.6f} invoice ${invoice:.6f} gap {gap*100:.2f}% -> investigate if above tolerance (say 1%)")
# wrong way: price everything at output rate
wrong = sum((u["input"] + u["output"] + u["reasoning"]) * D("3.20") / D(1_000_000) for d, t, f, p, u in reqs[1:])
right = sum(r["cost"] for r in rows[1:])
print(f"all-tokens-at-output-rate (June rows) ${wrong:.6f} vs correct ${right:.6f}")
