import time
import joblib
from sklearn.linear_model import LogisticRegression


def download_pretrained(name: str):
    time.sleep(5)                                   # pretend this is a big network download
    raise RuntimeError("no network in tests")


def fit_and_save(df, path):
    m = LogisticRegression().fit(df[["a", "b"]], df["y"])
    joblib.dump(m, path)
    return m


def load_embeddings(name: str):
    weights = download_pretrained(name)
    return weights
