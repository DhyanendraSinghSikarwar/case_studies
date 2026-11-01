import numpy as np
import pandas as pd
import pytest

from prep import impute_and_scale


def test_known_values_by_hand():
    # a = [1, NaN, 3] -> median 2 -> [1,2,3] -> mean 2, pop std sqrt(2/3)
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    out = impute_and_scale(df, ["a"])
    s = np.sqrt(2 / 3)
    np.testing.assert_allclose(out["a"].to_numpy(), [-1 / s, 0.0, 1 / s])


def test_output_is_standardised():
    df = pd.DataFrame({"a": [1.0, 2.0, 4.0, 8.0, np.nan]})
    out = impute_and_scale(df, ["a"])
    assert out["a"].mean() == pytest.approx(0.0, abs=1e-12)
    assert out["a"].std(ddof=0) == pytest.approx(1.0)
    assert not out["a"].isna().any()


@pytest.mark.parametrize(
    "data, why",
    [
        ({"a": [np.nan, np.nan, np.nan]}, "all NaN"),
        ({"a": [5.0, 5.0, 5.0]}, "constant"),
        ({"a": [5.0, np.nan, 5.0]}, "constant after imputing"),
    ],
)
def test_bad_columns_raise(data, why):
    with pytest.raises(ValueError):
        impute_and_scale(pd.DataFrame(data), ["a"])


def test_missing_column_raises():
    with pytest.raises(ValueError, match="missing columns"):
        impute_and_scale(pd.DataFrame({"a": [1.0, 2.0]}), ["b"])


def test_empty_frame_returns_empty_floats():
    df = pd.DataFrame({"a": pd.Series([], dtype="int64")})
    out = impute_and_scale(df, ["a"])
    assert len(out) == 0 and out["a"].dtype == np.float64


def test_input_not_mutated():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [1, 2, 3]})
    before = df.copy(deep=True)
    impute_and_scale(df, ["a"])
    pd.testing.assert_frame_equal(df, before)


def test_dtype_is_float_even_for_int_input_and_other_cols_untouched():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    out = impute_and_scale(df, ["a"])
    assert out["a"].dtype == np.float64
    assert out["b"].tolist() == ["x", "y", "z"]
