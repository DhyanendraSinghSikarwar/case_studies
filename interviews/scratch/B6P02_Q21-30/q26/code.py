import numpy as np

# Prompt arithmetic: head 80% / tail 20% of queries; tail NDCG 0.50 -> 0.46 (-8%); overall stable.
head_share, tail_share = 0.8, 0.2
tail0, tail1 = 0.50, 0.46
assert abs((tail1 - tail0) / tail0 + 0.08) < 1e-12
tail_loss = tail_share * (tail1 - tail0)               # -0.008 on overall NDCG
head_gain_needed = -tail_loss / head_share             # head must gain this much for overall to be flat
head0 = 0.70
head1 = head0 + head_gain_needed
print(f"tail drags overall by {tail_loss:+.3f}; head must rise {head0:.2f} -> {head1:.2f} ({head_gain_needed/head0:+.1%}) to hide it")
assert abs(tail_loss + 0.008) < 1e-12 and abs(head1 - 0.71) < 1e-12

# Simulation: per-query NDCG is noisy (sd 0.3). 10,000 queries per week: 8,000 head, 2,000 tail.
rng = np.random.default_rng(26)
def week(head_mean, tail_mean):
    h = np.clip(rng.normal(head_mean, 0.3, 8000), 0, 1); t = np.clip(rng.normal(tail_mean, 0.3, 2000), 0, 1)
    return h, t
h0, t0 = week(0.70, 0.50); h1, t1 = week(0.71, 0.46)
all0, all1 = np.r_[h0, t0], np.r_[h1, t1]
def diff_ci(a, b, B=2000):
    d = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(B)]
    return np.mean(b) - np.mean(a), np.percentile(d, [2.5, 97.5])
for name, a, b in [("overall", all0, all1), ("head", h0, h1), ("tail", t0, t1)]:
    d, ci = diff_ci(a, b)
    print(f"{name:8s} change {d:+.4f}  95% bootstrap CI [{ci[0]:+.4f}, {ci[1]:+.4f}]")
d_all, ci_all = diff_ci(all0, all1)
d_tail, ci_tail = diff_ci(t0, t1)
assert ci_all[0] < 0 < ci_all[1]                       # overall: not distinguishable from flat
assert ci_tail[1] < 0                                  # tail alone: clearly down
print("asserts passed")
