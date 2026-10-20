---

# Case Study 14 — ShopLook visual similar-item recommendations (Myntra) · `cs14_visual_similarity_recommendations.ipynb`

## D-14-01: Data source — simulated image embeddings with a hidden visual identity

- Date: 2026-10-20
- Case: 14
- Context / question: Myntra's images and labels are not public and the brief forbids real images and deep nets; we still need relevance truth and an online twin.
- Options considered: Street2Shop (real images, US-centric, no similarity truth); simulated embeddings with a hidden 14-dimension identity.
- Decision: 6,000 items (plus 60 near-duplicates), 10 types in the 5 documented groups, 2,500 outfits, frozen 64-dim embeddings with nuisance and domain shift.
- Why: Relevance, exact-item recall and a digital-twin A/B can all be defined.
- Assumption checks / evidence: Model-photo cosine to the catalogue photo 0.59, street 0.48; 90 failed embeddings, 59 of 60 duplicates caught.
- Impact if wrong / mitigation: Gaps depend on the nuisance we simulated; re-measure on real images. Public method detail is thin; this is not a reproduction.

## D-14-02: Evaluation protocol — per-type retrieval, self excluded, strict and lenient relevance

- Date: 2026-10-20
- Case: 14
- Context / question: How do we score similar-item retrieval fairly?
- Options considered: strict label match only; lenient only; both plus exact-item recall.
- Decision: Retrieve inside the detected article type, exclude the worn item, report NDCG@5, strict and lenient P@K and exact-item recall; outfit-cluster bootstrap CIs.
- Why: Garments in one outfit share a photo; the paper's P@K and expert review disagree.
- Assumption checks / evidence: Intra-outfit correlation 0.016, design effect 1.02; 6,166 detected garments scored.
- Impact if wrong / mitigation: The lenient rule is ours; confirm with real human judgements.

## D-14-03: Use a supervised (triplet-trained) embedding, not a frozen one

- Date: 2026-10-20
- Case: 14
- Context / question: Which embedding powers retrieval?
- Options considered: best-sellers, colour histogram, frozen Euclidean, frozen cosine, PCA-whitened, triplet-trained linear projection.
- Decision: Triplet-trained embedding (fixed settings, 24 dims).
- Why: NDCG@5 0.563 (CI 0.556 to 0.570) vs 0.351 frozen cosine; exact-item recall@5 86.7% vs 25.2%; Holm p < 0.0001 against all but the colour histogram on hit-once.
- Assumption checks / evidence: PCA-whitening hurt (0.269); dimension check 0.519/0.541/0.563/0.537 for 8/16/24/48.
- Impact if wrong / mitigation: A linear stand-in for a ResNet50 network; real gaps may differ.

## D-14-04: Keep funding active learning, aimed at skirts and bags

- Date: 2026-10-20
- Case: 14
- Context / question: Where does the detector limit the product?
- Options considered: accept the detector; active-learning loop on weak groups; crop-quality gate.
- Decision: Continue active learning, prioritise skirts and bags, add a crop-quality check.
- Why: End-to-end success rose in every group (Holm p < 0.0001): skirts 51.0% to 68.5%, bags 67.0% to 75.3%; full-outfit coverage 49.2% to 59.6%; badly cut crops 90.3% relevant vs 99.0%.
- Assumption checks / evidence: Documented group APs used as detection probabilities (AP is not recall).
- Impact if wrong / mitigation: Funnel is directional; measure real recall per type.

## D-14-05: Report strict and human-judged relevance together

- Date: 2026-10-20
- Case: 14
- Context / question: Why is P@K low when experts say results look right?
- Options considered: strict label match; lenient; simulated expert review.
- Decision: Use strict P@K for regression tests and a human-judged share for go/no-go.
- Why: Trained embedding strict P@3 45.3% vs lenient 79.9% (gap 34.6 points, CI 33.8 to 35.4); simulated review 77.4% (CI 73.5% to 80.8%, kappa 0.70).
- Assumption checks / evidence: The documented 477/500 (95.4%) is above our CI; we do not match it.
- Impact if wrong / mitigation: Our expert rule and 5% annotator error are assumptions.

## D-14-06: Offline rank screens; the A/B decides

- Date: 2026-10-20
- Case: 14
- Context / question: Can offline metrics replace an online test?
- Options considered: offline only; digital-twin check; live A/B.
- Decision: Treat offline rank as a screen only.
- Why: Spearman between NDCG@5 and twin click-through is +0.09 (p = 0.87); the colour histogram is second offline but near last online; best-sellers beat frozen embeddings on clicks (5.6% vs 4.3%).
- Assumption checks / evidence: Trained embedding best on both (CTR 6.28%, add-to-cart 1.43%); the twin's click model is assumed.
- Impact if wrong / mitigation: The documented +25% CTR and +4% add-to-cart have no known control; our lifts do not test them.

## D-14-07: A/B design — clicks first, add-to-cart as a long readout

- Date: 2026-10-20
- Case: 14
- Context / question: How big must the test be?
- Options considered: click-through primary; add-to-cart primary.
- Decision: Primary metric click-through (about 1,735 users per arm for +25%); add-to-cart pooled or long.
- Why: A +4% add-to-cart lift needs about 4.7 lakh users per arm; with 5 lakh carousels per arm the minimum detectable lift is 2.4% (clicks) and 6.8% (add-to-cart).
- Assumption checks / evidence: Twin control rates 5.58% and 0.77%; 3 carousels per user, ICC 0.05 (assumed).
- Impact if wrong / mitigation: Re-size with real control rates.

## D-14-08: Business case — about ₹98 crore a year, with a wide range

- Date: 2026-10-20
- Case: 14
- Context / question: What is it worth?
- Options considered: twin lift with 50% incrementality; best and worst cases.
- Decision: Base ₹98 crore a year gross over best-sellers (best ₹141 crore, worst ₹27 crore) against an assumed ₹3 crore cost; active learning alone about ₹12 crore.
- Why: 60 lakh views a day, 2.88 garments per image, 30% cart-to-order, ₹1,150 order, 16% margin (all assumed); worst halves the lift and uses the pre-active-learning detector.
- Assumption checks / evidence: Positive in all scenarios; brute-force search about 15 to 17 ms per query at 2 lakh items, so approximate nearest-neighbour search is needed at scale.
- Impact if wrong / mitigation: Treat the figure as an order of magnitude; rely on the method ranking.
