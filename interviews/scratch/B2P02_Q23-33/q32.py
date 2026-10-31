N, D = 8e9, 15e12
print("tokens/param:", D/N, "| Chinchilla ~20 tok/param -> compute-optimal D:", 20*N/1e12, "T tokens")
print("train FLOPs 6ND:", f"{6*N*D:.2e}")
# ILLUSTRATIVE toy cost model: all numbers are assumptions
def total(N, D, serve_tokens, usd_per_flop=1e-18*2):   # arbitrary $/FLOP
    train = 6*N*D; serve = 2*N*serve_tokens
    return train, serve, (train+serve)*usd_per_flop
serve = 2e15   # lifetime served tokens (assumed)
# Model A: 70B, 1.4T (about 20 tok/param). Model B: 8B, 15T. Assume equal quality (the big IF).
for name, n, d in [("70B @1.4T", 70e9, 1.4e12), ("8B @15T", 8e9, 15e12)]:
    tr, sv, c = total(n, d, serve)
    print(f"{name}: train {tr:.2e} serve {sv:.2e} total ${c/1e6:.2f}M-equiv")
# break-even served tokens where B total == A total
nA, dA, nB, dB = 70e9, 1.4e12, 8e9, 15e12
be = (6*nB*dB - 6*nA*dA) / (2*(nA-nB))
print("break-even served tokens:", f"{be:.2e}")
