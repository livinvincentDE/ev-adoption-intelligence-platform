/* @bruin

name: gold.ev_trends
type: duckdb.sql
materialization:
  type: table
description: EV trends aggregated by make and model year
depends:
  - silver.ev_data

@bruin */

SELECT 
    model_year,
    make,
    ev_type_clean,
    COUNT(*) as vehicle_count,
    COUNT(DISTINCT state) as states_represented,
    COUNT(DISTINCT county) as counties_represented,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY model_year), 2) as pct_of_year
FROM silver.ev_data
GROUP BY model_year, make, ev_type_clean
ORDER BY model_year DESC, vehicle_count DESC