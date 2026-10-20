"""Config loading, paths and logging."""
from __future__ import annotations

import copy
import logging
import os
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict:
    """Load config.yaml (default: project config)."""
    p = Path(path) if path else ROOT / "config" / "config.yaml"
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger(name)


def path_for(cfg: dict, key: str, root: Path | None = None) -> Path:
    """Resolve cfg['paths'][key]; interim can be redirected with env AMPBA_INTERIM_DIR (keep out of OneDrive)."""
    if key == "interim" and os.environ.get("AMPBA_INTERIM_DIR"):
        p = Path(os.environ["AMPBA_INTERIM_DIR"])
    else:
        p = Path(cfg["paths"][key])
        if not p.is_absolute():
            p = (root or ROOT) / p
    p.mkdir(parents=True, exist_ok=True)
    return p


def seed_everything(cfg: dict) -> np.random.Generator:
    """Seed numpy/random and return a Generator."""
    import random

    random.seed(cfg["seed"])
    np.random.seed(cfg["seed"])
    return np.random.default_rng(cfg["seed"])


def clone(cfg: dict) -> dict:
    """Deep copy of a config (for overrides)."""
    return copy.deepcopy(cfg)
