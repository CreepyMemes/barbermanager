#!/bin/bash

echo "Pulling latest code..."
git pull

echo "Starting containers..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Reloading Nginx..."
sudo nginx -t && sudo nginx -s reload
