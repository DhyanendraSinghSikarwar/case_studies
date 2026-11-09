# Book 3 — Python & pandas for Analysts | Part 1: Python Basics (Variables, Types, Lists, Dicts, Loops, Functions) 🟢

**Target:** 70 questions | **Actual:** 73 questions
**Scope:** Python fundamentals asked in 0-3 year data/MIS/business analyst rounds: variables and types, lists, tuples, sets, dictionaries, loops, conditionals, functions and lambdas, with small HR-flavoured coding tasks.

### Q1 ⭐⭐⭐ 🟢 What is the difference between a list and a tuple in Python?
**Asked at:** TCS and Capgemini (single Glassdoor candidate reports, seen as snippets; the TCS one is dated July 2025); also reported in an Indium Software (Hyderabad) review, Sep 2025.
**What the interviewer is checking:** Whether you know "mutable versus immutable" and can say when each is used.
**Say this in the interview:** "Both hold an ordered collection of items. A list can be changed after it is created, a tuple cannot. I use a list for data that grows or changes, and a tuple for fixed data like a record that should not be edited."
**Explain simply:**
- A list uses square brackets `[ ]`; a tuple uses round brackets `( )`.
- Mutable means "can be changed in place" (add, remove, replace items). Lists are mutable, tuples are not.
- Because tuples cannot change, they are slightly faster and can be used as dictionary keys; lists cannot.
- Follow-up trap: a tuple that contains a list is not fully frozen, because the inner list can still change.
**Code (what you write in the interview):**
```python
# A list can change
departments = ["HR", "Finance", "IT"]
departments.append("Sales")
print(departments)

# A tuple cannot change
joining_details = ("E101", "Asha", "2024-01-15")
print(joining_details[1])
joining_details[1] = "Ravi"
```
**Output:**
```text
['HR', 'Finance', 'IT', 'Sales']
Asha
TypeError: 'tuple' object does not support item assignment
```
**What it means:** The list accepted a new item; Python refused to edit the tuple and raised an error.
**Likely follow-ups:** 1) *Why use a tuple at all?* To protect data from accidental edits and to use it as a dictionary key. 2) *How do you make a one-item tuple?* Add a comma: `("HR",)`.
**Common mistakes:** Saying "a tuple is faster so always use it"; forgetting the comma in a one-item tuple; thinking a tuple containing a list cannot change at all.

### Q2 ⭐⭐⭐ 🟢 What are the main built-in data types in Python (int, float, str, bool, list, tuple, dict, set), and how do you check the type of a value?
**Asked at:** commonly asked (no company-specific report found); basic Python screens (for example Indium Software, Sep 2025 review) cover types, lists and tuples.
**What the interviewer is checking:** That you know the basic building blocks and can name them with an example.
**Say this in the interview:** "int is a whole number, float a decimal, str text, bool True or False, list an ordered changeable collection, tuple an ordered fixed collection, dict key-value pairs, and set unique items. I check with `type()`."
**Explain simply:**
- `int`: 101 (employee ID). `float`: 52000.50 (salary with paise). `str`: "Asha". `bool`: True or False.
- `list` `[ ]` ordered and changeable; `tuple` `( )` ordered and fixed; `dict` `{key: value}` labelled data; `set` `{ }` unique items, no order.
- `type(x)` tells the exact type. `isinstance(x, float)` answers "is it a float?" with True or False.
**Code (what you write in the interview):**
```python
employee_id = 101
salary = 52000.50
name = "Asha"
is_active = True
skills = ["Excel", "SQL"]
joining_details = ("E101", "HR")
employee = {"name": "Asha", "salary": 52000}
departments = {"HR", "IT", "HR"}

print(type(employee_id))
print(type(salary))
print(type(name))
print(type(is_active))
print(type(skills))
print(type(joining_details))
print(type(employee))
print(type(departments))
print(isinstance(salary, float))
```
**Output:**
```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'list'>
<class 'tuple'>
<class 'dict'>
<class 'set'>
True
```
**What it means:** Each value reports its own type. The set kept only one "HR" because sets drop duplicates.
**Likely follow-ups:** 1) *What is the type of `{}`?* An empty dict, not a set; use `set()` for an empty set. 2) *What is `None`?* A special "no value" type (`NoneType`).
**Common mistakes:** Treating a phone number or ID as a number when it should be text (leading zeros are lost); confusing `{}` with an empty set.

### Q3 ⭐⭐⭐ 🟢 What is the difference between a list and a dictionary, and when would you use each for employee data?
**Asked at:** commonly asked (no company-specific report found); lists and dicts are listed as core data-analyst topics in prep guides (Dataquest, snippet).
**What the interviewer is checking:** Whether you pick the right structure: position-based (list) or label-based (dict).
**Say this in the interview:** "A list is an ordered collection I read by position, like a column of salaries. A dictionary stores labelled pairs I read by key, like one employee's name, department and salary. One employee is a dictionary; many employees is a list of dictionaries."
**Explain simply:**
- List: `[52000, 61000]`; you ask for "the first item" with `salaries[0]`.
- Dictionary: `{"name": "Asha", "salary": 52000}`; you ask by label with `employee["salary"]`.
- Use a list for many similar values (all salaries, all department names).
- Use a dict for one record with different fields, or for lookups (employee ID to name).
- A list of dictionaries is exactly how a table of employees looks before it becomes a pandas DataFrame.
**Code (what you write in the interview):**
```python
# List: an ordered collection, found by position
salaries = [52000, 61000, 48000]
print(salaries[0])

# Dictionary: labelled data, found by key
employee = {"name": "Asha", "department": "HR", "salary": 52000}
print(employee["salary"])
```
**Output:**
```text
52000
52000
```
**What it means:** Same salary, two ways to reach it: by position in a list, by label in a dictionary.
**Likely follow-ups:** 1) *Which is faster to search?* A dictionary lookup by key is much faster than scanning a long list. 2) *Can a dict key repeat?* No; a repeated key overwrites the earlier value.
**Common mistakes:** Storing a record as a list and forgetting what each position means; expecting dict keys to be duplicated.

### Q4 ⭐⭐⭐ 🟢 What does mutable versus immutable mean in Python, and which common types are which?
**Asked at:** commonly asked (no company-specific report found); it is the usual follow-up to list vs tuple (see Q1).
**What the interviewer is checking:** That you understand "changed in place" versus "a new object is made".
**Say this in the interview:** "Mutable means the object can be changed after it is created: list, dict and set. Immutable means it cannot: int, float, str, bool and tuple. When you seem to change an immutable value, Python actually builds a new one."
**Explain simply:**
- Mutable: list, dict, set.
- Immutable: int, float, str, bool, tuple.
- Why it matters: if two names point to the same mutable list, changing one changes both (see Q17).
- Immutable types are safe as dictionary keys; mutable ones are not.
**Code (what you write in the interview):**
```python
# Mutable: a list can be changed in place
skills = ["Excel", "SQL"]
skills[0] = "Python"
print(skills)

# Immutable: a string method makes a new string, the old one is untouched
name = "Asha"
new_name = name.upper()
print(name, new_name)

# Immutable: a tuple cannot be edited
grade = ("E101", "A")
grade[1] = "B"
```
**Output:**
```text
['Python', 'SQL']
Asha ASHA
TypeError: 'tuple' object does not support item assignment
```
**What it means:** The list was edited in place; the string stayed the same and gave back a new one; the tuple refused the edit.
**Likely follow-ups:** 1) *Is a tuple holding a list immutable?* The tuple's slots are fixed, but the inner list can still change. 2) *Mutable default argument trap?* See the function questions later in this part (not covered here).
**Common mistakes:** Thinking `name = name + "x"` changes the old string (it creates a new one); calling a tuple "completely unchangeable" when it holds a list.

### Q5 ⭐⭐⭐ 🟢 Write code to count how many times each department appears in a list of employee departments using a dictionary.
**Asked at:** Tiger Analytics (duplicate/frequency style tasks are listed in the repo's interview research); frequency counting is also a standard practice-platform pattern (Dataford, DataDriven snippets).
**What the interviewer is checking:** Loop plus dictionary logic: check if a key exists, then add or start at 1.
**Say this in the interview:** "I loop through the departments. If the department is already a key I add 1, otherwise I create it with 1."
**Explain simply:**
- Start with an empty dictionary: department is the key, count is the value.
- `in` checks whether the key is already there.
- `+= 1` means "add one to the current count".
- This is the plain version of what pandas `value_counts()` does.
**Sample data:** `departments = ["HR", "IT", "HR", "Finance", "IT", "HR"]`
**Code (what you write in the interview):**
```python
departments = ["HR", "IT", "HR", "Finance", "IT", "HR"]

department_counts = {}
for department in departments:
    if department in department_counts:
        department_counts[department] += 1
    else:
        department_counts[department] = 1

print(department_counts)
```
**Output:**
```text
{'HR': 3, 'IT': 2, 'Finance': 1}
```
**What it means:** HR has 3 employees, IT 2, Finance 1.
**Alternative:** shorter with `.get`: `department_counts[department] = department_counts.get(department, 0) + 1`. Or `collections.Counter(departments)`.
**Likely follow-ups:** 1) *How would you sort by highest count?* `sorted(department_counts.items(), key=lambda pair: pair[1], reverse=True)`. 2) *What if a department is None or has different casing?* Clean it first, otherwise "hr" and "HR" count separately.
**Common mistakes:** Writing `department_counts[department] += 1` without first creating the key (KeyError); forgetting to start at 1 for a new key.

### Q6 ⭐⭐⭐ 🟢 How do you loop through a dictionary to print each employee name and salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know `.items()` and unpacking two values in a for loop.
**Say this in the interview:** "I use `for name, salary in salaries.items()`. The `.items()` method gives key and value pairs, and the loop unpacks each pair into two names."
**Explain simply:**
- Looping over the dictionary directly gives only the keys.
- `.items()` gives (key, value) pairs; `.values()` gives only values.
- Use names that say what they are (`name`, `salary`), not `k` and `v`.
**Sample data:** `salaries = {"Asha": 52000, "Ravi": 61000, "Meena": 48000}`
**Code (what you write in the interview):**
```python
salaries = {"Asha": 52000, "Ravi": 61000, "Meena": 48000}

for name, salary in salaries.items():
    print(name, salary)
```
**Output:**
```text
Asha 52000
Ravi 61000
Meena 48000
```
**What it means:** One line per employee, in the order they were added.
**Likely follow-ups:** 1) *Can you change the dict while looping?* Adding or deleting keys during the loop raises an error; loop over a copy instead. 2) *What does a plain `for name in salaries` give?* Just the keys.
**Common mistakes:** Forgetting `.items()` and getting "too many values to unpack" or only keys; forgetting the brackets `()`.

### Q7 ⭐⭐⭐ 🟢 What is a list comprehension, and how is it different from a normal for loop?
**Asked at:** commonly asked (no company-specific report found); comprehensions are listed as a core DA topic in prep guides (Dataquest, snippet).
**What the interviewer is checking:** That you can build a list in one readable line and know when a plain loop is clearer.
**Say this in the interview:** "A list comprehension is a short way to build a new list from an existing one in a single line. It does the same job as a for loop with append, just more compactly. I use it for simple transform or filter tasks, and a normal loop when the logic gets long."
**Explain simply:**
- Pattern: `[what to keep for item in list if condition]`.
- The condition at the end is optional.
- It always produces a new list.
- It is not magic, just shorthand; the result is identical to the loop.
**Code (what you write in the interview):**
```python
salaries = [52000, 61000, 48000]

# Normal loop: 3 lines to give everyone a 5000 raise
salaries_after_raise = []
for salary in salaries:
    salaries_after_raise.append(salary + 5000)

# List comprehension: the same thing in 1 line
salaries_after_raise = [salary + 5000 for salary in salaries]
print(salaries_after_raise)
```
**Output:**
```text
[57000, 66000, 53000]
```
**What it means:** Both ways give the same new list; the comprehension is just shorter.
**Likely follow-ups:** 1) *Is it faster?* Usually a little, but readability is the main reason. 2) *Is there a dictionary version?* Yes, `{name: salary for ...}`.
**Common mistakes:** Cramming long logic into one line; forgetting that it creates a new list rather than editing the original.

### Q8 ⭐⭐⭐ 🟢 Write a list comprehension that returns only the salaries above 50000 from a list of salaries.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** The filter form of a comprehension (`if` at the end).
**Say this in the interview:** "`[salary for salary in salaries if salary > 50000]`. It keeps each salary only when the condition is true."
**Explain simply:**
- First `salary` is what goes into the new list.
- `for salary in salaries` loops through the original list.
- `if salary > 50000` decides who is kept.
- "Above 50000" means strictly greater; exactly 50000 is dropped. Use `>=` if you want it included.
**Sample data:** `salaries = [45000, 52000, 61000, 48000, 75000]`
**Code (what you write in the interview):**
```python
salaries = [45000, 52000, 61000, 48000, 75000]

high_salaries = [salary for salary in salaries if salary > 50000]
print(high_salaries)
```
**Output:**
```text
[52000, 61000, 75000]
```
**What it means:** Three of the five employees earn more than 50,000.
**Alternative:** the same with a loop: `for salary in salaries: if salary > 50000: high_salaries.append(salary)`.
**Likely follow-ups:** 1) *How do you count them?* `len(high_salaries)`. 2) *What if the list has missing values (None)?* Comparing None with a number raises an error; filter them out first with `if salary is not None and salary > 50000`.
**Common mistakes:** Writing the `if` before the `for` (that form needs an `else`); using `=` instead of `==` or `>`.

### Q9 ⭐⭐⭐ 🟢 What is the difference between a for loop and a while loop, and when do you use each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you choose the loop by "known items" versus "until a condition".
**Say this in the interview:** "A for loop goes through a known set of items, like every employee in a list. A while loop keeps repeating as long as a condition stays true, and I use it when I do not know in advance how many times. With while I must make sure the condition eventually becomes false, or it never ends."
**Explain simply:**
- `for`: "do this for each item". Safe, ends by itself.
- `while`: "keep doing this until something changes". Needs a line that changes the condition.
- Analysts use `for` almost all the time; `while` is rare (retrying, waiting for a condition).
- `range(1, 4)` gives 1, 2, 3 (the end is not included).
**Code (what you write in the interview):**
```python
# for loop: we know what to go through
for month in range(1, 4):
    print("Processing payroll for month", month)

# while loop: repeat until a condition changes
openings = 3
while openings > 0:
    print("Hiring, openings left:", openings)
    openings -= 1
```
**Output:**
```text
Processing payroll for month 1
Processing payroll for month 2
Processing payroll for month 3
Hiring, openings left: 3
Hiring, openings left: 2
Hiring, openings left: 1
```
**What it means:** The for loop ran 3 times because 3 months were given; the while loop ran until openings hit 0.
**Likely follow-ups:** 1) *What is an infinite loop?* A while loop whose condition never becomes false. 2) *How do you exit early?* `break` (see the loop-control questions in this part).
**Common mistakes:** Forgetting `openings -= 1` in the while loop (it runs forever); expecting `range(1, 4)` to include 4.

