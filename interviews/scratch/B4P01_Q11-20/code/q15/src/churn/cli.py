import argparse
import json

from churn.config import TrainConfig
from churn.pipeline import predict, train


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="churn")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--data", required=True)
    t.add_argument("--out", default="model.joblib")
    t.add_argument("--seed", type=int, default=42)
    args = p.parse_args(argv)
    if args.cmd == "train":
        print(json.dumps(train(TrainConfig(data_path=args.data, out_path=args.out, seed=args.seed))))


if __name__ == "__main__":
    main()
