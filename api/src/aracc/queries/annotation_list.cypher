MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})-[:HAS_ANNOTATION]->(a:Annotation)
RETURN a.id AS id,
       a.entity_id AS entity_id,
       $investigation_id AS investigation_id,
       a.text AS text,
       a.created_at AS created_at
ORDER BY a.created_at DESC
