"""Project paths, config loading and logging."""
from __future__ import annotations

import copy
import logging
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "config.yaml"


def get_logger(name: str) -> logging.Logger:
    """Return a module logger with a simple console format (configured once)."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        datefmt="%H:%M:%S")
    return logging.getLogger(name)


@lru_cache(maxsize=4)
def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_config(path: Path | str | None = None) -> dict:
    """Load config.yaml (returns a fresh copy so callers may mutate it)."""
    return copy.deepcopy(_load(str(path or CONFIG_PATH)))
