"""Train stage: families, basket halo and demand estimates from the interim data -> engine table artifacts."""
from __future__ import annotations

import json

from .config import get_logger, path_for
from .pipeline import (
    build_engine_table,
    data_summary,
    default_dirs,
    load_stage_inputs,
    save_train_artifacts,
    to_py,
    train_summary,
)

log = get_logger("promo.train")


def main() -> None:
    """CLI entry: python -m promo.train."""
    cfg, out_dir, _, models_dir = default_dirs()
    sales, panel = load_stage_inputs(cfg)
    res = build_engine_table(sales, panel, cfg)
    save_train_artifacts(res, cfg, out_dir, models_dir)
    meta_p = path_for(cfg, "interim") / "meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {"raw_rows": -1}
    part = {"data": {**data_summary(meta["raw_rows"], sales, panel, cfg), **{k: v for k, v in meta.items() if k != "raw_rows"}}, **train_summary(res, cfg)}
    (out_dir / "train_summary.json").write_text(json.dumps(to_py(part), indent=2), encoding="utf-8")
    log.info("train stage done: %d SKUs in engine table", len(res["table"]))


if __name__ == "__main__":
    main()
