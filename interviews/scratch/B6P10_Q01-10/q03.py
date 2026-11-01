# Q3 churn: illustrative numbers from the prompt
subs, churn_rate = 400_000, 0.04
cost, value, budget = 150, 1_200, 3_000_000
churners = subs * churn_rate
contacts = budget // cost
be_share = cost / value                     # share of CONTACTED who must be saved by the offer
be_saved = contacts * be_share
print(f"churners/month {churners:,.0f}; contacts the budget allows {contacts:,}")
print(f"break-even save share of contacted {be_share:.1%} = {be_saved:,.0f} subscribers saved")
print(f"as share of all monthly churners: {be_saved/churners:.1%}")
# illustrative targeting: model puts 8,000 churners in the 20,000 contacted (precision 40%, recall 50%)
churn_in = 8_000
prec, rec = churn_in / contacts, churn_in / churners
need_rate = be_saved / churn_in   # offer must save this share of the churners it reaches
print(f"precision {prec:.0%}, recall {rec:.0%}; offer must save {need_rate:.2%} of reached churners")
def net(save_rate): return churn_in * save_rate * value - contacts * cost
for sr in (0.30, 0.3125, 0.35):
    print(f"save rate {sr:.2%}: saved {churn_in*sr:,.0f}, net {net(sr):,.0f}")
# contacting everyone who will churn at random (no model) versus the model
rand_churn_in = contacts * churn_rate
print(f"random 20,000 would hold {rand_churn_in:,.0f} churners; break-even save rate {be_saved/rand_churn_in:.0%} (impossible)")
assert churners == 16_000 and contacts == 20_000
assert be_share == 0.125 and be_saved == 2_500 and round(be_saved / churners, 4) == 0.1562
assert prec == 0.40 and rec == 0.50 and need_rate == 0.3125
assert net(0.30) == -120_000 and net(0.3125) == 0 and net(0.35) == 360_000
assert rand_churn_in == 800 and be_saved / rand_churn_in > 1
