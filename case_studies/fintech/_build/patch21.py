p = "_build/src/cs21.src"; s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert a in s, a[:70]; s = s.replace(a, b)
rep('''per_user_day = clk_raw.groupby(["user_id", "day"]).clicks.sum()
daily = clk_raw.groupby("day").clicks.sum(); robust_z = (daily - daily.rolling(7, center=True, min_periods=3).median()) / daily.median()''',
'''per_user_day = clk_raw.groupby(["user_id", "day"]).clicks.sum()
bots = per_user_day.groupby(level=0).max(); bots = bots[bots > 100].index.tolist()
daily = clk_raw[~clk_raw.user_id.isin(bots)].drop_duplicates(["user_id", "day", "category"]).groupby("day").clicks.sum()      # check gaps AFTER removing bots and duplicates''')
rep('''bots = per_user_day.groupby(level=0).max(); bots = bots[bots > 100].index.tolist(); gap_days = daily''', '''gap_days = daily''')
rep('''print(f"Bot users removed: {bots} | logging-gap days: {gap_days} (kept for history, excluded from evaluation)")''',
    '''print(f"Bot users removed: {bots} | logging-gap days (0-based): {gap_days} (kept for history, excluded from evaluation)")''')
rep('''We also look at a **too-short trend window** (w = 1), which over-reacts.''', '''We also compare a **slow trend window** (w = 14 days), which reacts late to spikes.''')
rep('''for d in TEST: d1.append(evaluate(d, scores(d, A_BEST, 1, "3 Bayesian trend filter"))[1].mean())
daily["Bayesian, w = 1 day"] = d1;''', '''for d in TEST: d1.append(evaluate(d, scores(d, A_BEST, 14, "3 Bayesian trend filter"))[1].mean())
daily["Bayesian, w = 14 days"] = d1; daily["w=best − w=14 (pp)"] = (daily["3 Bayesian trend filter"] - daily["Bayesian, w = 14 days"]) * 100;''')
rep('''daily = pd.DataFrame({m: R[m].groupby("day").hit.mean() for m in METHODS}); daily.index = daily.index + 1''',
    '''daily = pd.DataFrame({m: R[m].groupby("day").hit.mean() for m in METHODS}); daily.index = daily.index + 1                    # 1-based day numbers''')
rep('''money = money.drop(index=["3 Bayesian trend filter"]); money.index = ["Bayes vs " + i for i in money.index]''',
    '''head = -money.loc["oracle (true probabilities)"]; money = money.drop(index=["3 Bayesian trend filter", "oracle (true probabilities)"]); money.index = ["Bayes vs " + i for i in money.index]
print(f"Headroom: a perfect (oracle) ranking would add {head.iloc[0]:.2f} lakh tile clicks/day ≈ ₹{head.iloc[1]:.1f} crore/year more than the Bayesian filter")''')
open(p, "w", encoding="utf-8").write(s); print("patched")
