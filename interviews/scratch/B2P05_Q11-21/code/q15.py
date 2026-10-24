import torch
torch.set_num_threads(1)
# SYNTHETIC: DPO per-pair gradient weight = sigmoid(-beta * margin), where
# margin = (logp_c - ref_c) - (logp_r - ref_r) is the implicit-reward gap / beta.
m = torch.tensor([-4.0, -2.0, 0.0, 2.0, 4.0])   # implicit log-ratio margin (positive = correctly ranked)
for beta in [0.1, 0.5, 1.0]:
    z = (beta * m).clone().requires_grad_(True)
    loss = -torch.nn.functional.logsigmoid(z).sum()
    loss.backward()
    w = torch.sigmoid(-beta * m)
    print(f"beta={beta}: loss grad wrt z = {[round(-g,3) for g in z.grad.tolist()]}  weight sigmoid(-beta*m) = {[round(x,3) for x in w.tolist()]}")
# gradient wrt the policy log-probs is beta * weight (per pair); so beta both scales the step and the sigmoid width
for beta in [0.1, 0.5, 1.0]:
    print(f"beta={beta}: grad scale on logp_chosen = {[round(beta*x,3) for x in torch.sigmoid(-beta*m).tolist()]}")
