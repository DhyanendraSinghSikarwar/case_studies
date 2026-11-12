# Book 3 — Python & pandas for Analysts | Part 10: Basic Coding Logic Asked in DA Rounds 🟢🟡

**Target:** 65 questions | **Actual:** 71 questions
**Scope:** easy list, string and dictionary problems (reverse, palindrome, counts, duplicates) and basic CS/OOP fundamentals asked in data analyst coding rounds.

### Q1 ⭐⭐⭐ 🟢 Write code to reverse a string in Python.
**Asked at:** commonly asked (no company-specific report found); string reversal is listed as a standard opener in Analytics Vidhya and Glassdoor candidate snippets.
**What the interviewer is checking:** Do you know slicing, and can you also do it with a plain loop if they say "without slicing"?
**Say this in the interview:** "A string is a sequence, so I slice it with a step of minus one, which walks it backwards. If you want it without slicing, I can build it with a loop."
**Explain simply:**
- A *string* is text. Python lets you slice it as `text[start:stop:step]`.
- Leaving start and stop empty and using step `-1` means "the whole thing, backwards".
- Strings cannot be changed in place (they are *immutable*), so we always create a new reversed string.
**Sample data:** `text = "attrition"`
**Code (what you write in the interview):**
```python
text = "attrition"

# slicing with step -1 walks the string backwards
reversed_text = text[::-1]
print(reversed_text)
```
**Output:**
```
noitirtta
```
**What it means:** The last letter became the first, and so on. The original `text` is unchanged.
**Alternative:** The loop version, if the interviewer bans slicing.
```python
text = "attrition"

# build the reversed string one character at a time
reversed_text = ""
for character in text:
    reversed_text = character + reversed_text
print(reversed_text)
```
(Output: `noitirtta`.) Each new character is placed in front of what we already have.
**Likely follow-ups:**
- *Does `reversed()` work?* It returns an iterator, so you need `"".join(reversed(text))`.
- *Can you reverse in place?* Not for a string, because it is immutable.
**Common mistakes:** Calling `text.reverse()` (that is a list method, strings have none); forgetting that `print(reversed(text))` shows an object, not the text.

### Q2 ⭐⭐⭐ 🟢 Write code to check whether a string is a palindrome.
**Asked at:** commonly asked (no company-specific report found); palindrome checks appear in several Glassdoor DA candidate snippets (InkRevenue, intern reports).
**What the interviewer is checking:** Can you reuse the reversal idea and compare, and do you think about case?
**Say this in the interview:** "A palindrome reads the same both ways, so I compare the string with its reverse. For the basic version I assume the input is already clean."
**Explain simply:**
- *Palindrome*: a word like "madam" that is the same forwards and backwards.
- `word[::-1]` gives the reversed word; `==` compares the two texts.
- This basic version is case-sensitive: "Madam" would fail (Q42 handles case, spaces and punctuation).
**Sample data:** `word = "madam"`
**Code (what you write in the interview):**
```python
word = "madam"

# a palindrome reads the same forwards and backwards
if word == word[::-1]:
    print(word, "is a palindrome")
else:
    print(word, "is not a palindrome")
```
**Output:**
```
madam is a palindrome
```
**What it means:** The word equals its own reverse, so it is a palindrome.
**Alternative:** Compare characters from both ends with two positions moving inward (no extra copy of the string; uses less memory).
**Likely follow-ups:**
- *What about "Madam"?* Use `word.lower()` first.
- *What about an empty string?* It is treated as a palindrome (equal to its reverse).
**Common mistakes:** Forgetting case; writing `=` (assign) instead of `==` (compare).

### Q3 ⭐⭐⭐ 🟢 Write code to count how many times each character appears in a string.
**Asked at:** commonly asked (no company-specific report found); character frequency is named in Glassdoor DA snippets and the Dataford "frequency of characters" drill.
**What the interviewer is checking:** Can you use a dictionary as a counter?
**Say this in the interview:** "I keep a dictionary of character to count. For each character I read its current count, defaulting to zero, and add one."
**Explain simply:**
- A *dictionary* stores key-value pairs; here key = character, value = how many times seen.
- `dict.get(key, 0)` returns the value, or 0 if the key is missing, which avoids a KeyError.
- Spaces are characters too, so they are counted unless you skip them.
**Sample data:** `text = "hr analytics"`
**Code (what you write in the interview):**
```python
text = "hr analytics"

character_counts = {}
for character in text:
    # get() returns 0 if the character has not been seen yet
    character_counts[character] = character_counts.get(character, 0) + 1

print(character_counts)
```
**Output:**
```
{'h': 1, 'r': 1, ' ': 1, 'a': 2, 'n': 1, 'l': 1, 'y': 1, 't': 1, 'i': 1, 'c': 1, 's': 1}
```
**What it means:** "a" appears twice, every other character once (including the space). Keys appear in the order first seen.
**Alternative:** `collections.Counter(text)` does the same in one line; mention it, but interviewers often ask for the manual way.
**Likely follow-ups:**
- *Ignore case?* Use `text.lower()` in the loop.
- *Ignore spaces?* Add `if character != " ":` inside the loop.
**Common mistakes:** Writing `character_counts[character] += 1` on a missing key (KeyError); counting upper and lower case separately by accident.

### Q4 ⭐⭐⭐ 🟢 Write code to count the frequency of each word in a sentence using a dictionary.
**Asked at:** commonly asked (no company-specific report found); a word-frequency task is on PracHub, and Tiger Analytics reports mention duplicate-frequency questions (Glassdoor summary, unverified).
**What the interviewer is checking:** Same counter pattern as Q3, but on words: do you know `split()`?
**Say this in the interview:** "I split the sentence into words, then count each word in a dictionary using get with a default of zero."
**Explain simply:**
- `split()` with no argument cuts text at any whitespace and returns a list of words.
- The counting loop is identical to the character one.
- Real text needs `.lower()` and punctuation removal; this basic version assumes clean input.
**Sample data:** `sentence = "the team hired the best team"`
**Code (what you write in the interview):**
```python
sentence = "the team hired the best team"

word_counts = {}
for word in sentence.split():
    word_counts[word] = word_counts.get(word, 0) + 1

print(word_counts)
```
**Output:**
```
{'the': 2, 'team': 2, 'hired': 1, 'best': 1}
```
**What it means:** "the" and "team" each appear twice; "hired" and "best" once.
**Alternative:** `Counter(sentence.split())` from the `collections` module.
**Likely follow-ups:**
- *Case-insensitive?* `sentence.lower().split()`.
- *Most common word?* Sort the items by count (see Q16).
**Common mistakes:** Splitting on `" "` (gives empty strings if there are double spaces); not lowering case so "Team" and "team" are separate.

### Q5 ⭐⭐⭐ 🟢 Write code to find the largest number in a list without using max().
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write the "keep the best so far" loop?
**Say this in the interview:** "I start with the first number as the largest, scan the rest, and replace it whenever I see something bigger."
**Explain simply:**
- Start from the first element, not from 0 (0 breaks if all numbers are negative).
- One pass through the list, so the work grows in step with list size.
- An empty list has no first element; mention you would check for it.
**Sample data:** `salaries = [42000, 55000, 38000, 61000, 47000]`
**Code (what you write in the interview):**
```python
salaries = [42000, 55000, 38000, 61000, 47000]

largest = salaries[0]
for salary in salaries:
    # keep the biggest value seen so far
    if salary > largest:
        largest = salary

print(largest)
```
**Output:**
```
61000
```
**What it means:** 61000 is the highest salary in the list.
**Alternative:** `sorted(salaries)[-1]` works but sorts the whole list for no reason.
**Likely follow-ups:**
- *Empty list?* Check `if not salaries:` and return `None` or raise an error.
- *Smallest?* Flip `>` to `<`.
**Common mistakes:** Starting `largest = 0` (wrong for negative numbers); returning inside the loop too early.

### Q6 ⭐⭐⭐ 🟢 Write code to remove duplicates from a list of employee IDs.
**Asked at:** commonly asked (no company-specific report found); Tiger Analytics reports mention duplicate handling in Python (Glassdoor summary, unverified).
**What the interviewer is checking:** Do you know the difference between keeping the order and not?
**Say this in the interview:** "I loop through and add an ID only if I have not already kept it. That preserves the original order. A set is shorter but loses the order."
**Explain simply:**
- A *duplicate* is a value that appears more than once; we want each ID once.
- `not in` checks whether the ID is already in the new list.
- A *set* stores unique values only but has no reliable order.
**Sample data:** `employee_ids = [101, 102, 101, 103, 102, 104]`
**Code (what you write in the interview):**
```python
employee_ids = [101, 102, 101, 103, 102, 104]

unique_ids = []
for employee_id in employee_ids:
    if employee_id not in unique_ids:
        unique_ids.append(employee_id)

print(unique_ids)
```
**Output:**
```
[101, 102, 103, 104]
```
**What it means:** Each ID appears once, in the order it first showed up.
**Alternative:** `list(dict.fromkeys(employee_ids))` keeps order in one line (dictionary keys are unique and ordered). `list(set(employee_ids))` is shortest but the order can change (it printed `[104, 101, 102, 103]` here).
**Likely follow-ups:**
- *Is it fast for big lists?* `not in` on a list is slow for large data; use a set to track seen IDs.
- *In pandas?* `df["employee_id"].drop_duplicates()`.
**Common mistakes:** Modifying the list while looping over it; using `set` when order matters.

### Q7 ⭐⭐⭐ 🟢 Write code to check whether a number is prime.
**Asked at:** commonly asked (no company-specific report found); a Glassdoor DA snippet mentions "6 or 7 coding challenges like find prime number", and InkRevenue Jr Data Analyst lists prime.
**What the interviewer is checking:** Edge cases (0, 1, 2) and whether you know to stop at the square root.
**Say this in the interview:** "A prime is above 1 and divisible only by 1 and itself. I try divisors from 2 up to the square root; if any divides evenly, it is not prime."
**Explain simply:**
- *Prime*: a number greater than 1 with no divisors except 1 and itself (2, 3, 5, 7...).
- `%` gives the remainder; remainder 0 means it divides evenly.
- If a number has a factor larger than its square root, it also has a smaller one, so we only need to check up to the square root.
**Sample data:** test with 29, 21 and 1.
**Code (what you write in the interview):**
```python
def is_prime(number):
    # numbers below 2 are not prime
    if number < 2:
        return False
    # a factor larger than the square root would pair with a smaller one
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True

print(is_prime(29))
print(is_prime(21))
print(is_prime(1))
```
**Output:**
```
True
False
False
```
**What it means:** 29 is prime; 21 is 3 x 7; 1 is not prime by definition.
**Alternative:** Check every divisor up to `number - 1`: simpler but slower; fine to say first, then improve.
**Likely follow-ups:**
- *Why the square root?* Factors come in pairs, one of each pair is at most the square root.
- *Primes up to 100?* Call the function in a loop, or use the Sieve of Eratosthenes.
**Common mistakes:** Treating 1 (or 0, negatives) as prime; forgetting `+ 1` in `range`, which skips the square root itself (breaks 4 and 9).

### Q8 ⭐⭐⭐ 🟢 Write the FizzBuzz program: print 1 to 30, but Fizz for multiples of 3, Buzz for multiples of 5 and FizzBuzz for both.
**Asked at:** commonly asked (no company-specific report found); FizzBuzz is on Dataford as a Python drill.
**What the interviewer is checking:** Ordering of conditions: do you test the "both" case first?
**Say this in the interview:** "I loop 1 to 30 and check divisibility by 15 first, because those numbers are multiples of both 3 and 5. Then 3, then 5, else the number itself."
**Explain simply:**
- `range(1, 31)` gives 1 to 30 (the end is excluded).
- `number % 3 == 0` means "divisible by 3".
- `elif` stops at the first true branch; if "Fizz" were checked first, 15 would print only "Fizz".
**Sample data:** none needed (the numbers 1 to 30).
**Code (what you write in the interview):**
```python
for number in range(1, 31):
    # check the "both" case first
    if number % 15 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
```
**Output:**
```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
Fizz
22
23
Fizz
Buzz
26
Fizz
28
29
FizzBuzz
```
**What it means:** Every multiple of 3 shows Fizz, every multiple of 5 shows Buzz, and 15 and 30 show FizzBuzz.
**Alternative:** Check `% 3 == 0 and % 5 == 0` explicitly instead of `% 15`; same result, more words.
**Likely follow-ups:**
- *Why 15?* It is the smallest number divisible by both 3 and 5.
- *Make it configurable?* Put the limit in a variable `n`.
**Common mistakes:** Checking 3 before the "both" case; `range(1, 30)` (stops at 29).

### Q9 ⭐⭐⭐ 🟢 Write code to find which values are duplicated in a list and how many times each occurs.
**Asked at:** commonly asked (no company-specific report found); Tiger Analytics duplicate-frequency question (Glassdoor summary, unverified) and DataLemur duplicates drills.
**What the interviewer is checking:** Counter dictionary, then filtering on count greater than 1.
**Say this in the interview:** "First I count every value in a dictionary. Then I keep only the ones whose count is more than one."
**Explain simply:**
- Step 1 is the same counting loop as Q3 and Q4.
- Step 2 filters the counts: a value is a duplicate if it appears at least twice.
- Two simple steps are easier to explain than one clever line.
**Sample data:** `values = [101, 102, 101, 103, 102, 101, 104]`
**Code (what you write in the interview):**
```python
values = [101, 102, 101, 103, 102, 101, 104]

counts = {}
for value in values:
    counts[value] = counts.get(value, 0) + 1

# keep only the values that appear more than once
duplicates = {}
for value, count in counts.items():
    if count > 1:
        duplicates[value] = count

print(duplicates)
```
**Output:**
```
{101: 3, 102: 2}
```
**What it means:** ID 101 appears 3 times and 102 twice; 103 and 104 are unique.
**Alternative:** In pandas, `series.value_counts()` then keep counts above 1.
**Likely follow-ups:**
- *Only the duplicate values, not counts?* `list(duplicates)`.
- *Huge list?* This is one pass, so it scales fine.
**Common mistakes:** Using `list.count()` inside a loop (works but slow, it rescans the list each time); reporting a unique value as a duplicate by using `>= 1`.

