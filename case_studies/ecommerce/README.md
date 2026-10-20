# Indian Ecommerce and Quick-Commerce Data Science: 30 Case Studies, Solved End to End

A companion to the fintech case-study project. Thirty problems that Indian ecommerce, quick-commerce, food-delivery and marketplace data-science teams actually work on, and that interviews ask about: delivery ETA, demand forecasting, recommendations and search, ads ranking, A/B testing, customer lifetime value, coupon uplift, COD return-to-origin, and more. Each case is rated **★★★ Must-visit**, **★★ Good to have** or **★ Optional** (frequency in industry and in interviews).

Each notebook follows the same structure as the fintech series: a plain-English explanation for business leaders, what the company documented vs what we simulate, hypotheses, data and data-quality checks, EDA, **statistics as the core** (assumptions, effect sizes, CIs, power, multiple testing, written observations), a short ML section, a ₹ business case with best/base/worst scenarios, recommendation and KPIs, risks and an appendix of formulas and glossary.

> ⚠️ **All outcome data is synthetic.** Company logs are confidential. Generators are calibrated to figures the cited public sources actually state. Public method detail is thin for several problems (pricing, surge fees, sale-event planning, push notifications, marketing-mix modelling): for those, the reference file says so and the notebook is an **interview-standard solution on simulated data**, not a reproduction of any company's system. See `indian_ecommerce_data_science_case_studies.md` for the sourced case write-ups with evidence levels, and `decision.md` for every sourcing and design decision.

## How to run

```bash
pip install -r requirements.txt
python -m ipykernel install --user --name fintech-cases --display-name "Python 3.12 (fintech-cases)"   # same kernel name as the fintech project
jupyter nbconvert --to notebook --execute --inplace cs01_delivery_eta_prediction.ipynb               # regenerates its data in data/
# If `jupyter` is not on PATH: python -m nbconvert --to notebook --execute --inplace <file>
```

- Random seed = 42 everywhere (independent child streams via `SeedSequence(42)` where several random processes interact).
- Each notebook writes its generator to `data/generate_*.py` and regenerates its data in `data/<case>/`.
- `_build/nbtool.py` is the authoring tool (source to notebook, execute, dump, fill written observations, verify, update this table). It is not needed to run the notebooks. `_build/research/` holds the raw research notes.

<!-- CASE-INDEX-START -->
## All 30 case studies: priority and notebook status

Stars: **★★★ Must-visit** · **★★ Good to have** · **★ Optional**.

