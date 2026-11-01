# Standalone, numpy + torch (CPU, 1 thread). Storage and FLOP maths use ASSUMED sizes; the timing is a measurement on THIS machine only.
import time, numpy as np, torch
torch.set_num_threads(1)
N_PASS, TOK_PER_PASS, DIM = 10_000_000, 100, 128          # ASSUMED corpus and model shape
Q_TOK = 32                                                 # ASSUMED query length in token vectors
GB = 1e9
n_vec = N_PASS * TOK_PER_PASS
rows = [("ColBERT-style fp16 token vectors",            n_vec * DIM * 2),
        ("  int8 token vectors",                         n_vec * DIM * 1),
        ("  1-bit token vectors (sign bits)",            n_vec * DIM / 8),
        ("  residual-style 2-bit + 4B centroid id (from memory, ASSUMED layout)", n_vec * (DIM * 2 / 8 + 4)),
        ("  LITE-style 0.25 x fp16 (REPORTED ratio, not opened)", 0.25 * n_vec * DIM * 2),
        ("single-vector 768-d fp32 (3,072 B/passage)",   N_PASS * 768 * 4),
        ("single-vector PQ 96-byte codes",               N_PASS * 96)]
base = rows[0][1]
print(f"{n_vec:,} token vectors; sizes exclude ids, ANN graph/centroid tables and replicas (add overhead)")
print(f"{'option':72s}{'bytes/passage':>14s}{'GB':>10s}{'x fp16':>8s}")
for n, b in rows: print(f"{n:72s}{b / N_PASS:>14,.0f}{b / GB:>10,.2f}{b / base:>8.3f}")
assert rows[0][1] / GB == 256.0 and rows[1][1] / GB == 128.0 and rows[2][1] / GB == 16.0 and rows[5][1] / N_PASS == 3072 and rows[6][1] / GB == 0.96

# MaxSim cost: for each query token take the max dot product over document tokens, then sum
per_pair = Q_TOK * TOK_PER_PASS * DIM
print(f"\nMaxSim per query-passage pair: {Q_TOK} x {TOK_PER_PASS} x {DIM} = {per_pair:,} multiply-adds; single-vector dot: 768 multiply-adds ({per_pair / 768:.0f}x)")
for cand in (1_000, 10_000):
    print(f"  rerank {cand:>6,} candidates: {cand * per_pair:,.0f} multiply-adds")
print(f"  exhaustive MaxSim over all {N_PASS:,} passages: {N_PASS * per_pair:.2e} multiply-adds per query -> needs candidate generation first")

# measured timing for 1000 candidates on THIS machine (CPU, 1 thread, fp32); machine-specific, not a benchmark
g = torch.Generator().manual_seed(0)
q = torch.nn.functional.normalize(torch.randn(Q_TOK, DIM, generator=g), dim=-1)
docs = torch.nn.functional.normalize(torch.randn(1000, TOK_PER_PASS, DIM, generator=g), dim=-1)
def maxsim(q, docs): return torch.einsum("qd,ntd->nqt", q, docs).max(dim=-1).values.sum(dim=-1)
maxsim(q, docs); t = time.perf_counter(); reps = 5
for _ in range(reps): s = maxsim(q, docs)
ms = (time.perf_counter() - t) / reps * 1000
print(f"\nmeasured on this machine (labelled, machine-specific): MaxSim for 1,000 candidates, fp32, 1 thread: {ms:.1f} ms; output shape {tuple(s.shape)}")
chk = max(float((q @ docs[i].T).max(dim=1).values.sum() - s[i]) for i in range(3)); assert abs(chk) < 1e-4
# toy decision helper
for name, b in rows:
    fits = b / GB <= 64; print(f"fits in a 64 GB RAM box? {'yes' if fits else 'no':3s} {name.strip()}")