### Q10 ⭐⭐⭐ 🟢 Write code to count the vowels and consonants in a string.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you handle case and ignore non-letters?
**Say this in the interview:** "I lowercase the text, skip anything that is not a letter, and count a letter as a vowel if it is in 'aeiou', otherwise a consonant."
**Explain simply:**
- *Vowels*: a, e, i, o, u. *Consonants*: every other letter.
- `isalpha()` is True only for letters, so spaces, digits and punctuation are skipped.
- `.lower()` means "H" and "h" are treated the same.
**Sample data:** `text = "Human Resources"`
**Code (what you write in the interview):**
```python
text = "Human Resources"

vowels = "aeiou"
vowel_count = 0
consonant_count = 0

for character in text.lower():
    # ignore spaces, digits and punctuation
    if character.isalpha():
        if character in vowels:
            vowel_count += 1
        else:
            consonant_count += 1

print("Vowels:", vowel_count)
print("Consonants:", consonant_count)
```
**Output:**
```
Vowels: 6
Consonants: 8
```
**What it means:** "Human Resources" has 14 letters: 6 vowels (u, a, e, o, u, e) and 8 consonants; the space is ignored.
**Alternative:** `sum(1 for c in text.lower() if c in "aeiou")` for vowels only.
**Likely follow-ups:**
- *Is "y" a vowel?* Say the assumption out loud; here it counts as a consonant.
- *Count each vowel separately?* Use a dictionary as in Q3.
**Common mistakes:** Counting spaces as consonants; forgetting uppercase vowels.

### Q11 ⭐⭐⭐ 🟢 What is the difference between a list and a tuple, and what does mutable versus immutable mean?
**Asked at:** commonly asked (no company-specific report found); list vs tuple appears in generic Python interview lists.
**What the interviewer is checking:** Do you understand changeability, and its practical effects (safety, dictionary keys)?
**Say this in the interview:** "A list can be changed after it is created, a tuple cannot. Mutable means can be changed in place, immutable means it cannot. I use a tuple for fixed data like a (latitude, longitude) pair."
**Explain simply:**
- *Mutable*: the object can be changed after creation (list, dictionary, set).
- *Immutable*: it cannot (tuple, string, number); you can only make a new one.
- Lists use `[ ]`, tuples use `( )`.
- Because a tuple never changes, it can be a dictionary key; a list cannot.
- Tuples are slightly smaller and faster, and signal "do not modify this".
**Sample data:** a list and a tuple of skills.
**Code (what you write in the interview):**
```python
skills_list = ["SQL", "Excel"]
skills_list[0] = "Python"      # works: a list can change
skills_list.append("Tableau")
print(skills_list)

skills_tuple = ("SQL", "Excel")
skills_tuple[0] = "Python"     # fails: a tuple cannot change
```
**Output:**
```
['Python', 'Excel', 'Tableau']
TypeError: 'tuple' object does not support item assignment
```
**What it means:** The list was edited freely; the tuple refused any edit.
**Likely follow-ups:**
- *Can a tuple hold a list?* Yes, and that inner list can still change; the tuple only fixes which objects it holds.
- *Single-item tuple?* `(5,)` with the comma.
**Common mistakes:** Thinking `(5)` is a tuple (it is just the number 5); saying tuples are "faster" without noting the gain is small.

### Q12 ⭐⭐⭐ 🟢 What is a list comprehension? Rewrite a loop that squares only the even numbers of a list as one.
**Asked at:** commonly asked; a list comprehension question appears in a 2024 Accenture Python developer candidate report (developer role, not DA).
**What the interviewer is checking:** Can you convert a loop to the compact form, and read it back?
**Say this in the interview:** "A list comprehension builds a new list in one line: what to keep, a for loop, and an optional if filter. It is the same as the loop with append."
**Explain simply:**
- Pattern: `[expression for item in list if condition]`.
- Read it as: "give me number squared, for each number in numbers, if the number is even".
- Use it when it stays short; for complex logic a normal loop is more readable.
**Sample data:** `numbers = [1, 2, 3, 4, 5, 6]`
**Code (what you write in the interview):**
```python
numbers = [1, 2, 3, 4, 5, 6]

# loop version
squares_of_evens = []
for number in numbers:
    if number % 2 == 0:
        squares_of_evens.append(number ** 2)
print(squares_of_evens)

# list comprehension version: [what to keep  for item in list  if condition]
squares_of_evens = [number ** 2 for number in numbers if number % 2 == 0]
print(squares_of_evens)
```
**Output:**
```
[4, 16, 36]
[4, 16, 36]
```
**What it means:** Both give the squares of 2, 4 and 6; the comprehension is the loop on one line.
**Likely follow-ups:**
- *Dictionary comprehension?* `{n: n ** 2 for n in numbers}` (see Q29).
- *Is it faster?* Usually a bit, but readability is the main reason.
**Common mistakes:** Putting the `if` before the `for`; stuffing nested logic into one unreadable line.

### Q13 ⭐⭐⭐ 🟢 Write code to find the factorial of a number.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Loop basics and the 0! = 1 edge case.
**Say this in the interview:** "Factorial of n is 1 x 2 x ... x n. I start the result at 1 and multiply by each number up to n. Zero factorial is 1, which this handles naturally."
**Explain simply:**
- 5! (five factorial) = 5 x 4 x 3 x 2 x 1 = 120.
- `range(2, n + 1)` gives 2 up to n; multiplying by 1 is pointless.
- For n = 0 or 1 the loop does not run and the answer stays 1, which is correct.
**Sample data:** none needed (calls with 5 and 0).
**Code (what you write in the interview):**
```python
def factorial(n):
    result = 1
    for number in range(2, n + 1):
        result = result * number
    return result

print(factorial(5))
print(factorial(0))
```
**Output:**
```
120
1
```
**What it means:** 5! is 120 and 0! is defined as 1.
**Alternative:** `math.factorial(5)` from the standard library; or recursion (see Q51).
**Likely follow-ups:**
- *Negative input?* Factorial is not defined; raise an error.
- *Very large n?* Python integers do not overflow, but the number gets huge.
**Common mistakes:** Starting `result = 0` (everything becomes 0); `range(1, n)` which misses n.

### Q14 ⭐⭐⭐ 🟡 Write code to check whether two strings are anagrams of each other.
**Asked at:** AmbitionBox Accenture Data Science Analyst candidate report (anagram code, snippet only); Glassdoor Python DA snippets mention anagram tasks.
**What the interviewer is checking:** Can you compare two strings by their letters, ignoring order and case?
**Say this in the interview:** "Two words are anagrams if they use exactly the same letters the same number of times. If I sort the letters of both, they must be equal."
**Explain simply:**
- *Anagram*: a rearrangement of the same letters ("listen" and "silent").
- `sorted(text)` returns the letters in alphabetical order as a list; equal lists mean same letters and counts.
- Lowercase first, or "L" and "l" would differ.
**Sample data:** `first = "Listen"`, `second = "Silent"`
**Code (what you write in the interview):**
```python
first = "Listen"
second = "Silent"

# anagrams have the same letters once sorted (ignore case)
if sorted(first.lower()) == sorted(second.lower()):
    print("Anagrams")
else:
    print("Not anagrams")
```
**Output:**
```
Anagrams
```
**What it means:** Both words contain the same letters the same number of times.
**Alternative:** Count the letters of each with a dictionary (Q3) and compare the two dictionaries; this is faster for long strings (one pass instead of sorting).
**Likely follow-ups:**
- *Ignore spaces?* Remove them first with `.replace(" ", "")`.
- *Time complexity?* Sorting is n log n; counting is n.
**Common mistakes:** Comparing only the set of letters (misses repeat counts: "aab" vs "abb"); forgetting case.

### Q15 ⭐⭐⭐ 🟡 Write code to find the second largest number in a list.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you handle duplicates of the top value?
**Say this in the interview:** "I find the largest, then scan again for the biggest value that is strictly smaller than it. That way a repeated top value is not counted as the second."
**Explain simply:**
- If the top salary appears twice, the "second largest" should be the next different value, not the same one again.
- `second_largest = None` means "nothing found yet"; this also covers lists with only one distinct value.
- Two simple passes keep the logic easy to explain.
**Sample data:** `salaries = [42000, 55000, 61000, 61000, 47000]`
**Code (what you write in the interview):**
```python
salaries = [42000, 55000, 61000, 61000, 47000]

largest = max(salaries)
second_largest = None
for salary in salaries:
    # must be smaller than the largest, so duplicates of the top value are skipped
    if salary < largest:
        if second_largest is None or salary > second_largest:
            second_largest = salary

print(second_largest)
```
**Output:**
```
55000
```
**What it means:** 61000 is the top value (it appears twice); 55000 is the next distinct salary.
**Alternative:** `sorted(set(salaries))[-2]`: shortest, but sorts everything and fails if there is only one distinct value.
**Likely follow-ups:**
- *Can it be done in one pass?* Yes, track the largest and second largest together.
- *Interviewer says no max()?* Use the Q5 loop for the first step.
**Common mistakes:** Returning the second item of a sorted list without removing duplicates (gives 61000); crashing on a list with fewer than two distinct values.

### Q16 ⭐⭐⭐ 🟡 Write a function that takes a list of words and returns each word's count, then prints the three most frequent words, without using Counter.
**Asked at:** PracHub "count word frequency and print top three words" (snippet only); Counter-free variants are a standard follow-up to Q4.
**What the interviewer is checking:** A clean function, a manual counter, and sorting a dictionary by value.
**Say this in the interview:** "The function counts into a dictionary and returns it. Then I sort the items by count, highest first, and print the first three."
**Explain simply:**
- `word_counts.items()` gives (word, count) pairs.
- `sorted(..., key=..., reverse=True)` sorts by the count (second item of each pair), biggest first.
- A *lambda* is a tiny one-line function; here it says "sort by the second item".
- `[:3]` takes the first three pairs.
**Sample data:** `words = ["sql", "python", "sql", "excel", "python", "sql", "tableau", "excel"]`
**Code (what you write in the interview):**
```python
def count_words(words):
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

words = ["sql", "python", "sql", "excel", "python", "sql", "tableau", "excel"]
word_counts = count_words(words)

# sort (word, count) pairs by count, highest first
sorted_counts = sorted(word_counts.items(), key=lambda pair: pair[1], reverse=True)

# print the top three
for word, count in sorted_counts[:3]:
    print(word, count)
```
**Output:**
```
sql 3
python 2
excel 2
```
**What it means:** SQL is the most frequent; Python and Excel tie at 2. Python's sort is stable, so ties keep first-seen order.
**Likely follow-ups:**
- *Ties?* Say how you want to break them (alphabetically, or keep all tied words).
- *With Counter?* `Counter(words).most_common(3)`.
**Common mistakes:** Sorting by the word instead of the count (forgetting `key`); fewer than three distinct words is fine, slicing never errors.

### Q17 ⭐⭐⭐ 🟡 Write code to find the first non-repeating character in a string.
**Asked at:** commonly asked (no company-specific report found); a classic string-frequency problem.
**What the interviewer is checking:** Do you see it needs two passes: count first, then find in original order?
**Say this in the interview:** "First pass counts every character. Second pass walks the string in its original order and returns the first character whose count is one."
**Explain simply:**
- The dictionary only knows the counts; the second pass over the original string is what tells us which unique character comes first.
- `break` stops the loop at the first match.
- If every character repeats, the answer stays `None`.
**Sample data:** `text = "swiss"`
**Code (what you write in the interview):**
```python
text = "swiss"

character_counts = {}
for character in text:
    character_counts[character] = character_counts.get(character, 0) + 1

# walk in original order and return the first character seen only once
first_unique = None
for character in text:
    if character_counts[character] == 1:
        first_unique = character
        break

print(first_unique)
```
**Output:**
```
w
```
**What it means:** "s" repeats three times; "w" is the first letter that appears only once.
**Likely follow-ups:**
- *All repeat ("aabb")?* The result is `None`; say you would return that or -1.
- *Complexity?* Two passes, so linear time.
**Common mistakes:** Returning the first character with a low count in dictionary order; not handling the "no unique character" case.

### Q18 ⭐⭐ 🟢 Write code to print the first n numbers of the Fibonacci series.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Loop with two running variables and simultaneous assignment.
**Say this in the interview:** "Each number is the sum of the previous two, starting 0 and 1. I keep two variables and move them forward each step."
**Explain simply:**
- *Fibonacci series*: 0, 1, 1, 2, 3, 5, 8... each term = sum of the two before it.
- `previous, current = current, previous + current` updates both at once, so no temporary variable is needed.
- `end=" "` keeps the numbers on one line.
**Sample data:** none needed (`n = 10`).
**Code (what you write in the interview):**
```python
n = 10

previous, current = 0, 1
for _ in range(n):
    print(previous, end=" ")
    previous, current = current, previous + current
```
**Output:**
```
0 1 1 2 3 5 8 13 21 34 
```
**What it means:** These are the first 10 Fibonacci numbers.
**Alternative:** Recursion is shorter to write but very slow for large n (it recomputes values).
**Likely follow-ups:**
- *Return a list instead?* Append to a list inside the loop.
- *n = 0 or 1?* Prints nothing or just 0; both correct.
**Common mistakes:** Updating the two variables on separate lines, which overwrites a value too early; starting the series at 1, 1.

