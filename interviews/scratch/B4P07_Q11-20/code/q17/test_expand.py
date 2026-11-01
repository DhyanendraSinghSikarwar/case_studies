from expand import expand

def test_plain_product():
    assert len(expand({"a": [1, 2], "b": [1, 2, 3]})) == 6

def test_exclude():
    assert len(expand({"a": [1, 2], "b": [1, 2], "exclude": [{"a": 1, "b": 1}]})) == 3

def test_include_extends_existing():
    jobs = expand({"a": [1, 2], "include": [{"a": 1, "extra": "x"}]})
    assert len(jobs) == 2 and jobs[0]["extra"] == "x" and "extra" not in jobs[1]

def test_include_new_combo():
    assert len(expand({"a": [1, 2], "include": [{"a": 3}]})) == 3
