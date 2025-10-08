#!/bin/bash
set -e

# Create backup directory
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Helper function to backup a single service database
backup_database() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    echo "Backing up $service database..."

    # Get database connection details from environment file
    source <(grep "${service_name^^}_DB_" .env | sed 's/^/export /')
    
    # Perform database backup
    podman exec ${service_name}-db \
        pg_dump -Fc \
            -U ${!service_name^^}_DB_USER \
            ${!service_name^^}_DB_NAME \
            > "$BACKUP_DIR/${service_name}_db.dump"
}

# Helper function to backup MinIO data
backup_minio() {
    echo "Backing up MinIO data..."
    
    # Get MinIO credentials from environment file
    source <(grep "MINIO_" .env | sed 's/^/export /')
    
    # Use MinIO client to sync data
    podman run --rm \
        --network dnd_network \
        -v $BACKUP_DIR/minio:/backup \
        minio/mc \
        mirror minio/image-service /backup
}

# Helper function to backup service configuration
backup_config() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    echo "Backing up $service configuration..."

    # Backup configuration files
    if [ -d "$service/config" ]; then
        cp -r "$service/config" "$BACKUP_DIR/${service_name}_config"
    fi
}

# Helper function to backup service migrations
backup_migrations() {
    local service=$1
    local service_name=$(echo $service | tr '_' '-')
    echo "Backing up $service migrations..."

    # Backup Alembic migrations
    if [ -d "$service/alembic" ]; then
        cp -r "$service/alembic" "$BACKUP_DIR/${service_name}_migrations"
    fi
}

# Backup databases for all services that have them
services=(
    "message_hub"
    "character_service"
    "campaign_service"
    "image_service"
    "llm_service"
)

for service in "${services[@]}"; do
    if [ -d "$service" ]; then
        backup_database $service
        backup_config $service
        backup_migrations $service
    fi
done

# Backup MinIO data
backup_minio

# Create archive of backup directory
echo "Creating backup archive..."
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup complete! Archive created at $BACKUP_DIR.tar.gz"