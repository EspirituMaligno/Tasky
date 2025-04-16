#!/bin/sh

# Ожидание готовности PostgreSQL
echo "Waiting for PostgreSQL to start..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Ожидание готовности Redis
echo "Waiting for Redis to start..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo "Redis started"

# Применение миграций Alembic (если нужно)
alembic upgrade head

# Запуск приложения
exec "$@"