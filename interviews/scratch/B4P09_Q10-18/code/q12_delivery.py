# EMULATION in pure Python. No Kafka broker or client was run.
LOG = [f"m{i}" for i in range(10)]           # one partition, offsets 0..9
CRASH_AT = 4                                  # crash while handling offset 4

def run(order, sink_idempotent=False):
    committed, sink_list, sink_map = 0, [], {}
    def effect(off):
        if sink_idempotent: sink_map[("p0", off)] = LOG[off]   # upsert by (partition, offset)
        else: sink_list.append(LOG[off])                        # blind append
    for attempt in (1, 2):                    # attempt 2 = restart after crash
        off = committed                       # resume from committed offset
        while off < len(LOG):
            if order == "commit_then_process":
                committed = off + 1
                if attempt == 1 and off == CRASH_AT: break       # crash after commit, before effect
                effect(off)
            else:
                effect(off)
                if attempt == 1 and off == CRASH_AT: break       # crash after effect, before commit
                committed = off + 1
            off += 1
        if off >= len(LOG): break
    n = len(sink_map) if sink_idempotent else len(sink_list)
    seen = sorted({v for _, v in sink_map.items()}) if sink_idempotent else sink_list
    return n, seen

for order in ("commit_then_process", "process_then_commit"):
    n, seen = run(order)
    dup = len(seen) - len(set(seen)); miss = sorted(set(LOG) - set(seen))
    print(f"{order:20s} sink rows={n} duplicates={dup} missing={miss}")
n, seen = run("process_then_commit", sink_idempotent=True)
print(f"process_then_commit + idempotent sink keyed (partition, offset): rows={n} missing={sorted(set(LOG)-set(seen))}")
