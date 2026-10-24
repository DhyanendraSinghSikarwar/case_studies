import numpy as np
rng = np.random.default_rng(0)

# --- 1) online softmax over one row of scores, processed one block at a time
def online_softmax_denominator(s, block=4):
    m, l = -np.inf, 0.0
    for i in range(0, len(s), block):
        blk = s[i:i+block]
        m_new = max(m, blk.max())
        l = l * np.exp(m - m_new) + np.exp(blk - m_new).sum()   # rescale old sum, add new block
        m = m_new
    return m, l
s = rng.normal(size=19) * 5
m, l = online_softmax_denominator(s)
ref = np.exp(s - s.max()); 
print("max & denominator match:", np.isclose(m, s.max()), np.isclose(l, ref.sum()))
print("softmax match:", np.allclose(np.exp(s - m) / l, ref / ref.sum()))

# --- 2) tiled attention (FlashAttention-style forward, one head) vs standard
def std_attn(Q, K, V, causal=False):
    S = Q @ K.T / np.sqrt(Q.shape[1])
    if causal: S = np.where(np.triu(np.ones_like(S, bool), 1), -np.inf, S)
    P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
    return P @ V

def flash_attn(Q, K, V, Br=16, Bc=32, causal=False):
    N, d = Q.shape
    O = np.zeros_like(Q)
    for i in range(0, N, Br):                       # outer loop: query tile (kept in "SRAM")
        q = Q[i:i+Br]
        m = np.full(len(q), -np.inf); l = np.zeros(len(q)); acc = np.zeros((len(q), d))
        for j in range(0, N, Bc):                   # inner loop: stream K/V tiles
            if causal and j > i + len(q) - 1: break
            S = q @ K[j:j+Bc].T / np.sqrt(d)
            if causal:
                qi = np.arange(i, i+len(q))[:, None]; kj = np.arange(j, j+S.shape[1])[None, :]
                S = np.where(kj > qi, -np.inf, S)
            m_new = np.maximum(m, S.max(1))
            p = np.exp(S - m_new[:, None])
            scale = np.exp(m - m_new)               # exp(-inf - finite) = 0 on the first tile
            l = l * scale + p.sum(1)
            acc = acc * scale[:, None] + p @ V[j:j+Bc]
            m = m_new
        O[i:i+Br] = acc / l[:, None]                # normalise once at the end
    return O

N, d = 200, 32
Q, K, V = (rng.normal(size=(N, d)) * 2 for _ in range(3))
for causal in (False, True):
    print(f"causal={causal}: max abs diff tiled vs standard =", np.abs(flash_attn(Q, K, V, causal=causal) - std_attn(Q, K, V, causal=causal)).max())
# large scores: naive exp overflows, online stays fine
Qb = Q * 100
with np.errstate(over="ignore", invalid="ignore"):
    S = Qb @ K.T / np.sqrt(d); naive = np.exp(S); print("naive exp without max-subtraction has inf:", np.isinf(naive).any())
print("tiled with big scores matches stable standard:", np.allclose(flash_attn(Qb, K, V), std_attn(Qb, K, V)))

