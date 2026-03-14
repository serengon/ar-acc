MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})-[:HAS_TAG]->(t:Tag)
RETURN t.id AS id,
       $investigation_id AS investigation_id,
       t.name AS name,
       t.color AS color
ORDER BY t.name
