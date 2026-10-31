# NOT EXECUTED here (no Docker daemon). Run on a machine with Docker.
docker run -d --name m1 myorg/model:1.0 sleep 3600
docker exec m1 sh -c 'echo v2 > /app/model.pkl; echo hi > /tmp/x'
docker diff m1            # C /app/model.pkl ; A /tmp/x   (changes in the writable layer)
docker history myorg/model:1.0   # read-only layers, newest first
docker restart m1         # writable layer SURVIVES restart
docker rm -f m1           # writable layer is deleted here
docker run --rm myorg/model:1.0 cat /app/model.pkl   # original again
docker run -v model_vol:/models myorg/model:1.0      # data that must outlive the container
docker commit m1 myorg/model:hotfix   # works, but avoid it
