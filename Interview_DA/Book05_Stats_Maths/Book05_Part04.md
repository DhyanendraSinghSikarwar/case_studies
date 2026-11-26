# Book 5 — Statistics & Maths for Data Analysts | Part 4: Probability & Bayes 🟡

**Target:** 70 questions | **Actual:** 71 questions
**Scope:** interview-style probability and Bayes for analysts: basic rules, conditional probability, Bayes with test/HR/defect numbers, expected value, classic puzzles (Monty Hall, birthday).

### Q1 ⭐⭐⭐ 🟢 What is probability, and how do you calculate it for a simple event such as drawing a card or rolling a die?
**Asked at:** commonly asked (no company-specific report found); the sources file lists probability basics with percentages as a topic in Tiger Analytics candidate reports (snippet only, mostly 2021-22).
**What the interviewer is checking:** Do you know the basic definition and can you count favourable and total outcomes cleanly?
**Say this in the interview:** "Probability is a number between 0 and 1 that says how likely an event is. For equally likely outcomes I divide the number of outcomes I want by the total number of outcomes."
**Explain simply:**
- An **event** is the thing you are asking about (drawing an ace). An **outcome** is one possible result (the ace of spades).
- This simple counting method only works when every outcome is equally likely (a fair die, a well-shuffled deck).
- When outcomes are not equally likely, we estimate probability from data instead (see Q24).
**Formula in plain words:** probability = outcomes you want divided by all possible outcomes. P(event) = favourable / total.
**Worked example:** A deck has 52 cards, 4 of them aces, so P(ace) = 4/52. A fair die has 6 faces, 3 of them even (2, 4, 6), so P(even) = 3/6.
**Excel / Python:**
```python
# Count the outcomes we want and all possible outcomes for a card draw
aces_in_deck = 4
cards_in_deck = 52
probability_of_ace = aces_in_deck / cards_in_deck

# Same idea for rolling a fair die and getting an even number
even_faces = 3
faces_on_die = 6
probability_of_even = even_faces / faces_on_die

print("P(ace) =", round(probability_of_ace, 4))
print("P(even) =", round(probability_of_even, 4))
```
```text
P(ace) = 0.0769
P(even) = 0.5
```
About 7.7% of draws are aces, and exactly half of die rolls are even.
**Likely follow-ups:** 1) *What if outcomes are not equally likely?* Use observed frequencies (Q24). 2) *Can probability be negative or above 1?* No (Q23).
**Common mistakes:** Dividing by the wrong total; using the counting method for unequal outcomes (for example, "50% chance I get the job: it either happens or it does not").

### Q2 ⭐⭐⭐ 🟢 What is the difference between independent events and mutually exclusive events?
**Asked at:** commonly asked; the sources file lists "independent vs mutually exclusive" in a 2024 probability question bank (snippet only).
**What the interviewer is checking:** Do you avoid the classic mix-up of these two ideas?
**Say this in the interview:** "Independent means one event does not change the chance of the other. Mutually exclusive means they cannot happen together. They are almost opposites: if two events are mutually exclusive and both possible, knowing one happened tells you the other did not, so they are dependent."
**Explain simply:**
- **Independent:** an employee being born in March does not change their chance of resigning. Test: P(A and B) = P(A) x P(B).
- **Mutually exclusive:** one die roll cannot be both a 2 and a 5. Test: P(A and B) = 0.
- Mutually exclusive events (with non-zero probabilities) are never independent, because P(A and B) = 0 but P(A) x P(B) is not 0.
**Formula in plain words:** independent: chance of both = chance of A times chance of B. Mutually exclusive: chance of both = 0.
**Worked example:** One die roll. A = "roll a 2", B = "roll a 5": P(A and B) = 0, mutually exclusive. Two separate rolls: A = "first roll is 6", B = "second roll is 6": P(both) = 1/36 = 1/6 x 1/6, independent.
**Excel / Python:**
```python
# One roll: a 2 and a 5 cannot happen together
probability_two_and_five = 0
probability_two = 1 / 6
probability_five = 1 / 6
print("Mutually exclusive: P(both) =", probability_two_and_five)
print("Product of the two =", round(probability_two * probability_five, 4))

# Two rolls: a six on each is independent
probability_two_sixes = (1 / 6) * (1 / 6)
print("Independent: P(two sixes) =", round(probability_two_sixes, 4))
```
```text
Mutually exclusive: P(both) = 0
Product of the two = 0.0278
Independent: P(two sixes) = 0.0278
```
For exclusive events the "both" chance (0) does not equal the product (0.0278), so they are not independent. For two rolls it equals the product, so they are.
**Likely follow-ups:** 1) *Can events be both?* Only if one of them has probability 0. 2) *Why does it matter?* It decides whether you add or multiply (Q5).
**Common mistakes:** Saying "mutually exclusive means independent"; assuming events are independent without checking.

### Q3 ⭐⭐⭐ 🟢 What is conditional probability? Explain it with a simple example.
**Asked at:** commonly asked; the sources file reports a conditional probability question in Tiger Analytics candidate reports (snippet only, mostly 2021-22).
**What the interviewer is checking:** Can you narrow the "universe" to the given group and compute within it?
**Say this in the interview:** "Conditional probability is the chance of an event once I already know another event happened. P(A|B) means the chance of A among only the cases where B is true."
**Explain simply:**
- Read the bar "|" as "given that".
- Knowing B shrinks the group you look at to just B cases, so the denominator changes.
- It is how we ask "among remote employees, how many left?" instead of "among everyone".
**Formula in plain words:** chance of A given B = chance of both A and B, divided by chance of B. P(A|B) = P(A and B) / P(B).
**Worked example:** A company has 500 employees; 150 work remotely and 12 of those remote employees left. P(left | remote) = 12/150 = 8%. Out of all 500, P(remote and left) = 12/500 = 2.4% and P(remote) = 30%, so 2.4% / 30% = 8%.
**Excel / Python:**
```python
# Counts from the HR table
total_employees = 500
remote_employees = 150
remote_who_left = 12

# Method 1: look only inside the remote group
chance_left_given_remote = remote_who_left / remote_employees

# Method 2: use the formula with probabilities out of everyone
chance_remote_and_left = remote_who_left / total_employees
chance_remote = remote_employees / total_employees
chance_by_formula = chance_remote_and_left / chance_remote

print("Inside remote group:", round(chance_left_given_remote, 4))
print("By formula:", round(chance_by_formula, 4))
```
```text
Inside remote group: 0.08
By formula: 0.08
```
Both methods agree: 8% of remote employees left.
**Likely follow-ups:** 1) *Is P(A|B) = P(B|A)?* No (Q11). 2) *When does P(A|B) = P(A)?* When the events are independent.
**Common mistakes:** Dividing by the total headcount instead of the given group; forgetting the "given" changes the denominator.

### Q4 ⭐⭐⭐ 🟢 Explain Bayes' theorem in simple words and write its formula.
**Asked at:** Bayes/conditional probability reported in a Tiger Analytics technical round (GfG candidate report, page updated Jul 2025, interview year unknown); commonly asked elsewhere.
**What the interviewer is checking:** Can you state the formula, say what each part means, and use it once.
**Say this in the interview:** "Bayes' theorem flips a conditional probability. If I know how likely the evidence is when something is true, it tells me how likely the thing is true given the evidence. It updates a starting belief (the prior) using new evidence."
**Explain simply:**
- **Prior:** your belief before the evidence (for example, the overall attrition rate).
- **Likelihood:** how likely the evidence is if the belief is true.
- **Posterior:** the updated belief after the evidence.
- The bottom of the fraction is the total chance of seeing the evidence at all (Q15).
**Formula in plain words:** chance of A given B = (chance of B given A x chance of A) divided by chance of B. P(A|B) = P(B|A) x P(A) / P(B).
**Worked example:** 20% of employees leave. Among leavers, 60% had a low engagement score; among stayers, 25% did. An employee has a low score. P(leave | low) = 0.6 x 0.2 / (0.6 x 0.2 + 0.25 x 0.8) = 0.12 / 0.32 = 37.5%.
**Excel / Python:**
```python
# Prior belief and the two likelihoods
chance_leave = 0.20
chance_stay = 1 - chance_leave
chance_low_score_given_leave = 0.60
chance_low_score_given_stay = 0.25

# Total chance of seeing a low score (leavers plus stayers)
chance_low_score = (chance_low_score_given_leave * chance_leave
                    + chance_low_score_given_stay * chance_stay)

# Bayes: updated chance of leaving given a low score
chance_leave_given_low = chance_low_score_given_leave * chance_leave / chance_low_score

print("P(low score) =", round(chance_low_score, 4))
print("P(leave | low score) =", round(chance_leave_given_low, 4))
```
```text
P(low score) = 0.32
P(leave | low score) = 0.375
```
A low score lifts the leaving chance from 20% to 37.5%, but it is still not certain.
**Likely follow-ups:** 1) *What is the prior?* Starting probability. 2) *Why is the denominator needed?* To make the answer a proper share of all cases where the evidence appears.
**Common mistakes:** Forgetting the prior (base rate); using P(B|A) as if it were P(A|B) (Q11).

### Q5 ⭐⭐⭐ 🟢 What are the addition rule (OR) and the multiplication rule (AND) of probability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when to add, when to multiply, and the overlap correction?
**Say this in the interview:** "OR means add, but subtract the overlap so it is not counted twice. AND means multiply, using the conditional chance of the second event given the first. If events are independent that conditional chance is just its normal chance."
**Explain simply:**
- Addition rule: P(A or B) = P(A) + P(B) - P(A and B). For mutually exclusive events the overlap is 0, so just add.
- Multiplication rule: P(A and B) = P(A) x P(B|A). For independent events: P(A) x P(B).
- Clue words: "either/or/at least one" suggests adding; "both/and/then" suggests multiplying.
**Formula in plain words:** either = A + B - both. Both = A times (B given A).
**Worked example:** Draw one card: P(heart or king) = 13/52 + 4/52 - 1/52 = 16/52 (the king of hearts is the overlap). Two rolls: P(6 then 6) = 1/6 x 1/6 = 1/36.
**Excel / Python:**
```python
# Addition rule: heart OR king from one card (king of hearts counted once)
chance_heart = 13 / 52
chance_king = 4 / 52
chance_heart_and_king = 1 / 52
chance_heart_or_king = chance_heart + chance_king - chance_heart_and_king

# Multiplication rule: a six on two separate rolls
chance_two_sixes = (1 / 6) * (1 / 6)

print("P(heart or king) =", round(chance_heart_or_king, 4), "which is 16/52 =", round(16 / 52, 4))
print("P(two sixes) =", round(chance_two_sixes, 4))
```
```text
P(heart or king) = 0.3077 which is 16/52 = 0.3077
P(two sixes) = 0.0278
```
Without subtracting the overlap we would get 17/52 and count the king of hearts twice.
**Likely follow-ups:** 1) *When can I skip the subtraction?* Mutually exclusive events. 2) *When can I skip the conditional?* Independent events.
**Common mistakes:** Adding when the question means "and"; forgetting the overlap; multiplying for dependent events (Q16).

### Q6 ⭐⭐⭐ 🟢 What is the complement rule, and when does it make a probability question easier?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the "1 minus the opposite" shortcut for "at least one" questions?
**Say this in the interview:** "The complement of an event is 'it does not happen'. Since something must happen, P(event) = 1 minus P(not event). I use it whenever 'at least one' would need many cases but 'none' is a single case."
**Explain simply:**
- Event and its complement cover everything and never overlap, so they add to 1.
- "At least one" is hard to list directly; "none" is one simple product.
- Works for HR too: chance at least one of 10 new joiners quits = 1 minus chance none quit.
**Formula in plain words:** chance it happens = 1 minus chance it does not. P(A) = 1 - P(not A).
**Worked example:** Each of 10 new joiners independently has a 90% chance of staying a year. P(all stay) = 0.9^10 = 0.3487, so P(at least one leaves) = 1 - 0.3487 = 0.6513.
**Excel / Python:**
```python
# Chance one joiner stays the year, and how many joiners we look at
chance_one_stays = 0.90
number_of_joiners = 10

# Chance that ALL of them stay (independent, so multiply)
chance_all_stay = chance_one_stays ** number_of_joiners

# Complement: at least one leaves
chance_at_least_one_leaves = 1 - chance_all_stay

print("P(all stay) =", round(chance_all_stay, 4))
print("P(at least one leaves) =", round(chance_at_least_one_leaves, 4))
```
```text
P(all stay) = 0.3487
P(at least one leaves) = 0.6513
```
Even with a high individual stay rate, there is about a 65% chance that someone in the group leaves.
**Likely follow-ups:** 1) *Does it need independence?* The "all stay" product does; the 1 minus rule itself does not.
**Common mistakes:** Computing the complement of "at least one" as "at most one" (it is "none").

### Q7 ⭐⭐⭐ 🟢 What is the probability of getting a sum of 7 when two fair dice are rolled?
**Asked at:** the sources file lists "sum of 7 with two dice" in a 2024 probability question bank (snippet only).
**What the interviewer is checking:** Do you list the sample space systematically (36 outcomes) rather than guess?
**Say this in the interview:** "Two dice give 36 equally likely pairs. Six of them add up to 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). So the probability is 6/36, which is 1/6."
**Explain simply:**
- Treat the dice as different (first and second), so (1,6) and (6,1) are separate outcomes.
- 7 is the most likely sum because every first-die value has exactly one partner that makes 7.
**Formula in plain words:** favourable pairs divided by 36.
**Worked example:** Favourable = 6, total = 36, P = 6/36 = 0.1667.
**Excel / Python:**
```python
# Build every possible pair of two dice (first die, second die)
all_pairs = []
for first_die in range(1, 7):
    for second_die in range(1, 7):
        all_pairs.append((first_die, second_die))

# Keep only the pairs that add up to 7
pairs_summing_to_seven = []
for pair in all_pairs:
    if pair[0] + pair[1] == 7:
        pairs_summing_to_seven.append(pair)

# Probability = favourable pairs / all pairs
probability_of_seven = len(pairs_summing_to_seven) / len(all_pairs)

print("All pairs:", len(all_pairs))
print("Pairs summing to 7:", pairs_summing_to_seven)
print("P(sum = 7) =", round(probability_of_seven, 4))
```
```text
All pairs: 36
Pairs summing to 7: [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]
P(sum = 7) = 0.1667
```
Six of the 36 pairs work, so about 16.7%.
**Likely follow-ups:** 1) *Least likely sums?* 2 and 12 (1/36 each).
**Common mistakes:** Counting 11 sums (2 to 12) as equally likely, giving 1/11; counting (1,6) and (6,1) as one.

### Q8 ⭐⭐⭐ 🟢 What is the probability of getting at least one head in three tosses of a fair coin?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you use the complement ("no heads at all") instead of listing 7 cases?
**Say this in the interview:** "At least one head is the opposite of all tails. All tails is 1/2 x 1/2 x 1/2 = 1/8, so the answer is 1 minus 1/8 = 7/8."
**Explain simply:**
- There are 2 x 2 x 2 = 8 equally likely sequences; only TTT has no head.
- Listing the other 7 works too, but the complement is faster and scales to 20 tosses.
**Formula in plain words:** 1 minus (chance of tails) to the power of the number of tosses.
**Worked example:** 1 - (1/2)^3 = 1 - 0.125 = 0.875.
**Excel / Python:**
```python
from itertools import product

# List all 8 possible sequences of three tosses
all_sequences = list(product("HT", repeat=3))

# Keep sequences that contain at least one head
sequences_with_a_head = []
for sequence in all_sequences:
    if "H" in sequence:
        sequences_with_a_head.append(sequence)

probability_by_counting = len(sequences_with_a_head) / len(all_sequences)

# Shortcut with the complement rule
probability_by_complement = 1 - (0.5 ** 3)

print("Sequences:", len(all_sequences), "with a head:", len(sequences_with_a_head))
print("By counting:", probability_by_counting)
print("By complement:", probability_by_complement)
```
```text
Sequences: 8 with a head: 7
By counting: 0.875
By complement: 0.875
```
Seven of eight sequences contain a head, so 87.5%. In Excel: `=1-0.5^3` returns 0.875 (any version, not run in Excel here).
**Likely follow-ups:** 1) *What about 10 tosses?* 1 - 0.5^10 = 0.999.
**Common mistakes:** Adding 1/2 + 1/2 + 1/2 = 1.5 (probabilities for overlapping events cannot just be added).

### Q9 ⭐⭐⭐ 🟢 What is expected value, and how do you calculate it?
**Asked at:** commonly asked; the sources file lists expected value of games and payouts among frequent prep topics (quant-style guides, 2026 snippets).
**What the interviewer is checking:** Do you understand it as a long-run average, not a guaranteed result?
**Say this in the interview:** "Expected value is the average outcome if you repeated the situation many times. I multiply each possible value by its probability and add them up."
**Explain simply:**
- It need not be a value you can actually get (a die's expected value is 3.5).
- It is the "weighted average" where weights are probabilities.
- Used for decisions: compare options by their expected value, along with the risk.
**Formula in plain words:** add up (value x its probability) over all outcomes. E(X) = sum of x x P(x).
**Worked example:** A recruiter earns Rs 10,000 bonus with 30% chance, Rs 4,000 with 50% chance, and Rs 0 with 20% chance. E = 10,000 x 0.3 + 4,000 x 0.5 + 0 x 0.2 = 3,000 + 2,000 = Rs 5,000.
**Excel / Python:**
```python
# Possible bonus amounts and the chance of each
bonus_amounts = [10000, 4000, 0]
bonus_chances = [0.30, 0.50, 0.20]

# Multiply each amount by its chance and add the results
expected_bonus = 0
for amount, chance in zip(bonus_amounts, bonus_chances):
    expected_bonus = expected_bonus + amount * chance

print("Chances add up to:", sum(bonus_chances))
print("Expected bonus = Rs", expected_bonus)
```
```text
Chances add up to: 1.0
Expected bonus = Rs 5000.0
```
On average the recruiter gets Rs 5,000 per cycle, even though no single cycle pays exactly that. Excel: with amounts in A2:A4 and chances in B2:B4, `=SUMPRODUCT(A2:A4,B2:B4)` returns 5000 (works in all versions, not run in Excel here).
**Likely follow-ups:** 1) *Does a higher expected value always win?* Not if risk matters. 2) *Expected value of a die?* 3.5 (Q30).
**Common mistakes:** Using a plain average of the values and ignoring the probabilities; expecting the average to be an actual outcome.

### Q10 ⭐⭐⭐ 🟢 In a company of 200 employees, 40 left last year. What is the probability that a randomly chosen employee left, and what is the probability that a randomly chosen employee stayed?
**Asked at:** commonly asked (HR-flavoured gap-fill question, no company-specific report found).
**What the interviewer is checking:** Basic counting plus the complement.
**Say this in the interview:** "Left is 40 out of 200, which is 20%. Stayed is the complement, 160 out of 200, which is 80%. They add to 100%."
**Explain simply:**
- "Randomly chosen" means every employee is equally likely to be picked, so counting works.
- This is also the attrition rate: 20% for the year.
**Formula in plain words:** employees who left divided by total employees; stayed = 1 minus that.
**Worked example:** 40/200 = 0.20; 1 - 0.20 = 0.80 (= 160/200).
**Excel / Python:**
```python
# Headcount numbers
total_employees = 200
employees_who_left = 40

# Chance a random employee left, and the complement for stayed
chance_left = employees_who_left / total_employees
chance_stayed = 1 - chance_left

print("P(left) =", chance_left)
print("P(stayed) =", chance_stayed)
print("Check: stayed count =", total_employees - employees_who_left, "so", (total_employees - employees_who_left) / total_employees)
```
```text
P(left) = 0.2
P(stayed) = 0.8
Check: stayed count = 160 so 0.8
```
One in five employees left. Excel: `=40/200` returns 0.2 and `=1-40/200` returns 0.8 (not run in Excel here).
**Likely follow-ups:** 1) *Is this attrition rate?* Yes, if the 200 is the starting headcount (average headcount is often used in practice).
**Common mistakes:** Dividing 40 by 160 (the stayers) instead of 200.

