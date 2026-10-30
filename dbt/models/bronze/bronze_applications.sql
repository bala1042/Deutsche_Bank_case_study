{{ config(materialized='table') }}

SELECT
  applicant_id,
  applicant_name,
  ssn,
  loan_amount,
  property_value,
  monthly_gross_income,
  CURRENT_TIMESTAMP AS ingested_at
FROM {{ source('bronze', 'mortgage_applications') }}
