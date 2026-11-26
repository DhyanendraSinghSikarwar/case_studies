# Chapter 32 Answer Key: Algorithmic Thinking

These are model solutions. Any correct, clear procedure is acceptable. Every sample result below was recomputed by running an equivalent program on the sample data (including the guess counts for Q18 and the totals for Q19).

## Self-check answers

1. **No, it is a goal.** An algorithm must say *how*: exact steps, in order, that anyone can follow (for example: take the first sale as the best so far, compare each remaining sale, keep the larger).
2. "Start with the largest number" is circular: you do not know the largest number yet. Fix: start with the **first number in the list** as the best guess so far, then compare the rest.
3. Decide in advance and write it: usually "show 'no data' and stop". Without a rule, "take the first value" has nothing to take.

---

## Practice answers

**Q1** 🟢 Smallest number.
Plain steps: (1) if the list is empty, show "no data" and stop; (2) call the first number the smallest so far; (3) look at each other number; if it is smaller, it becomes the smallest so far; (4) show the smallest so far.
```text
GIVEN a list called daily_sales
IF daily_sales is empty THEN
    SHOW "no data"
    STOP
END IF

SET smallest_so_far TO the first value in daily_sales
FOR EACH sale IN the rest of daily_sales
    IF sale < smallest_so_far THEN
        SET smallest_so_far TO sale
    END IF
END FOR
SHOW smallest_so_far
```
Trace for 320, 280, 415, 260, 390: start 320; 280 smaller (280); 415 no; 260 smaller (260); 390 no. **Answer: 260.**

**Q2** 🟢 Total.
Plain steps: start a total at 0; add each amount; show the total (an empty list gives 0, which is sensible).
```text
GIVEN a list called order_amounts
SET total_amount TO 0
FOR EACH amount IN order_amounts
    SET total_amount TO total_amount + amount
END FOR
SHOW total_amount
```
Trace: 0, 150, 350, 425, 550. **Answer: 550.**

**Q3** 🟢 Count more than 100.
```text
GIVEN a list called numbers
SET count_above_100 TO 0
FOR EACH number IN numbers
    IF number > 100 THEN
        SET count_above_100 TO count_above_100 + 1
    END IF
END FOR
SHOW count_above_100
```
Trace: 90 no, 120 yes (1), 100 no (not more than 100), 150 yes (2), 101 yes (3), 99 no. **Answer: 3.**

**Q4** 🟢 Attendance award.
Plain steps: take the days present; if it is 22 or more, the result is "award"; otherwise "no award".
```text
GIVEN days_present
IF days_present >= 22 THEN
    SHOW "award"
ELSE
    SHOW "no award"
END IF
```
Trace: 22 gives award (22 is "at least 22"); 21 gives no award; 26 gives award. (The total working days, 26, is only context here; the rule uses the 22.)

**Q5** 🟢 Multiples of 5 up to a limit.
Plain steps: start at 5; while the number is not above the limit, show it and add 5.
```text
GIVEN a number called limit
SET current_number TO 5
WHILE current_number <= limit
    SHOW current_number
    SET current_number TO current_number + 5
END WHILE
```
Trace for limit 23: 5 shown, 10 shown, 15 shown, 20 shown, next is 25 which is more than 23, so stop. **Answer: 5, 10, 15, 20.**

**Q6** 🟢 Tea for one (one possible answer).
Plain steps: (1) fill the kettle with enough water for one cup and boil it; (2) put one teaspoon of tea leaves or one teabag in a cup; (3) pour in the hot water and wait three minutes; (4) take out the teabag or strain the leaves; (5) if there is milk, add a splash; otherwise skip milk; (6) add sugar only if wanted; (7) serve.
```text
FILL kettle with water for one cup
BOIL the water
PUT one teabag IN the cup
POUR hot water INTO the cup
WAIT 3 minutes
REMOVE the teabag
IF milk is available THEN
    ADD a splash of milk
ELSE
    SHOW "serving without milk"
END IF
SERVE the cup
```
Points checked: steps are ordered (water cannot be poured before it boils), finite, and the missing-milk case is handled.

