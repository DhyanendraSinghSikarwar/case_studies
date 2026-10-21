import numpy as np, torch
def softmax(z): z=np.asarray(z,float); e=np.exp(z-z.max()); return e/e.sum()
def min_p(p, m):
    keep = p >= m*p.max(); q = np.where(keep,p,0); return q/q.sum()
logits = np.array([4.0, 3.0, 1.0, 0.0, -1.0])
p = softmax(logits); print("p", p.round(4))
print("min_p .1", min_p(p,.1).round(4))
flat = softmax([1.0,.9,.8,.7,.6]); print("flat kept by min_p .5:", int((flat>=.5*flat.max()).sum()), "of 5")
print("peaked kept by min_p .5:", int((p>=.5*p.max()).sum()))
# order matters: temperature before vs after min-p
for T in (0.5, 2.0):
    a = min_p(softmax(logits/T), .1)     # temp then min_p
    pm = p>=.1*p.max(); b = np.where(pm, softmax(logits/T), 0); b/=b.sum()  # min_p on T=1 probs then temp
    print("T",T,"temp->minp kept",int((a>0).sum()),"minp->temp kept",int((b>0).sum()))
# Q20 penalties
def hf_rep(logits, seen, pen):
    l = logits.copy()
    for t in seen: l[t] = l[t]/pen if l[t]>0 else l[t]*pen
    return l
def openai_pen(logits, counts, freq, pres):
    return logits - freq*counts - pres*(counts>0)
l = np.array([2.0, -1.0, 0.5, 0.0]); print("hf 1.2:", hf_rep(l,[0,1],1.2).round(4))
counts = np.array([3,1,0,0]); print("openai f=.5 p=.5:", openai_pen(l,counts,.5,.5))
p0 = softmax(l); p1 = softmax(hf_rep(l,[0],1.2)); print(p0[0].round(4), p1[0].round(4))
# Q21
rng = np.random.default_rng(0); x = rng.standard_normal(100000).astype(np.float32)
s1 = x.sum(); s2 = x[::-1].sum(); s3 = sum(x.reshape(100,-1).sum(1)); 
print("sum fwd/rev/chunked", s1, s2, s3, s1==s2)
a,b,c = np.float32(1e8), np.float32(-1e8), np.float32(1)
print((a+b)+c, a+(b+c))
# near-tie flips argmax
lo = torch.tensor([1.0000001, 1.0000000]); print(lo.argmax().item(), (lo.bfloat16()).argmax().item(), lo.bfloat16().tolist())
