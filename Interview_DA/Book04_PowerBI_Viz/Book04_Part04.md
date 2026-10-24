# Book 4 — Power BI & Visualization | Part 4: DAX basics: calculated column vs measure, SUM vs SUMX, COUNT, CALCULATE 🟡

**Target:** 75 questions | **Actual:** 74 questions
**Scope:** DAX fundamentals for a beginner analyst: calculated column vs measure, SUM vs SUMX and iterators, the COUNT family, CALCULATE, row vs filter context basics, DIVIDE, and practical write-the-measure tasks. ALL/ALLEXCEPT, time intelligence and RANKX are Part 5.

### Q1 ⭐⭐⭐ 🟢 What is DAX, and where is it used in Power BI?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is the difference between a calculated column and a measure?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 How do you create a calculated column and a measure in Power BI Desktop?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Should "Salary Band" be a calculated column or a measure? Why?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is the difference between SUM and SUMX?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What is the difference between COUNT, COUNTA, COUNTROWS and DISTINCTCOUNT?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 What is filter context in DAX?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 What is row context in DAX?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 What does the CALCULATE function do?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 Write a DAX measure for total sales (or total payroll cost).
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 Write a DAX measure that counts unique employees.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is the difference between row context and filter context?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Write a DAX measure for total sales of one product category using CALCULATE.
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Write a DAX measure for total revenue when each row has Quantity and Unit Price columns.
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Why should you use DIVIDE instead of the / operator in a measure?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Why does my measure show the same number in every row of a table visual?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What is an iterator function in DAX, and which ones do you know?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is the difference between an implicit measure and an explicit measure?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 Can you write SUM(Sales[Quantity] * Sales[Price]) in DAX? Why or why not?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 What is BLANK() in DAX, and how is it different from zero or empty text?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟢 What is the difference between DAX and Excel formulas?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟢 What is the difference between DAX and M, the Power Query language?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟢 What is a quick measure, and what are its limits?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟢 Write a calculated column using IF to flag late arrivals in an attendance table.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟢 Write a DAX formula to calculate the number of days between two dates, for example leave days.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟢 Where are calculated columns stored, and how do they affect file size?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 Why does Microsoft recommend COUNTROWS rather than COUNT to count rows?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 How do you refer to columns and measures in a DAX formula (syntax conventions)?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 Write a DAX measure for average salary.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 Can one measure refer to another measure?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 What is the difference between AVERAGE and AVERAGEX?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 What is context transition in DAX?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Write a DAX measure for the headcount of active employees using CALCULATE and COUNTROWS.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Write a DAX measure for attendance percentage.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 How does CALCULATE treat several filter arguments?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 What happens when a CALCULATE filter targets a column that already has a slicer selection?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 What is the difference between a Boolean filter and the FILTER function inside CALCULATE?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What is the difference between SUMX(FILTER(...)) and CALCULATE(SUM(...), ...)?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Write a DAX measure for profit margin percentage.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Write a DAX measure for each department's share of total headcount.
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Write a DAX measure for net sales when the table has MRP and discount percentage columns.
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 How would you count unique customers when customer IDs are spread across several tables?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 Why does a calculated column that uses SUM show the same total on every row?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Should you add a column in Power Query or as a DAX calculated column?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 What does RELATED do, and why does it need row context?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 Write a calculated column for employee tenure in years from the joining date.
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 Write a DAX measure for average order value.
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 Write a DAX measure for total payroll cost when each row has basic pay and allowances columns.
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 What is SWITCH, and when do you use it instead of nested IF?
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 What are VAR and RETURN in DAX, and why use them?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 How do you debug a DAX measure that returns a wrong number?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🟢 What is a calculated table, and when would you use one?
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🟢 What happens if you use COUNT on a text column?
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🟢 Is DAX case-sensitive, and do spaces matter?
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🟢 How do you write comments in DAX?
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🟢 Does DAX work in Excel?
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🟢 Can you write DAX in Power BI Service, or on a Mac?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟢 What naming and organisation habits make measures easier to maintain (measure table, display folders)?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟢 Write a DAX measure for the latest hiring date.
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟢 What data types does DAX support, and what is implicit conversion?
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 How does DISTINCTCOUNT treat blanks, and what are the alternatives?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟡 What is a circular dependency error in DAX, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟡 What does the error "A single value for column cannot be determined" mean?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟡 Why does a ratio or average show the wrong grand total, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟡 What is the DAX query view in Power BI Desktop?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 What is a visual calculation, and how does it differ from a measure?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 Are there DAX limitations in DirectQuery mode?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟡 What does SELECTEDVALUE do, and when do you use it?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟡 When are measures calculated, and what does that mean for performance?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟡 Is SUMX always slower than SUM?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟡 Write a DAX measure that counts rows where a column is blank.
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟡 Write a DAX measure for sales in the North or South region.
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟡 Write a DAX measure for the total of orders that are each above Rs 10,000.
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 Write a DAX measure for the number of employees with more than 5 years of service.
<!-- ANSWER_PENDING -->
