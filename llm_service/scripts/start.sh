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

# Wait for Redis to be ready
echo "Waiting for Redis..."
python << END
import sys
import time
import redis
from os import environ

redis_url = environ.get('REDIS_URL', 'redis://localhost:6379')
max_retries = 30
retries = 0
while retries < max_retries:
    try:
        r = redis.from_url(redis_url)
        r.ping()
        sys.exit(0)
    except:
        retries += 1
        print(f"Redis connection attempt {retries} of {max_retries}")
        time.sleep(1)
sys.exit(1)
END

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Verify LLM access
echo "Verifying LLM provider access..."
python << END
import sys
import os
import openai
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def check_openai():
    if 'OPENAI_API_KEY' in os.environ:
        openai.api_key = os.environ['OPENAI_API_KEY']
        openai.Model.list()
        print("OpenAI connection verified")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def check_anthropic():
    if 'ANTHROPIC_API_KEY' in os.environ:
        client = anthropic.Client(api_key=os.environ['ANTHROPIC_API_KEY'])
        client.get_available_models()
        print("Anthropic connection verified")

try:
    check_openai()
    check_anthropic()
except Exception as e:
    print(f"Warning: Some LLM providers not available: {e}")
END

# Start the application with uvicorn
echo "Starting service..."
uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8100 \
    --workers 4 \
    --proxy-headers \
    --forwarded-allow-ips '*'