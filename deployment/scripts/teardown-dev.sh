#!/bin/bash
set -e

# Stop all services
echo "Stopping services..."
podman-compose down

# Clean up data directories if --clean flag is provided
if [ "$1" == "--clean" ]; then
    echo "Cleaning up data directories..."
    rm -rf ./data/postgres ./data/minio ./data/redis ./data/rabbitmq
    rm -rf ./*/alembic/versions/[0-9]*_*.py
    rm -f .env
    echo "Cleanup complete!"
else
    echo "Data directories preserved. Use '--clean' to remove all data."
fi