### Q19 ⭐⭐ 🟢 Write code to check whether a number is an Armstrong number.
**Asked at:** InkRevenue Jr Data Analyst (Glassdoor snippet lists Armstrong, prime and palindrome; small employer, low relevance to India); otherwise commonly asked as a classic warm-up.
**What the interviewer is checking:** Whether you can break a number into digits and combine a loop with a simple rule.
**Say this in the interview:** "An Armstrong number equals the sum of its digits, each raised to the power of the number of digits. For 153: 1 cubed + 5 cubed + 3 cubed = 153. I convert the number to a string to walk through its digits."
**Explain simply:**
- 153 has 3 digits, so each digit is raised to the power 3: 1 + 125 + 27 = 153.
- `str(number)` turns the number into text so a `for` loop can visit each digit.
- `len(digits)` gives the number of digits, which is the power to use.
- Another example: 1634 (4 digits) is Armstrong because 1^4 + 6^4 + 3^4 + 4^4 = 1634.
**Sample data:** `number = 153`
**Code (what you write in the interview):**
```python
number = 153

# split the number into digits
digits = str(number)
power = len(digits)

# raise each digit to the power of the digit count and add them up
total = 0
for digit in digits:
    total = total + int(digit) ** power

if total == number:
    print(number, "is an Armstrong number")
else:
    print(number, "is not an Armstrong number")
```
**Output:**
```text
153 is an Armstrong number
```
**What it means:** The digit powers add back up to the original number, so it qualifies.
**Alternative:** One line: `total = sum(int(d) ** len(str(number)) for d in str(number))`. Shorter, but the loop is easier to explain.
**Likely follow-ups:** 1) *Why use len() for the power?* Because the rule depends on how many digits there are, not always 3. 2) *Does 9474 work?* Yes: 9^4 + 4^4 + 7^4 + 4^4 = 9474.
**Common mistakes:** Hard-coding the power as 3; forgetting `int(digit)` (a text character cannot be raised to a power).

### Q20 ⭐⭐ 🟢 Write code to find the sum of the digits of a number.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know `%` (remainder) and `//` (whole-number division) and can use them in a loop.
**Say this in the interview:** "I take the last digit with `% 10`, add it to a total, then remove it with `// 10`, and repeat until the number reaches zero."
**Explain simply:**
- `4825 % 10` gives 5, the last digit (the remainder after dividing by 10).
- `4825 // 10` gives 482, the number with its last digit chopped off (floor division).
- A `while` loop repeats as long as the condition is true; here, while digits remain.
- Quick alternative idea: turn the number into text and add each character as a number.
**Sample data:** `number = 4825` (4 + 8 + 2 + 5 = 19)
**Code (what you write in the interview):**
```python
number = 4825
total = 0

# take the last digit with % 10, then drop it with // 10
while number > 0:
    total = total + number % 10
    number = number // 10

print(total)
```
**Output:**
```text
19
```
**What it means:** The digits 4, 8, 2 and 5 add up to 19.
**Alternative:** `sum(int(digit) for digit in str(4825))`. Shorter, and fine to give if the interviewer allows converting to a string.
**Likely follow-ups:** 1) *What about a negative number?* Use `abs(number)` first, otherwise the loop never runs. 2) *What about 0?* The loop does not run and the answer is 0, which is correct.
**Common mistakes:** Using `/` instead of `//` (gives a decimal and the loop never ends cleanly); changing `number` and then trying to print the original afterwards.

### Q21 ⭐⭐ 🟢 How do you swap the values of two variables in Python, with and without a temporary variable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the classic temp-variable method and Python's one-line tuple swap.
**Say this in the interview:** "With a temp variable I park one value in `temp`, copy the other across, then put temp back. In Python I can simply write `a, b = b, a`, which swaps them in one line."
**Explain simply:**
- Writing `a = b` straight away would lose the old value of `a`, so the temp variable keeps it safe.
- `a, b = b, a` works because Python builds a pair `(b, a)` first (a "tuple", a fixed pair of values) and then unpacks it into `a` and `b`.
- No temp variable is needed, and it works for any type of value, not just numbers.
**Sample data:** `a = 10`, `b = 20`
**Code (what you write in the interview):**
```python
a = 10
b = 20

# with a temporary variable
temp = a
a = b
b = temp
print(a, b)

# without a temporary variable (tuple unpacking)
a, b = b, a
print(a, b)
```
**Output:**
```text
20 10
10 20
```
**What it means:** The first swap gives 20 and 10; the second swap flips them back to 10 and 20.
**Alternative:** For numbers only, `a = a + b; b = a - b; a = a - b` swaps without a temp, but it is a trick that can lose accuracy with decimal numbers (rounding) and confuses readers; the tuple swap is the Pythonic answer.
**Likely follow-ups:** 1) *Can you swap list items this way?* Yes: `numbers[0], numbers[1] = numbers[1], numbers[0]`. 2) *Why does the right side not get confused?* It is fully worked out before any assignment happens.
**Common mistakes:** Writing `a = b` then `b = a` (both end up with the same value).

### Q22 ⭐⭐ 🟢 Write code to count the even and odd numbers in a list.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Loops, the `%` remainder operator and counters.
**Say this in the interview:** "I loop through the list, and for each number check `number % 2 == 0`. If true it is even, otherwise odd, and I add one to the matching counter."
**Explain simply:**
- `%` gives the remainder of a division; any even number leaves remainder 0 when divided by 2.
- A counter is a variable that starts at 0 and goes up by 1 each time something matches.
- Only one `if/else` is needed because a whole number is either even or odd.
**Sample data:** `numbers = [4, 7, 10, 13, 22, 35, 8]`
**Code (what you write in the interview):**
```python
numbers = [4, 7, 10, 13, 22, 35, 8]
even_count = 0
odd_count = 0

for number in numbers:
    if number % 2 == 0:
        even_count = even_count + 1
    else:
        odd_count = odd_count + 1

print("Even:", even_count)
print("Odd:", odd_count)
```
**Output:**
```text
Even: 4
Odd: 3
```
**What it means:** Four of the seven numbers are even (4, 10, 22, 8) and three are odd (7, 13, 35).
**Alternative:** `even_count = len([n for n in numbers if n % 2 == 0])`, then `odd_count = len(numbers) - even_count`.
**Likely follow-ups:** 1) *Does it work for negative numbers?* Yes, `-4 % 2` is 0 in Python. 2) *What if the list is empty?* Both counts stay 0.
**Common mistakes:** Using `=` instead of `==` in the condition; forgetting to set the counters to 0 before the loop.

### Q23 ⭐⭐ 🟢 Write code to reverse a list in three different ways.
**Asked at:** commonly asked (no company-specific report found); a variant of the string-reversal opener found in Analytics Vidhya and Glassdoor snippets.
**What the interviewer is checking:** That you know the slice, `reversed()` and `.reverse()`, and that one of them changes the original list.
**Say this in the interview:** "Slicing with `[::-1]` and `reversed()` give a new reversed list and leave the original alone. `.reverse()` flips the original list in place and returns nothing."
**Explain simply:**
- `[::-1]` is a slice that steps backwards through the whole list.
- `reversed()` gives a special object that walks the list backwards; wrap it in `list()` to see the values.
- `.reverse()` is a list method that changes the list itself ("in place") and returns `None`.
**Sample data:** `numbers = [1, 2, 3, 4, 5]`
**Code (what you write in the interview):**
```python
numbers = [1, 2, 3, 4, 5]

# way 1: slicing (makes a new reversed list)
print(numbers[::-1])

# way 2: reversed() built-in (makes a new list)
print(list(reversed(numbers)))

# way 3: reverse() method (changes the original list)
numbers.reverse()
print(numbers)
```
**Output:**
```text
[5, 4, 3, 2, 1]
[5, 4, 3, 2, 1]
[5, 4, 3, 2, 1]
```
**What it means:** All three give the same result; only the last one permanently changed `numbers`.
**Alternative:** A plain loop that builds a new list from the end: `for i in range(len(numbers) - 1, -1, -1): new_list.append(numbers[i])`.
**Likely follow-ups:** 1) *Which is the fastest to type?* The slice. 2) *Which keeps the original?* Slice and `reversed()`.
**Common mistakes:** Writing `numbers = numbers.reverse()` (that sets `numbers` to `None`); printing `reversed(numbers)` directly and getting an object address instead of the values.

### Q24 ⭐⭐ 🟢 Write code to find the longest word in a sentence.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** String splitting and the "keep the best so far" pattern.
**Say this in the interview:** "I split the sentence into words, keep a variable for the longest word so far, and replace it whenever I meet a longer one."
**Explain simply:**
- `.split()` with no argument cuts text at every space and returns a list of words.
- `longest_word` starts as an empty string, so the first real word always beats it.
- Using `>` (not `>=`) means that in a tie the first word found is kept.
**Sample data:** `sentence = "HR analytics helps reduce employee attrition"`
**Code (what you write in the interview):**
```python
sentence = "HR analytics helps reduce employee attrition"
words = sentence.split()

longest_word = ""
for word in words:
    # keep the word only if it is longer than the best one so far
    if len(word) > len(longest_word):
        longest_word = word

print(longest_word)
```
**Output:**
```text
analytics
```
**What it means:** "analytics" (9 letters) is the longest; "attrition" also has 9 letters but comes later, so it does not replace it.
**Alternative:** `longest_word = max(words, key=len)`, which also returns the first one in a tie.
**Likely follow-ups:** 1) *What about punctuation?* "end." counts 4 letters; strip it first with `word.strip(".,!?")`. 2) *How to return all words tied for longest?* Find the max length first, then collect every word of that length.
**Common mistakes:** Comparing the words themselves instead of their lengths; starting `longest_word` as `None` and then calling `len()` on it (error).

### Q25 ⭐⭐ 🟢 Write code to reverse the order of words in a sentence.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can combine `split`, reverse and `join`, and do not confuse this with reversing letters.
**Say this in the interview:** "I split the sentence into a list of words, reverse the list, and join it back with spaces. The words themselves stay spelled the same."
**Explain simply:**
- `.split()` turns the sentence into a list of words.
- `.reverse()` flips the order of that list.
- `" ".join(words)` glues the list back into one string using a space between words.
**Sample data:** `sentence = "payroll data is ready"`
**Code (what you write in the interview):**
```python
sentence = "payroll data is ready"

words = sentence.split()
words.reverse()
reversed_sentence = " ".join(words)

print(reversed_sentence)
```
**Output:**
```text
ready is data payroll
```
**What it means:** The last word comes first, and each word is untouched.
**Alternative:** One line: `" ".join(sentence.split()[::-1])`.
**Likely follow-ups:** 1) *What if there are extra spaces?* `.split()` with no argument ignores them. 2) *How would you reverse each word but keep the order?* `" ".join(word[::-1] for word in sentence.split())`.
**Common mistakes:** Using `sentence[::-1]` (that reverses every letter, giving "ydaer atad..."); writing `words = words.reverse()` (gives `None`).

### Q26 ⭐⭐ 🟢 Write code to find the common elements between two lists, for example employees present in both the HR list and the payroll list.
**Asked at:** commonly asked (no company-specific report found); the HR framing is a realistic live-coding variant.
**What the interviewer is checking:** Loops with membership checks, and whether you know sets as a shortcut.
**Say this in the interview:** "I loop over the HR list and keep each ID that is also in the payroll list. A set intersection does the same in one step, but I would mention that it loses the original order."
**Explain simply:**
- `employee in payroll_list` asks "is this ID anywhere in that list?" and gives True or False.
- The loop keeps the HR order, which is useful when order matters.
- A set is a collection of unique items with no order; sets make "in both" and "in one but not the other" very quick.
**Sample data:** `hr_list = ["E101", "E102", "E103", "E104", "E105"]`, `payroll_list = ["E103", "E104", "E105", "E106"]`
**Code (what you write in the interview):**
```python
hr_list = ["E101", "E102", "E103", "E104", "E105"]
payroll_list = ["E103", "E104", "E105", "E106"]

common_employees = []
for employee in hr_list:
    if employee in payroll_list:
        common_employees.append(employee)

print(common_employees)
```
**Output:**
```text
['E103', 'E104', 'E105']
```
**What it means:** Three employees appear in both HR and payroll records.
**Alternative:** `common_employees = list(set(hr_list) & set(payroll_list))`. Faster for big lists, but the order is not guaranteed.
**Likely follow-ups:** 1) *What if the lists are very large?* Convert the payroll list to a set first so each lookup is fast. 2) *What if IDs repeat?* The loop keeps repeats from the HR list; a set removes them.
**Common mistakes:** Comparing by position (`hr_list[i] == payroll_list[i]`) instead of checking membership; forgetting that IDs like "E103" and "e103" are different text.

### Q27 ⭐⭐ 🟢 Write code to find employees who are in the HR master list but missing from the payroll list, using sets.
**Asked at:** commonly asked (no company-specific report found); a realistic HR-flavoured gap-fill on the set-operations theme.
**What the interviewer is checking:** That you know set difference and why it matters for reconciling two records.
**Say this in the interview:** "I put both ID lists into sets and subtract: HR minus payroll gives everyone who is in HR but not in payroll. Those people may be missing salary."
**Explain simply:**
- A set difference `A - B` means "items in A that are not in B".
- Order matters: `payroll - hr_master` would answer the opposite question (paid but not in HR).
- Sets have no order, so wrap the result in `sorted()` to print it neatly.
- This is a reconciliation check, a very common data-quality task.
**Sample data:** `hr_master = {"E101", "E102", "E103", "E104", "E105"}`, `payroll = {"E103", "E104", "E105", "E106"}`
**Code (what you write in the interview):**
```python
hr_master = {"E101", "E102", "E103", "E104", "E105"}
payroll = {"E103", "E104", "E105", "E106"}

# in HR but not in payroll
missing_from_payroll = hr_master - payroll

print(sorted(missing_from_payroll))
```
**Output:**
```text
['E101', 'E102']
```
**What it means:** E101 and E102 are in the HR master list but have no payroll record, so they need checking.
**Alternative:** `hr_master.difference(payroll)` does the same thing and also accepts a list. If the data starts as lists, use `set(hr_list) - set(payroll_list)`.
**Likely follow-ups:** 1) *How to find IDs in only one of the two lists?* Symmetric difference: `hr_master ^ payroll`. 2) *Why use sets and not a loop?* It is shorter and faster on large lists.
**Common mistakes:** Subtracting in the wrong direction; writing `{}` to make an empty set (that creates an empty dictionary; use `set()`).

