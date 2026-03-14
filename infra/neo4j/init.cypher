// AR-ACC Neo4j Schema — Constraints and Indexes
// Applied on database initialization

// ── Uniqueness Constraints ──────────────────────────────
CREATE CONSTRAINT person_cuil_unique IF NOT EXISTS
  FOR (p:Person) REQUIRE p.cuil IS UNIQUE;

CREATE CONSTRAINT partner_id_unique IF NOT EXISTS
  FOR (p:Partner) REQUIRE p.partner_id IS UNIQUE;

CREATE CONSTRAINT company_cuit_unique IF NOT EXISTS
  FOR (c:Company) REQUIRE c.cuit IS UNIQUE;

CREATE CONSTRAINT contract_contract_id_unique IF NOT EXISTS
  FOR (c:Contract) REQUIRE c.contract_id IS UNIQUE;

CREATE CONSTRAINT sanction_sanction_id_unique IF NOT EXISTS
  FOR (s:Sanction) REQUIRE s.sanction_id IS UNIQUE;

CREATE CONSTRAINT public_office_id_unique IF NOT EXISTS
  FOR (po:PublicOffice) REQUIRE po.office_id IS UNIQUE;

CREATE CONSTRAINT investigation_id_unique IF NOT EXISTS
  FOR (i:Investigation) REQUIRE i.id IS UNIQUE;

CREATE CONSTRAINT health_establishment_id_unique IF NOT EXISTS
  FOR (h:Health) REQUIRE h.establishment_id IS UNIQUE;

CREATE CONSTRAINT finance_id_unique IF NOT EXISTS
  FOR (f:Finance) REQUIRE f.finance_id IS UNIQUE;

CREATE CONSTRAINT education_school_id_unique IF NOT EXISTS
  FOR (e:Education) REQUIRE e.school_id IS UNIQUE;

CREATE CONSTRAINT offshore_entity_id_unique IF NOT EXISTS
  FOR (o:OffshoreEntity) REQUIRE o.offshore_id IS UNIQUE;

CREATE CONSTRAINT offshore_officer_id_unique IF NOT EXISTS
  FOR (o:OffshoreOfficer) REQUIRE o.offshore_officer_id IS UNIQUE;

CREATE CONSTRAINT global_pep_id_unique IF NOT EXISTS
  FOR (g:GlobalPEP) REQUIRE g.pep_id IS UNIQUE;

CREATE CONSTRAINT cnv_proceeding_id_unique IF NOT EXISTS
  FOR (c:CNVProceeding) REQUIRE c.proceeding_id IS UNIQUE;

CREATE CONSTRAINT expense_id_unique IF NOT EXISTS
  FOR (e:Expense) REQUIRE e.expense_id IS UNIQUE;

CREATE CONSTRAINT pep_record_id_unique IF NOT EXISTS
  FOR (p:PEPRecord) REQUIRE p.pep_id IS UNIQUE;

CREATE CONSTRAINT legal_case_id_unique IF NOT EXISTS
  FOR (l:LegalCase) REQUIRE l.case_id IS UNIQUE;

CREATE CONSTRAINT international_sanction_id_unique IF NOT EXISTS
  FOR (s:InternationalSanction) REQUIRE s.sanction_id IS UNIQUE;

CREATE CONSTRAINT declared_asset_id_unique IF NOT EXISTS
  FOR (d:DeclaredAsset) REQUIRE d.asset_id IS UNIQUE;

CREATE CONSTRAINT bid_id_unique IF NOT EXISTS
  FOR (b:Bid) REQUIRE b.bid_id IS UNIQUE;

CREATE CONSTRAINT boletin_act_id_unique IF NOT EXISTS
  FOR (d:BoletinAct) REQUIRE d.act_id IS UNIQUE;

CREATE CONSTRAINT party_membership_id_unique IF NOT EXISTS
  FOR (pm:PartyMembership) REQUIRE pm.membership_id IS UNIQUE;

CREATE CONSTRAINT judicial_case_id_unique IF NOT EXISTS
  FOR (j:JudicialCase) REQUIRE j.judicial_case_id IS UNIQUE;