### Q10 ⭐⭐⭐ 🟢 How do you define a function in Python, and what is the difference between print and return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know `def`, parameters, and that `return` hands a value back while `print` only shows it.
**Say this in the interview:** "I define a function with `def`, a name, parameters in brackets, and an indented body. `return` sends a value back so I can store and reuse it. `print` only displays text on screen and the function gives back `None`."
**Explain simply:**
- `def calculate_bonus(salary):` starts the function; the indented lines are its body.
- `return` ends the function and gives a value to the caller, who can save it in a variable.
- `print` is for people to read; it cannot be reused in later calculations.
- A function with no `return` gives back `None`.
**Code (what you write in the interview):**
```python
def calculate_bonus(salary):
    bonus = salary * 0.10
    return bonus

def show_bonus(salary):
    print(salary * 0.10)

bonus = calculate_bonus(50000)
print("Return gave me:", bonus)

result = show_bonus(50000)
print("Print gave me:", result)
```
**Output:**
```text
Return gave me: 5000.0
5000.0
Print gave me: None
```
**What it means:** The returned bonus was saved and reusable; the print-only function showed 5000.0 but handed back `None`.
**Likely follow-ups:** 1) *Can a function return several values?* Yes, as a tuple: `return bonus, tax`. 2) *What are default arguments?* `def f(rate=0.10)` uses 0.10 when no value is given.
**Common mistakes:** Using `print` inside a function and then trying to use its result; code written after `return` never runs.

### Q11 ⭐⭐⭐ 🟢 What is a lambda function, and where do analysts typically use it (for example with sort or pandas apply)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know lambda is a small throwaway function and can name real uses.
**Say this in the interview:** "A lambda is a small one-line function without a name, written as `lambda input: output`. Analysts use it where a short rule is needed once, like the `key` in sort, or inside pandas `apply`."
**Explain simply:**
- `lambda salary: salary * 0.10` means "take salary, give back 10 percent of it".
- It is the same as a normal `def` function, just shorter, and limited to one expression.
- Typical uses: `sort(key=...)`, `sorted(..., key=...)`, `df["col"].apply(...)`.
- If the rule is long or reused, write a proper `def` function instead.
**Sample data:** a list of (name, salary) pairs.
**Code (what you write in the interview):**
```python
import pandas as pd

employees = [("Asha", 52000), ("Ravi", 61000), ("Meena", 48000)]

# Sort by salary (the second item of each pair)
employees.sort(key=lambda employee: employee[1])
print(employees)

# Use in pandas: add a 10% bonus column
df = pd.DataFrame(employees, columns=["name", "salary"])
df["bonus"] = df["salary"].apply(lambda salary: salary * 0.10)
print(df)
```
**Output:**
```text
[('Meena', 48000), ('Asha', 52000), ('Ravi', 61000)]
    name  salary   bonus
0  Meena   48000  4800.0
1   Asha   52000  5200.0
2   Ravi   61000  6100.0
```
**What it means:** The lambda told sort to compare salaries, and told pandas how to calculate each bonus.
**Likely follow-ups:** 1) *Is apply with lambda the fastest way?* No; `df["salary"] * 0.10` is faster and simpler when possible. 2) *Can a lambda have an if?* Yes: `lambda x: "High" if x > 50000 else "Low"`.
**Common mistakes:** Writing long multi-step logic in a lambda; using `apply` when a direct column calculation would do.

### Q12 ⭐⭐⭐ 🟢 Write a function that takes a list of salaries and returns the average.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Function basics plus `sum` and `len`, and thinking about an empty list.
**Say this in the interview:** "Average is total divided by count. I return `sum(salaries) / len(salaries)`. If the list could be empty I would check that first, because dividing by zero raises an error."
**Explain simply:**
- `sum()` adds all items; `len()` counts them.
- `/` always gives a decimal answer in Python 3.
- An empty list makes `len` zero, so the division fails (ZeroDivisionError). Mention this; adding the check shows care.
**Sample data:** salaries 52000, 61000, 48000.
**Code (what you write in the interview):**
```python
def average_salary(salaries):
    return sum(salaries) / len(salaries)

print(average_salary([52000, 61000, 48000]))
```
**Output:**
```text
53666.666666666664
```
**What it means:** The average salary is about 53,667 (round with `round(x, 2)` for a tidy report).
**Alternative:** safe version: `if len(salaries) == 0: return 0` (or `None`) before the division.
**Likely follow-ups:** 1) *What about None values in the list?* Remove them first, since `sum` fails on None. 2) *Median instead?* Sort the list and take the middle, or use the `statistics` module.
**Common mistakes:** Using `print` instead of `return`; dividing by a hard-coded number; forgetting the empty list case.

### Q13 ⭐⭐⭐ 🟢 How do you access, add, update and delete items in a dictionary, and what happens if a key does not exist?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic dictionary operations and awareness of KeyError.
**Say this in the interview:** "I read with `d[key]`, add or update with `d[key] = value` (same syntax for both), and delete with `del d[key]`. Reading a key that does not exist raises a KeyError, so I use `.get()` when the key might be missing."
**Explain simply:**
- Access: `employee["name"]`.
- Add: assign to a new key. Update: assign to an existing key. Python decides which by whether the key is there.
- Delete: `del employee["department"]` (or `employee.pop("department")`, which also returns the value).
- Missing key on read: KeyError. Missing key on assignment: no error, it is simply created.
**Code (what you write in the interview):**
```python
employee = {"name": "Asha", "salary": 52000}

print(employee["name"])               # access
employee["department"] = "HR"         # add a new key
employee["salary"] = 55000            # update an existing key
del employee["department"]            # delete
print(employee)

print(employee["age"])                # key does not exist
```
**Output:**
```text
Asha
{'name': 'Asha', 'salary': 55000}
KeyError: 'age'
```
**What it means:** The add, update and delete worked; asking for the missing key "age" crashed with a KeyError.
**Likely follow-ups:** 1) *How do you avoid the error?* Use `.get("age")` or check `"age" in employee`. 2) *What does `del` do on a missing key?* Also raises a KeyError; `pop(key, None)` is safe.
**Common mistakes:** Thinking assignment to a new key needs a special command; using `del` on a key that is not there.

### Q14 ⭐⭐⭐ 🟢 What is the difference between dict[key] and dict.get(key), and why does get avoid a KeyError?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle missing data safely.
**Say this in the interview:** "`dict[key]` raises a KeyError if the key is missing. `dict.get(key)` returns `None` instead, or a default value I choose, so the program keeps running. It avoids the error because it is written to check for the key first and return a fallback."
**Explain simply:**
- Use `[key]` when the key must exist and a crash is the right signal that data is wrong.
- Use `.get(key)` when missing is normal, such as an optional field like "age".
- `.get(key, default)` lets you give your own fallback, for example "Not available" or 0.
- `.get` never adds the key to the dictionary; it only reads.
**Code (what you write in the interview):**
```python
employee = {"name": "Asha", "salary": 52000}

print(employee.get("salary"))
print(employee.get("age"))
print(employee.get("age", "Not available"))
print(employee["age"])
```
**Output:**
```text
52000
None
Not available
KeyError: 'age'
```
**What it means:** `.get` quietly returned None or my default for the missing key; square brackets crashed.
**Likely follow-ups:** 1) *Where is `.get` handy?* Counting: `counts[key] = counts.get(key, 0) + 1`. 2) *Does `.get` tell you whether a key exists?* Not if the stored value is itself None; use `in` for that.
**Common mistakes:** Using `.get()` and then doing maths on the returned None; hiding real data problems by always using `.get`.

### Q15 ⭐⭐⭐ 🟢 How do you find the maximum, minimum, sum and length of a list without pandas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the built-in functions instead of writing loops.
**Say this in the interview:** "Python has built-in functions: `max()`, `min()`, `sum()` and `len()`. I just pass the list to each."
**Explain simply:**
- `max` biggest, `min` smallest, `sum` total, `len` how many items.
- Average is then `sum(salaries) / len(salaries)`.
- They work on lists, tuples and sets of numbers.
- An empty list breaks `max` and `min` (ValueError); `sum` of an empty list is 0.
**Sample data:** `salaries = [52000, 61000, 48000, 75000]`
**Code (what you write in the interview):**
```python
salaries = [52000, 61000, 48000, 75000]

print(max(salaries))
print(min(salaries))
print(sum(salaries))
print(len(salaries))
```
**Output:**
```text
75000
48000
236000
4
```
**What it means:** Highest salary 75,000, lowest 48,000, payroll total 236,000, across 4 employees.
**Likely follow-ups:** 1) *How would you do max without `max()`?* Keep a "highest so far" variable and update it in a loop. 2) *What if the list has None?* They fail; clean the list first.
**Common mistakes:** Naming a variable `sum` or `max` (it hides the built-in function); calling these on a list of text numbers like "52000".

### Q16 ⭐⭐⭐ 🟢 What is the difference between append(), extend() and insert() on a list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that append adds one item, extend adds many, insert adds at a position.
**Say this in the interview:** "`append` adds one item at the end. `extend` adds every item from another list at the end. `insert` puts one item at a position I choose. If I append a list, it goes in as one nested item, which is the common trap."
**Explain simply:**
- `append(x)`: one item, end of list.
- `extend(items)`: unpacks the items and adds each one at the end.
- `insert(index, x)`: adds at that position; later items shift right. Index 0 is the front.
- All three change the list in place and return `None`.
**Code (what you write in the interview):**
```python
team = ["Asha", "Ravi"]

team.append("Meena")
print(team)

team.extend(["Kiran", "Sana"])
print(team)

team.insert(0, "Dev")
print(team)

team.append(["Zoya", "Omar"])
print(team)
```
**Output:**
```text
['Asha', 'Ravi', 'Meena']
['Asha', 'Ravi', 'Meena', 'Kiran', 'Sana']
['Dev', 'Asha', 'Ravi', 'Meena', 'Kiran', 'Sana']
['Dev', 'Asha', 'Ravi', 'Meena', 'Kiran', 'Sana', ['Zoya', 'Omar']]
```
**What it means:** The last line shows the trap: appending a list adds it as a single nested item instead of two names.
**Likely follow-ups:** 1) *Join two lists into a new one?* `list_a + list_b`. 2) *Which is slowest?* `insert` at the front, because every item has to shift.
**Common mistakes:** Writing `team = team.append("x")` (this sets team to `None`); using append when extend was meant.

### Q17 ⭐⭐⭐ 🟢 What is the difference between == and is in Python?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate "same value" from "same object in memory".
**Say this in the interview:** "`==` checks whether two things have equal values. `is` checks whether they are the very same object in memory. Two separate lists with the same contents are equal but not identical. I use `is` mainly for `is None`."
**Explain simply:**
- `==` compares content: are the values equal?
- `is` compares identity: are both names pointing at the same object?
- `list_c = list_a` makes a second name for the same list, so `is` is True and changing one changes the other.
- Write `x is None`, not `x == None`, because None is a single object.
**Code (what you write in the interview):**
```python
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(list_a == list_b)
print(list_a is list_b)
print(list_a is list_c)

bonus = None
print(bonus is None)
```
**Output:**
```text
True
False
True
True
```
**What it means:** `list_a` and `list_b` hold equal values but are two different lists; `list_c` is the same list as `list_a`.
**Likely follow-ups:** 1) *Why does `is` sometimes seem to work for small numbers or short strings?* Python reuses some of them, but you should never rely on it (from memory, unverified). 2) *How do you check identity differently?* `id(a) == id(b)`.
**Common mistakes:** Using `is` to compare numbers or text; using `== None` instead of `is None`.

### Q18 ⭐⭐⭐ 🟢 Write a program that prints the numbers from 1 to 20 and labels each as even or odd.
**Asked at:** commonly asked (no company-specific report found); this is an even/odd classic for fresher Python screens (Indium Software review mentions "basic python codes", Sep 2025).
**What the interviewer is checking:** Loop, `range` end value, and the modulo operator `%`.
**Say this in the interview:** "I loop with `range(1, 21)` because the end is not included. For each number, `number % 2` is the remainder after dividing by 2: 0 means even, otherwise odd."
**Explain simply:**
- `range(1, 21)` gives 1 to 20; the last number (21) is never included.
- `%` (modulo) gives the remainder: `7 % 2` is 1, `8 % 2` is 0.
- `if` and `else` pick the label.
**Code (what you write in the interview):**
```python
for number in range(1, 21):
    if number % 2 == 0:
        print(number, "even")
    else:
        print(number, "odd")
```
**Output:**
```text
1 odd
2 even
3 odd
4 even
5 odd
6 even
7 odd
8 even
9 odd
10 even
11 odd
12 even
13 odd
14 even
15 odd
16 even
17 odd
18 even
19 odd
20 even
```
**What it means:** Every number from 1 to 20 appears once with the right label.
**Likely follow-ups:** 1) *How would you print only even numbers?* `range(2, 21, 2)`. 2) *HR use of `%`?* Spreading employees into 2 groups, or checking if an ID is even.
**Common mistakes:** `range(1, 20)` stops at 19; writing `=` instead of `==` in the condition.

### Q19 ⭐⭐⭐ 🟢 What is the difference between a set and a list, and how do you remove duplicates from a list using a set?
**Asked at:** commonly asked (no company-specific report found); duplicate handling appears in the repo's Tiger Analytics research (duplicate frequency, strings and lists).
**What the interviewer is checking:** That you know a set holds unique items with no order, and that converting a list to a set drops duplicates.
**Say this in the interview:** "A list is ordered and allows duplicates. A set keeps only unique items and has no order. To remove duplicates I wrap the list in `set()`, and `list()` turns it back into a list. The catch is that the original order is not kept."
**Explain simply:**
- List `[ ]`: ordered, duplicates allowed, items found by position.
- Set `{ }`: unique items only, no position, so `my_set[0]` does not work.
- Set membership checks (`x in my_set`) are very fast.
- Sets also do "who is in both" or "who is in one only" with `&` and `-`.
**Sample data:** `["E101", "E102", "E101", "E103", "E102"]` (employee IDs with repeats).
**Code (what you write in the interview):**
```python
employee_ids = ["E101", "E102", "E101", "E103", "E102"]

unique_ids = list(set(employee_ids))
print(sorted(unique_ids))
print(len(employee_ids), len(unique_ids))
```
**Output:**
```text
['E101', 'E102', 'E103']
5 3
```
**What it means:** The 5 IDs had only 3 distinct employees. I used `sorted` only to print them in a steady order, because a set has no fixed order.
**Likely follow-ups:** 1) *How do you remove duplicates and keep the order?* Loop and add only unseen items, or `list(dict.fromkeys(items))` (next question in this part). 2) *Can a set hold a list?* No, set items must be immutable (a tuple is fine).
**Common mistakes:** Expecting the original order after `set()`; writing `{}` for an empty set (that makes a dict).

