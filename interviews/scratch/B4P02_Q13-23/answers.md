# Book 4 Part 2, Q13-Q23 answers (Wave B agent)

### Q13 ⭐⭐⭐ 🟡 Volumes, bind mounts and tmpfs for ML containers. Where do you put training data, checkpoints, the model registry download cache and logs, and why? Compare named volumes, bind mounts (host path, UID and permission issues, slow on Docker Desktop) and tmpfs, what survives docker rm, the -v versus --mount syntax, how to back up a volume, and the read-only mount for input data. Show a run command that trains with data mounted read-only, checkpoints in a named volume, and a non-root user that can write there.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Data goes in as a read-only bind mount, checkpoints go in a named volume, scratch goes in tmpfs, logs go to stdout, and the container runs as a fixed non-root UID that owns the volume.

**Then explain:**
- **Where each thing lives**
  - Training data: bind mount or a data volume, mounted `readonly`. The job must never change its input.
  - Checkpoints: named volume (or object storage). They must survive `docker rm`.
  - Model-registry download cache and the Hugging Face cache: named volume, so a restart does not download again.
  - Logs: stdout and stderr, not files. The Docker log driver collects them (see Q30).
  - Scratch and temp files: `--tmpfs /tmp`. Fast, memory-backed, gone on stop.
- **Three mount types**
  - Named volume: Docker manages the path, works the same on Linux and Docker Desktop, survives `docker rm`. Best for state you own.
  - Bind mount: you choose the host path. Good for input data and local development. Host UID and permission problems show up here. On Docker Desktop (Mac, Windows) it goes through a file-sharing layer and is often slow for many small files.
  - tmpfs: lives in RAM, vanishes at stop, counts against the memory limit. Never put checkpoints there.
- **What survives `docker rm`:** named volumes and bind-mounted host files survive. The container writable layer and tmpfs do not. Anonymous volumes (a `VOLUME` line with no name) survive too, but `docker rm -v` or `--rm` removes them, which surprises people.
- **`-v` versus `--mount`:** `--mount` is explicit (`type=,src=,dst=,readonly`) and errors if a bind source does not exist. `-v host:ctr` silently creates a missing host directory, owned by root. I prefer `--mount` in scripts.
- **UID problem (the usual failure):** the container user is UID 10001, but the volume or host dir is owned by root, so the first checkpoint save gives `PermissionError`. Fixes: `chown` the path in the Dockerfile (a new named volume copies that ownership from the image), or `--user $(id -u):$(id -g)` for bind mounts, or a one-off init container that runs `chown`.
- **Failure modes:** a checkpoint written to the container layer is lost on `rm`; a volume mounted over a path hides what the image had there; a disk-full volume fails the job late.

**Example:** The job runs as UID 10001. The volume `ckpts` is created empty and owned by root. Epoch 1 ends, `torch.save` fails with permission denied, and 6 hours of training is lost. With the `chown 10001 /ckpts` line in the image, the same run saves fine. The simulation below reproduces exactly these cases with real UIDs: root-owned dir fails, chowned dir works, a read-only input dir rejects writes, and a backup tarball restores byte-for-byte.

**Code:** the Dockerfile and run commands are not executed (no daemon). The Python simulation ran.
```dockerfile
FROM python:3.12-slim-bookworm
RUN useradd --uid 10001 --create-home app \
 && mkdir -p /ckpts /data \
 && chown 10001:10001 /ckpts          # a NEW named volume mounted at /ckpts copies this ownership
WORKDIR /app
COPY --chown=10001:10001 train.py .
USER 10001
CMD ["python", "train.py", "--data", "/data", "--out", "/ckpts"]
```
```bash
# NOT EXECUTED here (no Docker daemon). Run on a Docker host.
docker volume create ckpts
docker run --rm --name train \
  --user 10001:10001 \
  --mount type=bind,src=/srv/data/churn,dst=/data,readonly \
  --mount type=volume,src=ckpts,dst=/ckpts \
  --mount type=volume,src=hfcache,dst=/home/app/.cache \
  --tmpfs /tmp:rw,size=512m \
  myorg/trainer:1.4.0

# same thing with the short -v syntax (a missing host path is silently created as root-owned)
docker run --rm -v /srv/data/churn:/data:ro -v ckpts:/ckpts myorg/trainer:1.4.0

# back up the named volume to a tarball in the current directory, then restore it
docker run --rm -v ckpts:/src:ro -v "$PWD":/backup alpine tar czf /backup/ckpts.tgz -C /src .
docker run --rm -v ckpts:/dst -v "$PWD":/backup:ro alpine tar xzf /backup/ckpts.tgz -C /dst
```
```python
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
```

**Output (my run):** `docker run` and `docker volume` were **not executed** (no Docker daemon in this sandbox). What did run: `hadolint` on the Dockerfile (clean), `bash -n` on the commands, `docker run --help` to confirm the flags exist, and the simulation. In step 3 the process is not root, so the read-only input dir is simulated with mode 0555. A real `:ro` mount gives `Read-only file system` (EROFS), not EACCES, even for root.
```text
$ hadolint q13_Dockerfile
(no output, exit 0)
$ bash -n q13_run.sh
bash syntax ok
$ docker run --help | grep -E -- '--mount|--tmpfs|--read-only'
      --mount mount                      Attach a filesystem mount to the
      --read-only                        Mount the container's root
      --tmpfs list                       Mount a tmpfs directory
$ python3 -I q13_volumes.py
1) vol owned by root, process runs as uid 10001: PermissionError: [Errno 13] Permission denied: '/tmp/q13_zviyss1_/vol_ckpt/ckpt_1.pt'
2) vol chown 10001, process uid 10001        : OK
3) input dir (read-only), process uid 10001  : PermissionError: [Errno 13] Permission denied: '/tmp/q13_zviyss1_/data/ckpt_1.pt'
4) backup files: ['ckpt_1.pt'] restored: ['ckpt_1.pt'] same: True
5) run-command checks: {'read-only input': True, 'named volume': True, 'non-root': True}
```

**Follow-ups:**
- *Why not just bind mount the checkpoint dir too?* You can on Linux. On Docker Desktop it is slower, and host UID clashes appear. A named volume avoids both.
- *How do you back up a volume?* Run a throwaway container that mounts the volume read-only plus a host dir, and `tar` it (commands above; the tar step is simulated in the script).
- *Can two containers share a volume?* Yes, but Docker does no locking. Two writers to one checkpoint file corrupt it.

**Common mistakes:**
- Running as root "to avoid permission errors", then shipping that.
- Writing checkpoints to a path that is not a volume.
- Mounting the whole repo over `/app` in production, which hides the code baked into the image.
- Putting caches on tmpfs: the model downloads again after every restart and RAM fills.

### Q14 ⭐⭐⭐ 🟡 A docker-compose.yml for a local ML stack: an inference API, an MLflow tracking server, Postgres for its backend store and MinIO for artifacts. Write the file with named volumes, a user-defined network, environment via an env_file, healthchecks and depends_on conditions, and ports published only where needed. Explain how services find each other by name, why localhost inside a container is not the host, and validate the file with docker compose config (works without a daemon) plus a pyyaml check that every depends_on target exists.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** One user-defined network, services call each other by service name, state sits in named volumes, health checks gate `depends_on`, and only the API (plus loopback-only admin ports) is published to the host.

**Then explain:**
- **Name resolution:** Compose creates a network for the project and registers each service name in its DNS. The API calls `http://mlflow:5000`, MLflow calls `postgres:5432` and `http://minio:9000`. No IPs.
- **`localhost` is the container itself.** If MLflow is told `localhost:5432` it looks inside its own container and fails. `localhost` only means "the host" when you use host networking, and not on Docker Desktop in the same way (Q15).
- **Ports:** `ports:` is for the host's benefit. Service-to-service traffic needs none. Postgres is not published at all. The MLflow UI and MinIO console are bound to `127.0.0.1` so only this machine can open them. Only the API is open on all interfaces.
- **Startup order:** `depends_on` with `condition: service_healthy` waits until the dependency's healthcheck passes. A plain `depends_on` only waits for the container to start, not for the database to accept connections.
- **Config:** one `.env` via `env_file` for local use. Caveat: `env_file` hands every variable to that service, so a real project splits files per service. Never commit real secrets.
- **Failure modes:** `$VAR` in a list-form `command` is not expanded (no shell), so I pass the Postgres URL through `environment:` where Compose interpolates it; healthcheck tools missing in an image (check `curl` or `mc` exists, else use Python); MinIO bucket must exist before MLflow logs artifacts (a one-shot init service or `mc mb`); `latest` tags in the file are for the demo only.

**Example:** `docker compose up` starts Postgres and MinIO first. When both are healthy MLflow starts. When MLflow's `/health` answers, the API starts. A bad `depends_on` typo (`mlfow`) is caught by the pyyaml check below, as the second output shows.