### Q28 ⭐⭐ 🟢 Write code to merge two dictionaries in Python.
**Asked at:** commonly asked (no company-specific report found); dictionary questions appear in Glassdoor Python DA snippets.
**What the interviewer is checking:** That you know a modern merge and what happens when keys clash.
**Say this in the interview:** "I use `|` in Python 3.9 and later, or `{**a, **b}` in older versions. If the same key is in both, the value from the second dictionary wins."
**Explain simply:**
- A dictionary stores pairs of key and value, such as employee ID and name.
- Keys must be unique, so a repeated key keeps only one value: the later one.
- `{**a, **b}` unpacks both dictionaries into a new one; it works on Python 3.5 and above.
- `a.update(b)` also works but changes `a` itself.
**Sample data:** `hr_data = {"E101": "Asha", "E102": "Ravi"}`, `new_hires = {"E103": "Meena", "E102": "Ravi K"}`
**Code (what you write in the interview):**
```python
hr_data = {"E101": "Asha", "E102": "Ravi"}
new_hires = {"E103": "Meena", "E102": "Ravi K"}

# Python 3.9+: the right-hand dictionary wins on duplicate keys
merged = hr_data | new_hires

print(merged)
```
**Output:**
```text
{'E101': 'Asha', 'E102': 'Ravi K', 'E103': 'Meena'}
```
**What it means:** All three employees are present, and E102 shows the updated name from the second dictionary.
**Alternative:** `merged = {**hr_data, **new_hires}` (works on older Python 3 versions).
**Likely follow-ups:** 1) *Which value is kept for a repeated key?* The last one. 2) *Is the original changed?* Not with `|` or `{**}`; `update()` changes it.
**Common mistakes:** Using `+` on dictionaries (error); expecting both values to be kept for a repeated key.

### Q29 ⭐⭐ 🟢 Write code to create the dictionary {1: 1, 2: 4, 3: 9, 4: 16, 5: 25} the most Pythonic way.
**Asked at:** Glassdoor Python data analyst snippets mention a "pythonic dictionary creation" question (snippet title only); otherwise commonly asked.
**What the interviewer is checking:** Whether you know dictionary comprehension.
**Say this in the interview:** "A dictionary comprehension: `{number: number ** 2 for number in range(1, 6)}`. It builds the whole dictionary in one readable line."
**Explain simply:**
- A comprehension is a compact way of building a collection from a loop.
- The shape is `{key: value for item in something}`.
- `range(1, 6)` gives 1 to 5; the end number 6 is not included.
- `** 2` means "to the power of 2" (squared).
**Sample data:** none needed.
**Code (what you write in the interview):**
```python
squares = {number: number ** 2 for number in range(1, 6)}

print(squares)
```
**Output:**
```text
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```
**What it means:** Each number is the key and its square is the value.
**Alternative:** The plain loop: `squares = {}` then `for number in range(1, 6): squares[number] = number ** 2`. Same result, a little longer.
**Likely follow-ups:** 1) *How to keep only even numbers?* Add `if number % 2 == 0` at the end. 2) *Can you do this for a list?* Yes, a list comprehension uses `[ ]`.
**Common mistakes:** Writing `range(1, 5)` (misses 5); using `[ ]` and getting a list; forgetting the colon between key and value.

### Q30 ⭐⭐ 🟢 Write code to print the multiplication table of a number.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic `for` loop with `range`.
**Say this in the interview:** "I loop `i` from 1 to 10 and print the number times `i` on each line."
**Explain simply:**
- `range(1, 11)` produces 1 up to 10 (the end value 11 is excluded).
- `print` with commas puts spaces between the parts automatically.
- Ask whether the interviewer wants 10 rows or a different limit; it is a one-number change.
**Sample data:** `number = 7`
**Code (what you write in the interview):**
```python
number = 7

for i in range(1, 11):
    print(number, "x", i, "=", number * i)
```
**Output:**
```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```
**What it means:** Ten lines, each showing the number multiplied by 1 through 10.
**Alternative:** An f-string: `print(f"{number} x {i} = {number * i}")`, which many interviewers like because it is tidy.
**Likely follow-ups:** 1) *How to read the number from the user?* `number = int(input())`. 2) *How to print up to a custom limit?* Use a second variable `limit` and `range(1, limit + 1)`.
**Common mistakes:** `range(1, 10)` (stops at 9); forgetting `int()` on typed input, which makes `number * i` repeat text instead of multiplying.

### Q31 ⭐⭐ 🟢 Write code to check whether a year is a leap year.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Careful handling of a rule with an exception, using `and`/`or`.
**Say this in the interview:** "A year is a leap year if it is divisible by 4, except century years like 1900, which must be divisible by 400. So 2000 is a leap year but 1900 is not."
**Explain simply:**
- Divisible by 4 and not by 100: leap (2024).
- Divisible by 100 but not by 400: not leap (1900).
- Divisible by 400: leap (2000).
- Brackets matter: `and` is worked out before `or`, so the brackets make the rule clear.
**Sample data:** `year = 2024`
**Code (what you write in the interview):**
```python
year = 2024

# divisible by 4, except century years, which must be divisible by 400
if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print(year, "is a leap year")
else:
    print(year, "is not a leap year")
```
**Output:**
```text
2024 is a leap year
```
**What it means:** 2024 divides by 4 and is not a century year, so February has 29 days.
**Alternative:** The built-in `calendar.isleap(year)` after `import calendar`; mention it, but write the rule yourself in the interview.
**Likely follow-ups:** 1) *Is 1900 a leap year?* No (century, not divisible by 400). 2) *Is 2000?* Yes.
**Common mistakes:** Checking only `year % 4 == 0`; mixing up `and` with `or`.

### Q32 ⭐⭐ 🟢 Write code to print a right-angled triangle pattern of stars with n rows.
**Asked at:** commonly asked (no company-specific report found); pattern printing is a classic campus-style question (the diamond variant is in the Deloitte campus note in the research).
**What the interviewer is checking:** Loop logic: row number controls how many stars to print.
**Say this in the interview:** "Row 1 has one star, row 2 has two, and so on. So I loop over rows 1 to n and print `"*" * row`."
**Explain simply:**
- In Python, multiplying text by a number repeats it: `"*" * 3` gives `***`.
- `range(1, n + 1)` runs from 1 to n inclusive.
- `print` moves to a new line after each call, so each row appears on its own line.
**Sample data:** `n = 5`
**Code (what you write in the interview):**
```python
n = 5

for row in range(1, n + 1):
    print("*" * row)
```
**Output:**
```text
*
**
***
****
*****
```
**What it means:** The number of stars grows by one each row, forming a right-angled triangle.
**Alternative:** The nested-loop version, if asked not to use `"*" * row`: an inner `for` prints `"*"` with `end=""`, then an empty `print()` moves to the next line.
**Likely follow-ups:** 1) *How to make it right-aligned?* Print `" " * (n - row) + "*" * row`. 2) *How to flip it upside down?* Use `range(n, 0, -1)`.
**Common mistakes:** `range(1, n)` (one row short); using `+` instead of `*` on text.

### Q33 ⭐⭐ 🟢 Write code that loops over a list of employee records and calculates the attrition rate.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill, since attrition is the core HR metric.
**What the interviewer is checking:** That you can loop over records, count a condition, and apply the attrition formula correctly.
**Say this in the interview:** "Attrition rate is employees who left divided by total employees, times 100. I loop over the records, count the ones with status Left, and divide by the list length."
**Explain simply:**
- Attrition (or turnover) means the share of employees who leave in a period.
- Each employee is a dictionary (key and value pairs), so `employee["status"]` reads the status.
- `len(employees)` is the total headcount. Strictly, the textbook formula uses the average headcount over the period; here we use the simple total.
- `:.1f` in the f-string shows one decimal place.
**Sample data:**

| id | status |
|---|---|
| E101 | Active |
| E102 | Left |
| E103 | Active |
| E104 | Left |
| E105 | Active |

**Code (what you write in the interview):**
```python
employees = [
    {"id": "E101", "status": "Active"},
    {"id": "E102", "status": "Left"},
    {"id": "E103", "status": "Active"},
    {"id": "E104", "status": "Left"},
    {"id": "E105", "status": "Active"},
]

left_count = 0
for employee in employees:
    if employee["status"] == "Left":
        left_count = left_count + 1

# attrition rate = employees who left / total employees
attrition_rate = left_count / len(employees) * 100
print(f"Attrition rate: {attrition_rate:.1f}%")
```
**Output:**
```text
Attrition rate: 40.0%
```
**What it means:** 2 of the 5 employees left, so attrition is 40%.
**Alternative:** `left_count = sum(1 for employee in employees if employee["status"] == "Left")`.
**Likely follow-ups:** 1) *What if the list is empty?* Dividing by zero raises an error, so check `if len(employees) == 0` first. 2) *What denominator do HR teams really use?* Average headcount of the period (opening plus closing, divided by 2).
**Common mistakes:** Dividing by the number of Active employees instead of everyone; forgetting to multiply by 100 (the result is 0.4, not 40%); not handling the empty list.

### Q34 ⭐⭐ 🟢 Write code to count how many employees in a list of dictionaries have more than 3 years of tenure.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill.
**What the interviewer is checking:** Loop plus condition on a dictionary field, and attention to "more than" meaning strictly greater.
**Say this in the interview:** "I loop through the employees, and when `tenure_years` is greater than 3 I add one to a counter. Someone with exactly 3 years is not counted, because the question says more than 3."
**Explain simply:**
- Tenure means how long someone has worked for the company.
- `>` is strictly greater; `>=` would include exactly 3 years.
- Decimal tenure such as 4.5 works with the same comparison.
**Sample data:**

| name | tenure_years |
|---|---|
| Asha | 5 |
| Ravi | 2 |
| Meena | 3 |
| John | 4.5 |

**Code (what you write in the interview):**
```python
employees = [
    {"name": "Asha", "tenure_years": 5},
    {"name": "Ravi", "tenure_years": 2},
    {"name": "Meena", "tenure_years": 3},
    {"name": "John", "tenure_years": 4.5},
]

count = 0
for employee in employees:
    if employee["tenure_years"] > 3:
        count = count + 1

print(count)
```
**Output:**
```text
2
```
**What it means:** Asha (5) and John (4.5) have more than 3 years; Meena has exactly 3, so she is excluded.
**Alternative:** `sum(1 for employee in employees if employee["tenure_years"] > 3)`.
**Likely follow-ups:** 1) *What if a record has no tenure key?* `employee["tenure_years"]` raises a KeyError; use `employee.get("tenure_years", 0)`. 2) *How to also list their names?* Append `employee["name"]` to a list.
**Common mistakes:** Using `>=` and counting Meena; returning the whole list instead of the count.

### Q35 ⭐⭐ 🟢 What is the difference between a function that prints a value and one that returns it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that `print` only shows text, while `return` hands a value back so the rest of the program can use it.
**Say this in the interview:** "`print` just displays something on the screen; the function gives nothing back, so the result is `None`. `return` sends the value back to the caller, so I can store it, calculate with it or test it."
**Explain simply:**
- `print` is for humans reading the screen. The value disappears after it is shown.
- `return` is for the program. The caller receives the value and can reuse it.
- A function with no `return` quietly gives back `None` (Python's "nothing" value).
- In real analysis work, functions should return results; print only at the very end or for checking.
**Sample data:** none needed.
**Code (what you write in the interview):**
```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

result_1 = add_print(2, 3)
result_2 = add_return(2, 3)

print(result_1)
print(result_2 * 10)
```
**Output:**
```text
5
None
50
```
**What it means:** The first "5" was printed inside `add_print`, but `result_1` holds `None`. `add_return` gave back 5, so multiplying by 10 worked and gave 50. `result_1 * 10` would have crashed.
**Alternative:** None needed; a good one-line summary is "print shows, return gives".
**Likely follow-ups:** 1) *Can a function return several values?* Yes, as a tuple: `return total, average`. 2) *What happens to code after `return`?* It does not run; `return` ends the function.
**Common mistakes:** Using `print` inside a function and then trying to use its result; writing code after `return` and expecting it to run.

