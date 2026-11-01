#!/usr/bin/env bash
# Q41: validate a compose file without a daemon
docker compose -f compose.yml config
echo "--- typo file"
docker compose -f bad.yml config; echo "exit=$?"
