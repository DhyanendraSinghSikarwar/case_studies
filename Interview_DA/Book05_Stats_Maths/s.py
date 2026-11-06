import numpy as np
from scipy import stats

# Month number and hires in that month
month_number = np.array([1, 2, 3, 4, 5, 6])
hires = np.array([20, 24, 25, 29, 33, 34])

# Fit the straight line through the six points
fit = stats.linregress(month_number, hires)

# Line values: intercept + slope x month gives the forecast for that month
print("Slope:", round(fit.slope, 4), "Intercept:", round(fit.intercept, 4), "R-squared:", round(fit.rvalue**2, 4))
print("Month 7:", round(fit.intercept + fit.slope * 7, 2))
print("Month 8:", round(fit.intercept + fit.slope * 8, 2))
print("Month 18:", round(fit.intercept + fit.slope * 18, 2))
