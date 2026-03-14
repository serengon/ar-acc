MATCH (e) WHERE (e.cpf = $id OR e.cnpj = $id
            OR e.contract_id = $id OR e.sanction_id = $id
            OR e.amendment_id = $id OR e.cnes_code = $id
            OR e.finance_id = $id OR e.embargo_id = $id
            OR e.school_id = $id OR e.convenio_id = $id
            OR e.partner_id = $id
            OR e.stats_id = $id OR elementId(e) = $id)
  AND (e:Person OR e:Partner OR e:Company OR e:Contract OR e:Sanction OR e:Election
       OR e:Amendment OR e:Finance OR e:Embargo OR e:Health OR e:Education
       OR e:Convenio OR e:LaborStats OR e:PublicOffice)
RETURN e, labels(e) AS entity_labels
LIMIT 1
