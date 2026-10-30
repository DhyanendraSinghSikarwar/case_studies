### Q45 ⭐ 🟢 Estimate the revenue pool for a data product in a country with 40,000 firms, of which 12% have more than 50 staff, with 25% of those expected to adopt within 3 years at 2,400 a year. Compute the annual revenue pool, show how adoption of 10% to 40% moves it, and say which input you would validate with data first.
**Asked at:** Market-sizing and unit-economics material (PracHub market-sizing concept page, MBB Prep unit-economics and market-sizing pages, PrepLounge break-even and Leland and RoadToOffer sizing guides); consulting-case guides rather than data-scientist-specific pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** The pool is 40,000 x 12% x 25% x 2,400 = 2.88 million a year (illustrative), and the input I would check first is the adoption rate, because it is the least known and moves the answer 4x between 10% and 40%.

**Clarifying questions:**
- Is "firms" all registered firms or active ones? Many registered firms are dormant, so the base could be too high.
- Is the 25% adoption at the end of year 3, or an average over 3 years? It changes whether 2.88 million is a year-3 run rate or a 3-year average.
- Is 2,400 a year the list price or what firms actually pay after discounts? Revenue pool should use paid price.
- Do firms with 50 staff or fewer matter at all? If they would buy a cheaper tier, the pool is understated.
- Is this the pool for the whole market or the share we could win? A pool is not our revenue.

**Approach:**
1. Write the chain: firms x share in scope x adoption x price.
2. Compute: 40,000 x 12% = 4,800 firms. 25% of 4,800 = 1,200 adopters. 1,200 x 2,400 = 2,880,000 a year.
3. Sweep adoption 10% to 40%: 1,152,000 to 4,608,000. Revenue is linear in adoption, so 40% gives exactly 4x the 10% case.
4. Rank inputs by uncertainty times leverage. Each input is a straight multiplier, so a 10% relative error in any of them gives a 10% error in revenue. The input with the widest plausible range is the one to validate.
5. Name data for it: a pilot conversion rate, win/loss from sales calls, a survey with real purchase intent, adoption of a similar tool in a neighbouring market.
6. Present a range, not one number, and say what we would do at the low end.

**Metrics:**
- Revenue pool = firms in scope x adoption rate x annual price. Numerator: money paid per year. Denominator: not a ratio.
- Adoption rate = adopting in-scope firms / all in-scope firms (1,200 / 4,800 = 25%).
- Guardrail: compare against a top-down check, for example spend per firm on all software. If 2,400 is a large share of that, adoption is probably too high.

**Risks:**
- Stated intent in surveys overstates real purchases.
- The 12% size share may count branches or shells as firms.
- The pool is a ceiling for the product, not a forecast for our revenue.
- One year-3 snapshot hides the ramp: years 1 and 2 earn less.

**What the interviewer scores:**
- Strong: clean chain, arithmetic right, a range, picks the input to validate and says why with data named. Weak: gives one number and says "adoption is uncertain" with no way to test it.
- Strong: separates market pool from our share. Weak: treats the pool as our revenue.
- Strong: notes the linear structure, so each input is equally sensitive per percent. Weak: ranks inputs by gut.

**Example:** Illustrative numbers. 4,800 big firms x 25% = 1,200 adopters x 2,400 = 2.88 million. At 10% adoption: 1.152 million. At 40%: 4.608 million. Weak: "about 3 million, looks good." Strong: "2.9 million at 25%, but 1.2 to 4.6 million across adoption of 10% to 40%, so I would run a paid pilot with 50 firms before investing."

**Code:**
```python
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
```

**Output (my run):**
```
firms >50 staff: 4800.0
adopters: 1200.0
annual revenue pool: 2880000.0

Adoption sweep (firms and price fixed)
  adoption 10%: 480 firms -> 1,152,000
  adoption 20%: 960 firms -> 2,304,000
  adoption 25%: 1,200 firms -> 2,880,000
  adoption 30%: 1,440 firms -> 3,456,000
  adoption 40%: 1,920 firms -> 4,608,000

One-at-a-time swing, each input at its own illustrative low/high
  adoption share                1,152,000 to  4,608,000  swing  3,456,000
  share of firms >50 staff      1,920,000 to  3,600,000  swing  1,680,000
  price per year                2,160,000 to  3,600,000  swing  1,440,000
```

**Follow-ups:**
- *Which input would you validate if adoption were already known?* The price, through a willingness-to-pay test on real quotes.
- *How do you turn the pool into our revenue?* Multiply by an achievable share and a ramp over the years. Part 5 Q19 shows break-even logic for the investment decision.
- *Top-down check?* Compare 2,400 a year against what a firm of that size spends in total on similar tools.

**Common mistakes:**
- Treating 25% as certain.
- Forgetting the 12% filter, or applying it twice.
- Calling the pool "our revenue".
- Sweeping adoption but leaving price and size fixed and calling it a sensitivity analysis.

