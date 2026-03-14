// Baseline: peer comparison by municipality/region
// Compares a company's contract metrics against regional peers
MATCH (co:Company)-[:VENCEU]->(c:Contract)
WHERE c.contracting_org IS NOT NULL
  AND ($entity_id IS NULL OR elementId(co) = $entity_id)
WITH co, c.contracting_org AS region,
     COUNT(c) AS contract_count, SUM(c.value) AS total_value

// Regional stats
MATCH (peer:Company)-[:VENCEU]->(pc:Contract)
WHERE pc.contracting_org = region
WITH region, co, contract_count, total_value,
     COUNT(DISTINCT peer) AS region_companies,
     COUNT(pc) AS region_contracts,
     SUM(pc.value) AS region_total_value
WITH region, co, contract_count, total_value,
     region_companies,
     toFloat(region_contracts) / CASE WHEN region_companies > 0
       THEN toFloat(region_companies) ELSE 1.0 END AS avg_contracts,
     toFloat(region_total_value) / CASE WHEN region_companies > 0
       THEN toFloat(region_companies) ELSE 1.0 END AS avg_value
RETURN co.razao_social AS company_name,
       co.cnpj AS company_cnpj,
       elementId(co) AS company_id,
       region,
       contract_count,
       total_value,
       region_companies,
       avg_contracts AS region_avg_contracts,
       avg_value AS region_avg_value,
       toFloat(contract_count) / CASE WHEN avg_contracts > 0
         THEN avg_contracts ELSE 1.0 END AS contract_ratio,
       toFloat(total_value) / CASE WHEN avg_value > 0
         THEN avg_value ELSE 1.0 END AS value_ratio
ORDER BY value_ratio DESC
LIMIT 50
