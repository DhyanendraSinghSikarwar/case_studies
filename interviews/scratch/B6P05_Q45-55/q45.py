firms=40_000; big_share=0.12; adopt=0.25; price=2_400
big=firms*big_share
adopters=big*adopt
pool=adopters*price
print("firms >50 staff:",big)
print("adopters:",adopters)
print("annual revenue pool:",pool)
assert big==4_800 and adopters==1_200 and pool==2_880_000

print("\nAdoption sweep (firms and price fixed)")
sweep={}
for a in (0.10,0.20,0.25,0.30,0.40):
    sweep[a]=big*a*price
    print(f"  adoption {a:.0%}: {big*a:,.0f} firms -> {sweep[a]:,.0f}")
assert sweep[0.10]==1_152_000 and sweep[0.40]==4_608_000
assert abs(sweep[0.40]/sweep[0.10]-4)<1e-9

print("\nOne-at-a-time swing, each input at its own illustrative low/high")
rng={"adoption share":(0.10,0.40,adopt),
     "share of firms >50 staff":(0.08,0.15,big_share),
     "price per year":(1_800,3_000,price)}
base=dict(a=adopt,s=big_share,p=price)
def f(a,s,p): return firms*s*a*p
swing={}
for name,(lo,hi,mid) in rng.items():
    k={"adoption share":"a","share of firms >50 staff":"s","price per year":"p"}[name]
    lo_v=f(**{**base,k:lo}); hi_v=f(**{**base,k:hi})
    swing[name]=hi_v-lo_v
    print(f"  {name:28s} {lo_v:>10,.0f} to {hi_v:>10,.0f}  swing {hi_v-lo_v:>10,.0f}")
assert max(swing,key=swing.get)=="adoption share"