### Q46 ⭐ 🟡 A vendor fraud model costs 300,000 a year and prevents 70% of 2,000,000 a year of fraud losses (1.4 million). An in-house model costs 500,000 in year 1 and 150,000 a year afterwards, and is expected to prevent 76% (1.52 million). Compute the 3-year net benefit of each and the difference, and say what makes the in-house number optimistic.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** Vendor nets 3.30 million over 3 years, in-house nets 3.76 million, so in-house looks 460,000 better (illustrative), but it wins only if it really prevents more than about 68.3% of losses and ships on time.

**Clarifying questions:**
- Is the 76% measured on our data or a forecast? A forecast from a build plan is usually optimistic.
- How long until the in-house model is live? The 500,000 in year 1 may buy no protection for months.
- Does 150,000 a year cover retraining, monitoring, on-call and labelling? Run cost is the usual hole.
- Does the vendor price rise at renewal? That moves the comparison the other way.
- Are the two prevention rates measured on the same transactions and the same false-positive cost? A model that prevents more but blocks more good customers is not comparable.

**Approach:**
1. Benefit per year = prevention rate x 2,000,000. Vendor 1,400,000. In-house 1,520,000.
2. Net each year = benefit - cost. Sum 3 years.
3. Vendor: 3 x (1,400,000 - 300,000) = 3,300,000.
4. In-house: 3 x 1,520,000 - (500,000 + 150,000 + 150,000) = 4,560,000 - 800,000 = 3,760,000.
5. Difference: 460,000 in favour of in-house.
6. Stress it: find the in-house prevention rate that only ties the vendor, then delay, run-cost and prevention scenarios.
7. Decide: the difference is about 14% of the vendor net, which is small next to the uncertainty. Pilot the vendor, then build only if the in-house shadow test beats it on our data.

**Metrics:**
- Net benefit = losses prevented - total cost, summed over the horizon. Prevention rate = fraud loss stopped / fraud loss without a model.
- Guardrails: false-positive rate and customer friction, time to live, and discounted values if the horizon were longer (no discounting used here).

**Risks:**
- Year-1 delay: if in-house is live for half of year 1, its net falls to 3.0 million and it loses to the vendor by 300,000.
- Prevention is the biggest lever: 1 point of prevention is worth 60,000 over 3 years, so a 7.7 point miss (460,000 / 60,000) erases the 460,000 lead.
- Fraud losses of 2,000,000 are themselves an estimate, and fraudsters adapt.
- Staff cost, key-person risk, and the vendor's data advantage across many clients.

**What the interviewer scores:**
- Strong: correct arithmetic, finds the break-even prevention rate, names delay and run cost. Weak: quotes 460,000 as fact.
- Strong: asks for a shadow test on our data. Weak: trusts both rates.
- Strong: mentions risk, lock-in and option value, not only total. Weak: pure cost comparison.

**Example:** Illustrative numbers. Vendor 3.3 million, in-house 3.76 million. If in-house prevents only 70%, its net is 3.4 million and the lead is 100,000. If it also goes live 6 months late, in-house loses. Weak: "In-house is 460k better, build it." Strong: "It is better only if prevention stays above 68.3% and it ships on time. I would shadow-test first."

**Code:**
```python
loss=2_000_000; years=3
vendor_cost=[300_000]*3
inh_cost=[500_000,150_000,150_000]
vendor_prev=0.70; inh_prev=0.76
v_ben=vendor_prev*loss; i_ben=inh_prev*loss
assert v_ben==1_400_000 and i_ben==1_520_000
v_net=sum(v_ben-c for c in vendor_cost)
i_net=sum(i_ben-c for c in inh_cost)
print("vendor 3-yr net:",v_net)
print("in-house 3-yr net:",i_net)
print("difference (in-house minus vendor):",i_net-v_net)
assert v_net==3_300_000 and i_net==3_760_000 and i_net-v_net==460_000

# in-house prevention rate at which it only ties vendor
tie=(v_net+sum(inh_cost))/(loss*years)
print(f"break-even in-house prevention rate: {tie:.4f}")
assert abs(tie-0.683333)<1e-5 and tie<vendor_prev

print("\nOptimism checks (illustrative)")
# a) year-1 delay: in-house model live for only 6 months of year 1
i_delay=i_net-0.5*i_ben
print("  in-house net if year 1 is half-live:",i_delay, "diff:",i_delay-v_net)
assert i_delay==3_000_000 and i_delay-v_net==-300_000
# b) prevention falls to 70% (same as vendor)
i_70=sum(0.70*loss-c for c in inh_cost)
print("  in-house net at 70% prevention:",i_70,"diff:",i_70-v_net)
assert abs(i_70-3_400_000)<1e-6 and abs(i_70-v_net-100_000)<1e-6
# c) a 1 percentage point prevention change is worth this over 3 years
print("  value of 1 prevention point over 3 years:",0.01*loss*years)
assert 0.01*loss*years==60_000
# d) maintenance cost doubles after year 1
i_m=sum(i_ben-c for c in [500_000,300_000,300_000])
print("  in-house net if run cost is 300k/yr after year 1:",i_m,"diff:",i_m-v_net)
assert i_m==3_460_000
print("  lead as share of vendor net:",round(460_000/v_net,3),"; points of prevention to erase lead:",round(460_000/60_000,2))
assert round(460_000/v_net,2)==0.14 and round(460_000/60_000,1)==7.7
```

