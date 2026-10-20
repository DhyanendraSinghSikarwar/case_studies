| D-17-01 | 17 | Synthetic impressions with hidden click model and exploration bucket | Ads are 85% of impressions in slots 2 and 5, so exploration is needed |
| D-17-02 | 17 | One model with isAds flag and crosses, scored at slot 1 | Ad AUC 0.7215 vs 0.7153; ad log loss Holm p = 0.04 |
| D-17-03 | 17 | Calibrate per population, check the slope | Ad slope 0.78 without crosses, 0.996 with |
| D-17-04 | 17 | Unified ranking replaces pinned slots | +14.2% organic orders, +5.7% ad revenue at lambda = 1 |
| D-17-05 | 17 | Bid weight by "organic orders must not fall"; lambda = 3 as upper arm | +1.5% organic, +44.1% revenue; sponsored share 39.6% |
| D-17-06 | 17 | Safe default for failed scores; redesign breaker | Default 0.5 at 10% failed: -7.0% organic; breaker reverted 42% normally |
| D-17-07 | 17 | ₹ case: assumptions and scenarios | ₹128.5 crore a year base (₹40.8 to ₹224.7 crore) |
| D-17-08 | 17 | A/B design: size by metric, at least a week | 2,517 requests per arm for revenue, 2.81 million for organic orders |
