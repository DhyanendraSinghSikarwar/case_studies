"""VRAM per replica for time-slicing and MIG, plus fit flags. All sizes are made-up round numbers."""
import yaml
cm = next(d for d in yaml.safe_load_all(open("gpu_share.yaml")) if d["kind"] == "ConfigMap")
REPLICAS = yaml.safe_load(cm["data"]["any"])["sharing"]["timeSlicing"]["resources"][0]["replicas"]
print("replicas parsed from the ConfigMap:", REPLICAS)
GPU_GB = 40                                              # assumed whole-GPU memory
MIG_GB = {"1g.5gb": 5, "2g.10gb": 10, "3g.20gb": 20}     # assumed profile sizes
HEADROOM = 1.2                                           # activations, CUDA context, KV cache

def time_slicing(replicas, models_gb):
    share = GPU_GB / replicas
    total = sum(m * HEADROOM for m in models_gb)
    flags = [f"model {m} GB is above the even share {share:g} GB" for m in models_gb if m > share]
    if total > GPU_GB:
        flags.append(f"sum with headroom {total:g} GB > {GPU_GB} GB pool: OOM risk")
    if len(models_gb) > replicas:
        flags.append("more pods than advertised replicas: extra pods stay Pending")
    return flags or ["ok on paper (still no isolation: one pod can eat the pool)"]

def mig(profile, model_gb):
    need = model_gb * HEADROOM
    cap = MIG_GB[profile]
    return "fits" if need <= cap else f"DOES NOT FIT ({need:g} GB needed > {cap} GB, hard cap)"

print(f"time-slicing x{REPLICAS}, models 6,6,6,6 GB:", time_slicing(REPLICAS, [6, 6, 6, 6]))
print(f"time-slicing x{REPLICAS}, models 6,6,6,18 GB:", time_slicing(REPLICAS, [6, 6, 6, 18]))
print("time-slicing x2, models 6,6,6 GB:", time_slicing(2, [6, 6, 6]))
for p in MIG_GB:
    print(f"MIG {p} for a 7 GB model:", mig(p, 7))
