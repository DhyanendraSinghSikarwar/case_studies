model_mb, cores, pod_gb, reserve_gb = 500, 4, 8, 1.5      # reserve: OS + runtime + headroom
usable_mb = (pod_gb - reserve_gb) * 1024
by_mem = int(usable_mb // (model_mb * 1.3))               # 1.3 = weights + activations/buffers per copy
workers = min(cores, by_mem)
print(f"usable {usable_mb:.0f} MB; each worker ~{model_mb*1.3:.0f} MB -> memory allows {by_mem}")
print(f"cores allow {cores} -> start with {workers} workers, intra_op_threads = {max(1, cores // workers)}")
