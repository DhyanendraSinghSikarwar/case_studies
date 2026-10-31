"""Config: defaults < YAML file < env vars (TRAIN_*) < CLI flags. Unknown keys and wrong types fail fast."""
import argparse, hashlib, json, os, sys
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")            # a typo like 'epoch' is an error, not silently ignored
    learning_rate: float = Field(0.1, gt=0, le=1)
    epochs: int = Field(10, ge=1)
    data_path: str = "data/train.csv"
    features: list[str] = Field(min_length=1)
    seed: int = 0

def load(path, cli_overrides):
    raw = yaml.safe_load(open(path)) or {}
    for key in Config.model_fields:                      # env: TRAIN_LEARNING_RATE=0.05 etc.
        env = os.environ.get("TRAIN_" + key.upper())
        if env is not None:
            raw[key] = yaml.safe_load(env)               # parse "0.05" -> float, "[a,b]" -> list
    raw.update({k: v for k, v in cli_overrides.items() if v is not None})
    return Config(**raw)                                 # validation happens here

def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--learning-rate", type=float)
    p.add_argument("--epochs", type=int)
    a = p.parse_args(argv)
    try:
        cfg = load(a.config, {"learning_rate": a.learning_rate, "epochs": a.epochs})
    except ValidationError as e:
        print(f"CONFIG ERROR ({e.error_count()} problem(s)):")
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']} (got {err.get('input')!r})")
        return 2
    resolved = cfg.model_dump()
    blob = json.dumps(resolved, sort_keys=True)
    print("resolved config:", blob)
    print("config hash:", hashlib.sha256(blob.encode()).hexdigest()[:12], "(log this with the run, e.g. as an MLflow param or a JSON file)")
    # ... training would start here, using only cfg.*
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
