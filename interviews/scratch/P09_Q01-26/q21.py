import numpy as np
def pe(T,d):
    pos=np.arange(T)[:,None]; i=np.arange(0,d,2)[None,:]
    ang=pos/10000**(i/d); P=np.zeros((T,d)); P[:,0::2]=np.sin(ang); P[:,1::2]=np.cos(ang); return P
P=pe(50,16); print(np.round(P[1,:4],3), P.shape)
# attention without PE is permutation-equivariant
rng=np.random.default_rng(0); X=rng.normal(size=(5,16)); W=rng.normal(size=(16,16))
def attn(X):
    S=(X@W)@(X@W).T/4; A=np.exp(S-S.max(1,keepdims=True)); A/=A.sum(1,keepdims=True); return A@X
perm=rng.permutation(5); print(np.allclose(attn(X)[perm],attn(X[perm])))
