#!/usr/bin/env bash
set -euo pipefail

# Installs daily Neo4j backup cron job.
# Usage: sudo bash infra/scripts/backup-cron.sh

DEPLOY_DIR="${DEPLOY_DIR:-/opt/bracc}"
CRON_ENTRY="0 3 * * * ${DEPLOY_DIR}/infra/scripts/backup-neo4j.sh >> /var/log/bracc-backup.log 2>&1"

if crontab -l 2>/dev/null | grep -qF "backup-neo4j.sh"; then
    echo "Backup cron already installed."
    exit 0
fi

(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
echo "Installed daily backup cron (03:00 UTC)."
echo "Logs: /var/log/bracc-backup.log"
