-- This concept creates a materialized view for survival of a patient w.r.t ventilation period
-- duration_hours : ventilation duration aggregated over icustay_id
-- hours_before_ventilation : gap in hours from admission time to ventilation start time
-- expired_during_ventilation : true if patient expired during any ventilation, otherwise false
-- Depends On:
--  1. Mimic-III Postgres Database
--  2. `Durations` concepts - ventdurations.
DROP MATERIALIZED VIEW IF EXISTS vent_stats CASCADE;
CREATE MATERIALIZED VIEW vent_stats AS
SELECT
  vd.icustay_id,
  count(vd.icustay_id) as count_ventilations,
  SUM(vd.duration_hours) AS duration_hours, 
  (p.dod_hosp IS NOT NULL AND (p.dod_hosp > MIN(vd.starttime) AND p.dod_hosp <= MAX(vd.endtime))) as expired_during_ventilation,
  ROUND(EXTRACT(EPOCH FROM MIN(vd.starttime) - adm.admittime)/3600) as hours_before_ventilation
FROM
  ventdurations vd
  LEFT JOIN icustays icu ON icu.icustay_id=vd.icustay_id
  LEFT JOIN admissions adm ON adm.hadm_id=icu.hadm_id
  LEFT JOIN patients p ON p.subject_id=icu.subject_id
  GROUP BY vd.icustay_id, adm.admittime, p.dod_hosp;
