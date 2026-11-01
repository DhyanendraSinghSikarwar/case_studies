import hashlib
import numpy as np

total, withdrawn = 120_000, 15_000
share = withdrawn / total
remaining = total - withdrawn
assert share == 0.125 and remaining == 105_000
print("withdrawn share", share, "remaining records", remaining)

# Consent ledger joined at training-table build time
rng = np.random.default_rng(19)
ids = np.arange(total)
w_ids = rng.choice(ids, withdrawn, replace=False)
status = np.full(total, "active", dtype=object)
status[w_ids] = "withdrawn"
train_ids = ids[status == "active"]
assert train_ids.size == remaining and not np.isin(train_ids, w_ids).any()

def manifest_hash(a):
    return hashlib.sha256(np.sort(a).tobytes()).hexdigest()[:12]
print("old manifest", manifest_hash(ids), "new manifest", manifest_hash(train_ids))
assert manifest_hash(ids) != manifest_hash(train_ids)

# Sharded training (K shards, each model trained on one shard): how many shards must be retrained?
K = 20
def expected_shards_touched(w, K=K):
    return K * (1 - (1 - 1 / K) ** w)
for w in (1, 10, 100, 15_000):
    print("withdrawals", w, "expected shards to retrain of", K, ":", round(expected_shards_touched(w), 2))
assert round(expected_shards_touched(1), 2) == 1.0
assert round(expected_shards_touched(10), 2) == 8.03
assert round(expected_shards_touched(15_000), 2) == 20.0   # a 12.5% batch touches every shard: sharding gives no saving

# Cost of waiting: retrain is 3 days compute; if withdrawals arrive weekly and we batch them
retrain_days = 3
batch_weekly_share = withdrawn / total / 52
print("if the same share arrived evenly over a year, weekly share:", round(batch_weekly_share * 100, 3), "%")
assert retrain_days == 3 and round(batch_weekly_share * 100, 3) == 0.24
