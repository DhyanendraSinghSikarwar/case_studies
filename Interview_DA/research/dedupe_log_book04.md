# Cross-part duplicate resolution (Book 4, Wave A)

Method: token-overlap scan of all 639 Book 4 questions (Jaccard >= 0.5 across different parts, 79 pairs), then manual judgement: false positives from shared words (e.g. "What is Power BI ...") kept; exact or near-identical questions removed from one part, keeping the copy in the part that owns the topic. Kept on purpose (different angle): P1Q5/P7Q11 (report vs dashboard vs app in the Service), P1Q15/P7Q15 (Import vs DirectQuery vs Live Connection from a refresh angle), P11Q12 (Copilot writing the attrition DAX), P7Q1/P10Q37 (RLS vs Tableau), P10Q27 (Mac for Tableau and Power BI). The Wave A counts fall below some part targets after removal; gap-fills are added afterwards.

| Removed (old ID) | Question | Kept copy |
|---|---|---|
| B4P1Q9 | What is DAX and what is it used for in Power BI? | B4P4Q1 |
| B4P1Q22 | What is My workspace in the Power BI Service? | B4P7Q4 |
| B4P1Q29 | What are the Power BI licence types (Free, Pro, Premium Per User, Fabric or Premium capacity), and how do they differ? | B4P7Q10 |
| B4P1Q43 | What are data source privacy levels (Public, Organizational, Private), and why do they matter? | B4P2Q59 |
| B4P1Q44 | What is a composite model in Power BI? | B4P3Q53 |
| B4P2Q4 | What is the difference between Load and Transform Data when you import a file in Power BI Desktop? | B4P1Q12 |
| B4P2Q53 | Can you use Power Query in Power BI Desktop on a Mac? | B4P1Q31 |
| B4P3Q17 | What is a semantic model in Power BI (formerly called a dataset)? | B4P1Q18 |
| B4P3Q36 | How do you create a date table in Power BI? | B4P5Q15 |
| B4P3Q38 | What is a calculated table, and when would you use one? | B4P4Q53 |
| B4P4Q15 | Write a DAX measure for the attrition rate. | B4P5Q24 |
| B4P5Q1 | What is filter context in DAX, and where does it come from? | B4P4Q7 |
| B4P5Q2 | What is the difference between row context and filter context? | B4P4Q12 |
| B4P5Q9 | What is context transition in DAX, and when does it happen? | B4P4Q33 |
| B4P5Q10 | What are variables (VAR and RETURN) in DAX, and why use them? | B4P4Q51 |
| B4P5Q16 | What is the difference between a Boolean filter and the FILTER function inside CALCULATE? | B4P4Q38 |
| B4P6Q20 | What is a hierarchy in Power BI, and how do you create one such as Department > Team > Employee? | B4P3Q39 |
| B4P6Q41 | How do you export the data behind a visual, and what does Show as a table do? | B4P1Q26 |
| B4P7Q10 | What are the different Power BI licences (Free, Pro, Premium Per User, Premium/Fabric capacity), and what does each allow? | B4P1Q29 |
| B4P7Q37 | What are Power BI Service features that Power BI Desktop does not have, and the other way round? | B4P1Q32 |
| B4P7Q40 | Can you use Power BI Desktop on a Mac? What alternatives exist? | B4P1Q31 |
| B4P7Q43 | What is Microsoft Fabric, and how does it relate to Power BI? | B4P1Q34 |
| B4P8Q2 | What is the difference between a report and a dashboard in Power BI? | B4P1Q5 |
| B4P8Q22 | Which KPIs and visuals would you put on an HR attrition dashboard? | B4P9Q4 |
| B4P9Q10 | Write a DAX measure for sales year-over-year growth percentage. | B4P5Q7 |
| B4P9Q13 | How would you set up a dashboard so each HR business partner sees only their own department's employees? | B4P7Q38 |
| B4P9Q27 | Write DAX measures for sales month-to-date and year-to-date. | B4P5Q6 |
| B4P9Q30 | Write a DAX measure for rolling 3-month average sales. | B4P5Q19 |
| B4P9Q32 | Write a DAX measure for headcount as of the month-end selected in a slicer. | B4P5Q25 |
| B4P9Q39 | The total row of your table does not equal the sum of the rows: why, and how do you fix it? | B4P5Q28 |
| B4P9Q52 | Write a DAX measure for each department's percentage share of total payroll. | B4P4Q41 |
| B4P9Q54 | How would you show opening headcount, hires, leavers and closing headcount as a waterfall? | B4P6Q60 |
| B4P9Q72 | How would you use DAX Studio alongside Performance Analyzer to investigate a slow measure? | B4P5Q34 |
| B4P9Q74 | How would you set up incremental refresh for a five-year sales table? | B4P7Q31 |
| B4P12Q4 | Walk me through a Power BI report you built from raw data to finished dashboard. | B4P9Q1 |
| B4P12Q9 | Can you run Power BI Desktop on a Mac, and what would you do if your laptop is a Mac? | B4P1Q31 |
