# COVID-19 ICU Burden: what can we learn from available ICU data?

The dataset have been made to be as highly relevant to COVID-19 related ICU capacity problem that currently threatens healthcare systems all over the world. Full description of the dataset is provide [below](#overview).

<img width="300px" src="https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/ICU.png">

An attempt has been to provide the dataset in a format as accessible and clearly document as possible. 

## :pushpin: Dataset Themes

- ICU
- pneumonia patients
- ARDS
- ventilation
- viral influenza

## :tv: Intended Audience

Anyone whose decisions related with COVID-19 depend on understanding ICU mortality, ventilation use, and ARDS in pneumonia patients.

## :information_source: Overview

The dataset consist of hospital admissions that led to an ICU stay. There are records for over 5,000 ICU stays where a pneumonia diagnosis is present. The dataset provides ~100 features on ventilation use, pneumonia characteristics, viral influenza, and acute respiratory distress syndrome (ARDS). There are a large number of blood serum markers available, including all known COVID-19 specific markers that were available.

The dataset is sampled from MIMIC, which *"is an openly available dataset developed by the MIT Lab for Computational Physiology, comprising deidentified health data associated with ~60,000 intensive care unit admissions. It includes demographics, vital signs, laboratory tests, medications, and more."* 

## :nut_and_bolt: Description

- BASE: **61,532** ICU stays (may be more than one per patient)
- SAMPLE SIZE: **5,890** patients with pneumonia diagnosis
- RECORD/ROW: each row represents a single hospital admission and in case the admission involves more than one ICU stay, the last ICU stay*
- FEATURES/COLUMNS: features contain patient meta-data, survival outcomes, pneumonia specific meta-data, ventilation durations, and various blood serum values, including those that are highlighted in COVID-19 literature

NOTE*:`ventilation_duration_hours` is a sum of ventilation duration from all the ICU stays for the patient on a single hospital admission, and `hours_before_ventilation` is the time between hospital admission and first instance of ventilation. The hospital admission id (`hadm_id`) used in MIMIC is obfuscated, but lookup table can be provided for those that verify their right to access MIMIC. 


## :open_file_folder: Data Taxonomy

<details>
  <summary>Display full data taxonomy</summary>
  
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
**CARBOXYHEMOGLOBIN_min** | first day CARBOXYHEMOGLOBIN_min, | (Numeric or Missing)
**CARBOXYHEMOGLOBIN_max** | first day CARBOXYHEMOGLOBIN_max, | (Numeric or Missing)
**METHEMOGLOBIN_min** | first day METHEMOGLOBIN_min, | (Numeric or Missing)
**METHEMOGLOBIN_max** | first day METHEMOGLOBIN_max, | (Numeric or Missing)
**PERCENTAGE_HEMOGLOBIN_A1C_min** | first day PERCENTAGE_HEMOGLOBIN_A1C_min, | (Numeric or Missing)
**PERCENTAGE_HEMOGLOBIN_A1C_max** | first day PERCENTAGE_HEMOGLOBIN_A1C_max, | (Numeric or Missing)
**ABSOLUTE_HEMOGLOBIN_min** | first day ABSOLUTE_HEMOGLOBIN_min, | (Numeric or Missing)
**ABSOLUTE_HEMOGLOBIN_max** | first day ABSOLUTE_HEMOGLOBIN_max, | (Numeric or Missing)
**ALANINE_AMINOTRANSFERASE_min** | first day ALANINE_AMINOTRANSFERASE_min, | (Numeric or Missing)
**ALANINE_AMINOTRANSFERASE_max** | first day ALANINE_AMINOTRANSFERASE_max, | (Numeric or Missing)
**ASPARATE_AMINOTRANSFERASE_min** | first day ASPARATE_AMINOTRANSFERASE_min, | (Numeric or Missing)
**ASPARATE_AMINOTRANSFERASE_max** | first day ASPARATE_AMINOTRANSFERASE_max, | (Numeric or Missing)
**C_REACTIVE_PROTEIN_min** | first day C_REACTIVE_PROTEIN_min, | (Numeric or Missing)
**C_REACTIVE_PROTEIN_max** | first day C_REACTIVE_PROTEIN_max, | (Numeric or Missing)
**D_DIMER_min** | first day D_DIMER_min, | (Numeric or Missing)
**D_DIMER_max** | first day D_DIMER_max, | (Numeric or Missing)
**ABSOLUTE_LYMPHOCYTE_min** | first day ABSOLUTE_LYMPHOCYTE_min, | (Numeric or Missing)
**ABSOLUTE_LYMPHOCYTE_max** | first day ABSOLUTE_LYMPHOCYTE_max, | (Numeric or Missing)
**ATYPICAL_LYMPHOCYTES_min** | first day ATYPICAL_LYMPHOCYTES_min, | (Numeric or Missing)
**ATYPICAL_LYMPHOCYTES_max** | first day ATYPICAL_LYMPHOCYTES_max, | (Numeric or Missing)
**FETAL_HEMOGLOBIN_min** | first day FETAL_HEMOGLOBIN_min, | (Numeric or Missing)
**FETAL_HEMOGLOBIN_max** | first day FETAL_HEMOGLOBIN_max, | (Numeric or Missing)
**FIBRINOGEN_min** | first day FIBRINOGEN_min, | (Numeric or Missing)
**FIBRINOGEN_max** | first day FIBRINOGEN_max, | (Numeric or Missing)
**HEMOGLOBIN_A2_min** | first day HEMOGLOBIN_A2_min, | (Numeric or Missing)
**HEMOGLOBIN_A2_max** | first day HEMOGLOBIN_A2_max, | (Numeric or Missing)
**HEMOGLOBIN_C_min** | first day HEMOGLOBIN_C_min, | (Numeric or Missing)
**HEMOGLOBIN_C_max** | first day HEMOGLOBIN_C_max, | (Numeric or Missing)
**HEMOGLOBIN_F_min** | first day HEMOGLOBIN_F_min, | (Numeric or Missing)
**HEMOGLOBIN_F_max** | first day HEMOGLOBIN_F_max, | (Numeric or Missing)
**LARGE_PLATELETS_min** | first day LARGE_PLATELETS_min, | (Numeric or Missing)
**LARGE_PLATELETS_max** | first day LARGE_PLATELETS_max, | (Numeric or Missing)
**LEUKOCYTE_ALKALINE_PHOSPHATASE_min** | first day LEUKOCYTE_ALKALINE_PHOSPHATASE_min, | (Numeric or Missing)
**LEUKOCYTE_ALKALINE_PHOSPHATASE_max** | first day LEUKOCYTE_ALKALINE_PHOSPHATASE_max, | (Numeric or Missing)
**LYMPHOCYTES_min** | first day LYMPHOCYTES_min, | (Numeric or Missing)
**LYMPHOCYTES_max** | first day LYMPHOCYTES_max, | (Numeric or Missing)
**LYMPHOCYTES_PERCENT_min** | first day LYMPHOCYTES_PERCENT_min, | (Numeric or Missing)
**LYMPHOCYTES_PERCENT_max** | first day LYMPHOCYTES_PERCENT_max, | (Numeric or Missing)
**PLATELET_CLUMPS_min** | first day PLATELET_CLUMPS_min, | (Numeric or Missing)
**PLATELET_CLUMPS_max** | first day PLATELET_CLUMPS_max, | (Numeric or Missing)
**PLATELET_SMEAR_min** | first day PLATELET_SMEAR_min, | (Numeric or Missing)
**PLATELET_SMEAR_max** | first day PLATELET_SMEAR_max, | (Numeric or Missing)
**RETICULOCYTE_min** | first day RETICULOCYTE_min, | (Numeric or Missing)
**RETICULOCYTE_max** | first day RETICULOCYTE_max | (Numeric or Missing)

</details>

The data taxonomy is available in [Google Sheet](https://docs.google.com/spreadsheets/d/1Pqyb_eMfog4NOH-Nst54ebzikquSxxi2JfmkyxCqbBE/edit?usp=sharing) and [csv](https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/TTI_ICU_Burden_Dataset_Taxonomy.csv). Alternatively, download to local machine:

`wget https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/TTI_ICU_Burden_Dataset_Taxonomy.csv`

## :inbox_tray: Download

You can download the dataset [here](https://github.com/autonomio/trauma-team-international/raw/master/data/icu_dataset.csv) or from command line: 

```
wget https://github.com/autonomio/trauma-team-international/raw/master/data/icu_dataset.csv
```

### 💬 How to get help

| I want to...                     | Go to...                                                  |
| -------------------------------- | ---------------------------------------------------------- |
| **...connect with others**      | [Discord]                                            |
| **...read the wiki**           | [Wiki]                                  |
| **...suggest something**  | [GitHub Issue Tracker]                                     |

<hr>

### 📢 Citations

If you use Trauma Team International's research, data, or findings for published work, please cite:

`Autonomio, Trauma Team International. (2020). Retrieved from http://github.com/autonomio/trauma-team-international/.`

You must separately cite MIMIC:

> MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. Available from: http://www.nature.com/articles/sdata201635

<hr>

### 📃 License

[MIT License](https://github.com/autonomio/talos/blob/master/LICENSE)

[github issue tracker]: https://github.com/automio/trauma-team-international/issues
[wiki]: https://github.com/autonomio/talos/wiki
[discord]: https://discord.gg/t7vk27
