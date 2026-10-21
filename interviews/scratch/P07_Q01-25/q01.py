import numpy as np
R = np.array([[5,4,0,1],
              [4,5,1,0],
              [1,0,5,4],
              [0,1,4,5]], float)       # 0 = not rated
def cos(M):
    n = np.linalg.norm(M, axis=1, keepdims=True)
    Mn = M / np.where(n == 0, 1, n)
    return Mn @ Mn.T
user_sim = cos(R)            # (users x users)
item_sim = cos(R.T)          # (items x items)
u, i = 0, 2                  # predict user 0 on item 2 (unrated)
# user-based: weighted avg of neighbours' ratings on item i
w = user_sim[u].copy(); w[u] = 0
mask = R[:, i] > 0
print("user-based", round((w[mask] @ R[mask, i]) / w[mask].sum(), 2))
# item-based: weighted avg of user's own ratings on similar items
w2 = item_sim[i].copy(); w2[i] = 0
m2 = R[u] > 0
print("item-based", round((w2[m2] @ R[u, m2]) / w2[m2].sum(), 2))
