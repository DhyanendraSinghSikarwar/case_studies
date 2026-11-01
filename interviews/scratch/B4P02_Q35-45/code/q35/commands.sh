# NOT executed here (needs a Docker daemon)
docker build --target test -t ml-svc:test .                 # builds base + test stage
docker run --rm ml-svc:test                                 # runs pytest in the image
docker run --rm -v "$PWD/src:/app/src:ro" -v "$PWD/tests:/app/tests:ro" ml-svc:test   # fast local loop
docker compose -f compose.test.yml up --build --exit-code-from tests --abort-on-container-exit
docker build --target final -t ml-svc:1.0 .                 # no pytest in this image