CREATE CONSTRAINT source_document_id_unique IF NOT EXISTS
  FOR (s:SourceDocument) REQUIRE s.doc_id IS UNIQUE;

CREATE CONSTRAINT ingestion_run_id_unique IF NOT EXISTS
  FOR (r:IngestionRun) REQUIRE r.run_id IS UNIQUE;

CREATE CONSTRAINT user_email_unique IF NOT EXISTS
  FOR (u:User) REQUIRE u.email IS UNIQUE;

// ── Indexes ─────────────────────────────────────────────
CREATE INDEX person_name IF NOT EXISTS
  FOR (p:Person) ON (p.name);

CREATE INDEX person_dni IF NOT EXISTS
  FOR (p:Person) ON (p.dni);

CREATE INDEX person_name_provincia IF NOT EXISTS
  FOR (p:Person) ON (p.name, p.provincia);

CREATE INDEX partner_name IF NOT EXISTS
  FOR (p:Partner) ON (p.name);

CREATE INDEX company_razon_social IF NOT EXISTS
  FOR (c:Company) ON (c.razon_social);

CREATE INDEX contract_value IF NOT EXISTS
  FOR (c:Contract) ON (c.value);

CREATE INDEX sanction_type IF NOT EXISTS
  FOR (s:Sanction) ON (s.type);

CREATE INDEX election_year IF NOT EXISTS
  FOR (e:Election) ON (e.year);

CREATE INDEX company_actividad_principal IF NOT EXISTS
  FOR (c:Company) ON (c.actividad_principal);

CREATE INDEX contract_organismo IF NOT EXISTS
  FOR (c:Contract) ON (c.organismo);

CREATE INDEX sanction_date_start IF NOT EXISTS
  FOR (s:Sanction) ON (s.date_start);

CREATE INDEX finance_type IF NOT EXISTS
  FOR (f:Finance) ON (f.type);

CREATE INDEX health_name IF NOT EXISTS
  FOR (h:Health) ON (h.name);

CREATE INDEX health_provincia IF NOT EXISTS
  FOR (h:Health) ON (h.provincia);

CREATE INDEX education_name IF NOT EXISTS
  FOR (e:Education) ON (e.name);

CREATE INDEX offshore_entity_name IF NOT EXISTS
  FOR (o:OffshoreEntity) ON (o.name);

CREATE INDEX global_pep_name IF NOT EXISTS
  FOR (g:GlobalPEP) ON (g.name);

CREATE INDEX global_pep_country IF NOT EXISTS
  FOR (g:GlobalPEP) ON (g.country);

CREATE INDEX expense_date IF NOT EXISTS
  FOR (e:Expense) ON (e.date);

CREATE INDEX public_office_org IF NOT EXISTS
  FOR (po:PublicOffice) ON (po.org);

CREATE INDEX pep_record_name IF NOT EXISTS
  FOR (p:PEPRecord) ON (p.name);

CREATE INDEX international_sanction_source IF NOT EXISTS
  FOR (s:InternationalSanction) ON (s.source);

CREATE INDEX boletin_act_date IF NOT EXISTS
  FOR (d:BoletinAct) ON (d.date);

CREATE INDEX judicial_case_number IF NOT EXISTS
  FOR (j:JudicialCase) ON (j.case_number);

CREATE INDEX ingestion_run_source_id IF NOT EXISTS
  FOR (r:IngestionRun) ON (r.source_id);

CREATE INDEX ingestion_run_status IF NOT EXISTS
  FOR (r:IngestionRun) ON (r.status);

// ── Fulltext Search Index ───────────────────────────────
CREATE FULLTEXT INDEX entity_search IF NOT EXISTS
  FOR (n:Person|Partner|Company|Health|Education|Contract|PublicOffice|OffshoreEntity|OffshoreOfficer|GlobalPEP|CNVProceeding|Expense|PEPRecord|LegalCase|DeclaredAsset|InternationalSanction|Bid|BoletinAct|PartyMembership|JudicialCase|SourceDocument)
  ON EACH [n.name, n.razon_social, n.cuil, n.cuit, n.dni, n.object, n.organismo, n.org, n.jurisdiction, n.description, n.case_number];
