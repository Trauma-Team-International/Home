 -- This query pivots covid related lab values taken in the first 24 hours of a patient's stay

-- Have already confirmed that the unit of measurement is always the same: null or the correct unit
DROP MATERIALIZED VIEW IF EXISTS firstdaycovidmarkers CASCADE;
CREATE materialized VIEW firstdaycovidmarkers AS
SELECT
  pvt.subject_id, pvt.hadm_id, pvt.icustay_id
, min(CASE WHEN label = 'CARBOXYHEMOGLOBIN' THEN valuenum ELSE null end) as CARBOXYHEMOGLOBIN_min
, max(CASE WHEN label = 'CARBOXYHEMOGLOBIN' THEN valuenum ELSE null end) as CARBOXYHEMOGLOBIN_max
, min(CASE WHEN label = 'METHEMOGLOBIN' THEN valuenum ELSE null end) as METHEMOGLOBIN_min
, max(CASE WHEN label = 'METHEMOGLOBIN' THEN valuenum ELSE null end) as METHEMOGLOBIN_max
, min(CASE WHEN label = 'PERCENTAGE_HEMOGLOBIN_A1C' THEN valuenum ELSE null end) as PERCENTAGE_HEMOGLOBIN_A1C_min
, max(CASE WHEN label = 'PERCENTAGE_HEMOGLOBIN_A1C' THEN valuenum ELSE null end) as PERCENTAGE_HEMOGLOBIN_A1C_max
, min(CASE WHEN label = 'ABSOLUTE_HEMOGLOBIN' THEN valuenum ELSE null end) as ABSOLUTE_HEMOGLOBIN_min
, max(CASE WHEN label = 'ABSOLUTE_HEMOGLOBIN' THEN valuenum ELSE null end) as ABSOLUTE_HEMOGLOBIN_max
, min(CASE WHEN label = 'ALANINE_AMINOTRANSFERASE' THEN valuenum ELSE null end) as ALANINE_AMINOTRANSFERASE_min
, max(CASE WHEN label = 'ALANINE_AMINOTRANSFERASE' THEN valuenum ELSE null end) as ALANINE_AMINOTRANSFERASE_max
, min(CASE WHEN label = 'ASPARATE_AMINOTRANSFERASE' THEN valuenum ELSE null end) as ASPARATE_AMINOTRANSFERASE_min
, max(CASE WHEN label = 'ASPARATE_AMINOTRANSFERASE' THEN valuenum ELSE null end) as ASPARATE_AMINOTRANSFERASE_max
, min(CASE WHEN label = 'C_REACTIVE_PROTEIN' THEN valuenum ELSE null end) as C_REACTIVE_PROTEIN_min
, max(CASE WHEN label = 'C_REACTIVE_PROTEIN' THEN valuenum ELSE null end) as C_REACTIVE_PROTEIN_max
, min(CASE WHEN label = 'D_DIMER' THEN valuenum ELSE null end) as D_DIMER_min
, max(CASE WHEN label = 'D_DIMER' THEN valuenum ELSE null end) as D_DIMER_max
, min(CASE WHEN label = 'ABSOLUTE_LYMPHOCYTE' THEN valuenum ELSE null end) as ABSOLUTE_LYMPHOCYTE_min
, max(CASE WHEN label = 'ABSOLUTE_LYMPHOCYTE' THEN valuenum ELSE null end) as ABSOLUTE_LYMPHOCYTE_max
, min(CASE WHEN label = 'ATYPICAL_LYMPHOCYTES' THEN valuenum ELSE null end) as ATYPICAL_LYMPHOCYTES_min
, max(CASE WHEN label = 'ATYPICAL_LYMPHOCYTES' THEN valuenum ELSE null end) as ATYPICAL_LYMPHOCYTES_max
, min(CASE WHEN label = 'FETAL_HEMOGLOBIN' THEN valuenum ELSE null end) as FETAL_HEMOGLOBIN_min
, max(CASE WHEN label = 'FETAL_HEMOGLOBIN' THEN valuenum ELSE null end) as FETAL_HEMOGLOBIN_max
, min(CASE WHEN label = 'FIBRINOGEN' THEN valuenum ELSE null end) as FIBRINOGEN_min
, max(CASE WHEN label = 'FIBRINOGEN' THEN valuenum ELSE null end) as FIBRINOGEN_max
, min(CASE WHEN label = 'HEMOGLOBIN_A2' THEN valuenum ELSE null end) as HEMOGLOBIN_A2_min
, max(CASE WHEN label = 'HEMOGLOBIN_A2' THEN valuenum ELSE null end) as HEMOGLOBIN_A2_max
, min(CASE WHEN label = 'HEMOGLOBIN_C' THEN valuenum ELSE null end) as HEMOGLOBIN_C_min
, max(CASE WHEN label = 'HEMOGLOBIN_C' THEN valuenum ELSE null end) as HEMOGLOBIN_C_max
, min(CASE WHEN label = 'HEMOGLOBIN_F' THEN valuenum ELSE null end) as HEMOGLOBIN_F_min
, max(CASE WHEN label = 'HEMOGLOBIN_F' THEN valuenum ELSE null end) as HEMOGLOBIN_F_max
, min(CASE WHEN label = 'LARGE_PLATELETS' THEN valuenum ELSE null end) as LARGE_PLATELETS_min
, max(CASE WHEN label = 'LARGE_PLATELETS' THEN valuenum ELSE null end) as LARGE_PLATELETS_max
, min(CASE WHEN label = 'LEUKOCYTE_ALKALINE_PHOSPHATASE' THEN valuenum ELSE null end) as LEUKOCYTE_ALKALINE_PHOSPHATASE_min
, max(CASE WHEN label = 'LEUKOCYTE_ALKALINE_PHOSPHATASE' THEN valuenum ELSE null end) as LEUKOCYTE_ALKALINE_PHOSPHATASE_max
, min(CASE WHEN label = 'LYMPHOCYTES' THEN valuenum ELSE null end) as LYMPHOCYTES_min
, max(CASE WHEN label = 'LYMPHOCYTES' THEN valuenum ELSE null end) as LYMPHOCYTES_max
, min(CASE WHEN label = 'LYMPHOCYTES_PERCENT' THEN valuenum ELSE null end) as LYMPHOCYTES_PERCENT_min
, max(CASE WHEN label = 'LYMPHOCYTES_PERCENT' THEN valuenum ELSE null end) as LYMPHOCYTES_PERCENT_max
, min(CASE WHEN label = 'PLATELET_CLUMPS' THEN valuenum ELSE null end) as PLATELET_CLUMPS_min
, max(CASE WHEN label = 'PLATELET_CLUMPS' THEN valuenum ELSE null end) as PLATELET_CLUMPS_max
, min(CASE WHEN label = 'PLATELET_SMEAR' THEN valuenum ELSE null end) as PLATELET_SMEAR_min
, max(CASE WHEN label = 'PLATELET_SMEAR' THEN valuenum ELSE null end) as PLATELET_SMEAR_max
, min(CASE WHEN label = 'RETICULOCYTE' THEN valuenum ELSE null end) as RETICULOCYTE_min
, max(CASE WHEN label = 'RETICULOCYTE' THEN valuenum ELSE null end) as RETICULOCYTE_max

