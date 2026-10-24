N = 7e9                      # parameters
GB = 1e9
parts = {"bf16 weights": 2, "bf16 grads": 2, "fp32 master weights": 4,
         "Adam m (fp32)": 4, "Adam v (fp32)": 4}
total = sum(parts.values())
for k, b in parts.items():
    print(f"{k:20s} {b} B/param -> {N*b/GB:5.0f} GB")
print(f"total {total} B/param -> {N*total/GB:.0f} GB, before activations")

d = 8                        # data-parallel GPUs
opt, grad, w = 12, 2, 2      # bytes/param: optimizer state (master+m+v), grads, weights
print("plain DP      :", N*(w+grad+opt)/GB, "GB per GPU")
print("ZeRO-1 (opt)  :", N*(w+grad+opt/d)/GB)
print("ZeRO-2 (+grad):", N*(w+(grad+opt)/d)/GB)
print("ZeRO-3 / FSDP :", N*(w+grad+opt)/d/GB)
