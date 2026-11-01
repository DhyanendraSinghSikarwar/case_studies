import numpy as np, pytest
from fitmod import make_df, train_test_split_and_fit

GOLDEN = 0.7666666666666667      # recorded once with seed=1 (python3 -I run, scikit-learn 1.9.1)


def test_same_seed_same_metric():
    df = make_df()
    assert train_test_split_and_fit(df, seed=1) == train_test_split_and_fit(df, seed=1)   # exact: same machine, same code


def test_golden_metric_with_tolerance():
    # 1e-6 absolute: allows tiny BLAS/platform differences, still catches a changed split or model
    assert train_test_split_and_fit(make_df(), seed=1) == pytest.approx(GOLDEN, abs=1e-6)


def test_metric_is_good_across_seeds():
    # property test: do not depend on one lucky split; assert a floor below the observed spread (min 0.678 over 20 seeds)
    accs = [train_test_split_and_fit(make_df(), seed=s) for s in range(20)]
    assert min(accs) > 0.60


def test_arrays_close():
    np.testing.assert_allclose(np.array([0.1 + 0.2]), [0.3], rtol=1e-9)   # 0.1+0.2 != 0.3 exactly
