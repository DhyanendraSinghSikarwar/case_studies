GB = 1e9
def est(P, seq_note=""):
    full = P * (2 + 2 + 12)                    # bf16 w + bf16 g + fp32 master+m+v
    lora_adapter = 0.01 * P                    # ASSUMED ~1% trainable (all-linear, r~16-64)
    lora = P * 2 + lora_adapter * (2 + 2 + 12) # frozen bf16 base + adapter w/g/Adam
    qlora = P * 0.5 * 1.03 + lora_adapter * (2 + 2 + 12)   # 4-bit + ~3% quant-constant overhead (assumed, with double quantization)
    return full / GB, lora / GB, qlora / GB
print("ESTIMATES, GB, excluding activations / CUDA context / fragmentation")
print(f"{'model':6s}{'full FT':>9s}{'LoRA(bf16)':>12s}{'QLoRA':>8s}")
for name, P in (("7B", 7e9), ("13B", 13e9)):
    f, l, q = est(P); print(f"{name:6s}{f:9.0f}{l:12.1f}{q:8.1f}")
print("13B bf16 weights alone:", 13e9 * 2 / GB, "GB; 40 GB headroom for LoRA:", round(40 - est(13e9)[1], 1), "GB")
print("13B QLoRA headroom on 40 GB:", round(40 - est(13e9)[2], 1), "GB")