### Q11 ⭐⭐⭐ 🟢 What is the difference between P(A|B) and P(B|A)? Are they the same?
**Asked at:** commonly asked; confusing the two is the core of Bayes-style questions in the sources file (Tiger Analytics reports, snippet only).
**What the interviewer is checking:** Do you know they usually differ, and why?
**Say this in the interview:** "No, they are different questions with different groups. P(A|B) is the share of B cases that are A; P(B|A) is the share of A cases that are B. Bayes' theorem converts one into the other."
**Explain simply:**
- Example: P(Sales | left) is "of leavers, how many were in Sales". P(left | Sales) is "of Sales staff, how many left". Different denominators.
- They are equal only when P(A) = P(B), or when both are zero.
**Formula in plain words:** P(A|B) = P(A and B) / P(B), and P(B|A) = P(A and B) / P(A): same top, different bottom.
**Worked example:** 200 employees, 80 in Sales, 40 left, 24 are Sales leavers. P(Sales | left) = 24/40 = 60%. P(left | Sales) = 24/80 = 30%.
**Excel / Python:**
```python
# HR counts
sales_who_left = 24
total_who_left = 40
total_in_sales = 80

# Same top number (24), two different bottom numbers
chance_sales_given_left = sales_who_left / total_who_left
chance_left_given_sales = sales_who_left / total_in_sales

print("P(Sales | left) =", chance_sales_given_left)
print("P(left | Sales) =", chance_left_given_sales)
```
```text
P(Sales | left) = 0.6
P(left | Sales) = 0.3
```
60% of leavers were in Sales, but only 30% of Sales staff left. Mixing them up would double the apparent risk.
**Likely follow-ups:** 1) *Name a real-life mix-up?* The prosecutor's fallacy (Q44).
**Common mistakes:** Reading "60% of leavers are in Sales" as "60% of Sales leave".

### Q12 ⭐⭐⭐ 🟡 A disease affects 1% of people and a test is 99% accurate in both directions (99% sensitivity and 99% specificity). If a person tests positive, what is the probability they have the disease?
**Asked at:** classic Bayes question; the sources file lists a 1% prevalence medical-test exercise (Codefinity) and Bayes in a Tiger Analytics technical round (GfG report, year unknown).
**What the interviewer is checking:** Do you resist the "99%" answer and use the base rate?
**Say this in the interview:** "It is only 50%. Out of 10,000 people, 100 are sick and 99 of them test positive. Of the 9,900 healthy people, 1% (99) also test positive. So 99 of the 198 positives are truly sick."
**Explain simply:**
- **Sensitivity:** chance a sick person tests positive (99%). **Specificity:** chance a healthy person tests negative (99%).
- The disease is rare, so the many healthy people produce as many false alarms as the few sick people produce true alarms.
**Formula in plain words:** true positives divided by all positives (true plus false). P(D|+) = P(+|D) P(D) / [P(+|D) P(D) + P(+|not D) P(not D)].
**Worked example:** 10,000 people: 100 sick (99 positive), 9,900 healthy (99 positive). 99 / (99 + 99) = 50%.
**Excel / Python:**
```python
# Given information
disease_rate = 0.01
sensitivity = 0.99
specificity = 0.99
false_positive_rate = 1 - specificity

# Picture 10,000 people to make it concrete
people = 10000
sick_people = people * disease_rate
healthy_people = people - sick_people
true_positives = sick_people * sensitivity
false_positives = healthy_people * false_positive_rate

# Chance of disease given a positive test
chance_disease_given_positive = true_positives / (true_positives + false_positives)

print("True positives:", round(true_positives, 2))
print("False positives:", round(false_positives, 2))
print("P(disease | positive) =", round(chance_disease_given_positive, 4))
```
```text
True positives: 99.0
False positives: 99.0
P(disease | positive) = 0.5
```
Half of all positive results are false alarms. Excel: `=0.99*0.01/(0.99*0.01+0.01*0.99)` returns 0.5 (not run in Excel here).
**Likely follow-ups:** 1) *What if prevalence were 10%?* About 91.7% (0.099 / (0.099 + 0.009)). 2) *What would you do after one positive?* Repeat the test (Q49).
**Common mistakes:** Answering 99%; forgetting that the false positives come from the large healthy group.

### Q13 ⭐⭐⭐ 🟡 A test is "99% accurate" and a patient tests positive. Does that mean there is a 99% chance the patient has the condition? Explain the base-rate idea.
**Asked at:** classic interview point; Bayes and base rates appear in the sources file (Tiger Analytics report, Chicago and Velasco lecture notes, snippets only).
**What the interviewer is checking:** Do you understand that "accuracy" and "chance I am sick given positive" are different, and that rarity matters?
**Say this in the interview:** "No. Accuracy says how the test behaves on sick and healthy people. What the patient wants is the chance of being sick given a positive result, and that depends on how common the condition is. The common-ness is the base rate."
**Explain simply:**
- **Base rate:** how common the condition is before any test (prevalence).
- Rare condition: most people are healthy, so even a small false-positive rate creates many false alarms.
- Common condition: the same test becomes much more trustworthy.
- "99% accurate" is also vague: it may mean sensitivity, specificity or overall correctness.
**Formula in plain words:** chance of condition given positive = true positives divided by (true positives plus false positives).
**Worked example:** Same 99% sensitivity and specificity, different base rates. At 0.1% prevalence the answer is about 9%; at 1% it is 50%; at 10% it is 91.7%; at 50% it is 99%.
**Excel / Python:**
```python
# Test quality is fixed; only the base rate changes
sensitivity = 0.99
false_positive_rate = 0.01
base_rates = [0.001, 0.01, 0.10, 0.50]

for base_rate in base_rates:
    # Probability of a positive result from sick and from healthy people
    positive_from_sick = sensitivity * base_rate
    positive_from_healthy = false_positive_rate * (1 - base_rate)

    # Chance of condition given a positive test
    chance_sick_given_positive = positive_from_sick / (positive_from_sick + positive_from_healthy)
    print("Base rate", base_rate, "-> P(sick | positive) =", round(chance_sick_given_positive, 4))
```
```text
Base rate 0.001 -> P(sick | positive) = 0.0902
Base rate 0.01 -> P(sick | positive) = 0.5
Base rate 0.1 -> P(sick | positive) = 0.9167
Base rate 0.5 -> P(sick | positive) = 0.99
```
The same test gives 9% or 99% depending only on how common the condition is.
**Likely follow-ups:** 1) *Where does this show up in HR?* A "flight risk" model flagging rare resignations, or a fraud flag (Q36).
**Common mistakes:** Treating accuracy as the answer; ignoring prevalence ("base-rate neglect").

### Q14 ⭐⭐⭐ 🟡 Of 200 employees, 80 are in Sales and 24 of the Sales employees left; 40 employees left overall. What is the probability that an employee left given that they are in Sales, and are "leaving" and "being in Sales" independent?
**Asked at:** HR-flavoured gap-fill (standard conditional probability and independence check); no company-specific report found.
**What the interviewer is checking:** Conditional probability and the independence test P(A and B) = P(A) x P(B).
**Say this in the interview:** "Among Sales, 24 of 80 left, so 30%. Overall attrition is 20%. Since 30% is not 20%, leaving and being in Sales are not independent: Sales staff leave more often."
**Explain simply:**
- Independent means knowing the department does not change the leaving chance.
- Here it does (30% vs 20%), so the events are dependent. This is an observation in this data, not proof of cause.
**Formula in plain words:** independent if P(left | Sales) = P(left), equivalently P(left and Sales) = P(left) x P(Sales).
**Worked example:** P(left and Sales) = 24/200 = 0.12. P(left) x P(Sales) = 0.20 x 0.40 = 0.08. 0.12 is not 0.08.
**Excel / Python:**
```python
# HR counts
total_employees = 200
sales_employees = 80
sales_who_left = 24
total_who_left = 40

# Conditional probability: leaving among Sales only
chance_left_given_sales = sales_who_left / sales_employees

# Overall leaving chance and Sales share
chance_left = total_who_left / total_employees
chance_sales = sales_employees / total_employees
chance_left_and_sales = sales_who_left / total_employees

print("P(left | Sales) =", chance_left_given_sales)
print("P(left) =", chance_left)
print("P(left and Sales) =", chance_left_and_sales)
print("P(left) x P(Sales) =", round(chance_left * chance_sales, 4))
print("Independent?", abs(chance_left_and_sales - chance_left * chance_sales) < 1e-12)
```
```text
P(left | Sales) = 0.3
P(left) = 0.2
P(left and Sales) = 0.12
P(left) x P(Sales) = 0.08
Independent? False
```
Sales attrition (30%) is 1.5 times the company rate (20%), so the events are not independent. With a sample this small one would still test significance before acting.
**Likely follow-ups:** 1) *Does Sales cause leaving?* Not shown; other factors may differ. 2) *How to test formally?* Chi-square test of independence.
**Common mistakes:** Calling it independent because 24 looks small; computing 24/40 (that is P(Sales | left)).

### Q15 ⭐⭐⭐ 🟡 What is the law of total probability, and how does it help in a Bayes problem?
**Asked at:** the sources file lists total probability as a standard topic (Codefinity, StrataScratch, InterviewBit snippets); no company-specific report found.
**What the interviewer is checking:** Can you build the denominator of Bayes by splitting into cases?
**Say this in the interview:** "If the population splits into non-overlapping groups that cover everyone, the chance of an event is the sum over groups of (group share x chance of the event in that group). In Bayes, that sum is the denominator."
**Explain simply:**
- Groups must not overlap and must cover everything (for example, machine A or machine B; sick or healthy).
- It answers "overall, how often do I see this evidence?"
- Divide one group's contribution by the total to get Bayes' answer.
**Formula in plain words:** P(B) = P(B|A1) P(A1) + P(B|A2) P(A2) + ... over all groups.
**Worked example:** Machine A makes 60% of items (2% defective), B makes 40% (5% defective). Overall defect rate = 0.6 x 0.02 + 0.4 x 0.05 = 0.012 + 0.020 = 3.2%. Of defects, B's share = 0.020 / 0.032 = 62.5%.
**Excel / Python:**
```python
# Share of output and defect rate for each machine
share_machine_a = 0.60
share_machine_b = 0.40
defect_rate_a = 0.02
defect_rate_b = 0.05

# Law of total probability: overall defect rate
defects_from_a = share_machine_a * defect_rate_a
defects_from_b = share_machine_b * defect_rate_b
overall_defect_rate = defects_from_a + defects_from_b

# Bayes: chance a defective item came from machine B
chance_b_given_defective = defects_from_b / overall_defect_rate

print("Overall defect rate =", round(overall_defect_rate, 4))
print("P(machine B | defective) =", round(chance_b_given_defective, 4))
```
```text
Overall defect rate = 0.032
P(machine B | defective) = 0.625
```
Machine B makes only 40% of items but 62.5% of the defects.
**Likely follow-ups:** 1) *Do the groups need to sum to 100%?* Yes.
**Common mistakes:** Using groups that overlap; adding the defect rates (2% + 5%) without weighting by share.

### Q16 ⭐⭐⭐ 🟡 Two cards are drawn from a standard deck without replacement. What is the probability that both are aces?
**Asked at:** commonly asked (card-draw classic; no company-specific report found).
**What the interviewer is checking:** Do you adjust for the changed deck after the first draw?
**Say this in the interview:** "First ace: 4/52. If that happened, 3 aces remain in 51 cards, so second ace: 3/51. Multiply: 12/2652 = 1/221, about 0.45%."
**Explain simply:**
- Without replacement, the first card stays out, so the draws are dependent.
- Multiplication rule: P(A and B) = P(A) x P(B | A).
**Formula in plain words:** (aces / cards) x ((aces - 1) / (cards - 1)).
**Worked example:** 4/52 x 3/51 = 12/2652 = 1/221 = 0.004525.
**Excel / Python:**
```python
from fractions import Fraction

# First draw: 4 aces in 52 cards
chance_first_ace = Fraction(4, 52)

# Second draw: one ace gone, one card gone
chance_second_ace_given_first = Fraction(3, 51)

# Multiply for "first AND second"
chance_both_aces = chance_first_ace * chance_second_ace_given_first

print("Exact fraction:", chance_both_aces)
print("As a decimal:", round(float(chance_both_aces), 6))
```
```text
Exact fraction: 1/221
As a decimal: 0.004525
```
About 1 chance in 221. Excel: `=(4/52)*(3/51)` returns 0.004525 (not run in Excel here).
**Likely follow-ups:** 1) *With replacement?* (4/52)^2 = 1/169 (Q17).
**Common mistakes:** Using 4/52 x 4/52; or 4/52 x 3/52.

### Q17 ⭐⭐⭐ 🟡 A bag has 5 red and 3 blue balls. What is the probability of drawing two red balls with replacement and without replacement?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Independent vs dependent draws.
**Say this in the interview:** "With replacement the bag is the same each time: 5/8 x 5/8 = 25/64, about 39.1%. Without replacement the second draw is 4/7: 5/8 x 4/7 = 20/56 = 5/14, about 35.7%."
**Explain simply:**
- With replacement: draws are independent.
- Without: one red is gone and the bag has 7 balls; draws are dependent.
- Removing a red ball lowers the chance of another red, so the without-replacement answer is smaller.
**Formula in plain words:** with replacement: (red/total)^2. Without: (red/total) x ((red-1)/(total-1)).
**Worked example:** 25/64 = 0.3906 versus 20/56 = 0.3571.
**Excel / Python:**
```python
from fractions import Fraction

red_balls = 5
total_balls = 8

# With replacement: the bag is restored, so each draw is 5/8
with_replacement = Fraction(red_balls, total_balls) * Fraction(red_balls, total_balls)

# Without replacement: second draw has 4 red among 7 balls
without_replacement = Fraction(red_balls, total_balls) * Fraction(red_balls - 1, total_balls - 1)

print("With replacement:", with_replacement, "=", round(float(with_replacement), 4))
print("Without replacement:", without_replacement, "=", round(float(without_replacement), 4))
```
```text
With replacement: 25/64 = 0.3906
Without replacement: 5/14 = 0.3571
```
Drawing without replacement makes two reds less likely (35.7% vs 39.1%).
**Likely follow-ups:** 1) *When does it hardly matter?* When the population is huge compared with the sample (Q29).
**Common mistakes:** Using 5/8 for both draws in the without-replacement case.

### Q18 ⭐⭐⭐ 🟡 Explain the Monty Hall problem. Should you switch doors, and why?
**Asked at:** classic puzzle; the sources file lists Monty Hall among frequent prep-site puzzles and mentions analytics puzzles reportedly asked at several firms (unverified claim); no company-specific report confirmed.
**What the interviewer is checking:** Can you resist intuition ("it is 50-50") and justify with probability.
**Say this in the interview:** "Yes, switch. You win by switching 2/3 of the time. Your first pick is right with chance 1/3 and the host always opens a goat door, so the remaining door holds the car whenever your first pick was wrong, which is 2/3 of the time."
**Explain simply:**
- Setup: 3 doors, 1 car, 2 goats. You pick a door. The host, who knows where the car is, opens another door showing a goat and offers a switch.
- The host's move is not random: he never opens the car. That gives you information.
- Your original door keeps its 1/3; the other 2/3 is squeezed onto the one door left.
- Assumption: the host always opens a goat door and always offers the switch.
**Formula in plain words:** win by staying = chance first pick was right (1/3); win by switching = chance first pick was wrong (2/3).
**Worked example:** Car behind door 1, you pick door 1: staying wins. You pick door 2 or 3: host opens the other goat, switching wins. That is 2 of 3 equally likely first picks.
**Excel / Python:**
```python
import random

random.seed(42)
number_of_games = 100000
stay_wins = 0
switch_wins = 0

for game in range(number_of_games):
    # Car hidden behind a random door; contestant picks a random door
    car_door = random.randint(1, 3)
    first_pick = random.randint(1, 3)

    # Host opens a goat door that is not the pick and not the car
    host_options = []
    for door in [1, 2, 3]:
        if door != first_pick and door != car_door:
            host_options.append(door)
    host_opens = random.choice(host_options)

    # The door you would switch to is the one left unopened (door numbers 1+2+3 add to 6)
    switch_pick = 6 - first_pick - host_opens

    if first_pick == car_door:
        stay_wins = stay_wins + 1
    if switch_pick == car_door:
        switch_wins = switch_wins + 1

print("Stay win rate:", round(stay_wins / number_of_games, 3))
print("Switch win rate:", round(switch_wins / number_of_games, 3))
```
```text
Stay win rate: 0.333
Switch win rate: 0.667
```
Over 100,000 simulated games, switching wins about two-thirds of the time and staying about one-third.
**Likely follow-ups:** 1) *What if the host opened a door at random and happened to show a goat?* Then it is 50-50, because the host's move carries no information. 2) *Intuition with 100 doors?* Pick one, host opens 98 goats: the last door clearly holds the 99% share.
**Common mistakes:** Saying 50-50 because two doors remain (two options are not two equally likely options).

### Q19 ⭐⭐⭐ 🟡 Machine A makes 60% of items with 2% defective, machine B makes 40% with 5% defective. An item is found defective. What is the probability it came from machine B?
**Asked at:** Bayes/conditional-probability questions are reported for Tiger Analytics (GfG candidate report, year unknown); this exact two-machine version is a standard textbook problem, commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you reverse a conditional probability (from "defective given machine" to "machine given defective") using Bayes' theorem?
**Say this in the interview:** "I find the chance an item is defective AND from B, then divide by the chance an item is defective at all. That gives 0.02 / 0.032 = 62.5%. B makes fewer items, but it is defective more often, so it is the more likely source."
**Explain simply:**
- **Bayes' theorem** updates a probability after you learn something new (here: the item is defective).
- Step 1: P(defective and A) = 0.60 x 0.02 = 0.012. Step 2: P(defective and B) = 0.40 x 0.05 = 0.020.
- Step 3: add them for the total defective rate (the **law of total probability**, adding up every route to "defective"): 0.032.
- Step 4: B's share of that total is 0.020 / 0.032.
**Formula in plain words:** Chance of B given defective = (chance of B x chance defective if B) divided by (total chance of defective). In symbols: P(B|D) = P(D|B) x P(B) / P(D).
**Worked example:** In 1,000 items, A makes 600 (12 defective) and B makes 400 (20 defective). Of 32 defective items, 20 came from B: 62.5%.
**Excel / Python:**
```python
# Share of items made by each machine
share_machine_a = 0.60
share_machine_b = 0.40

# Chance an item is defective, given the machine
defect_rate_a = 0.02
defect_rate_b = 0.05

# Chance of "defective AND from machine" for each machine
defective_and_a = share_machine_a * defect_rate_a
defective_and_b = share_machine_b * defect_rate_b

# Total chance an item is defective (law of total probability)
total_defective = defective_and_a + defective_and_b

# Bayes: chance it came from B, given it is defective
prob_b_given_defective = defective_and_b / total_defective

print("P(defective and A) =", round(defective_and_a, 4))
print("P(defective and B) =", round(defective_and_b, 4))
print("P(defective)       =", round(total_defective, 4))
print("P(B | defective)   =", round(prob_b_given_defective, 4))
```
Output:
```
P(defective and A) = 0.012
P(defective and B) = 0.02
P(defective)       = 0.032
P(B | defective)   = 0.625
```
Of all defective items, 62.5% come from machine B.
**Likely follow-ups:** 1) *What about A?* 1 - 0.625 = 37.5%, because the two shares must add to 100%. 2) *Why not just say 5% / (2% + 5%)?* That ignores that A makes more items (the base rate).
**Common mistakes:** Forgetting to weight by production share; answering 5% or 40%.

### Q20 ⭐⭐⭐ 🟡 How would you explain conditional probability and Bayes' theorem to a non-technical manager?
**Asked at:** commonly asked (no company-specific report found); communication of Bayes is a typical follow-up to the Bayes questions reported for Tiger Analytics.
**What the interviewer is checking:** Can you explain a tricky idea in plain business words, with numbers, without formulas?
**Say this in the interview:** "Conditional probability is the chance of something once you already know something else. Bayes' theorem is how I flip it: if I know how many leavers had low engagement scores, I can work out how many low-score people will actually leave."
**Explain simply:**
- **Conditional probability:** "out of only the people who have this feature, how many did that?"
- **Bayes' theorem:** turns "chance of the clue given the outcome" into "chance of the outcome given the clue".
- Easiest for managers: use 1,000 real people instead of percentages.
- The key message: the base rate (how common the outcome is overall) matters as much as the clue.
**Formula in plain words:** Chance of outcome given clue = (people with clue AND outcome) divided by (all people with the clue).
**Worked example:** 1,000 employees, 10% leave (100). 70% of leavers had a low engagement score (70 people) and so did 20% of stayers (180 people). Of the 250 people with a low score, 70 left, so 28%. The score is useful (28% vs 10% base) but most low-score people still stay.
**Excel / Python:**
```python
# Imagine 1,000 employees, so we can use whole people instead of percentages
total_employees = 1000

# 10% leave during the year
leavers = 100
stayers = total_employees - leavers

# 70% of leavers had a low engagement score; 20% of stayers did too
leavers_with_low_score = 0.70 * leavers
stayers_with_low_score = 0.20 * stayers

# Everyone with a low score, whether they left or not
all_low_score = leavers_with_low_score + stayers_with_low_score

# Of the people with a low score, what share actually left?
share_who_left = leavers_with_low_score / all_low_score

print("Low-score leavers:", leavers_with_low_score)
print("Low-score stayers:", stayers_with_low_score)
print("Share of low-score people who left:", round(share_who_left, 3))
```
Output:
```
Low-score leavers: 70.0
Low-score stayers: 180.0
Share of low-score people who left: 0.28
```
Only 28% of low-score employees leave, even though 70% of leavers had a low score.
**Likely follow-ups:** 1) *Why not just say 70%?* That is the chance of a low score among leavers, the reverse question. 2) *Why does it matter for HR?* Retention budgets should not assume every low-score person will quit.
**Common mistakes:** Using formulas on a manager; mixing up the two directions of the conditional.

