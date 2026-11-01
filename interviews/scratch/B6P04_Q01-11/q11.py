import numpy as np
rng = np.random.default_rng(11)

# Illustrative model: outcome (invites per user) = B + d * own_treated + s * share_of_friends_treated
d, s = 0.6, 0.5                       # direct effect, spillover from fully treated friend group
n_comm, size = 4_000, 50              # 200,000 users in 4,000 friend communities of 50
within = 0.9                          # 90% of friend ties are inside the community
k = 10                                # friends per user

comm = np.repeat(np.arange(n_comm), size)
N = n_comm * size
def friend_share_treated(T):
    # expected share treated among friends = within * (community mean of T, excluding self approx) + (1-within) * overall mean
    cm = T.reshape(n_comm, size).mean(axis=1)
    cm_user = np.repeat(cm, size)
    return within * cm_user + (1 - within) * T.mean()

# Design 1: user-level 50/50
T1 = (rng.random(N) < 0.5).astype(float)
e1 = friend_share_treated(T1)
# Design 2: community-level 50/50 (cluster randomization)
tc = (rng.random(n_comm) < 0.5).astype(float)
T2 = np.repeat(tc, size)
e2 = friend_share_treated(T2)

# Pure baseline B so that the observed control mean is 20.0 under user-level design
B = 20.0 - s * e1[T1 == 0].mean()
def outcome(T, e): return B + d * T + s * e
y1 = outcome(T1, e1); y2 = outcome(T2, e2)
m1 = y1[T1 == 1].mean() - y1[T1 == 0].mean()
m2 = y2[T2 == 1].mean() - y2[T2 == 0].mean()
global_effect = (B + d + s) - B          # everyone treated vs nobody treated
print(f"baseline with nobody treated B = {B:.2f}; control mean in user-level test = {y1[T1==0].mean():.2f}; treated mean = {y1[T1==1].mean():.2f}")
print(f"user-level measured lift = {m1:.2f} ({m1/y1[T1==0].mean()*100:.1f}% of control)")
print(f"cluster-level measured lift = {m2:.2f}")
print(f"true effect of launching to everyone = {global_effect:.2f} ({global_effect/B*100:.1f}% of baseline)")
assert abs(m1 - 0.6) < 0.05
assert m2 > m1 and m2 < global_effect + 0.01
assert abs(y1[T1 == 0].mean() - 20.0) < 1e-9 and abs(y1[T1 == 1].mean() - 20.6) < 0.05

# Variance cost of cluster randomization: design effect = 1 + (m - 1) * icc
for icc in (0.01, 0.05, 0.1):
    print(f"cluster size {size}, intra-cluster correlation {icc}: design effect = {1 + (size - 1) * icc:.2f}")
assert abs((1 + 49 * 0.05) - 3.45) < 1e-9
