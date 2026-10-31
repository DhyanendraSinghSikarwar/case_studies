import numpy as np
cap=100; vc=20
p0,p1=100,120
q0,q1=70,62
pr0=q0*(p0-vc); pr1=q1*(p1-vc)
print("nightly profit at 100:",pr0," at 120:",pr1," difference:",pr1-pr0)
drop=1-q1/q0
print(f"demand drop implied by 62 vs 70: {drop:.4f}")
assert pr0==5_600 and pr1==6_200 and round(drop,3)==0.114
# break-even rooms at 120
be=pr0/(p1-vc)
print("break-even rooms at 120:",be,"=> relative drop",round(1-be/q0,3))
assert be==56 and round(1-be/q0,3)==0.2

# nightly demand varies. Illustrative: demand at 100 ~ Normal(70,20) truncated at 0; at 120 it is 62/70 of that
rng=np.random.default_rng(7)
d0=np.clip(rng.normal(70,20,200_000),0,None)
d1=d0*(q1/q0)
s0=np.minimum(d0,cap); s1=np.minimum(d1,cap)
print(f"\nSimulated mean demand at 100: {d0.mean():.1f}; mean rooms sold: {s0.mean():.1f}")
print(f"Mean rooms sold at 120: {s1.mean():.1f}")
m0=(s0*(p0-vc)).mean(); m1=(s1*(p1-vc)).mean()
print(f"Average nightly profit at 100: {m0:.0f}; at 120: {m1:.0f}; difference {m1-m0:.0f}")
print(f"Share of nights sold out at 100: {(d0>=cap).mean():.3f}; at 120: {(d1>=cap).mean():.3f}")
# by demand band
for lo,hi in [(0,50),(50,80),(80,110),(110,500)]:
    k=(d0>=lo)&(d0<hi)
    a=(s0[k]*(p0-vc)).mean(); b=(s1[k]*(p1-vc)).mean()
    print(f"  base demand {lo:>3}-{hi:<3}: profit at 100 {a:7.0f}, at 120 {b:7.0f}, 120 better? {b>a}")
assert s0.mean()<d0.mean()           # capacity censors sales
assert m1>m0
# with a uniform 11.4% drop, 120 beats 100 on every band; the gain is largest on sell-out nights
k=d0>=110; g_peak=(s1[k]*(p1-vc)).mean()-(s0[k]*(p0-vc)).mean()
k=d0<50; g_weak=(s1[k]*(p1-vc)).mean()-(s0[k]*(p0-vc)).mean()
print(f"gain on peak nights {g_peak:.0f} vs weak nights {g_weak:.0f}")
assert g_peak>g_weak>0

# demand differs by night: soft nights (base demand < 70) lose 40% at 120, strong nights lose 0% (illustrative)
drop_n=np.where(d0<70,0.40,0.0)
d1b=d0*(1-drop_n)
s1b=np.minimum(d1b,cap)
flat120=(s1b*(p1-vc)).mean()
by_night=np.where(d0<70,s0*(p0-vc),s1b*(p1-vc)).mean()   # price 100 on soft nights, 120 on strong nights (needs a demand forecast)
print(f"\nSoft nights lose 40%, strong nights 0%: avg rooms at flat 120 = {s1b.mean():.1f}")
print(f"  flat 100: {m0:.0f}  flat 120: {flat120:.0f}  price by night: {by_night:.0f}")
assert by_night>flat120>m0
print(f"  average drop in rooms at flat 120 vs flat 100: {1-s1b.mean()/s0.mean():.3f} (a flat test would call this a ~{(1-s1b.mean()/s0.mean())*100:.0f}% drop)")
print("\nRevenue-only check:",q0*p0,q1*p1,(q1*p1-q0*p0),"plus saved variable cost",(q0-q1)*vc)
assert q0*p0==7_000 and q1*p1==7_440 and (q0-q1)*vc==160 and (q1*p1-q0*p0)+(q0-q1)*vc==600
