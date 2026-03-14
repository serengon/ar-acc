MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})
MATCH (i)-[:HAS_ANNOTATION]->(a:Annotation {id: $annotation_id})
DETACH DELETE a
RETURN 1 AS deleted
