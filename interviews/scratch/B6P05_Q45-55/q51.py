n=100_000; prem=1000; exp_=200
risky_n=10_000; risky_claims=1100
safe_n=90_000; safe_claims=700
p_risky=prem-exp_-risky_claims
p_safe=prem-exp_-safe_claims
print("profit per policy: risky",p_risky,"safe",p_safe)
tot_risky=risky_n*p_risky; tot_safe=safe_n*p_safe
port=tot_risky+tot_safe
print("risky group total:",tot_risky,"safe group total:",tot_safe,"portfolio:",port)
assert p_risky==-300 and p_safe==100 and tot_risky==-3_000_000 and tot_safe==9_000_000 and port==6_000_000
# portfolio average claims check
avg_claims=(risky_n*risky_claims+safe_n*safe_claims)/n
print("average claims per policy:",avg_claims,"; portfolio profit via average:",n*(prem-exp_-avg_claims))
assert avg_claims==740 and n*(prem-exp_-avg_claims)==port
# reprice risky to 1350, 40% lapse
new_prem=1350; lapse=0.40
stay=risky_n*(1-lapse)
p_stay=new_prem-exp_-risky_claims
risky_after=stay*p_stay
port2=risky_after+tot_safe
print(f"\nrepriced: stay {stay:,.0f} x {p_stay} = {risky_after:,.0f}; portfolio {port2:,.0f}; change {port2-port:+,.0f}")
assert stay==6_000 and p_stay==50 and risky_after==300_000 and port2==9_300_000
# break-even claims for the stayers
be_claims=new_prem-exp_
print("stayers' break-even average claims:",be_claims,"=",round(be_claims/risky_claims-1,4),"above 1,100")
assert be_claims==1150 and round(be_claims/risky_claims-1,3)==0.045
print("\nAdverse selection: stayers' true average claims -> portfolio profit")
for c in (1100,1150,1250,1350):
    pf=stay*(new_prem-exp_-c)+tot_safe
    print(f"  stayers claim {c}: stayers profit {stay*(new_prem-exp_-c):>10,.0f}, portfolio {pf:,.0f}")
assert 6_000*(1350-200-1250)==-600_000
# even if everyone risky lapsed
print("if all 10,000 risky lapse: portfolio",tot_safe)
assert tot_safe>port
# lapse sensitivity at 1100
for l in (0.0,0.4,0.8):
    st=risky_n*(1-l); print(f"  lapse {l:.0%}: portfolio {st*p_stay+tot_safe:,.0f}")
