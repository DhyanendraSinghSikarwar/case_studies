import random, math
random.seed(11)
n = 300
# invented per-answer score changes that match the prompt: 210 unchanged, 90 changed
# (a) all 90 moved down: 60 by -1, 30 by -2
d = [0]*210 + [-1]*60 + [-2]*30
assert len(d) == n and sum(d) == -120
print("mean change =", sum(d)/n)
assert abs(sum(d)/n - (-0.4)) < 1e-12
changed = sum(1 for x in d if x != 0)
print("answers changed:", changed, f"({changed/n:.0%})")
assert changed == 90 and changed/n == 0.30
# minimum number of changed answers needed for a -0.4 mean if scores are integers 1..5: each answer can fall at most 4
print("min answers with a change, if each fell by at most 4:", math.ceil(120/4))
# if all 90 moved down by exactly 1, mean change would be:
print("mean change if the 90 moved down by 1 only:", -90/n)
assert -90/n == -0.3
# so a mean drop of 0.4 needs bigger moves or more than 90 answers (given integer scores)
m = sum(d)/n; sd = (sum((x-m)**2 for x in d)/(n-1))**0.5
se = sd/math.sqrt(n)
print(f"sd of paired change {sd:.3f}, 95% CI of mean shift {m-1.96*se:.3f} to {m+1.96*se:.3f}")
assert m + 1.96*se < 0
# test-retest of the OLD judge on the same 300 answers: invented, 25 answers differ by one point, balanced
d0 = [0]*275 + [1]*12 + [-1]*13
print("old judge rerun mean change:", sum(d0)/n)
assert abs(sum(d0)/n) < 0.01
# bridge: this week's product scored with the NEW judge
new_week = 3.9
offset = 3.8 - 4.2
bridged = new_week - offset
print(f"new-judge score {new_week}; on old-judge scale {bridged:.1f}; product change vs 4.2 = {bridged-4.2:+.1f}")
assert abs(bridged - 4.3) < 1e-9
print(f"naive reading: {new_week-4.2:+.1f} (looks like a drop, but it is a gain after bridging)")
