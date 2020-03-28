-- This query creates a materialized view for survival of a patient w.r.t admission time
--  Depends On: Mimic-III Postgres Database
DROP MATERIALIZED VIEW IF EXISTS patient_survival CASCADE;
CREATE MATERIALIZED VIEW patient_survival AS
SELECT
  adm.hadm_id,
  (adm.hospital_expire_flag = 0) as hospital_survival,
  ((p.dod IS NULL) OR (extract(DAY FROM p.dod - adm.dischtime) > 30)) as month_survival,
  ((p.dod IS NULL) OR (extract(DAY FROM p.dod - adm.dischtime) > 365)) as year_survival
FROM
  admissions adm
  INNER JOIN patients p ON p.subject_id=adm.subject_id;