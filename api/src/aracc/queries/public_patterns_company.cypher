MATCH (c:Company)
WHERE elementId(c) = $company_id
   OR c.cnpj = $company_identifier
   OR c.cnpj = $company_identifier_formatted
OPTIONAL MATCH (c)-[:VENCEU]->(contract)
WITH c, count(DISTINCT contract) AS contract_count
OPTIONAL MATCH (c)-[:SANCIONADA]->(sanction)
WITH c, contract_count, count(DISTINCT sanction) AS sanction_count
OPTIONAL MATCH (c)-[:DEVE]->(debt)
WITH c, contract_count, sanction_count, count(DISTINCT debt) AS debt_count
OPTIONAL MATCH (c)-[:RECEBEU_EMPRESTIMO]->(loan)
WITH c, contract_count, sanction_count, debt_count, count(DISTINCT loan) AS loan_count
OPTIONAL MATCH (c)-[:BENEFICIOU]->(amendment:Amendment)
WITH c, contract_count, sanction_count, debt_count, loan_count, count(DISTINCT amendment) AS amendment_count
WITH c, contract_count, sanction_count, debt_count, loan_count, amendment_count, [
  {
    pattern_id: 'sanctioned_still_receiving',
    trigger: sanction_count > 0 AND contract_count > 0,
    summary_pt: 'Empresa sancionada com contratos públicos',
    summary_en: 'Sanctioned company with public contracts',
    risk_signal: sanction_count + contract_count
  },
  {
    pattern_id: 'debtor_contracts',
    trigger: debt_count > 0 AND contract_count > 0,
    summary_pt: 'Empresa devedora com contratos públicos',
    summary_en: 'Debtor company with public contracts',
    risk_signal: debt_count + contract_count
  },
  {
    pattern_id: 'loan_debtor',
    trigger: debt_count > 0 AND loan_count > 0,
    summary_pt: 'Empresa devedora com empréstimo público',
    summary_en: 'Debtor company with public loan',
    risk_signal: debt_count + loan_count
  },
  {
    pattern_id: 'amendment_beneficiary_contracts',
    trigger: amendment_count > 0 AND contract_count > 0,
    summary_pt: 'Beneficiária de emenda com contratos',
    summary_en: 'Amendment beneficiary with contracts',
    risk_signal: amendment_count + contract_count
  }
] AS patterns
UNWIND patterns AS p
WITH c, p, contract_count, sanction_count, debt_count, loan_count, amendment_count
WHERE p.trigger
RETURN p.pattern_id AS pattern_id,
       c.cnpj AS cnpj,
       c.razao_social AS company_name,
       contract_count,
       sanction_count,
       debt_count,
       loan_count,
       amendment_count,
       p.summary_pt AS summary_pt,
       p.summary_en AS summary_en,
       p.risk_signal AS risk_signal
ORDER BY risk_signal DESC
