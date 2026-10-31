# All money figures illustrative, from the prompt
docs, changed_per_month = 4000, 600
retrain, reindex = 2000, 300
yr_retrain, yr_reindex = 12*retrain, 12*reindex
print(f"yearly: retrain {yr_retrain:,} vs re-index {yr_reindex:,}; difference {yr_retrain-yr_reindex:,}; ratio {yr_retrain/yr_reindex:.1f}x")
assert (yr_retrain, yr_reindex) == (24000, 3600) and yr_retrain - yr_reindex == 20400 and round(yr_retrain/yr_reindex, 1) == 6.7
print(f"churn: {changed_per_month/docs:.0%} of documents per month, {12*changed_per_month:,} document updates a year")
assert changed_per_month/docs == 0.15 and 12*changed_per_month == 7200
# Per-document unit cost
print(f"retrain {retrain/changed_per_month:.2f} per changed doc; re-index {reindex/changed_per_month:.2f} per changed doc")
assert round(retrain/changed_per_month, 2) == 3.33 and reindex/changed_per_month == 0.5
# The comparison is incomplete: retrieval adds input tokens to every query. Illustrative: +1,500 context tokens at 3 per million.
extra_per_query = 1500*3/1e6
be_queries = (retrain - reindex) / extra_per_query
print(f"retrieval context costs {extra_per_query:.4f} per query; the 1,700/month saving is wiped out above {be_queries:,.0f} queries/month")
assert round(extra_per_query, 4) == 0.0045 and round(be_queries) == 377778
for q in (100_000, 1_000_000):
    print(f"{q:>9,} queries/month: retrieval tokens cost {q*extra_per_query:,.0f}/month vs the 1,700 gap")
assert round(100_000*extra_per_query) == 450 and round(1_000_000*extra_per_query) == 4500
# Freshness: lag between a policy change and the model knowing it
print("lag: re-index minutes to hours; monthly retrain up to 30 days (plus eval time)")