### Q20 ⭐⭐⭐ 🟢 How do you remove duplicates from a list while keeping the original order?
**Asked at:** commonly asked (no company-specific report found); one Tiger Analytics report (single anecdote) mentions Python duplicate tasks on lists.
**What the interviewer is checking:** Whether you know that `set()` loses the order, and can still solve it simply.
**Say this in the interview:** "A set removes duplicates but does not keep order. So I loop through the list and add an item to a new list only if it is not already there. That keeps the first occurrence and the original order."
**Explain simply:**
- A **set** is a collection with no repeated items and no guaranteed order, so `list(set(x))` can shuffle your data.
- The loop checks `not in` (is it already in my new list?) before adding.
- Dictionaries remember insertion order (Python 3.7+), which gives a one-line trick (see Alternative).
- The loop version is slower on very large lists, because `not in` on a list scans it each time.
**Sample data:** departments of six employees: `["HR", "IT", "HR", "Sales", "IT", "HR"]`
**Code (what you write in the interview):**
```python
employee_departments = ["HR", "IT", "HR", "Sales", "IT", "HR"]

# Keep a department only the first time we see it
unique_departments = []
for department in employee_departments:
    if department not in unique_departments:
        unique_departments.append(department)

print(unique_departments)
```
**Output:**
```text
['HR', 'IT', 'Sales']
```
**What it means:** Each department appears once, in the order it first showed up.
**Alternative:** `list(dict.fromkeys(employee_departments))` gives the same `['HR', 'IT', 'Sales']` in one line and is faster. `list(set(employee_departments))` also removes duplicates but gave `['IT', 'Sales', 'HR']` in my run, so the order is not safe.
**Likely follow-ups:** 1) *Why is the loop slow on big data?* `not in` on a list checks item by item. 2) *How would you make it faster by hand?* Track seen items in a set.
**Common mistakes:** Using `list(set(...))` and assuming order is kept; saying a dictionary keeps order without knowing it needs Python 3.7 or later.

### Q21 ⭐⭐⭐ 🟢 What is list slicing, and what do my_list[1:4], my_list[::-1] and my_list[-1] return?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand zero-based positions and that the stop position is excluded.
**Say this in the interview:** "Slicing takes a piece of a list using `start:stop:step`. The start is included, the stop is not. `[1:4]` gives positions 1, 2, 3. `[::-1]` reverses the list. `[-1]` is the last item."
**Explain simply:**
- Positions (indexes) start at **0**, so the first item is `my_list[0]`.
- `[start:stop]` stops just before `stop`, so `[1:4]` returns 3 items.
- A negative number counts from the end: `-1` is last, `-2` is second last.
- The step controls the jump; `-1` means walk backwards.
- Slicing returns a new list and does not change the original.
**Sample data:** `my_list = [10, 20, 30, 40, 50, 60]`
**Code (what you write in the interview):**
```python
my_list = [10, 20, 30, 40, 50, 60]

print(my_list[1:4])   # from index 1 up to (not including) index 4
print(my_list[::-1])  # whole list, stepping backwards
print(my_list[-1])    # last item
```
**Output:**
```text
[20, 30, 40]
[60, 50, 40, 30, 20, 10]
60
```
**What it means:** A slice is a piece of the list; reversing and "last item" are just special slices.
**Likely follow-ups:** 1) *What does `my_list[:3]` give?* The first three items. 2) *What if the slice goes beyond the end?* Python does not error, it returns what exists. (`my_list[-1]` on an empty list does raise an IndexError.)
**Common mistakes:** Thinking the stop index is included; counting from 1; forgetting that `[::-1]` makes a new list rather than reversing in place.

### Q22 ⭐⭐⭐ 🟢 Write code to sort a list of employee names alphabetically and a list of salaries from highest to lowest.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic use of `sorted()` and the `reverse` option.
**Say this in the interview:** "`sorted()` gives alphabetical or ascending order by default. For highest to lowest I add `reverse=True`."
**Explain simply:**
- `sorted(names)` returns a new sorted list; the original is untouched.
- Text sorts A to Z, numbers sort small to large.
- `reverse=True` flips the order.
- Capital letters sort before small letters, so "asha" lands after "Ravi" (see Common mistakes).
**Sample data:** `["Ravi", "asha", "Meena", "John"]` and `[45000, 62000, 38000, 55000]`
**Code (what you write in the interview):**
```python
employee_names = ["Ravi", "asha", "Meena", "John"]
salaries = [45000, 62000, 38000, 55000]

# Alphabetical order (A to Z)
sorted_names = sorted(employee_names)

# Highest to lowest
sorted_salaries = sorted(salaries, reverse=True)

print(sorted_names)
print(sorted_salaries)
```
**Output:**
```text
['John', 'Meena', 'Ravi', 'asha']
[62000, 55000, 45000, 38000]
```
**What it means:** Salaries are ranked top to bottom. Note "asha" came last only because it starts with a small letter.
**Alternative:** `sorted(employee_names, key=str.lower)` ignores capitals and would put "asha" first.
**Likely follow-ups:** 1) *Can you sort in place?* Yes, `list.sort()` (see Q23). 2) *How do you sort names ignoring case?* Use `key=str.lower`.
**Common mistakes:** Forgetting `reverse=True`; expecting `sorted()` to change the original list; mixed-case names sorting unexpectedly.

### Q23 ⭐⭐⭐ 🟡 What is the difference between sort() and sorted() on a list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know one changes the list and one gives a new list, and that `sort()` returns `None`.
**Say this in the interview:** "`sorted()` returns a new sorted list and leaves the original alone. `list.sort()` sorts the original list itself and returns `None`."
**Explain simply:**
- `sorted(x)` works on any collection (list, tuple, dictionary keys) and always gives back a list.
- `x.sort()` is a list-only method that rearranges the list in place.
- Because `sort()` returns `None`, writing `x = x.sort()` wipes out your data variable by accident.
- Use `sorted()` when you still need the original order; `sort()` when you do not and want to save memory.
**Sample data:** `salaries = [45000, 62000, 38000]`
**Code (what you write in the interview):**
```python
salaries = [45000, 62000, 38000]

# sorted() returns a new list, the original stays the same
new_list = sorted(salaries)
print(new_list)
print(salaries)

# sort() changes the original list and returns None
result = salaries.sort()
print(salaries)
print(result)
```
**Output:**
```text
[38000, 45000, 62000]
[45000, 62000, 38000]
[38000, 45000, 62000]
None
```
**What it means:** After `sorted()` the original was unchanged; after `sort()` the original itself was reordered and the return value was `None`.
**Likely follow-ups:** 1) *Do both accept `reverse` and `key`?* Yes. 2) *Which is faster?* `sort()` is slightly cheaper because it makes no copy.
**Common mistakes:** `salaries = salaries.sort()` (the list becomes `None`); trying `.sort()` on a tuple (no such method).

### Q24 ⭐⭐⭐ 🟡 How do you sort a list of dictionaries (for example employees) by the salary key?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can use `key=` with a lambda to tell Python what to compare.
**Say this in the interview:** "I use `sorted()` with a `key`. The key is a small lambda function that picks the salary out of each dictionary, so Python sorts by that value."
**Explain simply:**
- A **lambda** is a tiny one-line function without a name: `lambda employee: employee["salary"]` means "given an employee, return their salary".
- Python cannot compare two dictionaries directly, so you must say which value to use.
- Add `reverse=True` for highest salary first.
**Sample data:** three employees with `name` and `salary`.
**Code (what you write in the interview):**
```python
employees = [
    {"name": "Ravi", "salary": 45000},
    {"name": "Asha", "salary": 62000},
    {"name": "Meena", "salary": 38000},
]

# The lambda tells Python to compare employees by their salary
employees_by_salary = sorted(employees, key=lambda employee: employee["salary"], reverse=True)

for employee in employees_by_salary:
    print(employee["name"], employee["salary"])
```
**Output:**
```text
Asha 62000
Ravi 45000
Meena 38000
```
**What it means:** Employees are listed from highest to lowest paid; each dictionary stays intact.
**Alternative:** `employees.sort(key=...)` does the same in place. For a pandas table you would use `df.sort_values("salary")`.
**Likely follow-ups:** 1) *How do you sort by two keys, such as department then salary?* Return a tuple: `key=lambda e: (e["department"], e["salary"])`. 2) *What if a dictionary has no salary key?* You get a KeyError; use `e.get("salary", 0)`.
**Common mistakes:** Calling `sorted(employees)` with no key (TypeError); forgetting `reverse=True`; a missing key in one record.

### Q25 ⭐⭐⭐ 🟡 What is the difference between a shallow copy and a deep copy, and why does list2 = list1 not make a real copy?
**Asked at:** commonly asked (no company-specific report found); Dataquest's prep article lists shallow vs deep copy as a core data analyst topic (search snippet only).
**What the interviewer is checking:** Whether you understand that variables point to objects, and that nested items stay shared in a shallow copy.
**Say this in the interview:** "`list2 = list1` just gives the same list a second name, so a change through one shows in the other. A shallow copy makes a new outer list but the inner lists are still shared. A deep copy copies everything, so it is fully independent."
**Explain simply:**
- Think of a variable as a **label** stuck on a box. `list2 = list1` sticks a second label on the same box.
- **Shallow copy** (`list1.copy()`): new outer box, but inner boxes are the same ones.
- **Deep copy** (`copy.deepcopy`): new outer box and new inner boxes.
- For a flat list of numbers, a shallow copy is enough. The difference only shows with nested items.
**Sample data:** a list of `[name, salary]` pairs.
**Code (what you write in the interview):**
```python
import copy

list1 = [["Ravi", 45000], ["Asha", 62000]]

same_list = list1                  # not a copy, just a second name
shallow = list1.copy()             # new outer list, same inner lists
deep = copy.deepcopy(list1)        # fully independent copy

list1[0][1] = 99999                # change an inner value

print("list1:  ", list1)
print("same:   ", same_list)
print("shallow:", shallow)
print("deep:   ", deep)
```
**Output:**
```text
list1:   [['Ravi', 99999], ['Asha', 62000]]
same:    [['Ravi', 99999], ['Asha', 62000]]
shallow: [['Ravi', 99999], ['Asha', 62000]]
deep:    [['Ravi', 45000], ['Asha', 62000]]
```
**What it means:** Only the deep copy kept Ravi's old salary; the other two moved with the original.
**Likely follow-ups:** 1) *Other ways to make a shallow copy?* `list1[:]` or `list(list1)`. 2) *What about pandas?* `df.copy()` makes a deep copy by default.
**Common mistakes:** Believing `list2 = list1` copies; thinking `.copy()` protects nested lists; using deep copy everywhere on huge data (slow and memory heavy).

### Q26 ⭐⭐ 🟢 What is the difference between int, float and str, and how do you convert one to another (type casting)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the basic types and the conversion functions.
**Say this in the interview:** "`int` is a whole number, `float` is a number with decimals, `str` is text. I convert with `int()`, `float()` and `str()`. Converting is called type casting."
**Explain simply:**
- `int`: 45000. `float`: 45000.5. `str`: "45000" (text, even if it looks like a number).
- Data read from files (CSV, forms) often arrives as text, so you convert before doing maths.
- `int(7.9)` gives 7: it cuts off decimals and does not round.
- `"45000" + "5"` joins text into `"450005"`; it does not add.
**Code (what you write in the interview):**
```python
salary_text = "45000"
salary_number = int(salary_text)        # str to int
salary_decimal = float(salary_text)     # str to float
salary_back_to_text = str(salary_number)  # int to str

print(type(salary_number), salary_number)
print(type(salary_decimal), salary_decimal)
print(type(salary_back_to_text), salary_back_to_text)
print(int(7.9))      # int() cuts off the decimal, it does not round
print("45000" + "5") # text joins, numbers would add
```
**Output:**
```text
<class 'int'> 45000
<class 'float'> 45000.0
<class 'str'> 45000
7
450005
```
**What it means:** The same digits behave differently depending on the type, so convert first.
**Likely follow-ups:** 1) *What if the text is not a number?* ValueError (see Q27). 2) *How do you round?* Use `round()`.
**Common mistakes:** Adding numbers stored as text; expecting `int(7.9)` to give 8; `int("45.5")` fails (convert with `float` first).

### Q27 ⭐⭐ 🟢 What happens when you try to convert the string 'abc' to an integer, and how do you handle it safely?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know about `ValueError` and `try`/`except`.
**Say this in the interview:** "Python raises a `ValueError` and the program stops. To handle it safely I put the conversion in a `try` block and catch `ValueError` in `except`, then decide what to do, like skip the row or use a default."
**Explain simply:**
- An **error (exception)** stops the program unless you catch it.
- `try` runs the risky code; `except ValueError` runs only if that error happens.
- Name the specific error (`ValueError`), not a bare `except`, so you do not hide other bugs.
- `int("45.5")` also fails; `int(" 45000 ")` works (spaces are ignored).
**Sample data:** `["45000", "abc", "52000"]`
**Code (what you write in the interview):**
```python
values = ["45000", "abc", "52000"]

for value in values:
    try:
        number = int(value)
        print(number)
    except ValueError:
        print("Not a valid number:", value)
```
**Output:**
```text
45000
Not a valid number: abc
52000
```
**What it means:** The bad value was reported and the loop carried on instead of crashing.
**Alternative:** In pandas, `pd.to_numeric(column, errors="coerce")` turns bad values into NaN (missing) instead of an error.
**Likely follow-ups:** 1) *What is the exact error message?* `invalid literal for int() with base 10: 'abc'`. 2) *What does `finally` do?* Runs whether or not an error happened.
**Common mistakes:** A bare `except:` that hides every error; not realising `"45.5"` also fails with `int()`.

