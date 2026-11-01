import pytest
from bump import bump, release_id

def test_major_wins(): assert bump("2.3.1", ["retrain-new-data", "input-schema-change"]) == "3.0.0"
def test_minor():      assert bump("2.3.1", ["retrain-new-data"]) == "2.4.0"
def test_patch():      assert bump("2.3.1", ["preprocessing-bugfix"]) == "2.3.2"
def test_no_labels():
    with pytest.raises(ValueError): bump("1.0.0", [])
def test_unknown_label():
    with pytest.raises(ValueError): bump("1.0.0", ["vibes"])
def test_release_id(): assert release_id("2.3.1", "20261001", "ab12cd3") == "2.3.1+data.20261001.git.ab12cd3"