**Q7** 🟢 First employee older than 50.
```text
GIVEN a list of employees, each with name and age
FOR EACH employee IN the list
    IF employee.age > 50 THEN
        SHOW employee.name
        STOP
    END IF
END FOR
SHOW "nobody is older than 50"
```
Trace: Ravi 34 no, Meena 47 no, Imran 52 yes, so show Imran and stop. **Answer: Imran.** (Kavya, 61, is never examined because we stopped.) For a list with no one above 50 the loop finishes and the last line shows "nobody is older than 50".

**Q8** 🟡 Average ignoring blanks (same pattern as Example 5).
```text
GIVEN a list called overtime_hours
SET total_hours TO 0
SET number_of_entries TO 0
FOR EACH entry IN overtime_hours
    IF entry is NOT blank THEN
        SET total_hours TO total_hours + entry
        SET number_of_entries TO number_of_entries + 1
    END IF
END FOR
IF number_of_entries = 0 THEN
    SHOW "no data"
ELSE
    SHOW total_hours / number_of_entries
END IF
```
Trace: 12 (total 12, count 1), blank skip, 18 (30, 2), 15 (45, 3), blank skip, 15 (60, 4). 60 / 4 = **15**. If all entries are blank the count stays 0 and "no data" is shown (avoiding division by zero).

**Q9** 🟡 Largest and smallest in one pass.
```text
GIVEN a list called numbers (not empty)
SET largest_so_far TO the first value
SET smallest_so_far TO the first value
FOR EACH number IN the rest of numbers
    IF number > largest_so_far THEN
        SET largest_so_far TO number
    END IF
    IF number < smallest_so_far THEN
        SET smallest_so_far TO number
    END IF
END FOR
SHOW largest_so_far AND smallest_so_far
```
Trace for 34, 12, 56, 7, 45: start (34, 34); 12 gives smallest 12; 56 gives largest 56; 7 gives smallest 7; 45 changes nothing. **Answer: largest 56, smallest 7.** Both tests are separate IFs (not ELSE) because one number could in principle change either value; with the first value used for both, a list of one number works too.

**Q10** 🟡 Non-decreasing check.
Plain steps: compare each number with the one before it; as soon as a number is smaller than the previous one, the answer is "no"; if you reach the end without that, the answer is "yes".
```text
GIVEN a list called numbers
IF numbers has 0 or 1 items THEN
    SHOW "yes"
    STOP
END IF
SET previous_number TO the first value
FOR EACH number IN the rest of numbers
    IF number < previous_number THEN
        SHOW "no"
        STOP
    END IF
    SET previous_number TO number
END FOR
SHOW "yes"
```
Trace for 3, 5, 5, 9: 5 vs 3 fine; 5 vs 5 fine (equal is allowed); 9 vs 5 fine; end, **yes**. Trace for 2, 6, 4, 8: 6 vs 2 fine; 4 vs 6 is smaller, so **no**. (A list with 0 or 1 items is "yes" because there is nothing to break the rule; the first IF in the pseudocode handles that case.)

**Q11** 🟡 Missing from the bank.
```text
GIVEN a list called company_records
GIVEN a list called bank_statement
SET missing_at_bank TO an empty list
FOR EACH invoice IN company_records
    IF invoice is NOT in bank_statement THEN
        ADD invoice TO missing_at_bank
    END IF
END FOR
SHOW missing_at_bank
```
Trace: A12 not in bank (add), A15 in bank, A18 not in bank (add), A21 in bank, A30 not in bank (add). **Answer: A12, A18, A30.** (A40 is in the bank but not in the records; this question did not ask for that side.)

**Q12** 🟡 Tally per department.
Plain steps: keep a tally table (department, count). For each department in the list: if it is already in the table, add 1 to its count; otherwise add it with count 1.
```text
GIVEN a list called departments
SET tally TO an empty table of (department, count)
FOR EACH department IN departments
    IF department is already in tally THEN
        SET its count TO its count + 1
    ELSE
        ADD department TO tally with count 1
    END IF
END FOR
SHOW tally
```
Trace for HR, IT, HR, Sales, IT, HR, Ops: HR 1; IT 1; HR 2; Sales 1; IT 2; HR 3; Ops 1. **Answer: HR 3, IT 2, Sales 1, Ops 1** (total 7, matching the 7 items).

