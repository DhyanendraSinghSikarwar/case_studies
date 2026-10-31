# Q13: simulate a named volume: UID permissions, read-only input, tar backup/restore. No Docker needed.
import os, subprocess, tarfile, tempfile, shlex, filecmp
base = tempfile.mkdtemp(prefix="q13_")
data = os.path.join(base, "data"); vol = os.path.join(base, "vol_ckpt")
os.chmod(base, 0o755); os.makedirs(data); os.makedirs(vol)
open(os.path.join(data, "train.csv"), "w").write("x,y\n1,2\n")
os.chmod(data, 0o555); os.chmod(os.path.join(data, "train.csv"), 0o444)   # stand-in for :ro

def try_write(path, uid):
    code = f"import os; os.setgid({uid}); os.setuid({uid}); open({path!r}+'/ckpt_1.pt','w').write('w')"
    r = subprocess.run(["python3", "-I", "-c", code], capture_output=True, text=True)
    return "OK" if r.returncode == 0 else r.stderr.strip().splitlines()[-1]

print("1) vol owned by root, process runs as uid 10001:", try_write(vol, 10001))
os.chown(vol, 10001, 10001)                      # what you do once (image build or init step)
print("2) vol chown 10001, process uid 10001        :", try_write(vol, 10001))
print("3) input dir (read-only), process uid 10001  :", try_write(data, 10001))

arch = os.path.join(base, "backup.tgz")           # volume backup = tar of its contents
with tarfile.open(arch, "w:gz") as t: t.add(vol, arcname=".")
restore = os.path.join(base, "restored"); os.makedirs(restore)
with tarfile.open(arch) as t: t.extractall(restore, filter="data")
print("4) backup files:", sorted(os.listdir(vol)), "restored:", sorted(os.listdir(restore)),
      "same:", filecmp.cmp(os.path.join(vol, "ckpt_1.pt"), os.path.join(restore, "ckpt_1.pt"), shallow=False))

cmd = """docker run --rm --name train --user 10001:10001 --read-only
  --mount type=bind,src=/srv/data/churn,dst=/data,readonly
  --mount type=volume,src=ckpts,dst=/ckpts
  --mount type=volume,src=hfcache,dst=/home/app/.cache
  --tmpfs /tmp:rw,size=512m
  myorg/trainer:1.4.0 python train.py --data /data --out /ckpts"""
a = shlex.split(cmd)
ok = {"read-only input": "readonly" in cmd, "named volume": "type=volume,src=ckpts" in cmd,
      "non-root": a[a.index("--user")+1].split(":")[0] != "0"}
print("5) run-command checks:", ok)
