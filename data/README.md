<img width="100%" src="https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/ICU_burden_dataset_infosheet.jpg">

## COVID-19 ICU Burden: what can we learn from available ICU data?

Examples of good use for this dataset: 

- Capacity analysis (e.g. "how many ventilators do we need for a certain patient flow?")
- Survival analysis (e.g "how to increase rate of 1-year survival?")

The dataset is aimed to be highly relevant to COVID-19 related ICU capacity problem related research and decision making. Most data science and research workflows can be performed with zero ETL. Full description of the dataset is provided [below](#overview).

- [Dataset Themes](#pushpin-dataset-themes)
- [Intended Audience](#tv-intended-audience)
- [Overview](#information_source-overview)
- [Description](#nut_and_bolt-description)
- [Data Taxonomy](#open_file_folder-data-taxonomy)
- [Download](#inbox_tray-download)
- [Support](#speech_balloon-support)
- [Citations](#loudspeaker-citations)
- [License](#page_with_curl-license)

The underlying dataset from which a sample have been drawn, [MIMIC](https://mimic.physionet.org/), is used in a large number of ICU related scientific works and provides unparalleled confidence for the reseachers that work with it. An attempt has been made to provide the current dataset in a format as accessible and clearly documented as possible, without compromising the integrity of its origin (MIMIC). 

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

<img width="100%" src="https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/ICU_burden_dataset_infosheet_2.jpg">

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
**id** | masked identifier for last icu stay for a patient over all admissions | (string)
**icu_duration_hours** | hours of stay in ICU | (integer) 
**age_in_years** | age of patient at the time of admission | (integer) 
**age_group** | age group of patient | (interger range)
**pneumonia_influenza_source** | whether diagnosed with pneumonia due to influenza | (boolean)
**pneumonia_viral_source** | whether diagnozed with pneumonia due to viral infection | (boolean)
**hospital_survival** | patient survived till discharge from hospital | (boolean)
**month_survival** | patient survived at least 30 days after discharge from hospital | (boolean)
**year_survival** | patient survived at least 365 days after discharge from hospital | (boolean)
**on_ventilator** | patient was on ventilator during icu stay | (boolean)
**ventilation_duration_hours** | total hours of ventilation | (numeric)
**expired_during_ventilation** | patient expired during ventilation | (boolean)
**hours_before_ventilation** | time gap in hours between admission and first ventilation | (integer)
**diagnosed_ards** | whether diagnosed with ards | (boolean)
**aniongap_min** | first day aniongap_min | (numeric or missing)
**aniongap_max** | first day aniongap_max | (numeric or missing)
**albumin_min** | first day albumin_min | (numeric or missing)
**albumin_max** | first day albumin_max | (numeric or missing)
**bands_min** | first day bands_min | (numeric or missing)
**bands_max** | first day bands_max | (numeric or missing)
**bicarbonate_min** | first day bicarbonate_min | (numeric or missing)
**bicarbonate_max** | first day bicarbonate_max | (numeric or missing)
**bilirubin_min** | first day bilirubin_min | (numeric or missing)
**bilirubin_max** | first day bilirubin_max | (numeric or missing)
**creatinine_min** | first day creatinine_min | (numeric or missing)
**creatinine_max** | first day creatinine_max | (numeric or missing)
**chloride_min** | first day chloride_min | (numeric or missing)
**chloride_max** | first day chloride_max | (numeric or missing)
**glucose_min** | first day glucose_min | (numeric or missing)
**glucose_max** | first day glucose_max | (numeric or missing)
**hematocrit_min** | first day hematocrit_min | (numeric or missing)
**hematocrit_max** | first day hematocrit_max | (numeric or missing)
**hemoglobin_min** | first day hemoglobin_min | (numeric or missing)
**hemoglobin_max** | first day hemoglobin_max | (numeric or missing)
**lactate_min** | first day lactate_min | (numeric or missing)
**lactate_max** | first day lactate_max | (numeric or missing)
**platelet_min** | first day platelet_min | (numeric or missing)
**platelet_max** | first day platelet_max | (numeric or missing)
**potassium_min** | first day potassium_min | (numeric or missing)
**potassium_max** | first day potassium_max | (numeric or missing)
**ptt_min** | first day ptt_min | (numeric or missing)
**ptt_max** | first day ptt_max | (numeric or missing)
**inr_min** | first day inr_min | (numeric or missing)
**inr_max** | first day inr_max | (numeric or missing)
**pt_min** | first day pt_min | (numeric or missing)
**pt_max** | first day pt_max | (numeric or missing)
**sodium_min** | first day sodium_min | (numeric or missing)
**sodium_max** | first day sodium_max | (numeric or missing)
**bun_min** | first day bun_min | (numeric or missing)
**bun_max** | first day bun_max | (numeric or missing)
**wbc_min** | first day wbc_min | (numeric or missing)
**wbc_max** | first day wbc_max | (numeric or missing)
**sofa_score** | icu chartevents sofa score     | numeric
**sofa_respiration_score** | icu chartevents respiration sofa score | numeric
**sofa_coagulation_score** | icu chartevents coagulation sofa score | numeric
**sofa_liver_score**       | icu chartevents liver sofa score       | numeric
**sofa_cardiovascular_score** | icu chartevents cardiovascular sofa score | numeric
**sofa_cns_score**            | cns (sofa) score                          | numeric
**sofa_renal_score**          | renal (sofa) score                        | numeric
**qsofa_score**            | quick sofa score               | (numeric or missing)
**qsofa_sysbp_score**      | quick sofa sys BP score        | (numeric or missing)
**qsofa_gcs_score**        | quick sofa gcs score           | (numeric or missing)
**qsofa_resprate_score**   | quick sofa respiration rate score | (numeric or missing)
**min_fio2_set**     | fio2 set score min | (numeric or missing)
**max_fio2_set**     | fio2 set score max | (numeric or missing)
**min_arterial_pao2** | arterial PaO2 min | (numeric or missing)
**max_arterial_pao2** | arterial PaO2 max | (numeric or missing) 
</details>

The data taxonomy is also available in [Google Sheet](https://docs.google.com/spreadsheets/d/1Pqyb_eMfog4NOH-Nst54ebzikquSxxi2JfmkyxCqbBE/edit?usp=sharing) and [csv](https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/TTI_ICU_Burden_Dataset_Taxonomy.csv). Alternatively, download to local machine:

`wget https://raw.githubusercontent.com/autonomio/trauma-team-international/master/assets/TTI_ICU_Burden_Dataset_Taxonomy.csv`

## :inbox_tray: Download

You can download the dataset [here](https://github.com/autonomio/trauma-team-international/raw/master/data/icu_burden_dataset.csv) or from command line: 

```
wget https://github.com/autonomio/trauma-team-international/raw/master/data/icu_burden_dataset.csv
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
