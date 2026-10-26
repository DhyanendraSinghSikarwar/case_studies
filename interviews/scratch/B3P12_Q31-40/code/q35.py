# Q35: customers with no orders in 2025: NOT EXISTS vs NOT IN with a NULL in the subquery.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
""")

sql_answer = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in = """
SELECT c.customer_id, c.name FROM customers c
WHERE c.customer_id NOT IN (SELECT customer_id FROM orders
                            WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in_fixed = sql_not_in.replace("FROM orders\n", "FROM orders\n").replace(
    "WHERE order_date >= '2025-01-01'", "WHERE customer_id IS NOT NULL AND order_date >= '2025-01-01'")
got = pd.read_sql(sql_answer, con)
print("NOT EXISTS"); print(got.to_string(index=False))
print("\nNOT IN with the NULL row inside 2025, rows returned:", len(pd.read_sql(sql_not_in, con)))
fixed = pd.read_sql(sql_not_in_fixed, con)
print("NOT IN with customer_id IS NOT NULL added, rows returned:", len(fixed))

# --- pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
in_2025 = orders[(orders.order_date >= "2025-01-01") & (orders.order_date < "2026-01-01")]
want = customers[~customers.customer_id.isin(in_2025.customer_id)].reset_index(drop=True)
# --- end pandas
print("\npandas ~isin (the NaN in the list does not poison it)"); print(want.to_string(index=False))
print("customer_id dtype after read_sql:", orders.customer_id.dtype, "(float because of the NULL)")
pd.testing.assert_frame_equal(got, want, check_dtype=False)
pd.testing.assert_frame_equal(got, fixed, check_dtype=False)
print("assert passed: NOT EXISTS = pandas ~isin = guarded NOT IN, ordered by customer_id")
