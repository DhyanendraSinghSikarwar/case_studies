# NOT EXECUTED (needs a daemon or BuildKit builder and a registry).
# Registry cache: a separate tag holds cache metadata (and layers with mode=max)
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/example-org/model-api:buildcache \
  --cache-to   type=registry,ref=ghcr.io/example-org/model-api:buildcache,mode=max \
  -t ghcr.io/example-org/model-api:"$GIT_SHA" --push .
# Inline cache: cache metadata inside the image itself (only exports the final image's layers)
docker buildx build --cache-to type=inline --cache-from type=registry,ref=ghcr.io/example-org/model-api:latest -t ... --push .
