# Data quality and identifiability (generated from outputs/summary.json)

| Check | Value |
|---|---|
| Clean sales lines | 1,036,875 |
| Invoices / SKUs | 39,514 / 4,706 |
| Revenue | £19,863,342 |
| Date range | 2009-12-01 to 2011-12-09 |
| Q4 (Oct-Dec) revenue share | 37.9% |
| SKU-weeks (modal-price panel) | 196,142 |
| Consecutive-week pairs | 152,246 |
| Modal price changed > 1% / > 5% | 31.6% / 30.7% |
| Modal price dropped > 5% / > 10% | 15.0% / 14.3% |
| SKUs with enough price drops | 1,787 |
| SKUs identifiable (enough weeks and drops) | 1,593 |
| SKUs with one price only | 584 |

Counts differ slightly from the plan's DATA.md because this project also (a) keeps only 5-digit-prefixed product codes, (b) upper-cases stock codes and (c) drops two fully-cancelled bulk orders (see README Deviations).
