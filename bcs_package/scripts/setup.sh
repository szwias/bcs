#!/usr/bin/env bash
set -e

cd /home/ubuntu/src
docker login

echo "==> Pulling images"
docker pull postgres:14
docker pull szwias/bcs-web:latest

echo "==> Starting containers"
docker-compose up -d

echo "==> Waiting for database"
sleep 10

echo "==> Restoring database"
docker exec -i bcs_db psql -U projectuser -d bcs_db < bcs_dump.sql

echo "==> Restarting web"
docker-compose restart web
