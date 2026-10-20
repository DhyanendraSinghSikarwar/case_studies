# Regression Metrics — A Complete Course

*From "what is a residual" to "why RMSLE for house prices and MASE for forecasts."*

**Companion document to** *Classification Metrics — A Complete Course*. Same structure, same depth, same 12-section treatment per metric.

**How to use this document**
- Read Parts 0–1 first. Everything else builds on the residual.
- One 10-house example runs through the whole document, so every metric is computed on identical data and directly comparable.
- Every formula symbol is spelled out.
- Python snippets assume `import numpy as np` and `from sklearn.metrics import *`.
- All numeric values verified against scikit-learn and scipy.

---

## Table of Contents

| Part | Topic |
|---|---|
| 0 | Regression evaluation basics |
| 1 | The residual — read this before any metric |
| 2 | Absolute error family: MAE, MedAE, Max Error, MAD |
| 3 | Squared error family: SSE/RSS, MSE, RMSE |
| 4 | Percentage & relative error: MAPE, sMAPE, WAPE, MedAPE, MPE, RAE, RSE, MASE, Theil's U |
| 5 | Log-based error: MSLE, RMSLE, log accuracy ratio, MdSA |
| 6 | Goodness of fit: R², Adjusted R², Explained Variance, Pearson r, Spearman ρ, CCC |
| 7 | Robust & asymmetric losses: Huber, Log-Cosh, Quantile/Pinball, ε-insensitive, Tukey |
| 8 | Probabilistic regression: Gaussian NLL, CRPS, PICP, MPIW, Interval Score, Winkler |
| 9 | Model selection: AIC, AICc, BIC, Mallows' Cp, PRESS, CV error |
| 10 | Time-series specific metrics and pitfalls |
| 11 | Residual diagnostics (the part everyone skips) |
| 12 | Multi-output and multi-target regression |
| 13 | Master comparison tables |
| 14 | "Which metric should I use?" decision tree |
| 15 | Industry case studies |
| 16 | 120+ interview questions with answers |
| 17 | Cheat sheet, formula sheet, mnemonics, pitfalls |
| A–D | Appendices: full worked examples and reference code |

---

# PART 0 — The Basics

## 0.1 What is regression evaluation?

Regression evaluation is **measuring how close your numeric predictions are to the truth, on data the model has never seen.**

The fundamental difference from classification: in classification a prediction is right or wrong. In regression **every prediction is wrong**, and the only question is *by how much, in which direction, and does the size of the miss matter linearly or non-linearly?*

That single sentence generates the entire zoo of regression metrics:
- "By how much" → absolute error family (MAE)
- "Do big misses matter disproportionately?" → squared error family (MSE, RMSE)
- "Is a $10 miss on a $100 item the same as on a $10,000 item?" → percentage family (MAPE, RMSLE)
- "In which direction?" → bias metrics (MPE, mean residual)
- "How much of the variation did I explain?" → goodness-of-fit family (R²)
- "How confident should I be?" → probabilistic family (NLL, CRPS, interval coverage)

## 0.2 Why do we need evaluation metrics?

| Reason | Explanation |
|---|---|
| **Compare models** | Ridge vs LightGBM vs a neural net — you need one number to rank them |
| **Tune hyperparameters** | `GridSearchCV(scoring='neg_mean_absolute_error')` needs an objective |
| **Choose the loss function** | The metric you report should usually match the loss you train on. If they disagree you are optimising for the wrong thing |
| **Communicate with the business** | "Our forecast is off by 4.2% on average" is a metric. "The model is good" is not |
| **Detect overfitting** | Train error low, test error high |
| **Set expectations & SLAs** | Contracts specify forecast accuracy; safety cases specify worst-case error |
| **Diagnose the model** | Residual patterns reveal missing features, wrong functional form, and heteroscedasticity — things no single number shows |

## 0.3 What happens if you use the wrong metric?

**Failure 1 — Demand forecasting optimised for MAPE.**
MAPE divides by the actual value, so it explodes when demand is near zero and is undefined at zero. It also **systematically penalises over-forecasting more than under-forecasting** (an over-forecast can exceed 100% error, an under-forecast is capped at 100%). A team optimising MAPE will produce forecasts biased *low*, quietly creating stockouts. The right metric was WAPE or MASE.

**Failure 2 — House price model optimised for RMSE.**
RMSE is dominated by the most expensive houses. A model that fits $5M mansions well and is 40% wrong on $150k starter homes can beat a model that is 8% wrong everywhere. If your business is starter homes, you have selected the worse model. The right metric was RMSLE or MAPE.

**Failure 3 — Delivery-time model optimised for MAE.**
MAE is minimised by predicting the **conditional median**. If you promise customers the median delivery time, you are late 50% of the time. The right target was a high quantile — the 90th percentile, obtained with pinball loss.

**Failure 4 — Insurance reserving model reported with R² = 0.85.**
R² says the model explains 85% of the variance. It says nothing about whether the predictions are *unbiased in aggregate*, and reserving requires the total to be right. A model can have great R² and be systematically 12% low. The right metrics were the mean residual (bias) and total-vs-predicted ratio.

**One-line rule:** the metric is a mathematical statement of what "a good prediction" means for your business. Pick it — and its loss-function counterpart — *before* you train.

## 0.4 Regression metrics vs classification metrics

| | Regression | Classification |
|---|---|---|
| **Target** | Continuous number | Discrete category |
| **Core object** | The **residual** `e = y − ŷ` | The **confusion matrix** |
| **Question** | "How far off am I?" | "Did I pick the right bucket?" |
| **Every prediction is** | Somewhat wrong | Right or wrong |
| **Error has** | Magnitude **and sign** | Type (FP or FN) |
| **Typical range** | 0 → ∞ (lower better), except R² | 0 → 1 (higher better) |
| **Central problem** | Scale, outliers, heteroscedasticity | Class imbalance, threshold choice |
| **Threshold needed?** | No | Usually yes |
| **Scale-dependence** | Severe — MAE of 5 is meaningless without units | None — metrics are unitless ratios |
| **Analogue of imbalance** | Skewed target distribution / outliers |Class imbalance |

**Two structural differences worth internalising:**

1. **Regression metrics are usually in the units of the target.** MAE = 36 means "36 thousand dollars" or "36 units" — you must state the units, and you cannot compare across datasets. Classification metrics are dimensionless ratios and travel freely. This is why regression has a whole family of *relative* metrics (MAPE, MASE, R²) that exist purely to restore comparability.

2. **Regression errors have a sign, so bias is a first-class concern.** A classifier cannot be "systematically 12% too positive"; a regressor can. Metrics like MAE and RMSE take absolute values and are therefore **completely blind to systematic bias**. You must report a signed metric alongside them. This is the single most commonly skipped step in regression evaluation.

**The overlap:** metrics like Log Loss and Brier Score are classification metrics that behave like regression metrics because they measure numeric distance from a 0/1 target. Conversely, Gaussian NLL and CRPS are regression metrics that behave like proper scoring rules. The families meet in probabilistic prediction.

## 0.5 The three properties every regression metric has

Before learning any specific metric, learn these three axes. Every metric in this document is a point in this space.

**1. Scale dependence — is the metric in the target's units, or unitless?**

| Type | Metrics | Consequence |
|---|---|---|
| **Scale-dependent** (target units) | MAE, MSE, RMSE, MedAE, Max Error, SSE | Interpretable in context, **not comparable across datasets or across series with different magnitudes** |
| **Percentage** (unitless) | MAPE, sMAPE, WAPE, MedAPE, MPE | Comparable, but break near zero and are asymmetric |
| **Scaled / relative** (unitless) | R², MASE, RAE, RSE, Theil's U | Comparable and well-behaved near zero, but need a baseline |
| **Log-based** (unitless-ish) | MSLE, RMSLE | Approximately relative; requires non-negative targets |

**2. Outlier sensitivity — how much does one huge error dominate?**

```
Least sensitive  <------------------------------------->  Most sensitive
MedAE  <  MAE  <  Huber  <  Log-Cosh  <  RMSE  <  MSE  <  Max Error
```
This ordering follows directly from the power the error is raised to: median (rank-based) < |e|¹ < mixed < e² < max.

**3. Symmetry — does the metric treat over- and under-prediction equally?**

| Symmetric | Asymmetric by design | Accidentally asymmetric |
|---|---|---|
| MAE, MSE, RMSE, MedAE, R², Huber | Quantile/Pinball loss, custom cost-weighted loss | **MAPE**, **sMAPE**, **RMSLE** |

That third column is a trap. MAPE, sMAPE and RMSLE all penalise one direction more than the other **without anyone intending it**, and this silently biases models trained or tuned on them. Details in Parts 4 and 5.

## 0.6 The one thing to remember before Part 1

> **A single regression metric is never enough.** At minimum report:
> **(1) a magnitude metric** (MAE or RMSE), **(2) a signed bias metric** (mean residual or MPE), **(3) a relative metric** (MAPE, MASE, or R²), and **(4) a residual plot.**
>
> Any one of them alone can hide a fatal defect.

---

# PART 1 — The Residual

Everything in regression is built from one object. Learn it and the rest is arithmetic.

## 1.1 Definition and sign convention

```
Residual:  eᵢ = yᵢ − ŷᵢ
```
- **yᵢ** = the actual (true, observed) value for sample i
- **ŷᵢ** ("y-hat") = the model's predicted value for sample i
- **eᵢ** = the residual, in the same units as y

**The sign convention matters and is a common source of confusion:**

| Sign of e | Meaning | Also called |
|---|---|---|
| **e > 0** (y > ŷ) | The model predicted **too low** | **Under-prediction / under-forecast** |
| **e < 0** (y < ŷ) | The model predicted **too high** | **Over-prediction / over-forecast** |
| **e = 0** | Exact hit | — |

> **Warning:** some texts and some forecasting software define the error as `ŷ − y` (prediction minus actual), which flips every sign. Statistics and scikit-learn use `y − ŷ`. **Always state your convention** — an entire bias analysis can be reported backwards because of this.

**Residual vs error — a distinction that matters in interviews:**
- **Error** = `y − f(x)` where f is the *true* underlying function. Unobservable.
- **Residual** = `y − ŷ` where ŷ comes from your *fitted* model. Observable.
In ML practice the terms are used interchangeably, but in statistics the distinction is meaningful: residuals are estimates of errors, and they are not independent even when errors are (fitting the model induces dependence, which is why residual degrees of freedom is `n − p`, not `n`).

## 1.2 The three views of the residual set

Just as every classification metric is a ratio along one direction of the confusion matrix, every regression metric is a summary of the residual set along one of three directions.

```
                    THE RESIDUAL SET  {e₁, e₂, ..., eₙ}
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
   MAGNITUDE                  SIGN / BIAS              STRUCTURE
   "how big?"                 "which way?"             "is there a pattern?"
        |                         |                         |
  take |e| or e²            keep the sign            plot e vs ŷ, vs x, vs time
        |                         |                         |
  MAE, MSE, RMSE,          mean residual,           residual plots, Durbin-Watson,
  MedAE, MaxErr,           MPE, tracking signal,    Breusch-Pagan, Q-Q plot,
  MAPE, RMSLE, Huber       forecast bias            autocorrelation
        |                         |                         |
  "The model is off        "The model is            "The model is missing
   by about 36k"            systematically low"      a nonlinear term"
```

**The lesson:** magnitude metrics take absolute values or squares and therefore **destroy the sign information**. A model with residuals `{+50, +50, +50, +50}` and one with `{+50, −50, +50, −50}` have **identical MAE and identical RMSE** but the first is catastrophically biased and the second is unbiased. You cannot detect this from MAE. You need a signed metric.

## 1.3 Absolute vs relative residuals

The same residual means different things at different scales:

| Actual y | Predicted ŷ | Residual e | Relative error \|e\|/y | Reasonable? |
|---|---|---|---|---|
| $100 | $110 | −10 | 10% | Poor |
| $1,000 | $1,010 | −10 | 1% | Good |
| $100,000 | $100,010 | −10 | 0.01% | Excellent |

**Same absolute error, three completely different verdicts.** This is the entire motivation for the percentage and log families (Parts 4 and 5). Whether you should care about absolute or relative error is a business question:

| Care about **absolute** error when… | Care about **relative** error when… |
|---|---|
| The cost of a miss is proportional to the miss size in units | The cost of a miss is proportional to the item's value |
| Inventory units, kWh, minutes late, degrees Celsius | House prices, revenue, sales volumes spanning orders of magnitude |
| The target has a narrow range | The target is right-skewed and spans decades |
| Errors are homoscedastic (constant variance) | Errors are heteroscedastic (variance grows with y) |

## 1.4 THE RUNNING EXAMPLE — 10 houses, computed by hand

Used throughout the document so every metric is comparable on identical data.

**Setup.** Predicting house prices in **$1,000s** for 10 houses.

| i | Actual y | Predicted ŷ | Residual e = y − ŷ | \|e\| | e² | \|e\|/y |
|---|---|---|---|---|---|---|
| 1 | 200 | 220 | **−20** (over) | 20 | 400 | 0.1000 |
| 2 | 250 | 240 | **+10** (under) | 10 | 100 | 0.0400 |
| 3 | 300 | 310 | **−10** (over) | 10 | 100 | 0.0333 |
| 4 | 350 | 330 | **+20** (under) | 20 | 400 | 0.0571 |
| 5 | 400 | 420 | **−20** (over) | 20 | 400 | 0.0500 |
| 6 | 450 | 430 | **+20** (under) | 20 | 400 | 0.0444 |
| 7 | 500 | 520 | **−20** (over) | 20 | 400 | 0.0400 |
| 8 | 550 | 530 | **+20** (under) | 20 | 400 | 0.0364 |
| 9 | 600 | 620 | **−20** (over) | 20 | 400 | 0.0333 |
| 10 | **900** | **700** | **+200** (under) | **200** | **40,000** | **0.2222** |
| | **Σ = 4500** | Σ = 4320 | **Σ = +180** | **Σ = 360** | **Σ = 43,000** | Σ = 0.6568 |

**The essential summary statistics:**
```
n              = 10
Σ y            = 4,500          ȳ (mean actual)   = 450
Σ ŷ            = 4,320          mean predicted     = 432
Σ e            = +180           mean residual      = +18   <-- BIAS: model under-predicts
Σ |e|          = 360            MAE                = 36
Σ e²           = 43,000         MSE                = 4,300 ; RMSE = 65.57
Σ (y − ȳ)²     = 375,000        SS_tot             (variance of y × n)
median |e|     = 20             MedAE              = 20
max |e|        = 200            Max Error          = 200
```

**The story in plain English — hold this in your head, every metric below is one number summarising part of it:**

> Nine of the ten houses are predicted within $20k. The tenth — a $900k house — is under-predicted by $200k. On average the model misses by $36k, but that average is entirely distorted by the one bad case: the *typical* miss is only $20k. The model also has a systematic tendency to under-predict, by $18k on average, and almost all of that comes from the same expensive house.

Every metric in Parts 2–6 is a different way of compressing that paragraph into a single number, and each one keeps a different part of it.

**Python setup:**
```python
import numpy as np

y      = np.array([200, 250, 300, 350, 400, 450, 500, 550, 600, 900], dtype=float)
y_pred = np.array([220, 240, 310, 330, 420, 430, 520, 530, 620, 700], dtype=float)

e = y - y_pred                     # residuals (y minus y-hat)
print(e)                           # [-20  10 -10  20 -20  20 -20  20 -20 200]
print(e.sum(), e.mean())           # 180.0  18.0   <- signed: reveals the bias
print(np.abs(e).mean())            # 36.0         <- MAE
print((e**2).mean())               # 4300.0       <- MSE
```

## 1.5 The residual plot — read this before any metric

A single number can never tell you *why* the model is wrong. The residual plot can. It is the regression analogue of the confusion matrix: the diagnostic object you look at first.

**The standard plot: residuals (y-axis) against predicted values (x-axis), with a horizontal line at zero.**

```
Our example:

  +200 |                                             *  <- the $900k house
       |
  +100 |
       |
    +20|      *        *        *        *
     0 |----------------------------------------------
    -20| *        *        *        *        *
       |
  -100 |
       +----------------------------------------------
        220  240  310  330  420  430  520  530  620  700
                        PREDICTED VALUE
```

**What we learn that no metric tells us:**
1. Nine residuals sit tightly in a ±20 band with **no trend** — the model's functional form is fine in that range.
2. The residuals **alternate sign** in a regular pattern, which is an artefact of this toy example but in real data would suggest a missing periodic feature.
3. **One point is a massive outlier** at the top of the range. Whether that is a data error, a genuinely unusual property (a mansion in a normal neighbourhood), or evidence that the model breaks down for expensive houses is the single most important question about this model — and it is invisible in MAE = 36.

**The five patterns you must be able to recognise:**

```
(a) HEALTHY: random cloud, constant width, centred on zero
    |    . . .. . . . .. .. . . .
   0|--.-.-.--.-.--.-.-.--.-.-.--.--
    | . . .. . . .. . . . .. . .
    -> The model is fine. Use any sensible metric.

(b) CURVED (U or inverted-U): a systematic trend
    |  .              .
   0|----.--------.-------.-------
    |      . . .
    -> MISSING NONLINEARITY. Add polynomial terms, splines, interactions,
       or switch to a tree/GBM. No metric will fix this.

(c) FUNNEL / CONE: spread grows with the prediction
    |        .    .   .    .    .
   0|--.-.-.-.--.---.---.----.-----
    |   .      .     .     .    .
    -> HETEROSCEDASTICITY. Variance is proportional to level.
       -> Use RMSLE / MAPE / log-transform the target, or a
          gamma/tweedie/Poisson objective. RMSE will be dominated
          by the high end.

(d) SHIFTED: whole cloud sits above or below zero
    |  . . .. . . .. . .
  +5|--.-.-.--.-.--.-.-.--   <- mean residual > 0
   0|-----------------------
    -> BIAS. MAE and RMSE cannot see this. Report mean residual.
       Common causes: training on log target and back-transforming
       naively; distribution shift; a truncated target.

(e) STRIPES / STEPS
    |  ....        ....
   0|-------------------------
    |       ....        ....
    -> The target is discrete or bounded, or a categorical feature
       dominates. Consider ordinal/count models (Poisson, negative binomial).
```

**Additional diagnostic plots to always produce** (covered fully in Part 11):
- **Residuals vs each feature** — reveals which variable the missing nonlinearity belongs to
- **Residuals vs time / index** — reveals autocorrelation and drift
- **Q-Q plot of residuals** — reveals heavy tails and non-normality
- **Predicted vs actual with a 45° line** — the single best plot for a stakeholder audience
- **Histogram of residuals** — reveals skew and multimodality

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 3, figsize=(15, 4))

ax[0].scatter(y_pred, e); ax[0].axhline(0, ls='--', c='k')
ax[0].set_xlabel('Predicted'); ax[0].set_ylabel('Residual')
ax[0].set_title('Residuals vs Predicted')

ax[1].scatter(y, y_pred)
lims = [min(y.min(), y_pred.min()), max(y.max(), y_pred.max())]
ax[1].plot(lims, lims, 'k--')            # the 45-degree line of perfection
ax[1].set_xlabel('Actual'); ax[1].set_ylabel('Predicted')
ax[1].set_title('Predicted vs Actual')

from scipy import stats
stats.probplot(e, dist='norm', plot=ax[2])
ax[2].set_title('Q-Q plot of residuals')
plt.tight_layout()
```

## 1.6 The decomposition that explains every metric

Mean squared error decomposes exactly into bias and variance of the residuals:

```
MSE = (mean residual)²  +  variance of residuals
    = Bias²             +  Var(e)
```

**Verify on our example:**
```
mean residual   = 18            -> Bias²  = 324
Var(e)          = mean(e²) − (mean e)²  = 4300 − 324 = 3976
Bias² + Var(e)  = 324 + 3976 = 4300 = MSE  ✓
```

This is enormously useful because it tells you **which of the two problems you have**:
- `Bias² / MSE = 324/4300 = 7.5%` → only 7.5% of our squared error is systematic bias.
- `Var(e) / MSE = 92.5%` → the error is overwhelmingly *unsystematic scatter*.

**How to act on the split:**

| Bias² share | Diagnosis | Action |
|---|---|---|
| Large (> ~25%) | Systematic mis-calibration | Check for distribution shift, wrong back-transform, missing intercept/offset, truncated target. Often fixable cheaply with a recalibration step. |
| Small | Irreducible or unstructured scatter | Needs better features, more data, or a more flexible model. Recalibration will not help. |

> **This is the regression analogue of the Murphy decomposition of the Brier score** (reliability vs resolution) from the classification course. Both say the same thing: a squared-error-type metric bundles *systematic* and *random* error, and you should separate them before deciding what to fix.

**Note on terminology:** this residual-level decomposition is *not* the same as the classic **bias-variance decomposition** of expected prediction error, which decomposes error across hypothetical re-trainings on different datasets into `Bias² + Variance + Irreducible noise`. Both are called "bias-variance"; interviewers sometimes conflate them. The one above is computable from a single fitted model's residuals; the classic one requires re-training and is a statement about the *learning procedure*, not about one model's residuals.

---

# PART 2 — Absolute Error Family

## 2.1 MEAN ABSOLUTE ERROR (MAE)

### 1. Definition
The average of the absolute values of the residuals — the typical size of a miss, in the target's own units.

### 2. Intuition
MAE is the most honest, most interpretable regression metric: **"on average, how far off are we?"**

You can say the sentence out loud to a non-technical stakeholder without any translation: "our house price model is off by $36,000 on average." No other regression metric has that property.

Its defining behavioural feature: **MAE treats every unit of error equally.** Being wrong by 200 is exactly ten times as bad as being wrong by 20. That linearity is either exactly right (if your cost really is proportional to the miss) or exactly wrong (if large misses are catastrophically worse), and knowing which is the whole art of metric selection.

The deep property, worth memorising: **MAE is minimised by predicting the conditional MEDIAN.** If you train a model to minimise MAE, it learns to predict the median of `y | x`, not the mean. This has real consequences — see 2.1.10.

### 3. Formula
```
             1    n
MAE  =  ---  ×   Σ   | yᵢ − ŷᵢ |
             n   i=1
```
Symbol by symbol:
- **n** = number of samples
- **i** = sample index
- **yᵢ** = actual value for sample i
- **ŷᵢ** = predicted value for sample i
- **| · |** = absolute value — discards the sign, so over- and under-prediction are treated identically
- **1/n** = the average

Range: **[0, ∞)**. Lower is better. 0 = perfect. **Units: the same as y.**

Also called **L1 loss** or, in some forecasting literature, **MAD (Mean Absolute Deviation)** — although "MAD" more properly means Median Absolute Deviation in robust statistics (see 2.4).

### 4. Manual example

```
Residuals:  −20, +10, −10, +20, −20, +20, −20, +20, −20, +200
Absolute :   20,  10,  10,  20,  20,  20,  20,  20,  20,  200

Step 1 — sum the absolute residuals:
  20+10+10+20+20+20+20+20+20+200 = 360

Step 2 — divide by n = 10:
  MAE = 360 / 10 = 36
```
**MAE = 36 (thousand dollars).** The model misses by $36k on average.

**But look closely at what that average is made of:** nine of the ten absolute errors are 10 or 20. The single 200 contributes `200/360 = 56%` of the total. So the "average miss" of 36 is not a typical miss at all — the typical miss is 20. This is the limitation MedAE exists to fix.

### 5. Python

```python
from sklearn.metrics import mean_absolute_error
import numpy as np

mean_absolute_error(y, y_pred)        # 36.0
np.abs(y - y_pred).mean()             # 36.0  (identical, by hand)

# With sample weights (e.g. weight by revenue, or by recency)
mean_absolute_error(y, y_pred, sample_weight=w)

# In model selection — note the neg_ prefix
# GridSearchCV(model, params, scoring='neg_mean_absolute_error', cv=5)
```
Line-by-line:
- `mean_absolute_error(y_true, y_pred)` — argument order is `(truth, prediction)`. MAE is symmetric so the order does not change the value, but keep truth first as a habit because other functions are not symmetric.
- `sample_weight` is under-used and very powerful: weight each observation by its business importance (revenue, units, customer value) to get a business-relevant MAE.
- **`scoring='neg_mean_absolute_error'`** — sklearn negates all losses so that "greater is better" holds universally in model selection. Forgetting the `neg_` prefix is a rite of passage.

### 6. Interpretation

MAE is in the target's units, so interpretation is always relative to the target's scale. Three anchors:

| Comparison | Our example | Verdict |
|---|---|---|
| MAE vs the **mean of y** | 36 / 450 = **8.0%** | Reasonable |
| MAE vs the **standard deviation of y** | 36 / 193.6 = **0.186** | Good — error is well below natural variation |
| MAE vs a **naive baseline's MAE** | See below | The only rigorous comparison |

**Always compute the baseline.** For a general regression problem the naive baseline is "always predict the mean" or "always predict the median":
```python
mae_mean_baseline   = np.abs(y - y.mean()).mean()     # 150.0
mae_median_baseline = np.abs(y - np.median(y)).mean() # 150.0  (median of y = 425)
```
Our MAE of 36 against a median baseline of 150 gives a **relative absolute error of 36/150 = 0.24**, i.e. the model reduces typical error by 76% versus doing nothing. *That* is the interpretable statement, and it is what RAE and MASE formalise (Part 4).

| Value of MAE/σ(y) | Meaning |
|---|---|
| > 1.0 | The model is worse than predicting a constant. Something is broken. |
| 0.8 | Barely better than the mean |
| 0.5 | Moderate signal |
| 0.19 | Good — our example |
| 0.1 | Strong |
| 0.02 | Excellent (or leakage) |

### 7. Good vs bad values
There is no universal band, because MAE is scale-dependent. The correct procedure:
1. Divide by σ(y) or by the baseline MAE to get a unitless number.
2. Compare to the previous model in production.
3. Compare to the **irreducible noise level** if you can estimate it (e.g. the disagreement between two human appraisers, or the measurement precision of the sensor). If two appraisers differ by $30k on average, an MAE of $36k is essentially at the ceiling.

| Domain | Typical strong MAE, contextualised |
|---|---|
| House price (median $400k) | $25–50k, i.e. 6–12% |
| Retail demand forecast | 10–25% WAPE depending on SKU volatility |
| Delivery-time ETA | 2–5 minutes on a 30-minute trip |
| Temperature forecast (24h) | 1–2 °C |
| Energy load forecast (day-ahead) | 1.5–3% MAPE |

### 8. Business use cases
MAE is the right primary metric whenever **cost is linear in the size of the error**:
- **Inventory and demand planning:** each unit of over- or under-stock costs a roughly fixed amount, so total cost is proportional to total absolute error. MAE (or its weighted cousin WAPE) is the natural metric.
- **Staffing and capacity planning:** each mis-forecast hour costs one hour of wages.
- **Delivery-time ETAs:** each minute late costs roughly the same amount of customer goodwill (up to a point).
- **Energy load forecasting:** balancing costs are approximately linear in the MW imbalance over normal ranges.
- **Any dataset with genuine outliers you do not want to chase:** MAE's linear penalty means a single freak observation does not hijack training.
- **Reporting to executives:** MAE is the only regression metric that needs no explanation.
- **Robust model training** via `loss='absolute_error'` in `GradientBoostingRegressor`, `HuberRegressor`, or `QuantileRegressor(quantile=0.5)`.

### 9. Advantages
- **Directly interpretable** in the target's units, with no transformation.
- **Robust to outliers** relative to MSE/RMSE — a linear rather than quadratic penalty.
- Its gradient has **constant magnitude**, so a single extreme point exerts no more pull on the fit than a mild one (bounded influence).
- Symmetric — treats over- and under-prediction identically.
- Same units as the target, so it can be multiplied by a per-unit cost to give a currency figure directly.
- Well-defined for any real-valued target, including zeros and negatives (unlike MAPE and RMSLE).

### 10. Limitations
- **Scale-dependent** — not comparable across datasets, or across SKUs with different volumes. This is the main reason forecasting practice uses WAPE and MASE instead.
- **Blind to bias.** Residuals `{+36,+36,+36}` and `{+36,−36,+36}` give the same MAE. Always pair with the mean residual.
- **Blind to the distribution of errors.** Nine errors of 20 plus one of 200 gives MAE 36; ten errors of 36 also gives MAE 36. Completely different models. Pair with MedAE and Max Error.
- **Not differentiable at zero**, which historically made it awkward for gradient-based optimisation. In practice subgradients work fine and every major library supports it, but it converges more slowly than MSE and can oscillate near the optimum.
- **Optimises for the median**, not the mean. If your business needs the total to be right (revenue forecasts, insurance reserves), a median-optimal model will be **systematically biased low on right-skewed targets**, because the median of a right-skewed distribution is below its mean. This is a genuinely important and frequently missed issue.
- Gives no credit for explaining variance — a stakeholder cannot tell from MAE alone whether the model is doing anything clever.

### 11. Common mistakes
1. **Reporting MAE without the units.** "MAE is 36" is meaningless; "$36k" or "36 units/week" is a result.
2. **Reporting MAE without a baseline.** Always show the mean/median/naive baseline MAE alongside.
3. **Reporting MAE without a signed bias metric.** The single most common regression evaluation error.
4. Comparing MAE across series with different scales (e.g. averaging MAE over SKUs selling 5/week and 50,000/week — the big SKU dominates). Use WAPE or MASE.
5. **Training on MSE and reporting MAE**, or vice versa, without realising you are optimising for the mean while measuring the median. If MAE is the metric, train with an L1 or Huber loss.
6. Forgetting the `neg_` prefix in `scoring=`.
7. Assuming MAE ≤ RMSE is a coincidence. It is a mathematical guarantee (see 3.2.12).

### 12. Interview questions

**Easy — What is MAE?** The mean of the absolute residuals: `(1/n)Σ|y − ŷ|`. It is the average size of a miss, in the target's units.

**Easy — What are MAE's units?** The same as the target's.

**Easy — Range of MAE?** 0 to ∞, lower better.

**Medium — ★ MAE vs RMSE: when do you prefer each?**
Prefer MAE when you want an interpretable "typical error," when your cost is linear in the error size, and when the data has outliers you do not want to chase. Prefer RMSE when large errors are disproportionately costly, when you want a metric consistent with the mean (and with a Gaussian likelihood), and when you need smooth gradients. Report both: **the ratio RMSE/MAE is itself a diagnostic** — near 1.0 means uniform errors, well above 1.25 means a heavy tail.

**Medium — ★ What statistic does minimising MAE recover?**
The **conditional median** of `y | x`. Minimising MSE recovers the conditional **mean**. This matters because on a right-skewed target the median sits below the mean, so an MAE-optimal model systematically under-predicts the total. If you need the aggregate right, train on MSE (or a Poisson/Tweedie objective), not MAE.

**Medium — Why is MAE more robust to outliers than MSE?**
Because the penalty grows linearly rather than quadratically, so an error of 200 contributes 200 to the sum instead of 40,000. More precisely, MAE's gradient with respect to the prediction is `±1` regardless of the error's size, so an extreme point has bounded influence on the fit. MSE's gradient is proportional to the error, so one outlier can dominate the entire optimisation.

**Hard — ★ You report MAE = 36 and the stakeholder asks "is that good?" How do you answer?**
Give three comparisons rather than a verdict. (1) **Relative to scale:** 36 against a mean of 450 is 8%. (2) **Relative to a baseline:** the naive "predict the median" model has MAE 150, so we cut typical error by 76%. (3) **Relative to the noise floor:** if two human appraisers typically differ by $30k, we are essentially at the ceiling and further modelling has little headroom. Then add that MAE hides the distribution — nine of ten predictions are within $20k and one is off by $200k — so the honest summary is "usually excellent, with one failure mode we should investigate."

**Hard — Why is MAE not differentiable at zero, and does it matter?**
`|e|` has a kink at `e = 0`; its derivative jumps from −1 to +1. Gradient descent uses a subgradient (conventionally 0 at the kink), which works but means the gradient does not shrink as you approach the optimum. The practical consequences: slower convergence, potential oscillation near the minimum, and no closed-form solution for linear models (unlike OLS). **Huber loss exists precisely to fix this** — quadratic near zero for smooth convergence, linear far away for robustness.

---

## 2.2 MEDIAN ABSOLUTE ERROR (MedAE)

### 1. Definition
The median of the absolute residuals — the error of the *typical* prediction.

### 2. Intuition
MAE answers "what is the average miss?" MedAE answers a subtly different and often more useful question: **"what is the typical miss?"**

The difference is entirely about outliers. MedAE is the **most outlier-robust** metric in common use: it has a breakdown point of 50%, meaning **up to half your data could be arbitrarily corrupted and MedAE would barely move.** Nothing else in this document comes close.

Read it as a guarantee: "**half** our predictions are within MedAE of the truth."

### 3. Formula
```
MedAE = median( |y₁ − ŷ₁| , |y₂ − ŷ₂| , ... , |yₙ − ŷₙ| )
```
- Sort the absolute residuals and take the middle one (or the mean of the two middle ones if n is even).
- Range [0, ∞), lower better, **units the same as y**.
- Note: this is the median of the *absolute* residuals, not the absolute value of the median residual. Different quantities.

### 4. Manual example

```
Absolute residuals: 20, 10, 10, 20, 20, 20, 20, 20, 20, 200

Step 1 — sort ascending:
  10, 10, 20, 20, 20, 20, 20, 20, 20, 200
                     ^   ^
                  5th   6th

Step 2 — n = 10 is even, so average the 5th and 6th values:
  MedAE = (20 + 20) / 2 = 20
```
**MedAE = 20 (thousand dollars).**

**The contrast that makes the point:**
```
MAE   = 36    <- distorted by the one $200k miss
MedAE = 20    <- the typical miss, unaffected by it
Ratio = 36/20 = 1.8
```
**A large MAE/MedAE ratio is a direct, quantitative signal that outliers are present.** For symmetric well-behaved errors the ratio is close to 1.0–1.2. Ours is 1.8 → investigate the tail. This ratio is a free diagnostic that almost nobody computes.

### 5. Python

```python
from sklearn.metrics import median_absolute_error
import numpy as np

median_absolute_error(y, y_pred)          # 20.0
np.median(np.abs(y - y_pred))             # 20.0

# The full picture — always look at several quantiles of |e|
ae = np.abs(y - y_pred)
print(np.percentile(ae, [50, 75, 90, 95, 99]))   # [20. 20. 38. 119. 183.8]
print(f"MAE/MedAE ratio = {ae.mean()/np.median(ae):.2f}")   # 1.80
```
Line-by-line:
- `median_absolute_error` takes no `sample_weight` in older sklearn versions (weighted quantiles are newer); check your version.
- **The percentile array is the real deliverable.** Reporting the 50th, 90th, and 95th percentiles of `|e|` is far more informative than any single number, and it is exactly what an SLA conversation needs: "90% of our ETAs are within 4 minutes."

### 6. Interpretation
"Half of all predictions are within MedAE of the truth." Compare to MAE:

| Situation | MAE vs MedAE | Diagnosis |
|---|---|---|
| MAE ≈ MedAE | Ratio ≈ 1.0–1.2 | Errors are homogeneous; either metric is fine |
| MAE > MedAE | Ratio 1.5–3 | A heavy right tail — a minority of bad predictions. Ours: 1.8 |
| MAE ≫ MedAE | Ratio > 3 | Severe outliers, or the model fails catastrophically on a subgroup. Investigate before doing anything else |
| MAE < MedAE | Ratio < 1 | Essentially impossible for absolute errors with a right-skewed distribution; if you see it, check your code |

### 7. Good vs bad values
Same procedure as MAE: divide by σ(y), compare to a baseline, compare to the noise floor. Ours: `MedAE/σ(y) = 20/193.6 = 0.103`, notably better than MAE's 0.186 — which is exactly the point.

### 8. Business use cases
- **Any problem with genuine outliers you must not chase:** real-estate valuation (one mansion in a suburb), salary prediction (one CEO), claim severity (one catastrophic claim).
- **Data with known measurement errors or data-entry mistakes** — MedAE will not be corrupted by them, so it gives an honest read on the model while you clean the data.
- **Robust model comparison during development** — a model whose MedAE improves while MAE worsens is fitting the bulk better and the tail worse, which is often what you want.
- **SLA definitions:** "90% of ETAs within 5 minutes" is a quantile statement, and MedAE is the 50th-percentile version of it.
- **Automated monitoring:** MedAE is stable in production and will not fire spurious alerts when a single weird record arrives.
- **Zillow-style automated valuation models** report median absolute percentage error (MdAPE) as their headline public metric precisely because the property market has a long tail.

### 9. Advantages
- **Maximally robust** — 50% breakdown point; unaffected by any number of outliers up to half the data.
- Interpretable in target units, with a clean probabilistic reading ("half within this").
- Excellent for detecting outlier influence when compared against MAE.
- Stable in production monitoring.
- Not affected by heavy-tailed target distributions.

### 10. Limitations
- **Ignores the tail entirely** — and the tail is sometimes exactly where the money is. A model that is perfect for 51% of cases and catastrophically wrong for 49% has an excellent MedAE. If large errors are expensive, MedAE actively hides your risk.
- **Not differentiable and not usable as a training loss** (it depends only on the rank of one observation, so its gradient is zero almost everywhere).
- **Discards almost all the data** — it is determined by one or two observations, so it is statistically inefficient and has higher variance than MAE for a given n on well-behaved data.
- Scale-dependent.
- Blind to bias.
- Less familiar to stakeholders than MAE, though easy to explain.
- Insensitive to improvements: a model change that fixes the tail without moving the middle leaves MedAE unchanged, which can make it look like nothing happened.

### 11. Common mistakes
1. **Reporting only MedAE on a problem where the tail matters** (insurance, safety, capacity planning). You are hiding the risk.
2. Confusing MedAE with **MAD (Median Absolute Deviation)** — a robust *spread* estimator of a variable, `median(|xᵢ − median(x)|)`, used for outlier detection, not for model evaluation.
3. Confusing the median of absolute residuals with the absolute value of the median residual.
4. Using MedAE as a training objective (it has no useful gradient).
5. Reporting MedAE alone and being surprised when production has occasional catastrophic failures.

### 12. Interview questions

**Easy — What is MedAE?** The median of the absolute residuals — half of predictions are closer than this.

**Easy — Why is it more robust than MAE?** It depends only on the rank of the middle error, so extreme values cannot move it.

**Medium — What is a breakdown point, and what is MedAE's?**
The breakdown point is the fraction of the data that can be arbitrarily corrupted before the estimator becomes arbitrarily wrong. MedAE's is **50%** — the maximum possible. MAE's is 0% (a single infinite error makes MAE infinite), and MSE's is also 0% but it degrades much faster in practice.

**Medium — ★ What does a MAE/MedAE ratio of 3 tell you?**
That there is a substantial right tail: a minority of predictions are far worse than the typical one. It is a signal to (a) inspect the worst residuals individually, (b) check for data errors, (c) check whether the bad cases share a feature value (a subgroup the model fails on), and (d) reconsider whether RMSE or Max Error should be part of your metric set because that tail may be where the business risk lives.

**Hard — Why can't MedAE be used as a loss function?**
Because it is a function of a single order statistic. Changing any prediction other than the middle one leaves MedAE exactly unchanged, so the gradient is zero almost everywhere and gradient descent has no signal. The differentiable robust alternatives are **Huber loss** (quadratic-then-linear) and **quantile/pinball loss at τ = 0.5** (which *is* differentiable-in-subgradient and does target the median — and minimising pinball at 0.5 is equivalent to minimising MAE, up to a factor of 2).

**Hard — When would MedAE mislead you badly?**
When the loss is convex and steep in the tail. Example: an electricity grid balancing model. If 60% of hourly forecasts are within 1 MW (excellent MedAE) but 5% are off by 500 MW, the grid operator pays enormous imbalance penalties on those 5%, and the model is unacceptable. Here you need RMSE, Max Error, and the 99th percentile of |e|. The general rule: **MedAE describes the typical experience; the tail describes the risk. Report both.**

---

## 2.3 MAX ERROR

### 1. Definition
The largest absolute residual — the single worst prediction in the dataset.

### 2. Intuition
Max Error answers the question a safety engineer asks: **"what is the worst thing this model has ever done?"**

Every other metric averages. Max Error refuses to. It exists because in some domains a single bad prediction is the whole story: one structural load calculation wrong by 40%, one drug dosage off by a factor of three, one autonomous-vehicle distance estimate wrong by 5 metres. Averages are irrelevant when the failure mode is catastrophic and non-recoverable.

It is also the fastest, cheapest outlier detector you have.

### 3. Formula
```
Max Error = max( |y₁ − ŷ₁| , ... , |yₙ − ŷₙ| )   =  ‖e‖∞  (the L∞ norm)
```
- Range [0, ∞), lower better, **units the same as y**.
- Sometimes called the **Chebyshev error** or **worst-case error**.

### 4. Manual example

```
Absolute residuals: 20, 10, 10, 20, 20, 20, 20, 20, 20, 200

Max Error = 200
```
**Max Error = 200 (thousand dollars)**, occurring on house 10 (actual $900k, predicted $700k).

The complete picture of our model in three numbers:
```
MedAE     =  20    "typical miss"
MAE       =  36    "average miss"
Max Error = 200    "worst miss"
```
The ratio `Max/MedAE = 10` is a stark statement: the worst case is ten times the typical case. That is the single most decision-relevant fact about this model and it appears in none of the standard metrics.

### 5. Python

```python
from sklearn.metrics import max_error
import numpy as np

max_error(y, y_pred)                    # 200.0

# Always identify WHICH sample it is — that is the actionable part
i = int(np.argmax(np.abs(y - y_pred)))
print(f"Worst case: index {i}, actual {y[i]}, predicted {y_pred[i]}, error {y[i]-y_pred[i]}")
# Worst case: index 9, actual 900.0, predicted 700.0, error 200.0

# The top-k worst predictions — inspect these individually, every time
order = np.argsort(-np.abs(y - y_pred))[:5]
for j in order:
    print(f"  y={y[j]:7.1f}  yhat={y_pred[j]:7.1f}  e={y[j]-y_pred[j]:+7.1f}")
```
- `max_error` only supports single-output regression in sklearn.
- **The `argmax` line is more valuable than the metric.** The point of Max Error is to send you to look at a specific row of data.

### 6. Interpretation
Interpret as a worst-case guarantee, and always express it relative to something:

| Reference | Our example | Reading |
|---|---|---|
| vs the target's range (900 − 200 = 700) | 200/700 = **29%** | The worst error spans nearly a third of the target's range |
| vs σ(y) = 193.6 | 200/193.6 = **1.03** | The worst error is as large as the entire natural variation in y — a serious flag |
| vs MedAE = 20 | ratio **10×** | Extremely heavy tail |
| vs a business tolerance | If the tolerance is $50k, we fail | The only interpretation that matters operationally |

### 7. Good vs bad values
Entirely determined by whether it breaches a tolerance. In engineering and safety contexts the tolerance is specified in advance (by a standard, a regulation, or a hazard analysis), and Max Error is then a **pass/fail test**, not a score to minimise.

Practical guidance:
- **Max Error / σ(y) < 2** is typical for a well-behaved model on clean data.
- **Max Error / σ(y) > 3** almost always indicates either a data error, a genuine outlier the model cannot see, or a region of feature space with no training coverage.
- With large n, Max Error grows simply because you have more chances to draw an extreme — so **Max Error is not comparable across datasets of different sizes.** Use the 99th or 99.9th percentile of |e| instead when you need comparability. This is an under-appreciated point and a good interview answer.

### 8. Business use cases
- **Safety-critical engineering:** structural load prediction, brake-distance estimation, battery thermal models. Regulatory safety cases are written in terms of worst-case error, not average error.
- **Medical dosing and physiological models:** a single large error can be fatal, so the metric is the maximum, often with a mandated tolerance.
- **Autonomous systems:** distance-to-obstacle estimation — the average error is irrelevant if one estimate is 5 m short.
- **Financial risk / VaR-adjacent applications:** worst-case loss estimates.
- **Manufacturing tolerance verification:** a part either falls within specification or it does not.
- **Data quality auditing:** the fastest way to find corrupted rows, unit-conversion mistakes, and mislabelled records. Run `max_error`, look at the row, and you often find a bug rather than a modelling problem.
- **Contractual SLAs** framed as "never more than X off."
- **Debugging any new model** — always look at the worst five predictions before shipping.

### 9. Advantages
- **The only metric that speaks to worst-case risk.**
- Trivial to compute and explain.
- The best available outlier and data-error detector.
- Directly comparable to a specified engineering tolerance, giving a pass/fail decision.
- Immune to being "averaged away" by good performance elsewhere.

### 10. Limitations
- **Determined by a single observation**, so it is maximally unstable — enormous variance, and it changes completely if you resample the test set.
- **Grows with n** by construction, so not comparable across dataset sizes.
- **Uninformative about the bulk of predictions.** A model can have an excellent Max Error and be mediocre everywhere.
- **Cannot be used as a training loss** in any practical sense — a minimax objective is difficult to optimise and would let one point dictate the entire fit.
- Extremely sensitive to label noise: one mistyped value in the test set makes the metric meaningless.
- Scale-dependent; blind to bias.

### 11. Common mistakes
1. **Reporting Max Error as a primary quality metric** when the domain has no catastrophic failure mode. It will just look alarming and mislead.
2. **Comparing Max Error across test sets of different sizes.** Use high percentiles of |e| instead.
3. Not investigating the identified row. The metric's whole value is as a pointer.
4. Optimising for it — this leads to a model warped around one observation.
5. Assuming a bad Max Error means a bad model; it very often means a bad *data point*.

### 12. Interview questions

**Easy — What is Max Error?** The largest absolute residual — the worst single prediction.

**Easy — When is it the primary metric?** When a single large error is catastrophic: safety-critical engineering, medical dosing, autonomous perception.

**Medium — Why is Max Error not comparable across datasets of different sizes?**
Because the maximum of a sample grows with sample size: with more draws from the error distribution you are more likely to observe an extreme value. A model tested on 10,000 rows will show a larger Max Error than the same model tested on 100 rows, with no change in quality. Use the 99th or 99.9th percentile of |e|, which converges to a stable population quantile, when you need cross-dataset comparability.

**Medium — How do you use Max Error in practice, day to day?**
As a debugging tool rather than a score. After every training run, print the ten worst predictions with their feature values. In my experience the majority of extreme residuals turn out to be data problems — unit mix-ups, decimal-place errors, duplicated records, or genuinely out-of-distribution rows — and fixing those improves every other metric at once.

**Hard — ★ How would you build a metric set for a safety-critical regression problem?**
Layer three things. (1) **A hard constraint:** `Max Error ≤ tolerance` on a designated validation set, treated as pass/fail, with the tolerance derived from a hazard analysis rather than chosen for convenience. (2) **A tail metric that is statistically stable:** the 99.9th percentile of |e|, plus a *conservative* upper confidence bound on it (extreme-value theory or a distribution-free tolerance interval), because the empirical max understates the true worst case you will meet in production. (3) **A bulk metric** (MAE or RMSE) for ordinary model development. Then add **asymmetry**: in most safety contexts one direction is dangerous and the other merely inefficient, so use a quantile or cost-weighted loss so the model errs in the safe direction by design. Finally, define the operating envelope explicitly and monitor for out-of-distribution inputs, because worst-case guarantees only hold where you have coverage.

---

## 2.4 A NOTE ON "MAD" — THREE DIFFERENT THINGS

"MAD" is the most overloaded acronym in this field. Interviewers use it to see whether you ask for clarification.

| Name | Formula | What it measures | Where used |
|---|---|---|---|
| **Mean Absolute Deviation** (= MAE) | `(1/n)Σ|yᵢ − ŷᵢ|` | Model error | Forecasting literature; a synonym for MAE |
| **Mean Absolute Deviation from the mean** | `(1/n)Σ|xᵢ − x̄|` | Spread of a variable | Descriptive statistics |
| **Median Absolute Deviation** | `median(|xᵢ − median(x)|)` | Robust spread of a variable | Outlier detection, robust statistics |

**The robust one is the important one.** Median Absolute Deviation is the standard robust replacement for the standard deviation, and it is the basis of the **modified z-score** used to flag outliers:

```
                       0.6745 × (xᵢ − median(x))
modified z-score  =  -----------------------------
                                MAD
```
- The constant **0.6745** makes MAD a consistent estimator of σ for normally distributed data (because for a normal distribution, `MAD ≈ 0.6745 σ`).
- Conventional flag: `|modified z| > 3.5` marks an outlier.
- Preferred over the ordinary z-score because the ordinary z-score uses the mean and standard deviation, both of which are themselves corrupted by the outliers you are trying to find.

```python
import numpy as np

def modified_zscore(x):
    x = np.asarray(x, dtype=float)
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    if mad == 0:                                    # all values identical, or > 50% tied
        mad = np.mean(np.abs(x - med)) * 1.253314   # fall back to mean abs deviation
    return 0.6745 * (x - med) / mad

ae = np.abs(y - y_pred)
print(np.round(modified_zscore(ae), 2))
# the $200k residual is flagged with a very large score
```
**Interview (Medium) — Why use MAD rather than standard deviation for outlier detection?** Because the standard deviation is computed *from* the data including the outliers, so a single extreme value inflates σ and can hide itself ("masking"). MAD has a 50% breakdown point, so it estimates the spread of the *bulk* of the data and the outlier stands out clearly.

---

# PART 3 — Squared Error Family

## 3.0 Why square the error at all?

Three independent reasons, and knowing all three is the mark of understanding rather than memorising:

1. **Statistical:** minimising squared error recovers the **conditional mean**, and it is the **maximum-likelihood estimator under Gaussian noise**. If you believe `y = f(x) + ε` with `ε ~ N(0, σ²)`, then minimising MSE *is* maximum likelihood. This is why OLS is squared-error based and why the whole classical statistics apparatus (t-tests, F-tests, confidence intervals) sits on top of it.

2. **Computational:** `e²` is smooth and differentiable everywhere, with gradient `2e` — proportional to the error, so the optimiser pushes hardest where it is most wrong, and the gradient shrinks to zero at the optimum giving clean convergence. It also yields **closed-form solutions** for linear models (the normal equations), which is why OLS can be solved exactly while L1 regression cannot.

3. **Decision-theoretic:** squaring encodes the belief that **large errors are disproportionately costly**. Being wrong by 20 twice is cheaper than being wrong by 40 once (`2×400 = 800` vs `1600`). Whether that is true is a business question — but it very often is, because many real costs are convex in the error (grid imbalance penalties, stockout cascades, structural failure probability).

The cost of squaring: **extreme sensitivity to outliers.** One error of 200 contributes 40,000 to the sum, which is more than all nine other errors combined by a factor of eleven.

---

## 3.1 SUM OF SQUARED ERRORS (SSE / RSS / SSR)

### 1. Definition
The total of the squared residuals. The raw quantity from which MSE, RMSE, R², and the whole classical regression apparatus are derived.

### 2. Intuition
SSE is the **unaveraged** total squared error — the quantity OLS literally minimises. It exists mainly as a building block rather than a reported metric: R², AIC, BIC, F-statistics, and residual standard error are all expressed in terms of SSE.

### 3. Formula
```
             n
SSE  =      Σ   ( yᵢ − ŷᵢ )²     =  n × MSE
            i=1
```
- Range [0, ∞), lower better, **units are the square of y's units** (dollars-squared — physically meaningless, which is one reason it is not reported directly).
- Naming chaos, worth knowing: it is called **SSE** (Sum of Squared Errors), **RSS** (Residual Sum of Squares), and confusingly also **SSR** in some texts — where other texts use **SSR** to mean the *Regression* Sum of Squares, which is a different quantity. Always define your terms.

**The fundamental ANOVA identity:**
```
SS_tot        =        SS_reg        +        SS_res
Σ(yᵢ − ȳ)²    =    Σ(ŷᵢ − ȳ)²      +    Σ(yᵢ − ŷᵢ)²
"total          "variation explained     "variation left
 variation       by the model"            unexplained"
 in y"
```
- This identity holds **exactly** for OLS with an intercept. It does **not** hold in general for regularised, nonlinear, or tree-based models, which is why R² computed as `1 − SS_res/SS_tot` can behave oddly (and can go negative) outside OLS. This is a favourite advanced interview point.

### 4. Manual example
```
Squared residuals: 400, 100, 100, 400, 400, 400, 400, 400, 400, 40,000
SSE = 400+100+100+400+400+400+400+400+400+40000 = 43,000

Check the ANOVA components:
  SS_tot = Σ(y − 450)²
         = 62,500 + 40,000 + 22,500 + 10,000 + 2,500 + 0 + 2,500 + 10,000 + 22,500 + 202,500
         = 375,000
  SS_res = 43,000
  So the model leaves 43,000 / 375,000 = 11.5% of the total squared variation unexplained.
```
**SSE = 43,000.** Note that house 10 alone contributes 40,000 — **93% of the entire SSE.** Nine houses contribute 7%. Any model fitted by minimising SSE will bend itself around that one house.

### 5. Python
```python
import numpy as np
sse = ((y - y_pred) ** 2).sum()          # 43000.0
ss_tot = ((y - y.mean()) ** 2).sum()     # 375000.0

# Residual standard error (the classical "sigma hat") — SSE per residual degree of freedom
n, p = len(y), 3                          # p = number of predictors
rse = np.sqrt(sse / (n - p - 1))          # 84.66  -- note: divides by n-p-1, not n
```
- **Residual Standard Error (RSE)**, `√(SSE/(n−p−1))`, is what statsmodels prints as `Residual Std. Error` and is the unbiased estimate of the noise standard deviation σ. It differs from RMSE precisely because it corrects for the degrees of freedom consumed by fitting p+1 parameters. RMSE divides by n; RSE divides by n−p−1. On small samples with many features the difference is large.

### 6. Interpretation
Not directly interpretable — the units are squared. Use it as an input to MSE, RMSE, R², AIC, BIC, and F-tests, and use the **share of SSE contributed by the worst few observations** as a concentration diagnostic (ours: 93% from one point).

### 7–8. Good values / use cases
There are no absolute bands. SSE is used inside:
- **OLS estimation** (it is the objective).
- **R²** = `1 − SSE/SS_tot`.
- **AIC / BIC** (Part 9).
- **F-tests** for nested model comparison.
- **Mallows' Cp**.
- **PRESS** (leave-one-out SSE).
- **Concentration diagnostics** — "what fraction of my total squared error comes from the worst 1% of observations?"

### 9. Advantages
- The natural quantity for classical statistical inference.
- Additive across observations, so it decomposes cleanly and supports the ANOVA identity.
- Directly connects to likelihood under Gaussian errors.

### 10. Limitations
- **Grows with n**, so it cannot compare models fitted on different sample sizes. (MSE fixes this.)
- Squared units are meaningless to interpret.
- Extremely outlier-sensitive.
- The ANOVA identity it relies on breaks outside OLS-with-intercept.

### 11. Common mistakes
1. Comparing SSE across datasets of different sizes.
2. Confusing SS_res with SS_reg (both abbreviated SSR in different books).
3. Using RMSE where residual standard error is required (small-n inference).
4. Assuming `SS_tot = SS_reg + SS_res` for a random forest or a regularised model. It does not hold, and this is why out-of-sample R² can be negative.

### 12. Interview questions
**Easy — What is RSS/SSE?** The sum of squared residuals; the quantity OLS minimises.
**Medium — State the ANOVA identity and when it holds.** `SS_tot = SS_reg + SS_res`. It holds exactly for OLS *with an intercept*, because the residuals are orthogonal to the fitted values by construction. It fails for regularised regression, nonlinear models, tree ensembles, and any model not fitted by unpenalised least squares — which is why out-of-sample R² can be negative for those.
**Hard — Difference between RMSE and residual standard error?**
RMSE = `√(SSE/n)`; RSE = `√(SSE/(n−p−1))`. RMSE is a descriptive measure of in-sample or out-of-sample fit. RSE is an *unbiased estimator of the error standard deviation σ*, correcting for the p+1 degrees of freedom consumed by estimating the coefficients. On a training set with n = 20 and p = 10, RMSE understates σ substantially (`√(SSE/20)` vs `√(SSE/9)`), which is exactly why in-sample RMSE is an optimistically biased estimate of generalisation error and why adjusted R², AIC and BIC apply degrees-of-freedom penalties.

---

## 3.2 MEAN SQUARED ERROR (MSE)

### 1. Definition
The average of the squared residuals.

### 2. Intuition
MSE asks: **"what is my average squared miss?"** — which sounds strange until you realise it is really asking *"how much do I care about big misses relative to small ones?"* and answering *"quadratically more."*

Its two defining properties:
- **MSE is minimised by predicting the conditional MEAN.** (Contrast with MAE → median.) This is why MSE-trained models are unbiased in aggregate on average, which matters enormously when the total must be right.
- **MSE = Bias² + Variance of residuals** — it bundles systematic and random error into one number, and separating them is the first diagnostic step.

MSE is the workhorse *loss function* of regression (it is the default in essentially every library) but a poor *reporting* metric, because its units are squared.

### 3. Formula
```
             1    n
MSE  =  ---  ×   Σ   ( yᵢ − ŷᵢ )²        =  SSE / n
             n   i=1
```
- **( yᵢ − ŷᵢ )²** = squared residual — always non-negative, and grows quadratically
- Range [0, ∞), lower better, **units = y's units squared**
- Also called **L2 loss**, **quadratic loss**, or **squared error loss**

**The bias-variance decomposition of the residuals:**
```
MSE = ( mean residual )²  +  Var( residuals )
    =        Bias²        +      Var(e)
```

### 4. Manual example
```
Squared residuals: 400, 100, 100, 400, 400, 400, 400, 400, 400, 40,000

Step 1 — sum: 43,000
Step 2 — divide by n = 10:  MSE = 4,300

Decomposition check:
  mean residual = +18       ->  Bias² = 324
  Var(e) = mean(e²) − (mean e)² = 4,300 − 324 = 3,976
  Bias² + Var(e) = 324 + 3,976 = 4,300  ✓

  Bias² share = 324 / 4300 = 7.5%   -> mostly unstructured scatter, not systematic bias
```
**MSE = 4,300 (thousand-dollars-squared).** The unit is why nobody reports MSE to a stakeholder.

### 5. Python
```python
from sklearn.metrics import mean_squared_error
import numpy as np

mean_squared_error(y, y_pred)                  # 4300.0
((y - y_pred) ** 2).mean()                     # 4300.0

# The decomposition — do this every time
e = y - y_pred
bias, var = e.mean(), e.var()
print(f"MSE={ (e**2).mean():.1f}  Bias^2={bias**2:.1f}  Var={var:.1f}  "
      f"bias share={bias**2/(e**2).mean():.1%}")
# MSE=4300.0  Bias^2=324.0  Var=3976.0  bias share=7.5%

# In model selection
# GridSearchCV(model, params, scoring='neg_mean_squared_error', cv=5)
```
- In scikit-learn ≥ 1.4 the `squared=False` argument of `mean_squared_error` is deprecated in favour of the dedicated `root_mean_squared_error`. Use the latter.

### 6. Interpretation
Do not interpret MSE directly — take its square root and interpret RMSE instead. MSE's only interpretable uses are:
- **Relative comparison** between models on the same data (lower is better).
- **The decomposition** into Bias² and Var.
- **As a training loss.**

### 7. Good vs bad values
Compare `MSE / Var(y)`, which equals `1 − R²`:
```
MSE / Var(y) = 4300 / 37500 = 0.1147   ->  R² = 1 − 0.1147 = 0.8853
```
| MSE/Var(y) | Meaning |
|---|---|
| ≥ 1.0 | Worse than predicting the mean (R² ≤ 0) |
| 0.5 | Half the variance explained |
| 0.11 | Our example — 88.5% of variance explained |
| 0.05 | Strong |
| < 0.01 | Excellent, or leakage |

### 8. Business use cases
MSE is primarily a **training objective** rather than a reported metric:
- **Default loss** in linear regression, ridge, lasso, neural networks, gradient boosting, random forests.
- **Domains where cost is genuinely quadratic in the error:**
  - **Electricity grid balancing** — imbalance penalties escalate super-linearly with the imbalance size.
  - **Control systems** — LQR (Linear Quadratic Regulator) control is built entirely on quadratic cost.
  - **Portfolio optimisation** — variance *is* the risk measure, so squared deviation is the objective by definition.
  - **Signal processing** — MSE relates directly to power and to SNR.
  - **Engineering tolerance stack-up** — variances add, absolute errors do not.
- **Anywhere you need the aggregate/total to be right** (revenue forecasts, insurance reserving, capacity totals) — because MSE targets the conditional mean and means aggregate correctly.
- **A/B test analysis and any classical inference** — the entire t-test/F-test/confidence-interval framework is built on squared error.

### 9. Advantages
- **Smooth and differentiable everywhere**, with gradient `2e` — well-behaved, fast-converging optimisation; closed-form solutions for linear models.
- **Targets the conditional mean**, so the model is unbiased in aggregate and totals add up. Critical for financial and inventory aggregation.
- **Maximum likelihood under Gaussian noise**, giving it a principled statistical foundation and connecting it to the whole inference toolkit.
- Strictly convex, so a unique global optimum for linear models.
- **Decomposes exactly into Bias² + Variance**, which is genuinely actionable.
- Heavily penalises large errors — a feature when large errors really are disproportionately bad.
- Additive and mathematically tractable, which is why it underlies R², AIC, BIC, and Cp.

### 10. Limitations
- **Squared units** make it uninterpretable to humans. Always report RMSE instead.
- **Extremely outlier-sensitive.** In our example one house contributes 93% of the total. A single mistyped value can dominate training. Its breakdown point is 0%.
- **Scale-dependent** and, because of the squaring, *doubly* so — MSE scales with the square of the target's units, so a change of units from dollars to thousands of dollars changes MSE by a factor of a million.
- **Blind to bias when reported alone** — you must decompose it.
- On heteroscedastic data (variance growing with y) MSE is dominated by the high end, effectively ignoring the low end. This is the standard motivation for RMSLE and for log-transforming the target.
- Assumes symmetric costs.
- Not comparable across datasets.

### 11. Common mistakes
1. **Reporting MSE to stakeholders.** Report RMSE — same information, interpretable units.
2. Comparing MSE values across datasets or after a change of units.
3. **Training on MSE when the target is right-skewed and the business cares about relative error.** Log-transform the target or use RMSLE/Poisson/Tweedie objectives instead.
4. **Not checking whether one or two points dominate SSE.** Always compute the share of total squared error from the worst 1%.
5. Not decomposing into Bias² and Var.
6. Forgetting the `neg_` prefix in `scoring=`.
7. Using `squared=False` in recent sklearn versions (deprecated) instead of `root_mean_squared_error`.

### 12. Interview questions

**Easy — What is MSE?** The mean of the squared residuals.
**Easy — What are MSE's units?** The square of the target's units.
**Easy — What statistic does minimising MSE recover?** The conditional mean.

**Medium — ★ Why is MSE the default loss almost everywhere?**
Three reasons at once: it is differentiable with well-behaved gradients (so optimisation is easy and there are closed-form solutions for linear models), it is the maximum-likelihood objective under Gaussian noise (so it is statistically principled and connects to the whole inference toolkit), and it targets the conditional mean (so predictions aggregate correctly). No other loss has all three.

**Medium — ★ Give the bias-variance decomposition of MSE at the residual level and say why it is useful.**
`MSE = (mean residual)² + Var(residuals)`. It is useful because it tells you whether your error is *systematic* (fixable by recalibration, an offset, or investigating distribution shift) or *unstructured scatter* (needs better features or more data). In our example the bias share is only 7.5%, so recalibration would barely help — we need better features.

**Medium — Why is MSE bad for right-skewed targets?**
Because the squared penalty scales with the absolute error, and on a right-skewed target the absolute errors on large values are much bigger than on small values even when the *relative* error is identical. So MSE effectively weights the expensive/high-volume observations enormously and the cheap/low-volume ones almost not at all. If your business cares about relative accuracy across the whole range, use RMSLE, MAPE, or model `log(y)`.

**Hard — ★ You have one observation contributing 93% of your SSE. What do you do?**
First determine whether it is a **data error**, a **genuine but rare event**, or a **coverage gap**. Check the raw record for unit mistakes and typos; check whether its feature values fall inside the training distribution; check whether similar records exist in training. Then choose deliberately: if it is a data error, fix or remove it and document why. If it is genuine and important (a real $900k house you must value correctly), you need features that explain it — and you should consider whether the target should be modelled on a log scale so that relative rather than absolute error is optimised. If it is genuine but unimportant (a freak observation you will never see again), switch to a robust loss (Huber, or L1) so it stops dictating the fit, and report MedAE alongside RMSE. What you must not do is silently delete it to make the metric look better.

**Hard — Why does MSE correspond to maximum likelihood under Gaussian noise?**
If `yᵢ = f(xᵢ) + εᵢ` with `εᵢ ~ N(0, σ²)` independent, the log-likelihood is
`ln L = −(n/2)ln(2πσ²) − (1/(2σ²)) Σ(yᵢ − f(xᵢ))²`.
The only term depending on f is `−(1/(2σ²)) Σ(yᵢ − f(xᵢ))²`, so maximising the likelihood over f is exactly minimising `Σ(yᵢ − f(xᵢ))²` = minimising SSE = minimising MSE. This also tells you what to use when the noise is *not* Gaussian: Laplace noise → L1/MAE; Poisson counts → Poisson deviance; positive right-skewed with constant coefficient of variation → Gamma deviance; zero-inflated positive → Tweedie. **Choosing the loss is choosing the noise model**, and that is the correct way to think about it.

---

## 3.3 ROOT MEAN SQUARED ERROR (RMSE)

### 1. Definition
The square root of MSE — the standard deviation of the residuals about zero, expressed in the target's units.

### 2. Intuition
RMSE fixes MSE's only interpretability problem while keeping its properties: **it is MSE brought back into the target's units.**

Read it as: **"the typical size of a miss, with large misses counted extra."** It is always ≥ MAE, and the gap between them is a direct measure of how heavy-tailed your errors are.

If residuals are roughly normal and unbiased, RMSE has a clean probabilistic reading: **about 68% of predictions fall within ±1 RMSE of the truth, and about 95% within ±2 RMSE.** That interpretation is why RMSE dominates reporting in physical sciences and forecasting.

RMSE is the single most widely reported regression metric in the world, and for good reason: it is interpretable, differentiable-in-practice (via MSE), and consistent with the mean.

### 3. Formula
```
                       ______________________
                      /   1    n
RMSE  =  √MSE  =     /  ---  ×  Σ  ( yᵢ − ŷᵢ )²
                   \/    n     i=1
```
- Range [0, ∞), lower better, **units = y's units**.
- Also called the **quadratic mean of the errors** or, in older literature, the **standard error of the estimate**.
- **`RMSE ≥ MAE` always** (a consequence of the power-mean inequality; equality only when all `|eᵢ|` are identical).

**Important subtlety:** RMSE is a *monotone transform* of MSE, so **minimising RMSE and minimising MSE give the identical model.** RMSE is therefore a *reporting* metric; the *training* objective is MSE (or, equivalently, RMSE — libraries use MSE because the square root adds computation with no benefit and complicates the gradient).

### 4. Manual example
```
Step 1 — MSE = 4,300  (computed in 3.2)
Step 2 — RMSE = √4,300 = 65.574
```
**RMSE = 65.57 (thousand dollars).**

**The three-metric comparison — this is the heart of Part 3:**
```
MedAE =  20.00     "half our predictions are within $20k"
MAE   =  36.00     "average miss is $36k"
RMSE  =  65.57     "typical miss, weighting big misses heavily, is $66k"

RMSE / MAE = 65.57 / 36.00 = 1.82
```
**The RMSE/MAE ratio is a free, powerful diagnostic:**

| RMSE/MAE | Error distribution | Interpretation |
|---|---|---|
| **1.00** | All errors identical in magnitude | Perfectly uniform |
| **≈ 1.25** | Normally distributed errors | The theoretical value is `√(π/2) = 1.2533` |
| **1.5 – 2.0** | Moderately heavy tail | Some large errors. **Ours: 1.82** |
| **> 2.5** | Severe outliers | A few extreme errors dominate; investigate before trusting RMSE |

Demonstration with two constructed models, both with MAE = 10:
```
Model A errors: ±10 repeated ten times
   MAE = 10   RMSE = 10.00   ratio = 1.00   -> uniform errors
Model B errors: nine zeros and one error of 100
   MAE = 10   RMSE = 31.62   ratio = 3.16   -> one catastrophic error
```
**Identical MAE, RMSE differs by more than 3×.** If you reported only MAE these models look equivalent; they are not remotely equivalent. This example is the single best answer to "why report both MAE and RMSE?"

### 5. Python
```python
from sklearn.metrics import root_mean_squared_error, mean_squared_error
import numpy as np

root_mean_squared_error(y, y_pred)                # 65.5744   (sklearn >= 1.4)
np.sqrt(mean_squared_error(y, y_pred))            # 65.5744   (works everywhere)

# The diagnostic ratio — compute it every time
rmse = root_mean_squared_error(y, y_pred)
mae  = np.abs(y - y_pred).mean()
print(f"RMSE={rmse:.2f}  MAE={mae:.2f}  ratio={rmse/mae:.2f}  "
      f"(normal errors would give {np.sqrt(np.pi/2):.3f})")
# RMSE=65.57  MAE=36.00  ratio=1.82  (normal errors would give 1.253)

# In model selection
# GridSearchCV(model, params, scoring='neg_root_mean_squared_error', cv=5)
```
- `scoring='neg_root_mean_squared_error'` exists as a string; you do not need `make_scorer`.
- Because RMSE and MSE are monotonically related, `neg_mean_squared_error` selects the same model — but reporting RMSE is friendlier.

### 6. Interpretation

Three interpretations, in increasing order of usefulness:

**(a) Scale-relative:** `RMSE / σ(y) = 65.57 / 193.65 = 0.339`. Also note `1 − (RMSE/σ_y)² = 1 − 0.1147 = 0.8853 = R²` — RMSE and R² carry the same information when computed against the same baseline, a fact worth knowing.

**(b) Probabilistic (only valid if residuals are roughly normal and unbiased):**
> "About 68% of our predictions are within ±$66k of the truth, and about 95% are within ±$131k."
Check this claim on the data before making it — in our example the residuals are *not* normal (one huge outlier), so the ±1 RMSE band actually contains 9/10 = 90% of predictions, not 68%. **State the interpretation only after checking the Q-Q plot.**

**(c) Against a baseline:**
```python
rmse_baseline = np.sqrt(((y - y.mean())**2).mean())   # 193.65 (= σ_y)
print(rmse / rmse_baseline)                            # 0.339  -> RSE, see Part 4
```

| RMSE/σ(y) | Meaning |
|---|---|
| ≥ 1.0 | No better than the mean (R² ≤ 0) |
| 0.7 | Weak (R² ≈ 0.51) |
| 0.5 | Moderate (R² = 0.75) |
| 0.34 | Our example (R² = 0.885) |
| 0.2 | Strong (R² = 0.96) |
| 0.1 | Excellent (R² = 0.99), or check for leakage |

### 7. Good vs bad values

| Domain | Typical strong RMSE, contextualised |
|---|---|
| House prices (median ~$400k) | $40–70k, i.e. RMSE/σ ≈ 0.3–0.5 |
| Day-ahead electricity load | 1.5–3% of peak load |
| Temperature forecast (24h) | 1.5–2.5 °C |
| Sensor calibration | Within the instrument's stated precision |
| Kaggle tabular regression | Judged only relative to the leaderboard |
| Recommender rating prediction (1–5 stars) | 0.85–0.95 RMSE was state of the art on Netflix |

### 8. Business use cases
- **Weather and climate forecasting** — the field standard; verification systems are built on RMSE.
- **Energy load and price forecasting** — imbalance penalties are convex, so squared error matches the cost.
- **Kaggle competitions** — the most common regression leaderboard metric, along with RMSLE.
- **Recommender systems** rating prediction — the Netflix Prize was scored on RMSE, which is why it is still the reflex metric there.
- **Sensor calibration and metrology** — directly comparable to instrument precision specifications.
- **Financial volatility and risk modelling** — variance is the risk measure.
- **Scientific model validation** across physics, chemistry, and engineering.
- **Control systems** — quadratic cost is the standard formulation.
- **Any context where you want the aggregate to be right** and you want big misses penalised.

### 9. Advantages
- **Interpretable units** — the key advantage over MSE.
- Retains all of MSE's statistical properties (targets the conditional mean, Gaussian ML, smooth optimisation via MSE).
- **Clean probabilistic reading** under approximate normality (68/95 rule).
- Directly comparable to σ(y), which yields R² and the RSE.
- Universally recognised — you will never have to explain it.
- The RMSE/MAE ratio is a free tail diagnostic.
- Penalises large errors, which is correct when the cost is convex.

### 10. Limitations
- **Outlier-dominated.** Ours is inflated 82% above MAE by one house. Reporting RMSE alone on outlier-heavy data overstates the typical error.
- **Scale-dependent** — not comparable across datasets or across series of different magnitude.
- **Blind to bias** — squares the residuals and loses the sign.
- The 68/95 interpretation is **only valid under approximate normality**, and people quote it without checking.
- On heteroscedastic data it is dominated by the high-value region.
- **Not a "typical error"** despite being described as one — that is MedAE's job. RMSE is deliberately tail-weighted.
- Harder to explain than MAE ("root mean squared" needs unpacking), and stakeholders often mentally substitute MAE.

### 11. Common mistakes
1. **Reporting RMSE without MAE.** The pair, and their ratio, is the informative unit.
2. **Quoting the 68/95 interpretation without checking normality** of the residuals.
3. Calling RMSE the "average error" — it is not; it is a tail-weighted quadratic mean and is always ≥ MAE.
4. Comparing RMSE across datasets or after a unit change.
5. Blaming the model when RMSE is inflated by one mislabelled test record.
6. Believing that "minimising RMSE" differs from "minimising MSE." It does not — they are monotonically related.
7. Using RMSE on a strongly right-skewed target where relative error is what matters. Use RMSLE.
8. Forgetting the `neg_` prefix, or using the deprecated `squared=False`.

### 12. Interview questions

**Easy — What is RMSE?** The square root of the mean squared error, in the target's units.
**Easy — Is RMSE always ≥ MAE?** Yes, always, with equality only when all absolute errors are equal.

**Medium — ★ Why is RMSE ≥ MAE always?**
By the power-mean (or Cauchy-Schwarz / Jensen) inequality: the quadratic mean of a set of non-negative numbers is at least their arithmetic mean. Equivalently, `RMSE² − MAE² = Var(|e|) ≥ 0`, so `RMSE² = MAE² + Var(|e|)`. This is a nice exact statement: **the gap between RMSE and MAE is entirely driven by the variance of the absolute errors** — i.e. by how *unequal* your errors are. Uniform errors → RMSE = MAE. Highly variable errors → RMSE ≫ MAE.

**Medium — ★ What does RMSE/MAE tell you?**
It measures the heaviness of the error distribution's tail. 1.0 means all errors are the same size; `√(π/2) ≈ 1.253` is the expected value for normally distributed errors; well above ~1.5 indicates outliers or a subgroup on which the model fails; above ~2.5 means RMSE is essentially reporting a handful of observations and you should investigate them individually before trusting it.

**Medium — Two models: A has RMSE 50 / MAE 40; B has RMSE 45 / MAE 20. Which do you pick?**
B is better on both metrics, so it wins outright — but the ratios tell you *how* they differ. A's ratio is 1.25 (well-behaved, roughly normal errors, consistent performance). B's ratio is 2.25 (usually much better, but with a tail of large errors). If the cost is linear, B is clearly preferable (half the average error). If a large error is catastrophic, you should examine B's tail: it may be that B is excellent on 95% of cases and dangerous on 5%. Report the 95th and 99th percentiles of |e| for both before deciding, and consider whether a hybrid or a fallback rule for B's failure region is possible.

**Hard — Your RMSE improved from 70 to 65 but MAE worsened from 30 to 34. What happened, and is it an improvement?**
The new model traded typical accuracy for tail accuracy: it fixed some large errors (RMSE down) while degrading the bulk of predictions (MAE up). This commonly happens when you switch from an L1 objective to an L2 objective, add regularisation, or increase model smoothness. Whether it is an improvement is a pure business question: if the cost is convex (grid balancing, safety margins, cascading stockouts), the RMSE improvement is worth the MAE cost. If cost is linear (per-unit inventory holding), it is a regression. Do not decide from the metrics — compute expected cost under the actual cost function, or ask which failure mode the business fears.

**Hard — ★ When would you deliberately NOT use RMSE even though it is the field standard?**
(1) **Right-skewed targets where relative error matters** — house prices, sales volumes across orders of magnitude. RMSE will optimise the expensive tail and ignore the cheap bulk. Use RMSLE or model `log(y)`. (2) **Data with known label noise or outliers** — RMSE will chase the noise. Use MAE or Huber. (3) **When the decision is a quantile, not a mean** — delivery-time promises, inventory safety stock. Use pinball loss. (4) **When comparing across series of different scale** — cross-SKU forecasting. Use MASE or WAPE. (5) **When only the worst case matters** — safety-critical systems. Use Max Error and high percentiles. (6) **When you need a probabilistic forecast, not a point forecast** — use CRPS or NLL.

## 3.4 The absolute-vs-squared summary

| | MAE (L1) | RMSE (L2) |
|---|---|---|
| Formula | mean(\|e\|) | √mean(e²) |
| Our example | 36.00 | 65.57 |
| Units | y's units | y's units |
| Optimal predictor | Conditional **median** | Conditional **mean** |
| Implied noise model | Laplace | Gaussian |
| Outlier sensitivity | Moderate | High |
| Gradient magnitude | Constant (±1) | Proportional to error (2e) |
| Differentiable at 0 | No (kink) | Yes |
| Closed-form for linear models | No | Yes (normal equations) |
| Convergence | Slower, can oscillate | Fast, clean |
| Aggregates correctly (totals) | No — biased low on skewed targets | Yes |
| Best when | Cost linear in error; outliers present; want interpretability | Cost convex in error; need the mean/total; Gaussian noise |
| Reported as "average error" | Legitimately | Misleadingly |

**Rule of thumb:** **train on the loss that matches your cost function; report both MAE and RMSE plus their ratio; add MedAE and Max Error whenever the ratio exceeds ~1.5.**

---

# PART 4 — Percentage and Relative Error Family

## 4.0 Why these metrics exist

MAE and RMSE are in the target's units, which creates two problems:

1. **No comparability.** Is MAE = 36 good? You cannot say without knowing the scale. And you cannot average MAE across a SKU selling 5 units/week and one selling 50,000 units/week — the big SKU would dominate entirely.
2. **No sense of proportion.** A $10 error on a $100 item is a disaster; on a $100,000 item it is irrelevant. Absolute metrics treat them identically.

Percentage and relative metrics restore both, at a cost. There are **two distinct strategies**, and confusing them is a common error:

| Strategy | Divide by… | Metrics | Breaks when… |
|---|---|---|---|
| **Percentage** | the actual value `yᵢ` | MAPE, sMAPE, WAPE, MedAPE, MPE | y is zero, near zero, or can be negative |
| **Scaled / relative** | a benchmark model's error | MASE, RAE, RSE, Theil's U, R² | never (as long as the benchmark has non-zero error) |

**The scaled family is technically superior and less well known.** MASE in particular was designed specifically to fix MAPE's defects, and if you can name it in an interview you will stand out.

**A critical property of the percentage family that almost nobody states explicitly:**

> Dividing by `y` makes the metric **asymmetric**. An over-forecast can produce an unbounded percentage error; an under-forecast is capped at 100% (you cannot forecast less than zero). Therefore **MAPE systematically prefers models that under-forecast**, and a model tuned on MAPE will be biased low. This is not a subtlety — it is a documented cause of chronic stockouts in retail forecasting.

---

## 4.1 MEAN ABSOLUTE PERCENTAGE ERROR (MAPE)

### 1. Definition
The average of the absolute percentage errors — the average miss expressed as a percentage of the actual value.

### 2. Intuition
MAPE is the most *demanded* and most *criticised* regression metric in existence.

Demanded because it answers the question every business stakeholder actually asks: **"how far off are we, in percent?"** A single unitless number, comparable across products, regions, and time periods, immediately intelligible. "Our forecast accuracy is 94%" is a sentence that survives contact with a boardroom.

Criticised because the way it achieves that — dividing by the actual value — introduces four serious defects: it explodes near zero, it is undefined at zero, it is asymmetric, and it over-weights small actuals. Academic forecasting literature has recommended against it for decades; industry uses it anyway, because nothing else is as communicable.

**Your job is to use it knowingly:** report it because stakeholders want it, and report WAPE or MASE alongside because they are correct.

### 3. Formula
```
                100    n    | yᵢ − ŷᵢ |
MAPE (%)  =   ------  ×  Σ   ------------
                 n     i=1     | yᵢ |
```
Symbol by symbol:
- **yᵢ** = actual value — **appears in the denominator**, which is the source of every problem
- **ŷᵢ** = predicted value
- **| yᵢ − ŷᵢ | / | yᵢ |** = the absolute percentage error for sample i, as a fraction
- **× 100** = converts to a percentage (scikit-learn returns the **fraction**, not the percentage — multiply by 100 yourself)
- Range **[0, ∞)** — MAPE can exceed 100%, and often does on low-volume series
- **Undefined when any `yᵢ = 0`**; explodes when any `yᵢ` is small

**Note on "forecast accuracy":** business reporting often uses `Accuracy = 100% − MAPE`, which is a dangerous convention because MAPE > 100% gives negative "accuracy." Prefer `Accuracy = 100% − WAPE`, which is bounded more sensibly in practice.

### 4. Manual example
```
i    y     |e|    |e|/y
1   200     20    20/200  = 0.100000
2   250     10    10/250  = 0.040000
3   300     10    10/300  = 0.033333
4   350     20    20/350  = 0.057143
5   400     20    20/400  = 0.050000
6   450     20    20/450  = 0.044444
7   500     20    20/500  = 0.040000
8   550     20    20/550  = 0.036364
9   600     20    20/600  = 0.033333
10  900    200   200/900  = 0.222222
                          ----------
                    Σ    = 0.656840

MAPE = 0.656840 / 10 = 0.0656840  =  6.57%
```
**MAPE = 6.57%.**

**Now notice something instructive.** Compare against WAPE (4.3):
```
MAPE = 6.57%     (average of the per-item percentages)
WAPE = 8.00%     (total error / total actual = 360/4500)
```
**WAPE is higher.** Why? Because MAPE gives the $900k house — where the error is $200k — the same 1/10 weight as the $200k house, where the error is $20k. MAPE democratises across *items*; WAPE weights by *value*. When your errors are concentrated in the high-value items, **MAPE flatters the model.**

**The near-zero explosion, demonstrated:**
```
Actual y = 1, Predicted ŷ = 3      ->  |1−3|/1 = 200%
Actual y = 1000, Predicted ŷ = 1002 -> |1000−1002|/1000 = 0.2%
```
Both errors are 2 units. MAPE calls one a thousand times worse than the other. On an intermittent-demand SKU that sells 0, 0, 1, 0, 2 units per week, MAPE is either undefined or in the hundreds of percent, and is completely useless.

**The asymmetry, demonstrated:**
```
Actual y = 100:
  Over-forecast  ŷ = 200  ->  |100−200|/100 = 100%
  Over-forecast  ŷ = 400  ->  |100−400|/100 = 300%    <- unbounded
  Under-forecast ŷ =  50  ->  |100− 50|/100 =  50%
  Under-forecast ŷ =   0  ->  |100−  0|/100 = 100%    <- capped at 100%
```
**Under-forecasting can never cost more than 100%; over-forecasting is unbounded.** A model optimised on MAPE will therefore shade its forecasts downward. In retail this produces systematic under-stocking. This is the single most important thing to know about MAPE.

### 5. Python
```python
from sklearn.metrics import mean_absolute_percentage_error
import numpy as np

mean_absolute_percentage_error(y, y_pred)             # 0.06568  <- a FRACTION, not a %
mean_absolute_percentage_error(y, y_pred) * 100       # 6.568 %

# By hand, with explicit zero handling
def mape(y_true, y_pred, eps=None):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    mask = y_true != 0                                # drop zeros, and SAY SO
    if eps is not None:
        return np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), eps))) * 100
    if not mask.all():
        print(f"WARNING: dropped {(~mask).sum()} zero actuals from MAPE")
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

mape(y, y_pred)                                       # 6.568

# In model selection
# GridSearchCV(model, params, scoring='neg_mean_absolute_percentage_error', cv=5)
```
Line-by-line:
- **`mean_absolute_percentage_error` returns a fraction (0.0657), not a percentage.** Multiplying twice, or not at all, is an extremely common bug that produces reports off by 100×.
- sklearn does not raise on zeros; it substitutes a tiny epsilon internally, which silently produces an enormous MAPE rather than an error. **Check for zeros yourself.**
- If you must handle zeros, either drop them (and report how many), floor the denominator, or — better — switch to WAPE or MASE.

### 6. Interpretation

Conventional bands from the forecasting literature (Lewis, 1982) — worth quoting, with the caveat that they are only meaningful for reasonably-scaled, non-intermittent series:

| MAPE | Interpretation |
|---|---|
| < 10% | **Highly accurate** — our example at 6.57% |
| 10 – 20% | Good |
| 20 – 50% | Reasonable |
| > 50% | Inaccurate |

**But context dominates these bands entirely:**
- Day-ahead **electricity load**: 1.5–3% is normal; 10% is a failure.
- **Fast-moving retail** at store-SKU-day level: 30–60% MAPE is typical and 20% is exceptional.
- **New-product forecasts**: 50%+ is expected.
- **Intermittent spare parts**: MAPE is meaningless; use MASE.

Always ask **"MAPE of what, at what aggregation level?"** MAPE improves automatically as you aggregate (store→region→national, day→week→month) because errors cancel. A team can "improve MAPE" purely by reporting at a coarser level. This is a well-known gaming vector.

### 7. Good vs bad values
Compare to (a) the previous model, (b) a naive baseline's MAPE, and (c) an explicit statement of the aggregation level. Never quote a MAPE band without the domain.

### 8. Business use cases
- **Retail and CPG demand forecasting** — the industry's default reporting metric; supply-chain contracts and vendor scorecards are written in MAPE.
- **Energy load and price forecasting** — 1–3% MAPE targets are standard and meaningful because load never approaches zero.
- **Financial planning and revenue forecasting** — budget-vs-actual variance is naturally a percentage.
- **Call-centre volume forecasting** — staffing decisions scale with volume.
- **Airline passenger and capacity forecasting.**
- **Pharmaceutical demand planning.**
- **Any executive-facing forecast report**, because it is the only regression metric most executives already understand.
- **Cross-series comparison** where all series are comfortably above zero.

### 9. Advantages
- **Unitless and immediately interpretable** — the strongest communication properties of any regression metric.
- **Comparable across series, products, regions, and time periods** (when all values are safely above zero).
- **Scale-free**, so it can be averaged across heterogeneous items.
- Universally recognised in business; no explanation required.
- Directly maps to the "forecast accuracy = 100 − MAPE" convention that many organisations already use.

### 10. Limitations
This is the longest limitations list in the document, and every item matters.
- **Undefined when y = 0** and explodes when y is near zero. Fatal for intermittent demand, new products, count data with zeros, and anything that can be zero.
- **Asymmetric:** over-forecasts can exceed 100% error, under-forecasts cannot. **Optimising MAPE biases forecasts low.**
- **Over-weights low-value observations.** A 50% error on a 2-unit item counts as much as a 50% error on a 20,000-unit item, so MAPE can be optimised by nailing the trivial items.
- **Cannot be used for targets that go negative** (profit, temperature in Celsius, returns) — the ratio becomes meaningless.
- **Not a proper loss for the mean:** minimising MAPE targets a weighted median, and the weighting depends on `1/y`, so the implied estimator is obscure and biased.
- **Improves automatically with aggregation**, making it gameable.
- **The Lewis bands are arbitrary** and widely misapplied.
- Dominated by whichever observations happen to have the smallest actuals.
- Unstable — a single small actual can swing the whole metric.

### 11. Common mistakes
1. **The ×100 bug.** sklearn returns a fraction. Reporting 0.0657 as "0.07% MAPE" or 6.568 as "656.8%" both happen constantly.
2. **Using MAPE on data containing zeros** and either crashing, silently dropping rows, or getting an absurd value from sklearn's internal epsilon.
3. **Using MAPE on intermittent demand.** This is the classic supply-chain error. Use MASE.
4. **Optimising MAPE and not noticing the resulting downward bias.** Always report MPE (signed) alongside.
5. **Comparing MAPEs computed at different aggregation levels.**
6. **Using MAPE where WAPE is the right metric** — i.e. whenever the business cares about total value, not per-item percentage.
7. Using MAPE on targets that can be negative.
8. Quoting the "< 10% is excellent" band for a store-SKU-day forecast where 40% is genuinely good.

### 12. Interview questions

**Easy — What is MAPE?** The mean of `|y − ŷ| / |y|`, expressed as a percentage.
**Easy — What does sklearn's `mean_absolute_percentage_error` return?** A fraction, not a percentage.
**Easy — When is MAPE undefined?** When any actual value is zero.

**Medium — ★ Why is MAPE asymmetric, and what is the practical consequence?**
Because the denominator is the actual value. An under-forecast is bounded — the smallest possible forecast is zero, giving 100% error. An over-forecast is unbounded — forecasting 5× the actual gives 400% error. So the penalty for over-forecasting is strictly larger, and any model or hyperparameter search optimising MAPE will shade forecasts downward. In retail this manifests as **systematic under-stocking and chronic stockouts**, which is precisely the failure mode that motivated MASE.

**Medium — ★ Why can't you use MAPE for intermittent demand?**
Because intermittent series contain many zeros and many very small values. Zeros make MAPE undefined; small values make it explode. A spare-parts SKU selling `0, 0, 1, 0, 0, 2` per week will yield either a division-by-zero or a MAPE in the hundreds of percent, regardless of forecast quality. **MASE** is the standard replacement, because its denominator is the in-sample naive MAE — a single number for the whole series that is zero only in the degenerate case of a perfectly constant series.

**Medium — ★ MAPE vs WAPE — when do they diverge and which should you trust?**
MAPE averages per-item percentages, so every item gets equal weight. WAPE divides total absolute error by total actual, so items are weighted by their volume/value. They diverge whenever error is concentrated in high-volume or low-volume items. In our example MAPE = 6.57% and WAPE = 8.00%: the errors are concentrated in the biggest house, which MAPE down-weights. **Trust WAPE when the business cost is proportional to value** (which it usually is — you buy inventory in units, not in percentages), and report MAPE alongside for communication.

**Hard — Your MAPE is 12% at SKU-week level and 4% at national-month level. Which is real?**
Both are real; they answer different questions. Errors partially cancel under aggregation (both across SKUs and across time), so aggregate MAPE is always ≤ disaggregate MAPE. Which one matters depends on the decision the forecast drives: store-level replenishment decisions are made at SKU-store-week, so the 12% is the operationally relevant number; factory capacity planning is made at national-month, so 4% is relevant there. The failure mode to guard against is a team reporting the aggregate number to claim credit while the operational decisions are made — and failing — at the disaggregate level. Always report the level explicitly, and report at the level where the decision is taken.

**Hard — ★ You must report a percentage metric for a series containing zeros. What do you do?**
Do not patch MAPE. Choose deliberately from the alternatives, and justify it:
(1) **WAPE** — `Σ|e| / Σ|y|`. Well-defined as long as the *total* is non-zero, weights by volume, symmetric, and is directly interpretable as "total error as a fraction of total volume." This is the right default for supply chain.
(2) **MASE** — scaled by the in-sample naive MAE. Well-defined, symmetric, interpretable against a benchmark, and the academically recommended choice.
(3) **sMAPE** — divides by the average of actual and forecast. Handles zeros a bit better but is still asymmetric and has its own pathologies; I would not recommend it.
Then explain to the stakeholder that "accuracy = 100 − WAPE" gives them the same kind of sentence they wanted, without the mathematical defects.

---

## 4.2 SYMMETRIC MAPE (sMAPE)

### 1. Definition
A variant of MAPE that divides by the average of the actual and the forecast, intended to remove MAPE's asymmetry.

### 2. Intuition
The idea: MAPE's asymmetry comes from putting only `y` in the denominator. If we put *both* `y` and `ŷ` in the denominator, the metric should treat over- and under-forecasting equally.

It partially works — and it was the metric used in the influential M3 forecasting competition, which is why you will meet it. But **it does not actually achieve symmetry**, and it has its own pathologies. Treat it as a historically important metric to recognise rather than one to choose.

### 3. Formula

**The most common form (M3 competition, and what most libraries implement):**
```
                 100    n         | yᵢ − ŷᵢ |
sMAPE (%)  =   ------  ×  Σ   ---------------------
                  n     i=1   ( |yᵢ| + |ŷᵢ| ) / 2
```
- Range **[0, 200%]** — bounded above, unlike MAPE, which is genuinely useful.
- Undefined only when **both** y and ŷ are zero (a much rarer event than y alone being zero).

**Warning — there are at least three published definitions of sMAPE**, differing by a factor of 2 and by whether absolute values are taken. Some omit the `/2` (range [0,100%]); the original Armstrong (1985) version used `(y + ŷ)` without absolute values, which can go negative. **Always state which definition you used**, and never compare an sMAPE from one paper to one from another without checking. This definitional chaos is itself a reason to prefer MASE.

### 4. Manual example
```
i    y     ŷ     |e|    (|y|+|ŷ|)/2    |e| / avg
1   200   220     20     210            0.095238
2   250   240     10     245            0.040816
3   300   310     10     305            0.032787
4   350   330     20     340            0.058824
5   400   420     20     410            0.048780
6   450   430     20     440            0.045455
7   500   520     20     510            0.039216
8   550   530     20     540            0.037037
9   600   620     20     610            0.032787
10  900   700    200     800            0.250000
                                       ----------
                                 Σ  =   0.680940

sMAPE = 0.680940 / 10 = 0.068094 = 6.81%
```
**sMAPE = 6.81%**, compared to MAPE = 6.57%. Slightly higher here.

**Why sMAPE is still asymmetric — the demonstration that matters:**
```
Actual y = 100:
  Over-forecast  ŷ = 150:  |100−150| / ((100+150)/2) = 50/125 = 40.0%
  Under-forecast ŷ =  50:  |100− 50| / ((100+ 50)/2) = 50/ 75 = 66.7%
```
**Same 50-unit error, and sMAPE now penalises UNDER-forecasting more.** It has not removed the asymmetry — it has *reversed* it. A model optimised on sMAPE will be biased *high*, the opposite of MAPE. Neither is symmetric; the name is simply wrong.

### 5. Python
Not in scikit-learn — you must implement it, which means you must pick a definition:
```python
import numpy as np

def smape(y_true, y_pred):
    """M3-competition definition. Range [0, 200]%."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    mask = denom != 0                        # both zero -> undefined, skip
    return np.mean(np.abs(y_true[mask] - y_pred[mask]) / denom[mask]) * 100

smape(y, y_pred)      # 6.809
```
- The `mask` handles the both-zero case, which is the only undefined situation.
- If you use a different definition, document it in the same file as the metric.

### 6. Interpretation
Same bands as MAPE roughly, but note the [0, 200%] range: a completely wrong forecast (predicting 0 when actual is positive, or vice versa) gives exactly 200%. That boundedness is sMAPE's genuine advantage.

### 7. Good vs bad values
< 10% excellent, 10–20% good, 20–50% reasonable, > 50% poor. Same domain caveats as MAPE.

### 8. Business use cases
- **Forecasting competitions** — M3 used sMAPE, so historical benchmark results are reported in it. (The later M4 and M5 competitions moved to **OWA** (a combination of sMAPE and MASE) and **WRMSSE** respectively — a strong signal that the field abandoned sMAPE.)
- **Series containing occasional zeros** where MAPE fails but you still want a percentage — though WAPE is better.
- **Legacy reporting** where an organisation already uses it.
- **Academic comparison** against published sMAPE results.

### 9. Advantages
- **Bounded [0, 200%]** — a single terrible forecast cannot make the metric infinite, unlike MAPE.
- Defined when `y = 0` (as long as `ŷ ≠ 0`), which covers most intermittent-demand cases.
- Less explosive than MAPE near zero.
- Unitless and comparable across series.
- Historically important, so it appears in benchmark tables.

### 10. Limitations
- **Not actually symmetric** — the name is a misnomer, and the asymmetry runs *opposite* to MAPE's, biasing forecasts high.
- **At least three incompatible published definitions**, so cross-study comparison is unreliable.
- The denominator depends on the forecast, which is philosophically odd: **a metric whose scale the model can influence is a metric the model can game.** Inflating the forecast increases the denominator and can reduce sMAPE.
- Still unstable when both y and ŷ are small.
- Harder to explain than MAPE or WAPE ("percentage of the average of actual and forecast" is a mouthful with no natural business meaning).
- Not in scikit-learn.
- Superseded by MASE and by WAPE in both academic and industrial practice.

### 11. Common mistakes
1. **Assuming it is symmetric.** It is not.
2. **Comparing sMAPE across papers or tools without checking the definition.**
3. Using it when WAPE or MASE would be strictly better.
4. Reporting it without specifying the range convention ([0,100] vs [0,200]).

### 12. Interview questions
**Easy — What problem does sMAPE claim to solve?** MAPE's asymmetry and its explosion near zero.
**Medium — ★ Does sMAPE actually achieve symmetry? Prove it.** No. With actual 100, an over-forecast to 150 gives 50/125 = 40%, while an under-forecast to 50 gives 50/75 = 66.7%. Same absolute error, different penalty — and note the direction is *reversed* relative to MAPE, so sMAPE biases forecasts upward.
**Medium — Why is it problematic that sMAPE's denominator contains the forecast?** Because the model can influence the metric's scale. Inflating forecasts enlarges the denominator and can lower sMAPE without improving accuracy. A well-designed metric's denominator should depend only on the data.
**Hard — The M4 competition replaced sMAPE with OWA. Why?**
Because sMAPE's defects were well documented: false symmetry, definitional inconsistency, instability near zero, and a forecast-dependent denominator. OWA (Overall Weighted Average) averages the *relative* performance on sMAPE and on **MASE**, both normalised against a naive-2 benchmark, so it retains comparability with the historical sMAPE literature while incorporating a properly scaled, well-behaved metric. The M5 competition went further and used **WRMSSE** — a weighted, scaled RMSE — reflecting the field's convergence on scaled rather than percentage metrics.

---

## 4.3 WEIGHTED ABSOLUTE PERCENTAGE ERROR (WAPE / WMAPE)

### 1. Definition
Total absolute error divided by total actual value. Also called **MAD/Mean ratio** or, in supply chain, simply "the accuracy metric."

### 2. Intuition
This is, for most business purposes, **the metric MAPE should have been.**

Instead of averaging per-item percentages (which gives a 2-unit SKU the same voice as a 20,000-unit SKU), WAPE asks the question a business actually cares about: **"across everything, what fraction of total volume did we get wrong?"**

Equivalently: it is a **volume-weighted MAPE**, where each item's percentage error is weighted by its share of total volume. That is exactly the right weighting when cost is proportional to units or dollars.

It is also **immune to the zero problem** (the denominator is a total, not an individual value), **symmetric**, and **stable**. It is the default forecast-accuracy metric at most large retailers and CPG companies, usually reported as `Accuracy = 100% − WAPE`.

### 3. Formula
```
                  Σᵢ | yᵢ − ŷᵢ |            Σ |e|         MAE
WAPE (%)  =  100 × -------------------  = 100 × --------  =  100 × --------
                     Σᵢ | yᵢ |               Σ |y|        mean(|y|)
```
- **Numerator** = total absolute error, in units
- **Denominator** = total actual volume, in units
- The third form shows a useful identity: **WAPE = MAE / mean(|y|)**. So WAPE is just MAE normalised by the average actual — which makes it trivially easy to compute and to explain.
- Range [0, ∞) but in practice usually well under 1; undefined only if the total is zero.

**The weighted-MAPE identity** (worth deriving in an interview):
```
              Σ |eᵢ|         Σ ( |yᵢ| × |eᵢ|/|yᵢ| )                    |yᵢ|
WAPE  =  ---------------  =  --------------------------- =  Σ  wᵢ × APEᵢ ,   wᵢ = --------
              Σ |yᵢ|                  Σ |yᵢ|                                      Σ |yⱼ|
```
So WAPE is literally a **volume-weighted average of the individual absolute percentage errors.** That is where the "weighted" in the name comes from, and it is the cleanest one-line justification for using it.

### 4. Manual example
```
Σ |e| = 360
Σ  y  = 4,500

WAPE = 360 / 4500 = 0.08 = 8.00%
Forecast "accuracy" = 100% − 8% = 92%

Cross-check via the identity:
  MAE / mean(y) = 36 / 450 = 0.08  ✓
```
**WAPE = 8.00%.**

**The comparison table that shows why the choice matters:**
```
MAPE  = 6.57%   -> each house counts equally; the big house's $200k error is diluted
sMAPE = 6.81%
WAPE  = 8.00%   -> weighted by house value; the big house's error is properly heavy
```
**WAPE is the highest because our errors are concentrated in the highest-value item.** If a stakeholder is told "6.57%" they are being flattered; "8.00%" is the honest figure in value terms.

### 5. Python
```python
import numpy as np

def wape(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return np.abs(y_true - y_pred).sum() / np.abs(y_true).sum() * 100

wape(y, y_pred)                                        # 8.0

# Identity check
np.abs(y - y_pred).mean() / np.abs(y).mean() * 100     # 8.0

# In sklearn model selection, via a custom scorer
from sklearn.metrics import make_scorer
wape_scorer = make_scorer(wape, greater_is_better=False)
# GridSearchCV(model, params, scoring=wape_scorer, cv=5)

# Weighting by revenue rather than units — often what the business really wants
def wape_weighted(y_true, y_pred, value_per_unit):
    num = (np.abs(y_true - y_pred) * value_per_unit).sum()
    den = (np.abs(y_true) * value_per_unit).sum()
    return num / den * 100
```
- `greater_is_better=False` tells sklearn to negate the score internally so higher is better in the search. (In newer versions the parameter is `greater_is_better`; check your version's signature.)
- The `value_per_unit` variant is the version most supply-chain teams actually need: a 10% error on a high-margin item matters more than on a low-margin one.

### 6. Interpretation
Directly interpretable: **"our total absolute error is 8% of total volume."** Or, in the business convention, **"we are 92% accurate."**

| WAPE | Interpretation |
|---|---|
| < 10% | Strong |
| 10 – 20% | Good |
| 20 – 40% | Typical at disaggregate levels |
| > 50% | Weak, or an intrinsically hard/intermittent series |

**Crucially, the same aggregation caveat as MAPE applies:** WAPE improves as you aggregate. Always state the level.

### 7. Good vs bad values
| Level | Typical good WAPE (fast-moving retail) |
|---|---|
| National, monthly | 3 – 8% |
| National, weekly | 5 – 12% |
| Region, weekly | 10 – 20% |
| Store-SKU, weekly | 25 – 50% |
| Store-SKU, daily | 40 – 70% |

These numbers surprise people. **Store-SKU-daily forecasting is genuinely hard**, and a 45% WAPE there can be an excellent model. Quoting the wrong band for the wrong level is a classic mistake.

### 8. Business use cases
- **Retail and CPG demand forecasting** — the de facto industry standard, usually as "forecast accuracy = 100 − WAPE."
- **Supply-chain vendor scorecards and contracts.**
- **Inventory planning** — because the cost of a forecast error is proportional to units, and WAPE weights by units.
- **Intermittent demand** — well-defined even with many zeros, unlike MAPE.
- **Cross-SKU and cross-store aggregation** — the only percentage metric that aggregates coherently.
- **Revenue and financial forecasting**, weighting by value rather than units.
- **Call-centre and workforce planning.**
- **Any situation where a stakeholder wants a percentage but MAPE would mislead.**

### 9. Advantages
- **Well-defined with zeros** in the actuals — the single biggest practical advantage over MAPE.
- **Volume-weighted**, so it aligns with business cost rather than with item count.
- **Symmetric** — no built-in preference for over- or under-forecasting.
- **Stable** — one small actual cannot swing it, because the denominator is a total.
- **Interpretable as a percentage**, so it satisfies the same stakeholder demand as MAPE.
- Trivially computable as `MAE / mean(y)`.
- Aggregates coherently: the WAPE of a group is a proper weighted combination of its members' errors.
- **Naturally extensible to value-weighting** (revenue, margin, criticality).

### 10. Limitations
- **Not in scikit-learn** — you must implement it, and different teams implement it slightly differently (units vs value weighting).
- **Dominated by high-volume items.** This is usually the right behaviour, but it means poor performance on the long tail of small items is invisible. If tail items matter (e.g. they cause store-level stockouts and customer complaints), report a per-item metric such as MASE or a segmented WAPE by volume decile alongside.
- **Hides the direction of error** — like all absolute metrics, it is blind to bias. Report signed bias too.
- **Improves with aggregation**, so it is gameable if the level is not fixed.
- Not scale-free in the strict sense: it is comparable across series only when the series are measured in comparable units.
- Less familiar to academics (who prefer MASE), so it needs a definition in a paper.

### 11. Common mistakes
1. **Confusing WAPE with MAPE** and expecting them to agree. They diverge exactly when error is concentrated in high- or low-volume items — which is most of the time.
2. **Not stating the aggregation level.**
3. Reporting `100 − WAPE` as "accuracy" without noting it can go negative for very poor forecasts.
4. **Reporting WAPE alone and ignoring the long tail** of small items.
5. Not reporting signed bias alongside.
6. Weighting by units when the business cost is driven by value (or vice versa) — decide deliberately.

### 12. Interview questions
**Easy — What is WAPE?** Total absolute error divided by total actual, as a percentage. Equivalently `MAE / mean(y)`.
**Easy — Why does WAPE handle zeros when MAPE does not?** Because the denominator is the *sum* of actuals, not each individual actual. A zero contributes nothing to the denominator instead of causing a division by zero.

**Medium — ★ Prove that WAPE is a volume-weighted MAPE.**
`WAPE = Σ|eᵢ| / Σ|yᵢ|`. Write `|eᵢ| = |yᵢ| × (|eᵢ|/|yᵢ|) = |yᵢ| × APEᵢ`. Substituting gives `WAPE = Σ(|yᵢ| × APEᵢ) / Σ|yᵢ| = Σ wᵢ APEᵢ` with weights `wᵢ = |yᵢ| / Σ|yⱼ|` summing to 1. So WAPE is exactly the average of the per-item absolute percentage errors, weighted by each item's share of total volume.

**Medium — ★ MAPE = 6.6% and WAPE = 8.0% on the same data. What does that tell you?**
That the errors are concentrated in the **high-volume/high-value items**. MAPE weights every item equally, so a big error on the biggest item is diluted to 1/n; WAPE weights by volume, so it surfaces. (If WAPE were *lower* than MAPE, the errors would be concentrated in small items.) Since the business cost is proportional to volume, the 8% is the operationally honest figure, and I would investigate the largest items first.

**Hard — A stakeholder says our forecast accuracy is 92% but the warehouse keeps running out of stock. Reconcile that.**
Three likely explanations, all consistent with a good WAPE. (1) **Bias:** WAPE is an absolute metric and cannot see direction. If the forecast is systematically 5% low, WAPE looks fine while inventory is chronically short. Compute the signed bias (MPE or total forecast / total actual) immediately. (2) **Aggregation:** 92% may be measured at national-monthly level while replenishment happens at store-SKU-daily, where accuracy might be 55%. Errors that cancel in the aggregate do not cancel in a single store's stockroom. (3) **Tail concentration:** WAPE is volume-weighted, so poor accuracy on the long tail of slow-moving SKUs is invisible, yet those are exactly the items that go out of stock and generate complaints. The fix is to report bias, report at the decision-making level, and segment WAPE by volume band.

---

## 4.4 MEDIAN ABSOLUTE PERCENTAGE ERROR (MdAPE / MedAPE)

### 1. Definition
The median of the absolute percentage errors.

### 2. Intuition
MAPE's robustness fix, exactly analogous to MedAE fixing MAE. It answers: **"what is the typical percentage miss?"**

Because it is a median, no single exploding percentage error (from a near-zero actual) can move it. That makes it the practical choice whenever you want a percentage metric on data with occasional small actuals — which is most real data.

It is the **headline public metric for automated property valuation models**. Zillow, Redfin and similar services report "median error rate" precisely because the property market has a long tail and a mean-based percentage would be dominated by a handful of unusual homes.

### 3. Formula
```
MdAPE (%)  =  100 × median( |y₁−ŷ₁|/|y₁| , ... , |yₙ−ŷₙ|/|yₙ| )
```
- Range [0, ∞), lower better, unitless.
- Undefined for any observation with `yᵢ = 0`, but a single zero only removes one observation rather than destroying the metric — and if you drop zeros, the median of the rest is still meaningful.

A closely related and slightly better-behaved metric is the **MdAPE within-X%** family: "what fraction of predictions are within 10% / 20% of the truth?" These are called **PE10 / PE20** in real-estate valuation and are extremely communicable.

### 4. Manual example
```
Absolute percentage errors:
  0.1000, 0.0400, 0.0333, 0.0571, 0.0500, 0.0444, 0.0400, 0.0364, 0.0333, 0.2222

Sorted:
  0.0333, 0.0333, 0.0364, 0.0400, 0.0400, 0.0444, 0.0500, 0.0571, 0.1000, 0.2222
                                     ^      ^
                                    5th    6th

n = 10 is even -> average the 5th and 6th:
  MdAPE = (0.0400 + 0.0444) / 2 = 0.0422 = 4.22%
```
**MdAPE = 4.22%.**

**The full percentage-family comparison on identical data:**
```
MdAPE = 4.22%    "the typical house is valued within 4.2%"
MAPE  = 6.57%    "average percentage miss"
sMAPE = 6.81%
WAPE  = 8.00%    "8% of total value is mis-estimated"

MAPE / MdAPE = 1.56  -> a moderate right tail in percentage terms
```
Four legitimate percentage metrics spanning 4.2% to 8.0% on the same predictions. **Which one you report changes the headline by a factor of two.** That is why the choice must be justified from the business question, not chosen for the nicest number.

**PE10 / PE20 on our data:** 8 of 10 predictions are within 10% (all but house 1 at exactly 10.0% and house 10 at 22.2%); 9 of 10 are within 20%. So `PE10 = 80%` (counting <10% strictly) and `PE20 = 90%`.

### 5. Python
```python
import numpy as np

def mdape(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    mask = y_true != 0
    return np.median(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

mdape(y, y_pred)                          # 4.222

# The full quantile picture — far more useful than any single number
ape = np.abs((y - y_pred) / y) * 100
print(np.round(np.percentile(ape, [50, 75, 90, 95]), 2))   # [ 4.22  5.54 11.22 16.72]

# PE10 / PE20 — the real-estate industry's communicable metrics
print(f"PE10 = {(ape < 10).mean():.0%}   PE20 = {(ape < 20).mean():.0%}")
# PE10 = 80%   PE20 = 90%
```

### 6. Interpretation
"Half of our predictions are within MdAPE% of the truth." For property valuation, industry context:
- Leading automated valuation models report median errors around **2–8%** for on-market homes and higher for off-market ones.
- **PE10 above ~80%** is considered strong.

### 7. Good vs bad values
| MdAPE | Verdict (general) |
|---|---|
| < 5% | Excellent — our example at 4.2% |
| 5 – 10% | Good |
| 10 – 20% | Moderate |
| > 20% | Weak |

Combine with `MAPE/MdAPE`: a ratio above ~2 means a substantial minority of predictions are far worse than typical, and you should report the 90th/95th percentile too.

### 8. Business use cases
- **Automated property valuation (AVMs)** — the public standard, alongside PE10/PE20.
- **Insurance claim severity estimation** — heavy-tailed by nature.
- **Salary and compensation benchmarking** — a few executive outliers would wreck MAPE.
- **Used-car and asset pricing.**
- **Any right-skewed monetary target with occasional extreme values.**
- **Public-facing accuracy claims**, because a median is defensible and hard to game with outliers.
- **Data-quality-uncertain settings** — robust to bad records while you clean them.

### 9. Advantages
- **Robust** to both outlier residuals and near-zero actuals — the two failure modes of MAPE.
- Unitless and interpretable, with a clean "half within this" reading.
- Not gameable by a few extreme records.
- Pairs naturally with PE10/PE20, which are exceptionally communicable.
- Stable in production monitoring.

### 10. Limitations
- **Hides the tail completely** — and in insurance, valuation, and lending, the tail is where the loss is. Always report high percentiles alongside.
- Still undefined for zero actuals (though only observation-wise).
- Statistically inefficient — determined by one or two observations.
- Not usable as a training loss.
- **Can make a model look far better than it is.** Reporting MdAPE = 4.2% when the 95th percentile is 16.7% and the worst case is 22% is technically true and practically misleading if used alone.
- Not in scikit-learn.

### 11. Common mistakes
1. **Reporting MdAPE alone** on a tail-sensitive problem. Always add the 90th/95th percentile and Max Error.
2. Choosing MdAPE because it is the smallest number available. Choose it because the median is the right summary.
3. Confusing MdAPE with MedAE (percentage vs absolute).
4. Forgetting to handle zero actuals.

### 12. Interview questions
**Easy — What is MdAPE?** The median of the absolute percentage errors.
**Medium — Why do property-valuation companies report median error rather than mean error?** Because the property market is heavily right-skewed with genuine extreme values (unique architecture, distressed sales, mansions in ordinary neighbourhoods). A mean percentage error would be dominated by a handful of hard-to-value homes and would not reflect what a typical user experiences. The median does, and it is also much harder to distort.
**Medium — What are PE10 and PE20 and why are they useful?** The fraction of predictions within 10% and within 20% of the true value. They are useful because they translate directly into a user-facing promise ("8 out of 10 valuations are within 10%") and because they describe the *shape* of the error distribution rather than a single summary. They are the regression analogue of reporting precision at a threshold.
**Hard — ★ Your MdAPE is 4% but customers complain the valuations are wrong. Diagnose.**
Almost certainly a tail problem that the median conceals, and possibly a segment problem. Steps: (1) compute the full percentile curve of APE — if the 90th percentile is 25% and the 99th is 60%, then one in ten customers has a materially wrong number, and those are precisely the ones who complain. (2) **Segment the error** by property type, price band, geography, and data completeness; a model can have an excellent median overall while failing systematically on, say, rural properties or new-builds with thin comparable data. (3) Check **bias by segment** — a segment that is systematically low will generate a specific, loud kind of complaint. (4) Check **coverage** — complaints often come from properties whose features fall outside the training distribution. The fix is usually not a better global model but **per-segment models, an uncertainty estimate shown to the user, and an abstention rule** that declines to quote a value when the model's confidence is low. Reporting a prediction interval alongside the point estimate resolves most of these complaints even without improving the point estimate.

---

## 4.5 MEAN PERCENTAGE ERROR (MPE) — THE BIAS METRIC

### 1. Definition
The average of the **signed** percentage errors. Unlike every metric so far, it does **not** take absolute values.

### 2. Intuition
This is the metric that catches the failure mode every absolute metric is blind to: **systematic bias.**

MAE, RMSE, MAPE, WAPE, MedAE — all of them square or absolute the residual and therefore **cannot tell the difference between a model that is randomly wrong and one that is consistently wrong in the same direction.** MPE keeps the sign, so a model that always under-forecasts shows up immediately.

> **This is the most under-reported metric in regression practice and the single easiest way to improve your evaluation.** It costs one line of code and catches an entire class of production failures.

**Sign convention (using `e = y − ŷ`):**
- **MPE > 0** → the model **under-forecasts** on average (actuals exceed predictions)
- **MPE < 0** → the model **over-forecasts** on average
- **MPE ≈ 0** → unbiased *on average* (note: this can also happen when large positive and negative biases cancel — see limitations)

### 3. Formula
```
               100    n     ( yᵢ − ŷᵢ )
MPE (%)  =   ------  ×  Σ   -------------
                n     i=1       yᵢ
```
- **No absolute value** — that is the entire point.
- Range **(−∞, +∞)**; **target value is 0**.
- Also called **forecast bias** or **percentage bias**. The unnormalised version is simply the **mean residual** (also called Mean Error, ME, or Mean Forecast Error).

**Three related bias measures, all worth reporting:**
```
Mean residual (ME)    = (1/n) Σ (yᵢ − ŷᵢ)                   in target units
MPE               (%) = (100/n) Σ (yᵢ − ŷᵢ)/yᵢ              per-observation percentage
Total bias / "Bias%"  = 100 × [ Σ(yᵢ − ŷᵢ) ] / Σ yᵢ         aggregate percentage
```
The third is the one supply chain and finance care about most, because it says whether the **total** is right.

### 4. Manual example
```
i    y     e = y−ŷ     e/y
1   200    −20        −0.100000
2   250    +10        +0.040000
3   300    −10        −0.033333
4   350    +20        +0.057143
5   400    −20        −0.050000
6   450    +20        +0.044444
7   500    −20        −0.040000
8   550    +20        +0.036364
9   600    −20        −0.033333
10  900   +200        +0.222222
                      -----------
                Σ  =  +0.143507

MPE = +0.143507 / 10 = +0.0143507 = +1.44%
```
**MPE = +1.44%** → the model **under-forecasts** by about 1.4% on average.

**The other two bias measures on the same data:**
```
Mean residual = +180 / 10 = +18        -> under-predicts by $18k on average
Total bias    = 100 × 180 / 4500 = +4.00%   -> the TOTAL is 4% too low
```
**Note how different these three numbers are: +1.44%, +$18k, +4.00%.** They answer different questions:
- MPE (+1.44%) — the *typical* percentage bias per observation
- Mean residual (+$18k) — the *average* bias in dollars
- Total bias (+4.00%) — whether the **aggregate** is right

For a revenue forecast or an insurance reserve, the total bias is the one that matters. For a per-item forecast quality assessment, MPE. **Report the total bias whenever the sum has business meaning.**

**The demonstration of why bias metrics are essential:**
```
Model X residuals: +36, +36, +36, +36    MAE = 36   RMSE = 36   MPE > 0 strongly
Model Y residuals: +36, −36, +36, −36    MAE = 36   RMSE = 36   MPE = 0
```
**Identical MAE and identical RMSE. Model X is catastrophically biased; Model Y is unbiased.** For an inventory forecast, X guarantees chronic stockouts and Y averages out. No absolute metric can distinguish them.

### 5. Python
```python
import numpy as np

e = y - y_pred

# 1. Mean residual (target units)
print(e.mean())                                        # 18.0

# 2. MPE (per-observation percentage)
mask = y != 0
print((e[mask] / y[mask]).mean() * 100)                # 1.435 %

# 3. Total / aggregate bias — usually the most important
print(e.sum() / y.sum() * 100)                         # 4.000 %

# 4. Forecast-to-actual ratio — the supply-chain convention
print(y_pred.sum() / y.sum())                          # 0.96    -> forecasting 96% of actual

# 5. The complete bias report you should print for every model
def bias_report(y_true, y_pred):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    m = np.asarray(y_true, float) != 0
    return {
        'mean_residual'   : e.mean(),
        'median_residual' : np.median(e),
        'MPE_%'           : (e[m] / np.asarray(y_true, float)[m]).mean() * 100,
        'total_bias_%'    : e.sum() / np.asarray(y_true, float).sum() * 100,
        'pct_under'       : (e > 0).mean() * 100,     # share of under-forecasts
        'pct_over'        : (e < 0).mean() * 100,
    }

for k, v in bias_report(y, y_pred).items():
    print(f"{k:>16}: {v:>8.3f}")
```
Output:
```
   mean_residual:   18.000
 median_residual:    0.000       <- the MEDIAN residual is zero!
           MPE_%:    1.435
    total_bias_%:    4.000
       pct_under:   50.000
        pct_over:   50.000
```
**Look at that output carefully — it is a masterclass in why you need several bias measures.** The *median* residual is exactly 0 and the split of over/under is exactly 50/50, so by those measures the model is perfectly unbiased. But the *mean* residual is +18 and the total is 4% low, entirely because of the one large under-prediction. Interpretation: **the model is not systematically biased in its direction, but it is biased in its aggregate**, because its one large miss happens to be an under-prediction. For a revenue total this matters; for a per-item accuracy assessment it does not. Reporting only one of these would tell you the wrong story.

### 6. Interpretation

| MPE | Meaning | Typical cause |
|---|---|---|
| **> +10%** | Severely under-forecasting | Truncated/censored target; missing growth trend; over-regularisation shrinking predictions toward the mean; training on a lower-demand period |
| **+2 to +10%** | Meaningfully low | Mild version of the above; also common when a right-skewed target is modelled with an MAE loss (median < mean) |
| **−2 to +2%** | Acceptably unbiased | — |
| **−2 to −10%** | Meaningfully high | Naive back-transformation from a log model (see below); training on a higher-demand period; optimising sMAPE |
| **< −10%** | Severely over-forecasting | As above, plus data leakage of a high-value feature |

**The most common single cause of regression bias in practice, and a top interview answer:**
> **Naive back-transformation from a log-space model.** If you train on `log(y)` and predict with `ŷ = exp(prediction)`, you get the **conditional median**, not the conditional mean — because `E[exp(Z)] ≠ exp(E[Z])` by Jensen's inequality. On a lognormal target this **under-predicts the mean by a factor of `exp(σ²/2)`**. With residual variance σ² = 0.2 in log space, that is a systematic 10.5% under-prediction. The fix is a **smearing correction** (multiply by the mean of `exp(residuals)`) or the analytic `exp(μ̂ + σ̂²/2)` adjustment, or to model on the original scale with a Gamma/Tweedie/Poisson objective instead.

### 7. Good vs bad values
Target zero. In practice:

| Domain | Acceptable \|MPE\| or total bias |
|---|---|
| Financial reporting / revenue forecast | < 1–2% (a persistent bias is a compliance and credibility issue) |
| Insurance reserving | < 1% (regulated; the total must be right) |
| Retail demand planning | < 2–3%, and monitored for **drift**, not just level |
| Energy load | < 0.5–1% |
| Exploratory ML models | < 5% is usually fine if the direction is understood |

**More important than the level is the trend.** A stable bias can be corrected with an offset; a *drifting* bias means the world has changed and the model needs retraining. Track it as a control chart (see Tracking Signal, Part 10).

### 8. Business use cases
- **Supply chain and inventory:** a persistent negative bias (over-forecast) causes excess inventory and write-offs; a persistent positive bias (under-forecast) causes stockouts and lost sales. Bias is monitored continuously and is often a named KPI.
- **Financial forecasting and budgeting:** systematic optimism or pessimism in forecasts is a governance issue, and MPE quantifies it.
- **Insurance reserving (IBNR):** reserves must be adequate *in total*; the regulator cares about aggregate bias, not per-claim accuracy.
- **Revenue recognition and capacity planning:** totals must reconcile.
- **Energy trading and grid balancing:** persistent imbalance in one direction is expensive and can be penalised.
- **Model monitoring:** bias drift is the earliest and clearest signal of distribution shift, usually visible before MAE degrades.
- **Post-hoc model correction:** if you know the bias, you can often subtract it and improve every other metric for free — which is exactly why you should measure it.

### 9. Advantages
- **The only metric family that detects systematic bias.** Nothing else does.
- Trivial to compute; one line of code.
- **Directly actionable** — a known bias can often be corrected with an additive or multiplicative adjustment, giving an immediate improvement in MAE, RMSE, and MAPE.
- The best early-warning signal for distribution shift in production monitoring.
- Interpretable in exactly the terms operations teams use ("we are forecasting 96% of actual").
- Aggregate bias reconciles with financial totals, which is a hard requirement in many domains.

### 10. Limitations
- **Positive and negative errors cancel**, so MPE ≈ 0 does **not** mean the model is accurate. A model with residuals `{+1000, −1000}` has MPE ≈ 0 and is terrible. **MPE must always be reported alongside a magnitude metric (MAE/RMSE), never alone.** This is the mirror image of the magnitude metrics' blindness to bias — the two families are complements, not substitutes.
- **Can mask offsetting segment biases:** +15% on segment A and −15% on segment B gives an overall MPE of 0. **Always compute bias by segment.**
- Percentage form inherits MAPE's problems: undefined at zero, unstable near zero, asymmetric weighting.
- Unbounded, so a single small actual can dominate the percentage version. Prefer total bias for robustness.
- Not usable as a standalone loss (minimising it drives the model to any unbiased solution regardless of accuracy).

### 11. Common mistakes
1. **Not reporting it at all.** By far the most common. Every regression evaluation should include a signed bias measure.
2. **Reporting MPE ≈ 0 as evidence of a good model.** It only means the errors cancel.
3. **Not segmenting.** Overall bias of 0% with +20% on one region and −20% on another is two problems, not zero.
4. **Confusing the three bias measures** (mean residual, MPE, total bias) — they can differ substantially, as our example shows.
5. **Naive `exp()` back-transformation from a log model** and then being puzzled by a systematic negative bias.
6. Getting the sign convention backwards. State it explicitly in every report.
7. Correcting the bias with an offset without asking *why* it exists — if the cause is distribution shift, the offset will be stale next month.

### 12. Interview questions

**Easy — What is MPE and how does it differ from MAPE?** MPE keeps the sign of the error; MAPE takes the absolute value. MPE measures bias; MAPE measures magnitude.
**Easy — What does MPE = 0 tell you?** That the errors cancel on average. It says nothing about accuracy.

**Medium — ★ Why must you report a signed bias metric alongside MAE or RMSE?**
Because absolute and squared metrics destroy the sign, so they cannot distinguish a model that is randomly wrong from one that is consistently wrong in the same direction. Residuals `{+36,+36,+36,+36}` and `{+36,−36,+36,−36}` have identical MAE and RMSE, but the first guarantees systematic stockouts (or systematic over-reserving) and the second averages out. Bias is also usually the cheapest defect to fix — often a single offset — so measuring it has the highest return per line of code of anything in regression evaluation.

**Medium — ★ You trained on `log(y)` and your predictions are systematically 10% low. Why?**
Because `exp(E[log y]) = ` the conditional **median**, not the conditional mean, and for a right-skewed (roughly lognormal) target the median lies below the mean. Formally, by Jensen's inequality `E[exp(Z)] ≥ exp(E[Z])`, and for lognormal errors the gap is exactly a factor of `exp(σ²/2)` where σ² is the residual variance in log space. With σ² ≈ 0.2 that is `exp(0.1) = 1.105`, i.e. a 10.5% under-prediction — matching your symptom. **Fixes:** (a) Duan's smearing estimator — multiply by `mean(exp(residuals))`; (b) the analytic correction `exp(μ̂ + σ̂²/2)` if you are willing to assume lognormality; (c) do not log-transform at all and instead use a **Gamma or Tweedie GLM / objective** with a log link, which models the mean directly on the original scale. Option (c) is usually the cleanest and is what I would recommend.

**Medium — Your overall MPE is 0% but the business complains about accuracy. What do you check?**
Segment the bias. Compute MPE by region, product category, price band, customer segment, and time period. Offsetting biases (+15% here, −15% there) cancel in the aggregate but are two distinct, real problems experienced by two distinct groups. Also check the magnitude metrics — MPE = 0 is compatible with enormous MAE. And check bias over time: a bias oscillating between +15% and −15% month to month averages to zero while being useless for planning.

**Hard — ★ How would you design bias monitoring for a production forecasting system?**
Layer it. (1) **Track total bias and MPE on a rolling window** (e.g. trailing 4 and 13 weeks) rather than since inception, so drift is visible. (2) Use a **tracking signal** — cumulative sum of residuals divided by MAE — with control limits (conventionally ±4 to ±6); breaching the limit fires an alert. This is a classic statistical process control approach and it detects a persistent small bias much faster than watching the level. (3) **Segment**: monitor bias by the dimensions along which the business acts (SKU class, region, channel), because aggregate bias hides offsetting segment problems. (4) **Distinguish level shift from trend**: a step change usually means a data-pipeline or definition change; a gradual drift usually means genuine distribution shift. (5) **Automate a recalibration path**: if bias exceeds a threshold and is stable, apply a bounded multiplicative correction while a retrain is scheduled — but log every correction, cap its magnitude, and never let it silently mask an upstream data break. (6) Also monitor **prevalence-adjacent inputs** (total volume, mix, promotion calendar) so you can attribute the bias to a cause rather than just correcting the symptom.

---

## 4.6 SCALED ERROR METRICS: RAE, RSE, RRSE

These three are the "divide by a baseline model's error" family. They are unitless, well-behaved near zero, and directly interpretable as "how much better than doing nothing?"

### 4.6.1 Relative Absolute Error (RAE)

**Definition.** Total absolute error divided by the total absolute error of a naive baseline (usually the mean of y).

**Formula**
```
             Σ | yᵢ − ŷᵢ |            MAE_model
RAE  =  ---------------------  =  ------------------
             Σ | yᵢ − ȳ  |           MAE_baseline
```
- **ȳ** = the mean of the actual values (some definitions use the median, which is the MAE-optimal constant — state which you use)
- **RAE = 1** → no better than predicting the mean
- **RAE < 1** → better than the baseline
- **RAE = 0** → perfect
- Range [0, ∞), unitless

**Manual example**
```
Σ|y − ŷ| = 360
Σ|y − ȳ| = Σ|y − 450| = 250+200+150+100+50+0+50+100+150+450 = 1,500

RAE = 360 / 1500 = 0.24
```
**RAE = 0.24** → the model's total absolute error is 24% of the naive baseline's; equivalently it **removes 76% of the error** a constant predictor would make. This is a far more meaningful statement than "MAE = 36."

**Python**
```python
import numpy as np
rae = np.abs(y - y_pred).sum() / np.abs(y - y.mean()).sum()          # 0.24
# Median-baseline variant (the MAE-optimal constant)
rae_med = np.abs(y - y_pred).sum() / np.abs(y - np.median(y)).sum()  # 0.24
```
(Both give 0.24 here because `Σ|y − 450| = Σ|y − 425| = 1500` for this particular data.)

**Interpretation:** `1 − RAE` is the fraction of the baseline's error removed. Ours: 76%.

**Use cases:** cross-dataset model comparison; WEKA and several AutoML tools report RAE by default; reporting "how much better than nothing" to stakeholders.

**Limitations:** depends on which baseline you choose, so it must be stated; the mean is a weak baseline for time series (a naive last-value forecast is much stronger, which is what MASE uses); a value slightly under 1 is not obviously bad-looking even though it means the model is nearly useless.

### 4.6.2 Relative Squared Error (RSE) and Root Relative Squared Error (RRSE)

**Formula**
```
            Σ ( yᵢ − ŷᵢ )²          MSE_model
RSE  =  ---------------------  =  --------------  =  1 − R²
            Σ ( yᵢ −  ȳ  )²          Var(y)

RRSE  =  √RSE  =  RMSE_model / σ(y)
```
- **RSE = 1 − R² exactly.** So RSE and R² are the same information, differently framed: RSE says "fraction of variance left unexplained," R² says "fraction explained."
- **RRSE** is the square-root version, directly interpretable as "RMSE as a multiple of the target's standard deviation."

**Manual example**
```
Σ(y − ŷ)² = 43,000
Σ(y − ȳ)² = 375,000

RSE  = 43,000 / 375,000 = 0.11467       -> and indeed R² = 1 − 0.11467 = 0.88533 ✓
RRSE = √0.11467 = 0.33863               -> RMSE 65.57 / σ 193.65 = 0.33863 ✓
```
**RSE = 0.1147, RRSE = 0.3386.**

**Python**
```python
import numpy as np
from sklearn.metrics import r2_score
rse  = ((y - y_pred)**2).sum() / ((y - y.mean())**2).sum()   # 0.11467
rrse = np.sqrt(rse)                                           # 0.33863
print(1 - rse, r2_score(y, y_pred))                           # 0.88533  0.88533  (identical)
```

**Interpretation:** RRSE < 1 means better than the mean; ours at 0.34 means our RMSE is a third of the natural variation in y.

**Use cases:** WEKA/AutoML reporting; unitless cross-dataset comparison; a more intuitive framing of R² for some audiences ("we cut the error to a third of the baseline" often lands better than "R² = 0.885").

**Limitations:** identical to R²'s (see Part 6) — the mean baseline is weak for time series, it is inflated by adding features, and it can be negative out of sample.

**Interview (Medium) — Relate RSE, RRSE, R², and RMSE.**
`RSE = 1 − R² = MSE/Var(y)`; `RRSE = √RSE = RMSE/σ(y)`. They are four views of one quantity: the model's squared error relative to the variance of the target. R² is the "explained" framing, RSE the "unexplained" framing, and RRSE puts it on the interpretable standard-deviation scale.

---

## 4.7 MEAN ABSOLUTE SCALED ERROR (MASE)

### 1. Definition
MAE divided by the mean absolute error of a **naive one-step forecast computed on the training data**.

### 2. Intuition
MASE was proposed by Hyndman and Koehler (2006) explicitly to fix MAPE, and it is the metric the academic forecasting community actually recommends. If you can name it and explain why it exists, you signal real familiarity with the field.

Its logic: instead of dividing by the actual value (which explodes near zero), divide by **how hard the series is to forecast**, measured by how well the dumbest possible forecast does. The naive forecast — "tomorrow equals today" — is the natural benchmark for a time series.

Read it directly:
- **MASE = 1** → your model is exactly as good as the naive forecast. You have added nothing.
- **MASE < 1** → better than naive.
- **MASE > 1** → **worse than naive**, which is more common in practice than teams like to admit.
- **MASE = 0.5** → half the error of the naive forecast.

That single interpretable anchor at 1.0 is what makes MASE so useful: it is the only percentage-free accuracy metric that tells you immediately whether the model is worth having.

### 3. Formula

**Non-seasonal:**
```
                MAE_model                       (1/n) Σᵢ | yᵢ − ŷᵢ |
MASE  =  ------------------------------  =  --------------------------------------
          MAE of in-sample naive forecast     ( 1/(m−1) ) Σₜ₌₂ᵐ | yₜ − yₜ₋₁ |
```
Symbol by symbol:
- **Numerator** = the MAE of your forecasts on the test set
- **Denominator** = the **in-sample** MAE of the naive forecast, i.e. the mean absolute first difference of the *training* series
- **m** = number of observations in the training series
- **yₜ − yₜ₋₁** = the naive forecast's error at time t (predicting today's value for tomorrow)

**Seasonal version** (use this whenever the series has a known period **s** — 12 for monthly, 7 for daily-with-weekly-pattern, 24 for hourly-with-daily-pattern):
```
                            (1/n) Σᵢ | yᵢ − ŷᵢ |
MASE_seasonal  =  -------------------------------------------
                    ( 1/(m−s) ) Σₜ₌ₛ₊₁ᵐ | yₜ − yₜ₋ₛ |
```
- The denominator now uses the **seasonal naive** forecast ("this month equals the same month last year"), which is a much stronger and fairer benchmark for seasonal data.

**Two critical implementation details that are frequently got wrong:**
1. **The denominator must be computed on the TRAINING data, not the test data.** Using the test set makes MASE incomparable across horizons and lets a lucky/unlucky test period distort it. This is the most common MASE bug.
2. **For cross-series aggregation, average the MASE values**, not the numerators and denominators separately. Each series gets its own denominator — that is the whole point.

Range [0, ∞), lower better, **unitless**.

### 4. Manual example

Because MASE needs a training series, here is a small time-series example.

**Training series (in-sample):** `100, 105, 102, 110, 108, 115`
```
Naive one-step errors (absolute first differences):
  |105 − 100| =  5
  |102 − 105| =  3
  |110 − 102| =  8
  |108 − 110| =  2
  |115 − 108| =  7
                ---
        Σ    =  25       over m − 1 = 5 differences

  In-sample naive MAE = 25 / 5 = 5.0
```

**Test set:** actual `120, 125, 122, 130`; model forecast `118, 122, 126, 124`
```
Absolute errors: |120−118| = 2
                 |125−122| = 3
                 |122−126| = 4
                 |130−124| = 6
                            ---
                      Σ  =  15   over n = 4

  Model MAE = 15 / 4 = 3.75
```

```
MASE = Model MAE / naive MAE = 3.75 / 5.0 = 0.75
```
**MASE = 0.75** → the model's average error is 75% of the naive forecast's, i.e. it **removes 25% of the naive error**. A real but modest improvement.

**For our house-price running example**, MASE in its time-series form does not apply (there is no temporal order), but the same idea works with a cross-sectional baseline — which is exactly what RAE is. RAE = 0.24 is the cross-sectional analogue.

### 5. Python
```python
import numpy as np

def mase(y_true, y_pred, y_train, seasonality=1):
    """
    MASE with the denominator computed on the TRAINING series (correct practice).
    seasonality=1 -> naive; seasonality=12 -> seasonal naive for monthly data.
    """
    y_true  = np.asarray(y_true,  float)
    y_pred  = np.asarray(y_pred,  float)
    y_train = np.asarray(y_train, float)

    naive_mae = np.mean(np.abs(y_train[seasonality:] - y_train[:-seasonality]))
    if naive_mae == 0:
        return np.nan            # a perfectly constant training series: MASE undefined
    return np.mean(np.abs(y_true - y_pred)) / naive_mae

train = np.array([100, 105, 102, 110, 108, 115], float)
test  = np.array([120, 125, 122, 130], float)
fcst  = np.array([118, 122, 126, 124], float)

mase(test, fcst, train)                  # 0.75
mase(test, fcst, train, seasonality=1)   # 0.75

# Aggregating across many series: average the MASE values
# overall = np.mean([mase(t, f, tr, s) for t, f, tr in zip(tests, fcsts, trains)])
```
Line-by-line:
- `y_train[seasonality:] - y_train[:-seasonality]` computes the s-step differences in one vectorised expression: `s=1` gives first differences (naive), `s=12` gives year-over-year differences (seasonal naive).
- The `naive_mae == 0` guard handles the only degenerate case: a perfectly flat training series, where the naive forecast is perfect and MASE is undefined.
- **`sktime`, `darts`, and `statsmodels`-adjacent forecasting libraries all provide MASE**; use theirs in production, but be sure you know whether their denominator uses training or test data.

### 6. Interpretation

| MASE | Interpretation |
|---|---|
| **0.0** | Perfect |
| **0.5** | Half the naive forecast's error — strong |
| **0.75** | 25% better than naive — our example, a real improvement |
| **0.9** | Marginally better than naive; question whether the model complexity is worth it |
| **1.0** | **Exactly as good as the naive forecast. The model has added nothing.** |
| **> 1.0** | **Worse than naive.** Ship the naive forecast instead. |
| **> 1.5** | Something is badly wrong — check for leakage in the wrong direction, a broken pipeline, or a mis-specified seasonality |

**The 1.0 anchor is the whole value proposition.** No other accuracy metric tells you, from a single number with no context, whether your model beats doing nothing. It is remarkably common for sophisticated models to score above 1.0 on hard series, and MASE makes that impossible to hide — which is precisely why it is uncomfortable and therefore useful.

### 7. Good vs bad values
| MASE | Verdict |
|---|---|
| < 0.5 | Excellent |
| 0.5 – 0.7 | Good |
| 0.7 – 0.9 | Moderate |
| 0.9 – 1.0 | Barely worth the complexity |
| ≥ 1.0 | Do not deploy; the naive forecast is better |

For **highly seasonal** data, always compare against the **seasonal** naive (s = 12, 7, 24 etc.). Beating the plain naive forecast on strongly seasonal data is trivial and meaningless; beating the seasonal naive is the real test. Reporting non-seasonal MASE on seasonal data is a way of flattering the model.

### 8. Business use cases
- **Time-series forecasting generally** — the academically recommended default, and the metric used in M-competition evaluations (as part of OWA in M4).
- **Intermittent and lumpy demand** — spare parts, slow-moving SKUs, anything with zeros. This is MASE's killer application: it is well-defined where MAPE is not.
- **Cross-series comparison and aggregation** — averaging MASE across thousands of SKUs is statistically sound because each series is normalised by its own difficulty.
- **Forecast-value-add (FVA) analysis** — the discipline of proving that each step of a forecasting process (statistical model, then analyst override, then management adjustment) actually improves on the previous step. MASE against a naive benchmark is the natural currency of FVA, and it frequently reveals that human overrides *worsen* the forecast.
- **Automated model selection across a large SKU portfolio** — pick the best model per series using MASE, and fall back to naive where MASE ≥ 1.
- **Vendor/tool evaluation** — a defensible, gaming-resistant comparison.
- **Academic publication** — expected in forecasting papers.

### 9. Advantages
- **Well-defined with zeros and near-zero values** — the decisive advantage over MAPE. The denominator is a single number per series, not per observation.
- **Symmetric** — no built-in bias toward over- or under-forecasting.
- **Unitless and comparable across series** of wildly different scale and volatility.
- **Interpretable against a meaningful benchmark**, with a hard anchor at 1.0.
- **Stable** — cannot be blown up by one small actual.
- **Aggregates coherently** across many series (just average the MASE values).
- Normalises for **series difficulty**, so a 0.7 MASE on a volatile series is properly recognised as a better achievement than 0.7 on a smooth one.
- Recommended in the forecasting literature and used in the M-competitions.

### 10. Limitations
- **Requires a training series** — cannot be computed from test data alone, and does not apply to cross-sectional regression. (Use RAE for cross-sectional problems.)
- **Undefined if the training series is perfectly constant** (naive MAE = 0). Rare but real for slow-moving items with a long flat run.
- **Depends on the benchmark choice** — naive vs seasonal naive changes the number substantially, so it must be stated. Non-seasonal MASE on seasonal data flatters the model.
- **Less familiar to business stakeholders** than MAPE, so it needs one sentence of explanation ("1.0 means no better than assuming next week equals this week").
- Not in scikit-learn (it is in `sktime`, `darts`, and `statsmodels`-adjacent packages).
- Sensitive to the training-period definition: a training window that happened to be unusually volatile inflates the denominator and flatters the model.
- Being an absolute-error-based metric, it is still **blind to bias** — report MPE alongside.

### 11. Common mistakes
1. **Computing the denominator on the test set instead of the training set.** The most frequent MASE bug; it makes values incomparable across horizons and test periods.
2. **Using non-seasonal MASE on strongly seasonal data**, which makes a mediocre model look good.
3. **Aggregating by summing numerators and denominators** across series rather than averaging the per-series MASE values. This destroys the per-series normalisation that is MASE's entire purpose.
4. Not handling the constant-training-series case.
5. Reporting MASE without stating the seasonality used.
6. Assuming MASE < 1 automatically means the model is good — it means it beats naive, which on a smooth trending series is a very low bar.
7. Reporting MASE alone, with no bias metric.

### 12. Interview questions

**Easy — What is MASE?** MAE divided by the in-sample naive forecast's MAE. A value of 1 means no better than naive.
**Easy — What does MASE = 1.2 mean?** Your model is 20% *worse* than assuming next period equals this period. Do not deploy it.

**Medium — ★ Why was MASE created, and what does it fix?**
It was proposed by Hyndman and Koehler to fix MAPE's four defects. (1) **Zeros:** MAPE divides by each actual and is undefined at zero; MASE divides by a single per-series constant. (2) **Asymmetry:** MAPE penalises over-forecasting more; MASE is symmetric. (3) **Instability near zero:** MAPE explodes; MASE does not. (4) **No benchmark:** MAPE gives no sense of whether the model is worth having; MASE's 1.0 anchor does. It also normalises for series difficulty, making cross-series averaging valid.

**Medium — ★ Why must the MASE denominator use training data?**
Because the denominator is meant to measure the *intrinsic difficulty of the series*, which should be a fixed property, not something that varies with which test window you happened to choose. Using the test set makes MASE values incomparable across horizons and across evaluation periods, and it introduces a subtle dependence between the numerator and denominator (both computed on the same data) that can flatter or penalise the model arbitrarily.

**Medium — When would you use seasonal MASE, and why does it matter?**
Whenever the series has a known period — monthly retail data (s = 12), daily data with a weekly cycle (s = 7), hourly data with a daily cycle (s = 24). It matters because the plain naive forecast is a terrible benchmark for seasonal data: predicting "today equals yesterday" for December 25th retail sales is absurdly bad, so almost any model beats it and MASE looks flattering. The seasonal naive ("this December equals last December") is a genuinely competitive benchmark and beating it is meaningful.

**Hard — ★ How do you evaluate 10,000 SKU forecasts with one number?**
Compute **MASE per SKU with the appropriate seasonality**, then aggregate — but aggregate thoughtfully:
- **Simple mean of MASE** treats every SKU equally. Good for "does our method work across the portfolio?"
- **Volume- or revenue-weighted mean of MASE** reflects business impact. Good for "what is this worth?"
- **Median MASE** is robust and reports the typical SKU.
- **The fraction of SKUs with MASE ≥ 1** is arguably the most actionable single number: those SKUs should be served by the naive forecast, and that fraction is a direct measure of where the model adds nothing.
Also report the **distribution** (a histogram of MASE across SKUs) rather than only a summary, segment by volume band and intermittency class, and report **WAPE** alongside for the value-weighted view plus **total bias** because none of these sees direction. Finally, guard against averaging pathologies: MASE can be very large for a few near-constant series, so trim or use the median for the headline and report the mean separately.

**Hard — What is Forecast Value Add and how does MASE support it?**
FVA measures whether each successive step in a forecasting process improves accuracy over the previous step, using a naive forecast as the ultimate floor. You compute MASE (or MAE) for: the naive forecast, the statistical model, the model after analyst override, and the final consensus forecast after management adjustment. Each step's FVA is its improvement over the prior step. MASE is the natural currency because it is already normalised against naive and is comparable across the portfolio. The uncomfortable and well-documented finding in practice is that **downstream human adjustments frequently have negative FVA** — they add work and reduce accuracy — and MASE-based FVA analysis is how organisations discover that.

---

## 4.8 THEIL'S U STATISTICS

### 1. Definition
Two related statistics comparing a forecast's error to a naive benchmark's error. Confusingly, both are called "Theil's U."

- **U1 (Theil's inequality coefficient):** a normalised RMSE bounded in [0,1]. Rarely used today; hard to interpret.
- **U2:** the ratio of the model's RMSE to the naive forecast's RMSE. **This is the useful one** and is what people almost always mean.

### 2. Intuition
U2 is **the RMSE analogue of MASE**: "is my model better than the naive forecast, measured in squared-error terms?" Same 1.0 anchor, same interpretation, but tail-weighted rather than linear.

### 3. Formula
```
             RMSE_model            √( (1/n) Σ (yₜ − ŷₜ)² )
U2  =  --------------------  =  --------------------------------
             RMSE_naive          √( (1/n) Σ (yₜ − yₜ₋₁)² )
```
- **yₜ₋₁** = the naive (persistence) forecast for time t
- **U2 < 1** → better than naive; **U2 = 1** → equal to naive; **U2 > 1** → worse than naive
- Range [0, ∞), unitless

The original **U1** form is `U1 = √(Σ(yₜ−ŷₜ)²) / (√(Σyₜ²) + √(Σŷₜ²))`, bounded [0,1], but it has no clean interpretation and depends on the level of the series. Prefer U2, and say which you mean.

### 4. Manual example
Using the same time series as MASE. Training ends at 115, so the naive forecast for the test period is the previous actual each time.
```
Test actuals:      120, 125, 122, 130
Model forecasts:   118, 122, 126, 124
Naive forecasts:   115, 120, 125, 122       (previous actual)

Model errors:  2,  3, −4,  6   ->  squares  4,  9, 16, 36  -> Σ = 65
Naive errors:  5,  5, −3,  8   ->  squares 25, 25,  9, 64  -> Σ = 123

RMSE_model = √(65/4)  = √16.25 = 4.031
RMSE_naive = √(123/4) = √30.75 = 5.545

U2 = 4.031 / 5.545 = 0.727
```
**Theil's U2 = 0.727** → the model's RMSE is 73% of the naive forecast's. Compare with **MASE = 0.75** on the same data: they agree closely here because the errors are fairly uniform. When they *disagree*, the difference is informative: **U2 < MASE means the model is relatively better at avoiding large errors; U2 > MASE means it has a worse tail than its average suggests.**

### 5. Python
```python
import numpy as np

def theil_u2(y_true, y_pred, y_naive):
    y_true, y_pred, y_naive = (np.asarray(a, float) for a in (y_true, y_pred, y_naive))
    rmse_m = np.sqrt(np.mean((y_true - y_pred) ** 2))
    rmse_n = np.sqrt(np.mean((y_true - y_naive) ** 2))
    return np.nan if rmse_n == 0 else rmse_m / rmse_n

# Build the naive (persistence) forecast: previous actual, seeded from the last training value
last_train = 115.0
test  = np.array([120, 125, 122, 130], float)
naive = np.concatenate(([last_train], test[:-1]))     # [115, 120, 125, 122]
fcst  = np.array([118, 122, 126, 124], float)

theil_u2(test, fcst, naive)      # 0.7269
```
- Note the construction of `naive`: it must be seeded with the **last training observation**, not with the first test observation, or you leak future information.

### 6. Interpretation
Identical structure to MASE.

| U2 | Meaning |
|---|---|
| < 0.5 | Much better than naive |
| 0.727 | Our example — a solid improvement |
| 0.9 | Marginal |
| 1.0 | Equal to naive |
| > 1.0 | Worse than naive |

### 7–8. Good values / use cases
Same as MASE: < 0.7 good, 0.7–0.9 moderate, ≥ 1.0 do not deploy. Used in **econometrics and macroeconomic forecasting** (where Theil's work originated), **financial time-series forecasting**, and any setting where RMSE rather than MAE is the loss of record.

### 9. Advantages
- Clear 1.0 benchmark against a naive forecast.
- Unitless and cross-series comparable.
- Tail-weighted, so it matches convex cost structures where MASE would not.
- Established in econometrics.

### 10. Limitations
- **Two incompatible definitions share the name.** Always state whether you mean U1 or U2.
- Inherits RMSE's outlier sensitivity in both numerator and denominator.
- Requires a naive benchmark, so it needs the series' temporal structure.
- Less standard than MASE in modern forecasting practice.
- Undefined if the naive forecast is perfect.
- Blind to bias.

### 11. Common mistakes
1. Not specifying U1 vs U2.
2. Seeding the naive forecast from the test set (look-ahead leakage).
3. Comparing U2 values computed against different benchmarks (naive vs seasonal naive vs drift).
4. Reporting U2 alongside MASE as independent evidence — they measure the same thing under different loss functions.

### 12. Interview questions
**Easy — What does Theil's U2 = 0.8 mean?** The model's RMSE is 80% of the naive forecast's RMSE.
**Medium — MASE vs Theil's U2?** Both compare to a naive benchmark with a 1.0 anchor. MASE uses MAE (linear, robust); U2 uses RMSE (quadratic, tail-weighted). Report the one matching your cost function; if they disagree substantially, the model's tail behaviour differs from its typical behaviour, which is itself worth investigating.
**Hard — Why do modern forecasting papers prefer MASE to Theil's U?**
Three reasons. MASE has one unambiguous definition while "Theil's U" refers to two different statistics. MASE's denominator is computed **in-sample on the training data**, making it a stable property of the series rather than something that shifts with the test window, whereas U2 is conventionally computed with both terms on the test set. And MASE is based on MAE, which is robust and well-defined for the intermittent series that dominate real forecasting portfolios, whereas U2 inherits RMSE's outlier sensitivity in both numerator and denominator, so a single spike can make a good model look bad.

---

# PART 5 — Log-Based Error Metrics

## 5.0 Why take logs?

Log-based metrics exist to solve one specific, extremely common problem: **the target is positive, right-skewed, and spans orders of magnitude, and you care about relative rather than absolute error.**

House prices from $80k to $8M. Sales volumes from 1 to 100,000. Page views, incomes, claim amounts, city populations, gene expression levels. In every case:
- **RMSE** is dominated by the largest values and effectively ignores the small ones.
- **MAPE** works but explodes near zero and is asymmetric.
- **Logs** compress the scale so that a *ratio* becomes a *difference*, which is exactly what you want.

**The key mathematical fact:**
```
log(y) − log(ŷ)  =  log( y / ŷ )
```
**A difference of logs IS a log ratio.** So squaring or averaging log differences is measuring *relative* error, automatically, with no division by a possibly-zero actual. That is the whole trick.

**Useful approximation for interpretation:** for small errors,
```
log(y/ŷ) ≈ (y − ŷ)/ŷ  =  the relative error
```
so an RMSLE of 0.10 corresponds to roughly a **10% typical relative error** (more precisely `exp(0.10) − 1 = 10.5%`).

**The trade-off:** logs are **asymmetric by construction**, and this is a deliberate design property, not a defect — but you must know which direction it favours (see 5.1).

---

## 5.1 ROOT MEAN SQUARED LOGARITHMIC ERROR (RMSLE)

### 1. Definition
The RMSE computed on `log(1 + y)` instead of on y.

### 2. Intuition
RMSLE asks: **"how far off am I, in ratio terms, with big ratio-misses penalised quadratically?"**

It has three defining behaviours, and all three are the reason it is the go-to metric for skewed positive targets:

**(a) It measures relative, not absolute, error.** Predicting 100 when the truth is 110 and predicting 1,000 when the truth is 1,100 produce **almost identical RMSLE contributions**, because both are 10% off. RMSE would call the second error ten times worse.

**(b) It penalises under-prediction more than over-prediction.** This is asymmetric on purpose and it is the property people most often get backwards.
```
Actual y = 1000:
  Under-predict ŷ = 500   ->  |log(1001) − log(501)|  = |6.909 − 6.217| = 0.692
  Over-predict  ŷ = 2000  ->  |log(1001) − log(2001)| = |6.909 − 7.602| = 0.693
```
Those look symmetric — because 500 and 2000 are symmetric *ratios* (÷2 and ×2). The asymmetry appears when you compare symmetric *absolute* errors:
```
Actual y = 1000, absolute error of 500 either way:
  Under-predict ŷ =  500  ->  log ratio = log(1001/501)  = 0.692
  Over-predict  ŷ = 1500  ->  log ratio = log(1001/1501) = −0.405
```
**Same 500-unit error, but under-prediction is penalised 71% more heavily.** So **RMSLE is symmetric in ratios and asymmetric in absolute terms**, favouring over-prediction. If under-forecasting is the expensive failure (stockouts, under-reserving, under-provisioning capacity), that asymmetry is exactly what you want.

**(c) It is robust to large outliers** — because the log compresses the top of the scale, a single enormous actual cannot dominate the way it does in RMSE.

It is the standard metric for a large fraction of Kaggle regression competitions (house prices, sales, demand) precisely because those targets are all positive and right-skewed.

### 3. Formula
```
                  ______________________________________________
                 /   1    n
RMSLE  =        /  ---  ×  Σ  [ ln(1 + yᵢ) − ln(1 + ŷᵢ) ]²
              \/    n     i=1
```
Symbol by symbol:
- **ln** = natural logarithm. (Some implementations use log base 10; sklearn uses natural log. The choice rescales the metric by a constant factor and does not change model ranking, but changes the number — state which you use.)
- **1 +** = the `log1p` shift. It exists so that **y = 0 is allowed**: `ln(1+0) = ln(1) = 0`. Without it, zeros would give `ln(0) = −∞`.
- **[ ... ]²** = squared log-ratio, so large ratio errors are penalised quadratically
- Range **[0, ∞)**, lower better, **approximately unitless** (a log-ratio)
- **Requires `y ≥ 0` and `ŷ ≥ 0`.** Any negative prediction gives `ln` of a negative number → `nan`. This is the single biggest practical trap: models routinely predict small negatives, and you must clip.

**MSLE** is the same thing without the square root: `MSLE = RMSLE²`. sklearn provides `mean_squared_log_error`; take the square root yourself, or use `root_mean_squared_log_error` in newer versions.

**The identity that explains everything about RMSLE:**
```
                 ______________________________
                /   1        (  1 + yᵢ  )²
RMSLE  =       /  ---  ×  Σ [ ln --------- ]
             \/    n           (  1 + ŷᵢ  )
```
It is the root-mean-square of the log ratios. Everything about its behaviour follows from that.

### 4. Manual example
```
i     y      ŷ     ln(1+y)     ln(1+ŷ)     difference    squared
1    200    220    5.303305    5.398163    −0.094858    0.0089981
2    250    240    5.525453    5.484797    +0.040656    0.0016529
3    300    310    5.706930    5.739793    −0.032863    0.0010800
4    350    330    5.860786    5.802118    +0.058668    0.0034419
5    400    420    5.993961    6.042633    −0.048672    0.0023690
6    450    430    6.111467    6.066108    +0.045359    0.0020574
7    500    520    6.216606    6.255750    −0.039144    0.0015323
8    550    530    6.311735    6.274762    +0.036973    0.0013670
9    600    620    6.398595    6.431331    −0.032736    0.0010717
10   900    700    6.803505    6.552508    +0.250997    0.0629995
                                                       -----------
                                              Σ    =    0.0865579

Step 1 — MSLE  = 0.0865579 / 10 = 0.00865579
Step 2 — RMSLE = √0.00865579 = 0.093037
```
**RMSLE = 0.0930** (sklearn: 0.09304).

**Interpretation via the exponential:** `exp(0.0930) − 1 = 9.75%`, so **the typical relative error is about 9.75%**, tail-weighted.

**Now compare RMSLE to RMSE on the same data — this is the heart of Part 5:**
```
RMSE  = 65.57      dominated by house 10 (contributes 93% of SSE)
RMSLE = 0.0930     house 10 contributes 0.0630/0.0866 = 73% of MSLE
```
House 10 still dominates, but **much less** — 73% instead of 93%. And critically, the *relative* contributions of the other nine houses are now sensible: house 1 (a 10% error on a cheap house) contributes 0.0090, which is more than house 9 (a 3.3% error on an expensive house) at 0.0011. Under RMSE both contributed exactly 400 — identical — because both had a $20k absolute error. **RMSLE correctly recognises that a $20k miss on a $200k house is three times worse than a $20k miss on a $600k house.** That single sentence is why RMSLE exists.

### 5. Python
```python
import numpy as np
from sklearn.metrics import mean_squared_log_error, root_mean_squared_log_error

mean_squared_log_error(y, y_pred)                    # 0.0086558   (MSLE)
np.sqrt(mean_squared_log_error(y, y_pred))           # 0.0930365   (RMSLE)
root_mean_squared_log_error(y, y_pred)               # 0.0930365   (sklearn >= 1.4)

# By hand
np.sqrt(np.mean((np.log1p(y) - np.log1p(y_pred)) ** 2))   # 0.0930365

# CRITICAL: clip negative predictions or you get nan
y_pred_safe = np.clip(y_pred, 0, None)
root_mean_squared_log_error(y, y_pred_safe)

# Interpretation
rmsle = root_mean_squared_log_error(y, y_pred)
print(f"RMSLE {rmsle:.4f}  ->  typical relative error ~ {np.expm1(rmsle):.2%}")
# RMSLE 0.0930  ->  typical relative error ~ 9.75%

# The standard modelling pattern: train in log space, predict, invert
# model.fit(X_train, np.log1p(y_train))          # now MSE in log space == MSLE
# preds = np.expm1(model.predict(X_test))        # back to the original scale
# NOTE: expm1(mean of logs) gives the conditional MEDIAN, not the mean.
#       If you need the mean/total to be right, apply a smearing correction (see 4.5).

# In model selection
# GridSearchCV(model, params, scoring='neg_mean_squared_log_error', cv=5)
```
Line-by-line:
- **`np.log1p(x)` computes `ln(1+x)` with better numerical precision** for small x than `np.log(1+x)`. Use it. Its inverse is `np.expm1`.
- **`np.clip(y_pred, 0, None)` is mandatory in practice.** Linear models, and even GBMs on some folds, will predict small negatives, and `log1p` of a value below −1 is `nan`. sklearn raises a `ValueError` on negatives, which at least fails loudly.
- **The train-in-log-space pattern is the more common workflow than using RMSLE as a metric.** Minimising MSE on `log1p(y)` *is* minimising MSLE, so you get a well-behaved smooth objective and every library supports it. But remember the back-transformation bias (Part 4.5).

### 6. Interpretation

Convert to a relative error via `exp(RMSLE) − 1`:

| RMSLE | ≈ Typical relative error | Verdict |
|---|---|---|
| 0.05 | 5.1% | Excellent |
| 0.093 | **9.8%** | **Good — our example** |
| 0.15 | 16.2% | Moderate |
| 0.30 | 35.0% | Weak |
| 0.50 | 64.9% | Poor |
| 1.00 | 172% | The model is roughly a factor of 2.7 out |

**Kaggle context** (useful for calibrating expectations): the classic House Prices competition has winning RMSLE around **0.11–0.12**, with 0.13–0.15 being a solid score. Sales/demand competitions with RMSLE targets typically land in 0.4–0.6 because those series are far noisier.

### 7. Good vs bad values
| RMSLE | Band |
|---|---|
| < 0.10 | Excellent |
| 0.10 – 0.20 | Good |
| 0.20 – 0.40 | Moderate |
| > 0.40 | Weak |

These bands are more portable than RMSE's because RMSLE is approximately unitless — one of its practical advantages.

### 8. Business use cases
- **House price and real-estate valuation** — the canonical use. Prices span orders of magnitude, and a 10% error is what matters at every price point.
- **Retail sales and demand forecasting** — positive, right-skewed, spanning SKUs from 1 to 100,000 units.
- **Kaggle regression competitions** — one of the two most common leaderboard metrics for positive targets.
- **Web traffic, page-view, and app-install forecasting** — heavily right-skewed with a long tail.
- **Insurance claim severity** — positive and skewed, with the added benefit that RMSLE's under-prediction penalty aligns with the need for adequate reserves.
- **Count-adjacent targets** (with the log1p handling zeros) — though a Poisson or Tweedie objective is usually better for true counts.
- **Any target where a doubling is a doubling regardless of the starting level:** population, income, biological measurements, energy consumption across building sizes.
- **When under-prediction is more costly than over-prediction** — the built-in asymmetry does useful work.

### 9. Advantages
- **Measures relative error**, so it is meaningful across orders of magnitude and does not let the largest values dominate.
- **Robust to large outliers** compared to RMSE — the log compresses the tail.
- **Handles zeros** thanks to the `log1p` shift, unlike MAPE.
- **Approximately unitless**, so values are comparable across datasets and the bands above are portable.
- **Penalises under-prediction more heavily**, which matches many real cost structures (stockouts, under-reserving).
- **Smooth and differentiable**, so it works directly as a training objective (equivalently: MSE on `log1p(y)`), unlike MAPE which has awkward gradients.
- The train-in-log-space implementation is trivial and works with every library.

### 10. Limitations
- **Requires non-negative y and ŷ.** Negative predictions produce `nan` and must be clipped. This bites constantly in practice.
- **Cannot be used for targets that go negative** — profit, temperature, returns, changes. A hard restriction.
- **The asymmetry is a defect if your costs are symmetric.** It will systematically bias the model toward over-prediction, and if over-stocking is your expensive failure mode, RMSLE is actively wrong.
- **Not directly interpretable** — "RMSLE = 0.093" means nothing to a stakeholder without the `exp() − 1` translation. Always report the translated percentage.
- **The `+1` shift distorts small values.** For targets in the range 0–5, `ln(1+y)` changes the relative spacing substantially: `ln(1+0)=0`, `ln(1+1)=0.69`, `ln(1+2)=1.10`. So RMSLE is not a clean relative-error measure for small counts. Some practitioners use `log(y + c)` with a tuned constant c, which is defensible but must be documented.
- **Back-transformation bias:** training on `log1p(y)` and predicting `expm1(·)` yields the conditional median, so the aggregate is biased low. Requires a smearing correction if totals matter.
- Under-weights errors on the largest values, which is a problem if your revenue is concentrated there — the exact opposite concern to RMSE's.

### 11. Common mistakes
1. **Not clipping negative predictions**, producing `nan` and a mysteriously failing pipeline.
2. **Getting the asymmetry direction backwards.** RMSLE penalises **under**-prediction more (in absolute terms). Many people state the opposite.
3. **Reporting the raw RMSLE without translating it** into an approximate percentage.
4. **Using RMSLE for targets that can be negative.**
5. **Using RMSLE for small counts (0–10)** where the `+1` shift dominates. Use a Poisson objective instead.
6. **Forgetting the back-transformation bias** after training in log space, then being surprised the totals are low.
7. Comparing an RMSLE computed with natural log to one computed with log₁₀ (a factor of 2.303 apart).
8. Assuming RMSLE robustness means outliers can be ignored — it *reduces* their influence, it does not eliminate it (73% of our MSLE still comes from one house).

### 12. Interview questions

**Easy — What is RMSLE?** RMSE computed on `log(1+y)` instead of y. It measures relative rather than absolute error.

**Easy — Why the `+1`?** So that `y = 0` is allowed: `ln(1+0) = 0` instead of `ln(0) = −∞`.

**Medium — ★ Why does RMSLE measure relative error?**
Because `ln(1+y) − ln(1+ŷ) = ln((1+y)/(1+ŷ))`, a **log ratio**. A ratio is inherently relative, so an error of 10% contributes the same amount whether the actual is 100 or 100,000. RMSE, working on the raw difference, would call the second error a thousand times larger.

**Medium — ★ Is RMSLE symmetric? Explain carefully.**
It depends on what you hold fixed. It is **symmetric in ratios** — halving and doubling the prediction incur nearly the same penalty. It is **asymmetric in absolute terms** — for a fixed absolute error, under-prediction is penalised more. Example with actual 1000 and a 500-unit error: predicting 500 gives a log ratio of 0.692, predicting 1500 gives 0.405. So under-prediction costs 71% more, meaning a model tuned on RMSLE will lean toward over-prediction. Whether that is desirable is a business question.

**Medium — When would you use RMSLE over RMSE?**
When the target is positive, right-skewed, and spans orders of magnitude, and when relative error is what the business cares about. House prices, sales volumes, traffic, claim amounts. Also when under-prediction is the costlier direction, since RMSLE penalises it more. Not when the target can be negative, not when the target is a small count, and not when your costs are symmetric.

**Medium — What is the relationship between RMSLE and training on `log1p(y)` with MSE?**
They are the same objective. Minimising MSE on `log1p`-transformed targets is exactly minimising MSLE, and RMSLE is its square root — a monotone transform, so the optimal model is identical. This is why the standard implementation is to transform the target rather than to write a custom loss.

**Hard — ★ You train on `log1p(y)`, predict with `expm1`, and your total predicted sales are 8% below the total actual. Why, and how do you fix it?**
Because `expm1(E[log1p(y)])` recovers the conditional **median**, not the conditional mean, and for a right-skewed target the median is below the mean. Formally, by Jensen's inequality `E[expm1(Z)] ≥ expm1(E[Z])`; for approximately lognormal residuals the gap is a factor of `exp(σ²/2)` with σ² the residual variance in log space — σ² ≈ 0.154 gives exactly the 8% you observe.

**Fixes, in order of preference:**
(1) **Model the mean directly on the original scale** with a **Gamma or Tweedie objective and a log link** (e.g. `objective='reg:gamma'` or `'reg:tweedie'` in XGBoost, `family=Tweedie` in a GLM). This gets relative-error behaviour *and* an unbiased mean, and needs no correction.
(2) **Duan's smearing estimator:** multiply your back-transformed predictions by `mean(exp(residuals_in_log_space))`, estimated on a validation set. Non-parametric and robust.
(3) **Analytic lognormal correction:** predict `exp(μ̂ + σ̂²/2)`. Simple but assumes lognormality.
(4) **A final calibration step:** fit a one-parameter multiplicative adjustment on held-out data so the totals reconcile.
Note that (2)–(4) will *worsen* your RMSLE while *improving* your bias and your MAE/RMSE — which is the correct trade if the business needs totals to reconcile. **This tension is the point: you cannot simultaneously optimise relative error and aggregate unbiasedness on a skewed target.** State which one the business needs.

**Hard — Why is RMSLE inappropriate for small counts?**
Because the `+1` shift is large relative to the values. For y in 0–5, `log1p` maps `{0,1,2,3,4,5}` to `{0, 0.69, 1.10, 1.39, 1.61, 1.79}` — the spacing between 0 and 1 is 0.69 while between 4 and 5 it is 0.18, so the metric weights the low end enormously and is no longer a clean relative-error measure. For genuine count data use a **Poisson deviance** objective (or negative binomial if over-dispersed), which is the correct likelihood for counts, handles zeros natively, and gives an unbiased mean.

---

## 5.2 MEAN SQUARED LOGARITHMIC ERROR (MSLE)

**Definition.** RMSLE without the square root: `MSLE = (1/n) Σ [ln(1+y) − ln(1+ŷ)]²`.

**Our example: MSLE = 0.008656.**

**Relationship:** `RMSLE = √MSLE`. Monotonically related, so **the same model minimises both** — MSLE is the training objective, RMSLE the reported metric, exactly parallel to MSE and RMSE.

**Python**
```python
from sklearn.metrics import mean_squared_log_error
mean_squared_log_error(y, y_pred)      # 0.0086558
# scoring='neg_mean_squared_log_error'
```

**When you see it:** as the `scoring` string in sklearn, and as `objective='reg:squaredlogerror'` in XGBoost. Report RMSLE, not MSLE, for the same reason you report RMSE rather than MSE — the square root restores an interpretable scale.

**Interview (Easy) — MSLE vs RMSLE?** MSLE is the mean squared log error; RMSLE is its square root. Same ranking, RMSLE is interpretable.

---

## 5.3 LOG ACCURACY RATIO AND MEDIAN SYMMETRIC ACCURACY (MdSA)

### 1. Definition
Metrics built directly on the **accuracy ratio** `Q = ŷ/y`, whose log is the natural symmetric measure of relative error.

### 2. Intuition
The forecasting and space-weather literature (Morley et al., 2018) argues that if you care about relative error, you should measure it on the **log accuracy ratio** `ln(ŷ/y)` rather than patching MAPE. The reasons:
- `ln(ŷ/y)` is **exactly symmetric**: predicting double gives `+0.693`, predicting half gives `−0.693`. MAPE gives 100% and 50%. sMAPE gives 40% and 66.7%. Only the log ratio is genuinely symmetric.
- It is **unbounded in both directions**, so there is no artificial cap favouring one direction.
- Exponentiating a robust average of `|ln(ŷ/y)|` returns a directly interpretable percentage.

**MdSA (Median Symmetric Accuracy)** is the recommended robust summary:
```
MdSA  =  100 × ( exp( median | ln(ŷᵢ / yᵢ) | ) − 1 )
```
Read as: **"the typical prediction is within MdSA% of the truth, symmetrically."**

A companion bias measure, **Symmetric Signed Percentage Bias (SSPB)**, keeps the sign:
```
SSPB  =  100 × sign(M) × ( exp|M| − 1 ),      M = median( ln(ŷᵢ / yᵢ) )
```

### 3. Formula summary
```
Accuracy ratio        Qᵢ = ŷᵢ / yᵢ
Log accuracy ratio    Lᵢ = ln(Qᵢ) = ln(ŷᵢ) − ln(yᵢ)
MdSA (%)              = 100 × ( exp( median|Lᵢ| ) − 1 )
SSPB (%)              = 100 × sign(median Lᵢ) × ( exp|median Lᵢ| − 1 )
```
- Requires **strictly positive** y and ŷ (no zeros — there is no `+1` shift here).
- Both are unitless percentages, symmetric, robust, and unbounded.

### 4. Manual example
```
i     y     ŷ      Q = ŷ/y     L = ln(Q)      |L|
1    200   220     1.10000     +0.095310     0.095310
2    250   240     0.96000     −0.040822     0.040822
3    300   310     1.03333     +0.032790     0.032790
4    350   330     0.94286     −0.058841     0.058841
5    400   420     1.05000     +0.048790     0.048790
6    450   430     0.95556     −0.045462     0.045462
7    500   520     1.04000     +0.039221     0.039221
8    550   530     0.96364     −0.037041     0.037041
9    600   620     1.03333     +0.032790     0.032790
10   900   700     0.77778     −0.251314     0.251314

median |L| = average of the 5th and 6th smallest of |L|
sorted |L|: 0.032790, 0.032790, 0.037041, 0.039221, 0.040822,
            0.045462, 0.048790, 0.058841, 0.095310, 0.251314
                                  ^5th      ^6th
median|L| = (0.040822 + 0.045462)/2 = 0.043142

MdSA = 100 × (exp(0.043142) − 1) = 100 × 0.044086 = 4.41%
```
**MdSA = 4.41%** — "the typical prediction is within 4.4% of the truth."

Compare with **MdAPE = 4.22%**. They agree closely, as they should for small errors, but MdSA is the symmetric version and does not have MAPE's directional bias.

```
Sorted SIGNED values of L:
 −0.251314, −0.058841, −0.045462, −0.040822, −0.037041, +0.032790,
                                     ^5th        ^6th
median L = (−0.037041 + 0.032790)/2 = −0.0021257
SSPB = 100 × sign(−0.0021257) × (exp(0.0021257) − 1) = −0.213%
```
**SSPB = −0.21%** → a very slight tendency to **over**-predict at the median (recall the median residual was exactly 0 and the mean was +18 — SSPB agrees with the median view, not the mean view, exactly as a robust metric should).

### 5. Python
```python
import numpy as np

def mdsa(y_true, y_pred):
    """Median Symmetric Accuracy (%). Requires strictly positive values."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    m = (y_true > 0) & (y_pred > 0)
    L = np.log(y_pred[m] / y_true[m])
    return (np.exp(np.median(np.abs(L))) - 1) * 100

def sspb(y_true, y_pred):
    """Symmetric Signed Percentage Bias (%). Positive => over-prediction."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    m = (y_true > 0) & (y_pred > 0)
    M = np.median(np.log(y_pred[m] / y_true[m]))
    return np.sign(M) * (np.exp(abs(M)) - 1) * 100

mdsa(y, y_pred)      # 4.409
sspb(y, y_pred)      # -0.213
```

### 6. Interpretation
MdSA reads exactly like MdAPE ("typical prediction within X%") but with genuine symmetry. SSPB reads as a signed percentage bias, positive meaning over-prediction.

### 7–8. Good values / use cases
Same bands as MdAPE (< 5% excellent, 5–10% good, 10–20% moderate). Used in:
- **Space weather and geophysical forecasting** — where the metric was formalised.
- **Astronomy and physical-sciences model validation.**
- **Any strictly-positive target where you want a defensibly symmetric relative-error measure** and want to avoid MAPE's known biases.
- **Publication contexts** where a reviewer might object to MAPE.

### 9. Advantages
- **Genuinely symmetric** — the only percentage-style family with this property.
- **Robust** (median-based).
- **Unbounded in both directions**, so no artificial cap creates a directional preference.
- Directly interpretable as a percentage after exponentiating.
- Pairs with SSPB for a matched, equally robust bias measure.

### 10. Limitations
- **Requires strictly positive y and ŷ** — no zeros at all, and no `+1` rescue.
- **Unfamiliar** outside a few scientific communities; you will have to define it.
- Not in any mainstream ML library.
- Median-based, so it hides the tail (report high quantiles of `|L|` alongside).
- The exponentiation step confuses people the first time they see it.

### 11. Common mistakes
1. Applying it to data containing zeros.
2. Reporting `median|L|` (the log-space value) instead of the exponentiated percentage.
3. Getting SSPB's sign convention backwards — here positive means over-prediction, because the ratio is `ŷ/y`. Note this is the **opposite** convention to MPE (which uses `y − ŷ`, so positive means under-prediction). State it.
4. Reporting it alone without a tail measure.

### 12. Interview questions
**Medium — Why is `ln(ŷ/y)` the natural symmetric measure of relative error?** Because multiplicative errors become additive under the log: predicting double gives `+ln 2` and predicting half gives `−ln 2`, exactly equal in magnitude and opposite in sign. Every division-based percentage metric (MAPE, sMAPE) breaks this symmetry because the denominator differs between the two cases.
**Hard — Argue for MdSA over MAPE in a paper.** MAPE is asymmetric (bounded at 100% for under-prediction, unbounded for over-prediction), undefined at zero, unstable near zero, and its minimiser is an obscure weighted median — so it systematically biases models and its values are not comparable across studies with different target distributions. MdSA is exactly symmetric, robust to outliers via the median, unbounded in both directions, and exponentiates to a directly interpretable percentage. The cost is that it requires strictly positive data and is less familiar. If zeros are present, MASE or WAPE is the better choice; if all values are positive and you want a symmetric percentage, MdSA is the principled option, reported with SSPB for bias and a high quantile of the log ratio for tail behaviour.

## 5.4 Log-family summary on the running example

| Metric | Value | Reads as |
|---|---|---|
| MSLE | 0.008656 | (training objective; not for reporting) |
| **RMSLE** | **0.0930** | ≈ 9.8% typical relative error, tail-weighted |
| MdSA | 4.41% | Typical prediction within 4.4%, symmetric |
| SSPB | −0.21% | Very slight over-prediction at the median |
| MdAPE (for comparison) | 4.22% | Typical prediction within 4.2% |
| MAPE (for comparison) | 6.57% | Mean percentage miss |

**Reading the set:** the median-based measures (MdSA 4.4%, MdAPE 4.2%) agree and describe the typical case. The mean-based measures (RMSLE 9.8%, MAPE 6.6%) are higher because they absorb the one bad house. The gap between the two groups *is* the tail. Reporting one from each group, plus a signed bias, is a complete relative-error picture.

---

# PART 6 — Goodness of Fit

## 6.0 A different question

Everything in Parts 2–5 answers "**how big are my errors?**" This Part answers a different question: "**how much of the target's variation did my model actually explain?**"

The distinction matters. MAE = 36 tells you the size of the miss but nothing about whether the model is doing anything clever. If the target barely varies, an MAE of 36 might be terrible; if it varies wildly, it might be superb. Goodness-of-fit metrics build the comparison in.

They are all built on the same idea: **compare your model's error to the error of a trivial baseline.** That makes them unitless, comparable, and anchored — but it also means every one of them inherits the strengths and weaknesses of the baseline chosen.

---

## 6.1 R² (COEFFICIENT OF DETERMINATION)

### 1. Definition
The proportion of the variance in the target that is explained by the model, relative to a baseline that always predicts the mean.

### 2. Intuition
R² answers: **"how much better than just predicting the average am I?"**

- **R² = 1** → perfect predictions.
- **R² = 0** → exactly as good as predicting `ȳ` for everything. The model has added nothing.
- **R² < 0** → **worse than predicting the mean.** Entirely possible out-of-sample, and a genuinely useful red flag.

That anchoring at 0 is R²'s great virtue: unlike MAE or RMSE, it comes with a built-in "is this model worth having?" answer, in the same way MASE does for forecasting.

It is by far the most reported regression metric in academic papers and business dashboards, and also the most misunderstood — mainly because it means different things in-sample (where it is a *descriptive* measure of fit that mechanically increases with model complexity) and out-of-sample (where it is a genuine *predictive* measure that can go negative).

### 3. Formula
```
                SS_res           Σᵢ ( yᵢ − ŷᵢ )²             MSE_model
R²  =  1  −  -----------  =  1 − ---------------------  =  1 − -----------
                SS_tot           Σᵢ ( yᵢ −  ȳ  )²              Var(y)
```
Symbol by symbol:
- **SS_res** = residual sum of squares = the model's total squared error
- **SS_tot** = total sum of squares = `Σ(yᵢ − ȳ)²` = the squared error of the **mean-only baseline**
- **ȳ** = the mean of the *actual* values. **Which mean matters enormously** — see the limitations.
- The ratio `SS_res/SS_tot` is the fraction of variance left unexplained; subtracting from 1 gives the fraction explained.
- Range **(−∞, 1]**, higher better. Note the lower bound is **not** 0.
- Unitless.

**Equivalent expressions worth knowing:**
```
R²  =  1 − RSE                          (RSE from Part 4.6)
R²  =  1 − (RMSE / σ_y)²
R²  =  SS_reg / SS_tot                  ONLY for OLS with an intercept
R²  =  ( Pearson correlation of y and ŷ )²   ONLY for OLS with an intercept
```
The last two identities are the source of endless confusion. **They hold only for ordinary least squares with an intercept fitted on the same data.** For a random forest, a regularised model, or any out-of-sample evaluation, `R² ≠ corr(y,ŷ)²` and the ANOVA decomposition does not hold. This is a favourite advanced interview point.

### 4. Manual example
```
Step 1 — SS_res = Σ(y − ŷ)² = 43,000        (from Part 3)

Step 2 — SS_tot = Σ(y − ȳ)²  with ȳ = 450:
  (200−450)² = 62,500
  (250−450)² = 40,000
  (300−450)² = 22,500
  (350−450)² = 10,000
  (400−450)² =  2,500
  (450−450)² =      0
  (500−450)² =  2,500
  (550−450)² = 10,000
  (600−450)² = 22,500
  (900−450)² = 202,500
                --------
        Σ    = 375,000

Step 3 — R² = 1 − 43,000 / 375,000
            = 1 − 0.114667
            = 0.885333
```
**R² = 0.8853** → the model explains **88.5% of the variance** in house prices.

**Cross-check via RMSE:** `1 − (65.574/193.649)² = 1 − 0.114667 = 0.8853` ✓

**Now the caution.** Note that `(900−450)² = 202,500` is **54% of SS_tot**, and `(900−700)² = 40,000` is **93% of SS_res**. Both the numerator and denominator are dominated by the same single house. **R² on data with a strong outlier is largely a statement about that outlier**, and a very high R² can be manufactured by having one extreme point that the model gets roughly right. This is the leverage problem, and it is why you should always look at R² alongside a residual plot.

**Demonstration:** drop house 10 entirely.
```
Remaining 9 houses: y = 200..600, ŷ = 220..620, all errors ±10 or ±20
  SS_res = 3,000
  ȳ = 400, SS_tot = Σ(y−400)² = 40000+22500+10000+2500+0+2500+10000+22500+40000 = 150,000
  R² = 1 − 3000/150000 = 0.98
```
**R² jumps from 0.885 to 0.980 when one point is removed.** Same model behaviour on the nine remaining houses. That volatility is worth knowing about before you quote R² to three decimal places.

### 5. Python
```python
from sklearn.metrics import r2_score
import numpy as np

r2_score(y, y_pred)                                        # 0.885333
1 - ((y - y_pred)**2).sum() / ((y - y.mean())**2).sum()    # 0.885333

# Cross-check via RMSE and sigma
from sklearn.metrics import root_mean_squared_error
1 - (root_mean_squared_error(y, y_pred) / y.std())**2      # 0.885333

# Multi-output options
# r2_score(Y, Y_pred, multioutput='uniform_average')       # default: mean of per-target R²
# r2_score(Y, Y_pred, multioutput='variance_weighted')     # weight by each target's variance
# r2_score(Y, Y_pred, multioutput='raw_values')            # per-target array

# In model selection — R2 is already "greater is better", no neg_ prefix
# GridSearchCV(model, params, scoring='r2', cv=5)
```
Line-by-line:
- **`r2_score` uses the mean of `y_true` as the baseline**, and when you call it on a test set it uses the *test set's* mean. That is the standard convention but it is worth knowing: a test set with unusually low variance will produce a low R² even for a good model.
- **`model.score(X, y)` returns R² for regressors** in sklearn. Many people call `.score()` without knowing which metric they are getting.
- **`multioutput='variance_weighted'`** is usually the right choice for multi-target problems, because `'uniform_average'` lets a low-variance, hard-to-predict target drag the whole score down.

### 6. Interpretation

| R² | Meaning |
|---|---|
| **1.00** | Perfect. On real out-of-sample data, **suspect leakage.** |
| **0.90** | Excellent |
| **0.885** | Very good — **our example** |
| **0.70** | Good |
| **0.50** | Moderate — half the variance explained |
| **0.30** | Weak, but can be valuable in noisy domains |
| **0.00** | No better than predicting the mean |
| **< 0** | **Worse than predicting the mean.** A real and important signal. |

**Domain expectations vary enormously and quoting them well demonstrates experience:**

| Domain | Typical "good" R² |
|---|---|
| Physics / engineering with controlled measurement | 0.98 – 0.999 |
| House price prediction | 0.85 – 0.92 |
| Energy load forecasting | 0.95 – 0.99 |
| Credit risk / loss given default | 0.30 – 0.50 |
| Marketing response / customer LTV | 0.15 – 0.40 |
| Social science / psychology | 0.10 – 0.30 (and 0.30 is a strong result) |
| Individual stock returns | 0.01 – 0.05 (and profitable at that level) |
| Genome-wide association / polygenic scores | 0.05 – 0.20 |

**An R² of 0.05 can be extremely valuable** (a hedge fund with a 2% R² on returns makes money) and **an R² of 0.95 can be worthless** (if the baseline was already at 0.94). The number alone means nothing without the domain and the baseline.

### 7. Good vs bad values
Judge R² against three references, not against a universal band:
1. **The previous model** in production.
2. **The published literature** for the same problem.
3. **A trivial-but-nontrivial baseline** — not the mean, but e.g. "last year's value," "the group average," or a single-feature model. Beating the mean is a low bar; beating "the same house's last sale price adjusted for the market index" is a real bar.

### 8. Business use cases
- **Academic publication** — effectively mandatory in any paper reporting a regression.
- **Executive dashboards** — the "percent of variation explained" framing lands well.
- **Feature-importance and ablation studies:** the increase in R² from adding a feature block is a natural way to quantify its contribution.
- **Model monitoring** — a falling out-of-sample R² is a clear drift signal.
- **Communicating model value to non-technical audiences:** "we explain 88% of what drives price" is a strong sentence.
- **Cross-dataset benchmarking** — R² is unitless, so it travels where RMSE does not.
- **A/B comparison of feature sets** during development.
- **Credit risk and actuarial model documentation**, where it appears alongside domain-specific metrics.

### 9. Advantages
- **Unitless and scale-free**, so it is comparable across datasets and targets.
- **Anchored at 0**, giving a built-in "is this better than nothing?" verdict.
- **Intuitive framing** — "percent of variance explained" is easy to communicate.
- Universally recognised; no explanation needed.
- Directly related to RMSE via `R² = 1 − (RMSE/σ_y)²`, so it carries the same information in a friendlier form.
- Negative values are informative rather than an error — they immediately flag a broken model.
- Extends to multi-output with sensible weighting options.

### 10. Limitations
This list is long because R² is so widely misused.
- **In-sample R² always increases when you add a feature**, even a column of random noise. It therefore **cannot be used for model selection**. Use adjusted R², AIC/BIC, or cross-validated R².
- **Says nothing about bias.** A model can have R² = 0.95 and be systematically 12% low. (In OLS with an intercept the in-sample residuals sum to zero by construction, so this cannot happen in-sample — but it absolutely can out-of-sample, and for any non-OLS model.)
- **Says nothing about whether the functional form is right.** Anscombe's quartet is four datasets with identical R² (and identical means, variances, and regression lines) and radically different structures. A curved residual pattern is perfectly compatible with a high R².
- **Dominated by high-leverage points.** Ours moved from 0.885 to 0.980 on removing one observation.
- **Depends on the variance of the test set**, so R² computed on a homogeneous subsample looks worse than on a diverse one, for the same model. **This makes R² a poor choice for comparing performance across segments** — a segment with narrow y-range will always show a low R².
- **Does not imply causation or a good model** — only that the predictions co-vary with the actuals.
- **`R² = corr(y,ŷ)²` only for OLS with an intercept.** For other models the identity fails, and using the correlation-squared version can mask a badly miscalibrated model (see 6.5).
- **Cannot be compared across different target transformations.** An R² of 0.90 on `log(y)` and 0.90 on `y` are not the same achievement.
- For time series, "beating the mean" is a trivially low bar (a naive last-value forecast is far stronger), so R² on time series is often misleadingly high. Use MASE or Theil's U.
- Not defined when the target is constant (`SS_tot = 0`).

### 11. Common mistakes
1. **Using in-sample R² for model selection.** It monotonically increases with features; you will always pick the most complex model.
2. **Reporting only R² and no error magnitude.** R² = 0.885 does not tell a stakeholder that predictions are off by $36k. Report both.
3. **Assuming R² cannot be negative.** Out of sample it certainly can, and it means the model is worse than the mean.
4. **Comparing R² across segments with different target variance** and concluding one segment is "harder."
5. **Comparing R² across target transformations** (raw vs log).
6. **Believing high R² means the model is correctly specified.** Plot the residuals.
7. **Using R² as the headline metric for time series**, where the mean baseline is far too weak.
8. **Calling `model.score()` without knowing it returns R².**
9. Assuming `R² = corr²` for tree ensembles or regularised models.
10. Quoting R² to three decimals on a small test set, where its sampling variability is large.

### 12. Interview questions

**Easy — What is R²?** The proportion of the target's variance explained by the model, relative to a mean-only baseline: `1 − SS_res/SS_tot`.

**Easy — ★ Can R² be negative? What does it mean?**
Yes, out of sample. It means `SS_res > SS_tot`, i.e. the model's squared error exceeds that of simply predicting the mean of the test set. Causes: severe overfitting, distribution shift between train and test, a bug (wrong column, mis-aligned indices, inverted transform), or a test set whose mean differs a lot from the training mean. In-sample R² for OLS with an intercept cannot be negative, which is why people are surprised by it.

**Easy — Range of R²?** `(−∞, 1]`.

**Medium — ★ Why does in-sample R² always increase when you add a predictor?**
Because OLS minimises SS_res over a *larger* parameter space. The previous solution is still available (set the new coefficient to zero), so the new optimum can only be at least as good. Adding pure noise therefore never decreases in-sample R² and in finite samples almost always increases it, because the noise column will have some spurious correlation with the residuals. This is exactly why adjusted R², AIC, BIC, and cross-validation exist.

**Medium — ★ R² vs adjusted R²?**
R² penalises nothing; adjusted R² subtracts a penalty for the number of predictors, so it can *decrease* when you add a useless feature. Use adjusted R² (or better, cross-validated R²) when comparing models with different numbers of predictors on the same data.

**Medium — Your training R² is 0.95 and your test R² is 0.35. Diagnose.**
Severe overfitting. The model has memorised training-specific noise. Checks and remedies: reduce complexity (fewer features, shallower trees, stronger regularisation), verify there is no leakage that exists in train but not test, confirm the split is not temporally or group-wise contaminated, increase training data, and use cross-validation rather than a single split for the estimate. Also confirm the test set is genuinely comparable — a small or unusual test set can produce a low R² for reasons unrelated to overfitting.

**Medium — Why is a low R² acceptable in some domains?**
Because the irreducible noise dominates. Individual stock returns are close to unpredictable, so an R² of 0.02 represents a genuine and monetisable edge. Human behaviour in social science is intrinsically variable, so 0.20 is a strong finding. R² should be judged against the *achievable* ceiling for the domain, not against 1.0.

**Hard — ★ Explain Anscombe's quartet and what it means for R².**
Four small datasets constructed by Anscombe (1973) to have identical means, identical variances, identical correlation, identical OLS regression lines, and identical R² (0.67) — while being radically different: one is a clean linear relationship, one is a perfect parabola, one is linear with a single outlier, and one is a vertical cluster plus a single far-off point that alone determines the fitted slope. The lesson is that **summary statistics including R² cannot distinguish a well-specified model from a badly misspecified one**, and that a single high-leverage observation can manufacture a respectable R². The only defence is to plot the data and the residuals. The modern extension is the **Datasaurus Dozen**, which does the same trick with a dozen wildly different scatter plots.

**Hard — ★ Why is R² a bad metric for comparing performance across segments?**
Because R² is normalised by the *variance of the target within that segment*. Consider a house-price model evaluated on a luxury segment (prices $2M–$10M, σ large) and a starter-home segment (prices $180k–$220k, σ tiny). Even if the model's absolute and relative errors are identical in both, the starter-home R² will be far lower simply because `SS_tot` is small. You will wrongly conclude the model "does not work" for starter homes. **For segment comparison use a scale-free error measure like MdAPE, WAPE, or MASE, not R².** This is a very common real-world mistake.

**Hard — When is `R² = corr(y, ŷ)²`, and why does the distinction matter?**
Only for **OLS with an intercept, evaluated in-sample.** Under those conditions the residuals are orthogonal to the fitted values and the ANOVA identity `SS_tot = SS_reg + SS_res` holds exactly, which yields the identity. For any other model — regularised regression, tree ensembles, neural nets — or for any out-of-sample evaluation, they differ. The distinction matters because **the correlation-squared version is invariant to any affine rescaling of the predictions.** A model that predicts exactly `2 × y` has a correlation of 1.0 and hence "R²" of 1.0 under that formula, while the true `1 − SS_res/SS_tot` would be strongly negative. So reporting `corr²` can completely hide a miscalibrated model. Always compute R² as `1 − SS_res/SS_tot`, which is what `sklearn.metrics.r2_score` does.

---

## 6.2 ADJUSTED R²

### 1. Definition
R² penalised for the number of predictors, so that adding a useless feature can decrease it.

### 2. Intuition
R²'s fatal flaw for model selection is that it never decreases when you add a variable. Adjusted R² fixes this by asking: **"did that new feature explain more variance than a random feature would have?"**

The mechanism: instead of comparing raw sums of squares, compare them **per degree of freedom**. Adding a predictor consumes a degree of freedom, so the penalty is automatic. A feature that explains less than its "fair share" of variance makes adjusted R² go down.

### 3. Formula
```
                          (  SS_res / (n − p − 1)  )                        n − 1
Adj R²  =  1  −          (  ---------------------  )   =  1 − (1 − R²) × ------------
                          (  SS_tot / (n − 1)      )                       n − p − 1
```
Symbol by symbol:
- **n** = number of observations
- **p** = number of predictors (**not** counting the intercept)
- **n − p − 1** = residual degrees of freedom
- **n − 1** = total degrees of freedom
- The factor `(n−1)/(n−p−1)` is always ≥ 1, so **Adj R² ≤ R²** always, with equality only when p = 0.
- Range **(−∞, 1]**. It can be negative even in-sample.

**Behaviour:** adding a predictor raises R², which pulls Adj R² up, but also increases p, which pulls it down. The net effect is positive only if the new predictor's contribution exceeds what a random variable would contribute — informally, if its **partial F-statistic exceeds 1**.

### 4. Manual example
Suppose our model used **p = 3** predictors on **n = 10** observations.
```
R² = 0.885333,  n = 10,  p = 3

Step 1 — degrees of freedom:
  n − 1     = 9
  n − p − 1 = 10 − 3 − 1 = 6

Step 2 — the penalty factor:
  (n−1)/(n−p−1) = 9/6 = 1.5

Step 3 — apply:
  Adj R² = 1 − (1 − 0.885333) × 1.5
         = 1 − 0.114667 × 1.5
         = 1 − 0.172
         = 0.828
```
**Adjusted R² = 0.828**, down from R² = 0.885.

**The penalty is severe here because n is tiny relative to p.** With n = 10 and p = 3 we are using 4 of 10 degrees of freedom on parameters. Watch what happens as p grows with n fixed:

| p | n − p − 1 | Penalty factor | Adj R² |
|---|---|---|---|
| 0 | 9 | 1.000 | 0.885 |
| 1 | 8 | 1.125 | 0.871 |
| 3 | 6 | 1.500 | 0.828 |
| 5 | 4 | 2.250 | 0.742 |
| 7 | 2 | 4.500 | 0.484 |
| 8 | 1 | 9.000 | −0.032 |
| 9 | 0 | ∞ | undefined |

**At p = 9 with n = 10 the model has zero residual degrees of freedom** — it can fit the data perfectly (R² = 1) and adjusted R² is undefined. This table is the clearest possible illustration of why in-sample fit is meaningless when p approaches n, and it is a good thing to be able to sketch in an interview.

### 5. Python
Not in scikit-learn — implement it, or use statsmodels which reports it automatically.
```python
import numpy as np
from sklearn.metrics import r2_score

def adjusted_r2(y_true, y_pred, n_features):
    n = len(y_true)
    r2 = r2_score(y_true, y_pred)
    if n - n_features - 1 <= 0:
        return np.nan                       # no residual degrees of freedom
    return 1 - (1 - r2) * (n - 1) / (n - n_features - 1)

adjusted_r2(y, y_pred, n_features=3)        # 0.828

# statsmodels reports it in the standard OLS summary
# import statsmodels.api as sm
# res = sm.OLS(y, sm.add_constant(X)).fit()
# res.rsquared, res.rsquared_adj
```
- **Only meaningful in-sample**, on the data the model was fitted to. Computing adjusted R² on a test set is conceptually confused: out-of-sample R² already accounts for overfitting empirically, so no degrees-of-freedom penalty is needed. If you see "test adjusted R²" reported, it is a mistake.
- For models without a clean parameter count (random forests, GBMs, neural nets), **p is not well defined** and adjusted R² is not applicable. Use cross-validated R² instead.

### 6. Interpretation
Read it as R², but with a complexity charge. The most useful signals:
- **Adj R² increases when you add a feature** → the feature earns its keep.
- **Adj R² decreases** → the feature is not worth its degree of freedom; drop it.
- **A large gap between R² and Adj R²** → you have too many predictors for your sample size. Ours: 0.885 vs 0.828, a gap of 0.057 with only 3 predictors and 10 rows, which is a warning.

### 7. Good vs bad values
Same bands as R², but always report the pair. **The gap `R² − Adj R²` is itself the diagnostic**: a gap over ~0.05 suggests over-parameterisation relative to n.

### 8. Business use cases
- **Classical statistical modelling and econometrics** — reported by default in every OLS summary and expected in any regression write-up.
- **Feature selection in linear models** — stepwise procedures historically used adjusted R² as the criterion.
- **Academic publication** — reviewers expect it alongside R².
- **Regulated model documentation** (credit risk, actuarial) where linear/GLM models dominate and parsimony is valued for explainability.
- **Comparing nested linear models** on the same dataset.
- **Small-sample settings** where the degrees-of-freedom penalty is material.

### 9. Advantages
- **Penalises complexity**, so unlike R² it can be used for model comparison.
- Trivial to compute from R², n, and p.
- Standard output in statistical software, so universally recognised in that world.
- The R² vs Adj R² gap gives a free over-parameterisation diagnostic.
- Retains R²'s unitless, anchored interpretation.

### 10. Limitations
- **Only defined for models with a countable number of parameters.** Not applicable to random forests, GBMs (where effective complexity depends on depth, trees, and learning rate jointly), or neural networks.
- **A weak penalty compared to AIC/BIC**, and a much weaker one than actual cross-validation. It tends to retain too many variables — it will keep a feature whose partial F-statistic exceeds 1, which corresponds to a very lenient significance threshold.
- **Not a substitute for out-of-sample validation.** A model can have a good adjusted R² and generalise badly.
- Only meaningful in-sample; reporting it on a test set is a category error.
- Can be negative, which confuses people.
- Inherits every one of R²'s other limitations (outlier leverage, blindness to bias and misspecification, variance-dependence).
- Undefined when `n ≤ p + 1`.

### 11. Common mistakes
1. **Computing adjusted R² on a test set.** Out-of-sample R² already reflects overfitting; the penalty is meaningless there.
2. **Applying it to tree ensembles or neural nets** where p has no clean meaning.
3. **Treating it as sufficient for model selection.** It is far weaker than cross-validation; use CV as the primary tool and adjusted R² as a secondary sanity check.
4. Miscounting p — it excludes the intercept.
5. Not reporting plain R² alongside, so the reader cannot see the gap.

### 12. Interview questions

**Easy — Why does adjusted R² exist?** Because R² never decreases when you add a predictor, so it cannot be used to choose between models of different complexity.

**Easy — Can adjusted R² be negative?** Yes, even in-sample, when the model explains less variance than its degrees of freedom cost.

**Medium — ★ When does adding a variable increase adjusted R²?**
When the variable explains more variance than a purely random variable would be expected to — equivalently, when its partial F-statistic exceeds 1. That is a very lenient bar (roughly a t-statistic above 1, or p ≈ 0.32), which is why adjusted R² is a weak model-selection criterion and tends to keep too many variables compared to AIC (penalty ≈ F > 2) or BIC (penalty ≈ F > log n).

**Medium — Adjusted R², AIC, BIC — how do their penalties compare?**
All three trade fit against complexity, with increasing severity: adjusted R² ≈ retain if F > 1; **AIC** ≈ retain if F > 2; **BIC** ≈ retain if F > ln(n), which grows with sample size and so is far stricter for large n. AIC targets predictive accuracy (it estimates out-of-sample deviance); BIC targets identifying the true model and is consistent for model selection if the true model is in the candidate set. In practice, use cross-validation as the primary criterion — it makes no distributional assumptions and directly estimates the quantity you care about — and use these as fast, cheap complements.

**Hard — Why can't you use adjusted R² for a random forest?**
Because p — the number of parameters — is not well defined. A forest's effective complexity depends on the number of trees, their depth, the minimum leaf size, and the feature-subsampling rate in an interacting way; there is no integer that plays the role p plays in a linear model. The concept you want is **effective degrees of freedom**, which for ensembles must be estimated empirically (for example via the trace of the smoother matrix in some settings, or via generalised cross-validation). In practice you skip all of this and use **cross-validated R² or cross-validated RMSE**, which measures generalisation directly without needing a complexity count at all.

---

## 6.3 EXPLAINED VARIANCE SCORE

### 1. Definition
The proportion of the target's variance explained, computed on the **variance** of the residuals rather than their raw sum of squares. It differs from R² exactly by ignoring bias.

### 2. Intuition
R² asks "how much of the squared error did I remove?" Explained variance asks a subtly different question: **"how much of the variation did I capture, ignoring any constant offset?"**

The difference is precisely the **bias term**. If your predictions are perfectly shaped but uniformly 50 units too low, explained variance is high (you captured all the variation) while R² is lower (you have a systematic offset). The gap between the two is therefore a **free bias diagnostic**.

### 3. Formula
```
                          Var( y − ŷ )              Var( residuals )
Explained Variance  =  1 − ---------------  =  1 − -------------------
                             Var( y )                    Var( y )
```
- **Var(y − ŷ)** = the variance of the residuals = `mean(e²) − (mean e)²`
- Contrast with R², whose numerator is `mean(e²)` — including the squared mean
- Therefore:
```
                                        ( mean residual )²
Explained Variance  =  R²  +  ------------------------------
                                          Var( y )
```
So **Explained Variance ≥ R² always**, and the gap is exactly `Bias² / Var(y)`.
- Range (−∞, 1], unitless.

### 4. Manual example
```
mean residual = +18       ->  Bias² = 324
Var(e) = mean(e²) − (mean e)² = 4,300 − 324 = 3,976
Var(y) = 375,000 / 10 = 37,500

Explained Variance = 1 − 3,976 / 37,500 = 1 − 0.106027 = 0.893973

Check the identity:
  R² + Bias²/Var(y) = 0.885333 + 324/37,500 = 0.885333 + 0.008640 = 0.893973 ✓
```
**Explained Variance = 0.8940** versus **R² = 0.8853**.

**The gap = 0.0086 = Bias²/Var(y).** Small here, because our bias is small relative to the target's variance. But the diagnostic is immediate:
```
EVS − R² = 0.0086   ->  bias accounts for 0.86% of the target's variance
```
**If you ever see a large gap between EVS and R², you have a systematically biased model** — and you can fix a large part of your error simply by subtracting the mean residual.

### 5. Python
```python
from sklearn.metrics import explained_variance_score, r2_score
import numpy as np

explained_variance_score(y, y_pred)     # 0.893973
r2_score(y, y_pred)                     # 0.885333

# The gap IS the normalised squared bias — a free diagnostic
e = y - y_pred
gap = explained_variance_score(y, y_pred) - r2_score(y, y_pred)
print(f"EVS − R² = {gap:.6f}   Bias²/Var(y) = {e.mean()**2 / y.var():.6f}")
# EVS − R² = 0.008640   Bias²/Var(y) = 0.008640
```

### 6. Interpretation
Read the *gap*, not the level:

| EVS − R² | Meaning |
|---|---|
| ≈ 0 | Unbiased model. EVS and R² carry the same information; report R². |
| 0.01 – 0.05 | Mild systematic bias; worth investigating and probably worth correcting |
| > 0.05 | **Substantial bias.** Subtracting the mean residual will noticeably improve MAE, RMSE, and R² |

### 7. Good vs bad values
Same bands as R². The metric is most useful diagnostically rather than as a headline.

### 8. Business use cases
- **A bias diagnostic** used alongside R² — its best use.
- **Signal processing and physical sciences**, where "fraction of variance explained" is the natural language and a DC offset is often irrelevant or separately calibrated.
- **Detecting back-transformation bias** after log-space modelling — the EVS/R² gap will open up.
- **Comparing a model's shape-capturing ability separately from its calibration**, which is useful when a downstream recalibration step is planned anyway.
- **Neuroscience and psychophysics**, where variance-explained is the conventional metric.

### 9. Advantages
- **Isolates the model's ability to capture variation** from its calibration.
- **The EVS − R² gap is a free, exact bias diagnostic** requiring no extra work.
- Unitless and anchored like R².
- Available in scikit-learn.

### 10. Limitations
- **Ignores bias**, which is a serious flaw if used as the primary metric — a model that is uniformly 1000 units low can have EVS ≈ 1.0.
- Frequently confused with R², and the two are reported interchangeably by people who do not know they differ.
- Inherits R²'s other limitations (leverage sensitivity, variance-dependence, blindness to misspecification).
- Less familiar than R², so it needs explanation.
- Rarely the right headline metric.

### 11. Common mistakes
1. **Reporting EVS as if it were R².** They differ by exactly the normalised squared bias.
2. **Using EVS as the primary metric**, which lets a badly biased model look excellent.
3. Not exploiting the gap as a diagnostic — this is the metric's main value.

### 12. Interview questions
**Easy — How does explained variance differ from R²?** EVS uses the variance of the residuals; R² uses their mean square. EVS therefore ignores the mean residual (the bias).
**Medium — ★ State the exact relationship.** `EVS = R² + (mean residual)²/Var(y)`. So EVS ≥ R² always, and the gap is the normalised squared bias.
**Medium — When would EVS be much larger than R²?** When the model is systematically offset — for example after naive `exp()` back-transformation from a log model, or under distribution shift where the target level moved but its variation did not. It is a signal that a simple additive or multiplicative recalibration would recover most of the lost performance.
**Hard — Which should you report and why?** **R², as the headline**, because it accounts for both shape and calibration, and a biased model genuinely is worse. Report EVS alongside *specifically as a diagnostic*, and interpret the gap: a near-zero gap confirms unbiasedness; a large gap tells you that your error is mostly a correctable offset rather than an inability to capture the signal, which changes what you do next.

---

## 6.4 PEARSON CORRELATION (r) AND SPEARMAN CORRELATION (ρ)

### 1. Definition
- **Pearson r:** the linear correlation between actual and predicted values.
- **Spearman ρ:** the Pearson correlation of the *ranks* — a measure of monotonic association.

### 2. Intuition
Both answer: **"do the predictions move in the same direction as the actuals?"** Neither answers "are the predictions correct."

That distinction is the whole story. Correlation is **invariant to any affine transformation** of the predictions:
```
If ŷ' = a·ŷ + b  (with a > 0), then corr(y, ŷ') = corr(y, ŷ)
```
So a model predicting exactly `2y + 1000` has **r = 1.000** and is completely useless as a point predictor. Correlation measures **ranking/shape**, not accuracy.

This makes correlation:
- **Wrong as a primary accuracy metric** — it cannot detect scale or offset errors.
- **Right when only the ordering matters** — asset selection, candidate ranking, lead prioritisation, screening, and any downstream step that sorts rather than uses the values.

**Spearman** goes further and discards even the linearity requirement, measuring only whether the relationship is monotonic. It is robust to outliers and to nonlinear monotone distortion.

### 3. Formula
```
                     Σ (yᵢ − ȳ)(ŷᵢ − ŷ̄)                    Cov(y, ŷ)
Pearson  r  =  --------------------------------------  =  ------------------
                √Σ(yᵢ − ȳ)²  ·  √Σ(ŷᵢ − ŷ̄)²             σ_y · σ_ŷ

Spearman ρ  =  Pearson r computed on rank(y) and rank(ŷ)
```
- Range **[−1, +1]** for both; +1 = perfect positive association, 0 = none, −1 = perfectly inverted.
- **Pearson** measures *linear* association and is sensitive to outliers.
- **Spearman** measures *monotonic* association and is robust; it is unaffected by any monotone transformation of either variable.
- **Kendall's τ** is a third option, based on concordant/discordant pairs; it is more robust still and has a cleaner probabilistic interpretation, but is less common.

### 4. Manual example
```python
from scipy import stats
stats.pearsonr(y, y_pred)[0]      # 0.961653
stats.spearmanr(y, y_pred)[0]     # 1.000000
```
**Pearson r = 0.9617, Spearman ρ = 1.0000.**

**Spearman is exactly 1.0** — because our predictions preserve the ordering of the houses **perfectly**: the cheapest house has the lowest prediction, the most expensive has the highest, with no inversions anywhere. As a *ranking* system, this model is flawless.

**Pearson is 0.9617** — lower, because although the ordering is perfect the *magnitudes* are compressed at the top end (the $900k house is predicted at only $700k), which weakens the linear relationship.

**Now compare all four fit metrics:**
```
Spearman ρ         = 1.0000   perfect ordering
Pearson r          = 0.9617   strong linear association
r²                 = 0.9248   (r squared)
Explained Variance = 0.8940
R²                 = 0.8853   actual predictive accuracy
```
**Note the strict ordering ρ > r > r² > EVS > R².** This is typical and highly informative:
- `ρ = 1` but `R² = 0.885` → **the model ranks perfectly but is mis-scaled.** A monotone recalibration (isotonic regression on the predictions) could push R² much closer to 1 *without changing the ranking at all.*
- `r² = 0.925 > R² = 0.885` → the gap of 0.04 quantifies the **scale/offset miscalibration**, exactly analogous to the discrimination-vs-calibration split in classification.

**The critical warning:** if you reported `r² = 0.925` and called it "R²", you would be overstating your model's accuracy. Papers do this. `r²` and `R²` coincide only for in-sample OLS with an intercept.

### 5. Python
```python
from scipy import stats
import numpy as np

r,   p_r   = stats.pearsonr(y, y_pred)      # 0.9617, p-value
rho, p_rho = stats.spearmanr(y, y_pred)     # 1.0000, p-value
tau, p_tau = stats.kendalltau(y, y_pred)    # 1.0000, p-value

# The diagnostic comparison — do this whenever ranking might matter
from sklearn.metrics import r2_score
print(f"Spearman rho = {rho:.4f}   (ranking quality)")
print(f"Pearson  r   = {r:.4f}   r^2 = {r**2:.4f}   (linear association)")
print(f"R2           = {r2_score(y, y_pred):.4f}   (actual accuracy)")
print(f"r^2 - R2     = {r**2 - r2_score(y, y_pred):.4f}   <- miscalibration")
# Spearman rho = 1.0000   (ranking quality)
# Pearson  r   = 0.9617   r^2 = 0.9248   (linear association)
# R2           = 0.8853   (actual accuracy)
# r^2 - R2     = 0.0395   <- miscalibration
```
- `scipy.stats` returns a `(statistic, p_value)` tuple. The p-value tests the null of zero correlation and is rarely the interesting part in an ML context.
- **If `r² ≫ R²`, your model is miscalibrated and a monotone or linear recalibration will improve it for free.** Fit isotonic regression or a simple linear regression of `y` on `ŷ` using held-out data.

### 6. Interpretation

| Value | Pearson r | Spearman ρ |
|---|---|---|
| 1.0 | Perfect linear relationship | Perfect ordering |
| 0.9 | Very strong | Very strong ordering |
| 0.7 | Strong | Strong |
| 0.5 | Moderate | Moderate |
| 0.3 | Weak | Weak |
| 0.0 | No linear relationship | No monotonic relationship |
| < 0 | Inverted — check the sign of your predictions | Inverted |

**The comparison is the informative part:**

| Pattern | Diagnosis |
|---|---|
| ρ ≈ r | The relationship is approximately linear |
| **ρ > r** | A **nonlinear but monotone** relationship, or outliers depressing r. Ours: ρ=1.00 vs r=0.96 → the top end is compressed. A monotone transform of the predictions would help. |
| ρ < r | Rare; usually indicates ties in the data or that a few high-leverage points are inflating r |
| **r² ≫ R²** | **Miscalibration** — right shape, wrong scale or offset. Recalibrate. |
| ρ high, R² low | The model is an excellent *ranker* and a poor *estimator*. Perfectly fine if the downstream use is ranking. |

### 7. Good vs bad values
Judge against the domain. In quantitative finance a Spearman ρ (there called the **Information Coefficient**, IC) of **0.03–0.06** between predicted and realised returns is a genuinely valuable signal. In physical measurement anything below 0.99 is a problem.

### 8. Business use cases
Correlation is the right primary metric when **only the ordering is consumed**:
- **Quantitative finance:** the **Information Coefficient** (rank correlation between predicted and realised returns) is the standard signal-quality metric, because portfolio construction sorts assets rather than using the predicted magnitudes.
- **Lead scoring and sales prioritisation:** the sales team works a sorted list.
- **Candidate/resume ranking**, subject to fairness constraints.
- **Recommendation ranking:** relative ordering determines what the user sees.
- **Screening and triage:** which cases to examine first.
- **Feature screening:** Spearman between each feature and the target is a fast, monotone-relationship-aware filter (and unlike Pearson it catches nonlinear monotone relationships).
- **Method comparison in the sciences:** does a cheap assay rank samples the same way as an expensive one?
- **As a calibration diagnostic** alongside R², via the `r² − R²` gap.

### 9. Advantages
- **Directly measures ranking quality**, which is the right target for many real systems.
- **Invariant to affine (Pearson) or any monotone (Spearman) rescaling**, so it isolates shape from calibration.
- **Spearman is robust** to outliers and to nonlinear monotone distortion.
- Unitless and universally understood.
- Comes with a significance test.
- Cheap and fast; good for feature screening.
- The `r² − R²` gap is a free miscalibration diagnostic.

### 10. Limitations
- **Cannot detect scale or offset errors** — this is disqualifying for use as an accuracy metric. `ŷ = 2y` gives r = 1.
- **Says nothing about the size of errors.**
- **Pearson is outlier-sensitive** and assumes linearity.
- **Spearman discards magnitude information entirely**, so it cannot distinguish a near-miss from a large miss as long as the order is preserved.
- **`r²` is routinely mislabelled as `R²`** in papers and dashboards, overstating accuracy.
- Correlation does not imply the model is usable, calibrated, or causal.
- Sensitive to ties (Spearman) and to restricted range (both — evaluating on a narrow subset of y attenuates correlation, exactly as it deflates R²).
- Undefined if either series is constant.

### 11. Common mistakes
1. **Reporting `r²` as `R²`.** The single most common error in this area. They differ whenever the model is not in-sample OLS with an intercept, and `r² ≥ R²` in practice, so the mislabelling always flatters.
2. **Using correlation as the primary accuracy metric.** It cannot see calibration.
3. Using Pearson on data with outliers or a nonlinear relationship, and concluding there is no association.
4. Ignoring the ρ-vs-r comparison, which is a free diagnostic.
5. Concluding a model is good because r = 0.95 while RMSE is enormous.
6. Comparing correlations across samples with different ranges of y without noting range restriction.

### 12. Interview questions

**Easy — Difference between Pearson and Spearman?** Pearson measures linear association on the raw values; Spearman measures monotonic association on the ranks. Spearman is robust and catches nonlinear monotone relationships.

**Easy — ★ Can a model have r = 1.0 and be useless?** Yes. If `ŷ = 2y + 1000`, the correlation is exactly 1.0 while every prediction is badly wrong. Correlation is invariant to affine rescaling and therefore blind to calibration.

**Medium — ★ Why is `r²` not the same as `R²`?**
`r²` is the squared Pearson correlation between y and ŷ; `R² = 1 − SS_res/SS_tot`. They coincide **only** for OLS with an intercept evaluated in-sample. In general `r² ≥ R²`, because `r²` measures only how well the predictions *co-vary* with the actuals while `R²` also charges you for getting the scale and offset wrong. So `r² − R²` is a measure of miscalibration. Reporting `r²` as `R²` therefore systematically overstates accuracy.

**Medium — Your Spearman ρ is 0.98 but R² is 0.45. What is happening and what do you do?**
The model ranks almost perfectly but its predicted *values* are badly mis-scaled — compressed, offset, or nonlinearly distorted. This is a **calibration** problem, not a **discrimination** problem, and it is the good kind of problem to have because it is cheap to fix. Fit a monotone recalibration on held-out data: **isotonic regression** of `y` on `ŷ` (fully flexible, needs a few hundred points) or a simple linear regression `y ~ ŷ` (two parameters, works with little data). Because both are monotone, they leave Spearman unchanged while potentially raising R² dramatically. This is the direct regression analogue of Platt/isotonic calibration in classification, and being able to name that parallel is a strong answer.

**Medium — What is the Information Coefficient in finance?**
The rank (Spearman) correlation between a model's predicted returns and the realised returns, computed cross-sectionally each period and then averaged. It is the standard measure of signal quality because portfolio construction only needs the *ordering* of assets, not accurate return magnitudes. Values of 0.03–0.06 are considered good, which is why R² or RMSE on return prediction look catastrophic while the strategy is profitable — a nice illustration of matching the metric to the downstream decision.

**Hard — When is correlation the *correct* primary metric, and what must you add to it?**
When the downstream system consumes only the ordering: portfolio construction, top-k selection, prioritised worklists, recommendation ranking, triage. In those cases magnitude errors are literally not used, so penalising them is measuring something the business does not care about. What you must add: (1) a **top-k metric** (correlation weights all pairs equally, but you only act on the top — so report precision-at-k analogues, decile lift, or the mean actual value in the top decile); (2) a **stability measure** across time periods or folds, because a signal with high average IC and huge variance is not tradeable; (3) **calibration if any downstream step uses the values** — a common failure is that "we only rank" turns out to be false because someone sizes positions by the predicted magnitude. Report Spearman for ranking, plus decile-level actuals, plus R² so the calibration question is at least visible.

---

## 6.5 CONCORDANCE CORRELATION COEFFICIENT (CCC / Lin's CCC)

### 1. Definition
A measure of **agreement** rather than association: it penalises both poor correlation and poor calibration.

### 2. Intuition
Pearson r asks "do they move together?" CCC asks the stricter question **"do they agree?"** — i.e. do the points fall on the 45° line `ŷ = y`, not merely on *some* straight line.

It is the standard metric in **method-comparison and agreement studies** (does a new cheap instrument agree with the gold standard?), and it neatly decomposes into a correlation part and a calibration part, making it a good single-number summary when both matter.

### 3. Formula
```
                          2 · Cov(y, ŷ)
CCC  =  ------------------------------------------------
          Var(y) + Var(ŷ) + ( mean(y) − mean(ŷ) )²
```
- **Numerator** `2·Cov(y,ŷ)` rewards co-variation.
- **`Var(y) + Var(ŷ)`** penalises a mismatch in *spread* (a model whose predictions are too compressed is penalised).
- **`(mean(y) − mean(ŷ))²`** penalises **bias** directly.
- Range **[−1, +1]**; **+1 requires the points to lie exactly on the 45° line.**

**The decomposition that makes CCC useful:**
```
CCC  =  r  ×  C_b
```
where **r** is the Pearson correlation (the *precision* component) and **C_b ∈ (0,1]** is a **bias-correction factor** measuring how far the best-fit line is from the 45° line (the *accuracy* component). So CCC = "how tightly do the points cluster around a line" × "is that line the right one."

### 4. Manual example
```
mean(y)  = 450        Var(y)  = 37,500
mean(ŷ)  = 432        Var(ŷ)  = ?

ŷ = 220,240,310,330,420,430,520,530,620,700 ; mean 432
deviations: −212,−192,−122,−102,−12,−2,88,98,188,268
squares: 44944, 36864, 14884, 10404, 144, 4, 7744, 9604, 35344, 71824
Σ = 231,760      ->  Var(ŷ) = 23,176

Cov(y, ŷ) = mean[(y−450)(ŷ−432)]
  (−250)(−212) =  53,000
  (−200)(−192) =  38,400
  (−150)(−122) =  18,300
  (−100)(−102) =  10,200
  ( −50)( −12) =     600
  (   0)(  −2) =       0
  (  50)(  88) =   4,400
  ( 100)(  98) =   9,800
  ( 150)( 188) =  28,200
  ( 450)( 268) = 120,600
                 --------
        Σ    =   283,500   ->  Cov = 28,350

CCC = 2 × 28,350 / ( 37,500 + 23,176 + (450 − 432)² )
    = 56,700 / ( 37,500 + 23,176 + 324 )
    = 56,700 / 61,000
    = 0.929508
```
**CCC = 0.9295.**

**Compare the whole fit family:**
```
Spearman ρ = 1.0000   perfect ordering
Pearson  r = 0.9617   strong linear association
CCC        = 0.9295   good agreement (penalises the compressed spread and the bias)
r²         = 0.9248
EVS        = 0.8940
R²         = 0.8853
```
CCC sits between r and R², which is exactly where it should: it charges for the miscalibration (Var(ŷ) = 23,176 is well below Var(y) = 37,500 — the predictions are **too compressed**) and for the bias (18 units), but it is less punitive than R² because it normalises differently.

**The compressed-variance finding is the most actionable thing in this table:** `Var(ŷ)/Var(y) = 0.618`, so the model's predictions span only 62% of the target's spread. That is the classic signature of **regression to the mean** from over-regularisation or from an under-fitted model, and it is fixable.

### 5. Python
```python
import numpy as np

def ccc(y_true, y_pred):
    """Lin's Concordance Correlation Coefficient."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    my, mp = y_true.mean(), y_pred.mean()
    vy, vp = y_true.var(), y_pred.var()             # population variance (ddof=0)
    cov = ((y_true - my) * (y_pred - mp)).mean()
    return 2 * cov / (vy + vp + (my - mp) ** 2)

ccc(y, y_pred)          # 0.929508

# The decomposition: CCC = r * C_b
from scipy import stats
r = stats.pearsonr(y, y_pred)[0]
print(f"r = {r:.4f}   C_b = {ccc(y, y_pred)/r:.4f}")
# r = 0.9617   C_b = 0.9666      -> 96.7% of the achievable accuracy given that correlation

# The variance-ratio diagnostic — check this on every model
print(f"Var(pred)/Var(actual) = {y_pred.var()/y.var():.3f}")
# Var(pred)/Var(actual) = 0.618   -> predictions are too compressed
```

### 6. Interpretation

Conventional agreement bands (from the method-comparison literature):

| CCC | Agreement |
|---|---|
| > 0.99 | Almost perfect |
| 0.95 – 0.99 | Substantial |
| 0.90 – 0.95 | Moderate — **our example at 0.930** |
| < 0.90 | Poor |

These bands are strict because CCC comes from clinical instrument validation, where the question is "can this replace the gold standard?" For general ML they are unreasonably harsh; use them only in an agreement context.

**The `Var(ŷ)/Var(y)` ratio deserves to be a standard part of every regression report:**

| Ratio | Meaning |
|---|---|
| ≈ 1.0 | Prediction spread matches reality |
| **< 1** | **Predictions too compressed** — regression to the mean. Causes: over-regularisation, under-fitting, insufficient signal, or an averaging ensemble. Our 0.62 is substantial compression. |
| > 1 | Predictions too spread out — over-fitting, or an unstable model amplifying noise |

### 7. Good vs bad values
Use the bands above for agreement studies; for general ML treat CCC as a summary that combines r and calibration and compare it across models rather than against absolute thresholds.

### 8. Business use cases
- **Method-comparison / instrument validation studies:** does a new sensor, assay, or wearable agree with the reference standard? This is CCC's home territory, and it is often reported with a **Bland-Altman plot** (residuals vs the mean of the two measurements, with limits of agreement).
- **Clinical measurement validation** and regulatory submissions for diagnostic devices.
- **Inter-rater agreement on continuous scales** — the continuous analogue of Cohen's Kappa.
- **Model-vs-human comparison** where you want to claim equivalence rather than mere correlation.
- **Digital biomarker validation** (a phone-derived measure vs a clinical one).
- **Any setting where "our model agrees with the gold standard" is the claim**, since correlation alone is insufficient to support it.
- **As a compression diagnostic** via its variance-ratio component.

### 9. Advantages
- **Measures agreement, not just association** — penalises both bias and spread mismatch, which r does not.
- **Decomposes into `r × C_b`**, separating precision from accuracy in one line.
- Bounded [−1, 1] and unitless.
- The gold standard in method-comparison studies, so it is expected in that literature.
- Its variance-ratio component surfaces regression-to-the-mean, a common and fixable defect.
- The continuous analogue of Cohen's Kappa, which makes it easy to explain to anyone who knows Kappa.

### 10. Limitations
- **Not in scikit-learn**; must be implemented, and there are variants (with/without the `n−1` correction) that differ slightly.
- **Unfamiliar in mainstream ML**, so it needs defining.
- **Sensitive to the range of the data** — like all correlation-based metrics, restricting the range of y attenuates it, so it is not comparable across segments with different spreads.
- The conventional bands are calibrated for clinical instruments and are too strict for typical ML problems.
- Being a single number, it does not tell you *whether* the problem is bias or compression — you need the decomposition or the variance ratio for that.
- Assumes the two variables are on the same scale and units (which is true for actual vs predicted, but means it cannot be used for e.g. comparing two instruments with different units).

### 11. Common mistakes
1. Reporting Pearson r in a method-comparison study, where agreement is the claim. r cannot support "these measurements agree."
2. Applying the strict clinical bands to a general ML problem and concluding the model is poor.
3. Not reporting the decomposition or the variance ratio, which is where the diagnostic value lies.
4. Using population vs sample variance inconsistently between implementations, producing slightly different values.

### 12. Interview questions
**Easy — What does CCC measure?** Agreement with the 45° line — it penalises poor correlation, bias, and mismatched spread.
**Medium — ★ Why is Pearson r insufficient for a method-comparison study?** Because r is invariant to scale and offset. A new instrument reading exactly twice the reference value has r = 1.0 and does not agree with it at all. CCC penalises the scale and offset error; r cannot see them. In practice you report CCC *and* a Bland-Altman plot, which shows bias and the limits of agreement directly.
**Medium — What does `Var(ŷ)/Var(y) = 0.6` tell you?** That the model's predictions span only 60% of the target's spread — regression to the mean. Typical causes: too much regularisation, an under-fitted model, weak features, or heavy ensemble averaging. It means the model is systematically conservative: it under-predicts high values and over-predicts low ones. A linear recalibration can restore the spread, though it will increase variance and may worsen MSE — which is the correct trade only if the downstream use needs the full range (e.g. capacity planning for peaks).
**Hard — Relate CCC to the classification metrics you know.** CCC is to Pearson r what **Cohen's Kappa is to raw accuracy**: both correct a naive association/agreement measure for something it should not get credit for. And CCC's decomposition into `r × C_b` is structurally the same idea as the **discrimination-versus-calibration split** in probabilistic classification (ROC-AUC measures ranking; Brier/Log Loss also charge for calibration; Platt/isotonic scaling fixes calibration without changing ranking). The regression analogue of Platt scaling is a linear or isotonic recalibration of `ŷ`, which raises CCC and R² while leaving Spearman ρ untouched.

## 6.6 Goodness-of-fit summary on the running example

| Metric | Value | What it measures | Blind to |
|---|---|---|---|
| Spearman ρ | **1.0000** | Ranking quality | Everything about magnitude |
| Pearson r | 0.9617 | Linear association | Scale and offset |
| r² | 0.9248 | Squared linear association | Scale and offset |
| CCC | 0.9295 | Agreement with the 45° line | — (penalises both) |
| Explained Variance | 0.8940 | Variance captured | Bias |
| **R²** | **0.8853** | Predictive accuracy vs the mean baseline | Functional form, outlier leverage |
| Adjusted R² (p=3) | 0.8280 | R² penalised for complexity | Same as R² |

**How to read this ladder — the single most useful diagnostic pattern in Part 6:**

```
Spearman  1.000  ─┐
Pearson²  0.925  ─┤  gap of 0.075 = the model ranks better than it estimates
R²        0.885  ─┘  -> MISCALIBRATION: right shape, wrong scale
                     -> Fix with isotonic/linear recalibration (free improvement)

EVS       0.894  ─┐
R²        0.885  ─┘  gap of 0.009 = Bias²/Var(y)
                     -> Small bias; not the main problem here

Var(ŷ)/Var(y) = 0.618
                     -> COMPRESSION: predictions span only 62% of the real range
                     -> Regression to the mean; consider less regularisation
```

**The verdict on our model, from the fit metrics alone:** it identifies the ordering of house prices perfectly, but it systematically compresses the range — under-predicting expensive houses and over-predicting cheap ones. That is a calibration problem, not a signal problem, and it is the cheapest kind to fix. **No single metric in the table tells you that; the pattern across them does.**

---

# PART 7 — Robust and Asymmetric Losses

## 7.0 Why this Part exists

Parts 2–6 gave you metrics. This Part gives you **loss functions** — objectives you actually train on — and it exists because the two most common regression complaints have the same root cause:

1. **"MSE chases my outliers."** One bad record dominates the fit. You want MAE's robustness but MSE's smooth gradients.
2. **"My cost is asymmetric."** Being 10 units short costs $500 (a stockout); being 10 units over costs $5 (holding cost). MSE and MAE both treat those identically, so *no symmetric loss can ever produce the right model*.

Both are solved here. The metrics in this Part are usable as objectives, which is the whole point: **you cannot fix a cost mismatch by choosing a reporting metric — you must change what the model optimises.**

**The landscape:**

```
                        Small errors        Large errors      Optimal predictor
MSE       (L2)          quadratic           quadratic         conditional mean
MAE       (L1)          linear              linear            conditional median
Huber                   quadratic           linear            mean-ish, robustified
Log-Cosh                quadratic           linear            mean-ish (smooth Huber)
Quantile (pinball)      linear, weighted    linear, weighted   conditional QUANTILE tau
epsilon-insensitive     ZERO inside the tube linear            a "tube" of acceptability
Tukey biweight          quadratic           ZERO (rejects)     mean of the inliers only
```

---

## 7.1 HUBER LOSS

### 1. Definition
A hybrid loss: quadratic for small residuals, linear for large ones, with a tuning parameter δ marking the switch point.

### 2. Intuition
Huber loss is the standard answer to "**I want MAE's robustness and MSE's smoothness.**"

The reasoning is precise. MSE's problem is its gradient `2e`, which grows without bound so one extreme point dominates. MAE's problem is its gradient `±1`, which never shrinks so convergence near the optimum is poor. Huber takes the best of each:
- **Inside ±δ** (ordinary observations): behave like MSE — smooth, gradient shrinks to zero at the optimum, fast convergence.
- **Outside ±δ** (outliers): behave like MAE — constant gradient magnitude δ, so an extreme point exerts **bounded influence** no matter how extreme it is.

That "bounded influence" phrase is the technical heart of robust statistics: an observation 1,000 units out pulls exactly as hard as one 10 units out (once both exceed δ). Huber is the canonical M-estimator and was introduced by Peter Huber in 1964, founding the field.

### 3. Formula
```
                  ⎧  ½ · e²                        if | e | ≤ δ
L_δ(e)  =        ⎨
                  ⎩  δ · ( | e | − ½δ )            if | e | >  δ
```
Symbol by symbol:
- **e** = the residual `y − ŷ`
- **δ** (delta) = the threshold separating "ordinary" from "outlier." **Units are the same as y.**
- **½ e²** = the quadratic branch. The ½ exists so the derivative is `e` (clean), not `2e`.
- **δ(|e| − ½δ)** = the linear branch, constructed so the two branches **match in value and in slope at |e| = δ** (the function is C¹ continuous).

The total loss is the mean of `L_δ(eᵢ)` over the dataset.

**The gradient — this is where the robustness lives:**
```
                  ⎧  e                if | e | ≤ δ
dL/dŷ ∝          ⎨
                  ⎩  δ · sign(e)      if | e | >  δ     <-- CAPPED at delta
```
**The gradient is clipped at ±δ.** That single fact is the entire robustness mechanism, and it is worth being able to state in one sentence.

**Limiting behaviour:**
- **δ → ∞** → pure MSE (everything is "ordinary")
- **δ → 0** → behaves like MAE, scaled (everything is an "outlier")

Range [0, ∞), lower better. Units: y's units squared for small errors, y's units for large ones — so Huber loss values are **not directly interpretable** and should be used for training, with MAE/RMSE reported.

### 4. Manual example (δ = 50)

```
Threshold delta = 50. Residual magnitudes: 20,10,10,20,20,20,20,20,20,200

|e| = 20  (<= 50):  quadratic branch  ->  0.5 × 20²  = 0.5 × 400 = 200      [7 times]
|e| = 10  (<= 50):  quadratic branch  ->  0.5 × 10²  = 0.5 × 100 =  50      [2 times]
|e| = 200 ( > 50):  linear branch     ->  50 × (200 − 0.5×50)
                                       =  50 × (200 − 25)
                                       =  50 × 175 = 8,750                  [1 time]

Sum  = 7 × 200 + 2 × 50 + 8,750
     = 1,400 + 100 + 8,750
     = 10,250

Huber loss = 10,250 / 10 = 1,025
```
**Huber loss (δ=50) = 1,025.**

**The comparison that shows the mechanism working:**
```
½ × MSE      = 0.5 × 4,300 = 2,150     <- what pure MSE would charge
Huber (δ=50) =               1,025     <- 52% lower

The outlier's contribution:
  under ½e²:  0.5 × 200² = 20,000      (93% of the total)
  under Huber: 8,750                   (85% of the total)
  -> reduced by 56%
```
**The outlier's influence is cut by more than half** while the nine ordinary observations are treated exactly as MSE would treat them. That is precisely the intended behaviour.

**Choosing δ — a worked sweep:**

| δ | Outlier's charge | Total loss | Behaviour |
|---|---|---|---|
| 10 | 10(200−5) = 1,950 | **310** | Nearly pure MAE — even the ±20 errors are "outliers" |
| 20 | 20(200−10) = 3,800 | **530** | The ±20 errors sit exactly at the boundary |
| **50** | 50(200−25) = 8,750 | **1,025** | Our choice — ordinary errors quadratic, outlier linear |
| 100 | 100(200−50) = 15,000 | **1,650** | Only the extreme point is down-weighted |
| 200 | 0.5(200²) = 20,000 | **2,150** | = ½ MSE. δ ≥ max\|e\| means no robustification at all |

**Key insight from the table: if δ ≥ max|e|, Huber IS MSE.** Setting δ too large is the most common Huber mistake and silently does nothing.

### 5. Python
```python
import numpy as np

def huber_loss(y_true, y_pred, delta=1.0):
    e = np.abs(np.asarray(y_true, float) - np.asarray(y_pred, float))
    quadratic = 0.5 * e ** 2
    linear    = delta * (e - 0.5 * delta)
    return np.mean(np.where(e <= delta, quadratic, linear))

huber_loss(y, y_pred, delta=50)      # 1025.0
huber_loss(y, y_pred, delta=200)     # 2150.0  == 0.5 * MSE

# --- As a training objective ---

# sklearn: HuberRegressor (linear model). Note: 'epsilon' is delta,
# and it is applied to STANDARDISED residuals, so scale your features/target.
from sklearn.linear_model import HuberRegressor
# HuberRegressor(epsilon=1.35, alpha=0.0001).fit(X, y)
#   epsilon=1.35 is the classic default: ~95% statistical efficiency under
#   Gaussian noise while still bounding the influence of outliers.

# sklearn: gradient boosting with a Huber objective
from sklearn.ensemble import GradientBoostingRegressor
# GradientBoostingRegressor(loss='huber', alpha=0.9).fit(X, y)
#   here 'alpha' is the QUANTILE used to set delta adaptively each iteration,
#   not delta itself -- a common source of confusion.

# XGBoost / LightGBM
# XGBRegressor(objective='reg:pseudohubererror')     # smooth Huber approximation
# LGBMRegressor(objective='huber', alpha=1.0)        # alpha here IS delta

# PyTorch / TensorFlow
# torch.nn.HuberLoss(delta=1.0)        # or SmoothL1Loss, which is Huber with delta=1
# tf.keras.losses.Huber(delta=1.0)
```
Line-by-line and the traps:
- **`np.where(e <= delta, quadratic, linear)`** evaluates both branches and selects — fine for numpy, but in a custom autograd loss prefer a masked formulation to avoid NaN gradients.
- **`HuberRegressor`'s `epsilon` is δ, applied to *scaled* residuals.** If you do not standardise, δ=1.35 is meaningless relative to your target's scale. Always `StandardScaler` first.
- **`GradientBoostingRegressor(loss='huber', alpha=0.9)`** — `alpha` is *not* δ. It is the quantile of the absolute residuals used to *set* δ at each boosting iteration, so δ adapts as the fit improves. This adaptive behaviour is usually what you want and removes the need to tune δ manually.
- **`torch.nn.SmoothL1Loss` is Huber with δ = 1** (its `beta` parameter is δ). It is the standard bounding-box regression loss in object detection (Fast R-CNN onwards) for exactly the robustness reason described here.

### 6. Interpretation
The loss value itself is not interpretable (mixed units). **Report MAE and RMSE; use Huber only as the objective.** What you interpret is the *effect*: a Huber-trained model should show MAE close to an MAE-trained model's, with better convergence and less sensitivity to the worst records.

**How to know δ is set sensibly:** check the fraction of residuals exceeding δ.
```python
frac_linear = (np.abs(y - y_pred) > delta).mean()
```
| Fraction in the linear branch | Diagnosis |
|---|---|
| 0% | δ too large — you are doing pure MSE. Increase robustness by lowering δ. |
| **1 – 10%** | **A sensible robust regime** |
| > 30% | δ too small — you are effectively doing MAE, losing the smooth-gradient benefit |

Ours with δ=50: `1/10 = 10%`, at the upper end of sensible for a 10-row example.

### 7. Choosing δ — practical guidance
| Approach | Method | When |
|---|---|---|
| **Classic default** | δ = 1.35 × σ̂ (on standardised residuals, δ = 1.35) | General purpose; gives ~95% efficiency under Gaussian noise |
| **Robust scale** | δ = k × MAD(residuals), k ≈ 1.5–3 | When you want δ to track the data's natural spread |
| **Quantile-based** | δ = the 90th–95th percentile of \|e\| | Directly controls what fraction is treated as an outlier. This is what sklearn's GBM does. |
| **Business threshold** | δ = the error size above which the cost stops growing | The principled choice when you know the cost function |
| **Cross-validation** | Tune δ like any hyperparameter | Always worth doing if you have the budget |

The last one deserves emphasis: **δ has a business meaning — it is the error magnitude beyond which you stop caring proportionally more.** If a delivery more than 30 minutes late is "just late" regardless of whether it is 30 or 300 minutes, then δ = 30 minutes is not a hyperparameter, it is a fact about your business.

### 8. Business use cases
- **Object detection bounding-box regression** — `SmoothL1Loss` (Huber, δ=1) has been the standard since Fast R-CNN, because coordinate targets occasionally contain annotation errors that L2 would chase.
- **Financial and economic time series** — heavy-tailed by nature, with genuine extreme events you must not let dominate the fit.
- **Sensor and IoT data** — occasional spikes from hardware faults.
- **Any dataset with suspected label noise or data-entry errors** — Huber is the safe default when you cannot fully clean the data.
- **Insurance claim severity** — large genuine claims exist, but you do not want a handful of catastrophic claims to define the model for the other 99%.
- **Real-estate valuation** — the exact situation in our running example.
- **Robotics and control** — bounded gradients prevent a single bad reading from producing a violent control action.
- **Robust regression generally** — the default when you want MSE-like behaviour without MSE's fragility.

### 9. Advantages
- **Differentiable everywhere**, including at zero — the key advantage over MAE. Smooth, well-behaved optimisation with clean convergence.
- **Bounded influence** — an arbitrarily extreme observation cannot dominate, because its gradient is capped at δ.
- **Tunable** via δ, so you can dial continuously between MSE and MAE behaviour rather than choosing one.
- **δ can be given a business meaning** (the error size at which cost stops growing proportionally), turning a hyperparameter into a specification.
- Convex, so a unique optimum for linear models.
- Statistically well-founded (the founding M-estimator, with known efficiency properties: 95% efficiency under Gaussian noise at δ=1.35σ).
- Supported natively across sklearn, XGBoost, LightGBM, PyTorch, and TensorFlow.

### 10. Limitations
- **δ must be chosen**, and it is **scale-dependent** — a δ tuned for a target in dollars is meaningless if you switch to thousands of dollars. This is the main practical friction. Standardise, or use a quantile/MAD-based δ.
- **The loss value is not interpretable** (mixed units across the two branches). Always report MAE/RMSE alongside.
- **Not fully robust in the technical sense.** Its influence function is *bounded* but does not *redescend* to zero, so an infinitely extreme outlier still exerts the maximum pull δ. Tukey's biweight redescends (see 7.4) and is more robust — but is non-convex.
- **The optimal predictor is not a clean statistic.** MSE gives the mean, MAE gives the median; Huber gives something in between that depends on δ. So the model's predictions do not have a crisp interpretation, and **totals will not aggregate exactly** (unlike MSE).
- Confusing parameter naming across libraries (`epsilon`, `alpha`, `delta`, `beta` all appear).
- Adds a hyperparameter to tune.
- If your problem genuinely has symmetric quadratic costs, Huber is a needless approximation.

### 11. Common mistakes
1. **Setting δ larger than the largest residual**, which makes Huber identical to MSE while you believe you have robustified the model. **Always check the fraction of residuals in the linear branch.**
2. **Not standardising before `HuberRegressor`**, whose `epsilon` applies to scaled residuals.
3. **Confusing `alpha` in `GradientBoostingRegressor(loss='huber')` with δ.** It is a quantile.
4. **Reporting the Huber loss value as a performance metric.** It has mixed units and no interpretation.
5. Assuming Huber makes the model immune to outliers — it bounds their influence, it does not eliminate it.
6. Using Huber when the real problem is asymmetric cost. Huber is symmetric; you need quantile loss.
7. Tuning δ on the test set.

### 12. Interview questions

**Easy — What is Huber loss?** A loss that is quadratic for small residuals and linear for large ones, with the switch at |e| = δ.

**Easy — ★ Why use Huber instead of MAE or MSE?** It combines MSE's smooth gradients near the optimum (fast, stable convergence, differentiable at zero) with MAE's bounded gradient far from it (robustness to outliers).

**Medium — ★ What happens as δ → 0 and δ → ∞?**
δ → ∞ gives pure MSE (every residual is in the quadratic branch). δ → 0 gives MAE behaviour (every residual is in the linear branch), scaled by δ. So δ is a continuous dial between the two.

**Medium — ★ Explain the robustness mechanism precisely.**
Through the gradient. For MSE the gradient with respect to the prediction is proportional to `e`, unbounded — so an observation with e = 1,000 pulls 100× harder than one with e = 10 and can dominate the entire fit. Huber's gradient is `e` inside the threshold and **clipped to `δ·sign(e)`** outside it. Once an observation exceeds δ, making it more extreme does not increase its pull at all. That bounded influence function is exactly what "robust" means in M-estimation.

**Medium — How do you choose δ in practice?**
Four options, in increasing order of principle. (1) Standardise and use the classic 1.35, which gives ~95% efficiency under Gaussian noise. (2) Set `δ = k × MAD(residuals)` so it tracks the robust spread. (3) Set δ to a high quantile of |e| (the 90th–95th), which directly controls the fraction treated as outliers — this is what sklearn's GBM does adaptively per iteration. (4) **Best: derive δ from the business cost function** — it is the error magnitude beyond which the cost stops growing proportionally. Then validate by checking that 1–10% of residuals fall in the linear branch.

**Hard — Why is Huber's influence function "bounded but not redescending", and does it matter?**
The influence function of an M-estimator is proportional to the derivative of the loss, ψ(e). For Huber, ψ(e) = e for |e| ≤ δ and δ·sign(e) beyond — bounded, but it plateaus at δ rather than returning to zero. So an observation at e = 10⁶ still contributes the maximum influence δ, forever. **Redescending** estimators (Tukey's biweight, Hampel) have ψ(e) → 0 for very large |e|, so extreme outliers are fully *rejected* rather than merely down-weighted. It matters when you have gross errors — a decimal-point mistake making a value 1,000× too large should ideally be ignored entirely, not given maximum weight. The trade-off is that redescending losses are **non-convex**, so optimisation has local minima and needs a good starting point (usually from a Huber or L1 fit). Practical guidance: Huber for ordinary heavy tails; redescending only when you have genuine gross errors and can afford careful initialisation.

**Hard — Huber is a symmetric loss. When is that a problem, and what do you use instead?**
It is a problem whenever the cost of over-prediction differs from the cost of under-prediction — which covers most inventory, capacity, staffing, delivery, and reserving problems. No amount of δ tuning fixes it, because δ controls *outlier sensitivity*, not *direction*. You need **quantile (pinball) loss** to target a specific conditional quantile, or a **custom asymmetric loss** with different multipliers on positive and negative residuals. Note that you can combine the ideas: an asymmetric Huber (different δ and different slope per side) is straightforward to implement and gives you robustness and asymmetry together.

---

## 7.2 LOG-COSH LOSS

### 1. Definition
The logarithm of the hyperbolic cosine of the residual — a smooth approximation to Huber loss with no tuning parameter.

### 2. Intuition
Log-Cosh does what Huber does — quadratic near zero, linear far away — but as a **single smooth analytic expression** with no δ to choose and with derivatives of all orders continuous.

Why that matters: Huber's second derivative is discontinuous at |e| = δ (it jumps from 1 to 0). Optimisers that use curvature — Newton's method, L-BFGS, and crucially the **Hessian-based split-finding in XGBoost and LightGBM** — behave better with a genuinely twice-differentiable loss. Log-Cosh is the "smooth Huber," and it is the reason gradient-boosting libraries offer a "pseudo-Huber" objective.

The cost: **no tuning parameter** means the switch point is fixed at roughly |e| ≈ 1, so **Log-Cosh is only meaningful on standardised or naturally O(1) targets.** On a target in the hundreds of thousands it degenerates to pure MAE.

### 3. Formula
```
L(e)  =  log( cosh(e) )       where  cosh(e) = ( eˣ + e⁻ˣ ) / 2  with x = e
```
**Asymptotic behaviour** (this is why it works):
```
Small |e| :  log(cosh e)  ≈  ½ e²          (Taylor: cosh e ≈ 1 + e²/2, log(1+u) ≈ u)
Large |e| :  log(cosh e)  ≈  |e| − log 2   (since cosh e ≈ e^|e|/2)
```
So it is exactly Huber's shape, with the transition around |e| ≈ 1 and offset by `log 2 ≈ 0.693` in the tail.

**The gradient — elegant and bounded:**
```
dL/de  =  tanh(e)          ->  bounded in (−1, +1) for ALL e
```
**`tanh` is naturally bounded**, so the gradient is capped at ±1 automatically, with no clipping logic. That is the cleanest possible statement of robustness.

**Second derivative:** `d²L/de² = sech²(e) = 1 − tanh²(e)`, smooth and positive everywhere, decaying to 0 in the tails — exactly what Hessian-based optimisers want.

**A scaled variant** with a Huber-like parameter exists and is what libraries actually implement:
```
Pseudo-Huber:  L(e) = δ² ( √(1 + (e/δ)²) − 1 )
```
This has the same quadratic-then-linear shape, is twice differentiable, and restores the δ scale parameter. `objective='reg:pseudohubererror'` in XGBoost is this.

Range [0, ∞), lower better. Numerically, compute it as `|e| + log1p(exp(−2|e|)) − log 2` to avoid `cosh` overflowing for large e.

### 4. Manual example
```
Residual magnitudes: 20,10,10,20,20,20,20,20,20,200

For |e| >> 1, log(cosh e) ≈ |e| − log 2 = |e| − 0.6931

|e| = 10  ->  10  − 0.6931 =   9.3069   [2 times]
|e| = 20  ->  20  − 0.6931 =  19.3069   [7 times]
|e| = 200 -> 200  − 0.6931 = 199.3069   [1 time]

Sum  = 2(9.3069) + 7(19.3069) + 199.3069
     = 18.6137 + 135.1483 + 199.3069
     = 353.069

Log-Cosh = 353.069 / 10 = 35.307
```
**Log-Cosh = 35.31.**

**Compare to MAE = 36.00.** They are almost identical — and that is the lesson:
```
MAE      = 36.000
Log-Cosh = 35.307   = MAE − log 2 = 36 − 0.693 = 35.307   exactly
```
**On our data Log-Cosh has degenerated into MAE minus a constant**, because every residual is far larger than 1. The quadratic region (|e| ≲ 1) is never visited. **Log-Cosh is useless here without rescaling** — a concrete demonstration of its main limitation, and the reason you must standardise the target before using it.

**With a standardised target** (`e/σ`, σ = 193.65), the residuals become 0.103, 0.052, ..., 1.033 — now mostly inside the quadratic region, and Log-Cosh behaves as intended.

### 5. Python
```python
import numpy as np

def logcosh_loss(y_true, y_pred):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    # numerically stable: log(cosh(e)) = |e| + log1p(exp(-2|e|)) - log(2)
    a = np.abs(e)
    return np.mean(a + np.log1p(np.exp(-2 * a)) - np.log(2))

logcosh_loss(y, y_pred)                              # 35.3069
np.mean(np.log(np.cosh(y - y_pred)))                 # 35.3069 (overflows for |e| > ~710)

# Pseudo-Huber (the parameterised, library version)
def pseudo_huber(y_true, y_pred, delta=1.0):
    e = (np.asarray(y_true, float) - np.asarray(y_pred, float)) / delta
    return np.mean(delta**2 * (np.sqrt(1 + e**2) - 1))

pseudo_huber(y, y_pred, delta=50)                    # 925.49

# As a training objective
# XGBRegressor(objective='reg:pseudohubererror')
# tf.keras.losses.LogCosh()
# In PyTorch: torch.log(torch.cosh(e)) or the stable form above
```
- **The naive `np.log(np.cosh(e))` overflows** for |e| beyond about 710 (double-precision limit on `exp`). The stable rearrangement is mandatory in production code and is a good detail to know.
- `pseudo_huber` restores the scale parameter and is what you should reach for on unstandardised targets.

### 6. Interpretation
Not directly interpretable — report MAE/RMSE. Its value is as an objective. The one thing to check: **is the target scaled so that typical residuals are O(1)?** If not, Log-Cosh is just MAE.

### 7. When to use it
| Situation | Verdict |
|---|---|
| Target standardised, want robustness with no tuning | **Log-Cosh — ideal** |
| Using a Hessian-based optimiser (XGBoost, LightGBM, L-BFGS, Newton) | **Log-Cosh / pseudo-Huber — preferred over Huber** |
| Unstandardised target with large values | Use **pseudo-Huber with δ**, or Huber |
| You want explicit control over the outlier threshold | Use **Huber** (δ is interpretable) |
| Asymmetric costs | Neither — use **quantile loss** |

### 8. Business use cases
- **Deep learning regression** where a smooth robust loss is wanted without a hyperparameter — image-to-value regression, depth estimation, keypoint localisation.
- **Gradient boosting** via `reg:pseudohubererror` when the data has heavy tails and you want stable second-order split finding.
- **Optical flow and disparity estimation** in computer vision, where the "Charbonnier penalty" (a pseudo-Huber variant) is standard.
- **Any pipeline that already standardises the target**, where Log-Cosh's fixed transition point is appropriate.
- **Autoencoder and reconstruction losses** on normalised inputs.
- **Robust curve fitting** where you want C² smoothness for a Newton-type optimiser.

### 9. Advantages
- **No hyperparameter** to tune (in the plain form) — the main appeal over Huber.
- **Twice differentiable everywhere**, so it works cleanly with Hessian-based optimisers and with XGBoost/LightGBM's second-order split finding, where Huber's discontinuous second derivative is a genuine nuisance.
- **Naturally bounded gradient** (`tanh ∈ (−1,1)`) with no clipping logic.
- Convex.
- Approximately MSE near zero and MAE far away — the desirable shape.
- Numerically stable when written correctly.

### 10. Limitations
- **The transition point is fixed at |e| ≈ 1**, so it is **scale-dependent in the worst way**: on a large-valued target it silently degenerates to MAE (as our example shows), and on a tiny-valued target to MSE. **You must standardise the target** or use the pseudo-Huber form.
- **Less interpretable than Huber**, whose δ has a direct meaning.
- Loss value has no interpretation.
- The naive implementation overflows.
- Same "bounded but not redescending" caveat as Huber — extreme outliers still exert maximum influence.
- Symmetric, so no help with asymmetric costs.
- Slightly more expensive to compute than Huber (exponentials vs a comparison).

### 11. Common mistakes
1. **Using it on an unstandardised large-valued target** and unknowingly training with MAE. Check whether typical |residual| is O(1).
2. **Implementing `log(cosh(e))` naively** and getting `inf`/`nan` for large residuals.
3. Reporting the loss value as a metric.
4. Assuming "no hyperparameter" means "no scale sensitivity." The opposite is true — the absence of δ is exactly what makes it scale-sensitive.

### 12. Interview questions
**Easy — What shape does Log-Cosh have?** Quadratic near zero, linear far from zero — like Huber, but smooth.
**Medium — ★ Why prefer Log-Cosh over Huber?** Because it is twice differentiable everywhere. Huber's second derivative jumps discontinuously at |e| = δ, which degrades Newton-type and Hessian-based optimisers — notably XGBoost's and LightGBM's second-order split finding. Log-Cosh also removes the δ hyperparameter.
**Medium — Why is its gradient automatically bounded?** Because `d/de log(cosh e) = tanh(e)`, and tanh is bounded in (−1, 1) for all real e. No clipping is needed; the robustness is intrinsic to the function.
**Hard — ★ Your Log-Cosh loss equals your MAE minus 0.693. What does that tell you?**
That every residual is far larger than 1, so the loss is operating entirely in its asymptotic linear regime `|e| − log 2` and the quadratic region is never used. You are effectively training with MAE and getting none of the smoothness benefit. The fix is to **standardise the target** (so typical residuals are O(1)) or to use the **pseudo-Huber form with an explicit δ** matched to your target's scale. This is a good diagnostic to know: compute `logcosh − MAE` and if it is ≈ −0.693 you have the degenerate case.

---

## 7.3 QUANTILE LOSS (PINBALL LOSS)

### 1. Definition
An asymmetric loss that penalises under- and over-prediction with different weights `τ` and `1−τ`, and whose minimiser is the **conditional τ-quantile** of `y | x`.

### 2. Intuition
This is the single most practically important loss in this Part, and the one most under-used relative to its value.

Every metric so far has answered "what is my best guess?" Quantile loss answers a different and often far more useful question: **"what value will I exceed only 10% of the time?"**

Why that matters. Consider promising a delivery time. If you predict the **mean** or **median** you are late **50% of the time** — a terrible customer promise. What you want is the **90th percentile**: a time you will beat 90% of the time. No symmetric loss can produce that. Quantile loss can, by construction.

The mechanism is simple and elegant: **charge more for the error direction you want to avoid.**
- Want to avoid under-prediction (stockouts, late deliveries, insufficient capacity)? Use a **high τ** (0.9, 0.95) so under-prediction is penalised 9–19× more.
- Want to avoid over-prediction (over-ordering perishables, over-provisioning expensive capacity)? Use a **low τ** (0.1, 0.2).
- τ = 0.5 recovers MAE (up to a factor of 2) and the median.

It is also the foundation of **prediction intervals**: train two models at τ = 0.05 and τ = 0.95 and you have a 90% interval, with no distributional assumption whatsoever.

### 3. Formula
```
                  ⎧  τ · e              if e ≥ 0   (under-prediction: y > ŷ)
L_τ(e)  =        ⎨
                  ⎩  (τ − 1) · e        if e <  0   (over-prediction:  y < ŷ)
```
Equivalently, in the form that makes the asymmetry obvious:
```
                  ⎧  τ       · | e |     if under-predicting
L_τ(e)  =        ⎨
                  ⎩  (1 − τ) · | e |     if over-predicting
```
And the compact single-expression form used in implementations:
```
L_τ(e)  =  max( τ · e ,  (τ − 1) · e )
```
Symbol by symbol:
- **e = y − ŷ**, so `e > 0` means the model predicted **too low** (under-prediction)
- **τ (tau)** ∈ (0,1) = the target quantile
- **τ · |e|** is charged for under-prediction; **(1−τ) · |e|** for over-prediction
- The total loss is the mean over observations.

**Reading the asymmetry — memorise this table:**

| τ | Under-pred weight | Over-pred weight | Cost ratio | Model behaves |
|---|---|---|---|---|
| 0.10 | 0.10 | 0.90 | over-prediction 9× worse | Predicts **low** (10th pct) |
| 0.25 | 0.25 | 0.75 | over-prediction 3× worse | Predicts low |
| **0.50** | 0.50 | 0.50 | **equal** | Predicts the **median** (= MAE/2) |
| 0.75 | 0.75 | 0.25 | under-prediction 3× worse | Predicts high |
| 0.90 | 0.90 | 0.10 | under-prediction 9× worse | Predicts **high** (90th pct) |
| 0.95 | 0.95 | 0.05 | under-prediction 19× worse | Predicts very high |

**Setting τ from costs — the formula to remember:**
```
                C_under
τ*  =  ---------------------------
          C_under  +  C_over
```
Example: a stockout costs $500 in lost margin and goodwill; holding one unit of excess costs $5.
```
τ* = 500 / (500 + 5) = 0.990
```
**Forecast the 99th percentile of demand.** That is a rigorous, defensible answer to "how much safety stock?", and it is the *newsvendor solution* from operations research — the same formula, derived from the same logic. Being able to connect quantile loss to the newsvendor problem is a strong interview signal.

Range [0, ∞), lower better. Units: y's units (× the weight), so pinball values are roughly comparable to MAE in magnitude.

### 4. Manual example

**At τ = 0.9** (heavily penalising under-prediction):
```
i    e = y−ŷ    direction        charge
1     −20      over-pred    (1−0.9)×20  = 0.1×20  =   2.0
2     +10      under-pred    0.9    ×10 = 0.9×10  =   9.0
3     −10      over-pred     0.1    ×10           =   1.0
4     +20      under-pred    0.9    ×20           =  18.0
5     −20      over-pred     0.1    ×20           =   2.0
6     +20      under-pred    0.9    ×20           =  18.0
7     −20      over-pred     0.1    ×20           =   2.0
8     +20      under-pred    0.9    ×20           =  18.0
9     −20      over-pred     0.1    ×20           =   2.0
10   +200      under-pred    0.9    ×200          = 180.0
                                                  --------
                                        Σ    =     252.0

Pinball loss (τ=0.9) = 252.0 / 10 = 25.2
```
**Pinball(0.9) = 25.2.**

**The full sweep across τ:**

| τ | Pinball loss | Interpretation |
|---|---|---|
| 0.1 | **10.8** | Only 10% weight on the (dominant) under-predictions |
| 0.5 | **18.0** | = MAE / 2 = 36/2 ✓ |
| 0.9 | **25.2** | 90% weight on under-predictions, which our model commits |

**The τ = 0.5 identity is worth verifying:** `Pinball(0.5) = 0.5 × MAE` exactly, because both directions get weight 0.5. So `2 × Pinball(0.5) = MAE`. Some implementations include the factor of 2 to make this identity exact; sklearn's `mean_pinball_loss` does not.

**Reading the sweep:** our loss *increases* with τ, from 10.8 to 25.2. That tells you the model's errors are **net under-predictions** (its largest error, +200, is an under-prediction). A model that over-predicted would show the opposite pattern. **The direction of the pinball sweep is itself a bias diagnostic.**

### 5. Python
```python
import numpy as np
from sklearn.metrics import mean_pinball_loss

mean_pinball_loss(y, y_pred, alpha=0.1)     # 10.8
mean_pinball_loss(y, y_pred, alpha=0.5)     # 18.0   == MAE/2
mean_pinball_loss(y, y_pred, alpha=0.9)     # 25.2

# By hand
def pinball(y_true, y_pred, tau):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    return np.mean(np.maximum(tau * e, (tau - 1) * e))

pinball(y, y_pred, 0.9)                     # 25.2

# --- Training quantile models ---

# sklearn: linear quantile regression
from sklearn.linear_model import QuantileRegressor
# QuantileRegressor(quantile=0.9, alpha=0.0, solver='highs').fit(X, y)

# sklearn: gradient boosting
from sklearn.ensemble import GradientBoostingRegressor
# GradientBoostingRegressor(loss='quantile', alpha=0.9).fit(X, y)
from sklearn.ensemble import HistGradientBoostingRegressor
# HistGradientBoostingRegressor(loss='quantile', quantile=0.9).fit(X, y)

# LightGBM / XGBoost
# LGBMRegressor(objective='quantile', alpha=0.9)
# XGBRegressor(objective='reg:quantileerror', quantile_alpha=0.9)   # XGBoost >= 2.0

# --- The standard prediction-interval recipe: fit three models ---
models = {}
for q in (0.05, 0.50, 0.95):
    m = GradientBoostingRegressor(loss='quantile', alpha=q, random_state=0)
    # m.fit(X_train, y_train)
    models[q] = m
# lower, median, upper = (models[q].predict(X_test) for q in (0.05, 0.50, 0.95))
# -> a 90% prediction interval with NO distributional assumption

# In model selection
from sklearn.metrics import make_scorer
q90_scorer = make_scorer(mean_pinball_loss, alpha=0.9, greater_is_better=False)
```
Line-by-line and the traps:
- **The parameter is called `alpha` in sklearn's metric and in the GBM losses, `quantile` in `QuantileRegressor` and `HistGradientBoostingRegressor`, and `quantile_alpha` in XGBoost.** Inconsistent naming; check the signature.
- **`np.maximum(tau*e, (tau-1)*e)`** is the whole computation — the max automatically selects the right branch because one term is always negative.
- **You must fit a separate model per quantile.** Three quantiles = three fits. (`HistGradientBoostingRegressor` and LightGBM support this; some libraries now offer multi-quantile fitting in a single model.)
- **Quantile crossing** is a real problem: independently fitted τ=0.05 and τ=0.95 models can produce a lower bound above the upper bound for some inputs. Fixes: sort the predicted quantiles post-hoc, use a monotone-constrained joint model, or use a single distributional model (see Part 8).

### 6. Interpretation
Pinball loss values are roughly on the scale of a weighted MAE and are used for **comparing models at the same τ** — never across different τ, since the weights differ.

**How to validate a quantile model — this is the essential check:** the fraction of actuals falling below the predicted τ-quantile should be ≈ τ.
```python
coverage = (y <= y_pred_q90).mean()      # should be ~0.90 for a good tau=0.9 model
```
| Empirical coverage vs τ | Diagnosis |
|---|---|
| ≈ τ | Well-calibrated quantile |
| < τ | The quantile is too low — under-covering. Intervals too narrow. |
| > τ | The quantile is too high — over-covering. Intervals too wide (conservative). |

This coverage check is the quantile analogue of a calibration curve, and it is mandatory before deploying a quantile model.

### 7. Choosing τ
| Business situation | τ | Reasoning |
|---|---|---|
| Delivery-time promise (want to beat it) | 0.90 – 0.95 | Late is much worse than early |
| Safety stock / inventory (stockout ≫ holding) | 0.90 – 0.99 | τ* = C_under/(C_under + C_over) |
| Perishable inventory (waste ≫ stockout) | 0.30 – 0.60 | Over-ordering destroys the product |
| Cloud/server capacity planning | 0.95 – 0.99 | An outage costs far more than an idle instance |
| Staffing (understaffing hurts service) | 0.80 – 0.90 | Depends on overtime vs SLA cost |
| Loan loss provisioning (regulatory) | 0.95 – 0.999 | Regulators require conservatism |
| Balanced / unknown costs | 0.50 | Recovers the median (= MAE) |
| Prediction interval | pairs, e.g. 0.05 & 0.95 | Gives a 90% interval |

### 8. Business use cases
- **Delivery-time and ETA promises** — the canonical use. Ride-hailing, food delivery, and logistics all quote a high quantile, not a mean.
- **Inventory and safety-stock optimisation** — quantile loss *is* the newsvendor solution, with τ set from the stockout-to-holding cost ratio. This is one of the cleanest metric-to-business mappings in all of ML.
- **Cloud capacity and autoscaling** — provision for the 99th percentile of load, not the mean.
- **Energy demand and peak-load planning** — grid capacity must cover the peak, so the relevant forecast is a high quantile.
- **Financial risk / Value at Risk** — VaR *is* a quantile of the loss distribution, and quantile regression is the direct way to model it.
- **Loan loss provisioning and stress testing** — regulators require conservative (high-quantile) estimates.
- **Probabilistic forecasting competitions** — the M5 "Uncertainty" track was scored on a scaled, weighted pinball loss across nine quantiles.
- **Prediction intervals for any regression model**, distribution-free.
- **Revenue guidance** — companies quote ranges, which are quantiles.
- **Healthcare resource planning** — ICU bed capacity for the 95th-percentile scenario.
- **Construction and project timelines** — the P50/P80/P90 estimates standard in project management are exactly quantiles.

### 9. Advantages
- **Directly encodes asymmetric costs**, which no symmetric loss can. This is its decisive advantage.
- **τ has an exact business derivation:** `τ* = C_under/(C_under + C_over)` — the newsvendor formula. It is a specification, not a hyperparameter.
- **Produces genuine prediction intervals** with **no distributional assumption** — no normality, no homoscedasticity. Enormously valuable in practice.
- **Naturally handles heteroscedasticity**: quantile models learn different spreads in different regions of feature space automatically, which a single point model plus a global σ cannot.
- **Robust** — it is a weighted absolute loss, so it inherits MAE's linear penalty and bounded gradient.
- Convex, so optimisation is well-behaved.
- Reduces to MAE at τ = 0.5, so it generalises rather than replaces.
- Supported in sklearn, LightGBM, XGBoost, and the deep-learning frameworks.
- Its coverage check gives an immediate, interpretable validation criterion.

### 10. Limitations
- **One model per quantile** — three quantiles means three fits, three sets of hyperparameters, and three models to deploy and monitor. Cost and complexity scale with the number of quantiles.
- **Quantile crossing:** independently fitted quantiles can be non-monotonic (predicted 5th percentile above the 95th for some inputs), which is logically incoherent. Requires post-hoc sorting, monotonicity constraints, or a joint model.
- **Not differentiable at e = 0** (like MAE), so convergence is slower and can oscillate.
- **Extreme quantiles (τ < 0.01 or > 0.99) are hard to estimate** — by definition very few data points inform them, so estimates are high-variance. For genuinely extreme tails, extreme-value theory is more appropriate than quantile regression.
- **Loss values are not comparable across τ**, which confuses reporting.
- Requires enough data in the relevant tail; small datasets cannot support high quantiles.
- Predictions are not means, so **they do not aggregate** — the sum of 90th-percentile forecasts is *not* the 90th percentile of the sum (it is far more conservative). This is a genuinely important and often-missed point for hierarchical planning.
- Inconsistent parameter naming across libraries.

### 11. Common mistakes
1. **Using a mean or median prediction for a promise or a capacity decision.** If you promise the median delivery time, you are late half the time. This is the mistake quantile loss exists to prevent, and it is extremely common.
2. **Not validating coverage.** A τ=0.9 model whose actuals fall below the prediction only 72% of the time is broken, and you will not know unless you check.
3. **Ignoring quantile crossing** and shipping incoherent intervals.
4. **Summing high quantiles across a hierarchy** and believing you have the aggregate's high quantile. You have something far more conservative, because quantiles are not additive. Model the aggregate directly, or use a copula/simulation approach.
5. **Choosing τ arbitrarily** instead of deriving it from `C_under/(C_under + C_over)`.
6. **Comparing pinball losses at different τ.**
7. Trying to estimate τ = 0.999 from 500 data points.
8. Confusing the parameter names across libraries (`alpha` vs `quantile` vs `quantile_alpha`).

### 12. Interview questions

**Easy — What is quantile loss?** An asymmetric absolute loss weighting under-prediction by τ and over-prediction by 1−τ; its minimiser is the conditional τ-quantile.

**Easy — What does τ = 0.5 give you?** The conditional median, and the loss equals MAE/2.

**Medium — ★ Why can't you use MSE or MAE for a delivery-time promise?**
Because both are symmetric and both target a central tendency — MSE the mean, MAE the median. If you promise the median you are late 50% of the time, which is a bad customer experience regardless of how accurate the model is. The problem is not accuracy, it is the **choice of functional** — you need a high conditional quantile (say the 90th), and only an asymmetric loss produces one.

**Medium — ★ How do you choose τ from business costs?**
`τ* = C_under / (C_under + C_over)`. If a stockout costs $500 and holding one excess unit costs $5, then τ* = 500/505 = 0.99, so forecast the 99th percentile of demand. This is exactly the **newsvendor solution** from operations research — the critical fractile — which is a nice illustration that quantile regression is the machine-learning version of a classical inventory result.

**Medium — ★ How do you build a prediction interval with quantile loss?**
Fit two models, one at τ = 0.05 and one at τ = 0.95; their predictions bound a 90% prediction interval. The great advantage is that this requires **no distributional assumption** — no normality, no constant variance — and the interval width **adapts to the input**, automatically widening where the data is noisy or sparse. A normal-theory interval (`ŷ ± 1.96σ̂`) assumes constant σ and will be systematically too narrow in high-variance regions and too wide in low-variance ones. Validate by checking that ~90% of actuals fall inside.

**Medium — How do you validate a quantile model?**
Check **empirical coverage**: the fraction of actuals below the predicted τ-quantile should be ≈ τ. Do this overall *and by segment* — a model can have 90% coverage overall while badly under-covering one subgroup. Also check that the quantiles are monotone (no crossing), and report pinball loss at the τ of interest for model comparison.

**Hard — ★ What is quantile crossing and how do you fix it?**
When quantiles are fitted independently, nothing forces `q̂_0.05(x) ≤ q̂_0.50(x) ≤ q̂_0.95(x)` for every x, so for some inputs the "lower bound" exceeds the "upper bound" — logically impossible and embarrassing in production. Fixes, in increasing sophistication: (1) **post-hoc sorting** of the predicted quantiles per observation, which is simple, cheap, and provably does not worsen the pinball loss; (2) **monotonicity-constrained joint estimation**, fitting all quantiles simultaneously with non-crossing constraints; (3) **model a full distribution instead** — a parametric distributional regression (NGBoost, LightGBM with a distributional objective, or a Gaussian/mixture output layer) from which any quantile can be read off coherently by construction; (4) **conformalised quantile regression**, which wraps quantile regression in a conformal calibration step to give finite-sample coverage guarantees while enforcing validity. For most production purposes (1) is sufficient; (3) or (4) if you need principled uncertainty.

**Hard — ★ Why can't you sum 90th-percentile forecasts up a hierarchy?**
Because quantiles are not additive. If `Q_0.9(A)` and `Q_0.9(B)` are the 90th percentiles of two demands, `Q_0.9(A) + Q_0.9(B) ≥ Q_0.9(A + B)` in general, with equality only under perfect positive dependence. Intuitively, it is unlikely that *both* SKUs hit their 90th percentile in the same week, so the sum of the individual 90th percentiles is a much more conservative number than the 90th percentile of the total — this is exactly the risk-pooling effect that makes centralised warehouses need less safety stock than distributed ones. **Consequence:** if you need a high quantile at an aggregate level, either model the aggregate series directly, or simulate the joint distribution (with the correlation structure) and take the quantile of the simulated totals. Naively adding quantiles up a product hierarchy systematically over-provisions and is a common and expensive planning error.

**Hard — Quantile loss vs a custom asymmetric MSE. Which and why?**
Both encode asymmetry, but they target different functionals. Quantile (weighted L1) loss targets a **quantile**, which has a clean probabilistic meaning ("I will exceed this 10% of the time") and is robust. A weighted-squared loss (e.g. `w⁺e²` for e>0, `w⁻e²` for e<0) targets a weighted-mean-like quantity with no clean interpretation, but it retains smooth gradients and penalises large errors more heavily — which matters if the cost is genuinely convex, not just asymmetric. **Decision rule:** if your cost is asymmetric and roughly *linear* in the miss size (per-unit stockout cost, per-minute lateness cost), use quantile loss and derive τ from the cost ratio. If your cost is asymmetric and *convex* (escalating penalties, cascading failures), use an asymmetric squared or asymmetric Huber loss. State the cost function first; the loss follows.

---

## 7.4 EPSILON-INSENSITIVE LOSS AND TUKEY'S BIWEIGHT

Two further losses worth recognising. Both are less common than the above but appear in specific contexts and in interviews.

### 7.4.1 Epsilon-insensitive loss (SVR)

**Definition.** Zero loss inside a tube of width ±ε around the prediction; linear outside it.
```
L_ε(e)  =  max( 0 , | e | − ε )
```
- **ε** = the half-width of the "don't care" tube, in y's units.
- This is the regression counterpart of the **hinge loss** in classification: zero cost once you are "close enough," linear cost beyond. It is the objective of **Support Vector Regression**.

**Intuition.** It encodes a genuinely common business reality: **errors below a tolerance simply do not matter.** If a temperature setpoint within ±0.5 °C is indistinguishable to the occupant, or a delivery within ±5 minutes of the promise counts as on time, then charging *any* penalty inside that band is measuring something nobody cares about.

It also produces **sparse solutions**: only observations outside the tube (the **support vectors**) influence the fit, which is the source of SVR's compactness.

**Manual example (ε = 25):**
```
Residual magnitudes: 20,10,10,20,20,20,20,20,20,200
|e| ≤ 25 -> loss 0  (nine observations!)
|e| = 200 -> 200 − 25 = 175

Sum = 175   ->  mean = 17.5
```
**Loss = 17.5, and nine of ten observations contribute exactly zero.** Only house 10 is a support vector. That is a vivid demonstration of sparsity — and also of the risk: with ε set this wide, the model receives learning signal from a single observation.

**Python**
```python
import numpy as np
def eps_insensitive(y_true, y_pred, epsilon=1.0):
    e = np.abs(np.asarray(y_true, float) - np.asarray(y_pred, float))
    return np.mean(np.maximum(0.0, e - epsilon))

eps_insensitive(y, y_pred, epsilon=25)     # 17.5

from sklearn.svm import SVR, LinearSVR
# SVR(kernel='rbf', epsilon=0.1, C=1.0).fit(X_scaled, y_scaled)
#   ALWAYS scale features AND target for SVR: epsilon and C are scale-dependent.
```
**Use cases:** Support Vector Regression; any problem with an explicit tolerance band (engineering tolerances, temperature control, on-time-delivery windows, measurement precision limits); high-dimensional small-n problems where SVR's margin-based regularisation generalises well.

**Advantages:** encodes a real tolerance; produces sparse, compact models; robust (linear penalty outside the tube); convex.

**Limitations:** ε must be chosen and is scale-dependent (**always scale the target for SVR**); the model receives no gradient from in-tube observations, so a wide ε discards most of the data; kernel SVR scales poorly (roughly O(n²)–O(n³)); the loss value is not interpretable; SVR gives no probabilistic output.

**Interview (Medium) — What is the classification analogue of ε-insensitive loss?** Hinge loss. Both are "zero cost once you are close enough / correct by a margin, linear cost beyond," both produce sparse support-vector solutions, and both underpin SVM-family methods.

**Interview (Hard) — How do you choose ε?** From the business tolerance, not by tuning. It is the error magnitude below which the outcome is operationally identical — measurement precision, a contractual on-time window, a perceptual threshold. If no such tolerance exists, ε is a pure regularisation knob and should be cross-validated (and you should question whether SVR is the right model). A useful diagnostic: check the fraction of observations that are support vectors; if it is under ~10%, ε is too wide and you are discarding most of your data.

### 7.4.2 Tukey's biweight (bisquare) loss

**Definition.** A **redescending** robust loss: quadratic near zero, then flattening, then **completely flat** beyond a cut-off c — so extreme outliers are given **zero** weight.
```
                  ⎧  (c²/6) · [ 1 − ( 1 − (e/c)² )³ ]     if | e | ≤ c
L_c(e)  =        ⎨
                  ⎩  c² / 6                                if | e | >  c
```
- **c** = the rejection threshold (commonly c = 4.685 × σ̂ for 95% Gaussian efficiency)
- Beyond |e| = c the loss is **constant**, so its derivative is **exactly zero** — the observation is fully rejected and exerts no influence at all.

**Why it matters.** Huber's influence function plateaus at δ; Tukey's **redescends to zero**. So a value that is wrong by a factor of 1,000 (a decimal-point error) is *ignored* rather than given maximum weight. This is the strongest form of robustness among the common losses, with a breakdown point that can approach 50%.

**The cost: non-convexity.** The loss is not convex, so there are local minima and the optimiser needs a good starting point — conventionally an L1 or Huber fit. This is why it is rare in mainstream ML despite its superior robustness.

**Python**
```python
import numpy as np
def tukey_biweight(y_true, y_pred, c=4.685):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    r = np.abs(e) / c
    inner = (c**2 / 6) * (1 - (1 - np.minimum(r, 1.0)**2)**3)
    return np.mean(inner)      # equals c^2/6 automatically wherever |e| > c

# In practice: statsmodels RLM with a Tukey norm
# import statsmodels.api as sm
# sm.RLM(y, sm.add_constant(X), M=sm.robust.norms.TukeyBiweight()).fit()
```

**Use cases:** robust regression in the presence of **gross errors** (data-entry mistakes, sensor failures, unit mix-ups); astronomy and physical sciences with contaminated measurements; computer vision robust fitting (RANSAC-adjacent problems); any setting where a fraction of the data is simply wrong rather than merely extreme.

**Limitations:** **non-convex** (local minima, needs careful initialisation); c must be tuned and is scale-dependent; can *reject genuine* extreme observations, which is dangerous if the tail is real and important (insurance catastrophes, peak loads); rarely available in ML libraries; loss value uninterpretable.

**Interview (Hard) — ★ Huber vs Tukey: when would you accept non-convexity?**
When you have **gross errors** rather than a heavy tail. Huber's influence function is bounded but plateaus, so a value that is 1,000× too large — a decimal-point typo — still exerts the maximum pull δ on the fit. Tukey's redescends to zero, so such a point is fully rejected. I would accept the non-convexity when (a) I have concrete evidence of gross data errors that I cannot clean upstream, (b) I can initialise from an L1 or Huber fit to land in the right basin, and (c) the extreme values are genuinely *errors* rather than genuinely *rare events*. That last condition is the crucial one: in insurance or peak-load forecasting the extremes are real and economically decisive, and rejecting them would be catastrophic. **The question is always "is this observation wrong, or is it rare?" — Tukey assumes wrong, Huber hedges, MSE assumes rare and important.**

## 7.5 Robust and asymmetric loss summary on the running example

| Loss | Parameter | Value | Symmetric? | Optimal predictor | Outlier handling |
|---|---|---|---|---|---|
| MSE (÷2 for comparison) | — | 2,150.0 | Yes | Conditional mean | Chases them |
| **Huber** | δ = 50 | **1,025.0** | Yes | Between mean and median | Bounded influence |
| Pseudo-Huber | δ = 50 | 925.5 | Yes | As Huber, C² smooth | Bounded influence |
| MAE | — | 36.0 | Yes | Conditional median | Linear penalty |
| **Log-Cosh** | — (fixed ≈1) | **35.3** | Yes | Mean-ish | Bounded gradient (tanh) |
| ε-insensitive | ε = 25 | 17.5 | Yes | A tube, not a point | Ignores small errors |
| **Pinball** | τ = 0.1 | **10.8** | **No** | 10th percentile | Linear, weighted |
| **Pinball** | τ = 0.5 | **18.0** | Yes | Median (= MAE/2) | Linear |
| **Pinball** | τ = 0.9 | **25.2** | **No** | 90th percentile | Linear, weighted |
| Tukey biweight | c = 4.685σ | (rejects house 10) | Yes | Mean of inliers | Full rejection |

**How to choose, in one table:**

| Your situation | Loss |
|---|---|
| Symmetric cost, no outliers, need the mean/total | **MSE** |
| Symmetric cost, outliers present, want interpretability | **MAE** |
| Symmetric cost, outliers present, want smooth optimisation | **Huber** (δ from business or a quantile of \|e\|) |
| As above, using a Hessian-based optimiser or a standardised target | **Log-Cosh / pseudo-Huber** |
| **Asymmetric cost** | **Pinball**, τ = C_under/(C_under + C_over) |
| Need a prediction interval | **Pinball at two quantiles** |
| An explicit tolerance band exists | **ε-insensitive** |
| Gross data errors you cannot clean | **Tukey** (initialise from Huber) |
| Positive skewed target, relative error matters | **MSLE**, or Gamma/Tweedie with a log link |
| Count target | **Poisson deviance** (negative binomial if over-dispersed) |

**The single most important sentence in Part 7:** a mismatch between your cost function and your loss function cannot be fixed by choosing a different *reporting metric*. If under-prediction costs ten times more than over-prediction, you must **train** on an asymmetric loss. Reporting MAE more carefully will not help.

---

# PART 8 — Probabilistic Regression Metrics

## 8.0 Why point predictions are not enough

Every metric so far scores a **single number** against a single truth. But many decisions need to know **how uncertain** the prediction is:

- "The house is worth $420k" → useless for a lender. "$420k ± $30k" changes the loan-to-value decision.
- "Demand will be 1,000 units" → you cannot set safety stock. "1,000 with a 90% chance of being under 1,350" you can.
- "The patient's glucose will be 7.2" → a clinician needs to know whether 12.0 is plausible.
- An autonomous vehicle estimating distance needs to know when it *does not know*.

**This is the exact regression analogue of the calibration discussion in classification.** There, a classifier that outputs 0.7 must be right 70% of the time for that number to be usable in a formula. Here, a regressor that outputs a 90% interval must contain the truth 90% of the time.

**The two things you must measure, and they are independent:**

| Property | Question | Metrics |
|---|---|---|
| **Sharpness** | Are my intervals *narrow*? | MPIW, interval width, predictive σ |
| **Calibration / Coverage** | Do my intervals *contain the truth* at the stated rate? | PICP, coverage, PIT histogram |

**The trade-off is the whole game.** An interval of `(−∞, +∞)` has perfect coverage and zero value. An interval of zero width is maximally sharp and never contains the truth. The goal, in Gneiting's formulation, is: **maximise sharpness subject to calibration.** Metrics like CRPS and NLL combine both into one number; PICP and MPIW separate them for diagnosis.

**Three ways to produce a probabilistic forecast:**

| Approach | Output | Metric |
|---|---|---|
| **Parametric** — predict μ and σ | A distribution (e.g. Normal(μ,σ)) | Gaussian NLL, CRPS |
| **Quantile** — predict several quantiles | A set of quantiles | Pinball loss, Interval Score |
| **Ensemble / sample** — produce N samples | An empirical distribution | Empirical CRPS, energy score |

---

## 8.1 GAUSSIAN NEGATIVE LOG-LIKELIHOOD (NLL)

### 1. Definition
The negative log of the probability density that the model's predicted distribution assigns to the observed value, averaged over observations, under a Gaussian assumption.

### 2. Intuition
NLL is the direct regression analogue of **Log Loss** in classification, and it behaves the same way: **it rewards putting high probability density on what actually happened, and punishes confident wrongness brutally.**

The mechanism, which is worth spelling out because it is elegant: the model outputs both a mean μ and a standard deviation σ. The loss contains two competing terms:
- `(y − μ)² / (2σ²)` — the squared error, **scaled down by σ².** So the model can reduce this term by claiming a *large* σ.
- `½ ln(σ²)` — a **penalty for claiming a large σ.** So it cannot just declare infinite uncertainty.

**The model is forced to be honest about its uncertainty.** If it says σ is small it had better be accurate; if it is inaccurate it must admit a large σ, and pay for it. This is what makes NLL a **proper scoring rule** — the expected loss is minimised only by reporting the true predictive distribution.

An immediate consequence, and a good interview point: **when σ is fixed and constant, minimising Gaussian NLL is exactly minimising MSE.** NLL is the generalisation of MSE to the case where the model also predicts its own uncertainty. This is the regression mirror of "Log Loss generalises accuracy by scoring the probability, not the label."

### 3. Formula

**Per observation:**
```
                      1                        ( yᵢ − μᵢ )²
NLLᵢ  =  −ln p(yᵢ) =  ─ ln( 2π σᵢ² )  +  ────────────────────
                      2                          2 σᵢ²
```
Symbol by symbol:
- **yᵢ** = the observed value
- **μᵢ** = the model's predicted **mean** for observation i
- **σᵢ** = the model's predicted **standard deviation** for observation i (note: **per observation** — this is what allows heteroscedastic modelling)
- **σᵢ²** = the predicted variance
- **½ ln(2π σᵢ²)** = the **normalisation / sharpness penalty**. It grows with σ, so over-claiming uncertainty is punished. The `2π` is the Gaussian normalising constant and contributes a fixed `½ ln(2π) ≈ 0.9189`.
- **(yᵢ − μᵢ)²/(2σᵢ²)** = the **accuracy term**, the squared error divided by the claimed variance. This is a *standardised* squared error — the z-score squared, halved.

**Averaged over the dataset:**
```
             1    n  ⎡  1                    ( yᵢ − μᵢ )²  ⎤
NLL  =  ───  ×   Σ   ⎢ ─── ln( 2π σᵢ² )  +  ─────────────  ⎥
             n   i=1 ⎣  2                       2 σᵢ²      ⎦
```
Range **(−∞, +∞)** — and note it can be **negative**, because a probability *density* can exceed 1 when σ is small. This surprises people. Lower is better.

**The homoscedastic special case:** if σᵢ = σ for all i, then
```
NLL = ½ ln(2πσ²) + MSE/(2σ²)
```
which is minimised over σ at `σ² = MSE`, giving `NLL = ½ ln(2πe·MSE)`. So with a single fitted σ, **NLL is a monotone function of MSE** — it adds nothing. NLL only earns its keep when σ varies with x.

### 4. Manual example

Three observations, with the model predicting both a mean and a standard deviation:

| i | y | μ | σ | z = (y−μ)/σ | ½ln(2πσ²) | (y−μ)²/(2σ²) | NLLᵢ |
|---|---|---|---|---|---|---|---|
| 1 | 10 | 9 | 2 | +0.5 | 1.61209 | 1/8 = 0.12500 | **1.73709** |
| 2 | 20 | 22 | 2 | −1.0 | 1.61209 | 4/8 = 0.50000 | **2.11209** |
| 3 | 30 | 30 | 5 | 0.0 | 2.52838 | 0/50 = 0.00000 | **2.52838** |

**Working for observation 1:**
```
σ² = 4
½ ln(2π × 4) = ½ ln(25.13274) = ½ × 3.22417 = 1.61209
(10 − 9)² / (2 × 4) = 1/8 = 0.12500
NLL₁ = 1.61209 + 0.12500 = 1.73709
```
**Working for observation 3** — the instructive one:
```
σ² = 25
½ ln(2π × 25) = ½ ln(157.0796) = ½ × 5.05676 = 2.52838
(30 − 30)² / (2 × 25) = 0
NLL₃ = 2.52838 + 0 = 2.52838
```
```
Mean NLL = (1.73709 + 2.11209 + 2.52838) / 3 = 6.37756 / 3 = 2.12585
```
**Gaussian NLL = 2.1258.**

**Now read observation 3 carefully, because it is the entire point of NLL.** The model's mean was **exactly right** (μ = 30, y = 30) — a perfect point prediction, zero squared error. Yet it has the **worst NLL of the three** (2.528), because it claimed σ = 5 when it did not need to. **NLL punishes unwarranted uncertainty even when the point prediction is perfect.** No point metric can do that. Conversely, observation 1 has a non-zero error but a confident, appropriate σ, and scores best.

**The over-confidence penalty, demonstrated:** suppose observation 2 had claimed σ = 0.5 instead of 2.
```
½ ln(2π × 0.25) = ½ ln(1.5708) = 0.22579
(20 − 22)² / (2 × 0.25) = 4 / 0.5 = 8.00000
NLL = 0.22579 + 8.00000 = 8.22579        <- vs 2.11209 at sigma = 2
```
**Nearly 4× worse.** Claiming false confidence is catastrophic under NLL, exactly as claiming 0.99 probability on a false class is catastrophic under Log Loss.

### 5. Python
```python
import numpy as np
from scipy import stats

def gaussian_nll(y_true, mu, sigma):
    y_true, mu, sigma = (np.asarray(a, float) for a in (y_true, mu, sigma))
    sigma = np.maximum(sigma, 1e-6)                    # guard against sigma -> 0
    return np.mean(0.5 * np.log(2 * np.pi * sigma**2) + (y_true - mu)**2 / (2 * sigma**2))

y3  = np.array([10., 20., 30.])
mu3 = np.array([ 9., 22., 30.])
sd3 = np.array([ 2.,  2.,  5.])

gaussian_nll(y3, mu3, sd3)                             # 2.12585
-np.mean(stats.norm.logpdf(y3, loc=mu3, scale=sd3))    # 2.12585  (identical)

# --- Models that predict mu AND sigma ---

# PyTorch: a two-headed network
# torch.nn.GaussianNLLLoss()            # takes (mu, target, var) -- note: VARIANCE, not sd
# A network outputs mu and log(var); exponentiate log(var) for numerical stability.

# NGBoost: natural-gradient boosting for distributional regression
# from ngboost import NGBRegressor
# NGBRegressor(Dist=Normal).fit(X, y); ngb.pred_dist(X_test).params  # {'loc':..,'scale':..}

# LightGBM / statsmodels: GLMs with a variance function, or a two-stage
# mean-then-residual-variance model

# sklearn: GaussianProcessRegressor returns mu and sigma natively
# from sklearn.gaussian_process import GaussianProcessRegressor
# mu, sigma = gp.predict(X_test, return_std=True)
```
Line-by-line and the traps:
- **`np.maximum(sigma, 1e-6)`** is essential. Nothing in the loss prevents the optimiser from driving σ → 0 on an easy observation, and `1/(2σ²)` then explodes. Every production implementation clamps σ or parameterises `log σ`.
- **`torch.nn.GaussianNLLLoss` takes the VARIANCE, not the standard deviation.** Passing σ where σ² is expected is a very common bug that silently produces a mis-specified model.
- **Always predict `log σ` and exponentiate**, never σ directly — this guarantees positivity and improves conditioning.
- **`stats.norm.logpdf`** is the cleanest reference implementation for testing your own.

### 6. Interpretation

NLL values are **not comparable across datasets** (they depend on the target's scale — the `ln σ²` term carries units) and can be negative. Interpret via:

**(a) Against a baseline.** The natural baseline is a constant Gaussian fitted to the target: `μ = ȳ`, `σ = σ_y`. Its NLL is `½ ln(2πe σ_y²)`. Any useful model must beat it.
```python
baseline_nll = 0.5 * np.log(2 * np.pi * np.e * y.var())
```
For our house data: `0.5 × ln(2π × e × 37500) = 0.5 × ln(640,589) = 6.685`.

**(b) As a per-observation likelihood.** `exp(−NLL)` is the geometric mean predictive density. Its units are 1/y-units, so it is only useful for relative comparison.

**(c) By decomposing it.** Split the average into the sharpness term and the accuracy term:
```python
sharp = np.mean(0.5*np.log(2*np.pi*sd3**2))     # 1.9175
acc   = np.mean((y3-mu3)**2/(2*sd3**2))         # 0.2083
```
Ours: 1.918 from sharpness, 0.208 from accuracy → **the loss is dominated by the width of the intervals, not by the point errors.** That is an actionable finding: the model should be more confident.

### 7. Good vs bad values
Always report **NLL minus the baseline NLL** (an information gain, in nats). Positive means the model is worse than a constant Gaussian.

| NLL − baseline NLL | Meaning |
|---|---|
| > 0 | Worse than a constant Gaussian — the model is broken |
| −0.1 | Marginal |
| −0.5 | Meaningful |
| −1.0 | Strong (predictive density ~2.7× higher on average) |
| −2.0 | Excellent |

### 8. Business use cases
- **Training deep probabilistic models** — a two-headed network outputting μ and log σ, trained on NLL, is the standard recipe for heteroscedastic deep regression.
- **Gaussian Processes** — NLL (the marginal likelihood) is both the training objective and the model-selection criterion for kernel hyperparameters.
- **NGBoost and distributional gradient boosting.**
- **Weather forecasting ensembles** — probabilistic verification is the field's core competence.
- **Financial risk and volatility modelling** — GARCH-family models are fitted by maximum likelihood, i.e. by minimising NLL, precisely because σ varies over time.
- **Bayesian model comparison** — the log predictive density is the fundamental quantity (WAIC, LOO-CV).
- **Anomaly detection** — an observation with very high NLL under the predictive distribution is an anomaly, and the metric doubles as the detector.
- **Autonomous systems** — knowing when the model does not know is a safety requirement, and NLL is how you train and validate it.
- **Insurance pricing** — the premium depends on the whole loss distribution, not just its mean.

### 9. Advantages
- **A proper scoring rule** — cannot be gamed by misstating uncertainty; minimised only by the true predictive distribution.
- **Scores the full distribution**, capturing both accuracy and calibrated uncertainty in one number.
- **Naturally handles heteroscedasticity** — σ can be a function of x, learned automatically.
- **Differentiable**, so it is directly usable as a training objective (unlike coverage metrics).
- **Generalises MSE**: with constant σ it reduces to MSE, so it strictly extends the familiar case.
- Extends to any parametric family (Student-t for heavy tails, Gamma for positive skew, Poisson/negative binomial for counts, mixtures for multimodality).
- Theoretically grounded (maximum likelihood, KL divergence, information theory).

### 10. Limitations
- **Assumes a distributional family.** Gaussian NLL is wrong for skewed, bounded, or multimodal targets, and a mis-specified family gives confidently wrong uncertainty. Use Student-t, Gamma, or a mixture as appropriate.
- **Unbounded and dominated by outliers** — the accuracy term `(y−μ)²/(2σ²)` grows without limit, so one observation the model was confident about and wrong on can dominate the average. Exactly the same weakness as Log Loss. **CRPS is the bounded alternative** (see 8.2).
- **Numerically fragile:** σ → 0 makes the loss → −∞, so it must be clamped. Training can collapse to "predict tiny σ on the easy points" without care.
- **Not interpretable** — the value has awkward units, can be negative, and is not comparable across datasets. Always report against a baseline.
- **Requires a model that outputs uncertainty**, which excludes most off-the-shelf regressors.
- Being scale-dependent, it cannot be compared across targets.
- The `σ` it learns is the *predictive* uncertainty only if the model is well specified; a mis-specified mean function will be absorbed into an inflated σ, masking the real problem.

### 11. Common mistakes
1. **Passing σ where σ² is expected** (or vice versa) — especially `torch.nn.GaussianNLLLoss`, which wants variance.
2. **Not clamping σ**, leading to divergence or `nan`.
3. **Predicting σ directly instead of log σ**, allowing negative values.
4. **Reporting a raw NLL with no baseline.** The number is uninterpretable alone.
5. **Being surprised that NLL is negative.** Densities can exceed 1.
6. **Using Gaussian NLL on a skewed or bounded target** (prices, counts, durations) — the intervals will extend below zero and the tails will be wrong.
7. **Comparing NLL across datasets or after a target transformation.**
8. Fitting a single global σ and reporting NLL as if it added information beyond MSE. It does not.

### 12. Interview questions

**Easy — What is Gaussian NLL?** The negative log predictive density under a Normal(μ, σ) model, averaged over observations. It scores the whole predicted distribution, not just the mean.

**Easy — Can NLL be negative?** Yes. It is a density, not a probability, and a density can exceed 1 when σ is small, making its log positive and the negative log negative.

**Medium — ★ Why does NLL force the model to be honest about its uncertainty?**
Because the two terms pull in opposite directions. The accuracy term `(y−μ)²/(2σ²)` gets smaller as σ grows, so the model would like to claim huge uncertainty. But the sharpness term `½ln(2πσ²)` gets larger as σ grows, so it pays a price for doing so. The minimum of the sum is achieved at the σ that actually matches the model's typical error. That is exactly what makes it a **proper scoring rule**: you cannot improve your score by lying about your confidence in either direction.

**Medium — ★ Relate Gaussian NLL to MSE.**
With a **fixed, constant** σ, `NLL = ½ln(2πσ²) + MSE/(2σ²)`, so NLL is a monotone increasing function of MSE and the two are equivalent for ranking models. Minimising over σ as well gives `σ̂² = MSE` and `NLL = ½ln(2πe·MSE)`. So **MSE is the special case of Gaussian NLL with homoscedastic noise**, and NLL earns its keep only when σ is allowed to vary with x. That is the crisp answer.

**Medium — Why must you predict `log σ` rather than σ?**
Because σ must be strictly positive, and an unconstrained network output can be negative. Parameterising `s = log σ` and using `σ = exp(s)` enforces positivity automatically, gives better conditioning (the loss becomes `s + (y−μ)²e^(−2s)/2 + const`, which is well-behaved), and avoids the need for clipping or a softplus that can saturate.

**Hard — ★ Your NLL is excellent but your prediction intervals under-cover. How?**
This is possible and instructive. NLL is an *average* over observations, so it can be minimised by being very sharp and well-calibrated on the majority of easy observations while being badly over-confident on a minority of hard ones. The average looks good; the coverage — which is a *frequency*, not an average of densities — fails. Diagnosis: (1) compute **coverage by bin of predicted σ** — over-confidence usually concentrates in one region; (2) plot the **PIT histogram** (see 8.4), which will show excess mass at the extremes; (3) check for a **mis-specified family** — heavy-tailed real errors under a Gaussian assumption produce exactly this signature, and switching to a Student-t often fixes it; (4) check whether σ has collapsed on the training set (over-fitting the variance head). Remedies: a heavier-tailed family, variance regularisation, ensembling to capture epistemic as well as aleatoric uncertainty, or **conformal calibration** which gives distribution-free finite-sample coverage guarantees regardless of the model's own σ.

**Hard — Aleatoric vs epistemic uncertainty, and which does NLL capture?**
**Aleatoric** uncertainty is irreducible noise in the data-generating process — two identical houses selling for different prices. **Epistemic** uncertainty is the model's ignorance, from limited data or limited capacity, and it *is* reducible with more data. A single network trained on NLL with a σ head captures **aleatoric** uncertainty: it learns how noisy the target is in each region of feature space. It does **not** capture epistemic uncertainty — it will be confidently wrong far from the training data, which is the classic failure mode of deep regression on out-of-distribution inputs. To capture epistemic uncertainty you need **deep ensembles** (train several models, and the spread of their μ predictions is epistemic), MC dropout, Bayesian neural networks, or Gaussian Processes (which give epistemic uncertainty analytically and grow it away from the data). Deep ensembles of NLL-trained networks capture both: total predictive variance ≈ mean of the σ² (aleatoric) + variance of the μ (epistemic). This decomposition is a strong answer.

---

## 8.2 CONTINUOUS RANKED PROBABILITY SCORE (CRPS)

### 1. Definition
The integrated squared difference between the predicted cumulative distribution function and the step function at the observed value.

### 2. Intuition
CRPS is the **regression analogue of the Brier score**, and it plays the same role: a **bounded, robust, proper scoring rule** for probabilistic forecasts, and the safer alternative to NLL when confident errors would otherwise dominate.

The picture is the clearest way to understand it. Your forecast is a CDF `F(x)`. Reality is a step function that jumps from 0 to 1 at the observed value y. **CRPS is the area between those two curves, squared:**

```
  1.0 |                    ,--------------------  <- reality: step at y
      |                   ,|
      |          ,,''''''  |
  F(x)|      ,,''    ####  |     ### = the squared gap being integrated
      |   ,,''       ####  |
      | ,''          ####  |
  0.0 |''            ####  |
      +----------------------------------------
                          y
                     observed value
```
- A **sharp, accurate** forecast (steep CDF centred on y) → small area → low CRPS.
- A **sharp, wrong** forecast → large area → high CRPS, but **bounded** (unlike NLL, which goes to infinity).
- A **wide, vague** forecast → moderate area regardless of where y falls → moderate CRPS.

So CRPS penalises both miscalibration and lack of sharpness, in one number, without ever exploding.

**Two properties make it the practitioner's favourite:**
1. **It is in the units of y.** CRPS = 1.01 means "about 1.01 units," directly comparable to MAE.
2. **It reduces to MAE for a deterministic (point) forecast.** So CRPS *generalises MAE* to probabilistic forecasts — which means you can compare a probabilistic model to a point model on the same scale. Nothing else lets you do that.

### 3. Formula

**The definition:**
```
                ∞
CRPS(F, y)  =  ∫   [ F(x) − 1{x ≥ y} ]²  dx
               −∞
```
Symbol by symbol:
- **F(x)** = the model's predicted CDF evaluated at x
- **1{x ≥ y}** = the indicator (Heaviside step) function: 0 for x < y, 1 for x ≥ y — the "perfect" CDF for the observed outcome
- **[ ... ]²** = the squared vertical gap between the two curves at each x
- **∫ dx** = integrate over the whole real line, in the units of y

**The closed form for a Gaussian forecast** `F = N(μ, σ)` — this is the version you compute:
```
CRPS( N(μ,σ), y )  =  σ [ z ( 2Φ(z) − 1 )  +  2φ(z)  −  1/√π ]

                                 y − μ
                       where  z = ───── ,
                                   σ
                       Φ = standard normal CDF,  φ = standard normal PDF
```
- **z** = the standardised error (the z-score)
- **z(2Φ(z) − 1)** = the accuracy term, growing roughly linearly in |z|
- **2φ(z)** = a sharpness term
- **1/√π ≈ 0.5642** = a constant offset ensuring CRPS = 0 for a perfect deterministic forecast

**The ensemble / sample form** (when you have N samples rather than a parametric distribution) — the **energy form**, which is how CRPS is usually computed in practice:
```
                    1   N                    1     N   N
CRPS  ≈  E|X − y| − ─ E|X − X'|  =  ───  Σ |xᵢ − y|  −  ─────  Σ  Σ |xᵢ − xⱼ|
                    2                N   i=1            2N²   i=1 j=1
```
- **First term** = mean absolute distance from the samples to the truth → rewards accuracy
- **Second term** = mean absolute pairwise distance among the samples → *rewards sharpness*, since it is subtracted (a tight ensemble has small spread and loses less)
- This form makes the sharpness-vs-accuracy trade-off explicit and is the easiest to reason about.

**The quantile decomposition** — the bridge to Part 7:
```
              1
CRPS  =  2 ∫    PinballLoss_τ  dτ
             0
```
**CRPS is the pinball loss integrated over all quantile levels.** So minimising CRPS is minimising the average pinball loss across every τ — which is exactly why the M5 Uncertainty competition's weighted-pinball metric over nine quantiles is a discretised CRPS. This identity is one of the most satisfying results in forecast verification and an excellent thing to be able to state.

Range **[0, ∞)**, lower better, **units of y**. `CRPS = 0` only for a point mass exactly at y.

### 4. Manual example

Using the same three observations as the NLL example:

| i | y | μ | σ | z = (y−μ)/σ | Φ(z) | φ(z) | CRPSᵢ |
|---|---|---|---|---|---|---|---|
| 1 | 10 | 9 | 2 | +0.5 | 0.691462 | 0.352065 | **0.662807** |
| 2 | 20 | 22 | 2 | −1.0 | 0.158655 | 0.241971 | **1.204883** |
| 3 | 30 | 30 | 5 | 0.0 | 0.500000 | 0.398942 | **1.168475** |

**Full working for observation 1:**
```
z = (10 − 9)/2 = 0.5
Φ(0.5) = 0.691462     φ(0.5) = 0.352065

Step 1 — accuracy term:  z(2Φ(z) − 1) = 0.5 × (2×0.691462 − 1)
                                       = 0.5 × 0.382925 = 0.191462
Step 2 — sharpness term: 2φ(z) = 2 × 0.352065 = 0.704131
Step 3 — constant:       1/√π = 0.564190
Step 4 — bracket:        0.191462 + 0.704131 − 0.564190 = 0.331403
Step 5 — multiply by σ:  CRPS₁ = 2 × 0.331403 = 0.662807
```
**Full working for observation 3** — again the instructive one:
```
z = 0            Φ(0) = 0.5        φ(0) = 0.398942
bracket = 0×(2×0.5 − 1) + 2(0.398942) − 0.564190
        = 0 + 0.797885 − 0.564190 = 0.233694
CRPS₃ = 5 × 0.233694 = 1.168475
```
```
Mean CRPS = (0.662807 + 1.204883 + 1.168475)/3 = 3.036165/3 = 1.012055
```
**CRPS = 1.0121 (in the units of y).**

**Compare the two proper scoring rules on the identical data:**
```
              obs 1     obs 2     obs 3     mean
NLL          1.737     2.112     2.528     2.126
CRPS         0.663     1.205     1.168     1.012
```
**Both agree that observation 1 is best and observation 2 is worst.** But look at the *magnitude* of disagreement: NLL rates observation 3 (perfect mean, wide σ) as the **worst**; CRPS rates it as **middle**, slightly better than observation 2. Why? Because NLL's `½ln(2πσ²)` term punishes width logarithmically and unboundedly, while CRPS's penalty for width is linear in σ and gentler. **CRPS is more forgiving of over-cautious forecasts and much more forgiving of confidently-wrong ones.** That difference in temperament is the practical reason to prefer CRPS for reporting and NLL for training.

**A key sanity check — the deterministic limit.** Let σ → 0 for observation 1 (a point forecast of 9 when the truth is 10):
```
As σ -> 0, CRPS -> |y − μ| = |10 − 9| = 1.0
```
**CRPS collapses to absolute error.** So a point forecaster's CRPS *is* its MAE, and a probabilistic forecaster with CRPS below the point forecaster's MAE is genuinely adding value. This is the single most useful practical fact about CRPS.

### 5. Python
```python
import numpy as np
from scipy.stats import norm

def crps_gaussian(y_true, mu, sigma):
    """Closed-form CRPS for a Gaussian predictive distribution. Units of y."""
    y_true, mu, sigma = (np.asarray(a, float) for a in (y_true, mu, sigma))
    sigma = np.maximum(sigma, 1e-12)
    z = (y_true - mu) / sigma
    return np.mean(sigma * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1/np.sqrt(np.pi)))

crps_gaussian(y3, mu3, sd3)            # 1.012055

def crps_ensemble(y_true, samples):
    """
    Empirical CRPS from an ensemble/sample. samples shape (n_obs, n_samples).
    Uses the energy form: E|X-y| - 0.5*E|X-X'|
    """
    y_true  = np.asarray(y_true, float)[:, None]
    samples = np.asarray(samples, float)
    n = samples.shape[1]
    term1 = np.abs(samples - y_true).mean(axis=1)
    term2 = np.abs(samples[:, :, None] - samples[:, None, :]).sum(axis=(1, 2)) / (2 * n**2)
    return np.mean(term1 - term2)

# The deterministic limit: CRPS of a point forecast == MAE
crps_gaussian(y, y_pred, np.full_like(y, 1e-9))        # 36.0  == MAE
np.abs(y - y_pred).mean()                              # 36.0

# Libraries
# import properscoring as ps;  ps.crps_gaussian(y, mu, sig);  ps.crps_ensemble(y, samples)
# scoringrules (modern, fast, many distributions)
```
Line-by-line:
- **`crps_gaussian` is the workhorse.** Memorise the closed form; it is short and appears in interviews.
- **`crps_ensemble`'s pairwise term is O(N²) in memory** for the naive broadcast shown. For large ensembles use the sorted formulation, which is O(N log N): `CRPS = (2/N²) Σᵢ (xᵢ − y)(N·1{y<xᵢ} − i + ½)` with x sorted.
- **The deterministic-limit check is worth putting in your test suite** — it verifies your implementation against MAE.

### 6. Interpretation

CRPS is in the units of y, so interpret it **exactly as you would interpret MAE** — with the crucial extra fact that it accounts for the whole distribution.

**The single most useful comparison:**
```
CRPS_probabilistic_model   vs   MAE_point_model
```
If CRPS < MAE of your best point model, the probabilistic forecast is genuinely better *as a decision input*, not merely more informative.

**Skill score form** (recommended for reporting):
```
CRPSS  =  1 − CRPS_model / CRPS_baseline
```
where the baseline is typically the climatological distribution (the unconditional distribution of y) or a naive/persistence probabilistic forecast. `CRPSS = 1` is perfect, `0` is no better than the baseline, negative is worse. This is the direct analogue of the Brier Skill Score.

### 7. Good vs bad values
| Reference | Reading |
|---|---|
| CRPS vs MAE of a point model | Below it → the probabilistic model adds value |
| CRPS vs σ(y) | Below ~0.3 σ(y) is strong |
| CRPSS vs climatology | > 0.3 meaningful, > 0.5 strong, > 0.7 excellent |

### 8. Business use cases
- **Weather and climate forecasting** — CRPS is *the* standard verification metric for probabilistic forecasts at every major meteorological centre. This is its home field.
- **Energy load and price forecasting** — probabilistic forecasts drive reserve procurement, and CRPS is the standard score in the Global Energy Forecasting Competitions.
- **Retail demand forecasting with uncertainty** — the M5 Uncertainty track used a weighted-scaled-pinball metric that is a discretised CRPS.
- **Hydrology and flood forecasting** — probabilistic river-level forecasts.
- **Renewable generation forecasting** (wind, solar) — inherently uncertain, and the whole value is in the distribution.
- **Actuarial and insurance loss modelling** — pricing needs the distribution, not the mean.
- **Comparing probabilistic to point forecasts on one scale**, which no other metric permits.
- **Evaluating deep ensembles and Bayesian models** — the standard uncertainty-quantification benchmark alongside NLL.

### 9. Advantages
- **A proper scoring rule** — cannot be gamed.
- **Bounded and robust** — unlike NLL, a confidently wrong forecast produces a large but finite penalty, so one observation cannot destroy the average. This is the decisive practical advantage over NLL for reporting and monitoring.
- **In the units of y** — directly interpretable, and comparable to MAE.
- **Reduces to MAE for point forecasts**, so probabilistic and deterministic models can be compared on one scale.
- **Distribution-free in its ensemble form** — no parametric assumption needed; works for samples from any model, including MCMC output and deep ensembles.
- **Equals the integral of pinball loss over all quantiles**, tying it cleanly to quantile regression.
- Rewards sharpness *and* calibration simultaneously.
- Well-defined at σ = 0 (unlike NLL, which diverges).

### 10. Limitations
- **Not in scikit-learn** — requires `properscoring`, `scoringrules`, or a hand-rolled implementation.
- **Scale-dependent**, so not comparable across datasets or targets. Use CRPSS.
- **Less sensitive to the tails than NLL.** Because the penalty is a squared *CDF* difference integrated over x, extreme miscalibration far out in the tail contributes relatively little. For applications where tail accuracy is the point (catastrophe risk, extreme weather), CRPS may under-penalise tail failures and you should add tail-specific scores (the **threshold-weighted CRPS**, or quantile losses at extreme τ).
- **The ensemble form is O(N²)** naively, though O(N log N) with sorting.
- **Not differentiable in a form convenient for all training setups** — although the Gaussian closed form *is* differentiable and can be used as a loss, and doing so is increasingly common.
- Harder to explain than a coverage percentage to a non-technical audience.
- Being an average, it can hide poor performance on a subgroup — always segment.

### 11. Common mistakes
1. **Comparing CRPS across datasets with different target scales.** Use the skill score.
2. **Not exploiting the MAE comparison** — the fact that CRPS reduces to MAE is its most useful property and most people do not know it.
3. **Using the naive O(N²) ensemble form on a large ensemble** and running out of memory.
4. **Assuming CRPS captures tail behaviour adequately** for extreme-risk applications. Add threshold-weighted variants.
5. **Reporting CRPS alone** — pair it with coverage (PICP) and interval width (MPIW), which are what stakeholders understand.
6. Computing the Gaussian closed form when the predictive distribution is clearly not Gaussian (skewed, bounded, multimodal). Use the ensemble form instead.

### 12. Interview questions

**Easy — What does CRPS measure?** The integrated squared difference between the predicted CDF and the step function at the observed value — the area between the forecast CDF and reality.

**Easy — What are CRPS's units?** The units of the target, which is why it is directly comparable to MAE.

**Medium — ★ How does CRPS relate to MAE?**
For a **deterministic** forecast (a point mass), `CRPS = |y − ŷ|`, so the average CRPS equals MAE. CRPS therefore **generalises MAE to probabilistic forecasts**, and this is enormously useful in practice: it means you can put a probabilistic model and a point model on the same axis and ask directly whether the extra machinery earned its keep.

**Medium — ★ CRPS vs NLL — which would you report and why?**
Both are proper. **NLL for training, CRPS for reporting and monitoring.** NLL's gradient behaviour is better for optimisation and it is the natural maximum-likelihood objective, but it is unbounded, so one confidently-wrong observation can dominate the average and a σ → 0 collapse can make it diverge. CRPS is bounded, is in the units of the target, degrades gracefully, and reduces to MAE — all of which make it far safer as a production monitoring metric and far easier to explain. Report both if you can, plus coverage.

**Medium — ★ State the relationship between CRPS and pinball loss.**
`CRPS = 2 ∫₀¹ PinballLoss_τ dτ`. CRPS is the pinball loss averaged over all quantile levels. This means (a) minimising CRPS is equivalent to getting *every* quantile right on average, (b) a discrete weighted sum of pinball losses over a grid of quantiles is a practical approximation to CRPS — which is exactly what the M5 Uncertainty competition used — and (c) if you have a quantile-regression model you can estimate CRPS from its quantiles without assuming a distributional family.

**Hard — Why might CRPS under-penalise tail failures, and what do you do about it?**
Because CRPS integrates the squared *CDF* difference. Far out in the tail, both `F(x)` and the indicator are close to 0 or close to 1, so even a badly wrong tail contributes a small squared difference over that region. A forecast that assigns essentially zero probability to a catastrophic outcome that then occurs is penalised, but not nearly as severely as NLL would penalise it (NLL would be near-infinite). For catastrophe risk, extreme weather, or any application where the tail *is* the decision, use **threshold-weighted CRPS** (which applies a weight function `w(x)` emphasising the region of interest), **quantile/pinball losses at extreme τ**, or **NLL with a heavy-tailed family**, and report tail-specific coverage. The general principle: match the score's region of sensitivity to the region where your decisions are made.

**Hard — ★ How would you evaluate a deep ensemble's uncertainty end to end?**
A four-part protocol. (1) **Proper scores:** NLL and CRPS on held-out data, both against a climatological/constant-distribution baseline so the numbers are interpretable as skill. (2) **Calibration:** the **PIT histogram** (should be uniform) and **coverage of nominal intervals** at several levels (50%, 80%, 90%, 95%), reported as a reliability curve of nominal vs empirical coverage. (3) **Sharpness:** mean interval width (MPIW) at each level — because good coverage with enormous intervals is worthless, and sharpness must be reported *conditional* on calibration. (4) **Out-of-distribution behaviour:** the decisive test for epistemic uncertainty. Evaluate on inputs deliberately shifted away from the training distribution and verify that predicted σ *grows*. A single NLL-trained network will fail this — it captures aleatoric noise but is confidently wrong off-distribution — whereas a deep ensemble should show its μ predictions diverging. Decompose total predictive variance into `mean(σ²)` (aleatoric) plus `var(μ)` (epistemic) across ensemble members and check that the epistemic component rises with distance from the training data. Finally, if you need *guaranteed* coverage, wrap the whole thing in **conformal prediction**, which gives distribution-free finite-sample validity regardless of whether the model's own uncertainty is honest.

---

## 8.3 PREDICTION INTERVAL COVERAGE PROBABILITY (PICP) AND MEAN INTERVAL WIDTH (MPIW)

### 1. Definition
- **PICP:** the fraction of actual values that fall inside the predicted interval.
- **MPIW:** the average width of the predicted intervals.

### 2. Intuition
These two metrics are the **stakeholder-facing** uncertainty metrics. Nobody outside a research team can interpret a CRPS of 1.01, but everybody understands:

> "Our 90% interval contains the true price 89% of the time, and it is $58k wide on average."

That is a complete, honest, actionable statement of model uncertainty in one sentence, and it is what you put on a slide.

They must **always be reported together**, because each alone is trivially gameable:
- **PICP alone:** predict `(−∞, +∞)` → PICP = 100%. Useless.
- **MPIW alone:** predict a zero-width interval → MPIW = 0. Useless.

**The rule, from the forecasting literature (Gneiting & Raftery): maximise sharpness subject to calibration.** First achieve the nominal coverage; then, among models that do, prefer the narrowest intervals.

### 3. Formula
```
                1    n
PICP  =        ───  ×  Σ  1{ Lᵢ  ≤  yᵢ  ≤  Uᵢ }
                n   i=1

                1    n
MPIW  =        ───  ×  Σ  ( Uᵢ − Lᵢ )
                n   i=1
```
Symbol by symbol:
- **Lᵢ, Uᵢ** = the lower and upper bounds of the predicted interval for observation i
- **1{...}** = the indicator: 1 if the actual falls inside, 0 otherwise
- **PICP** ∈ [0,1], target = the **nominal level** (0.90 for a 90% interval)
- **MPIW** ≥ 0, in the **units of y**, lower is better *conditional on adequate coverage*

**Normalised MPIW (NMPIW)** makes width comparable across datasets:
```
NMPIW  =  MPIW / ( max(y) − min(y) )      or      MPIW / σ(y)
```

**Combined scores** that trade the two off automatically:
```
CWC (Coverage Width-based Criterion)  =  NMPIW × ( 1 + γ · e^(−η(PICP − μ)) )
```
where μ is the nominal level and γ activates the penalty only when PICP < μ. In practice the **Interval Score** (8.4) is a cleaner and proper alternative, so prefer it.

### 4. Manual example

Suppose we produce 90% prediction intervals for our ten houses:

| i | y | Lower | Upper | Width | Inside? |
|---|---|---|---|---|---|
| 1 | 200 | 185 | 255 | 70 | ✔ |
| 2 | 250 | 205 | 275 | 70 | ✔ |
| 3 | 300 | 275 | 345 | 70 | ✔ |
| 4 | 350 | 295 | 365 | 70 | ✔ |
| 5 | 400 | 385 | 455 | 70 | ✔ |
| 6 | 450 | 395 | 465 | 70 | ✔ |
| 7 | 500 | 485 | 555 | 70 | ✔ |
| 8 | 550 | 495 | 565 | 70 | ✔ |
| 9 | 600 | 585 | 655 | 70 | ✔ |
| 10 | **900** | 665 | 735 | 70 | **✘** (900 > 735) |

```
PICP = 9 / 10 = 0.90    -> exactly the nominal 90%. Well calibrated.
MPIW = 700 / 10 = 70    -> intervals average $70k wide

NMPIW = 70 / (900 − 200) = 70/700 = 0.10
      = 70 / 193.65      = 0.361  (relative to sigma)
```
**PICP = 0.90, MPIW = 70.**

**But look at the failure.** Coverage is exactly nominal — yet the *one* observation outside the interval is the $900k house, missed by $165k. The interval was `(665, 735)` and the truth was 900. **A constant-width interval on a heteroscedastic target achieves nominal coverage overall while failing systematically in the high-value region.** This is the single most important lesson about PICP: **average coverage can be correct while conditional coverage is badly wrong.**

**Conditional coverage** is the fix — report coverage by segment:
```
Houses 1-5 (cheap):    5/5 = 100%   -> intervals too WIDE here
Houses 6-9 (mid):      4/4 = 100%   -> intervals too WIDE here
House 10 (expensive):  0/1 =   0%   -> intervals too NARROW here
```
The intervals should be narrow at the bottom and wide at the top. A **quantile-regression** or heteroscedastic model produces exactly that; a `ŷ ± 1.96σ` interval with a global σ cannot.

**Now compare against an adaptive interval** (widths proportional to the prediction):

| i | y | Interval | Width | Inside? |
|---|---|---|---|---|
| 1–9 | — | ŷ ± 0.10ŷ | 44–124 | 9/9 ✔ |
| 10 | 900 | 700 ± 140 = (560, 840) | 280 | ✘ |

Still misses house 10 — because the point prediction itself is 200 low, and no reasonable interval width rescues a badly biased centre. **A well-calibrated interval cannot compensate for a biased point forecast**, which is why bias diagnostics (Part 4.5) come before uncertainty diagnostics.

### 5. Python
```python
import numpy as np

def picp(y_true, lower, upper):
    y_true, lower, upper = (np.asarray(a, float) for a in (y_true, lower, upper))
    return np.mean((y_true >= lower) & (y_true <= upper))

def mpiw(lower, upper):
    return np.mean(np.asarray(upper, float) - np.asarray(lower, float))

lower = np.array([185,205,275,295,385,395,485,495,585,665.])
upper = np.array([255,275,345,365,455,465,555,565,655,735.])

picp(y, lower, upper)          # 0.9
mpiw(lower, upper)             # 70.0
mpiw(lower, upper) / y.std()   # 0.361  (normalised)

# --- The reliability curve: coverage at MULTIPLE nominal levels ---
# This is the uncertainty analogue of a calibration curve. Always produce it.
def coverage_curve(y_true, quantile_preds):
    """quantile_preds: dict {nominal_level: (lower_array, upper_array)}"""
    rows = []
    for nominal, (lo, hi) in sorted(quantile_preds.items()):
        rows.append((nominal, picp(y_true, lo, hi), mpiw(lo, hi)))
    return rows

# for nominal, empirical, width in coverage_curve(y_test, preds):
#     print(f"nominal {nominal:.0%}  empirical {empirical:.1%}  width {width:.1f}")

# --- CONDITIONAL coverage: the check that actually matters ---
def coverage_by_bin(y_true, lower, upper, y_pred, n_bins=5):
    """Coverage within bins of the PREDICTED value."""
    y_true, lower, upper = (np.asarray(a, float) for a in (y_true, lower, upper))
    edges = np.quantile(y_pred, np.linspace(0, 1, n_bins + 1))
    for lo_e, hi_e in zip(edges[:-1], edges[1:]):
        m = (y_pred >= lo_e) & (y_pred <= hi_e)
        if m.sum():
            print(f"pred in [{lo_e:7.1f},{hi_e:7.1f}]  n={m.sum():3d}  "
                  f"coverage={picp(y_true[m], lower[m], upper[m]):.0%}  "
                  f"width={mpiw(lower[m], upper[m]):6.1f}")

coverage_by_bin(y, lower, upper, y_pred, n_bins=5)
```
- **The reliability curve across several nominal levels is the key deliverable.** A model can be well calibrated at 90% and badly calibrated at 50%; only the curve reveals it.
- **`coverage_by_bin` is the diagnostic that catches our failure mode.** Report it always.

### 6. Interpretation

| PICP vs nominal | Diagnosis | Action |
|---|---|---|
| **≈ nominal** | Calibrated | Now minimise MPIW |
| **< nominal** (under-coverage) | **Over-confident** — intervals too narrow. The dangerous direction: you will be surprised more often than you promised. | Widen; check for a mis-specified noise family; add epistemic uncertainty (ensembling); apply conformal calibration |
| **> nominal** (over-coverage) | **Under-confident** — intervals too wide. Safe but wasteful: you over-provision, over-reserve, over-promise. | Sharpen; reduce regularisation on the variance head |

**Under-coverage is the more serious failure**, because the consequences are unmodelled surprises. Over-coverage merely costs money.

### 7. Good vs bad values
| Nominal | Acceptable empirical PICP (large test set) |
|---|---|
| 50% | 47 – 53% |
| 80% | 77 – 83% |
| 90% | 87 – 93% |
| 95% | 93 – 97% |

Tolerances should be based on the **sampling variability** of a proportion: with n test points the standard error of PICP is `√(p(1−p)/n)`. At nominal 90% with n = 100 that is 3 percentage points, so an empirical 86% is *within noise* — do not over-react to small test sets. Compute a binomial confidence interval on PICP before declaring miscalibration.

For MPIW, judge against `σ(y)`: a well-calibrated 90% interval on Gaussian noise has width `2 × 1.645 σ_ε = 3.29 σ_ε`, so `MPIW / σ(y)` well below 3.29 indicates the model has genuinely reduced uncertainty relative to the unconditional distribution.

### 8. Business use cases
- **Any stakeholder-facing uncertainty communication.** Property valuation ("$420k, likely between $390k and $455k"), delivery windows, revenue guidance ranges, project timelines (P50/P80).
- **Inventory and safety stock** — the upper bound of the interval *is* the reorder quantity for a given service level.
- **Capacity planning** — provision to the upper bound.
- **Regulatory stress testing and loan loss provisioning** — regulators specify confidence levels and check coverage.
- **Clinical decision support** — a risk range changes treatment decisions in a way a point estimate does not.
- **Energy reserve procurement** — reserve requirements are set from forecast interval widths.
- **Model monitoring** — coverage drift is a clear, interpretable early-warning signal that the world has changed.
- **Uncertainty-quantification research benchmarks** — PICP and MPIW are the standard reported pair.
- **Conformal prediction** — coverage is the guarantee conformal methods provide, so PICP is the natural validation metric.

### 9. Advantages
- **Immediately interpretable to anyone.** No other uncertainty metric comes close.
- **Directly checkable against a promise** — you said 90%, we measured 89%, so the promise held.
- **Distribution-free** — no assumption about the shape of the predictive distribution.
- **PICP has an exact target value** (the nominal level), which makes it self-anchoring in the way MASE's 1.0 is.
- Works for any interval-producing method: quantile regression, parametric σ, bootstrap, conformal, Bayesian.
- **Conditional coverage by segment** is a powerful diagnostic that localises the failure.
- Cheap and stable to compute; good for production monitoring.

### 10. Limitations
- **Neither is a proper scoring rule, and each alone is trivially gameable.** PICP is maximised by infinite intervals; MPIW by zero-width intervals. They *must* be reported as a pair, and even then the trade-off is not resolved for you — use the **Interval Score** or **CRPS** for a single proper number.
- **PICP measures only *marginal* (average) coverage.** As our example shows, a model can hit nominal coverage overall while systematically under-covering an important segment. **Conditional coverage is what you actually want, and it is much harder to achieve and to verify.**
- **PICP is a coarse, discrete statistic** — it counts hits and misses and ignores *how far outside* the misses were. Missing by $1 and missing by $500k score identically. The Interval Score fixes this.
- **High sampling variability on small test sets.** With 50 test points, PICP moves in 2% steps and its confidence interval is wide.
- MPIW is scale-dependent; normalise it.
- No information about the *shape* of the predictive distribution (skew, multimodality).
- Coverage tells you nothing about the point prediction's accuracy.

### 11. Common mistakes
1. **Reporting PICP without MPIW** (or vice versa). Each alone is meaningless.
2. **Reporting only marginal coverage** and missing systematic conditional failure. **Always bin by predicted value and by key segments.**
3. **Reporting coverage at a single nominal level.** Produce the full reliability curve — a model calibrated at 90% can be badly wrong at 50%.
4. **Over-reacting to small deviations on a small test set.** Compute the binomial confidence interval on PICP first.
5. **Using `ŷ ± 1.96 σ̂` with a single global σ̂ on heteroscedastic data.** This is the most common way to produce badly conditionally-calibrated intervals, and it is what our worked example illustrates.
6. **Treating good coverage as evidence of a good model.** A model can have perfect coverage, enormous intervals, and no predictive skill at all.
7. Forgetting that a biased point forecast cannot be rescued by interval width.

### 12. Interview questions

**Easy — What is PICP?** The fraction of actual values falling inside the predicted intervals; it should equal the nominal level.

**Easy — ★ Why must PICP and MPIW be reported together?** Because each is trivially gameable alone. Predicting `(−∞, +∞)` gives PICP = 100% with zero information; predicting a zero-width interval gives MPIW = 0 and never contains the truth. Together they express the real trade-off: maximise sharpness subject to calibration.

**Medium — Your 90% intervals have 78% coverage. What do you do?**
First check whether it is real: compute the binomial confidence interval on PICP — with n = 200, the standard error at p = 0.9 is 2.1pp, so 78% is well outside noise and is a genuine failure. Then diagnose: (1) **conditional coverage by segment and by predicted value** to see whether the failure is localised; (2) check for a **mis-specified noise family** — Gaussian intervals systematically under-cover heavy-tailed errors, and switching to Student-t often fixes it in one step; (3) check whether σ was fitted **in-sample** and is therefore over-optimistic — refit the variance on held-out data; (4) check for **missing epistemic uncertainty** — a single network only models aleatoric noise, so ensembling will widen intervals where the model is genuinely ignorant; (5) check for **distribution shift** between the calibration and test periods. Then, as a guaranteed fix, apply **conformal prediction**, which adjusts the interval width using a held-out calibration set to give distribution-free finite-sample coverage — it will restore 90% coverage regardless of whether the underlying model's uncertainty is honest.

**Medium — ★ What is the difference between marginal and conditional coverage, and why does it matter?**
**Marginal coverage** is the overall hit rate: 90% of all actuals fall inside their interval. **Conditional coverage** requires that 90% of actuals fall inside their interval *within every region of feature space*. Marginal coverage is much weaker and can be achieved by over-covering easy cases and under-covering hard ones — exactly the failure in our worked example, where constant-width intervals over-covered cheap houses and completely missed the expensive one. It matters because decisions are made *conditionally*: the lender valuing an expensive property does not care that the model over-covers starter homes. Standard conformal prediction guarantees only marginal coverage; **Mondrian/group-conditional conformal** or **conformalised quantile regression** are needed for approximate conditional coverage, and exact conditional coverage is provably impossible in a distribution-free setting.

**Hard — ★ Design a complete uncertainty evaluation protocol.**
Six components. (1) **A proper score** — CRPS (primary, in target units and comparable to MAE) and NLL — each reported as a skill score against a climatological baseline so the number is interpretable. (2) **A reliability curve:** empirical vs nominal coverage at 50/80/90/95/99%, with binomial confidence intervals, so calibration is assessed across the whole range rather than at one level. (3) **Sharpness:** MPIW and NMPIW at each level, interpreted only *conditional on* calibration being adequate. (4) **Conditional coverage:** coverage and width binned by predicted value and by every business-relevant segment, plus a **PIT histogram** (should be uniform; a U-shape means under-coverage, a hump means over-coverage, a slope means bias). (5) **Out-of-distribution behaviour:** verify that predicted intervals *widen* on deliberately shifted inputs — the decisive test for epistemic uncertainty, which a single NLL-trained network will fail. (6) **A guarantee layer:** wrap the model in **conformal prediction** on a held-out calibration set, which gives distribution-free finite-sample marginal coverage regardless of model misspecification, and use group-conditional conformal if segment-level validity is required. Report all of it in one table plus two plots (reliability curve, PIT histogram) — that is a complete and defensible uncertainty assessment.

---

## 8.4 INTERVAL SCORE AND WINKLER SCORE

### 1. Definition
A **proper** scoring rule for intervals that combines width and coverage into one number, penalising misses in proportion to *how far outside* they fall.

### 2. Intuition
PICP is coarse: it counts a miss by $1 and a miss by $500k identically. The Interval Score fixes this by charging a penalty proportional to the distance outside the interval, on top of the interval's width.

Read the formula as three charges:
1. **Always pay the width** — you are charged for how vague you were.
2. **If the truth falls below the lower bound**, pay extra proportional to how far below.
3. **If the truth falls above the upper bound**, pay extra proportional to how far above.

The multiplier `2/α` on the exceedance makes the score **proper** — with that exact constant, the score is minimised by reporting the true `α/2` and `1−α/2` quantiles. Any other constant would let you game it.

It is also called the **Winkler score** (Winkler, 1972), and the mean over observations is the **Mean Interval Score (MIS)** or **Mean Winkler Score**. The M4 competition's uncertainty evaluation used it.

### 3. Formula
```
                                     2                            2
IS_α(L, U, y)  =  (U − L)  +  ─── (L − y) · 1{y < L}  +  ─── (y − U) · 1{y > U}
                                     α                            α
```
Symbol by symbol:
- **L, U** = the lower and upper interval bounds, targeting the `α/2` and `1 − α/2` quantiles
- **α** = the miscoverage level. For a **90% interval**, α = 0.10 and `2/α = 20`.
- **(U − L)** = the width penalty, always paid
- **(2/α)(L − y)** when `y < L` = the under-shoot penalty
- **(2/α)(y − U)** when `y > U` = the over-shoot penalty
- Range [0, ∞), lower better, **units of y**

**The exceedance multiplier is severe and that is deliberate:** for a 90% interval it is **20×**. Being outside the interval by one unit costs the same as making the interval 20 units wider. For a 95% interval (α = 0.05) it is **40×**. This is what forces honest coverage.

**Relationship to pinball loss** — the identity that shows it is proper:
```
IS_α  =  (2/α) × [ PinballLoss_{α/2}(L, y)  +  PinballLoss_{1−α/2}(U, y) ]
```
So the Interval Score is just a scaled sum of two pinball losses at the interval's endpoints. And since CRPS is the integral of pinball loss over all τ, the **Weighted Interval Score** across several nested intervals approximates CRPS — which is exactly how the COVID-19 Forecast Hub scored probabilistic case and death forecasts.

**Scaled version** for cross-series comparison, analogous to MASE:
```
MSIS  =  MIS / ( in-sample naive MAE )      (Mean Scaled Interval Score, used in M4)
```

### 4. Manual example

Using the intervals from 8.3, with **α = 0.10** so `2/α = 20`:

| i | y | L | U | Width | Outside by | Penalty | IS |
|---|---|---|---|---|---|---|---|
| 1 | 200 | 185 | 255 | 70 | — | 0 | **70** |
| 2 | 250 | 205 | 275 | 70 | — | 0 | **70** |
| 3 | 300 | 275 | 345 | 70 | — | 0 | **70** |
| 4 | 350 | 295 | 365 | 70 | — | 0 | **70** |
| 5 | 400 | 385 | 455 | 70 | — | 0 | **70** |
| 6 | 450 | 395 | 465 | 70 | — | 0 | **70** |
| 7 | 500 | 485 | 555 | 70 | — | 0 | **70** |
| 8 | 550 | 495 | 565 | 70 | — | 0 | **70** |
| 9 | 600 | 585 | 655 | 70 | — | 0 | **70** |
| 10 | **900** | 665 | 735 | 70 | **165 above** | **20 × 165 = 3,300** | **3,370** |

```
Step 1 — sum: 9 × 70 + 3,370 = 630 + 3,370 = 4,000
Step 2 — mean: MIS = 4,000 / 10 = 400
```
**Mean Interval Score = 400.**

**Compare with what PICP told us.** PICP was exactly 0.90 — nominally perfect. But the Interval Score is 400, of which **3,370/4,000 = 84% comes from the single miss.** The score is screaming that one observation is catastrophically outside, while PICP registered it as a single tolerable miss.

**This is the whole argument for the Interval Score over PICP:** PICP says "we hit our target"; the Interval Score says "we hit our target by over-covering nine easy cases and missing one case by $165k, and that miss dominates our loss." The second statement is the true one.

**A sharper-but-shifted alternative, for contrast.** Suppose we widened only the top interval to (600, 950), width 350:
```
Houses 1-9: 9 × 70 = 630
House 10: width 350, y = 900 inside -> penalty 0 -> IS = 350
MIS = (630 + 350)/10 = 98
```
**MIS falls from 400 to 98** by widening one interval where it mattered — a 70% improvement — while PICP rises only from 0.90 to 1.00. The Interval Score correctly rewards **adaptive, heteroscedastic** intervals; PICP barely notices.

### 5. Python
```python
import numpy as np

def interval_score(y_true, lower, upper, alpha=0.10):
    """Mean Interval Score (Winkler score). alpha = miscoverage, e.g. 0.10 for a 90% PI."""
    y_true, lower, upper = (np.asarray(a, float) for a in (y_true, lower, upper))
    width  = upper - lower
    under  = (2.0 / alpha) * np.clip(lower - y_true, 0, None)   # y below L
    over   = (2.0 / alpha) * np.clip(y_true - upper, 0, None)   # y above U
    return np.mean(width + under + over)

interval_score(y, lower, upper, alpha=0.10)         # 400.0

# Decompose it -- always do this, it is where the diagnosis lives
def interval_score_parts(y_true, lower, upper, alpha=0.10):
    y_true, lower, upper = (np.asarray(a, float) for a in (y_true, lower, upper))
    w = np.mean(upper - lower)
    u = np.mean((2/alpha) * np.clip(lower - y_true, 0, None))
    o = np.mean((2/alpha) * np.clip(y_true - upper, 0, None))
    return {'width': w, 'under_penalty': u, 'over_penalty': o, 'total': w + u + o}

interval_score_parts(y, lower, upper)
# {'width': 70.0, 'under_penalty': 0.0, 'over_penalty': 330.0, 'total': 400.0}

# Scaled version for cross-series comparison (M4's MSIS)
def msis(y_true, lower, upper, y_train, alpha=0.10, seasonality=1):
    naive = np.mean(np.abs(np.asarray(y_train, float)[seasonality:]
                          - np.asarray(y_train, float)[:-seasonality]))
    return interval_score(y_true, lower, upper, alpha) / naive

# Weighted Interval Score across nested intervals ~ CRPS (COVID-19 Forecast Hub style)
def weighted_interval_score(y_true, median_pred, intervals):
    """intervals: dict {alpha: (lower, upper)}. Approximates CRPS."""
    K = len(intervals)
    total = 0.5 * np.abs(np.asarray(y_true, float) - np.asarray(median_pred, float))
    for a, (lo, hi) in intervals.items():
        w = a / 2
        lo, hi = np.asarray(lo, float), np.asarray(hi, float)
        s = (hi - lo) + (2/a)*np.clip(lo - y_true, 0, None) + (2/a)*np.clip(y_true - hi, 0, None)
        total = total + w * s
    return np.mean(total / (K + 0.5))
```
Line-by-line:
- **`np.clip(x, 0, None)`** implements the indicator-times-distance cleanly: it is zero when the truth is inside and equals the exceedance when outside.
- **The decomposition into width / under / over is the most valuable output.** Ours shows 70 from width and 330 from over-shoot — so the model's problem is under-coverage at the top, not vagueness. That immediately tells you to make the intervals heteroscedastic rather than uniformly wider.
- **`weighted_interval_score`** is the discretised CRPS used by the COVID-19 Forecast Hub; knowing it exists is a good signal of familiarity with modern probabilistic-forecast evaluation.

### 6. Interpretation
In units of y, lower better. Interpret via:
- **The decomposition:** what share comes from width vs from exceedance? Width-dominated → intervals too wide, sharpen. Exceedance-dominated → under-covering, widen (and make width adaptive).
- **Against a baseline:** MSIS (scaled by the naive MAE) gives a MASE-like anchor.
- **Against a well-calibrated reference:** a perfectly calibrated Gaussian 90% interval on noise σ has expected IS ≈ `3.29 σ + small exceedance term`, so `MIS / σ(y)` around 3–4 is roughly the calibrated benchmark.

Ours: `400 / 193.65 = 2.07`, which looks low relative to σ(y) only because our intervals are narrow — and the decomposition reveals the cost is being paid in exceedance, not width.

### 7. Good vs bad values
Judge by decomposition share and by MSIS. As a rule of thumb, a well-tuned model should have **less than ~30–40% of its Interval Score coming from exceedance penalties**; more than that means the intervals are systematically too narrow somewhere.

### 8. Business use cases
- **M4 forecasting competition** — MSIS was the official uncertainty metric.
- **COVID-19 Forecast Hub** — the Weighted Interval Score was the primary evaluation metric for all submitted probabilistic case, hospitalisation, and death forecasts. This is the highest-profile recent use of the metric.
- **Energy forecasting competitions** and reserve-setting.
- **Epidemic and public-health forecasting** generally.
- **Any setting where you need a single, proper, interpretable number for interval quality** rather than the PICP/MPIW pair.
- **Model selection among interval-producing models** — because it is proper, you can safely optimise it.
- **Regulatory reporting of forecast uncertainty**, where a defensible single score is wanted.

### 9. Advantages
- **A proper scoring rule** — unlike PICP and MPIW, it cannot be gamed, so it can be used as a selection or training objective.
- **Combines width and coverage in one number**, resolving the trade-off automatically with a principled weighting.
- **Penalises misses by distance**, not just by count — the key improvement over PICP.
- **In the units of y**, so it is interpretable and comparable to MAE.
- **Decomposes cleanly** into width, under-shoot, and over-shoot, which localises the problem immediately.
- **Reduces to pinball loss** at the endpoints, and the weighted multi-interval version approximates CRPS — so it sits coherently within the proper-scoring-rule family.
- Has a scaled version (MSIS) for cross-series comparison.
- Established in major forecasting competitions and public-health forecasting.

### 10. Limitations
- **Scale-dependent** — not comparable across datasets without scaling (use MSIS).
- **Dominated by exceedances**, since the multiplier is `2/α` (20× for a 90% interval, 40× for 95%). A single extreme miss can dominate the mean, exactly as with RMSE. Report the median Interval Score or the decomposition alongside.
- **Requires choosing α**, and scores at different α are not comparable.
- **Less intuitive than PICP** for a non-technical audience — "our interval score is 330" needs explanation, while "our 90% interval contains the truth 89% of the time" does not. **Report both:** Interval Score for model selection, PICP/MPIW for communication.
- Evaluates only the two endpoints, so it says nothing about the shape of the distribution between them (the weighted multi-interval version addresses this).
- Not in scikit-learn.

### 11. Common mistakes
1. **Getting the multiplier wrong.** It is `2/α`, so 20 for a 90% interval — not `1/α`, and not `2/(1−α)`. The exact constant is what makes the score proper.
2. **Comparing Interval Scores across different α levels.**
3. **Not decomposing**, and therefore not knowing whether to widen or sharpen.
4. **Reporting it alone to stakeholders** instead of alongside PICP and MPIW.
5. Comparing raw Interval Scores across series of different scale — use MSIS.
6. Being surprised that one observation dominates; that is expected with a 20× multiplier, and the median or a trimmed mean is a useful complement.

### 12. Interview questions

**Easy — What does the Interval Score add over PICP?** It penalises misses in proportion to how far outside the interval the truth fell, and it charges for interval width, all in one proper score. PICP only counts hits and misses.

**Easy — For a 90% interval, what is the exceedance multiplier?** `2/α = 2/0.10 = 20`.

**Medium — ★ Why is the Interval Score proper while PICP and MPIW are not?**
Because with the exact multiplier `2/α` the score is minimised only by reporting the true `α/2` and `1−α/2` quantiles — it is a scaled sum of the pinball losses at those two levels, and pinball loss is minimised at its corresponding quantile. PICP and MPIW are each optimised by degenerate forecasts (infinite and zero width respectively), so a forecaster can improve either one without improving the forecast. Propriety is what allows you to safely *optimise* the Interval Score rather than merely report it.

**Medium — Your Interval Score decomposes into 40 from width and 290 from exceedance. What does that tell you?**
That the intervals are far too narrow: 88% of the loss is coming from the truth falling outside them. Widening the intervals would trade a small increase in the width term for a large decrease in the exceedance term and would substantially improve the score. Critically, before widening uniformly, check the **conditional** decomposition — if the exceedance is concentrated in one region of feature space (as in our worked example, entirely at the top of the price range), the correct fix is a **heteroscedastic or quantile model** that widens only where needed, not a global widening that would waste sharpness everywhere else.

**Hard — ★ Relate the Interval Score, pinball loss, and CRPS.**
They form a single family. **Pinball loss** at level τ scores one quantile. The **Interval Score** at level α is `(2/α)` times the sum of the pinball losses at `α/2` and `1−α/2` — it scores one interval, i.e. a pair of quantiles. **CRPS** is `2∫₀¹ pinball_τ dτ` — it scores the entire predictive distribution, i.e. all quantiles. And the **Weighted Interval Score** over a set of nested intervals is a discretised approximation to CRPS: as you add more intervals it converges to it. So the choice among them is really a choice of *how much of the distribution you are evaluating*: one quantile (pinball, e.g. a service-level target), one interval (Interval Score, e.g. a communicated range), or the whole distribution (CRPS). All three are proper, all three are in the units of y, and all three are minimised by the correct predictive distribution — which is why the COVID-19 Forecast Hub could use WIS as a practical stand-in for CRPS while asking forecasters only for a handful of quantiles.

---

## 8.5 PROBABILITY INTEGRAL TRANSFORM (PIT) HISTOGRAM

### 1. Definition
The histogram of `pᵢ = F̂ᵢ(yᵢ)` — the predicted CDF evaluated at the observed value. For a perfectly calibrated model these values are **Uniform(0,1)**.

### 2. Intuition
This is the **calibration curve of probabilistic regression** — the direct analogue of the reliability diagram in classification, and the single most informative uncertainty diagnostic.

The logic: if your predictive distribution is correct, then the observed value is a random draw from it, so its **percentile within that distribution** is uniformly distributed. If the model claims a distribution and the truth systematically lands in the tails, the model is over-confident. If the truth always lands in the middle, the model is under-confident.

**The shapes and their meanings — this table is the payoff:**

```
(a) UNIFORM: well calibrated
    |####  ####  ####  ####  ####
    +--------------------------------
    0                              1

(b) U-SHAPED: OVER-confident. Truth lands in the tails
    |####                      ####       too often -> intervals TOO NARROW
    |####  ##            ##    ####       -> under-coverage
    +--------------------------------

(c) HUMP-SHAPED: UNDER-confident. Truth lands in the middle
    |        ####  ####                   too often -> intervals TOO WIDE
    | ##     ####  ####     ##            -> over-coverage
    +--------------------------------

(d) SLOPED (rising): the model predicts too LOW
    |  ##   ###   ####  #####  ######     truth lands high in the distribution
    +--------------------------------      -> POSITIVE BIAS in the residual sense

(e) SLOPED (falling): the model predicts too HIGH
    |######  #####  ####   ###   ##
    +--------------------------------      -> NEGATIVE BIAS
```

**A single plot diagnoses bias, over-confidence, and under-confidence simultaneously.** Nothing else in this document does that.

### 3. Formula
```
pᵢ  =  F̂ᵢ( yᵢ )                              for a continuous predictive CDF F̂ᵢ

For a Gaussian forecast:   pᵢ = Φ( (yᵢ − μᵢ) / σᵢ )
For an ensemble:           pᵢ ≈ (1/N) Σⱼ 1{ xᵢⱼ ≤ yᵢ }   (the empirical CDF)
```
Under correct calibration, `pᵢ ~ Uniform(0,1)`.

**Formal tests** of uniformity: the Kolmogorov-Smirnov test, the Cramér-von Mises test, or a chi-squared test on histogram bins. In practice the plot is usually more informative than the p-value.

The discrete-ensemble analogue is the **rank histogram** (or **Talagrand diagram**), which plots where the observation ranks among the N ensemble members — same interpretation, same shapes.

### 4. Manual example

Using the three-observation NLL example (`z` values +0.5, −1.0, 0.0):
```
p₁ = Φ(+0.5) = 0.691
p₂ = Φ(−1.0) = 0.159
p₃ = Φ( 0.0) = 0.500
```
With only three points there is nothing to conclude — **PIT histograms need a few hundred observations** to be readable, which is an important practical caveat.

**A synthetic illustration with 1,000 points, to show the diagnostic power:**

| Scenario | True σ | Claimed σ | PIT shape | PICP (90%) |
|---|---|---|---|---|
| Well calibrated | 10 | 10 | Uniform | 0.90 |
| **Over-confident** | 10 | **5** | **U-shaped** | **0.66** |
| **Under-confident** | 10 | **20** | **Hump** | **0.99** |
| **Biased low** (μ 5 too low) | 10 | 10 | **Rising slope** | 0.86 |

**The key insight:** the over-confident and biased cases *both* show reduced coverage (0.66 and 0.86), so **PICP alone cannot distinguish over-confidence from bias.** The PIT histogram can: a U-shape means the width is wrong; a slope means the centre is wrong. Those require completely different fixes — widen the intervals versus debias the point forecast — so distinguishing them matters.

### 5. Python
```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def pit_values_gaussian(y_true, mu, sigma):
    y_true, mu, sigma = (np.asarray(a, float) for a in (y_true, mu, sigma))
    return stats.norm.cdf((y_true - mu) / np.maximum(sigma, 1e-12))

def pit_values_ensemble(y_true, samples):
    """samples shape (n_obs, n_samples)."""
    y_true = np.asarray(y_true, float)[:, None]
    return (np.asarray(samples, float) <= y_true).mean(axis=1)

def plot_pit(pit, n_bins=20, ax=None):
    ax = ax or plt.gca()
    ax.hist(pit, bins=n_bins, range=(0, 1), density=True,
            edgecolor='k', alpha=0.75)
    ax.axhline(1.0, ls='--', c='r', label='perfect calibration')
    ax.set_xlabel('PIT value  F(y)'); ax.set_ylabel('density')
    ax.legend()
    # Formal test of uniformity
    ks = stats.kstest(pit, 'uniform')
    ax.set_title(f"PIT histogram (KS p = {ks.pvalue:.3f})")
    return ks

# pit = pit_values_gaussian(y_test, mu_pred, sigma_pred)
# plot_pit(pit)

# Quantitative summaries of PIT non-uniformity
# pit_mean should be 0.5 (bias check); pit_var should be 1/12 = 0.0833 (dispersion check)
def pit_summary(pit):
    pit = np.asarray(pit, float)
    return {
        'mean'      : pit.mean(),          # 0.5 if unbiased; >0.5 => predicts low
        'variance'  : pit.var(),           # 1/12 = 0.0833 if calibrated
                                           #   > 1/12 => over-confident (U-shape)
                                           #   < 1/12 => under-confident (hump)
        'ks_pvalue' : stats.kstest(pit, 'uniform').pvalue,
    }
```
Line-by-line:
- **`pit_summary` is the compact quantitative version of the plot** and is what you put in a monitoring dashboard. `mean > 0.5` means the truth lands high in the predicted distribution, i.e. **the model predicts too low**. `variance > 1/12` means excess mass in the tails, i.e. **over-confidence**.
- **The 1/12 reference is worth memorising:** the variance of Uniform(0,1) is exactly `1/12 = 0.08333`.
- The KS test on PIT values is slightly conservative when the same data was used to fit σ, so prefer held-out data.

### 6. Interpretation

| PIT statistic | Value | Diagnosis | Fix |
|---|---|---|---|
| mean | ≈ 0.5 | Unbiased centre | — |
| mean | > 0.5 | Truth lands high → **predicts too low** | Debias the point forecast (offset, smearing correction, check back-transform) |
| mean | < 0.5 | Truth lands low → **predicts too high** | Debias |
| variance | ≈ 0.0833 | Correct dispersion | — |
| variance | > 0.0833 | U-shaped → **over-confident** | Widen; heavier-tailed family; add epistemic uncertainty; conformalise |
| variance | < 0.0833 | Hump → **under-confident** | Sharpen; reduce variance regularisation |

### 7–8. Good values / use cases
- **Ensemble weather forecasting** — the rank histogram has been standard practice since the 1990s and is where these diagnostics were developed.
- **Any probabilistic regression model validation** — deep ensembles, NGBoost, Gaussian Processes, Bayesian models.
- **Uncertainty-quantification research** — reported alongside NLL and CRPS as the standard trio.
- **Production monitoring of probabilistic models** — track `PIT mean` and `PIT variance` over time as two scalar control charts; drift in either is an interpretable, actionable alert.
- **Diagnosing whether an uncertainty failure is a width problem or a centre problem**, which is its unique contribution.

### 9. Advantages
- **The single most diagnostic uncertainty plot** — it distinguishes bias, over-confidence, and under-confidence in one picture, which no scalar metric does.
- **Distribution-free** — works for any predictive distribution, parametric or ensemble.
- Has a clean theoretical target (uniformity) and formal tests.
- Reduces to two interpretable scalars (mean and variance) for monitoring.
- Directly analogous to the classification calibration curve, so it transfers intuition.

### 10. Limitations
- **Needs a few hundred observations** to be readable; useless on small test sets.
- **Bin-count dependent** in appearance, like all histograms.
- **Assesses only marginal calibration.** A model can have a perfectly uniform overall PIT while being over-confident on one segment and under-confident on another, with the two cancelling. **Always compute PIT by segment.** This is the same marginal-versus-conditional caveat as PICP.
- Uniformity is necessary but **not sufficient** for a good model — a climatological forecast (the unconditional distribution of y) has a perfectly uniform PIT and no predictive skill at all. **Always pair with CRPS or NLL**, which measure sharpness.
- Visual, so it cannot be optimised directly; use CRPS/NLL as the objective.
- Slightly conservative if σ was fitted on the same data.

### 11. Common mistakes
1. **Interpreting a PIT histogram from 30 observations.** It will look ragged regardless.
2. **Reporting a uniform PIT as evidence of a good model.** It only proves calibration; the climatological forecast passes too. Pair with a proper score.
3. **Only checking the marginal PIT** and missing cancelling segment-level failures.
4. **Confusing the U-shape and hump-shape interpretations.** U-shape = truth in the tails = **over**-confident = intervals too narrow. Mnemonic: *U for "Under-covering."*
5. Not computing the mean and variance, which are the compact monitorable summaries.

### 12. Interview questions

**Easy — What should a PIT histogram look like for a calibrated model?** Uniform on [0,1].

**Medium — ★ What does a U-shaped PIT histogram mean?** The observed values fall in the tails of the predicted distribution more often than they should, which means the predictive distributions are too narrow — the model is **over-confident** and its intervals will under-cover.

**Medium — ★ Why is PIT more informative than PICP?**
Because PICP is one number at one nominal level and it conflates two different failures. A reduced PICP could mean the intervals are too narrow (a dispersion problem) *or* that the point forecast is biased so the intervals are centred in the wrong place (a location problem). Those need opposite fixes. The PIT histogram distinguishes them geometrically: a **U-shape** is a dispersion problem, a **slope** is a location problem, and a **hump** is over-dispersion. It also assesses calibration across the whole distribution rather than at a single level.

**Medium — What are the target mean and variance of PIT values?** Mean 0.5 and variance 1/12 ≈ 0.0833, being the moments of Uniform(0,1). Deviations in the mean indicate bias; deviations in the variance indicate mis-specified dispersion.

**Hard — Your PIT histogram is uniform but your CRPS is poor. Explain.**
Calibration and sharpness are independent, and PIT measures only calibration. The extreme illustration is the **climatological forecast**: predict the unconditional distribution of y for every observation. Its PIT is *exactly* uniform by construction, because every observation genuinely is a draw from that distribution — yet it has no predictive skill whatsoever and its CRPS equals the climatological baseline. So a uniform PIT with a poor CRPS means your model is **honest but uninformative**: it correctly reports how uncertain it is, and it is very uncertain. The fix is not calibration work but **better features, more capacity, or more data** — the same conclusion you would reach from a low R² with unbiased residuals. This is exactly parallel to a classifier with perfect calibration and ROC-AUC of 0.5, and being able to draw that parallel is a strong answer.

## 8.6 Probabilistic metric summary

| Metric | Measures | Units | Proper? | Bounded? | Best for |
|---|---|---|---|---|---|
| **Gaussian NLL** | Calibration + sharpness | awkward, can be negative | Yes | **No** | **Training** probabilistic models |
| **CRPS** | Calibration + sharpness | **units of y** | Yes | **Yes** | **Reporting**; comparable to MAE |
| **Pinball loss** | One quantile | units of y | Yes | Yes | Service-level targets |
| **Interval Score / Winkler** | One interval (width + exceedance) | units of y | Yes | Yes | Model selection on intervals |
| **Weighted Interval Score** | Several nested intervals ≈ CRPS | units of y | Yes | Yes | Competitions; quantile submissions |
| **PICP** | Coverage only | fraction | **No** | Yes | **Communication** |
| **MPIW** | Sharpness only | units of y | **No** | Yes | Communication (with PICP) |
| **PIT histogram** | Calibration diagnosis | — | n/a | n/a | **Diagnosis** — bias vs dispersion |

**The recommended reporting set for any probabilistic regression model:**
1. **CRPS** (with a skill score against climatology) — the headline proper score, in target units.
2. **NLL** — as the training objective and a secondary score.
3. **PICP and MPIW at 50/80/90/95%** — the reliability curve, for communication and calibration checking.
4. **PIT histogram** plus its mean and variance — for diagnosis.
5. **All of the above by segment** — because every one of these metrics is marginal and can hide conditional failure.
6. **A conformal wrapper** if coverage must be guaranteed.

---

# PART 9 — Model Selection Criteria

## 9.0 A different job

Everything so far measures **how good a model's predictions are**. This Part measures something else: **which model should I choose?**

The two are not the same, and the reason is the central problem of statistics: **in-sample fit always improves with complexity.** Add a feature, add a polynomial term, add a tree — training error goes down, every time, even if the addition is pure noise. So in-sample MSE, RMSE, and R² **cannot** be used to choose a model; they will always pick the most complex one.

There are two families of solutions:

| Family | Approach | Members | Assumption |
|---|---|---|---|
| **Penalise complexity analytically** | Add a term that charges for parameters | Adjusted R², AIC, AICc, BIC, Mallows' Cp | A likelihood or a parameter count exists |
| **Estimate out-of-sample error empirically** | Hold data out and measure | Cross-validated RMSE/MAE, PRESS, test-set error | Data is exchangeable (or blocked correctly) |

**The modern practical verdict, and the right thing to say in an interview:** **cross-validation is the primary tool.** It makes no distributional assumption, requires no parameter count, works for any model including deep networks and tree ensembles, and directly estimates the quantity you care about. AIC and BIC are fast, principled complements that are especially useful for classical models, small samples, or when refitting is expensive — and they remain the expected vocabulary in statistics, econometrics, and regulated modelling.

---

## 9.1 AKAIKE INFORMATION CRITERION (AIC)

### 1. Definition
A measure of a model's out-of-sample predictive deviance, estimated as its in-sample log-likelihood penalised by twice its number of parameters.

### 2. Intuition
AIC answers: **"of these candidate models, which will predict new data best?"**

The derivation is elegant. Akaike showed that the in-sample log-likelihood is a *biased* estimate of the expected out-of-sample log-likelihood, and that — remarkably — **the bias is approximately equal to the number of parameters, k.** So you can correct it analytically:

```
expected out-of-sample deviance  ≈  in-sample deviance  +  2k
```

That is AIC. It is an **estimate of out-of-sample error obtained without holding any data out** — which is why it was revolutionary and why it is still used when data is scarce or refitting is expensive.

**Its purpose is predictive accuracy, not truth.** AIC does not try to identify the "true" model; it tries to minimise expected prediction error. It is **asymptotically equivalent to leave-one-out cross-validation**, which is the single most useful fact about it and the cleanest way to remember what it does.

### 3. Formula
```
AIC  =  2k  −  2 ln L̂
```
Symbol by symbol:
- **k** = the number of **estimated parameters**, including the intercept **and the error variance σ²**. For an OLS model with p predictors: `k = p + 2`. Forgetting σ² is the most common counting error.
- **L̂** = the maximised likelihood of the model
- **−2 ln L̂** = the **deviance**, a measure of misfit (lower is better)
- **2k** = the complexity penalty: **each parameter costs 2 units of deviance**

**For OLS with Gaussian errors**, the maximised log-likelihood has a closed form:
```
                n  ⎡                    ( RSS )        ⎤
ln L̂  =  −  ───  ⎢  ln(2π)  +  ln ( ─── )  +  1   ⎥
                2  ⎣                    (  n  )        ⎦
```
so
```
AIC  =  n · ln( RSS / n )  +  2k  +  n·( 1 + ln(2π) )
```
The last term is the same for all models on the same data, so it is usually **dropped**, giving the common shortcut:
```
AIC*  =  n · ln( RSS / n )  +  2k'          (differences are what matter)
```
**Only differences in AIC are meaningful.** The absolute value depends on which constants your software includes, so **never compare AIC values from different tools.**

Range (−∞, +∞); **lower is better**.

### 4. Manual example

Our model: `n = 10`, `RSS = 43,000`, `p = 3` predictors → `k = p + 2 = 5` (3 slopes + intercept + σ²).

```
Step 1 — the maximised log-likelihood:
  RSS/n = 43,000/10 = 4,300
  ln(4,300)  = 8.366370
  ln(2π)     = 1.837877

  ln L̂ = −(10/2) × [ 1.837877 + 8.366370 + 1 ]
        = −5 × 11.204247
        = −56.021237

Step 2 — deviance:
  −2 ln L̂ = 112.042474

Step 3 — penalty:
  2k = 2 × 5 = 10

Step 4 — AIC:
  AIC = 10 + 112.042474 = 122.042474
```
**AIC = 122.04.**

**Now the point of AIC — comparing candidate models.** Suppose we have four nested models on the same 10 observations:

| Model | p | k = p+2 | RSS | ln(RSS/n) | −2lnL̂ | 2k | **AIC** | ΔAIC |
|---|---|---|---|---|---|---|---|---|
| A: intercept only | 0 | 2 | 375,000 | 10.5321 | 133.70 | 4 | **137.70** | +15.66 |
| B: 1 predictor | 1 | 3 | 90,000 | 9.1050 | 119.43 | 6 | **125.43** | +3.39 |
| **C: 3 predictors** | 3 | 5 | 43,000 | 8.3664 | 112.04 | 10 | **122.04** | **0.00** |
| D: 6 predictors | 6 | 8 | 40,000 | 8.2940 | 111.32 | 16 | **127.32** | +5.28 |

**Model C wins.** Reading the table:
- **A → B:** RSS falls from 375,000 to 90,000 — an enormous improvement that easily pays the 2-parameter cost. AIC drops 12.3.
- **B → C:** RSS falls from 90,000 to 43,000 — still worth the extra 2 parameters. AIC drops 3.4.
- **C → D:** RSS barely improves (43,000 → 40,000, a 7% reduction) but three more parameters cost 6 units of penalty. **AIC rises by 5.3, so the extra features are not worth it.** In-sample R² would have preferred D; AIC correctly rejects it.

**Interpreting ΔAIC — the Burnham & Anderson conventions, worth quoting:**

| ΔAIC (vs the best model) | Interpretation |
|---|---|
| 0 – 2 | Essentially indistinguishable; both models are supported |
| 2 – 4 | The best model is somewhat better |
| 4 – 7 | Considerably less support for the worse model |
| > 10 | Essentially no support for the worse model |

Our B is at ΔAIC = 3.39, so it is a plausible alternative to C — with only 10 observations we should not be confident. D at 5.28 has considerably less support, and A at 15.68 is decisively rejected.

**Akaike weights** turn ΔAIC into probabilities:
```
                exp(−ΔAICᵢ/2)
wᵢ  =  ──────────────────────────
             Σⱼ exp(−ΔAICⱼ/2)
```
Ours: `w_C = 0.797`, `w_B = 0.146`, `w_D = 0.057`, `w_A = 0.000`. So there is roughly an 80% chance model C is the best of this set by AIC's criterion — a much more honest summary than "C wins."

### 5. Python
```python
import numpy as np

def aic_gaussian(y_true, y_pred, n_params, include_sigma=True):
    """
    AIC for a Gaussian-error regression model.
    n_params = number of predictors + 1 (intercept); sigma^2 added if include_sigma.
    """
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    n   = len(y_true)
    rss = ((y_true - y_pred) ** 2).sum()
    k   = n_params + (1 if include_sigma else 0)
    ll  = -0.5 * n * (np.log(2 * np.pi) + np.log(rss / n) + 1)
    return 2 * k - 2 * ll

aic_gaussian(y, y_pred, n_params=4)        # 122.042   (3 predictors + intercept, + sigma)

# statsmodels reports it directly and handles the parameter count for you
# import statsmodels.api as sm
# res = sm.OLS(y, sm.add_constant(X)).fit()
# res.aic, res.bic, res.llf, res.df_model

# Akaike weights
def akaike_weights(aics):
    aics = np.asarray(aics, float)
    d = aics - aics.min()
    w = np.exp(-d / 2)
    return w / w.sum()

akaike_weights([137.70, 125.43, 122.04, 127.32])
# array([3.0e-04, 0.146, 0.797, 0.057])
```
Line-by-line and the traps:
- **The `include_sigma` flag matters.** `k = p + 2` for OLS (slopes + intercept + σ²). Some references use `k = p + 1`, which shifts every AIC by 2 — harmless for *comparison within one convention* but fatal if you mix conventions.
- **statsmodels' `.aic` includes all constants**, so its absolute values differ from the shortcut form. **Only compare AICs computed the same way, on the same data, with the same n.**
- **Never compare AIC across models fitted to different numbers of observations** (e.g. after dropping rows with missing values in one model but not another) — the `n·ln(...)` term scales with n and the comparison is meaningless.
- **AIC is not defined for models without a likelihood.** Random forests, GBMs, and neural nets have no clean k, so use cross-validation.

### 6. Interpretation
AIC values themselves are meaningless; **ΔAIC** and Akaike weights are what you interpret. Use the Burnham & Anderson bands above. Report the full table of candidate models with ΔAIC and weights, not just the winner.

### 7. Good vs bad values
There is no such thing as a "good AIC." There is only a *lower* AIC among candidates fitted to the same data with the same n and the same convention.

### 8. Business use cases
- **Econometrics and time-series order selection** — choosing p, d, q in ARIMA is done almost universally by AIC (or AICc). `statsmodels`' and `pmdarima`'s `auto_arima` search AIC by default.
- **Classical statistical modelling** — GLM and mixed-model specification searches.
- **Small-sample settings** where holding out data is too costly — AIC's whole appeal is estimating out-of-sample error without a holdout.
- **Actuarial and credit-risk model documentation**, where GLMs dominate and AIC/BIC are the expected criteria.
- **Ecology and biostatistics** — model averaging with Akaike weights is standard practice.
- **Variable selection in linear/GLM pipelines**, as a fast screen before more expensive cross-validation.
- **Expensive-to-refit models** where k-fold CV would require k full fits.

### 9. Advantages
- **Estimates out-of-sample error without holding data out** — decisive when data is scarce.
- **Asymptotically equivalent to leave-one-out cross-validation**, so it targets the right quantity with a principled justification.
- **Cheap** — one fit, one arithmetic expression.
- **Comparable across non-nested models** fitted to the same data (unlike an F-test, which requires nesting).
- **Akaike weights** provide a natural basis for model averaging and for honest expression of selection uncertainty.
- Well-established with widely-cited interpretation conventions.

### 10. Limitations
- **Requires a likelihood** and a well-defined parameter count. Not applicable to tree ensembles, deep networks, or any model with implicit regularisation.
- **Assumes a correctly-specified likelihood family.** For OLS-AIC that means Gaussian, homoscedastic, independent errors. Under heteroscedasticity or autocorrelation the likelihood is wrong and AIC is misleading.
- **An asymptotic result** — it is biased for small n relative to k, which is exactly what **AICc** corrects (see 9.2). With `n/k < 40` you should use AICc.
- **Not consistent for model selection:** as `n → ∞`, AIC has a non-vanishing probability of selecting an over-parameterised model. It is optimising *prediction*, not *identification* — which is a feature, not a bug, but must be understood.
- **Absolute values are convention-dependent** and not comparable across software.
- **Not comparable across different n**, or across different target transformations (an AIC on `y` and one on `log y` are incomparable, because the likelihood is of a different quantity — you would need a Jacobian correction).
- Penalises parameters equally regardless of their nature, which is crude for regularised models where effective degrees of freedom are fractional.

### 11. Common mistakes
1. **Miscounting k** — forgetting σ² for OLS, or forgetting the intercept.
2. **Comparing AICs from different software** or different formula conventions.
3. **Comparing AICs across models fitted to different sample sizes** (a silent trap when missing-value handling differs between models).
4. **Comparing AIC across target transformations** without a Jacobian correction.
5. **Using AIC for a random forest or neural network.** There is no valid k.
6. **Reporting only the winner** instead of the ΔAIC table and weights, which hides selection uncertainty.
7. **Using AIC when n/k < 40** instead of AICc.
8. **Treating AIC selection as a hypothesis test.** It is not; there is no p-value and no error rate.

### 12. Interview questions

**Easy — What is AIC?** `2k − 2ln L̂`: the deviance plus twice the number of parameters. Lower is better, and only differences are meaningful.

**Easy — For OLS with 4 predictors and an intercept, what is k?** 6 — four slopes, one intercept, and σ².

**Medium — ★ What is AIC actually estimating?**
The expected out-of-sample predictive deviance. Akaike's insight was that the in-sample log-likelihood is optimistically biased as an estimate of out-of-sample log-likelihood, and that the bias is approximately k, so adding 2k to the deviance corrects it. So AIC is an *analytic estimate of generalisation error* obtained without holding out data.

**Medium — ★ Relationship between AIC and cross-validation?**
AIC is **asymptotically equivalent to leave-one-out cross-validation.** Both estimate expected out-of-sample predictive performance; AIC does it analytically under likelihood assumptions, LOO-CV does it empirically without them. Practically: use CV when you can afford it and when the model has no clean likelihood or parameter count; use AIC when refitting is expensive, data is scarce, or you are in a classical modelling context where it is the expected vocabulary. If they disagree substantially, trust CV, because it makes fewer assumptions.

**Medium — ★ AIC vs BIC — which and when?**
Their penalties differ: AIC charges `2k`, BIC charges `k·ln(n)`. Since `ln(n) > 2` for `n > 7`, **BIC is stricter for any realistic sample size and gets stricter as n grows.** They answer different questions: **AIC targets predictive accuracy** (asymptotically equivalent to LOO-CV) and will happily keep a small, slightly-helpful variable; **BIC targets identifying the true model** and is consistent — if the true model is among the candidates, BIC selects it with probability → 1 as `n → ∞`, which AIC does not. Practical guidance: AIC if the goal is prediction, BIC if the goal is parsimonious explanation or you want a smaller model for interpretability. Report both; if they disagree you have a genuinely borderline variable, which is itself useful information.

**Hard — Why is AIC not "consistent" for model selection, and is that a problem?**
Consistency means the probability of selecting the true model tends to 1 as `n → ∞`. AIC's penalty `2k` does not grow with n, so the deviance improvement from adding a spurious parameter — which is O(1) in expectation, roughly chi-squared with 1 degree of freedom — remains competitive with the fixed cost of 2 forever. So AIC retains a non-vanishing probability (about 16% per spurious parameter) of over-fitting even with infinite data. BIC's penalty `k·ln n` grows, so spurious parameters are eventually always rejected. **Is it a problem? Only if you care about identification.** AIC is *designed* to minimise prediction error, and a slightly over-parameterised model often predicts better than a slightly under-parameterised one because the variance cost of an extra weak parameter is small while the bias cost of omitting a real one is not. So AIC's "inconsistency" is the correct behaviour for its stated goal, and criticising it for failing at a goal it does not have is a common misunderstanding.

---

## 9.2 AICc (CORRECTED AIC)

**Definition.** AIC with a small-sample bias correction.
```
                       2k ( k + 1 )
AICc  =  AIC  +  ─────────────────────
                       n − k − 1
```
- The correction term is always positive and **grows as k approaches n**, so AICc penalises complexity much more aggressively in small samples.
- As `n → ∞` with k fixed, the correction → 0 and `AICc → AIC`.
- **Undefined when `n = k + 1`** (division by zero) — a signal that you have as many parameters as data.

**Manual example** (our model: n = 10, k = 5, AIC = 122.042):
```
correction = 2 × 5 × (5+1) / (10 − 5 − 1)
           = 60 / 4
           = 15.0

AICc = 122.042 + 15.0 = 137.042
```
**AICc = 137.04 versus AIC = 122.04 — a correction of 15 units, which is enormous.** With `n/k = 10/5 = 2`, we are deep in small-sample territory and AIC is badly optimistic.

**Redoing the model comparison with AICc:**

| Model | p | k | AIC | correction | **AICc** | ΔAICc |
|---|---|---|---|---|---|---|
| A: intercept only | 0 | 2 | 137.70 | 2(2)(3)/(10−2−1) = 1.71 | **139.41** | +9.98 |
| **B: 1 predictor** | 1 | 3 | 125.43 | 2(3)(4)/(10−3−1) = 4.00 | **129.43** | **0.00** |
| C: 3 predictors | 3 | 5 | 122.04 | 2(5)(6)/(10−5−1) = 15.00 | **137.04** | +7.61 |
| D: 6 predictors | 6 | 8 | 127.32 | 2(8)(9)/(10−8−1) = 144.00 | **271.32** | +141.89 |

**The winner changes from C to B.** With only 10 observations, AICc says a **single predictor** is all the data can support, and that the 3-predictor model C is considerably worse (ΔAICc = 7.6). Model D becomes absurd (correction of 144).

**This is the single most important practical lesson about AIC:** with small n it will confidently recommend a model that is over-fitted, and AICc fixes it. **The rule of thumb: use AICc whenever `n / k < 40`.** Ours is 2. Many published analyses have quietly made this mistake.

**Python**
```python
def aicc_gaussian(y_true, y_pred, n_params, include_sigma=True):
    n = len(y_true)
    k = n_params + (1 if include_sigma else 0)
    aic = aic_gaussian(y_true, y_pred, n_params, include_sigma)
    if n - k - 1 <= 0:
        return np.inf                       # not enough data for this many parameters
    return aic + (2 * k * (k + 1)) / (n - k - 1)

aicc_gaussian(y, y_pred, n_params=4)        # 137.042
```

**When to use:** always, when `n/k < 40`. It costs nothing and converges to AIC when n is large, so **AICc is a strictly safer default than AIC.** It is the default in `pmdarima`'s `auto_arima` for short series and is standard practice in ecology and in any small-sample field.

**Interview (Medium) — ★ When must you use AICc instead of AIC?** Whenever the sample size is small relative to the number of parameters — the conventional threshold is `n/k < 40`. AIC is an asymptotic result and is optimistically biased in small samples, so it systematically over-selects complex models. AICc adds `2k(k+1)/(n−k−1)`, which vanishes as n grows, so it is safe to use always. In our 10-observation example the correction changed the selected model from three predictors to one.

---

## 9.3 BAYESIAN INFORMATION CRITERION (BIC / SIC / SBC)

### 1. Definition
Like AIC, but with a complexity penalty of `k·ln(n)` rather than `2k`, derived as an approximation to the log marginal likelihood of the model.

### 2. Intuition
BIC asks a different question from AIC: **"which of these models is most likely to be the true one?"** rather than "which will predict best?"

Its derivation is Bayesian: `−2 × BIC` approximates twice the log **marginal likelihood** (the model evidence) under a unit-information prior, so **differences in BIC approximate log Bayes factors.** That gives it a direct probabilistic interpretation that AIC lacks.

Practically, the thing to remember is that **BIC is much stricter, and gets stricter as n grows**, because `ln(n)` replaces the constant 2. It therefore favours smaller, more parsimonious models — which is what you want for explanation and interpretability, and often not what you want for pure prediction.

### 3. Formula
```
BIC  =  k · ln(n)  −  2 ln L̂
```
- **k** = number of estimated parameters (same convention as AIC: `p + 2` for OLS)
- **n** = number of observations
- **ln(n)** = the penalty per parameter, replacing AIC's constant 2

**The crossover:** `ln(n) > 2` when `n > e² ≈ 7.39`. So for essentially any real dataset, **BIC penalises complexity more heavily than AIC**, and the gap widens with n:

| n | ln(n) | Penalty per parameter | vs AIC's 2 |
|---|---|---|---|
| 10 | 2.30 | 2.30 | 1.15× |
| 100 | 4.61 | 4.61 | 2.30× |
| 1,000 | 6.91 | 6.91 | 3.45× |
| 100,000 | 11.51 | 11.51 | 5.76× |
| 1,000,000 | 13.82 | 13.82 | 6.91× |

**At n = 1,000,000, BIC charges nearly 7× what AIC charges per parameter.** On large datasets BIC will select noticeably smaller models than AIC.

Range (−∞, +∞); lower is better; only differences are meaningful.

### 4. Manual example

Our model: `n = 10`, `k = 5`, `−2 ln L̂ = 112.042474`.
```
Step 1 — penalty:
  ln(10) = 2.302585
  k · ln(n) = 5 × 2.302585 = 11.512925

Step 2 — BIC:
  BIC = 11.512925 + 112.042474 = 123.555399
```
**BIC = 123.56** versus **AIC = 122.04** — only 1.5 apart, because with n = 10, `ln(n) = 2.30` is barely above 2.

**The full comparison, showing how AIC and BIC diverge:**

| Model | p | k | −2lnL̂ | AIC penalty (2k) | **AIC** | BIC penalty (k·ln10) | **BIC** | AICc |
|---|---|---|---|---|---|---|---|---|
| A | 0 | 2 | 133.70 | 4 | 137.70 | 4.61 | **138.30** | 139.41 |
| **B** | 1 | 3 | 119.43 | 6 | 125.43 | 6.91 | **126.34** | **129.43** ← AICc |
| **C** | 3 | 5 | 112.04 | 10 | **122.04** ← AIC | 11.51 | **123.56** ← BIC | 137.04 |
| D | 6 | 8 | 111.32 | 16 | 127.32 | 18.42 | **129.74** | 271.32 |

**Three criteria, and with n = 10 they give two different answers:** AIC and BIC both pick C; AICc picks B. That disagreement is the honest signal that **10 observations cannot distinguish these models**, and the right response is to say so rather than to pick a winner.

**With a larger n the criteria separate more decisively.** If the same RSS pattern occurred with n = 1,000 (scaling RSS proportionally), BIC's penalty per parameter would be 6.91 versus AIC's 2, and BIC would likely choose B where AIC chose C.

**Interpreting ΔBIC as evidence (Kass & Raftery conventions):**

| ΔBIC | Bayes factor | Evidence against the worse model |
|---|---|---|
| 0 – 2 | 1 – 3 | Not worth more than a bare mention |
| 2 – 6 | 3 – 20 | Positive |
| 6 – 10 | 20 – 150 | Strong |
| > 10 | > 150 | Very strong |

Ours: `ΔBIC(B vs C) = 126.34 − 123.56 = 2.78` — only "positive" evidence for C, again confirming that the data cannot settle the question.

**BIC weights** (approximate posterior model probabilities, assuming equal priors):
```
                exp(−ΔBICᵢ/2)
Pr(Mᵢ|data) ≈ ───────────────────
                Σⱼ exp(−ΔBICⱼ/2)
```

### 5. Python
```python
import numpy as np

def bic_gaussian(y_true, y_pred, n_params, include_sigma=True):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    n   = len(y_true)
    rss = ((y_true - y_pred) ** 2).sum()
    k   = n_params + (1 if include_sigma else 0)
    ll  = -0.5 * n * (np.log(2 * np.pi) + np.log(rss / n) + 1)
    return k * np.log(n) - 2 * ll

bic_gaussian(y, y_pred, n_params=4)        # 123.555

# statsmodels
# res.bic

# A convenient side-by-side comparison table
def compare_models(fits, y_true):
    """fits: list of (name, y_pred, n_params)."""
    rows = []
    for name, yp, p in fits:
        rows.append({
            'model': name, 'p': p,
            'RSS':   ((y_true - yp)**2).sum(),
            'AIC':   aic_gaussian(y_true, yp, p),
            'AICc':  aicc_gaussian(y_true, yp, p),
            'BIC':   bic_gaussian(y_true, yp, p),
        })
    import pandas as pd
    df = pd.DataFrame(rows)
    for c in ('AIC', 'AICc', 'BIC'):
        df['d' + c] = df[c] - df[c].min()
    return df.sort_values('AICc')
```
- **Also available: `sklearn.linear_model.LassoLarsIC(criterion='aic'|'bic')`**, which selects the lasso regularisation strength by AIC or BIC using the number of non-zero coefficients as k. A neat, cheap alternative to cross-validated lasso.

### 6. Interpretation
Only ΔBIC matters. Use the Kass & Raftery bands, and report BIC weights to express selection uncertainty honestly.

### 7. Good vs bad values
As with AIC: there is no good absolute value, only a lower one among comparable candidates.

### 8. Business use cases
- **Explanatory modelling** where a parsimonious, interpretable model is the deliverable — economics, epidemiology, social science.
- **Regulated model documentation** (credit risk, insurance) where a small, defensible variable set is required for explainability and where regulators are suspicious of complexity.
- **Time-series order selection** — offered alongside AIC in every ARIMA implementation; BIC gives lower-order, more stable models.
- **Bayesian model comparison and model averaging** — ΔBIC approximates log Bayes factors, so it plugs directly into a Bayesian workflow.
- **Clustering** — BIC is the standard criterion for choosing the number of components in Gaussian mixture models (`GaussianMixture(...).bic(X)`), which is one of its most common practical uses in ML.
- **Large-n variable selection** where you want to resist the tendency of large samples to make every variable "significant."
- **Structure learning** in graphical models and Bayesian networks.

### 9. Advantages
- **Consistent for model selection** — if the true model is among the candidates, BIC finds it with probability → 1 as n → ∞. AIC does not.
- **Favours parsimony**, which aids interpretability, stability, and regulatory acceptance.
- **ΔBIC approximates log Bayes factors**, giving a genuine probabilistic interpretation and enabling posterior model probabilities.
- Cheap — one fit.
- Penalty grows with n, correctly resisting the large-sample tendency to over-select.
- Standard for choosing the number of clusters/components in mixture models.

### 10. Limitations
- **Assumes the true model is in the candidate set** — a strong and usually false assumption ("all models are wrong"). When it fails, BIC's consistency guarantee is vacuous and its parsimony may simply mean under-fitting.
- **Often under-fits for predictive purposes**, especially with many weak-but-real predictors — exactly the situation in most modern ML problems. If prediction is the goal, AIC or cross-validation usually gives a better model.
- Same structural limitations as AIC: **requires a likelihood and a parameter count**, so not usable for tree ensembles or deep networks; assumes a correctly-specified error family; absolute values are convention-dependent; not comparable across different n or target transformations.
- The unit-information prior implicit in the derivation is arbitrary and may not reflect genuine prior beliefs.
- No small-sample correction as standard (though variants exist).
- Treats all parameters as equally costly.

### 11. Common mistakes
1. **Using BIC when the goal is prediction.** It will under-fit. Use AIC or cross-validation.
2. **Believing the "true model" assumption is harmless.** It is the assumption that licenses BIC's consistency, and it is essentially always false.
3. Miscounting k, or mixing conventions between models.
4. Comparing BICs across different n, different software, or different target transformations.
5. Using BIC for models without a likelihood.
6. Reporting only the winner rather than the ΔBIC table and weights.
7. **Reporting AIC and BIC as if they were two independent pieces of evidence.** They are the same deviance with different penalties; if they agree that is one finding, and if they disagree that is the interesting finding.

### 12. Interview questions

**Easy — What is BIC and how does its penalty differ from AIC's?** `BIC = k·ln(n) − 2lnL̂`. Its penalty is `k·ln(n)` rather than AIC's `2k`, so it is stricter for any `n > 7` and gets stricter as n grows.

**Easy — At what n do AIC and BIC penalties coincide?** `n = e² ≈ 7.4`.

**Medium — ★ AIC vs BIC: what different questions do they answer?**
AIC estimates **out-of-sample predictive deviance** and is asymptotically equivalent to leave-one-out cross-validation — its goal is prediction. BIC approximates the **log marginal likelihood** and is consistent for identifying the true model if it is in the candidate set — its goal is explanation. Consequently AIC keeps weak-but-real predictors that improve prediction slightly, and BIC discards them for parsimony. Use AIC/CV for prediction, BIC for parsimonious explanation, and report both because disagreement flags a borderline variable.

**Medium — Why does BIC's penalty grow with n?**
Because it comes from a Laplace approximation to the marginal likelihood, in which each additional parameter contributes a factor of roughly `n^(−1/2)` to the integrated likelihood — a penalty of `½ln(n)` per parameter in log terms, giving `k·ln(n)` in the `−2 log` scale. Intuitively: with more data you can detect smaller true effects, so a parameter must clear a *higher* bar of evidence to be worth including, otherwise large samples would make every trivial effect "worth keeping."

**Hard — ★ Your AIC picks a 12-variable model and your BIC picks a 5-variable model. What do you do?**
Recognise that they are answering different questions and let the *purpose* decide. If the deliverable is a **prediction system**, follow AIC — and then verify with **cross-validated RMSE**, which is the direct empirical estimate of what AIC approximates. If the deliverable is an **explanatory or regulatory model** where interpretability and stability matter, follow BIC. Then investigate the seven disputed variables specifically: check their cross-validated marginal contribution, their coefficient stability across folds and across time, their collinearity with the retained five, and whether they have a plausible causal story. Often you will find they are collinear proxies adding little, in which case BIC is right; occasionally you will find a few carry genuine independent signal, in which case a model between the two is best. Finally, if `n/k < 40`, recompute with **AICc**, which may well move AIC's choice toward BIC's — that is a common resolution and is worth checking before anything else.

---

## 9.4 MALLOWS' Cp

**Definition.** An estimate of the total standardised mean squared prediction error of a subset model, benchmarked against the full model's error variance.
```
             RSS_p
Cp  =  ───────────  −  n  +  2p
             σ̂²_full
```
- **RSS_p** = residual sum of squares of the candidate model with p predictors
- **σ̂²_full** = the error variance estimated from the **full** model (all candidate predictors), i.e. `RSS_full/(n − p_full − 1)`
- **p** = number of parameters in the candidate model **including** the intercept
- **The target: `Cp ≈ p`.** A model with `Cp ≈ p` has negligible bias; `Cp ≫ p` indicates important omitted variables.

**Intuition.** Cp asks: **"how much prediction error do I incur by dropping variables, measured in units of the full model's noise?"** If dropping variables introduced no bias, the expected value of Cp is exactly p. So you plot Cp against p and look for models sitting on or below the `Cp = p` line, choosing the smallest such p.

**Manual example.** Take the full model to be D (6 predictors, RSS = 40,000, n = 10):
```
σ̂²_full = RSS_full / (n − p_full − 1) = 40,000 / (10 − 6 − 1) = 40,000/3 = 13,333.3

Model C (3 predictors, so p = 4 including intercept; RSS = 43,000):
  Cp = 43,000 / 13,333.3 − 10 + 2(4)
     = 3.225 − 10 + 8
     = 1.225

Compare to p = 4:  Cp (1.23) < p (4)  ->  no evidence of important omitted bias

Model B (1 predictor, p = 2; RSS = 90,000):
  Cp = 90,000/13,333.3 − 10 + 4
     = 6.750 − 10 + 4
     = 0.750
Compare to p = 2:  Cp (0.75) < p (2)  ->  also acceptable

Model A (intercept only, p = 1; RSS = 375,000):
  Cp = 375,000/13,333.3 − 10 + 2
     = 28.125 − 10 + 2
     = 20.125
Compare to p = 1:  Cp (20.1) >> p (1)  ->  SEVERE omitted-variable bias
```
So Cp decisively rejects the intercept-only model and finds both B and C acceptable, agreeing with the AIC/AICc ambiguity. (With such a small n these values are unstable; the illustration is the method, not the conclusion.)

**Python**
```python
import numpy as np

def mallows_cp(y_true, y_pred_sub, p_sub, rss_full, n, p_full):
    """p_sub, p_full count parameters INCLUDING the intercept."""
    sigma2_full = rss_full / (n - p_full - 1)
    rss_p = ((np.asarray(y_true, float) - np.asarray(y_pred_sub, float))**2).sum()
    return rss_p / sigma2_full - n + 2 * p_sub

mallows_cp(y, y_pred, p_sub=4, rss_full=40000, n=10, p_full=6)   # 1.225
```

**Relationship to AIC.** For Gaussian OLS with a known σ², **Mallows' Cp and AIC select the same model** — they are monotonically related. Cp came from the linear-model literature (Mallows, 1973) and AIC from information theory, and their agreement in the Gaussian linear case is a satisfying convergence. Cp survives mainly in classical regression texts, best-subset-selection tooling, and the `leaps`/`regsubsets` tradition in R.

**Limitations:** requires a trustworthy full model to estimate σ² — which fails when `p_full` is close to n, or when the full model is itself badly specified; only defined for linear models; no small-sample correction; superseded in practice by AIC/AICc and cross-validation.

**Interview (Medium) — What is Mallows' Cp and what value do you look for?** An estimate of standardised total prediction error for a subset model. You look for `Cp ≈ p` (or below), which indicates no substantial bias from the omitted variables, and among such models you choose the smallest p. `Cp ≫ p` means important variables have been dropped.

**Interview (Hard) — Cp requires estimating σ² from the full model. When does that break?** When the full model is itself over-parameterised or misspecified. If `p_full` approaches n, `σ̂²_full = RSS_full/(n − p_full − 1)` is estimated from very few degrees of freedom and is both unstable and biased downward (the full model over-fits and its residual variance understates the true noise). An artificially small σ̂² inflates every Cp, making all subset models look badly biased and pushing you toward the full model — precisely the wrong direction. In the modern `p > n` regime Cp is unusable, which is why cross-validation and regularisation-path methods replaced it.

---

## 9.5 PRESS AND CROSS-VALIDATED ERROR

### 1. Definition
- **PRESS (Prediction Sum of Squares):** the leave-one-out cross-validated sum of squared errors.
- **Cross-validated RMSE/MAE:** the same idea generalised to k folds and to any metric.

### 2. Intuition
This is the empirical alternative to AIC/BIC, and **the primary tool in modern practice**: instead of *estimating* out-of-sample error analytically, **measure it** by repeatedly holding data out.

No likelihood assumption, no parameter count, no asymptotics. It works for any model — linear, tree, ensemble, neural — and it directly estimates the quantity you actually care about. Its cost is computational (k refits) and, for small data, variance.

### 3. Formula
```
                n
PRESS  =       Σ   ( yᵢ − ŷ₍₋ᵢ₎ )²
               i=1
```
- **ŷ₍₋ᵢ₎** = the prediction for observation i from a model fitted **without** observation i
- So each prediction is genuinely out-of-sample.

**Predicted R²** (a.k.a. `Q²`, R²_pred, or cross-validated R²):
```
                        PRESS
R²_pred  =  1  −  ───────────────
                        SS_tot
```
**The comparison `R² vs R²_pred` is the single best cheap overfitting diagnostic for a linear model.** A large gap means the model does not generalise.

**The OLS shortcut — a genuinely useful piece of knowledge.** For linear models you get LOO-CV **for free**, with no refitting, using the hat matrix:
```
                     eᵢ
ŷᵢ − ŷ₍₋ᵢ₎  ->   ───────────         so       PRESS  =  Σ  ( eᵢ / (1 − hᵢᵢ) )²
                   1 − hᵢᵢ
```
- **eᵢ** = the ordinary in-sample residual
- **hᵢᵢ** = the **leverage** of observation i, the i-th diagonal element of the hat matrix `H = X(XᵀX)⁻¹Xᵀ`
- `Σ hᵢᵢ = p + 1` (the number of parameters), and `0 ≤ hᵢᵢ ≤ 1`
- **High-leverage points get their residuals inflated**, which is exactly right: an observation the model bends to accommodate would be predicted badly if it were removed.

**General k-fold cross-validation:**
```
                     1    K
CV metric  =        ───  Σ   metric( y_fold k , ŷ_fold k )
                     K   k=1
```
with the model refitted on the other K−1 folds each time.

### 4. Manual example

Suppose our 10 observations have leverages `hᵢᵢ` (which must sum to `p+1 = 4` for a 3-predictor model with intercept):
```
i    eᵢ      hᵢᵢ     1−hᵢᵢ    eᵢ/(1−hᵢᵢ)   squared
1   −20     0.20     0.80      −25.00        625.0
2   +10     0.15     0.85      +11.76        138.4
3   −10     0.12     0.88      −11.36        129.1
4   +20     0.10     0.90      +22.22        493.8
5   −20     0.10     0.90      −22.22        493.8
6   +20     0.10     0.90      +22.22        493.8
7   −20     0.12     0.88      −22.73        516.5
8   +20     0.15     0.85      +23.53        553.6
9   −20     0.21     0.79      −25.32        641.0
10 +200     0.75     0.25     +800.00     640,000.0     <-- HIGH LEVERAGE
                                          -----------
                          Σ  hᵢᵢ = 2.00 (illustrative)   PRESS = 644,085

R²_pred = 1 − 644,085 / 375,000 = 1 − 1.7176 = −0.7176
```
**R²_pred = −0.72 versus in-sample R² = +0.885.**

**This is the most important single number in Part 9.** The in-sample fit says the model explains 88.5% of the variance. Leave-one-out cross-validation says it is **worse than predicting the mean**. The cause is entirely observation 10: with leverage 0.75, the model is bending itself to accommodate that one house, and if that house were removed from training the prediction for it would be catastrophically wrong (`e/(1−h) = 200/0.25 = 800`).

**The lesson:** a high in-sample R² on a small dataset with a high-leverage point is close to meaningless. **Always compute R²_pred (or a proper CV score) before believing an in-sample fit.** The gap between them is your overfitting measure.

(The leverage values above are illustrative rather than derived from actual X data, since we never specified the features — but the mechanism and the arithmetic are exactly as shown.)

### 5. Python
```python
import numpy as np
from sklearn.model_selection import cross_val_score, KFold, TimeSeriesSplit, GroupKFold
from sklearn.metrics import make_scorer, mean_absolute_error

# --- General k-fold CV, the primary tool ---
cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Note the neg_ prefix: sklearn scorers are "greater is better"
rmse_scores = -cross_val_score(model, X, y, cv=cv,
                               scoring='neg_root_mean_squared_error')
print(f"CV RMSE = {rmse_scores.mean():.3f} +/- {rmse_scores.std():.3f}")

# Report the SPREAD, not just the mean -- it tells you how stable the estimate is
r2_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')

# --- Multiple metrics at once ---
from sklearn.model_selection import cross_validate
res = cross_validate(model, X, y, cv=cv,
                     scoring=['neg_root_mean_squared_error',
                              'neg_mean_absolute_error', 'r2'],
                     return_train_score=True)   # <- train vs test gap = overfitting

# --- PRESS / LOO for a linear model, via leverage (no refitting) ---
def press_ols(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])            # add intercept
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    resid = y - X1 @ beta
    H = X1 @ np.linalg.pinv(X1.T @ X1) @ X1.T             # hat matrix
    h = np.diag(H)
    press = np.sum((resid / (1 - h)) ** 2)
    r2_pred = 1 - press / ((y - y.mean()) ** 2).sum()
    return press, r2_pred, h

# --- CRITICAL: the right CV scheme for the data structure ---
# TimeSeriesSplit(n_splits=5)      -> time series: never train on the future
# GroupKFold(n_splits=5)           -> grouped data: keep a group entirely in one fold
# KFold(shuffle=True)              -> i.i.d. data only
```
Line-by-line and the traps:
- **`cross_val_score` returns negated losses** for loss metrics. Negate to report.
- **Report the standard deviation across folds.** A CV RMSE of `65 ± 3` and `65 ± 30` are very different situations; the second means your estimate is unreliable and you need repeated CV or more data.
- **`return_train_score=True`** gives you the train-vs-test gap for free — the cleanest overfitting diagnostic available.
- **The CV scheme must match the data structure**, and getting this wrong is the most damaging mistake in this Part:
  - **Time series** → `TimeSeriesSplit` (expanding or rolling window). Shuffled K-fold **leaks the future into the past** and produces wildly optimistic scores.
  - **Grouped data** (multiple rows per customer, patient, store, or document) → `GroupKFold`. Otherwise near-duplicate rows appear in both train and test.
  - **Spatial data** → blocked/spatial CV, because nearby points are correlated.
  - **Any preprocessing** (scaling, imputation, target encoding, feature selection) must go **inside a `Pipeline`** so it is fitted on the training fold only. Fitting a scaler or a target encoder on all the data before CV is a classic silent leak.

### 6. Interpretation

**The three-number comparison you should always report:**
```
In-sample RMSE      -> optimistically biased; the model has seen this data
CV / out-of-sample  -> the honest estimate of generalisation
The gap             -> your overfitting measure
```

| Train vs CV gap | Diagnosis |
|---|---|
| Small (CV ≈ train) | Well-regularised, or under-fitting — check whether both are poor |
| Moderate | Normal for a flexible model |
| **Large** (CV ≫ train) | **Overfitting.** Reduce complexity, add regularisation, get more data |
| CV RMSE > σ(y), i.e. CV R² < 0 | The model is worse than the mean — badly broken or badly over-fitted |

### 7. Good vs bad values
Judge the CV metric against the same baselines as always (σ(y), a naive model, the previous production model), and always with its fold-to-fold standard deviation attached.

### 8. Business use cases
- **Essentially all modern model selection and hyperparameter tuning** — `GridSearchCV`, `RandomizedSearchCV`, Optuna, and every AutoML system are cross-validation loops.
- **Early stopping** in gradient boosting and neural networks uses a validation fold.
- **Feature selection** with a proper wrapper method.
- **Comparing fundamentally different model families** (linear vs GBM vs neural net) where no shared likelihood or parameter count exists, so AIC/BIC cannot be used.
- **Estimating the uncertainty of a performance estimate** via the fold-to-fold spread or repeated CV.
- **Regulated model validation**, where out-of-time and out-of-sample testing is mandated.
- **Nested CV** when you need an unbiased estimate of performance *after* hyperparameter tuning.

### 9. Advantages
- **Assumption-free** — no likelihood, no parameter count, no asymptotics, no distributional form.
- **Works for any model**, including those with no meaningful k.
- **Directly estimates generalisation error**, the quantity of interest, rather than approximating it.
- **Works with any metric**, including business-specific and asymmetric ones.
- **Provides an uncertainty estimate** through the fold-to-fold spread.
- Extends naturally to time series, grouped, and spatial structures with the right splitter.
- The `train_score` vs `test_score` gap is a free, direct overfitting diagnostic.

### 10. Limitations
- **Computationally expensive** — k refits, and `k × (hyperparameter grid)` for tuning. LOO-CV is n refits, which is prohibitive except for models with an analytic shortcut.
- **High variance on small datasets**, where each fold's estimate is noisy. Mitigate with **repeated k-fold** and by reporting the spread.
- **Leakage is easy and silent.** Preprocessing outside the pipeline, shuffled splits on time series, ungrouped splits on grouped data, and target encoding fitted on all data are all common and all produce optimistic scores that only reveal themselves in production.
- **Slightly pessimistic** as an estimate of the final model's performance, because each fold model is trained on only `(K−1)/K` of the data.
- **Selection bias:** if you use CV to choose among many models and then report that model's CV score, the reported score is optimistically biased. **Nested cross-validation** or a held-out final test set is required for an honest number.
- LOO-CV has low bias but high variance and is not always preferable to 5- or 10-fold.
- Does not, by itself, tell you *why* the model fails — residual diagnostics do that.

### 11. Common mistakes
1. **Shuffled K-fold on time-series data.** Trains on the future to predict the past; produces spectacular, meaningless scores. Use `TimeSeriesSplit`.
2. **Not grouping** when rows are correlated within customers/patients/stores. Near-duplicate rows straddle the split and inflate the score.
3. **Preprocessing outside the pipeline** — fitting a scaler, imputer, PCA, or target encoder on the full dataset before splitting. A silent, very common leak.
4. **Reporting the best CV score from a large hyperparameter search as the expected performance.** That number is optimistically biased by the selection itself; use nested CV or a final untouched test set.
5. **Reporting only the mean CV score** without the fold-to-fold standard deviation.
6. **Forgetting the `neg_` prefix** and reporting negative RMSEs.
7. **Using in-sample R² or RMSE for model selection at all.**
8. Choosing K = 2 or K = n reflexively; 5 or 10 is the usual bias-variance sweet spot.

### 12. Interview questions

**Easy — What is PRESS?** The leave-one-out cross-validated sum of squared errors.

**Easy — What is predicted R²?** `1 − PRESS/SS_tot` — the cross-validated analogue of R². It can be negative, and a large gap from in-sample R² indicates overfitting.

**Medium — ★ Why can you compute LOO-CV for a linear model without refitting n times?**
Because of the hat-matrix identity `y_i − ŷ₍₋ᵢ₎ = eᵢ/(1 − hᵢᵢ)`, where `hᵢᵢ` is the leverage of observation i. So `PRESS = Σ(eᵢ/(1−hᵢᵢ))²` is computable from a **single** fit. This is a genuinely useful practical result and also explains *why* leverage matters: a high-leverage point has `hᵢᵢ` close to 1, so its LOO residual is enormously inflated — the model was bending to fit it, and without it the prediction would be badly wrong.

**Medium — ★ Cross-validation vs AIC: when do you use which?**
Use cross-validation as the default: it makes no assumptions, works for any model, and directly measures generalisation with any metric you choose. Use AIC when refitting is expensive, when data is too scarce to hold out, or when you are in a classical modelling context where it is the expected vocabulary. They are targeting the same quantity — AIC is asymptotically equivalent to LOO-CV — so they should broadly agree; if they disagree materially, trust CV because it relies on fewer assumptions, and investigate whether AIC's likelihood assumptions (Gaussian, homoscedastic, independent errors) are violated.

**Medium — Why report the standard deviation across folds?**
Because it tells you how reliable the point estimate is. `RMSE = 65 ± 3` supports a confident claim; `65 ± 30` means the folds disagree wildly and the number should not be used to choose between models differing by less than that. A large fold-to-fold spread usually indicates a small dataset, an influential subgroup, or a leaky/mismatched split, and it should trigger repeated CV.

**Hard — ★ Your CV RMSE is 45 and your test-set RMSE is 78. Diagnose.**
Something has gone wrong with the CV procedure or the data structure — a 73% degradation is far too large to be sampling noise. Work through the likely causes in order. (1) **Leakage in CV:** preprocessing fitted outside the pipeline (scaler, imputer, target encoder, feature selection) so the CV folds saw information from the whole dataset. (2) **Wrong split scheme:** shuffled K-fold on time-ordered data, or ungrouped folds on data with repeated entities, means the CV folds contained near-duplicates of their training data while the test set does not. (3) **Distribution shift:** the test set is from a later period or different population — check feature distributions and target level between CV data and test data. (4) **Selection bias:** if you searched a large hyperparameter space by CV, the winning CV score is optimistically biased; the honest estimate requires nested CV. (5) **Test-set peculiarity:** a small test set with a few high-leverage observations. Check the test residual distribution and whether a handful of points dominate. The fix depends on the cause, but the diagnostic order matters — check the pipeline and the split scheme first, because those are both common and both completely invalidate the CV number.

**Hard — What is nested cross-validation and when do you need it?**
An outer CV loop estimates generalisation performance while an inner CV loop, run separately inside each outer training fold, selects hyperparameters. You need it whenever you want an **unbiased estimate of the performance of your whole modelling procedure including tuning.** If you tune with a single CV loop and then report the best CV score, that score is optimistically biased because you selected the configuration that happened to do best on those particular folds — with a large search space the bias can be substantial. Nested CV costs `K_outer × K_inner` fits, so the cheaper practical alternative is to tune with CV on a development set and report performance on a **single final test set that is touched exactly once.**

## 9.6 Model selection summary

| Criterion | Penalty | Goal | Needs a likelihood? | Needs refitting? | Best for |
|---|---|---|---|---|---|
| In-sample R²/RMSE | none | — | No | No | **Never use for selection** |
| Adjusted R² | `(n−1)/(n−p−1)` | Weak parsimony | No, but needs p | No | Quick linear-model check |
| Mallows' Cp | `2p` in σ² units | Prediction | No, but needs σ̂²_full | No | Classical best-subset selection |
| **AIC** | `2k` | **Prediction** | Yes | No | Classical models; ARIMA order |
| **AICc** | `2k + 2k(k+1)/(n−k−1)` | Prediction, small n | Yes | No | **Whenever n/k < 40** |
| **BIC** | `k·ln(n)` | **True model / parsimony** | Yes | No | Explanation; GMM component count |
| PRESS / R²_pred | empirical (LOO) | Prediction | No | No (linear shortcut) | Linear-model overfitting check |
| **k-fold CV** | empirical | **Prediction, any metric** | **No** | Yes (K fits) | **The default for everything** |
| Nested CV | empirical | Unbiased post-tuning estimate | No | Yes (K×K fits) | Honest reporting after tuning |

**Penalty severity, ordered:** `Adjusted R² (F>1) < AIC (F>2) < BIC (F>ln n) < AICc when n is small`.

**The practical recipe:**
1. **Never** select on in-sample fit.
2. **Default to cross-validation** with the correct splitter for your data structure and the metric your business cares about.
3. **Add AICc (not AIC) as a cheap complement** for classical models, especially with small n.
4. **Report BIC too** if parsimony or interpretability matters; disagreement between AIC and BIC identifies the borderline variables worth investigating.
5. **Report the fold-to-fold spread**, and use a **final untouched test set** or nested CV for the number you publish.

---

# PART 10 — Time-Series Specific Metrics and Pitfalls

## 10.0 Why time series is different

Every metric in Parts 2–9 assumes the observations are exchangeable — you can shuffle them without losing information. **Time series breaks that assumption**, and the consequences are severe enough to justify a separate Part.

**Five things change:**

| Issue | Consequence |
|---|---|
| **Temporal order matters** | You must never train on the future. Shuffled K-fold CV is invalid and produces wildly optimistic scores. |
| **The naive baseline is strong** | "Tomorrow = today" is often hard to beat. Comparing to the *mean* (as R² does) is a meaninglessly low bar. |
| **Errors are autocorrelated** | Consecutive residuals are correlated, so standard errors and confidence intervals from i.i.d. formulas are wrong. |
| **The forecast horizon matters** | A 1-step-ahead error and a 12-step-ahead error are different problems. A single metric averaged over horizons hides everything. |
| **Series differ wildly in scale** | Averaging MAE across SKUs selling 5 and 50,000 units is dominated by the big one. Scaled metrics are mandatory. |

**The metrics that matter most here have already been covered:**
- **MASE** (Part 4.7) — the workhorse. Scaled by the in-sample naive MAE, well-defined with zeros, anchored at 1.0.
- **WAPE** (Part 4.3) — volume-weighted, the industry standard for supply chain.
- **Theil's U2** (Part 4.8) — the RMSE analogue of MASE.
- **MPE / total bias** (Part 4.5) — because forecast bias compounds into inventory problems.
- **Pinball loss** (Part 7.3) — for service-level and safety-stock decisions.
- **CRPS / Interval Score** (Part 8) — for probabilistic forecasts.

This Part covers what is *specific* to time series: horizon-wise evaluation, the tracking signal, correct backtesting, and the pitfalls.

---

## 10.1 THE TIME-SERIES RUNNING EXAMPLE

Reusing the example from Part 4.7, extended.

**Training series (in-sample), t = 1..6:** `100, 105, 102, 110, 108, 115`
**Test series (out-of-sample), t = 7..10:** actual `120, 125, 122, 130`
**Model forecast:** `118, 122, 126, 124`
**Naive (persistence) forecast:** `115, 120, 125, 122` — each is the previous *actual*, seeded from the last training value 115

```
Naive in-sample errors (first differences of the training series):
  |105−100|=5, |102−105|=3, |110−102|=8, |108−110|=2, |115−108|=7
  Σ = 25 over 5 differences  ->  in-sample naive MAE = 5.0

Model test errors:   e = y − ŷ
  t=7 : 120 − 118 = +2
  t=8 : 125 − 122 = +3
  t=9 : 122 − 126 = −4
  t=10: 130 − 124 = +6
  |e| = 2, 3, 4, 6   ->  Σ = 15,  MAE = 3.75
  e²  = 4, 9, 16, 36 ->  Σ = 65,  MSE = 16.25,  RMSE = 4.031
  Σe  = +7           ->  mean residual = +1.75  (model under-forecasts)

Naive test errors:
  t=7 : 120 − 115 = +5
  t=8 : 125 − 120 = +5
  t=9 : 122 − 125 = −3
  t=10: 130 − 122 = +8
  |e| = 5, 5, 3, 8   ->  MAE_naive = 21/4 = 5.25
  e²  = 25,25,9,64   ->  RMSE_naive = √(123/4) = 5.545
```

**All the key metrics on this series:**

| Metric | Value | Reading |
|---|---|---|
| MAE | 3.75 | Off by 3.75 units on average |
| RMSE | 4.031 | Tail-weighted; RMSE/MAE = 1.075 → very uniform errors |
| Mean residual | **+1.75** | **Systematically under-forecasting** |
| MPE | +1.35% | Under-forecasting by ~1.4% |
| Total bias | +1.41% | Total forecast is 1.4% below total actual |
| MAPE | 2.99% | |
| WAPE | 3.02% | Nearly equal to MAPE → errors evenly spread across levels |
| **MASE** (in-sample naive) | **0.75** | **25% better than naive** |
| MASE (test-period naive) | 0.714 | *Different number — this is why the convention matters* |
| **Theil's U2** | **0.727** | 27% lower RMSE than naive |
| **R²** | **−0.145** | ***NEGATIVE* — see below** |

**Note the last row.** The model beats the naive forecast by 25% (MASE 0.75) and yet its R² is **negative**. Compute it: `ȳ_test = 124.25`, `SS_tot = (120−124.25)² + (125−124.25)² + (122−124.25)² + (130−124.25)² = 18.06 + 0.56 + 5.06 + 33.06 = 56.75`; `SS_res = 65`; so `R² = 1 − 65/56.75 = −0.145`.

**R² is negative.** The model is "worse than predicting the test-set mean" — while simultaneously being 25% better than the naive forecast, which is the benchmark that matters. **This is the clearest possible demonstration that R² is the wrong metric for time series**, and it is worth remembering as a concrete example.

---

## 10.2 HORIZON-WISE EVALUATION

### The problem
A forecasting system usually predicts several steps ahead: 1 week, 2 weeks, ..., 13 weeks. Error grows with horizon — that is a law of nature, not a defect. **Reporting a single averaged metric across horizons is close to useless**, because it conflates an easy problem (h=1) with a hard one (h=13) and tells you nothing about where the system breaks down.

### The right report: a metric-by-horizon table

Illustrative example from a weekly demand forecast:

| Horizon h | MASE | WAPE | Bias % | Comment |
|---|---|---|---|---|
| 1 | 0.52 | 12% | +0.3% | Strong |
| 2 | 0.61 | 15% | +0.5% | |
| 4 | 0.74 | 19% | +1.2% | |
| 8 | 0.91 | 26% | +3.1% | Barely beating naive |
| 13 | **1.08** | 34% | **+6.8%** | **Worse than naive; bias compounding** |
| **Average** | **0.77** | **21%** | **+2.4%** | **Hides the h=13 failure completely** |

**The averaged row says the system is good (MASE 0.77). The h=13 row says the system should not be used at that horizon.** Both are true. Only the table reveals it.

**What to look for in a horizon table:**
1. **Where does MASE cross 1.0?** Beyond that horizon, ship the naive forecast instead. This is the single most actionable number in forecasting evaluation.
2. **Does bias grow with horizon?** Growing bias means a mis-specified trend — the model's drift term is wrong, and the error compounds. This is a different and more serious problem than growing variance, which is expected.
3. **Does the error grow faster than `√h`?** For a random walk, forecast error variance grows linearly in h so RMSE grows as `√h`. Growth much faster than that indicates the model is doing something actively harmful at long horizons.

```python
import numpy as np, pandas as pd

def horizon_report(y_true, y_pred, horizons, y_train, seasonality=1):
    """
    y_true, y_pred, horizons: aligned arrays; horizons gives h for each forecast.
    """
    naive = np.mean(np.abs(np.asarray(y_train, float)[seasonality:]
                          - np.asarray(y_train, float)[:-seasonality]))
    rows = []
    for h in sorted(set(horizons)):
        m = np.asarray(horizons) == h
        yt, yp = np.asarray(y_true, float)[m], np.asarray(y_pred, float)[m]
        e = yt - yp
        rows.append({
            'h': h, 'n': m.sum(),
            'MAE':  np.abs(e).mean(),
            'MASE': np.abs(e).mean() / naive,
            'WAPE_%': 100 * np.abs(e).sum() / np.abs(yt).sum(),
            'bias_%': 100 * e.sum() / yt.sum(),
        })
    return pd.DataFrame(rows)
```

---

## 10.3 TRACKING SIGNAL

### 1. Definition
The cumulative sum of forecast errors divided by the mean absolute deviation — a statistical process control chart for forecast bias.

### 2. Intuition
Bias is the most damaging and most correctable forecast defect (Part 4.5), but a *small* persistent bias is hard to see: a 2% under-forecast every week looks like noise week by week, and yet it compounds into a chronic stockout.

The tracking signal solves this by **accumulating** the signed errors. Random errors cancel and the cumulative sum stays near zero; a persistent bias accumulates linearly and the signal drifts out of control limits. It detects a small consistent bias far faster than watching the level of MPE.

It is a classic supply-chain tool, dating from the 1960s, and it is exactly the right instrument for automated forecast monitoring.

### 3. Formula
```
                 Σₜ ( yₜ − ŷₜ )            cumulative signed error
Tracking Signal = ───────────────────  =  ───────────────────────────
                        MAD                 mean absolute deviation
```
- **Numerator** = the running cumulative sum of signed errors (RSFE, Running Sum of Forecast Errors)
- **MAD** = the mean absolute error, usually computed as a **smoothed** (exponentially weighted) value so it adapts
- Range unbounded; **target 0**
- **Control limits: conventionally ±4 (tight) to ±6 (loose)**. A signal outside the limits means "investigate."

**Why the limits are around 4–6:** if errors were independent and symmetric, the expected absolute value of the cumulative sum after n periods grows as `√n × MAD × √(2/π)`, so a signal beyond ±4 is a low-probability event under the no-bias hypothesis. The conventional ±4 corresponds roughly to a 3-sigma control limit. Practitioners use ±4 for critical items and ±6 to reduce false alarms on noisy ones.

**Exponentially smoothed variant** (more responsive, standard in production):
```
Smoothed error   Eₜ = α·eₜ + (1−α)·Eₜ₋₁
Smoothed MAD     Mₜ = α·|eₜ| + (1−α)·Mₜ₋₁
Tracking signal      = Eₜ / Mₜ          -> bounded in [−1, +1]
```
This version is bounded, which makes threshold-setting easier: `|E/M| > 0.5` is a common alert level.

### 4. Manual example

Using our test period, plus two more periods to show accumulation:

| t | y | ŷ | e | Cumulative Σe | MAD (running) | Tracking Signal |
|---|---|---|---|---|---|---|
| 7 | 120 | 118 | +2 | +2 | 2.00 | **+1.00** |
| 8 | 125 | 122 | +3 | +5 | 2.50 | **+2.00** |
| 9 | 122 | 126 | −4 | +1 | 3.00 | **+0.33** |
| 10 | 130 | 124 | +6 | +7 | 3.75 | **+1.87** |
| 11 | 133 | 128 | +5 | +12 | 4.00 | **+3.00** |
| 12 | 136 | 130 | +6 | +18 | 4.33 | **+4.15** ← breach |

```
Working for t = 12:
  Cumulative Σe = 2 + 3 − 4 + 6 + 5 + 6 = 18
  MAD = (2 + 3 + 4 + 6 + 5 + 6) / 6 = 26/6 = 4.333
  Tracking Signal = 18 / 4.333 = 4.154
```
**The signal crosses +4 at t = 12 and fires an alert.**

**Read what happened.** At t = 10 the signal was +1.87 — unremarkable. Two more periods of modest under-forecasting (+5, +6) pushed the cumulative sum to +18 and the signal to +4.15. **No individual error looked alarming, but the persistence did.** The signal correctly identifies that the model is now systematically under-forecasting, most likely because the series has developed an upward trend the model is not capturing (look at the actuals: 120, 125, 122, 130, 133, 136 — clearly trending, while the forecasts lag).

**Compare what the level-based metrics said at t = 12:**
```
MAE  = 4.33      -> looks fine
MAPE = 3.36%     -> looks fine
Mean residual = +3.0   -> mildly positive
Tracking Signal = +4.15  -> ALERT
```
Only the tracking signal escalates. **This is why it belongs in every production forecast monitor.**

### 5. Python
```python
import numpy as np, pandas as pd

def tracking_signal(y_true, y_pred, limit=4.0):
    """Classic cumulative tracking signal with a running MAD."""
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    cum   = np.cumsum(e)
    mad   = np.cumsum(np.abs(e)) / np.arange(1, len(e) + 1)
    ts    = np.divide(cum, mad, out=np.zeros_like(cum), where=mad != 0)
    return pd.DataFrame({'e': e, 'cum_e': cum, 'MAD': mad,
                         'TS': ts, 'breach': np.abs(ts) > limit})

def smoothed_tracking_signal(y_true, y_pred, alpha=0.1):
    """Exponentially smoothed version. Bounded in [-1, 1]."""
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    E = M = 0.0
    out = []
    for ei in e:
        E = alpha * ei + (1 - alpha) * E
        M = alpha * abs(ei) + (1 - alpha) * M
        out.append(E / M if M else 0.0)
    return np.array(out)

yt = np.array([120,125,122,130,133,136.])
yp = np.array([118,122,126,124,128,130.])
print(tracking_signal(yt, yp))
```
- **Use the smoothed version in production** — it is bounded, responsive, and does not require storing the full history.
- **Set the limit per item class:** tight (±4 or `|E/M| > 0.4`) for high-value/critical SKUs, loose (±6 or 0.6) for noisy low-value ones, to control the false-alarm rate.
- Pair the alert with an automatic diagnosis: is it a **step change** (usually a data-pipeline or definition break) or a **gradual drift** (usually genuine distribution shift)?

### 6. Interpretation

| Tracking Signal | Diagnosis | Action |
|---|---|---|
| Within ±4 | In control | None |
| Persistently +2 to +4 | Mild under-forecasting building | Watch; check for an emerging trend |
| **> +4** | **Systematic under-forecasting** | Investigate: emerging trend, promotion not in the model, upward level shift, data break |
| **< −4** | **Systematic over-forecasting** | Investigate: declining demand, discontinued item, double-counting, naive log back-transform |
| Oscillating across zero | Seasonality not captured | Add or fix seasonal terms |
| Sudden jump | Step change | Almost always a data/definition break, not a model problem |

### 7–8. Use cases and value
- **Production forecast monitoring at scale** — the standard mechanism for flagging which of 50,000 SKU forecasts need human attention. It converts an unmanageable monitoring problem into a small exception list.
- **Automated forecast maintenance:** a breach triggers a retrain, a model re-selection, or routing to a planner.
- **Demand planning exception management** — the "exception report" in every APS/ERP system is essentially this.
- **Distinguishing model decay from data breaks** by the shape of the signal.
- **Any setting where a small persistent bias is expensive**: inventory, reserving, capacity, staffing.

### 9. Advantages
- **Detects small persistent bias far faster than level metrics** — its whole reason for existing.
- Cheap, streaming, and requires almost no state in the smoothed form.
- Has a natural alert threshold with a statistical justification.
- Interpretable — the sign tells you the direction of the problem immediately.
- Scale-free (normalised by MAD), so one threshold works across items of different volume.
- Long-established, so it needs no explanation to supply-chain professionals.

### 10. Limitations
- **Detects only bias, not accuracy.** A model with enormous but symmetric errors has a tracking signal of 0. Must be paired with MASE/WAPE.
- **The cumulative version has memory** — a bias from a year ago still influences today's signal unless it is reset or windowed. Use the smoothed version, or reset after a corrective action.
- **Sensitive to the MAD estimate**, which is itself noisy on short or intermittent series.
- **Threshold choice trades false alarms against detection delay**, and on 50,000 series a ±4 limit will generate many alerts by chance alone. Apply a multiple-testing mindset, or tier the thresholds by item importance.
- Not meaningful for very short histories.
- Not a standard ML library function; must be implemented.

### 11. Common mistakes
1. **Not resetting after a corrective action.** If you fix the model, reset the cumulative sum, or the historical bias will keep the signal out of control and mask the fix.
2. **Using one threshold across a heterogeneous portfolio**, producing an unmanageable alert volume.
3. **Treating a breach as a model failure** without first checking for a data break — the majority of sudden breaches are upstream data problems.
4. **Monitoring only bias** and not accuracy.
5. Using the unbounded cumulative form in production where the smoothed bounded form is easier to threshold.

### 12. Interview questions
**Easy — What does the tracking signal measure?** Cumulative forecast bias, normalised by MAD, with conventional control limits at ±4 to ±6.
**Medium — ★ Why use a tracking signal rather than just monitoring MPE?** Because a small persistent bias is invisible in a period-by-period level metric — a 2% under-forecast every week looks like noise — but it *accumulates*, so the cumulative sum drifts steadily while random errors cancel. The tracking signal therefore detects a small consistent bias much faster and with a principled alert threshold. It is statistical process control applied to forecasting.
**Hard — You monitor 50,000 SKU forecasts with a ±4 tracking-signal limit and get 3,000 alerts a week. What do you do?**
Three things. (1) **Recognise the multiple-comparisons problem:** with 50,000 series, even a perfectly unbiased process will breach ±4 by chance in a meaningful number of cases, so a fixed limit is not a per-series decision rule — it is a screening filter that needs calibrating. Set the threshold from the *observed* false-alarm rate on a known-good period, or use an FDR-style adjustment. (2) **Tier by business impact:** apply tight limits to the top items by revenue or criticality (where a planner's time is well spent) and loose limits, or automated correction only, to the long tail. Rank the alert list by `|bias| × value` so the exception report is ordered by money rather than by statistical significance. (3) **Automate the common causes:** classify each breach as step change (data break — route to data engineering), sustained drift (route to retraining), or seasonal oscillation (route to model re-specification), and auto-apply a bounded multiplicative correction for the drift class while a retrain is queued. The goal is to convert 3,000 statistical alerts into perhaps 50 items that genuinely need human judgement.

---

## 10.4 CORRECT BACKTESTING

### The single most damaging mistake in time-series ML

```python
# WRONG -- this leaks the future into the past
from sklearn.model_selection import KFold, cross_val_score
cross_val_score(model, X, y, cv=KFold(5, shuffle=True))   # <-- INVALID for time series
```
Shuffled K-fold trains on observations from **after** the test period. On a trending or autocorrelated series this produces scores that can be several times better than reality, and the failure only surfaces in production.

### The correct schemes

**(a) Expanding window (walk-forward, anchored)** — the default:
```
Fold 1:  train [1..50]           test [51..60]
Fold 2:  train [1..60]           test [61..70]
Fold 3:  train [1..70]           test [71..80]
Fold 4:  train [1..80]           test [81..90]
```
Each fold uses all history up to the cut, mimicking how you would actually refit in production.

**(b) Rolling window (sliding, unanchored)** — when older data is stale:
```
Fold 1:  train [1..50]           test [51..60]
Fold 2:  train [11..60]          test [61..70]
Fold 3:  train [21..70]          test [71..80]
```
Fixed training length, so it discards distant history. Preferable when the process changes regime.

**(c) With a gap (purged/embargoed)** — essential when features have look-back windows or targets have look-forward windows:
```
Fold 1:  train [1..50]   GAP [51..53]   test [54..63]
```
The gap prevents leakage through overlapping windows — for example, a 3-day rolling-mean feature computed at t=51 uses data from t=49–51, which is in the training set. In finance this is called **purging and embargoing**, and omitting it is a well-documented source of spurious backtest performance.

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

# Expanding window
tscv = TimeSeriesSplit(n_splits=5)
for tr, te in tscv.split(X):
    print(f"train {tr.min()}..{tr.max()}   test {te.min()}..{te.max()}")

# Rolling window with a gap
tscv = TimeSeriesSplit(n_splits=5, max_train_size=50, gap=3)

# Multi-horizon backtest: evaluate each horizon separately
def backtest(series, model_fn, n_train, horizon, step=1):
    """Expanding-window backtest returning per-horizon errors."""
    rows = []
    t = n_train
    while t + horizon <= len(series):
        train = series[:t]
        fc    = model_fn(train, horizon)           # returns h forecasts
        for h in range(1, horizon + 1):
            rows.append({'origin': t, 'h': h,
                         'actual': series[t + h - 1], 'forecast': fc[h - 1]})
        t += step
    import pandas as pd
    return pd.DataFrame(rows)
```

### The backtesting checklist

```
[ ] Split respects time order (TimeSeriesSplit, never shuffled KFold)
[ ] A GAP is inserted if features look back or targets look forward
[ ] Every feature is computable at forecast time (no future information)
[ ] Lag features use only data available at the forecast origin
[ ] Preprocessing (scaling, encoding, imputation) is fitted INSIDE each fold
[ ] Target encodings / aggregates use only training-fold data
[ ] Errors are reported BY HORIZON, not averaged across horizons
[ ] Multiple forecast origins are used, not a single train/test cut
[ ] The naive and seasonal-naive baselines are computed on the same folds
[ ] Metrics are scaled (MASE / WAPE), not raw MAE, if aggregating across series
[ ] Bias is reported alongside accuracy
[ ] The final reported number comes from data used exactly once
```

**The most insidious leaks in time-series feature engineering:**

| Feature | Leak | Fix |
|---|---|---|
| Rolling mean of the target | Includes the current value | Shift by 1 before rolling |
| "Total sales this month" | Not known until the month ends | Use last month's total |
| Target-encoded category mean | Computed on all data | Compute within the training fold only, with a time cut |
| Scaling by the global mean/σ | Uses future data | Fit the scaler on the training fold |
| Holiday/promotion flags | Usually fine (known in advance) | Verify they are genuinely known ex ante |
| Weather | Actuals are not known in advance | Use *forecast* weather, as production would |

**Interview (Hard) — ★ Why is shuffled K-fold invalid for time series, and how bad is it in practice?**
Two reasons. First, **temporal leakage**: the model trains on observations from after the test period, so it can exploit information genuinely unavailable at forecast time — on a trending series it effectively learns the level of the test period. Second, **autocorrelation**: adjacent observations are highly correlated, so a randomly-chosen test point almost always has near-neighbours in the training set, making the task far easier than forecasting a genuinely future point. In practice the inflation can be large — it is common to see a shuffled-CV RMSE two to four times better than a proper walk-forward RMSE on a trending, autocorrelated series, and I have seen models with excellent shuffled-CV scores that were worse than the naive forecast when properly backtested. The correct approach is `TimeSeriesSplit` with an appropriate gap, evaluated per horizon, against a naive baseline.

---

## 10.5 TIME-SERIES METRIC PITFALLS

**1. Using R² on a time series.**
Demonstrated in 10.1: our model beat the naive forecast by 25% (MASE 0.75) while having a **negative R²**. R² benchmarks against the *mean*, which is a hopeless baseline for a trending series, and conversely on a strongly trending series R² can be 0.99 for a model that is *worse* than "tomorrow = today." **Use MASE or Theil's U, which benchmark against the naive forecast.**

**2. Averaging MAE or RMSE across series of different scale.**
A portfolio of 10,000 SKUs where one sells 50,000 units/week and most sell 5. The average MAE is essentially the big SKU's MAE. **Use MASE (average the per-series values) or WAPE (volume-weighted, if that is what you want).**

**3. Reporting a single metric averaged over horizons.**
Hides the horizon at which the model stops beating naive. **Report a horizon table.**

**4. Comparing MASE values computed with different denominators.**
Training-period naive vs test-period naive gave 0.75 vs 0.714 on our data. Both are "MASE." **State the convention; use the training-period version.**

**5. Non-seasonal MASE on seasonal data.**
Beating "tomorrow = today" on December retail sales is trivial. **Use seasonal MASE with the right period (7, 12, 24, 52).**

**6. Reporting accuracy without bias.**
Bias compounds into inventory positions in a way that symmetric error does not. **Always report total bias and a tracking signal.**

**7. Evaluating on a single train/test cut.**
One cut gives one number with no uncertainty and may land on an unrepresentative period. **Use multiple forecast origins.**

**8. Ignoring intermittency.**
For a series that is mostly zeros, MAPE is undefined, RMSE is dominated by the non-zero weeks, and MASE's denominator may be tiny. Intermittent demand needs its own treatment: Croston-type methods, and metrics like MASE plus **the number-of-periods-until-stockout** or a **cumulative-error-over-lead-time** measure that reflects the actual inventory decision.

**9. Forecasting a transformed target and evaluating on the transformed scale.**
An RMSE of 0.09 on `log(sales)` is not interpretable to the business and does not correspond to the cost function. **Back-transform (with a bias correction) and evaluate on the original scale.**

**10. Aggregating high quantiles up a hierarchy.**
Covered in Part 7.3: `Σ Q_0.9 ≠ Q_0.9(Σ)`. Systematically over-provisions.

**11. Ignoring forecast reconciliation.**
If you forecast at SKU, category, and total level independently, the numbers will not add up. Metrics computed at each level independently can all look fine while the hierarchy is incoherent. Use a reconciliation method (bottom-up, top-down, or optimal/MinT) and evaluate coherently.

**12. Comparing to a weak baseline.**
"Our model beats the mean" is not a claim. **Always report naive, seasonal naive, and — if applicable — the current production forecast** as baselines.

## 10.6 The recommended time-series metric set

```
ACCURACY (scaled, so it aggregates)
  [ ] MASE per series, with the correct seasonality, denominator on TRAINING data
  [ ] WAPE at the level the decision is taken (volume-weighted)
  [ ] Fraction of series with MASE >= 1  (these should use the naive forecast)

BIAS (never omit)
  [ ] Total bias %  (sum of forecast / sum of actual)
  [ ] Tracking signal, with control limits, per series
  [ ] Bias BY HORIZON (growing bias => mis-specified trend)

STRUCTURE
  [ ] Metric-by-horizon table (find where MASE crosses 1.0)
  [ ] Metrics by segment (volume band, intermittency class, category, region)
  [ ] Residual ACF / Ljung-Box test (see Part 11) -- leftover autocorrelation
      means exploitable signal remains

UNCERTAINTY (if the forecast drives a service level)
  [ ] Pinball loss at the service-level quantile
  [ ] PICP / MPIW, or the Interval Score
  [ ] CRPS if a full predictive distribution is produced

BASELINES (always)
  [ ] Naive, seasonal naive, and the incumbent production forecast
  [ ] Evaluated on identical folds and horizons
```

---

# PART 11 — Residual Diagnostics

## 11.0 Why this Part matters more than any metric

Every metric in this document compresses the residual set into one number. **Diagnostics look at the residuals themselves**, and they answer the question no metric can: **why is the model wrong, and what should I do about it?**

This is the regression analogue of "always look at the confusion matrix." A metric tells you *how much*; the residuals tell you *what kind*.

**The four assumptions of a well-specified regression model, and what breaks if each fails:**

| Assumption | Diagnostic | If violated |
|---|---|---|
| **Linearity / correct form** | Residuals vs fitted; residuals vs each feature | Biased predictions in specific regions; no metric will fix it |
| **Homoscedasticity** (constant variance) | Residuals vs fitted (funnel shape); Breusch-Pagan | Standard errors and intervals are wrong; RMSE dominated by the high end |
| **Independence** | Residuals vs time; ACF; Durbin-Watson; Ljung-Box | Standard errors badly understated; exploitable signal remains |
| **Normality of errors** | Q-Q plot; Shapiro-Wilk; histogram | Intervals and p-values are wrong (least critical of the four for prediction) |

**A crucial framing point for interviews:** these assumptions matter for **inference** (p-values, confidence intervals, standard errors) far more than for **prediction**. A tree ensemble making point predictions does not need normal, homoscedastic errors. But **every one of the four still matters for prediction in a specific way**: non-linearity means biased predictions, heteroscedasticity means your prediction intervals are wrong, autocorrelation means you left signal on the table, and non-normality means your Gaussian intervals under-cover. So do not dismiss diagnostics as "only for classical statistics."

---

## 11.1 THE SIX ESSENTIAL PLOTS

Produce all six. Together they take ten lines of code and reveal more than any metric table.

```python
import numpy as np, matplotlib.pyplot as plt
from scipy import stats

def diagnostic_panel(y_true, y_pred, X=None, feature_names=None, times=None):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    fig, ax = plt.subplots(2, 3, figsize=(16, 9))

    # 1. Predicted vs Actual (the stakeholder plot)
    ax[0,0].scatter(y_true, y_pred, alpha=.6)
    lims = [min(np.min(y_true), np.min(y_pred)), max(np.max(y_true), np.max(y_pred))]
    ax[0,0].plot(lims, lims, 'k--'); ax[0,0].set_title('Predicted vs Actual')
    ax[0,0].set_xlabel('Actual'); ax[0,0].set_ylabel('Predicted')

    # 2. Residuals vs Fitted (the single most important plot)
    ax[0,1].scatter(y_pred, e, alpha=.6); ax[0,1].axhline(0, ls='--', c='k')
    ax[0,1].set_title('Residuals vs Fitted'); ax[0,1].set_xlabel('Fitted')

    # 3. Scale-Location: sqrt|standardised residual| vs fitted (heteroscedasticity)
    s = e / (e.std() or 1)
    ax[0,2].scatter(y_pred, np.sqrt(np.abs(s)), alpha=.6)
    ax[0,2].set_title('Scale-Location'); ax[0,2].set_xlabel('Fitted')

    # 4. Q-Q plot (normality)
    stats.probplot(e, dist='norm', plot=ax[1,0]); ax[1,0].set_title('Normal Q-Q')

    # 5. Histogram of residuals (skew, multimodality, bias)
    ax[1,1].hist(e, bins=30, edgecolor='k'); ax[1,1].axvline(0, ls='--', c='r')
    ax[1,1].axvline(e.mean(), c='b', label=f'mean={e.mean():.2f}')
    ax[1,1].legend(); ax[1,1].set_title('Residual distribution')

    # 6. Residuals vs order/time (autocorrelation, drift)
    t = np.arange(len(e)) if times is None else times
    ax[1,2].plot(t, e, marker='.'); ax[1,2].axhline(0, ls='--', c='k')
    ax[1,2].set_title('Residuals vs time/order')

    plt.tight_layout(); return fig
```

**Applied to our running example** (10 houses), the panel shows:
1. **Predicted vs Actual** — nine points hug the 45° line; house 10 sits far below it (predicted 700, actual 900). The visual signature of range compression.
2. **Residuals vs Fitted** — nine residuals in a tight ±20 band with no trend; one at +200.
3. **Scale-Location** — flat for nine points, one spike. Insufficient data to judge heteroscedasticity, but the design (a target spanning 200 to 900) makes it likely.
4. **Q-Q plot** — nine points roughly on the line, one far off in the upper tail. Classic heavy-right-tail signature.
5. **Histogram** — mean at +18, median at 0, one point at +200. Right-skewed.
6. **Residuals vs order** — the regular alternating ±20 pattern (an artefact of this toy example, but in real data it would be a red flag for a missing periodic feature).

---

## 11.2 HETEROSCEDASTICITY

### What it is
The variance of the residuals changes across the range of fitted values or of a feature. The classic signature is a **funnel** or **cone** in the residuals-vs-fitted plot.

```
    HOMOSCEDASTIC (good)             HETEROSCEDASTIC (funnel)
    |  . . .. . . .. . .             |          .    .     .
   0|--.-.-.--.-.--.-.--.--         0|--.-.-.-.--.---.---.----.--
    | . .. . . .. . . .              |   .      .     .     .
    +---------------------           +---------------------------
       fitted values                     fitted values
```

### Why it matters — three distinct consequences

1. **Prediction intervals are wrong.** `ŷ ± 1.96σ̂` with a single global σ̂ will be too narrow at the high end and too wide at the low end. Our PICP example in Part 8.3 is exactly this failure: nominal coverage overall, complete failure on the expensive house.
2. **RMSE is dominated by the high-variance region.** If variance grows with the level, MSE effectively optimises for the largest values and ignores the smallest — the same problem RMSLE solves.
3. **Standard errors and p-values are wrong** (for inference). OLS coefficients remain unbiased but their standard errors are inconsistent, so t-tests and confidence intervals are invalid.

### Formal tests

**Breusch-Pagan test.** Regress the squared residuals on the predictors; if they have explanatory power, variance depends on X.
```
H₀: homoscedastic     Test statistic ~ chi-squared(p)
```

**White test.** Like Breusch-Pagan but includes squares and cross-products, so it detects a wider range of forms. More general, less powerful for any specific one.

**Goldfeld-Quandt test.** Split the data by a suspected ordering variable and compare residual variances with an F-test.

```python
import numpy as np, statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

# X1 must include a constant column
# resid = y - y_pred
# bp_stat, bp_p, f_stat, f_p = het_breuschpagan(resid, X1)
# print(f"Breusch-Pagan p = {bp_p:.4f}   (p < 0.05 => heteroscedastic)")

# A quick non-parametric check with no statsmodels dependency:
def variance_by_bin(y_true, y_pred, n_bins=5):
    e = np.asarray(y_true, float) - np.asarray(y_pred, float)
    order = np.argsort(y_pred)
    for chunk in np.array_split(order, n_bins):
        print(f"fitted {y_pred[chunk].mean():9.1f}   "
              f"resid sd {e[chunk].std():8.2f}   n={len(chunk)}")
```
**The `variance_by_bin` check is the one to reach for first** — if the residual standard deviation roughly doubles from the lowest to the highest bin, you have heteroscedasticity and you do not need a p-value to act on it.

### The fixes, in order of preference

| Fix | When | Note |
|---|---|---|
| **Log-transform the target** | Variance ∝ level² (constant coefficient of variation) | Simplest and most common. Beware the back-transform bias (Part 4.5). |
| **Square-root transform** | Variance ∝ level (Poisson-like) | Natural for counts |
| **Gamma / Tweedie GLM with a log link** | Positive right-skewed target | **Usually the best choice** — models the mean directly, no back-transform bias, correct variance function |
| **Poisson / negative binomial** | Count targets | Correct likelihood; handles zeros |
| **Weighted least squares** | You know the variance function | `sample_weight = 1/σᵢ²` |
| **Quantile regression** | You need intervals | Learns the spread per region automatically; no assumption needed |
| **Heteroscedastic NLL** (predict μ and σ) | Deep models | Part 8.1 |
| **Robust (HC) standard errors** | Inference only, prediction unaffected | `cov_type='HC3'` in statsmodels — fixes the p-values, not the model |

**Interview (Medium) — ★ Your residuals fan out with the fitted value. What does that mean and what do you do?**
It means heteroscedasticity: the error variance grows with the level of the target. Three consequences: prediction intervals built with a single global σ will be too narrow at the top and too wide at the bottom; RMSE will be dominated by the high-value observations, so the model effectively ignores the low end; and if I am doing inference, my standard errors are invalid. The fix depends on the target: if it is positive and right-skewed, I would model it with a **Gamma or Tweedie objective and a log link**, which handles the variance structure correctly and — unlike log-transforming the target — models the mean directly so there is no back-transformation bias. If I need intervals, **quantile regression** learns the region-specific spread automatically. If I only need valid p-values, robust HC3 standard errors fix the inference without changing the model.

---

## 11.3 AUTOCORRELATION

### What it is
Residuals are correlated with their own past values. Almost universal in time-series and spatial data, and it means **the model has left exploitable structure on the table.**

### Why it matters
1. **Signal remains.** If today's residual predicts tomorrow's, you can improve the forecast. Autocorrelated residuals are a direct statement that the model is incomplete.
2. **Standard errors are badly understated.** Positive autocorrelation means your effective sample size is much smaller than n, so t-statistics are inflated and you will find spurious "significant" effects. This is the classic source of over-confident time-series regressions.
3. **Prediction intervals are too narrow.**

### Durbin-Watson statistic

```
              Σₜ₌₂ⁿ ( eₜ − eₜ₋₁ )²
DW  =  ─────────────────────────────
                  Σₜ₌₁ⁿ  eₜ²
```
- Range **[0, 4]**; **DW ≈ 2 means no first-order autocorrelation**
- `DW < 2` → **positive** autocorrelation (consecutive residuals similar)
- `DW > 2` → **negative** autocorrelation (residuals alternate)
- Approximate relation: `DW ≈ 2(1 − ρ̂₁)`, where ρ̂₁ is the first-order residual autocorrelation
- Rule of thumb: **DW below 1.5 or above 2.5 warrants investigation**

**Manual example on our house residuals** (treating the index as an order, purely illustratively):
```
e = [−20, +10, −10, +20, −20, +20, −20, +20, −20, +200]

Numerator   Σ(eₜ − eₜ₋₁)²:
  (10−(−20))² = 900      (−10−10)²  = 400     (20−(−10))² = 900
  (−20−20)²   = 1600     (20−(−20))²= 1600    (−20−20)²   = 1600
  (20−(−20))² = 1600     (−20−20)²  = 1600    (200−(−20))²= 48,400
  Σ = 900+400+900+1600+1600+1600+1600+1600+48400 = 58,600

Denominator Σeₜ² = 43,000

DW = 58,600 / 43,000 = 1.363
```
**DW = 1.363**, below 1.5, suggesting positive autocorrelation. (In this toy example the "autocorrelation" is really the alternating pattern plus the outlier, so the statistic should not be over-interpreted — but the arithmetic is exactly as shown.)

**A contrast to build intuition.** For a strongly positively autocorrelated series like `e = [1,2,3,4,5,−1,−2,−3,−4,−5]`:
```
DW = 0.40   ->  strong positive autocorrelation
```

### The better tests

**Durbin-Watson only detects lag-1 autocorrelation.** For a complete picture use:

**Ljung-Box test** — tests whether autocorrelations up to lag h are jointly zero:
```
                     h    ρ̂ₖ²
Q  =  n(n+2)  ×      Σ   ─────        ~  chi-squared(h − p)
                    k=1   n − k
```
`H₀: no autocorrelation up to lag h`. **This is the standard residual test for any fitted time-series model** and is reported automatically by ARIMA implementations.

**The residual ACF plot** — the most informative of all. Plot the autocorrelation of the residuals at lags 1..40 with confidence bands. Any spike outside the bands is structure the model missed, and the *lag* tells you what kind (lag 7 → weekly, lag 12 → monthly seasonality, lag 1 → simple persistence).

```python
import numpy as np
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf

e = y - y_pred
print(f"Durbin-Watson = {durbin_watson(e):.3f}")          # ~2 is good

# Ljung-Box up to lag 10 (use lags ~ min(10, n/5) for short series)
# lb = acorr_ljungbox(e, lags=[5, 10, 20], return_df=True)
# print(lb)   # p < 0.05 at any lag => autocorrelation remains

# The ACF plot -- the most informative diagnostic
# plot_acf(e, lags=40)

# Pure-numpy DW if you want no dependency
def dw(e):
    e = np.asarray(e, float)
    return np.sum(np.diff(e)**2) / np.sum(e**2)
```

### The fixes

| Cause | Fix |
|---|---|
| Missing lag features | Add lagged target and lagged exogenous variables |
| Missing seasonality | Add seasonal dummies, Fourier terms, or a seasonal difference |
| Missing trend | Add a trend term, or difference the series |
| Wrong model class | Use ARIMA/SARIMAX/state-space, which model the error process explicitly |
| Genuine serial correlation in the noise | Model it: ARMA errors, GLS, or Newey-West/HAC standard errors for inference |
| Spatial correlation | Spatial lag/error models, or spatially blocked CV |

**Interview (Medium) — ★ Your residual ACF shows a significant spike at lag 12 on monthly data. What is happening?**
The model has not captured annual seasonality — the residual in a given month is correlated with the residual twelve months earlier, meaning there is a repeating yearly pattern the model is systematically missing. Concretely, it is probably under-predicting every December and over-predicting every February (or similar). Fixes: add monthly dummies or Fourier seasonal terms, apply a seasonal difference (`y_t − y_{t−12}`), or switch to a SARIMA/seasonal-ETS specification. I would also switch my headline metric to **seasonal MASE** (denominator = seasonal naive), because non-seasonal MASE would flatter any model on a seasonal series, and re-check the residual ACF after the fix to confirm the spike is gone.

---

## 11.4 NORMALITY

### What it is and why it matters (less than people think)

**Normality of the residuals is the least important of the four assumptions for prediction**, and it is the one people over-test. The Gauss-Markov theorem gives OLS its optimality properties (unbiased, minimum variance among linear estimators) **without** requiring normality. What normality buys you is:
- Exact small-sample t-tests and F-tests
- Correct Gaussian prediction intervals (`ŷ ± 1.96σ̂`)
- Maximum-likelihood efficiency

For **large samples**, the central limit theorem makes coefficient inference approximately valid regardless. For **prediction intervals**, non-normality matters directly — heavy tails mean your 95% interval under-covers.

### The Q-Q plot — and how to read it

```
   NORMAL (good)        HEAVY TAILS         RIGHT-SKEWED
   |        .           |          .        |         .
   |      .             |        .          |       .
   |    .               |     .             |    .
   |  .                 |  .                | .
   |.                   |.                  |.
   +---------           +----------         +----------
   Points on the line   S-shape / points    Curve bending up:
                        curving away at     residuals more
                        BOTH ends           positive than normal
```
| Pattern | Meaning | Consequence |
|---|---|---|
| On the line | Normal | Gaussian intervals valid |
| **Both tails above/below the line (S or inverted-S)** | **Heavy tails** | **Gaussian intervals under-cover.** Use Student-t, or quantile/conformal intervals |
| Curved (one side only) | Skew | Consider a transform or a skewed likelihood (Gamma, lognormal) |
| Discrete steps | Rounded/integer target | Consider a count or ordinal model |
| A few extreme points off the end | Outliers | Investigate individually (Part 2.3) |

### Formal tests, with a warning

```python
from scipy import stats
e = y - y_pred
print(stats.shapiro(e))          # Shapiro-Wilk: best power for small n
print(stats.jarque_bera(e))      # Jarque-Bera: based on skewness and kurtosis
print(stats.anderson(e, 'norm')) # Anderson-Darling: sensitive in the tails
print(f"skew={stats.skew(e):.3f}  kurtosis(excess)={stats.kurtosis(e):.3f}")
```
**The warning, and it is important:** with large n these tests reject normality for trivially small, practically irrelevant deviations. With n = 100,000, essentially any real dataset fails Shapiro-Wilk. **Use the Q-Q plot and the skew/kurtosis values to judge whether the deviation matters, not the p-value.** A useful rule: `|skew| < 0.5` and `|excess kurtosis| < 1` is practically normal for most purposes.

**On our data:** `skew = 2.31`, `excess kurtosis = 4.00` — strongly right-skewed and heavy-tailed, driven entirely by house 10. Gaussian prediction intervals would under-cover, exactly as we saw in Part 8.3.

---

## 11.5 INFLUENCE AND LEVERAGE

### The three distinct concepts

| Concept | Question | Measure |
|---|---|---|
| **Outlier** | Is the *residual* unusually large? | Standardised / studentised residual |
| **Leverage** | Is the *feature vector* unusual? | Hat value `hᵢᵢ` |
| **Influence** | Would removing it *change the model*? | Cook's distance, DFFITS, DFBETAS |

**These are independent, and confusing them is a common error.** A point can be:
- **High residual, low leverage** — an outlier in y that the model ignores. Bad for the metric, harmless to the fit.
- **Low residual, high leverage** — an unusual x that the model fits well. Dangerous: it is *dictating* the fit, and you cannot tell because its residual looks fine.
- **High residual AND high leverage** — the genuinely dangerous case: it is both badly fitted and controlling the model. **This is house 10 in our example.**

### Leverage

```
hᵢᵢ = the i-th diagonal element of  H = X(XᵀX)⁻¹Xᵀ
Σ hᵢᵢ = p + 1        0 ≤ hᵢᵢ ≤ 1        average hᵢᵢ = (p+1)/n
```
**Rule of thumb: investigate any point with `hᵢᵢ > 2(p+1)/n`** (twice the average) or `> 3(p+1)/n` for a stricter screen.

### Cook's distance — the standard influence measure

```
                Σⱼ ( ŷⱼ − ŷⱼ₍₋ᵢ₎ )²                eᵢ²            hᵢᵢ
Dᵢ  =  ─────────────────────────────  =  ──────────── × ──────────────
                 (p + 1) · σ̂²              (p+1)σ̂²      ( 1 − hᵢᵢ )²
```
- Measures **how much all the fitted values change** when observation i is removed. It combines residual size and leverage multiplicatively — which is exactly right, since influence requires both.
- **Rules of thumb: `Dᵢ > 1` is clearly influential; `Dᵢ > 4/n` is a screening threshold.**

**DFFITS** measures the change in the fitted value for observation i itself (threshold `2√((p+1)/n)`); **DFBETAS** measures the change in each individual coefficient (threshold `2/√n`). Use DFBETAS when you need to know *which coefficient* an observation is driving — valuable in regulated modelling where a single record moving a key coefficient is a finding.

```python
import numpy as np
import statsmodels.api as sm

# X1 = sm.add_constant(X)
# res = sm.OLS(y, X1).fit()
# infl = res.get_influence()
# summary = infl.summary_frame()      # cooks_d, hat_diag, dffits, standard_resid, ...

# Pure-numpy version
def influence_measures(X, y):
    X1 = np.column_stack([np.ones(len(X)), np.asarray(X, float)])
    n, k = X1.shape
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    e = y - X1 @ beta
    H = X1 @ np.linalg.pinv(X1.T @ X1) @ X1.T
    h = np.diag(H)
    sigma2 = (e**2).sum() / (n - k)
    cooks = (e**2 / (k * sigma2)) * (h / (1 - h)**2)
    stud  = e / np.sqrt(sigma2 * (1 - h))
    return {'leverage': h, 'cooks_d': cooks, 'studentised': stud,
            'lev_thresh': 2*k/n, 'cooks_thresh': 4/n}

# The workflow that matters: always print the top influential points and LOOK at them
# m = influence_measures(X, y)
# top = np.argsort(-m['cooks_d'])[:10]
# print(pd.DataFrame({'cooks_d': m['cooks_d'][top], 'leverage': m['leverage'][top]},
#                    index=top))
```

**Connecting to Part 9.5:** recall the PRESS identity `y_i − ŷ₍₋ᵢ₎ = eᵢ/(1 − hᵢᵢ)`. With `hᵢᵢ = 0.75` for house 10, its leave-one-out residual is `200/0.25 = 800` — four times its in-sample residual. That is what "high influence" means concretely, and it is why our `R²_pred` was negative while in-sample R² was 0.885.

### What to do with an influential point

**Do not delete it to make the metric look better.** The decision tree:

```
Is it a DATA ERROR? (unit mix-up, decimal slip, duplicate, mis-keyed value)
  YES -> Fix it, or remove it and DOCUMENT why
  NO  -> continue

Is it OUT OF SCOPE for the model's intended use?
  (a $8M mansion in a model built to value suburban homes)
  YES -> Define the operating envelope explicitly, exclude it, and add an
         out-of-distribution check in production so such inputs are flagged
         rather than silently scored
  NO  -> continue

Is it GENUINE and IN SCOPE?
  YES -> The model must handle it. Options, in order:
         1. Add features that explain it (usually the real answer)
         2. Model on a log scale / use a Gamma-Tweedie objective, so relative
            rather than absolute error is optimised
         3. Use a robust loss (Huber) so it stops dictating the fit,
            and report MedAE alongside RMSE
         4. Fit a separate model for that segment
         5. Report the limitation honestly and quote an interval, not a point
```

**Interview (Hard) — ★ A single observation has Cook's distance of 3.5. Walk me through what you do.**
`D = 3.5` is far above the `D > 1` threshold, so this one observation is materially controlling the fitted model. First I would **look at the raw record** — in my experience the majority of extreme influence points turn out to be data problems: a unit mix-up, a decimal error, a duplicated or mis-joined row. Second, I would decompose the influence: Cook's distance combines residual size and leverage, so I would check `hᵢᵢ` and the studentised residual separately, because "unusual x" and "unusual y" imply different fixes. Third, I would run **DFBETAS** to see *which coefficients* it is driving — if it is single-handedly determining the sign of a key coefficient, that is a serious finding for any model that will be interpreted or regulated. Fourth, I would refit **without** it and compare the coefficients and the cross-validated error; if the model changes materially, I cannot ship a model whose conclusions rest on one row. Finally I would decide deliberately: fix it if it is an error; exclude it and define the operating envelope if it is genuinely out of scope, adding an out-of-distribution guard in production; or — if it is genuine and in scope — add features that explain it, switch to a log/Gamma objective so relative error is optimised, or use a robust loss so it informs the fit without dictating it. What I would not do is delete it silently, and I would report `R²_pred` or a cross-validated score alongside in-sample R², because a high-leverage point makes in-sample fit meaningless.

---

## 11.6 THE RESIDUAL DIAGNOSTIC CHECKLIST

```
STRUCTURE  (is the functional form right?)
[ ] Residuals vs fitted: any curve, trend, or pattern?
[ ] Residuals vs EACH feature: which variable carries the missed nonlinearity?
[ ] Residuals vs interactions / by segment: is there a subgroup the model fails on?
[ ] Predicted vs actual with a 45-degree line: is the range compressed?
    -> Var(pred)/Var(actual) << 1 means regression to the mean

BIAS  (never omit)
[ ] Mean residual, median residual, total bias %
[ ] Bias by segment, by predicted decile, and over time
[ ] Explained-variance minus R²  = Bias^2/Var(y)  -- a free bias check

VARIANCE
[ ] Residual sd by bin of the fitted value (does it double across the range?)
[ ] Breusch-Pagan / White test
[ ] If heteroscedastic: log/Gamma/Tweedie objective, WLS, or quantile intervals

INDEPENDENCE  (time series and spatial data)
[ ] Residuals vs time
[ ] Residual ACF/PACF plot with confidence bands
[ ] Durbin-Watson (lag 1) and Ljung-Box (joint, up to lag h)
[ ] If autocorrelated: add lags/seasonality, or model the error process

DISTRIBUTION
[ ] Q-Q plot; skewness and excess kurtosis
[ ] Histogram of residuals
[ ] Heavy tails => Gaussian intervals under-cover; use t, quantile, or conformal

INFLUENCE
[ ] Top 10 by |residual| -- LOOK at the raw records
[ ] Top 10 by leverage (h > 2(p+1)/n)
[ ] Top 10 by Cook's distance (D > 4/n screen, D > 1 serious)
[ ] DFBETAS if any coefficient will be interpreted
[ ] Refit without the top influential points: does anything material change?
[ ] Compare in-sample R^2 with R^2_pred / CV R^2

FAIRNESS AND SEGMENTS
[ ] All metrics recomputed by each business-relevant segment
[ ] Bias by segment (offsetting biases cancel in the aggregate)
[ ] Interval coverage by segment (marginal coverage hides conditional failure)
```

**The single most valuable habit in this entire document:** after every training run, print the **ten worst residuals with their feature values** and look at them. It costs thirty seconds and it catches data errors, coverage gaps, and specification problems that no metric will ever surface.

---

# PART 12 — Multi-Output Regression

## 12.0 The problem

When the model predicts several targets at once — `Y` of shape `(n, m)` — you must decide **how to aggregate across targets**, and the choice is exactly as consequential as the macro/micro/weighted decision in multi-class classification.

**Examples:** predicting a patient's systolic and diastolic blood pressure; forecasting demand for 12 months ahead simultaneously; predicting the x, y, z coordinates of a keypoint; predicting sales for 500 SKUs from one model.

**The core issue: the targets are usually on different scales.** Predicting blood pressure (~120) and heart rate (~70) and temperature (~37) with one metric will be dominated by whichever has the largest units.

---

## 12.1 THE AGGREGATION OPTIONS

sklearn's `multioutput` parameter offers four choices, and they mean genuinely different things.

| Option | Behaviour | Use when |
|---|---|---|
| **`'raw_values'`** | Return the per-target array; no aggregation | **Always look at this first** |
| **`'uniform_average'`** | Simple mean across targets (the default) | Targets are on comparable scales and equally important |
| **`'variance_weighted'`** | Weight by each target's variance (R² only) | Targets have different variances and you want the high-variance ones to count more |
| **custom weights** | Supply an array of weights | You know the relative business importance |

**Worked example.** Two targets: price in dollars (variance 37,500) and a rating from 1–5 (variance 0.5).

| Target | Var(y) | MSE | R² |
|---|---|---|---|
| Price | 37,500 | 4,300 | 0.885 |
| Rating | 0.5 | 0.30 | 0.400 |

```
MSE, uniform_average    = (4300 + 0.30)/2 = 2,150.15    <- meaningless; price dominates
MSE, raw_values         = [4300, 0.30]                   <- informative

R²,  uniform_average    = (0.885 + 0.400)/2 = 0.6425     <- targets weighted equally
R²,  variance_weighted  = (0.885 × 37500 + 0.400 × 0.5) / 37500.5
                        = (33,187.5 + 0.2) / 37,500.5 = 0.885   <- price dominates entirely
```
**Look at what happened.** The averaged MSE (2,150) is a nonsense number in mixed units. And **variance-weighted R² (0.885) is numerically identical to the price-only R²**, because price's variance is 75,000× the rating's — the rating target has effectively been erased from the metric.

**The lesson, and it is the central lesson of Part 12:**
- **Never average a scale-dependent metric (MSE, RMSE, MAE) across targets on different scales.** Report `raw_values`, or normalise each target first.
- **`variance_weighted` R² is dominated by the highest-variance target** — it is the analogue of `weighted avg` in a classification report, and it has the same blind spot for the small/rare thing you might care about most.
- **`uniform_average` R² is the analogue of macro-averaging** and gives each target an equal vote, which is usually what you want when the targets are genuinely distinct quantities.

### Python
```python
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# ALWAYS start here
r2_score(Y, Y_pred, multioutput='raw_values')             # per-target array
mean_absolute_error(Y, Y_pred, multioutput='raw_values')

# Then choose an aggregation deliberately
r2_score(Y, Y_pred, multioutput='uniform_average')        # macro: equal per target
r2_score(Y, Y_pred, multioutput='variance_weighted')      # dominated by high-variance targets
r2_score(Y, Y_pred, multioutput=np.array([0.7, 0.3]))     # explicit business weights

# The safe way to aggregate a scale-dependent metric: normalise per target first
def normalised_rmse_per_target(Y, Y_pred):
    Y, Y_pred = np.asarray(Y, float), np.asarray(Y_pred, float)
    rmse  = np.sqrt(((Y - Y_pred) ** 2).mean(axis=0))
    sigma = Y.std(axis=0)
    return rmse / np.maximum(sigma, 1e-12)      # unitless, comparable, averageable

nrmse = normalised_rmse_per_target(Y, Y_pred)
print(nrmse, nrmse.mean())     # now the mean IS meaningful
```

---

## 12.2 METRICS THAT ONLY EXIST FOR MULTI-OUTPUT

### Mean Euclidean distance (for spatially coupled targets)
When the targets are coordinates of a single physical thing — a keypoint at (x,y), a 3-D position, a robot end-effector pose — the natural error is the **Euclidean distance**, not the per-axis MAE.
```
                     1    n     ______________________
MED  =              ───  Σ    √ Σⱼ ( yᵢⱼ − ŷᵢⱼ )²
                     n   i=1
```
This is the standard metric in **pose estimation** (where it appears as **Mean Per Joint Position Error, MPJPE**) and in **robot kinematics**. Averaging per-axis MAE would allow a model to be systematically wrong in a consistent diagonal direction while looking fine on each axis separately.

```python
def mean_euclidean_distance(Y, Y_pred):
    return np.sqrt(((np.asarray(Y, float) - np.asarray(Y_pred, float)) ** 2)
                   .sum(axis=1)).mean()
```

### Multivariate coverage and the energy score
For probabilistic multi-output forecasts, the analogue of CRPS is the **energy score**, which accounts for the **dependence** between targets:
```
                                     1
ES  =  E‖X − y‖  −  ─────  E‖X − X'‖
                                     2
```
where `‖·‖` is the Euclidean norm and X, X' are independent draws from the predictive distribution. It reduces to CRPS when m = 1. The **variogram score** is an alternative that is more sensitive to the correlation structure specifically.

**Why dependence matters:** two forecasts can have identical per-target marginal distributions and completely different joint behaviour. If you forecast demand for SKU A and SKU B, whether they peak *together* determines your warehouse capacity requirement. Per-target metrics are blind to this; the energy score is not.

### Hierarchical coherence
When targets form a hierarchy (SKU → category → total; region → country → global), an additional requirement appears: **the forecasts should add up.** Independently-produced forecasts will not.
```
Coherence error  =  | forecast(total)  −  Σ forecast(components) |
```
Report it as a percentage of the total. Non-zero coherence error means the plan is internally inconsistent, which causes real operational conflict between planning levels. **Reconciliation methods** — bottom-up, top-down, middle-out, or optimal (MinT) — enforce coherence, and MinT can *improve* accuracy at every level by exploiting the aggregation structure.

---

## 12.3 Multi-output checklist

```
[ ] Print per-target metrics FIRST (multioutput='raw_values')
[ ] Never average MSE/RMSE/MAE across targets on different scales
[ ] Normalise per target (divide by sigma or by the mean) before averaging
[ ] Choose the aggregation deliberately:
      uniform_average    -> every target counts equally (macro-like)
      variance_weighted  -> dominated by the highest-variance target
      custom weights     -> encode business importance
[ ] Check whether any target is being ignored (very poor per-target R²)
[ ] If targets are coordinates of one object -> use Euclidean distance / MPJPE
[ ] If targets are correlated and you produce distributions -> energy score,
    not just per-target CRPS
[ ] If targets form a hierarchy -> report coherence error and reconcile
[ ] Report bias per target, not just aggregate accuracy
```

**Interview (Medium) — ★ You have a 3-output model and report an averaged R² of 0.72. What is wrong with that?**
Potentially several things. First, I would not know whether that is `uniform_average` or `variance_weighted`, and they can differ enormously — variance-weighted R² is dominated by the highest-variance target, so a 0.72 could mean "one target at 0.72 and two at 0.1 that the metric ignored." Second, the average hides whether any single target is failing outright, including the possibility of a negative per-target R². Third, if the targets are on different scales I would want to check that the aggregation is not simply reporting the largest one. The fix is to always print `multioutput='raw_values'` first, choose the aggregation deliberately with a stated reason, and — if the targets are coordinates of one physical object or are strongly correlated — use a metric that respects that structure (Euclidean distance, or the energy score for probabilistic outputs) rather than any per-target average.

---

# PART 13 — Master Comparison Tables

## 13.1 Core reference table

| Metric | Purpose | Formula | Range | Best | Units | Outlier sensitivity | Symmetric? | Optimal predictor |
|---|---|---|---|---|---|---|---|---|
| **MAE** | Typical miss | mean\|e\| | [0,∞) | 0 | y | Moderate | Yes | **Median** |
| **MedAE** | Typical miss, robust | median\|e\| | [0,∞) | 0 | y | **Very low** | Yes | — |
| **Max Error** | Worst case | max\|e\| | [0,∞) | 0 | y | **Maximal** | Yes | — |
| **SSE/RSS** | Total squared error | Σe² | [0,∞) | 0 | y² | High | Yes | Mean |
| **MSE** | Mean squared error | mean(e²) | [0,∞) | 0 | y² | High | Yes | **Mean** |
| **RMSE** | Tail-weighted miss | √mean(e²) | [0,∞) | 0 | y | High | Yes | **Mean** |
| **MAPE** | % miss per item | mean\|e/y\| | [0,∞) | 0 | % | Moderate | **No** (favours under) | Weighted median |
| **sMAPE** | % miss, "symmetric" | mean(\|e\|/((\|y\|+\|ŷ\|)/2)) | [0,2] | 0 | % | Moderate | **No** (favours over) | — |
| **WAPE** | Σ\|e\|/Σ\|y\| | Σ\|e\|/Σ\|y\| | [0,∞) | 0 | % | Moderate | Yes | — |
| **MdAPE** | Typical % miss | median\|e/y\| | [0,∞) | 0 | % | **Very low** | No | — |
| **MPE** | **BIAS** | mean(e/y) | (−∞,∞) | **0** | % | Moderate | signed | — |
| **RAE** | vs mean-baseline MAE | Σ\|e\|/Σ\|y−ȳ\| | [0,∞) | 0 | — | Moderate | Yes | — |
| **RSE** | vs mean-baseline MSE | Σe²/Σ(y−ȳ)² = 1−R² | [0,∞) | 0 | — | High | Yes | — |
| **MASE** | vs naive MAE | MAE/MAE_naive_insample | [0,∞) | 0 (**1 = naive**) | — | Moderate | Yes | — |
| **Theil's U2** | vs naive RMSE | RMSE/RMSE_naive | [0,∞) | 0 (**1 = naive**) | — | High | Yes | — |
| **MSLE** | Squared log error | mean(Δlog1p²) | [0,∞) | 0 | — | Low | **No** (favours over) | — |
| **RMSLE** | Relative error | √MSLE | [0,∞) | 0 | ≈% | Low | **No** (favours over) | — |
| **MdSA** | Symmetric % miss | exp(median\|ln(ŷ/y)\|)−1 | [0,∞) | 0 | % | **Very low** | **Yes** | — |
| **R²** | Variance explained | 1−SSres/SStot | (−∞,1] | 1 | — | High | Yes | Mean |
| **Adj R²** | R² penalised for p | 1−(1−R²)(n−1)/(n−p−1) | (−∞,1] | 1 | — | High | Yes | — |
| **Explained Var** | Variance captured | 1−Var(e)/Var(y) | (−∞,1] | 1 | — | High | Yes | — |
| **Pearson r** | Linear association | Cov/σσ | [−1,1] | 1 | — | High | Yes | — |
| **Spearman ρ** | Monotone association | r on ranks | [−1,1] | 1 | — | **Very low** | Yes | — |
| **CCC** | Agreement (45° line) | 2Cov/(Vy+Vŷ+Δμ²) | [−1,1] | 1 | — | High | Yes | — |
| **Huber** | Robust smooth loss | ½e² or δ(\|e\|−½δ) | [0,∞) | 0 | mixed | Bounded | Yes | Between |
| **Log-Cosh** | Smooth Huber | mean ln cosh(e) | [0,∞) | 0 | mixed | Bounded | Yes | Between |
| **Pinball** | Quantile τ | max(τe,(τ−1)e) | [0,∞) | 0 | y | Moderate | **No, by design** | **Quantile τ** |
| **ε-insensitive** | Tolerance band | max(0,\|e\|−ε) | [0,∞) | 0 | y | Bounded | Yes | A tube |
| **Tukey biweight** | Redescending robust | see 7.4.2 | [0,∞) | 0 | mixed | **Rejects** | Yes | Inlier mean |
| **Gaussian NLL** | Predictive density | ½ln(2πσ²)+e²/2σ² | (−∞,∞) | −∞ | awkward | **Unbounded** | Yes | Distribution |
| **CRPS** | Predictive CDF | ∫(F−1{x≥y})²dx | [0,∞) | 0 | **y** | Bounded | Yes | Distribution |
| **PICP** | Coverage | fraction inside | [0,1] | **nominal** | — | Low | — | — |
| **MPIW** | Interval width | mean(U−L) | [0,∞) | 0* | y | Low | — | — |
| **Interval Score** | Width + exceedance | (U−L)+2/α·exceed | [0,∞) | 0 | y | High | — | Quantiles α/2, 1−α/2 |
| **AIC** | Predictive selection | 2k−2lnL | (−∞,∞) | min | — | High | — | — |
| **AICc** | AIC, small n | AIC+2k(k+1)/(n−k−1) | (−∞,∞) | min | — | High | — | — |
| **BIC** | Parsimony selection | k·ln(n)−2lnL | (−∞,∞) | min | — | High | — | — |
| **Mallows' Cp** | Subset selection | RSSp/σ̂²−n+2p | (−∞,∞) | ≈p | — | High | — | — |
| **PRESS / R²_pred** | LOO error | Σ(e/(1−h))² | [0,∞) / (−∞,1] | 0 / 1 | y² / — | **Very high** | Yes | — |
| **CV RMSE/MAE** | Empirical generalisation | mean over folds | [0,∞) | 0 | y | varies | Yes | — |

*MPIW: lower is better only conditional on adequate coverage.

## 13.2 Best use case and business example

| Metric | Best use case | Business example |
|---|---|---|
| MAE | Cost linear in the error | Inventory units; ETA minutes; staffing hours |
| MedAE | Outliers present, want the typical case | Property valuation; salary benchmarking |
| Max Error | A single failure is catastrophic | Structural loads; drug dosing; obstacle distance |
| MSE | Training objective; need the mean/total | Any default loss; portfolio variance |
| RMSE | Cost convex in the error; need the mean | Weather; energy load; Netflix-style ratings |
| MAPE | Executive reporting, all values well above zero | Energy load %; revenue variance-to-budget |
| sMAPE | Legacy / M3 benchmark comparison | Historical forecasting competition results |
| **WAPE** | **Supply-chain accuracy, weighted by volume** | **Retail/CPG "forecast accuracy = 100 − WAPE"** |
| MdAPE / PE10 | Public accuracy claims, heavy-tailed target | Zillow-style AVM "median error rate" |
| **MPE / total bias** | **Detecting systematic bias — always report** | **Stockouts vs overstock; insurance reserving** |
| RAE / RSE | Unitless cross-dataset comparison | AutoML / WEKA reporting |
| **MASE** | **Forecasting, incl. intermittent demand** | **Spare parts; cross-SKU aggregation; FVA analysis** |
| Theil's U2 | Forecasting where RMSE is the loss | Macroeconomic forecasting |
| **RMSLE** | **Positive skewed target, relative error** | **House prices; sales volumes; web traffic; Kaggle** |
| MdSA / SSPB | Symmetric relative error, strictly positive | Space weather; physical-science model validation |
| **R²** | **Variance explained; academic reporting** | **Papers; exec dashboards; model monitoring** |
| Adj R² | Comparing nested linear models | Econometrics; GLM specification |
| Explained Var | Bias diagnostic (gap vs R²) | Detecting back-transform bias |
| Spearman ρ | Only the ranking is consumed | Finance Information Coefficient; lead scoring |
| CCC | Agreement with a gold standard | Instrument/method-comparison studies |
| Huber | Robust training with smooth gradients | Bounding-box regression; financial series; sensors |
| Log-Cosh | Robust, no hyperparameter, Hessian optimisers | Deep regression; XGBoost pseudo-Huber |
| **Pinball** | **Asymmetric cost; service levels; intervals** | **Safety stock (newsvendor); ETA promises; VaR** |
| ε-insensitive | An explicit tolerance band exists | SVR; engineering tolerances |
| Tukey | Gross data errors present | Astronomy; contaminated sensor data |
| Gaussian NLL | **Training** probabilistic models | Deep ensembles; GPs; GARCH; NGBoost |
| **CRPS** | **Reporting probabilistic forecasts** | **Weather; energy; M5 Uncertainty; comparable to MAE** |
| PICP / MPIW | **Communicating** uncertainty | "90% interval contains truth 89% of the time" |
| Interval Score | Proper single score for intervals | M4 (MSIS); COVID-19 Forecast Hub (WIS) |
| AIC / AICc | Classical model selection | ARIMA order; GLM specification |
| BIC | Parsimony; number of mixture components | GMM cluster count; regulated models |
| CV RMSE | **Default for all model selection** | Every `GridSearchCV`; AutoML |

## 13.3 Advantages and limitations at a glance

| Metric | Key advantage | Key limitation |
|---|---|---|
| MAE | Interpretable "average miss" | Blind to bias; targets the median, so totals are biased low on skewed targets |
| MedAE | 50% breakdown point | Ignores the tail entirely |
| Max Error | The only worst-case metric | One observation; grows with n |
| MSE | Smooth gradients; MLE under Gaussian; targets the mean | Squared units; outlier-dominated |
| RMSE | MSE in interpretable units; 68/95 reading | Dominated by outliers; not a "typical" error |
| MAPE | Universally understood percentage | Undefined at 0; explodes near 0; **asymmetric, biases forecasts low** |
| sMAPE | Bounded [0,200%] | **Not actually symmetric**; three incompatible definitions |
| WAPE | Handles zeros; volume-weighted; symmetric | Hides the long tail of small items |
| MdAPE | Robust percentage | Hides the tail; can flatter badly |
| MPE | **The only bias detector** | Errors cancel; must pair with a magnitude metric |
| RAE/RSE | Unitless, benchmarked | Mean baseline is weak, especially for time series |
| MASE | Zeros-safe; 1.0 = naive anchor; aggregates | Needs a training series; seasonality must be stated |
| Theil's U2 | RMSE-based naive benchmark | Two definitions share the name |
| RMSLE | Relative error; robust; handles 0 | Needs y ≥ 0; asymmetric; back-transform bias |
| MdSA | Genuinely symmetric relative error | Needs y > 0; unfamiliar |
| R² | Anchored at 0; unitless; universal | In-sample always rises with p; leverage-sensitive; **bad across segments and for time series** |
| Adj R² | Penalises complexity | Weak penalty; needs a countable p |
| Explained Var | Isolates shape from calibration | Ignores bias — so a bad headline metric |
| Pearson r | Measures association | **Blind to scale and offset; `r²` ≠ `R²`** |
| Spearman ρ | Robust ranking measure | Discards all magnitude information |
| CCC | Penalises bias and spread mismatch | Range-sensitive; unfamiliar |
| Huber | Smooth + robust; δ has business meaning | δ is scale-dependent; loss uninterpretable |
| Log-Cosh | No hyperparameter; C² smooth | **Fixed transition at \|e\|≈1 → must standardise** |
| Pinball | Encodes asymmetric cost; gives intervals | One model per quantile; quantiles do not add |
| ε-insensitive | Encodes a tolerance; sparse solutions | ε scale-dependent; discards in-tube data |
| Tukey | Fully rejects gross errors | **Non-convex**; can reject genuine rare events |
| Gaussian NLL | Proper; trainable; heteroscedastic | Unbounded; needs a distributional family; fragile at σ→0 |
| CRPS | Proper, bounded, **in y's units, = MAE for points** | Not in sklearn; under-penalises extreme tails |
| PICP | Instantly interpretable | Not proper; marginal only; coarse |
| MPIW | Interpretable sharpness | Not proper; meaningless alone |
| Interval Score | Proper; width + distance-weighted exceedance | Exceedance-dominated; α-specific |
| AIC | LOO-CV without holding out data | Needs a likelihood and k; asymptotic (use AICc) |
| BIC | Consistent; favours parsimony | Assumes the true model is in the set; under-fits for prediction |
| CV | Assumption-free; any model, any metric | Expensive; leakage is easy and silent |

## 13.4 Which metrics move together (avoid double-counting)

| Group | Members | Relationship |
|---|---|---|
| Same thing, different names | MAE = Mean Absolute Deviation (forecasting sense) = L1 loss | Identical |
| | MSE = L2 loss = quadratic loss | Identical |
| | SSE = RSS = (sometimes) SSR | Identical |
| Trivial transforms | RMSE = √MSE; RMSLE = √MSLE | Monotone — same model ranking |
| | Error Rate analogues: RSE = 1 − R² | Exact |
| | RRSE = √RSE = RMSE/σ_y | Exact |
| | WAPE = MAE / mean\|y\| | Exact |
| | Gini-style: none in regression | — |
| Exact identities | EVS = R² + Bias²/Var(y) | Gap = normalised squared bias |
| | MSE = Bias² + Var(e) | Exact decomposition |
| | RMSE² = MAE² + Var(\|e\|) | Exact |
| | Pinball(τ=0.5) = MAE/2 | Exact |
| | CRPS(point forecast) = MAE | Exact |
| | CRPS = 2∫₀¹ pinball_τ dτ | Exact |
| | Interval Score = (2/α)[pinball_{α/2} + pinball_{1−α/2}] | Exact |
| | Dice-analogue: none | — |
| Only equal in special cases | r² = R² | **Only** for in-sample OLS with an intercept |
| | Mallows' Cp ≈ AIC | For Gaussian OLS |
| | AIC ≈ LOO-CV | Asymptotically |
| | Gaussian NLL ≈ MSE | When σ is constant |
| | Log-Cosh = MAE − ln2 | When all \|e\| ≫ 1 (the degenerate case) |
| Same quantity, different penalty | AIC (2k), BIC (k ln n), AICc, Adj R² | Same deviance, different complexity charge |

**What to report instead — a non-redundant regression dashboard:**
**MAE · RMSE (and their ratio) · MedAE · Max Error · total bias % · a scaled metric (MASE / WAPE / R²) · CV score with fold spread · the residual panel.**

---

# PART 14 — Which Metric Should I Use? (Decision Tree)

## 14.1 The main decision tree

```
START: What is the prediction used for?
│
├── A RANKING or a SELECTION (top-k, sort, prioritise)?
│      -> SPEARMAN rho (primary), plus decile-level actuals
│      -> Add R2 only to make the calibration question visible
│      -> Do NOT lead with RMSE/MAE: magnitude is not consumed
│
├── A PROBABILITY / DISTRIBUTION (pricing, risk, capacity, expected value)?
│      -> Train on GAUSSIAN NLL (or a distributional objective)
│      -> Report CRPS (with a skill score), PICP/MPIW at 50/80/90/95%,
│         and a PIT histogram
│      -> Add CONFORMAL PREDICTION if coverage must be guaranteed
│
├── A QUANTILE / SERVICE LEVEL (safety stock, ETA promise, capacity)?
│      -> Train on PINBALL LOSS with tau = C_under/(C_under + C_over)
│      -> Report pinball at that tau, plus empirical coverage at tau
│      -> Do NOT use MAE/RMSE: they target the median/mean, not a quantile
│
└── A POINT PREDICTION -> continue
      │
      ├── Is the COST ASYMMETRIC? (under- and over-prediction cost differently)
      │      YES -> PINBALL LOSS (linear cost) or an asymmetric squared/Huber
      │              loss (convex cost). No symmetric metric can substitute.
      │      NO  -> continue
      │
      ├── Is the TARGET positive, right-skewed, spanning orders of magnitude?
      │      YES -> Relative error is what matters:
      │              - RMSLE, or train on log1p(y), or
      │              - GAMMA/TWEEDIE objective with a log link  <- usually best
      │                (no back-transform bias; models the mean directly)
      │              - Report MdAPE / MdSA / WAPE for communication
      │              - Beware: if you log-transform, apply a smearing correction
      │                or the totals will be biased low
      │      NO  -> continue
      │
      ├── Is the target a COUNT (0,1,2,...) ?
      │      YES -> POISSON deviance (or NEGATIVE BINOMIAL if over-dispersed;
      │              TWEEDIE if zero-inflated and continuous-positive)
      │              Do NOT use RMSLE (the +1 shift distorts small counts)
      │      NO  -> continue
      │
      ├── Does a SINGLE LARGE ERROR matter more than many small ones?
      │      YES, catastrophically -> MAX ERROR (as a pass/fail tolerance)
      │                              + the 99.9th percentile of |e|
      │                              + an ASYMMETRIC loss so errors go the safe way
      │      YES, convexly         -> RMSE (train on MSE)
      │      NO                    -> MAE (train on L1 or Huber)
      │
      ├── Are there OUTLIERS or suspected label noise?
      │      YES -> Train on HUBER (delta from a quantile of |e| or from business)
      │              or LOG-COSH (standardise the target first)
      │              Report MedAE alongside RMSE, and the RMSE/MAE ratio
      │              If GROSS ERRORS -> TUKEY (initialise from Huber)
      │      NO  -> MSE/RMSE is fine
      │
      ├── Is this a TIME SERIES?
      │      YES -> MASE (correct seasonality, training-set denominator)
      │              + WAPE at the decision level
      │              + total bias % and a TRACKING SIGNAL
      │              + a METRIC-BY-HORIZON table (find where MASE crosses 1.0)
      │              + residual ACF / Ljung-Box
      │              Backtest with TimeSeriesSplit and a GAP. Never shuffled KFold.
      │              Do NOT use R2 (the mean is a hopeless baseline)
      │
      ├── Are you AGGREGATING ACROSS SERIES/ITEMS of different scale?
      │      YES -> MASE (average the per-series values) or WAPE (volume-weighted)
      │              Never average raw MAE/RMSE across scales
      │
      ├── Do you need to COMPARE ACROSS DATASETS or report to executives?
      │      -> A unitless metric: R2, MASE, WAPE, MdAPE, RMSLE
      │      -> Plus the absolute metric in units, for context
      │
      └── SELECTING A MODEL (not measuring one)?
             -> CROSS-VALIDATED score with the right splitter
                (TimeSeriesSplit / GroupKFold / KFold), preprocessing inside
                a Pipeline, and the fold-to-fold spread reported
             -> Complement with AICc (small n) and BIC (parsimony) for
                classical models
             -> Never select on in-sample R2/RMSE
             -> Use nested CV or an untouched test set for the published number
```

## 14.2 Fast lookup by scenario

| Scenario | Primary metric | Train on | Also report | Never use alone |
|---|---|---|---|---|
| General regression, symmetric cost, no outliers | RMSE | MSE | MAE, bias, R², CV | R² |
| Cost linear in the miss | MAE | L1 / Huber | RMSE, bias, MedAE | RMSE |
| Outliers / label noise present | MedAE + MAE | Huber | RMSE, Max Error, RMSE/MAE ratio | RMSE |
| Single catastrophic error | Max Error (tolerance) | Asymmetric loss | p99.9 of \|e\|, RMSE | MAE |
| Positive skewed target (prices, sales) | RMSLE | log1p MSE or Gamma/Tweedie | MdAPE, WAPE, bias | RMSE |
| Count target | Poisson deviance | Poisson / NB | MAE, bias | RMSLE |
| Asymmetric cost | Pinball at τ* | Pinball | Coverage at τ, expected cost | MAE, RMSE |
| Safety stock / service level | Pinball at τ = C_u/(C_u+C_o) | Pinball | Empirical coverage, fill rate | MAPE |
| ETA / delivery promise | Pinball at 0.9 | Pinball | % late, coverage | MAE |
| Time-series forecast | MASE (seasonal) | depends on cost | WAPE, bias, tracking signal, horizon table | R², MAPE |
| Intermittent demand | MASE | Tweedie / Croston | WAPE, cumulative-error-over-lead-time | MAPE, RMSE |
| Cross-SKU portfolio | mean MASE + % with MASE ≥ 1 | per-series | WAPE (weighted), bias | mean MAE |
| Executive reporting | WAPE or MAPE | — | MAE in units, bias, baseline | any single number |
| Ranking / selection only | Spearman ρ | any | Decile actuals, stability across folds | RMSE |
| Probabilistic forecast | CRPS (skill score) | Gaussian NLL | PICP/MPIW curve, PIT histogram | PICP alone |
| Prediction intervals | Interval Score | Pinball (2 quantiles) | PICP, MPIW, conditional coverage | MPIW alone |
| Instrument / method comparison | CCC | — | Bland-Altman plot, bias | Pearson r |
| Model selection, any model | CV score (business metric) | — | Fold spread, train-test gap | in-sample anything |
| Model selection, classical, small n | **AICc** | — | BIC, CV, ΔAICc table + weights | AIC |
| Explanatory / regulated model | BIC + Adj R² | — | CV, coefficient stability, DFBETAS | R² |
| Multi-output, different scales | per-target raw_values | — | Normalised RMSE per target, then average | averaged MSE |
| Multi-output coordinates | Mean Euclidean distance / MPJPE | — | Per-axis MAE | per-axis average |
| Hierarchical forecasts | MASE per level + coherence error | — | Reconciled metrics | independent per-level |
| Fairness / segment audit | Per-segment MdAPE + bias | — | Coverage per segment, worst segment | aggregate anything |

## 14.3 The four questions that determine everything

1. **What does the prediction *do*, and what does each direction of error *cost*?**
   → point vs quantile vs distribution; symmetric vs asymmetric loss.
2. **Do I care about absolute or relative error?**
   → MAE/RMSE vs RMSLE/MAPE/Gamma-Tweedie.
3. **Do large errors matter disproportionately, and are any of them data errors?**
   → MAE/Huber/MedAE vs RMSE vs Max Error vs Tukey.
4. **Is the data i.i.d., or is it a time series / grouped / hierarchical?**
   → determines the baseline (mean vs naive), the CV scheme, and whether R² is meaningful.

Answer those four and the metric follows mechanically. **Then add a signed bias metric and a residual plot, always.**

---

# PART 15 — Industry Case Studies

## 15.1 House Price / Automated Valuation (AVM)

**Setup.** Prices from $80k to $8M, heavily right-skewed. Predictions used by lenders (loan-to-value), sellers (list price), and internal analytics.

**Cost structure.** Roughly **relative**: a 10% error matters equally at $200k and $2M. Slight asymmetry for lending — over-valuation creates credit risk, so lenders prefer conservatism.

**Metrics**
- **Primary: MdAPE and PE10/PE20** — the public industry standard. "Half of valuations within 4.2%; 80% within 10%." Robust to the genuine long tail of unusual properties.
- **RMSLE** as the modelling metric, or better, train with a **Gamma/Tweedie objective and log link** so relative error is optimised without back-transform bias.
- **Segment everything** — by price band, property type, geography, and data completeness. A model with excellent overall MdAPE can fail systematically on new-builds or rural properties.
- **Prediction intervals** — a valuation without a range is not usable for lending. Quantile regression at 0.1/0.5/0.9, validated with PICP **by price band** (not marginally).
- **Bias by segment** — persistent over-valuation in a segment is a credit-risk exposure.
- **Max Error and the p99 of APE** — for the tail that generates complaints and disputes.

**Why these.** The target spans two orders of magnitude, so RMSE would optimise for mansions and ignore starter homes. The market has genuine extreme values, so mean-based percentage metrics are unstable. And the consumer-facing product is a number people will dispute, so a median-based claim plus an interval is both more honest and more defensible.

**Do not use:** RMSE as the headline; R² across segments (narrow-range segments will look artificially bad); MAPE (unstable at the low end).

**Practical note.** Report an abstention rate: the fraction of properties where the model declines to quote because its interval is too wide. Showing a wide interval or declining is far better for trust than a confident wrong number.

---

## 15.2 Retail Demand Forecasting

**Setup.** 50,000 SKU-store combinations, weekly, many intermittent. Drives replenishment, allocation, and labour planning.

**Cost structure.** Strongly **asymmetric**: a stockout costs lost margin plus customer goodwill; excess costs holding, markdown, and waste. Typical ratios 5:1 to 50:1 favouring availability — but the ratio inverts for perishables.

**Metrics**
- **Primary: WAPE at the decision level** (store-SKU-week), reported as "accuracy = 100 − WAPE." The industry convention, volume-weighted so it tracks business impact.
- **MASE per series with the correct seasonality**, plus the **fraction of series with MASE ≥ 1** — those should be served by the seasonal naive forecast, and that fraction is a direct measure of where the model adds nothing.
- **Total bias % and a tracking signal per series** — non-negotiable. Bias compounds into inventory positions, and a 92%-accurate but 3%-biased forecast causes chronic stockouts.
- **Pinball loss at the service-level quantile** — because the replenishment decision is a quantile, not a mean. `τ = C_stockout/(C_stockout + C_holding)`, the newsvendor fractile.
- **A metric-by-horizon table** — accuracy at h=1 is a different business than h=13.
- **Segment by volume band and intermittency class** — WAPE is volume-weighted, so the long tail is invisible in the headline and is exactly where stockouts happen.

**Why these.** MAPE is undefined or absurd for intermittent SKUs, and it biases forecasts low because of its asymmetry. Raw MAE cannot be aggregated across SKUs of wildly different volume. And the decision is a quantile, so evaluating the mean forecast measures the wrong functional.

**Do not use:** MAPE (zeros and downward bias); averaged MAE across SKUs; R²; accuracy without bias; a single number averaged across horizons.

---

## 15.3 Delivery Time / ETA Prediction

**Setup.** Predicting arrival time for a ride, a food order, or a parcel. The prediction is a **promise shown to a customer.**

**Cost structure.** Sharply **asymmetric and non-linear**: being early is nearly free (mildly wasteful); being late damages trust and generates support contacts, with the cost escalating past a threshold.

**Metrics**
- **Primary: pinball loss at τ ≈ 0.85–0.95.** The ETA shown should be a high quantile, not the mean or median. **If you show the median you are late half the time** — the single most important insight in this case study.
- **Percentage of promises met** (`P(actual ≤ promised)`) — the customer-facing KPI, and it should match your chosen τ.
- **Conditional coverage** by time of day, distance band, weather, and city — marginal coverage hides systematic lateness in rush hour.
- **MAE / MedAE on the *median* prediction** for internal model quality, separately from the promise.
- **Asymmetric expected cost:** `C_late × E[max(0, actual − promised)] + C_early × E[max(0, promised − actual)]` — the number that justifies the τ choice.
- **The p95 and p99 of lateness** — the tail that generates escalations.

**Why these.** The whole problem is a quantile problem masquerading as a regression problem. Teams routinely build an excellent MAE-optimal model and then wonder why customer satisfaction is poor — the model is fine, the *functional* is wrong.

**Do not use:** MAE or RMSE as the primary metric; symmetric loss; marginal coverage only.

**Practical note.** Two-sided display ("15–25 min") is a two-quantile problem and should be evaluated with the Interval Score, not with MAE on the midpoint.

---

## 15.4 Energy Load Forecasting

**Setup.** Day-ahead and intraday electricity demand at system level. Drives generation scheduling and reserve procurement.

**Cost structure.** **Convex and asymmetric.** Imbalance penalties escalate super-linearly; under-forecasting risks load shedding (catastrophic), over-forecasting wastes spinning reserve (expensive but recoverable).

**Metrics**
- **Primary: MAPE** — genuinely appropriate here, because load never approaches zero and the industry targets 1.5–3%. One of the few domains where MAPE is the right choice.
- **RMSE** — because the cost is convex, squared error matches the penalty structure better than absolute error.
- **Pinball loss / quantile forecasts** for reserve setting; reserve requirements *are* quantiles of the forecast error distribution.
- **CRPS** for probabilistic forecasts — the standard in the Global Energy Forecasting Competitions.
- **Peak-period metrics reported separately** — errors during the daily and annual peak matter far more than errors at 3 a.m., so a flat average is misleading. Report MAPE during peak hours as a separate KPI.
- **Metric-by-horizon** and **by hour of day**.

**Why these.** Convex cost → RMSE. Non-zero, stable magnitude → MAPE is safe and interpretable. Reserve decisions are quantile decisions → pinball/CRPS.

**Do not use:** MAE alone (understates the convex penalty); a single average across hours (hides peak failures).

---

## 15.5 Insurance Claim Severity and Reserving

**Setup.** Predicting the ultimate cost of a claim. Positive, extremely right-skewed, with genuine catastrophic tail events. Drives pricing and statutory reserves.

**Cost structure.** For pricing, the **mean** must be right (premium = frequency × severity). For reserving, the **total** must be adequate, and regulators require conservatism.

**Metrics**
- **Primary: total bias / actual-vs-expected ratio** — reserving is a *total* problem, and being 5% low in aggregate is a regulatory and solvency issue regardless of per-claim accuracy. This is the metric that matters most, and it is a signed one.
- **Train with a Gamma or Tweedie objective and log link** — the correct likelihood for positive skewed data, models the mean directly (so the totals aggregate), and handles the variance structure. **Not** log-transformed MSE, because the back-transform bias would systematically under-reserve.
- **MedAE / MdAPE** for per-claim typical accuracy, robust to catastrophic claims.
- **High quantiles (pinball at 0.95/0.99) and CRPS** for the tail, because the reserve is a high quantile of the aggregate distribution, not its mean.
- **Lorenz curve / Gini** for pricing segmentation quality — the ability to rank risks matters as much as absolute accuracy for competitive pricing.
- **Segment A/E ratios** by line of business, region, and cohort.

**Why these.** The distinction between "get the mean right" (pricing) and "get the aggregate tail right" (reserving) drives everything, and the two need different metrics. And because the target is skewed with a real tail, RMSE would be dominated by a handful of catastrophic claims while MedAE would ignore them entirely — you need both plus explicit tail metrics.

**Do not use:** RMSE as the headline; log-MSE with naive back-transformation (systematically under-reserves); any absolute metric without a signed bias metric.

---

## 15.6 Financial Return Prediction

**Setup.** Predicting next-period asset returns. Signal-to-noise is extremely low. Predictions feed portfolio construction, which **sorts** assets.

**Cost structure.** Determined by the portfolio, not by per-asset error. What matters is whether the *ranking* is informative and whether it is *stable*.

**Metrics**
- **Primary: Information Coefficient** — the cross-sectional Spearman correlation between predicted and realised returns, computed each period and averaged. **0.03–0.06 is a good IC.**
- **IC stability:** the mean IC divided by its standard deviation across periods (an "IC information ratio"). A high average IC with huge variance is not tradeable.
- **Decile spread:** the realised return of the top decile minus the bottom decile — the direct economic translation of the signal.
- **R² and RMSE are near-useless as headlines** — an R² of 0.01 can be highly profitable, and reporting it makes the model look worthless.
- **Turnover and decay:** how fast the signal loses value, and how much trading it implies. A signal with a great IC and 300% monthly turnover may not survive transaction costs.
- **Backtest hygiene:** purged, embargoed walk-forward CV; point-in-time data; no survivorship bias. The metric is only as good as the backtest.

**Why these.** Portfolio construction consumes the ordering, so rank correlation is the right functional. Absolute accuracy metrics measure something the strategy never uses, and their values are so poor in absolute terms that they mislead stakeholders about a genuinely valuable signal.

**Do not use:** R², RMSE, or MAPE as headline metrics; any in-sample or shuffled-CV backtest.

---

## 15.7 Clinical / Physiological Prediction

**Setup.** Predicting a continuous clinical value — blood glucose, blood pressure, creatinine clearance, length of stay. Drives treatment decisions.

**Cost structure.** Often **asymmetric and zone-dependent.** In glucose prediction, an error that leads to under-treating hypoglycaemia is dangerous, while the same magnitude of error in the normal range is harmless.

**Metrics**
- **Primary: clinically-weighted / zone-based metrics.** In glucose prediction the standard is the **Clarke or Parkes Error Grid**, which classifies each prediction into zones A–E by clinical consequence rather than by numeric error. This is a domain-specific metric that encodes the cost function directly and is far more meaningful than RMSE.
- **RMSE / MAE** as supporting numbers and for comparability with the literature.
- **Prediction intervals with validated coverage** — a clinician needs to know the plausible range, and coverage must hold *within* clinically important sub-ranges (conditional, not marginal).
- **CCC and a Bland-Altman plot** when validating a new measurement device against a gold standard — Pearson r is insufficient because it cannot detect bias or scale error.
- **Bias by patient subgroup** — a model biased for one demographic is a safety and equity issue.
- **Calibration curves** if the output is used quantitatively in a clinical formula.

**Why these.** The cost of an error depends on *where in the range* it occurs, which no scale-free numeric metric captures. Error-grid analysis exists precisely because clinicians rejected RMSE as clinically uninformative.

**Do not use:** RMSE alone; aggregate metrics without subgroup breakdown; Pearson r for device validation.

---

## 15.8 Case study summary

| Case | Target character | Cost structure | Primary metric | Train on | Never use |
|---|---|---|---|---|---|
| **House price / AVM** | Positive, skewed, 2 orders of magnitude | Relative, mildly asymmetric | **MdAPE + PE10/PE20** | Gamma/Tweedie log link | RMSE headline; segment R² |
| **Retail demand** | Non-negative, intermittent, many series | Asymmetric (stockout ≫ holding) | **WAPE + MASE + bias** | Pinball at τ*, or Tweedie | MAPE; averaged MAE |
| **Delivery ETA** | Positive, right-skewed | Sharply asymmetric (late ≫ early) | **Pinball at τ≈0.9** | Pinball | MAE, RMSE |
| **Energy load** | Positive, never near zero | Convex, asymmetric | **MAPE + RMSE + CRPS** | MSE, pinball for reserves | MAE alone |
| **Insurance severity** | Positive, extreme tail | Total must be adequate | **Total bias (A/E) + tail quantiles** | Gamma/Tweedie | log-MSE naive back-transform |
| **Financial returns** | Near-zero signal | Ranking-driven | **Information Coefficient** | anything | R², RMSE headline |
| **Clinical values** | Bounded, zone-dependent risk | Asymmetric, zone-dependent | **Error grid / zone metric** | asymmetric loss | RMSE alone |

**The pattern across all seven:** the metric is determined by (a) the **functional** the decision needs (mean, median, quantile, ranking, or distribution), (b) whether the cost is **absolute or relative** and **symmetric or asymmetric**, and (c) the **operational constraint** (regulatory adequacy, service level, capacity, clinical safety). It is never determined by which metric is most familiar.

---

# PART 16 — 120+ Interview Questions with Answers

*Organised by level. ★ = commonly asked. Answers build on the running example throughout the document.*

---

## 16.1 Beginner (Q1–Q25)

**Q1. What is a regression metric?**
A number that summarises how close a model's numeric predictions are to the true values on held-out data. Unlike classification, every regression prediction is *somewhat* wrong; the metric quantifies the size and character of the miss.

**Q2. What is a residual?**
`eᵢ = yᵢ − ŷᵢ`. A positive residual means the model predicted *too low* (under-prediction); negative means too high.

**Q3. What is MAE?**
Mean Absolute Error: `mean(|y − ŷ|)`. The average size of a miss, in the target's own units. On our 10-house example, MAE = 36 → the model misses by $36k on average.

**Q4. What is RMSE?**
Root Mean Squared Error: `√mean((y − ŷ)²)`. Like MAE but extra-sensitive to large errors because they are squared. Our RMSE = 65.57 vs MAE = 36, ratio 1.82 — the large gap signals an outlier.

**Q5. ★ Is RMSE always ≥ MAE?**
Yes, always. The quadratic mean of non-negative numbers ≥ their arithmetic mean (power-mean inequality). Exactly: `RMSE² = MAE² + Var(|e|)`, so equality holds only when all absolute errors are identical.

**Q6. What are the units of MAE, RMSE, and MSE?**
MAE and RMSE are in the same units as the target (e.g. dollars, minutes). MSE is in the *squared* units — dollar-squared — which is why MSE is not reported directly.

**Q7. What is R²?**
The fraction of the target's variance explained by the model: `1 − SS_res/SS_tot`. R² = 0 means the model is no better than predicting the mean; R² = 1 is perfect; R² < 0 (possible out-of-sample) means the model is *worse* than the mean.

**Q8. What is the range of R²?**
(−∞, 1]. It is unbounded below. On our example, in-sample R² = 0.885; out-of-sample (PRESS-based) R²_pred = −0.72, entirely because one observation has leverage 0.75 and dominates the fit.

**Q9. What is MAPE?**
Mean Absolute Percentage Error: `mean(|y − ŷ|/|y|) × 100%`. Answers "how far off as a percentage of the actual value." Our MAPE = 6.57%. Undefined when any actual is zero.

**Q10. Why is MAPE undefined at zero?**
Because it divides by the actual value. `|e|/0 = ∞`.

**Q11. What is the difference between MAE and MedAE?**
MAE is the *mean* of the absolute errors; MedAE is the *median*. MedAE is more robust — up to 50% of observations can be arbitrarily corrupted and MedAE is unaffected. Our MedAE = 20, MAE = 36; the gap reveals a heavy tail.

**Q12. ★ What does a negative R² mean?**
That the model's squared error exceeds the squared error of simply predicting the sample mean. The model is worse than doing nothing. Common causes: severe overfitting, distribution shift between train and test, a bug (wrong column, inverted transform).

**Q13. What is WAPE?**
`Σ|e| / Σ|y|`. Total absolute error divided by total actual. Equivalently, MAE/mean(|y|). Well-defined when the *total* is non-zero, even if individual actuals are zero. Volume-weighted so high-value items count more. Our WAPE = 8.0%.

**Q14. How does WAPE differ from MAPE?**
MAPE averages per-item percentages (equal weight to each item). WAPE weights by volume. They diverge when errors concentrate in high- or low-value items. Our MAPE = 6.57%, WAPE = 8.00% — errors are in the most expensive house, which MAPE dilutes.

**Q15. What is MPE and why must you always report it?**
Mean Percentage Error: `mean((y − ŷ)/y) × 100%`. It keeps the *sign*, so it detects systematic bias. MAE and RMSE take absolute values and cannot tell a randomly-wrong model from a consistently-wrong one. Our MPE = +1.4% (under-forecasts on average).

**Q16. What is Max Error?**
The largest single absolute residual. Our Max Error = 200 (house 10). The only metric that describes the worst case. It grows with n, so use the 99th-percentile of |e| for cross-dataset comparison.

**Q17. What is the bias-variance decomposition of MSE at the residual level?**
`MSE = (mean residual)² + Var(residuals)`. On our data: Bias² = 324 (7.5%), Var(e) = 3,976 (92.5%). The error is mostly unstructured scatter, not systematic bias — so recalibration alone would barely help.

**Q18. What is RMSLE?**
Root Mean Squared Logarithmic Error: `√mean((log1p(y) − log1p(ŷ))²)`. Measures relative rather than absolute error; handles zeros via the +1 shift; penalises under-prediction more than over-prediction. Our RMSLE = 0.093 ≈ 9.8% typical relative error.

**Q19. When should you use RMSLE over RMSE?**
When the target is positive and right-skewed and relative (percentage) error is what the business cares about — house prices, sales volumes, web traffic. RMSE would be dominated by the expensive/high-volume end; RMSLE weights the whole range equally.

**Q20. What is the difference between the training loss and the evaluation metric?**
The loss is what the optimiser minimises during training; the metric is what you report. They should usually match — training on MSE while reporting MAE means you are optimising for the mean but measuring the median, and the mismatch can hide important model defects.

**Q21. What is AIC?**
Akaike Information Criterion: `2k − 2ln(L̂)`. Estimates out-of-sample predictive deviance. Lower is better. Only differences (ΔAIC) are meaningful. Adds a penalty of 2 per parameter to prevent over-fitting. Asymptotically equivalent to leave-one-out cross-validation.

**Q22. What is BIC?**
Bayesian Information Criterion: `k·ln(n) − 2ln(L̂)`. Like AIC but with penalty `k·ln(n)`, which grows with n, so BIC is stricter and prefers smaller models. BIC targets identifying the true model; AIC targets prediction.

**Q23. What is MASE?**
Mean Absolute Scaled Error: MAE divided by the in-sample naive forecast's MAE. MASE = 1 means no better than naive. MASE < 1 is better; MASE > 1 means the naive forecast would have been better. On our time-series example, MASE = 0.75 — 25% better than naive.

**Q24. What is cross-validation in regression?**
Repeatedly holding out a portion of the data, fitting the model on the rest, measuring the metric on the held-out portion, and averaging. The primary tool for estimating generalisation error. Must use `TimeSeriesSplit` (not shuffled K-fold) for time series.

**Q25. Why is in-sample R² not a valid model-selection criterion?**
Because R² (and all in-sample fit metrics) always improve when you add predictors, even random noise. A model with 9 useless predictors on 10 observations has R² = 1 in-sample. Use cross-validated R², AICc, or BIC.

---

## 16.2 Intermediate (Q26–Q55)

**Q26. ★ Why does MAE target the conditional median while MSE targets the conditional mean?**
MAE = `mean(|e|)`. Its subgradient with respect to `ŷ` is `sign(ŷ − y)`. Setting the expected gradient to zero gives `E[sign(ŷ − y)] = 0`, which means the probability of over- and under-prediction are equal — i.e. `ŷ` is the conditional median. MSE's gradient is `2(ŷ − y)`, and setting its expectation to zero gives `ŷ = E[y]` — the conditional mean.

**Q27. ★ You report MAE = 36 and the stakeholder asks "is that good?" How do you answer?**
Three comparisons: (1) vs scale — 36/450 = 8% of the mean; (2) vs a naive baseline — the median-predict baseline has MAE 150, so we reduce typical error by 76%; (3) vs the noise floor — if two expert appraisers differ by $30k on average, our model is essentially at the ceiling. Then note that MAE hides the distribution: nine houses are within $20k and one is off by $200k, which is the honest summary.

**Q28. ★ What is the RMSE/MAE ratio and what does it tell you?**
`RMSE/MAE = √(MSE/MAE²) = √(1 + Var(|e|)/MAE²)`. It equals 1 when all errors are equal; √(π/2) ≈ 1.253 for normally distributed errors; higher means a heavier tail. Our 1.82 signals the outlier. It is a free diagnostic that almost nobody computes but costs one line of code.

**Q29. ★ MAE vs RMSE: when do you choose each?**
MAE when cost is linear in the error (per-unit inventory, per-minute ETA), outliers are present, and interpretability matters. RMSE when cost is convex (grid imbalance penalties, cascading failures), you need the aggregate/total to be right (targets the conditional mean), or you want a metric consistent with classical inference.

**Q30. ★ Why is MAPE asymmetric and why does it bias forecasts downward?**
Because the denominator is the actual value y. An over-forecast can exceed 100% error (predicting 5× the actual = 400%); an under-forecast is capped at 100% (can't predict less than zero). So the penalty for over-forecasting is strictly larger, and any optimiser minimising MAPE shades forecasts low, causing chronic stockouts in retail.

**Q31. ★ Why can't you use MAPE for intermittent demand?**
Intermittent series contain many zeros and near-zeros. Division by zero is undefined; near-zeros inflate the percentage error to hundreds or thousands of percent from a perfectly reasonable absolute miss. Use MASE — its denominator is the single in-sample naive MAE, which is stable regardless of whether individual actuals are zero.

**Q32. ★ What is MASE's key advantage over MAPE? List three.**
(1) Well-defined for zeros — denominator is a series-level constant, not per-observation. (2) Symmetric — no built-in preference for over or under-prediction. (3) Has a meaningful benchmark at 1.0 — MASE > 1 immediately says the naive forecast is better, which MAPE never reveals.

**Q33. Why should the MASE denominator use training-set errors, not test-set errors?**
Because the denominator is meant to characterise the *difficulty of the series*, a fixed property. Using the test set creates dependency between numerator and denominator, shifts the value with the test window, and makes MASE incomparable across horizons or evaluation periods.

**Q34. ★ Why is `r²` not the same as `R²`, and which can overstate accuracy?**
`r²` = squared Pearson correlation between y and ŷ; `R²` = `1 − SS_res/SS_tot`. They are equal *only* for in-sample OLS with an intercept. In general `r² ≥ R²`. A model predicting `2y` has r = 1.0 and looks perfect under `r²`, but R² is strongly negative. Always compute R² as `1 − SS_res/SS_tot`.

**Q35. Why is R² a bad metric for time series?**
Because R² benchmarks against the sample mean, which is a hopeless baseline for a trending/seasonal series. On our time-series example the model beat the naive forecast by 25% (MASE = 0.75) while having R² = −0.145. Use MASE or Theil's U2, which benchmark against the naive forecast.

**Q36. ★ Your training R² is 0.95 and test R² is 0.35. What happened?**
Severe overfitting. The model memorised training-specific noise. Remedies: reduce complexity (fewer features, shallower trees, stronger regularisation), verify no leakage (future data in features, target encoding on full dataset), confirm split is not time-contaminated, increase data, use cross-validation rather than one split.

**Q37. ★ What does EVS − R² tell you?**
`EVS − R² = (mean residual)² / Var(y)` — the normalised squared bias. If the gap is large, the model is systematically offset and a simple additive correction would improve performance for free. On our data the gap = 0.009, confirming bias accounts for only 0.9% of the target's variance.

**Q38. Why is R² a bad metric for comparing performance across segments?**
Because R² is normalised by the *variance of y within that segment*. A segment with narrow y-range has small SS_tot; even accurate predictions produce a low R² because the denominator is small. This makes high-price and low-price segments look incomparable when the model may actually perform equally well on both. Use MdAPE, WAPE, or MASE.

**Q39. ★ What is Huber loss and why use it?**
A loss quadratic for |e| ≤ δ and linear beyond. It gives MSE's smooth gradients near the optimum *and* MAE's bounded influence for outliers (gradient capped at ±δ). Use when data has a heavy tail or label noise but you want better convergence than pure L1. δ should be set from a high quantile of |e| or from the business cost structure.

**Q40. What is quantile (pinball) loss and what does it minimise?**
`max(τe, (τ−1)e)`. It is minimised by the conditional τ-quantile of y|x. Under-prediction is penalised τ×|e|; over-prediction (1−τ)×|e|. Setting τ = 0.9 means the model is trained to predict high enough that only 10% of actuals exceed the prediction.

**Q41. ★ How do you choose τ for inventory safety stock?**
`τ* = C_stockout / (C_stockout + C_holding)`. This is the newsvendor formula / critical fractile. If a stockout costs $500 and holding one unit costs $5, τ* = 500/505 ≈ 0.99 — forecast the 99th percentile of demand.

**Q42. ★ What is the Log-Cosh loss and when do you prefer it to Huber?**
`mean(log(cosh(e)))`. Quadratic for small |e|, linear for large. Unlike Huber it is *twice differentiable* everywhere (gradient = tanh(e), always bounded in (−1,1)). Prefer it when using a Hessian-based optimiser such as XGBoost or LightGBM, where Huber's discontinuous second derivative at |e| = δ degrades second-order split finding. Must standardise the target first — the transition point is fixed at |e| ≈ 1.

**Q43. What is Gaussian NLL and how does it relate to MSE?**
NLL = `½ln(2πσ²) + (y−μ)²/(2σ²)`. With constant σ it reduces to MSE up to a monotone transform — same model ranking. NLL adds value when σ varies with x (heteroscedastic), because it simultaneously learns calibrated uncertainty. It is minimised by reporting the true predictive distribution (a proper scoring rule).

**Q44. ★ What is CRPS and why is it preferred over NLL for reporting?**
Continuous Ranked Probability Score: `∫(F(x) − 1{x≥y})²dx`. For point forecasts it equals MAE, so it generalises MAE to probabilistic forecasts. Preferred over NLL for reporting because it is bounded (a confident wrong forecast produces a large but finite penalty, unlike NLL which diverges), is in the units of y, and is directly comparable to MAE.

**Q45. What is PICP and why must it always be paired with MPIW?**
PICP = fraction of actuals inside the predicted intervals. MPIW = mean interval width. PICP alone is trivially maximised by predicting `(−∞, +∞)`. MPIW alone is minimised by a zero-width interval. Together they describe the sharpness-coverage trade-off. For a single number, use the Interval Score.

**Q46. What is the Interval Score?**
`(U − L) + (2/α)(L − y)·1{y < L} + (2/α)(y − U)·1{y > U}`. Charges for width (always) and for the distance outside the interval (when the truth is outside). The multiplier 2/α is what makes it proper — the exact constant that prevents gaming. For a 90% interval, α = 0.10, multiplier = 20.

**Q47. ★ What is a PIT histogram? What does a U-shape mean?**
Probability Integral Transform: the histogram of `Fᵢ(yᵢ)`, the predicted CDF evaluated at the truth. Under perfect calibration it is Uniform(0,1). A U-shape means the truth lands in the distribution's tails more often than expected — the model is **over-confident** and its intervals under-cover. A hump means under-confidence (too wide). A slope means bias.

**Q48. ★ Why is shuffled K-fold cross-validation invalid for time series?**
Because it trains on observations from *after* the test period, leaking future information. And because adjacent observations are correlated, so a randomly-drawn test point always has near-neighbours in training, making the task unrealistically easy. Use `TimeSeriesSplit` with a gap.

**Q49. What is the tracking signal?**
`cumulative signed error / MAD`. A statistical process control chart for forecast bias. Random errors cancel; a persistent bias accumulates. Conventional control limits are ±4 to ±6. Breaching the limit triggers investigation. The key advantage over MPE: it detects a *small persistent* bias much faster by accumulating the evidence across periods.

**Q50. ★ What is AICc and when must you use it instead of AIC?**
Corrected AIC: `AIC + 2k(k+1)/(n−k−1)`. The correction is positive and grows as k approaches n. Use whenever `n/k < 40`. On our 10-observation, 5-parameter model the correction is 15 units, changing the selected model from 3 predictors to 1. AICc is always safe — it converges to AIC for large n.

**Q51. What does Mallows' Cp measure and what value do you seek?**
Standardised total prediction error for a subset model, in units of the full model's noise. Seek `Cp ≈ p` (the number of parameters including the intercept), indicating negligible omitted-variable bias. `Cp ≫ p` means important variables are absent.

**Q52. What is PRESS and R²_pred?**
PRESS = Leave-One-Out sum of squared errors, computed without refitting via the hat-matrix: `Σ(eᵢ/(1−hᵢᵢ))²`. `R²_pred = 1 − PRESS/SS_tot`. High in-sample R² with negative R²_pred — as on our data — is the clearest possible overfitting signal.

**Q53. ★ What is the Concordance Correlation Coefficient?**
`CCC = 2Cov(y,ŷ)/(Var(y) + Var(ŷ) + (mean(y)−mean(ŷ))²)`. Measures agreement with the 45° line, penalising both poor correlation and calibration (bias, scale mismatch). Decomposes as `r × C_b`: Pearson r times a bias-correction factor. The standard metric for instrument-comparison studies where Pearson r is insufficient.

**Q54. Why is Var(ŷ)/Var(y) a useful diagnostic?**
It measures range compression (regression to the mean). Our ratio is 0.618 — predictions span only 62% of the target's spread. The model ranks well (Spearman ρ = 1.0) but is systematically conservative: under-predicts high values, over-predicts low ones. A monotone recalibration (isotonic regression) can fix this without changing the ranking.

**Q55. What is multi-output regression's key aggregation pitfall?**
Averaging a scale-dependent metric (MSE, RMSE, MAE) across targets on different scales. The result is dominated by the highest-variance target and is numerically meaningless. Always print `multioutput='raw_values'` first, normalise per target (divide by σ), then aggregate. For R², prefer `uniform_average` over `variance_weighted` unless you explicitly want the high-variance target to dominate.

---

## 16.3 Advanced (Q56–Q80)

**Q56. ★ Derive the bias-variance decomposition of MSE at the residual level and explain how to use it.**
`MSE = E[(y − ŷ)²] = (E[y−ŷ])² + Var(y−ŷ) = Bias² + Var(e)`. On our data: Bias² = 18² = 324, Var(e) = 4300 − 324 = 3976, bias share 7.5%. Action: if bias share is large (>~25%) investigate distribution shift, wrong back-transform, or missing intercept — recalibration will help. If small (as here) the problem is unstructured scatter — needs better features or more data.

**Q57. ★ Why does minimising MAE give the median and minimising MSE give the mean?**
For MAE: the subgradient with respect to ŷ is `sign(ŷ−y)`. Setting the expected subgradient to zero requires `P(ŷ > y) = P(ŷ < y) = 0.5`, i.e. ŷ is the conditional median. For MSE: derivative is `2(ŷ−y)`, expectation = 0 gives `ŷ = E[y|x]`, the conditional mean. Consequence: an MAE-trained model on a right-skewed target will systematically under-predict the mean, so aggregate totals are biased low. Train on MSE (or Gamma/Tweedie) when totals must aggregate correctly.

**Q58. ★ Why is RMSLE asymmetric and which direction does it favour?**
`RMSLE = √mean((log1p(y) − log1p(ŷ))²)`. This measures the squared log ratio `log((1+y)/(1+ŷ))`. For a *fixed absolute error*, under-prediction (ŷ < y) gives a larger log ratio than over-prediction. Concretely: actual 1000, error 500 → under-pred log ratio 0.692, over-pred 0.405. So RMSLE penalises under-prediction more, biasing models toward over-prediction. Whether this is good depends on your cost structure.

**Q59. Why does training on `log1p(y)` produce systematic under-prediction of the mean, and how do you fix it?**
Because `exp(E[log y]) = conditional median ≠ conditional mean` for right-skewed targets (Jensen's inequality). For lognormal residuals the gap is `exp(σ²/2)`. Fix: (a) Duan smearing estimator — multiply back-transformed predictions by `mean(exp(residuals))`; (b) analytic lognormal correction `exp(μ̂ + σ̂²/2)`; (c) switch to a Gamma/Tweedie objective with log link, which models the mean directly without a back-transform at all.

**Q60. ★ Explain the four shapes of a PIT histogram and their remedies.**
Uniform → calibrated; no action. U-shaped → over-confidence, intervals too narrow → widen intervals, heavier-tailed distributional family, add epistemic uncertainty (ensembling), conformal calibration. Hump → under-confidence, intervals too wide → sharpen, reduce variance regularisation. Slope (rising) → bias, model predicts too low → debias the point forecast (offset, smearing correction, check back-transform).

**Q61. ★ Prove that the Interval Score is a proper scoring rule.**
`IS_α(L,U,y) = (U−L) + (2/α)(L−y)·1{y<L} + (2/α)(y−U)·1{y>U}`. The expected score at nominal level α, under the true distribution F, equals `(2/α)[PB_{α/2}(L,y) + PB_{1−α/2}(U,y)]` where PB is pinball loss. Pinball loss at level τ is minimised uniquely by the τ-quantile of F. So the Interval Score is minimised by setting L = F^{−1}(α/2) and U = F^{−1}(1−α/2) — the true quantiles. Any other L or U increases the expected score.

**Q62. ★ Your Spearman ρ is 0.98 but R² is 0.45. What is happening and what do you do?**
The model ranks almost perfectly but is badly miscalibrated — predictions are compressed or offset relative to the truth. The `ρ − √R²` gap is entirely a *calibration* problem, not a discrimination problem, and it is cheap to fix. Fit isotonic regression (fully flexible) or linear regression (`y ~ ŷ`) on held-out data. Because both are monotone, they leave ρ unchanged while pushing R² toward `r²` (which here is about 0.96). This is the direct regression analogue of Platt scaling in classification.

**Q63. ★ You have one observation contributing 93% of SSE. Walk through what you do.**
(1) Check the raw record for data errors (unit mix-up, decimal slip, duplicate row). (2) Check whether its feature vector is inside the training distribution — compute its leverage and Mahalanobis distance. (3) Refit without it and compare coefficients: if they change substantially, the model's conclusions rest on one row, which is a serious finding. (4) Decision: fix if error; define operating envelope and add an OOD guard if genuinely out of scope; if genuine and in scope, add features that explain it, model on a log/Gamma scale so relative error is optimised, or use Huber to bound its influence. Never delete silently.

**Q64. ★ AIC picks a 12-variable model and BIC picks a 5-variable model. What do you do?**
Check AICc first — on small n it often resolves the discrepancy toward BIC. Then let purpose decide: AIC for prediction, BIC for parsimony/explanation. Examine the 7 disputed variables: their cross-validated marginal contribution, coefficient stability across folds, and collinearity with the retained 5. Often they are correlated proxies adding little incremental signal, in which case BIC is right. Report both, and report the CV RMSE for the two candidate models, which gives the empirical answer.

**Q65. Why is R²_pred commonly negative while in-sample R² is strongly positive?**
High-leverage points. A high-leverage observation (large hᵢᵢ) bends the model to fit itself; its in-sample residual is small. But its LOO residual is `eᵢ/(1−hᵢᵢ)`, which can be enormous. For house 10 with hᵢᵢ = 0.75: LOO residual = 200/0.25 = 800. PRESS = Σ(eᵢ/(1−hᵢᵢ))² includes this 640,000 contribution, making PRESS > SS_tot, so R²_pred < 0. The model fits the training data by bending around outliers, not by learning signal.

**Q66. ★ Relate CRPS to MAE and to pinball loss.**
(1) For a *deterministic* forecast (σ→0), `CRPS = |y − ŷ| = MAE` for the average. So CRPS generalises MAE to probabilistic forecasts: a probabilistic model with CRPS < the point model's MAE is genuinely superior. (2) `CRPS = 2∫₀¹ PinballLoss_τ dτ`. CRPS is the pinball loss integrated over all quantiles — scoring the entire distribution. The weighted sum of pinball losses over a discrete set of quantiles (as used by COVID-19 Forecast Hub) is a practical approximation.

**Q67. ★ Explain aleatoric vs epistemic uncertainty and how Gaussian NLL captures (only) one.**
*Aleatoric*: irreducible noise in the data-generating process (two identical houses selling at different prices). *Epistemic*: the model's ignorance from limited data — reducible with more data. A single NLL-trained network with a σ head learns aleatoric noise: the region-specific unpredictability. It does *not* model epistemic uncertainty — it will be confidently wrong far from training data. To capture epistemic: use deep ensembles (the spread of μ across members), MC dropout, or GPs. Total predictive variance in a deep ensemble ≈ mean(σ²) (aleatoric) + Var(μ) (epistemic).

**Q68. ★ Why does BIC favour parsimony more than AIC on large n?**
BIC's penalty per parameter is `ln(n)`, which grows with n. AIC's is the constant 2. At n = 1,000, BIC charges 6.9 per parameter vs AIC's 2. Intuitively: with more data you can detect smaller true effects, so a variable must clear a higher bar to be worth retaining. BIC is consistent — with enough data it always selects the true model; AIC retains a fixed false-inclusion probability per spurious variable.

**Q69. Why does the Huber loss produce "bounded influence" and what does that mean?**
The influence of an observation on a regression estimator is proportional to its loss gradient. For MSE the gradient is `2e` — unbounded, so an observation with e = 1000 pulls 100× harder than one with e = 10. Huber's gradient is `e` inside ±δ and `δ·sign(e)` outside — *capped* at δ. So no matter how extreme the error, the observation exerts at most δ units of pull. "Bounded influence" means the breakdown point improves: a finite number of arbitrarily extreme observations cannot make the estimator arbitrarily wrong.

**Q70. What is the energy score and why does it matter for multi-output probabilistic forecasts?**
`ES = E‖X − y‖ − ½E‖X − X'‖` where X, X' are independent samples from the predictive distribution and ‖·‖ is Euclidean distance. It is the multivariate generalisation of CRPS, and it captures the *joint* predictive distribution including the correlations between targets. Per-target CRPS or NLL are blind to whether targets co-vary correctly — a forecast that gets all marginals right but predicts the wrong correlation structure (e.g. that demand for SKU A and B always peak together when they actually anti-correlate) looks fine per-target but fails the energy score.

**Q71. ★ What is conditional coverage and why is marginal coverage insufficient?**
*Marginal coverage* = the overall fraction of actuals inside the intervals (should equal the nominal level). *Conditional coverage* = for every subgroup of inputs, the fraction of actuals inside the intervals should equal the nominal level. A model can achieve marginal 90% coverage by over-covering cheap houses (110% coverage) and badly under-covering expensive ones (30% coverage), with the two averaging to 90%. Marginal PICP reports success; conditional PICP reveals the failure. Standard conformal prediction guarantees only marginal coverage. Mondrian/group-conditional conformal or conformalised quantile regression are needed for approximate conditional coverage.

**Q72. ★ Why can't you sum 90th-percentile forecasts up a product hierarchy?**
Because quantiles are not additive. `Q_0.9(A+B) ≤ Q_0.9(A) + Q_0.9(B)`, with equality only under perfect positive correlation. Intuitively: it is unlikely that A and B *both* hit their 90th percentile simultaneously — risk pooling. So summing individual 90th percentiles gives a number far more conservative than the 90th percentile of the aggregate, leading to chronic over-provisioning. Model the aggregate series directly, or simulate the joint distribution with the correlation structure and take the quantile of the simulated sums.

**Q73. How does the PIT mean and variance work as scalars for monitoring?**
For Uniform(0,1): mean = 0.5, variance = 1/12 ≈ 0.0833. Deviations from these are the compact monitoring signal. PIT mean > 0.5 → model predicts too low (truth lands high in the distribution). PIT variance > 1/12 → over-confidence (U-shape). PIT variance < 1/12 → under-confidence (hump). Both can be tracked as control charts without storing or plotting the full histogram.

**Q74. Explain the "fit ladder" diagnostic on the running example.**
Our metrics: Spearman ρ = 1.0000 → r² = 0.9248 → EVS = 0.8940 → R² = 0.8853, with Var(ŷ)/Var(y) = 0.618. Perfect ranking, compressed range, slight bias. The gap ρ=1 vs r²=0.92 means the model ranks better than it estimates (miscalibration). The gap r²=0.92 vs R²=0.885 is `Bias²/Var(y)` = the offset error. The Var ratio 0.618 is the compression: predictions span only 62% of the real range — regression to the mean, fixable with less regularisation or isotonic recalibration.

**Q75. ★ Design a production uncertainty monitoring protocol.**
Six components: (1) CRPS skill score (against climatology/naive) and NLL on a rolling window. (2) PIT mean and variance as streaming scalars — flag mean > 0.52 or variance deviating > 20% from 1/12. (3) PICP at 90% with a binomial CI — flag if outside [87%, 93%] on 200+ points. (4) Conditional coverage by key segments (price band, region, hour of day) — marginal coverage can mask segment failures. (5) OOD detection — track the feature distribution vs training (e.g. Mahalanobis distance or a classifier discriminating train vs recent data); if OOD, the uncertainty estimates are untrusted. (6) A conformal recalibration layer — if empirical coverage drifts below nominal, apply a conformity-score adjustment to restore the guarantee without retraining.

**Q76. ★ Heteroscedasticity: three consequences and three fixes.**
*Consequences*: (1) Prediction intervals built with a global σ̂ are too narrow at the high end and too wide at the low end. (2) RMSE is dominated by the high-variance region, so the model effectively ignores the low end. (3) OLS standard errors are inconsistent — inference is invalid. *Fixes*: (1) Gamma/Tweedie GLM with log link — correct variance function, models the mean directly. (2) Log-transform the target — simplest, but check the back-transform bias. (3) Quantile regression — learns region-specific spread automatically, no distributional assumption.

**Q77. ★ Your residual ACF shows a significant spike at lag 12 on monthly data. Diagnose.**
The model has not captured annual seasonality — the December residual correlates with last December's, meaning there is a repeating yearly pattern the model misses. It is probably under-predicting every December and over-predicting every February. Fixes: add monthly dummies or Fourier seasonal terms; seasonal difference (y_t − y_{t−12}); switch to SARIMA/seasonal-ETS. After the fix, recheck the ACF and re-validate with seasonal MASE (denominator = seasonal naive, period = 12). Report bias by month explicitly.

**Q78. What is the Bland-Altman plot and when do you need it?**
A plot of the *difference* (y − ŷ) vs the *mean* ((y + ŷ)/2), with horizontal lines for the mean difference (bias) and ±1.96σ limits of agreement. Used in method-comparison studies when the claim is "this new instrument agrees with the gold standard." Pearson r cannot support this claim (a factor-of-2 scale error gives r = 1). The Bland-Altman plot reveals bias, heteroscedasticity of differences, and proportional error. It is the standard clinical instrument validation plot.

**Q79. ★ Nested cross-validation: when and why?**
When you want an *unbiased estimate* of the performance of a *whole modelling pipeline including hyperparameter tuning*. If you select hyperparameters by CV and then report that model's CV score, the reported score is optimistically biased — you selected the configuration that did best on those folds. Nested CV runs an *outer* CV to estimate performance while an *inner* CV, run separately inside each outer training fold, selects hyperparameters. The outer fold's test score is never used to make any model choice and is therefore unbiased. Cost: `K_outer × K_inner` fits.

**Q80. ★ Your MASE is 0.75 — is your model definitely good?**
Not necessarily. MASE 0.75 means 25% better than the naive forecast, which on a *smooth, predictable* series is a low bar — a simple exponential smoothing might score 0.3. Check: (1) Is the comparison against *non-seasonal* naive on a *seasonal* series? If so, almost any model beats it trivially; recompute with seasonal MASE. (2) What does the horizon table look like? Average MASE of 0.75 across horizons 1–13 may hide MASE > 1 at the longer horizons. (3) Does a simple benchmark (ETS, ARIMA, last-year × trend) achieve the same? MASE is relative, not absolute — you still need to check whether a simple approach is sufficient.

---

## 16.4 Scenario-Based (Q81–Q95)

**Q81. ★ A retail team reports "92% forecast accuracy." You are sceptical. What questions do you ask?**
(1) What metric is accuracy? Likely `100 − WAPE` or `100 − MAPE` — which? They mean different things and can diverge substantially. (2) At what level? National monthly? Store-SKU daily? WAPE improves automatically when you aggregate. (3) Is the baseline stated? 92% against a naive forecast is different from 92% against a perfect forecast. (4) Is bias reported? A model can be 92% accurate and still be systematically 5% low, causing stockouts. (5) By segment? Volume-weighted metrics can be great overall while failing on a specific category. (6) What horizon? h=1 accuracy vs h=8 are different numbers.

**Q82. ★ Two models have identical MAE = 36 but one has RMSE = 36 and the other has RMSE = 65. Which do you prefer?**
Prefer the first (MAE = RMSE = 36) if cost is linear in the error — it has uniform errors and is more predictable. Prefer the second (MAE = 36, RMSE = 65) if you *only* care about the average miss and can tolerate occasional large ones. But the high RMSE/MAE ratio (1.8) of the second signals a heavy tail — investigate those large errors: are they data problems, a segment failure, or a genuine hard-to-predict regime? The choice also depends on whether large errors are catastrophic (RMSE/second is dangerous) or merely expensive but recoverable (linear cost → first is better).

**Q83. You train on RMSLE and the totals are 8% low. Why and how do you fix it?**
Training on RMSLE (equivalently, MSE on `log1p(y)`) produces predictions of the conditional *median*. For a right-skewed target the median < mean, so totals are underestimated by `exp(σ²/2) − 1` where σ² is the log-space residual variance. Fix: (a) Duan smearing — multiply by `mean(exp(residuals))`; (b) analytic lognormal correction `exp(μ̂ + σ̂²/2)`; (c) switch to a Gamma or Tweedie objective with log link, which models the conditional mean directly and has no back-transform bias. Option (c) is usually best.

**Q84. Your A/B test says Model B has lower CV RMSE but higher CV MAE than Model A. How do you decide?**
The disagreement means Model B has a worse typical error but a better tail (lower RMSE despite higher MAE → the RMSE/MAE ratio fell, i.e. fewer extreme errors). Decision depends entirely on the cost function. If cost is linear in the error: Model A (lower MAE) is better. If cost is convex (large errors disproportionately costly): Model B (lower RMSE) is better. Compute the expected cost under the actual cost function. If you don't have the cost function precisely, also look at the 90th/95th percentile of |e| for each model, which is what the reduced RMSE is reflecting.

**Q85. You have 50,000 SKU forecasts and need a single number to report to the board. What do you report?**
WAPE (volume-weighted, at the operational level) as the primary number, because the business cost scales with volume and it is immediately interpretable as "X% of total demand was mis-forecast." Add: (1) the fraction of SKUs with MASE ≥ 1 (where we should use the naive forecast), which is the action-oriented number; (2) total bias % (aggregate under/over), which determines cash flow; (3) one sentence on the worst 5 segments by WAPE. Never report a single average MAE — it is dominated by the largest SKUs and is uninterpretable.

**Q86. Your model has R² = 0.90 in-sample but R²_pred = −0.30. What do you report and do?**
Report both numbers — that gap is the most important finding. R²_pred = −0.30 means the model, when evaluated honestly out-of-sample, is *worse than the mean*. The root cause is almost certainly a small number of high-leverage observations bending the fit to itself. Steps: (1) Compute leverage and Cook's distance; the culprits will be obvious. (2) Investigate those records (data errors? genuine outliers? coverage gaps?). (3) Report the honest generalisation estimate (R²_pred = −0.30) to stakeholders alongside what it means: "the model is not yet ready for production." (4) Fix: more data, correct data errors, robust loss, log/Gamma objective to reduce leverage at the extremes.

**Q87. A competitor claims their model has MAPE = 3% and yours has MAPE = 5%. Are they better?**
Not necessarily. Check: (1) What *level* is their 3%? Day→Week→Month aggregation: a 3% monthly MAPE and 5% weekly MAPE can be the same underlying model. (2) What *series* are included? Excluding intermittent SKUs (which have terrible MAPE) massively flatters the metric. (3) Is it MAPE or WAPE? They differ when error is concentrated in certain items. (4) What is the bias? A 3% MAPE with −8% total bias is worse for inventory than 5% with 0% bias. (5) What horizon? Your 5% at h=4 may beat their 3% at h=1. Ask to see the methodology; a headline comparison without context is usually misleading.

**Q88. You deploy a probabilistic model and discover its 90% intervals have 71% empirical coverage. Diagnose systematically.**
Step 1: is the sample size large enough for the PICP to be reliable? With n = 30, the 95% CI on PICP spans ±9pp — 71% might be noise. With n = 200+, 71% is 19pp below nominal and is real. Step 2: check conditional coverage by the predicted interval width, by time, and by segment. Step 3: the three root causes — (a) under-calibrated σ: the model is over-confident, σ too small everywhere → widen via a conformal post-calibration step; (b) mis-specified family: heavy-tailed reality under a Gaussian model → switch to Student-t or use the ensemble empirical distribution; (c) distribution shift: the validation set used to fit σ is from a different regime → detect via PIT mean/variance drift and retrain or recalibrate. Apply conformal prediction as the immediate guaranteed fix while investigating the root cause.

**Q89. An executive asks why your model's R² went from 0.88 to 0.85 after adding more data. Is this bad?**
Almost certainly not. More data usually (1) reduces optimism in the in-sample fit as the model can no longer easily memorise patterns, and (2) brings in harder-to-predict observations that expand the target's natural variation. If the *cross-validated* R² also fell, investigate; if only in-sample R² fell, the model is generalising better. The more meaningful comparison is: did CV RMSE improve? If yes, the model is genuinely better. Frame it for the executive: "The model is now trained on more realistic conditions and its self-reported accuracy is more honest."

**Q90. ★ You must forecast 3-year demand for a new product with no history. What metrics apply?**
This is a cold-start / analogical forecasting problem. Standard time-series metrics are inapplicable (no training history for MASE denominator; no baseline). Evaluate instead against: (1) a range of analyst-supplied scenarios, scored ex-post once history arrives; (2) the analogical series used (similar products at launch), with MASE denominated by their naive MAE; (3) explicit uncertainty: quantile forecasts evaluated with pinball loss and coverage once the first actuals arrive. Report the forecast as a distribution, not a point, and calibrate the interval width to a reasonable confidence level based on how well the analogue cohort self-predicted at the same stage.

**Q91. Your delivery-time model has MAE = 3 minutes. The ops team says customers are unhappy with late deliveries. Diagnose.**
MAE = 3 minutes is the *average* miss, which says nothing about the direction or the tail. Compute: (1) Mean residual — is the model systematically optimistic (negative, over-predicts speed)? Even MAE = 3 with a mean residual of −8 minutes means every quoted time is 8 minutes too early. (2) Fraction late — what fraction of actual deliveries exceed the promised time? If you are quoting the median, that fraction is approximately 50%. (3) p90 of lateness — how late are the worst 10%? Customers notice the tail. (4) The quoted time is probably the mean or median prediction; replace it with a high quantile (τ = 0.85–0.90) from a pinball-trained model so the "promise kept" rate immediately improves.

**Q92. ★ You are comparing a GBM and a neural network on the same regression task. You have AIC for the GBM — can you use it to compare?**
No. AIC requires a well-defined number of parameters k. For a GBM the effective complexity depends on the number of trees, depth, learning rate, and subsampling in an interacting way — there is no clean integer k. For a neural network the same applies, plus implicit regularisation from early stopping and dropout changes the effective degrees of freedom. Use **cross-validated RMSE (or MAE/CRPS depending on your cost function)** as the comparison metric — it makes no distributional assumptions, works for any model family, and directly measures what you care about.

**Q93. Your RMSLE is 0.09 on training and 0.22 on test. What is wrong?**
A factor of 2.4× degradation suggests overfitting, a data leak, or a distribution shift. Check: (1) Is the split correct? For tabular data with a date column, check that no test-period information leaked into features (rolling statistics, target-encoded groups). (2) Does the train/test split stratify by outcome? A split that puts all the large-valued (hard-to-predict) houses in test will inflate test RMSLE. (3) Are there any outliers in test that were not in training? One house at $8M in test with no comparable training data would dominate. (4) Is the RMSLE computed the same way? Check for a log-base mismatch (ln vs log₁₀ differ by 2.3×). Fix: use a proper walk-forward CV; apply data-cleaning checks to both train and test; report the full CV distribution, not just the mean.

**Q94. You need a single "forecast accuracy" number for a press release. What do you use?**
WAPE reported as `100 − WAPE = X% accuracy`, at the aggregate (national/monthly) level. This is the industry convention (supply chain), immediately interpretable ("we forecast demand within X% of actual"), avoids MAPE's zero problem, and is volume-weighted so it tracks business impact. Supplement internally (never in a press release) with bias and the level-at-which-it-was-computed, so the number is not gameable by further aggregation.

**Q95. ★ You have a model with CRPS = 1.01 and a deterministic model with MAE = 1.20. Can you say the probabilistic model is better?**
Yes — directly. Because CRPS reduces to MAE for deterministic forecasts, the units are identical. CRPS = 1.01 < MAE = 1.20 means the probabilistic model outperforms the deterministic one on the same scale. This is CRPS's unique practical value: it is the only proper scoring rule in the target's units that degenerates to MAE, enabling a direct comparison between probabilistic and deterministic forecasters on a single axis.

---

## 16.5 Coding (Q96–Q105)

**Q96. ★ Implement MAE, RMSE, MAPE, and WAPE in pure NumPy.**
```python
import numpy as np

def mae(y, yhat):   return np.abs(y - yhat).mean()
def rmse(y, yhat):  return np.sqrt(((y - yhat)**2).mean())
def mape(y, yhat):  
    m = y != 0
    return np.abs((y[m] - yhat[m]) / y[m]).mean() * 100
def wape(y, yhat):  return np.abs(y - yhat).sum() / np.abs(y).sum() * 100
```

**Q97. ★ Implement MASE with training-set denominator, handling seasonality.**
```python
def mase(y_test, y_pred, y_train, s=1):
    naive = np.abs(y_train[s:] - y_train[:-s]).mean()
    return np.nan if naive == 0 else np.abs(y_test - y_pred).mean() / naive
```

**Q98. Implement the Gaussian CRPS closed form.**
```python
from scipy.stats import norm
def crps_gaussian(y, mu, sigma):
    sigma = np.maximum(sigma, 1e-12)
    z = (y - mu) / sigma
    return np.mean(sigma * (z*(2*norm.cdf(z)-1) + 2*norm.pdf(z) - 1/np.sqrt(np.pi)))
```

**Q99. ★ Why does sklearn's `mean_absolute_percentage_error` not return a percentage?**
It returns a *fraction* (e.g. 0.0657 for 6.57%). Multiply by 100 to get the percentage. The `neg_mean_absolute_percentage_error` scorer in GridSearchCV also operates on the fraction. Forgetting to multiply is one of the most common bugs in regression pipelines.

**Q100. ★ Write a pipeline that correctly computes CV RMSE for a regression model including preprocessing.**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
import numpy as np

pipe = Pipeline([('scaler', StandardScaler()), ('model', GradientBoostingRegressor())])
scores = -cross_val_score(pipe, X, y, cv=TimeSeriesSplit(5),
                          scoring='neg_root_mean_squared_error')
print(f"CV RMSE = {scores.mean():.3f} ± {scores.std():.3f}")
```
Key: preprocessing is *inside* the Pipeline, so the scaler is fit only on training folds. `TimeSeriesSplit` prevents future leakage. The `neg_` prefix is negated back.

**Q101. Implement the Durbin-Watson statistic.**
```python
def durbin_watson(e):
    return np.sum(np.diff(e)**2) / np.sum(e**2)
# ~2 = no autocorrelation; <1.5 = positive; >2.5 = negative
```

**Q102. Implement the Interval Score (Winkler score) for a 90% interval.**
```python
def interval_score(y, lower, upper, alpha=0.10):
    width = upper - lower
    under = (2/alpha) * np.clip(lower - y, 0, None)
    over  = (2/alpha) * np.clip(y - upper, 0, None)
    return np.mean(width + under + over)
```

**Q103. ★ Implement the bias-variance decomposition of MSE.**
```python
def mse_decompose(y, yhat):
    e = y - yhat
    bias2 = e.mean()**2
    var_e = e.var()
    mse   = (e**2).mean()
    assert abs(bias2 + var_e - mse) < 1e-9
    return {'mse': mse, 'bias2': bias2, 'var_e': var_e,
            'bias_pct': 100*bias2/mse, 'var_pct': 100*var_e/mse}
```

**Q104. Implement the tracking signal with a breach alert.**
```python
def tracking_signal(y, yhat, limit=4.0):
    e = y - yhat
    cum = np.cumsum(e)
    mad = np.cumsum(np.abs(e)) / np.arange(1, len(e)+1)
    ts  = np.where(mad > 0, cum/mad, 0.0)
    breaches = np.where(np.abs(ts) > limit)[0]
    return ts, breaches
```

**Q105. Implement adjusted R².**
```python
def adjusted_r2(y, yhat, n_features):
    n = len(y); r2 = 1 - ((y-yhat)**2).sum() / ((y-y.mean())**2).sum()
    denom = n - n_features - 1
    return np.nan if denom <= 0 else 1 - (1 - r2)*(n-1)/denom
```

---

## 16.6 Research and Theory (Q106–Q113)

**Q106. ★ What is a proper scoring rule and which regression metrics are proper?**
A scoring rule S(F, y) is *proper* if the expected score is minimised when F equals the true predictive distribution P: `E_P[S(F,y)] ≥ E_P[S(P,y)]` for all F. Proper rules cannot be improved by misreporting uncertainty. Among regression metrics: **Gaussian NLL**, **CRPS**, **Pinball loss**, and **Interval Score** are proper. PICP, MPIW, MAE, RMSE, and R² are *not* proper (they can be improved by misreporting the distribution).

**Q107. What is the Gauss-Markov theorem and what does it say about OLS?**
Among all *linear unbiased estimators*, OLS is the one with minimum variance — it is BLUE (Best Linear Unbiased Estimator). The assumptions: linear model, exogenous regressors, homoscedasticity, no autocorrelation. Notably, normality is *not* required. What it does *not* say: OLS is optimal among all estimators (ML under Gaussian errors is), or that it is good when the assumptions are violated.

**Q108. ★ What is the bias-variance trade-off for the model (not the residuals) and how do metrics expose it?**
The expected prediction error decomposes as `Bias²[model] + Variance[model] + irreducible noise`. A simple model (high bias, low variance) makes systematic errors but is consistent across datasets; a complex model (low bias, high variance) fits training data well but generalises poorly. Metrics expose it via: **training vs CV score gap** (large gap = high model variance = overfitting); **R²_pred vs in-sample R²** gap; **Adj R² vs R²** gap. The residual-level `MSE = Bias² + Var(e)` decomposition is a different thing — it is about the *prediction* of the current model, not about the model family's generalisation behaviour.

**Q109. What is the connection between AIC and LOO cross-validation?**
For Gaussian linear models with known σ², `AIC ≈ −2 × (LOO log-predictive density)` asymptotically. For exponential-family GLMs: AIC is asymptotically equivalent to LOO cross-validation evaluated by log-predictive density. Practical implication: AIC estimates the same thing as LOO-CV but without requiring re-fitting. When they disagree materially, it usually means the asymptotic approximation is poor (small n or heavy-tailed errors), and you should trust CV.

**Q110. Why is the Ljung-Box test preferred over Box-Pierce?**
Both test whether k autocorrelations are jointly zero: `Q = n(n+2)Σₕ ρ̂ₕ²/(n−h)` (Ljung-Box) vs `n·Σρ̂ₕ²` (Box-Pierce). The Ljung-Box correction factor `(n+2)/(n−h)` down-weights higher lags, making the statistic better approximated by a chi-squared on finite samples. Box-Pierce over-rejects (too many false positives) on short series, especially at higher lags.

**Q111. What is the Continuous Ranked Probability Score's relationship to the energy score for multivariate forecasts?**
CRPS is a special case of the energy score `ES(F,y) = E‖X−y‖ − ½E‖X−X'‖` when the norm is the absolute value (m=1 target). For m > 1 targets, the energy score extends CRPS to jointly evaluate the predictive distribution, penalising not just marginal inaccuracy but also incorrect dependence structure. The variogram score is an alternative that is more sensitive to dependence but less sensitive to location errors.

**Q112. ★ What is the variance of a Uniform(0,1) random variable and why is it the PIT target?**
`Var[Uniform(0,1)] = 1/12 ≈ 0.0833`. This is the expected variance of the PIT values under a perfectly calibrated model, because `F̂(y) ~ Uniform(0,1)` when F̂ = true CDF. Monitoring the sample variance of PIT values against 1/12 gives a scalar calibration diagnostic: values above 1/12 indicate over-confidence (U-shaped histogram), below indicate under-confidence (hump-shaped).

**Q113. What is conformal prediction and what guarantee does it provide?**
A distribution-free framework that wraps any regression model to produce prediction intervals with a *finite-sample marginal coverage guarantee*: `P(y_{n+1} ∈ Î_{n+1}) ≥ 1 − α`, exactly, without any distributional assumption, for any exchangeable data. Implementation: split the data into training and calibration. Compute conformity scores `s_i = |y_i − ŷ_i|` on calibration. The prediction interval for a new point is `ŷ_{n+1} ± q̂_{1−α}` where `q̂_{1−α}` is the `⌈(1−α)(n_cal+1)⌉/n_cal` quantile of calibration scores. The guarantee is *marginal*, not conditional — Mondrian conformal extends to group-conditional guarantees.

---

## 16.7 Business and Communication (Q114–Q123)

**Q114. ★ How do you explain R² to a non-technical stakeholder?**
"Before our model, if you had to guess every house's price using just one number — the average — you would be off by roughly $193k on average. Our model reduces that error to about $66k. R² = 0.885 means we explained 88.5% of the variation that was there to be explained. The remaining 11.5% is genuine unpredictability — no model can remove it."

**Q115. How do you report forecast accuracy for a supply-chain executive review?**
One primary number: "Our forecast accuracy is X% [= 100 − WAPE at the store-SKU-week level]." Then: "Bias: the total forecast is Y% [above/below] actual — [action we are taking]." Then the three things an executive wants to know: "What improved? What worsened? What are the top 5 SKUs/regions driving performance?" Avoid MAE (not interpretable without context), avoid averaged MAPE (gameable by aggregating), and always state the level.

**Q116. A data scientist proposes switching from RMSE to MAE as the primary metric. What questions do you ask?**
(1) Does our cost function actually change from quadratic to linear? If large errors are still disproportionately costly, RMSE is the right loss. (2) Do we have an outlier problem? If so, Huber or MedAE may be better than simply switching to MAE. (3) Do we need the aggregate/total to be right? MAE targets the median; if totals matter, MSE/RMSE is necessary. (4) What is the training loss? If we report MAE but still train on MSE, we are measuring one thing and optimising another. (5) Has the model been tested with an L1 training objective? Switching only the metric without the loss may not change the model at all.

**Q117. ★ How do you justify a 90% prediction interval to a business stakeholder?**
"Our delivery time estimate comes with a range: [lower, upper]. This means that based on our historical data, about 9 out of 10 deliveries will arrive within that window. We specifically chose 90% rather than showing the average, because if we showed you the average you would be late half the time — and late deliveries cost customer trust. The 10% of deliveries that still fall outside are on the tails of the distribution, which we also monitor separately."

**Q118. Your model has WAPE = 12% but the competitor claims 8%. How do you evaluate that claim?**
Ask for methodology: (1) What aggregation level? Their 8% may be national-monthly vs our 12% at store-SKU-weekly. (2) Which SKUs are included? Excluding intermittent/new items can cut MAPE/WAPE by half. (3) Is it WAPE or MAPE? Different answers when errors concentrate differently. (4) What baseline does it beat? 8% might be achievable by a naive model on their product mix. (5) What is the bias? 8% WAPE with −6% total bias is operationally worse for inventory than 12% with 0% bias. Request a head-to-head comparison on your exact data, with your exact metric definition, at your level.

**Q119. You need to communicate model uncertainty to a patient's family in a clinical setting.**
Avoid technical language. Say: "Our model estimates [value] for [measure]. Based on patients with similar profiles, we expect the true value to fall between [lower] and [upper] about 9 times out of 10. This range accounts for the natural variation we see across patients." Do not quote CRPS, PICP, or NLL. Do quote the interval width and the coverage fraction in plain language. And add: "This is a supporting tool for the clinical team — the doctor will interpret this alongside the full clinical picture."

**Q120. ★ The board wants to know if the model justifies its implementation cost. What metrics do you present?**
Frame it as a business case: (1) **Baseline**: what does the current process produce? (Naive forecast, human expert, previous model.) (2) **Improvement**: `ΔMAE` or `ΔWAPE` (use the metric that maps to cost). (3) **Translate to money**: if MAE drops from 150 to 36 units per week and each misforecast unit costs $X, the annual saving is `114 × weeks × units × $X`. (4) **Total cost**: model development, compute, monitoring. (5) **R²_pred or CV score** to confirm it generalises. (6) **Payback period**. Present the range of outcomes (the fold-to-fold CV spread) so the board is not surprised if performance varies.

**Q121. When is a model with R² = 0.02 valuable?**
In quantitative finance. Asset return prediction is near-random — markets are efficient. A signal with IC (cross-sectional rank correlation) of 0.04 — roughly equivalent to an R² of 0.02 on returns — can support a profitable strategy if it is consistent, has low turnover, and survives transaction costs. The lesson: R² must be benchmarked against the *achievable ceiling* for the domain, which in returns is close to zero. A 0.02 R² that beats the information set's theoretical ceiling is enormously valuable; a 0.95 R² in a domain where 0.99 is achievable is mediocre.

**Q122. ★ How do you detect whether a forecast is being gamed (someone is picking the metric definition to get the best number)?**
Three checks: (1) Ask for the metric at *multiple aggregation levels*. If MAPE at national-monthly is 4% but WAPE at store-SKU-weekly is 40%, someone has chosen the most favourable level. (2) Ask for it *with and without* new products and intermittent SKUs. Excluding them halves the apparent difficulty. (3) Compute the naive or seasonal-naive baseline on exactly the same data, same level, same SKU set. If the model barely beats it, the metric is not informative. (4) Ask for the total bias alongside accuracy. A 4% MAPE with a −10% total bias is operationally disastrous; reporting only MAPE hides it.

**Q123. ★ A stakeholder says "our model is 94% accurate." What do you ask?**
(1) What is the metric? "Accuracy" in regression is usually `100 − MAPE` or `100 − WAPE` — which? (2) At what level and over what period? (3) Compared to what baseline? "The naive forecast is 91% accurate" would make 94% much less impressive. (4) Is bias included? A model can be "94% accurate" and systematically 8% low. (5) Is 94% good for this domain? Store-SKU-day level should be compared to what a similar retailer achieves, not to an abstract benchmark. (6) What is the uncertainty on that estimate? With a small test set, 94% ± 5% is the honest statement.

---

# PART 17 — Cheat Sheet

## 17.1 One-page ASCII summary

```
THE REGRESSION EVALUATION CHEAT SHEET
======================================

FOUR THINGS TO ALWAYS REPORT
────────────────────────────
1. MAGNITUDE    MAE or RMSE (or both + their ratio)
2. SIGNED BIAS  mean residual  or  MPE  or  total bias %
3. RELATIVE     MAPE/WAPE for communication; MASE/R² for comparison
4. RESIDUAL PLOT: always look at the residuals before deciding anything

THE DIAGNOSTIC RATIO
────────────────────
RMSE/MAE   ≈ 1.0    uniform errors
           ≈ 1.25   normal errors (exactly √(π/2) = 1.253)
           > 1.5    heavy tail — investigate the worst cases
           > 2.5    severe outliers — RMSE is essentially reporting a few rows

SCALE LADDER (our 10-house example)
────────────────────────────────────
Spearman ρ  = 1.000   ← perfect ranking
Pearson  r  = 0.962
    r²      = 0.925   ← miscalibration gap (r² > R² means mis-scaled)
    EVS     = 0.894   ← bias gap (EVS − R² = Bias²/Var(y) = 0.009)
    R²      = 0.885   ← actual predictive accuracy
    Adj R²  = 0.828   ← R² penalised for 3 predictors on 10 rows
Var(ŷ)/Var(y) = 0.618   ← RANGE COMPRESSED: fix with isotonic/linear recalibration

ASYMMETRIC LOSS FORMULA
───────────────────────
τ* = C_under / (C_under + C_over)       <- the newsvendor critical fractile
Example: stockout $500, holding $5 → τ* = 0.990 → forecast the 99th percentile

WHICH METRIC — 30-SECOND RULE
──────────────────────────────
Cost linear, symmetric       → MAE (train L1/Huber)
Cost convex, symmetric       → RMSE (train MSE)
Cost ASYMMETRIC              → Pinball at τ* (NEVER use a symmetric metric)
Target positive, skewed      → RMSLE or Gamma/Tweedie objective
Intermittent / zeros         → MASE (not MAPE)
Cross-series comparison      → MASE or WAPE (not raw MAE)
Time series                  → MASE, NOT R²
Model selection              → Cross-validated score + AICc
Probabilistic output         → CRPS headline, NLL for training
Communication                → WAPE / MdAPE / PICP + MPIW
```

---

## 17.2 Complete formula sheet

**Absolute error family**
```
MAE       = (1/n) Σ|yᵢ − ŷᵢ|
MedAE     = median(|yᵢ − ŷᵢ|)
Max Error = max(|yᵢ − ŷᵢ|)
MAD       = median(|xᵢ − median(x)|)   [robust spread, not a model metric]
```

**Squared error family**
```
SSE = RSS = Σ(yᵢ − ŷᵢ)²
MSE       = (1/n) Σ(yᵢ − ŷᵢ)²  = SSE/n
RMSE      = √MSE
RSE (residual std error) = √(SSE/(n−p−1))    [for inference, not reporting]
MSE = Bias² + Var(e)               [decomposition: always compute it]
RMSE² = MAE² + Var(|e|)            [exact; gap is the tail measure]
```

**Percentage family**
```
MAPE      = (100/n) Σ |eᵢ/yᵢ|          [undefined at 0; biases low]
sMAPE     = (100/n) Σ |eᵢ|/((|yᵢ|+|ŷᵢ|)/2)   [range 0–200; biases high]
WAPE      = 100 × Σ|eᵢ|/Σ|yᵢ| = 100 × MAE/mean(|y|)
MdAPE     = 100 × median(|eᵢ/yᵢ|)
PE10      = 100 × mean(|eᵢ/yᵢ| < 0.10)
MPE       = (100/n) Σ (eᵢ/yᵢ)           [signed; target = 0; ALWAYS REPORT]
total bias = 100 × Σeᵢ/Σyᵢ              [aggregate version; often more useful]
```

**Scaled family**
```
RAE       = Σ|eᵢ| / Σ|yᵢ − ȳ|         [= MAE/MAE_mean_baseline]
RSE       = Σeᵢ² / Σ(yᵢ−ȳ)²            [= 1 − R²]
RRSE      = √RSE = RMSE/σ(y)
MASE      = MAE_test / MAE_naive_insample   [anchor at 1 = naive]
             seasonal: denominator uses s-step differences
Theil U2  = RMSE_model / RMSE_naive
```

**Log family**
```
MSLE      = (1/n) Σ [ln(1+yᵢ) − ln(1+ŷᵢ)]²
RMSLE     = √MSLE         [≈ MAPE when errors small; exp(RMSLE)−1 = rel. error]
MdSA      = 100 × (exp(median|ln(ŷ/y)|) − 1)    [symmetric; needs y,ŷ > 0]
SSPB      = 100 × sign(M) × (exp|M| − 1),   M = median(ln(ŷ/y))   [signed bias]
Back-transform bias: log model underpredicts mean by factor exp(σ²/2)
```

**Goodness of fit**
```
R²        = 1 − Σeᵢ²/Σ(yᵢ−ȳ)² = 1−RSE             [range (−∞,1]; lower unbounded]
Adj R²    = 1 − (1−R²)(n−1)/(n−p−1)
EVS       = 1 − Var(e)/Var(y)                         [EVS − R² = Bias²/Var(y)]
r         = Cov(y,ŷ)/(σ_y σ_ŷ)   [Pearson; r² = R² only for in-sample OLS]
ρ         = r on rank(y), rank(ŷ)  [Spearman; robust]
CCC       = 2Cov / (Var(y)+Var(ŷ)+(ȳ−ŷ̄)²)  = r × C_b
```

**Robust and asymmetric losses**
```
Huber_δ(e)     = ½e²           if |e| ≤ δ
               = δ(|e|−½δ)     if |e| > δ
Log-Cosh(e)    = ln(cosh(e))  ≈ ½e² (small) ≈ |e|−ln2 (large)   [grad = tanh(e)]
Pinball_τ(e)   = max(τe, (τ−1)e)            [minimises conditional quantile τ]
ε-insensitive  = max(0, |e|−ε)
τ* (newsvendor) = C_under / (C_under + C_over)
```

**Probabilistic**
```
NLL (Gaussian)  = ½ln(2πσ²) + (y−μ)²/(2σ²)          [proper; unbounded]
CRPS (Gaussian) = σ[z(2Φ(z)−1) + 2φ(z) − 1/√π],  z=(y−μ)/σ  [proper; in y units]
CRPS (ensemble) = E|X−y| − ½E|X−X'|               [energy form]
CRPS = 2∫₀¹ PinballLoss_τ dτ                        [fundamental identity]
CRPS(deterministic) = MAE                           [use to compare point vs prob]
PICP    = mean(1{Lᵢ ≤ yᵢ ≤ Uᵢ})            [target = nominal level]
MPIW    = mean(Uᵢ − Lᵢ)                    [lower better, conditional on coverage]
IS_α    = (U−L) + (2/α)(L−y)·1{y<L} + (2/α)(y−U)·1{y>U}   [proper; exceedance ×2/α]
IS_α    = (2/α)[Pinball_{α/2}(L,y) + Pinball_{1−α/2}(U,y)]  [equivalence]
PIT pᵢ  = F̂ᵢ(yᵢ)   ~Uniform(0,1) if calibrated   [mean=0.5, var=1/12]
```

**Model selection**
```
AIC  = 2k − 2lnL̂         [k = params incl. intercept and σ²; ≈ LOO-CV]
AICc = AIC + 2k(k+1)/(n−k−1)    [use whenever n/k < 40]
BIC  = k·ln(n) − 2lnL̂   [stricter; consistent; favours parsimony]
Akaike weights: wᵢ = exp(−ΔAICᵢ/2) / Σ exp(−ΔAICⱼ/2)
Cp   = RSSp/σ̂²_full − n + 2p   [seek Cp ≈ p; σ̂² from the full model]
PRESS= Σ(eᵢ/(1−hᵢᵢ))²           [LOO SSE; no refitting for linear models]
R²_pred = 1 − PRESS/SS_tot       [negative = worse than the mean]
```

**Diagnostics**
```
Durbin-Watson   = Σ(eₜ−eₜ₋₁)² / Σeₜ²    [≈2 good; <1.5 pos autocorr]
Cook's D        = eᵢ²/(k·σ̂²) × hᵢᵢ/(1−hᵢᵢ)²   [>4/n: screen; >1: serious]
Leverage        = hᵢᵢ = diagonal of H = X(XᵀX)⁻¹Xᵀ    [>2k/n: investigate]
Tracking signal = cumulative Σeₜ / MAD    [limits ±4 to ±6]
```

---

## 17.3 Mnemonics

**The four things to always report:**
> **MSBR** — **M**agnitude · **S**igned bias · **B**aseline-relative · **R**esidual plot

**MAE vs MSE optimal predictor:**
> **MAE → Median, MSE → Mean** — same first letter.

**RMSE ≥ MAE — the gap formula:**
> `RMSE² = MAE² + Var(|e|)` — "**RMSE squared equals MAE squared plus the error's own variance**." The gap is entirely the variability of the error sizes.

**MAPE directions:**
> "**MAPE Misses Actual Too Easily**" — it Penalises over-forecast Massively, so models shade low. Alternatively: "MAPE biases low → stockouts."

**sMAPE asymmetry direction:**
> "**sMAPE biases HIGH**" — the opposite of MAPE. Reversed because ŷ is now in the denominator too.

**RMSLE asymmetry:**
> "**RMSLE penalises Under**" — Under-prediction has the bigger log ratio in absolute terms. Models trained on RMSLE over-predict.

**Log-Cosh degenerate check:**
> `Log-Cosh = MAE − ln2` when every |e| ≫ 1 — if you see this, the target is not standardised.

**Back-transform bias:**
> `exp(E[log y]) < E[y]` always (Jensen). "**Exponentiated mean ≠ mean of exponents.**" The correction factor is `exp(σ²/2)`.

**MASE anchor:**
> "**1 = naive, under 1 is good, over 1 means go home.**"

**Quantile from costs:**
> "**τ = Under / (Under + Over)**" — the newsvendor fractile.

**PIT shapes:**
> "**U for Under-cover** (over-confident) · **Hump for Heavy intervals** (under-confident) · **Slope for Skewed predictions** (bias)"

**AIC vs BIC:**
> "**AIC = 2k; BIC = k log n.**" For n > 7, BIC is stricter. "**AIC for pAths, BIC for Bottom-line parsimony.**"

**AICc rule:**
> "**n/k < 40 → use AICc, not AIC.**" With our 10 obs / 5 params = 2, the correction was 15 units.

**The r² vs R² trap:**
> "**r² is rank; R² is real.**" Pearson r measures rank-like linear association, which is scale-invariant; R² = 1−SS_res/SS_tot measures actual accuracy including calibration.

**CCC decomposition:**
> `CCC = r × C_b` — "**Precision times Accuracy**" — the same words used in classification but for agreement.

**CRPS degenerates to MAE:**
> "**CRPS collapses to MAE for a point forecast**" — the single most useful comparison property.

**The five residual-plot patterns:**
> **CFBDS** — **C**lean (healthy) · **F**unnel (heteroscedasticity) · **B**end/curve (nonlinearity) · **D**rift (bias/shift) · **S**tripes (discrete target)

---

## 17.4 Common pitfalls — numbered list

1. **Reporting MAE without units.** "MAE = 36" is meaningless; "$36k" is a result.
2. **Reporting RMSE without MAE.** Their ratio is a free tail diagnostic.
3. **Not reporting a signed bias metric.** The single most common regression evaluation error.
4. **Comparing MAE/RMSE across series of different scale.** Use MASE or WAPE.
5. **Using MAPE on data containing zeros.** Silent undefined results or absurd values.
6. **Optimising MAPE and not noticing the systematic downward bias** in forecasts.
7. **Using non-seasonal MASE on seasonal data.** Beating "tomorrow = today" on December retail is trivial.
8. **Computing MASE with test-set denominator** instead of training-set denominator.
9. **Aggregating 90th-percentile forecasts up a hierarchy.** Quantiles do not add up.
10. **Reporting R² on time series.** Benchmarks against the mean; use MASE or Theil's U2.
11. **Comparing R² across segments with different target variance.** A narrow-range segment will always show lower R² even if the model is equally accurate.
12. **Using in-sample R² for model selection.** Always increases with more features. Use CV or AICc.
13. **Not checking R²_pred or CV R².** In-sample 0.88, out-of-sample −0.72 on our data — a completely meaningless in-sample fit.
14. **Reporting `r²` as `R²`.** They are only equal for in-sample OLS with an intercept. `r² ≥ R²` always.
15. **The ×100 bug with sklearn's MAPE.** Returns a fraction; multiply by 100.
16. **Shuffled K-fold on time-series data.** Leaks the future; produces wildly optimistic scores.
17. **Preprocessing outside the Pipeline in cross-validation.** Scaler/imputer/target encoder fitted on all data → silent, severe data leak.
18. **Reporting only the best CV score from a hyperparameter search** — selection bias; use nested CV or an untouched test set.
19. **Not reporting fold-to-fold spread.** `RMSE = 65 ± 30` is very different from `65 ± 3`.
20. **Using AIC when n/k < 40 instead of AICc.** AIC is biased for small samples; the correction can change the selected model.
21. **Applying AIC/BIC to tree ensembles or neural networks.** No valid parameter count k.
22. **Not clamping σ in Gaussian NLL training.** σ → 0 makes the loss diverge; always clamp or predict log σ.
23. **Passing σ where σ² is expected** in `torch.nn.GaussianNLLLoss`. A very common silent bug.
24. **Reporting PICP without MPIW.** PICP = 100% for infinite intervals — useless alone.
25. **Reporting only marginal coverage.** A model can hit nominal coverage overall while systematically failing in a segment. Always check conditional coverage.
26. **Log-transforming the target without a smearing correction.** Training on `log1p(y)` and predicting `expm1(ŷ)` gives the conditional median, not the mean — totals are systematically low.
27. **Using RMSLE on negative targets.** `log1p` of a value ≤ −1 is undefined.
28. **Using RMSLE on small counts (0–5).** The +1 shift dominates; use Poisson deviance instead.
29. **Interpreting Log-Cosh on a large-valued target.** It degenerates to MAE when all |e| ≫ 1.
30. **Setting Huber δ above the maximum absolute error.** This is pure MSE with no robustification.
31. **Reporting the Huber or Log-Cosh loss value as a performance metric.** Mixed units; not interpretable.
32. **Choosing τ for quantile regression arbitrarily** instead of deriving it from the cost ratio.
33. **Deleting an influential observation without documenting why** and checking whether it is a data error.
34. **Comparing AICs from different software.** Absolute values are convention-dependent.
35. **Comparing AIC across models fitted on different sample sizes.**
36. **Comparing AIC across different target transformations** (raw y vs log y) without a Jacobian correction.
37. **Using MPE ≈ 0 as evidence of a good model.** Positive and negative biases can cancel.
38. **Not segmenting bias.** +15% in one region and −15% in another gives aggregate 0% — two problems, not zero.
39. **Not resetting the tracking signal after a corrective action.**
40. **Comparing CRPS/NLL values across datasets or after target transformations.** Use skill scores.
41. **Confusing MedAE with MAD.** MedAE scores a model; MAD estimates the spread of a variable for outlier detection.
42. **Assuming Max Error is comparable across test sets of different sizes.** Use the 99th percentile of |e| instead.
43. **Not computing the bias-variance decomposition of MSE.** A free, actionable diagnostic.
44. **Averaging MSE/RMSE/MAE across targets in multi-output regression.** Dominated by the highest-variance target; meaningless if units differ.
45. **Not checking Var(ŷ)/Var(y).** Range compression (< 1) is a very common and fixable defect that no scalar metric surfaces.
46. **Reporting only MedAE on a problem where the tail carries the risk** (insurance, safety). MedAE ignores everything above the median.
47. **Using a single train/test cut for time series evaluation** instead of multiple forecast origins.
48. **Not computing the metric at the decision level.** National-monthly WAPE is irrelevant if replenishment is store-SKU-daily.
49. **Treating a good CRPS as proof of good conditional calibration.** Always produce the PIT histogram and segment-level coverage.
50. **Using naive log-space interpretation of RMSLE.** `exp(RMSLE) − 1` is the approximate relative error; state it explicitly — "RMSLE = 0.093 ≈ 9.8% typical relative error."

---

## 17.5 Pre-deployment regression model checklist

```
POINT ACCURACY
[ ] MAE and RMSE reported (and their ratio — is the tail heavy?)
[ ] MedAE reported if RMSE/MAE > 1.5 (tail present)
[ ] Max Error / 95th / 99th percentile of |e| — what is the worst case?
[ ] All of the above at the OPERATIONAL level (where decisions are made)

BIAS (never omit)
[ ] Mean residual in target units
[ ] Total bias % = Σe/Σy
[ ] MPE per observation
[ ] All three by key segments (region, price band, category, time period)
[ ] Confirmed: there is no back-transform bias (log model → smearing correction applied)

RELATIVE/SCALED METRIC
[ ] MASE with correct seasonality and training-set denominator (time series)
[ ] WAPE at the decision level (cross-series comparison)
[ ] R² or RMSLE for cross-dataset communication (with the appropriate caveats)

UNCERTAINTY (if the output drives a stochastic decision)
[ ] A probabilistic model producing (μ, σ) or multiple quantiles
[ ] CRPS skill score (compared to climatological or naive distribution)
[ ] PICP at 80/90/95% with a binomial CI on each
[ ] Conditional coverage by the key segments (not just marginal)
[ ] MPIW at each level (conditional on coverage being adequate)
[ ] PIT histogram with mean and variance annotation
[ ] Conformal calibration layer applied if guaranteed coverage is required

MODEL SELECTION
[ ] Cross-validated score (appropriate splitter: TimeSeriesSplit / GroupKFold / KFold)
[ ] Fold-to-fold spread reported alongside the mean
[ ] AICc (not AIC) for classical models if n/k < 40
[ ] In-sample R² explicitly NOT used for selection
[ ] Final reported score from an untouched test set or nested CV

RESIDUAL DIAGNOSTICS
[ ] Predicted-vs-actual plot (range compression visible?)
[ ] Residuals-vs-fitted (funnel = heteroscedasticity; curve = missing nonlinearity)
[ ] Q-Q plot (heavy tails will under-cover Gaussian intervals)
[ ] Residuals-vs-time (autocorrelation → left-over signal)
[ ] Top 10 worst residuals inspected and explained
[ ] Leverage and Cook's D: no single observation controls the fit

OPERATIONAL READINESS
[ ] OOD detection mechanism: flag inputs outside the training distribution
[ ] Monitoring plan: MAE/RMSE + total bias + (if probabilistic) PIT mean/variance,
    all tracked on a rolling window with control limits
[ ] Tracking signal per series (for forecast systems)
[ ] Documented decision for any influential observation removed or kept
[ ] Back-transform logic verified (no silent underestimation of the mean)
[ ] Bias correction applied if the mean residual is systematically non-zero
[ ] Operating envelope defined: the feature ranges within which guarantees hold

COMMUNICATION
[ ] Metric reported with units and at the decision level
[ ] A baseline (naive, previous model) shown alongside
[ ] Uncertainty communicated as an interval, not just a point, wherever possible
[ ] Stakeholder-facing summary follows the MSBR rule:
      Magnitude · Signed bias · Baseline-relative · Residual evidence
```

---

# APPENDIX A — Full Running-Example Table

All 35+ metrics on the identical 10-house dataset. Every number verified against scikit-learn and scipy.

```
y    = [200, 250, 300, 350, 400, 450, 500, 550, 600, 900]
ŷ    = [220, 240, 310, 330, 420, 430, 520, 530, 620, 700]
e    = [-20, +10, -10, +20, -20, +20, -20, +20, -20, +200]
n=10,  ȳ=450,  Var(y)=37500,  σ(y)=193.65
```

| Metric | Value | Notes |
|---|---|---|
| **MAE** | **36.000** | Σ\|e\|=360; 56% from house 10 |
| MedAE | 20.000 | 5th+6th abs errors / 2 |
| Max Error | 200.000 | house 10 |
| MAE/MedAE ratio | 1.800 | Moderate heavy tail |
| **MSE** | **4,300.0** | Bias²=324 + Var(e)=3,976 |
| **RMSE** | **65.574** | RMSE/MAE = 1.822 |
| RMSE/σ(y) (= RRSE) | 0.339 | |
| Residual sum | +180 | Under-predictions dominate |
| **Mean residual (bias)** | **+18.0** | Model under-predicts on average |
| Median residual | 0.0 | Bias is tail-driven, not median-level |
| Bias²/Var(y) | 0.0086 | 0.86% of target variance |
| **MAPE** | **6.568%** | sklearn returns fraction 0.0657; ×100 for % |
| sMAPE | 6.809% | M3 definition, range [0,200%] |
| **WAPE** | **8.000%** | = MAE/mean(y) = 36/450 |
| MdAPE | 4.222% | Most robust % metric |
| PE10 | 80% | 8/10 within 10% |
| PE20 | 90% | 9/10 within 20% |
| **MPE** | **+1.435%** | Per-item percentage bias |
| Total bias % | +4.000% | = Σe/Σy = 180/4500 |
| Forecast/actual ratio | 0.960 | |
| RAE | 0.240 | = 36/150; model removes 76% of baseline error |
| RSE | 0.1147 | = 1 − R² |
| RRSE | 0.3386 | = RMSE/σ(y) |
| **MASE** | **0.750** | In-sample naive denominator (toy cross-section) |
| MSLE | 0.008656 | |
| **RMSLE** | **0.09304** | ≈ 9.75% typical relative error |
| MdSA | 4.409% | Symmetric; exp(median\|ln(ŷ/y)\|)−1 |
| SSPB | −0.21% | Very slight over-prediction at the median |
| **R²** | **0.8853** | 1 − 43,000/375,000 |
| Adj R² (p=3) | 0.8280 | n=10, k=5 |
| Explained Variance | 0.8940 | R² + Bias²/Var(y) |
| Pearson r | 0.9617 | |
| Pearson r² | 0.9248 | ≠ R² (miscalibration gap = 0.039) |
| **Spearman ρ** | **1.0000** | Perfect ranking |
| CCC | 0.9295 | r × C_b = 0.9617 × 0.9666 |
| Var(ŷ)/Var(y) | 0.618 | Range compressed: isotonic recalibration will help |
| C_b | 0.9666 | Accuracy component of CCC |
| Huber (δ=50) | 1,025.0 | vs ½MSE = 2,150 |
| Pseudo-Huber (δ=50) | 925.49 | |
| Log-Cosh | 35.307 | = MAE − ln2 (degenerate: all \|e\| ≫ 1) |
| Pinball (τ=0.1) | 10.8 | |
| Pinball (τ=0.5) | 18.0 | = MAE/2 ✓ |
| Pinball (τ=0.9) | 25.2 | |
| ε-insensitive (ε=25) | 17.5 | 9/10 inside the tube |
| Durbin-Watson | 1.363 | Slight positive autocorrelation (alternating pattern) |
| Skewness | 2.31 | Right-skewed |
| Excess kurtosis | 4.00 | Heavy-tailed |
| **AIC (p=3, k=5)** | **122.04** | Full likelihood formula |
| AICc | 137.04 | Correction = 15.0 (n/k = 2 — very small sample) |
| BIC | 123.56 | |
| PRESS (illustrative) | ~644,085 | Using h=[0.20,..,0.75] for house 10 |
| R²_pred | ~−0.72 | In-sample 0.885 → out-of-sample −0.72: severe leverage |

---

# APPENDIX B — Time-Series Example All Metrics

```
Training:  [100, 105, 102, 110, 108, 115]   (m=6 periods)
Test y:    [120, 125, 122, 130]              ȳ_test = 124.25
Test ŷ:    [118, 122, 126, 124]
Naive ŷ:   [115, 120, 125, 122]   (persistence, seeded from last train value 115)
In-sample naive MAE = mean([5,3,8,2,7]) = 5.0
```

| Metric | Value | Notes |
|---|---|---|
| **MAE** | **3.750** | |
| RMSE | 4.031 | RMSE/MAE = 1.075 → very uniform errors |
| MedAE | 3.500 | |
| Max Error | 6.0 | |
| Mean residual | +1.750 | Under-forecasting on average |
| MPE | +1.35% | |
| Total bias | +1.41% | Σe/Σy = 7/496 |
| MAPE | 2.99% | |
| WAPE | 3.02% | ≈ MAPE (errors uniform across levels) |
| **MASE** | **0.750** | 3.75 / 5.0 — beats naive by 25% |
| MASE (test naive) | 0.714 | 3.75 / 5.25 — different convention |
| **Theil's U2** | **0.727** | 4.031 / 5.545 |
| MAE_naive (test) | 5.250 | |
| RMSE_naive (test) | 5.545 | |
| **R²** | **−0.145** | SS_res=65, SS_tot=56.75 → NEGATIVE despite good MASE |

---

# APPENDIX C — Probabilistic and Interval Example

Three observations with Gaussian predictions:

| i | y | μ | σ | NLLᵢ | CRPSᵢ |
|---|---|---|---|---|---|
| 1 | 10 | 9 | 2 | 1.73709 | 0.662807 |
| 2 | 20 | 22 | 2 | 2.11209 | 1.204883 |
| 3 | 30 | 30 | 5 | 2.52838 | 1.168475 |
| **Mean** | | | | **2.12585** | **1.01205** |

**Key observations:**
- Obs 3 has *zero* point error but the *worst* NLL — because it claimed σ=5 when it did not need to. NLL penalises unnecessary uncertainty.
- NLL is higher than CRPS for all observations: NLL is more sensitive to over-confidence.
- CRPS = 1.012, which is in the *units of y*. A deterministic forecast with MAE = 1.012 would be equivalent.
- Over-confidence demo: obs 2 with σ=0.5 → NLL = 8.226, 4× worse; shows how NLL explodes for confident-wrong predictions.

**Prediction interval example (10 houses, 90% intervals, constant width 70):**

| Metric | Value | Notes |
|---|---|---|
| PICP | 0.90 | Exactly nominal — but achieved by over-covering 9/9 cheap houses |
| MPIW | 70.0 | |
| NMPIW | 0.361 | = 70/σ(y) |
| NMPIW (vs range) | 0.100 | = 70/(900−200) |
| **Interval Score (α=0.1)** | **400.0** | Width contribution: 70; exceedance: 330 (84% from house 10) |
| MIS with top interval widened to (600,950) | 98.0 | Heteroscedastic intervals: 75% improvement |
| PIT mean | 0.500 | Appears unbiased (but coverage is asymmetric by price band) |
| PIT variance | *would be ~0.15* | Slightly high → mild over-confidence |

**The critical lesson from the interval example:** PICP = 0.90 (perfect) while the Interval Score = 400 is 5.7× higher than it would be for ideally-calibrated heteroscedastic intervals. PICP hides the failure; the Interval Score exposes it.

---

# APPENDIX D — Reference Code: `full_regression_report()`

A single function that computes and prints the complete non-redundant metric set for a regression model.

```python
import numpy as np
from scipy import stats
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error, median_absolute_error,
    max_error, mean_squared_error, r2_score, explained_variance_score,
    mean_absolute_percentage_error, mean_squared_log_error,
    mean_pinball_loss, root_mean_squared_log_error
)

def full_regression_report(y_true, y_pred, label="Model",
                           y_train=None, seasonality=1,
                           n_features=None):
    """
    Print the complete non-redundant regression metric set.

    Parameters
    ----------
    y_true     : array-like, true values
    y_pred     : array-like, model predictions
    label      : str, model label for the report header
    y_train    : optional array-like, training series (for MASE denominator)
    seasonality: int, seasonal period for MASE (default 1 = naive)
    n_features : optional int, number of predictors for Adjusted R²
    """
    y_true  = np.asarray(y_true,  float)
    y_pred  = np.asarray(y_pred,  float)
    e       = y_true - y_pred
    ae      = np.abs(e)
    n       = len(y_true)
    bar     = "=" * 60

    print(f"\n{bar}\n REGRESSION REPORT: {label}\n{bar}")

    # ── MAGNITUDE ──────────────────────────────────────────────
    print("\n── MAGNITUDE ──────────────────────────────────────────")
    mae   = ae.mean()
    rmse  = np.sqrt((e**2).mean())
    medae = np.median(ae)
    mxe   = ae.max()
    print(f"  MAE          = {mae:.4f}   (in target units)")
    print(f"  RMSE         = {rmse:.4f}   (tail-weighted; RMSE/MAE = {rmse/mae:.3f})")
    print(f"  MedAE        = {medae:.4f}   (half of predictions within this)")
    print(f"  Max Error    = {mxe:.4f}   (worst single prediction)")
    print(f"  Percentiles of |e|: "
          f"p50={np.percentile(ae,50):.2f}  p90={np.percentile(ae,90):.2f}"
          f"  p95={np.percentile(ae,95):.2f}  p99={np.percentile(ae,99):.2f}")
    if rmse / mae > 1.5:
        print(f"  [!] RMSE/MAE = {rmse/mae:.2f} — heavy tail present. "
              f"Inspect the worst {min(5,n)} residuals.")

    # ── BIAS  (signed metrics — always include) ──────────────
    print("\n── BIAS (signed) ──────────────────────────────────────")
    mr  = e.mean()
    med = np.median(e)
    mask = y_true != 0
    mpe  = np.mean(e[mask] / y_true[mask]) * 100
    tbias= e.sum() / y_true.sum() * 100
    print(f"  Mean residual     = {mr:+.4f}   (>0 = under-prediction)")
    print(f"  Median residual   = {med:+.4f}")
    print(f"  MPE               = {mpe:+.4f}%  (per-observation percentage bias)")
    print(f"  Total bias        = {tbias:+.4f}%  (Σe/Σy; the aggregate is what matters)")
    print(f"  Bias share of MSE = {(mr**2)/(e**2).mean()*100:.2f}%  "
          f"(if large, a calibration fix will help)")
    if abs(tbias) > 5:
        print(f"  [!] Total bias {tbias:+.1f}% exceeds 5% — investigate and correct.")

    # ── RELATIVE / SCALED ──────────────────────────────────────
    print("\n── RELATIVE / SCALED ──────────────────────────────────")
    wape = ae.sum() / np.abs(y_true).sum() * 100
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    mdape= np.median(ae[mask] / y_true[mask]) * 100
    r2   = r2_score(y_true, y_pred)
    evs  = explained_variance_score(y_true, y_pred)
    print(f"  WAPE   = {wape:.3f}%   (volume-weighted; well-defined with zeros)")
    print(f"  MAPE   = {mape:.3f}%   (per-item; undefined at 0 — use WAPE for supply chain)")
    print(f"  MdAPE  = {mdape:.3f}%  (robust median %; report with p90 for full picture)")
    print(f"  R²     = {r2:.6f}   ({r2:.2%} of variance explained vs mean baseline)")
    print(f"  EVS    = {evs:.6f}   (EVS − R² = {evs-r2:.6f} = normalised Bias²)")
    if n_features is not None and n - n_features - 1 > 0:
        ar2 = 1 - (1 - r2) * (n - 1) / (n - n_features - 1)
        print(f"  Adj R² = {ar2:.6f}   (penalised for {n_features} features)")
    if r2 < 0:
        print("  [!] R² < 0: the model is WORSE than predicting the mean.")
    try:
        rmsle = root_mean_squared_log_error(
            y_true, np.clip(y_pred, 0, None))
        print(f"  RMSLE  = {rmsle:.6f}   (≈ {(np.expm1(rmsle)*100):.2f}% typical relative error)")
    except Exception:
        print("  RMSLE: skipped (requires y ≥ 0)")

    # ── MASE (if training series provided) ──────────────────
    if y_train is not None:
        y_train = np.asarray(y_train, float)
        naive_d = np.abs(y_train[seasonality:] - y_train[:-seasonality]).mean()
        if naive_d > 0:
            mase = mae / naive_d
            print(f"\n── MASE ────────────────────────────────────────────────")
            print(f"  MASE = {mase:.4f}  (seasonality={seasonality}; "
                  f"1.0 = naive; < 1 = better than naive)")
            if mase > 1:
                print("  [!] MASE > 1: the NAIVE forecast is better. "
                      "Reconsider the model.")

    # ── CORRELATION / CALIBRATION ────────────────────────────
    print("\n── CORRELATION / CALIBRATION ──────────────────────────")
    r_p = stats.pearsonr(y_true, y_pred)[0]
    r_s = stats.spearmanr(y_true, y_pred)[0]
    def ccc(a, b):
        cov = ((a-a.mean())*(b-b.mean())).mean()
        return 2*cov/(a.var()+b.var()+(a.mean()-b.mean())**2)
    vr = y_pred.var() / y_true.var()
    print(f"  Spearman ρ = {r_s:.6f}   (ranking quality)")
    print(f"  Pearson  r = {r_p:.6f}   r² = {r_p**2:.6f}")
    print(f"  r² − R²    = {r_p**2 - r2:.6f}   (miscalibration; 0 = perfectly calibrated)")
    print(f"  CCC        = {ccc(y_true, y_pred):.6f}")
    print(f"  Var(ŷ)/Var(y) = {vr:.4f}   "
          f"({'compressed — range too narrow' if vr < 0.8 else 'ok'})")

    # ── RESIDUAL DISTRIBUTION ───────────────────────────────
    print("\n── RESIDUAL DISTRIBUTION ──────────────────────────────")
    sk  = stats.skew(e)
    ku  = stats.kurtosis(e)                      # excess kurtosis
    dw  = np.sum(np.diff(e)**2) / np.sum(e**2)
    print(f"  Skewness   = {sk:.3f}   (|>1| = meaningfully skewed)")
    print(f"  Excess Kurt= {ku:.3f}   (|>1| = heavy tails; Gaussian intervals may under-cover)")
    print(f"  Durbin-Watson = {dw:.3f}  "
          f"({'ok' if 1.5 <= dw <= 2.5 else '[!] autocorrelation suspected'})")

    # ── TOP WORST RESIDUALS ──────────────────────────────────
    print("\n── TOP 5 WORST PREDICTIONS ─────────────────────────────")
    order = np.argsort(-ae)[:5]
    print(f"  {'i':>4}  {'actual':>10}  {'predicted':>10}  "
          f"{'error':>10}  {'|e|/sigma':>10}")
    for idx in order:
        print(f"  {idx:>4}  {y_true[idx]:>10.3f}  {y_pred[idx]:>10.3f}  "
              f"  {e[idx]:>+10.3f}  {ae[idx]/y_true.std():>10.4f}")

    print(f"\n{bar}\n")


# ── EXAMPLE USAGE ─────────────────────────────────────────────
y      = np.array([200,250,300,350,400,450,500,550,600,900.])
y_pred = np.array([220,240,310,330,420,430,520,530,620,700.])

full_regression_report(y, y_pred, label="10-House Model", n_features=3)
```

---

# APPENDIX E — Diagnostic-Panel Plot Function

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def regression_diagnostic_panel(y_true, y_pred, title="Regression Diagnostics",
                                  times=None, figsize=(16, 9)):
    """
    Six-panel diagnostic plot for a regression model.
    
    Panels:
        1. Predicted vs Actual (45° line)
        2. Residuals vs Fitted
        3. Scale-Location (√|standardised residual| vs Fitted)
        4. Normal Q-Q
        5. Residual histogram with mean line
        6. Residuals vs time/index
    """
    y_true  = np.asarray(y_true,  float)
    y_pred  = np.asarray(y_pred,  float)
    e       = y_true - y_pred
    sigma   = e.std() if e.std() > 0 else 1.0
    std_e   = e / sigma
    t       = np.arange(len(e)) if times is None else np.asarray(times, float)

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # 1. Predicted vs Actual
    ax = axes[0, 0]
    lims = [min(y_true.min(), y_pred.min()) * 0.97,
            max(y_true.max(), y_pred.max()) * 1.03]
    ax.scatter(y_true, y_pred, alpha=0.7, edgecolors='k', linewidths=0.5)
    ax.plot(lims, lims, 'r--', lw=1.5, label='Perfect (45°)')
    ax.set_xlim(lims); ax.set_ylim(lims)
    ax.set_xlabel('Actual'); ax.set_ylabel('Predicted')
    ax.set_title(f'Predicted vs Actual  (R²={1-((e**2).sum()/((y_true-y_true.mean())**2).sum()):.3f})')
    ax.legend(fontsize=8)

    # 2. Residuals vs Fitted
    ax = axes[0, 1]
    ax.scatter(y_pred, e, alpha=0.7, edgecolors='k', linewidths=0.5)
    ax.axhline(0, color='r', ls='--', lw=1.5)
    ax.axhline(e.mean(), color='b', ls=':', lw=1, label=f'mean={e.mean():.2f}')
    ax.set_xlabel('Fitted values'); ax.set_ylabel('Residual')
    ax.set_title('Residuals vs Fitted')
    ax.legend(fontsize=8)
    if abs(e.mean()) > 0.1 * e.std():
        ax.set_title('Residuals vs Fitted  [⚠ BIAS DETECTED]', color='darkred')

    # 3. Scale-Location
    ax = axes[0, 2]
    ax.scatter(y_pred, np.sqrt(np.abs(std_e)), alpha=0.7,
               edgecolors='k', linewidths=0.5)
    ax.set_xlabel('Fitted values')
    ax.set_ylabel('√|Standardised residual|')
    ax.set_title('Scale-Location  (funnel → heteroscedasticity)')

    # 4. Q-Q plot
    ax = axes[1, 0]
    stats.probplot(e, dist='norm', plot=ax)
    ax.set_title(
        f'Normal Q-Q  (skew={stats.skew(e):.2f},'
        f' kurt={stats.kurtosis(e):.2f})')

    # 5. Residual histogram
    ax = axes[1, 1]
    ax.hist(e, bins=min(30, max(5, n // 3)) if (n := len(e)) else 10,
            edgecolor='k', alpha=0.75, color='steelblue')
    ax.axvline(0, color='r', ls='--', lw=1.5, label='zero')
    ax.axvline(e.mean(), color='b', ls='-', lw=1.5,
               label=f'mean={e.mean():.2f}')
    ax.axvline(np.median(e), color='g', ls='-.', lw=1.5,
               label=f'median={np.median(e):.2f}')
    ax.set_xlabel('Residual'); ax.set_ylabel('Count')
    ax.set_title('Residual Distribution')
    ax.legend(fontsize=8)

    # 6. Residuals vs time
    ax = axes[1, 2]
    ax.plot(t, e, marker='o', ms=4, lw=0.8, alpha=0.8)
    ax.axhline(0, color='r', ls='--', lw=1.5)
    ax.fill_between(t, -e.std(), e.std(), alpha=0.1, color='blue',
                    label='±1σ band')
    dw = np.sum(np.diff(e)**2) / max(np.sum(e**2), 1e-12)
    ax.set_xlabel('Index / Time')
    ax.set_ylabel('Residual')
    ax.set_title(f'Residuals vs Time  (DW={dw:.3f}'
                 f'{", [⚠ autocorrelation]" if not (1.5 <= dw <= 2.5) else ""})')
    ax.legend(fontsize=8)

    plt.tight_layout()
    return fig


# Usage
y      = np.array([200,250,300,350,400,450,500,550,600,900.])
y_pred = np.array([220,240,310,330,420,430,520,530,620,700.])
fig = regression_diagnostic_panel(y, y_pred, title="10-House Model Diagnostics")
# fig.savefig("diagnostics.png", dpi=150, bbox_inches='tight')
# plt.show()
```

---

# Final Goal Checklist

After studying this document, you should be able to:

- [ ] **State what any regression metric measures** in one sentence, without confusing it with a similar one.
- [ ] **Choose the correct metric** (and loss) for a given cost structure, target distribution, and decision type without being prompted.
- [ ] **Identify what a metric cannot see** (bias from MAE/RMSE, calibration from Pearson r, functional form from R²).
- [ ] **Construct the minimum non-redundant metric set** for a new problem: at least magnitude + signed bias + relative + residual plot.
- [ ] **Apply the four things to always report** (MSBR) from memory to any regression deliverable.
- [ ] **Explain the RMSE/MAE ratio** as a free tail diagnostic.
- [ ] **Derive the bias-variance decomposition** of MSE from the residual definition.
- [ ] **Explain why MAE → median, MSE → mean**, and why that matters for totals on skewed targets.
- [ ] **Identify the failure modes of MAPE** (zeros, asymmetry, downward bias, scale-dependence) and name MASE and WAPE as the correct replacements.
- [ ] **Set τ for quantile regression** from a stockout-vs-holding cost ratio.
- [ ] **Explain what CRPS measures** and why it is preferred over NLL for reporting.
- [ ] **Interpret a PIT histogram** and diagnose over-confidence, under-confidence, and bias from its shape.
- [ ] **Build a correct time-series backtest** using TimeSeriesSplit with a gap and report a metric-by-horizon table.
- [ ] **Relate AIC, AICc, BIC, and cross-validation** to each other and choose the right tool for each situation.
- [ ] **Use the PRESS identity** to get LOO-CV for a linear model without refitting.
- [ ] **Interpret the fit ladder** (Spearman → r² → EVS → R²) and Var(ŷ)/Var(y) to diagnose a miscalibrated model.
- [ ] **Recognise the five residual-plot patterns** and name the fix for each.
- [ ] **Explain why R² is wrong for time series**, comparing with MASE on the same data.
- [ ] **Describe the multi-output aggregation trap** and avoid averaging scale-dependent metrics across targets.
- [ ] **Implement MAE, RMSE, MASE, CRPS, and the Interval Score** in NumPy from memory.
- [ ] **Answer "is this model good?"** by comparing to a baseline, stating the level, reporting bias, and acknowledging the tail — not by quoting one number.

> **One-sentence takeaway.**
>
> **A single regression metric is never enough** — always report magnitude, signed bias, a relative/scaled metric, and a residual plot; choose the metric and its matching loss from the cost function, not from familiarity; and every number you quote is only as honest as the cross-validation scheme that produced it.
