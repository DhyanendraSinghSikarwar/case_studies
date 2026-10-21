import numpy as np
rng=np.random.default_rng(0)
E=rng.normal(size=(10000,64)).astype("float32")
E/=np.linalg.norm(E,axis=1,keepdims=True)       # normalise once -> dot == cosine
q=E[42]+0.1*rng.normal(size=64).astype("float32"); q/=np.linalg.norm(q)
scores=E@q
top=np.argsort(-scores)[:3]; print(top, np.round(scores[top],2))