**Output (my run):**
```
vendor 3-yr net: 3300000.0
in-house 3-yr net: 3760000.0
difference (in-house minus vendor): 460000.0
break-even in-house prevention rate: 0.6833

Optimism checks (illustrative)
  in-house net if year 1 is half-live: 3000000.0 diff: -300000.0
  in-house net at 70% prevention: 3400000.0 diff: 100000.0
  value of 1 prevention point over 3 years: 60000.0
  in-house net if run cost is 300k/yr after year 1: 3460000.0 diff: 160000.0
  lead as share of vendor net: 0.139 ; points of prevention to erase lead: 7.67
```

**Follow-ups:**
- *Would discounting change it?* Slightly. In-house costs are front-loaded, so discounting hurts it a little.
- *Hybrid?* Buy now, build in parallel, switch when the in-house model beats the vendor in shadow mode.
- *What if the vendor prevention is 70% on its own data, not ours?* Then both numbers need re-measuring on our traffic.

**Common mistakes:**
- Ignoring the build timeline.
- Leaving out the maintenance cost.
- Comparing prevention rates without comparing false positives.
- Treating the 460,000 difference as precise.

### Q47 ⭐ 🟡 A dark store costs 80,000 a month in fixed costs and serves an area expected to give 24,000 orders a month, cutting delivery cost from 3.20 to 2.10 per order (1.10 saved). Compute the break-even monthly orders and the monthly result at forecast volume, and say what else could justify it.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** On delivery savings alone the dark store needs about 72,727 orders a month, which is 3.03 times the 24,000 forecast, and at forecast it loses 53,600 a month (illustrative), so it needs another source of value to be justified.

**Clarifying questions:**
- Is the 1.10 saved a true marginal saving, or an average that includes costs that will not really go away? A saving only counts if the cost leaves.
- Is the 80,000 all fixed, including staff shifts? If staff scale with orders, break-even changes.
- Are the 24,000 orders new orders or orders that would have come from the old stores anyway? Moved orders add only the saving, new orders add margin too.
- What is the order margin before delivery cost? Needed to value extra orders.
- How fast does volume ramp, and for how long can we fund losses?

**Approach:**
1. Contribution per order = saving = 3.20 - 2.10 = 1.10.
2. Break-even orders = fixed cost / contribution = 80,000 / 1.10 = 72,727.3 a month.
3. Result at forecast = 24,000 x 1.10 - 80,000 = 26,400 - 80,000 = -53,600 a month.
4. Frame the gap: fixed cost per forecast order is 3.33 against a 1.10 saving. The saving would need to be 3.33 per order, or volume 3x.
5. Ask what else changes: faster delivery lifting order frequency and basket, fewer late orders and refunds, stock availability, a lower promo need, strategic coverage, option value for growth.
6. Value those with a test or a similar existing store, not by assertion. If extra margin on incremental orders is, for example, 2.23 per forecast order, it would close the gap. That is the number to test.
7. Recommend: do not open on savings alone. Open only if the extra effects are shown, or if the volume forecast is raised with evidence.

**Metrics:**
- Break-even orders = monthly fixed cost / contribution per order.
- Monthly result = orders x contribution - fixed cost.
- Guardrails: delivery time, late rate, order growth in the zone, cannibalisation of nearby stores.

**Risks:**
- Volume forecast and saving per order are both uncertain; the answer is very sensitive to volume.
- Saving per order may fall if the store is under-used (couriers idle).
- Ramp-up: months of losses before volume arrives. At 5% monthly growth it takes 23 months to reach 72,727.
- Cannibalising an existing profitable store.

**What the interviewer scores:**
- Strong: says plainly it does not break even at forecast and quantifies the gap. Weak: computes break-even and says "we will grow into it".
- Strong: separates incremental orders from moved orders. Weak: counts all 24,000 as new.
- Strong: proposes what to test (pilot zone, volume ramp). Weak: lists benefits with no numbers.

**Example:** Illustrative numbers. Break-even 72,727. Forecast 24,000. Result -53,600 a month. Weak: "Break-even is 72,727 orders, so we need to grow." Strong: "At forecast it loses 53,600 a month. It needs 3.03x volume, or about 2.23 extra margin per order from other effects. I would pilot before committing."

