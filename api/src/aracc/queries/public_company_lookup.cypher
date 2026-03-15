MATCH (c:Company)
WHERE elementId(c) = $company_id
   OR c.cuit = $company_identifier
   OR c.cuit = $company_identifier_formatted
RETURN c, labels(c) AS entity_labels, elementId(c) AS entity_id
LIMIT 1