FROM
( -- begin query that extracts the data
  SELECT ie.subject_id, ie.hadm_id, ie.icustay_id
  -- here we assign labels to ITEMIDs
  -- this also fuses together multiple ITEMIDs containing the same data
  , CASE
        WHEN itemid = 50805 THEN 'CARBOXYHEMOGLOBIN'
        WHEN itemid = 50814 THEN 'METHEMOGLOBIN'
        WHEN itemid = 50852 THEN 'PERCENTAGE_HEMOGLOBIN_A1C'
        WHEN itemid = 50855 THEN 'ABSOLUTE_HEMOGLOBIN'
        WHEN itemid = 50861 THEN 'ALANINE_AMINOTRANSFERASE'
        WHEN itemid = 50878 THEN 'ASPARATE_AMINOTRANSFERASE'
        WHEN itemid = 50889 THEN 'C_REACTIVE_PROTEIN'
        WHEN itemid = 50915 THEN 'D_DIMER'
        WHEN itemid = 51133 THEN 'ABSOLUTE_LYMPHOCYTE'
        WHEN itemid = 51143 THEN 'ATYPICAL_LYMPHOCYTES'
        WHEN itemid = 51196 THEN 'D_DIMER'
        WHEN itemid = 51212 THEN 'FETAL_HEMOGLOBIN'
        WHEN itemid = 51214 THEN 'FIBRINOGEN'
        WHEN itemid = 51223 THEN 'HEMOGLOBIN_A2'
        WHEN itemid = 51224 THEN 'HEMOGLOBIN_C'
        WHEN itemid = 51225 THEN 'HEMOGLOBIN_F'
        WHEN itemid = 51240 THEN 'LARGE_PLATELETS'
        WHEN itemid = 51241 THEN 'LEUKOCYTE_ALKALINE_PHOSPHATASE'
        WHEN itemid = 51244 THEN 'LYMPHOCYTES'
        WHEN itemid = 51245 THEN 'LYMPHOCYTES_PERCENT'
        WHEN itemid = 51264 THEN 'PLATELET_CLUMPS'
        WHEN itemid = 51266 THEN 'PLATELET_SMEAR'
        WHEN itemid = 51285 THEN 'RETICULOCYTE'
      ELSE null
    END AS label
  , -- Note: there is no sanity checks on the values
  -- the where clause below requires all valuenum to be > 0, so there needs to upper limit checks
  le.valuenum AS valuenum

  FROM icustays ie

  LEFT JOIN labevents le
    ON le.subject_id = ie.subject_id AND le.hadm_id = ie.hadm_id
    AND le.charttime BETWEEN (ie.intime - interval '6' hour) AND (ie.intime + interval '1' day)
    AND le.ITEMID in
    (
        -- comment is: LABEL | CATEGORY | FLUID | NUMBER OF ROWS IN LABEVENTS
        50805, -- Carboxyhemoglobin | Blood | Blood Gas  | 20563-3
        50814, -- Methemoglobin | Blood | Blood Gas  | 2614-6
        50852, -- % Hemoglobin A1c | Blood | Chemistry  | 4548-4
        50855, -- Absolute Hemoglobin | Blood | Chemistry  | 718-7
        50861, -- Alanine Aminotransferase (ALT) | Blood | Chemistry  | 1742-6
        50878, -- Asparate Aminotransferase (AST) | Blood | Chemistry  | 1920-8
        50889, -- C-Reactive Protein | Blood | Chemistry  | 1988-5
        50915, -- D-Dimer | Blood | Chemistry | 
        51133, -- Absolute Lymphocyte Count | Blood | Hematology | 26474-7
        51143, -- Atypical Lymphocytes | Blood | Hematology | 733-6
        51196, -- D-Dimer | Blood | Hematology | 48065-7
        51212, -- Fetal Hemoglobin | Blood | Hematology | 4576-5
        51214, -- Fibrinogen, Functional | Blood | Hematology | 3255-7
        51223, -- Hemoglobin A2 | Blood | Hematology | 4552-6
        51224, -- Hemoglobin C | Blood | Hematology | 4561-7
        51225, -- Hemoglobin F | Blood | Hematology | 9749-3
        51240, -- Large Platelets | Blood | Hematology | 34167-7
        51241, -- Leukocyte Alkaline Phosphatase | Blood | Hematology | 4659-9
        51244, -- Lymphocytes | Blood | Hematology | 731-0
        51245, -- Lymphocytes, Percent | Blood | Hematology | 26478-8
        51264, -- Platelet Clumps | Blood | Hematology | 40741-1
        51266, -- Platelet Smear | Blood | Hematology | 778-1
        51285 -- Reticulocyte, Cellular Hemoglobin | Blood | Hematology | 
    )
    AND valuenum IS NOT null AND valuenum > 0 -- lab values cannot be 0 and cannot be negative
) pvt
GROUP BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id
ORDER BY pvt.subject_id, pvt.hadm_id, pvt.icustay_id;



