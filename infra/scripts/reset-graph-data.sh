#!/usr/bin/env bash
# Reset graph data while preserving User, Investigation, Annotation, and Tag nodes.
# Usage: bash infra/scripts/reset-graph-data.sh [neo4j-password]

set -euo pipefail

PASSWORD="${1:-${NEO4J_PASSWORD:-changeme}}"
URI="${NEO4J_URI:-bolt://localhost:9687}"

echo "Deleting all graph data EXCEPT User/Investigation/Annotation/Tag nodes..."

docker exec aracc-neo4j cypher-shell -u neo4j -p "$PASSWORD" \
  "MATCH (n) WHERE NOT n:User AND NOT n:Investigation AND NOT n:Annotation AND NOT n:Tag DETACH DELETE n"

echo "Done. User accounts preserved."
