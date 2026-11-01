# NOT EXECUTED here (no daemon).
docker build --secret id=pip_token,env=PIP_TOKEN -t myorg/model:1.0 .     # from an env var
docker build --secret id=pip_token,src=$HOME/.pip_token -t myorg/model:1.0 .   # or from a file
docker history --no-trunc myorg/model:1.0 | grep -i token                 # should print nothing
docker run --rm --env-file runtime.env myorg/model:1.0                   # runtime secret, not baked in
