import numpy as np, pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def _accuracy(seed_data, seed_split):
    X, y = make_classification(n_samples=300, n_features=5, n_informative=3, class_sep=1.5,
                               random_state=seed_data)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed_split)
    return LogisticRegression().fit(Xtr, ytr).score(Xte, yte)

def test_flaky_exact_threshold():
    # BAD: nothing is seeded (None = fresh randomness each run) and the threshold is tight
    assert _accuracy(None, None) >= 0.85

def test_fixed_seeded_and_range():
    # GOOD 1: seeded, so the result is the same every run; assert a band, not a magic number
    acc = _accuracy(0, 0)
    assert 0.7 <= acc <= 1.0

def test_fixed_statistical():
    # GOOD 2: if randomness is the point, test the average over many seeds against a loose bound
    accs = [_accuracy(s, s) for s in range(20)]
    assert np.mean(accs) == pytest.approx(0.85, abs=0.1)

@pytest.mark.quarantine
def test_quarantined_example():
    assert _accuracy(None, None) >= 0.95   # known flaky, tracked in an issue, runs nightly only