**Code:**
```python
fixed=80_000; orders=24_000; save=3.20-2.10
assert abs(save-1.10)<1e-12
be=fixed/save
print(f"break-even orders/month: {be:,.1f}  ({be/orders:.2f}x forecast)")
res=orders*save-fixed
print("monthly result at forecast:",round(res,2))
print(f"fixed cost per forecast order: {fixed/orders:.2f} vs saving per order {save:.2f}")
assert round(be,1)==72_727.3 and round(res,2)==-53_600.00
assert 3<be/orders<3.1
# what would have to be true at forecast volume
need_save=fixed/orders
print(f"saving per order needed at 24,000 orders: {need_save:.2f}")
assert round(need_save,2)==3.33
# what other value could close the gap
gap=-res
print("gap per month:",round(gap,2),"= per forecast order:",round(gap/orders,2))
assert round(gap/orders,2)==2.23
# volume growth: months of growth at 5%/month to reach break-even
m=0; v=orders
while v<be:
    v*=1.05; m+=1
print("months at 5% monthly growth to reach break-even:",m)
assert m==23
```

**Output (my run):**
```
break-even orders/month: 72,727.3  (3.03x forecast)
monthly result at forecast: -53600.0
fixed cost per forecast order: 3.33 vs saving per order 1.10
saving per order needed at 24,000 orders: 3.33
gap per month: 53600.0 = per forecast order: 2.23
months at 5% monthly growth to reach break-even: 23
```

**Follow-ups:**
- *How would you cut the break-even?* Lower fixed cost (smaller store, shared staff), raise saving per order (batching), or raise margin per order.
- *Would you open it anyway?* Only if the strategic value is stated and capped, for example a fixed budget for a fixed number of months.
- *What is the single most important number?* Volume, since break-even is 3 times the forecast.

**Common mistakes:**
- Stopping at the break-even number without comparing it to the forecast.
- Counting moved orders as incremental.
- Treating average cost savings as marginal.
- Ignoring the ramp period.

### Q48 ⭐ 🟡 A 100-room hotel sells 70 rooms a night at 100 and expects to sell 62 at 120, about 11% fewer than 70, with 20 of variable cost per occupied room. Compute nightly profit at each price, and say why a flat comparison is not enough when demand varies by night.
**Asked at:** Dynamic-pricing and surge material (a Dataford surge-pricing switchback question, Codemia and Final Round AI pages on designing surge pricing for Uber or Lyft, a Prepfully pricing-riders product case, a Glassdoor Uber entry as listed in snippets); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** At 120 the hotel makes 62 x 100 = 6,200 a night against 70 x 80 = 5,600 at 100, so 120 wins by 600 on the average night (illustrative), but demand and price sensitivity change by night, so I would price by night, not pick one flat price.

**Clarifying questions:**
- Where do the 70 and 62 come from? Average of a test, a model forecast, or a guess? A guess makes the whole comparison weak.
- Does the 62 at 120 hold on every night or only on average? Weekend and weekday demand differ a lot.
- Is 20 the only variable cost? Cleaning, commissions and breakfast can change the margin per room.
- Can the hotel see turned-away demand (sold-out nights)? Without it, sales understate demand.
- Do guests who see 120 go to a competitor or book another night? That decides whether lost rooms come back.

**Approach:**
1. Margin per room: at 100 it is 80, at 120 it is 100.
2. Profit at 100: 70 x 80 = 5,600. At 120: 62 x 100 = 6,200. Difference: +600 a night.
3. The demand fall implied is 1 - 62/70 = 11.4%, which the prompt rounds to about 11%.
4. Break-even: 120 needs only 5,600 / 100 = 56 rooms, a 20% fall from 70. So 120 wins unless demand falls by more than 20%.
5. Now add nights. Capacity is 100 rooms. On a peak night demand at 100 already exceeds 100, so raising the price loses nobody and every room earns 20 more. On a soft night, the room loss is real.
6. Simulate (illustrative demand, mean 70, sd 20, capped at 100 rooms): flat 120 beats flat 100 by about 640 a night. Gains are about 1,960 on peak nights and 339 on soft nights.
7. If soft nights are more price sensitive (they lose 40% at 120, strong nights 0%), flat 120 earns 5,862, flat 100 earns 5,555, and pricing by night earns 6,403. Price by night wins.
8. To estimate sensitivity by night type, run price tests by randomised dates or room types, controlling for day of week and events.

**Metrics:**
- Profit per available room night = rooms sold x (price - variable cost) / rooms available. Revenue per available room is a guardrail but ignores cost.
- Occupancy = rooms sold / 100. Sell-out share = nights with demand at or above capacity / all nights.
- Guardrails: repeat bookings, review score, cancellation rate.

**Risks:**
- Averages hide the sell-out nights, where sales are capped and demand is censored.
- Price effects differ by segment and season.
- Competitor prices and events move demand independently of our price.
- Selection: a price change tested on quiet weeks looks worse than it is.

**What the interviewer scores:**
- Strong: correct profit, break-even demand fall, and the capacity point (sold-out nights give free price increases). Weak: compares 70 x 100 with 62 x 120 using revenue only, forgetting variable cost.
- Strong: proposes price by night with randomised testing. Weak: says "just run an A/B test" with no thought about dates or capacity.
- Strong: notes the 70 is censored on busy nights. Weak: treats observed sales as demand.

**Example:** Illustrative numbers. 70 x 80 = 5,600 against 62 x 100 = 6,200. Break-even is 56 rooms. Weak: "120 is better, by 600, ship it." Strong: "On average yes, but I would raise price on the peak nights first, and test the soft nights separately, because the gain is mostly from nights that are already full."

