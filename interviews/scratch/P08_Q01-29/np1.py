import numpy as np
# Q1 backprop tiny net
rng=np.random.default_rng(0)
X=rng.normal(size=(4,3)); y=rng.normal(size=(4,1))
W1=rng.normal(size=(3,5))*.5; W2=rng.normal(size=(5,1))*.5
def loss(W1,W2):
    h=np.tanh(X@W1); return ((h@W2-y)**2).mean()
h=np.tanh(X@W1); p=h@W2
dp=2*(p-y)/len(y); dW2=h.T@dp; dh=dp@W2.T; dz=dh*(1-h**2); dW1=X.T@dz
eps=1e-6; W1b=W1.copy(); W1b[0,0]+=eps
print("analytic",dW1[0,0],"numeric",(loss(W1b,W2)-loss(W1,W2))/eps)
# Q4 dropout
rng=np.random.default_rng(0)
a=np.ones(100000); p=0.2
mask=(rng.random(a.shape)>=p)/(1-p)
print("mean train",(a*mask).mean())
# Q5 momentum on ill-conditioned quadratic
def run(mom,lr=0.09,steps=50):
    w=np.array([1.,1.]); v=np.zeros(2); H=np.array([10.,.5])
    for _ in range(steps):
        g=H*w; v=mom*v+g; w=w-lr*v
    return 0.5*(H*w*w).sum()
print("sgd",run(0),"mom",run(0.9,lr=0.02))
# Q7 vanishing
for act,name in [(lambda z:1/(1+np.exp(-z)),'sigmoid')]:
    print("sigmoid max deriv",0.25,"0.25^10=",0.25**10)
# Q10 / Q50 Adam bias correction
g=1.0; b1,b2=.9,.999; m=v=0
for t in range(1,4):
    m=b1*m+(1-b1)*g; v=b2*v+(1-b2)*g*g
    print(t,"raw m",round(m,4),"raw step",round(m/np.sqrt(v),3),"corrected",round((m/(1-b1**t))/np.sqrt(v/(1-b2**t)),3))
# Q12 init
rng=np.random.default_rng(0)
for name,sc in [("N(0,1)",lambda n:1.0),("Xavier",lambda n:np.sqrt(1/n)),("He",lambda n:np.sqrt(2/n))]:
    for act in ("tanh","relu"):
        x=rng.normal(size=(512,256))
        for _ in range(20):
            W=rng.normal(size=(256,256))*sc(256); z=x@W
            x=np.tanh(z) if act=="tanh" else np.maximum(z,0)
        print(name,act,"std after 20 layers: %.2e"%x.std())
# Q19
z=np.array([1000.,1001.,1002.])
print("naive",np.exp(z)/np.exp(z).sum() if False else "nan/inf")
m=z.max(); s=np.exp(z-m)/np.exp(z-m).sum(); print("stable",s.round(4), "logsumexp",m+np.log(np.exp(z-m).sum()))
with np.errstate(all='ignore'): print("naive",np.exp(z)/np.exp(z).sum())
# Q23
def conv(H,W,Cin,Cout,k,s=1,p=0):
    return (H+2*p-k)//s+1,(W+2*p-k)//s+1, Cout*(Cin*k*k+1)
print(conv(224,224,3,64,7,2,3), conv(32,32,16,32,3,1,1))
# Q28 / Q46 softmax CE grad check
z=rng.normal(size=4); yv=2
sm=np.exp(z)/np.exp(z).sum(); g=sm.copy(); g[yv]-=1
L=lambda z:-np.log(np.exp(z[yv])/np.exp(z).sum())
num=np.array([(L(z+eps*np.eye(4)[i])-L(z))/eps for i in range(4)])
print(np.allclose(g,num,atol=1e-4))
