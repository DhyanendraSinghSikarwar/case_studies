from fitmod import make_df, train_test_split_and_fit
def test_flaky():
    # unseeded split: the metric moves around, and the threshold sits right in the middle of that spread
    assert train_test_split_and_fit(make_df()) > 0.77
