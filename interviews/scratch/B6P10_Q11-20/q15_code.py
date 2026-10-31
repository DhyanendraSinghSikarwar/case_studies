import numpy as np

# Prompt arithmetic: raw vector storage, decimal GB (1 GB = 1e9 bytes)
resumes, jobs, dim = 2_000_000, 150_000, 768
f32 = resumes * dim * 4
i8 = resumes * dim * 1
assert f32 == 6_144_000_000 and i8 == 1_536_000_000
print("float32 resumes GB:", f32 / 1e9, "| int8 GB:", i8 / 1e9, "| ratio:", f32 / i8)
job_f32 = jobs * dim * 4
assert job_f32 == 460_800_000
print("job vectors float32 GB:", job_f32 / 1e9)

# Brute-force cost per job query: dot products against every resume
macs_per_query = resumes * dim
assert macs_per_query == 1_536_000_000
all_jobs_macs = macs_per_query * jobs
print("multiply-adds per query:", macs_per_query, "| for all jobs (nightly batch):", f"{all_jobs_macs:.3e}")
assert all_jobs_macs == 1_536_000_000 * 150_000

# Does int8 quantisation keep the shortlist? Small test: 20,000 synthetic unit vectors, 768 dims, top-200 overlap
rng = np.random.default_rng(15)
n, d, k = 20_000, 768, 200
base = rng.normal(size=(n, d)).astype(np.float32)
base += 0.6 * rng.normal(size=(1, d)).astype(np.float32)          # shared direction, so scores are not all near zero
base /= np.linalg.norm(base, axis=1, keepdims=True)
scale = np.abs(base).max()
q8 = np.round(base / scale * 127).astype(np.int8)
deq = q8.astype(np.float32) * (scale / 127)
overlaps = []
for _ in range(50):
    q = base[rng.integers(n)] + 0.3 * rng.normal(size=d).astype(np.float32)
    q /= np.linalg.norm(q)
    exact = set(np.argpartition(-(base @ q), k)[:k])
    approx = set(np.argpartition(-(deq @ q), k)[:k])
    overlaps.append(len(exact & approx) / k)
ov = float(np.mean(overlaps))
print("top-200 overlap, int8 vs float32 (synthetic, illustrative):", round(ov, 3))
assert ov > 0.9
assert q8.nbytes * 4 == base.nbytes
print("bytes ratio in the test:", base.nbytes / q8.nbytes)
