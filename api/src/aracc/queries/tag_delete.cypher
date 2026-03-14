MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})
MATCH (i)-[:HAS_TAG]->(t:Tag {id: $tag_id})
DETACH DELETE t
RETURN 1 AS deleted
