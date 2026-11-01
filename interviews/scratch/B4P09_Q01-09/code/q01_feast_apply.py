# Q1: minimal local Feast repo: Parquet source, 1 entity, 1 feature view, SQLite online store.
import subprocess, sys, textwrap, pathlib, shutil
import pandas as pd

root = pathlib.Path(sys.argv[1]); shutil.rmtree(root, ignore_errors=True)
repo = root / "repo"; repo.mkdir(parents=True)
pd.DataFrame({
    "user_id": [1, 1, 2],
    "event_ts": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-01"]),
    "txn_count_7d": [3, 5, 1],
    "avg_amount_7d": [200.0, 220.0, 90.0],
}).to_parquet(repo / "user_stats.parquet")

(repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
    project: q01demo
    provider: local
    registry: {root}/registry.db
    online_store:
      type: sqlite
      path: {root}/online.db
    offline_store:
      type: file
    entity_key_serialization_version: 3
    """))
(repo / "definitions.py").write_text(textwrap.dedent(f"""\
    from datetime import timedelta
    from feast import Entity, FeatureView, Field, FileSource
    from feast.types import Float32, Int64
    from feast.value_type import ValueType

    user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
    src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
    user_stats = FeatureView(
        name="user_stats", entities=[user], ttl=timedelta(days=30),
        schema=[Field(name="txn_count_7d", dtype=Int64),
                Field(name="avg_amount_7d", dtype=Float32)],
        source=src)
    """))
feast = str(pathlib.Path(sys.executable).parent / "feast")
r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
print(r.stdout.strip()); print("rc =", r.returncode, r.stderr.strip()[-300:] if r.returncode else "")

from feast import FeatureStore
fs = FeatureStore(repo_path=str(repo))
print("entities     :", [(e.name, e.join_key) for e in fs.list_entities()])
for fv in fs.list_feature_views():
    print("feature view :", fv.name, "| ttl:", fv.ttl, "| features:", [f.name + ":" + str(f.dtype) for f in fv.features],
          "| source:", type(fv.batch_source).__name__)
print("data sources :", [s.name for s in fs.list_data_sources()])
print("files created:", sorted(p.name for p in root.iterdir()))
