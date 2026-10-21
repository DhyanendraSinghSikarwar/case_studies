import torch, torch.nn as nn
from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split
torch.manual_seed(0)
X=torch.randn(1000,10); w=torch.randn(10); y=(X@w+0.5*torch.randn(1000)>0).float()
ds=TensorDataset(X,y); tr,va=random_split(ds,[800,200],generator=torch.Generator().manual_seed(0))
tl=DataLoader(tr,batch_size=64,shuffle=True); vl=DataLoader(va,batch_size=256)
dev="cuda" if torch.cuda.is_available() else "cpu"
model=nn.Sequential(nn.Linear(10,32),nn.ReLU(),nn.Dropout(0.2),nn.Linear(32,1)).to(dev)
opt=torch.optim.AdamW(model.parameters(),lr=1e-2,weight_decay=1e-2)
lossf=nn.BCEWithLogitsLoss()
for ep in range(5):
    model.train(); tot=0
    for xb,yb in tl:
        xb,yb=xb.to(dev),yb.to(dev)
        opt.zero_grad(); loss=lossf(model(xb).squeeze(1),yb); loss.backward(); opt.step()
        tot+=loss.item()*len(xb)
    model.eval(); vt=0; ok=0
    with torch.no_grad():
        for xb,yb in vl:
            xb,yb=xb.to(dev),yb.to(dev); lo=model(xb).squeeze(1)
            vt+=lossf(lo,yb).item()*len(xb); ok+=((lo>0).float()==yb).sum().item()
    print(f"ep{ep} train {tot/len(tr):.3f} val {vt/len(va):.3f} acc {ok/len(va):.3f}")
# Q6 grad accumulation
m=nn.Linear(1,1,bias=False); nn.init.constant_(m.weight,1.0)
x=torch.tensor([[2.0]])
for i in range(2): m(x).sum().backward()
print("accumulated grad",m.weight.grad.item())
m.zero_grad(); print("after zero_grad",m.weight.grad)  # None in torch2
d=nn.Dropout(0.5); d.train(); print(d(torch.ones(6))); d.eval(); print(d(torch.ones(6)))
with torch.no_grad(): print("requires_grad in no_grad:",m(x).requires_grad)
# Q4 torch dropout scaling
torch.manual_seed(0); print("scaled values",torch.unique(nn.Dropout(0.2)(torch.ones(1000))))
# Q9 norm
x=torch.randn(8,4)*3+5
bn=nn.BatchNorm1d(4); ln=nn.LayerNorm(4)
print("BN col means",bn(x).mean(0).detach().round(decimals=3), "LN row means",ln(x).mean(1).detach().round(decimals=3))
# Q15 AdamW vs Adam l2 with huge gradient scale
def final(opt_cls,**kw):
    w=torch.nn.Parameter(torch.tensor([1.0,1.0]))
    o=opt_cls([w],lr=0.1,**kw)
    for _ in range(50):
        o.zero_grad(); (w*torch.tensor([100.0,0.01])*0).sum().backward()  # zero loss grad: pure decay
        o.step()
    return w.detach()
print("Adam l2 pure decay",final(torch.optim.Adam,weight_decay=0.1))
print("AdamW pure decay",final(torch.optim.AdamW,weight_decay=0.1))
# Q14 scheduler
p=nn.Parameter(torch.zeros(1)); o=torch.optim.SGD([p],lr=0.1)
sch=torch.optim.lr_scheduler.OneCycleLR(o,max_lr=0.1,total_steps=10)
lrs=[]
for _ in range(10): o.step(); lrs.append(round(o.param_groups[0]['lr'],4)); sch.step()
print(lrs)
o=torch.optim.SGD([p],lr=0.1); sch=torch.optim.lr_scheduler.CosineAnnealingLR(o,T_max=10); l=[]
for _ in range(10): o.step(); l.append(round(o.param_groups[0]['lr'],4)); sch.step()
print(l)
# Q18
import os,tempfile
f=os.path.join(tempfile.gettempdir(),"p08ck.pt")
mm=nn.Linear(3,2); oo=torch.optim.Adam(mm.parameters())
torch.save({"model":mm.state_dict(),"opt":oo.state_dict(),"epoch":4},f)
ck=torch.load(f,weights_only=True); m2=nn.Linear(3,2); m2.load_state_dict(ck["model"]); print("resume epoch",ck["epoch"]+1, torch.equal(m2.weight,mm.weight))
# Q19
z=torch.tensor([[1000.,1001.,1002.]]); print(torch.softmax(z,1), torch.logsumexp(z,1))
print(nn.CrossEntropyLoss()(z,torch.tensor([2])))
# Q21 params
class MLP(nn.Module):
    def __init__(s,i,h,o):
        super().__init__(); s.fc1=nn.Linear(i,h); s.fc2=nn.Linear(h,o); s.extra=[nn.Linear(1,1)]
    def forward(s,x): return s.fc2(torch.relu(s.fc1(x)))
mlp=MLP(4,8,2); print([n for n,_ in mlp.named_parameters()], sum(p.numel() for p in mlp.parameters()))
# Q23
c=nn.Conv2d(3,64,7,stride=2,padding=3); print(c(torch.zeros(1,3,224,224)).shape, sum(p.numel() for p in c.parameters()))
# Q26 / Q27 clip
m=nn.Linear(3,1); (m(torch.ones(1,3)*100)).sum().backward()
print("norm before",torch.nn.utils.clip_grad_norm_(m.parameters(),1.0).item(), "after",torch.sqrt(sum((p.grad**2).sum() for p in m.parameters())).item())
# Q29
logits=torch.randn(6,1); tgt=torch.tensor([0,0,0,0,0,1.]).unsqueeze(1)
pw=torch.tensor(5.0); print(nn.BCEWithLogitsLoss(pos_weight=pw)(logits,tgt).item())
# Q28/Q20 dataset
class Tab(Dataset):
    def __init__(s,X,y): s.X=torch.as_tensor(X,dtype=torch.float32); s.y=torch.as_tensor(y,dtype=torch.float32)
    def __len__(s): return len(s.X)
    def __getitem__(s,i): return s.X[i],s.y[i]
dl=DataLoader(Tab(torch.randn(10,3).numpy(),torch.arange(10)),batch_size=4,shuffle=False)
print([b[0].shape for b in dl])
def collate(batch):
    xs=[b[0] for b in batch]; L=torch.tensor([len(x) for x in xs])
    return nn.utils.rnn.pad_sequence(xs,batch_first=True), L
dl=DataLoader([(torch.ones(n),0) for n in (2,5,3)],batch_size=3,collate_fn=collate)
xb,L=next(iter(dl)); print(xb.shape,L)
