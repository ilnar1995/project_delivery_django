#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 2
    done
    sleep 7
    echo "PostgreSQL started"
fi

exec "$@"