### Q21 ⭐⭐ 🟢 What are a sample space and an event? Give an example.
**Asked at:** commonly asked (no company-specific report found); a basics question in the probability lists we found.
**What the interviewer is checking:** Do you know the vocabulary that every probability calculation starts from?
**Say this in the interview:** "The sample space is the list of every possible outcome. An event is any group of outcomes we care about. Probability is the size of the event divided by the size of the sample space, when outcomes are equally likely."
**Explain simply:**
- **Sample space:** all possible results. One die: {1, 2, 3, 4, 5, 6}.
- **Event:** a subset of the sample space. "Even number" = {2, 4, 6}.
- HR version: for one employee, the sample space is {stays, leaves}; "leaves" is an event.
- Always list the sample space first; it stops you missing cases.
**Formula in plain words:** Probability of event = number of outcomes in the event divided by number of outcomes in the sample space (equally likely outcomes only). P(E) = n(E) / n(S).
**Worked example:** P(even on a die) = 3 / 6 = 0.5.
**Excel / Python:**
```python
# The sample space: every possible result of one die roll
sample_space = [1, 2, 3, 4, 5, 6]

# The event "result is even": a chosen subset of the sample space
event_even = [outcome for outcome in sample_space if outcome % 2 == 0]

# Probability = outcomes in the event / outcomes in the sample space
probability_even = len(event_even) / len(sample_space)

print("Sample space:", sample_space)
print("Event (even):", event_even)
print("P(even) =", probability_even)
```
Output:
```
Sample space: [1, 2, 3, 4, 5, 6]
Event (even): [2, 4, 6]
P(even) = 0.5
```
The event has 3 outcomes out of 6 possible, so the probability is one half.
**Likely follow-ups:** 1) *Sample space for two coin tosses?* {HH, HT, TH, TT}, 4 outcomes, not 3. 2) *What is the empty event?* No outcomes; probability 0.
**Common mistakes:** Listing HT and TH as one outcome; counting outcomes that are not equally likely as if they were.

### Q22 ⭐⭐ 🟢 What is the difference between probability and odds?
**Asked at:** commonly asked (no company-specific report found); odds ratio appears in the prep lists, so odds is the prerequisite.
**What the interviewer is checking:** Do you know the two scales and can you convert between them?
**Say this in the interview:** "Probability is wins out of all tries; odds is wins compared with losses. A 20% chance is odds of 1 to 4."
**Explain simply:**
- **Probability** = favourable / total, always between 0 and 1.
- **Odds** = chance it happens / chance it does not, from 0 to infinity.
- Same information, different scale. Odds are used in logistic regression and betting.
- Odds above 1 mean "more likely than not".
**Formula in plain words:** Odds = p divided by (1 - p). Probability = odds divided by (1 + odds).
**Worked example:** A candidate accepts with probability 0.20. Odds = 0.20 / 0.80 = 0.25, i.e. 1 to 4. Check back: 0.25 / 1.25 = 0.20.
**Excel / Python:**
```python
# Probability that a candidate accepts the offer
probability_accept = 0.20

# Odds = chance it happens / chance it does not
odds_accept = probability_accept / (1 - probability_accept)

# Going back: probability = odds / (1 + odds)
probability_again = odds_accept / (1 + odds_accept)

print("Probability:", probability_accept)
print("Odds:", odds_accept, "(that is 1 to 4)")
print("Back to probability:", probability_again)
```
Output:
```
Probability: 0.2
Odds: 0.25 (that is 1 to 4)
Back to probability: 0.2
```
Probability 0.2 and odds 0.25 describe the same chance.
**Likely follow-ups:** 1) *Odds of 3 to 1 in favour?* Probability 3/4 = 75%. 2) *Why do analysts use odds?* Logistic regression models log-odds.
**Common mistakes:** Saying "odds of 1 in 5" when meaning probability 1/5 (odds would be 1 to 4).

### Q23 ⭐⭐ 🟢 What is the range of a probability value, and what do a probability of 0 and a probability of 1 mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic sanity-check skill: can you spot an impossible probability in an answer?
**Say this in the interview:** "A probability is always between 0 and 1. Zero means impossible, one means certain. If my calculation gives 1.2 or -0.1, I know I made an error."
**Explain simply:**
- 0 = cannot happen (a die showing 7). 1 = must happen (a die showing 1 to 6).
- 0.5 = equally likely to happen or not. As a percentage, between 0% and 100%.
- Probabilities of all outcomes in the sample space add to exactly 1.
- Nuance: for continuous variables, probability 0 does not always mean impossible (any exact salary such as 50,000.0000 has probability 0), but at interview level "impossible" is the expected answer.
**Formula in plain words:** 0 <= P(A) <= 1, and P(A) + P(not A) = 1.
**Worked example:** P(an employee is in Sales) = 80 / 200 = 0.4. If someone gave 80 / 20 = 4, the value is above 1, so the setup is wrong.
**Likely follow-ups:** 1) *Can a probability be negative?* No. 2) *If P(A) = 0.3, what is P(not A)?* 0.7.
**Common mistakes:** Dividing the wrong way round and not noticing a value above 1; treating "very unlikely" as exactly 0.

### Q24 ⭐⭐ 🟢 What is the difference between classical (theoretical) probability and empirical (relative-frequency) probability?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where a probability comes from: reasoning or data?
**Say this in the interview:** "Classical probability comes from counting equally likely outcomes, like 1/6 for a six. Empirical probability comes from data: the share of times it actually happened. In analytics, almost everything is empirical."
**Explain simply:**
- **Classical:** works when outcomes are equally likely (fair die, fair coin, shuffled deck).
- **Empirical:** count what happened. "40 of 200 employees left" gives 0.20.
- No fair-dice assumption exists for real HR data, so we estimate from history.
- With more data, empirical moves towards the true value (law of large numbers, Q27).
**Formula in plain words:** Classical: favourable outcomes / all possible outcomes. Empirical: times it happened / times we looked.
**Worked example:** Roll a die: classical P(six) = 1/6 = 0.1667. A simulation of 60, 600 and 60,000 rolls gives 0.1667, 0.1817, 0.1683.
**Excel / Python:**
```python
import random

# Fix the random seed so the run can be repeated exactly
random.seed(42)

# Classical probability of a six: 1 favourable face out of 6
classical_probability = 1 / 6

# Empirical probability: roll a die many times and count sixes
for number_of_rolls in [60, 600, 60000]:
    sixes_seen = 0
    for roll_number in range(number_of_rolls):
        roll = random.randint(1, 6)
        if roll == 6:
            sixes_seen += 1
    empirical_probability = sixes_seen / number_of_rolls
    print(number_of_rolls, "rolls -> sixes:", sixes_seen, "-> share:", round(empirical_probability, 4))

print("Classical answer:", round(classical_probability, 4))
```
Output:
```
60 rolls -> sixes: 10 -> share: 0.1667
600 rolls -> sixes: 109 -> share: 0.1817
60000 rolls -> sixes: 10096 -> share: 0.1683
Classical answer: 0.1667
```
The empirical shares wobble around 0.1667; they are not exactly equal even for 60,000 rolls, but they are close.
**Likely follow-ups:** 1) *Which one do you use for attrition?* Empirical, from past records. 2) *Could the two disagree?* Yes, if the die is loaded.
**Common mistakes:** Assuming outcomes are equally likely when they are not (e.g. "50% chance a candidate joins: join or not join").

### Q25 ⭐⭐ 🟢 What is a random variable? Explain discrete versus continuous with examples.
**Asked at:** commonly asked (no company-specific report found); distributions are covered in Part 3.
**What the interviewer is checking:** Do you understand the building block behind averages, variance and distributions?
**Say this in the interview:** "A random variable is a number whose value depends on chance, like the number of leavers next month. Discrete means countable values; continuous means any value in a range, like salary or tenure."
**Explain simply:**
- **Random variable:** turns an uncertain outcome into a number, so we can calculate with it.
- **Discrete:** can be listed and counted: number of leavers (0, 1, 2, ...), dice total, number of absences.
- **Continuous:** measured on a scale with decimals: salary, commute time, weight, tenure in years.
- Discrete variables have probabilities for each value; continuous ones have probabilities over ranges (area under a curve).
**Worked example:** X = number of heads in 2 coin tosses (discrete): P(0) = 0.25, P(1) = 0.5, P(2) = 0.25. Y = a random employee's monthly salary (continuous): we ask P(40,000 < Y < 60,000), not P(Y = exactly 50,000).
**Likely follow-ups:** 1) *Is age discrete or continuous?* Age in completed years is discrete; exact age is continuous. 2) *Which distributions fit?* Binomial/Poisson for counts, normal for measurements (Part 3).
**Common mistakes:** Calling every number "continuous"; mixing up the random variable with its observed value.

### Q26 ⭐⭐ 🟢 What are joint, marginal and conditional probability? Show them on a two-way table.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read three different probabilities off a single table without mixing them up?
**Say this in the interview:** "Joint is both things together, marginal is one thing ignoring the other (a row or column total), and conditional is one thing inside a chosen group."
**Explain simply:**
- **Joint:** P(Sales AND Left), one cell divided by the grand total.
- **Marginal:** P(Left), a column total divided by the grand total.
- **Conditional:** P(Left | Sales), one cell divided by its row total only.
- The denominator is the whole clue: grand total, column total, or row total.
**Formula in plain words:** Conditional = joint divided by marginal of the condition. P(A|B) = P(A and B) / P(B).
**Worked example:** 200 employees: Sales left 24, Sales stayed 56, Other left 16, Other stayed 104. Joint = 24/200 = 0.12, marginal P(Left) = 40/200 = 0.20, conditional P(Left|Sales) = 24/80 = 0.30.
**Excel / Python:**
```python
import pandas as pd

# Headcount table: department by whether the person left
headcount = pd.DataFrame(
    {"Left": [24, 16], "Stayed": [56, 104]},
    index=["Sales", "Other"],
)
total_employees = headcount.values.sum()

# Joint probability: Sales AND Left
joint_sales_and_left = headcount.loc["Sales", "Left"] / total_employees

# Marginal probabilities: one row or one column total over everyone
marginal_left = headcount["Left"].sum() / total_employees
marginal_sales = headcount.loc["Sales"].sum() / total_employees

# Conditional probability: Left, looking only at the Sales row
conditional_left_given_sales = headcount.loc["Sales", "Left"] / headcount.loc["Sales"].sum()

print(headcount)
print("Joint P(Sales and Left)  =", joint_sales_and_left)
print("Marginal P(Left)         =", marginal_left)
print("Marginal P(Sales)        =", marginal_sales)
print("Conditional P(Left|Sales)=", conditional_left_given_sales)
```
Output:
```
       Left  Stayed
Sales    24      56
Other    16     104
Joint P(Sales and Left)  = 0.12
Marginal P(Left)         = 0.2
Marginal P(Sales)        = 0.4
Conditional P(Left|Sales)= 0.3
```
Sales employees leave at 30%, compared with 20% across the company.
**Likely follow-ups:** 1) *Excel?* `=B2/SUM($B$2:$C$3)` for joint (layout: Sales/Other in A2:A3, Left in B, Stayed in C; not run in Excel here). 2) *Are they independent?* No, 30% is not 20% (Q37).
**Common mistakes:** Using the grand total as denominator for a conditional probability.

### Q27 ⭐⭐ 🟢 What is the law of large numbers, and why does a coin not "owe" you a tail after five heads in a row?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that averages settle with more data, but that single events have no memory?
**Say this in the interview:** "The law of large numbers says that as the number of trials grows, the observed average gets closer to the true probability. It does not say the coin compensates; it just gets swamped by later tosses."
**Explain simply:**
- Small samples are noisy: 10 tosses can easily give 70% heads.
- Large samples settle: 100,000 tosses give about 50%.
- The coin has no memory; each toss is independent, so the next toss is still 50/50.
- Early imbalance is not corrected, it is diluted: 5 extra heads matter less and less as tosses pile up.
- For analysts: a team of 10 with 2 leavers (20%) tells you less than a company of 10,000.
**Worked example (simulation):**
```python
import random

# Fix the random seed so the run can be repeated exactly
random.seed(7)

# Toss a fair coin many times; track the share of heads so far
heads_so_far = 0
checkpoints = [10, 100, 1000, 100000]
for toss_number in range(1, 100001):
    toss = random.random() < 0.5
    if toss:
        heads_so_far += 1
    if toss_number in checkpoints:
        print(toss_number, "tosses -> share of heads:", round(heads_so_far / toss_number, 4))
```
Output:
```
10 tosses -> share of heads: 0.7
100 tosses -> share of heads: 0.54
1000 tosses -> share of heads: 0.537
100000 tosses -> share of heads: 0.5004
```
The share of heads drifts towards 0.5 as tosses increase.
**Likely follow-ups:** 1) *Is that the same as the gambler's fallacy?* The fallacy is misreading this law (Q28). 2) *Why use big samples?* Less noise.
**Common mistakes:** Believing the law means "things even out soon".

### Q28 ⭐⭐ 🟢 What is the gambler's fallacy?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand independence in practice?
**Say this in the interview:** "It is the wrong belief that after a streak, the opposite outcome is 'due'. With independent events, the past does not change the next probability."
**Explain simply:**
- After 5 heads, the next toss is still 50% heads.
- It comes from feeling that randomness must "balance out" in the short run.
- HR example: "We had 3 resignations from this team, so the next month must be quiet" is the fallacy if resignations are independent. (If they are not independent, e.g. a bad manager, the opposite worry may be right: check the data.)
- Reverse error, the "hot hand", assumes a streak will continue; check independence before assuming either.
**Worked example (simulation of 2 million tosses, looking only at the toss right after 5 or more heads in a row):**
```python
import random

# Fix the random seed so the run can be repeated exactly
random.seed(1)

# Collect the toss that follows every run of 5 heads in a row
tosses_after_five_heads = []
heads_in_a_row = 0
for toss_number in range(2000000):
    is_head = random.random() < 0.5
    if heads_in_a_row >= 5:
        tosses_after_five_heads.append(is_head)
    if is_head:
        heads_in_a_row += 1
    else:
        heads_in_a_row = 0

# Share of heads on the toss right after 5 heads in a row
share_heads = sum(tosses_after_five_heads) / len(tosses_after_five_heads)
print("Streaks of 5+ heads checked:", len(tosses_after_five_heads))
print("Share of heads on the next toss:", round(share_heads, 3))
```
Output:
```
Streaks of 5+ heads checked: 62855
Share of heads on the next toss: 0.502
```
Right after a streak, heads still appears about half the time, so no tail is "due".
**Likely follow-ups:** 1) *Chance of 6 heads in a row from the start?* (1/2)^6 = 1.6%, but given 5 already, the 6th is still 50%. 2) *Link to the law of large numbers?* Q27.
**Common mistakes:** Mixing "6 heads in a row is rare" (true before starting) with "the next toss after 5 is rare" (false).

### Q29 ⭐⭐ 🟢 What is the difference between sampling with replacement and without replacement, and how does it change the probability?
**Asked at:** commonly asked (no company-specific report found); the idea underlies the card and ball questions in the sources.
**What the interviewer is checking:** Do you notice when the pool changes between draws?
**Say this in the interview:** "With replacement, I put the item back, so every draw has the same probabilities and draws are independent. Without replacement, the pool shrinks, so the second probability depends on the first."
**Explain simply:**
- **With replacement:** same pool each time; multiply identical probabilities.
- **Without replacement:** reduce both the favourable count and the total after each draw.
- HR example: choosing 2 people from a team for a survey: you cannot pick the same person twice, so it is without replacement.
- With huge populations the difference is tiny; with small ones it is large.
**Formula in plain words:** Both draws favourable: with replacement (k/n) x (k/n); without replacement (k/n) x ((k-1)/(n-1)).
**Worked example:** 10 employees, 4 are women; pick 2. With replacement: 0.4 x 0.4 = 0.16. Without: (4/10) x (3/9) = 0.1333.
**Excel / Python:**
```python
# A team of 10 employees, 4 of them women; pick 2 people one after another
women = 4
team_size = 10

# With replacement: the first person goes back before the second pick
with_replacement = (women / team_size) * (women / team_size)

# Without replacement: the pool shrinks to 9 people with 3 women left
without_replacement = (women / team_size) * ((women - 1) / (team_size - 1))

print("Both women, with replacement:   ", round(with_replacement, 4))
print("Both women, without replacement:", round(without_replacement, 4))
```
Output:
```
Both women, with replacement:    0.16
Both women, without replacement: 0.1333
```
Without replacement the chance is lower, because one woman is already used up.
**Likely follow-ups:** 1) *Which is used in real surveys?* Mostly without replacement. 2) *Do draws stay independent without replacement?* No.
**Common mistakes:** Using the same fraction twice when the item is not returned.

### Q30 ⭐⭐ 🟢 What is the expected value of a single roll of a fair six-sided die?
**Asked at:** expected-value dice questions appear in quant and prep sources (quantt, PracHub, 2026 snippets); commonly asked (no DA company-specific report found).
**What the interviewer is checking:** Can you apply the "value x probability, then add" rule?
**Say this in the interview:** "Expected value is the long-run average. For a die it is (1+2+3+4+5+6)/6 = 3.5. You never actually roll 3.5; it is the average over many rolls."
**Explain simply:**
- Multiply each outcome by its probability and add them.
- Each face has probability 1/6, so it is the simple average of 1 to 6.
- It need not be a possible outcome.
**Formula in plain words:** Expected value = sum of (each value x its probability). E[X] = sum of x x P(x).
**Worked example:** (1+2+3+4+5+6) x 1/6 = 21/6 = 3.5.
**Excel / Python:**
```python
# Each face of a fair die and its probability
faces = [1, 2, 3, 4, 5, 6]
probability_of_each_face = 1 / 6

# Expected value = sum of (value x probability)
expected_value = 0
for face in faces:
    expected_value += face * probability_of_each_face

print("Expected value of one roll:", round(expected_value, 4))
```
Output:
```
Expected value of one roll: 3.5
```
Over many rolls the average comes to 3.5. In Excel with faces in A1:A6: `=AVERAGE(A1:A6)` returns 3.5 (not run in Excel here).
**Likely follow-ups:** 1) *Two dice?* 7, by adding. 2) *Variance?* 35/12 = 2.92 (Q57).
**Common mistakes:** Answering 3 or "any of 1 to 6"; forgetting it is an average.

### Q31 ⭐⭐ 🟡 If 5 shortlisted candidates each accept an offer independently with probability 20%, what is the probability that at least one accepts?
**Asked at:** HR-flavoured gap-fill using the standard complement rule; commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you use the complement ("at least one" = 1 - none)?
**Say this in the interview:** "I find the chance that nobody accepts, 0.8 to the power 5, and subtract from 1. That is about 67%."
**Explain simply:**
- "At least one" has many cases (1, 2, 3, 4 or 5 accept), so count the single opposite case: none accept.
- **Independent** means one person's choice does not affect another's, so we can multiply.
- Nobody accepts: 0.8 x 0.8 x 0.8 x 0.8 x 0.8.
**Formula in plain words:** P(at least one) = 1 - (chance of no success)^number of tries. 1 - (1-p)^n.
**Worked example:** 0.8^5 = 0.32768, so 1 - 0.32768 = 0.67232. Note that 5 x 20% = 100% would be wrong (Q50).
**Excel / Python:**
```python
# Each of 5 candidates accepts with probability 20%, independently
number_of_candidates = 5
probability_accept = 0.20
probability_decline = 1 - probability_accept

# Chance that everyone declines
probability_all_decline = probability_decline ** number_of_candidates

# Complement rule: at least one accepts = 1 - nobody accepts
probability_at_least_one = 1 - probability_all_decline

print("P(all five decline):", round(probability_all_decline, 5))
print("P(at least one accepts):", round(probability_at_least_one, 5))
```
Output:
```
P(all five decline): 0.32768
P(at least one accepts): 0.67232
```
There is about a 67% chance of at least one acceptance. Excel: `=1-0.8^5` returns 0.67232 (not run in Excel here).
**Likely follow-ups:** 1) *Chance all five accept?* 0.2^5 = 0.032%. 2) *How many candidates for 95% chance?* 1-0.8^n >= 0.95 gives n = 14 (0.8^14 = 0.044).
**Common mistakes:** Multiplying 5 x 0.20 = 1.0; assuming candidates are independent when they compare offers.

