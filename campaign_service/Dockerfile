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
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 campaign

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Set up app directory
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY ./src ./src
COPY ./alembic.ini .
COPY ./alembic ./alembic
COPY ./scripts/start.sh ./scripts/start.sh

# Fix permissions
RUN chown -R campaign:campaign /app
RUN chmod +x /app/scripts/start.sh

# Switch to non-root user
USER campaign

# Set Python path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the service
CMD ["/app/scripts/start.sh"]