"""Append-only promotion ledger (JSON lines) with rollback. Pure python, no registry needed."""
import json, datetime, pathlib


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def read(path):
    p = pathlib.Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def current(path):
    rows = read(path)
    return rows[-1]["to"] if rows else None


def _append(path, row):
    with open(path, "a") as f:            # append only: never rewrite history
        f.write(json.dumps(row, sort_keys=True) + "\n")


def promote(path, version, who, reason="release"):
    row = {"ts": _now(), "action": "promote", "from": current(path), "to": str(version),
           "who": who, "reason": reason}
    _append(path, row)
    return row


def rollback(path, who, reason, exists=lambda v: True, target=None):
    """Restore the previous champion. 'exists' checks the old artifact is still there."""
    if not reason.strip():
        raise ValueError("rollback needs a reason")
    rows = read(path)
    cur = rows[-1]["to"] if rows else None
    # walk back to the last different version
    prev = str(target) if target else None
    for r in (reversed(rows) if prev is None else []):
        if r["to"] != cur:
            prev = r["to"]
            break
    if prev is None:
        raise RuntimeError("nothing to roll back to")
    if not exists(prev):
        raise RuntimeError(f"previous version {prev} no longer exists")
    row = {"ts": _now(), "action": "rollback", "from": cur, "to": prev, "who": who, "reason": reason}
    _append(path, row)
    return row


if __name__ == "__main__":
    import argparse, sys
    p = argparse.ArgumentParser()
    p.add_argument("--ledger", required=True)
    p.add_argument("--who", default="local")
    p.add_argument("--reason", required=True)
    p.add_argument("--version", default="")      # blank = previous champion
    a = p.parse_args()
    print(json.dumps(rollback(a.ledger, a.who, a.reason, target=a.version or None)))
