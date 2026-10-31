import torch
torch.manual_seed(0)
d, T = 16, 6
Wq, Wk, Wv = (torch.randn(d, d) for _ in range(3))
x = torch.randn(T, d)
def full(x):                      # recompute everything, causal
    q, k, v = x@Wq, x@Wk, x@Wv
    s = q@k.T/d**0.5
    s = s.masked_fill(torch.triu(torch.ones(len(x), len(x), dtype=torch.bool), 1), float('-inf'))
    return s.softmax(-1)@v
kc, vc, outs = [], [], []
for t in range(T):                # decode: one new token at a time
    xt = x[t:t+1]
    kc.append(xt@Wk); vc.append(xt@Wv)          # append to cache
    K, V = torch.cat(kc), torch.cat(vc)         # (t+1, d)
    s = (xt@Wq)@K.T/d**0.5                      # (1, t+1): no mask needed
    outs.append(s.softmax(-1)@V)
print("cached == uncached:", torch.allclose(torch.cat(outs), full(x), atol=1e-5))
def kv_bytes(layers, kv_heads, hd, seq, batch, nbytes=2): return 2*layers*kv_heads*hd*seq*batch*nbytes
print("Llama-2-7B  (32L,32kv,128), 4096 ctx, bs1 fp16: %.2f GiB" % (kv_bytes(32,32,128,4096,1)/2**30))
print("Llama-3-8B  (32L, 8kv,128), 8192 ctx, bs1 fp16: %.2f GiB" % (kv_bytes(32,8,128,8192,1)/2**30))
print("Llama-3-8B  per token: %d KiB" % (kv_bytes(32,8,128,1,1)/1024))
