# Q31 better ETA, fewer orders (illustrative numbers)
sessions = 100_000
conv0 = 0.30
shown_old, shown_new = 24, 28      # average ETA shown, minutes
actual = 30                        # average actual delivery time, minutes
elasticity = -0.005                # relative drop in conversion per extra displayed minute (assumed)
conv1 = conv0 * (1 + elasticity * (shown_new - shown_old))
orders0, orders1 = sessions * conv0, sessions * conv1
print("bias old/new (min, shown - actual):", shown_old - actual, shown_new - actual)
print("orders before/after:", round(orders0), round(orders1), " change:", round(orders1 / orders0 - 1, 3))
assert round(orders0) == 30_000 and round(orders1) == 29_400 and round(orders1 / orders0 - 1, 3) == -0.02

late0, late1 = 0.30, 0.12          # share of orders delivered later than shown + 5 min
cancel_late, cancel_ontime = 0.10, 0.02
cr0 = late0 * cancel_late + (1 - late0) * cancel_ontime
cr1 = late1 * cancel_late + (1 - late1) * cancel_ontime
d0, d1 = orders0 * (1 - cr0), orders1 * (1 - cr1)
print("cancel rate before/after:", round(cr0, 4), round(cr1, 4))
print("delivered orders before/after:", round(d0), round(d1), " change:", round(d1 / d0 - 1, 4))
assert round(cr0, 3) == 0.044 and round(cr1, 4) == 0.0296
assert round(d0) == 28_680 and round(d1) == 28_530 and round(d1 / d0 - 1, 4) == -0.0052
# what repeat-rate gain from fewer late orders would turn delivered orders positive over 8 weeks?
repeat_uplift_needed = d0 / d1 - 1
print("delivered-order gain needed from repeat purchases:", round(repeat_uplift_needed, 4))
assert round(repeat_uplift_needed, 4) == 0.0053
# the "15% better accuracy" in the prompt, read as mean absolute error falling 15%
mae_old, mae_new = 6.0, 5.1
print("MAE change:", round(mae_new / mae_old - 1, 3))
assert round(mae_new / mae_old - 1, 3) == -0.15
