# Book 9 — Basic ML + AI Tools for Analysts | Part 9: GenAI for Analysts (ChatGPT/Claude/Copilot for SQL and Analysis, Prompts, Verifying Output, Privacy) 🟢🟡

**Target:** 100 questions | **Actual:** 100 questions
**Scope:** using generative AI tools (ChatGPT, Claude, Copilot) as an analyst's assistant for SQL, Excel/Power BI and analysis: basic concepts, prompt basics, checking AI output, data privacy and responsible use, and AI-workflow scenarios; LLM/RAG internals are Part 10, SQL/DAX mechanics belong to Books 2 and 4.

### Q1 ⭐⭐⭐ 🟢 How do you use AI tools such as ChatGPT, Claude or Copilot in your day-to-day analysis work?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What is a large language model (LLM), explained in two sentences to a non-technical HR manager?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is generative AI, and how is it different from the traditional analytics and machine learning you do as an analyst?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is an AI hallucination, and why is it dangerous when an analyst uses AI for numbers or SQL?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you verify AI-generated output before you use it in a report?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What is a prompt, and what are the basic ingredients of a good prompt for an analysis task?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 Which tasks in an analyst's job are good candidates for AI help, and which tasks would you keep fully human?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 Is it safe to paste company data into a public AI chatbot? What would you do instead?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 What kind of data should you never paste into ChatGPT or any external AI tool?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 Can AI replace a data analyst? Give your honest view in an interview.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 If an AI tool and your own manual calculation give different numbers, what do you do?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟢 How would you use ChatGPT or Claude to help write a SQL query when you are stuck?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟢 What information do you give an AI tool so that the SQL it writes uses your real tables and columns?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟢 Does AI-generated SQL that runs without errors mean the answer is correct? Explain.
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟢 Who is accountable if a wrong AI-generated number reaches the leadership dashboard: the tool or the analyst?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟢 What is Microsoft Copilot in Excel or Power BI, and what can it do for an analyst?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟢 What does it mean to be "AI-literate" as a data analyst in 2026?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟢 Why should you tell the AI which SQL dialect (MySQL, PostgreSQL, SQL Server) you use?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Describe one analysis in which you used an AI tool: what you asked, how you checked the answer, and what you decided yourself.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 AI wrote the query below for "average salary by department name". Find what is wrong and fix it.
Schema: employees(emp_id, name, dept_id, salary, hire_date); departments(dept_id, dept_name)
AI-generated query for "average salary by department name":
```sql
SELECT d.dept_name, AVG(e.salary)
FROM employees e JOIN departments d ON e.dept_id = d.dept_id;
```
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 Walk through a checklist you would apply to any AI-generated SQL before running it on production data.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 How would you explain the privacy risk of AI tools to a colleague who regularly pastes employee records into a chatbot?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🟡 Give an example of a weak prompt and a strong prompt for the same analysis request, and say why the strong one is better.
Request: "look at our attendance data and tell me what is wrong".
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🟡 What is the difference between asking an AI to write code for you and asking an AI to analyse your uploaded file directly? Which is easier to verify?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐⭐ 🟡 An AI assistant summarises your sales file and says "revenue grew in all four quarters". How would you check this claim before sending it on?
Quarterly revenue (Rs lakh), your own check: Q1 120, Q2 135, Q3 128, Q4 150.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐⭐ 🟡 What is data anonymisation or masking, and how would you apply it before sharing a sample with an AI tool?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐⭐ 🟡 How do you check an AI-generated Excel formula or DAX measure before putting it in a report?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐⭐ 🔴 Your manager says "just ask ChatGPT, it's faster" for a payroll reconciliation involving real employee names and salaries. How do you respond and what do you do?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 What is the difference between ChatGPT, Claude and Microsoft Copilot from a user's point of view? Keep it practical, without claiming which model is best.
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 What is a chatbot's "context window" in simple words, and why does it matter when you paste a big table?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 Why can the same prompt give different answers on different runs?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 What is prompt engineering, and is it a real skill for analysts or just hype?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 What does it mean to give an AI "context" in a prompt? Give an HR example.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 Why is it useful to tell the AI what role to play and what output format you want?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 What is a follow-up prompt, and how do you use iteration to improve a first answer?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 How can AI help you clean messy data, for example inconsistent department names, and what must you still check?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 How can AI help you write a summary of findings for a non-technical audience?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟢 How can you use AI to explain a SQL query or Excel formula that a colleague wrote?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟢 How can AI help you learn a new tool such as Power BI or pandas faster, and what are the risks of learning only through AI?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟢 What is the difference between a free consumer AI account and an enterprise AI account in terms of data handling? What would you check with your IT team?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟢 Can you trust the sources or links an AI gives you? What do you do before citing them?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟢 What is bias in AI output, and give a simple example relevant to hiring data.
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟢 Do you need to tell your manager or client when AI helped with an analysis? What is a reasonable practice?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟢 What does a company's AI usage policy usually cover, and how would you find out what yours allows?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟢 How do you ask an AI to explain its reasoning, and does a fluent explanation prove the answer is right?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟢 Why should you keep the AI-written query and your checks together in a short note?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟢 What can Copilot in Power BI do, such as suggesting DAX or summarising a report page, and why must you still review it?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟢 What can Copilot in Excel do, and why does it usually work better when data is in a proper Excel table?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Write a prompt that asks an AI to generate a SQL query for monthly attrition by department. What details must the prompt include?
Table: employees(emp_id, dept, join_date, exit_date). Dialect: PostgreSQL. Attrition = exits in month / employees at month start.
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 An AI wrote the query below for "each customer's first order date and total spend". What may go wrong, and how do you test it?
```sql
SELECT c.customer_id, MIN(o.order_date), SUM(o.amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items i ON o.order_id = i.order_id
GROUP BY c.customer_id;
```
Hint: orders has one row per order; order_items has several rows per order.
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 AI wrote this query for "employees earning more than their department average". Is it correct, and how would you test it with a tiny table?
```sql
SELECT emp_id FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 How would you ask an AI to debug a SQL error message? What do you paste and what do you leave out?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 What does "AI joined on the wrong key" look like in practice, and how do you spot it by checking row counts?
Before join: orders = 1,000 rows. After the AI's join with payments: 1,240 rows. Each order should have one payment record.
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 How would you ask an AI to convert a MySQL query into PostgreSQL or SQL Server, and how would you verify the converted query gives identical results?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 How would you use AI to translate a business question into a list of metrics and a data requirement, and what would you check yourself?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 What is few-shot prompting? Show how you would use two example rows to get consistent output when classifying survey comments.
Comments: "Manager is supportive", "Salary is too low", "Commute is long". Categories: Management, Pay, Logistics.
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 How would you use AI to classify 500 free-text survey comments into themes, and how would you check its accuracy before reporting percentages?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 What is a sensible way to ask AI to produce a pandas script to clean a file, and how do you test the script on a small sample first?
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 How would you ask AI to review your own SQL for performance or readability, and why should you still run EXPLAIN or test timings yourself?
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 Your AI-generated chart summary says "sales fell because of the price increase". What is wrong with that sentence from an analyst's point of view?
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🟡 What risks come from letting an AI tool run queries directly on a production database, and what safeguards would you want?
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🟡 How would you compare two AI answers to the same analysis question and decide which to trust?
<!-- ANSWER_PENDING -->

### Q63 ⭐⭐ 🟡 How would you document your use of AI for an analysis so someone else can reproduce and audit it?
<!-- ANSWER_PENDING -->

### Q64 ⭐⭐ 🟡 A DAX measure suggested by Copilot returns a number that is double what your pivot table shows. How do you investigate?
Pivot total sales = 5,00,000. Copilot measure total = 10,00,000.
<!-- ANSWER_PENDING -->

### Q65 ⭐⭐ 🟡 What is prompt injection in simple terms, and why should you be careful when asking AI to read text from emails or files that others wrote?
<!-- ANSWER_PENDING -->

### Q66 ⭐⭐ 🟡 How would you use an AI assistant to prepare for an interview or learn a topic without memorising wrong facts?
<!-- ANSWER_PENDING -->

### Q67 ⭐⭐ 🟡 What is the DPDP Act (India), at a one-line level, and why does it matter when you send employee or customer data to an AI tool? State only what you are sure of and say what you would confirm with legal.
<!-- ANSWER_PENDING -->

### Q68 ⭐⭐ 🔴 AI suggests a SQL query that returns revenue by region and the total matches finance within 0.1%. What further checks would you still do before trusting it?
<!-- ANSWER_PENDING -->

### Q69 ⭐⭐ 🔴 You are asked to build a monthly HR dashboard and your team wants AI to generate all DAX measures. Describe a workflow that is fast but safe.
<!-- ANSWER_PENDING -->

### Q70 ⭐⭐ 🔴 A colleague pasted a spreadsheet of employee IDs, salaries and performance ratings into a public chatbot last week. What should you do, and who should you inform?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟢 What is the difference between AI, machine learning and generative AI?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟢 What are tokens, and why do AI tools have limits on how much text you can send?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟢 What is a "temperature" setting in an AI tool, in simple words?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟢 What is an AI agent compared with a chatbot, in one sentence each?
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟢 What do you think are the biggest limitations of current AI tools for analysis work?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟢 Will AI change the skills a fresher data analyst needs to learn? What would you learn first?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟢 What is a custom GPT, project or reusable prompt template, and how could an analyst use one for repeated reporting tasks?
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🟢 Why might an AI tool give confident-sounding wrong answers on data from your own company?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🟡 What is Retrieval-Augmented Generation (RAG) in one paragraph, and how does it help an AI answer using company documents? (Detailed RAG is covered in Part 10.)
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🟡 How would you set up a simple evaluation of an AI tool for SQL help: a list of test questions with known answers and a pass rate?
Suppose you test 20 questions with known answers. The AI is correct on 15. What is the pass rate, and why is 20 questions a weak basis for a big decision?
<!-- ANSWER_PENDING -->

### Q81 ⭐ 🟡 What is chain-of-thought prompting, and when would you ask an AI to work step by step on a calculation?
<!-- ANSWER_PENDING -->

### Q82 ⭐ 🟡 AI says the mean tenure is 4.2 years and the median is 6.8. What should this make you check, and how would you ask AI to help while staying in control?
Tenure data from your file (years): 1, 1, 2, 2, 3, 3, 3, 4, 9, 14. Compute the mean and median yourself.
<!-- ANSWER_PENDING -->

### Q83 ⭐ 🟡 How would you use AI to generate realistic fake data for practice or testing a dashboard without exposing real employees?
<!-- ANSWER_PENDING -->

### Q84 ⭐ 🟡 An AI tool gives you a regex or Excel formula that works on 10 test rows. How would you test edge cases before applying it to 50,000 rows?
<!-- ANSWER_PENDING -->

### Q85 ⭐ 🟡 How would you explain to a manager the trade-off between speed gained from AI and time spent verifying?
Example: a manual task takes 3 hours; AI draft takes 20 minutes, review takes 60 minutes. Compute the time saved.
<!-- ANSWER_PENDING -->

### Q86 ⭐ 🟡 What is an AI-assisted text-to-SQL tool in a BI product, and what must be in place (clean schema, definitions) for it to be reliable?
<!-- ANSWER_PENDING -->

### Q87 ⭐ 🟡 What is a semantic layer or data dictionary, and why does giving it to an AI improve SQL accuracy?
<!-- ANSWER_PENDING -->

### Q88 ⭐ 🟡 What copyright or licensing questions might arise when you use AI-generated code or text in client deliverables?
<!-- ANSWER_PENDING -->

### Q89 ⭐ 🟡 What is the difference between Claude, ChatGPT and Copilot in how they handle uploaded files (such as CSV or Excel)? Say what you would test rather than what you assume.
<!-- ANSWER_PENDING -->

### Q90 ⭐ 🟡 AI provided a function in Python to calculate attrition rate. Read it and say whether the logic matches the usual definition.
```python
def attrition_rate(leavers, headcount_end):
    return leavers / headcount_end * 100
