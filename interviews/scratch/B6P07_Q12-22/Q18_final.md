### Q18 ⭐⭐⭐ 🔴 Over three releases the offline pass rate on a 1,000-question set rose from 82% to 86% (4 points absolute), but the online resolution rate stayed at 61% then 61.5% across 20,000 conversations a month. List the reasons the two can diverge, say which check you do first, and how you would build an online metric you trust.
**Asked at:** LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The offline +4 points and the online +0.5 points disagree even after noise (the online interval tops out near +1.5), so I would first check whether the offline set matches live traffic, then build an online metric from outcomes I trust.

**Clarifying questions:**
- How was the 1,000-question set built, and was it used to tune the releases? Why it matters: tuning on it inflates the offline score.
- What does "resolution" mean online, and who decides? Why it matters: it must reflect the user's problem being solved.
- What was the online metric before and after the three releases (the prompt shows "61% then 61.5%")? Why it matters: the comparison window sets the noise.
- Does the question mix match live intents? Why it matters: a different mix dilutes or hides gains.
- Are conversations grouped by user? Why it matters: repeat users make the online interval wider.

**Approach:**
1. Noise first. Online: +0.5 points, SE 0.49, 95% interval about -0.45 to +1.45 (assuming independent conversations). Offline: +4 points, SE 1.64 unpaired, interval about 0.8 to 7.2 (a paired test is tighter).
2. The offline +4 sits above the online upper limit of +1.45, so noise alone does not explain it. With clustered users the online interval widens (about +1.85 with a design effect of 2), so it is not certain either.
3. First check: traffic mix. Re-weight the offline results by the real intent distribution. Example: 50% hard items in the set with +8 gain on hard items gives +4 offline, but with 10% hard traffic the online gain is +0.8.
4. Then check: overfitting to the set across three releases, contamination (the set leaked into prompts or training data), judge or grader mismatch with real users, and different input styles (live typos, long chats).
5. Check the online definition: a resolution metric can be moved by user behaviour, channel changes, seasonality, and escalation rules, not only answer quality.
6. Build the online metric: resolution = conversations in scope with no re-contact in 7 days and no human escalation / all in-scope conversations. Validate it against human review on a sample of 300 conversations.
7. Add a randomised holdout or A/B for each release and report the interval. Use a calibrated LLM judge only after agreement with humans is measured (Cohen's kappa) and re-checked regularly.
8. Refresh the offline set every quarter with fresh sampled traffic and keep a locked set that is never used for tuning.

**Metrics:**
- Offline pass rate = questions passed / 1,000, per intent slice and re-weighted by traffic share.
- Online resolution rate = resolved in-scope conversations / in-scope conversations, with a user-clustered interval.
- Gap = offline gain minus online gain, with an interval.
- Judge-human agreement (kappa) and audit sample size.
- Guardrails: escalation rate, complaint rate, cost per resolution.

**Risks:**
- Chasing the offline score (Goodhart's law: a metric that becomes a target stops measuring what you wanted).
- A resolution metric that counts abandoned chats as resolved.
- Concluding the releases are useless when the online test was underpowered.
- Judge drift between releases.

**What the interviewer scores:**
- Strong: quantifies noise on both sides, reweights by traffic, names a first check, defines the online metric exactly.
- Strong: notes clustering and holdouts.
- Weak: "online is noisy, trust offline" or the reverse.
- Weak: a list of reasons with no first step.

**Example:** Illustrative. Weak: "Offline is up 4 points, so the model is better, the online number is noise." Strong: "Online noise alone allows up to about +1.5, so +4 is a real gap. I would reweight offline by live intent mix, because if hard questions are 10% of traffic an 8-point gain on them is only 0.8 overall. Then I would run a holdout on the next release."

**Code:**
```python
import math
def two_prop(p1, n1, p2, n2):
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    return d, se, d / se, d - 1.96 * se, d + 1.96 * se
d, se, z, lo, hi = two_prop(0.61, 20_000, 0.615, 20_000)
print(f"online: +{d*100:.1f} pts, SE {se*100:.2f}, z {z:.2f}, 95% CI {lo*100:.2f} to {hi*100:.2f} pts (assumes independent conversations)")
assert round(se * 100, 2) == 0.49 and round(z, 2) == 1.03 and (round(lo * 100, 2), round(hi * 100, 2)) == (-0.45, 1.45)
d2, se2, z2, lo2, hi2 = two_prop(0.82, 1000, 0.86, 1000)
print(f"offline (unpaired view): +{d2*100:.0f} pts, SE {se2*100:.2f}, z {z2:.2f}, 95% CI {lo2*100:.1f} to {hi2*100:.1f} pts")
assert round(z2, 2) == 2.44 and (round(lo2 * 100, 1), round(hi2 * 100, 1)) == (0.8, 7.2)
print(f"offline +4 sits above the online upper limit +{hi*100:.2f}: {0.04 > hi}")
assert 0.04 > hi
# Mix effect: offline set 50% hard / 50% easy, gain only on hard items (+8). Online traffic is 10% hard.
gain_hard = 8.0
off = 0.5 * gain_hard; on = 0.1 * gain_hard
print(f"mix effect: offline gain {off:.1f} pts, online gain {on:.1f} pts")
assert off == 4.0 and abs(on - 0.8) < 1e-9
# Clustering: conversations come from users; a design effect of 2 inflates the online SE by sqrt(2).
deff = 2.0
print(f"with design effect {deff:.0f}: online SE {se*math.sqrt(deff)*100:.2f} pts, CI upper {(d+1.96*se*math.sqrt(deff))*100:.2f}")
assert round(se * math.sqrt(deff) * 100, 2) == 0.69
# Online sample size to see +1 point at 60% (80% power, 5% two-sided).
n_arm = 2 * 0.6 * 0.4 * (1.96 + 0.84) ** 2 / 0.01 ** 2
print(f"conversations per arm to detect +1 point at 60%: {n_arm:,.0f}")
assert round(n_arm) == 37_632
```

**Output (my run):**
```
online: +0.5 pts, SE 0.49, z 1.03, 95% CI -0.45 to 1.45 pts (assumes independent conversations)
offline (unpaired view): +4 pts, SE 1.64, z 2.44, 95% CI 0.8 to 7.2 pts
offline +4 sits above the online upper limit +1.45: True
mix effect: offline gain 4.0 pts, online gain 0.8 pts
with design effect 2: online SE 0.69 pts, CI upper 1.85
conversations per arm to detect +1 point at 60%: 37,632
```

**Follow-ups:**
- Which do you trust more? Neither alone. Online measures what users experience; offline is fast and controlled. They must reconcile.
- How big an online test? About 37,600 per arm to see +1 point at 60% (80% power), and more if users repeat.
- Can an LLM judge be the online metric? Only after checking agreement with human labels and watching it for drift.

**Common mistakes:**
- Comparing offline and online without intervals.
- A test set that has been tuned against.
- Treating conversations as independent when users repeat.
- Changing the online metric definition between releases.

