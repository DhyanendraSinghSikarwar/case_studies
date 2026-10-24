# Padding waste with and without packing, on a synthetic length distribution (lognormal, clipped). Pure numpy.
import numpy as np
rng = np.random.default_rng(0)
MAXLEN = 1024
lens = np.clip(rng.lognormal(mean=5.5, sigma=0.8, size=4000).astype(int), 16, MAXLEN)   # synthetic token counts
print(f"{len(lens)} examples, mean length {lens.mean():.0f}, max {lens.max()}, real tokens {lens.sum():,}")

# 1) naive padding: batches of 8 in arrival order, each padded to the longest in the batch
B = 8
padded = sum(B * lens[i:i+B].max() for i in range(0, len(lens), B))
print(f"padded to batch max (batch {B}): slots {padded:,}  padding fraction {1 - lens.sum()/padded:.1%}")

# 2) padding to a fixed max_length for every example
fixed = len(lens) * MAXLEN
print(f"padded to fixed {MAXLEN}: slots {fixed:,}  padding fraction {1 - lens.sum()/fixed:.1%}")

# 3) packing: concatenate examples into rows of MAXLEN
def pack_wrapped(lens):
    """'wrapped'-style: concatenate everything and cut into MAXLEN rows (examples may be split across rows)."""
    return -(-lens.sum() // MAXLEN)                      # ceil rows; only the last row has padding

def pack_bfd(lens):
    """best-fit-decreasing bin packing: examples are kept whole, each placed in the fullest row that still fits."""
    free = []                                            # remaining space per row
    for L in sorted(lens, reverse=True):
        best, bi = None, None
        for i, f in enumerate(free):
            if f >= L and (best is None or f < best):
                best, bi = f, i
        if bi is None: free.append(MAXLEN - L)
        else: free[bi] -= L
    return len(free)

for name, rows in [("wrapped (cut across rows)", pack_wrapped(lens)), ("best-fit-decreasing (whole examples)", pack_bfd(lens))]:
    slots = rows * MAXLEN
    print(f"{name:38s}: rows {rows:5d} slots {slots:,}  padding fraction {1 - lens.sum()/slots:.2%}")
