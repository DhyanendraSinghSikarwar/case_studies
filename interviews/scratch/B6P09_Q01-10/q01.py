# Q1 fintech fraud: illustrative numbers from the prompt
N, fraud, blocked, tp = 1_000_000, 1000, 2000, 600
fp = blocked - tp            # genuine customers blocked
fn = fraud - tp              # fraud missed
precision, recall = tp / blocked, tp / fraud
friction = fp * 20           # support + goodwill
missed = fn * 500
saved = tp * 500
net_vs_no_model = saved - friction
fpr = fp / (N - fraud)
be_precision = 20 / (500 + 20)   # block is worth it if p*500 > (1-p)*20
ev_per_block = precision * 500 - (1 - precision) * 20
lift = precision / (fraud / N)
print(f"precision {precision:.0%}, recall {recall:.0%}, FPR {fpr:.4%}, lift over base rate {lift:.0f}x")
print(f"friction {friction:,}, missed fraud {missed:,}, fraud saved {saved:,}, net vs no model {net_vs_no_model:,}")
print(f"break-even precision {be_precision:.2%}, expected value per block {ev_per_block:.0f}")
print(f"no model loses {fraud*500:,}; with model loses {missed + friction:,}")
# day-to-day noise on the 1,000 fraud/day base rate (Poisson sd) so one day's recall is not over-read
print(f"Poisson sd of daily fraud count about {1000**0.5:.0f}")
assert (fp, fn) == (1400, 400)
assert precision == 0.30 and recall == 0.60
assert friction == 28_000 and missed == 200_000 and saved == 300_000 and net_vs_no_model == 272_000
assert round(fpr * 100, 2) == 0.14 and round(lift) == 300
assert round(be_precision * 100, 2) == 3.85 and round(ev_per_block) == 136
assert fraud * 500 == 500_000 and missed + friction == 228_000
acc = (N - fp - fn) / N
print(f"accuracy {acc:.2%} versus never-block accuracy {1 - fraud / N:.2%}")
assert round(acc * 100, 2) == 99.82 and round((1 - fraud / N) * 100, 2) == 99.90
