d, r = 4096, 16
full = d * d
lora = r * d + d * r
print(f"full matrix {full:,}  LoRA r={r} {lora:,}  ratio {100*lora/full:.2f}%")
for r in (4, 8, 16, 64):
    print(f"r={r:3d} params {2*r*d:>9,} ({100*2*r*d/full:.2f}%)  scale alpha=2r: {2*r/r}  rsLoRA alpha=16: {16/r**0.5:.2f} vs standard {16/r:.2f}")
