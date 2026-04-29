/* @bruin

name: platinum.ev_insights
type: duckdb.sql
materialization:
  type: table
description: High-level EV adoption insights and KPIs
depends:
  - gold.ev_trends

@bruin */

SELECT 
    model_year,
    make,
    ev_type_clean,
    vehicle_count,
    states_represented,
    counties_represented,
    pct_of_year
FROM gold.ev_trends
WHERE vehicle_count > 100
ORDER BY vehicle_count DESC
LIMIT 20