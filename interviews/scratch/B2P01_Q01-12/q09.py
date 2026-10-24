import torch, time
for n in (1024, 4096, 32768, 131072):
    print(f"n={n:7d}: score matrix per head per layer fp16 = {n*n*2/2**30:8.2f} GiB, x32 heads = {32*n*n*2/2**30:9.1f} GiB")
# sliding-window cost
n, w = 4096, 512
print("full pairs:", n*n, "window pairs ~", n*w, "ratio", n*n/(n*w))
