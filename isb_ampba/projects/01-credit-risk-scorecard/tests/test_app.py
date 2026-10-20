from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_app_parses():
    import ast

    ast.parse((ROOT / "app" / "streamlit_app.py").read_text(encoding="utf-8"))


@pytest.mark.skipif(not (ROOT / "outputs" / "summary.json").exists() or not (ROOT / "models" / "xgb.joblib").exists(),
                    reason="artefacts not built yet")
def test_app_runs_headless():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "app" / "streamlit_app.py"), default_timeout=600).run()
    assert not at.exception
    assert len(at.tabs) == 4
