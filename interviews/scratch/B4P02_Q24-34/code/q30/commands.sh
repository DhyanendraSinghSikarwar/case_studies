# NOT EXECUTED against a daemon. Read-only first, destructive last.
docker system df                         # images, containers, volumes, build cache: size and RECLAIMABLE
docker system df -v                      # per-image / per-volume detail
docker image prune                       # dangling (untagged) images only
docker image prune -a --filter "until=720h"   # ALL images not used by a container, older than 30 days
docker container prune                   # stopped containers
docker builder prune                     # build cache
docker volume prune                      # unused anonymous volumes (add -a for named ones: data loss risk)
docker system prune                      # stopped containers, unused networks, dangling images, build cache
docker system prune -a --volumes         # the dangerous one: also unused images AND unused volumes
# per-container override of the default log settings:
docker run --log-driver json-file --log-opt max-size=50m --log-opt max-file=3 model-api:1.4.0