### Q32 ⭐⭐ 🟡 What is the probability that a month with 31 days has 5 Sundays?
**Asked at:** "probability of 5 Sundays in a 31-day month" is mentioned in Tiger Analytics candidate reports (search-snippet summary of Glassdoor/Naukri/AmbitionBox, mostly 2021-22, unverified).
**What the interviewer is checking:** Can you break a puzzle into a simple repeating pattern (weeks)?
**Say this in the interview:** "31 days is 4 full weeks plus 3 extra days. Every weekday appears 4 times, and the 3 extra days get a fifth. 5 Sundays happen if Sunday is among those 3 days, so 3 out of 7."
**Explain simply:**
- 28 days = exactly 4 weeks, so each weekday appears 4 times.
- The extra 3 days are the 1st, 2nd and 3rd weekday of the month's start.
- If the month starts on Friday, Saturday or Sunday, Sunday is among the extra days.
- Assume the 1st can fall on any weekday with equal chance (the 7 possibilities are equally likely).
**Formula in plain words:** Probability = starting weekdays that work / 7 = 3/7.
**Worked example:** 3/7 = 0.4286. (For a 30-day month it is 2/7; for a 29-day leap February 1/7.)
**Excel / Python:**
```python
# A 31-day month = 4 full weeks (28 days) + 3 extra days.
# 5 Sundays happen only if Sunday is among those 3 extra days.
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Try each possible weekday for the 1st of the month
months_with_five_sundays = 0
for first_day_index in range(7):
    sundays_counted = 0
    for day_of_month in range(31):
        weekday = weekdays[(first_day_index + day_of_month) % 7]
        if weekday == "Sun":
            sundays_counted += 1
    print("1st is", weekdays[first_day_index], "-> Sundays:", sundays_counted)
    if sundays_counted == 5:
        months_with_five_sundays += 1

print("P(5 Sundays) =", months_with_five_sundays, "/ 7 =", round(months_with_five_sundays / 7, 4))
```
Output:
```
1st is Mon -> Sundays: 4
1st is Tue -> Sundays: 4
1st is Wed -> Sundays: 4
1st is Thu -> Sundays: 4
1st is Fri -> Sundays: 5
1st is Sat -> Sundays: 5
1st is Sun -> Sundays: 5
P(5 Sundays) = 3 / 7 = 0.4286
```
Three of the seven possible start days give 5 Sundays.
**Likely follow-ups:** 1) *Any 5 of a given weekday?* Same, 3/7 for each weekday. 2) *February in a leap year?* 1/7 for any chosen weekday.
**Common mistakes:** Saying 1/7 or 5/31; forgetting the 3 extra days.

### Q33 ⭐⭐ 🟡 In a hiring funnel, 50% of applicants clear screening, 40% of those clear the interview, and 80% of those accept the offer. What is the probability that an applicant ends up joining?
**Asked at:** HR-flavoured gap-fill using the multiplication rule; commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you chain conditional probabilities by multiplying?
**Say this in the interview:** "Each percentage is conditional on the previous step, so I multiply: 0.5 x 0.4 x 0.8 = 0.16, so 16% of applicants join."
**Explain simply:**
- "40% of those" means 40% of screening-passers, not of all applicants.
- Multiplying conditionals gives the joint chance of getting through all stages (multiplication rule).
- Check with a headcount: 1,000 applicants, 500 pass screening, 200 pass interview, 160 join.
**Formula in plain words:** P(join) = P(screen) x P(interview | screen) x P(accept | interview). 
**Worked example:** 0.50 x 0.40 x 0.80 = 0.16.
**Excel / Python:**
```python
# Stage pass rates
clear_screening = 0.50
clear_interview = 0.40
accept_offer = 0.80

# AND across stages: multiply
probability_joining = clear_screening * clear_interview * accept_offer

# Same thing for 1,000 applicants
applicants = 1000
after_screening = applicants * clear_screening
after_interview = after_screening * clear_interview
joiners = after_interview * accept_offer

print("P(joining) =", round(probability_joining, 4))
print("Applicants -> screened -> interviewed -> joined:", applicants, after_screening, after_interview, joiners)
```
Output:
```
P(joining) = 0.16
Applicants -> screened -> interviewed -> joined: 1000 500.0 200.0 160.0
```
Sixteen of every 100 applicants join. Excel: `=0.5*0.4*0.8` returns 0.16 (not run in Excel here).
**Likely follow-ups:** 1) *To hire 48 people, how many applicants?* 48 / 0.16 = 300. 2) *Which stage to improve?* The interview has the highest drop rate (60% of those who reach it), while screening loses the most people (500 of 1,000).
**Common mistakes:** Adding (0.5+0.4+0.8) or averaging the percentages.

### Q34 ⭐⭐ 🟡 How do you draw and use a probability tree diagram? Solve one example.
**Asked at:** commonly asked (no company-specific report found); tree-diagram framing is common in the Bayes teaching material we found.
**What the interviewer is checking:** Can you organise a multi-step problem visually and answer a reverse question from it?
**Say this in the interview:** "I draw the first split, then split each branch again, writing the probability on each branch. I multiply along a path to get that outcome, and add paths that give the same result."
**Explain simply:**
- Level 1: the first event (department). Level 2: the next event (left or stayed), with probabilities conditional on the branch.
- **Multiply** along a path (AND). **Add** across paths ending in the same result (OR).
- Reverse questions (Bayes): take the path you want and divide by the sum of all paths with the clue.
- Branches from one point must add to 1.
**Worked example:** 40% of employees are in Sales (30% leave), 60% in Support (10% leave).
```
Start
|-- Sales 0.40
|     |-- Left 0.30    -> 0.40 x 0.30 = 0.12
|     |-- Stayed 0.70  -> 0.28
|-- Support 0.60
      |-- Left 0.10    -> 0.06
      |-- Stayed 0.90  -> 0.54
```
Total leaving = 0.12 + 0.06 = 0.18. Given someone left, chance they were in Sales = 0.12 / 0.18.
**Excel / Python:**
```python
# First split: department
share_sales = 0.40
share_support = 0.60

# Second split: chance of leaving inside each department
leave_rate_sales = 0.30
leave_rate_support = 0.10

# Multiply along each branch that ends in "left"
sales_and_left = share_sales * leave_rate_sales
support_and_left = share_support * leave_rate_support

# Add the "left" branches: total chance of leaving
total_left = sales_and_left + support_and_left

# Reverse question: given someone left, were they in Sales?
sales_given_left = sales_and_left / total_left

print("Sales and left   =", round(sales_and_left, 3))
print("Support and left =", round(support_and_left, 3))
print("P(left)          =", round(total_left, 3))
print("P(Sales | left)  =", round(sales_given_left, 3))
```
Output:
```
Sales and left   = 0.12
Support and left = 0.06
P(left)          = 0.18
P(Sales | left)  = 0.667
```
Two thirds of all leavers come from Sales, though Sales is only 40% of staff.
**Likely follow-ups:** 1) *What if branches are not conditional?* Then they are independent and the same probabilities repeat on each branch. 2) *When is a tree better than the formula?* With 3 or more steps.
**Common mistakes:** Using unconditional probabilities on the second level; forgetting the second-level branches must add to 1.

### Q35 ⭐⭐ 🟡 Define sensitivity, specificity, false positive rate and false negative rate, and relate them to Bayes' theorem.
**Asked at:** commonly asked (no company-specific report found); the medical-test Bayes exercise is in all sources, but these four names are standard definitions, not company-specific.
**What the interviewer is checking:** Do you know the four rates and that the real "is a flag trustworthy?" answer also needs the base rate?
**Say this in the interview:** "Sensitivity is the share of real cases the test catches; specificity is the share of non-cases it correctly clears. False negative rate is 1 minus sensitivity; false positive rate is 1 minus specificity. Bayes' theorem combines them with how common the condition is to give the chance a flagged person is truly a case."
**Explain simply:**
- **Sensitivity (true positive rate):** flagged among real cases.
- **Specificity (true negative rate):** cleared among non-cases.
- **False negative rate:** missed real cases = 1 - sensitivity. **False positive rate:** wrongly flagged non-cases = 1 - specificity.
- Bayes then gives **precision** (positive predictive value): of all flagged people, how many are real. It depends on prevalence (the base rate).
**Formula in plain words:** Precision = real cases flagged / all flagged = (sensitivity x prevalence) / (sensitivity x prevalence + false positive rate x (1 - prevalence)).
**Worked example:** 1,000 employees, 10% truly have an issue. Test: sensitivity 90%, specificity 80%. Real cases caught 90, missed 10; non-cases wrongly flagged 180, cleared 720. Of 270 flagged, 90 are real: 33.3%.
**Excel / Python:**
```python
# 1,000 employees screened; 10% truly have the issue
people_with_issue = 100
people_without_issue = 900

# Screening test: catches 90% of real cases; clears 80% of non-cases
sensitivity = 0.90
specificity = 0.80

# The four boxes of the confusion table
true_positives = sensitivity * people_with_issue
false_negatives = people_with_issue - true_positives
true_negatives = specificity * people_without_issue
false_positives = people_without_issue - true_negatives

# Rates
false_negative_rate = false_negatives / people_with_issue
false_positive_rate = false_positives / people_without_issue

# Bayes: of all flagged people, how many are real? (precision)
probability_real_given_flag = true_positives / (true_positives + false_positives)

print("TP, FN, TN, FP:", true_positives, false_negatives, true_negatives, false_positives)
print("False negative rate:", false_negative_rate)
print("False positive rate:", false_positive_rate)
print("P(real | flagged):", round(probability_real_given_flag, 4))
```
Output:
```
TP, FN, TN, FP: 90.0 10.0 720.0 180.0
False negative rate: 0.1
False positive rate: 0.2
P(real | flagged): 0.3333
```
Even a test with good-looking rates gives only a one-in-three chance that a flagged person is real, because real cases are rare.
**Likely follow-ups:** 1) *Can you raise both sensitivity and specificity?* Usually trading one for the other via the cut-off. 2) *Which matters for fraud?* Depends on cost of misses versus false alarms.
**Common mistakes:** Confusing sensitivity (P(flag|real)) with precision (P(real|flag)); ignoring prevalence.

### Q36 ⭐⭐ 🟡 An attendance-fraud model flags 95% of real cases but also flags 3% of honest employees, and 2% of employees commit fraud. If an employee is flagged, what is the probability of fraud?
**Asked at:** HR-flavoured gap-fill on the standard Bayes structure (sources file); commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you apply Bayes with a low base rate, and do you grasp why a good-looking model still gives many false alarms?
**Say this in the interview:** "Flagged and fraud is 0.02 x 0.95 = 0.019. Flagged and honest is 0.98 x 0.03 = 0.0294. So the chance a flagged employee is a fraudster is 0.019 / 0.0484, about 39%. More than half of the flags are false alarms, because honest staff are so many."
**Explain simply:**
- Base rate: only 2% commit fraud, so honest employees vastly outnumber fraudsters.
- Even a 3% false-alarm rate on a big honest group creates many false flags.
- Always add both routes to "flagged" before dividing.
**Formula in plain words:** P(fraud | flagged) = (fraud rate x catch rate) divided by (that + honest rate x false-alarm rate).
**Worked example:** In 10,000 employees: 200 commit fraud, 190 are flagged; 9,800 are honest, 294 are flagged. Of 484 flags, 190 are real: 39.3%.
**Excel / Python:**
```python
# Base rate and model behaviour
fraud_rate = 0.02
flag_rate_if_fraud = 0.95
flag_rate_if_honest = 0.03

# Chance of "flagged AND fraud" and "flagged AND honest"
flagged_and_fraud = fraud_rate * flag_rate_if_fraud
flagged_and_honest = (1 - fraud_rate) * flag_rate_if_honest

# Total chance of being flagged
total_flagged = flagged_and_fraud + flagged_and_honest

# Bayes: chance of fraud given flagged
probability_fraud_given_flag = flagged_and_fraud / total_flagged

print("P(flagged and fraud)  =", round(flagged_and_fraud, 4))
print("P(flagged and honest) =", round(flagged_and_honest, 4))
print("P(fraud | flagged)    =", round(probability_fraud_given_flag, 4))
```
Output:
```
P(flagged and fraud)  = 0.019
P(flagged and honest) = 0.0294
P(fraud | flagged)    = 0.3926
```
About 39% of flagged employees are truly fraudulent, so each flag needs a manual review before action. Excel: `=0.02*0.95/(0.02*0.95+0.98*0.03)` returns 0.3926 (not run in Excel here).
**Likely follow-ups:** 1) *How to improve?* Lower the false-alarm rate or review only high-score flags. 2) *What if fraud were 20%?* About 89%: the base rate drives the answer.
**Common mistakes:** Answering 95%; ignoring the honest majority.

### Q37 ⭐⭐ 🟡 How do you check from a table whether two events are independent?
**Asked at:** commonly asked (no company-specific report found); independence appears in the question banks we found (btw.so list, InterviewBit).
**What the interviewer is checking:** Whether you can test independence with numbers, not just define it.
**Say this in the interview:** "Two events are independent if knowing one happened does not change the chance of the other. From a table I check one of three equal tests: P(A and B) equals P(A) times P(B), or P(A|B) equals P(A), or P(B|A) equals P(B). If any fails, they are dependent."
**Explain simply:**
- Independent means "one event tells me nothing about the other". Example: a coin toss and the weather.
- In a two-way table, work out the overall chance of A, then the chance of A inside the B group. If they match, the events are independent.
- In real data the match is almost never perfect, so a small gap can be chance; a statistical test (chi-square, a later topic) decides whether the gap is real.
**Formula in plain words:** The chance of both equals the product of the separate chances. P(A and B) = P(A) x P(B).
**Worked example:** 200 employees; 100 work from home (WFH); 40 left; 20 are WFH and left. Overall leaving rate is 20%, and among WFH employees it is also 20%, so leaving and WFH are independent. In the Sales table (80 in Sales, 24 Sales leavers, 40 leavers overall) the rate in Sales is 30% against 20% overall, so they are dependent.
**Excel / Python:**
```python
# Table 1: 200 employees, work-from-home (WFH) versus left
total_employees = 200
wfh_employees = 100
employees_who_left = 40
wfh_and_left = 20

# Probability of leaving overall
probability_left = employees_who_left / total_employees

# Probability of leaving among WFH employees only (conditional)
probability_left_given_wfh = wfh_and_left / wfh_employees

# Joint probability, and the product of the two separate probabilities
probability_wfh = wfh_employees / total_employees
probability_wfh_and_left = wfh_and_left / total_employees
product_of_separate = probability_wfh * probability_left

print("P(left)         =", probability_left)
print("P(left | WFH)   =", probability_left_given_wfh)
print("P(WFH and left) =", probability_wfh_and_left, "  P(WFH) x P(left) =", round(product_of_separate, 4))

# Table 2 (Q14 data): Sales 80, Sales leavers 24
sales_employees = 80
sales_who_left = 24
probability_left_given_sales = sales_who_left / sales_employees
probability_sales_and_left = sales_who_left / total_employees
product_for_sales = (sales_employees / total_employees) * probability_left

print("Sales: P(left | Sales) =", probability_left_given_sales, "  vs P(left) =", probability_left)
print("Sales: P(Sales and left) =", probability_sales_and_left, "  P(Sales) x P(left) =", round(product_for_sales, 4))
```
Output:
```
P(left)         = 0.2
P(left | WFH)   = 0.2
P(WFH and left) = 0.1   P(WFH) x P(left) = 0.1
Sales: P(left | Sales) = 0.3   vs P(left) = 0.2
Sales: P(Sales and left) = 0.12   P(Sales) x P(left) = 0.08
```
For WFH the numbers match, so independent. For Sales they do not match (0.12 against 0.08), so dependent.
**Likely follow-ups:** 1) *Can events be both independent and mutually exclusive?* Only if one has probability zero. 2) *Is a small gap enough to say dependent?* Not in sampled data; use a chi-square test.
**Common mistakes:** Comparing counts instead of proportions; declaring dependence from a tiny gap in a sample; mixing up "independent" with "mutually exclusive".

### Q38 ⭐⭐ 🟡 What is P(A or B) when A and B can occur together, and why do we subtract P(A and B)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand double counting, not just the formula.
**Say this in the interview:** "P(A or B) = P(A) + P(B) - P(A and B). When both can happen together, adding P(A) and P(B) counts the overlap twice, so I subtract it once."
**Explain simply:**
- Picture two overlapping circles. Adding the circles' areas counts the overlap region two times.
- "Or" here is inclusive: A, or B, or both.
- If A and B cannot happen together (mutually exclusive), the overlap is zero and you just add.
**Formula in plain words:** Chance of either = chance of A + chance of B - chance of both. P(A or B) = P(A) + P(B) - P(A and B).
**Worked example:** 200 employees; 80 have more than 5 years of service, 60 are managers, 30 are both. P(either) = 0.40 + 0.30 - 0.15 = 0.55, which is 110 people.
**Excel / Python:**
```python
# 200 employees: 80 have more than 5 years of service, 60 are managers, 30 are both
total_employees = 200
long_service = 80
managers = 60
both = 30

p_long_service = long_service / total_employees
p_manager = managers / total_employees
p_both = both / total_employees

# Adding both counts the "both" group twice, so subtract it once
p_either = p_long_service + p_manager - p_both
print("P(long service) =", p_long_service)
print("P(manager)      =", p_manager)
print("P(both)         =", p_both)
print("P(either)       =", round(p_either, 2))

# Check by counting directly: people in at least one group
people_in_either = long_service + managers - both
print("Headcount in either group =", people_in_either, "out of", total_employees, "=", people_in_either / total_employees)
```
Output:
```
P(long service) = 0.4
P(manager)      = 0.3
P(both)         = 0.15
P(either)       = 0.55
Headcount in either group = 110 out of 200 = 0.55
```
Without the subtraction we would get 0.70, which overstates the group by the 30 people counted twice.
**Likely follow-ups:** 1) *What if A and B are independent?* Then P(A and B) = P(A) x P(B). 2) *Three events?* Add singles, subtract pairs, add the triple (inclusion-exclusion).
**Common mistakes:** Forgetting to subtract the overlap; subtracting it even when events are mutually exclusive (it is just zero).

### Q39 ⭐⭐ 🟡 You roll a fair die 4 times. What is the probability of getting at least one six?
**Asked at:** commonly asked (no company-specific report found); a standard complement-rule exercise.
**What the interviewer is checking:** Whether you reach for the complement rule ("at least one" means 1 minus "none").
**Say this in the interview:** "At least one six is the opposite of no six at all. No six on one roll is 5/6; four independent rolls give (5/6)^4 = 0.482. So the answer is 1 - 0.482 = 0.518, about 51.8%."
**Explain simply:**
- "At least one" has many cases (one six, two sixes, and so on). The opposite case, "no sixes", is a single case.
- Rolls are independent, so we multiply the chances.
**Formula in plain words:** 1 minus the chance of failing every time. P(at least one) = 1 - (1 - p)^n.
**Worked example:** p = 1/6, n = 4: 1 - (5/6)^4 = 0.5177. It is slightly better than even odds.
**Excel / Python:**
```python
# Chance of no six on one roll
p_no_six_one_roll = 5 / 6

# Four independent rolls with no six at all
p_no_six_four_rolls = p_no_six_one_roll ** 4

# Complement: at least one six
p_at_least_one_six = 1 - p_no_six_four_rolls
print("P(no six in 4 rolls)       =", round(p_no_six_four_rolls, 4))
print("P(at least one six in 4)   =", round(p_at_least_one_six, 4))

# Check by simulation
import numpy as np
random_generator = np.random.default_rng(seed=1)
rolls = random_generator.integers(1, 7, size=(200000, 4))
has_a_six = (rolls == 6).any(axis=1)
print("Simulated                  =", round(has_a_six.mean(), 4))
```
Output:
```
P(no six in 4 rolls)       = 0.4823
P(at least one six in 4)   = 0.5177
Simulated                  = 0.5165
```
The simulation of 200,000 plays agrees with the exact answer. In Excel (any version): `=1-(5/6)^4` returns 0.5177 (not run in Excel here).
**Likely follow-ups:** 1) *Why not 4 x 1/6?* That gives 0.667, which double counts (see Q50). 2) *How many rolls for 90%?* Solve 1 - (5/6)^n >= 0.9, so n = 13.
**Common mistakes:** Multiplying n by p; computing only "exactly one six".

