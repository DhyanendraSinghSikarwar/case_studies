d, heads, mlp, L, r = 4096, 32, 11008, 32, 16     # assumed Llama-7B-like, no GQA
attn = {n: (d, d) for n in ("q", "k", "v", "o")}
mlpm = {"gate": (d, mlp), "up": (d, mlp), "down": (mlp, d)}
n = lambda s: s[0] * s[1]
a = sum(map(n, attn.values())); m = sum(map(n, mlpm.values()))
print(f"per layer attention {a:,} ({100*a/(a+m):.1f}%)  MLP {m:,} ({100*m/(a+m):.1f}%)")
lo = lambda s: r * (s[0] + s[1])
qv = lo(attn["q"]) + lo(attn["v"])
allp = sum(map(lo, attn.values())) + sum(map(lo, mlpm.values()))
print(f"r={r} per layer: q,v only {qv:,}; all linear {allp:,}")
print(f"x{L} layers: q,v only {qv*L:,} ({qv*L/1e6:.1f}M); all linear {allp*L:,} ({allp*L/1e6:.1f}M)")
print(f"base linear params in layers {(a+m)*L/1e9:.2f}B; all-linear LoRA share {100*allp/(a+m):.2f}%")