### Q28 ⭐⭐ 🟢 What are Python's rules for naming variables, and what is the difference between a variable and a constant by convention?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowledge of the naming rules and awareness that Python has no true constants.
**Say this in the interview:** "A name can have letters, digits and underscores, cannot start with a digit, cannot have spaces and cannot be a keyword like `for`. Names are case sensitive. Python has no real constants, so by convention we write constants in CAPITALS to tell people not to change them."
**Explain simply:**
- Valid: `total_salary`, `_temp`, `employee2`. Invalid: `2employee`, `total salary`, `class`.
- `Salary` and `salary` are two different variables.
- Style (PEP 8, the official style guide): `snake_case` for variables, `CAPITAL_LETTERS` for constants.
- A constant is a value that should not change, such as `MAX_WORKING_DAYS`. Python will not stop you from changing it; it is a promise between people.
**Code (what you write in the interview):**
```python
# Good names
employee_name = "Ravi"
total_salary = 45000
MAX_WORKING_DAYS = 26   # constant by convention: capital letters

# Python allows changing it, the capitals are only a promise between people
MAX_WORKING_DAYS = 24
print(MAX_WORKING_DAYS)
```
**Output:**
```text
24
```
**What it means:** Python let the "constant" change, so protection comes only from team discipline.
**Likely follow-ups:** 1) *Can a name be `if`?* No, keywords are reserved. 2) *Why use descriptive names?* Others (and future you) can read the code.
**Common mistakes:** Starting with a digit; using spaces or hyphens; naming a variable `list` or `sum` (it hides the built-in function).

### Q29 ⭐⭐ 🟢 What is the difference between / , // and % operators in Python, with an example such as working days and weeks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know division, floor division and remainder.
**Say this in the interview:** "`/` is normal division with decimals. `//` is floor division, which keeps only the whole part. `%` is the remainder. For 23 working days in 5-day weeks: `/` gives 4.6, `//` gives 4 full weeks, and `%` gives 3 days left over."
**Explain simply:**
- `/` always returns a float (decimal number), even for `10 / 5` which gives `2.0`.
- `//` rounds **down** to a whole number (floor).
- `%` (modulo) is what is left after the whole divisions.
- `%` is also the classic even/odd check: `number % 2 == 0` means even.
**Code (what you write in the interview):**
```python
working_days = 23

weeks = working_days // 5           # full weeks
days_left_over = working_days % 5   # remaining days
exact_weeks = working_days / 5      # true division, with decimals

print(exact_weeks)
print(weeks)
print(days_left_over)
```
**Output:**
```text
4.6
4
3
```
**What it means:** 23 working days is 4 full weeks plus 3 extra days (4.6 weeks in decimals).
**Likely follow-ups:** 1) *What does `-7 // 2` give?* -4, because floor goes down, not toward zero. 2) *What does `divmod(23, 5)` do?* Returns `(4, 3)` in one step.
**Common mistakes:** Expecting `//` to round normally (it floors); expecting `/` to return an integer; dividing by zero (ZeroDivisionError).

### Q30 ⭐⭐ 🟢 What does the range() function do, and does range(5) include 5?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Zero-based counting and the excluded stop value.
**Say this in the interview:** "`range()` produces a sequence of numbers. `range(5)` gives 0, 1, 2, 3, 4, so it does not include 5. It starts at 0 and stops just before the number given."
**Explain simply:**
- `range(stop)`, `range(start, stop)` or `range(start, stop, step)`.
- The stop value is always excluded, like slicing.
- It does not build the whole list in memory; wrap it in `list()` to see the numbers.
- Handy for "do this N times".
**Code (what you write in the interview):**
```python
for number in range(5):
    print(number)

# start, stop, step
print(list(range(1, 11, 2)))
```
**Output:**
```text
0
1
2
3
4
[1, 3, 5, 7, 9]
```
**What it means:** Five numbers, 0 to 4; the second line shows odd numbers up to 9.
**Likely follow-ups:** 1) *How do you count 1 to 5?* `range(1, 6)`. 2) *How do you count down?* `range(5, 0, -1)`.
**Common mistakes:** Expecting 5 to be included; expecting `print(range(5))` to show numbers (it shows `range(0, 5)`).

### Q31 ⭐⭐ 🟢 What does enumerate() do, and why is it preferred over range(len(my_list))?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you write clean Python rather than index-juggling.
**Say this in the interview:** "`enumerate()` gives me the position and the item together as I loop. It is cleaner and less error-prone than `range(len(my_list))` where I have to index the list myself."
**Explain simply:**
- Each loop step returns a pair: (position, item).
- Positions start at 0; use `start=1` for human-style numbering (rows, ranks).
- With `range(len(x))` you write `x[i]` each time, which is more to type and easier to get wrong.
**Sample data:** `["Ravi", "Asha", "Meena"]`
**Code (what you write in the interview):**
```python
employee_names = ["Ravi", "Asha", "Meena"]

# start=1 so the numbering begins at 1 instead of 0
for position, name in enumerate(employee_names, start=1):
    print(position, name)
```
**Output:**
```text
1 Ravi
2 Asha
3 Meena
```
**What it means:** Each employee is printed with a running number.
**Likely follow-ups:** 1) *Does it work on other collections?* Yes, any iterable (list, tuple, string). 2) *When is `range(len())` still fine?* When you must change items by index.
**Common mistakes:** Forgetting that counting starts at 0; swapping the order (it is position first, then item).

### Q32 ⭐⭐ 🟢 How do you loop through two lists together (for example names and salaries) using zip()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can pair up related lists without index tricks.
**Say this in the interview:** "`zip()` pairs the first item of each list, then the second of each, and so on, so I can loop over both at once."
**Explain simply:**
- Think of a zip fastener: two sides meet tooth by tooth.
- Each step gives a pair, which you unpack into two names: `for name, salary in zip(...)`.
- If the lists have different lengths, `zip` stops at the shorter one and silently drops the rest.
- `dict(zip(names, salaries))` builds a dictionary from two lists.
**Sample data:** names `["Ravi", "Asha", "Meena"]`, salaries `[45000, 62000, 38000]`
**Code (what you write in the interview):**
```python
employee_names = ["Ravi", "Asha", "Meena"]
salaries = [45000, 62000, 38000]

for name, salary in zip(employee_names, salaries):
    print(name, "earns", salary)
```
**Output:**
```text
Ravi earns 45000
Asha earns 62000
Meena earns 38000
```
**What it means:** Each name is matched with the salary at the same position.
**Likely follow-ups:** 1) *What if lengths differ?* Stops at the shortest (my run: zipping 3 names with 2 numbers gave only 2 pairs). 2) *How do you make a dictionary?* `dict(zip(names, salaries))` gave `{'Ravi': 45000, 'Asha': 62000}` for two items.
**Common mistakes:** Assuming lists are the same length and losing data silently; reusing a `zip` object after it is used up.

### Q33 ⭐⭐ 🟢 What do break, continue and pass do inside a loop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Loop control basics.
**Say this in the interview:** "`break` stops the whole loop. `continue` skips the rest of this round and moves to the next item. `pass` does nothing; it is a placeholder where Python needs some code."
**Explain simply:**
- `break`: exit the loop right now (for example, stop when you find the employee).
- `continue`: skip just this item (for example, ignore absent rows).
- `pass`: an empty statement so an empty `if`, loop or function does not cause an error.
**Sample data:** attendance list `["present", "absent", "present", "leave", "present"]`
**Code (what you write in the interview):**
```python
attendance = ["present", "absent", "present", "leave", "present"]

for status in attendance:
    if status == "absent":
        continue          # skip this one, go to the next item
    if status == "leave":
        break             # stop the whole loop
    print(status)

def calculate_bonus():
    pass                  # placeholder, to be written later
```
**Output:**
```text
present
present
```
**What it means:** "absent" was skipped, then "leave" ended the loop, so the last "present" was never reached.
**Likely follow-ups:** 1) *Does `break` stop all nested loops?* No, only the innermost one. 2) *Does `continue` skip the `while` condition check?* No, it jumps back to it.
**Common mistakes:** Mixing up `break` and `continue`; using `continue` in a `while` loop before updating the counter (infinite loop).

### Q34 ⭐⭐ 🟢 How do you use if, elif and else to assign a rating band to a score, for example 5 = Outstanding, 3-4 = Meets, below 3 = Needs improvement?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured composite question.
**What the interviewer is checking:** Condition order and clean branching.
**Say this in the interview:** "Python checks the conditions from top to bottom and runs the first one that is true. `elif` means 'else if' and `else` catches everything left."
**Explain simply:**
- `if` is the first test, `elif` is any further test, `else` is the fallback (no condition).
- Only one branch runs.
- Order matters: put the most specific test first. After `score == 5` fails, `score >= 3` already means 3 or 4.
- Wrapping it in a function makes it reusable on a whole list (or with pandas `apply`).
**Code (what you write in the interview):**
```python
def rating_band(score):
    if score == 5:
        return "Outstanding"
    elif score >= 3:
        return "Meets"
    else:
        return "Needs improvement"

for score in [5, 4, 3, 2]:
    print(score, rating_band(score))
```
**Output:**
```text
5 Outstanding
4 Meets
3 Meets
2 Needs improvement
```
**What it means:** Each score gets exactly one band.
**Likely follow-ups:** 1) *What about a score of 4.5?* It lands in "Meets" with this code; ask the interviewer whether scores can be decimals and use `>= 5` if they can reach 5. 2) *How in pandas?* `df["score"].apply(rating_band)` or `pd.cut`.
**Common mistakes:** Writing `elif score == 3 or 4` (always true); wrong order, such as testing `>= 3` first so 5 becomes "Meets"; missing colons or indentation.

### Q35 ⭐⭐ 🟢 What are the Python boolean operators and, or, not, and what values count as False (truthy and falsy)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Logic basics and knowing what Python treats as "empty".
**Say this in the interview:** "`and` is True only if both sides are True, `or` is True if at least one is, and `not` flips the result. Falsy values are `False`, `None`, zero, and empty things like `''`, `[]`, `{}`. Everything else is truthy."
**Explain simply:**
- **Truthy** means "counts as True in an `if`"; **falsy** means "counts as False".
- Falsy: `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`.
- Truthy: anything else, including `"0"` (a non-empty text), `[0]` (a list with something in it), and `-1`.
- Handy: `if employees:` checks that a list is not empty.
**Code (what you write in the interview):**
```python
is_full_time = True
has_resigned = False

print(is_full_time and has_resigned)
print(is_full_time or has_resigned)
print(not has_resigned)

# Falsy values
for value in [0, 0.0, "", [], {}, None, False]:
    print(repr(value), bool(value))

print(bool("0"), bool([0]), bool(-1))
```
**Output:**
```text
False
True
True
0 False
0.0 False
'' False
[] False
{} False
None False
False False
True True True
```
**What it means:** All seven "empty or zero" values are False; non-empty things are True, even `"0"`.
**Likely follow-ups:** 1) *Is `NaN` falsy?* No, `bool(float("nan"))` is True (from memory, not run here). 2) *What does `and` return?* Python stops early, so it returns one of the two values, not always True or False.
**Common mistakes:** Thinking `"0"` or `"False"` is falsy; confusing `and`/`or` with `&`/`|` (those are for pandas columns and need brackets).

### Q36 ⭐⭐ 🟢 How do you check whether an item is present in a list or a dictionary using the in operator?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Membership testing, and that for dictionaries `in` checks keys.
**Say this in the interview:** "`item in my_list` returns True or False. For a dictionary, `in` checks the keys; to check values I use `.values()`."
**Explain simply:**
- Result is always `True` or `False`; `not in` tests the opposite.
- On a list it scans item by item; on a dictionary (or set) it jumps straight to the key, which is much faster on big data.
- Searching a dictionary by value needs `.values()`.
**Sample data:** `employee_ids = [101, 102, 103]`, `employee_salaries = {"Ravi": 45000, "Asha": 62000}`
**Code (what you write in the interview):**
```python
employee_ids = [101, 102, 103]
employee_salaries = {"Ravi": 45000, "Asha": 62000}

print(102 in employee_ids)
print(999 in employee_ids)
print("Ravi" in employee_salaries)      # checks keys
print(45000 in employee_salaries)       # values are not checked
print(45000 in employee_salaries.values())
```
**Output:**
```text
True
False
True
False
True
```
**What it means:** Employee 102 and the key "Ravi" exist; 45000 is a value, so you must look in `.values()`.
**Likely follow-ups:** 1) *Does it work on strings?* Yes, `"av" in "Ravi"` is True (substring). 2) *Which is faster on big data?* Set or dictionary (see Q55).
**Common mistakes:** Expecting `in` on a dictionary to search values; confusing `in` (test) with the `for x in` loop.

### Q37 ⭐⭐ 🟢 Write code to find the second highest salary in a list.
**Asked at:** commonly asked (no company-specific report found); the SQL version (second highest salary) is reported at Tiger Analytics (single anecdote), and the Python version is a standard follow-up.
**What the interviewer is checking:** Whether you handle duplicates in the top value.
**Say this in the interview:** "I remove duplicates with a set, sort from highest to lowest, and take the item at index 1. Removing duplicates matters because two people could share the top salary."
**Explain simply:**
- Without `set`, a list like `[62000, 62000, 55000]` would give 62000 again, which is the highest, not the second highest.
- `sorted(..., reverse=True)` puts the highest first; index 1 is the second one.
- You need at least two different salaries, otherwise index 1 does not exist (IndexError); check `len(unique_salaries) >= 2` if inputs can be short.
**Sample data:** `[45000, 62000, 62000, 38000, 55000]` (62000 appears twice)
**Code (what you write in the interview):**
```python
salaries = [45000, 62000, 62000, 38000, 55000]

# Remove duplicates, sort from highest to lowest, take the second one
unique_salaries = sorted(set(salaries), reverse=True)
second_highest = unique_salaries[1]

print(second_highest)
```
**Output:**
```text
55000
```
**What it means:** The top salary is 62000 (shared by two people); the second highest distinct salary is 55000.
**Alternative:** `max(s for s in salaries if s < max(salaries))` avoids sorting. Without the `set`, `sorted(salaries, reverse=True)[1]` returns 62000, which is the wrong answer here.
**Likely follow-ups:** 1) *Third highest?* Use index 2. 2) *Do it without sorting?* Find the maximum, then the maximum of the rest.
**Common mistakes:** Forgetting duplicates; not handling a list with fewer than two distinct values; sorting ascending and taking the wrong index.

