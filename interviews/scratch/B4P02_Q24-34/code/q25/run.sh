# NOT EXECUTED (no daemon, no GPU here). Run on the GPU box.
docker run --rm -it --name lab-$USER \
  --user "$(id -u):$(id -g)" -e HOME=/home/ds \
  --gpus '"device=0"' --shm-size=8g \
  -p 127.0.0.1:8888:8888 \
  -e JUPYTER_TOKEN="$JUPYTER_TOKEN" \
  -v "$PWD":/workspace -v ds-home:/home/ds -v /data/shared:/data:ro \
  -w /workspace jupyter-gpu:2026-10 \
  jupyter lab --ip=0.0.0.0 --no-browser
# From the laptop:  ssh -L 8888:localhost:8888 user@gpu-box   then open http://localhost:8888
