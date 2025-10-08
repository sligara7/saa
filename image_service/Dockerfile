# Build stage
FROM python:3.11-slim as builder

# Install poetry
RUN pip install poetry==1.6.1

# Copy poetry files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Configure poetry to create venv in the project directory
RUN poetry config virtualenvs.in-project true

# Install dependencies
RUN poetry install --no-dev --no-root

# Runtime stage
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

# Install Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 image

# Set up app directory
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY ./src ./src
COPY ./alembic.ini .
COPY ./alembic ./alembic
COPY ./scripts/start.sh ./scripts/start.sh
COPY ./scripts/init_storage.sh ./scripts/init_storage.sh
COPY ./models ./models

# Fix permissions
RUN chown -R image:image /app
RUN chmod +x /app/scripts/start.sh /app/scripts/init_storage.sh

# Switch to non-root user
USER image

# Set Python path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8002/health')"

# Start the service
CMD ["/app/scripts/start.sh"]