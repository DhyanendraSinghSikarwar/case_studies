import torch.nn as nn
backbone=nn.Sequential(nn.Conv2d(3,16,3),nn.ReLU(),nn.Conv2d(16,32,3),nn.ReLU(),nn.AdaptiveAvgPool2d(1),nn.Flatten())  # stands in for a pretrained net
head=nn.Linear(32,5)
model=nn.Sequential(backbone,head)
def trainable(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)
for p in backbone.parameters(): p.requires_grad=False          # stage 1: feature extraction
print("stage1 trainable:",trainable(model))
for p in backbone[2:].parameters(): p.requires_grad=True        # stage 2: unfreeze top block
print("stage2 trainable:",trainable(model))
import torch
opt=torch.optim.AdamW([{"params":backbone.parameters(),"lr":1e-5},{"params":head.parameters(),"lr":1e-3}])  # discriminative LRs
print([g["lr"] for g in opt.param_groups])