### Q38 ⭐⭐ 🟢 Write code to merge two lists into one and to merge two dictionaries.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing `+` for lists and `{**a, **b}` (or `update`) for dictionaries, and what happens on duplicate keys.
**Say this in the interview:** "For lists I use `+`, which joins them end to end. For dictionaries I use `{**first, **second}`; if a key is in both, the second dictionary wins."
**Explain simply:**
- `list1 + list2` makes a new list; `list1.extend(list2)` changes `list1` itself.
- `{**a, **b}` unpacks both dictionaries into a new one.
- Duplicate keys are not kept twice: the **last** value overwrites the earlier one.
- Python 3.9+ also has `a | b` for dictionaries (checked: `{"a": 1} | {"a": 2}` gives `{'a': 2}`).
**Sample data:** two city lists and two salary dictionaries (Asha appears in both).
**Code (what you write in the interview):**
```python
hyderabad_employees = ["Ravi", "Asha"]
bengaluru_employees = ["Meena", "John"]
all_employees = hyderabad_employees + bengaluru_employees
print(all_employees)

salaries_jan = {"Ravi": 45000, "Asha": 62000}
salaries_feb = {"Asha": 65000, "Meena": 38000}
merged_salaries = {**salaries_jan, **salaries_feb}
print(merged_salaries)
```
**Output:**
```text
['Ravi', 'Asha', 'Meena', 'John']
{'Ravi': 45000, 'Asha': 65000, 'Meena': 38000}
```
**What it means:** The lists are joined in order. In the dictionary, Asha's February salary replaced her January one.
**Alternative:** `salaries_jan.update(salaries_feb)` merges into the first dictionary in place. `first_list.extend(second_list)` does the same for lists.
**Likely follow-ups:** 1) *How do you keep both salaries for a repeated key?* Store a list of values per key. 2) *Does a list merge remove duplicates?* No, wrap with a set or use the order-keeping loop from Q20.
**Common mistakes:** Trying `+` on dictionaries (TypeError); forgetting that the later dictionary overwrites; confusing `append` (adds one item) with `extend` (adds many).

### Q39 ⭐⭐ 🟢 What is a dictionary comprehension? Write one that maps each employee name to a bonus of 10 percent of salary.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a dictionary in one readable line, and do you know `.items()`?
**Say this in the interview:** "A dictionary comprehension builds a new dictionary from an existing one in a single line: `{key: value for ... in ...}`. Here the key is the name and the value is salary times 0.10."
**Explain simply:**
- A dictionary stores pairs: a key (the name) and a value (the salary), like a lookup table.
- A comprehension is a short way to write a loop that builds a new collection.
- `.items()` hands you each name and salary pair so you can unpack them in the loop.
- It is the same result as a normal loop with `bonus[name] = salary * 0.10`, just shorter.
**Sample data:** Asha 40000, Ravi 45000, Meena 52000.
**Code (what you write in the interview):**
```python
employees = {"Asha": 40000, "Ravi": 45000, "Meena": 52000}

# for each name, the bonus is 10 percent of the salary
bonus = {name: salary * 0.10 for name, salary in employees.items()}
print(bonus)
```
**Output:**
```
{'Asha': 4000.0, 'Ravi': 4500.0, 'Meena': 5200.0}
```
**What it means:** Each employee now has a bonus amount next to their name.
**Alternative:** A normal `for` loop that fills an empty dictionary gives the same result and is fine if you are nervous.
**Likely follow-ups:**
- Can you filter inside it? Yes, add `if salary > 40000` at the end.
- What if two names repeat? The later value overwrites the earlier one, because keys are unique.
**Common mistakes:** Looping over `employees` directly (you only get names, not salaries); forgetting the colon between key and value (that makes a set or an error).

### Q40 ⭐⭐ 🟢 How do you get the keys, values and key-value pairs of a dictionary (keys(), values(), items())?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic dictionary navigation.
**Say this in the interview:** "`keys()` gives the names of the entries, `values()` gives what is stored, and `items()` gives both together as pairs, which is what I use in loops."
**Explain simply:**
- `keys()`: all the labels (employee names).
- `values()`: all the stored data (salaries).
- `items()`: each (key, value) pair as a small tuple (a fixed pair like `('Asha', 40000)`).
- These return "views" that follow the dictionary; wrap in `list()` to see them as a list.
**Sample data:** Asha 40000, Ravi 45000, Meena 52000.
**Code (what you write in the interview):**
```python
employee_salary = {"Asha": 40000, "Ravi": 45000, "Meena": 52000}

print(list(employee_salary.keys()))
print(list(employee_salary.values()))
print(list(employee_salary.items()))

# loop over names and salaries together
for name, salary in employee_salary.items():
    print(name, salary)
```
**Output:**
```
['Asha', 'Ravi', 'Meena']
[40000, 45000, 52000]
[('Asha', 40000), ('Ravi', 45000), ('Meena', 52000)]
Asha 40000
Ravi 45000
Meena 52000
```
**What it means:** Three ways to look at the same data: only names, only salaries, or both.
**Likely follow-ups:**
- What does a plain `for x in dict` give? Only the keys.
- Is order kept? Yes, insertion order (Python 3.7 and later).
**Common mistakes:** Expecting `keys()` to print as a plain list (it prints `dict_keys([...])`); looping with one variable over `items()` and getting tuples.

### Q41 ⭐⭐ 🟢 What is a nested list or nested dictionary, and how do you access an inner value such as the city of an employee?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you read layered data, like a JSON file from an HR system?
**Say this in the interview:** "Nested means a list or dictionary inside another one. You step in one level at a time: `employee['address']['city']`."
**Explain simply:**
- A nested dictionary is a dictionary whose value is another dictionary (an employee with an address block).
- A nested list is a list of lists, accessed with two positions: `team[1][0]`.
- Read it left to right: first the outer key or position, then the inner one.
- Real data (JSON from an API) is usually nested like this.
**Sample data:** one employee with an address; a small team list; a list of employee dictionaries.
**Code (what you write in the interview):**
```python
employee = {
    "name": "Asha",
    "salary": 40000,
    "address": {"city": "Hyderabad", "pincode": 500081},
}
print(employee["address"]["city"])

# nested list: position 1 is Ravi's row, position 0 is his name
team = [["Asha", "HR"], ["Ravi", "Sales"]]
print(team[1][0])

# list of dictionaries, each holding a dictionary
employees = [
    {"name": "Asha", "address": {"city": "Hyderabad"}},
    {"name": "Ravi", "address": {"city": "Pune"}},
]
print(employees[1]["address"]["city"])
```
**Output:**
```
Hyderabad
Ravi
Pune
```
**What it means:** Each pair of brackets goes one level deeper.
**Likely follow-ups:**
- What if the key is missing? `[]` raises KeyError; use `.get("address", {}).get("city")` for a safe read.
**Common mistakes:** Writing `employee["city"]` (the city is one level down); mixing up list positions (start at 0) with dictionary keys.

### Q42 ⭐⭐ 🟢 What is the difference between parameters and arguments, and what are default arguments?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Correct vocabulary and comfort with function signatures.
**Say this in the interview:** "Parameters are the names in the function definition; arguments are the actual values I pass when I call it. A default argument is a value used when the caller does not give one."
**Explain simply:**
- Parameter: the empty slot (`base`), like a blank on a form.
- Argument: what you fill in (`40000`).
- Default argument: a pre-filled slot (`bonus_percent=10`) used when you skip it.
- Parameters with defaults must come after those without.
**Sample data:** base salary 40000, bonus percent default 10.
**Code (what you write in the interview):**
```python
def final_salary(base, bonus_percent=10):
    return base + base * bonus_percent / 100

print(final_salary(40000))                     # uses the default 10
print(final_salary(40000, 20))                 # overrides the default
print(final_salary(base=40000, bonus_percent=5))  # named arguments
```
**Output:**
```
44000.0
48000.0
42000.0
```
**What it means:** Without a second value the 10 percent default applies; passing one replaces it.
**Likely follow-ups:**
- Positional vs keyword arguments? Positional goes by order; keyword goes by name and order does not matter.
- Any danger with defaults? Yes, mutable defaults (see Q46).
**Common mistakes:** Using the two words as if they were identical; putting a default parameter before a non-default one (SyntaxError).

### Q43 ⭐⭐ 🟢 What are *args and **kwargs in a function definition?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how a function accepts a flexible number of inputs?
**Say this in the interview:** "`*args` collects any extra positional values into a tuple; `**kwargs` collects extra named values into a dictionary. The names args and kwargs are just convention."
**Explain simply:**
- `*args`: "as many values as you like", stored as a tuple.
- `**kwargs`: "as many name=value pairs as you like", stored as a dictionary.
- Useful when you do not know in advance how many inputs will come.
- The stars are what matter, not the words.
**Sample data:** three salaries; one employee given as name=value pairs.
**Code (what you write in the interview):**
```python
def total_pay(*salaries):
    return sum(salaries)

def show_employee(**details):
    for key, value in details.items():
        print(key, value)

print(total_pay(40000, 45000, 52000))
show_employee(name="Asha", department="HR")
```
**Output:**
```
137000
name Asha
department HR
```
**What it means:** The first function adds any number of salaries; the second prints any details it is given.
**Likely follow-ups:**
- Can you use both? Yes, `def f(a, *args, **kwargs)`, in that order.
**Common mistakes:** Thinking `args` is a list (it is a tuple); using one star when passing named values.

### Q44 ⭐⭐ 🟢 What is the difference between local and global variables, and what does the global keyword do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding of variable scope (where a name is visible).
**Say this in the interview:** "A local variable lives only inside its function. A global one is defined outside and visible everywhere to read. To change a global inside a function, you must declare it with `global`; I usually avoid that and return values instead."
**Explain simply:**
- Local: created inside a function, disappears when it ends.
- Global: created at the top level of the file.
- Assigning to a name inside a function creates a new local variable, even if a global has the same name.
- `global` tells Python "I mean the outer one".
**Sample data:** headcount = 100.
**Code (what you write in the interview):**
```python
headcount = 100

def hire_one():
    global headcount          # change the outer variable
    headcount = headcount + 1

def local_example():
    headcount = 5             # a new local variable, outer one untouched
    return headcount

print(local_example())
print(headcount)
hire_one()
print(headcount)
```
**Output:**
```
5
100
101
```
**What it means:** The local copy did not change the global; only `hire_one` with `global` did.
**Likely follow-ups:**
- Why avoid global? It makes code hard to trace and test; pass inputs and return outputs.
**Common mistakes:** Assigning to a global inside a function without `global` (it silently makes a local, or raises UnboundLocalError if you read it first).

### Q45 ⭐⭐ 🟢 How do you return multiple values from a function, and how do you unpack them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know functions can return a tuple and that unpacking assigns names in one line?
**Say this in the interview:** "I return the values separated by commas; Python packs them into a tuple. The caller unpacks them into separate variables."
**Explain simply:**
- `return a, b, c` really returns one tuple.
- Unpacking: `x, y, z = function()` splits it into three names.
- The number of names must match the number of values.
**Sample data:** salaries 40000, 45000, 52000.
**Code (what you write in the interview):**
```python
def salary_summary(salaries):
    return min(salaries), max(salaries), sum(salaries) / len(salaries)

lowest, highest, average = salary_summary([40000, 45000, 52000])
print(lowest, highest, average)
print(salary_summary([40000, 45000, 52000]))   # without unpacking: one tuple
```
**Output:**
```
40000 52000 45666.666666666664
(40000, 52000, 45666.666666666664)
```
**What it means:** One call gives three results; unpacking gives each its own name.
**Alternative:** Return a dictionary (`{"min": ..., "max": ...}`) when there are many values and names help readability.
**Likely follow-ups:**
- What if the counts do not match? ValueError.
**Common mistakes:** Calling the function three times instead of once; wrong number of names on the left.

### Q46 ⭐⭐ 🟡 What is the mutable default argument trap, for example def add(item, bucket=[]), and how do you fix it?
**Asked at:** reported in interviews (Glassdoor Deliveroo question on an empty list as a default argument, undated, not a data analyst role; also common in Python prep blogs)
**What the interviewer is checking:** Do you understand that default values are created once, when the function is defined?
**Say this in the interview:** "The default list is created once and shared by every call, so items pile up between calls. The fix is `bucket=None` and creating a fresh list inside the function."
**Explain simply:**
- Python builds the default value one time, at `def`, not at each call.
- A list is mutable (can be changed in place), so the shared list keeps growing.
- Safe defaults (numbers, strings, None) are immutable, so this never bites them.
- The `None` pattern gives each call its own new list.
**Sample data:** two names added in two separate calls.
**Code (what you write in the interview):**
```python
def add_bad(item, bucket=[]):
    bucket.append(item)
    return bucket

def add_good(item, bucket=None):
    if bucket is None:
        bucket = []          # a fresh list for every call
    bucket.append(item)
    return bucket

print(add_bad("Asha"))
print(add_bad("Ravi"))
print(add_good("Asha"))
print(add_good("Ravi"))
```
**Output:**
```
['Asha']
['Asha', 'Ravi']
['Asha']
['Ravi']
```
**What it means:** The bad version remembered Asha from the first call; the good version starts clean each time.
**Likely follow-ups:**
- Does it affect dict and set defaults too? Yes, any mutable type.
**Common mistakes:** Writing `if not bucket:` (it also replaces a list the caller passed that is empty); thinking the bug appears on the first call (it only shows on later calls).

### Q47 ⭐⭐ 🟡 How do you use map(), filter() and sorted() with a lambda, and when is a list comprehension better?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Comfort with lambdas and a sense of readable style.
**Say this in the interview:** "`map` applies a function to every item, `filter` keeps items where the function is True, and `sorted` with `key=` sorts by whatever the lambda returns. For simple cases I prefer a list comprehension because it reads more clearly."
**Explain simply:**
- A lambda is a tiny one-line function with no name: `lambda salary: salary * 1.10`.
- `map` and `filter` return lazy objects, so wrap them in `list()`.
- `sorted(..., key=lambda e: e[1])` sorts by the second item of each pair.
- Comprehensions are usually clearer and handle map plus filter together.
**Sample data:** salaries 40000, 45000, 52000, 61000; employees as (name, salary) pairs.
**Code (what you write in the interview):**
```python
salaries = [40000, 45000, 52000, 61000]
employees = [("Asha", 40000), ("Ravi", 45000), ("Meena", 52000)]

# map: add 10 percent to every salary
with_bonus = list(map(lambda salary: salary * 1.10, salaries))

# filter: keep salaries above 50000
high_salaries = list(filter(lambda salary: salary > 50000, salaries))

# sorted: highest salary first
highest_first = sorted(employees, key=lambda employee: employee[1], reverse=True)

print(with_bonus)
print(high_salaries)
print(highest_first)

# the comprehension version of the filter
print([salary for salary in salaries if salary > 50000])
```
**Output:**
```
[44000.0, 49500.00000000001, 57200.00000000001, 67100.0]
[52000, 61000]
[('Meena', 52000), ('Ravi', 45000), ('Asha', 40000)]
[52000, 61000]
```
**What it means:** Same results either way; the tiny decimals like 49500.00000000001 are normal float rounding.
**Likely follow-ups:**
- Why `list()` around map? It returns an iterator, not a list.
**Common mistakes:** Forgetting `list()`; writing long, hard to read lambdas (use a normal `def` then).

