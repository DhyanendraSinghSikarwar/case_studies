# EMULATION in pure Python. No Kafka broker or client was run.
# Real Kafka's default partitioner uses murmur2 on the key bytes; this uses zlib.crc32 as a stand-in.
import zlib, random, collections
def part(key, n): return zlib.crc32(key.encode()) % n

keys = [f"user{i}" for i in range(1000)]
moved = sum(part(k, 6) != part(k, 8) for k in keys)
print(f"keys that change partition when 6 -> 8: {moved} of 1000 ({moved/10:.1f}%)")
print("same key, same partition (6):", {part('user7', 6) for _ in range(5)})

# ordering per partition only: two keys, events interleaved; consumer reads partitions independently
events = [("A", 1), ("B", 1), ("A", 2), ("B", 2), ("A", 3)]
log = collections.defaultdict(list)
for k, seq in events: log[part(k, 6)].append((k, seq))
print("partition logs:", dict(log))

# adding partitions mid-stream: key A's later events land elsewhere
pa6, pa8 = part("A", 6), part("A", 8)
print(f"key A: partition {pa6} with 6 parts, {pa8} with 8 parts ->", "ORDER AT RISK" if pa6 != pa8 else "same")
bad = [k for k in keys if part(k, 6) != part(k, 8)][:1]
print("example key that moves:", bad, part(bad[0], 6), "->", part(bad[0], 8))

# retry without idempotence: two batches in flight (max.in.flight > 1); batch 1's first try is lost
def send(batches, fail_first_try_of, with_sequence_check):
    broker, next_seq, retry = [], 0, []
    for seq, name in enumerate(batches):                 # both sent before any ack
        if name == fail_first_try_of: retry.append((seq, name)); continue
        if with_sequence_check and seq != next_seq:      # broker expects seq 0 first: rejects out-of-order
            retry.append((seq, name)); continue
        broker.append(name); next_seq += 1
    for seq, name in retry: broker.append(name)          # client retries what failed or was rejected
    return broker
print("no idempotence      :", send(["msg1", "msg2"], "msg1", False), "(sent order msg1, msg2)")
print("sequence check (idem):", send(["msg1", "msg2"], "msg1", True))

# skew: 1000 events, 60% from one hot key
random.seed(7)
ev = ["merchant_hot"] * 600 + [f"merchant{random.randrange(200)}" for _ in range(400)]
cnt = collections.Counter(part(k, 6) for k in ev)
print("events per partition (60% hot key):", dict(sorted(cnt.items())))
print("max/mean ratio:", round(max(cnt.values()) / (len(ev) / 6), 2))
uni = collections.Counter(part(f"user{i}", 6) for i in range(1000))
print("1000 distinct keys, one event each:", dict(sorted(uni.items())))
