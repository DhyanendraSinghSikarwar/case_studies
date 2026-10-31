#!/usr/bin/env bash
set -euo pipefail

# 1. defaults from env
: "${MODEL_DIR:=/tmp/models}"
: "${DEP_HOST:=127.0.0.1}"
: "${DEP_PORT:=5999}"
: "${DEP_TIMEOUT:=10}"

# 2. wait for a dependency, with a timeout (bash /dev/tcp, no extra tools needed)
echo "[entrypoint] pid=$$ waiting for ${DEP_HOST}:${DEP_PORT} (max ${DEP_TIMEOUT}s)"
deadline=$(( $(date +%s) + DEP_TIMEOUT ))
until (exec 3<>"/dev/tcp/${DEP_HOST}/${DEP_PORT}") 2>/dev/null; do
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "[entrypoint] dependency not reachable, giving up" >&2
    exit 1
  fi
  sleep 0.5
done
echo "[entrypoint] dependency is up"

# 3. one-time setup: model download stand-in (idempotent: skip if already there)
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_DIR/model.bin" ]; then
  echo "[entrypoint] fetching model into $MODEL_DIR"
  printf 'fake-weights' > "$MODEL_DIR/model.bin"
else
  echo "[entrypoint] model already present, skipping download"
fi

# 4. hand over: exec replaces the shell, the server becomes PID 1 in a container
echo "[entrypoint] exec: $*"
"$@"
