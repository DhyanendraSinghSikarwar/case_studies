"""Approval tags + separation of duties on an MLflow registry (sqlite)."""
import datetime as dt
import sys

from mlflow import MlflowClient


class PromotionRefused(Exception):
    pass


def approve(client, name, version, approver, gate_report_url, workflow_run_id, break_glass_reason=None):
    mv = client.get_model_version(name, str(version))
    author = mv.tags.get("author")
    if not author:
        raise PromotionRefused("version has no author tag; cannot check separation of duties")
    if approver == author:
        raise PromotionRefused(f"approver '{approver}' is the author; a second person must approve")
    if not gate_report_url and not break_glass_reason:
        raise PromotionRefused("gate_report URL is required (or a break-glass reason)")
    tags = {
        "approved_by": approver,
        "approved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "gate_report": gate_report_url or "none",
        "workflow_run_id": str(workflow_run_id),
    }
    if break_glass_reason:
        tags["break_glass"] = "true"
        tags["break_glass_reason"] = break_glass_reason
    for k, v in tags.items():
        client.set_model_version_tag(name, str(version), k, v)
    return tags


def promote(client, name, version, alias="champion"):
    mv = client.get_model_version(name, str(version))
    for need in ("approved_by", "gate_report", "workflow_run_id"):
        if need not in mv.tags:
            raise PromotionRefused(f"cannot promote: tag '{need}' missing")
    client.set_registered_model_alias(name, alias, str(version))
    return alias


if __name__ == "__main__":
    # tiny CLI: approve.py <tracking_uri> <name> <version> <approver> <report_url> <run_id>
    uri, name, ver, who, url, run = sys.argv[1:7]
    c = MlflowClient(tracking_uri=uri, registry_uri=uri)
    try:
        approve(c, name, ver, who, url, run)
        promote(c, name, ver)
        print(f"promoted {name} v{ver} to champion, approved by {who}")
    except PromotionRefused as e:
        print("REFUSED:", e)
        sys.exit(1)