### Q36 ⭐⭐ 🟢 What is a lambda function, and how is it different from a function defined with def?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know lambda is a short anonymous function and when it is appropriate.
**Say this in the interview:** "A lambda is a small one-line function without a name, made of a single expression. `def` can hold many lines and has a name. I use lambda for quick throwaway jobs, such as the `key` for sorting."
**Explain simply:**
- Anonymous means it needs no name; it returns the result of its one expression automatically (no `return` keyword).
- A lambda can hold only one expression, so no several-line logic, loops or assignments inside it.
- `def` is better when the logic needs a name, a description, several steps or reuse in many places.
- Both produce an ordinary function that you call the same way.
**Sample data:** `employees = [("Asha", 50000), ("Ravi", 42000), ("Meena", 61000)]` (name, salary)
**Code (what you write in the interview):**
```python
# lambda: one expression, no name needed
add_bonus = lambda salary: salary + 5000

# the same thing with def
def add_bonus_def(salary):
    return salary + 5000

print(add_bonus(50000))
print(add_bonus_def(50000))

# the usual use: a quick key for sorting
employees = [("Asha", 50000), ("Ravi", 42000), ("Meena", 61000)]
employees.sort(key=lambda employee: employee[1])
print(employees)
```
**Output:**
```text
55000
55000
[('Ravi', 42000), ('Asha', 50000), ('Meena', 61000)]
```
**What it means:** Both functions behave the same; the lambda in `sort` told Python to order people by salary (second item).
**Alternative:** Assigning a lambda to a name (as above) works, but style guides prefer `def` in that case; the real value of lambda is passing it directly into `sort`, `sorted`, `map` or pandas `apply`.
**Likely follow-ups:** 1) *Can a lambda have several arguments?* Yes: `lambda a, b: a + b`. 2) *Can it contain if/else?* Yes, as a one-line expression: `lambda x: "high" if x > 50000 else "low"`.
**Common mistakes:** Cramming complex logic into a lambda (hard to read); writing `return` inside a lambda (a syntax error).

### Q37 ⭐⭐ 🟢 What is a class and an object in Python? Write a simple Employee class with a method.
**Asked at:** LatentView (2020 campus technical round, OOP basics, per a GfG report); also listed in OOP question banks (foundit, AlmaBetter).
**What the interviewer is checking:** Whether you can explain "blueprint versus real thing" and write a small, correct class.
**Say this in the interview:** "A class is a blueprint, like an employee form template. An object is one filled-in form, for example Asha's record. The class defines what data each employee holds and what they can do."
**Explain simply:**
- A **class** describes the shape: which data (name, salary) and which actions (annual_salary).
- An **object** (also called an instance) is one real employee built from that class.
- Many objects can come from one class, each with its own data.
- A **method** is a function that lives inside a class.
**Sample data:** Two employees: Asha earns 50000 a month, Ravi earns 62000.
**Code (what you write in the interview):**
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12


asha = Employee("Asha", 50000)
ravi = Employee("Ravi", 62000)
print(asha.name, asha.annual_salary())
print(ravi.name, ravi.annual_salary())
```
**Output:**
```text
Asha 600000
Ravi 744000
```
**What it means:** One class made two separate employee objects; each method call used its own object's salary.
**Likely follow-ups:** 1) *How many objects can one class create?* As many as you want. 2) *Is `asha` the class or an object?* An object; `Employee` is the class.
**Common mistakes:** Forgetting `self` in the method definition; calling `Employee.annual_salary()` on the class instead of on an object; forgetting the brackets when calling a method.

### Q38 ⭐⭐ 🟢 What does the self keyword mean in a class method?
**Asked at:** commonly asked in OOP basics (LatentView 2020 campus report mentions OOP basics; no report names `self` specifically).
**What the interviewer is checking:** That you understand `self` means "the object this method is working on".
**Say this in the interview:** "`self` is the object that called the method. When I write `asha.give_raise(5000)`, Python passes `asha` in as `self`, so the method changes Asha's salary and nobody else's."
**Explain simply:**
- `self` is not a magic word, just a strong convention; any name works, but everyone uses `self`.
- Python fills it in automatically; you do not pass it yourself when calling.
- `self.salary` means "the salary stored on this particular object".
- Without `self`, a method has no way to reach the object's own data.
**Sample data:** Asha (50000) and Ravi (62000); only Asha gets a raise of 5000.
**Code (what you write in the interview):**
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def give_raise(self, amount):
        self.salary = self.salary + amount   # self = the employee being called


asha = Employee("Asha", 50000)
ravi = Employee("Ravi", 62000)
asha.give_raise(5000)
print(asha.salary)
print(ravi.salary)
```
**Output:**
```text
55000
62000
```
**What it means:** Only Asha changed, because `self` pointed to Asha during that call.
**Likely follow-ups:** 1) *Can I rename it?* Yes, but do not. 2) *Why do I write `give_raise(self, amount)` but call `give_raise(5000)`?* Python supplies `self` for you.
**Common mistakes:** Writing `salary = salary + amount` without `self.` (it changes a temporary variable, or errors); leaving `self` out of the parameter list (TypeError about too many arguments).

### Q39 ⭐⭐ 🟢 What does the __init__ method do, and how is it different from an ordinary method?
**Asked at:** commonly asked in OOP basics (constructors appear in foundit/AlmaBetter OOP lists; no company-specific report found).
**What the interviewer is checking:** That you know `__init__` sets up a new object automatically.
**Say this in the interview:** "`__init__` is the constructor. Python runs it by itself the moment I create an object, to set the starting values. An ordinary method only runs when I call it by name."
**Explain simply:**
- `__init__` runs once, automatically, at `Employee("Meera")`.
- Its job is to store the starting data (name, salary, status) on `self`.
- An ordinary method (like `leave_company`) runs only when you call it, as often as you like.
- `__init__` should not return a value; it only prepares the object.
- Default values (`salary=30000`) let you skip arguments.
**Sample data:** A new hire, Meera, joins with the default salary.
**Code (what you write in the interview):**
```python
class Employee:
    def __init__(self, name, salary=30000):
        self.name = name
        self.salary = salary
        self.is_active = True

    def leave_company(self):
        self.is_active = False


new_hire = Employee("Meera")
print(new_hire.name, new_hire.salary, new_hire.is_active)
new_hire.leave_company()
print(new_hire.is_active)
```
**Output:**
```text
Meera 30000 True
False
```
**What it means:** `__init__` ran by itself and filled in the values; `leave_company` ran only when called.
**Likely follow-ups:** 1) *Is `__init__` mandatory?* No; without it the object just starts empty. 2) *Is it the same as creating the object?* Not exactly; the object is created first, then `__init__` sets it up.
**Common mistakes:** Calling it a "constructor that builds memory" (it initialises an already-created object); forgetting `self.` so values vanish after `__init__` ends.

### Q40 ⭐⭐ 🟡 Write code to find the two numbers in a list that add up to a given target (Two Sum).
**Asked at:** commonly asked; Two Sum appears in DataLemur's Python data structure questions (snippet-level evidence, no company-specific report).
**What the interviewer is checking:** Whether you move from the slow double loop to a fast dictionary lookup.
**Say this in the interview:** "For each number I work out which partner I need, `target - number`. I keep a dictionary of numbers I have already seen, so checking the partner is instant. One pass, no nested loop."
**Explain simply:**
- Brute force: two loops over every pair; slow for big lists (time grows with the square of the list size).
- Better: remember seen numbers in a dictionary (number -> position).
- At each number, ask "have I already seen the partner I need?"
- This is one pass over the list, so time grows in line with its size.
**Sample data:** `numbers = [2, 7, 11, 15]`, `target = 9`.
**Code (what you write in the interview):**
```python
numbers = [2, 7, 11, 15]
target = 9

seen = {}   # number -> its position
for position, number in enumerate(numbers):
    needed = target - number
    if needed in seen:
        print(seen[needed], position)
        break
    seen[number] = position
```
**Output:**
```text
0 1
```
**What it means:** The numbers at positions 0 and 1 (2 and 7) add up to 9.
**Likely follow-ups:** 1) *What if there are duplicates like [3, 3], target 6?* It still works, because we check before storing the current number. 2) *What if no pair exists?* Nothing prints; add an else message if asked.
**Common mistakes:** Using the same element twice (storing before checking); returning values when the question asks for positions, or the reverse; nested loops on a huge list.

### Q41 ⭐⭐ 🟡 Write code to find the missing number in a list that should contain 1 to n.
**Asked at:** commonly asked (no company-specific report found); a standard easy-array exercise.
**What the interviewer is checking:** Whether you know the sum formula instead of searching repeatedly.
**Say this in the interview:** "The numbers 1 to n always add up to n times n plus 1, divided by 2. I subtract the sum of my list from that total, and what is left is the missing number."
**Explain simply:**
- Expected total of 1 to n is `n * (n + 1) // 2` (the `//` keeps it a whole number).
- The list is missing one number, so its sum is short by exactly that number.
- No loops over the list beyond `sum()`; fast and short.
**Sample data:** `numbers = [1, 2, 4, 5, 6]`, `n = 6` (employee badge numbers 1 to 6, one not returned).
**Code (what you write in the interview):**
```python
numbers = [1, 2, 4, 5, 6]
n = 6

expected_total = n * (n + 1) // 2
missing_number = expected_total - sum(numbers)
print(missing_number)
```
**Output:**
```text
3
```
**What it means:** 3 is the number absent from the list.
**Alternative:** `for i in range(1, n + 1): if i not in numbers: print(i)`. Simple but slower, since each `in` scans the list.
**Likely follow-ups:** 1) *What if two numbers are missing?* The sum only gives their total; use a set difference instead. 2) *What if the list has duplicates?* The sum trick breaks; use a set.
**Common mistakes:** Using `/` (gives 21.0, a float) instead of `//`; setting `n` to the list length (that is n minus 1 here).

### Q42 ⭐⭐ 🟡 Write code to check whether a string is a palindrome while ignoring case, spaces and punctuation.
**Asked at:** commonly asked; palindrome checks are reported in Glassdoor DA intern and Python analyst candidate notes (snippets), and this is the usual follow-up version.
**What the interviewer is checking:** That you clean the text first, then compare with its reverse.
**Say this in the interview:** "I first keep only letters and digits and make them lower case. Then a palindrome simply equals its own reverse, which in Python is `cleaned[::-1]`."
**Explain simply:**
- A **palindrome** reads the same forwards and backwards.
- `isalnum()` is True for letters and digits, False for spaces and punctuation.
- `[::-1]` is a slice that walks the string backwards.
- Lower-casing makes "A" and "a" equal.
**Sample data:** `"A man, a plan, a canal: Panama"`.
**Code (what you write in the interview):**
```python
text = "A man, a plan, a canal: Panama"

# keep only letters and digits, in lower case
cleaned = ""
for character in text:
    if character.isalnum():
        cleaned = cleaned + character.lower()

print(cleaned == cleaned[::-1])
```
**Output:**
```text
True
```
**What it means:** After cleaning, the text reads the same both ways.
**Alternative:** `cleaned = "".join(c.lower() for c in text if c.isalnum())`, the same idea in one line.
**Likely follow-ups:** 1) *Empty string?* Counts as a palindrome (True). 2) *Without slicing?* Compare characters from both ends with two pointers.
**Common mistakes:** Forgetting `.lower()`; stripping only spaces and leaving commas; comparing the original text instead of the cleaned one.

### Q43 ⭐⭐ 🟡 Write code to group employees by department using a dictionary of lists.
**Asked at:** commonly asked (no company-specific report found); a core "dictionary of lists" pattern in DA rounds.
**What the interviewer is checking:** Whether you can build a group-by by hand, the idea behind pandas `groupby`.
**Say this in the interview:** "The department is the key and the value is a list of names. For each employee, if I have not seen the department yet I create an empty list, then I append the name."
**Explain simply:**
- A dictionary holds key-value pairs; here key = department, value = list of employee names.
- The `if department not in by_department` check avoids a KeyError on the first visit.
- This is exactly what `groupby` does for you in pandas.
**Sample data:** five employees (name, department) across HR, Sales and IT.
**Code (what you write in the interview):**
```python
employees = [
    {"name": "Asha", "department": "HR"},
    {"name": "Ravi", "department": "Sales"},
    {"name": "Meera", "department": "HR"},
    {"name": "John", "department": "IT"},
    {"name": "Priya", "department": "Sales"},
]

by_department = {}
for employee in employees:
    department = employee["department"]
    if department not in by_department:
        by_department[department] = []      # first time we see this department
    by_department[department].append(employee["name"])

print(by_department)
```
**Output:**
```text
{'HR': ['Asha', 'Meera'], 'Sales': ['Ravi', 'Priya'], 'IT': ['John']}
```
**What it means:** Each department now lists its employees.
**Alternative:** `by_department.setdefault(department, []).append(name)` does the check and create in one line.
**Likely follow-ups:** 1) *How do I get headcount per department?* `len(by_department["HR"])`. 2) *What is `defaultdict`?* A dictionary that creates the empty list for you.
**Common mistakes:** Writing `by_department[department] = []` every time (wipes earlier names); appending to a missing key (KeyError).

### Q44 ⭐⭐ 🟡 Write code to sort a list of employee dictionaries by salary, highest first, without pandas.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know `sorted` with a `key` function and `reverse=True`.
**Say this in the interview:** "I use `sorted` and tell it what to sort by with `key`: each employee's salary. `reverse=True` puts the highest first. It returns a new list and leaves the original alone."
**Explain simply:**
- `key` is a small function that picks the value to compare; here a **lambda** (a one-line unnamed function) that returns the salary.
- `sorted()` returns a new list; `list.sort()` changes the list in place.
- Sorting is ascending by default; `reverse=True` flips it.
**Sample data:** three employees with salaries 50000, 62000 and 45000.
**Code (what you write in the interview):**
```python
employees = [
    {"name": "Asha", "salary": 50000},
    {"name": "Ravi", "salary": 62000},
    {"name": "Meera", "salary": 45000},
]

sorted_employees = sorted(employees, key=lambda employee: employee["salary"], reverse=True)

for employee in sorted_employees:
    print(employee["name"], employee["salary"])
```
**Output:**
```text
Ravi 62000
Asha 50000
Meera 45000
```
**What it means:** Employees are listed from the highest salary to the lowest.
**Likely follow-ups:** 1) *Ties?* Python's sort is stable, so tied employees keep their original order. 2) *Sort by department then salary?* Return a tuple from the key.
**Common mistakes:** Calling `.sort()` and printing its result (it returns None); forgetting the key so Python errors comparing dictionaries.

