import numpy as np
rng=np.random.default_rng(0)
T,d=4,8
X=rng.normal(size=(T,d))
Wq,Wk,Wv=[rng.normal(size=(d,d))/np.sqrt(d) for _ in range(3)]
Q,K,V=X@Wq,X@Wk,X@Wv
S=Q@K.T/np.sqrt(d)
mask=np.triu(np.ones((T,T),bool),1)   # causal mask (decoder)
S=np.where(mask,-1e9,S)
A=np.exp(S-S.max(1,keepdims=True)); A/=A.sum(1,keepdims=True)
print(np.round(A,2)); print((A@V).shape, A.sum(1))
