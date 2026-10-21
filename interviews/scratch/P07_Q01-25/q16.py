import numpy as np
a = np.array([1.0, 0.0]); 
items = {"popular_big": np.array([4.0, 3.0]), "niche_aligned": np.array([0.9, 0.0]), "off_topic": np.array([0.0, 2.0])}
for n, v in items.items():
    print(f"{n:14s} dot={a@v:5.2f} cos={a@v/np.linalg.norm(a)/np.linalg.norm(v):5.2f} euclid={np.linalg.norm(a-v):5.2f}")
