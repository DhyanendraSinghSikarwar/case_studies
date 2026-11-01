python3 -I make_golden.py                                   # once, at training time
SERVICE=buggy  python3 -I -m pytest -q -p no:cacheprovider tests   # parity test fails
SERVICE=shared python3 -I -m pytest -q -p no:cacheprovider tests   # passes