```
Data: leavers 12, headcount at start 200, headcount at end 190, so average headcount 195. State which denominator you would use and why.
<!-- ANSWER_PENDING -->

### Q91 ⭐ 🟡 You get two AI-written queries for "customers who bought in January but not in February". How do you decide which is correct?
Query A: LEFT JOIN feb ON customer_id WHERE feb.customer_id IS NULL
Query B: WHERE customer_id NOT IN (SELECT customer_id FROM feb_orders)
Hint: think about NULLs in feb_orders.customer_id.
<!-- ANSWER_PENDING -->

### Q92 ⭐ 🟡 How would you use an AI tool to draft an email or slide for stakeholders from your analysis, and what would you check before sending?
<!-- ANSWER_PENDING -->

### Q93 ⭐ 🟡 What is data leakage in the context of AI tools (not ML leakage): how can company information leave your control through prompts?
<!-- ANSWER_PENDING -->

### Q94 ⭐ 🟡 How would you handle a situation where your team lead tells you not to use AI at all, but you believe it would save time?
<!-- ANSWER_PENDING -->

### Q95 ⭐ 🔴 Design a safe AI-assisted workflow for a weekly attrition report from raw HRMS exports, covering data prep, prompting, checks, sign-off and privacy.
<!-- ANSWER_PENDING -->

### Q96 ⭐ 🔴 AI-written SQL gave a headline number that leadership already quoted, and you later discover a join fan-out inflated it by about 20%. How do you handle the correction?
<!-- ANSWER_PENDING -->

### Q97 ⭐ 🔴 How would you evaluate whether a new AI feature in your BI tool is good enough to roll out to non-technical business users?
<!-- ANSWER_PENDING -->

### Q98 ⭐ 🔴 You are asked to build a chat interface where HR managers ask questions about employee data in plain English. What risks would you raise first?
<!-- ANSWER_PENDING -->

### Q99 ⭐ 🔴 Explain why an AI answer can be well written, well formatted and still wrong, and what in the review process catches the different kinds of error (logic, data, definition, presentation).
<!-- ANSWER_PENDING -->

### Q100 ⭐ 🔴 How would you prepare for an interview round where AI tools are permitted, and what would you show the interviewer about how you work with them?
<!-- ANSWER_PENDING -->
