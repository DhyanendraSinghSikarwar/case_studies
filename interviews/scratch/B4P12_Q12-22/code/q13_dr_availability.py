"""Q13: RTO/RPO table checks and serial-chain availability (invented figures)."""
assets = {  # asset: (RTO min, RPO min, target RTO min, strategy)
 "serving endpoint":   (15, 5, 15, "second Region warm, image digest + model artefact replicated"),
 "feature store":      (60, 5, 60, "online store replicated or rebuilt from stream; offline from versioned tables"),
 "model registry":     (240, 60, 240, "metadata DB backup + artefact bucket versioning/replication"),
 "training pipeline":  (2880, 1440, 2880, "code in git, configs as code, rebuild in other Region; data snapshot restore"),
}
print(f"{'asset':18s}{'RTO(min)':>9s}{'RPO(min)':>9s}  meets target")
for k, (rto, rpo, tgt, s) in assets.items():
    assert rto <= tgt
    print(f"{k:18s}{rto:9d}{rpo:9d}  {rto <= tgt}")

MIN_MONTH = 30 * 24 * 60
def down(a): return (1 - a) * MIN_MONTH
feature, registry_cfg, model_store = 0.999, 0.995, 0.999  # invented dependency availabilities
serial = feature * registry_cfg * model_store
print(f"\nserial chain A*B*C = {feature}*{registry_cfg}*{model_store} = {serial:.6f}  (~{down(serial):.0f} min down per 30 days)")
# dependency B (the weakest) gets a cached fallback that works 90% of the time B is down
cov = 0.90
b_eff = registry_cfg + (1 - registry_cfg) * cov
with_fb = feature * b_eff * model_store
print(f"B with cached fallback covering {cov:.0%} of its outages: {b_eff:.5f}")
print(f"chain with fallback = {with_fb:.6f}  (~{down(with_fb):.0f} min down per 30 days)")
assert with_fb > serial
# hand check: B down 0.5% of time -> 0.005*0.1 = 0.0005 left uncovered
assert abs((1 - b_eff) - 0.0005) < 1e-12
# a region failure takes out everything in that region at once: independence assumption breaks
print("\nIf all three share one Region and it fails, they fail together: the product above is a best case.")
