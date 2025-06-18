#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"


if [ "$RUN_MIGRATIONS" = "1" ]; then
    python manage.py migrate
fi

exec "$@"