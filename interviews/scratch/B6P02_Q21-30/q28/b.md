**Follow-ups:**
- How does this affect training? Recent rows have incomplete labels and look negative; train only on matured rows or use a survival or delayed-feedback model.
- What if the delay curve changes? Re-estimate it on a rolling window of matured cohorts and alert when it moves.
- Could you alert faster? Yes, with the maturity-adjusted ratio and a wider band, but label it an early read and confirm with the matured cohort.

**Common mistakes:**
- Evaluating calibration on cohorts younger than the window.
- Forgetting to log cohort age with the metric.
- Using one alert threshold for cohorts of different maturity.
- Training on immature rows labelled as negatives.
- Declaring recalibration needed before the cohort has matured.
