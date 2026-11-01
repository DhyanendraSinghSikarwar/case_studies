# NOT EXECUTED here: needs a GPU host with Docker. Order of checks when a GPU container fails.
nvidia-smi                                   # 1. host driver works?
nvidia-ctk --version                         # 2. toolkit installed?
sudo nvidia-ctk runtime configure --runtime=docker   # writes the runtime into /etc/docker/daemon.json
sudo systemctl restart docker                # 3. daemon must restart to pick it up
docker info | grep -i runtimes               # 4. nvidia listed?
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi   # 5. smoke test (tag is an example)
docker run --rm --gpus all myorg/model-gpu:1.0 python -c "import torch;print(torch.cuda.is_available())"
docker exec c env | grep NVIDIA              # 6. NVIDIA_VISIBLE_DEVICES / DRIVER_CAPABILITIES set?
