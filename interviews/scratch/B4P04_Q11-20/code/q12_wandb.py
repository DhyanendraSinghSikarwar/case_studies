import warnings; warnings.filterwarnings("ignore")
import wandb
from sklearn.datasets import make_classification
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
X, y = make_classification(n_samples=800, n_features=10, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(X, y, random_state=1)
run = wandb.init(project="demo-proj", config={"lr": 0.01, "epochs": 5}, dir=".", mode="offline", name="sgd-1")
cfg = run.config
m = SGDClassifier(loss="log_loss", learning_rate="constant", eta0=cfg.lr, random_state=0)
for epoch in range(cfg.epochs):
    m.partial_fit(Xtr, ytr, classes=[0, 1])
    wandb.log({"epoch": epoch, "val_auc": roc_auc_score(yva, m.decision_function(Xva))})
run.summary["final_val_auc"] = roc_auc_score(yva, m.decision_function(Xva))
art = wandb.Artifact("train-data", type="dataset", metadata={"rows": len(Xtr)})
with art.new_file("note.txt") as f: f.write("synthetic data, seed 0\n")
run.log_artifact(art)
print("mode:", run.settings.mode, "| project:", run.project, "| entity:", run.entity, "| run id:", run.id)
run.finish()