### Q40 ⭐⭐ 🟡 A game pays Rs 100 if a fair die shows 6 and costs Rs 20 to play. What is the expected profit, and should you play?
**Asked at:** commonly asked; a dice payout game appears in the PracHub question bank (2026, search snippet only, not read in full).
**What the interviewer is checking:** Whether you weigh each outcome by its probability and then decide using the sign of the result.
**Say this in the interview:** "Expected profit is probability-weighted profit. I win Rs 80 net with probability 1/6 and lose Rs 20 with probability 5/6. That is 80/6 - 100/6 = about minus Rs 3.33 per game, so on average I lose money and should not play."
**Explain simply:**
- Expected value (EV) is the long-run average result per play, not what happens in one play.
- Net profit if the die shows 6 is prize minus cost: 100 - 20 = 80.
- I assume the Rs 100 is the total paid out and the Rs 20 fee is lost either way. If the prize were Rs 100 on top of getting the fee back, the answer would change; state your assumption aloud.
**Formula in plain words:** Add up (outcome x its probability). E = sum of value x probability.
**Worked example:** E = (1/6)(80) + (5/6)(-20) = 13.33 - 16.67 = -3.33. Break-even prize would be Rs 120.
**Excel / Python:**
```python
# Game rules: prize if the die shows 6, fee to play, chance of each result
prize_if_six = 100
cost_to_play = 20
p_six = 1 / 6
p_not_six = 5 / 6

# Profit if we win is prize minus cost; if we lose we only lose the cost
profit_if_win = prize_if_six - cost_to_play
profit_if_lose = -cost_to_play

expected_profit = p_six * profit_if_win + p_not_six * profit_if_lose
print("Expected profit per game =", round(expected_profit, 2))

# Over 600 games, what do we expect in total?
print("Expected profit over 600 games =", round(600 * expected_profit, 2))
# Break-even prize: the prize that makes expected profit zero
break_even_prize = cost_to_play / p_six
print("Break-even prize =", break_even_prize)
```
Output:
```
Expected profit per game = -3.33
Expected profit over 600 games = -2000.0
Break-even prize = 120.0
```
On average you lose Rs 3.33 each play; over many plays the loss becomes predictable.
**Likely follow-ups:** 1) *Would you ever play?* Only for fun or if you value the thrill; the EV says no. 2) *Does one win disprove it?* No, EV is a long-run average.
**Common mistakes:** Forgetting to subtract the cost on wins; saying "EV is what I will get next game".

### Q41 ⭐⭐ 🟡 Two dice are rolled and the total is 8. What is the expected value of the first die?
**Asked at:** the quantt.co.uk expected-value guide lists a conditional-EV die problem of this kind (2026 prep guide for quant roles, search snippet only); not a reported DA question.
**What the interviewer is checking:** Whether you can restrict to the given condition and then average.
**Say this in the interview:** "Given total 8, only five equally likely pairs remain: (2,6), (3,5), (4,4), (5,3), (6,2). The first die takes values 2, 3, 4, 5, 6, whose average is 4."
**Explain simply:**
- "Given the total is 8" shrinks the sample space to the pairs that add to 8.
- Each of those 5 pairs was equally likely before, so they stay equally likely.
- Then take an ordinary average of the first die over them. This is a conditional expectation (see Q62).
**Formula in plain words:** Average of the first die across only the outcomes that satisfy the condition. E(first | total = 8).
**Worked example:** (2+3+4+5+6) / 5 = 20 / 5 = 4. It is the symmetric middle; the unconditional average of one die is 3.5.
**Excel / Python:**
```python
# List every pair (first die, second die) whose total is 8
pairs_with_total_8 = []
for first_die in range(1, 7):
    for second_die in range(1, 7):
        if first_die + second_die == 8:
            pairs_with_total_8.append((first_die, second_die))
print("Pairs:", pairs_with_total_8)

# Average of the first die across those equally likely pairs
first_die_values = [pair[0] for pair in pairs_with_total_8]
expected_first_die = sum(first_die_values) / len(first_die_values)
print("Expected first die given total 8 =", expected_first_die)
```
Output:
```
Pairs: [(2, 6), (3, 5), (4, 4), (5, 3), (6, 2)]
Expected first die given total 8 = 4.0
```
Knowing the total is 8 lifts the first die's average from 3.5 to 4 and rules out a first die of 1.
**Likely follow-ups:** 1) *And the expected value of the second die?* Also 4, by symmetry. 2) *What if the total is 12?* Only (6,6), so the first die is 6.
**Common mistakes:** Averaging over all 36 outcomes; counting (4,4) twice.

### Q42 ⭐⭐ 🟡 You have two children and at least one is a girl. What is the probability that both are girls, and why is the answer not 1/2?
**Asked at:** commonly asked (no company-specific report found); a classic conditional-probability puzzle.
**What the interviewer is checking:** Whether you list the sample space properly instead of trusting intuition.
**Say this in the interview:** "The four equally likely families are BB, BG, GB, GG. 'At least one girl' removes BB, leaving three, and only one of them is GG. So the answer is 1/3, not 1/2."
**Explain simply:**
- The intuitive 1/2 treats the information as "the other child is a girl" with a 50% chance. But we do not know which child is the girl.
- BG and GB are different families (older/younger) and both fit, which is why the girl-plus-boy case is twice as likely as two girls.
- Assumptions: each child is a boy or girl with equal chance, independently.
**Formula in plain words:** Chance of both girls given at least one girl = (chance of both girls) / (chance of at least one girl) = (1/4) / (3/4) = 1/3.
**Worked example:** Of 400 two-child families, about 100 are GG, 200 are one of each, 100 are BB. Of the 300 with a girl, 100 are GG: one in three.
**Excel / Python:**
```python
from itertools import product

# All four equally likely families (oldest child first): B = boy, G = girl
all_families = list(product("BG", repeat=2))
print("All families:", all_families)

# Keep only families with at least one girl
at_least_one_girl = [family for family in all_families if "G" in family]
print("At least one girl:", at_least_one_girl)

# Among those, how many have two girls?
two_girls = [family for family in at_least_one_girl if family == ("G", "G")]
print("P(both girls | at least one girl) =", len(two_girls), "/", len(at_least_one_girl))
```
Output:
```
All families: [('B', 'B'), ('B', 'G'), ('G', 'B'), ('G', 'G')]
At least one girl: [('B', 'G'), ('G', 'B'), ('G', 'G')]
P(both girls | at least one girl) = 1 / 3
```
Three families survive and only one is two girls. See Q52 for how the answer changes if you meet one specific child.
**Likely follow-ups:** 1) *What if the older child is a girl?* Then 1/2. 2) *What if you meet a girl at random?* Also 1/2 (Q52).
**Common mistakes:** Treating BG and GB as one case; ignoring how the information was obtained.

### Q43 ⭐⭐ 🟡 A spam filter marks 20% of emails as spam; the word "offer" appears in 50% of spam and 5% of non-spam emails. What is the probability that an email containing "offer" is spam?
**Asked at:** commonly asked (no company-specific report found); a Bayes problem in the standard prep lists.
**What the interviewer is checking:** Whether you can apply Bayes with the law of total probability in the denominator.
**Say this in the interview:** "Of every 10,000 emails, 2,000 are spam and 1,000 of those contain 'offer'; 8,000 are not spam and 400 of those contain 'offer'. So among 1,400 emails with 'offer', 1,000 are spam: 71.4%."
**Explain simply:**
- Reading the question: "20% marked as spam" is the starting share of spam (prior). Treat it as the true share of spam.
- The word "offer" is evidence. It is much more common in spam (50% against 5%), so it raises the spam chance from 20% to about 71%.
- The denominator is every email with "offer", spam or not.
**Formula in plain words:** Spam share among "offer" emails = (spam emails with offer) / (all emails with offer). P(S|O) = P(O|S) P(S) / [P(O|S) P(S) + P(O|not S) P(not S)].
**Worked example:** (0.5 x 0.2) / (0.5 x 0.2 + 0.05 x 0.8) = 0.10 / 0.14 = 0.714.
**Excel / Python:**
```python
# Given: share of spam, and how often the word "offer" appears in each type
p_spam = 0.20
p_not_spam = 1 - p_spam
p_offer_given_spam = 0.50
p_offer_given_not_spam = 0.05

# Total chance that a random email contains "offer"
p_offer = p_offer_given_spam * p_spam + p_offer_given_not_spam * p_not_spam

# Bayes: spam share among emails containing "offer"
p_spam_given_offer = p_offer_given_spam * p_spam / p_offer
print("P(offer)        =", round(p_offer, 4))
print("P(spam | offer) =", round(p_spam_given_offer, 4))

# Same thing as counts: 10,000 emails
emails = 10000
spam_with_offer = emails * p_spam * p_offer_given_spam
nonspam_with_offer = emails * p_not_spam * p_offer_given_not_spam
print("Spam with offer:", spam_with_offer, " Non-spam with offer:", nonspam_with_offer)
print("Share spam:", round(spam_with_offer / (spam_with_offer + nonspam_with_offer), 4))
```
Output:
```
P(offer)        = 0.14
P(spam | offer) = 0.7143
Spam with offer: 1000.0  Non-spam with offer: 400.0
Share spam: 0.7143
```
The counts match the head-count story above.
**Likely follow-ups:** 1) *Why not 50%?* That is P(offer | spam), the reverse question (Q11). 2) *What if spam were rarer, 2%?* The answer falls to about 17%.
**Common mistakes:** Answering 50%; leaving out the non-spam emails in the denominator.

### Q44 ⭐⭐ 🟡 What is the prosecutor's fallacy, and how does it connect to confusing P(A|B) with P(B|A)?
**Asked at:** commonly asked (no company-specific report found); it appears as a conditional-probability trap in general prep material.
**What the interviewer is checking:** Whether you can spot P(evidence | innocent) being misread as P(innocent | evidence).
**Say this in the interview:** "It is the mistake of saying 'the chance an innocent person matches this evidence is tiny, so the chance this matching person is innocent is tiny'. Those are two different probabilities, P(match | innocent) and P(innocent | match), and they can differ enormously once you account for how many people were checked."
**Explain simply:**
- A tiny false-match rate sounds convincing, but if you search a huge group, many innocent people will match by pure chance.
- The right question is: among everyone who matches, what share is actually guilty?
- Same trap in HR: an attendance-fraud model with a 1-in-10,000 false-flag rate, run across a million records, still flags about 100 honest people.
**Formula in plain words:** Chance of guilt given a match = guilty matches / all matches. P(guilty | match) = P(match | guilty) P(guilty) / P(match).
**Worked example:** Population 1,000,000, one culprit who always matches, false match 1 in 10,000. About 100 innocent people match plus the culprit, so P(guilty | match) = 1/101 = about 1%, not 99.99%.
**Excel / Python:**
```python
# A fraud check "matches" 1 in 10,000 honest people by chance.
population = 1_000_000
chance_match_if_innocent = 1 / 10000

# One real culprit always matches
guilty_people = 1
innocent_people = population - guilty_people

# Expected number of innocent people who also match by pure chance
innocent_matches = innocent_people * chance_match_if_innocent
total_matches = innocent_matches + guilty_people

p_guilty_given_match = guilty_people / total_matches
print("Innocent people who match by chance:", round(innocent_matches, 1))
print("P(match | innocent)  =", chance_match_if_innocent)
print("P(guilty | match)    =", round(p_guilty_given_match, 4))
```
Output:
```
Innocent people who match by chance: 100.0
P(match | innocent)  = 0.0001
P(guilty | match)    = 0.0099
```
A one-in-10,000 false-match rate still leaves only about a 1% chance that a given matched person is guilty, because there are no other clues pointing at them.
**Likely follow-ups:** 1) *What changes the answer?* Other evidence that narrows the suspect pool (higher prior). 2) *Link to Bayes?* It is the missing prior and denominator.
**Common mistakes:** Quoting the false-positive rate as if it were the error rate among flagged cases.

### Q45 ⭐⭐ 🟡 How many people must be in a room before the chance of two sharing a birthday exceeds 50%, and why is the answer surprising?
**Asked at:** commonly asked (no company-specific report found); a classic puzzle in prep lists (see Q68 for the step-by-step version).
**What the interviewer is checking:** Whether you use the complement and know the surprising result.
**Say this in the interview:** "23 people. The chance of at least one shared birthday passes 50% at 23, giving 50.7%. It feels too small because we think of one person matching me, but with 23 people there are 253 pairs, and any pair can match."
**Explain simply:**
- Assume 365 equally likely birthdays and ignore leap years.
- Easier to compute "everyone has a different birthday" and subtract from 1.
- The surprise: people compare 23 with 365, but the number of pairs grows roughly with the square of the group size.
**Formula in plain words:** Chance all different = 365/365 x 364/365 x 363/365 and so on. Chance of a match = 1 minus that.
**Worked example:** With 23 people the chance of no match is 0.4927, so a match is 0.5073.
**Excel / Python:**
```python
# Probability that everyone in a room has a different birthday (365 days, ignore leap years)
people_in_room = 0
p_all_different = 1.0
while True:
    people_in_room = people_in_room + 1
    # The next person must avoid the birthdays already taken
    days_still_free = 365 - (people_in_room - 1)
    p_all_different = p_all_different * days_still_free / 365
    p_shared = 1 - p_all_different
    if people_in_room in (10, 20, 22, 23, 30, 50, 70):
        print(people_in_room, "people: P(shared) =", round(p_shared, 4))
    if people_in_room == 70:
        break

# First room size where the chance passes 50%
people_in_room = 0
p_all_different = 1.0
while 1 - p_all_different <= 0.5:
    people_in_room = people_in_room + 1
    p_all_different = p_all_different * (365 - (people_in_room - 1)) / 365
print("First size above 50%:", people_in_room, "->", round(1 - p_all_different, 4))
print("Number of pairs among 23 people:", 23 * 22 // 2)
```
Output:
```
10 people: P(shared) = 0.1169
20 people: P(shared) = 0.4114
22 people: P(shared) = 0.4757
23 people: P(shared) = 0.5073
30 people: P(shared) = 0.7063
50 people: P(shared) = 0.9704
70 people: P(shared) = 0.9992
First size above 50%: 23 -> 0.5073
Number of pairs among 23 people: 253
```
At 22 people it is still below half; 23 tips it over. By 70 people a shared birthday is almost certain.
**Likely follow-ups:** 1) *What if birthdays are not uniform?* Matches become more likely, so fewer than 23 are needed. 2) *Why use the complement?* "At least one match" has too many cases.
**Common mistakes:** Answering 183 (half of 365); counting only matches with yourself.

### Q46 ⭐⭐ 🟡 What is the expected number of tosses of a fair coin needed to get the first head?
**Asked at:** expected flips until heads appears in Glassdoor quant-analyst question pages (quant roles, not DA; search snippet only).
**What the interviewer is checking:** Whether you can set up an expectation, ideally with the quick "first toss" argument.
**Say this in the interview:** "The answer is 2. With probability 1/2 I am done in one toss; otherwise I have used one toss and am back at the start. So E = 1 + (1/2) x E, which gives E = 2. It is 1 divided by p."
**Explain simply:**
- Always at least one toss is needed (the "1").
- Half the time that first toss is a tail, and the process restarts, adding E again on average.
- For a coin with head probability p, the expected tosses are 1/p. A 20% offer-acceptance rate means on average 5 candidates per acceptance.
**Formula in plain words:** Expected tosses = 1 / chance of success on each toss. E = 1/p.
**Worked example:** p = 0.5 gives 2 tosses; the sum 1(1/2) + 2(1/4) + 3(1/8) + ... also converges to 2.
**Excel / Python:**
```python
# Exact: sum of (number of tosses x probability) = 1(1/2) + 2(1/4) + 3(1/8) + ...
expected_tosses = 0.0
for tosses in range(1, 60):
    probability_first_head_on_this_toss = 0.5 ** tosses
    expected_tosses = expected_tosses + tosses * probability_first_head_on_this_toss
print("Series sum =", round(expected_tosses, 6))

# Simulation: toss until the first head, 100,000 times
import numpy as np
random_generator = np.random.default_rng(seed=2)
tosses_needed = []
for game in range(100000):
    tosses = 1
    while random_generator.random() >= 0.5:   # a value below 0.5 counts as heads
        tosses = tosses + 1
    tosses_needed.append(tosses)
print("Simulated average =", round(np.mean(tosses_needed), 3))
```
Output:
```
Series sum = 2.0
Simulated average = 2.002
```
Both the exact sum and the simulation give 2.
**Likely follow-ups:** 1) *For a die and a six?* 6 rolls on average. 2) *Two heads in a row?* 6 (Q65).
**Common mistakes:** Answering 1; forgetting that the number of tosses has no fixed maximum.

### Q47 ⭐⭐ 🟡 How do you calculate the expected value of a business decision, for example a discount offer with uncertain uptake?
**Asked at:** commonly asked (no company-specific report found); a business-case style question.
**What the interviewer is checking:** Whether you can turn uncertain outcomes into one decision number and state your assumptions.
**Say this in the interview:** "List the scenarios, give each a probability that adds to 100%, work out the profit in each, multiply and add. I compare that expected profit with the no-offer profit. I also check how sensitive it is to the probabilities."
**Explain simply:**
- Step 1: define the decision and the baseline (do nothing).
- Step 2: list scenarios and their probabilities (must sum to 1).
- Step 3: profit per scenario, then probability-weighted total.
- Step 4: compare with the baseline and look at the worst case too, because EV hides risk.
**Formula in plain words:** Expected profit = sum of (scenario probability x scenario profit).
**Worked example (illustrative numbers, not real data):** Without an offer, 100 customers buy at Rs 300 margin = Rs 30,000. A Rs 50 discount applies to every sale. Uptake: 20% chance of 110 buyers, 50% chance of 130, 30% chance of 150. Margin per sale becomes Rs 250. Expected profit = Rs 33,000, a gain of Rs 3,000.
**Excel / Python:**
```python
# Assumed numbers (illustrative): normal buyers, profit per sale, discount size
baseline_buyers = 100
margin_per_sale = 300
discount_per_sale = 50

# Profit with no offer
profit_without_offer = baseline_buyers * margin_per_sale

# Uncertain uptake: (probability, total buyers if we run the offer)
scenarios = [
    ("low uptake",    0.20, 110),
    ("medium uptake", 0.50, 130),
    ("high uptake",   0.30, 150),
]

expected_profit_with_offer = 0
for name, probability, total_buyers in scenarios:
    # Every sale now earns the margin minus the discount
    profit = total_buyers * (margin_per_sale - discount_per_sale)
    print(name, "profit =", profit)
    expected_profit_with_offer = expected_profit_with_offer + probability * profit

print("Profit without offer      =", profit_without_offer)
print("Expected profit with offer =", expected_profit_with_offer)
print("Expected gain from offer   =", expected_profit_with_offer - profit_without_offer)
```
Output:
```
low uptake profit = 27500
medium uptake profit = 32500
high uptake profit = 37500
Profit without offer      = 30000
Expected profit with offer = 33000.0
Expected gain from offer   = 3000.0
```
On average the offer adds Rs 3,000, but in the low-uptake case it loses Rs 2,500, so the decision depends on how much risk the business accepts.
**Likely follow-ups:** 1) *Where do the probabilities come from?* Past campaigns or a small pilot test. 2) *Is a positive EV enough?* No; check the downside and the cost of being wrong.
**Common mistakes:** Probabilities that do not add to 1; ignoring that the discount also applies to customers who would have bought anyway.

