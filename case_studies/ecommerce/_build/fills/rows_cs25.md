| D-25-01 | 25 | Synthetic COD orders with hidden risk and profiles | Needed to test selection bias and re-identification |
| D-25-02 | 25 | Train on the randomised holdout | Legacy RTO 27.1% vs 31.7%; FPR 4.65% vs 2.78% at a 3% cap |
| D-25-03 | 25 | Match threshold 0.6 for social features | 98.1% match precision, 86% of found profiles kept |
| D-25-04 | 25 | Gradient boosting with a 3% false-positive cap | AUC 0.8066, recall 25.9%, precision 81.6%; social adds +0.014 AUC |
| D-25-05 | 25 | Audit fairness before using social features | FPR 1.4% to 4.2% by type, p = 0.042, no pairwise gap after Holm |
| D-25-06 | 25 | Capped threshold before the cost rule | Cost rule flags 62.8% of orders; calibration slope 1.106 |
| D-25-07 | 25 | About ₹24.7 crore a year (capped, base) | Worst ₹12.2 crore, best ₹37.3 crore at 1 lakh COD orders a day |
| D-25-08 | 25 | A/B test of the nudge | 764 orders for a 35% effect; 2,193 for 20% |
