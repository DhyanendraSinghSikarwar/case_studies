# Chapter 3 Answer Key: AND, OR, NOT and Truth Tables

## Self-check answers

1. **F (false).** NOT flips the value, and the office is open (true), so "the office is not open" is false.
2. **Only when both p and q are false.** One true part is enough for OR to be true (and both true also gives true).
3. **8 rows.** Each statement has 2 values, so 2 x 2 x 2 = 8.

## Practice answers

### Q1 🟢

NOT flips each value. One statement means 2 rows.

| p | NOT p |
|---|---|
| T | F |
| F | T |

**Answer:** NOT p is F when the server is running and T when it is not.

### Q2 🟢

AND is true only when both are true.

| p | q | p AND q |
|---|---|---|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**Answer:** only the first row (T, T) is true: the letter is issued only when probation is complete and HR has signed.

### Q3 🟢

OR is false only when both are false.

| p | q | p OR q |
|---|---|---|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**Answer:** the fine is waived in **3** of the 4 rows (all except F, F). Nobody is both under 12 and over 65, so in real life the T, T row never happens, but the table still lists it because a table covers every combination.

### Q4 🟢

Compute the helper column NOT q first, then AND with p.

| p | q | NOT q | p AND NOT q |
|---|---|---|---|
| T | T | F | F |
| T | F | T | T |
| F | T | F | F |
| F | F | T | F |

**Answer:** the order ships in only one row: paid (T) and not on hold (q is F).

### Q5 🟢

First p OR q, then flip it with NOT.

| p | q | p OR q | NOT (p OR q) |
|---|---|---|---|
| T | T | T | F |
| T | F | T | F |
| F | T | T | F |
| F | F | F | T |

**Answer:** "Nothing to drink" shows only in the last row (F, F): no tea and no coffee.

### Q6 🟢

Keep the first column T for the top half and F for the bottom half, then halve the block size for each next column.

| p | q | r |
|---|---|---|
| T | T | T |
| T | T | F |
| T | F | T |
| T | F | F |
| F | T | T |
| F | T | F |
| F | F | T |
| F | F | F |

**Answer:** the table above has 8 rows. 4 statements need 2 x 2 x 2 x 2 = **16** rows. 5 statements need **32** rows.

### Q7 🟢


| p | q | p OR q |
|---|---|---|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**Answer:** in the row where it rains and the road is closed, "late" is **true**. Some people think it is false because in daily speech "or" often suggests only one of the two; logical OR is inclusive, so both happening still makes the rule true.

### Q8 🟡


| p | q | p AND q | NOT (p AND q) | NOT p | NOT q | (NOT p) OR (NOT q) |
|---|---|---|---|---|---|---|
| T | T | T | F | F | F | F |
| T | F | F | T | F | T | T |
| F | T | F | T | T | F | T |
| F | F | F | T | T | T | T |

