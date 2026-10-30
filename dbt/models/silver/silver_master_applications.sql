{{ config(materialized='table') }}

WITH joined AS (
  SELECT
    a.applicant_id,
    a.applicant_name,
    a.ssn,
    a.loan_amount,
    a.property_value,
    a.monthly_gross_income,
    b.fico_score,
    b.monthly_debt,
    (a.loan_amount / NULLIF(a.property_value, 0)) * 100 AS ltv_pct,
    (b.monthly_debt / NULLIF(a.monthly_gross_income, 0)) * 100 AS dti_pct
  FROM {{ ref('bronze_applications') }} AS a
  LEFT JOIN {{ ref('bronze_credit_bureau') }} AS b
    ON a.applicant_id = b.applicant_id
),
masked AS (
  SELECT
    applicant_id,
    CONCAT('***', RIGHT(applicant_name, 3)) AS applicant_name,
    CONCAT('***-**-', RIGHT(ssn, 4)) AS ssn,
    loan_amount,
    property_value,
    monthly_gross_income,
    fico_score,
    monthly_debt,
    ltv_pct,
    dti_pct
  FROM joined
)
SELECT * FROM masked
