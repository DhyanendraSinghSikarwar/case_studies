import torch
torch.manual_seed(0)
V, D = 10, 4
old_emb = torch.nn.Embedding(V, D)                  # old vocab: 10 tokens
old = old_emb.weight.data.clone()

# new token used to be split by the old tokenizer into old sub-tokens [3, 5, 7]
parts = [3, 5, 7]
new_emb = torch.nn.Embedding(V + 1, D)              # resized matrix: one extra row
with torch.no_grad():
    new_emb.weight[:V] = old                        # copy old rows
    new_emb.weight[V] = old[parts].mean(dim=0)      # mean-of-sub-tokens init

w = new_emb.weight.detach()
print("old rows unchanged:", torch.equal(w[:V], old))
print("new row == mean of sub-token rows:", torch.allclose(w[V], old[parts].mean(0)))
print("new row norm %.3f | mean old-row norm %.3f" % (w[V].norm(), old.norm(dim=1).mean()))
# with a tied output head, the same row gives the new token's logit: it starts "between" its parts
h = old[7]                                          # hidden state resembling the last sub-token
print("logit new %.3f | logits of its parts %s" % ((h @ w[V]), [round(float(h @ old[i]), 3) for i in parts]))
