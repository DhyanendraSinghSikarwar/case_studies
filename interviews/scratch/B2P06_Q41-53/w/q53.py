# Standalone, numpy only. TOY: a LINEAR bag-of-words embedding and a pseudo-inverse. This is NOT a real inversion attack (Vec2Text-style
# attacks target real neural embedders); it only shows that an embedding keeps enough information to recover words. Harmless placeholder words.
import numpy as np
rng = np.random.default_rng(0)
V, WORDS_PER_DOC, NDOC = 300, 8, 300
vocab = [f"word{i}" for i in range(V)]
docs = [rng.choice(V, WORDS_PER_DOC, replace=False) for _ in range(NDOC)]          # each doc = 8 distinct words
X = np.zeros((NDOC, V)); [X[i].__setitem__(d, 1.0) for i, d in enumerate(docs)]      # bag-of-words matrix

def leak(dim, noise=0.0):
    W = rng.normal(size=(V, dim)) / np.sqrt(dim)                                     # the "embedder": a fixed random linear map
    E = X @ W + noise * rng.normal(size=(NDOC, dim))                                 # what sits in the vector store (optionally noised)
    X_hat = E @ np.linalg.pinv(W)                                                    # attacker who knows W (or has a copy of the model): pseudo-inverse
    got = np.argsort(-X_hat, 1)[:, :WORDS_PER_DOC]                                   # top-8 recovered words
    return np.mean([len(set(g) & set(d)) / WORDS_PER_DOC for g, d in zip(got, docs)])
print(f"vocabulary {V}, {WORDS_PER_DOC} words per document; fraction of a document's words recovered from its vector alone:")
for dim in (32, 64, 128, 256, 300): print(f"  embedding dim {dim:3d}: {leak(dim):.2f}")
print("with noise added to the stored vectors (dim 128):")
for nz in (0.0, 0.25, 0.5, 1.0): print(f"  noise std {nz:4.2f}: recovered {leak(128, nz):.2f}")
print("example doc words:", [vocab[i] for i in docs[0]])