### Q45 ⭐⭐ 🟡 Write a function that calculates net salary from gross salary using simple tax slabs with if-elif.
**Asked at:** commonly asked as an HR-flavoured gap-fill (no company-specific report found).
**What the interviewer is checking:** Clean if-elif ordering, a returned value, and handling the last "everything else" case.
**Say this in the interview:** "I check the slabs from the lowest upward, so the first match wins. I pick a tax rate, then return gross minus tax. I will state my slab assumptions: here the rate applies to the whole salary, a simplification."
**Explain simply:**
- **Gross salary** is pay before tax; **net salary** is what is left after tax.
- `if / elif / else` is checked top to bottom; only the first true branch runs.
- Order matters: with `<= 25000` first, later branches only see higher salaries.
- Real tax is *marginal* (each slab taxed at its own rate); this question asks the simple version.
**Sample data:** slabs assumed: up to 25000 is 0%, up to 50000 is 10%, up to 100000 is 20%, above that 30%.
**Code (what you write in the interview):**
```python
def net_salary(gross):
    if gross <= 25000:
        tax_rate = 0
    elif gross <= 50000:
        tax_rate = 0.10
    elif gross <= 100000:
        tax_rate = 0.20
    else:
        tax_rate = 0.30
    return gross - gross * tax_rate


print(net_salary(20000))
print(net_salary(40000))
print(net_salary(80000))
print(net_salary(150000))
```
**Output:**
```text
20000
36000.0
64000.0
105000.0
```
**What it means:** Each salary was taxed at the rate of its slab and the remainder returned.
**Likely follow-ups:** 1) *How would marginal slabs work?* Tax only the part of salary inside each slab and add them up. 2) *Negative salary?* Add a check and raise an error.
**Common mistakes:** Checking the biggest slab first with `<=` (everything matches it); printing instead of returning; using `if` repeatedly so several branches run.

### Q46 ⭐⭐ 🟡 What is the output of a = [1, 2, 3]; b = a; b.append(4); print(a)? Explain why.
**Asked at:** commonly asked Python gotcha (no company-specific report found).
**What the interviewer is checking:** Whether you know assignment copies the reference, not the list.
**Say this in the interview:** "It prints `[1, 2, 3, 4]`. `b = a` does not copy the list; both names point to the same list in memory. Appending through `b` changes the one shared list, so `a` sees it too."
**Explain simply:**
- A variable is a **label** attached to an object, not a box holding a copy.
- `b = a` sticks a second label on the same list.
- Lists are **mutable** (changeable in place), so changes show up under every label.
- `a is b` checks whether two names point to the same object.
- To get an independent list use `b = a.copy()` or `b = a[:]`.
**Sample data:** none needed (the list is in the code).
**Code (what you write in the interview):**
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
print(a is b)
```
**Output:**
```text
[1, 2, 3, 4]
True
```
**What it means:** There is only one list; `a` and `b` are two names for it.
**Likely follow-ups:** 1) *Would it differ with integers?* `b = a` then `b = b + 1` leaves `a` alone, because ints are immutable and `+` makes a new object. 2) *How to copy?* See the shallow copy question next.
**Common mistakes:** Thinking `b = a` duplicates the data; passing a list into a function and being surprised the function changed it.

### Q47 ⭐⭐ 🟡 What is the difference between a shallow copy and a deep copy?
**Asked at:** commonly asked Python fundamentals (no company-specific report found).
**What the interviewer is checking:** Whether you know a shallow copy still shares nested objects.
**Say this in the interview:** "A shallow copy makes a new outer list but the inner lists are still shared. A deep copy copies everything all the way down, so the copy is fully independent."
**Explain simply:**
- Shallow copy: `copy.copy(x)`, `x.copy()` or `x[:]`; copies only the top level.
- Deep copy: `copy.deepcopy(x)`; copies nested lists and dictionaries too.
- It only matters when a list contains other mutable things (lists, dictionaries).
- For a flat list of numbers or strings, shallow is enough.
**Sample data:** a list of `[name, salary]` pairs, copied both ways, then Asha's salary is changed in the original.
**Code (what you write in the interview):**
```python
import copy

team = [["Asha", 50000], ["Ravi", 62000]]

shallow = copy.copy(team)
deep = copy.deepcopy(team)

team[0][1] = 99999   # change a value inside the inner list

print("original:", team)
print("shallow: ", shallow)
print("deep:    ", deep)
```
**Output:**
```text
original: [['Asha', 99999], ['Ravi', 62000]]
shallow:  [['Asha', 99999], ['Ravi', 62000]]
deep:     [['Asha', 50000], ['Ravi', 62000]]
```
**What it means:** The shallow copy changed too because it shares the inner lists; the deep copy did not.
**Likely follow-ups:** 1) *Is deep copy slower?* Yes, it copies everything. 2) *Does `b = a` count as a copy?* No, no copy at all.
**Common mistakes:** Believing `.copy()` protects nested data; using `deepcopy` everywhere on large data without need.

### Q48 ⭐⭐ 🟡 What are the four pillars of object-oriented programming? Explain each in plain words with an example.
**Asked at:** LatentView (2020 campus technical round, OOP basics, per GfG); the four pillars are standard in OOP lists (foundit, AlmaBetter).
**What the interviewer is checking:** Whether you can name all four and give a simple real example for each.
**Say this in the interview:** "Encapsulation, inheritance, polymorphism and abstraction. In HR terms: keep salary private inside the employee, let Manager reuse Employee, let each role compute its own bonus, and show users only what they need."
**Explain simply:**
- **Encapsulation:** bundle data with the methods that use it, and protect it. A salary hidden behind `get_salary()`.
- **Inheritance:** a new class reuses another's features. A Manager is an Employee with extras.
- **Polymorphism:** same method name, different behaviour per class. `bonus()` is 5% for Employee, 10% for Manager.
- **Abstraction:** expose the simple "what", hide the messy "how". You call `bonus()` without knowing the formula.
**Sample data:** two employees, Asha (50000) and Ravi, a manager (80000).
**Code (what you write in the interview):**
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary          # encapsulation: kept private

    def get_salary(self):
        return self.__salary

    def bonus(self):
        return self.__salary * 0.05


class Manager(Employee):                # inheritance
    def bonus(self):                    # polymorphism: same name, own version
        return self.get_salary() * 0.10


for person in [Employee("Asha", 50000), Manager("Ravi", 80000)]:
    print(person.name, person.bonus())
```
**Output:**
```text
Asha 2500.0
Ravi 8000.0
```
**What it means:** One loop called `bonus()` on both people and each used its own rule.
**Likely follow-ups:** 1) *Is Python's privacy strict?* No; double underscore only renames the attribute, it is a convention. 2) *Where is abstraction?* Callers use `bonus()` without seeing the calculation (formal version uses `abc.ABC`).
**Common mistakes:** Mixing up encapsulation and abstraction; listing the pillars without an example.

### Q49 ⭐⭐ 🟡 What is inheritance? Write a Manager class that inherits from an Employee class.
**Asked at:** LatentView (2020 campus, OOP basics, per GfG); inheritance is a standard item in OOP question banks.
**What the interviewer is checking:** Syntax `class Manager(Employee)` and correct use of `super().__init__`.
**Say this in the interview:** "Inheritance lets a child class reuse a parent class. Manager gets everything Employee has, and I add or change only what is different, like team size."
**Explain simply:**
- Parent (base) class: `Employee`. Child (derived) class: `Manager`.
- `class Manager(Employee)` means "Manager is an Employee".
- `super().__init__(...)` runs the parent's setup so we do not repeat code.
- A child can **override** a method by defining one with the same name.
**Sample data:** one manager, Ravi, salary 80000, team of 5.
**Code (what you write in the interview):**
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return self.name + " earns " + str(self.salary)


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)     # reuse Employee's setup
        self.team_size = team_size

    def describe(self):
        return self.name + " manages " + str(self.team_size) + " people"


ravi = Manager("Ravi", 80000, 5)
print(ravi.describe())
print(ravi.salary)
```
**Output:**
```text
Ravi manages 5 people
80000
```
**What it means:** Manager reused `name` and `salary` from Employee and added its own `team_size` and `describe`.
**Likely follow-ups:** 1) *What if I forget `super().__init__`?* `name` and `salary` are never set. 2) *Can a class inherit from two parents?* Yes (multiple inheritance), used with care.
**Common mistakes:** Forgetting `super().__init__`; passing arguments in the wrong order; copying the parent's code instead of inheriting.

### Q50 ⭐⭐ 🟡 What are *args and **kwargs, and when would you use them?
**Asked at:** commonly asked Python fundamentals (no company-specific report found).
**What the interviewer is checking:** That you know `*args` collects extra positional values and `**kwargs` collects extra named ones.
**Say this in the interview:** "`*args` lets a function accept any number of positional arguments, packed into a tuple. `**kwargs` accepts any number of named arguments, packed into a dictionary. I use them when I do not know in advance how many inputs will come."
**Explain simply:**
- `*args` -> a tuple, e.g. `(1000, 2500, 500)`.
- `**kwargs` -> a dictionary, e.g. `{"name": "Asha", "department": "HR"}`.
- The names `args` and `kwargs` are convention; the stars do the work.
- Common use: wrapper functions and flexible helper functions.
**Sample data:** none needed (bonuses 1000, 2500, 500 and one employee's details).
**Code (what you write in the interview):**
```python
def total_pay(*bonuses):
    return sum(bonuses)


def show_employee(**details):
    for key, value in details.items():
        print(key, "=", value)


print(total_pay(1000, 2500, 500))
show_employee(name="Asha", department="HR", salary=50000)
```
**Output:**
```text
4000
name = Asha
department = HR
salary = 50000
```
**What it means:** The first function added any number of bonuses; the second printed any named details it was given.
**Likely follow-ups:** 1) *Order in a definition?* Normal parameters, then `*args`, then `**kwargs`. 2) *Can I unpack a list into a call?* Yes, `f(*my_list)`.
**Common mistakes:** Using one star for named arguments; putting `**kwargs` before `*args` (SyntaxError); expecting `args` to be a list (it is a tuple).

### Q51 ⭐⭐ 🟡 What is recursion? Write a recursive function for factorial and state its drawback.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A clear base case and the correct recursive step.
**Say this in the interview:** "Recursion is a function calling itself on a smaller version of the problem until it reaches a base case where it stops. The drawback is that each call uses memory, so very deep recursion hits Python's limit and a loop is usually faster."
**Explain simply:**
- `factorial(5)` = 5 x 4 x 3 x 2 x 1 = 120.
- **Base case:** `n <= 1` returns 1; this stops the calls.
- **Recursive step:** `n * factorial(n - 1)`.
- Drawback: each call is stacked in memory; Python allows about 1000 nested calls by default, then raises `RecursionError`.
- Without a base case it never stops.
**Sample data:** none needed (`factorial(5)`).
**Code (what you write in the interview):**
```python
def factorial(n):
    if n <= 1:                     # base case: stop here
        return 1
    return n * factorial(n - 1)    # smaller version of the same problem


print(factorial(5))
```
**Output:**
```text
120
```
**What it means:** 5 was multiplied down through 4, 3, 2 and 1 to give 120.
**Alternative:** A plain `for` loop multiplying a running total; no depth limit and simpler.
**Likely follow-ups:** 1) *What is `factorial(0)`?* 1 (handled by the base case). 2) *Negative input?* Returns 1 here; real code should reject it.
**Common mistakes:** Missing base case (infinite recursion); calling `factorial(n)` instead of `n - 1`.

### Q52 ⭐⭐ 🟡 Why is checking membership in a set faster than in a list? Explain time complexity (Big O) in simple words.
**Asked at:** commonly asked (no company-specific report found); a standard follow-up when you use a set to speed up duplicate or lookup code.
**What the interviewer is checking:** Whether you understand "scan everything" versus "jump straight to it", and can say it in Big O.
**Say this in the interview:** "A list checks items one by one, so the work grows with the list size: O(n). A set uses hashing, which turns the value into an address, so it jumps straight to the spot: about O(1), constant time, whatever the size."
**Explain simply:**
- **Big O** describes how the work grows as data grows, ignoring small details.
- **O(n):** double the employees, roughly double the checking time.
- **O(1):** the time stays about the same however big the set is.
- A set's trick is **hashing**: a formula turns each value into a slot number, like a locker number.
- Trade-offs: sets use more memory, have no order, and need hashable items (numbers, strings, tuples, not lists).
**Sample data:** one million employee IDs, looking for the very last one.
**Code (what you write in the interview):**
```python
import time

employee_ids = list(range(1_000_000))
employee_id_set = set(employee_ids)

start = time.time()
print(999_999 in employee_ids)        # list: checks one by one
print("list:", round(time.time() - start, 5), "seconds")

start = time.time()
print(999_999 in employee_id_set)     # set: jumps straight to it
print("set: ", round(time.time() - start, 5), "seconds")
```
**Output:**
```text
True
list: 0.00869 seconds
True
set:  0.0 seconds
```
**What it means:** The list had to walk a million entries; the set went directly to the answer. Exact times change from machine to machine; the gap is the point.
**Likely follow-ups:** 1) *Is set lookup always O(1)?* On average yes; many hash collisions can make it slower. 2) *When is a list fine?* Small data, or when order and duplicates matter.
**Common mistakes:** Saying sets are "sorted"; looping with `in list` inside another loop on big data (O(n x n)); building a set inside the loop instead of once outside.

### Q53 ⭐ 🟢 Write code to find the length of a string without using len().
**Asked at:** commonly asked beginner exercise (no company-specific report found).
**What the interviewer is checking:** That you can count with a simple loop.
**Say this in the interview:** "I start a counter at zero and add one for every character as I loop through the string. When the loop ends, the counter is the length."
**Explain simply:**
- Looping over a string gives one character at a time.
- Spaces and punctuation count as characters too.
- An empty string never enters the loop, so the answer stays 0.
**Sample data:** `text = "attrition"`.
**Code (what you write in the interview):**
```python
text = "attrition"

