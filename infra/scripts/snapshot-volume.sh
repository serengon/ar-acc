#!/usr/bin/env bash
set -euo pipefail

# Creates a Hetzner Cloud volume snapshot of the Neo4j data volume.
# Requires: hcloud CLI authenticated (hcloud context use <project>)
# Usage: bash infra/scripts/snapshot-volume.sh [volume-name]

VOLUME_NAME="${1:-bracc-neo4j-data}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DESC="bracc-backup-${TIMESTAMP}"

if ! command -v hcloud &> /dev/null; then
    echo "Error: hcloud CLI not installed. Install from https://github.com/hetznercloud/cli"
    exit 1
fi

VOLUME_ID=$(hcloud volume describe "$VOLUME_NAME" -o format='{{.ID}}' 2>/dev/null)
if [ -z "$VOLUME_ID" ]; then
    echo "Error: Volume '$VOLUME_NAME' not found."
    echo "List volumes: hcloud volume list"
    exit 1
fi

echo "Creating snapshot of volume '$VOLUME_NAME' (ID: $VOLUME_ID)..."
hcloud volume create-snapshot "$VOLUME_ID" --description "$SNAPSHOT_DESC"
echo "Snapshot created: $SNAPSHOT_DESC"

# Prune snapshots older than 30 days
echo "Pruning old snapshots..."
CUTOFF=$(date -d '30 days ago' +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -v-30d +%Y-%m-%dT%H:%M:%S)
hcloud volume list-snapshots "$VOLUME_ID" -o columns=id,description,created \
    | tail -n +2 \
    | while read -r snap_id snap_desc snap_created; do
        if [[ "$snap_desc" == bracc-backup-* ]] && [[ "$snap_created" < "$CUTOFF" ]]; then
            echo "Deleting old snapshot $snap_id ($snap_desc)"
            hcloud volume delete-snapshot "$snap_id"
        fi
    done

echo "Done."
