# Q25 festival-week DAU: compare with the same festival in past years (illustrative numbers)
import statistics as st
# ratio = DAU in festival week / DAU baseline (average of the same weekday over the 4 prior weeks)
past = {"year-1": 0.950, "year-2": 0.940, "year-3": 0.955}
this_year = round(9.4 / 10.0, 4)
vals = list(past.values())
mean, sd = st.mean(vals), st.stdev(vals)
print("past ratios:", vals)
print("mean:", round(mean, 4), "sd:", round(sd, 4))
print("this year ratio:", this_year, " drop:", round(1 - this_year, 3))
excess = this_year - mean
z = excess / sd
print("excess vs seasonal mean (pts):", round(excess * 100, 2), " z:", round(z, 2))
inside_range = min(vals) <= this_year <= max(vals)
print("inside past range:", inside_range)
# calendar-week comparison (wrong): same ISO week last year, festival fell in another week
print("a plain week-over-week view calls it a drop of", round((1 - this_year) * 100, 1), "pts")
assert round(mean, 4) == 0.9483 and round(sd, 4) == 0.0076
assert round(excess * 100, 2) == -0.83 and round(z, 2) == -1.09
assert inside_range
