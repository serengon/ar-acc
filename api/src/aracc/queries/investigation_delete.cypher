MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $id})
OPTIONAL MATCH (i)-[:HAS_TAG]->(t:Tag)
OPTIONAL MATCH (i)-[:HAS_ANNOTATION]->(a:Annotation)
DETACH DELETE i, t, a
RETURN 1 AS deleted