**Code:**
```python
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
```

**Output (my run):**
```
nightly profit at 100: 5600  at 120: 6200  difference: 600
demand drop implied by 62 vs 70: 0.1143
break-even rooms at 120: 56.0 => relative drop 0.2

Simulated mean demand at 100: 70.0; mean rooms sold: 69.4
Mean rooms sold at 120: 61.9
Average nightly profit at 100: 5555; at 120: 6192; difference 637
Share of nights sold out at 100: 0.067; at 120: 0.016
  base demand   0-50 : profit at 100    3161, at 120    3499, 120 better? True
  base demand  50-80 : profit at 100    5271, at 120    5836, 120 better? True
  base demand  80-110: profit at 100    7217, at 120    8049, 120 better? True
  base demand 110-500: profit at 100    8000, at 120    9960, 120 better? True
gain on peak nights 1960 vs weak nights 339

Soft nights lose 40%, strong nights 0%: avg rooms at flat 120 = 58.6
  flat 100: 5555  flat 120: 5862  price by night: 6403
  average drop in rooms at flat 120 vs flat 100: 0.156 (a flat test would call this a ~16% drop)

Revenue-only check: 7000 7440 440 plus saved variable cost 160
```

**Follow-ups:**
- *Why does revenue alone mislead?* 70 x 100 = 7,000 vs 62 x 120 = 7,440, a gap of 440 instead of 600, because it misses the 160 of variable cost saved on the 8 rooms not sold (440 + 160 = 600).
- *How do you measure demand on sold-out nights?* Log turned-away requests, searches and abandoned bookings, or fit a censored model like Part 5 Q53.
- *Could this be a bandit?* Yes, once you have a few price points and enough nights.

**Common mistakes:**
- Using revenue instead of profit.
- Using one average demand drop for every night.
- Ignoring the capacity cap.
- Testing price on a few nights and attributing weekday-weekend swings to price.

### Q49 ⭐ 🟡 A growth team issued 100,000 first-order vouchers worth 6 each, and 25,000 were redeemed. An audit estimates that 20% of redeemers (5,000) would have ordered anyway, so 20,000 are new customers, each delivering 9 of 90-day margin before the voucher cost. Compute the voucher cost per incremental customer and the net value, and say how you would measure the 20% share.
**Asked at:** Promotion and incrementality material (Talon.One and Uniqodo pages on promotion ROI and incrementality, an INFORMS Management Science paper on whether coupons expand or cannibalise revenue, an incrmntal post on promos and ad spend); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** Voucher cost is 25,000 x 6 = 150,000; with 20,000 incremental customers that is 7.50 per incremental customer, and the net is 20,000 x 9 - 150,000 = +30,000 (illustrative), but it turns negative once more than a third of redeemers would have ordered anyway.

**Clarifying questions:**
- How was the 20% "would have ordered anyway" estimated? If by survey or by matching, it is shaky. A randomised holdout is the proper answer.
- Is the 9 of 90-day margin net of delivery, support and fraud? It must be contribution, not revenue.
- Do the 5,000 non-incremental redeemers still get the 6? Yes, and that cost is already in the 150,000.
- Is there any value after day 90? A 90-day window ignores later orders and also ignores later churn.
- Was there voucher abuse (multiple accounts)? Abuse inflates both redemptions and "new" customers.

**Approach:**
1. Cost: redeemed x value = 25,000 x 6 = 150,000. Unredeemed vouchers cost nothing.
2. Incremental customers: 25,000 x (1 - 0.20) = 20,000.
3. Cost per incremental customer = 150,000 / 20,000 = 7.50, against 9 of margin each.
4. Net = 20,000 x 9 - 150,000 = +30,000. Only incremental customers count for margin; the 5,000 would have ordered anyway so their margin is not caused by the voucher.
5. Break-even: 150,000 / 9 = 16,667 incremental customers, which is 66.7% of redeemers. So the non-incremental share can be up to 33.3% before the net is zero.
6. At 40% non-incremental the net is -15,000. The decision is sensitive to a number we only estimated.
7. Measure the share: randomise vouchers (for example 50% eligible, 50% not), compare first-order rates, and count the incremental share as (treated rate - control rate) x eligible / redeemers. Run it long enough to see pull-forward and later retention.

**Metrics:**
- Cost per incremental customer = total voucher cost / (treated first-order customers - control first-order customers, scaled to group size).
- Net value = incremental customers x contribution margin - voucher cost.
- Guardrails: later repeat rate, abuse flags, margin after the voucher period.

**Risks:**
- Audit estimate of 20% is soft; the net swings from +75,000 (0%) to -60,000 (60%).
- Pull-forward: users who would have ordered next week order now.
- Voucher-hunters churn after the voucher.
- Unequal groups if the audit compares redeemers with non-redeemers (selection).

