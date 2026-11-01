# validate.py CONFIG : parse config.pbtxt, check dynamic-batching rules, then a small queue-delay model. Triton is NOT run.
import sys, pathlib, random, statistics
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from pbtxt import parse
def validate(text):
    c, errs = parse(text), []
    for k in ("name", "backend", "max_batch_size", "input", "output", "dynamic_batching", "instance_group"):
        if k not in c: errs.append(f"missing key: {k}")
    if errs: return errs
    mb = c["max_batch_size"][0]
    if mb < 1: errs.append("dynamic batching needs max_batch_size > 0")
    db = c["dynamic_batching"][0]
    pref = db.get("preferred_batch_size", [])
    if any(p > mb for p in pref): errs.append(f"preferred_batch_size {pref} above max_batch_size {mb}")
    if pref != sorted(pref): errs.append("preferred_batch_size should be ascending")
    d = db.get("max_queue_delay_microseconds", [0])[0]
    if not 0 <= d <= 10_000: errs.append(f"queue delay {d} us outside the sane 0..10000 range for an online model")
    for g in c["instance_group"]:
        if g.get("count", [1])[0] < 1: errs.append("instance count < 1")
        if g["kind"][0] not in ("KIND_CPU", "KIND_GPU"): errs.append("bad kind")
    return errs
text = pathlib.Path(sys.argv[1]).read_text()
print("config problems:", validate(text) or "none")
print("bad config (preferred 16 > max 8, delay 50000):", validate(text.replace("[ 4, 8 ]", "[ 4, 16 ]").replace("100\n", "50000\n")))

# Queue-delay model (a toy of the idea, not Triton's scheduler): a batch starts when the first request arrives and is
# sent when preferred size is reached or max_queue_delay has passed. Single worker model is ignored; only waiting is measured.
def waits(rate_per_ms, delay_ms, pref, n=20000, seed=1):
    rnd, t, arr = random.Random(seed), 0.0, []
    for _ in range(n): t += rnd.expovariate(rate_per_ms); arr.append(t)
    w, i = [], 0
    while i < n:
        start, j = arr[i], i
        while j + 1 < n and arr[j + 1] - start <= delay_ms and (j - i + 1) < pref: j += 1
        close = arr[j] if (j - i + 1) >= pref else start + delay_ms   # full batch leaves at once, else wait for the delay
        w += [close - a for a in arr[i:j + 1]]; i = j + 1
    return w
print("delay = 0.1 ms (100 us), preferred 8:")
for rate in (0.5, 5, 50):       # requests per millisecond: 500, 5000, 50000 req/s
    w = waits(rate, 0.1, 8)
    print(f"  arrival {rate*1000:>7.0f} req/s: p50 queue wait {statistics.median(w):.3f} ms, max {max(w):.3f} ms")
print("hand check: one lone request waits the full 0.100 ms, so p50 added is at most about 0.1 ms")
