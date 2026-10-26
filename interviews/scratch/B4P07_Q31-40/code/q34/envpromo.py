"""Ordered promotion: a version must hold the staging alias before it can become champion."""
import json, pathlib, time
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

ORDER = ["staging", "champion"]

class PromotionError(Exception):
    pass

def _ledger(path, **row):
    row["ts"] = round(time.time(), 3)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")

def promote(client, name, version, target, actor, ledger_path):
    version = str(version)
    if target not in ORDER:
        raise PromotionError(f"unknown environment {target!r}")
    try:
        mv = client.get_model_version(name, version)
    except MlflowException:
        raise PromotionError(f"version {version} of {name} does not exist")
    if target == "champion" and mv.tags.get("reached_staging") != "true":
        raise PromotionError(f"v{version} never reached staging; refusing to skip it")
    try:
        current = str(client.get_model_version_by_alias(name, target).version)
    except MlflowException:
        current = None
    if current == version:                      # idempotent re-run
        return "noop"
    client.set_registered_model_alias(name, target, version)
    if target == "staging":
        client.set_model_version_tag(name, version, "reached_staging", "true")
    client.set_model_version_tag(name, version, f"promoted_to_{target}_by", actor)
    _ledger(ledger_path, name=name, version=version, env=target, previous=current, actor=actor)
    return "moved"
