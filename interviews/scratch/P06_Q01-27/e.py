import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.holtwinters import ExponentialSmoothing

rng = np.random.default_rng(1)
n = 120; t = np.arange(n)
y = pd.Series(100 + 0.5*t + 12*np.sin(2*np.pi*t/12) + rng.normal(0, 3, n),
              pd.date_range("2015-01", periods=n, freq="MS"))

def walk_forward(y, fit_forecast, horizon=3, first_train=60, step=3, window=None):
    errs = []
    for end in range(first_train, len(y) - horizon + 1, step):
        start = 0 if window is None else end - window     # expanding vs rolling
        train, test = y.iloc[start:end], y.iloc[end:end+horizon]
        errs.append(np.mean(np.abs(test.values - fit_forecast(train, horizon))))
    return np.mean(errs), len(errs)

snaive = lambda tr, h: np.resize(tr.values[-12:], h)
hw = lambda tr, h: ExponentialSmoothing(tr, trend="add", seasonal="add",
                                        seasonal_periods=12).fit().forecast(h).values
for name, f in [("seasonal naive", snaive), ("Holt-Winters", hw)]:
    e, k = walk_forward(y, f)
    r, _ = walk_forward(y, f, window=48)
    print(f"{name}: expanding MAE={e:.2f}  rolling(48) MAE={r:.2f}  folds={k}")

# Q44 from scratch
def sma(x, w): return np.convolve(x, np.ones(w)/w, mode="valid")
def ses(x, alpha):
    l = x[0]; out = [l]
    for v in x[1:]:
        l = alpha*v + (1-alpha)*l; out.append(l)
    return np.array(out)                       # out[t] = level after seeing x[t]; forecast = out[-1]
def acf_np(x, nlags):
    x = x - x.mean(); d = (x*x).sum()
    return np.array([(x[:len(x)-k]*x[k:]).sum()/d for k in range(nlags+1)])
def seasonal_naive(x, m, h): return np.array([x[len(x)-m + (i % m)] for i in range(h)])
x = y.values
print("SMA3 last", sma(x, 3)[-1].round(2), "| SES a=.3 forecast", ses(x, .3)[-1].round(2))
print("ACF lag1,12", acf_np(x - np.polyval(np.polyfit(t, x, 1), t), 12)[[1, 12]].round(2))
print("snaive h=3", seasonal_naive(x, 12, 3).round(1))
from statsmodels.tsa.stattools import acf
print("check vs statsmodels", np.allclose(acf_np(x, 12), acf(x, nlags=12)))
