# Q52: advertiser-level randomization in a shared auction with shared budgets (illustrative simulation)
import numpy as np
rng = np.random.default_rng(52)
ADV, IMP, BUD = 40, 20_000, 520.0           # advertisers, impressions, budget each (budget binds)
def run(boost, seed=0):
    """second-price auction per impression; boost[i] multiplies advertiser i's bid; a spent budget stops bidding."""
    r = np.random.default_rng(seed)
    val = r.lognormal(0, 0.5, (IMP, ADV)) * r.lognormal(0, 0.3, ADV)      # value per impression
    wins = np.zeros(ADV); value = np.zeros(ADV); spend = np.zeros(ADV)
    budget = np.full(ADV, BUD)
    for t in range(IMP):
        bid = val[t] * boost; bid = np.where(spend < budget, bid, 0.0)
        top = np.argsort(bid)[-2:]
        i, price = top[1], bid[top[0]]
        if bid[i] <= 0: continue
        wins[i] += 1; value[i] += val[t, i]; spend[i] += price
    return wins, value, spend
B = 1.25
ctrl_all = run(np.ones(ADV), seed=1)
trt_all = run(np.full(ADV, B), seed=1)
truth = (trt_all[1].sum() - ctrl_all[1].sum()) / ctrl_all[1].sum()
truth_spend = (trt_all[2].sum() - ctrl_all[2].sum()) / ctrl_all[2].sum()
print("TRUTH (everyone vs nobody boosted): value delivered", f"{100*truth:+.1f}%", " spend", f"{100*truth_spend:+.1f}%")
# advertiser-randomised: half the advertisers boosted, same marketplace
naive = []; spill = []
for s in range(8):
    arm = rng.permutation(ADV) < ADV // 2
    w, v, sp = run(np.where(arm, B, 1.0), seed=1)
    naive.append(v[arm].mean() / v[~arm].mean() - 1)
    spill.append(v[~arm].sum() / ctrl_all[1][~arm].sum() - 1)   # control advertisers vs the same advertisers in the all-control world
print("NAIVE (advertiser-level 50/50): value per advertiser treated vs control", f"{100*np.mean(naive):+.1f}%", "(range", f"{100*min(naive):+.1f}% to {100*max(naive):+.1f}%)")
print("SPILLOVER: control advertisers' own value vs the all-control world:", f"{100*np.mean(spill):+.1f}%", "(SUTVA says this would be 0)")
assert np.mean(spill) > 0.1
# auction-level split: each impression is randomly given to a 'boosted' or 'plain' mini-marketplace with half budgets
r = np.random.default_rng(1); val = r.lognormal(0, 0.5, (IMP, ADV)) * r.lognormal(0, 0.3, ADV)
side = rng.random(IMP) < 0.5
def mini(mask, boost):
    v = np.zeros(ADV); spend = np.zeros(ADV); bud = BUD / 2
    for t in np.where(mask)[0]:
        bid = np.where(spend < bud, val[t] * boost, 0.0); top = np.argsort(bid)[-2:]
        i, p = top[1], bid[top[0]]
        if bid[i] <= 0: continue
        v[i] += val[t, i]; spend[i] += p
    return v, spend
vt, st = mini(side, B); vc, sc = mini(~side, 1.0)
est = vt.sum() / vc.sum() - 1
print("AUCTION-LEVEL split with half budgets in each arm: value", f"{100*est:+.1f}%", "(truth", f"{100*truth:+.1f}%)")
assert abs(np.mean(naive) - truth) > 0.15 and np.mean(naive) < truth
assert abs(est - truth) < 0.05
