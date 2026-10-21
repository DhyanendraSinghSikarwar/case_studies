import torch, torch.nn as nn
torch.manual_seed(0)
net = nn.Sequential(nn.Linear(3, 4), nn.Tanh(), nn.Linear(4, 1))
for p in net.parameters(): nn.init.constant_(p, 0.5)
net(torch.randn(8, 3)).sum().backward()
print(net[0].weight.grad)
class MLP(nn.Module):
    def __init__(self, i, h, o):
        super().__init__()
        self.fc1 = nn.Linear(i, h); self.fc2 = nn.Linear(h, o)
        self.drop = nn.Dropout(0.1)
        self.skip = nn.ModuleList([nn.Linear(h, h)])
        self.bad = [nn.Linear(1, 1)]
    def forward(self, x):
        return self.fc2(self.drop(torch.relu(self.fc1(x))))
m = MLP(4, 8, 2)
print([n for n, _ in m.named_parameters()], sum(p.numel() for p in m.parameters()))
torch.manual_seed(0)
def grad_first(skip, depth=30):
    layers = nn.ModuleList(nn.Linear(16, 16) for _ in range(depth))
    x = torch.randn(32, 16); h = x
    for l in layers: h = (h + torch.tanh(l(h))) if skip else torch.tanh(l(h))
    h.pow(2).mean().backward()
    return layers[0].weight.grad.norm().item()
print("plain", grad_first(False), "residual", grad_first(True))
def focal(logits, y, gamma=2.0):
    bce = nn.functional.binary_cross_entropy_with_logits(logits, y, reduction="none")
    p_t = torch.exp(-bce)
    return ((1 - p_t) ** gamma * bce).mean()
l=torch.randn(6,1); y=torch.tensor([0,0,0,0,0,1.]).unsqueeze(1); print(focal(l,y).item())
m=nn.Linear(3,1); m(torch.ones(1,3)*100).sum().backward()
pre=torch.nn.utils.clip_grad_norm_(m.parameters(),1.0); print(pre.item())
