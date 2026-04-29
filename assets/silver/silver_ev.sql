/* @bruin

name: silver.ev_data
type: duckdb.sql
materialization:
  type: table
description: Cleaned and standardized EV data
depends:
  - bronze.ev_data

@bruin */

SELECT 
    vin,
    UPPER(TRIM(CAST(county AS VARCHAR))) as county,
    UPPER(TRIM(CAST(city AS VARCHAR))) as city,
    UPPER(TRIM(CAST(state AS VARCHAR))) as state,
    TRIM(CAST(postal_code AS VARCHAR)) as postal_code,
    model_year,
    UPPER(TRIM(CAST(make AS VARCHAR))) as make,
    UPPER(TRIM(CAST(model AS VARCHAR))) as model,
    CASE 
        WHEN CAST(ev_type AS VARCHAR) LIKE '%Battery%' THEN 'BEV'
        WHEN CAST(ev_type AS VARCHAR) LIKE '%Plug%' THEN 'PHEV'
        ELSE 'Other'
    END as ev_type_clean,
    CAST(cafv_eligibility AS VARCHAR) as cafv_eligibility,
    CURRENT_TIMESTAMP as loaded_at
FROM bronze.ev_data
WHERE model_year IS NOT NULL
    AND make IS NOT NULL
    AND model IS NOT NULL