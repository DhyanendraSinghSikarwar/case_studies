import re, json
files = ["agent1_delivery", "agent2_demand_pricing", "agent3_search_recsys", "agent4_growth", "agent5_trust_returns"]
RATE = {  # case: (stars, notebook, why)
 1: (3, "cs01_delivery_eta_prediction", "ETA / delivery-time regression with SLA-aware loss: the most-asked ML case in food and quick-commerce interviews"),
 2: (2, "cs02_prep_time_dispatch", "Prep-time estimation and its effect on dispatch: noisy-label regression and cost of lateness"),
 3: (2, "cs03_dark_store_inventory", "Demand planning for availability vs wastage plus picking batching: the newsvendor core"),
 4: (2, "cs04_rider_assignment_batching", "Assignment and batching as an optimisation problem; rolling-horizon dispatch"),
 5: (2, "cs05_delivery_promise_date", "Delivery promise with breach control: quantile regression and coverage guarantees"),
 6: (1, "cs06_address_quality_geocoding", "Address and geocoding quality: classification with clustering; narrower use"),
 7: (3, "cs07_quickcommerce_demand_forecasting", "Demand forecasting under stock-outs (censored sales): asked in every supply-chain interview"),
 8: (2, "cs08_price_elasticity_discounts", "Price elasticity and discount efficacy; interview staple but little public company method"),
 9: (2, "cs09_delivery_fee_surge_pricing", "Surge and fee design; marketplace economics, little public company method"),
 10: (1, "cs10_sale_event_capacity_planning", "Sale-event capacity planning; methods undisclosed, seasonal and peak forecasting"),
 11: (3, "cs11_new_item_demand_forecasting", "Cold-start demand forecasting for new items (fashion); strongly documented"),
 12: (2, "cs12_hierarchical_probabilistic_forecasting", "Hierarchical, probabilistic forecasting; advanced but increasingly standard"),
 13: (2, "cs13_hinglish_search_queries", "Query understanding for Hinglish; NLP evaluation in search"),
 14: (2, "cs14_visual_similarity_recommendations", "Visual similar-item retrieval with A/B-validated lift"),
 15: (3, "cs15_item_to_item_collaborative_filtering", "Item-to-item CF: the foundational recommender, asked in almost every ecommerce interview"),
 16: (2, "cs16_dish_search_ranking", "Search relevance and ranking metrics (NDCG, MRR) in food delivery"),
 17: (3, "cs17_ads_ranking_ctr_cvr", "Sponsored/organic ranking with CTR/CVR prediction and calibration: the revenue engine of marketplaces"),
 18: (2, "cs18_cold_start_exploration_bandits", "Cold start and bandit exploration for feeds"),
 19: (3, "cs19_experimentation_ab_testing", "A/B testing, variance reduction, interference and switchbacks: THE interview staple"),
 20: (3, "cs20_customer_lifetime_value", "Predicted customer LTV for acquisition bidding: asked everywhere, drives marketing spend"),
 21: (2, "cs21_membership_programme_retention", "Membership design and retention: causal measurement without randomisation"),
 22: (3, "cs22_coupon_allocation_uplift_budget", "Uplift targeting and budget-constrained coupon allocation: the core promo-optimisation problem"),
 23: (1, "cs23_push_notification_optimisation", "Notification volume and timing experiments; methods undisclosed"),
 24: (2, "cs24_marketing_mix_modelling", "Marketing-mix modelling with geo-lift calibration; common in D2C and marketplaces"),
 25: (3, "cs25_cod_rto_prediction", "COD return-to-origin prediction: imbalanced classification with a business cost; India-specific and very common"),
 26: (2, "cs26_size_fit_returns", "Size/fit prediction to cut returns in fashion"),
 27: (2, "cs27_fake_review_rating_fraud", "Rating-fraud detection with anomaly scoring"),
 28: (1, "cs28_catalogue_attribute_extraction", "Catalogue attribute extraction with multimodal models; heavy deep-learning engineering"),
 29: (2, "cs29_support_automation_resolution", "Support automation, containment vs CSAT"),
 30: (2, "cs30_buy_box_seller_quality", "Buy Box and seller quality: auditing a ranking algorithm from outside"),
}
PARTS = [(1, 6, "PART A — DELIVERY & QUICK-COMMERCE OPERATIONS"), (7, 12, "PART B — DEMAND, PRICING & SUPPLY CHAIN"), (13, 18, "PART C — SEARCH, RECOMMENDATIONS & ADS"),
         (19, 24, "PART D — GROWTH, EXPERIMENTATION & CUSTOMER VALUE"), (25, 30, "PART E — TRUST, RETURNS, RISK & SUPPORT")]
STAR = {3: "★★★ Must-visit", 2: "★★ Good to have", 1: "★ Optional"}
cases = {}; n = 0
for f in files:
    s = open(f"_build/research/{f}.md", encoding="utf-8").read()
    body, _, notes = s.partition("## Notes for the notebook author")
    open(f"_build/research/notes_{f}.md", "w", encoding="utf-8").write(notes)
    parts = re.split(r"(?m)^## Case R\d+ — ", body)[1:]
    for p in parts:
        n += 1; title, _, rest = p.partition("\n"); cases[n] = (title.strip(), rest)
