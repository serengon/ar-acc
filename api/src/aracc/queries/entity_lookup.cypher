MATCH (e)
WHERE (e:Person AND (e.cuil = $identifier OR e.cuil = $identifier_formatted))
   OR (e:Company AND (e.cuit = $identifier OR e.cuit = $identifier_formatted))
RETURN e, labels(e) AS entity_labels, elementId(e) AS entity_id
LIMIT 1
