{{ config(materialized='table') }}

SELECT
  applicant_id,
  applicant_name,
  ssn,
  loan_amount,
  property_value,
  monthly_gross_income,
  fico_score,
  monthly_debt,
  'MISSING_CRITICAL_FIELD' AS rejection_reason
FROM {{ ref('silver_master_applications') }}
WHERE fico_score IS NULL
   OR property_value IS NULL
   OR monthly_gross_income IS NULL
