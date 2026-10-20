# ISB AMPBA — Top 10 Case Studies

Master plan: [docs/ISB_AMPBA_Top10_CaseStudies_Plan.md](docs/ISB_AMPBA_Top10_CaseStudies_Plan.md)

## One-time setup
Run `install_skills.bat` (double-click) or `powershell -ExecutionPolicy Bypass -File .\install_skills.ps1` — or just ask Claude Code "set up the skills". Then restart Claude Code in this folder.

## How to start (in Claude Code, from this folder)
```text
/ampba-new-project 01
```
Then:
```text
/ampba-build-milestone 01 M1
```
Repeat M2..M5, run `/ampba-review 01 mid` after M3 and `/ampba-review 01 final` after M5, then `/ampba-decision-memo 01`.

## Progress tracker
| # | Case study | Spec | M1 | M2 | M3 | Mid-review | M4 | M5 | Final review | Memo |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Credit Risk Scorecard & Limit Engine | [spec](case-studies/01-credit-risk-scorecard.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 02 | T&E Fraud Detection + GenAI Audit Copilot | [spec](case-studies/02-tne-fraud-genai-audit.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 03 | Agentic Credit Underwriting | [spec](case-studies/03-agentic-credit-underwriting.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 04 | NSE Factor Screener & Backtester | [spec](case-studies/04-nse-factor-backtester.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 05 | Promotion Cannibalisation Engine | [spec](case-studies/05-promotion-cannibalisation.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 06 | RFM, CLV, Market Basket & Recommender | [spec](case-studies/06-rfm-clv-basket-recsys.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 07 | Churn + Uplift Retention | [spec](case-studies/07-churn-uplift-retention.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 08 | Two-sided Marketplace Pricing | [spec](case-studies/08-two-sided-marketplace-pricing.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 09 | Dark-store Forecasting & Serviceability | [spec](case-studies/09-darkstore-forecast-serviceability.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Review Intelligence + RAG Copilot | [spec](case-studies/10-review-intelligence-rag.md) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

Recommended order: 01 → 05 → 06 → 07 → 02 → 08 → 04 → 09 → 03 → 10.
