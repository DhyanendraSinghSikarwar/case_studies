**Follow-ups:**
- Why would the inputs look the same but churn behave differently? Because the price change altered how customers respond to usage, not how much they use.
- How much post-change data is enough? Enough to estimate the changed relationship with a small standard error; in the toy, 3,000 rows were enough, but in real data with many features it takes more. Check by learning curves.
- When would you prefer separate models by regime? When the relationship differs a lot and each regime has enough data; otherwise a shared model with regime interactions borrows strength.

**Common mistakes:**
- Calling it data drift because the PSI is small, or ignoring it because the PSI is small.
- Validating on a random split that mixes regimes.
- Retraining on a window that mostly predates the change.
- Not adding the price or plan feature.
- Waiting for a large sample when a small fresh sample already shows the change.