length = 0
for character in text:
    length = length + 1

print(length)
```
**Output:**
```text
9
```
**What it means:** The string has 9 characters.
**Likely follow-ups:** 1) *Why not `len()`?* It is the normal answer; this just tests loops. 2) *Same for a list?* Yes, the loop works on any iterable.
**Common mistakes:** Starting the counter at 1; counting only letters and forgetting spaces.

### Q54 ⭐ 🟢 Write code to check whether a list is sorted in ascending order.
**Asked at:** commonly asked beginner exercise (no company-specific report found).
**What the interviewer is checking:** Comparing neighbours and stopping at the first break.
**Say this in the interview:** "I compare each item with the next one. If any item is bigger than the one after it, the list is not sorted, so I stop. If I get through the whole list, it is sorted."
**Explain simply:**
- Only neighbouring pairs need checking; no full sort needed.
- Use `>` not `>=`, so equal values (ties) are still allowed in ascending order.
- The loop runs to `len(numbers) - 1` so `i + 1` stays inside the list.
- Empty and one-item lists count as sorted.
**Sample data:** `numbers = [1, 3, 3, 7, 9]` (ties allowed).
**Code (what you write in the interview):**
```python
numbers = [1, 3, 3, 7, 9]

is_sorted = True
for i in range(len(numbers) - 1):
    if numbers[i] > numbers[i + 1]:
        is_sorted = False
        break

print(is_sorted)
```
**Output:**
```text
True
```
**What it means:** Every item is less than or equal to the next, so the list is in ascending order.
**Alternative:** `numbers == sorted(numbers)`, a one-liner that is short but sorts a copy (more work than needed).
**Likely follow-ups:** 1) *How to check descending?* Flip the comparison to `<`. 2) *Why break?* No need to keep checking once one pair is out of order.
**Common mistakes:** Looping to `len(numbers)` (IndexError on the last item); using `>=` so duplicates wrongly fail.

### Q55 ⭐ 🟢 Write code to sort a list of strings by their length.
**Asked at:** commonly asked (no company-specific report found); a standard `key=` drill in beginner Python sets.
**What the interviewer is checking:** Whether you know `sorted()` and the `key` argument.
**Say this in the interview:** "I use `sorted` with `key=len`, so Python compares the words by length instead of alphabetically."
**Explain simply:**
- `sorted()` returns a new sorted list and leaves the original alone (`list.sort()` changes the list in place).
- `key` is a function Python applies to each item before comparing; `len` gives the length of each word.
- Words of the same length keep their original order (the sort is "stable").
- For longest first, add `reverse=True`.
**Sample data:** `skills = ["payroll", "HR", "attendance", "hiring", "exit"]`
**Code (what you write in the interview):**
```python
skills = ["payroll", "HR", "attendance", "hiring", "exit"]

# key=len tells sorted() to compare words by their length
sorted_skills = sorted(skills, key=len)

print(sorted_skills)
```
**Output:**
```text
['HR', 'exit', 'hiring', 'payroll', 'attendance']
```
**What it means:** The shortest word comes first and the longest last.
**Likely follow-ups:**
- *Sort by length, then alphabetically?* `sorted(skills, key=lambda word: (len(word), word))`.
**Common mistakes:** Writing `key=len()` with brackets (that calls it too early); expecting `sorted` to change the original list.

### Q56 ⭐ 🟢 Is Python a compiled or an interpreted language, and what does that mean?
**Asked at:** commonly asked (no company-specific report found); appears in generic Python fundamentals lists.
**What the interviewer is checking:** Whether you understand the basics of how Python code runs, without over-claiming.
**Say this in the interview:** "Python is usually called interpreted: you run the code directly without a separate build step. Strictly, Python first compiles your code to bytecode, and then the Python interpreter runs that bytecode line by line."
**Explain simply:**
- Compiled language (like C): the whole program is translated to machine code first, then run. Fast, but you need a build step.
- Interpreted language: a program (the interpreter) reads and runs your code as it goes. Easy to test one line at a time.
- Python does both small steps: it turns your file into bytecode (a simpler internal form, the `.pyc` files you may see) and the Python virtual machine runs it.
- Why it matters for analysts: you can try code in a notebook cell by cell. The cost is that plain Python loops are slower than compiled code, which is why pandas and NumPy use fast compiled code underneath.
**What it means:** Python is compiled to bytecode first and then interpreted, which is why people can fairly call it either, as long as they explain the two steps.
**Likely follow-ups:**
- *Why are pandas operations fast then?* The heavy work runs in compiled C code inside NumPy and pandas.
**Common mistakes:** Saying "Python is only interpreted" with no mention of bytecode; believing that errors only show up when a line runs (syntax errors are caught before anything runs).

### Q57 ⭐ 🟡 Write code to find the GCD (greatest common divisor) of two numbers.
**Asked at:** commonly asked (no company-specific report found); a classic number-logic drill.
**What the interviewer is checking:** Whether you can write a loop with a clear stopping rule (Euclid's method).
**Say this in the interview:** "The GCD is the biggest number that divides both numbers with no remainder. I use Euclid's method: replace (a, b) with (b, a mod b) until b is zero, and a is the answer."
**Explain simply:**
- GCD example: for 48 and 18, the biggest number dividing both is 6.
- `a % b` is the remainder after dividing a by b.
- The pair shrinks each step: (48, 18) then (18, 12) then (12, 6) then (6, 0), so the answer is 6.
- Real-life use: splitting two team sizes into the largest equal groups.
**Sample data:** `a = 48`, `b = 18`.
**Code (what you write in the interview):**
```python
def find_gcd(a, b):
    # Euclid's method: keep replacing (a, b) with (b, remainder)
    while b != 0:
        a, b = b, a % b
    return a

print(find_gcd(48, 18))
```
**Output:**
```text
6
```
**What it means:** 6 is the largest number that divides both 48 and 18 exactly.
**Alternative:** `math.gcd(48, 18)` does this in one call; mention it, but write the loop if the interviewer says "without built-ins".
**Likely follow-ups:**
- *What if one number is 0?* `find_gcd(5, 0)` returns 5, which is correct.
**Common mistakes:** Looping from 1 up to the smaller number (works, but slow); stopping when `a` is zero instead of `b`.

### Q58 ⭐ 🟡 Write code to flatten a nested list such as [[1, 2], [3, [4, 5]]].
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can handle unknown depth, which needs recursion (a function calling itself).
**Say this in the interview:** "I loop over the items. If an item is a list, I flatten it with the same function; otherwise I add it to the result."
**Explain simply:**
- Nested list: a list that contains other lists, sometimes several levels deep.
- `isinstance(item, list)` asks "is this item a list?".
- Recursion works here because each inner list is a smaller version of the same problem.
- `extend` adds all items of a list; `append` adds one item.
**Sample data:** `[[1, 2], [3, [4, 5]]]`
**Code (what you write in the interview):**
```python
def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            # item is itself a list, so flatten it too
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list

print(flatten([[1, 2], [3, [4, 5]]]))
```
**Output:**
```text
[1, 2, 3, 4, 5]
```
**What it means:** All the numbers come out in one plain list, in the original order.
**Likely follow-ups:**
- *What if the list is only one level deep?* A comprehension is enough: `[x for row in nested for x in row]`.
**Common mistakes:** Using `append` instead of `extend` for the inner result (gives a list inside a list); a one-level solution that fails on `[3, [4, 5]]`.

### Q59 ⭐ 🟡 Write code to rotate a list by k positions.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Comfort with slicing and with the case where k is bigger than the list.
**Say this in the interview:** "To rotate right by k, the last k items move to the front. With slices that is `numbers[-k:] + numbers[:-k]`, after taking k modulo the length."
**Explain simply:**
- Slice `numbers[-k:]` means "the last k items"; `numbers[:-k]` means "everything except the last k".
- `k % len(numbers)` turns a big k (like 10 on a 7-item list) into the same rotation (3).
- Rotating left by k is the mirror: `numbers[k:] + numbers[:k]`.
**Sample data:** `numbers = [1, 2, 3, 4, 5, 6, 7]`, `k = 3`
**Code (what you write in the interview):**
```python
numbers = [1, 2, 3, 4, 5, 6, 7]
k = 3

# k % len handles k bigger than the list
k = k % len(numbers)

# last k items go to the front, the rest follow
rotated = numbers[-k:] + numbers[:-k]

print(rotated)
```
**Output:**
```text
[5, 6, 7, 1, 2, 3, 4]
```
**What it means:** The last three items (5, 6, 7) moved to the front.
**Likely follow-ups:**
- *What if k is 0?* It still works: the slices give the whole list plus an empty list.
- *Empty list?* `k % 0` raises an error, so check `if not numbers` first.
**Common mistakes:** Forgetting the modulo; mixing up left and right rotation.

### Q60 ⭐ 🟡 Write code to move all zeros in a list to the end while keeping the other numbers in order.
**Asked at:** commonly asked (no company-specific report found); a well-known easy array problem.
**What the interviewer is checking:** Whether you keep the order of the other numbers and handle counting cleanly.
**Say this in the interview:** "I collect the non-zero numbers in order, count the zeros, and then add that many zeros at the end."
**Explain simply:**
- One pass over the list: non-zeros go into a new list, zeros are only counted.
- `[0] * zero_count` makes a list of that many zeros.
- Order of non-zero numbers stays the same because we add them as we meet them.
- An in-place version with two pointers exists; mention it if asked about memory.
**Sample data:** `numbers = [0, 1, 0, 3, 12, 0, 5]`
**Code (what you write in the interview):**
```python
numbers = [0, 1, 0, 3, 12, 0, 5]

non_zeros = []
zero_count = 0

for number in numbers:
    if number == 0:
        zero_count += 1
    else:
        non_zeros.append(number)

# put the zeros back at the end
result = non_zeros + [0] * zero_count

print(result)
```
**Output:**
```text
[1, 3, 12, 5, 0, 0, 0]
```
**What it means:** The non-zero numbers keep their order and all zeros sit at the end.
**Alternative:** `sorted(numbers, key=lambda x: x == 0)` also works because the sort is stable (False sorts before True).
**Likely follow-ups:**
- *Do it without a new list?* Keep a write position; copy each non-zero forward, then fill the rest with zeros.
**Common mistakes:** Using `sort()` (changes the order of the other numbers); removing zeros while looping (see Q68).

### Q61 ⭐ 🟡 Write code to swap the keys and values of a dictionary, and say what goes wrong if values repeat.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice that dictionary keys must be unique, so repeated values lose data.
**Say this in the interview:** "I loop over the items and store value as key and key as value. If two keys share a value, the later one overwrites the earlier, so data is lost. To keep everything, I make each new key hold a list of names."
**Explain simply:**
- Dictionary: pairs of key and value; keys cannot repeat.
- After swapping, the old values become keys, so repeated values collide.
- Safe fix: group the old keys in a list under each value.
**Sample data:** employee grades where Asha and Meena both have grade A.
**Code (what you write in the interview):**
```python
employee_grade = {"Asha": "A", "Ravi": "B", "Meena": "A", "John": "C"}

swapped = {}
for name, grade in employee_grade.items():
    swapped[grade] = name

print(swapped)
```
**Output:**
```text
{'A': 'Meena', 'B': 'Ravi', 'C': 'John'}
```
**What it means:** Asha has disappeared: grade A kept only Meena, the last one written.
**Alternative (safe version, keeps everyone):**
```python
grade_to_names = {}
for name, grade in employee_grade.items():
    if grade not in grade_to_names:
        grade_to_names[grade] = []
    grade_to_names[grade].append(name)

print(grade_to_names)
```
Output: `{'A': ['Asha', 'Meena'], 'B': ['Ravi'], 'C': ['John']}`
**Likely follow-ups:**
- *One-line version?* `{value: key for key, value in d.items()}`, with the same data-loss problem.
- *What if values are lists?* Lists cannot be dictionary keys (not hashable), so it raises an error.
**Common mistakes:** Not noticing the silent data loss; no error is shown when values repeat.

### Q62 ⭐ 🟡 Write code to find the longest streak of consecutive present days in an attendance list of 'P' and 'A'.
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured version of the "longest run" problem.
**What the interviewer is checking:** Whether you can track a running count and a best count with one loop.
**Say this in the interview:** "I keep two numbers: the current streak and the longest streak so far. A 'P' adds one to the current streak; an 'A' resets it to zero."
**Explain simply:**
- 'P' = present, 'A' = absent.
- The current streak is reset whenever the run breaks; the longest streak is only updated when the current one beats it.
- Need only one pass, so the work grows in step with the number of days.
**Sample data:** `["P", "P", "A", "P", "P", "P", "A", "P"]`
**Code (what you write in the interview):**
```python
attendance = ["P", "P", "A", "P", "P", "P", "A", "P"]

longest_streak = 0
current_streak = 0

for day in attendance:
    if day == "P":
        current_streak += 1
        if current_streak > longest_streak:
            longest_streak = current_streak
    else:
        # an absent day breaks the streak
        current_streak = 0

