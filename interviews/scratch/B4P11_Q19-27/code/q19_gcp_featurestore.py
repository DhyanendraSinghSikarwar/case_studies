"""Q19 Vertex side: FeatureView proto offline + deprecation-clock checker. No network."""
import warnings; warnings.filterwarnings("ignore")
from datetime import date
import importlib.metadata as md
from google.cloud.aiplatform_v1beta1.types import FeatureView
print("google-cloud-aiplatform", md.version("google-cloud-aiplatform"))

# Current design: a FeatureView syncs from a BigQuery source on a cron schedule.
fv = FeatureView(
    big_query_source=FeatureView.BigQuerySource(
        uri="bq://my-proj.fs_demo.user_features", entity_id_columns=["user_id"]),
    sync_config=FeatureView.SyncConfig(cron="0 */6 * * *"),
)
print(FeatureView.to_json(fv, indent=None))

# Deprecation clock. Dates are from search snippets of the docs-deprecations page, NOT opened.
SNIPPET_DATES = {"deprecated": date(2026, 2, 17), "no_new_features": date(2026, 5, 17), "sunset": date(2027, 2, 17)}
LEGACY = {"legacy_featurestore", "optimized_online_serving"}

def risk(design: dict, today: date) -> str:
    uses = design.get("online_serving")
    if uses not in LEGACY:
        return "ok: not on the legacy services (still check current docs)"
    if today >= SNIPPET_DATES["sunset"]:
        return "BLOCKER: past the snippet sunset date, migrate now"
    if today >= SNIPPET_DATES["no_new_features"]:
        return "HIGH: no new features expected, plan the migration this quarter"
    if today >= SNIPPET_DATES["deprecated"]:
        return "MEDIUM: deprecated, do not start new work on it"
    return "LOW: not deprecated yet by the snippet dates"

for d in [{"online_serving": "legacy_featurestore"}, {"online_serving": "bigtable"},
          {"online_serving": "optimized_online_serving"}]:
    for t in (date(2026, 1, 1), date(2026, 10, 26), date(2027, 3, 1)):
        print(t, d["online_serving"], "->", risk(d, t))
