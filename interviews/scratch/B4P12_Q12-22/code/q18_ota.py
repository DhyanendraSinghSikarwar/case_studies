"""Q18: model update download time and storage/egress in abstract units (invented inputs)."""
MB, DEVICES, MBPS = 60, 100_000, 2
sec = MB * 8 / MBPS
print(f"one 60 MB update at 2 Mbps: {MB} MB * 8 / {MBPS} = {sec:.0f} s = {sec/60:.1f} min (ideal, no overhead)")
for eff in (1.0, 0.6):
    print(f"  at {eff:.0%} link efficiency: {sec/eff/60:.1f} min")
total_gb = MB * DEVICES / 1000
print(f"fleet transfer: {MB} MB x {DEVICES:,} = {total_gb:,.0f} GB (decimal) per full rollout")
UNIT_STORE, UNIT_EGRESS = 1.0, 1.0   # abstract units per GB-month stored and per GB sent (NOT real prices)
print(f"server storage for 1 copy: {MB/1000:.2f} GB; keep 5 versions: {5*MB/1000:.2f} GB -> {5*MB/1000*UNIT_STORE:.2f} units/month")
print(f"egress per full rollout: {total_gb*UNIT_EGRESS:,.0f} units")
for label, frac in (("delta patch 25% of size", 0.25),):
    print(f"{label}: {total_gb*frac:,.0f} GB, {sec*frac/60:.1f} min per device")
# retries: link drops; with resumable downloads only the lost chunks resend; without, restart
import random; random.seed(18)
def sim(resume, n=2000, drop_p=0.15, chunks=60):
    sent = 0
    for _ in range(n):
        done = 0
        while done < chunks:
            if random.random() < drop_p and not resume: sent += random.randint(1, chunks - done) ; done = 0; continue
            sent += 1; done += 1
            if random.random() < drop_p and resume: sent += 0  # resumes from the last chunk
    return sent / (n * chunks)
print(f"bytes sent / model size, restart-on-drop: {sim(False):.2f}x ; resumable chunks: {sim(True):.2f}x  (toy loss model)")
