"""Cold-start estimate per option. ALL NUMBERS ARE MADE-UP ASSUMPTIONS, not measurements."""
MODEL_GB = 20            # weights
IMAGE_GB_CODE = 2        # image without weights
NET_GBPS = 1.0           # GB/s from object store to node (assumed)
REGISTRY_GBPS = 0.5      # GB/s image pull (assumed)
DISK_GBPS = 2.0          # GB/s local disk read into GPU memory path (assumed)
PVC_GBPS = 0.8           # GB/s from shared network volume (assumed)
LOAD_S = 20              # seconds for the server to init the model once bytes are local (assumed)
REPLICAS = 4
NODES = 4                # one replica per node
SHARED_STORE_LIMIT_GBPS = 2.0   # object store / PVC aggregate cap (assumed)

def share(per_pod_gbps, pods):   # many pods hitting one source split its aggregate cap
    return min(per_pod_gbps, SHARED_STORE_LIMIT_GBPS / pods)

options = {
 "A baked into image (cold node)":       (MODEL_GB + IMAGE_GB_CODE) / share(REGISTRY_GBPS, NODES) + LOAD_S,
 "A baked into image (image cached)":    LOAD_S,
 "B init container -> emptyDir":         IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / share(NET_GBPS, REPLICAS) + LOAD_S,
 "C node cache (DaemonSet pre-pull), hit": IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / DISK_GBPS + LOAD_S,
 "D RWX/ROX PVC mounted":                IMAGE_GB_CODE / REGISTRY_GBPS + MODEL_GB / share(PVC_GBPS, REPLICAS) + LOAD_S,
 "E stream weights at start":            IMAGE_GB_CODE / REGISTRY_GBPS + max(MODEL_GB / share(NET_GBPS, REPLICAS), LOAD_S),
}
print(f"assumptions: model {MODEL_GB} GB, {REPLICAS} replicas on {NODES} nodes, shared source cap {SHARED_STORE_LIMIT_GBPS} GB/s")
for k, v in options.items():
    print(f"{k:42} ~{v:6.0f} s")
disk_extra = {"A baked into image (cold node)": MODEL_GB, "B init container -> emptyDir": MODEL_GB,
              "C node cache (DaemonSet pre-pull), hit": MODEL_GB, "D RWX/ROX PVC mounted": 0, "E stream weights at start": 0}
print("\nextra node disk per node (GB):", disk_extra)
