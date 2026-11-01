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
