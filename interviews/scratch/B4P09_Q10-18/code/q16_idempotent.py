# EMULATION in pure Python. No Kafka broker or real producer client was run.
import random
def run(n_msgs, loss_ack_p, use_seq, seed=11):
    rnd = random.Random(seed)
    log, last_seq = [], -1                    # broker side, one producer id, one partition
    dups_dropped = 0
    for seq in range(n_msgs):
        while True:                           # producer retries until it sees an ack
            # request reaches the broker (always, in this model)
            if use_seq and seq <= last_seq:
                dups_dropped += 1             # broker: already have this (pid, seq): drop, still ack
            else:
                log.append(seq); last_seq = seq
            if rnd.random() >= loss_ack_p: break   # ack arrived, producer moves on
            # else ack lost on the network: producer times out and retries the same message
    return log, dups_dropped

for use_seq in (False, True):
    log, dropped = run(1000, 0.2, use_seq)
    print(f"seq check={use_seq!s:5}: sent=1000 log_size={len(log)} duplicates={len(log)-len(set(log))} dropped_by_broker={dropped} in_order={log==sorted(log)}")

# transactions: all-or-nothing across two partitions, read_committed hides aborted data
topic = {"A": [], "B": []}                   # (value, txn_id, state)
def txn(tid, vals, commit):
    for p, v in vals: topic[p].append([v, tid, "open"])
    for p in topic:
        for rec in topic[p]:
            if rec[1] == tid: rec[2] = "committed" if commit else "aborted"
txn("t1", [("A", "x1"), ("B", "y1")], True)
txn("t2", [("A", "x2"), ("B", "y2")], False)
rc = {p: [r[0] for r in recs if r[2] == "committed"] for p, recs in topic.items()}
ru = {p: [r[0] for r in recs] for p, recs in topic.items()}
print("read_uncommitted:", ru)
print("read_committed  :", rc)
