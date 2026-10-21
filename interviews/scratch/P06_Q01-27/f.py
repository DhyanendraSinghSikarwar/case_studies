import numpy as np, pandas as pd
# Q13 holiday / promo features (known in advance -> safe for the forecast horizon)
d = pd.DataFrame({"date": pd.date_range("2024-10-20", periods=20)})
hol = pd.to_datetime(["2024-10-31", "2024-11-01"])           # e.g. Diwali window
d["is_holiday"] = d.date.isin(hol).astype(int)
nxt = np.searchsorted(hol.values, d.date.values)               # index of next holiday on/after date
nxt_d = np.where(nxt < len(hol), hol.values[np.minimum(nxt, len(hol)-1)], np.datetime64("NaT"))
d["days_to_holiday"] = (pd.to_datetime(nxt_d) - d.date).dt.days.clip(upper=14)   # 14 = "far away"
d["pre_holiday_week"] = d.days_to_holiday.between(1, 7).astype(int)
print(d.iloc[[0, 10, 11, 12, 13]].to_string(index=False))

# Q23 calendar encodings
c = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=400)})
c["dow"] = c.date.dt.dayofweek
c["dow_sin"], c["dow_cos"] = np.sin(2*np.pi*c.dow/7), np.cos(2*np.pi*c.dow/7)
doy = c.date.dt.dayofyear
for k in (1, 2, 3):                                            # yearly Fourier terms
    c[f"yr_sin{k}"], c[f"yr_cos{k}"] = np.sin(2*np.pi*k*doy/365.25), np.cos(2*np.pi*k*doy/365.25)
print(c.filter(like="dow_").iloc[[0, 6]].round(3).to_string())
print("Sunday->Monday distance raw:", abs(6-0), " sin/cos:", round(float(np.hypot(
    c.dow_sin[6]-c.dow_sin[7], c.dow_cos[6]-c.dow_cos[7])), 3), " Mon->Tue:", round(float(np.hypot(
    c.dow_sin[7]-c.dow_sin[8], c.dow_cos[7]-c.dow_cos[8])), 3))
print(c.shape)
