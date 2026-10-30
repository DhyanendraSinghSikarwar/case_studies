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