### Q48 ⭐⭐ 🟡 What is the difference between a list and a generator, and why would you use a generator for a huge file of records?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of memory use and lazy evaluation.
**Say this in the interview:** "A list holds all items in memory at once. A generator produces one item at a time when asked, so memory stays small. For a huge file I would read it line by line with a generator."
**Explain simply:**
- List: all values stored now. Generator: a recipe that makes the next value on demand.
- A generator can be used once; after it is exhausted it gives nothing.
- Written with `yield` in a function, or with round brackets `( ... for ...)`.
- Best when you only need to process records one by one (counting, filtering).
**Sample data:** one million numbers, and a tiny three-item generator.
**Code (what you write in the interview):**
```python
import sys

records_list = [number for number in range(1_000_000)]
records_generator = (number for number in range(1_000_000))
print(sys.getsizeof(records_list))
print(sys.getsizeof(records_generator))

# a generator that reads a big file one line at a time
def read_records(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()

squares = (n * n for n in range(3))
print(next(squares))
print(next(squares))
print(list(squares))
print(list(squares))   # already used up
```
**Output:**
```
8448728
192
0
1
[4]
[]
```
**What it means:** The list takes about 8 MB; the generator about 192 bytes. Once consumed, a generator is empty.
**Likely follow-ups:**
- Can you index a generator? No, only loop through it or call `next()`.
- pandas equivalent? `read_csv(..., chunksize=...)` reads in pieces.
**Common mistakes:** Trying to use a generator twice; calling `len()` on it (not supported). Sizes vary slightly by Python version.

### Q49 ⭐⭐ 🟡 Write a function that takes a list of employee dictionaries and returns the attrition rate (percentage with 'left': True).
**Asked at:** HR-flavoured composite; no company-specific report found
**What the interviewer is checking:** Loop plus counter plus percentage, and handling an empty list.
**Say this in the interview:** "I count how many employees have `left` equal to True, divide by the total, and multiply by 100. I guard against an empty list to avoid dividing by zero."
**Explain simply:**
- Attrition rate = employees who left / total employees x 100.
- Use a counter that goes up by one for each leaver.
- Dividing by zero crashes, so return 0 for an empty list.
**Sample data:** five employees, two have left (Ravi, John).
**Code (what you write in the interview):**
```python
def attrition_rate(employees):
    total = len(employees)
    if total == 0:
        return 0                      # avoid dividing by zero
    left_count = 0
    for employee in employees:
        if employee["left"] == True:
            left_count = left_count + 1
    return left_count / total * 100

employees = [
    {"name": "Asha", "left": False},
    {"name": "Ravi", "left": True},
    {"name": "Meena", "left": False},
    {"name": "John", "left": True},
    {"name": "Priya", "left": False},
]
print(attrition_rate(employees))
print(attrition_rate([]))
```
**Output:**
```
40.0
0
```
**What it means:** 2 of 5 employees left, so attrition is 40 percent.
**Alternative:** `sum(employee["left"] for employee in employees) / len(employees) * 100` (True counts as 1).
**Likely follow-ups:**
- How would you do this in pandas? `df["left"].mean() * 100`.
- Is this rate annual? Only if the data covers one year; real attrition often uses average headcount as the denominator.
**Common mistakes:** Forgetting `* 100`; integer thinking (in Python 3 `/` gives decimals, fine); missing `left` key in some records.

### Q50 ⭐⭐ 🟡 Write a function that groups employees by department into a dictionary of lists (use defaultdict or setdefault).
**Asked at:** commonly asked (no company-specific report found); grouping and frequency tasks are a standard coding-round pattern on practice platforms
**What the interviewer is checking:** Can you build a grouped structure without a pandas groupby?
**Say this in the interview:** "I loop through the employees and append each name to the list for its department. `defaultdict(list)` creates the empty list automatically the first time a department appears."
**Explain simply:**
- A normal dictionary raises KeyError for a new department; `defaultdict(list)` quietly starts an empty list.
- `setdefault(key, [])` does the same job on a plain dictionary.
- The result is like a pivot: department to list of names.
**Sample data:** four employees across HR, Sales, IT.
**Code (what you write in the interview):**
```python
from collections import defaultdict

def group_by_department(employees):
    groups = defaultdict(list)
    for employee in employees:
        groups[employee["department"]].append(employee["name"])
    return dict(groups)

employees = [
    {"name": "Asha", "department": "HR"},
    {"name": "Ravi", "department": "Sales"},
    {"name": "Meena", "department": "HR"},
    {"name": "John", "department": "IT"},
]
print(group_by_department(employees))
```
**Output:**
```
{'HR': ['Asha', 'Meena'], 'Sales': ['Ravi'], 'IT': ['John']}
```
**What it means:** Each department holds the names of its people.
**Alternative:** Plain dictionary version, same output:
```python
groups = {}
for employee in employees:
    groups.setdefault(employee["department"], []).append(employee["name"])
```
**Likely follow-ups:**
- Pandas equivalent? `df.groupby("department")["name"].apply(list)`.
**Common mistakes:** `groups[dept] = [name]` inside the loop (overwrites earlier names); forgetting the import.

### Q51 ⭐⭐ 🟡 What is collections.Counter, and how do you get the top 3 most common values from a list?
**Asked at:** commonly asked (no company-specific report found); frequency counting is a standard coding-round pattern
**What the interviewer is checking:** Do you know the built-in tool for counting?
**Say this in the interview:** "`Counter` counts how many times each item appears and behaves like a dictionary. `most_common(3)` returns the top three as (item, count) pairs."
**Explain simply:**
- It replaces the manual loop with a counting dictionary (see Q5).
- `most_common(n)` sorts by count, highest first.
- Ties keep first-seen order.
**Sample data:** ten department entries.
**Code (what you write in the interview):**
```python
from collections import Counter

departments = ["HR", "Sales", "IT", "Sales", "HR", "Sales", "Finance", "IT", "Sales", "HR"]

counts = Counter(departments)
print(counts)
print(counts.most_common(3))
```
**Output:**
```
Counter({'Sales': 4, 'HR': 3, 'IT': 2, 'Finance': 1})
[('Sales', 4), ('HR', 3), ('IT', 2)]
```
**What it means:** Sales is the biggest department in this list, then HR, then IT.
**Likely follow-ups:**
- Pandas equivalent? `Series.value_counts().head(3)`.
- Missing item? `counts["Legal"]` gives 0, no error.
**Common mistakes:** Forgetting to import; expecting `most_common()` without a number to return only one (it returns all, sorted).

### Q52 ⭐⭐ 🟡 Why is looping over rows slower than vectorised operations in pandas or NumPy, and when is a plain loop still acceptable?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you think in whole columns, not row by row?
**Say this in the interview:** "A Python loop handles one value at a time with interpreter overhead each step. A vectorised operation runs the whole column in optimised compiled code, so it is much faster. A loop is fine for small data or logic that cannot be expressed on a column."
**Explain simply:**
- Vectorised means "one command applied to the whole column at once".
- pandas and NumPy do the repeated work in fast compiled code (C) underneath.
- Loops are acceptable for a few hundred rows, for calling an external service per row, or complex step-by-step rules; readability matters too.
- Even then, try `np.where`, `.map`, or `.apply` first.
**Sample data:** one million salaries (1 to 1,000,000), add a 10 percent bonus.
**Code (what you write in the interview):**
```python
import pandas as pd

salaries = pd.Series(range(1, 1_000_001))

# loop version: one value at a time
bonus_loop = []
for salary in salaries:
    bonus_loop.append(salary * 0.10)

# vectorised version: the whole column at once
bonus_vectorised = salaries * 0.10
```
**Output:** The code prints nothing. Timing it separately on this machine (single run, varies by machine): loop about 0.109 seconds, vectorised about 0.0066 seconds, roughly 15 times faster here; the gap grows with more complex work.
**What it means:** Same answer, far less time with the column operation.
**Likely follow-ups:**
- Why is `iterrows()` especially slow? It builds a new Series object for every row.
**Common mistakes:** Using `iterrows()` to compute a new column; assuming loops are always wrong.

### Q53 ⭐⭐ 🟡 What is the output of a loop that modifies a list while iterating over it, and how do you avoid the problem?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the skipped-item bug?
**Say this in the interview:** "Removing items from a list while looping over it makes the loop skip elements, because the positions shift. I build a new list with a comprehension, or loop over a copy."
**Explain simply:**
- The loop walks by position (0, 1, 2...). When you remove an item, the next item slides into the current position, and the loop moves past it.
- Result: some items are never checked.
- Safe fixes: a comprehension that keeps what you want, or loop over `numbers[:]` (a copy).
**Sample data:** `[2, 4, 6, 8, 9]`, we want to remove the even numbers.
**Code (what you write in the interview):**
```python
numbers = [2, 4, 6, 8, 9]
for number in numbers:
    if number % 2 == 0:
        numbers.remove(number)       # buggy: changes the list mid-loop
print(numbers)

numbers = [2, 4, 6, 8, 9]
# safe: build a new list of the items to keep
odd_numbers = [number for number in numbers if number % 2 != 0]
print(odd_numbers)
```
**Output:**
```
[4, 8, 9]
[9]
```
**What it means:** The buggy loop left 4 and 8 behind because it skipped them after each removal.
**Likely follow-ups:**
- Same problem for dictionaries? Python raises an error if you change dictionary size while looping.
**Common mistakes:** Believing the loop "just works" because it ran without an error; the bug is silent.

### Q54 ⭐⭐ 🟡 How do you find the common and the different items between two lists, for example employee IDs in two HR files (set intersection and difference)?
**Asked at:** HR-flavoured composite; no company-specific report found
**What the interviewer is checking:** Can you reconcile two lists with sets?
**Say this in the interview:** "I convert both lists to sets. `&` gives IDs in both, `-` gives IDs only in the first, and `^` gives IDs in one file but not both."
**Explain simply:**
- A set is an unordered collection with no duplicates; set maths is fast.
- Intersection (`&`): in both files. Difference (`-`): in A but not B.
- Symmetric difference (`^`): in exactly one of the two.
- Sets have no order, so use `sorted()` to print neatly.
**Sample data:** file A IDs 101 to 105; file B IDs 103 to 106.
**Code (what you write in the interview):**
```python
file_a_ids = [101, 102, 103, 104, 105]
file_b_ids = [103, 104, 105, 106]

common_ids = set(file_a_ids) & set(file_b_ids)
only_in_a = set(file_a_ids) - set(file_b_ids)
only_in_b = set(file_b_ids) - set(file_a_ids)
in_either_but_not_both = set(file_a_ids) ^ set(file_b_ids)

print(sorted(common_ids))
print(sorted(only_in_a))
print(sorted(only_in_b))
print(sorted(in_either_but_not_both))
```
**Output:**
```
[103, 104, 105]
[101, 102]
[106]
[101, 102, 106]
```
**What it means:** Three IDs match, 101 and 102 are missing from file B, and 106 is missing from file A.
**Likely follow-ups:**
- Pandas version? `merge` with `indicator=True`, or `isin()`.
**Common mistakes:** Using `a - b` and forgetting it is not symmetric; expecting set output in sorted order; duplicates are lost when converting to a set.

### Q55 ⭐⭐ 🟡 What is the time complexity of searching an item in a list versus a set or dictionary, and why does it matter for large data?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic efficiency thinking.
**Say this in the interview:** "Searching a list is O(n): it may check every item. Searching a set or dictionary is O(1) on average, because it uses hashing to jump straight to the spot. On millions of records that is the difference between seconds and instant."
**Explain simply:**
- O(n) means time grows in proportion to the number of items; O(1) means roughly constant time.
- Sets and dictionaries use a hash (a number computed from the item) to find its location directly.
- It matters when you check membership repeatedly, for example "is this ID in the other file?" inside a loop.
- Trade-off: sets use more memory and need unique, hashable items.
**Sample data:** one million employee IDs, looking for the last one (999999).
**Code (what you write in the interview):**
```python
employee_ids_list = list(range(1_000_000))
employee_ids_set = set(employee_ids_list)

print(999_999 in employee_ids_list)   # scans the list, slow
print(999_999 in employee_ids_set)    # direct lookup, fast
```
**Output:**
```
True
True
```
**What it means:** Same answer, very different speed. Timing 100 searches separately on this machine (one run): list about 0.99 seconds, set about 0.00001 seconds.
**Likely follow-ups:**
- What is the worst case for a set? O(n) with many hash collisions, which is rare.
**Common mistakes:** Calling `in` on a big list inside a loop (that becomes O(n x m)); forgetting that building the set also takes time.

### Q56 ⭐ 🟢 What is Python, and why is it popular for data analysis compared with Excel?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain it plainly and honestly compare tools?
**Say this in the interview:** "Python is a general-purpose programming language that is easy to read. For analysis it handles much larger data than Excel, makes work repeatable with a script, and has libraries like pandas for cleaning, grouping and charts. I still use Excel for quick checks and sharing."
**Explain simply:**
- Python is free and open source; Excel is a paid spreadsheet.
- Excel slows or stops near its row limit (1,048,576 rows per sheet); pandas handles millions of rows, depending on memory.
- A Python script can be re-run on next month's file in seconds; manual Excel steps must be repeated by hand.
- Libraries: pandas (tables), NumPy (numbers), matplotlib (charts).
- Excel is still better for quick, visual, one-off work and for non-technical audiences.
**Likely follow-ups:**
- When would you stay in Excel? Small data, quick checks, a stakeholder who needs to edit the file.
**Common mistakes:** Saying Python replaces Excel entirely; claiming Excel cannot automate (it can, with macros and Power Query).

### Q57 ⭐ 🟢 What is the difference between a script and a Jupyter notebook cell when running Python code, and what does indentation mean in Python?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Familiarity with the tools and Python's block syntax.
**Say this in the interview:** "A script is a `.py` file that runs top to bottom in one go. A notebook is split into cells that I run one at a time, keeping variables in memory between cells, with results and charts shown beneath. Indentation in Python is not decoration: it defines which lines belong to an `if`, loop or function."
**Explain simply:**
- Script: good for automation and scheduled jobs; run from the command line.
- Notebook cell: good for exploring, explaining and sharing analysis. Running cells out of order can give confusing results.
- Indentation: the spaces at the start of a line (4 is standard) mark a block.
- Wrong indentation changes meaning or raises IndentationError.
**Sample data:** a salary check with two indented lines.
**Code (what you write in the interview):**
```python
salary = 45000
if salary > 40000:
    print("Above average")    # indented: runs only if the condition is true
    print("Checked")           # also inside the if block
print("Done")                  # not indented: always runs
```
**Output:**
```
Above average
Checked
Done
```
**What it means:** The first two lines only run when the salary is above 40000; the last runs regardless.
**Likely follow-ups:**
- Tabs or spaces? Use one consistently, preferably 4 spaces.
**Common mistakes:** Mixing tabs and spaces; running notebook cells out of order and trusting stale variables.

