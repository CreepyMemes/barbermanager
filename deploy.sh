#!/bin/bash

echo "Pulling latest code..."
git pull

echo "Starting containers..."
docker compose up -d

echo "Reloading Caddy..."
sudo caddy reload --config /etc/caddy/Caddyfile
