**Say this first (1 line):** On this sample the classifier has precision 36% and recall 90%, and the fake share is about 12% (9.2% to 14.8%), so I would not take down flagged reviews automatically: two in three flagged reviews are genuine; I would use the flags to prioritise human review and graded actions.

**Clarifying questions:**
- Was the 500 a simple random sample, and were the auditors blind to the classifier flags? Otherwise the audit labels are biased toward the model.
- What is the audit's own reliability (two auditors, agreement)? 60 fake labels are only as good as the labelling.
- What is the action on a flag: removal, hiding, a badge, a lower rank? Cost of a wrong action differs for each.
- Which threshold gave 150 flags, and can it be moved? A higher threshold trades recall for precision.
- Is the 12% the same in all categories and for new versus old products? One sample may hide big differences.

**Approach:**
1. Compute from the sample. Precision = 54 / 150 = 36%. Recall = 54 / 60 = 90%. The classifier flags 150 / 500 = 30% of reviews while only 12% are fake.
2. Interval for the fake share. p = 60 / 500 = 0.12, standard error = sqrt(0.12 x 0.88 / 500) = 0.0145, so 0.12 +/- 1.96 x 0.0145 gives 9.2% to 14.8%. The normal approximation is fine here because both 60 and 440 are well above 10.
3. Add intervals for precision and recall. With only 150 flagged and 60 fake, precision is 29% to 44% and recall 80% to 95% (Wilson intervals in the run). The recall interval is wide because only 60 fakes were in the sample.
4. Spell out what a blanket takedown does. Scaled to an illustrative 1,000,000 reviews: 300,000 flagged, of which 192,000 would be genuine, and about 12,000 fake reviews would still be missed. That is a lot of wrongly removed customers' content.
5. Use the flags in tiers. Rank by score; send the top slice (higher precision) to human reviewers, with extra signals (account age, device, burst patterns, text similarity); auto-act only above a threshold where audited precision is high; for the middle, use reversible actions (lower weight in the rating, no removal) and an appeal path.
6. Keep auditing. Draw a fresh random sample each month for the base rate, and a stratified sample by score band to measure precision per band, so thresholds can be set from data.

**Metrics:**
- Precision = flagged and fake / flagged = 54 / 150 = 36%.
- Recall = flagged and fake / fake = 54 / 60 = 90%.
- Fake share = fake / sampled reviews = 12% with a 95% interval of 9.2% to 14.8%.
- Guardrails: wrongly removed genuine reviews (appeals upheld), reviewer agreement, time to action, and effect on seller ratings.

**Risks:**
- The audit sample is small for recall (60 positives).
- Fraudsters adapt; a stable precision today may fall.
- Auditors who see the model flag may anchor on it.
- Removing genuine reviews harms honest sellers and shoppers.
- Any rule on how reviews may be removed or disclosed is for the trust and legal teams to specify.

**What the interviewer scores:**
- Strong: gets 36%, 90% and 9.2% to 14.8%, and notes how the interval is built.
- Strong: sees that precision, not recall, makes automatic takedown unsafe, and quantifies it.
- Strong: proposes tiers, human review, appeals and ongoing random audits.
- Weak: "recall is 90% so it is great", or removing everything flagged.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Ninety per cent recall is excellent, so I would remove all flagged reviews."
- Strong: "Of 150 flagged, 54 are fake, so precision is 36%. At a million reviews that would remove about 192,000 genuine ones. Fake share is 12%, with a 95% interval of 9.2% to 14.8%. I would send the highest-scoring flags to human review with extra signals, only auto-act where audited precision is high, and keep a monthly random audit so the threshold rests on measured numbers."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How big an audit sample do you need? For a 95% interval of +/- 1 point at 12%, about 4,060 reviews (1.96^2 x 0.12 x 0.88 / 0.01^2), more for per-category estimates.
- How would you raise precision? Raise the threshold, add features, or require agreement from a second model; recall will fall, so measure both.
- Why a Wilson interval for precision? It behaves better than the simple normal one when the proportion is far from 0.5 or the sample is small.

**Common mistakes:**
- Reading recall alone.
- Assuming the 12% is exact.
- Taking down flagged reviews with no review or appeal.
- Using flagged-only data to estimate the fake share.
