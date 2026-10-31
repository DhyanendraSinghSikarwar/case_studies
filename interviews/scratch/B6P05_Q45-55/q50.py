orders=1_000_000; fee=4.0; keep_m=15.0; ret_cost=8.0
def margin(n,rate,fee_income):
    kept=n*(1-rate); ret=n*rate
    return kept*keep_m-ret*ret_cost+ret*fee_income, kept, ret
b,kb,rb=margin(orders,0.22,0)
print(f"before: kept {kb:,.0f}, returned {rb:,.0f}, margin {b:,.0f}")
assert kb==780_000 and rb==220_000 and b==9_940_000
n1=orders*0.97
a_fee,ka,ra=margin(n1,0.18,fee)
a_nofee,_,_=margin(n1,0.18,0)
print(f"after (orders {n1:,.0f}, kept {ka:,.0f}, returned {ra:,.0f}):")
print(f"  margin if fee income is kept by the retailer: {a_fee:,.0f}  change {a_fee-b:+,.0f}")
print(f"  margin if fee is ignored:                      {a_nofee:,.0f}  change {a_nofee-b:+,.0f}")
assert abs(a_fee-11_232_600)<1e-6 and abs(a_nofee-10_534_200)<1e-6
# per-order margin and break-even relative drop in orders
pm_b=0.78*15-0.22*8
pm_fee=0.82*15-0.18*8+0.18*4
pm_nofee=0.82*15-0.18*8
print(f"\nper-order margin: before {pm_b:.4f}, after with fee {pm_fee:.4f}, after without fee {pm_nofee:.4f}")
be_fee=1-pm_b/pm_fee; be_nofee=1-pm_b/pm_nofee
print(f"break-even relative drop in orders: with fee {be_fee:.4f}, without fee {be_nofee:.4f}")
assert round(pm_b,2)==9.94 and round(pm_fee,2)==11.58 and round(pm_nofee,2)==10.86
assert round(be_fee,4)==0.1416 and round(be_nofee,4)==0.0847
# check by direct computation at the break-even
n_be=orders*(1-be_fee)
assert abs(margin(n_be,0.18,fee)[0]-b)<1e-3
n_be2=orders*(1-be_nofee)
assert abs(margin(n_be2,0.18,0)[0]-b)<1e-3
print("margin at break-even order levels equals before-margin: OK")
# sensitivity: if returns only fall to 20%
for r in (0.22,0.20,0.18):
    m,_,_=margin(n1,r,fee); print(f"  returns {r:.0%} with 3% fewer orders (fee kept): margin {m:,.0f}")
nofee_same=margin(n1,0.22,0)[0]
print("returns unchanged at 22%, 3% fewer orders, no fee income:",f"{nofee_same:,.0f}")
assert nofee_same<b
print("orders at break-even (fee, no fee):",round(orders*(1-be_fee)),round(orders*(1-be_nofee)))
assert round(orders*(1-be_fee))==858_377 and round(orders*(1-be_nofee))==915_285
assert abs(margin(n1,0.20,fee)[0]-10_864_000)<1e-6 and abs(margin(n1,0.22,fee)[0]-10_495_400)<1e-6
