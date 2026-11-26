# Chapter 10 answer key

Every grid puzzle (Q1 to Q3, Q5 to Q7, Q9 to Q11, Q13 to Q15) was checked by brute force over all possible arrangements: each has exactly one solution, and removing any single clue makes it ambiguous, so every clue is needed. The table problems (Q4, Q8, Q12) were checked by searching all whole-number fillings: each has exactly one. Worked examples and scenarios were checked the same way.

## Self-check answers

1. A cell is the box where one row and one column cross. The Payroll row and Contract column cell shows how many contract staff Payroll has.
2. The row totals add to 10 + 20 + 30 = 60, which is the grand total. The column totals must also add to 60, so the missing one is 60 - 25 - 15 = 20.
3. Pooja must be in Pune (last one standing: the Pune column has crosses for Neha and Om, so only Pooja can fill it). Then the rest of Pooja's row becomes crosses for the other places.

## Practice answers

### Q1

Clue 1: Omar is in Training. Naveen is not in Payroll (clue 2) and Training is taken by Omar, so Naveen is in Recruitment. Meera is left with Payroll.

|  | Team |
|---|---|
| Meera | Payroll |
| Naveen | Recruitment |
| Omar | Training |

### Q2

Clue 1 gives Sana < Rohan. Clue 2 gives Priya < Sana. Joining: Priya < Sana < Rohan. So Priya earns the lowest (30,000), Sana the middle (45,000), Rohan the highest (60,000).

| Person | Salary |
|---|---|
| Priya | 30,000 |
| Sana | 45,000 |
| Rohan | 60,000 |

### Q3

Uma is in Payroll (clue 1). Vivek works the Morning shift (clue 3). The Helpdesk person works Night (clue 2). Helpdesk cannot be Uma (Payroll), and cannot be Vivek (Morning, not Night), so Tarun is in Helpdesk on Night. Vivek is left with Compliance. Uma's shift is the one left: Evening.

| Person | Team | Shift |
|---|---|---|
| Tarun | Helpdesk | Night |
| Uma | Payroll | Evening |
| Vivek | Compliance | Morning |

### Q4

Payroll Contract = 11 - 8 = 3. Recruitment Permanent = 9 - 5 = 4. Permanent column: 8 + 4 + Training Permanent = 20, so Training Permanent = 8. Grand total 34 = 11 + 9 + Training Total, so Training Total = 14. Training Contract = 14 - 8 = 6. Contract Total = 3 + 5 + 6 = 14. Check: 20 + 14 = 34.

| | Permanent | Contract | Total |
|---|---|---|---|
| Payroll | 8 | 3 | 11 |
| Recruitment | 4 | 5 | 9 |
| Training | 8 | 6 | 14 |
| Total | 20 | 14 | 34 |

### Q5

Naveen is Monday. Meera and Zoya are on consecutive days (Zoya right after Meera) within Tuesday, Wednesday, Thursday: either Tuesday and Wednesday, or Wednesday and Thursday. If Meera is Tuesday and Zoya Wednesday, Wasim is left with Thursday, which clue 3 forbids. So Meera is Wednesday, Zoya is Thursday, and Wasim is Tuesday.

| Day | Trainee |
|---|---|
| Monday | Naveen |
| Tuesday | Wasim |
| Wednesday | Meera |
| Thursday | Zoya |

### Q6

Omar is on floor 3 (clue 1) and Priya is on floor 2 (clue 4). Sana and Rohan take floors 1 and 4; Rohan is higher (clue 6), so Rohan is on floor 4 and Sana on floor 1. Sana is in Payroll. Omar, Priya and Rohan share Recruitment, Training and Compliance. Compliance is directly above Training (clue 2), so the pair is (Training 2, Compliance 3) or (Training 3, Compliance 4); Training 1 is impossible because floor 1 is Payroll. Priya (floor 2) is not in Recruitment (clue 5), and floor 2 can only be Training (if Compliance were on floor 2, Training would have to be floor 1). So Priya is Training, Omar (floor 3) is Compliance and Rohan (floor 4) is Recruitment.

| Floor | Person | Team |
|---|---|---|
| 1 | Sana | Payroll |
| 2 | Priya | Training |
| 3 | Omar | Compliance |
| 4 | Rohan | Recruitment |

### Q7

