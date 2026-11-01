import math
C = 1e23
N = math.sqrt(C / 120); D = 20 * N
print(f"C={C:.0e}: N={N:.3e} ({N/1e9:.1f}B params), D={D:.3e} ({D/1e9:.0f}B tokens), check 6ND={6*N*D:.3e}")
for r in [10, 15, 20, 25]:
    n = math.sqrt(C / (6 * r)); print(f"ratio {r:2d}: N={n/1e9:5.1f}B  D={r*n/1e9:6.0f}B tokens")
# Chinchilla check
Nc, Dc = 70e9, 1.4e12; print("Chinchilla 6ND:", f"{6*Nc*Dc:.2e}", "D/N:", Dc/Nc)
Ng, Dg = 280e9, 300e9; print("Gopher 6ND (D=300B tokens, from memory):", f"{6*Ng*Dg:.2e}")
# model sized for Chinchilla's budget
C2 = 6*Nc*Dc; n2 = math.sqrt(C2/120); print("N* for that C:", round(n2/1e9, 1), "B  D*:", round(20*n2/1e9), "B")
# inference-heavy: overtrain a 7B on 2T
print("7B on 2T tokens: D/N =", round(2e12/7e9), " C =", f"{6*7e9*2e12:.2e}")
