# Standalone, numpy only. Every number below is an ASSUMPTION or SYNTHETIC; this is a planning model, not data.
import numpy as np
rng = np.random.default_rng(0)

# ---- Part 1: throughput and cost calculator (ASSUMED inputs) ----
A = dict(target_pairs=50_000, redundancy=3, gold_share=0.10, min_per_task=4.0, adjud_min=8.0, audit_share=0.05, audit_min=6.0,
         disagree_rate=0.50, reject_rate=0.15, hours_per_day=6.0, days=20, cost_per_hour=6.0, overhead_per_task=0.05)
def plan(a):
    pairs_to_label = a["target_pairs"] / (1 - a["reject_rate"])          # some pairs are rejected (ambiguous, unsafe, broken)
    label_tasks = pairs_to_label * a["redundancy"] * (1 + a["gold_share"])  # gold items are extra tasks
    minutes = label_tasks * a["min_per_task"] + pairs_to_label * a["disagree_rate"] * a["adjud_min"] + pairs_to_label * a["audit_share"] * a["audit_min"]
    hours = minutes / 60
    people = hours / (a["hours_per_day"] * a["days"])
    cost = hours * a["cost_per_hour"] + label_tasks * a["overhead_per_task"]
    return label_tasks, hours, people, cost, cost / a["target_pairs"]
lt, h, ppl, cost, per = plan(A)
print(f"label tasks {lt:,.0f} | work hours {h:,.0f} | annotators needed over {A['days']} days {ppl:.1f} | cost {cost:,.0f} | cost per accepted pair {per:.2f}  (currency units, ASSUMED rates)")
for r in (1, 2, 3, 5):
    a = dict(A, redundancy=r); print(f"  redundancy {r}: cost per accepted pair {plan(a)[4]:.2f}, annotators {plan(a)[2]:.1f}")

# ---- Part 2: agreement simulation (SYNTHETIC): 3 labels per pair, majority vote, adjudication, gold filtering ----
N = 20000
truth = rng.random(N) < 0.5                                              # which response a careful expert would choose
hard = rng.random(N) < 0.30                                              # 30% of pairs are hard: even good annotators are near coin flip
acc_ann = np.concatenate([rng.uniform(0.80, 0.92, 16), rng.uniform(0.55, 0.65, 4)])   # 16 good, 4 careless annotators
def label(ann): 
    p = np.where(hard, 0.5 + (acc_ann[ann] - 0.5) * 0.3, acc_ann[ann])
    return np.where(rng.random(N) < p, truth, ~truth)
def run(pool):
    L = np.stack([label(rng.choice(pool, N)) for _ in range(3)])        # (3, N) labels (annotator picked per label, per pair)
    agree = np.mean([(L[i] == L[j]).mean() for i in range(3) for j in range(i + 1, 3)])
    maj = L.sum(0) >= 2; unanimous = (L == L[0]).all(0)
    adj = ~unanimous                                                    # send non-unanimous pairs to an expert (assumed correct 95%)
    final = np.where(adj, np.where(rng.random(N) < 0.95, truth, ~truth), maj)
    return agree, (maj == truth).mean(), adj.mean(), (final == truth).mean()
all_pool = np.arange(20)
# gold items: each annotator does 200 gold items; drop anyone below 75% accuracy
gold_acc = np.array([ (rng.random(200) < acc_ann[i]).mean() for i in range(20)])
good_pool = np.array([i for i in range(20) if gold_acc[i] >= 0.75])
print(f"\nannotators kept after gold check: {len(good_pool)} of 20 (careless ones have true accuracy {acc_ann[16:].round(2)})")
for name, pool in [("all 20 annotators", all_pool), ("after gold filtering", good_pool)]:
    ag, mj, adjshare, fin = run(pool)
    print(f"{name:22s} pairwise agreement {ag:.3f} | majority-vote accuracy {mj:.3f} | share to adjudication {adjshare:.2f} | accuracy after adjudication {fin:.3f}")
