## Data set : ICU Ventilator Data 
### Source : Mimic-III Database

#### Data Description: CSV file with Header labels as follows

name | description
--- | ---
**id** | Identifier for last icu stay for a patient over all admissions (String) 
**age_in_years** | Age of patient at the time of admission (Integer) 
**age_group** | Age group of patient (Interger Range)
**pneumonia_influenza_source** | Whether diagnosed with pneumonia due to influenza (Boolean)
**pneumonia_viral_source** | Whether diagnozed with pneumonia due to viral infection (Boolean)
**hospital_survival** | Patient survived till discharge from hospital (Boolean)
**month_survival** | Patient survived at least 30 days after discharge from hospital (Boolean)
**year_survival** | Patient survived at least 365 days after discharge from hospital (Boolean)
**on_ventilator** | Patient was on ventilator during icu stay (Boolean)
**ventilation_duration_hours** | Total hours of ventilation (Numeric)
**expired_during_ventilation** | Patient expired during ventilation (Boolean)
**hours_before_ventilation** | Time gap in hours between admission and first ventilation (Integer)
