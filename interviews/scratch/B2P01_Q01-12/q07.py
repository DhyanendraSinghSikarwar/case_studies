# Arithmetic intensity of decode for a 7B model, fp16, batch b (weights dominate bytes)
P = 7e9
for b in (1, 8, 64, 256):
    flops = 2*P*b; bytes_ = 2*P          # weights read once per step
    print(f"batch {b:4d}: {flops/bytes_:6.0f} FLOP/byte")
# A100 80GB approx: 312 TFLOPs bf16, ~2.0 TB/s -> ridge point
print("A100 ridge ~", round(312e12/2.0e12), "FLOP/byte")
# prefill: 2000 tokens at once
print("prefill 2000 tok:", 2*P*2000/(2*P), "FLOP/byte")
print("batch-1 decode lower bound on A100: %.1f ms/token" % (2*P/2.0e12*1e3))
