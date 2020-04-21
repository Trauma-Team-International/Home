
-- This query creates the materialized view for final ICU Burden dataset
--   by composing multiple concepts (views) together.
-- Depends On:
--  1. Mimic-III Postgres Database
--  2. Concepts:
--      age-group, 
--      pneumonia, 
--      ventilation-stats, 
--      survival,
--      first-day-labs, 
--      sofa,
--      qsofa,
--       covid-markers
-- 
-- (  
--    last icu stay id, 
--    age, 
--    age_group, 
--    pneumonia influenza source,
--    pneumonia viral source,
--    hospital_survival,
--    month_survival,
--    year_survival,
--    on_ventilator,
--    ventilation_duration_hours,
--    expired_during_ventilation,
--    hours_before_ventilation,
--    diagnosed_ards,
--    labsfirstday concept...
--    sofa concept...
--    qsofa concept...
--    pao2, fio2 concept...
--    total
-- )
DROP MATERIALIZED VIEW IF EXISTS icu_burden CASCADE;
CREATE MATERIALIZED VIEW icu_burden AS
SELECT
  md5(icu.icustay_id::varchar) as id,
  icu.duration_hours as icu_duration_hours,
  -- icu.icustay_id as id,
  -- age_group concept
  ag.age as age_in_years,
  ag.age_group as age_group_range,

  -- pneumonia concept
  CASE
    WHEN pn.pneumonia_influenza_source THEN 1
    ELSE 0
  END
  as pneumonia_influenza_source,
  CASE
    WHEN pn.pneumonia_viral_source THEN 1
    ELSE 0
  END
  as pneumonia_viral_source,

  -- survival concept
  CASE
    WHEN ps.hospital_survival THEN 1
    ELSE 0
  END
  as hospital_survival,
  CASE
    WHEN ps.month_survival THEN 1
    ELSE 0
  END
  as month_survival,
  CASE
    WHEN ps.year_survival THEN 1
    ELSE 0
  END
  as year_survival,

  -- vent_stats concept
  CASE
    WHEN (vs.count_ventilations IS NOT NULL) THEN 1
    ELSE 0
  END
  as on_ventilator,
  vs.duration_hours as ventilation_duration_hours,
  CASE
    WHEN vs.expired_during_ventilation THEN 1
    ELSE 0
  END
  as expired_during_ventilation,
  GREATEST(vs.hours_before_ventilation,0) as hours_before_ventilation,

  -- diag_ards concept
  CASE
    WHEN (coalesce(ards.diagnosed_ards, false) IS true) THEN 1
    ELSE 0
  END
  as diagnosed_ards,

  -- labsfirstday concept
  lfd.aniongap_min,
  lfd.aniongap_max,
  lfd.albumin_min,
  lfd.albumin_max,
  lfd.bands_min,
  lfd.bands_max,
  lfd.bicarbonate_min,
  lfd.bicarbonate_max,
  lfd.bilirubin_min,
  lfd.bilirubin_max,
  lfd.creatinine_min,
  lfd.creatinine_max,
  lfd.chloride_min,
  lfd.chloride_max,
  lfd.glucose_min,
  lfd.glucose_max,
  lfd.hematocrit_min,
  lfd.hematocrit_max,
  lfd.hemoglobin_min,
  lfd.hemoglobin_max,
  lfd.lactate_min,
  lfd.lactate_max,
  lfd.platelet_min,
  lfd.platelet_max,
  lfd.potassium_min,
  lfd.potassium_max,
  lfd.ptt_min,
  lfd.ptt_max,
  lfd.inr_min,
  lfd.inr_max,
  lfd.pt_min,
  lfd.pt_max,
  lfd.sodium_min,
  lfd.sodium_max,
  lfd.bun_min,
  lfd.bun_max,
  lfd.wbc_min,
  lfd.wbc_max,
  
  -- sofa score
  sofa.sofa as sofa_score,
  coalesce(sofa.respiration, 0) as sofa_respiration_score,
  coalesce(sofa.coagulation, 0) as sofa_coagulation_score,
  coalesce(sofa.liver, 0) as sofa_liver_score,
  coalesce(sofa.cardiovascular, 0) as sofa_cardiovascular_score,
  coalesce(sofa.cns, 0) as sofa_cns_score,
  coalesce(sofa.renal, 0) as sofa_renal_score,  

  -- qsofa score
  qsofa.qsofa as qsofa_score,
  qsofa.sysbp_score as qsofa_sysbp_score,
  qsofa.gcs_score as qsofa_gcs_score,
  qsofa.resprate_score as qsofa_resprate_score,

  -- pao2, fio2 values
  pf.min_fio2_set as min_fio2_set,
  pf.max_fio2_set as max_fio2_set,
  pf.min_arterial_pao2 as min_arterial_pao2,
  pf.max_arterial_pao2 as max_arterial_pao2,
  
  -- group by icustay_id count
  1 as total
FROM
  last_icustay icu
  LEFT JOIN vent_stats vs ON icu.icustay_id=vs.icustay_id
  LEFT JOIN age_group ag ON icu.hadm_id=ag.hadm_id
  LEFT JOIN pneumonia pn ON icu.hadm_id=pn.hadm_id
  LEFT JOIN patient_survival ps ON icu.hadm_id=ps.hadm_id
  LEFT JOIN diag_ards ards ON icu.hadm_id=ards.hadm_id
  LEFT JOIN labsfirstday lfd ON icu.icustay_id=lfd.icustay_id
  LEFT JOIN sofa sofa ON icu.icustay_id=sofa.icustay_id
  LEFT JOIN qsofa qsofa ON icu.icustay_id=qsofa.icustay_id
  LEFT JOIN pao2_fio2 pf ON icu.icustay_id=pf.icustay_id
WHERE
  (pn.pneumonia_influenza_source IS NOT NULL
  OR
  pn.pneumonia_viral_source IS NOT NULL)
  AND
  ag.age > 14
  AND
  ag.age < 100
ORDER BY
  ag.age;
  