### Q58 ⭐ 🟢 How do you take input from a user and print formatted output using f-strings (for example 'Ravi earns 45000')?
**Asked at:** commonly asked (no company-specific report found); a basic-Python warm-up in fresher screens.
**What the interviewer is checking:** Whether you know `input()` always returns text, and can build a sentence from variables with an f-string.
**Say this in the interview:** "`input()` shows a question and gives back what the user typed, always as text. An f-string is a string starting with `f` where anything in curly brackets is replaced by the variable's value."
**Explain simply:**
- `input("question")` pauses the program and waits for the user to type. The answer comes back as a **string** (text), even if they typed digits.
- To do maths on it, convert it: `int(...)` for whole numbers, `float(...)` for decimals.
- An **f-string** is a text with `f` before the opening quote. Names inside `{}` are replaced by their values.
- Inside the braces you can format: `{salary:,}` adds thousand separators, `{rate:.1f}` shows 1 decimal place.
**Code (what you write in the interview):**
```python
# Ask the user for a name and a salary (input always gives text)
name = input("Enter employee name: ")
salary = int(input("Enter salary: "))

# Print using an f-string: the {} parts are filled with the variables
print(f"{name} earns {salary}")
print(f"{name} earns {salary:,} per month")
```
**Output:** (I typed `Ravi` and `45000` when asked)
```text
Enter employee name: Ravi
Enter salary: 45000
Ravi earns 45000
Ravi earns 45,000 per month
```
**What it means:** The program collected two values and built a readable sentence. Because `salary` was converted with `int`, we could also add or compare it.
**Likely follow-ups:** 1) *What if the user types "abc" for salary?* `int("abc")` raises a ValueError; wrap it in try/except (see Q27). 2) *Older way?* `"{} earns {}".format(name, salary)` or `%` formatting; f-strings are the modern, shorter choice.
**Common mistakes:** Forgetting the `f` before the quote (the braces print literally); forgetting `int()` so `"45000" + 1000` fails; mixing quote types inside the f-string.

### Q59 ⭐ 🟢 How do you add comments and docstrings in Python, and why are they useful?
**Asked at:** commonly asked (no company-specific report found); readability and handover habits are often probed in analytics firms.
**What the interviewer is checking:** Whether you write code others (and future you) can understand.
**Say this in the interview:** "A comment starts with `#` and is ignored by Python; it explains why a step exists. A docstring is a triple-quoted text on the first line inside a function that describes what the function does. Both make code easy to hand over."
**Explain simply:**
- **Comment:** anything after `#` on a line. Python skips it. Use it to explain a step in plain words.
- **Docstring:** a string in triple quotes `"""..."""` placed as the first line inside a function. It is documentation that stays attached to the function, so `help(function_name)` can show it.
- Why useful: a teammate (or you, six months later) can understand a payroll calculation without guessing.
- Good comments say *why*, not just repeat the code.
**Code (what you write in the interview):**
```python
def attrition_rate(left, total):
    """Return attrition percentage = employees who left / total employees * 100."""
    # Avoid dividing by zero for an empty team
    if total == 0:
        return 0
    return left / total * 100

print(attrition_rate(12, 150))
```
**Output:**
```text
8.0
```
**What it means:** 12 leavers out of 150 employees is 8% attrition. The docstring describes the function; the comment explains the zero check. (I also ran `help(attrition_rate)`: it prints the docstring text.)
**Likely follow-ups:** 1) *Multi-line comments?* Python has none; use several `#` lines (a triple-quoted string not assigned to anything works but is not a real comment). 2) *In Jupyter?* Markdown cells explain the story, `#` comments explain code lines.
**Common mistakes:** Comments that repeat the code ("add 1 to x"); outdated comments that no longer match the code; putting the docstring below the first line so it is not a docstring.

### Q60 ⭐ 🟢 What is None in Python, and how is it different from 0 or an empty string?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate "no value" from "a value that happens to be zero or empty", which matters when handling missing data.
**Say this in the interview:** "`None` means there is no value at all. `0` is a real number and `''` is real but empty text. In HR data a missing salary should be None, not 0, otherwise it drags the average down."
**Explain simply:**
- `None` is Python's way of saying "nothing here / not known". Its type is `NoneType`.
- `0` is a number (a bonus of zero rupees is a real fact). `""` is a text with no characters.
- They are not equal: `None == 0` and `None == ""` are both False.
- Check for it with `is None` (see Q68).
- This is the same idea as a blank cell or NaN (missing) in pandas.
**Code (what you write in the interview):**
```python
manager = None        # no manager recorded
bonus = 0             # a real bonus of zero rupees
comment = ""          # a comment that was typed but is empty

print(manager is None)
print(bonus is None)
print(comment is None)
print(manager == 0, manager == "")

# Missing salary must not be treated as zero
salaries = [50000, None, 60000]
known_salaries = [s for s in salaries if s is not None]
print(sum(known_salaries) / len(known_salaries))
```
**Output:**
```text
True
False
False
False False
55000.0
```
**What it means:** Only `manager` is truly "nothing". Ignoring the missing salary gives an average of 55,000; treating it as 0 would have given 36,667.
**Likely follow-ups:** 1) *Is None truthy?* No, it is falsy like 0 and "" (see Q35). 2) *What does a function return if it has no return line?* None.
**Common mistakes:** Filling missing values with 0 without thinking; using `== None` instead of `is None`; trying to add `None` to a number (TypeError).

### Q61 ⭐ 🟢 What is the difference between the pop(), remove() and del operations on a list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know removal by position versus by value, and which one returns the item.
**Say this in the interview:** "`pop(i)` removes by position and gives the item back. `remove(x)` removes the first item equal to x, by value. `del` removes by position (or a slice) and returns nothing."
**Explain simply:**
- **Index** = the position of an item, starting from 0.
- `pop()` with no number removes the last item. Useful when you want to use the removed item.
- `remove("Ravi")` searches for the value and removes only the first match. If it is not there, you get a ValueError.
- `del employees[0]` deletes by position; `del employees[1:3]` deletes a range; `del employees` deletes the whole list name.
**Sample data:** `employees = ["Asha", "Ravi", "Meena", "Ravi", "Kiran"]`
**Code (what you write in the interview):**
```python
employees = ["Asha", "Ravi", "Meena", "Ravi", "Kiran"]

removed_by_position = employees.pop(1)    # removes index 1 and gives it back
print(removed_by_position, employees)

employees.remove("Ravi")                  # removes first match by value
print(employees)

del employees[0]                          # removes by position, gives nothing back
print(employees)
```
**Output:**
```text
Ravi ['Asha', 'Meena', 'Ravi', 'Kiran']
['Asha', 'Meena', 'Kiran']
['Meena', 'Kiran']
```
**What it means:** `pop(1)` took out the first Ravi; `remove("Ravi")` took out the second one; `del` dropped Asha. (I checked: `employees.remove("Zoya")` raises `ValueError: list.remove(x): x not in list`.)
**Likely follow-ups:** 1) *How to remove all matches?* Build a new list: `[n for n in employees if n != "Ravi"]`. 2) *pop on an empty list?* IndexError.
**Common mistakes:** Expecting `remove` to delete every match; expecting `del` to return the item; removing items inside a loop over the same list (see Q53).

### Q62 ⭐ 🟢 How do you count the occurrences of an item in a list, and how do you find its position (count and index)?
**Asked at:** commonly asked (no company-specific report found); frequency counting is a standard coding-round pattern.
**What the interviewer is checking:** Knowing two simple built-in list methods and their limits.
**Say this in the interview:** "`my_list.count(x)` tells me how many times x appears. `my_list.index(x)` tells me the position of its first appearance, counting from 0, and raises an error if it is missing."
**Explain simply:**
- `count("HR")` scans the list and returns a number, 0 if there is none.
- `index("IT")` returns the position of the **first** match only.
- Positions start from 0, so the first item is position 0.
- To count every item at once, use a dictionary or `Counter` (see Q5, Q51).
**Sample data:** `departments = ["HR", "IT", "HR", "Sales", "HR", "IT"]`
**Code (what you write in the interview):**
```python
departments = ["HR", "IT", "HR", "Sales", "HR", "IT"]

how_many_hr = departments.count("HR")        # how many times
first_it_position = departments.index("IT")  # first position (starts at 0)

print(how_many_hr)
print(first_it_position)
```
**Output:**
```text
3
1
```
**What it means:** HR appears 3 times, and IT first appears at position 1 (the second item). (Checked: `departments.index("Finance")` raises ValueError.)
**Likely follow-ups:** 1) *Find all positions of "HR"?* `[i for i, d in enumerate(departments) if d == "HR"]` gives `[0, 2, 4]`. 2) *Safe check first?* `if "Finance" in departments:`.
**Common mistakes:** Expecting `index` to return every position; forgetting counting starts at 0; not guarding against ValueError.

### Q63 ⭐ 🟢 What is tuple unpacking, and where does it appear when looping over dict.items()?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand why `for name, salary in data.items()` works.
**Say this in the interview:** "Tuple unpacking means splitting a tuple into separate variables in one line. `dict.items()` hands out each key-value pair as a tuple, so the loop unpacks it into two names automatically."
**Explain simply:**
- A **tuple** is a fixed group of values, like `("Asha", 50000)`.
- Unpacking: `name, salary = ("Asha", 50000)` puts "Asha" in `name` and 50000 in `salary`. The number of names must match the number of values.
- `salaries.items()` gives pairs: `("Asha", 50000)`, `("Ravi", 42000)`, and so on.
- The loop line `for name, salary in salaries.items()` unpacks one pair per turn.
**Sample data:** `salaries = {"Asha": 50000, "Ravi": 42000, "Meena": 61000}`
**Code (what you write in the interview):**
```python
salaries = {"Asha": 50000, "Ravi": 42000, "Meena": 61000}

# Tuple unpacking: one pair is split into two variables
pair = ("Asha", 50000)
name, salary = pair
print(name, salary)

# The same thing happens in every loop turn
for name, salary in salaries.items():
    print(name, salary)
```
**Output:**
```text
Asha 50000
Asha 50000
Ravi 42000
Meena 61000
```
**What it means:** The first line is manual unpacking; the next three lines show the loop doing it for every pair.
**Likely follow-ups:** 1) *What if counts do not match?* ValueError: too many or not enough values to unpack. 2) *Ignore one value?* Use `_`: `for name, _ in salaries.items()`.
**Common mistakes:** Looping `for x in salaries` and expecting pairs (you only get keys); wrong number of names on the left.

### Q64 ⭐ 🟢 What does the len() function return for a list, a string and a dictionary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic familiarity with what "length" means for each type.
**Say this in the interview:** "`len` returns the number of items: elements in a list, characters in a string, and key-value pairs (number of keys) in a dictionary."
**Explain simply:**
- List: how many items it holds (headcount of the list).
- String: how many characters, including spaces.
- Dictionary: how many keys, which equals the number of pairs.
- For a nested list, `len` counts only the outer items, not everything inside.
**Code (what you write in the interview):**
```python
salaries_list = [50000, 42000, 61000]
employee_name = "Meena"
employee_record = {"name": "Meena", "dept": "HR", "salary": 61000}

print(len(salaries_list))
print(len(employee_name))
print(len(employee_record))
```
**Output:**
```text
3
5
3
```
**What it means:** 3 salaries, 5 letters in "Meena", 3 fields in the record.
**Likely follow-ups:** 1) *len of a number?* TypeError, numbers have no length. 2) *len of None?* Also TypeError.
**Common mistakes:** Thinking `len` of a dictionary counts values separately; forgetting spaces count in strings.

### Q65 ⭐ 🟡 What is the difference between a function and a method, with examples from lists?
**Asked at:** commonly asked (no company-specific report found); basic Python and OOP basics are asked at some analytics firms (LatentView, per research/interview_processes.md).
**What the interviewer is checking:** Whether you understand the dot-call style belongs to an object.
**Say this in the interview:** "A function stands alone and I pass data into it, like `len(my_list)`. A method belongs to an object and is called with a dot, like `my_list.append(5)`; it works on that object."
**Explain simply:**
- **Function:** `len(x)`, `sum(x)`, `max(x)`, `sorted(x)`. Called by name, data goes inside brackets.
- **Method:** a function that lives inside an object type (list, string, dict). Called as `object.method()`.
- Methods act on the object they are attached to: `salaries.append(55000)` changes that very list.
- `sorted(x)` is a function that returns a new list; `x.sort()` is a method that changes the list in place (see Q23).
**Code (what you write in the interview):**
```python
salaries = [50000, 42000, 61000]

# Function: you pass the thing in
print(len(salaries))
print(sum(salaries))

# Method: belongs to the list, called with a dot
salaries.append(55000)
salaries.sort()
print(salaries)
```
**Output:**
```text
3
153000
[42000, 50000, 55000, 61000]
```
**What it means:** `len` and `sum` only looked at the list; `append` and `sort` changed it.
**Likely follow-ups:** 1) *Can you write your own method?* Yes, define a function inside a class. 2) *Methods on strings and dicts?* `"abc".upper()`, `data.keys()`.
**Common mistakes:** Writing `salaries.len()` or `append(salaries, 5)`; forgetting the brackets so the method is not actually called.

### Q66 ⭐ 🟡 What is a recursive function? Write a factorial function and mention when recursion is risky.
**Asked at:** commonly asked (no company-specific report found); a classic basics question.
**What the interviewer is checking:** Whether you know a base case and the risk of unlimited self-calls.
**Say this in the interview:** "A recursive function calls itself on a smaller version of the problem until it reaches a stopping rule called the base case. Factorial of 5 is 5 times factorial of 4. It is risky when there is no base case or the depth is very large, because Python stops with a RecursionError."
**Explain simply:**
- **Factorial** of n (written n!) is n x (n-1) x ... x 1. So 5! = 120.
- **Base case:** the simple case answered directly (1! = 1). Without it the function never stops.
- **Recursive step:** `n * factorial(n - 1)` shrinks the problem each time.
- Risk: every call uses memory; Python's default limit is about 1000 nested calls, so very deep recursion fails. A loop is safer for big inputs.
- Analysts rarely need recursion; loops and pandas cover most work.
**Code (what you write in the interview):**
```python
def factorial(n):
    # Stopping rule: 1! is 1 (and 0! is 1)
    if n <= 1:
        return 1
    # The function calls itself with a smaller number
    return n * factorial(n - 1)

print(factorial(5))
```
**Output:**
```text
120
```
**What it means:** 5 x 4 x 3 x 2 x 1 = 120.
**Alternative:** a loop version (no recursion risk):
```python
result = 1
for number in range(2, 6):
    result = result * number
print(result)   # 120
```
**Likely follow-ups:** 1) *What if n is negative?* This code returns 1; a careful version should raise an error. 2) *Built-in?* `math.factorial(5)`.
**Common mistakes:** Forgetting the base case (infinite calls until RecursionError); calling with the same n instead of n - 1.

