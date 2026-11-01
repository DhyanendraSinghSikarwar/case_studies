for i in 1 2 3 4 5 6 7 8; do python3 -I -m pytest -q -p no:cacheprovider test_flaky.py | tail -1; done   # flaky, then count
python3 -I -m pytest -q -p no:cacheprovider test_fixed.py