Helpdesk has the top salary 60,000 (clue 3), so Zoya is not 60,000 (clue 6) and Zoya is 40,000 or 50,000. If Zoya were 40,000, Vivek (one step below) would be 30,000 and clue 1 would need Tarun below Zoya, but 30,000 is taken: impossible. So Zoya is 50,000 and Vivek 40,000. Tarun and Uma take 30,000 and 60,000; Zoya earns more than Tarun, so Tarun is 30,000 and Uma is 60,000. Uma earns the most, so Uma is in Helpdesk. Tarun is in Training. Vivek (40,000) and Zoya (50,000) are in Recruitment and Payroll; Recruitment earns less than Payroll, so Vivek is Recruitment and Zoya is Payroll.

| Salary | Person | Team |
|---|---|---|
| 30,000 | Tarun | Training |
| 40,000 | Vivek | Recruitment |
| 50,000 | Zoya | Payroll |
| 60,000 | Uma | Helpdesk |

### Q8

Payroll Tue = 9 - 3 - 2 = 4. Recruitment Mon = 8 - 3 - 1 = 4 (Monday column). Recruitment Wed = 10 - 4 - 4 = 2. Training Wed = 9 - 2 - 2 = 5 (Wednesday column). Training Total = 1 + 5 + 5 = 11. Tuesday Total = 4 + 4 + 5 = 13. Grand total = 8 + 13 + 9 = 30, and also 9 + 10 + 11 = 30. Tuesday has the most late arrivals (13).

| | Mon | Tue | Wed | Total |
|---|---|---|---|---|
| Payroll | 3 | 4 | 2 | 9 |
| Recruitment | 4 | 4 | 2 | 10 |
| Training | 1 | 5 | 5 | 11 |
| Total | 8 | 13 | 9 | 30 |

### Q9

Accountant is 11am (clue 1). The Recruiter interview is later than 11am, so it is 12pm (clue 5). Analyst and Trainer take 9am and 10am. Sana is immediately before the Analyst (clue 2), so the Analyst cannot be 9am (nobody can be before it): Analyst is 10am, Sana is 9am, and the 9am role is Trainer. Meera, Naveen and Rohan share 10am, 11am and 12pm. Naveen is not 12pm (clue 4) and Meera is earlier than Naveen (clue 3), so Meera 10am, Naveen 11am, Rohan 12pm.

| Time | Interviewer | Role |
|---|---|---|
| 9am | Sana | Trainer |
| 10am | Meera | Analyst |
| 11am | Naveen | Accountant |
| 12pm | Rohan | Recruiter |

### Q10

Priya is January. Sana and Rohan are not April, and Priya is January, so Omar is April. Omar did not take Earned (clue 3) and Sana took Comp-off, so Omar took Sick or Casual. Sick cannot be April (Casual would have to be the month after), so Omar took Casual, and Sick was March. Sana has Comp-off, so the March Sick leave is Rohan's; Sana is February. Priya has the remaining kind, Earned.

| Month | Person | Leave |
|---|---|---|
| Jan | Priya | Earned |
| Feb | Sana | Comp-off |
| Mar | Rohan | Sick |
| Apr | Omar | Casual |

### Q11

Naveen is at desk 1 and is Training (clues 1 and 3). Omar is at desk 2 (clue 7). Meera, Priya and Rohan fill desks 3 to 5. Rohan is not at an end (clue 4), so Rohan is at desk 4. Meera is left of Priya (clue 2), so Meera is 3 and Priya is 5. Payroll is desk 5 (Priya). Rohan (desk 4) is two desks right of Compliance, so Compliance is desk 2 (Omar). Recruitment is next to Compliance: desk 1 is Training, so Recruitment is desk 3 (Meera). Helpdesk is left: desk 4 (Rohan).

| Desk | Person | Team |
|---|---|---|
| 1 | Naveen | Training |
| 2 | Omar | Compliance |
| 3 | Meera | Recruitment |
| 4 | Rohan | Helpdesk |
| 5 | Priya | Payroll |

### Q12

Let Payroll Senior be s. Payroll: 6 + Mid + s = 15, so Payroll Mid = 9 - s. Mid column: Payroll Mid + Recruitment Mid + 8 = 17, so Recruitment Mid = 9 - (9 - s) = s. Recruitment: Junior + s + 2 = 14, so Recruitment Junior = 12 - s. Junior column: 6 + (12 - s) + Training Junior = 20, so Training Junior = 2 + s. Training Senior = s + 3 (clue). Training Total = 50 - 15 - 14 = 21 (grand total minus the other two rows), so Training Junior + 8 + Training Senior = 21, i.e. (2 + s) + 8 + (s + 3) = 21, giving 2s + 13 = 21 and s = 4. Then Payroll Mid 5, Recruitment Mid 4, Recruitment Junior 8, Training Junior 6, Training Senior 7. Senior total = 4 + 2 + 7 = 13. Check: columns 20 + 17 + 13 = 50.

