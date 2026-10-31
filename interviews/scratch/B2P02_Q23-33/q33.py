N, D = 7e9, 2e12
F = 6*N*D; print(f"FLOPs: {F:.2e}")
peak, price = 989e12, 2.0     # ASSUMPTIONS: H100-class bf16 dense peak; $2/GPU-hour
for mfu in (0.3, 0.4, 0.5):
    gh = F/(peak*mfu*3600)
    print(f"MFU {mfu:.0%}: {gh:,.0f} GPU-hours, ${gh*price:,.0f}, days on 1024 GPUs: {gh/1024/24:.1f}")