**What the interviewer scores:**
- Strong: costs only redeemed vouchers, counts margin only for incremental customers, gives break-even share. Weak: 100,000 x 6 as cost, or counts margin from all 25,000.
- Strong: proposes a randomised holdout and explains how to read it. Weak: "ask users in a survey".
- Strong: mentions long-run value and abuse. Weak: stops at day 90.

**Example:** Illustrative numbers. 20,000 x 9 = 180,000 margin, minus 150,000 cost, gives +30,000. At 40% non-incremental, 15,000 x 9 = 135,000, a loss of 15,000. Weak: "30% redemption... fine." Strong: "It pays only while at least two thirds of redeemers are truly new. I would randomise the next voucher wave to measure that."

**Code:**
```python
issued=100_000; value=6; redeemed=25_000
cost=redeemed*value
non_incr=0.20*redeemed
incr=redeemed-non_incr
margin=9
print("voucher cost:",cost,"incremental customers:",incr)
cpic=cost/incr
net=incr*margin-cost
print("voucher cost per incremental customer:",cpic)
print("net value:",net)
assert cost==150_000 and incr==20_000 and cpic==7.5 and net==30_000
print("redemption rate:",redeemed/issued)
# break-even incremental share
be_inc=cost/margin
print(f"break-even incremental customers: {be_inc:,.0f} = {be_inc/redeemed:.4f} of redeemers (non-incremental share {1-be_inc/redeemed:.4f})")
assert round(be_inc)==16_667 and round(1-be_inc/redeemed,3)==0.333
print("\nSensitivity to the non-incremental share:")
for s in (0.0,0.2,1/3,0.4,0.6):
    inc=redeemed*(1-s); print(f"  {s:.2%} non-incremental: incremental {inc:>7,.0f}, net {inc*margin-cost:>9,.0f}, cost per incremental {cost/inc:5.2f}")
assert 20_000*margin-cost>0 and 15_000*margin-cost<0
# measuring the share with a randomised holdout (illustrative, built to match the audit's 20%):
# 100,000 eligible users get vouchers, 100,000 do not. Organic first-order rate 5%. 25% redeem; 80% of redeemers are new.
import numpy as np
rng=np.random.default_rng(11)
n=100_000
p_ctrl=0.05
p_treat=0.05+0.20      # 5,000 organic orders + 20,000 voucher-driven new orders
c=rng.binomial(n,p_ctrl); t=rng.binomial(n,p_treat)
lift=t/n-c/n
se=((t/n)*(1-t/n)/n+(c/n)*(1-c/n)/n)**0.5
print(f"\nHoldout sim: treated first-order rate {t/n:.4f}, control {c/n:.4f}, lift {lift:.4f} +/- {1.96*se:.4f}")
redeemers=redeemed
inc_share=lift*n/redeemers
print(f"measured incremental share of redeemers: {inc_share:.3f} (design value 0.800); non-incremental {1-inc_share:.3f}")
assert abs(lift-0.20)<4*se and abs(inc_share-0.8)<0.03
```

**Output (my run):**
```
voucher cost: 150000 incremental customers: 20000.0
voucher cost per incremental customer: 7.5
net value: 30000.0
redemption rate: 0.25
break-even incremental customers: 16,667 = 0.6667 of redeemers (non-incremental share 0.3333)

Sensitivity to the non-incremental share:
  0.00% non-incremental: incremental  25,000, net    75,000, cost per incremental  6.00
  20.00% non-incremental: incremental  20,000, net    30,000, cost per incremental  7.50
  33.33% non-incremental: incremental  16,667, net         0, cost per incremental  9.00
  40.00% non-incremental: incremental  15,000, net   -15,000, cost per incremental 10.00
  60.00% non-incremental: incremental  10,000, net   -60,000, cost per incremental 15.00

Holdout sim: treated first-order rate 0.2523, control 0.0495, lift 0.2028 +/- 0.0030
measured incremental share of redeemers: 0.811 (design value 0.800); non-incremental 0.189
```

**Follow-ups:**
- *Why not compare redeemers with non-redeemers?* Redeemers are the keen ones, so the gap overstates the effect. Compare the whole eligible group with a randomised control.
- *What if margin includes later orders?* Extend the window and discount it; the break-even share moves up.
- *Is there a cheaper design?* A smaller voucher or a threshold (for example spend 30 to get 6) can cut the non-incremental redeemers.

**Common mistakes:**
- Costing all 100,000 vouchers.
- Counting margin from non-incremental redeemers.
- Estimating the non-incremental share from redeemers versus non-redeemers.
- Ignoring abuse.

### Q50 ⭐ 🟡 A retailer with 1,000,000 orders a year and a 22% return rate (of orders) plans to charge 4.00 for returns. It expects returns to fall to 18% of orders (4 points absolute) and orders to fall by 3% relative to today. A kept order earns 15 of margin, and a returned order earns nothing and costs 8 to handle. Compute annual margin before and after, and the relative order drop at which the change breaks even.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** Annual margin goes from 9.94 million to 11.23 million if the retailer keeps the 4.00 fee, or to 10.53 million if the fee is ignored (illustrative), and the policy breaks even only if orders fall by about 14.2% (or 8.5% without the fee income), against the 3% expected.

