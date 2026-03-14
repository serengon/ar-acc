MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})
CREATE (a:Annotation {
  id: $id,
  entity_id: $entity_id,
  text: $text,
  created_at: datetime()
})
CREATE (i)-[:HAS_ANNOTATION]->(a)
RETURN a.id AS id,
       a.entity_id AS entity_id,
       $investigation_id AS investigation_id,
       a.text AS text,
       a.created_at AS created_at
