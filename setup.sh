#!/bin/bash
echo "Opening VSCode"
code . &

echo "Opening Docker Desktop"
"C:/Program Files/Docker/Docker/frontend/Docker Desktop.exe" &&

echo "Building and Spinning Up Containers"
docker compose -f compose.nginx.yaml up -d --build &&

echo "Activating Virtual Environment"
source env/Scripts/activate