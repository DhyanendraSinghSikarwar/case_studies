import numpy as np
from scipy import optimize
a1,a2=6.0,3.0
rev=lambda s1,s2: a1*np.sqrt(s1)+a2*np.sqrt(s2)
B=10
r55=rev(5,5); r82=rev(8,2)
print(f"revenue at 5/5: {r55:.3f}  at 8/2: {r82:.3f}  gain {r82-r55:.3f} ({r82/r55-1:.2%})")
assert round(r55,2)==20.12 and round(r82,2)==21.21 and round(r82-r55,2)==1.09
# marginal returns
m=lambda a,s: a/(2*np.sqrt(s))
print(f"marginal return at 5/5: A {m(a1,5):.3f}, B {m(a2,5):.3f}")
print(f"marginal return at 8/2: A {m(a1,8):.3f}, B {m(a2,2):.3f}")
assert abs(m(a1,8)-m(a2,2))<1e-12 and m(a1,5)>m(a2,5)
# derive the split: s1/s2=(a1/a2)^2
ratio=(a1/a2)**2; s1=B*ratio/(1+ratio)
print("optimal split from s1/s2=(a1/a2)^2:",s1,B-s1)
assert abs(s1-8)<1e-12
res=optimize.minimize_scalar(lambda x:-rev(x,B-x),bounds=(0,B),method='bounded',options={'xatol':1e-10})
print("numeric optimum for channel A:",round(res.x,4))
assert abs(res.x-8)<1e-3
# average ROAS at each point
print(f"average return per unit spend at 8/2: A {rev(8,0)/8:.3f}, B {a2*np.sqrt(2)/2:.3f}  (equal because both curves are k x sqrt(s) with s1/s2 = 4)")
assert abs(6*np.sqrt(8)/8-3*np.sqrt(2)/2)<1e-12

# If the true curves are equal (observational data gave channel A a better-looking fit because it is bought on high-demand days)
true_a=(4.5,4.5)
loss=(true_a[0]*(np.sqrt(5)+np.sqrt(5))) - (true_a[0]*np.sqrt(8)+true_a[1]*np.sqrt(2))
print(f"\nIf both channels truly have coefficient 4.5: revenue at 5/5 {4.5*2*np.sqrt(5):.3f}, at 8/2 {4.5*(np.sqrt(8)+np.sqrt(2)):.3f}; moving loses {loss:.3f}")
assert loss>0.9

# noise in the fitted coefficients: how often does the 8/2 move lose money?
rng=np.random.default_rng(2)
trials=20000
# illustrative: truth is a1=5, a2=3.5 (ratio 1.43); fitted ratio is noisy, say 20% relative error on each coefficient
t1,t2=5.0,3.5
f1=t1*(1+rng.normal(0,0.2,trials)); f2=t2*(1+rng.normal(0,0.2,trials))
f1=np.clip(f1,0.1,None); f2=np.clip(f2,0.1,None)
r=(f1/f2)**2; s1h=B*r/(1+r); s2h=B-s1h
true_rev=t1*np.sqrt(s1h)+t2*np.sqrt(s2h)
true_55=t1*np.sqrt(5)+t2*np.sqrt(5)
worse=(true_rev<true_55).mean()
print(f"With 20% noise on each fitted coefficient, {worse:.1%} of re-fitted 'optimal' splits earn less than 5/5 on the true curves")
print(f"Typical (median) true gain vs 5/5: {np.median(true_rev-true_55):.3f}")
assert 0<worse<1
# extrapolation: channel B was never run near 2 or channel A near 8
print("\nspend ranges implied: A rises 60% (5 to 8), B falls 60% (5 to 2); the data may not cover those ranges")
assert abs(8/5-1-0.6)<1e-12 and abs(1-2/5-0.6)<1e-12