**Code:** `docker-compose.yml`, `.env`, and the pyyaml check. `docker compose up` is not executed.
```yaml
name: mlstack
services:
  postgres:
    image: postgres:16-bookworm        # pin minor/digest in real use; check current tags
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks: [mlnet]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 10
  minio:
    image: minio/minio:latest          # pin a dated release tag in real use
    command: server /data --console-address ":9001"
    env_file: .env
    volumes:
      - miniodata:/data
    networks: [mlnet]
    ports:
      - "127.0.0.1:9001:9001"          # console for humans, bound to loopback only
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]   # assumes curl in the image; check
      interval: 5s
      timeout: 3s
      retries: 10
  mlflow:
    build: ./mlflow                    # small image: mlflow + psycopg2 + boto3
    env_file: .env
    environment:
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000   # service name, not localhost
      MLFLOW_BACKEND_STORE_URI: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      MLFLOW_ARTIFACTS_DESTINATION: s3://mlflow-artifacts   # env names: check current MLflow docs
    command: ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]   # no shell, so no $VAR here
    networks: [mlnet]
    ports:
      - "127.0.0.1:5000:5000"
    depends_on:
      postgres: {condition: service_healthy}
      minio: {condition: service_healthy}
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:5000/health')"]
      interval: 10s
      timeout: 3s
      start_period: 20s
      retries: 6
  api:
    build: ./api
    env_file: .env
    environment:
      MLFLOW_TRACKING_URI: http://mlflow:5000
    networks: [mlnet]
    ports:
      - "8000:8000"                    # the only service users call
    depends_on:
      mlflow: {condition: service_healthy}
networks:
  mlnet:
    driver: bridge
volumes:
  pgdata:
  miniodata:
```
```dotenv
POSTGRES_USER=mlflow
POSTGRES_PASSWORD=change-me-local-only
POSTGRES_DB=mlflow
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=change-me-local-only
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=change-me-local-only
```
```python
# Q14: pyyaml checks on the compose file: depends_on targets exist, ports, networks, volumes, env_file.
import sys, yaml, os
d = yaml.safe_load(open(sys.argv[1])); base = os.path.dirname(sys.argv[1])
svcs = d["services"]; errs = []
for n, s in svcs.items():
    deps = s.get("depends_on", {}); deps = deps if isinstance(deps, list) else list(deps)
    for t in deps:
        if t not in svcs: errs.append(f"{n}: depends_on unknown service {t}")
    for t, c in (s.get("depends_on", {}) if isinstance(s.get("depends_on"), dict) else {}).items():
        if c.get("condition") == "service_healthy" and "healthcheck" not in svcs.get(t, {}):
            errs.append(f"{n}: waits for {t} healthy but {t} has no healthcheck")
    for net in s.get("networks", []):
        if net not in d.get("networks", {}): errs.append(f"{n}: undefined network {net}")
    for v in s.get("volumes", []):
        src = v.split(":")[0]
        if not src.startswith((".", "/")) and src not in d.get("volumes", {}): errs.append(f"{n}: undefined volume {src}")
    ef = s.get("env_file");
    if ef and not os.path.exists(os.path.join(base, ef)): errs.append(f"{n}: env_file {ef} missing")
    pubs = [p for p in s.get("ports", [])]
    print(f"{n:9} published: {pubs or 'none'}")
print("ERRORS:" if errs else "all checks passed", *errs, sep="\n" if errs else " ")
```

**Output (my run):** `docker compose config` ran for real (it needs no daemon). Starting the stack was **not executed** (no daemon, and images such as `postgres`, `minio` and MLflow were not pulled). The two Dockerfiles in `build:` are one-line stubs only so that `config` can resolve them.
```text
$ docker compose -f q14/docker-compose.yml config > q14_config.out
(exit 0; normalised file, 4 services, 2 volumes, 1 network; env_file values expanded into each service)
$ python3 -I q14_check.py q14/docker-compose.yml
postgres  published: none
minio     published: ['127.0.0.1:9001:9001']
mlflow    published: ['127.0.0.1:5000:5000']
api       published: ['8000:8000']
all checks passed
$ python3 -I q14_check.py q14/bad.yml   # depends_on typo
postgres  published: none
minio     published: ['127.0.0.1:9001:9001']
mlflow    published: ['127.0.0.1:5000:5000']
api       published: ['8000:8000']
ERRORS:
api: depends_on unknown service mlfow
api: waits for mlfow healthy but mlfow has no healthcheck
```

**Follow-ups:**
- *Why not `sleep 10` before MLflow?* It is a guess. A healthcheck is a fact.
- *Does `depends_on` keep working after startup?* No. If Postgres dies later, MLflow is not restarted. Use restart policies and retries in the app.
- *How would the API reach MLflow running on the host instead?* `host.docker.internal` (Docker Desktop) or `host-gateway` via `extra_hosts` on Linux (Q15).

**Common mistakes:**
- `localhost` for another service.
- Publishing Postgres to the world "for debugging".
- Using `latest` and getting a different MinIO next week.
- Putting credentials in the compose file itself.
- Forgetting named volumes, then losing the DB on `docker compose down -v`.

### Q15 ⭐⭐⭐ 🟡 Docker networking for a model API. The uvicorn app works with python app.py on the laptop but curl localhost:8000 hangs after docker run -p 8000:8000. Explain bridge, host and none networks, port publishing (-p host:container), why binding to 127.0.0.1 inside the container is the usual bug and 0.0.0.0 the fix, user-defined bridge DNS versus the default bridge, how a container reaches a database on the host (host.docker.internal on Docker Desktop, host-gateway on Linux), and how EXPOSE differs from -p. Show a Python check that parses a Dockerfile and compose file for the common mistakes.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Inside the container the server must listen on `0.0.0.0`; if it listens on `127.0.0.1`, the published port reaches the container's network interface and nothing is listening there, so `curl` hangs or resets.

**Then explain:**
- **Network modes**
  - `bridge` (default): the container gets a private IP behind NAT; you reach it with `-p`.
  - `host`: shares the host network stack. No `-p` needed (and ignored). Port clashes are possible. Behaves differently on Docker Desktop (check current docs).
  - `none`: only loopback. Good for offline batch jobs that must not call out.
