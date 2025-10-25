#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Postgres not ready yet..."
  sleep 2
done

echo "PostgreSQL is ready!"

exec "$@"
