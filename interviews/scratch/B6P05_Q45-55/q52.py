import numpy as np
# GMV(t) = G0*(1 - 2.5*(t-0.10)),  revenue R(t) = t*GMV(t),  G0 = 1 (index)
g=lambda t:1-2.5*(t-0.10)
R=lambda t:t*g(t)
# check the fit reproduces the tested points
assert abs(g(0.12)-0.95)<1e-12 and abs(g(0.10)-1)<1e-12
topt=1.25/5      # R = 1.25t - 2.5t^2 ; dR/dt = 1.25 - 5t = 0
print("revenue-maximising take rate:",topt)
assert abs(topt-0.25)<1e-12
print("revenue index at 10%, 12%, 25%:",round(R(0.10),5),round(R(0.12),5),round(R(topt),5))
gain=R(topt)/R(0.10)-1
print(f"gain vs today: {gain:.4f}; at 12%: {R(0.12)/R(0.10)-1:.4f}")
assert round(gain,4)==0.5625 and round(R(0.12)/R(0.10)-1,3)==0.14
# numeric check of the optimum
ts=np.linspace(0.05,0.45,40001); assert abs(ts[np.argmax(R(ts))]-0.25)<1e-4
print(f"GMV at the optimum: {g(topt):.3f} of today (a {1-g(topt):.1%} fall, 7.5x the 5% fall actually seen at 12%)")
assert round(1-g(topt),3)==0.375
# another curve through the same two points: constant elasticity GMV = (t/0.10)^(-e)
e=-np.log(0.95)/np.log(1.2)
print(f"constant-elasticity curve through (10%,1) and (12%,0.95): e={e:.4f}")
Rc=lambda t:t*(t/0.10)**(-e)
for t in (0.10,0.12,0.25,0.40):
    print(f"  take {t:.0%}: linear revenue {R(t):.4f}  vs constant-elasticity {Rc(t):.4f}  GMV linear {g(t):.3f} vs {(t/0.10)**(-e):.3f}")
assert Rc(0.40)>Rc(0.25)>Rc(0.12)   # no interior optimum here: revenue keeps rising
assert R(0.40)<R(0.25)
# the line through two points: how sensitive is the slope to noise in the 12% test?
rng=np.random.default_rng(3)
sd=0.02   # illustrative: 2% noise on measured GMV index in each arm
slopes=[]
for _ in range(20000):
    g0=1+rng.normal(0,sd); g1=0.95+rng.normal(0,sd)
    slopes.append((g1/g0-1)/0.02)       # fall per unit of take rate (here -2.5 at truth)
slopes=np.array(slopes)
# optimum for slope s (GMV=1+s*(t-0.10)): R=t+s t^2-0.1 s t -> t*=(0.1*s-1)/(2*s)
s=slopes; tstar=(0.1*s-1)/(2*s)
tstar=tstar[s<0]
lo,hi=np.percentile(tstar,[5,95])
print(f"with 2% noise in each arm, the 'optimal' take rate ranges {lo:.2f} to {hi:.2f} (5th to 95th percentile)")
assert hi-lo>0.1