### Q48 ⭐⭐ 🟡 If a coin is tossed 3 times, what is the probability of exactly two heads?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can count outcomes cleanly.
**Say this in the interview:** "There are 8 equally likely outcomes. Exactly two heads happens in HHT, HTH and THH, which is 3 outcomes. So the probability is 3/8 = 0.375."
**Explain simply:**
- Three tosses give 2 x 2 x 2 = 8 outcomes, each equally likely.
- Count the ones with exactly two heads: the single tail can sit in 3 positions.
- The general shortcut is the binomial formula (Book 5 Part 3).
**Formula in plain words:** (Number of ways to choose which tosses are heads) x (chance of that pattern). P = C(3,2) x (1/2)^3 = 3 x 1/8.
**Worked example:** 3/8 = 37.5%; the same logic gives 3/8 for exactly one head and 1/8 each for zero or three heads, totalling 1.
**Excel / Python:**
```python
from itertools import product

# All 8 equally likely outcomes of three tosses
all_outcomes = list(product("HT", repeat=3))
outcomes_with_two_heads = [outcome for outcome in all_outcomes if outcome.count("H") == 2]
print("Outcomes with exactly two heads:", ["".join(o) for o in outcomes_with_two_heads])
print("Probability =", len(outcomes_with_two_heads), "/", len(all_outcomes), "=", len(outcomes_with_two_heads) / len(all_outcomes))

# Check with the binomial formula: 3 ways x (1/2)^3
from math import comb
print("Binomial formula =", comb(3, 2) * 0.5 ** 3)
```
Output:
```
Outcomes with exactly two heads: ['HHT', 'HTH', 'THH']
Probability = 3 / 8 = 0.375
Binomial formula = 0.375
```
Excel (2010+): `=BINOM.DIST(2,3,0.5,FALSE)` returns 0.375 (not run in Excel here).
**Likely follow-ups:** 1) *At least two heads?* 3/8 + 1/8 = 1/2. 2) *With a biased coin?* Replace 1/2 with p and 1-p.
**Common mistakes:** Counting only HHT; answering 1/3 by treating "0, 1, 2, 3 heads" as equally likely.

### Q49 ⭐⭐ 🟡 A test is repeated: a person tests positive twice in two independent tests. How does the probability of disease update?
**Asked at:** commonly asked (no company-specific report found); an extension of the standard medical-test Bayes exercise.
**What the interviewer is checking:** Whether you know that yesterday's posterior becomes today's prior.
**Say this in the interview:** "Using the standard numbers (1% prevalence, 99% sensitivity and specificity), one positive takes the chance of disease from 1% to 50%. I use 50% as the new prior, update again and get 99% after the second positive. That assumes the tests are independent given the true state."
**Explain simply:**
- Each update uses the previous result as the starting belief.
- A faster way: odds. Each positive multiplies the odds of disease by the likelihood ratio, sensitivity / false positive rate = 0.99 / 0.01 = 99.
- Starting odds are 1 to 99; after one positive 1 to 1; after two, 99 to 1.
- Independence is the key assumption: if both tests share the same flaw (same lab error), the second test adds less.
**Formula in plain words:** New odds = old odds x likelihood ratio. Likelihood ratio = chance of a positive if diseased / chance of a positive if healthy.
**Worked example:** 1% -> 50% -> 99%. Using 1,000,000 people: 10,000 have it; 9,900 test positive; of 990,000 healthy, 9,900 test positive. Half of positives are real (50%). Of those 19,800, retest: 9,801 real positives versus 99 false, so 99%.
**Excel / Python:**
```python
# Standard numbers: 1% have the disease; the test is 99% right in both directions
prevalence = 0.01
sensitivity = 0.99   # P(positive | disease)
specificity = 0.99   # P(negative | no disease)
false_positive_rate = 1 - specificity

belief = prevalence   # starting belief before any test
for test_number in (1, 2):
    # Chance of a positive result overall, given the current belief
    p_positive = sensitivity * belief + false_positive_rate * (1 - belief)
    # Bayes update: the posterior becomes the next prior
    belief = sensitivity * belief / p_positive
    print("After positive test", test_number, ": P(disease) =", round(belief, 4))

# Odds form: each positive multiplies the odds by 99
odds = prevalence / (1 - prevalence)
likelihood_ratio = sensitivity / false_positive_rate
odds_after_two = odds * likelihood_ratio ** 2
print("Odds form check:", round(odds_after_two / (1 + odds_after_two), 4))
```
Output:
```
After positive test 1 : P(disease) = 0.5
After positive test 2 : P(disease) = 0.99
Odds form check: 0.99
```
Two independent positives move us from "unlikely" to "very likely".
**Likely follow-ups:** 1) *What if the second test is negative?* The odds are multiplied by (0.01/0.99), taking it back to about 1%. 2) *Why do doctors retest?* Because one positive on a rare condition is weak evidence.
**Common mistakes:** Starting the second update from 1% again; ignoring dependence between repeated tests.

### Q50 ⭐⭐ 🟡 Is the probability of at least one success in n independent trials equal to n times p? Explain the mistake.
**Asked at:** commonly asked (no company-specific report found); a common beginner trap.
**What the interviewer is checking:** Whether you know why adding probabilities fails when events overlap.
**Say this in the interview:** "No. n times p adds the chances as if the events could not overlap, so it double counts cases where several trials succeed. It can even exceed 1. The correct value is 1 - (1 - p)^n."
**Explain simply:**
- Adding works only for mutually exclusive events (Q38). Separate trials can all succeed together, so they overlap.
- A probability can never be above 1, which proves n x p is wrong once n x p > 1.
- n x p is a good rough approximation only when n x p is small (rare events).
**Formula in plain words:** At least one success = 1 - chance every trial fails. P = 1 - (1 - p)^n.
**Worked example:** 5 shortlisted candidates, each accepts with 20%: n x p = 100%, which is clearly absurd; the correct answer is 67.2%. With 10 candidates, n x p = 200% against a correct 89.3%.
**Excel / Python:**
```python
# Each of 5 independent candidates accepts with probability 20%
chance_each_accepts = 0.20
number_of_trials = 5

# Wrong shortcut
wrong_answer = number_of_trials * chance_each_accepts
# Correct: 1 minus the chance that all trials fail
correct_answer = 1 - (1 - chance_each_accepts) ** number_of_trials
print("n x p (wrong)   =", wrong_answer)
print("1 - (1-p)^n     =", round(correct_answer, 4))

# With 10 trials, n x p would exceed 1, which is impossible
print("n=10: n x p =", 10 * chance_each_accepts, " correct =", round(1 - (1 - chance_each_accepts) ** 10, 4))
```
Output:
```
n x p (wrong)   = 1.0
1 - (1-p)^n     = 0.6723
n=10: n x p = 2.0  correct = 0.8926
```
The shortcut says 100% and 200%; the true chances are 67% and 89%.
**Likely follow-ups:** 1) *When is n x p close enough?* When p is tiny, such as p = 0.001 and n = 10 (0.010 against 0.00995). 2) *What about dependent trials?* You need conditional probabilities.
**Common mistakes:** Adding probabilities of overlapping events; forgetting independence is needed for the (1-p)^n step.

### Q51 ⭐⭐ 🟡 Three attrition risk teams have attrition rates 10%, 15% and 25% and sizes 100, 200 and 100. What is the probability that a randomly picked leaver came from the third team?
**Asked at:** commonly asked (no company-specific report found); an HR-flavoured gap-fill of the standard "which machine" Bayes problem.
**What the interviewer is checking:** Whether you use Bayes with a weighted denominator (law of total probability).
**Say this in the interview:** "Count the expected leavers per team: 10, 30 and 25, total 65. The third team supplies 25 of them, so the answer is 25/65 = 38.5%, even though it holds only 25% of employees."
**Explain simply:**
- We are flipping the question: given that someone left, which team were they from? That is P(team | left), not P(left | team).
- Leavers per team = team size x attrition rate.
- Team 3 has a quarter of staff but 38% of leavers because its rate is highest.
**Formula in plain words:** Share of leavers from team 3 = leavers in team 3 / all leavers. P(T3 | L) = P(L | T3) P(T3) / sum over teams of P(L | T) P(T).
**Worked example:** (0.25 x 0.25) / (0.10 x 0.25 + 0.15 x 0.50 + 0.25 x 0.25) = 0.0625 / 0.1625 = 0.3846.
**Excel / Python:**
```python
# Team headcounts and yearly attrition rates
team_sizes = {"Team 1": 100, "Team 2": 200, "Team 3": 100}
attrition_rates = {"Team 1": 0.10, "Team 2": 0.15, "Team 3": 0.25}

# Expected number of leavers in each team = size x rate
leavers_by_team = {}
for team in team_sizes:
    leavers_by_team[team] = team_sizes[team] * attrition_rates[team]
print("Leavers by team:", leavers_by_team)

total_leavers = sum(leavers_by_team.values())
print("Total leavers:", total_leavers)

# Bayes: share of all leavers that came from Team 3
p_team3_given_left = leavers_by_team["Team 3"] / total_leavers
print("P(Team 3 | left) =", round(p_team3_given_left, 4))
print("P(Team 3) before knowing they left =", 100 / 400)
```
Output:
```
Leavers by team: {'Team 1': 10.0, 'Team 2': 30.0, 'Team 3': 25.0}
Total leavers: 65.0
P(Team 3 | left) = 0.3846
P(Team 3) before knowing they left = 0.25
```
Learning that the person left raises the chance they are from Team 3 from 25% to 38%.
**Likely follow-ups:** 1) *What if Team 2 were smaller?* Team 3's share would rise. 2) *Link to Q19?* Same structure with two machines.
**Common mistakes:** Answering 25% (the headcount share) or 25/(10+15+25) using rates alone, which ignores team size.

### Q52 ⭐⭐ 🔴 A family has two children; you meet one child and it is a boy. Does the probability that the other is a boy change versus "at least one is a boy"? Explain.
**Asked at:** commonly asked (no company-specific report found); a classic puzzle extending Q42.
**What the interviewer is checking:** Whether you see that how the information arrives changes the answer.
**Say this in the interview:** "Yes, it can. If I only learn 'at least one child is a boy', the answer is 1/3. If I meet one child chosen at random and it is a boy, the other child is independent, so the answer is 1/2. The two statements carry different information."
**Explain simply:**
- Case A (at least one boy): families BB, BG, GB remain, equally likely; one of three is BB, so 1/3.
- Case B (a randomly met child is a boy): the other child's sex has nothing to do with the one you met, so 1/2. Another way to see it: BB families make you meet a boy with certainty, BG/GB families only half the time, so BB's weight is 1 against 2 x 0.5 = 1, an even split.
- Honest caveat: the puzzle is ambiguous as worded. Say which reading you adopt. With "meet one child", 1/2 is the sensible reading.
**Formula in plain words:** Case B: P(BB | met a boy) = (1/4 x 1) / (1/4 x 1 + 2/4 x 1/2) = 1/2.
**Worked example:** Of 400 families: 100 BB, 200 mixed, 100 GG. Meeting a random child, we meet a boy in 100 (BB) + 100 (half of mixed) = 200 cases; in 100 of them the other is a boy: 1/2.
**Excel / Python:**
```python
from itertools import product
import numpy as np

# Case A: "at least one is a boy" (we learn only that, nothing about which child)
all_families = list(product("BG", repeat=2))
at_least_one_boy = [family for family in all_families if "B" in family]
both_boys = [family for family in at_least_one_boy if family == ("B", "B")]
print("Case A: P(both boys | at least one boy) =", len(both_boys), "/", len(at_least_one_boy))

# Case B: we meet one randomly chosen child and it is a boy
random_generator = np.random.default_rng(seed=3)
number_of_families = 400000
children = random_generator.integers(0, 2, size=(number_of_families, 2))  # 1 = boy, 0 = girl
child_we_meet = random_generator.integers(0, 2, size=number_of_families)  # which child (0 or 1)
met_child_is_boy = children[np.arange(number_of_families), child_we_meet] == 1
other_child = 1 - child_we_meet
other_is_boy = children[np.arange(number_of_families), other_child] == 1
print("Case B (simulated): P(other is boy | met child is boy) =", round(other_is_boy[met_child_is_boy].mean(), 3))
```
Output:
```
Case A: P(both boys | at least one boy) = 1 / 3
Case B (simulated): P(other is boy | met child is boy) = 0.499
```
The same fact, "there is a boy", gives 1/3 or 1/2 depending on how we learned it.
**Likely follow-ups:** 1) *Why does it matter in data work?* How a sample was selected changes the probabilities. 2) *And "the older child is a boy"?* 1/2.
**Common mistakes:** Assuming both cases give 1/3; not stating the selection process.

### Q53 ⭐⭐ 🔴 In a Monty Hall game with 100 doors where the host opens 98 empty doors, what is the probability of winning by switching, and what does it show?
**Asked at:** commonly asked (no company-specific report found); the usual way to make Monty Hall intuitive.
**What the interviewer is checking:** Whether you understand why switching wins, not only the 3-door answer.
**Say this in the interview:** "Switching wins with probability 99/100. My first pick is right only 1% of the time, and that does not change when the host opens 98 empty doors. The other 99% is concentrated on the one remaining door."
**Explain simply:**
- Assumptions: the host knows where the car is, always opens empty doors other than my pick, and always offers a switch.
- My first pick has 1/100 chance. The group of the other 99 doors holds 99/100, and the host's 98 reveals squeeze all of it onto one door.
- It shows that new information from a host who knows the answer does not change my first pick's odds, but it does sharpen the rest. With 3 doors the same logic gives 2/3.
**Formula in plain words:** Switching wins whenever my first pick was wrong. P(win by switching) = 1 - 1/N = 99/100.
**Worked example:** Play 100 times: stay wins about 1 time, switch wins about 99 times.
**Excel / Python:**
```python
import numpy as np
random_generator = np.random.default_rng(seed=4)

number_of_games = 200000
number_of_doors = 100

# Car position and our first pick, both uniformly random
car_door = random_generator.integers(0, number_of_doors, size=number_of_games)
first_pick = random_generator.integers(0, number_of_doors, size=number_of_games)

# Host opens 98 empty doors, leaving our pick and one other door.
# Switching wins exactly when our first pick was wrong.
switch_wins = (first_pick != car_door)
stay_wins = (first_pick == car_door)
print("Exact: stay =", 1 / 100, " switch =", 99 / 100)
print("Simulated stay   =", round(stay_wins.mean(), 4))
print("Simulated switch =", round(switch_wins.mean(), 4))
```
Output:
```
Exact: stay = 0.01  switch = 0.99
Simulated stay   = 0.0101
Simulated switch = 0.9899
```
The simulation uses the fact that the host's remaining door must be the car whenever my pick was wrong. Staying wins about 1% of the time and switching about 99%.
**Likely follow-ups:** 1) *What if the host opens a door at random and happens to show a goat?* Then switching and staying are both 1/2 (the host's knowledge is the key). 2) *Why is 3 doors less obvious?* 2/3 against 1/3 feels like a coin flip.
**Common mistakes:** Saying the two remaining doors are 50-50; ignoring that the host knows where the car is.

### Q54 ⭐ 🟢 What is the difference between frequentist and Bayesian probability?
**Asked at:** commonly asked (no company-specific report found); a conceptual question (no report found of where it is asked).
**What the interviewer is checking:** Whether you can explain the two viewpoints without jargon.
**Say this in the interview:** "A frequentist says probability is the long-run frequency of an event over many repeats, and parameters like the true attrition rate are fixed but unknown. A Bayesian says probability measures belief, and updates a prior belief with data to get a posterior. Both give similar answers with lots of data."
**Explain simply:**
- Frequentist: "The true attrition rate is one fixed number; my best estimate from this sample is 30%." The sample is what is random; the true rate is not.
- Bayesian: "Before the data I believed about 20%; after seeing 12 of 40 left I now believe about 28%, with a range." The belief is updated and described by a distribution.
- Bayesian needs a prior (a starting belief), which is useful when data are small but is debated because it adds judgement.
- A 95% confidence interval (frequentist) and a 95% credible interval (Bayesian) look alike but are interpreted differently.
**Formula in plain words:** Posterior belief is proportional to prior belief times the likelihood of the data. P(parameter | data) is proportional to P(data | parameter) x P(parameter).
**Worked example:** Of 40 sampled employees, 12 left. Frequentist estimate: 12/40 = 30%. Bayesian with a prior of "2 leavers in 10 past cases" (Beta(2, 8)): posterior mean = 14/50 = 28%, pulled slightly toward the prior.
**Excel / Python:**
```python
from scipy import stats

employees_checked = 40
leavers_seen = 12

# Frequentist: just the observed proportion
observed_rate = leavers_seen / employees_checked
print("Frequentist estimate of attrition rate =", observed_rate)

# Bayesian: prior belief of about 20% (like 2 leavers in 10 past employees) = Beta(2, 8)
prior_leavers, prior_stayers = 2, 8
posterior_leavers = prior_leavers + leavers_seen
posterior_stayers = prior_stayers + (employees_checked - leavers_seen)
posterior_mean = posterior_leavers / (posterior_leavers + posterior_stayers)
print("Bayesian posterior mean                =", round(posterior_mean, 4))

# 95% credible interval: range holding 95% of the updated belief
lower, upper = stats.beta.ppf([0.025, 0.975], posterior_leavers, posterior_stayers)
print("95% credible interval =", round(lower, 3), "to", round(upper, 3))
```
Output:
```
Frequentist estimate of attrition rate = 0.3
Bayesian posterior mean                = 0.28
95% credible interval = 0.166 to 0.411
```
The Bayesian estimate sits between the prior (20%) and the data (30%); with more data the prior's pull fades. "Beta" is just a flexible curve for a rate between 0 and 1.
**Likely follow-ups:** 1) *Which is better?* Neither always; Bayesian helps with small data and prior knowledge, frequentist is standard in A/B testing. 2) *Is Bayes' theorem Bayesian only?* No, frequentists use it too (e.g. medical tests); the debate is about treating parameters as uncertain.
**Common mistakes:** Saying the Bayesian approach is "guessing"; reading a 95% confidence interval as "95% chance the true value is inside".

### Q55 ⭐ 🟢 What are prior, likelihood and posterior in Bayes' theorem?
**Asked at:** Bayes and conditional probability were reported in a Tiger Analytics technical round (GfG candidate report, page updated Jul 2025, interview year unknown); otherwise commonly asked, no other company-specific report found.
**What the interviewer is checking:** Can you name the three parts of a Bayes update and say which one is your starting belief?
**Say this in the interview:** "The prior is what I believed before seeing the evidence. The likelihood is how likely that evidence is under each possible explanation. The posterior is my updated belief after combining the two."
**Explain simply:**
- **Prior:** your starting probability, for example the 10% of employees who leave in a year.
- **Likelihood:** the chance of seeing the evidence if a given explanation is true, for example how often leavers had no promotion in 3 years.
- **Posterior:** the new probability after the evidence. It becomes the prior for the next update.
- The likelihood is *not* the posterior: it answers "how likely is this evidence if the employee leaves?", not "how likely is leaving given this evidence?" (Q11).
**Formula in plain words:** posterior = prior x likelihood, divided by the total chance of the evidence. P(H|E) = P(H) x P(E|H) / P(E).
**Worked example:** 10% of employees leave. 60% of leavers had no promotion in 3 years, against 30% of stayers. For an employee with no promotion: leave share = 0.10 x 0.60 = 0.06; stay share = 0.90 x 0.30 = 0.27; posterior = 0.06 / (0.06 + 0.27) = 18.2%. The evidence nearly doubled the risk from 10%.
**Excel / Python:**
```python
# Prior: share of employees who leave in a year (before any evidence)
prior_leave = 0.10
prior_stay = 1 - prior_leave

# Likelihood: how often the evidence "no promotion in 3 years" shows up in each group
no_promotion_given_leave = 0.60
no_promotion_given_stay = 0.30

# Multiply prior by likelihood for each group
leave_and_no_promotion = prior_leave * no_promotion_given_leave
stay_and_no_promotion = prior_stay * no_promotion_given_stay

# Posterior: leave share among everyone showing the evidence
posterior_leave = leave_and_no_promotion / (leave_and_no_promotion + stay_and_no_promotion)

print("Prior P(leave) =", prior_leave)
print("Posterior P(leave | no promotion) =", round(posterior_leave, 4))
```
```text
Prior P(leave) = 0.1
Posterior P(leave | no promotion) = 0.1818
```
The 10% starting risk rises to about 18% once we know the employee has had no promotion.
**Likely follow-ups:** 1) *Does the posterior ever become the next prior?* Yes, that is how repeated updating works (Q60). 2) *What if the prior is wrong?* The posterior inherits the error, so state it as an assumption.
**Common mistakes:** Treating the likelihood as the posterior (confusing P(E|H) with P(H|E)); ignoring the prior when it is small.

