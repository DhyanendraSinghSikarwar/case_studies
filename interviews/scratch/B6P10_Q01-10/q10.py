import math
# Q10 credit scoring: illustrative numbers from the prompt
per_month, months, unlabelled_months, dr = 3_000, 12, 4, 0.07
total = per_month * months
labelled = per_month * (months - unlabelled_months)
unl = per_month * unlabelled_months
defaulters = labelled * dr
se = math.sqrt(dr * (1 - dr) / labelled)
print(f"total {total:,}; labelled {labelled:,}; unlabelled {unl:,}; defaulters {defaulters:,.0f}")
print(f"default rate {dr:.0%} +/- {1.96*se*100:.2f} pts (95%) -> defaulters {labelled*(dr-1.96*se):,.0f} to {labelled*(dr+1.96*se):,.0f}")
# out-of-time split: oldest 5 matured months train, newest 3 matured months validate
train, valid = per_month * 5, per_month * 3
print(f"train {train:,} (~{train*dr:,.0f} defaulters), validate {valid:,} (~{valid*dr:,.0f})")
# an expected-value cut-off: loss given default vs margin on a good loan (illustrative)
lgd, margin = 10_000, 800
be_pd = margin / (margin + lgd)
print(f"approve if PD below {be_pd:.2%} (illustrative loss 10,000, margin 800)")
weeks = {"label definition+data audit": 2, "baseline+features": 2, "model+validation": 3, "governance+pilot setup": 3}
print(weeks, sum(weeks.values()))
print(f"first outcomes on new loans arrive {4} months (~17 weeks) after launch, beyond the 10-week plan")
assert total == 36_000 and labelled == 24_000 and unl == 12_000 and round(defaulters) == 1_680
assert round(1.96 * se * 100, 2) == 0.32
assert train == 15_000 and valid == 9_000 and round(valid * dr) == 630
assert round(be_pd, 4) == 0.0741 and sum(weeks.values()) == 10
