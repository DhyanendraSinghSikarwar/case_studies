import os
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

LEAK = os.environ.get("LEAK") == "1"   # flip to 1 to inject a leaky feature and watch tests fail


def make_data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    x0 = rng.normal(size=n)                      # informative, positive effect
    x1 = rng.normal(size=n)                      # informative, negative effect
    noise = rng.normal(size=n)                   # should be irrelevant
    y = (1.5 * x0 - 1.0 * x1 + rng.normal(scale=0.7, size=n) > 0).astype(int)
    if LEAK:
        noise = y + rng.normal(scale=0.1, size=n)  # the "irrelevant" column secretly encodes the label
    return np.c_[x0, x1, noise], y


@pytest.fixture(scope="module")
def split():
    X, y = make_data()
    idx = np.arange(len(y))
    tr, te = train_test_split(idx, test_size=0.3, random_state=0, stratify=y)
    return X[tr], X[te], y[tr], y[te], tr, te


@pytest.fixture(scope="module")
def model(split):
    Xtr, _, ytr, *_ = split
    return LogisticRegression().fit(Xtr, ytr)


# ---- pre-train style: no quality bar, just "is the machinery sane"
def test_output_shape_range_sum(model, split):
    p = model.predict_proba(split[1])
    assert p.shape == (len(split[1]), 2)
    assert ((p >= 0) & (p <= 1)).all()
    np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-9)


def test_can_overfit_ten_rows():
    X, y = make_data(n=10, seed=1)
    m = LogisticRegression(C=1e6, max_iter=1000).fit(X, y)
    assert (m.predict(X) == y).mean() == 1.0     # if it cannot memorise 10 rows, the pipeline is broken


# ---- post-train behaviour
def test_min_accuracy_on_slice(model, split):
    _, Xte, _, yte, *_ = split
    mask = Xte[:, 0] > 0                         # slice: x0 positive
    acc = (model.predict(Xte[mask]) == yte[mask]).mean()
    assert acc >= 0.80, f"slice accuracy {acc:.3f}"


def test_invariance_to_irrelevant_feature(model, split):
    Xte = split[1]
    shifted = Xte.copy(); shifted[:, 2] += 0.5   # nudge the column that should not matter
    flips = (model.predict(Xte) != model.predict(shifted)).mean()
    assert flips <= 0.02, f"{flips:.1%} predictions flipped"


def test_directional_expectation(model, split):
    Xte = split[1]
    up = Xte.copy(); up[:, 0] += 1.0             # more x0 -> probability of class 1 must not drop
    assert (model.predict_proba(up)[:, 1] >= model.predict_proba(Xte)[:, 1] - 1e-12).all()


def test_no_train_test_overlap(split):
    *_, tr, te = split
    assert set(tr).isdisjoint(te)
