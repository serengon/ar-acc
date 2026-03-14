MATCH (u:User {id: $user_id})-[:OWNS]->(i:Investigation {id: $investigation_id})
MATCH (i)-[r:INCLUDES]->(e)
WHERE (e.cpf = $entity_id OR e.cnpj = $entity_id
   OR e.contract_id = $entity_id OR e.sanction_id = $entity_id
   OR e.amendment_id = $entity_id OR e.cnes_code = $entity_id
   OR e.finance_id = $entity_id OR e.embargo_id = $entity_id
   OR e.school_id = $entity_id OR e.convenio_id = $entity_id
   OR e.partner_id = $entity_id
   OR e.stats_id = $entity_id OR elementId(e) = $entity_id)
  AND (e:Person OR e:Partner OR e:Company OR e:Contract OR e:Sanction OR e:Election
       OR e:Amendment OR e:Finance OR e:Embargo OR e:Health OR e:Education
       OR e:Convenio OR e:LaborStats OR e:PublicOffice)
DELETE r
RETURN 1 AS deleted