- **`-p host:container`** maps a host port to a container port. `-p 127.0.0.1:8000:8000` keeps it local. `-p 8000:8000` opens all host interfaces. `EXPOSE` only documents the port and publishes nothing. `-P` publishes every `EXPOSE`d port to random host ports.
- **The classic bug:** `uvicorn app:app` defaults to `127.0.0.1`. On the laptop that is fine. In the container, traffic arrives on `eth0`, not loopback. Fix: `--host 0.0.0.0`. The socket demo below shows the same effect on one machine.
- **DNS:** on a user-defined bridge (and Compose networks) containers resolve each other by name. On the default `bridge` network they do not, only by IP (or legacy `--link`). So create a network: `docker network create ml`.
- **Reaching a service on the host:** Docker Desktop provides `host.docker.internal`. On Linux add `--add-host=host.docker.internal:host-gateway` (or use the host's bridge IP). The host service must listen on an address the container can reach, not only `127.0.0.1`.
- **Failure modes:** a port already used on the host; a firewall in front; a mismatch between `-p` container port and the app port; the app crashed (check `docker logs`).

**Example:** The app listens on `127.0.0.1:8001` inside, the Dockerfile says `EXPOSE 8000`, and the run uses `-p 8000:8000`. Two bugs (wrong bind address, wrong port), one symptom: hang. The checker below finds both in the Dockerfile, and also three compose problems.

**Code:** the checker and the bind demo ran. The docker commands are not executed.
```bash
# NOT EXECUTED (no daemon)
docker network create ml
docker run -d --name api --network ml -p 127.0.0.1:8000:8000 myorg/api:1.0   # app must bind 0.0.0.0
docker run --rm --network ml curlimages/curl http://api:8000/health      # DNS by name works on a user-defined network
docker run --rm --add-host=host.docker.internal:host-gateway myorg/api:1.0   # reach a host service on Linux
```
```python
# Q15: lint a Dockerfile and a compose file for common networking mistakes (regex/pyyaml; not a full parser).
import re, sys, yaml

def check_dockerfile(path):
    out, text = [], open(path).read()
    exposed = {int(p) for m in re.finditer(r"^EXPOSE\s+(.+)$", text, re.M) for p in re.findall(r"\d+", m.group(1))}
    cmd = re.search(r"^(?:CMD|ENTRYPOINT)\s+(.+)$", text, re.M)
    line = cmd.group(1) if cmd else ""
    host = re.search(r"--host[ =\"',]+([0-9.a-z]+)", line)
    port = re.search(r"--port[ =\"',]+(\d+)", line)
    if host and host.group(1) in ("127.0.0.1", "localhost"):
        out.append(f"{path}: server binds {host.group(1)} inside the container; -p will not reach it, use 0.0.0.0")
    if not host and "uvicorn" in line:
        out.append(f"{path}: uvicorn without --host defaults to 127.0.0.1; add --host 0.0.0.0")
    if port and exposed and int(port.group(1)) not in exposed:
        out.append(f"{path}: app listens on {port.group(1)} but EXPOSE says {sorted(exposed)} (EXPOSE is only documentation)")
    return out

def check_compose(path):
    out, d = [], yaml.safe_load(open(path))
    for n, s in d["services"].items():
        for k, v in (s.get("environment") or {}).items():
            if re.search(r"(localhost|127\.0\.0\.1)", str(v)):
                out.append(f"{path}: {n}.{k} points at localhost; inside a container that is the container itself, use the service name")
        if s.get("network_mode") == "host" and s.get("ports"):
            out.append(f"{path}: {n} uses network_mode: host AND ports; ports are ignored with host networking")
        for p in s.get("ports", []):
            if str(p).count(":") == 1 and re.search(r"postgres|mysql|redis|mongo", str(s.get("image", ""))):
                out.append(f"{path}: {n} publishes {p} on all host interfaces; use 127.0.0.1:{p} or drop it")
    return out

findings = check_dockerfile(sys.argv[1]) + check_compose(sys.argv[2])
print("\n".join(findings) or "no findings"); print(f"{len(findings)} finding(s)")

# ---- second script: q15_bind_demo.py ----
# Q15: why 127.0.0.1 inside the container is the bug. Same idea on one machine: connect via the non-loopback address.
import socket, threading
def serve(bind):
    s = socket.socket(); s.bind((bind, 0)); s.listen(1); return s
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); u.connect(("10.255.255.255", 1))  # no packet sent; picks the outbound interface
non_loop = u.getsockname()[0]; u.close()
for bind in ("127.0.0.1", "0.0.0.0"):
    s = serve(bind); port = s.getsockname()[1]
    # docker-proxy / NAT delivers traffic to the container's eth0 address, not its loopback
    c = socket.socket(); c.settimeout(1)
    try: c.connect((non_loop, port)); r = "connected"
    except OSError as e: r = f"failed ({type(e).__name__})"
    print(f"server bound to {bind:9} -> client via {non_loop}: {r}")
    c.close(); s.close()
```

**Output (my run):** Both scripts ran with `python3 -I`. The sample files `q15/Dockerfile.bad` and `q15/compose.bad.yml` are deliberately wrong. No container was started (**not executed**).
```text
$ python3 -I q15_netcheck.py q15/Dockerfile.bad q15/compose.bad.yml
q15/Dockerfile.bad: server binds 127.0.0.1 inside the container; -p will not reach it, use 0.0.0.0
q15/Dockerfile.bad: app listens on 8001 but EXPOSE says [8000] (EXPOSE is only documentation)
q15/compose.bad.yml: api.DB_URL points at localhost; inside a container that is the container itself, use the service name
q15/compose.bad.yml: api uses network_mode: host AND ports; ports are ignored with host networking
q15/compose.bad.yml: db publishes 5432:5432 on all host interfaces; use 127.0.0.1:5432:5432 or drop it
5 finding(s)
$ python3 -I q15_bind_demo.py
server bound to 127.0.0.1 -> client via 192.0.2.2: failed (ConnectionRefusedError)
server bound to 0.0.0.0   -> client via 192.0.2.2: connected
$ docker run --help | grep -E -- '-p, --publish|--add-host|--network '
      --add-host list                    Add a custom host-to-IP mapping
      --network network                  Connect a container to a network
  -p, --publish list                     Publish a container's port(s) to
```
The checker prints 5 findings: two from the Dockerfile, and the localhost URL, the host-networking-plus-ports pair and the public Postgres port from the compose file. It is regex and pyyaml based: it does not follow `ARG` substitution, multi-stage `CMD`, or compose `extends`.

**Follow-ups:**
- *Why does `host` networking "fix" it?* The app's loopback is then the host's loopback. It works but gives up isolation.
- *Why can containers on the default bridge not use names?* Automatic DNS is only provided on user-defined networks.
- *Does `EXPOSE` matter?* Only as documentation and for `-P` and some tools.

**Common mistakes:**
- `localhost` in a database URL inside a container.
- Binding `127.0.0.1` in the app.
- Publishing every port instead of the one that users need.
- Expecting `-p` to work with `--network host`.

### Q16 ⭐⭐⭐ 🔴 Where do model weights live: baked into the image, mounted as a volume, or downloaded at start? Compare the three for a 2 GB model and for a 30 GB model on image size, pull time, cold start, rollbacks, registry cost, reproducibility (image digest pins the model), air-gapped clusters, and secrets for the model store. Say which you choose for a small sklearn model, a medium transformer and a big LLM, and how a startup download should be made safe (checksum, retries, a readiness gate).
**Asked at:** PracHub write-up 'Docker optimization, container fundamentals, and CI/CD for an ML model service' (listed on the site as an eBay applied scientist question; search snippet only, not opened, not independently verified) and a ResumeLens article on containerizing ML models; editorial, not a verified candidate report; ML engineer and MLOps rounds at product companies
**Say this first (1 line):** Small model: bake it in. Medium: bake it if releases are rare, otherwise download into a cache volume with a pinned checksum. Big LLM: keep it out of the image and put it on a volume or a pre-warmed node cache, behind a readiness gate.

**Then explain:**
| | Baked in image | Mounted volume | Downloaded at start |
|---|---|---|---|
| Image size and pull time | Grows with the model, every node pulls it | Small image; weights arrive separately | Small image |
| Cold start | Pull time, then fast load | Fast if the volume is warm | Download time on every fresh node (until cached) |
| Rollback | Retag the old image, done | Need versioned dirs and a pointer | Config change to the old version; needs old file kept |
| Reproducibility | Best: the image digest pins code and model | Depends on how the volume is filled | Only if you pin a version id and checksum |
| Registry cost | Every model version stores a new big layer (sharing helps only if the model layer is unchanged) | None | None |
| Air-gapped | Works, one artifact | Works with a prefilled volume | Needs an internal mirror |
| Secrets | None at runtime; registry pull credentials only | Storage access to fill it | Needs a token at runtime for the model store |
- **Small sklearn model (MBs):** bake it. One digest equals one tested thing.
- **Medium transformer (about 2 GB):** bake if the registry is close and you ship rarely. If code ships weekly and the model monthly, put the model in its own layer (copied before the code, so the weekly rebuild reuses it) or download to a cache volume. Judgement call; say so in the interview.
- **Big LLM (about 30 GB):** do not bake. Very large layers are slow to push and pull, and some registries have size limits (check current docs). Use a shared volume, a node-local cache filled by a daemonset, or a download with caching.
- **Safe startup download:** pin an exact version and a sha256 (not `latest`), retry with backoff, write to a temp file then rename, verify the checksum before use, and only flip readiness when the model is loaded. If it fails, exit non-zero so the orchestrator restarts instead of serving garbage.
- **Failure modes:** a half-downloaded file loaded as a model; two replicas starting together and downloading the same 30 GB; the store being down during an autoscale event; a token that expired.

**Example:** The script below fakes a store with a local HTTP server. The first two requests return 503, the third works and the sha256 matches, so READY is written. The second file is corrupt, fails the checksum twice, is never renamed into place, and the process gives up with a non-zero exit.

**Code:** a Dockerfile for the download variant (linted by hadolint), the download-and-verify script, and the not-executed commands.
```dockerfile
# Variant B: download at start (small image). Weights fetched by entrypoint into a volume.
FROM python:3.12-slim-bookworm
RUN useradd --uid 10001 --create-home app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=10001:10001 app/ ./app/
ENV MODEL_DIR=/models MODEL_URL="" MODEL_SHA256=""
VOLUME ["/models"]
USER 10001
HEALTHCHECK --start-period=300s CMD ["python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000/ready')"]
ENTRYPOINT ["python", "-m", "app.fetch_then_serve"]
```
```python
# Q16: safe startup download: retries with backoff, sha256 check, atomic rename, readiness gate. Local HTTP server stands in for the model store.
import hashlib, http.server, os, tempfile, threading, time, urllib.request, urllib.error

MODEL = os.urandom(200_000)                       # stand-in "weights"
GOOD = hashlib.sha256(MODEL).hexdigest()
calls = {"n": 0}

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        calls["n"] += 1
        if self.path == "/flaky.bin" and calls["n"] <= 2:      # first two tries fail
            self.send_error(503); return
        body = MODEL[:1000] + b"X" if self.path == "/corrupt.bin" else MODEL
        self.send_response(200); self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass

srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"

def fetch(url, dest, sha256, tries=4, delay=0.05):
    for i in range(1, tries + 1):
        tmp = dest + ".part"
        try:
            with urllib.request.urlopen(url, timeout=5) as r, open(tmp, "wb") as f: f.write(r.read())
            h = hashlib.sha256(open(tmp, "rb").read()).hexdigest()
            if h != sha256: raise ValueError(f"checksum mismatch {h[:8]} != {sha256[:8]}")
            os.replace(tmp, dest)                  # atomic: readers never see half a file
            return i
        except (urllib.error.URLError, ValueError) as e:
            print(f"  attempt {i}: {e}")
            if os.path.exists(tmp): os.remove(tmp)
            time.sleep(delay * 2 ** i)             # exponential backoff
    raise SystemExit("giving up: container exits non-zero, orchestrator restarts it, NOT ready")

d = tempfile.mkdtemp(); ready = os.path.join(d, "READY")
print("flaky store, good checksum:")
n = fetch(base + "/flaky.bin", os.path.join(d, "model.bin"), GOOD); print(f"  ok after {n} attempt(s)")
open(ready, "w").write(GOOD)                       # readiness gate: /ready handler would check this file or the loaded model
print("ready file present:", os.path.exists(ready), "| leftover .part files:", [f for f in os.listdir(d) if f.endswith('.part')])
print("corrupt file:")
try: fetch(base + "/corrupt.bin", os.path.join(d, "bad.bin"), GOOD, tries=2)
except SystemExit as e: print(" ", e)
print("bad.bin exists:", os.path.exists(os.path.join(d, "bad.bin")))
```
```bash
# NOT EXECUTED (no daemon, no registry)
# Variant A: bake. Model copied before app code so weekly code changes reuse the big layer.
docker build -t myorg/api:1.14.0-m23 -f Dockerfile.baked .
# Variant B: download at start into a cache volume
docker run -v models:/models -e MODEL_URL=https://store.example.com/churn/23/model.bin -e MODEL_SHA256=<sha256> myorg/api:1.14.0
```

**Output (my run):** the script ran with `python3 -I` (real local HTTP server, random weights, so the hash changes each run). `hadolint` ran on the Dockerfile. No image was built (**not executed**).
```text
$ hadolint --no-color q16_Dockerfile
(no findings, exit 0)
$ python3 -I q16_safe_download.py
flaky store, good checksum:
  attempt 1: HTTP Error 503: Service Unavailable
  attempt 2: HTTP Error 503: Service Unavailable
  ok after 3 attempt(s)
ready file present: True | leftover .part files: []
corrupt file:
  attempt 1: checksum mismatch 52948119 != bc53979a
  attempt 2: checksum mismatch 52948119 != bc53979a
  giving up: container exits non-zero, orchestrator restarts it, NOT ready
bad.bin exists: False
```

**Follow-ups:**
- *Why checksum if the URL is HTTPS?* TLS protects transit, not a truncated file, a wrong version, or a changed object.
- *How do you pin a model with download?* Version id in config, sha256 in config, and log both at startup.
- *Why a readiness gate?* So the load balancer sends traffic only after the model is loaded (Q12).

**Common mistakes:**
- `MODEL_URL=.../latest/model.bin`.
- Loading the file while it is still being written.
- Baking a 30 GB model and then wondering why scale-out takes 20 minutes.
- Putting the model-store token in the image.

### Q17 ⭐⭐⭐ 🟢 .dockerignore and the build context. docker build sends the whole directory to the daemon; a repo with data/ (20 GB), .git, models/ and notebooks makes every build slow, and COPY . leaks .env into the image. Explain the build context, what .dockerignore does and its pattern rules (including ! exceptions), why it also helps the cache, and how to check what would be sent without a daemon. Write a .dockerignore for an ML repo and a Python script that lists which files it would exclude (use a simplified matcher and say what it does not cover).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** `docker build .` tars the whole context directory and sends it to the builder; `.dockerignore` removes files from that tarball, so builds are faster, caches stay valid and secrets like `.env` cannot be copied in.

**Then explain:**
- **Context:** the directory you pass (the `.`). Everything in it is a candidate for `COPY`. A 20 GB `data/` makes every build start by shipping 20 GB (with BuildKit only the needed files are transferred, but you cannot rely on that; check current docs).
- **Cache:** `COPY . /app` hashes the files it copies. A changed notebook, log or `.git` file changes that hash and busts the layer (Q2). Ignoring them keeps the hash stable.
- **Security:** `.env`, keys and `.git` history do not get into the image if they never reach the context.
- **Pattern rules (Docker's, simplified):** one pattern per line; `#` comments; paths are relative to the context root; `*` matches within one directory level, so `*.ipynb` only matches in the root; `**/*.ipynb` matches at any depth; a trailing `/` is optional; the **last matching line wins**; `!pattern` re-includes something an earlier line excluded, so put exceptions after the rule they undo.
- **Without a daemon:** list the files yourself with a matcher (below). `docker build` has no real dry-run that needs no daemon here.
- **What my matcher does not cover:** exact Go `filepath.Match` rules (`[a-z]` classes, escapes), `**` in the middle in every position, `!` interaction with parent-directory pruning (Docker may skip a whole excluded directory for speed, but still honours `!` exceptions for files below it; check current docs), symlinks, and case sensitivity on Windows. The Dockerfile and `.dockerignore` are always sent to the builder; ignoring them only hides them from `COPY`.
- **Failure mode:** you ignore `models/` but the Dockerfile has `COPY models/prod.pt`. The build fails with "not found". Add an exception, or do not ignore it.

**Example:** My sample tree has `.env`, `.env.example`, `.git/HEAD`, `data/raw/big.csv`, `models/big.pt`, `models/tiny_test.pt`, a notebook, a `.pem` file, a `.pyc` file, `requirements.txt` and `src/app.py`. After the rules, four files are sent: `.env.example`, `models/tiny_test.pt` (the `!` exception), `requirements.txt`, `src/app.py`.

**Code:** the `.dockerignore` and the simplified matcher. Both ran.
```gitignore
# VCS and editor
.git
.gitignore
.idea
.vscode
# secrets and local config
.env
.env.*
!.env.example
**/*.pem
# big or generated ML artefacts
data/
models/
checkpoints/
mlruns/
wandb/
**/*.ckpt
**/*.pt
!models/tiny_test.pt
# python junk
**/__pycache__
**/*.pyc
.venv/
.pytest_cache/
# notebooks and docs
**/*.ipynb
docs/
# Dockerfile and .dockerignore are still sent to the builder even if listed; COPY just cannot see them
Dockerfile*
docker-compose*.yml
```
```python
# Q17: simplified .dockerignore matcher. Last matching rule wins; '!' re-includes. Prints what would be sent.
import os, re, sys

def to_regex(pat):
    pat = pat.rstrip("/")
    out, i = "", 0
    while i < len(pat):
        c = pat[i]
        if pat[i:i+3] == "**/": out += "(?:.*/)?"; i += 3
        elif pat[i:i+2] == "**": out += ".*"; i += 2
        elif c == "*": out += "[^/]*"; i += 1
        elif c == "?": out += "[^/]"; i += 1
        else: out += re.escape(c); i += 1
    return re.compile("^" + out + "(?:/.*)?$")      # a match on a directory covers everything under it

def load(path):
    rules = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"): continue
        neg = line.startswith("!"); rules.append((neg, line.lstrip("!"), to_regex(line.lstrip("!").lstrip("/"))))
    return rules

def ignored(rel, rules):
    res, why = False, None
    for neg, raw, rx in rules:
        if rx.match(rel): res, why = (not neg), raw
    return res, why

if __name__ == "__main__":
    root, ig = sys.argv[1], sys.argv[2]
    rules = load(ig); sent, skipped = [], []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), root); size = os.path.getsize(os.path.join(dp, f))
            ign, why = ignored(rel, rules)
            (skipped if ign else sent).append((rel, size, why))
    print("SENT to daemon:");   [print(f"  {r}  ({s} B)") for r, s, _ in sorted(sent)]
    print("EXCLUDED:");         [print(f"  {r}  <- {w}") for r, s, w in sorted(skipped)]
    print(f"context: {sum(s for _,s,_ in sent)} B sent, {sum(s for _,s,_ in skipped)} B kept out")
```

**Output (my run):** the script ran with `python3 -I` on a temporary tree of 100-byte files. The second run shows the gotcha: a bare `*.ipynb` does not match `nb/eda.ipynb`. No `docker build` was run (**not executed**, no daemon).
```text
$ python3 -I q17_ignore.py <tmp-tree> q17.dockerignore
SENT to daemon:
  .env.example  (100 B)
  models/tiny_test.pt  (100 B)
  requirements.txt  (100 B)
  src/app.py  (100 B)
EXCLUDED:
  .env  <- .env
  .git/HEAD  <- .git
  Dockerfile  <- Dockerfile*
  data/raw/big.csv  <- data/
  models/big.pt  <- **/*.pt
  nb/eda.ipynb  <- **/*.ipynb
  notes.pem  <- **/*.pem
  src/__pycache__/app.cpython-312.pyc  <- **/*.pyc
context: 400 B sent, 800 B kept out
$ python3 -I q17_ignore.py <tmp-tree> <file containing only '*.ipynb'>  # filtered to ipynb lines
--- with only '*.ipynb':
  nb/eda.ipynb  (100 B)
```

**Follow-ups:**
- *Is `.gitignore` enough?* No. Docker does not read it. Keep both, and keep them similar.
- *Does `.dockerignore` shrink the image?* Only what `COPY` would have copied. Layers from `RUN` are unaffected.
- *Where do data and weights go instead?* Mounted at run time or fetched at start (Q13, Q16).

**Common mistakes:**
- `*.ipynb` instead of `**/*.ipynb`.
- An exception placed before the rule it should undo.
- Ignoring `requirements.txt` by accident with a broad pattern.
- Believing `.dockerignore` protects secrets that are passed as `ARG`.

### Q18 ⭐⭐ 🟢 Container versus virtual machine, for an ML engineer. Explain namespaces (pid, net, mnt), cgroups (cpu, memory), a shared host kernel, startup time and isolation trade-offs, why a container cannot ship its own kernel or GPU driver, and what that means for a model that needs a specific CUDA driver. Say when a VM or a micro-VM is the better boundary (untrusted code, multi-tenant notebooks).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** A container is an ordinary process on the host kernel, isolated by namespaces and limited by cgroups; a VM boots its own kernel on virtual hardware, so it is heavier but a stronger boundary.

**Then explain:**
- **Namespaces** give each container its own view: `pid` (process IDs, the first process is PID 1), `net` (interfaces, ports, routing), `mnt` (filesystem tree), plus `uts` (hostname), `ipc` and `user`.
- **cgroups** limit and account for resources: CPU shares or quota, memory limit, process count. `docker run --memory` and `--cpus` set them.
- **Shared kernel:** every container on a host runs on the same kernel. A kernel bug or a misconfigured privileged container affects the host. A container cannot ship its own kernel.
- **Speed and size:** a container starts in about the time it takes to start a process (no boot, no OS). A VM boots an OS. Containers are smaller because they hold only userland files.
- **GPU consequence:** the GPU driver is a kernel module on the host, so the image cannot contain it. The image carries the CUDA runtime and libraries; the host supplies the driver, and the container toolkit exposes the device files. A model needing a newer CUDA than the host driver supports fails no matter how the image is built (Q6).
- **When to use a VM or micro-VM:** running untrusted code (user-submitted notebooks, other tenants' models), hard multi-tenant isolation, different kernel requirements, or compliance rules. Sandboxed runtimes (gVisor, Kata, Firecracker-style micro-VMs; check current docs for each) sit between the two.
- **Failure modes:** `--privileged`, mounting `docker.sock`, or host PID/network namespaces remove the isolation you thought you had. Limits are not automatic: without `--memory`, one container can use the whole host RAM.

**Example:** The script below shows this process's namespace IDs, its cgroup paths and the kernel release (the same kernel a container here would use), then starts a command in a **new PID namespace** using `unshare`, where it sees itself as PID 1 while the host sees a normal PID. That is the container trick without Docker.

**Code:** run with `python3 -I`. Needs Linux; the `unshare` step needs root or user namespaces.
```python
# Q18: look at the kernel features containers are built from: namespaces, cgroups, shared kernel. Read-only; no Docker.
import os, platform, subprocess
print("kernel (shared with every container on this host):", platform.release())
print("namespaces of this process:")
for ns in sorted(os.listdir("/proc/self/ns")):
    print(f"  {ns:18} {os.readlink('/proc/self/ns/' + ns)}")
print("cgroup membership:", open("/proc/self/cgroup").read().strip() or "(none)")
for f in ("memory.max", "cpu.max", "pids.max"):
    p = "/sys/fs/cgroup/" + f
    print(f"  {f:11}", open(p).read().strip() if os.path.exists(p) else "not present here")
# a new PID namespace: the child sees itself as PID 1 (needs root or user namespaces)
r = subprocess.run(["unshare", "--pid", "--fork", "--mount-proc", "python3", "-I", "-c", "import os; print('in new pid ns, my pid =', os.getpid())"],
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
print("host pid of this script:", os.getpid())
```

**Output (my run):** real output of this sandbox. It shows cgroup v1 style paths and no `memory.max` file at the v2 location, so the limit lines say "not present here". On a cgroup v2 host those files exist (see Q19). No container ran (**not executed**, no daemon).
```text
$ python3 -I q18_isolation.py
kernel (shared with every container on this host): 6.18.44-fc-v153
namespaces of this process:
  cgroup             cgroup:[4026531835]
  ipc                ipc:[4026531839]
  mnt                mnt:[4026531832]
  net                net:[4026531833]
  pid                pid:[4026531836]
  pid_for_children   pid:[4026531836]
  time               time:[4026531834]
  time_for_children  time:[4026531834]
  user               user:[4026531837]
  uts                uts:[4026531838]
cgroup membership: 9:name=systemd:/
8:pids:/
7:blkio:/
6:freezer:/
5:devices:/
4:memory:/process_api/01a1784e-af58-7445-8b1b-fa61a2ed0e82/claude-code-bash
3:cpuset:/
2:cpuacct:/
1:cpu:/
0::/
  memory.max  not present here
  cpu.max     not present here
  pids.max    not present here
in new pid ns, my pid = 1
host pid of this script: 13078
```

**Follow-ups:**
- *Is a container secure by default?* Reasonably isolated for trusted code, not a security boundary for hostile code.
- *Can I run a Linux image on a Mac?* Docker Desktop runs a small Linux VM and the containers live inside it.
- *Why is a micro-VM useful?* Near-container start with a separate kernel per workload.

**Common mistakes:**
- "A container is a lightweight VM."
- Saying the image contains the NVIDIA driver.
- Forgetting resource limits.
- Running untrusted notebooks in a shared-kernel container with the Docker socket mounted.

### Q19 ⭐⭐ 🟡 Container killed with exit code 137 or a DataLoader crash 'bus error, shared memory'. Explain what exit 137 means (SIGKILL, often the OOM killer), the difference between --memory limits and host memory, how Python and PyTorch memory behave under a cgroup limit, why DataLoader workers need /dev/shm (default 64 MB in Docker; fix with --shm-size or --ipc=host), and how to confirm OOM (docker inspect OOMKilled, dmesg). Show the run flags and a Python script that reads cgroup memory limits from /sys/fs/cgroup if present.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Exit 137 is 128 plus signal 9, SIGKILL, most often the kernel OOM killer after the container hit its memory limit; the "bus error, shared memory" crash is a different cause: the 64 MB default `/dev/shm`, which DataLoader workers use to pass tensors.

**Then explain:**
- **137:** `128 + 9`. Something sent SIGKILL: the OOM killer, `docker kill`, or `docker stop` after the grace period. Confirm with `docker inspect -f '{{.State.OOMKilled}} {{.State.ExitCode}}' <c>` and `dmesg | grep -i 'killed process'` on the host. Caveat: if the kernel kills a child worker, `OOMKilled` can be false while the symptom is the same.
- **Limits:** `--memory 8g` sets the cgroup limit. Without it the container can use the host's RAM. Tools that read `/proc/meminfo` (and `os.cpu_count()` for CPUs) see the **host**, not the limit, so they plan for more than they will get. Read the cgroup files instead. Setting `--memory-swap` equal to `--memory` disables extra swap.
- **Python and PyTorch under a limit:** page cache, pinned memory, many DataLoader workers (each can hold a copy of the data), and big batches all count. Python often does not return freed memory to the OS right away, so RSS looks high.
- **Shared memory:** DataLoader workers send tensors through `/dev/shm`. Docker gives it 64 MB by default. Symptoms: `RuntimeError: DataLoader worker (pid N) is killed by signal: Bus error` and a message about shared memory. Fixes: `--shm-size=2g` (size it to batch and worker count), or `--ipc=host` (shares the host IPC namespace, so weaker isolation). Last resort: `num_workers=0`.
- **Fixes for 137:** lower batch size or workers, stream data, raise the limit, or find the leak.

**Example:** 4 workers, batch 64 images of 3x224x224 floats is about 38 MB per batch in flight per worker, so a handful of prefetched batches overruns 64 MB at once. Hand-check: 64*3*224*224*4 bytes = 38,535,168 bytes. That is why the default 64 MB breaks.

**Code:**
```bash
# NOT EXECUTED (no daemon)
docker run --rm --gpus all --memory 16g --memory-swap 16g --shm-size 2g myorg/trainer:1.4.0
# or: --ipc=host (less isolation)
docker inspect -f '{{{{.State.OOMKilled}}}} {{{{.State.ExitCode}}}}' train
dmesg | grep -i 'killed process'
```
```python
# Q19: read cgroup memory limit/usage (v2 or v1), /dev/shm size, and show why a SIGKILL exit looks like 137.
import os, subprocess, signal, sys

def rd(p):
    try: return open(p).read().strip()
    except OSError: return None

def mem():
    v2 = rd("/sys/fs/cgroup/memory.max")
    if v2 is not None:
        return "cgroup v2", v2, rd("/sys/fs/cgroup/memory.current"), (rd("/sys/fs/cgroup/memory.events") or "").replace("\n", "; ")
    v1 = rd("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    if v1 is not None:
        return "cgroup v1", v1, rd("/sys/fs/cgroup/memory/memory.usage_in_bytes"), None
    return None

m = mem()
if not m: print("no cgroup memory files visible")
else:
    ver, lim, cur, ev = m
    unlimited = lim == "max" or (lim.isdigit() and int(lim) > 1 << 60)
    print(f"{ver}: limit={'UNLIMITED' if unlimited else str(int(lim)//2**20) + ' MiB'}, current={int(cur)//2**20 if cur else '?'} MiB, events={ev}")
st = os.statvfs("/dev/shm"); print(f"/dev/shm size: {st.f_blocks * st.f_frsize // 2**20} MiB (Docker default for a container is 64 MiB)")
print("host-visible RAM from /proc/meminfo (what many libs wrongly trust):", int(open('/proc/meminfo').readline().split()[1])//1024, "MiB")

# exit 137 = 128 + 9: the process was killed by SIGKILL (the OOM killer sends it, so does docker kill)
p = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(30)"]); p.send_signal(signal.SIGKILL); p.wait()
print("python returncode:", p.returncode, "-> shell/docker would report", 128 + abs(p.returncode))
```

**Output (my run):** the script ran with `python3 -I`. The sandbox shows cgroup v1 with no limit, and `/dev/shm` here is not Docker's 64 MB default, so this run shows the reader working, not an OOM. The exit-code lines come from a real SIGKILL of a child. `docker run` and `docker inspect` were **not executed** (no daemon); `docker run --help` confirms `--memory` and `--shm-size` exist.
```text
$ python3 -I q19_cgroup_mem.py
cgroup v1: limit=UNLIMITED, current=2388 MiB, events=None
/dev/shm size: 16091 MiB (Docker default for a container is 64 MiB)
host-visible RAM from /proc/meminfo (what many libs wrongly trust): 16091 MiB
python returncode: -9 -> shell/docker would report 137
```

**Follow-ups:**
- *Is 137 always OOM?* No. Check `OOMKilled`, `dmesg`, and whether something ran `docker kill` or a stop timed out.
- *Why not always use `--ipc=host`?* It shares IPC with the host and other containers; fine on a private box, poor in multi-tenant setups.
- *Is `--memory` the same as a Kubernetes limit?* Same cgroup idea, set through the pod spec (later part).

**Common mistakes:**
- Raising `num_workers` to speed up and then hitting 137.
- Sizing from `free -m` inside the container.
- Not setting any limit on a shared GPU box.
- Ignoring that page cache and pinned memory count.

### Q20 ⭐⭐ 🟢 Dockerfile instruction details interviewers ask. COPY versus ADD (tar auto-extract, URLs), RUN with && chaining and why a later RUN rm does not shrink an image, apt-get update plus install in one RUN with --no-install-recommends and cleaning /var/lib/apt/lists, WORKDIR versus cd, EXPOSE as documentation only, and LABEL for metadata. Give a before and after Dockerfile and the hadolint rules (DL numbers) that catch each mistake, run if hadolint is installable.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Use `COPY` not `ADD`, chain `apt-get update && install --no-install-recommends && rm -rf /var/lib/apt/lists/*` in ONE `RUN`, use `WORKDIR` not `cd`, and remember a later `RUN rm` cannot shrink an earlier layer.

**Then explain:**
- **COPY vs ADD:** `COPY` copies files. `ADD` also auto-extracts a local tar archive and can fetch a URL. That magic is surprising, so use `COPY`. For downloads, `RUN curl ... && verify checksum` (or `ADD --checksum` where your BuildKit supports it; check current docs).
- **Layers only add:** each `RUN` is a layer. Files deleted in a later layer are only hidden, the earlier layer still ships. So clean up in the same `RUN` that created the files.
- **apt:** `update` and `install` in the same `RUN` (a cached `update` layer goes stale), `--no-install-recommends` for a smaller layer, delete `/var/lib/apt/lists` in that same command. Versions pinning is possible but a trade-off (Q8).
- **WORKDIR vs cd:** `RUN cd /app` only affects that one `RUN`. `WORKDIR` persists, creates the directory and is clearer.
- **EXPOSE** is documentation, it publishes nothing (Q15). **LABEL** adds metadata (use the `org.opencontainers.image.*` keys): source, revision, version. Labels are visible in `docker inspect`, so never put secrets in them.
- **Exec form CMD** (`["python", "serve.py"]`) so signals reach the app (Q11).
- **Failure mode:** a linter cannot see that `RUN rm -rf /root/.cache` in its own layer saves nothing. Only reading the layer sizes with `docker history` shows it (not executed here).

**Example:** Before: 11 findings from 9 rule IDs. After: `slim` base, one apt `RUN`, `WORKDIR`, `COPY`, `--no-cache-dir`, JSON `CMD`. hadolint output shows the rule numbers before, and one remaining warning after, which I suppress on purpose with a comment (`DL3008`, apt version pinning) and a stated reason.

**Code:** before and after Dockerfiles, and the lint commands.
```dockerfile
# ---- Dockerfile.before ----
FROM python:3.12
ADD https://example.com/model.tar.gz /models/
ADD requirements.txt /app/requirements.txt
RUN cd /app
RUN apt-get update
RUN apt-get install -y build-essential libgomp1
RUN pip install -r /app/requirements.txt
COPY . /app
RUN rm -rf /root/.cache
EXPOSE 8000
CMD python /app/serve.py

# ---- Dockerfile.after ----
FROM python:3.12-slim-bookworm
LABEL org.opencontainers.image.title="churn-api" \
      org.opencontainers.image.source="https://example.com/repo"
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "serve.py"]
```
```bash
pip install hadolint-py     # worked here via the proxy: Haskell Dockerfile Linter 2.15.1
hadolint --no-color Dockerfile.before
hadolint --no-color Dockerfile.after
# docker build / docker history on these were NOT EXECUTED (no daemon)
```

**Output (my run):** hadolint ran for real. The suppression in the "after" file is `# hadolint ignore=DL3008` with the reason in the Follow-ups below. Image building was **not executed**.
```text
$ hadolint --no-color q20/Dockerfile.before
q20/Dockerfile.before:3 DL3020 error: Use COPY instead of ADD for files and folders
q20/Dockerfile.before:4 DL3003 warning: Use WORKDIR to switch to a directory
q20/Dockerfile.before:4 SC2164 warning: Use 'cd ... || exit' or 'cd ... || return' in case cd fails.
q20/Dockerfile.before:5 DL3009 info: Delete the apt lists (/var/lib/apt/lists) after installing something
q20/Dockerfile.before:5 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:6 DL3015 info: Avoid additional packages by specifying `--no-install-recommends`
q20/Dockerfile.before:6 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:6 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
q20/Dockerfile.before:7 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
q20/Dockerfile.before:7 DL3042 warning: Avoid use of cache directory with pip. Use `pip install --no-cache-dir <package>`
q20/Dockerfile.before:11 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments

# after (with the ignore comment):
(no findings, exit 0)
# after, ignore comment removed:
/tmp/Dockerfile.noignore:4 DL3008 warning: Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
```
Rule map: DL3020 `ADD` instead of `COPY`; DL3003 `cd` instead of `WORKDIR` (plus shellcheck SC2164); DL3009 apt lists not deleted; DL3015 missing `--no-install-recommends`; DL3008 unpinned apt packages; DL3042 pip cache not disabled; DL3025 shell-form `CMD`; DL3059 consecutive `RUN`s (info). The `RUN rm` in its own layer and the `ADD <url>` are **not** flagged.

**Follow-ups:**
- *Why suppress DL3008?* Debian security updates change versions; pinning breaks builds when old versions leave the mirror. The reason belongs in a comment next to the ignore.
- *Does `ENV` or `ARG` in the same `RUN` help size?* No; size comes from files written.
- *`ADD` of a local `.tar.gz`?* It is extracted. If you wanted the tarball itself, use `COPY`.

**Common mistakes:**
- `RUN apt-get update` on its own line.
- `rm` in a later `RUN`.
- Using `ADD` for plain files.
- Putting secrets in `LABEL`.

### Q21 ⭐⭐ 🟢 ARG versus ENV, build time versus run time configuration. Explain scope and visibility of each (ARG gone at runtime but visible in history, ENV persists), how --build-arg and docker run -e or --env-file work, why model paths and thresholds should be runtime config (12-factor), why FROM can use ARG before the first stage, and the ARG-before-FROM scope gotcha in multi-stage builds. Show a small Dockerfile and a script that lists which variables are build-only.
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** `ARG` exists only while building and is gone at runtime (but its value can still show in `docker history`); `ENV` is baked into the image and visible to the running process; model paths and thresholds should be runtime config so one image works everywhere.

**Then explain:**
- **ARG:** set with `--build-arg NAME=value`; usable in later build instructions in its stage; not in the container's environment at run time. Never pass secrets this way, they appear in image metadata (Q9).
- **ENV:** persists into the image and the running container. A default can be overridden at run time with `docker run -e NAME=value` or `--env-file file`. `-e NAME` with no value passes the host's current value through.
- **12-factor:** config that changes between environments (model path, threshold, feature flags, URLs) belongs in environment variables at run time, not in the image. One image, many environments, no rebuild to change a threshold.
- **ARG before FROM:** allowed, but only for use in `FROM` lines (for example `FROM python:${PY_VERSION}-slim`). After `FROM`, that value is out of scope. To use it inside the stage, redeclare the name: `ARG PY_VERSION`. Each stage has its own scope too, so declare ARGs again in every stage that needs them.
- **Pattern for build info:** `ARG GIT_SHA` then `LABEL ...revision="${GIT_SHA}"` or `ENV BUILD_SHA=${GIT_SHA}` when the app should report its own version. Remember that this changes the layer on every commit, so place it late (Q2).
- **Failure modes:** an ARG used in a stage where it was not declared silently expands to an empty string; an `ENV` default hides a missing runtime variable; baking a threshold into `ENV` and forgetting it is overridable.

**Example:** In the sample Dockerfile below, `PY_VERSION` is declared globally and used in two `FROM` lines. Only stage 1 redeclares it, so only stage 1 can use it in `RUN`. `GIT_SHA` is build-only, but stage 1 copies its value into `ENV BUILD_SHA`, so the value does survive at runtime that way. `MODEL_PATH` and `THRESHOLD` are runtime ENV with defaults.

**Code:** the Dockerfile, the scope script, and commands that were not executed.
```dockerfile
ARG PY_VERSION=3.12
FROM python:${PY_VERSION}-slim AS builder
ARG PIP_INDEX_URL=https://pypi.org/simple
ARG GIT_SHA=unknown
RUN echo "index is $PIP_INDEX_URL, sha is $GIT_SHA"

FROM python:${PY_VERSION}-slim
ARG GIT_SHA
ENV MODEL_PATH=/models/churn.pkl \
    THRESHOLD=0.5 \
    BUILD_SHA=${GIT_SHA}
LABEL org.opencontainers.image.revision="${GIT_SHA}"
ARG PY_VERSION
RUN echo "python is ${PY_VERSION}"
CMD ["python", "-c", "import os; print(os.environ['MODEL_PATH'], os.environ['THRESHOLD'])"]
```
```bash
# NOT EXECUTED (no daemon)
docker build --build-arg GIT_SHA=$(git rev-parse --short HEAD) -t myorg/api:dev .
docker run --rm -e THRESHOLD=0.7 -e MODEL_PATH=/models/v2.pkl myorg/api:dev
docker run --rm --env-file prod.env myorg/api:dev      # file lines are KEY=VALUE, # comments allowed
```
```python
# Q21: list ARG/ENV scope per stage: which ARGs are build-only, which become runtime ENV, and the ARG-before-FROM gotcha.
import re, sys
text = open(sys.argv[1]).read().replace("\\\n", " ")
global_args, stage, stages = {}, None, []
for ln in text.splitlines():
    ln = ln.strip()
    m = re.match(r"(ARG|ENV|FROM)\s+(.*)", ln, re.I)
    if not m: 
        if stage is not None and re.match(r"RUN|CMD|LABEL", ln): stage["uses"] |= set(re.findall(r"\$\{?(\w+)", ln))
        continue
    k, rest = m.group(1).upper(), m.group(2)
    if k == "ARG" and stage is None:
        n = rest.split("=")[0]; global_args[n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "FROM":
        stage = {"from": rest, "args": {}, "env": {}, "uses": set()}; stages.append(stage)
    elif k == "ARG":
        n = rest.split("=")[0]; stage["args"][n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "ENV":
        for n, v in re.findall(r"(\w+)=(\S+)", rest): stage["env"][n] = v; stage["uses"] |= set(re.findall(r"\$\{?(\w+)", v))
print("global ARGs (before first FROM):", list(global_args), "-> usable ONLY in FROM lines unless redeclared")
for i, s in enumerate(stages):
    print(f"\nstage {i}: FROM {s['from']}")
    for n in s["args"]:
        in_env = n in s["env"] or any(f"${{{n}}}" in v or f"${n}" in v for v in s["env"].values())
        redeclared = n in global_args
        status = "build-only (gone at runtime)"
        extra = " (redeclared: value inherited from global default)" if redeclared and s["args"][n] is None else ""
        print(f"  ARG {n:14} {status}{extra}; value baked into an ENV: {in_env}")
    for n, v in s["env"].items(): print(f"  ENV {n:14} runtime (visible in docker inspect/ps env): {v}")
    for u in sorted(s["uses"]):
        if u not in s["args"] and u not in s["env"]: print(f"  WARNING: ${u} used but not declared in this stage (empty at build time)")
```

**Output (my run):** the script and hadolint ran. Building and running the image were **not executed** (no daemon). The script is a line-based reader (handles `\` continuations, `KEY=value` ENV only), not a full Dockerfile parser.
```text
$ python3 -I q21_scope.py q21/Dockerfile
global ARGs (before first FROM): ['PY_VERSION'] -> usable ONLY in FROM lines unless redeclared

stage 0: FROM python:${PY_VERSION}-slim AS builder
  ARG PIP_INDEX_URL  build-only (gone at runtime); value baked into an ENV: False
  ARG GIT_SHA        build-only (gone at runtime); value baked into an ENV: False

stage 1: FROM python:${PY_VERSION}-slim
  ARG GIT_SHA        build-only (gone at runtime); value baked into an ENV: True
  ARG PY_VERSION     build-only (gone at runtime) (redeclared: value inherited from global default); value baked into an ENV: False
  ENV MODEL_PATH     runtime (visible in docker inspect/ps env): /models/churn.pkl
  ENV THRESHOLD      runtime (visible in docker inspect/ps env): 0.5
  ENV BUILD_SHA      runtime (visible in docker inspect/ps env): ${GIT_SHA}
$ hadolint --no-color q21/Dockerfile
(no findings, exit 0)
```

**Follow-ups:**
- *Why does ARG show in history?* Build args are recorded in the image's build metadata and layer commands.
- *How do I see runtime env?* `docker inspect` shows ENV and `-e` values for a container, so no secrets there either on shared hosts.
- *Where do big configs go?* A mounted file, with the path in an env var.

**Common mistakes:**
- Expecting an ARG to exist in the running container.
- Using `ARG` before `FROM` inside the stage without redeclaring.
- Baking environment-specific URLs into the image.
- Putting a changing ARG (commit hash) early in the Dockerfile and killing the cache.

### Q22 ⭐⭐ 🟡 Tagging and versioning images for ML. Compare latest, semantic version, git SHA and model-version tags, why latest is a trap for rollbacks, why tags are mutable and digests immutable, how to tag one image several ways, and how to tie an image to a model registry version and a training run. Propose a tag scheme for a team that ships a model API weekly and retrains monthly, and show the docker tag and push commands (not executed, no registry here).
**Asked at:** Editorial Docker interview guides (Techoral 'Docker Interview Questions 2026', Cloud Soft Solutions 2026 guide, KodeKloud, Adaface, MentorCruise; search snippets only, not opened); guides, not verified candidate reports; DevOps, MLOps and ML engineer screens, including IT-services and GCC hiring
**Say this first (1 line):** Tag every image with an immutable identifier (git SHA), add human tags (semantic version, model version), treat `latest` and environment names as moving pointers only, and deploy by digest so you always know what ran.

**Then explain:**
- **`latest`** is just a default tag name, not "newest". It is mutable. Rollback by "the previous latest" is impossible, because that tag now points at the new image. Two nodes can pull different images under the same tag.
- **Tags are mutable pointers; digests are immutable.** A digest (`@sha256:...`) is the hash of the manifest. Some registries can enforce tag immutability (check current docs). Deploying `repo@sha256:...` guarantees the same bytes.
- **One image, many tags:** `docker tag` adds names to the same image ID. Pushing them uploads the layers once.
- **Link to model and run:** put the model registry version and training run ID in image labels and in the tag if the model is baked in. Also record the image digest back in the model registry entry, so you can go both ways.
- **Weekly code, monthly retrain scheme (proposal):**
  - Code release tag `1.14.0` (semver, weekly).
  - `1.14.0-g9f3c2a1`, the exact commit, built once by CI. The others are retags of it.
  - `sha-<12 chars>` for any commit build.
  - `1.14.0-churn-m23` when model version 23 is baked in. If weights are mounted or downloaded (Q16), the model version goes in runtime config and the tag only tracks code.
  - `staging` and `prod` as moving pointers, set by the deploy job, never used as the only record.
- **Failure modes:** tag collisions from retagging `1.14.0` after a hotfix (cut `1.14.1` instead); invalid tag characters or over 128 chars; a retention rule that deletes the tag your rollback needs.

**Example:** Release 1.14.0 moves `latest`. The script prints the registry state: before and after, `latest` points somewhere else, while `1.13.0` still points to the previous image, so rollback by version works and by `latest` does not.

**Code:** the script ran; the `docker` commands it prints were not executed.
```python
# Q22: build a tag set for one image, validate tag syntax, print the (not executed) docker commands, and show why 'latest' breaks rollback.
import re, datetime as dt
TAG_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")     # Docker tag grammar (check current docs)

def tags(app_ver, git_sha, model_name, model_ver, run_id, built, channel=None):
    t = [f"{app_ver}",                                   # human release, moves nothing once pushed
         f"{app_ver}-g{git_sha[:7]}",                    # exact code
         f"sha-{git_sha[:12]}",                          # CI convenience, unique per commit
         f"{app_ver}-{model_name}-m{model_ver}",         # which registry model version is inside / configured
         f"{built:%Y%m%d}-m{model_ver}"]                 # date for humans and retention rules
    if channel: t.append(channel)                        # moving pointer: staging / prod. NEVER the only tag
    return t

built = dt.date(2026, 10, 26)
ts = tags("1.14.0", "9f3c2a1b7d4e5f60", "churn", 23, "run-8841", built, channel="staging")
for t in ts: print(f"{t:32} valid={bool(TAG_RE.match(t))}")
bad = ["churn:v1", "my tag", "-lead", "x" * 129]
print("invalid examples:", [(b[:12], bool(TAG_RE.match(b))) for b in bad])

img, reg = "churn-api", "registry.example.com/ml"
print("\n# NOT EXECUTED (no registry, no daemon):")
print(f"docker build -t {reg}/{img}:{ts[1]} --label org.opencontainers.image.revision=9f3c2a1b7d4e5f60 --label ml.model.version=23 --label ml.run.id=run-8841 .")
for t in ts[:1] + ts[2:]: print(f"docker tag {reg}/{img}:{ts[1]} {reg}/{img}:{t}")
print(f"docker push --all-tags {reg}/{img}")

# latest vs immutable-by-convention: a registry as a dict tag -> digest
reg_state = {"latest": "sha256:aaa1", "1.13.0": "sha256:aaa1"}
reg_state["latest"] = "sha256:bbb2"; reg_state["1.14.0"] = "sha256:bbb2"       # a release moves latest
print("\nafter release 1.14.0, 'latest' ->", reg_state["latest"], "| what was running before? unknown unless you recorded the digest")
print("rollback by tag 1.13.0 ->", reg_state["1.13.0"], "(still there)")
```

**Output (my run):** the script ran with `python3 -I`. `docker build`, `docker tag`, `docker push` were **not executed** (no daemon, no registry); `docker tag --help` and `docker push --help` ran and confirm `--all-tags` exists. The commit hash and registry host are made-up examples.
```text
$ python3 -I q22_tags.py
1.14.0                           valid=True
1.14.0-g9f3c2a1                  valid=True
sha-9f3c2a1b7d4e                 valid=True
1.14.0-churn-m23                 valid=True
20261026-m23                     valid=True
staging                          valid=True
invalid examples: [('churn:v1', False), ('my tag', False), ('-lead', False), ('xxxxxxxxxxxx', False)]

# NOT EXECUTED (no registry, no daemon):
docker build -t registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 --label org.opencontainers.image.revision=9f3c2a1b7d4e5f60 --label ml.model.version=23 --label ml.run.id=run-8841 .
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:1.14.0
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:sha-9f3c2a1b7d4e
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:1.14.0-churn-m23
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:20261026-m23
docker tag registry.example.com/ml/churn-api:1.14.0-g9f3c2a1 registry.example.com/ml/churn-api:staging
docker push --all-tags registry.example.com/ml/churn-api

after release 1.14.0, 'latest' -> sha256:bbb2 | what was running before? unknown unless you recorded the digest
rollback by tag 1.13.0 -> sha256:aaa1 (still there)
$ docker push --help | grep -E -- '--all-tags'
      -a, --all-tags          Push all tags of an image to the repository
```

**Follow-ups:**
- *How does the cluster deploy?* Reference the digest (or a tag that the deploy job records as a digest). Tools differ; check current docs.
- *Can I reuse a version tag?* Don't. If you must, you have lost auditability.
- *Date tags?* Handy for retention and humans, not for identity.

**Common mistakes:**
- Deploying `latest`.
- Not recording which model went into which image.
- Moving a release tag after a hotfix.
- Tags with `/`, spaces or a leading dash.

### Q23 ⭐⭐ 🟡 Container registries for ML teams: Docker Hub, GitHub Container Registry, and cloud registries (ECR, Artifact Registry, ACR; hedge names and check current docs). Explain push and pull flow, authentication (docker login, short-lived tokens), Docker Hub pull rate limits and mirrors or pull-through caches, private versus public images, image retention and cleanup policies, and cost of storing many 8 GB images. Cloud-specific ECR and IAM details belong to a later part; stay on registry concepts. Mark all commands not executed.
**Asked at:** Bengaluru MLOps job postings that list Docker, Kubernetes and GPU/CUDA workloads (Infosys-linked, Quantiphi-linked, Skyworks, GrabJobs listings; snippets only) plus editorial Docker interview guides (snippets only); postings show required skills, not interview questions; IT-services firms, GCCs and AI product companies in India
**Say this first (1 line):** A registry stores images by repository, tag and digest; you log in, push layers (only missing ones are uploaded), and pull from nodes. For ML teams the real concerns are rate limits, private access, cleanup and the cost of many large images.

**Then explain:**
- **Names:** `registry/repo:tag` or `@digest`. With no registry the CLI assumes Docker Hub; a single-name official image like `python` becomes `docker.io/library/python`. The script below parses these.
- **Flow:** `docker login registry` stores credentials (by default in `~/.docker/config.json`; a credential helper is safer). `docker push` uploads each layer blob that the registry does not already have, then the manifest that lists them. `docker pull` fetches the manifest, then only layers the node lacks. This is why layer order and sharing matter (Q2, Q7).
- **Auth:** prefer `--password-stdin` with a token over typing a password. In CI use short-lived tokens or workload identity where the registry supports it (check current docs; the cloud-specific IAM details come in a later part). Never bake registry credentials into images.
- **Registries (hedged):** Docker Hub; GitHub Container Registry (`ghcr.io`), tied to your GitHub org permissions; cloud registries from the big cloud providers (AWS ECR, Google Artifact Registry, Azure Container Registry), which integrate with cloud identity and live near your compute. Check current docs for features and limits.
- **Docker Hub rate limits:** anonymous and free-tier pulls are limited per time window, and the limits change (check current docs). A cluster pulling the same base image from many nodes behind one IP can hit them. Mitigations: log in with a token, mirror base images into your own registry, or run a pull-through cache (`registry-mirrors` in `daemon.json`, or a registry configured as a proxy cache).
- **Public vs private:** weights, proprietary code and data baked in images must be private. Public images leak whatever is in their layers (Q9).
- **Retention and cost:** old images pile up. Cost grows with unique layer bytes stored (shared layers are stored once) plus transfer across regions or out of the cloud. Use lifecycle or cleanup policies (the names differ by registry): keep tags in use and the last N releases, expire untagged manifests, expire PR/CI tags quickly. Do not delete the tag a rollback needs.
- **Failure modes:** rate-limited pull during an autoscale event; expired token; deleting a tag that production still references; a rebuilt base layer that makes every new image share nothing.

**Example:** With toy sizes (MB): base 2000, deps 5000, four app layers of 20, two model layers of 1500. Four images listed by tag sum to 31,080 MB if you count each separately, but the registry stores 10,080 MB because base and deps are shared. Delete the oldest tag and 20 MB comes back; change the base and 7,000 MB is added. The numbers are invented to show the effect.

**Code:** the parser and retention simulation ran. The commands are not executed.
```bash
# NOT EXECUTED (no daemon, no registry, no credentials)
echo "$REGISTRY_TOKEN" | docker login ghcr.io -u myuser --password-stdin
docker push ghcr.io/myorg/churn-api:1.14.0
docker pull ghcr.io/myorg/churn-api:1.14.0
# pull-through cache / mirror: set in /etc/docker/daemon.json  {{"registry-mirrors": ["https://mirror.example.com"]}}
```
```python
# Q23: (1) parse image references the way the docker CLI normalises them, (2) simulate a retention policy and layer-shared storage.
import re

def parse(ref):
    digest = None
    if "@" in ref: ref, digest = ref.split("@", 1)
    first, _, rest = ref.partition("/")
    if rest and ("." in first or ":" in first or first == "localhost"): reg, path = first, rest
    else: reg, path = "docker.io", ref                      # default registry (Docker Hub)
    if reg == "docker.io" and "/" not in path: path = "library/" + path   # official images
    tag = None
    if ":" in path.rsplit("/", 1)[-1]: path, tag = path.rsplit(":", 1)
    if tag is None and digest is None: tag = "latest"
    return reg, path, tag, digest

for r in ["python:3.12-slim", "myorg/trainer:1.4.0", "ghcr.io/myorg/api:sha-9f3c2a1",
          "123456789012.dkr.ecr.us-east-1.amazonaws.com/ml/api:1.0", "localhost:5000/ml/api",
          "python@sha256:" + "ab" * 32]:
    reg, path, tag, dg = parse(r); print(f"{r[:30]:30} -> registry={reg:34} repo={path:16} tag={tag} digest={'yes' if dg else '-'}")

# Retention: keep tags in use + newest N release tags; untagged manifests expire. Sizes are layer MB (toy numbers).
layers = {"base": 2000, "deps": 5000, "app1": 20, "app2": 20, "app3": 20, "app4": 20, "model_v1": 1500, "model_v2": 1500}
images = {  # tag -> layers, newest last
    "1.10.0": ["base", "deps", "app1"], "1.11.0": ["base", "deps", "app2"],
    "1.12.0": ["base", "deps", "app3", "model_v1"], "1.13.0": ["base", "deps", "app4", "model_v2"]}
def stored(tags): return sum(layers[l] for l in {l for t in tags for l in images[t]})
naive = sum(layers[l] for t in images for l in images[t])
print(f"\nsum of image sizes (no sharing): {naive} MB | stored with layer sharing: {stored(images)} MB")
in_use = {"1.12.0", "1.13.0"}; keep_new = 3
keep = in_use | set(list(images)[-keep_new:])
print("keep:", sorted(keep), "| delete:", sorted(set(images) - keep), "| stored after cleanup:", stored(keep), "MB")
print("lesson: a changed base or deps layer breaks sharing, so every rebuild then costs the full", layers["base"] + layers["deps"], "MB again")
```

**Output (my run):** the script ran with `python3 -I`. All `docker login/push/pull` commands are **not executed** (no daemon, no registry); `docker login --help` ran to confirm `--password-stdin`. No rate-limit or cloud behaviour was tested.
```text
$ python3 -I q23_registry.py
python:3.12-slim               -> registry=docker.io                          repo=library/python   tag=3.12-slim digest=-
myorg/trainer:1.4.0            -> registry=docker.io                          repo=myorg/trainer    tag=1.4.0 digest=-
ghcr.io/myorg/api:sha-9f3c2a1  -> registry=ghcr.io                            repo=myorg/api        tag=sha-9f3c2a1 digest=-
123456789012.dkr.ecr.us-east-1 -> registry=123456789012.dkr.ecr.us-east-1.amazonaws.com repo=ml/api           tag=1.0 digest=-
localhost:5000/ml/api          -> registry=localhost:5000                     repo=ml/api           tag=latest digest=-
python@sha256:abababababababab -> registry=docker.io                          repo=library/python   tag=None digest=yes

sum of image sizes (no sharing): 31080 MB | stored with layer sharing: 10080 MB
keep: ['1.11.0', '1.12.0', '1.13.0'] | delete: ['1.10.0'] | stored after cleanup: 10060 MB
lesson: a changed base or deps layer breaks sharing, so every rebuild then costs the full 7000 MB again
$ docker login --help | grep -- '--password-stdin'
      --password-stdin    Take the Password or Personal Access Token
```

**Follow-ups:**
- *Why not `docker login -p`?* The password shows in shell history and process lists.
- *Mirror or pull-through cache?* A mirror is a copy you maintain; a pull-through cache fetches on demand and keeps what it saw. Either avoids upstream limits.
- *Where do big model files go?* Often outside the registry (object storage or a volume, Q16), which also keeps image storage down.

**Common mistakes:**
- Relying on anonymous Docker Hub pulls in production.
- No cleanup policy until the bill arrives.
- Deleting by age and removing a tag in use.
- Rebuilding the base layer constantly, so nothing is shared.
