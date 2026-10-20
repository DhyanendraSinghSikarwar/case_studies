"""Config loading, logging and seeding helpers."""
from __future__ import annotations

import logging
import random
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load config.yaml (default: project config/config.yaml)."""
    path = Path(path) if path else ROOT / "config" / "config.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    """Return a module logger with a basic stream configuration."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger(name)


def set_seed(seed: int) -> None:
    """Seed python and numpy global RNGs."""
    random.seed(seed)
    np.random.seed(seed)


def resolve(cfg: dict[str, Any], key: str, root: Path | None = None) -> Path:
    """Resolve a configured relative path against the project root and create it."""
    p = (root or ROOT) / cfg["paths"][key]
    p.mkdir(parents=True, exist_ok=True)
    return p
