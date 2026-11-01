# Q4: PURE-PYTHON EMULATION of Kafka log semantics. No Kafka broker or Kafka client was run.
import zlib

class OffsetOutOfRange(Exception): pass

class Partition:
    def __init__(self): self.records, self.start = [], 0          # start = log start offset (moves with retention)
    def append(self, rec): self.records.append(rec); return self.start + len(self.records) - 1
    @property
    def end(self): return self.start + len(self.records)          # next offset to be written (log end offset)
    def read(self, offset, max_n=100):
        if offset < self.start or offset > self.end: raise OffsetOutOfRange(f"offset {offset}, valid {self.start}..{self.end}")
        return [(offset + i, r) for i, r in enumerate(self.records[offset - self.start: offset - self.start + max_n])]
    def truncate_before(self, new_start):                          # retention deletes OLD records, offsets keep their numbers
        drop = new_start - self.start; self.records = self.records[drop:]; self.start = new_start

class Topic:
    def __init__(self, name, n): self.name, self.parts = name, [Partition() for _ in range(n)]
    def produce(self, key, value):                                 # same key -> same partition (crc32 here; real Kafka uses murmur2)
        p = zlib.crc32(key.encode()) % len(self.parts)
        return p, self.parts[p].append((key, value))

class Broker:                                                      # holds topics and the committed offsets (__consumer_offsets analogue)
    def __init__(self): self.committed = {}                        # (group, topic, partition) -> next offset to read
class Consumer:
    def __init__(self, broker, group, topic): self.b, self.g, self.t = broker, group, topic
    def poll(self, p):
        off = self.b.committed.get((self.g, self.t.name, p), 0)
        return self.t.parts[p].read(off)
    def commit(self, p, next_offset): self.b.committed[(self.g, self.t.name, p)] = next_offset

b, topic = Broker(), Topic("payments", 3)
for i, (k, v) in enumerate([("u1", "a"), ("u2", "b"), ("u1", "c"), ("u3", "d"), ("u1", "e"), ("u2", "f")]):
    print("produce", k, v, "->", topic.produce(k, v))
print("log end offsets:", [p.end for p in topic.parts])

c = Consumer(b, "fraud", topic)
for p in range(3):
    batch = c.poll(p); print(f"group fraud reads partition {p} from committed offset:", batch)
    if batch: c.commit(p, batch[-1][0] + 1)
print("committed:", {k[2]: v for k, v in b.committed.items() if k[0] == "fraud"})
print("poll again after commit (nothing new):", [c.poll(p) for p in range(3)])

print("\nnew group 'audit' is independent, starts at 0:", sum(len(Consumer(b, 'audit', topic).poll(p)) for p in range(3)), "records")
p_u1 = zlib.crc32(b"u1") % 3
topic.produce("u1", "g"); print("after one more u1 record, fraud sees on partition", p_u1, ":", c.poll(p_u1))

print("\nretention: delete the oldest 2 records of partition", p_u1)
topic.parts[p_u1].truncate_before(2)
print("partition now holds offsets", topic.parts[p_u1].start, "..", topic.parts[p_u1].end - 1, "(offsets not renumbered)")
try: Consumer(b, "late-group", topic).poll(p_u1)
except OffsetOutOfRange as e: print("new group asking offset 0 ->", type(e).__name__, "-", e)
