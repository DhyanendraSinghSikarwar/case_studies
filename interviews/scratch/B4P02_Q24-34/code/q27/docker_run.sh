# NOT EXECUTED (no daemon). 'ckpt' is a named volume, so it survives the container being replaced.
docker run --name train-42 --init --gpus all --stop-timeout 60 \
  -v ckpt:/ckpt -e CKPT_PATH=/ckpt/state.json \
  --restart on-failure:5 \
  model-train:1.4.0 python train.py
# docker stop sends SIGTERM, waits 60 s, then SIGKILL. On a spot reclaim the node often gives
# only a short warning (check your cloud's docs), so keep SAVE_EVERY small too.
