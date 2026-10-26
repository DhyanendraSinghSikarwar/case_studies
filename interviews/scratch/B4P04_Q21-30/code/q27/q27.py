# Q27: W&B Artifact built locally. Nothing is uploaded; we inspect the manifest/digest.
import os, wandb
os.makedirs("data/imgs", exist_ok=True)
open("data/train.csv", "w").write("x,y\n1,2\n3,4\n")
open("data/imgs/a.txt", "w").write("img-a")

def build(extra=None):
    art = wandb.Artifact("train-data", type="dataset", description="tiny demo", metadata={"rows": 2})
    art.add_file("data/train.csv")
    art.add_dir("data/imgs", name="imgs")
    art.add_reference("https://example.com/raw/events.parquet", name="raw_events", checksum=False)   # pointer, nothing copied (s3:// works the same but needs boto3 + credentials)
    if extra: art.add_file(extra)
    return art

a1 = build()
print("name:", a1.name, "| type:", a1.type, "| size entries:", len(a1.manifest.entries))
for path, e in sorted(a1.manifest.entries.items()):
    print(f"  {path:16} digest={e.digest[:12]}... ref={e.ref}")
print("artifact digest v1:", a1.digest)
a1b = build()
print("same content, rebuilt -> same digest?", a1b.digest == a1.digest)
open("data/train.csv", "a").write("5,6\n")
a2 = build()
print("one row appended -> new digest?", a2.digest != a1.digest)
print("version/aliases before upload:", getattr(a1, "version", None), "| (v0/v1/latest are assigned by the server on log_artifact)")
try:
    a1.add_reference("s3://my-bucket/raw/events.parquet", name="s3ref")   # needs boto3 (and creds to checksum)
except Exception as e:
    print("s3:// reference here ->", type(e).__name__ + ":", str(e)[:90])
# the real lineage calls, shown but NOT run:
print("\nnot run: run.log_artifact(a2, aliases=['latest']) / run.use_artifact('train-data:v0') need an account")
