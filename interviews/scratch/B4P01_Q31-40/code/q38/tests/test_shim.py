import pytest, teamlib

def test_old_name_warns_and_still_works():
    with pytest.warns(DeprecationWarning, match="use make_features"):
        out = teamlib.build_features([1, None, 3])
    assert out == [1, 0, 3]

def test_new_name_is_silent(recwarn):
    teamlib.make_features([1, None])
    assert len(recwarn) == 0