**Q13** 🟡 Second largest distinct value.
Plain steps (one way): find the largest; then find the largest among the values that are **not equal** to it.
```text
GIVEN a list called numbers
SET largest_value TO the largest value in numbers (use the Example 1 steps)
SET second_largest TO nothing yet
FOR EACH number IN numbers
    IF number is NOT equal to largest_value THEN
        IF second_largest is nothing yet OR number > second_largest THEN
            SET second_largest TO number
        END IF
    END IF
END FOR
SHOW second_largest
```
Trace for 40, 90, 90, 75, 60: largest is 90. 40 becomes second (40); 90 skipped; 90 skipped; 75 beats 40 (75); 60 does not beat 75. **Answer: 75.** The trap is the duplicate 90: a method that just takes "the second item in sorted order" would wrongly give 90.

**Q14** 🟡 Remove duplicates, keep first.
```text
GIVEN a list called employee_ids
SET unique_ids TO an empty list
FOR EACH id IN employee_ids
    IF id is NOT in unique_ids THEN
        ADD id TO the end of unique_ids
    END IF
END FOR
SHOW unique_ids
```
Trace for E4, E7, E4, E9, E7, E2: E4 add; E7 add; E4 already there; E9 add; E7 already there; E2 add. **Answer: E4, E7, E9, E2.**

**Q15** 🔴 Reverse a list.
Plain steps: make an empty new list; take items from the **end** of the original, one at a time, back to the start, adding each to the new list.
```text
GIVEN a list called words
SET reversed_words TO an empty list
SET position TO number of items in words
WHILE position >= 1
    ADD the item at position in words TO the end of reversed_words
    SET position TO position - 1
END WHILE
SHOW reversed_words
```
Trace for Mon, Tue, Wed, Thu: position 4 adds Thu; 3 adds Wed; 2 adds Tue; 1 adds Mon; position 0 stops. **Answer: Thu, Wed, Tue, Mon.**

**Q16** 🔴 Highest day and days above average.
```text
GIVEN a list called daily_sales (not empty)

NOTE: pass 1 finds the total, the average and the best day
SET total_sales TO 0
SET best_sales TO the first value
SET best_day TO 1
SET day_number TO 0
FOR EACH sale IN daily_sales
    SET day_number TO day_number + 1
    SET total_sales TO total_sales + sale
    IF sale > best_sales THEN
        SET best_sales TO sale
        SET best_day TO day_number
    END IF
END FOR
SET average_sales TO total_sales / number of items in daily_sales

NOTE: pass 2 counts the days above the average
SET days_above_average TO 0
FOR EACH sale IN daily_sales
    IF sale > average_sales THEN
        SET days_above_average TO days_above_average + 1
    END IF
END FOR

SHOW best_day AND days_above_average
```
Trace: total = 220 + 310 + 180 + 400 + 260 = 1,370; average = 1,370 / 5 = 274. Best is 400 on **day 4**. Days above 274: 310 and 400, so **2 days**. (The average must be known before counting, which is why two passes are needed.)

**Q17** 🔴 Merge two sorted lists.
Plain steps: keep a pointer at the front of each list. Repeatedly compare the two items at the pointers; move the smaller to the result and advance that pointer. When one list runs out, copy over the rest of the other.
```text
GIVEN sorted lists first_list and second_list
SET merged_list TO an empty list
SET first_position TO 1
SET second_position TO 1

WHILE first_position <= size of first_list AND second_position <= size of second_list
    IF item at first_position in first_list <= item at second_position in second_list THEN
        ADD that first_list item TO merged_list
        SET first_position TO first_position + 1
    ELSE
        ADD that second_list item TO merged_list
        SET second_position TO second_position + 1
    END IF
END WHILE

NOTE: one list is finished; the rest of the other is already in order
ADD all remaining items of first_list TO merged_list
ADD all remaining items of second_list TO merged_list
SHOW merged_list
```
Trace for (2, 6, 11) and (3, 4, 15, 20): 2 vs 3 gives 2; 6 vs 3 gives 3; 6 vs 4 gives 4; 6 vs 15 gives 6; 11 vs 15 gives 11; first list is finished, so add 15, 20. **Answer: 2, 3, 4, 6, 11, 15, 20.**

