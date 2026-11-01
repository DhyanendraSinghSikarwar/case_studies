rows, dup, avg = 200_000, 6_000, 50
rep = rows * avg
true = (rows - dup) * avg
print(f"reported {rep:,}; overstated by {dup*avg:,}; corrected {true:,}")
assert rep == 10_000_000 and dup*avg == 300_000 and true == 9_700_000
print(f"overstatement vs reported {dup/rows:.2%}, vs corrected {dup*avg/true:.2%}")
assert round(dup/rows, 4) == 0.03 and round(dup*avg/true, 4) == 0.0309
# range to send: if only some flagged rows are true duplicates
for share in (1.0, 0.5, 0.0):
    print(f"if {share:.0%} of flagged rows are real duplicates: {rep - share*dup*avg:,.0f}")
assert rep - 0.5*dup*avg == 9_850_000
