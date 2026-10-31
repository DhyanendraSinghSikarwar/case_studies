# Q49: unit economics of a GenAI assistant by segment (illustrative numbers)
import pandas as pd

VALUE = 3.0   # Rs of value per extra completed task (assumed: retained revenue + conversion), illustrative
seg = pd.DataFrame({
    "segment":  ["light", "mid", "heavy"],
    "share":    [0.60, 0.30, 0.10],       # share of active users
    "base":     [8.0, 20.0, 40.0],         # completions per user per month without the assistant
    "extra":    [0.4, 2.4, 8.2],           # extra completions per user per month with it
    "cost":     [3.0, 6.0, 24.0],          # inference Rs per user per month
})
seg["uplift_pct"] = seg.extra / seg.base * 100
seg["value"] = seg.extra * VALUE
seg["net"] = seg.value - seg.cost
seg["cost_per_extra"] = seg.cost / seg.extra
print(seg.round(2).to_string(index=False))

tot_base = (seg.share * seg.base).sum()
tot_extra = (seg.share * seg.extra).sum()
tot_cost = (seg.share * seg.cost).sum()
tot_net = (seg.share * seg.net).sum()
print(f"\noverall uplift {tot_extra/tot_base:.1%}, cost per active user Rs {tot_cost:.2f}, "
      f"extra completions/user {tot_extra:.2f}, net per user Rs {tot_net:.2f}, cost per extra completion Rs {tot_cost/tot_extra:.2f}")
assert round(tot_extra / tot_base, 2) == 0.12 and round(tot_cost, 2) == 6.0
assert round(tot_extra, 2) == 1.78 and round(tot_net, 2) == -0.66 and round(tot_cost / tot_extra, 2) == 3.37

# who pays for itself: cost per extra completion below VALUE
pays = seg[seg.cost_per_extra <= VALUE].segment.tolist()
print("segments with cost per extra completion <= Rs", VALUE, ":", pays)
assert pays == ["mid", "heavy"]

# what-if: stop serving the light segment with the big model (serve nothing, so cost 0 and extra 0)
keep = seg[seg.segment != "light"]
net_keep = (keep.share * keep.net).sum()              # per original active user
print(f"net per original active user if light is not served: Rs {net_keep:.2f}")
assert round(net_keep, 2) == 0.42
