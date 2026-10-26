# EMULATION in pure Python. No Kafka broker or client was run.
def range_assign(parts, consumers):
    consumers = sorted(consumers); n, m = len(parts), len(consumers)
    out, i = {c: [] for c in consumers}, 0
    for k, c in enumerate(consumers):
        take = n // m + (1 if k < n % m else 0)
        out[c] = parts[i:i + take]; i += take
    return out

def rr_assign(parts, consumers):
    consumers = sorted(consumers)
    out = {c: [] for c in consumers}
    for i, p in enumerate(parts):
        out[consumers[i % len(consumers)]].append(p)
    return out

def sticky_cooperative(prev, parts, consumers):
    """Keep what each survivor owns; give orphan partitions to the least loaded."""
    out = {c: [p for p in prev.get(c, []) if p in parts] for c in consumers}
    owned = {p for ps in out.values() for p in ps}
    for p in parts:
        if p not in owned:
            out[min(out, key=lambda c: (len(out[c]), c))].append(p)
    return out

P = list(range(6))
for n in (1, 3, 8):
    cs = [f"c{i}" for i in range(n)]
    print(f"--- {n} consumer(s), 6 partitions")
    print(" range      ", range_assign(P, cs))
    print(" round-robin", rr_assign(P, cs))
    idle = [c for c, ps in range_assign(P, cs).items() if not ps]
    print(" idle consumers:", idle)

print("--- consumer c1 leaves a group of 3 (range before, then rebalance)")
before = range_assign(P, ["c0", "c1", "c2"])
eager = range_assign(P, ["c0", "c2"])
coop = sticky_cooperative(before, P, ["c0", "c2"])
print(" before      ", before)
print(" eager after ", eager, "-> partitions revoked from everyone first:", sorted(sum(before.values(), [])))
moved = sorted(p for c in coop for p in coop[c] if p not in before.get(c, []))
print(" coop after  ", coop, "-> only moved:", moved)

print("--- lag per partition = log end offset - committed offset")
end = {0: 120, 1: 118, 2: 300, 3: 95, 4: 100, 5: 101}
committed = {0: 120, 1: 100, 2: 150, 3: 95, 4: 99, 5: 101}
lag = {p: end[p] - committed[p] for p in P}
print(" lag", lag, "total", sum(lag.values()), "max partition", max(lag, key=lag.get))
