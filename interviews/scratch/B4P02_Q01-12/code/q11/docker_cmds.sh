# NOT EXECUTED here (no daemon)
docker run myorg/model:1.0                         # entrypoint.sh uvicorn src.api:app ...
docker run myorg/model:1.0 python -m src.train     # CMD replaced, ENTRYPOINT kept
docker run --entrypoint sh -it myorg/model:1.0     # ENTRYPOINT replaced (CMD becomes args to sh)
docker run --init myorg/model:1.0                  # tini as PID 1: forwards signals, reaps zombies
docker stop -t 30 model                            # SIGTERM, wait 30 s, then SIGKILL
