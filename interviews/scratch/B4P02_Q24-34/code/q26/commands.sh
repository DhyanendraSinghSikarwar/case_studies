# NOT EXECUTED (needs a daemon or a registry). Shown for the interview.
docker buildx create --use --name multi                       # a builder that can do multi-platform
docker buildx build --platform linux/amd64,linux/arm64 \
    -t registry.example.com/team/model-api:1.4.0 --push .      # pushes ONE tag that points to a manifest list
docker buildx imagetools inspect registry.example.com/team/model-api:1.4.0   # lists the platforms
docker image inspect --format '{{.Os}}/{{.Architecture}}' model-api:dev       # arch of a local image
docker run --rm --platform linux/amd64 model-api:dev          # on an M-series Mac: runs under QEMU emulation (slow)
# CI, native runners, one build per arch, then merge: see Q33 for caching
