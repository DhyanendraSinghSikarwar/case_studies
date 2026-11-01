N, D = 8e9, 15e12
print(D/N, 20*N/1e12)                  # tokens/param, Chinchilla-style D in T tokens
# ILLUSTRATIVE assumptions: equal quality (the big "if"), 2e15 lifetime served tokens
serve = 2e15
for name, n, d in [("70B @1.4T", 70e9, 1.4e12), ("8B @15T", 8e9, 15e12)]:
    train, sv = 6*n*d, 2*n*serve       # train = 6ND, serve = 2N per token
    print(name, f"train {train:.2e} serve {sv:.2e} total {train+sv:.2e}")
be = (6*8e9*15e12 - 6*70e9*1.4e12) / (2*(70e9-8e9))
print(f"break-even served tokens {be:.2e}")
