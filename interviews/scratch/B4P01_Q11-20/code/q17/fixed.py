import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def train_and_report(path, seed=0):
    df = pd.read_csv(path)
    X, y = df.drop(columns="y"), df["y"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    model = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=200)).fit(Xtr, ytr)  # selection inside the pipeline
    print("test accuracy", round(model.score(Xte, yte), 3))
    return model
