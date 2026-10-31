import importlib, os
import numpy as np
from hypothesis import assume, given, settings, strategies as st

impl = importlib.import_module(os.environ["IMPL"])
S = settings(derandomize=True, database=None, max_examples=200)   # same run every time
finite = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
arrays = st.lists(finite, min_size=1, max_size=20)

@S
@given(arrays)
def test_minmax_in_unit_interval(xs):
    out = impl.minmax(xs)
    assert out.shape == (len(xs),)
    assert np.all((out >= 0) & (out <= 1)), out          # also fails on NaN

@S
@given(arrays)
def test_minmax_is_monotone(xs):
    assume(len(set(xs)) > 1)                              # constant columns are a separate rule
    x, out = np.asarray(xs), impl.minmax(xs)
    order = np.argsort(x, kind="stable")
    assert (np.diff(out[order]) >= 0).all()               # bigger input never gives smaller output

@S
@given(st.lists(st.sampled_from([float("nan"), float("inf"), -float("inf"), 1.0, 2.0]), min_size=1, max_size=5))
def test_minmax_rejects_non_finite_or_returns_finite(xs):
    try:
        out = impl.minmax(xs)
    except ValueError:
        return
    assert np.isfinite(out).all(), out                  # never hand NaN downstream silently

split_args = dict(n=st.integers(2, 50), frac=st.floats(0.05, 0.95), seed=st.integers(0, 2**32 - 1))

@S
@given(**split_args)
def test_split_sizes_add_up_no_loss_no_dup(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) + len(te) == n, (len(tr), len(te))
    assert sorted(np.concatenate([tr, te]).tolist()) == list(range(n))   # every row exactly once

@S
@given(**split_args)
def test_split_both_sides_non_empty(n, frac, seed):
    tr, te = impl.split_idx(n, frac, seed)
    assert len(tr) > 0 and len(te) > 0

@S
@given(**split_args)
def test_split_is_deterministic(n, frac, seed):
    a, b = impl.split_idx(n, frac, seed), impl.split_idx(n, frac, seed)
    assert all(np.array_equal(p, q) for p, q in zip(a, b))
