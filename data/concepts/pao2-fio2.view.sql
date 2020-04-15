-- This view creates concept for aggreated pao2, fio2 values for icu stay

-- itemid |     label     |   linksto   | category 
-- --------+---------------+-------------+----------
--     190 | FiO2 Set      | chartevents | 
--     490 | PAO2          | chartevents | 
--     779 | Arterial PaO2 | chartevents | ABG
--    3420 | FIO2          | chartevents | 

DROP MATERIALIZED VIEW IF EXISTS pao2_fio2 CASCADE;
CREATE materialized VIEW pao2_fio2 AS
    SELECT subject_id, icustay_id
        , min(
            CASE    
                WHEN itemid = 3420 THEN valuenum
                ELSE NULL END
        ) AS min_fio2
        , max(
            CASE    
                WHEN itemid = 3420 THEN valuenum
                ELSE NULL END
        ) AS max_fio2
        , min(
            CASE
                WHEN itemid = 190 AND valuenum > 0.20 AND valuenum < 1
                -- well formatted but not in %
                THEN valuenum * 100
                ELSE NULL END
        ) AS min_fio2_set
        , max(
            CASE
                WHEN itemid = 190 AND valuenum > 0.20 AND valuenum < 1
                -- well formatted but not in %
                THEN valuenum * 100
                ELSE NULL END
        ) AS max_fio2_set
        , min(
            CASE WHEN itemid=490 THEN valuenum
            ELSE NULL END
        ) AS min_pao2
        , max(
            CASE WHEN itemid=490 THEN valuenum
            ELSE NULL END
        ) AS max_pao2
        , min(
            CASE WHEN itemid=779 THEN valuenum
            ELSE NULL END
        ) AS min_arterial_pao2
        , max(
            CASE WHEN itemid=779 THEN valuenum
            ELSE NULL END
        ) AS max_arterial_pao2
    FROM chartevents
    WHERE itemid IN
    (
    3420 -- FiO2
    , 190 -- FiO2 set
    , 490 -- PA02
    , 779 -- Arterial PaO2
    )
    -- exclude rows marked as error
    AND error IS DISTINCT FROM 1
    GROUP BY subject_id, icustay_id;
 



