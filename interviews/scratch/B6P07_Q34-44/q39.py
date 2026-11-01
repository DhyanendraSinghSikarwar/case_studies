# Illustrative numbers from the prompt
uploads, flagged, minutes = 50_000, 1_000, 5
print("flag rate:", flagged / uploads)
assert flagged / uploads == 0.02

hours = flagged * minutes / 60
print(f"review: {flagged} files x {minutes} min = {hours:.1f} hours = {hours/40:.1f} person-weeks of 40 h")
assert round(hours, 1) == 83.3 and round(hours / 40, 1) == 2.1

# Scanning alone is not enough: the unflagged 49,000 files are never read.
# Invented scenario: 100 truly poisoned files in 50,000, scanner catches 80 of them (80% recall).
poisoned, caught = 100, 80
missed = poisoned - caught
precision = caught / flagged
print(f"poisoned files that slip through: {missed}; share of flagged files that are truly poisoned: {precision:.0%}")
assert missed == 20 and precision == 0.08

# Audit a random sample of the UNflagged files to estimate the miss rate
unflagged = uploads - flagged
sample = 490
audit_hours = sample * minutes / 60
print(f"audit {sample} of {unflagged} unflagged files: {audit_hours:.1f} hours")
assert unflagged == 49_000 and round(audit_hours, 1) == 40.8
# If the audit finds zero poisoned files, the 'rule of three' upper bound (95%) on the unflagged poison rate is 3/n
ub = 3 / sample
print(f"zero found -> upper bound {ub:.2%} of unflagged files, i.e. up to {ub*unflagged:.0f} files")
assert round(ub * 100, 2) == 0.61 and round(ub * unflagged) == 300
# so a clean audit does not show the corpus is clean; it bounds it. Architecture must limit the damage.
