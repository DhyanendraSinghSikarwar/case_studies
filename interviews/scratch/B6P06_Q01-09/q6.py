visitors = 400_000
li = visitors * 0.40
lo = visitors - li
conv_all = visitors * 0.02
conv_li = li * 0.035
conv_lo = conv_all - conv_li
print(f"logged-in {li:,.0f} -> {conv_li:,.0f}; logged-out {lo:,.0f} -> {conv_lo:,.0f} = {conv_lo/lo:.2%}")
assert (li, lo, round(conv_all), round(conv_li), round(conv_lo)) == (160000, 240000, 8000, 5600, 2400)
assert abs(conv_lo/lo - 0.01) < 1e-12
# weighted average check
assert abs(0.4*0.035 + 0.6*0.01 - 0.02) < 1e-12
# headline comparison needs the same segment in the old flow
print(f"logged-in rate is {0.035/0.01:.1f}x the logged-out rate")
assert round(0.035/0.01, 1) == 3.5
