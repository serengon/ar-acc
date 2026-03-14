MATCH (e)
WHERE (e:Person AND (e.cpf = $identifier OR e.cpf = $identifier_formatted))
   OR (e:Company AND (e.cnpj = $identifier OR e.cnpj = $identifier_formatted))
RETURN e, labels(e) AS entity_labels, elementId(e) AS entity_id
LIMIT 1