**Clarifying questions:**
- Does the 4.00 go to the retailer as income, or does it just cover a cost? The prompt does not say, so I show both. It moves the break-even drop from 14.2% to 8.5%.
- Is the return fall to 18% measured or hoped for? It is the biggest lever.
- Will the 3% order drop be spread evenly? Losing high-margin repeat buyers costs more than 3% of margin.
- Is the 8 handling cost only warehouse work? Refund processing and resale discount also matter.
- Does the fee apply to all returns or only some categories (for example fashion)?

**Approach:**
1. Before: 1,000,000 orders. Returned 220,000, kept 780,000. Margin = 780,000 x 15 - 220,000 x 8 = 11,700,000 - 1,760,000 = 9,940,000. Per order: 9.94.
2. After: orders = 970,000. Returns at 18% = 174,600. Kept = 795,400. Kept margin = 11,931,000. Handling = 1,396,800.
3. With fee income: + 174,600 x 4 = 698,400. Margin = 11,232,600, a gain of 1,292,600.
4. Without fee income: 10,534,200, a gain of 594,200.
5. Break-even drop in orders: per-order margin after is 11.58 (with fee) or 10.86 (without). Orders can fall until 11.58 x N = 9.94 million. N = 858,377, a relative fall of 14.16%. Without fee: 915,285 orders, a fall of 8.47%.
6. Sensitivity (fee kept, 3% fewer orders): returns at 20% give 10,864,000; returns unchanged at 22% give 10,495,400, still above 9,940,000 only because of fee income. Without fee income, unchanged returns would be a clear loss. So the gain depends on the fee income and on the return rate falling.
7. Test: randomise the fee by user or region and measure orders, return rate, and 6-month repeat purchase.

**Metrics:**
- Margin per original order = (kept orders x 15 - returned orders x 8 + returned orders x fee) / original orders.
- Return rate = returned orders / orders. Order retention = orders after / orders before.
- Guardrails: conversion, repeat rate, customer-service contacts, share of lost orders that were low-return buyers.

**Risks:**
- Selection: the 3% of lost orders may be the customers with high return rates (good for margin) or loyal ones (bad).
- Customers may switch to a rival, with long-run effects beyond a year.
- Some of the return fall is mix shift (buyers who return a lot now order less), so the 18% and the 3% are linked.
- Fee could cause chargebacks or complaints.

**What the interviewer scores:**
- Strong: separates kept, returned, and fee income, and states the fee assumption. Weak: multiplies orders by 15 only.
- Strong: solves break-even for the order drop with per-order margins. Weak: tries a fixed table by trial and error.
- Strong: proposes a randomised test and a long window. Weak: trusts the forecast.

**Example:** Illustrative numbers. Before 9,940,000. After with fee 11,232,600. Break-even order drop 14.2%. Weak: "Returns fall 4 points, so margin rises." Strong: "It rises by 1.29 million if the fee is income, but the real risk is lost loyal buyers, so I would test it on a sample first."

**Code:**
```python
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
```

**Output (my run):**
```
before: kept 780,000, returned 220,000, margin 9,940,000
after (orders 970,000, kept 795,400, returned 174,600):
  margin if fee income is kept by the retailer: 11,232,600  change +1,292,600
  margin if fee is ignored:                      10,534,200  change +594,200

per-order margin: before 9.9400, after with fee 11.5800, after without fee 10.8600
break-even relative drop in orders: with fee 0.1416, without fee 0.0847
margin at break-even order levels equals before-margin: OK
  returns 22% with 3% fewer orders (fee kept): margin 10,495,400
  returns 20% with 3% fewer orders (fee kept): margin 10,864,000
  returns 18% with 3% fewer orders (fee kept): margin 11,232,600
returns unchanged at 22%, 3% fewer orders, no fee income: 9,641,800
orders at break-even (fee, no fee): 858377 915285
```

**Follow-ups:**
- *Why does the 4 point fall matter so much?* Each avoided return turns a cost of 8 into a kept order worth 15, a swing of 23 per order.
- *What if only high-return categories are charged?* The fee hits the buyers who cost most, and order loss is probably smaller.
- *Free returns elsewhere?* Part 5 Q20 shows per-order contribution in the same way.

**Common mistakes:**
- Ignoring the 8 handling cost on returned orders.
- Applying the order drop only to kept orders.
- Mixing up the 4 point absolute fall with a relative one.
- Not saying whether the fee is income.

### Q51 ⭐ 🔴 An insurer has 100,000 policies at a premium of 1,000 with 200 of expenses each, and a new risk model finds 10,000 policies with expected claims of 1,100 while the other 90,000 average 700. Compute profit for each group and the portfolio, then reprice the risky group to 1,350 assuming 40% of them lapse, compute the new portfolio profit, and say what adverse selection implies for the 1,100 figure.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** The risky group loses 3.0 million, the rest earns 9.0 million, so the portfolio makes 6.0 million; repricing the risky group to 1,350 lifts it to 9.3 million on paper (illustrative), but adverse selection means the people who stay will likely claim more than 1,100, and the cushion is only 50 a policy.