print(longest_streak)
```
**Output:**
```text
3
```
**What it means:** The employee's best run was 3 present days in a row.
**Likely follow-ups:**
- *All absent or an empty list?* Returns 0, which is correct.
- *Longest absent streak?* Swap 'P' and 'A' in the condition.
**Common mistakes:** Forgetting to reset on 'A'; only checking the longest streak when the run ends (misses a streak that runs to the last day).

### Q63 ⭐ 🟡 Write code to do a basic validity check of email addresses in a list without using regex.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** String methods and clear rules, not a perfect email checker.
**Say this in the interview:** "I state my rules first: exactly one @, something before it, and a dot inside the domain part, not at its start or end. Then I check each email against those rules."
**Explain simply:**
- Regex (regular expression) is a pattern language for text; the question asks us to avoid it and use plain string tools.
- `count("@")` counts the @ signs; `split("@")` cuts the email into name and domain.
- This is a basic check only: it cannot prove the mailbox exists.
**Sample data:** seven emails, some good, some broken.
**Code (what you write in the interview):**
```python
emails = ["asha@company.com", "ravi.company.com", "meena@", "@gmail.com",
          "john@@mail.com", "priya@mail", "sam@mail.org"]

for email in emails:
    # exactly one @, something before it, a dot in the domain part
    if email.count("@") == 1:
        name, domain = email.split("@")
        is_valid = (name != "" and "." in domain
                    and not domain.startswith(".") and not domain.endswith("."))
    else:
        is_valid = False
    print(email, is_valid)
```
**Output:**
```text
asha@company.com True
ravi.company.com False
meena@ False
@gmail.com False
john@@mail.com False
priya@mail False
sam@mail.org True
```
**What it means:** Only the two well-formed addresses pass.
**Likely follow-ups:**
- *Is this enough in production?* No; use a proper library or send a confirmation email.
- *Spaces?* Add `" " not in email`.
**Common mistakes:** Only checking `"@" in email` (passes `john@@mail.com`); trusting a format check as proof the email is real.

### Q64 ⭐ 🟡 Implement binary search on a sorted list and explain why it is faster than a linear search.
**Asked at:** commonly asked (no company-specific report found); a standard algorithm question in basic coding rounds.
**What the interviewer is checking:** Whether you can write the low/high/middle loop correctly and explain halving.
**Say this in the interview:** "Binary search needs a sorted list. I look at the middle item: if it is the target I am done, if the target is bigger I discard the left half, otherwise the right half. Halving each time means about log n steps instead of n."
**Explain simply:**
- Linear search checks items one by one: up to 1,000,000 checks for 1,000,000 items.
- Binary search halves the range each time: about 20 checks for 1,000,000 items.
- It only works on sorted data (sorting costs time too, so it pays off when you search many times).
- Returns the position, or -1 if not found.
**Sample data:** sorted employee IDs.
**Code (what you write in the interview):**
```python
def binary_search(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        middle = (low + high) // 2
        if sorted_list[middle] == target:
            return middle
        elif sorted_list[middle] < target:
            low = middle + 1      # target is in the right half
        else:
            high = middle - 1     # target is in the left half

    return -1  # not found

employee_ids = [101, 104, 109, 115, 120, 133, 148]
print(binary_search(employee_ids, 120))
print(binary_search(employee_ids, 125))
```
**Output:**
```text
4
-1
```
**What it means:** 120 is at position 4; 125 is not in the list.
**Likely follow-ups:**
- *Time complexity?* O(log n), against O(n) for linear search.
- *Duplicates?* It returns one match, not necessarily the first.
**Common mistakes:** Using it on an unsorted list; `while low < high` (misses the last item); forgetting `+ 1` and `- 1`, which causes an endless loop.

### Q65 ⭐ 🟡 Write code to sort a list using bubble sort and explain how it works.
**Asked at:** commonly asked (no company-specific report found); a classic "sorting without sort()" drill.
**What the interviewer is checking:** Nested loops and swapping; knowing it is simple but slow.
**Say this in the interview:** "Bubble sort compares neighbours and swaps them if they are in the wrong order. After each pass the biggest unsorted number has 'bubbled' to the end, so I repeat until all are in place."
**Explain simply:**
- Pass 1 moves the largest number to the last position; pass 2 moves the second largest, and so on.
- The inner loop gets shorter each pass (`n - 1 - i`) because the end is already sorted.
- Slow for big lists: roughly n times n steps (O(n squared)). In real work use `sorted()`.
**Sample data:** `numbers = [64, 25, 12, 22, 11]`
**Code (what you write in the interview):**
```python
numbers = [64, 25, 12, 22, 11]

n = len(numbers)
for i in range(n - 1):
    for j in range(n - 1 - i):
        # swap neighbours that are in the wrong order
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

print(numbers)
```
**Output:**
```text
[11, 12, 22, 25, 64]
```
**What it means:** The list is now sorted from smallest to largest.
**Likely follow-ups:**
- *How to stop early on a sorted list?* Track whether any swap happened in a pass; if none, stop.
- *A faster sort?* Merge sort or Python's built-in Timsort, both about O(n log n).
**Common mistakes:** Running the inner loop to the end (index error on `j + 1`); forgetting that bubble sort is too slow for large data.

### Q66 ⭐ 🟡 Write code to print a diamond pattern of stars.
**Asked at:** a 2021 Deloitte campus-round anecdote on GeeksforGeeks lists a diamond pattern (from internal research; only a summary, unverified).
**What the interviewer is checking:** Loop logic with spaces and stars; each row's count follows a rule.
**Say this in the interview:** "Row i of the top half has (n - i) spaces and (2i - 1) stars. I print the top half including the middle, then the bottom half in reverse."
**Explain simply:**
- Star counts for n = 3 go 1, 3, 5, then back to 3, 1 (always odd numbers).
- Spaces on the left keep the shape centred; they shrink as stars grow.
- `" " * 2` repeats a string, so `"*" * 5` gives five stars.
**Sample data:** none needed (`n = 3`).
**Code (what you write in the interview):**
```python
n = 3  # rows in the top half

# top half including the middle row
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))

# bottom half
for i in range(n - 1, 0, -1):
    print(" " * (n - i) + "*" * (2 * i - 1))
```
**Output:**
```text
  *
 ***
*****
 ***
  *
```
**What it means:** A diamond with 5 rows; change `n` to make it bigger.
**Likely follow-ups:**
- *Hollow diamond?* Print only the first and last star of each row.
**Common mistakes:** Printing the middle row twice (the bottom loop must start at `n - 1`); using `2 * i` stars (gives even widths).

### Q67 ⭐ 🟡 Why is using a mutable default argument such as def f(x, items=[]) a bug?
**Asked at:** commonly asked (no company-specific report found); a famous Python gotcha.
**What the interviewer is checking:** Whether you know when default values are created.
**Say this in the interview:** "The default list is created once, when the function is defined, not on each call. So every call that uses the default shares the same list and keeps adding to it. The fix is `items=None` and creating a new list inside."
**Explain simply:**
- Mutable means it can be changed in place (list, dict, set). Immutable means it cannot (number, string, tuple).
- A default value is made once and reused, so a changed list stays changed.
- Safe defaults: `None`, numbers, strings, tuples.
**Sample data:** none needed (two calls to one function).
**Code (what you write in the interview):**
```python
def add_employee(name, team=[]):
    team.append(name)
    return team

print(add_employee("Asha"))
print(add_employee("Ravi"))
```
**Output:**
```text
['Asha']
['Asha', 'Ravi']
```
**What it means:** The second call was meant to start a new team but still contains Asha.
**Alternative (the fix):**
```python
def add_employee(name, team=None):
    # create a fresh list on every call
    if team is None:
        team = []
    team.append(name)
    return team
```
Output of the same two calls: `['Asha']` then `['Ravi']`.
**Likely follow-ups:**
- *Is it ever useful?* Rarely, as a deliberate cache; better to be explicit.
**Common mistakes:** Writing `if not team:` as the check (also replaces an empty list that the caller passed in on purpose).

### Q68 ⭐ 🟡 Why does removing items from a list while looping over it give wrong results, and how do you do it safely?
**Asked at:** commonly asked (no company-specific report found); a classic Python gotcha.
**What the interviewer is checking:** Whether you understand that the loop walks by position.
**Say this in the interview:** "When I remove an item, everything after it shifts left by one, but the loop moves on to the next position, so it skips an item. The safe way is to build a new list of what I want to keep."
**Explain simply:**
- The loop keeps an internal position counter (0, 1, 2 ...).
- Remove the item at position 0 and the next item slides into position 0, but the loop goes to position 1, so one item is never checked.
- Safe options: a list comprehension, or loop over a copy (`for n in numbers[:]`).
**Sample data:** `[2, 4, 6, 7, 8]`; goal: remove the even numbers.
**Code (what you write in the interview):**
```python
numbers = [2, 4, 6, 7, 8]

for number in numbers:
    if number % 2 == 0:
        numbers.remove(number)

print(numbers)
```
**Output:**
```text
[4, 7]
```
**What it means:** Wrong: 4 is even but stayed, because the loop skipped it after 2 was removed. The correct answer is `[7]`.
**Alternative (the safe way):**
```python
odd_numbers = [number for number in numbers if number % 2 != 0]
```
For the same starting list, output: `[7]`.
**Likely follow-ups:**
- *Same problem with dicts?* Python raises an error if a dictionary changes size during a loop.
**Common mistakes:** Assuming the loop "sees" the change correctly; using `remove` on duplicates (it deletes only the first match).

### Q69 ⭐ 🟡 Why does 0.1 + 0.2 == 0.3 return False in Python?
**Asked at:** commonly asked (no company-specific report found); a standard float-precision question.
**What the interviewer is checking:** Whether you know computers store decimals in binary, with tiny errors.
**Say this in the interview:** "Python stores decimals as binary floating point, and 0.1 and 0.2 cannot be stored exactly in binary, just like 1/3 cannot be written exactly in decimal. The sum is 0.30000000000000004, so the comparison is False. I compare with a tolerance using `math.isclose`."
**Explain simply:**
- Float: a number with a decimal point, stored approximately.
- The error is about 1 part in a quadrillion; harmless for averages, harmful for `==` checks.
- For money, use `Decimal` or whole paise/cents instead of float.
**Sample data:** none needed (the numbers 0.1, 0.2 and 0.3).
**Code (what you write in the interview):**
```python
import math

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)

# compare with a small tolerance instead
print(math.isclose(0.1 + 0.2, 0.3))
```
**Output:**
```text
0.30000000000000004
False
True
```
**What it means:** The two values differ by a tiny amount, so `==` fails, but they are close enough for practical use.
**Alternative:** `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` is `True` (from `decimal`, pass the numbers as strings); `round(0.1 + 0.2, 2) == 0.3` also gives `True`.
**Likely follow-ups:**
- *Is it a Python bug?* No, the same happens in Java, JavaScript and Excel (Excel hides it by rounding the display).
- *In pandas?* Use `np.isclose` for float columns instead of `==`.
**Common mistakes:** Comparing floats with `==`; building `Decimal(0.1)` from a float (carries the same error).

### Q70 ⭐ 🟡 What are iterators and generators, and what does yield do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can explain lazy (one at a time) processing.
**Say this in the interview:** "An iterator is an object that gives me one item at a time with `next()`. A generator is a simple way to make one: a function that uses `yield`, which hands back a value and pauses, then continues from the same place on the next call. It saves memory because values are made on demand."
**Explain simply:**
- Iterable: anything you can loop over (list, string, dict). Iterator: the object that remembers where you are in that loop.
- `return` ends a function; `yield` pauses it and keeps its state.
- Good for huge files: read and process one row at a time instead of loading a million rows.
- A generator can be used only once; after it is finished it gives nothing.
**Sample data:** none needed (`count_up_to(3)`).
**Code (what you write in the interview):**
```python
def count_up_to(n):
    number = 1
    while number <= n:
        yield number   # pause here and hand back one value
        number += 1

counter = count_up_to(3)
print(next(counter))
print(next(counter))
print(next(counter))

# a generator can be used up only once
print(list(counter))
```
**Output:**
```text
1
2
3
[]
```
**What it means:** Each `next` gave the following number; once finished, the generator is empty.
**Alternative:** a generator expression, `(n * n for n in range(5))`, is the one-line version.
**Likely follow-ups:**
- *`next` after the end?* Raises `StopIteration`; a `for` loop handles this for you.
- *When is it better than a list?* When the data is large or you only need part of it.
**Common mistakes:** Treating a generator like a list (no indexing, no second pass); confusing `yield` with `return`.

### Q71 ⭐ 🔴 What is a decorator in Python? Write one that prints how long a function takes.
**Asked at:** commonly asked (no company-specific report found); an advanced topic that can set a candidate apart.
**What the interviewer is checking:** Functions as values, wrapper functions, and `*args, **kwargs`.
**Say this in the interview:** "A decorator is a function that takes another function and returns a new version with extra behaviour added, without changing the original code. I put `@timer` above a function, and it records the time before and after the call."
**Explain simply:**
- In Python a function can be passed around like any value.
- `@timer` above `def total_payroll` is shorthand for `total_payroll = timer(total_payroll)`.
- `*args, **kwargs` lets the wrapper accept any arguments and pass them on (see Q50).
- Typical uses: timing, logging, checking permissions.
**Sample data:** `salaries = [40000, 35000, 60000]`
**Code (what you write in the interview):**
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def total_payroll(salaries):
    return sum(salaries)

print(total_payroll([40000, 35000, 60000]))
```
**Output:**
```text
total_payroll took 0.0000 seconds
135000
```
**What it means:** The timing line is printed by the decorator and the normal result is still returned; the work was too tiny to show any time.
**Likely follow-ups:**
- *Why `return result`?* Without it the decorated function would return `None`.
- *Why `functools.wraps`?* It keeps the original function's name and docstring; mention it as a refinement.
**Common mistakes:** Forgetting to return `result`; calling `func` with no arguments; forgetting to return `wrapper` from the decorator.
