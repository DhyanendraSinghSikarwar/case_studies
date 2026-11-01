python3 -I -m pytest -v -s -p no:cacheprovider               # default: slow test skipped
python3 -I -m pytest -q -p no:cacheprovider --runslow        # includes the slow test (fails here: no network)
