import json, logging, sys
import pandas as pd

class JsonFormatter(logging.Formatter):
    def format(self, record):
        d = {"level": record.levelname, "logger": record.name, "msg": record.getMessage(), "run_id": RUN_ID}
        d.update(getattr(record, "ctx", {}))              # structured extras: row counts etc.
        if record.exc_info:
            d["exc"] = repr(record.exc_info[1])
        return json.dumps(d, sort_keys=True)

RUN_ID = "run-0001"     # fixed here so the output is reproducible; use uuid.uuid4().hex[:8] in real code
log = logging.getLogger("scoring")
h = logging.StreamHandler(sys.stdout); h.setFormatter(JsonFormatter())
log.addHandler(h); log.setLevel(logging.INFO); log.propagate = False

class BadInputError(ValueError):
    """The batch itself is unusable (missing column, empty). Stop the job."""

def score_batch(df: pd.DataFrame, max_bad_frac: float = 0.2) -> pd.DataFrame:
    log.info("batch received", extra={"ctx": {"rows_in": len(df)}})
    if "income" not in df.columns:
        raise BadInputError("missing column: income")        # specific exception, caller can alert on it
    if df.empty:
        raise BadInputError("empty batch")
    ok = df["income"].notna() & (df["income"] >= 0)
    n_bad = int((~ok).sum())
    if n_bad:
        log.warning("dropping bad rows", extra={"ctx": {"rows_bad": n_bad, "bad_ids": df.loc[~ok, "id"].tolist()}})
    if n_bad / len(df) > max_bad_frac:                        # a few bad rows: continue. Too many: stop.
        raise BadInputError(f"{n_bad}/{len(df)} bad rows exceeds limit {max_bad_frac:.0%}")
    out = df[ok].assign(score=lambda d: (d["income"] / 100).clip(upper=1.0))
    log.info("batch scored", extra={"ctx": {"rows_in": len(df), "rows_out": len(out), "rows_bad": n_bad}})
    return out

def main():
    batches = {
      "good":   pd.DataFrame({"id": range(1, 6), "income": [10., 50., 80., 120., 30.]}),
      "ragged": pd.DataFrame({"id": range(1, 11), "income": [10., None, 80., 120., 30., 5., 6., 7., 8., 9.]}),   # 1 bad of 10
      "bad":    pd.DataFrame({"id": range(1, 6), "income": [None, -5., None, 120., 30.]}),                        # 3 bad of 5
      "nocol":  pd.DataFrame({"id": [1, 2], "salary": [1., 2.]}),
    }
    code = 0
    for name, df in batches.items():
        print(f"--- batch: {name}")
        try:
            score_batch(df)
        except BadInputError as e:
            log.error("batch rejected", extra={"ctx": {"reason": str(e)}}, exc_info=True)
            code = 1                       # non-zero exit lets the scheduler mark the job failed
        # NOT: except Exception: pass   (hides real bugs, the job 'succeeds' with no output)
    return code

if __name__ == "__main__":
    sys.exit(main())