| | Junior | Mid | Senior | Total |
|---|---|---|---|---|
| Payroll | 6 | 5 | 4 | 15 |
| Recruitment | 8 | 4 | 2 | 14 |
| Training | 6 | 8 | 7 | 21 |
| Total | 20 | 17 | 13 | 50 |

### Q13

Uma is Monday and Tarun is Tuesday, with the Leave audit (clues 4, 5, 2). The Payroll audit must be earlier than Tuesday, so it is Monday: Uma audits Payroll. Vivek, Wasim and Zoya share Wednesday to Friday. Zoya does the Training audit, and the Expense audit is on Wednesday, so Zoya is not Wednesday. If Zoya were Thursday, Vivek and Wasim would take Wednesday and Friday; Wasim is not Friday, so Wasim Wednesday and Vivek Friday, which breaks 'Vivek earlier than Wasim'. So Zoya is Friday. Then Vivek is Wednesday and Wasim Thursday (clue 3). Vivek does the Expense audit (Wednesday) and Wasim the remaining area, Recruitment.

| Day | Auditor | Area |
|---|---|---|
| Monday | Uma | Payroll |
| Tuesday | Tarun | Leave |
| Wednesday | Vivek | Expense |
| Thursday | Wasim | Recruitment |
| Friday | Zoya | Training |

### Q14

Priya has rank 4 (clue 5) and the Delhi person has rank 4 (clue 3), so Priya is in Delhi. Omar is in Payroll (clue 8). The Kolkata person works in Recruitment, so Kolkata is not Omar (Payroll) and not Priya (Delhi); it is not Sana (clue 6), so it is Rohan: Rohan is in Kolkata, in Recruitment. The Kolkata person has a lower rank than the Pune person (clue 4), so the Pune person ranks above Rohan; Pune is Omar or Sana. Rohan ranks above Sana (clue 7), so Sana cannot be the Pune person (she ranks below Rohan). So Omar is in Pune and Sana in Chennai. Ranks: Priya 4; Omar > Rohan > Sana, so Omar 3, Rohan 2, Sana 1. The Training person ranks above the Payroll person (Omar, rank 3), so Training is rank 4: Priya. Sana has the last team, Helpdesk.

| Rank | Person | Team | City |
|---|---|---|---|
| 1 | Sana | Helpdesk | Chennai |
| 2 | Rohan | Recruitment | Kolkata |
| 3 | Omar | Payroll | Pune |
| 4 | Priya | Training | Delhi |

### Q15

Meera is G5 and Naveen is G2. The Helpdesk person is G1. Tarun (Recruitment) cannot be G1, and Zoya is lower than Uma (clue 10), so Uma cannot be G1 (nobody would be lower). So Zoya is G1 in Helpdesk. Tarun and Uma take G3 and G4. Teams left for Naveen, Meera and Uma: Payroll, Training, Compliance. Compliance is directly above Training (clue 6), and the Recruitment person (Tarun) is above the Payroll person (clue 11). Try Tarun G4, Uma G3: Payroll must be below G4, so Payroll is Naveen (G2) or Uma (G3); either way the remaining two among Naveen G2, Meera G5, Uma G3 cannot be neighbours (G2 and G5, or G3 and G5 are not adjacent), so this fails. So Tarun is G3 and Uma is G4. Payroll must be below G3: Naveen (G2) is Payroll. Meera (G5) and Uma (G4) are Compliance and Training with Compliance above: Meera Compliance, Uma Training. Cities: Uma is Kolkata; Payroll is Pune, so Naveen is in Pune. The remaining cities Delhi, Chennai, Jaipur go to Zoya, Tarun, Meera. Zoya (Helpdesk) is not Chennai (clue 7). Zoya is G1, the lowest, so she cannot be the Delhi person (Delhi must be above Chennai). So Zoya is in Jaipur. Delhi is above Chennai, so Meera (G5) is Delhi and Tarun (G3) is Chennai.

| Grade | Person | Team | City |
|---|---|---|---|
| G1 | Zoya | Helpdesk | Jaipur |
| G2 | Naveen | Payroll | Pune |
| G3 | Tarun | Recruitment | Chennai |
| G4 | Uma | Training | Kolkata |
| G5 | Meera | Compliance | Delhi |

