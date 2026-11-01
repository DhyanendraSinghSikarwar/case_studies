def params(L, d, n_h, n_kv, dh, ffn, V, tied=False):
    attn = d*n_h*dh + 2*d*n_kv*dh + n_h*dh*d      # Wq, Wk+Wv, Wo
    mlp = 3*d*ffn                                  # gate, up, down (SwiGLU)
    norms = 2*d
    per = attn + mlp + norms
    emb = V*d; head = 0 if tied else V*d
    tot = L*per + emb + head + d
    return dict(attn=attn, mlp=mlp, per_layer=per, emb=emb, total=tot)
def kv_bytes(L, n_kv, dh, T, B, b=2):
    return 2*L*n_kv*dh*T*B*b
cfgs = {
 "Llama-2-7B (MHA)": dict(L=32,d=4096,n_h=32,n_kv=32,dh=128,ffn=11008,V=32000),
 "Llama-3-8B (GQA)": dict(L=32,d=4096,n_h=32,n_kv=8,dh=128,ffn=14336,V=128256),
}
for n,c in cfgs.items():
    p = params(**c)
    print(n, {k: f"{v:,}" for k,v in p.items()}, f"-> {p['total']/1e9:.2f}B; fp16 weights {p['total']*2/2**30:.1f} GiB")
    print("  KV per token:", kv_bytes(c['L'],c['n_kv'],c['dh'],1,1), "bytes =", kv_bytes(c['L'],c['n_kv'],c['dh'],1,1)/2**10, "KiB")
    for T,B in [(4096,1),(4096,32),(32768,1),(8192,16)]:
        print(f"  T={T} B={B}: {kv_bytes(c['L'],c['n_kv'],c['dh'],T,B)/2**30:.2f} GiB")
