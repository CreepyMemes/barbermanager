#!/bin/bash
set -e  # Exit on first error

echo "Pulling latest code..."
git config --global --add safe.directory "$(pwd)"  # Fix Git safe-dir issue in some CI
git pull origin master

echo "Starting containers..."
sudo docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

echo "Reloading Nginx..."
sudo nginx -t && sudo nginx -s reload
