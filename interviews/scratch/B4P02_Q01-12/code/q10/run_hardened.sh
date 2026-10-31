# NOT EXECUTED here (no daemon). Equivalent docker run:
docker run -d --name model --user 10001:10001 --read-only --tmpfs /tmp:rw,size=256m \
  --cap-drop ALL --security-opt no-new-privileges:true \
  -v model_vol:/models:ro -p 8000:8000 myorg/model:1.0
# CI (names are examples; check current docs for your scanner):  trivy image --exit-code 1 --severity HIGH,CRITICAL myorg/model:1.0
# NEVER:  -v /var/run/docker.sock:/var/run/docker.sock   --privileged
