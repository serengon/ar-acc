MATCH (c:Company)
WHERE elementId(c) = $company_id
   OR c.cnpj = $company_identifier
   OR c.cnpj = $company_identifier_formatted
RETURN c, labels(c) AS entity_labels, elementId(c) AS entity_id
LIMIT 1