| Case | Priority | Notebook | Status | Core technique | Public evidence |
|---|---|---|---|---|---|
| 1 | ★★★ Must-visit | `cs01_delivery_eta_prediction.ipynb` | ✅ built & verified | ETA / delivery-time regression with SLA-aware loss: the most-asked ML case in food and quick-commerce interviews | Strong |
| 2 | ★★ Good to have | `cs02_prep_time_dispatch.ipynb` | ⏳ pending | Prep-time estimation and its effect on dispatch: noisy-label regression and cost of lateness | Strong |
| 3 | ★★ Good to have | `cs03_dark_store_inventory.ipynb` | ⏳ pending | Demand planning for availability vs wastage plus picking batching: the newsvendor core | Strong |
| 4 | ★★ Good to have | `cs04_rider_assignment_batching.ipynb` | ⏳ pending | Assignment and batching as an optimisation problem; rolling-horizon dispatch | Strong |
| 5 | ★★ Good to have | `cs05_delivery_promise_date.ipynb` | ⏳ pending | Delivery promise with breach control: quantile regression and coverage guarantees | Strong |
| 6 | ★ Optional | `cs06_address_quality_geocoding.ipynb` | ⏳ pending | Address and geocoding quality: classification with clustering; narrower use | Strong |
| 7 | ★★★ Must-visit | `cs07_quickcommerce_demand_forecasting.ipynb` | ✅ built & verified | Demand forecasting under stock-outs (censored sales): asked in every supply-chain interview | Medium |
| 8 | ★★ Good to have | `cs08_price_elasticity_discounts.ipynb` | ⏳ pending | Price elasticity and discount efficacy; interview staple but little public company method | Weak |
| 9 | ★★ Good to have | `cs09_delivery_fee_surge_pricing.ipynb` | ⏳ pending | Surge and fee design; marketplace economics, little public company method | Weak |
| 10 | ★ Optional | `cs10_sale_event_capacity_planning.ipynb` | ⏳ pending | Sale-event capacity planning; methods undisclosed, seasonal and peak forecasting | Weak |
| 11 | ★★★ Must-visit | `cs11_new_item_demand_forecasting.ipynb` | ⏳ pending | Cold-start demand forecasting for new items (fashion); strongly documented | Strong |
| 12 | ★★ Good to have | `cs12_hierarchical_probabilistic_forecasting.ipynb` | ⏳ pending | Hierarchical, probabilistic forecasting; advanced but increasingly standard | Medium |
| 13 | ★★ Good to have | `cs13_hinglish_search_queries.ipynb` | ⏳ pending | Query understanding for Hinglish; NLP evaluation in search | Medium |
| 14 | ★★ Good to have | `cs14_visual_similarity_recommendations.ipynb` | ⏳ pending | Visual similar-item retrieval with A/B-validated lift | Strong |
| 15 | ★★★ Must-visit | `cs15_item_to_item_collaborative_filtering.ipynb` | ✅ built & verified | Item-to-item CF: the foundational recommender, asked in almost every ecommerce interview | Strong |
| 16 | ★★ Good to have | `cs16_dish_search_ranking.ipynb` | ⏳ pending | Search relevance and ranking metrics (NDCG, MRR) in food delivery | Strong |
| 17 | ★★★ Must-visit | `cs17_ads_ranking_ctr_cvr.ipynb` | ⏳ pending | Sponsored/organic ranking with CTR/CVR prediction and calibration: the revenue engine of marketplaces | Strong |
| 18 | ★★ Good to have | `cs18_cold_start_exploration_bandits.ipynb` | ⏳ pending | Cold start and bandit exploration for feeds | Medium |
| 19 | ★★★ Must-visit | `cs19_experimentation_ab_testing.ipynb` | ⏳ pending | A/B testing, variance reduction, interference and switchbacks: THE interview staple | Medium |
| 20 | ★★★ Must-visit | `cs20_customer_lifetime_value.ipynb` | ⏳ pending | Predicted customer LTV for acquisition bidding: asked everywhere, drives marketing spend | Medium |
| 21 | ★★ Good to have | `cs21_membership_programme_retention.ipynb` | ⏳ pending | Membership design and retention: causal measurement without randomisation | Weak |
| 22 | ★★★ Must-visit | `cs22_coupon_allocation_uplift_budget.ipynb` | ⏳ pending | Uplift targeting and budget-constrained coupon allocation: the core promo-optimisation problem | Strong |
| 23 | ★ Optional | `cs23_push_notification_optimisation.ipynb` | ⏳ pending | Notification volume and timing experiments; methods undisclosed | Weak |
| 24 | ★★ Good to have | `cs24_marketing_mix_modelling.ipynb` | ⏳ pending | Marketing-mix modelling with geo-lift calibration; common in D2C and marketplaces | Weak |
| 25 | ★★★ Must-visit | `cs25_cod_rto_prediction.ipynb` | ⏳ pending | COD return-to-origin prediction: imbalanced classification with a business cost; India-specific and very common | Strong |
| 26 | ★★ Good to have | `cs26_size_fit_returns.ipynb` | ⏳ pending | Size/fit prediction to cut returns in fashion | Strong |
| 27 | ★★ Good to have | `cs27_fake_review_rating_fraud.ipynb` | ⏳ pending | Rating-fraud detection with anomaly scoring | Strong |
| 28 | ★ Optional | `cs28_catalogue_attribute_extraction.ipynb` | ⏳ pending | Catalogue attribute extraction with multimodal models; heavy deep-learning engineering | Medium |
| 29 | ★★ Good to have | `cs29_support_automation_resolution.ipynb` | ⏳ pending | Support automation, containment vs CSAT | Medium |
| 30 | ★★ Good to have | `cs30_buy_box_seller_quality.ipynb` | ⏳ pending | Buy Box and seller quality: auditing a ranking algorithm from outside | Medium |
<!-- CASE-INDEX-END -->
