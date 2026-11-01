import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def train_and_report(path="/home/me/data.csv"):              # smell: hard-coded path
    df = pd.read_csv(path)
    y = df["y"]
    X = df.drop(columns="y")
    X = SelectKBest(f_classif, k=20).fit_transform(X, y)      # BUG 1: selection sees the test rows
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3)  # BUG 2: no random_state
    model = LogisticRegression(max_iter=200).fit(Xtr, ytr)
    print("accuracy", round(model.score(Xtr, ytr), 3))       # BUG 3: metric on the TRAIN split
    return model
