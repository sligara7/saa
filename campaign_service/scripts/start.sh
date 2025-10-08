#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for database..."
python << END
import sys
import time
import asyncpg
from os import environ

max_retries = 30
retries = 0
while retries < max_retries:
    try:
        conn = asyncpg.connect(environ['DATABASE_URL'])
        conn.close()
        sys.exit(0)
    except:
        retries += 1
        print(f"Database connection attempt {retries} of {max_retries}")
        time.sleep(1)
sys.exit(1)
END

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Start the application with uvicorn
echo "Starting service..."
uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --proxy-headers \
    --forwarded-allow-ips '*'