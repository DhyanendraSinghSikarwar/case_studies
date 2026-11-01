**Follow-ups:**
- How many tail queries do you need? For a slice mean with per-query sd of 0.3, the standard error is 0.3 / sqrt(n); with 2,000 queries it is about 0.0067, so a 0.04 change is visible, but a 0.01 change is not. Pool several weeks for smaller changes.
- Should you optimise the tail at the expense of the head? Not blindly: set a protected-slice rule, such as no head regression beyond a small margin, and weigh by business value.
- Is the tail always low value? No; in some products rare queries carry high intent, so check conversion by bucket.

**Common mistakes:**
- Trusting a single overall metric.
- Reading small-slice point estimates without intervals.
- Defining the slices after looking at the results.
- Fixing ranking when the item was never retrieved.
- Letting popularity features bury new or rare items.
