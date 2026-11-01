import math
def replicas(target_rps, per_replica_rps, utilisation=0.6, spare=1):
    """per_replica_rps = throughput ONE replica sustains while meeting the p99 target (measured, not at saturation).
    utilisation = fraction of that we plan to use (headroom). spare = extra replicas for a failure (N+1)."""
    if target_rps <= 0 or per_replica_rps <= 0 or not 0 < utilisation <= 1 or spare < 0:
        raise ValueError("bad input")
    return math.ceil(target_rps / (per_replica_rps * utilisation)) + spare

def survives_zone_loss(n, zones, target_rps, per_replica_rps, utilisation=1.0):
    """spread evenly over zones; lose the biggest zone; do the rest still carry target_rps at 'utilisation'?"""
    biggest = math.ceil(n / zones)
    return (n - biggest) * per_replica_rps * utilisation >= target_rps
