MATCH (t:Tag {id: $tag_id})
MATCH (e) WHERE (e:Person OR e:Company OR e:Contract OR e:Sanction)
  AND elementId(e) = $entity_id
MERGE (t)-[:APPLIED_TO]->(e)
RETURN t.id AS tag_id, elementId(e) AS entity_id