### Q56 ⭐ 🟢 What does "at random" and "equally likely" mean in a probability question, and why do interviewers state it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that probability rules depend on the stated assumptions about how outcomes are chosen?
**Say this in the interview:** "'At random' means every item had the same chance of being picked, and 'equally likely' means each listed outcome has the same probability. Without that statement, the counting method (favourable over total) is not valid."
**Explain simply:**
- **At random:** the selection is fair, like pulling a name from a hat. It is not the manager's favourite or the first row of a sheet.
- **Equally likely:** each outcome in the list has the same probability. Interviewers say it so you can count outcomes.
- The trap is counting outcomes that are *not* equally likely. The 11 possible sums of two dice are not equally likely, but the 36 (die 1, die 2) pairs are.
- If the statement is missing, say your assumption aloud ("I assume a fair die and independent rolls").
**Formula in plain words:** Only when all outcomes are equally likely: probability = favourable outcomes / total outcomes.
**Worked example:** Picking one employee at random from 200 gives each person a 1/200 chance, so P(Sales) = 80/200 = 0.4 when 80 are in Sales. For two dice, listing the 36 equal pairs shows a sum of 7 has 6 pairs (1/6), not 1/11.
**Excel / Python:**
```python
# List every (die 1, die 2) pair: these 36 pairs ARE equally likely
sum_counts = {}
for first_die in range(1, 7):
    for second_die in range(1, 7):
        total = first_die + second_die
        sum_counts[total] = sum_counts.get(total, 0) + 1

# The 11 possible sums are NOT equally likely
for total in sorted(sum_counts):
    print("sum", total, ":", sum_counts[total], "of 36 pairs =", round(sum_counts[total] / 36, 4))

# Wrong answer if we wrongly treat the 11 sums as equally likely
print("Wrong P(sum = 7) =", round(1 / 11, 4))
print("Right P(sum = 7) =", round(sum_counts[7] / 36, 4))
```
```text
sum 2 : 1 of 36 pairs = 0.0278
sum 3 : 2 of 36 pairs = 0.0556
sum 4 : 3 of 36 pairs = 0.0833
sum 5 : 4 of 36 pairs = 0.1111
sum 6 : 5 of 36 pairs = 0.1389
sum 7 : 6 of 36 pairs = 0.1667
sum 8 : 5 of 36 pairs = 0.1389
sum 9 : 4 of 36 pairs = 0.1111
sum 10 : 3 of 36 pairs = 0.0833
sum 11 : 2 of 36 pairs = 0.0556
sum 12 : 1 of 36 pairs = 0.0278
Wrong P(sum = 7) = 0.0909
Right P(sum = 7) = 0.1667
```
Sum 7 is the most likely total because it has 6 pairs; sums 2 and 12 have 1 pair each. Counting sums instead of pairs gives the wrong 9.1%.
**Likely follow-ups:** 1) *How do you pick equally likely outcomes?* Break the event down until each piece is symmetric, such as ordered pairs. 2) *What if the die is loaded?* Use observed frequencies (Q24).
**Common mistakes:** Counting the 11 sums as equally likely; ignoring the 'random' wording and assuming bias or a hidden pattern.

### Q57 ⭐ 🟡 What is the variance of a random variable, and how do you calculate it for a die roll?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that variance measures spread, and can you compute it from a probability table?
**Say this in the interview:** "Variance is the average squared distance from the expected value. For a die the expected value is 3.5 and the variance is 35/12, about 2.92, so the standard deviation is about 1.71."
**Explain simply:**
- **Expected value (mean):** the long-run average outcome.
- **Variance:** how far outcomes typically sit from the mean. We square the distances so that high and low misses do not cancel.
- **Standard deviation:** the square root of variance, back in the original units.
- Shortcut: variance = E[X squared] minus (E[X]) squared. For a die: 91/6 - 3.5 x 3.5 = 35/12.
**Formula in plain words:** variance = the probability-weighted average of (value minus mean) squared. Var(X) = sum of P(x) x (x - mean)^2.
**Worked example:** For die faces 1 to 6 with mean 3.5: squared distances are 6.25, 2.25, 0.25, 0.25, 2.25, 6.25. Their average is 17.5/6 = 2.9167. In HR terms, two teams with the same average rating of 3.5 can differ hugely in spread; variance tells you which team is more consistent.
**Excel / Python:**
```python
import numpy as np

# The six faces, each with probability 1/6
faces = np.array([1, 2, 3, 4, 5, 6])
probability_of_each_face = 1 / 6

# Expected value: average of the faces, weighted by probability
expected_value = np.sum(faces * probability_of_each_face)

# Squared distance of each face from the expected value
squared_distances = (faces - expected_value) ** 2

# Variance: probability-weighted average of the squared distances
variance = np.sum(squared_distances * probability_of_each_face)

# Standard deviation: square root brings the units back to "die points"
standard_deviation = np.sqrt(variance)

print("Expected value =", round(float(expected_value), 4))
print("Variance =", round(float(variance), 4), " (exact 35/12 =", round(35 / 12, 4), ")")
print("Standard deviation =", round(float(standard_deviation), 4))
```
```text
Expected value = 3.5
Variance = 2.9167  (exact 35/12 = 2.9167 )
Standard deviation = 1.7078
```
The average face is 3.5 and a typical roll lands about 1.7 away from it.
**Likely follow-ups:** 1) *Why square the distances?* So positives and negatives do not cancel and large misses count more. 2) *Population vs sample variance?* This is the population form because we know all six equally likely outcomes; for data samples divide by n minus 1.
**Common mistakes:** Forgetting to square; mixing up variance and standard deviation units; dividing by 5 for a full distribution.

### Q58 ⭐ 🟡 What is linearity of expectation, and how does it simplify a problem like the expected number of fixed points or matches?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you break a hard counting problem into simple indicator pieces and add the expectations?
**Say this in the interview:** "Linearity of expectation says the expected total is the sum of the expected parts, and it works even when the parts are dependent. So I give each candidate a 1 if they match and add up 1/n, n times, to get exactly 1."
**Explain simply:**
- **Expectation** means the long-run average.
- **Linearity:** E(A + B) = E(A) + E(B), always, with no independence needed.
- **Indicator trick:** write the count as a sum of 0/1 pieces ("did candidate 1 get the right laptop?"), find each piece's probability, then add.
- **Fixed point:** an item that lands in its own original position after a random shuffle. Each of n items is fixed with probability 1/n, so the expected number is n x 1/n = 1, whatever n is.
**Formula in plain words:** Expected total = sum of expected parts. For indicators, E(count) = sum of P(each piece happens).
**Worked example:** 10 candidates are given 10 laptops at random. Each candidate matches with probability 1/10, so expected matches = 10 x 1/10 = 1. The matches are dependent (if 9 match, the 10th must), yet the answer still holds.
**Excel / Python:**
```python
import random

# Setup: 10 candidates are handed 10 laptops at random; a "match" is a candidate who gets their own laptop
number_of_candidates = 10

# By linearity: each candidate matches with probability 1/10, so expected matches = 10 x 1/10
expected_matches = number_of_candidates * (1 / number_of_candidates)
print("Expected matches by linearity =", expected_matches)

# Check by simulation: shuffle the laptops many times and count matches each time
random.seed(42)
number_of_trials = 100000
total_matches = 0
for trial in range(number_of_trials):
    laptops = list(range(number_of_candidates))
    random.shuffle(laptops)
    matches_this_trial = 0
    for candidate in range(number_of_candidates):
        if laptops[candidate] == candidate:
            matches_this_trial += 1
    total_matches += matches_this_trial

print("Simulated average matches =", round(total_matches / number_of_trials, 3))
```
```text
Expected matches by linearity = 1.0
Simulated average matches = 1.002
```
Both the formula and the 100,000-shuffle simulation give about 1 match, regardless of group size.
**Likely follow-ups:** 1) *Does it need independence?* No, that is its power. 2) *Does it apply to variance?* No, variance adds only for independent parts.
**Common mistakes:** Thinking the parts must be independent; trying to enumerate all arrangements instead of using indicators.

### Q59 ⭐ 🟡 What is the difference between P(A and B) and P(A|B)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell a joint probability from a conditional one by looking at the denominator?
**Say this in the interview:** "P(A and B) is out of everyone. P(A|B) is out of only the B group. The two are linked: P(A and B) = P(B) x P(A|B)."
**Explain simply:**
- **P(A and B)** (joint): both things happen, measured against the whole population.
- **P(A|B)** (conditional): given B has already happened, how likely is A? The population shrinks to the B group.
- Same numerator (the overlap), different denominators. P(A|B) is always at least P(A and B).
- Mixing them up is the root of many mistakes (Q11, Q44).
**Formula in plain words:** P(A and B) = P(B) x P(A|B), so P(A|B) = P(A and B) / P(B).
**Worked example:** Of 200 employees, 80 are in Sales and 24 of those left. P(Sales and left) = 24/200 = 12%. P(left | Sales) = 24/80 = 30%. Same 24 people, different base.
**Excel / Python:**
```python
# Counts from the 200-employee table
total_employees = 200
in_sales = 80
left_and_in_sales = 24

# P(A and B): out of ALL employees, how many are in Sales AND left
probability_sales_and_left = left_and_in_sales / total_employees

# P(left | Sales): out of SALES employees only, how many left
probability_left_given_sales = left_and_in_sales / in_sales

print("P(Sales and left) =", probability_sales_and_left)
print("P(left | Sales) =", probability_left_given_sales)

# Link between them: P(A and B) = P(B) x P(A | B)
probability_sales = in_sales / total_employees
print("P(Sales) x P(left | Sales) =", probability_sales * probability_left_given_sales)
```
```text
P(Sales and left) = 0.12
P(left | Sales) = 0.3
P(Sales) x P(left | Sales) = 0.12
```
12% of the whole company is Sales leavers, but 30% of Sales employees left.
**Likely follow-ups:** 1) *When are they equal?* Only when P(B) = 1. 2) *Which is bigger?* P(A|B) is at least P(A and B), strictly bigger unless B is certain.
**Common mistakes:** Using the whole-company total as the denominator for a conditional question; saying P(A|B) = P(B|A).

### Q60 ⭐ 🟡 Explain the Bayesian update when you toss an unknown coin and see 3 heads in a row, with a fair or two-headed coin equally likely at the start.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you run a clean two-hypothesis Bayes update with evidence from repeated trials?
**Say this in the interview:** "Start 50/50. Three heads has probability 1/8 with a fair coin and 1 with a two-headed coin. So the posterior for two-headed is 0.5 x 1 over 0.5 x 1/8 + 0.5 x 1, which is 8/9, about 89%."
**Explain simply:**
- **Hypotheses:** H1 fair coin, H2 two-headed coin, each with prior 0.5.
- **Evidence:** HHH. Likelihood under fair = 0.5 x 0.5 x 0.5 = 1/8; under two-headed = 1.
- **Posterior:** weight each prior by its likelihood, then divide by the total.
- One tail would have ruled out the two-headed coin (likelihood 0), so every head only strengthens it.
**Formula in plain words:** P(two-headed | HHH) = P(HHH | two-headed) x P(two-headed) divided by [that plus P(HHH | fair) x P(fair)].
**Worked example:** Two-headed share = 0.5 / (0.5 + 0.0625) = 0.8889. Chance the 4th toss is heads = 0.8889 x 1 + 0.1111 x 0.5 = 0.9444.
**Excel / Python:**
```python
# Prior: two coin types equally likely at the start
prior_fair = 0.5
prior_two_headed = 0.5

# Likelihood of seeing 3 heads in a row under each coin type
likelihood_fair = 0.5 ** 3
likelihood_two_headed = 1.0 ** 3

# Multiply prior by likelihood
fair_and_evidence = prior_fair * likelihood_fair
two_headed_and_evidence = prior_two_headed * likelihood_two_headed

# Posterior: divide by the total chance of seeing 3 heads
total_evidence = fair_and_evidence + two_headed_and_evidence
posterior_two_headed = two_headed_and_evidence / total_evidence
posterior_fair = fair_and_evidence / total_evidence

print("P(two-headed | HHH) =", round(posterior_two_headed, 4), "= 8/9 =", round(8 / 9, 4))
print("P(fair | HHH) =", round(posterior_fair, 4))

# Bonus: chance the 4th toss is also heads
probability_next_head = posterior_two_headed * 1.0 + posterior_fair * 0.5
print("P(4th toss is heads) =", round(probability_next_head, 4))
```
```text
P(two-headed | HHH) = 0.8889 = 8/9 = 0.8889
P(fair | HHH) = 0.1111
P(4th toss is heads) = 0.9444
```
After three heads you should be about 89% sure the coin is two-headed; the next toss is a head about 94% of the time.
**Likely follow-ups:** 1) *What about 2 heads?* Posterior = 4/5 = 80%. 2) *What if two-headed coins are rare (1 in 1000)?* The prior dominates and the posterior falls sharply; recompute with the new prior.
**Common mistakes:** Answering 1/8 (the likelihood) or 50% (ignoring the evidence); forgetting that the 4th toss mixes both coin types.

### Q61 ⭐ 🟡 How would you use simulation (Monte Carlo) to estimate a probability that is hard to compute by hand?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to estimate a probability by repeated random experiments when the maths is messy?
**Say this in the interview:** "I simulate the process many times with random numbers, count how often the event occurs, and divide. The more runs, the closer the estimate is to the true probability."
**Explain simply:**
- **Monte Carlo simulation:** repeat a random experiment thousands of times on a computer and use the observed share as the probability.
- Useful when the event involves many moving parts (different rates per team) and no clean formula.
- Set a **seed** so results can be reproduced; use more runs for a tighter estimate.
- Where possible, check against an exact answer for a simpler version.
**Formula in plain words:** estimated probability = number of simulated runs where the event happened / total runs.
**Worked example:** Five HR teams have different monthly leaving chances. What is the chance that 20 or more employees leave in a month? Simulating 100,000 months gives about 48%; the exact convolution check gives 48.6%.
**Excel / Python:**
```python
import numpy as np

# Five teams with different monthly leaving chances (assumed for the example)
team_sizes = [100, 200, 100, 50, 150]
team_leave_chances = [0.02, 0.03, 0.05, 0.01, 0.04]

# Question: what is the chance that 20 or more employees leave in one month?
threshold = 20
number_of_simulations = 100000
random_generator = np.random.default_rng(seed=1)

# Simulate one month many times: each team's leavers come from its own chance
total_leavers_each_month = np.zeros(number_of_simulations, dtype=int)
for team_size, leave_chance in zip(team_sizes, team_leave_chances):
    leavers_in_team = random_generator.binomial(team_size, leave_chance, size=number_of_simulations)
    total_leavers_each_month += leavers_in_team

# Share of simulated months where leavers reached the threshold
months_at_or_above_threshold = np.sum(total_leavers_each_month >= threshold)
estimated_probability = months_at_or_above_threshold / number_of_simulations

print("Average leavers per month =", round(float(total_leavers_each_month.mean()), 2))
print("Estimated P(20 or more leave) =", round(float(estimated_probability), 4))

# Exact check (possible here only because teams are independent): combine team distributions
from scipy.stats import binom
combined_distribution = np.array([1.0])
for team_size, leave_chance in zip(team_sizes, team_leave_chances):
    team_distribution = binom.pmf(np.arange(team_size + 1), team_size, leave_chance)
    combined_distribution = np.convolve(combined_distribution, team_distribution)
exact_probability = combined_distribution[threshold:].sum()
print("Exact P(20 or more leave) =", round(float(exact_probability), 4))
```
```text
Average leavers per month = 19.49
Estimated P(20 or more leave) = 0.4832
Exact P(20 or more leave) = 0.4857
```
The simulation (48.3%) lands within a fraction of a point of the exact answer (48.6%); the average of 19.5 leavers sits just under the threshold of 20, so it is close to a coin flip.
**Likely follow-ups:** 1) *How accurate is it?* Error shrinks with the square root of the number of runs. 2) *Can it replace maths?* It is an estimate; use exact when it is easy.
**Common mistakes:** Too few runs; no seed so results cannot be reproduced; wrong simulation logic (simulating a different process from the question).

### Q62 ⭐ 🟡 What is conditional expectation, and how would you use it to find the average salary given a department?
**Asked at:** commonly asked (no company-specific report found); the sources file lists a conditional expected value of a die given a sum in a 2026 quant prep guide (snippet only).
**What the interviewer is checking:** Can you compute an average within a group and link it to the overall average?
**Say this in the interview:** "Conditional expectation is the average of a variable given a condition, for example the average salary given the department is IT. In pandas it is just a groupby mean."
**Explain simply:**
- **E[X | group]:** the mean of X using only people in that group.
- It changes with the group; the overall mean is the weighted average of the group means (law of total expectation).
- Weights are each group's share of the population.
- It is the basis of pivot tables and group-wise predictions.
**Formula in plain words:** Overall average = sum over groups of (group share x group average). E[X] = sum of P(group) x E[X | group].
**Worked example:** 9 employees: Sales average 50, HR 40, IT 85 (thousand Rs). Shares: Sales 3/9, HR 2/9, IT 4/9. Weighted sum = 63.33, the same as the overall average.
**Excel / Python:**
```python
import pandas as pd

# Small salary table (monthly salary in Rs thousands)
employees = pd.DataFrame({
    "department": ["Sales", "Sales", "Sales", "HR", "HR", "IT", "IT", "IT", "IT"],
    "monthly_salary": [40, 50, 60, 35, 45, 70, 80, 90, 100],
})

# Overall expected salary (ignoring department)
overall_average = employees["monthly_salary"].mean()

# Conditional expectation: average salary within each department
average_by_department = employees.groupby("department")["monthly_salary"].mean()

# Share of employees in each department (the weights)
department_share = employees["department"].value_counts(normalize=True)

# Law of total expectation: weighted sum of department averages equals the overall average
weighted_average = (average_by_department * department_share).sum()

print("Overall average =", round(overall_average, 2))
print(average_by_department)
print("Weighted sum of department averages =", round(weighted_average, 2))
```
```text
Overall average = 63.33
department
HR       40.0
IT       85.0
Sales    50.0
Name: monthly_salary, dtype: float64
Weighted sum of department averages = 63.33
```
IT earns the most on average (85); the weighted group averages rebuild the overall 63.33. In Excel, `=AVERAGEIF(department_range, "IT", salary_range)` gives the IT average (not run in Excel here).
**Likely follow-ups:** 1) *Is E[X|Y] a number?* For a fixed Y yes; as a function of Y it is itself random. 2) *Related to regression?* Regression models E[Y | X].
**Common mistakes:** Averaging the group averages without weights; using a wrong group filter.

### Q63 ⭐ 🟡 What is the odds ratio versus the relative risk, and why are they not the same?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two measures are different and when they nearly agree?
**Say this in the interview:** "Relative risk compares probabilities between groups; the odds ratio compares odds, which are leavers divided by stayers. They are close only when the outcome is rare."
**Explain simply:**
- **Risk** = leavers / everyone in the group. **Relative risk** = risk in group 1 / risk in group 2.
- **Odds** = leavers / stayers. **Odds ratio** = odds in group 1 / odds in group 2.
- Odds blow up as risk grows, so the odds ratio overstates the effect for common outcomes.
- Logistic regression coefficients exponentiate to odds ratios.
**Formula in plain words:** relative risk = P(event | exposed) / P(event | not exposed). odds ratio = [p1/(1-p1)] / [p2/(1-p2)].
**Worked example:** 30 of 100 overtime workers left against 10 of 100 others: risk 30% vs 10%, relative risk 3.0; odds 30/70 vs 10/90, odds ratio 3.86. For a rare event (3 vs 1 per 1000) they match: 3.0 and 3.006.
**Excel / Python:**
```python
# Counts: employees who work overtime vs not, and how many left
overtime_left, overtime_stayed = 30, 70
no_overtime_left, no_overtime_stayed = 10, 90

# Risk = leavers divided by everyone in the group
risk_overtime = overtime_left / (overtime_left + overtime_stayed)
risk_no_overtime = no_overtime_left / (no_overtime_left + no_overtime_stayed)
relative_risk = risk_overtime / risk_no_overtime

# Odds = leavers divided by stayers in the group
odds_overtime = overtime_left / overtime_stayed
odds_no_overtime = no_overtime_left / no_overtime_stayed
odds_ratio = odds_overtime / odds_no_overtime

print("Relative risk =", round(relative_risk, 3))
print("Odds ratio =", round(odds_ratio, 3))

# Rare outcome: 3 of 1000 vs 1 of 1000 leave, the two measures nearly agree
rare_relative_risk = (3 / 1000) / (1 / 1000)
rare_odds_ratio = (3 / 997) / (1 / 999)
print("Rare case relative risk =", round(rare_relative_risk, 3))
print("Rare case odds ratio =", round(rare_odds_ratio, 3))
```
```text
Relative risk = 3.0
Odds ratio = 3.857
Rare case relative risk = 3.0
Rare case odds ratio = 3.006
```
Overtime triples the risk but the odds ratio says 3.86; saying 'almost four times as likely' would be wrong.
**Likely follow-ups:** 1) *Which is easier to explain?* Relative risk. 2) *When must you use odds ratio?* In case-control studies and logistic regression.
**Common mistakes:** Reporting an odds ratio as 'times more likely'; ignoring that the gap grows for common outcomes.

