import torch
torch.set_num_threads(1)
# SIMPLIFIED READING, not the papers' code. Toy pair: token log-probs of a short chosen and a long rejected answer.
logp_c = torch.tensor([-1.0, -0.8, -1.2])                 # chosen: 3 tokens
logp_r = torch.tensor([-0.9, -1.0, -1.1, -1.0, -1.2, -1.1, -1.0, -1.3])   # rejected: 8 tokens
ref_c  = torch.tensor([-1.2, -1.0, -1.3])
ref_r  = torch.tensor([-0.9, -1.0, -1.1, -1.0, -1.2, -1.1, -1.0, -1.3])
beta, gamma = 2.0, 0.5
ls = torch.nn.functional.logsigmoid

# DPO: implicit reward = beta * (sum logp - sum logp_ref); needs the reference model
dpo_margin = beta * ((logp_c.sum() - ref_c.sum()) - (logp_r.sum() - ref_r.sum()))
print("DPO  margin:", round(dpo_margin.item(), 3), " loss:", round((-ls(dpo_margin)).item(), 3))

# SimPO-style: implicit reward = beta * average logp (length-normalised), no reference, plus target margin gamma
sim_margin = beta * (logp_c.mean() - logp_r.mean()) - gamma
print("SimPO-style margin:", round(sim_margin.item(), 3), " loss:", round((-ls(sim_margin)).item(), 3))

# what a raw sum-logp reward without normalisation would say (length effect)
print("sum-logp gap chosen - rejected:", round((logp_c.sum() - logp_r.sum()).item(), 3),
      "| mean-logp gap:", round((logp_c.mean() - logp_r.mean()).item(), 3))
