{{ config(materialized='table') }}

SELECT
  applicant_id,
  ssn,
  fico_score,
  monthly_debt,
  CURRENT_TIMESTAMP AS ingested_at
FROM {{ source('bronze', 'credit_bureau') }}
