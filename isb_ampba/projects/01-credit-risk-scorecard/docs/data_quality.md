# Data quality notes (UCI 350)

Counts are in `outputs/data_quality.json` (written by `analysis/run_analysis.py`).

1. No nulls; all 24 columns are integers. Row count and default rate are asserted in `validate.py`.
2. `EDUCATION` has undocumented codes 0, 5, 6 -> mapped to 4 ("others"). `MARRIAGE` 0 -> 3.
3. `PAY_*` codes: -2 (no consumption), -1 (paid in full), 0 (revolving credit), 1-9 months delayed. -2/-1/0 all mean "no delay" in the delay features.
4. There is no `PAY_1`; the columns are `PAY_0, PAY_2 ... PAY_6` (`PAY_0` = September, the latest month).
5. `BILL_AMT*` can be negative (credit balance). Rows are kept; utilisation can therefore be negative.
6. Exact duplicate rows exist; they are kept (immaterial) - decision recorded in README "Decisions".
7. Month alignment: the payment made in month i settles the bill of month i+1 (see `features.py`).
8. Amounts are NT$; INR conversion (`fx_ntd_inr`) is applied only to business outputs.
9. `AGE` is in [21, 79]; `SEX` in {1, 2}; `SEX` is excluded from models.
10. Single snapshot (Apr-Sep 2005): no true time ordering, hence a stratified random split and no out-of-time test.
