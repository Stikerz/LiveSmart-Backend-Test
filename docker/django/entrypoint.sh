#!/usr/bin/env bash

set -o errexit
set -o pipefail

# todo: turn on after #1295
# set -o nounset


cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_USER

exec $cmd