**Q18** 🔴 Halving search.
Plain steps: keep a low and a high position (start 1 and 9). Take the middle position (round down). If the middle item is the target, stop. If it is smaller than the target, the target can only be in the upper half, so move low to middle + 1; if larger, move high to middle minus 1. If low passes high, the target is not there. Count each look as one guess.
```text
GIVEN a sorted list called sorted_numbers and a number called target
SET low TO 1
SET high TO number of items in sorted_numbers
SET guesses TO 0
WHILE low <= high
    SET middle TO the whole-number part of (low + high) / 2
    SET guesses TO guesses + 1
    IF item at middle = target THEN
        SHOW middle AND guesses
        STOP
    ELSE IF item at middle < target THEN
        SET low TO middle + 1
    ELSE
        SET high TO middle - 1
    END IF
END WHILE
SHOW "not found" AND guesses
```
Trace for **35**: low 1, high 9, middle 5 (21 is smaller than 35, low becomes 6); middle 7 (35, found). **Found at position 7 in 2 guesses.**
Trace for **10**: middle 5 (21 is larger, high 4); middle 2 (8 is smaller, low 3); middle 3 (12 is larger, high 2); low 3 is past high 2, stop. **Not found, 3 guesses.**
Trace for **3**: middle 5 (21 larger, high 4); middle 2 (8 larger, high 1); middle 1 (3, found). **Found at position 1 in 3 guesses.**

**Q19** 🔴 Reconcile with date and amount.
Plain steps: for each company entry, look for a bank entry with the same date **and** the same amount; if none, put it in "unmatched records". Do the same the other way for bank entries. Add up each side. Report totals and the difference.
```text
GIVEN a list called company_entries of (date, amount)
GIVEN a list called bank_entries of (date, amount)
SET unmatched_records TO an empty list
SET unmatched_bank TO an empty list

FOR EACH entry IN company_entries
    IF no bank entry has the same date AND the same amount THEN
        ADD entry TO unmatched_records
    END IF
END FOR

FOR EACH entry IN bank_entries
    IF no company entry has the same date AND the same amount THEN
        ADD entry TO unmatched_bank
    END IF
END FOR

SET total_records TO the sum of all amounts in company_entries
SET total_bank TO the sum of all amounts in bank_entries
SHOW unmatched_records AND unmatched_bank
SHOW total_records minus total_bank
```
Trace: records (5 Mar, 1,200) matches; (6 Mar, 450) has no match (unmatched); (7 Mar, 980) has no match, because the bank has 990 on that date (unmatched). Bank (5 Mar, 1,200) matches; (7 Mar, 990) no match; (8 Mar, 300) no match.
**Unmatched records:** (6 Mar, 450), (7 Mar, 980). **Unmatched bank:** (7 Mar, 990), (8 Mar, 300).
Totals: records 1,200 + 450 + 980 = 2,630; bank 1,200 + 990 + 300 = 2,490. **Difference = 140.** Cross-check: unmatched records total 450 + 980 = 1,430; unmatched bank total 990 + 300 = 1,290; 1,430 minus 1,290 = 140. The 10-rupee gap on 7 March (980 versus 990) is likely a typing error, but the procedure only reports it; it does not decide. (Edge case not covered by this sample: two identical entries on one side, which would need a rule such as "each bank entry can be matched only once".)

**Q20** 🔴 Longest run above target.
Plain steps: keep a current run length and a best run length, both 0. For each day: if sales are above the target, add 1 to the current run; otherwise reset the current run to 0. After each day, if the current run is longer than the best, update the best.
```text
GIVEN a list called daily_sales and a number called target
SET current_run TO 0
SET longest_run TO 0
FOR EACH sale IN daily_sales
    IF sale > target THEN
        SET current_run TO current_run + 1
    ELSE
        SET current_run TO 0
    END IF
    IF current_run > longest_run THEN
        SET longest_run TO current_run
    END IF
END FOR
SHOW longest_run
```
Trace for target 100 and 120, 90, 110, 130, 105, 80, 140, 150: 120 (run 1, best 1); 90 (run 0); 110 (run 1); 130 (run 2, best 2); 105 (run 3, best 3); 80 (run 0); 140 (run 1); 150 (run 2). **Answer: 3** (days 3 to 5).