**Clarifying questions:**
- Are the 1,100 and 700 expected claims from a back-test or only a model estimate? Model error on a 10,000 group can be large.
- Do expenses of 200 fall when a policy lapses? Here I assume yes.
- Is repricing allowed by the regulator, and can we price by this risk factor at all? Some factors cannot be used.
- Will competitors see the same signal? If they price the 90,000 safe policies lower, we lose the profitable ones.
- Why 40% lapse? Is it measured from a price test or assumed?

**Approach:**
1. Profit per policy: risky = 1,000 - 200 - 1,100 = -300. Rest = 1,000 - 200 - 700 = +100.
2. Totals: risky 10,000 x -300 = -3,000,000. Rest 90,000 x 100 = 9,000,000. Portfolio 6,000,000. Average claims are 740, which gives the same 6.0 million.
3. Reprice risky to 1,350: 40% lapse, so 6,000 remain. Profit per remaining policy = 1,350 - 200 - 1,100 = +50. Total 300,000.
4. New portfolio = 300,000 + 9,000,000 = 9,300,000, a gain of 3.3 million.
5. Adverse selection: the 1,100 is the average of the whole risky group. The 40% who leave are probably the less risky ones, who shop around. The 6,000 who stay may average more than 1,100. Break-even for stayers is 1,350 - 200 = 1,150, only 4.5% above 1,100. At 1,250 the group loses 600,000. Portfolio stays above the 6.0 million baseline in these cases, because lapses also remove loss-making policies, but the "+300,000" is not safe.
6. Bigger risk is on the other side: the 90,000 good policies earn 9.0 million. If a rival prices them lower, we are left with the worst risks. Monitor lapse by risk band.
7. Roll out in steps, a randomised or phased increase, and track claims for stayers, not only price acceptance.

**Metrics:**
- Profit per policy = premium - expenses - expected claims. Loss ratio = claims / premium (for example 1,100 / 1,350 = 81.5% after repricing).
- Lapse rate by risk band = lapsed policies / policies in the band.
- Guardrails: claims of stayers versus the model, rate-change complaints, regulatory limits.

**Risks:**
- Adverse selection: those who accept a rise know something the model does not.
- Model error: the 1,100 may be wrong, and a risky group chosen by a model suffers "winner's curse" (the group selected for high predicted claims is partly selected for model error, so true claims may be lower, which works the other way).
- The safe group is poached.
- Fairness and regulation.

**What the interviewer scores:**
- Strong: gets both groups and the portfolio right, then reprices, then explains why stayers differ from the group average. Weak: reprices and says "profit goes up".
- Strong: gives the break-even claims (1,150). Weak: no sensitivity.
- Strong: worries about the 90,000, not only the 10,000. Weak: only the risky group.

**Example:** Illustrative numbers. Before: -3.0 million + 9.0 million = 6.0 million. After: 0.3 million + 9.0 million = 9.3 million. Stayers' claims at 1,250: -0.6 million, portfolio 8.4 million. Weak: "Repricing adds 3.3 million." Strong: "It adds up to 3.3 million, but only if stayers claim about 1,100, and the margin is just 50 a policy."

**Code:**
```python
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
print("loss ratio after repricing:",round(risky_claims/new_prem,4))
assert round(risky_claims/new_prem,3)==0.815
```

**Output (my run):**
```
profit per policy: risky -300 safe 100
risky group total: -3000000 safe group total: 9000000 portfolio: 6000000
average claims per policy: 740.0 ; portfolio profit via average: 6000000.0

repriced: stay 6,000 x 50 = 300,000; portfolio 9,300,000; change +3,300,000
stayers' break-even average claims: 1150 = 0.0455 above 1,100

Adverse selection: stayers' true average claims -> portfolio profit
  stayers claim 1100: stayers profit    300,000, portfolio 9,300,000
  stayers claim 1150: stayers profit          0, portfolio 9,000,000
  stayers claim 1250: stayers profit   -600,000, portfolio 8,400,000
  stayers claim 1350: stayers profit -1,200,000, portfolio 7,800,000
if all 10,000 risky lapse: portfolio 9000000
  lapse 0%: portfolio 9,500,000
  lapse 40%: portfolio 9,300,000
  lapse 80%: portfolio 9,100,000
loss ratio after repricing: 0.8148
```

**Follow-ups:**
- *Why does lapse help here?* Each lapsed policy removes a -300 policy, so a lapse is worth +300 relative to staying at the old price.
- *How would you check the model?* Compare predicted and actual claims by decile on a hold-out period, and check calibration for the risky band.
- *Alternatives to a big price rise?* Raise the premium in steps, add deductibles, or offer a safer-driving discount.

**Common mistakes:**
- Forgetting that expenses of 200 still apply to staying policies.
- Treating the average claims of the group as the claims of those who stay.
- Ignoring the 90,000 profitable policies.
- Using the repriced premium for lapsed policies.