**Answer:** the columns NOT (p AND q) and (NOT p) OR (NOT q) are identical (F, T, T, T). They are **equivalent** (De Morgan's first law).

### Q9 🟡


| p | q | p OR q | NOT (p OR q) | NOT p | NOT q | (NOT p) AND (NOT q) |
|---|---|---|---|---|---|---|
| T | T | T | F | F | F | F |
| T | F | T | F | F | T | F |
| F | T | T | F | T | F | F |
| F | F | F | T | T | T | T |

**Answer:** both result columns read F, F, F, T. They are **equivalent** (De Morgan's second law).

### Q10 🟡


| p | q | NOT p | (NOT p) AND q |
|---|---|---|---|
| T | T | F | F |
| T | F | F | F |
| F | T | T | T |
| F | F | T | F |

**Answer:** an interview is booked only when p is F (not rejected) and q is T (shortlisted): the third row only.

### Q11 🟡

Helper columns: p OR q, then NOT r, then AND.

| p | q | r | p OR q | NOT r | (p OR q) AND NOT r |
|---|---|---|---|---|---|
| T | T | T | T | F | F |
| T | T | F | T | T | T |
| T | F | T | T | F | F |
| T | F | F | T | T | T |
| F | T | T | T | F | F |
| F | T | F | T | T | T |
| F | F | T | F | F | F |
| F | F | F | F | T | F |

**Answer:** **3** rows give access (T,T,F; T,F,F; F,T,F). During a lockdown (r is T) nobody gets in.

### Q12 🟡

Helper columns: NOT p, then q AND r, then OR.

| p | q | r | NOT p | q AND r | (NOT p) OR (q AND r) |
|---|---|---|---|---|---|
| T | T | T | F | T | T |
| T | T | F | F | F | F |
| T | F | T | F | F | F |
| T | F | F | F | F | F |
| F | T | T | T | T | T |
| F | T | F | T | F | T |
| F | F | T | T | F | T |
| F | F | F | T | F | T |

**Answer:** **5** rows are true: the four rows where p is F, plus the row T, T, T.

### Q13 🟡


| p | q | r | q OR r | p AND (q OR r) | p AND q | (p AND q) OR r |
|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T |
| T | T | F | T | T | T | T |
| T | F | T | T | T | F | T |
| T | F | F | F | F | F | F |
| F | T | T | T | F | F | T |
| F | T | F | T | F | F | F |
| F | F | T | T | F | F | T |
| F | F | F | F | F | F | F |

**Answer:** **not equivalent.** They differ in rows 5 (F, T, T) and 7 (F, F, T): there r is true and p is false, so the second rule is true (r alone is enough) but the first is false (it needs p). The first rule gives 3 true rows, the second gives 5. Moving a bracket changes the meaning.

### Q14 🟡


| p | q | p OR q | p AND q | (p OR q) AND NOT (p AND q) |
|---|---|---|---|---|
| T | T | T | T | F |
| T | F | T | F | T |
| F | T | T | F | T |
| F | F | F | F | F |

**Answer:** true in the rows T, F and F, T (exactly one of the two). This is the **exclusive or**.

### Q15 🟡


| p | q | NOT p | (NOT p) OR q |
|---|---|---|---|
| T | T | F | T |
| T | F | F | F |
| F | T | T | T |
| F | F | T | T |

**Answer:** **3** rows are true. The single false row is T, F: the claim is above the limit and no approval is attached.

### Q16 🔴


| p | NOT p | p OR NOT p | p AND NOT p |
|---|---|---|---|
| T | F | T | F |
| F | T | T | F |

**Answer:** "p OR NOT p" is true in every row: a **tautology** (always true). "p AND NOT p" is false in every row: a **contradiction** (always false). In data work a filter that is a contradiction returns nothing, and a tautology returns everything.

### Q17 🔴

Helper columns: i AND c, then NOT d, then g AND NOT d, then OR.

| i | c | g | d | i AND c | NOT d | g AND NOT d | approve |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | F | F | T |
| T | T | T | F | T | T | T | T |
| T | T | F | T | T | F | F | T |
| T | T | F | F | T | T | F | T |
| T | F | T | T | F | F | F | F |
| T | F | T | F | F | T | T | T |
| T | F | F | T | F | F | F | F |
| T | F | F | F | F | T | F | F |
| F | T | T | T | F | F | F | F |
| F | T | T | F | F | T | T | T |
| F | T | F | T | F | F | F | F |
| F | T | F | F | F | T | F | F |
| F | F | T | T | F | F | F | F |
| F | F | T | F | F | T | T | T |
| F | F | F | T | F | F | F | F |
| F | F | F | F | F | T | F | F |

**Answer:** **7** of the 16 rows are approved: 4 rows with i and c both true (any g, d), plus the rows with g true and d false that were not already counted (3 more).

### Q18 🔴


| p | q | r | q OR r | p AND (q OR r) | NOT (p AND (q OR r)) | (NOT q) AND (NOT r) | (NOT p) OR ((NOT q) AND (NOT r)) |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | F | F | F |
| T | T | F | T | T | F | F | F |
| T | F | T | T | T | F | F | F |
| T | F | F | F | F | T | T | T |
| F | T | T | T | F | T | F | T |
| F | T | F | T | F | T | F | T |
| F | F | T | T | F | T | F | T |
| F | F | F | F | F | T | T | T |

**Answer:** the two result columns are identical, so they are **equivalent** (De Morgan applied twice). **5** rows are true.

### Q19 🔴

The wanted column is true when p and q are the same (both T or both F). Build it from two cases joined by OR.

| p | q | p AND q | (NOT p) AND (NOT q) | (p AND q) OR ((NOT p) AND (NOT q)) |
|---|---|---|---|---|
| T | T | T | F | T |
| T | F | F | F | F |
| F | T | F | F | F |
| F | F | F | T | T |

**Answer:** (p AND q) OR ((NOT p) AND (NOT q)) gives T, F, F, T. In words: "p and q have the same truth value" (both true, or both false). Any rule with the same column is also correct.

### Q20 🔴

At least two means (a AND b) OR (a AND c) OR (b AND c).

| a | b | c | a AND b | a AND c | b AND c | alarm |
|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T |
| T | T | F | T | F | F | T |
| T | F | T | F | T | F | T |
| T | F | F | F | F | F | F |
| F | T | T | F | F | T | T |
| F | T | F | F | F | F | F |
| F | F | T | F | F | F | F |
| F | F | F | F | F | F | F |

**Answer:** the alarm rings in **4** rows (T,T,T; T,T,F; T,F,T; F,T,T). Exactly one sensor is triggered in **3** rows (T,F,F; F,T,F; F,F,T), and in those rows the alarm stays silent.

