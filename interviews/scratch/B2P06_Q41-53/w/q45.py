# Standalone, standard library only. Pure arithmetic; decimal units (1 GB = 1e9 bytes). ASSUMED parameters are labelled.
N, D, RAM = 800_000_000, 768, 200e9
GB = lambda b: b / 1e9
raw32 = N * D * 4
print(f"raw fp32: {GB(raw32):,.0f} GB = {raw32/1e12:.2f} TB  -> {raw32/RAM:.1f}x the 200 GB budget (does not fit)")
print(f"raw fp16: {GB(N*D*2):,.0f} GB | int8: {GB(N*D):,.0f} GB (still too big)")
IDS = N * 8                                                   # 8-byte id per vector
NLIST = 1_048_576                                             # ASSUMED coarse cells (2^20; tune on your data)
cent = NLIST * D * 4
print(f"\nASSUMED IVF with nlist={NLIST:,}: centroids {GB(cent):.1f} GB, ids {GB(IDS):.1f} GB")
print(f"{'PQ bytes/vec':>12} {'codes GB':>9} {'+ids+centroids GB':>18} {'fits 200 GB?':>13} {'compression':>12}")
for m in (16, 32, 64, 96, 128):                               # m sub-vectors, 8 bits (1 byte) each
    codes = N * m; tot = codes + IDS + cent + m * 256 * (D // m) * 4
    print(f"{m:>12} {GB(codes):>9.1f} {GB(tot):>18.1f} {'yes' if tot < RAM*0.8 else 'tight/no':>13} {D*4/m:>11.0f}x")
print("\nIn-RAM HNSW is the wrong tool: graph links alone for M=32 (ASSUMED, ~2*M links x 4 B per vector on layer 0):",
      f"{GB(N*2*32*4):.0f} GB, and it still needs full vectors for distances ({GB(raw32):,.0f} GB).")
# SSD rerank cost, ASSUMED workload
qps, shortlist = 1000, 100
print(f"\nSSD rerank (ASSUMED {qps} QPS, shortlist {shortlist}): {qps*shortlist:,} random 3 KB reads/s, {qps*shortlist*D*4/1e6:,.0f} MB/s;"
      " NVMe drives are commonly rated for hundreds of thousands of IOPS (check the drive spec).")
for per_machine in (200e9,):
    print(f"Alternative: shard full fp32 vectors in RAM: {raw32/(per_machine*0.7):.0f} machines at 70% usable RAM each (ASSUMED)")
print(f"Sharded IVF-PQ(96) over 4 machines: {GB(N*96+IDS+cent)/4:.1f} GB per machine for codes+ids+centroids")
