# Book 2 — SQL | Part 8: Scenario business queries (sales, HR, e-commerce, banking)

**Target:** 70 | **Actual:** 74 | **Scope:** Business-style SQL asked as "here are the tables, write the query" in sales, HR/payroll, e-commerce and banking. Retention/cohort/funnel/MoM growth belong to Part 9; nth highest, de-duplication, gaps-and-islands, recursive CTEs belong to Part 10.

### Q1 ⭐⭐⭐ 🟢 HR: Using `employees` (emp_id, name, dept_id) and `departments` (dept_id, dept_name), show the headcount of every department, including departments that currently have no employees.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Sales: Using `orders`, `order_items` (order_id, product_id, qty, unit_price) and `products` (product_id, category), find total revenue per product category, highest first.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Sales: Find the top 5 customers by total amount spent, showing customer name and total spend.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 HR: List employees earning more than ₹80,000 with their department name and salary, highest salary first.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 E-commerce: Orders have a status (delivered, cancelled, returned, in-transit). Calculate total revenue counting only delivered orders.
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Sales: Show the number of orders and total sales value per day for the last 7 days.
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Sales: Show total revenue for each calendar month of 2025 (month name and amount), including months with zero sales.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 HR/payroll: Show each department's total monthly payroll and its percentage share of the company payroll.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Banking: `transactions` has account_id, txn_type ('deposit' or 'withdrawal') and amount. Calculate the current balance of each account.
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 HR: Using `employees` (join_date, left_date, dept_id), calculate the attrition rate per department for 2025 (leavers divided by average headcount), and explain your denominator.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 HR: Calculate each current employee's tenure in years from join_date, the average tenure per department, and list employees with more than 5 years of service.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 E-commerce: Find customers who placed more than 3 orders in the last 90 days.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 HR: `attendance` has emp_id, work_date and status (present/absent/leave). Find employees whose attendance in March 2026 was below 75% of working days.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 E-commerce: Find customers who bought both 'Laptop' and 'Mouse' (in any orders).
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 HR: List departments that have more than 5 employees and an average salary above ₹60,000.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 E-commerce: Find products that have never been sold (present in `products` but not in `order_items`).
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 Sales: Calculate average order value per customer city.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🔴 HR: Using join_date and left_date, produce for each month of 2025 the opening headcount, joiners, leavers and closing headcount.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🔴 E-commerce: Find customers who placed at least one order in every month of 2025.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🔴 Sales: Find the top 3 products by revenue within each product category.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 HR: Show the number of male and female employees in each department.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 HR: List employees who joined in the last 90 days (new hires) with their department.
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 HR: Show the highest, lowest and spread (max minus min) of salary in each department.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 E-commerce: Count orders by status (delivered, cancelled, returned, in-transit).
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 E-commerce: Calculate the overall order cancellation rate as a percentage.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 HR: Find employees who have no manager assigned and employees whose department is missing (NULLs).
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 Banking: Using `customers` (dob), count customers by age band: under 25, 25-40, 41-60, above 60.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 Retail: `inventory` has product_id, stock_qty and reorder_level. List products that need re-ordering.
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 E-commerce (food delivery): Calculate the cancellation rate per city and show cities above the company average.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 HR/payroll: Monthly payroll cost = salary + bonus, where bonus can be NULL. Show total payroll cost per month for 2025.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 HR: Find employees who have taken no leave this year (`leaves`: emp_id, start_date, end_date).
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 HR: Calculate average leave days per employee per department and list employees who took more than 20 days.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 HR: From `attendance` (clock_in, clock_out), find employees whose overtime exceeded 40 hours in a month (standard day = 9 hours).
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 HR: `salary_history` has emp_id, effective_date and salary. Calculate each employee's hike percentage between their last two revisions.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 HR: Show the number of direct reports per manager and list managers with more than 5.
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 HR/recruitment: From `applications` (applied_date, offer_date, source), find the average time-to-offer by sourcing channel (referral, portal, agency).
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 HR: Split leavers into voluntary and involuntary using exit_reason, per department, with percentages.
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 HR: Find employees who left within 6 months of joining (early attrition) and the share of total leavers they represent.
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Banking: Flag customers who made transactions totalling more than ₹50,000 in a single day.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Banking: Find dormant accounts: accounts with no transaction in the last 6 months.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Banking: Show average balance by account type and list branches whose average balance is above the bank-wide average.
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 Banking: Using `loans` (customer_id, loan_amount) and `repayments` (loan_id, amount), show total outstanding balance per customer.
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 E-commerce: Calculate the late-delivery rate (delivered_at later than promised_at) per delivery partner.
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 E-commerce: Calculate the return rate (returned items divided by items sold) per product category.
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 E-commerce: What percentage of customers have placed two or more orders (overall repeat-purchase rate)?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 Sales: Compare total sales on weekdays versus weekends.
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 Sales: Show quarterly sales per region as columns Q1, Q2, Q3, Q4 (one row per region).
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 Sales: List customers whose total spend is above the average spend of customers in their own city.
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🔴 Banking: `transfers` has from_account, to_account and amount. Compute the net inflow (received minus sent) for every account.
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🔴 Sales: For each quarter, find the region with the highest sales, keeping all regions in case of a tie.
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🟢 HR: Group employees into salary bands (below 30k, 30-60k, 60-100k, above 100k) and count each band.
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟢 HR: List employees whose work anniversary falls in the current month.
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟢 E-commerce: Compare average order value of orders that used a coupon with those that did not.
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🟢 Sales: Show the number of customers per city, largest first.
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🟡 HR: Find the headcount of active employees on a given date (for example 30 Sep 2025), by department.
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🟡 HR: Calculate each department's average salary after excluding its highest and lowest paid employee.
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟡 HR: Find pairs of employees in the same department with identical salary.
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟡 HR/payroll: Find salary payments in `payroll` made to employees after their left_date (payroll audit).
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟡 E-commerce: Reconcile data: find orders where the order total does not equal the sum of its item lines.
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟡 Banking: Find customers holding accounts in more than one branch.
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 HR/recruitment: Calculate the offer-acceptance rate per recruiter (offers accepted divided by offers made).
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟡 HR: Using `training_assignments` (emp_id, course_id, completed_date), find training completion rate per department.
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟡 HR: Compare average salary of men and women within each job grade to spot a pay gap.
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟡 Retail: List products priced above the average price of their category.
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟡 Banking: Bucket overdue loan instalments into 1-30, 31-60, 61-90 and 90+ days past due, and count loans in each bucket per branch.
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 Sales: Calculate revenue lost to discounts (list price minus sold price times quantity) per category.
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 Banking: Find accounts where ATM withdrawals on a single day exceeded the ₹40,000 daily limit.
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 E-commerce: For each customer, find the category of their very first order.
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🔴 Banking (fraud check): Find accounts with 3 or more transactions of the same amount within a 10-minute window.
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🔴 Sales: Find the smallest set of products that together make up 80% of revenue (Pareto analysis).
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🔴 E-commerce: Find the pairs of products most frequently bought together in the same order (basket analysis).
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🔴 HR: From `leaves`, find pairs of employees of the same team who are on leave on overlapping dates.
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🔴 HR: Find the employee(s) whose salary equals the median salary of their department.
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🔴 E-commerce: Split customers into 10 equal spend groups (deciles) and show the share of total revenue from the top decile.
<!-- ANSWER_PENDING -->
