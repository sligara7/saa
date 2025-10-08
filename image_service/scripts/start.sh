#!/bin/bash
set -e

# Initialize storage
echo "Initializing storage..."
/app/scripts/init_storage.sh

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

# Download model if not present
echo "Checking model files..."
python << END
import os
from huggingface_hub import snapshot_download

model_id = "stabilityai/stable-diffusion-xl-base-1.0"
if not os.path.exists("/app/models/sdxl"):
    print(f"Downloading {model_id}...")
    snapshot_download(
        repo_id=model_id,
        local_dir="/app/models/sdxl",
        local_dir_use_symlinks=False
    )
END

# Start the application with uvicorn
echo "Starting service..."
uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8002 \
    --workers 4 \
    --proxy-headers \
    --forwarded-allow-ips '*'