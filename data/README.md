# Ventilation and Pneumonia focused ICU Dataset

The origin dataset is MIMIC-III database [link](https://mimic.physionet.org/). You must cite the below if you use this data.

> MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. Available from: http://www.nature.com/articles/sdata201635

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
