#!/bin/bash

echo "Pulling latest code..."
git pull

echo "Starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Reloading Caddy..."
sudo caddy reload --config /etc/caddy/Caddyfile
