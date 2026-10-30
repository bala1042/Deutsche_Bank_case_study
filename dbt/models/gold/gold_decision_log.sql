{{ config(materialized='table') }}

WITH valid_applications AS (
  SELECT *
  FROM {{ ref('silver_master_applications') }}
  WHERE applicant_id NOT IN (
    SELECT applicant_id FROM {{ ref('technical_rejections') }}
  )
),
finalized AS (
  SELECT
    applicant_id,
    applicant_name,
    ssn,
    loan_amount,
    property_value,
    monthly_gross_income,
    fico_score,
    monthly_debt,
    ltv_pct,
    dti_pct,
    CASE
      WHEN ltv_pct > 95 THEN 'DECLINED_LTV_EXCEEDED'
      WHEN dti_pct > 43 THEN 'DECLINED_DTI_EXCEEDED'
      WHEN fico_score < 620 THEN 'DECLINED_CREDIT_SCORE_BELOW_620'
      WHEN fico_score BETWEEN 620 AND 660 AND dti_pct BETWEEN 36 AND 43 THEN 'REQUIRES_CO_SIGNER'
      ELSE 'APPROVED'
    END AS decision_status,
    CASE
      WHEN ltv_pct > 95 THEN 'DECLINED_LTV_EXCEEDED'
      WHEN dti_pct > 43 THEN 'DECLINED_DTI_EXCEEDED'
      WHEN fico_score < 620 THEN 'DECLINED_CREDIT_SCORE_BELOW_620'
      WHEN fico_score BETWEEN 620 AND 660 AND dti_pct BETWEEN 36 AND 43 THEN 'REQUIRES_CO_SIGNER'
      ELSE 'APPROVED'
    END AS reason_code
  FROM valid_applications
)
SELECT * FROM finalized
