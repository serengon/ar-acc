#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/opt/bracc/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "Backing up Neo4j database..."
docker compose -f /opt/bracc/infra/docker-compose.prod.yml exec -T neo4j \
    neo4j-admin database dump neo4j --to-stdout > "$BACKUP_DIR/neo4j_${TIMESTAMP}.dump"

echo "Pruning backups older than ${RETENTION_DAYS} days..."
find "$BACKUP_DIR" -name "neo4j_*.dump" -mtime "+${RETENTION_DAYS}" -delete

echo "Backup complete: neo4j_${TIMESTAMP}.dump"
