import numpy as np

# 12 employees: yearly cash pay and the yearly value of stock grants (in lakh rupees)
cash_pay = np.array([6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 30, 45])
stock_value = np.array([0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 40, 150])
total_pay = cash_pay + stock_value

def five_numbers(label, values):
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    print(label, "| mean", round(values.mean(), 1), "| median", median, "| Q1", q1, "| Q3", q3, "| max", values.max())

five_numbers("Cash pay    ", cash_pay)
five_numbers("Total pay   ", total_pay)

people_with_stock = (stock_value > 0).sum()
print("People holding stock:", people_with_stock, "of", len(stock_value))
print("Median stock among holders:", np.median(stock_value[stock_value > 0]))
print("Top earner share of all total pay:", round(total_pay.max() / total_pay.sum() * 100, 1), "%")
