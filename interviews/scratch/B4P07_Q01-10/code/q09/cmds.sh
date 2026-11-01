pytest -v -p no:cacheprovider
python -I router.py src/training/loss.py data/train.csv.dvc
python -I router.py deploy/alias.yaml
