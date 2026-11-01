# Q10: build vs buy (thousands of one unit, illustrative)
build_up, build_yr, vendor_yr = 900, 150, 400
b3 = build_up + 3 * build_yr
v3 = 3 * vendor_yr
be = build_up / (vendor_yr - build_yr)          # years where cumulative costs meet
print("3-year build", b3, "vendor", v3, "vendor cheaper by", b3 - v3)
print("break-even years", be)
assert (b3, v3, be) == (1350, 1200, 3.6)

# sensitivity 1: maintenance really 250 a year (the 'hidden cost' finance fears)
be_hi = build_up / (vendor_yr - 250)
print("break-even if maintenance 250:", be_hi)
assert be_hi == 6.0
# sensitivity 2: vendor raises price 10% a year (the 'hidden cost' engineering fears)
def cum_vendor(y, esc=0.10):
    return sum(vendor_yr * (1 + esc) ** k for k in range(y))
def cum_build(y):
    return build_up + build_yr * y
for y in range(1, 6):
    print("year", y, "build", cum_build(y), "vendor+10%/yr", round(cum_vendor(y), 1))
assert round(cum_vendor(3), 1) == 1324.0 and cum_vendor(3) < cum_build(3)
assert cum_vendor(4) > cum_build(4)             # flips in year 4
# sensitivity 3: discount at 10%, upfront at t0, annual costs at year end
r = 0.10
ann = sum(1 / (1 + r) ** t for t in (1, 2, 3))
pv_b = build_up + build_yr * ann
pv_v = vendor_yr * ann
print("PV build", round(pv_b, 1), "PV vendor", round(pv_v, 1))
assert round(pv_b, 1) == 1273.0 and round(pv_v, 1) == 994.7
