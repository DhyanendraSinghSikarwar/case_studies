import math

# OCR sizing. OCR runs on every page, whether or not the invoice later goes straight through.
invoices, pages_per, ocr_s, window_h, util = 50_000, 2.2, 0.8, 6, 0.50
pages = invoices * pages_per
core_s = pages * ocr_s
usable_per_core = window_h * 3600 * util
assert round(pages) == 110_000 and round(core_s) == 88_000 and usable_per_core == 10_800
cores = math.ceil(core_s / usable_per_core)
assert cores == 9
print("pages:", round(pages), "| core-seconds:", round(core_s), "| usable seconds per core:", usable_per_core,
      "| cores (exact):", round(core_s / usable_per_core, 2), "-> cores:", cores)

# Human review of the non-straight-through share
stp, review_s, hours_per_person = 0.85, 90, 7
manual = round(invoices * (1 - stp))
review_hours = manual * review_s / 3600
people = math.ceil(review_hours / hours_per_person)
assert round(manual) == 7_500 and review_hours == 187.5 and people == 27
print("invoices to review:", round(manual), "| review hours:", review_hours, "| reviewers (exact):",
      round(review_hours / hours_per_person, 2), "-> reviewers:", people)

# Sensitivity: each 1 point of straight-through rate changes review load by 500 invoices = 12.5 hours = 1.8 people
per_point = round(invoices * 0.01)
assert per_point == 500 and per_point * review_s / 3600 == 12.5
print("1 point of straight-through rate = invoices:", per_point, "= hours:", per_point * review_s / 3600,
      "= people:", round(per_point * review_s / 3600 / hours_per_person, 2))
for r in (0.75, 0.80, 0.85, 0.90):
    n = math.ceil(invoices * (1 - r) * review_s / 3600 / hours_per_person)
    print(f"straight-through {r:.0%} -> reviewers {n}")
assert math.ceil(invoices * 0.25 * 90 / 3600 / 7) == 45 and math.ceil(invoices * 0.10 * 90 / 3600 / 7) == 18

# Sample size to check the straight-through error rate: 0 errors in n audited gives 95% upper bound about 3/n
n_audit = math.ceil(math.log(0.05) / math.log(1 - 0.005))
print("clean audited invoices to bound field-level error under 0.5% at 95%:", n_audit)
assert n_audit == 598
