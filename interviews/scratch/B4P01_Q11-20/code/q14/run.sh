python3 -I -m pytest -q -p no:cacheprovider            # all pass
LEAK=1 python3 -I -m pytest -q -p no:cacheprovider     # injected leak: invariance test fails
