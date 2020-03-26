# Ventilation and Pneumonia focused ICU Dataset

This dataset is intended for researchers, decision makers, technology developers, and others whose decisions depend on understanding of ventilation use in an ICU setting, specifically in viral influenza context. The origin dataset is MIMIC-III database [link](https://mimic.physionet.org/). You must cite the below if you use this data.

> MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. Available from: http://www.nature.com/articles/sdata201635

## Description

- BASE: **61,532** ICU stays (may be more than one per patient)
- SAMPLE SIZE: **5,890** patients with pneumonia diagnosis
- RECORD/ROW: each row represents a single hospital admission and in case the admission involves more than one ICU stay, the last ICU stay*
- FEATURES/COLUMNS: features contain patient meta-data, survival outcomes, pneumonia specific meta-data, ventilation durations, and various blood serum values, including those that are highlighted in COVID-19 literature

NOTE*:`ventilation_duration_hours` is a sum of ventilation duration from all the ICU stays for the patient on a single hospital admission, and `hours_before_ventilation` is the time between hospital admission and first instance of ventilation.

## Data Taxonomy

name | description | type
--- | --- | ---
**id** | Masked identifier for last icu stay for a patient over all admissions | (String) 
**age_in_years** | Age of patient at the time of admission | (Integer) 
**age_group** | Age group of patient | (Interger Range)
**pneumonia_influenza_source** | Whether diagnosed with pneumonia due to influenza | (Boolean)
**pneumonia_viral_source** | Whether diagnozed with pneumonia due to viral infection | (Boolean)
**hospital_survival** | Patient survived till discharge from hospital | (Boolean)
**month_survival** | Patient survived at least 30 days after discharge from hospital | (Boolean)
**year_survival** | Patient survived at least 365 days after discharge from hospital | (Boolean)
**on_ventilator** | Patient was on ventilator during icu stay | (Boolean)
**ventilation_duration_hours** | Total hours of ventilation | (Numeric)
**expired_during_ventilation** | Patient expired during ventilation | (Boolean)
**hours_before_ventilation** | Time gap in hours between admission and first ventilation | (Integer)
**diagnosed_ards** | Whether diagnosed with ARDS | (Boolean)
**aniongap_min** | first day aniongap_min | (Numeric or Missing)
**aniongap_max** | first day aniongap_max | (Numeric or Missing)
**albumin_min** | first day albumin_min | (Numeric or Missing)
**albumin_max** | first day albumin_max | (Numeric or Missing)
**bands_min** | first day bands_min | (Numeric or Missing)
**bands_max** | first day bands_max | (Numeric or Missing)
**bicarbonate_min** | first day bicarbonate_min | (Numeric or Missing)
**bicarbonate_max** | first day bicarbonate_max | (Numeric or Missing)
**bilirubin_min** | first day bilirubin_min | (Numeric or Missing)
**bilirubin_max** | first day bilirubin_max | (Numeric or Missing)
**creatinine_min** | first day creatinine_min | (Numeric or Missing)
**creatinine_max** | first day creatinine_max | (Numeric or Missing)
**chloride_min** | first day chloride_min | (Numeric or Missing)
**chloride_max** | first day chloride_max | (Numeric or Missing)
**glucose_min** | first day glucose_min | (Numeric or Missing)
**glucose_max** | first day glucose_max | (Numeric or Missing)
**hematocrit_min** | first day hematocrit_min | (Numeric or Missing)
**hematocrit_max** | first day hematocrit_max | (Numeric or Missing)
**hemoglobin_min** | first day hemoglobin_min | (Numeric or Missing)
**hemoglobin_max** | first day hemoglobin_max | (Numeric or Missing)
**lactate_min** | first day lactate_min | (Numeric or Missing)
**lactate_max** | first day lactate_max | (Numeric or Missing)
**platelet_min** | first day platelet_min | (Numeric or Missing)
**platelet_max** | first day platelet_max | (Numeric or Missing)
**potassium_min** | first day potassium_min | (Numeric or Missing)
**potassium_max** | first day potassium_max | (Numeric or Missing)
**ptt_min** | first day ptt_min | (Numeric or Missing)
**ptt_max** | first day ptt_max | (Numeric or Missing)
**inr_min** | first day inr_min | (Numeric or Missing)
**inr_max** | first day inr_max | (Numeric or Missing)
**pt_min** | first day pt_min | (Numeric or Missing)
**pt_max** | first day pt_max | (Numeric or Missing)
**sodium_min** | first day sodium_min | (Numeric or Missing)
**sodium_max** | first day sodium_max | (Numeric or Missing)
**bun_min** | first day bun_min | (Numeric or Missing)
**bun_max** | first day bun_max | (Numeric or Missing)
**wbc_min** | first day wbc_min | (Numeric or Missing)
**wbc_max** | first day wbc_max | (Numeric or Missing)

