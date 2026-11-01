"""Compare-and-set promotion: only move the alias FORWARD, and only if it still points where we think."""
import argparse, sys
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException


def current(client, name, alias="champion"):
    try:
        return int(client.get_model_version_by_alias(name, alias).version)
    except MlflowException:
        return None


def promote_forward(client, name, version, alias="champion", expected=None):
    """expected: the version the caller saw before deciding (None = do not check)."""
    version = int(version)
    cur = current(client, name, alias)
    if expected is not None and cur != expected:
        return False, f"REFUSED: alias moved under us (expected {expected}, found {cur})"
    if cur is not None and version < cur:
        return False, f"REFUSED: v{version} is older than current champion v{cur}"
    if cur == version:
        return True, f"NO-OP: already v{version}"
    client.set_registered_model_alias(name, alias, str(version))
    return True, f"PROMOTED: v{cur} -> v{version}"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--uri", required=True); p.add_argument("--name", required=True)
    p.add_argument("--version", required=True)
    a = p.parse_args()
    ok, msg = promote_forward(MlflowClient(a.uri, registry_uri=a.uri), a.name, a.version)
    print(msg)
    sys.exit(0 if ok else 3)
