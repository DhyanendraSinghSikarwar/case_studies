import numpy as np
import pytest
from mlsvc import predict, softmax

def test_softmax_sums_to_one():
    assert softmax([1, 2, 3]).sum() == pytest.approx(1.0)

def test_softmax_no_overflow():
    assert np.isfinite(softmax([1000, 1001])).all()

def test_predict_picks_larger_logit():
    assert predict([1.0, 2.0], [[1, 0], [0, 1]]) == 1
