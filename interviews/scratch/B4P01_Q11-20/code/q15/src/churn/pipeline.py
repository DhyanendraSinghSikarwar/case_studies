import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from churn.config import TrainConfig


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def split(df: pd.DataFrame, cfg: TrainConfig):
    X, y = df[list(cfg.features)], df[cfg.target]
    return train_test_split(X, y, test_size=cfg.test_size, random_state=cfg.seed, stratify=y)


def build_model(seed: int) -> Pipeline:
    # scaler lives INSIDE the pipeline, so fit() only ever sees training rows
    return Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(random_state=seed))])


def train(cfg: TrainConfig) -> dict:
    df = load_data(cfg.data_path)
    Xtr, Xte, ytr, yte = split(df, cfg)
    model = build_model(cfg.seed).fit(Xtr, ytr)
    metrics = {"accuracy": round(float(model.score(Xte, yte)), 4), "n_train": len(Xtr), "n_test": len(Xte)}
    joblib.dump({"model": model, "features": list(cfg.features)}, cfg.out_path)
    return metrics


def predict(model_path: str, rows: pd.DataFrame):
    art = joblib.load(model_path)
    return art["model"].predict(rows[art["features"]])
