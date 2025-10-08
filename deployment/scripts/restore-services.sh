#!/bin/bash
set -e

# Check for backup archive argument
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_archive.tar.gz>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Backup archive not found: $1"
    exit 1
fi

# Extract backup archive
echo "Extracting backup archive..."
BACKUP_DIR=$(basename "$1" .tar.gz)
tar -xzf "$1"

# Helper function to restore a single service database
restore_database() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    local dump_file="$BACKUP_DIR/${service_name}_db.dump"

    if [ ! -f "$dump_file" ]; then
        echo "No database backup found for $service, skipping..."
        return
    fi

    echo "Restoring $service database..."

    # Get database connection details from environment file
    source <(grep "${service_name^^}_DB_" .env | sed 's/^/export /')
    
    # Drop and recreate database
    podman exec ${service_name}-db \
        psql -U ${!service_name^^}_DB_USER -d postgres \
        -c "DROP DATABASE IF EXISTS ${!service_name^^}_DB_NAME;"
    
    podman exec ${service_name}-db \
        psql -U ${!service_name^^}_DB_USER -d postgres \
        -c "CREATE DATABASE ${!service_name^^}_DB_NAME;"
    
    # Restore database from backup
    podman exec -i ${service_name}-db \
        pg_restore -U ${!service_name^^}_DB_USER \
        -d ${!service_name^^}_DB_NAME < "$dump_file"
}

# Helper function to restore MinIO data
restore_minio() {
    local minio_backup="$BACKUP_DIR/minio"
    if [ ! -d "$minio_backup" ]; then
        echo "No MinIO backup found, skipping..."
        return
    fi

    echo "Restoring MinIO data..."
    
    # Get MinIO credentials from environment file
    source <(grep "MINIO_" .env | sed 's/^/export /')
    
    # Use MinIO client to sync data
    podman run --rm \
        --network dnd_network \
        -v $minio_backup:/backup \
        minio/mc \
        mirror /backup minio/image-service
}

# Helper function to restore service configuration
restore_config() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    local config_dir="$BACKUP_DIR/${service_name}_config"

    if [ ! -d "$config_dir" ]; then
        echo "No configuration backup found for $service, skipping..."
        return
    fi

    echo "Restoring $service configuration..."
    if [ -d "$service/config" ]; then
        rm -rf "$service/config"
    fi
    cp -r "$config_dir" "$service/config"
}

# Helper function to restore service migrations
restore_migrations() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    local migrations_dir="$BACKUP_DIR/${service_name}_migrations"

    if [ ! -d "$migrations_dir" ]; then
        echo "No migrations backup found for $service, skipping..."
        return
    fi

    echo "Restoring $service migrations..."
    if [ -d "$service/alembic" ]; then
        rm -rf "$service/alembic"
    fi
    cp -r "$migrations_dir" "$service/alembic"
}

# Stop all services
echo "Stopping services..."
podman-compose down

# Restore data for all services that have backups
services=(
    "message_hub"
    "character_service"
    "campaign_service"
    "image_service"
    "llm_service"
)

for service in "${services[@]}"; do
    if [ -d "$service" ]; then
        restore_database $service
        restore_config $service
        restore_migrations $service
    fi
done

# Restore MinIO data
restore_minio

# Start all services
echo "Starting services..."
podman-compose up -d

# Wait for all services to be healthy
echo "Waiting for services to be healthy..."
for service in "${services[@]}"; do
    service_name=$(echo $service | tr '_' '-')
    echo "Checking $service_name service..."
    timeout 30 bash -c "until curl -s http://localhost:$(grep -A 1 \"$service_name\" docker-compose.yml | grep ports | cut -d':' -f2 | tr -d ' ')/health > /dev/null; do echo \"Service $service_name is unavailable - sleeping\"; sleep 1; done"
done

# Clean up
echo "Cleaning up..."
rm -rf "$BACKUP_DIR"

echo "Restore complete!"