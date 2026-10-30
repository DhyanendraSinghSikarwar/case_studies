# Q18: unseen ticket categories (open-set problem). Illustrative simulation, seeded, numpy only.
import numpy as np
rng = np.random.default_rng(18)

D, K = 6, 5
centroids = rng.normal(0, 3.0, size=(K, D))              # 5 known categories
novel_centre = rng.normal(0, 3.0, size=D)                # new product line: a region the model never saw
def tickets(n, centre): return centre + rng.normal(0, 1.2, size=(n, D))

def softmax_conf(X, T=2.0):
    d2 = ((X[:, None, :] - centroids[None]) ** 2).sum(-1)
    logits = -d2 / (2 * T * T)
    e = np.exp(logits - logits.max(1, keepdims=True)); p = e / e.sum(1, keepdims=True)
    return p.argmax(1), p.max(1), d2.min(1)

# Traffic: 10,000 tickets/week, 12% from the new line
n_total, share = 10_000, 0.12
n_new = int(n_total * share); n_known = n_total - n_new
assert n_new == 1200 and n_known == 8800
Xk_list, yk = [], []
for k in range(K):
    m = n_known // K + (1 if k < n_known % K else 0)
    Xk_list.append(tickets(m, centroids[k])); yk += [k] * m
Xk, yk = np.vstack(Xk_list), np.array(yk)
Xn = tickets(n_new, novel_centre)
pk, ck, dk = softmax_conf(Xk); pn, cn, dn = softmax_conf(Xn)
acc_known = (pk == yk).mean()
print(f"accuracy on KNOWN categories (what the dashboard measures) = {100*acc_known:.1f}%")
print(f"all {n_new} new-line tickets get a known-category label anyway: mean confidence {cn.mean():.2f} (known: {ck.mean():.2f})")
print(f"true overall routing correctness = {100*(pk == yk).sum()/n_total:.1f}% of all tickets (new-line tickets are all misrouted)")
assert acc_known > 0.9 and (pk == yk).sum() / n_total < acc_known * 0.9

# Detection 1: max-softmax confidence threshold at the 5th percentile of KNOWN tickets
thr = np.quantile(ck, 0.05)
print(f"confidence rule (flag if < {thr:.2f}): catches {100*(cn < thr).mean():.1f}% of new-line tickets, flags {100*(ck < thr).mean():.1f}% of known")
# Detection 2: distance to nearest category centre (embedding-distance rule) at the 95th percentile of KNOWN
dthr = np.quantile(dk, 0.95)
print(f"distance rule (flag if > {dthr:.1f}): catches {100*(dn > dthr).mean():.1f}% of new-line tickets, flags {100*(dk > dthr).mean():.1f}% of known")
assert (dn > dthr).mean() > (cn < thr).mean() - 1e-9 and (dn > dthr).mean() > 0.7
# What the flag volume looks like in the weekly queue
flag_known = (dk > dthr).sum(); flag_new = (dn > dthr).sum()
print(f"weekly human-triage queue: {flag_new + flag_known} tickets, of which {flag_new} are new-line ({100*flag_new/(flag_new+flag_known):.0f}% precision)")
# Share-of-flagged trend as a launch monitor: the novel share of flagged tickets rises from 0% to ~12% of traffic
