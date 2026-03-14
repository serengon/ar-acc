// Sample peer entities for percentile computation (capped at 500 for performance)
// For companies: peers share the same cnae_principal
// For persons: peers share the same primary label
MATCH (peer)
WHERE ($peer_label IS NULL OR $peer_label IN labels(peer))
  AND ($cnae IS NULL OR peer.cnae_principal = $cnae)
  AND elementId(peer) <> $entity_id
WITH peer LIMIT 500
OPTIONAL MATCH (peer)-[r]-(connected)
WITH peer, count(r) AS conn_count
OPTIONAL MATCH (peer)-[:VENCEU]->(c:Contract)
WITH peer, conn_count, COALESCE(sum(c.value), 0) AS contract_vol
OPTIONAL MATCH (peer)-[:RECEBEU_EMPRESTIMO|DEVE]->(f:Finance)
WITH peer, conn_count, contract_vol + COALESCE(sum(f.value), 0) AS fin_vol
RETURN
  count(peer) AS peer_count,
  collect(conn_count) AS connection_counts,
  collect(fin_vol) AS financial_volumes
