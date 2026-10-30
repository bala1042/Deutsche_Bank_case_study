{{ config(materialized='table') }}

SELECT
  decision_status,
  COUNT(*) AS application_count,
  SUM(loan_amount) AS total_loan_volume,
  AVG(fico_score) AS avg_fico_score,
  AVG(ltv_pct) AS avg_ltv_pct,
  AVG(dti_pct) AS avg_dti_pct
FROM {{ ref('gold_decision_log') }}
GROUP BY decision_status
ORDER BY decision_status