assert n == 30, n
ev = {}
for k, (t, r) in cases.items():
    m = re.search(r"\*\*Evidence Level:\*\*\s*\**\s*(Strong|Medium|Weak)", r); ev[k] = m.group(1) if m else "ND"
out = ["# How Real Indian Ecommerce and Quick-Commerce Data Scientists Solved Real Business Problems", "",
 "**30 case studies from food delivery, quick commerce, marketplaces and fashion/beauty ecommerce: delivery, demand, search, ads, growth, trust and support**", "",
 "*Research compiled: 17 October 2026. All facts come from the cited public sources that the research agents actually opened. \"Not publicly disclosed\" (ND) means the sources do not state the detail. \"What a Data Scientist Can Learn\" sections are interpretation and are labelled as such.*", "",
 "---", "", "## Executive Summary", "",
 "### What was researched",
 "- Company engineering blogs (Swiggy Bytes, Zomato, Flipkart Tech, Myntra, Meesho), arXiv and conference papers by company authors (Flipkart, Myntra, Amazon, Swiggy), cloud-vendor case studies, IPO coverage and business press.",
 "- Five parallel research streams (delivery and quick-commerce operations, demand and pricing, search and recommendations, growth and customer value, trust and returns), each told to record only what it could read and to mark the rest as ND.",
 "- **Several primary pages were unreachable** (Medium, parts of Swiggy Bytes, some press sites). Where a post was read through an archive or a summary, the entry says so. Anything seen only in a search snippet was left out.", "",
 "### How well documented is each case?", "", "| Evidence | Cases | Count |", "|---|---|---|"]
for lvl in ("Strong", "Medium", "Weak"):
    out.append(f"| {lvl} | {', '.join(str(k) for k in cases if ev[k] == lvl) or '-'} | {sum(1 for k in cases if ev[k] == lvl)} |")
out += ["", "### What the research found about public disclosure",
 "1. **Method detail is public for forecasting, search, recommendations, ETA, and returns/fraud classification**, mostly through company-authored papers. Pricing, surge/fee design, sale-event planning, push notifications and marketing-mix modelling have almost no public method detail from Indian companies; those entries say so, and the notebooks treat them as **interview-standard problems solved with simulated data**, not as reproductions of any company's system.",
 "2. **Impact numbers are rare and are almost always the company's own claims.** The strongest quantified results are Flipkart's unified ads ranking (organic orders +1.36%, ad revenue +3.4%) and Myntra's visual-similarity A/B (CTR +25%, add-to-cart +4%).",
 "3. **Several cases substitute a better-documented company for the one first named** (e.g., Myntra for Flipkart on delivery promise; Meituan for Indian coupon allocation; Cabify for switchback experiments). Each entry states the substitution.",
 "4. **Cash-on-delivery and returns are India-specific problems:** Meesho's IPO documents (as reported by MediaNama) put COD at the large majority of its orders, and Flipkart's published COD study found 32% RTO in its sample.",
 "", "### Evidence legend", "", "| Level | Meaning | Shown as |", "|---|---|---|",
 "| A | Company or named employee described the project | **Strong** |", "| C | Paper / conference talk by company team | **Strong** |",
 "| B | Credible external source on the actual implementation | **Medium** |", "| D | Generic or vendor marketing with little method detail | **Weak / partially documented** |", "",
 "---", "", "<!-- PRIORITY-INDEX-START -->", "### Priority guide (added by the notebook series)", "",
 "How to read the stars: **★★★ Must-visit** = core techniques that Indian ecommerce and quick-commerce teams use every day and that interviews ask about most; study these first. **★★ Good to have** = valuable technique, narrower use or thinner public evidence. **★ Optional** = niche, or mostly deep-learning engineering. Ratings are my interpretation (frequency in industry and in interviews), not part of the sources.", "",
 "| Case | Priority | Why | Notebook | Status |", "|---|---|---|---|---|"]
for k in range(1, 31):
    st, nb, why = RATE[k]; out.append(f"| {k} | {STAR[st]} | {why} | `{nb}.ipynb` | ⏳ |")
out += ["<!-- PRIORITY-INDEX-END -->", ""]
for a, b, name in PARTS:
    out += ["---", "", f"# {name}", ""]
    for k in range(a, b + 1):
        st, nb, why = RATE[k]; title, rest = cases[k]
        out += [f"## Case Study {k} — {title}", "", f"**Priority:** {STAR[st]} — {why}. **Notebook:** `{nb}.ipynb` (⏳ notebook pending)", "", rest.strip(), ""]
out += ["---", "", "# MASTER COMPARISON TABLE", "", "| # | Priority | Case | Evidence |", "|---|---|---|---|"]
for k in range(1, 31): out.append(f"| {k} | {STAR[RATE[k][0]].split()[0]} | {cases[k][0][:110]} | {ev[k]} |")
open("indian_ecommerce_data_science_case_studies.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump({k: RATE[k] for k in RATE}, open("_build/rate.json", "w"))
print("cases", len(cases), {l: sum(1 for k in ev if ev[k] == l) for l in ("Strong", "Medium", "Weak", "ND")})
