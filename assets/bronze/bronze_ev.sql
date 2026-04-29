/* @bruin

name: bronze.ev_data
type: duckdb.sql
materialization:
  type: table
description: Raw EV adoption data loaded from CSV file

@bruin */

SELECT 
    "VIN (1-10)" as vin,
    County as county,
    City as city,
    State as state,
    "Postal Code" as postal_code,
    "Model Year"::INTEGER as model_year,
    Make as make,
    Model as model,
    "Electric Vehicle Type" as ev_type,
    "Clean Alternative Fuel Vehicle (CAFV) Eligibility" as cafv_eligibility
FROM read_csv_auto('assets/data/Electric_Vehicle_Population_Data.csv');