-- This Query creates a table categorizing pneumonia related 
--   ICD_9 codes into Influenza and Viral Influenza sources.
-- Pre-requisites: Mimic-III Postgres Database.
DROP TABLE IF EXISTS pneumonia_source;
CREATE Table pneumonia_source(
influenza integer not null,
viral integer not null, 
icd9_code varchar(10) references d_icd_diagnoses(icd9_code) not null
);

INSERT INTO pneumonia_source
(influenza, viral, icd9_code)
values
( 0, 1, '4800'),
( 0, 1, '4801'),
( 1, 1, '4802'),
( 1, 1, '4803'),
( 1, 1, '4808'),
( 1, 1, '4822'),
( 0, 1, '4841'),
( 1, 1, '4870'),
( 1, 1, '4809'),
( 1, 1, '48801'),
( 1, 1, '48811'),
( 1, 1, '48881'),
( 0, 0, '01166'),
( 0, 0, '00322'),
( 0, 0, '01160'),
( 0, 0, '01161'),
( 0, 0, '01162'),
( 0, 0, '01163'),
( 0, 0, '01164'),
( 0, 0, '01165'),
( 0, 0, '0382'),
( 0, 0, '11505'),
( 0, 0, '11515'),
( 0, 0, '11595'),
( 0, 0, '0730'),
( 0, 0, '48249'),
( 0, 0, '48281'),
( 0, 0, '48282'),
( 0, 0, '48283'),
( 0, 0, '481'),
( 0, 0, '4820'),
( 0, 0, '4821'),
( 0, 0, '48230'),
( 0, 0, '48231'),
( 0, 0, '48232'),
( 0, 0, '48239'),
( 0, 0, '48240'),
( 0, 0, '48241'),
( 0, 0, '48242'),
( 0, 0, '48284'),
( 0, 0, '48289'),
( 0, 0, '4829'),
( 0, 0, '4830'),
( 0, 0, '4831'),
( 0, 0, '4838'),
( 0, 0, '4843'),
( 0, 0, '4845'),
( 0, 0, '4846'),
( 0, 0, '4847'),
( 0, 0, '4848'),
( 0, 0, '485'),
( 0, 0, '486'),
( 0, 0, '51630'),
( 0, 0, '51635'),
( 0, 0, '51636'),
( 0, 0, '5171'),
( 0, 0, '7700'),
( 0, 0, '99731'),
( 0, 0, '99732'),
( 0, 0, '51637');



-- This query creates a materialized view for all admissions diagnosed with pneumonia.
-- Depends On:
--  1. Mimic-III Postgres Database
--  2. Table: pneumonia_source
DROP MATERIALIZED VIEW IF EXISTS pneumonia CASCADE;
CREATE MATERIALIZED VIEW pneumonia AS
SELECT
  adm.hadm_id,
  MAX(ps.influenza) = 1 as pneumonia_influenza_source,
  MAX(ps.viral) = 1 as pneumonia_viral_source
FROM
  admissions adm
  INNER JOIN diagnoses_icd diag ON diag.hadm_id=adm.hadm_id
  INNER JOIN pneumonia_source ps ON ps.icd9_code=diag.icd9_code
  GROUP BY adm.hadm_id;


-- ARDS
DROP MATERIALIZED VIEW IF EXISTS diag_ards CASCADE;
CREATE MATERIALIZED VIEW diag_ards AS
SELECT
  adm.hadm_id,
  (diag.icd9_code = '51882') AS diagnosed_ards
FROM
  admissions adm
  INNER JOIN diagnoses_icd diag ON diag.hadm_id=adm.hadm_id
  GROUP BY  adm.hadm_id, diag.icd9_code
  HAVING diag.icd9_code = '51882';



