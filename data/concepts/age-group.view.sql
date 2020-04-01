-- This query generates a materialized view for age group distribution of all admissions.

-- Depends On:
    -- Mimic-III Postgres Database

-- function for mapping age to age group
-- groups (15–18, 19–33, 34–48, 49–64, 65–78, and 79–98)
-- source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3825015/
CREATE OR REPLACE FUNCTION age_group(integer)
RETURNS int4range AS $$
  SELECT int4range(
    CASE
      WHEN $1 < 15 THEN int4range(0,15)
      WHEN ($1 >=15 AND $1<19) THEN int4range(15,19)
      WHEN ($1 >=19 AND $1<34) THEN int4range(19,34)
      WHEN ($1 >=34 AND $1<49) THEN int4range(34,49)
      WHEN ($1 >=49 AND $1<65) THEN int4range(49,65)
      WHEN ($1 >=65 AND $1<79) THEN int4range(65,79)
      WHEN ($1 >=79 AND $1<99) THEN int4range(79,99)
      ELSE int4range(99,300)
    END
  )
$$
LANGUAGE SQL;

-- Age group concept
  --  age group at the time of admission.
  -- groups (15–18, 19–33, 34–48, 49–64, 65–78, and 79–98)
  -- source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3825015/
  DROP MATERIALIZED VIEW IF EXISTS age_group CASCADE;
  CREATE MATERIALIZED VIEW age_group AS
  SELECT
  adm.hadm_id,
  date_part('year', age(adm.admittime, p.dob)) as age,
  age_group(date_part('year', age(adm.admittime, p.dob))::integer) as age_group
  FROM
  admissions adm
  INNER JOIN patients p ON p.subject_id=adm.subject_id;
