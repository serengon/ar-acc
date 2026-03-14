// Baseline: peer comparison by CNAE sector
// Compares a company's contract metrics against sector average
MATCH (co:Company)-[:VENCEU]->(c:Contract)
WHERE co.cnae_principal IS NOT NULL
  AND ($entity_id IS NULL OR elementId(co) = $entity_id)
WITH co, COUNT(c) AS contract_count, SUM(c.value) AS total_value, co.cnae_principal AS cnae
WITH cnae, co, contract_count, total_value

// Sector-wide stats
MATCH (peer:Company)-[:VENCEU]->(pc:Contract)
WHERE peer.cnae_principal = cnae
WITH cnae, co, contract_count, total_value,
     COUNT(DISTINCT peer) AS sector_companies,
     COUNT(pc) AS sector_contracts,
     SUM(pc.value) AS sector_total_value
WITH cnae, co, contract_count, total_value,
     sector_companies,
     toFloat(sector_contracts) / CASE WHEN sector_companies > 0
       THEN toFloat(sector_companies) ELSE 1.0 END AS avg_contracts,
     toFloat(sector_total_value) / CASE WHEN sector_companies > 0
       THEN toFloat(sector_companies) ELSE 1.0 END AS avg_value
RETURN co.razao_social AS company_name,
       co.cnpj AS company_cnpj,
       elementId(co) AS company_id,
       cnae AS sector_cnae,
       contract_count,
       total_value,
       sector_companies,
       avg_contracts AS sector_avg_contracts,
       avg_value AS sector_avg_value,
       toFloat(contract_count) / CASE WHEN avg_contracts > 0
         THEN avg_contracts ELSE 1.0 END AS contract_ratio,
       toFloat(total_value) / CASE WHEN avg_value > 0
         THEN avg_value ELSE 1.0 END AS value_ratio
ORDER BY value_ratio DESC
LIMIT 50
