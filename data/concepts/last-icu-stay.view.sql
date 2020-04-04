-- This Query generates materialized view for last icu stay of a patient over all admissions.
-- Depends On: Mimic-III Postgres Database

-- Last icu stay for a subject.
  DROP MATERIALIZED VIEW IF EXISTS last_icustay CASCADE;
  CREATE MATERIALIZED VIEW last_icustay AS
  SELECT
    icu.hadm_id,
    icu.icustay_id,
    icu.intime,
    ROUND(EXTRACT(EPOCH FROM icu.outtime - icu.intime)/3600) as duration_hours
  FROM
    icustays icu
    INNER JOIN (
      SELECT
        subject_id,
        MAX(intime) as maxInTime
      FROM
        icustays
      GROUP BY subject_id
    ) groupedIcuStay
    ON icu.subject_id = groupedIcuStay.subject_id
    AND
    icu.intime = groupedIcuStay.maxInTime;
