"""Promote a registry version to an alias. Idempotent. Exit 0 ok, 2 refused."""
import argparse, os, sys, datetime
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException


def promote(client, name, version, alias="champion", who="unknown", run_url=""):
    try:
        mv = client.get_model_version(name, str(version))
    except MlflowException as e:
        return 2, f"REFUSED: version {version} of {name} not found ({e.error_code})"
    if mv.tags.get("gate") != "passed":
        return 2, f"REFUSED: version {version} has no gate=passed tag"
    try:
        cur = str(client.get_model_version_by_alias(name, alias).version)
    except MlflowException:
        cur = None
    if cur == str(version):
        return 0, f"NO-OP: {alias} already points at version {version}"
    client.set_registered_model_alias(name, alias, str(version))
    client.set_model_version_tag(name, str(version), "promoted_by", who)
    client.set_model_version_tag(name, str(version), "promoted_run", run_url)
    client.set_model_version_tag(name, str(version), "promoted_at",
                                 datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    if cur:
        client.set_model_version_tag(name, cur, "replaced_by", str(version))
    return 0, f"PROMOTED: {alias} {cur} -> {version}"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--uri", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--version", required=True)
    a = p.parse_args()
    c = MlflowClient(a.uri, registry_uri=a.uri)
    who = os.environ.get("GITHUB_ACTOR", "local-user")
    run = os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + os.environ.get("GITHUB_REPOSITORY", "org/repo") \
        + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "0")
    def show(tag):
        try:
            print(f"{tag}: champion -> v{c.get_model_version_by_alias(a.name, 'champion').version}")
        except MlflowException:
            print(f"{tag}: champion -> (unset)")
    show("before")
    code, msg = promote(c, a.name, a.version, who=who, run_url=run)
    print(msg)
    show("after")
    sys.exit(code)
