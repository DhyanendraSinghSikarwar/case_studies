"""Tests first: pin down what the code does TODAY (golden output) before touching it."""
def legacy_score(rows):                       # pretend this is the tangled function we want to refactor
    out = []
    for r in rows:
        v = r.get("a", 0) * 2 + (1 if r.get("flag") else 0)
        out.append(round(v, 2))
    return out

# GOLDEN was produced by running the CURRENT code once and checking it by eye; it lives in git next to the test.
GOLDEN = [3.0, 5.0, 0, -2]
ROWS = [{"a": 1.0, "flag": True}, {"a": 2.5}, {}, {"a": -1, "flag": False}]

def test_characterization():
    assert legacy_score(ROWS) == GOLDEN

test_characterization()
print("characterization test passed: refactor may start; it must keep this green")
