# Shows what happens when you call wandb.sweep with no account/network (offline mode).
import wandb, yaml
cfg = yaml.safe_load(open("sweep.yaml"))
try:
    sid = wandb.sweep(cfg, project="demo")
    print("sweep id:", sid)
except Exception as e:
    print(type(e).__name__ + ":", str(e).splitlines()[0][:200])
