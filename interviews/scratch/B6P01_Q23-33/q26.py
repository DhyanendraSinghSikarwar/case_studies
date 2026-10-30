# Q26 channel mix and blended D7 retention (illustrative numbers)
last = {"organic+referral": (0.60, 0.300), "paid social": (0.40, 0.120)}   # (share of signups, D7 retention)
this = {"organic+referral": (0.40, 0.305), "paid social": (0.60, 0.125)}

def blend(d):
    return sum(s * r for s, r in d.values())

b_last, b_this = blend(last), blend(this)
print("blended last:", round(b_last, 4), " blended this:", round(b_this, 4), " change pts:", round((b_this - b_last) * 100, 2))
# standardise: this month's channel rates at last month's mix
std = sum(last[k][0] * this[k][1] for k in last)
print("this month at last month's mix:", round(std, 4), " change pts:", round((std - b_last) * 100, 2))
mix_effect = b_this - std
rate_effect = std - b_last
print("mix effect pts:", round(mix_effect * 100, 2), " rate effect pts:", round(rate_effect * 100, 2))
assert round(b_last, 3) == 0.228 and round(b_this, 3) == 0.197
assert round(std, 3) == 0.233
assert abs(mix_effect + rate_effect - (b_this - b_last)) < 1e-12
assert round(mix_effect * 100, 2) == -3.6 and round(rate_effect * 100, 2) == 0.5
assert all(this[k][1] > last[k][1] for k in last)   # every channel improved
# cost lens: retained users per Rs 100k spend (paid CAC Rs 250 per signup, organic costs 0) -> only paid is bought
paid_cac = 250
paid_signups = 100_000 / paid_cac
retained_per_100k = paid_signups * this["paid social"][1]
print("paid signups per Rs 100k:", paid_signups, " D7-retained:", retained_per_100k, " Rs per D7-retained:", 100_000 / retained_per_100k)
assert paid_signups == 400 and retained_per_100k == 50 and 100_000 / retained_per_100k == 2000
