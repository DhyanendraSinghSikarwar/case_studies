# Helper shared by the Feast demos: builds a throw-away local repo and runs `feast apply`.
import pathlib, shutil, subprocess, sys, textwrap
import pandas as pd

def make_repo(root, df, ttl_days=30, project="demo"):
    root = pathlib.Path(root); shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"; repo.mkdir(parents=True)
    df.to_parquet(repo / "user_stats.parquet")
    (repo / "feature_store.yaml").write_text(textwrap.dedent(f"""\
        project: {project}
        provider: local
        registry: {root}/registry.db
        online_store:
          type: sqlite
          path: {root}/online.db
        offline_store:
          type: file
        entity_key_serialization_version: 3
        """))
    ttl = f"timedelta(days={ttl_days})" if ttl_days else "None"
    (repo / "definitions.py").write_text(textwrap.dedent(f"""\
        from datetime import timedelta
        from feast import Entity, FeatureView, Field, FileSource
        from feast.types import Float32, Int64
        from feast.value_type import ValueType
        user = Entity(name="user", join_keys=["user_id"], value_type=ValueType.INT64)
        src = FileSource(path="{repo}/user_stats.parquet", timestamp_field="event_ts")
        user_stats = FeatureView(name="user_stats", entities=[user], ttl={ttl},
            schema=[Field(name="txn_count_7d", dtype=Int64), Field(name="avg_amount_7d", dtype=Float32)],
            source=src)
        """))
    feast = str(pathlib.Path(sys.executable).parent / "feast")
    r = subprocess.run([feast, "apply"], cwd=repo, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    return repo

def write_rows(repo, df):
    df.to_parquet(pathlib.Path(repo) / "user_stats.parquet")
