# Q25 claims-photo triage sizing (illustrative)
import math
photos, share, window_h = 20_000, 0.70, 4
raw_B, comp_B, uplink_bps = 1_200_000, 250_000, 500_000
t_raw, t_comp = raw_B * 8 / uplink_bps, comp_B * 8 / uplink_bps
assert t_raw == 19.2 and t_comp == 4.0 and abs(t_raw / t_comp - 4.8) < 1e-9
print(f"upload time: raw {t_raw:.1f} s, compressed {t_comp:.1f} s ({t_raw/t_comp:.1f}x faster)")

peak_photos = photos * share
peak_rate = peak_photos / (window_h * 3600)
assert peak_photos == 14_000 and abs(peak_rate - 0.9722) < 1e-3
gpu_rate = 40
gpus = math.ceil(peak_rate / gpu_rate)
util = peak_rate / gpu_rate
assert gpus == 1 and abs(util - 0.0243) < 1e-3
print(f"peak rate={peak_rate:.3f} photos/s, GPUs needed={gpus}, utilisation={util:.1%}")

# Burst check: even a 10x burst over the even-spread rate
burst = 10 * peak_rate
assert math.ceil(burst / gpu_rate) == 1 and burst < gpu_rate
print(f"10x burst={burst:.2f} photos/s still fits one GPU (use 2 for redundancy)")

# Ingest bandwidth at the server for compressed photos
ingest_bps = peak_rate * comp_B * 8
assert abs(ingest_bps - 1_944_444) < 10
print(f"server ingest at peak ~ {ingest_bps/1e6:.2f} Mbit/s")

# Per claim with 6 photos (invented): customer waits
per_claim_raw, per_claim_comp = 6 * t_raw, 6 * t_comp
assert abs(per_claim_raw - 115.2) < 1e-9 and per_claim_comp == 24.0
print(f"6 photos one after another: raw {per_claim_raw:.1f} s, compressed {per_claim_comp:.1f} s")
# Scoring time per photo on a GPU is 1/40 s
assert 1 / 40 == 0.025
print("GPU scoring time per photo = 0.025 s versus 4.0 s upload: upload is 160x longer")
assert 4.0 / 0.025 == 160
