#!/bin/sh
set -e
echo "entrypoint: warming up"
exec python3 "$@"
