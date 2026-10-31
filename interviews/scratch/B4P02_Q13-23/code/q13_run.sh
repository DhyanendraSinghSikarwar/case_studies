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
