# Problem statement - Promotion Cannibalisation Engine

## Objective
Replace the promoted-SKU uplift view of a promotion with **family net contribution** = incremental margin of the promoted SKU - subsidy on baseline units - margin lost on cannibalised siblings + basket pull (halo), and recommend discounts per product family under a subsidy budget.

## KPIs
- % of proposed promos correctly classified profitable / unprofitable vs simulation truth (dashboard rule vs family-net rule).
- GBP (and INR) net contribution per promotion; family net of the reference promotion (10% off, top-24 SKUs).
- Break-even elasticity per SKU and discount, and its distribution across the assumption sweep; break-even multiplier (break-even / estimated elasticity).
- Share of assumption conditions profitable under the promoted-only view vs the family view ("dashboard trap" share).

## Constraints
- Data: UCI Online Retail II only; no cost data and no promotion flags, so margin is an assumption and promotions are inferred from non-randomised price drops.
- Offline and reproducible: seed 42, `python tasks.py all` under 15 minutes on a laptop, tests offline on a synthetic fixture.
- Every number in README / memo comes from `outputs/summary.json` written by code.

## Success criteria
1. Engine identity `family_net = direct - subsidy - cannibalised + halo` holds to 1e-6 (unit test).
2. Sweep of at least 1,000 Latin-hypercube draws, reproducible with the seed.
3. Memo reports the reference-promo family net, % profitable under both views and the break-even elasticity / multiplier.
4. Optimiser plan never exceeds the budget; the Streamlit app runs; CI (ruff + pytest) green.
5. Identification limits are stated: where price does not vary, priors and the sweep are used.

## Stakeholders
Category managers (approve promotions), pricing analytics (owner of the engine), finance (supplies margins), ISB AMPBA reviewers.
