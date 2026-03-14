MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})
CREATE (t:Tag {
  id: $id,
  name: $name,
  color: $color
})
CREATE (i)-[:HAS_TAG]->(t)
RETURN t.id AS id,
       $investigation_id AS investigation_id,
       t.name AS name,
       t.color AS color
