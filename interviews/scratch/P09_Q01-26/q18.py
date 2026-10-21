import numpy as np
# probs the model assigned to each true next token
p=np.array([0.2,0.5,0.1,0.4,0.25])
ce=-np.log(p).mean(); print("CE nats",round(ce,3),"PPL",round(np.exp(ce),2))
print("uniform over 10k vocab PPL:",np.exp(-np.log(1/10000)))
