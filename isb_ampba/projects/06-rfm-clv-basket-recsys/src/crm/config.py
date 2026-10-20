"""Config loading, logging and seeding helpers."""
from __future__ import annotations

import logging
import os
import random
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict:
    """Load the YAML config (default: config/config.yaml at project root)."""
    path = Path(path) if path else ROOT / "config" / "config.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with a sane default format."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger(name)


def seed_everything(seed: int) -> None:
    """Seed python and numpy RNGs."""
    random.seed(seed)
    np.random.seed(seed)


def resolve(cfg: dict, key: str) -> Path:
    """Resolve a cfg['paths'] entry to an absolute path (env CRM_OUTPUTS overrides outputs)."""
    if key == "outputs" and os.environ.get("CRM_OUTPUTS"):
        return Path(os.environ["CRM_OUTPUTS"])
    return ROOT / cfg["paths"][key]
