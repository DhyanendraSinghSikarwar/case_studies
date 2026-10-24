# Standalone, numpy + heapq. TOY TIMING MODEL: every number is an ASSUMPTION, not a measurement of any system.
import heapq, numpy as np
rng = np.random.default_rng(0)
ASSUME = dict(gpus=16, samples=2048, prompt_toks=200, mean_len=400, sigma=0.9, max_len=4096,
              t_step=0.025, slots=64, train_tok_per_gpu_s=3000, score_s=3.0, sync_disagg_s=8.0, swap_coloc_s=5.0)
A = ASSUME
lens = np.minimum(rng.lognormal(np.log(A["mean_len"]) - A["sigma"]**2 / 2, A["sigma"], A["samples"]), A["max_len"]).astype(int) + 1
print(f"response lengths: mean {lens.mean():.0f}, median {np.median(lens):.0f}, p99 {np.percentile(lens, 99):.0f}, max {lens.max()} (long tail)")

def gen_static(lens, engines):                      # each wave of engines*slots sequences waits for its LONGEST sequence
    per_wave = engines * A["slots"]; t = 0.0
    for i in range(0, len(lens), per_wave): t += lens[i:i + per_wave].max() * A["t_step"]
    return t
def gen_continuous(lens, engines):                  # a free slot is refilled at once (continuous batching); makespan by greedy assignment
    heap = [0.0] * (engines * A["slots"]); heapq.heapify(heap)
    for L in sorted(lens, reverse=True): heapq.heappush(heap, heapq.heappop(heap) + L * A["t_step"])
    return max(heap)
train_tokens = (lens + A["prompt_toks"]).sum()
def train_time(g): return train_tokens / (A["train_tok_per_gpu_s"] * g)

G = A["gpus"]; rows = []
useful_gen = lens.sum() * A["t_step"] / A["slots"]          # total GPU-seconds of full-slot decoding needed, whatever the design
def share(train_gpus, T): return (useful_gen + train_time(train_gpus) * train_gpus) / (G * T)
# 1) colocated, synchronous, static batches: all 16 GPUs generate, then all 16 train
T = gen_static(lens, G) + A["score_s"] + train_time(G) + A["swap_coloc_s"]; rows.append(("colocated, sync, static batching", T, share(G, T)))
# 2) colocated, sync, continuous batching
T = gen_continuous(lens, G) + A["score_s"] + train_time(G) + A["swap_coloc_s"]; rows.append(("colocated, sync, continuous batching", T, share(G, T)))
# 3) disaggregated 8 gen + 8 train, still synchronous (each side waits for the other)
g, t = gen_continuous(lens, G // 2), train_time(G // 2)
T = g + A["score_s"] + t + A["sync_disagg_s"]; rows.append(("disaggregated 8+8, sync", T, share(G // 2, T)))
# 4) disaggregated 8+8, asynchronous with one-step lag: generation of batch k+1 overlaps training on batch k
T = max(g + A["score_s"], t + A["sync_disagg_s"]); rows.append(("disaggregated 8+8, async (lag 1)", T, share(G // 2, T)))
print(f"{'design':40s}{'sec/iteration':>14s}{'useful-GPU share':>18s}")
for n, T, u in rows: print(f"{n:40s}{T:14.1f}{u:18.2f}")
print("(useful-GPU share = GPU-seconds of full-slot decoding + training, divided by all GPU-seconds; scoring and weight sync count as overhead)")
print(f"gen time static {gen_static(lens, G):.0f}s vs continuous {gen_continuous(lens, G):.0f}s on 16 engines; ideal (mean length, no tail) {lens.sum()*A['t_step']/(G*A['slots']):.0f}s")

# ---- staleness: how far does the sampling policy lag behind the trainer? (SYNTHETIC random-walk policy) ----
print("\nclipped fraction of tokens (ratio outside [0.8, 1.2]) when samples come from a policy 'lag' updates old")
V = 200
for lag in (0, 1, 2, 4, 8):
    clipped = []
    for _ in range(200):
        steps = rng.normal(0, 0.04, (lag, V)); old = rng.normal(0, 1, V); new = old + steps.sum(0)
        po, pn = np.exp(old - old.max()), np.exp(new - new.max()); po, pn = po / po.sum(), pn / pn.sum()
        a = rng.choice(V, 2000, p=po); r = pn[a] / po[a]; clipped.append(((r < .8) | (r > 1.2)).mean())
    print(f"  lag {lag}: {np.mean(clipped):.3f}")
