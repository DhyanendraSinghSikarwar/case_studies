# Q51: group-chat metrics when users depend on each other (illustrative numbers + a seeded simulation)
import numpy as np
rng = np.random.default_rng(51)

# Week 1: 20 groups of 5, everyone active, 10 messages each.
# Week 2: 10 groups stay intact; 10 groups have only 2 of 5 members active, and those 2 message 14 each.
w1 = dict(groups=[(5, 10)] * 20)                       # (active members, messages per active member)
w2 = dict(groups=[(5, 10)] * 10 + [(2, 14)] * 10)

def summarize(groups):
    dau = sum(a for a, _ in groups)
    msgs = sum(a * m for a, m in groups)
    healthy = sum(1 for a, _ in groups if a >= 3)      # a group is "healthy" if >= 3 members active
    return dau, msgs, msgs / dau, healthy / len(groups)

for name, w in (("week 1", w1), ("week 2", w2)):
    dau, msgs, per_user, healthy = summarize(w["groups"])
    print(f"{name}: DAU {dau}, messages {msgs}, messages per active user {per_user:.2f}, healthy-group share {healthy:.0%}")
s1, s2 = summarize(w1["groups"]), summarize(w2["groups"])
assert s1[:3] == (100, 1000, 10.0) and s2[:2] == (70, 780) and round(s2[2], 2) == 11.14
assert s1[3] == 1.0 and s2[3] == 0.5

# Why the weak groups matter: leaving depends on how many friends are still active.
def simulate(start_active, weeks=8, n_groups=2000, size=5):
    active = np.full(n_groups, start_active)
    for _ in range(weeks):
        # chance an active member leaves this week: 5% if >=3 active in the group, 30% otherwise
        p = np.where(active >= 3, 0.05, 0.30)
        active = active - rng.binomial(active, p)
    return active.mean()
healthy_end = simulate(5)
weak_end = simulate(2)
print(f"after 8 weeks, mean active members: group that started with 5 = {healthy_end:.2f}, started with 2 = {weak_end:.2f}")
assert weak_end < 0.5 and healthy_end > 3.0 and weak_end < healthy_end / 5

# Edge-level metric: share of messages answered within an hour (reciprocity), per-user vs per-group
replied = np.array([8, 9, 7, 2, 1])                    # per group of 5 chats, replies within 1h out of 10 messages each
print("reply-within-1h rate by group:", (replied / 10).tolist(), "mean", replied.mean() / 10)
assert replied.mean() / 10 == 0.54
