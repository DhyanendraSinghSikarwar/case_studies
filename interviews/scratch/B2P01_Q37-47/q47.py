GiB = 2**30
def kv_bytes_per_token(layers, kv_heads, head_dim, bytes_=2): return 2 * layers * kv_heads * head_dim * bytes_
cfgs = {"MHA 32 kv heads": 32, "GQA 8 kv heads": 8, "GQA 4 kv heads": 4}
for name, kvh in cfgs.items():
    b = kv_bytes_per_token(32, kvh, 128)
    print(f"{name:16s}: {b/1024:.0f} KiB/token, 32k ctx = {b*32768/GiB:.2f} GiB per sequence (fp16), {b*32768/2/GiB:.2f} GiB (int8)")
params = 8e9
print("weights 8B: fp16 %.1f GiB, int8 %.1f GiB, 4-bit %.1f GiB" % (params*2/GiB, params/GiB, params/2/GiB))
b = kv_bytes_per_token(32, 8, 128)
for gpu in (24, 40, 80):
    for wb, nm in ((2, "fp16"), (1, "int8")):
        free = gpu*0.9 - params*wb/GiB      # 10% reserved for activations/overheads (assumption)
        print(f"{gpu} GB GPU, {nm} weights: {free:.1f} GiB for KV -> {int(free*GiB // (b*32768))} full 32k sequences (GQA-8, fp16 KV)")
# sliding window layers: half the layers window 4096
full = b*32768; mixed = b/32*(16*32768 + 16*4096)   # per-layer bytes/token * tokens kept per layer
print("GQA-8, half layers windowed to 4k: %.2f GiB vs %.2f GiB" % (mixed/GiB, full/GiB))
