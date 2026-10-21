import torch, torch.nn as nn
torch.manual_seed(0)
# tiny synthetic "images": class = which half is brighter
def make(n):
    x=torch.randn(n,1,16,16)*0.5; y=torch.randint(0,2,(n,))
    x[y==0,:,:,:8]+=0.6; x[y==1,:,:,8:]+=0.6
    return x,y
xtr,ytr=make(60); xva,yva=make(400)
def augment(x):                      # random crop (pad 2) + noise; no flip: flip would swap the labels here!
    x=nn.functional.pad(x,(2,2,2,2),mode="reflect")
    i,j=torch.randint(0,5,(2,)).tolist()
    return x[:,:,i:i+16,j:j+16]+0.1*torch.randn(x.shape[0],1,16,16)
net=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.BatchNorm2d(8),nn.ReLU(),nn.MaxPool2d(2),
                  nn.Conv2d(8,16,3,padding=1),nn.BatchNorm2d(16),nn.ReLU(),nn.AdaptiveAvgPool2d(1),
                  nn.Flatten(),nn.Dropout(0.3),nn.Linear(16,2))
opt=torch.optim.AdamW(net.parameters(),1e-2,weight_decay=1e-2)
best,bad,patience,best_state=1e9,0,5,None
for ep in range(60):
    net.train(); opt.zero_grad()
    loss=nn.functional.cross_entropy(net(augment(xtr)),ytr); loss.backward(); opt.step()
    net.eval()
    with torch.no_grad(): vl=nn.functional.cross_entropy(net(xva),yva).item(); acc=(net(xva).argmax(1)==yva).float().mean().item()
    if vl<best-1e-4: best,bad,best_state=vl,0,{k:v.clone() for k,v in net.state_dict().items()}
    else:
        bad+=1
        if bad>=patience: break
net.load_state_dict(best_state)
print("stopped at epoch",ep,"best val loss",round(best,3))