### Q64 ⭐ 🟡 A rare event has probability 0.1% per day. What is the probability it happens at least once in a year of 365 days?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you use the complement rule instead of adding 365 small probabilities?
**Say this in the interview:** "I find the chance it never happens, 0.999 to the power 365, and subtract from 1. That gives about 30.6%, not 36.5%."
**Explain simply:**
- Days are assumed independent with the same 0.1% chance.
- 'At least once' is the opposite of 'never', so use the complement (Q6).
- Multiplying 365 x 0.001 = 0.365 over-counts, because it adds up cases where the event happens on several days.
- The shortcut is close for small totals only.
**Formula in plain words:** P(at least once) = 1 minus (1 minus p) raised to the power n.
**Worked example:** P(never) = 0.999^365 = 0.6941. P(at least once) = 1 - 0.6941 = 30.59%. In HR terms: a 0.1% daily chance of a serious data breach gives about a 3 in 10 chance each year.
**Excel / Python:**
```python
# Chance the event happens on one day
daily_probability = 0.001
days_in_year = 365

# Chance it does NOT happen on a day
probability_not_today = 1 - daily_probability

# Chance it never happens in 365 independent days
probability_never = probability_not_today ** days_in_year

# Complement: chance it happens at least once
probability_at_least_once = 1 - probability_never

print("P(never in a year) =", round(probability_never, 4))
print("P(at least once) =", round(probability_at_least_once, 4))
print("Wrong shortcut 365 x 0.001 =", round(days_in_year * daily_probability, 4))
```
```text
P(never in a year) = 0.6941
P(at least once) = 0.3059
Wrong shortcut 365 x 0.001 = 0.365
```
Roughly a 31% chance in a year; the naive 36.5% overstates it.
**Likely follow-ups:** 1) *What is the Excel formula?* `=1-(1-0.001)^365` (not run in Excel here). 2) *Is independence realistic?* Often not; say it is an assumption.
**Common mistakes:** Multiplying n x p; forgetting the day-to-day independence assumption.

### Q65 ⭐ 🟡 What is the expected number of tosses to get two heads in a row?
**Asked at:** commonly asked in quant-style rounds; the sources file mentions only the simpler 'expected flips until first head' in quant-analyst candidate reports (not data-analyst roles). No report found for HH.
**What the interviewer is checking:** Can you set up expected value with states (recursion)?
**Say this in the interview:** "I track two states: no head yet, and one head in hand. Writing an equation for each gives an expected 6 tosses for HH."
**Explain simply:**
- State **start**: toss; heads moves to the 'one head' state, tails stays at start.
- State **one head**: toss; heads finishes, tails sends you back to start.
- Solving the two equations gives 6.
- It is more than the 2 tosses a beginner guesses because failures restart you (Q71 compares this with HT).
**Formula in plain words:** a = 1 + 0.5 b + 0.5 a, b = 1 + 0.5 a, so a = 6.
**Worked example:** Exact answer 6. A 200,000-run simulation gives 6.01.
**Excel / Python:**
```python
import random

# Exact method with two states. a = expected tosses from the start, b = expected tosses after one head.
# From the start: one toss; heads (1/2) moves us to state b, tails (1/2) leaves us at the start.
#   a = 1 + 0.5*b + 0.5*a
# After one head: one toss; heads (1/2) finishes, tails (1/2) sends us back to the start.
#   b = 1 + 0.5*a
# Putting b into the first line gives a = 1.5 + 0.75*a, so a = 1.5 / 0.25
expected_tosses_exact = 1.5 / (1 - 0.75)
print("Exact expected tosses for HH =", expected_tosses_exact)

# Simulation check
random.seed(7)
number_of_trials = 200000
total_tosses = 0
for trial in range(number_of_trials):
    tosses = 0
    previous_was_head = False
    while True:
        tosses += 1
        is_head = random.random() < 0.5
        if is_head and previous_was_head:
            break
        previous_was_head = is_head
    total_tosses += tosses

print("Simulated average tosses =", round(total_tosses / number_of_trials, 3))
```
```text
Exact expected tosses for HH = 6.0
Simulated average tosses = 6.012
```
The exact equation and the simulation agree on about 6 tosses.
**Likely follow-ups:** 1) *Expected tosses for the first head?* 2 (Q46). 2) *For HHH?* 14.
**Common mistakes:** Answering 4 (2 x 2) or ignoring the restart after a tail.

### Q66 ⭐ 🟡 You are given the probabilities of A, B and A or B. How do you find the probability that exactly one of A and B happens?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use the addition rule backwards to find an overlap?
**Say this in the interview:** "First I find P(A and B) = P(A) + P(B) - P(A or B). Exactly one happens means A or B minus both, which simplifies to 2 x P(A or B) - P(A) - P(B)."
**Explain simply:**
- 'Exactly one' means A only or B only, never both.
- P(A or B) includes the overlap, so subtract the overlap once to remove the 'both' case.
- Equivalent: P(A) + P(B) - 2 x P(A and B).
**Formula in plain words:** P(exactly one) = P(A or B) - P(A and B) = 2 x P(A or B) - P(A) - P(B).
**Worked example:** P(A) = 0.5, P(B) = 0.4, P(A or B) = 0.7. Overlap = 0.5 + 0.4 - 0.7 = 0.2. Exactly one = 0.7 - 0.2 = 0.5.
**Excel / Python:**
```python
# Given values
probability_a = 0.50
probability_b = 0.40
probability_a_or_b = 0.70

# Step 1: find P(A and B) from the addition rule
probability_both = probability_a + probability_b - probability_a_or_b

# Step 2: exactly one = A or B, minus the overlap
probability_exactly_one = probability_a_or_b - probability_both

# Shortcut formula: 2 x P(A or B) - P(A) - P(B)
shortcut = 2 * probability_a_or_b - probability_a - probability_b

print("P(A and B) =", round(probability_both, 2))
print("P(exactly one) =", round(probability_exactly_one, 2))
print("Shortcut check =", round(shortcut, 2))
```
```text
P(A and B) = 0.2
P(exactly one) = 0.5
Shortcut check = 0.5
```
Half the time exactly one of the two events happens; 20% of the time both do.
**Likely follow-ups:** 1) *Exactly none?* 1 - P(A or B) = 0.3. 2) *Are A and B independent here?* 0.5 x 0.4 = 0.2, equal to P(A and B), so yes.
**Common mistakes:** Reporting P(A or B) as 'exactly one'; adding P(A) + P(B) without subtracting the overlap.

### Q67 ⭐ 🟡 What are conditional independence and a common confounding mistake in probability reasoning?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that apparent links can disappear once you account for a third factor?
**Say this in the interview:** "Two events can be dependent overall but independent once we fix a third factor. If we ignore that factor, a confounder, we may wrongly claim one causes the other."
**Explain simply:**
- **Conditional independence:** A and B are independent *given* C, so P(A and B | C) = P(A|C) x P(B|C).
- **Confounder:** a hidden factor driving both, such as seniority driving both salary and training.
- Independence overall and conditional independence do not imply each other.
- Fix: compare within groups (stratify) before concluding.
**Formula in plain words:** P(A and B | C) = P(A | C) x P(B | C) for conditional independence.
**Worked example:** Half the staff are seniors. Seniors have 80% high salary and 80% advanced training; juniors 20% and 20%, independent within each group. Overall P(both) = 0.34 but 0.5 x 0.5 = 0.25, so they look linked. Inside the seniors alone the product 0.64 equals the joint 0.64.
**Excel / Python:**
```python
# Two equal groups of 100: juniors and seniors
# Within each group, high salary and advanced training are independent
share_senior = 0.5
share_junior = 0.5
high_salary_given_senior, high_salary_given_junior = 0.8, 0.2
trained_given_senior, trained_given_junior = 0.8, 0.2

# Overall chances (law of total probability)
p_high_salary = share_senior * high_salary_given_senior + share_junior * high_salary_given_junior
p_trained = share_senior * trained_given_senior + share_junior * trained_given_junior

# Overall chance of both: add up within each group (independent inside a group)
p_both = (share_senior * high_salary_given_senior * trained_given_senior
          + share_junior * high_salary_given_junior * trained_given_junior)

print("P(high salary) =", round(p_high_salary, 2))
print("P(trained) =", round(p_trained, 2))
print("P(both) =", round(p_both, 2))
print("P(high salary) x P(trained) =", round(p_high_salary * p_trained, 2))

# Inside seniors only: product equals joint, so independent given seniority
print("Seniors only: P(both) =", round(high_salary_given_senior * trained_given_senior, 2))
print("Seniors only: product =", round(high_salary_given_senior * trained_given_senior, 2))
```
```text
P(high salary) = 0.5
P(trained) = 0.5
P(both) = 0.34
P(high salary) x P(trained) = 0.25
Seniors only: P(both) = 0.64
Seniors only: product = 0.64
```
Overall the two look related (0.34 against 0.25), but inside one seniority group they are independent, so seniority explains the link, not training causing pay.
**Likely follow-ups:** 1) *How does this relate to Simpson's paradox?* The group view can reverse the overall pattern. 2) *How do you fix it?* Stratify or control for the variable in a model.
**Common mistakes:** Concluding causation from overall correlation; assuming independence given C also means independence overall.

### Q68 ⭐ 🔴 Explain the birthday problem calculation step by step and relate it to finding duplicate employee IDs or dates in data.
**Asked at:** commonly asked (no company-specific report found); the sources file lists the birthday problem as a frequent puzzle in prep material.
**What the interviewer is checking:** Can you compute the complement step by step and link it to a data task?
**Say this in the interview:** "I find the chance everyone's birthday is different, 365/365 x 364/365 and so on, and subtract from 1. At 23 people the chance of a shared birthday passes 50%. The same logic says duplicates in data appear far sooner than you would guess."
**Explain simply:**
- Count pairs, not people: 23 people make 253 pairs, each a chance of a match.
- P(all different) multiplies shrinking fractions: person 2 avoids 1 date, person 3 avoids 2, and so on.
- P(match) = 1 - P(all different). Approximation: 1 - exp(-n(n-1)/(2 x days)).
- Assumes equally likely birthdays; real birthdays are uneven, which makes matches slightly more likely.
- Data link: random IDs or dates in a small range collide quickly, so always check duplicates in joining dates or generated IDs.
**Formula in plain words:** P(match among n) = 1 minus the product of (365 - k)/365 for k = 0 to n - 1.
**Worked example:** 23 people give 50.7%; 50 people give 97.0%. For 40 hires joining on random days from 250 working days, the chance two share a joining date is 96.3%.
**Excel / Python:**
```python
import math
import random

# Exact: P(no shared birthday among n people) = 365/365 x 364/365 x ... ; then take the complement
def probability_of_a_match(number_of_people, days=365):
    probability_all_different = 1.0
    for person_number in range(number_of_people):
        probability_all_different *= (days - person_number) / days
    return 1 - probability_all_different

for people in [10, 22, 23, 30, 50]:
    print(people, "people: P(match) =", round(probability_of_a_match(people), 4))

# Quick approximation: 1 - exp(-n(n-1)/(2 x 365))
approx_23 = 1 - math.exp(-23 * 22 / (2 * 365))
print("Approximation for 23 =", round(approx_23, 4))

# Simulation check for 23 people
random.seed(3)
trials = 100000
matches = 0
for trial in range(trials):
    birthdays = [random.randrange(365) for person in range(23)]
    if len(set(birthdays)) < 23:
        matches += 1
print("Simulated for 23 =", round(matches / trials, 4))

# Data link: 40 employees joining on random working days (about 250 days) in a year
print("40 joiners over 250 days: P(two share a joining date) =", round(probability_of_a_match(40, days=250), 4))
```
```text
10 people: P(match) = 0.1169
22 people: P(match) = 0.4757
23 people: P(match) = 0.5073
30 people: P(match) = 0.7063
50 people: P(match) = 0.9704
Approximation for 23 = 0.5
Simulated for 23 = 0.5075
40 joiners over 250 days: P(two share a joining date) = 0.9631
```
Exact (50.7%), approximation (50.0%) and simulation (50.8%) agree for 23 people.
**Likely follow-ups:** 1) *Why surprising?* Pairs grow quadratically. 2) *Practical use?* Estimating collision risk in IDs and in hashing.
**Common mistakes:** Thinking you need about 183 people (half of 365); multiplying instead of using the complement.

### Q69 ⭐ 🔴 A drunk-driver style puzzle: 90% of a city's taxis are green and 10% blue; a witness who is 80% reliable says the taxi was blue. What is the probability it was blue?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use the base rate with an imperfect witness (Bayes)?
**Say this in the interview:** "Only 10% of taxis are blue, so even a fairly reliable witness is usually wrong when they say blue. Bayes gives 0.08 over 0.08 + 0.18, about 31%."
**Explain simply:**
- **Premise note:** '80% reliable' is read as correct 80% of the time for both colours.
- Of every 100 taxis: 10 are blue and the witness says blue for 8 of them; 90 are green and the witness says blue for 18 of them.
- So among 26 'blue' calls, only 8 are truly blue.
- The base rate (few blue taxis) beats the witness's accuracy.
**Formula in plain words:** P(blue | says blue) = P(says blue | blue) x P(blue) / [that plus P(says blue | green) x P(green)].
**Worked example:** 0.8 x 0.1 = 0.08; 0.2 x 0.9 = 0.18; 0.08 / 0.26 = 30.77%.
**Excel / Python:**
```python
# Prior: 10% of taxis are blue
prior_blue = 0.10
prior_green = 0.90

# Witness is right 80% of the time for either colour
says_blue_given_blue = 0.80
says_blue_given_green = 0.20

# Chance the witness says "blue" in each case
blue_and_says_blue = prior_blue * says_blue_given_blue
green_and_says_blue = prior_green * says_blue_given_green

# Bayes: share of "says blue" cases that really are blue
posterior_blue = blue_and_says_blue / (blue_and_says_blue + green_and_says_blue)

print("P(blue and says blue) =", round(blue_and_says_blue, 2))
print("P(green and says blue) =", round(green_and_says_blue, 2))
print("P(blue | says blue) =", round(posterior_blue, 4))
```
```text
P(blue and says blue) = 0.08
P(green and says blue) = 0.18
P(blue | says blue) = 0.3077
```
The witness is right 80% of the time, but a 'blue' report is correct only about 31% of the time.
**Likely follow-ups:** 1) *If the split were 50/50?* 80%. 2) *Link to medical tests?* Same structure (Q12).
**Common mistakes:** Answering 80% (ignoring the base rate); treating 'reliable' as the posterior.

### Q70 ⭐ 🔴 What is the probability that a random chord of a circle is longer than the side of an inscribed equilateral triangle, and what does this show about defining "random"?
**Asked at:** commonly asked (no company-specific report found); a classic puzzle (the Bertrand paradox) that is more common in quant prep than in data-analyst reports.
**What the interviewer is checking:** Do you see that 'random' needs a precise definition and the answer depends on it?
**Say this in the interview:** "The answer is 1/3, 1/2 or 1/4, depending on what 'random chord' means. That is the Bertrand paradox: always state how the randomness is generated."
**Explain simply:**
- A chord is 'long' if longer than the triangle side, which is root 3 times the radius.
- **Method 1** (two random points on the edge): probability 1/3.
- **Method 2** (random point along a radius, chord perpendicular): probability 1/2.
- **Method 3** (random midpoint anywhere inside the disk): probability 1/4.
- All three are valid readings; the question as asked is ambiguous. Lesson for data work: define how a sample is chosen.
**Formula in plain words:** Method 1: 1/3. Method 2: 1/2. Method 3: 1/4 (chord is long when its midpoint lies within half the radius, an area of 1/4 of the disk).
**Worked example:** Simulating one million chords per method gives 0.334, 0.499 and 0.250.
**Excel / Python:**
```python
import numpy as np

# Circle of radius 1; the triangle side is sqrt(3), so a chord is "long" if length > sqrt(3)
radius = 1.0
long_chord_length = np.sqrt(3)
number_of_chords = 1000000
random_generator = np.random.default_rng(seed=5)

# Method 1: pick two random points on the circle edge
angle_one = random_generator.uniform(0, 2 * np.pi, number_of_chords)
angle_two = random_generator.uniform(0, 2 * np.pi, number_of_chords)
chord_length_method_1 = 2 * radius * np.abs(np.sin((angle_one - angle_two) / 2))

# Method 2: pick a random point along a radius; chord is perpendicular to it
distance_from_centre = random_generator.uniform(0, radius, number_of_chords)
chord_length_method_2 = 2 * np.sqrt(radius ** 2 - distance_from_centre ** 2)

# Method 3: pick a random midpoint inside the disk (uniform over area)
distance_of_midpoint = radius * np.sqrt(random_generator.uniform(0, 1, number_of_chords))
chord_length_method_3 = 2 * np.sqrt(radius ** 2 - distance_of_midpoint ** 2)

print("Method 1 (two edge points): ", round(float(np.mean(chord_length_method_1 > long_chord_length)), 3))
print("Method 2 (point on radius): ", round(float(np.mean(chord_length_method_2 > long_chord_length)), 3))
print("Method 3 (midpoint in disk):", round(float(np.mean(chord_length_method_3 > long_chord_length)), 3))
```
```text
Method 1 (two edge points):  0.334
Method 2 (point on radius):  0.499
Method 3 (midpoint in disk): 0.25
```
Three equally 'random' selection rules produce three different answers, 1/3, 1/2 and 1/4.
**Likely follow-ups:** 1) *Which is correct?* None alone; the question is ill-posed until the method is stated. 2) *Data relevance?* Sampling method changes conclusions.
**Common mistakes:** Quoting one answer without naming the method; treating the ambiguity as a mistake in the maths.

### Q71 ⭐ 🔴 You flip a fair coin until you see heads then tails (HT) versus heads then heads (HH). Which is expected sooner and why?
**Asked at:** commonly asked in quant-style rounds; no company-specific report found for a data-analyst role.
**What the interviewer is checking:** Can you reason about overlap in patterns and restarts?
**Say this in the interview:** "HT is expected sooner: 4 tosses on average against 6 for HH. After a failed HH attempt (a tail) I restart; after a failed HT attempt (a head) I still hold a head and can continue."
**Explain simply:**
- Expected tosses: HT = 4, HH = 6 (Q65 derives 6).
- With HT, once you hold a head you only need a tail; if you get another head you still hold a head, so no progress is lost.
- With HH, a tail destroys your head and you restart from scratch.
- In a race, HT and HH are equally likely to appear first (50%): both need a head, then the next toss decides. Do not confuse 'appears first' with 'expected waiting time'.
**Formula in plain words:** Expected tosses by states: HT needs 4 (head, then wait for a tail), HH needs 6 (see Q65).
**Worked example:** Simulation of 200,000 runs: HT averages 4.00 tosses, HH averages 6.00; HT came first in 50% of races.
**Excel / Python:**
```python
import random

# Run the experiment many times and record tosses until the pattern first appears
def tosses_until_pattern(pattern):
    last_two = ""
    tosses = 0
    while last_two != pattern:
        tosses += 1
        new_toss = "H" if random.random() < 0.5 else "T"
        last_two = (last_two + new_toss)[-2:]
    return tosses

random.seed(11)
number_of_trials = 200000
total_for_ht = 0
total_for_hh = 0
for trial in range(number_of_trials):
    total_for_ht += tosses_until_pattern("HT")
    total_for_hh += tosses_until_pattern("HH")

print("Average tosses until HT =", round(total_for_ht / number_of_trials, 3), "(exact 4)")
print("Average tosses until HH =", round(total_for_hh / number_of_trials, 3), "(exact 6)")

# Race: which pattern appears first? Both need a head first, then the next toss decides
wins_for_ht = 0
for trial in range(number_of_trials):
    last_two = ""
    while last_two not in ("HT", "HH"):
        new_toss = "H" if random.random() < 0.5 else "T"
        last_two = (last_two + new_toss)[-2:]
    if last_two == "HT":
        wins_for_ht += 1
print("P(HT appears before HH) =", round(wins_for_ht / number_of_trials, 3), "(exact 0.5)")
```
```text
Average tosses until HT = 4.001 (exact 4)
Average tosses until HH = 5.996 (exact 6)
P(HT appears before HH) = 0.5 (exact 0.5)
```
HT arrives about two tosses sooner on average, yet it wins a head-to-head race only half the time.
**Likely follow-ups:** 1) *Which is more likely to appear first?* Tied at 50%. 2) *Why is the average different?* HH has no overlap with itself after a miss.
**Common mistakes:** Saying they are equal because both have probability 1/4 in two tosses; mixing up race odds and average waiting time.