### Q67 ⭐ 🟡 What is a decorator in Python, in simple terms, and have you used one?
**Asked at:** commonly asked (no company-specific report found); a differentiator more than a core DA topic.
**What the interviewer is checking:** Whether you can explain it simply and are honest about real use.
**Say this in the interview:** "A decorator is a wrapper that adds behaviour to a function without changing the function's own code; you put `@name` above the function. I have mostly used built-in ones like `@property` or `@st.cache_data`; writing my own is less common in analysis work." (Say only what is true for you.)
**Explain simply:**
- A function can be passed around like any value, so one function can take another and return an upgraded version.
- `@show_progress` above `def total_payroll` is shorthand for `total_payroll = show_progress(total_payroll)`.
- Typical uses: logging, timing how long a function runs, caching results, access checks.
- The inner `wrapper` runs extra steps before and after the original function.
**Code (what you write in the interview):**
```python
def show_progress(function):
    def wrapper(*args):
        print("Starting...")
        result = function(*args)
        print("Done")
        return result
    return wrapper

@show_progress
def total_payroll(salaries):
    return sum(salaries)

print(total_payroll([50000, 42000, 61000]))
```
**Output:**
```text
Starting...
Done
153000
```
**What it means:** The payroll function itself only sums; the decorator printed messages around it.
**Likely follow-ups:** 1) *What is `*args`?* It collects all positional arguments (see Q43). 2) *Common built-ins?* `@property`, `@staticmethod`, `functools.lru_cache`.
**Common mistakes:** Forgetting to `return result` inside the wrapper (function then returns None); claiming you use them daily when you do not.

### Q68 ⭐ 🟡 What is the difference between is None and == None, and why do analysts check for None before calculating?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the correct, safe way to test for missing values.
**Say this in the interview:** "`is None` checks identity: is this the one special None object. `== None` checks equality, which usually works but can be fooled by custom objects, so the recommended style is `is None`. I check first because adding None to a number crashes."
**Explain simply:**
- `None` is a single object in Python, so `is` is the exact test for it (PEP 8, Python's style guide, recommends `is None`).
- `== None` gives the same answer for normal values, but a class can redefine `==`, and tools like NumPy or pandas can return something unexpected. `is None` cannot be redefined.
- Why check before calculating: `50000 + None` raises `TypeError`. A missing salary in a loop stops the whole report.
- Decide what to do: skip the value, fill it, or flag it, rather than silently treating it as 0 (see Q60).
**Code (what you write in the interview):**
```python
bonus = None

print(bonus is None)
print(bonus == None)

salaries = [50000, None, 61000]
total = 0
for salary in salaries:
    # Skip missing values, adding None would crash
    if salary is None:
        continue
    total = total + salary
print(total)
```
**Output:**
```text
True
True
111000
```
**What it means:** Both tests say True here, but `is None` is the safe habit. The loop skipped the missing salary and totalled the rest. (Checked: `50000 + None` gives `TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'`.)
**Likely follow-ups:** 1) *Does `if not value` work?* It also catches 0 and "", so it can wrongly treat a real 0 as missing. 2) *In pandas?* Use `isna()`.
**Common mistakes:** Using `if not salary:` and dropping real zeros; writing `is not None` as `not x is None` (works but harder to read).

### Q69 ⭐ 🟡 Write a function that classifies an employee's tenure in years as New (under 1), Mid (1-3) or Senior (over 3), and apply it to a list.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the standard if/elif banding task.
**What the interviewer is checking:** Clean if/elif ordering, clear boundary handling (is exactly 1 or 3 included?), and applying a function to many values.
**Say this in the interview:** "I will check from the lowest band up: under 1 is New, up to and including 3 is Mid, everything else is Senior. I will confirm with you that 1 and 3 belong to Mid, then apply the function with a list comprehension."
**Explain simply:**
- `if / elif / else` tests conditions top to bottom and stops at the first one that is true, so order matters.
- The boundaries need a decision: "1-3" here means 1 to 3 inclusive, and "over 3" means above 3. Ask the interviewer.
- A **list comprehension** builds a new list by running the function on each item (see Q7).
**Sample data:** `tenures = [0.5, 1, 2.5, 3, 3.5, 8]`
**Code (what you write in the interview):**
```python
def tenure_band(years):
    # Under 1 year
    if years < 1:
        return "New"
    # 1 to 3 years (both included)
    elif years <= 3:
        return "Mid"
    # More than 3 years
    else:
        return "Senior"

tenures = [0.5, 1, 2.5, 3, 3.5, 8]
bands = [tenure_band(years) for years in tenures]
print(bands)
```
**Output:**
```text
['New', 'Mid', 'Mid', 'Mid', 'Senior', 'Senior']
```
**What it means:** 0.5 is New; 1, 2.5 and exactly 3 are Mid; 3.5 and 8 are Senior.
**Alternative:** in pandas the same function is applied with `df["tenure_years"].apply(tenure_band)`, or `pd.cut` for bands.
**Likely follow-ups:** 1) *What about a missing or negative tenure?* Add a first check: `if years is None or years < 0: return "Invalid"`. 2) *Why elif, not three ifs?* Elif stops after a match and avoids overlap.
**Common mistakes:** Using `<` where the band needs `<=` (3 years becomes Senior); wrong order of conditions; printing inside the function instead of returning.

### Q70 ⭐ 🟡 Write code to build a monthly attendance summary: given a list of daily statuses ('P', 'A', 'L'), return counts of each using a loop and a dictionary.
**Asked at:** commonly asked (no company-specific report found); the loop-and-dictionary counting pattern is standard (Dataford, DataDriven practice platforms).
**What the interviewer is checking:** Whether you can build a frequency count by hand with a loop and a dict.
**Say this in the interview:** "I create a dictionary with each status starting at zero, loop over the days, and add one to the matching status."
**Explain simply:**
- Codes: P = present, A = absent, L = leave.
- The dictionary is a tally sheet: key = status, value = number of days.
- Starting every count at 0 first avoids a KeyError when a status is never used (see Q14).
- For an unknown set of statuses use `counts.get(status, 0) + 1` (see Q5).
**Sample data:** 10 days: `P P A P L P P A P P`
**Code (what you write in the interview):**
```python
daily_status = ["P", "P", "A", "P", "L", "P", "P", "A", "P", "P"]

# Start every count at zero
summary = {"P": 0, "A": 0, "L": 0}

# Add one to the matching status for each day
for status in daily_status:
    summary[status] = summary[status] + 1

print(summary)
```
**Output:**
```text
{'P': 7, 'A': 2, 'L': 1}
```
**What it means:** 7 days present, 2 absent, 1 on leave; the total is 10 days.
**Alternative:** `from collections import Counter` then `Counter(daily_status)` gives the same counts in one line.
**Likely follow-ups:** 1) *Attendance percentage?* `summary["P"] / len(daily_status) * 100` = 70%. 2) *Unexpected code like "H"?* The loop raises KeyError; use `.get` or validate first.
**Common mistakes:** Forgetting to initialise the counts; resetting the dictionary inside the loop; returning the print instead of the dictionary when a function is requested.

### Q71 ⭐ 🟡 What are Python's integer and float precision issues, such as 0.1 + 0.2 not equal to 0.3, and how do you compare floats safely or round money values?
**Asked at:** commonly asked (no company-specific report found); a differentiator question.
**What the interviewer is checking:** Whether you know decimals are stored approximately and can handle comparisons and money safely.
**Say this in the interview:** "Computers store decimals in binary, and numbers like 0.1 cannot be stored exactly, so 0.1 + 0.2 gives 0.30000000000000004. I never compare floats with `==`; I use `math.isclose`, and for money I round to 2 decimals or use the Decimal type."
**Explain simply:**
- A **float** is a decimal number stored approximately (like 1/3 in decimal: 0.3333...). Tiny errors appear in the far digits.
- **Integers** in Python are exact and have no size limit, so no such problem. A trick for money: store paise as whole numbers.
- `math.isclose(a, b)` asks "are these equal within a tiny tolerance?".
- `round(value, 2)` rounds to 2 decimals for display or payroll.
- `Decimal("0.1")` (from the `decimal` module, created from text) is exact for decimal money, but slower.
**Code (what you write in the interview):**
```python
import math

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)

# Safe comparison: "close enough"
print(math.isclose(0.1 + 0.2, 0.3))

# Money: round to 2 decimals
salary = 45000
pf_rate = 0.0833
pf_amount = round(salary * pf_rate, 2)
print(pf_amount)
```
**Output:**
```text
0.30000000000000004
False
True
3748.5
```
**What it means:** Direct `==` fails because of the hidden tiny error; `isclose` says they are equal for practical purposes; the provident fund (PF) amount is rounded to paise.
**Alternative:** exact decimals:
```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
```
**Likely follow-ups:** 1) *Why does `round(2.5)` give 2?* Python rounds halves to the nearest even number ("banker's rounding"): `round(2.5)` is 2 and `round(3.5)` is 4 (verified). For payroll rules, use Decimal with an explicit rounding mode. 2) *Does Excel have this?* Yes, it hides much of it by displaying fewer digits.
**Common mistakes:** Comparing floats with `==`; building Decimal from a float (`Decimal(0.1)` keeps the error) instead of a string; rounding too early in a chain of calculations.

### Q72 ⭐ 🔴 Given a list of (candidate, stage) tuples from a hiring funnel, write code that returns how many candidates reached each stage and the drop-off percentage between stages.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured composite of the dict-counting and funnel-metric patterns.
**What the interviewer is checking:** Counting with a dictionary, using an explicit stage order, and computing percentage drop between consecutive stages correctly (base = the previous stage).
**Say this in the interview:** "First I count how many candidates are at each stage using a dictionary. Then I walk the stages in funnel order and compute (previous minus current) divided by previous times 100. I will state the assumption that each candidate appears once per stage they reached."
**Explain simply:**
- **Funnel:** a series of stages where people drop out, like Applied, Screened, Interviewed, Offered, Joined.
- **Drop-off %** between two stages = (people at the earlier stage minus people at the next stage) divided by people at the earlier stage, times 100. The base is the earlier stage.
- Dictionaries have no guaranteed funnel order of meaning, so I keep a separate `stage_order` list.
- If a candidate appeared twice in the same stage you would double count; remove duplicates first (use a set).
**Sample data:** 5 applied, 4 screened, 3 interviewed, 2 offered, 1 joined (each candidate repeated once per stage reached).
**Code (what you write in the interview):**
```python
# (candidate, stage) pairs: each candidate appears once per stage reached
funnel_records = [
    ("A", "Applied"), ("B", "Applied"), ("C", "Applied"), ("D", "Applied"), ("E", "Applied"),
    ("A", "Screened"), ("B", "Screened"), ("C", "Screened"), ("D", "Screened"),
    ("A", "Interviewed"), ("B", "Interviewed"), ("C", "Interviewed"),
    ("A", "Offered"), ("B", "Offered"),
    ("A", "Joined"),
]
stage_order = ["Applied", "Screened", "Interviewed", "Offered", "Joined"]

# Count the candidates at each stage
candidates_per_stage = {}
for candidate, stage in funnel_records:
    candidates_per_stage[stage] = candidates_per_stage.get(stage, 0) + 1

# Drop-off between each stage and the next one
for i in range(1, len(stage_order)):
    previous_stage = stage_order[i - 1]
    this_stage = stage_order[i]
    previous_count = candidates_per_stage[previous_stage]
    this_count = candidates_per_stage[this_stage]
    drop_off = (previous_count - this_count) / previous_count * 100
    print(f"{previous_stage} -> {this_stage}: {previous_count} -> {this_count}, drop-off {drop_off:.0f}%")
```
**Output:**
```text
Applied -> Screened: 5 -> 4, drop-off 20%
Screened -> Interviewed: 4 -> 3, drop-off 25%
Interviewed -> Offered: 3 -> 2, drop-off 33%
Offered -> Joined: 2 -> 1, drop-off 50%
```
**What it means:** The biggest leak in percentage terms is Offered to Joined (half the offers were not accepted); overall only 1 of 5 applicants (20%) joined.
**Likely follow-ups:** 1) *What if the records list only each candidate's last stage?* Then a candidate who "Joined" also passed earlier stages; count a candidate for every stage up to and including their last. 2) *Zero at a stage?* Guard the division when `previous_count` is 0. 3) *Overall conversion?* Joined divided by Applied = 20%.
**Common mistakes:** Dividing by the current stage instead of the previous; relying on dictionary order instead of the funnel order; double counting duplicate records; mixing "reached" counts with "stuck at" counts.

### Q73 ⭐ 🔴 What is a closure in Python, and what goes wrong with lambda functions created inside a loop?
**Asked at:** commonly asked (no company-specific report found); an advanced-basics differentiator.
**What the interviewer is checking:** Whether you understand that inner functions remember variables (not values) from the enclosing scope.
**Say this in the interview:** "A closure is an inner function that remembers variables from the function that created it, even after that outer function has finished. The trap: lambdas created in a loop all share the same loop variable and look it up when they run, so they all see its final value. Fix it by passing the value in as a default argument."
**Explain simply:**
- **Closure example:** `make_bonus_calculator(0.10)` returns an inner function that still remembers `rate = 0.10`. Useful for building small custom calculators.
- **Late binding:** the inner function looks up `rate` when it is *called*, not when it is *created*.
- In a loop, all lambdas point to the same `rate`; by the time you call them the loop is over and `rate` is the last value (0.15).
- **Fix:** `lambda salary, rate=rate: salary * rate` evaluates and stores `rate` at creation time.
**Code (what you write in the interview):**
```python
# Closure: inner function remembers the outer variable
def make_bonus_calculator(rate):
    def calculate(salary):
        return salary * rate
    return calculate

ten_percent = make_bonus_calculator(0.10)
print(ten_percent(50000))

# The trap: lambdas in a loop
rates = [0.05, 0.10, 0.15]
calculators = [lambda salary: salary * rate for rate in rates]
print([calc(100000) for calc in calculators])

# Fix: freeze the value with a default argument
calculators = [lambda salary, rate=rate: salary * rate for rate in rates]
print([calc(100000) for calc in calculators])
```
**Output:**
```text
5000.0
[15000.0, 15000.0, 15000.0]
[5000.0, 10000.0, 15000.0]
```
**What it means:** The first line shows a working closure (10% of 50,000). The wrong list gives 15% three times; the fixed list gives the expected 5%, 10% and 15% of 100,000.
**Likely follow-ups:** 1) *Another fix?* Use a factory function like `make_bonus_calculator` to create each function. 2) *Can a closure change the outer variable?* Only with the `nonlocal` keyword.
**Common mistakes:** Assuming each lambda captured its own value; confusing closures with global variables; forgetting that the trap also applies to ordinary `def` functions defined in a loop.
