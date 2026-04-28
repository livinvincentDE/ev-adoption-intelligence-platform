/* @bruin name: gold_ev_trends type: duckdb.sql */

SELECT year, brand, COUNT(*) AS model_count 
FROM silver_ev 
GROUP BY year, brand;
