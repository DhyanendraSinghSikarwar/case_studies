# NOT EXECUTED (no daemon). Triage order for a container that will not stay up.
docker ps -a --filter name=api                       # 1. what state, what exit code, how long ago
docker logs --tail 100 api                           # 2. the app's own last words (stdout/stderr)
docker inspect api --format '{{json .State}}'        # 3. ExitCode, OOMKilled, Error (runtime errors live here, not in logs)
docker events --since 10m --filter container=api     # 4. die / oom / restart timeline
docker run --rm -it --entrypoint sh model-api:dev    # 5. get a shell INSIDE the image without the broken entrypoint
docker exec -it api sh                               # 6. only works while it is up
