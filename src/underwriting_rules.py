from __future__ import annotations

from typing import Any, Dict, List


def calculate_ltv(loan_amount: float, property_value: float) -> float:
    if property_value in (None, 0):
        raise ValueError("Property value cannot be zero or null.")
    return (float(loan_amount) / float(property_value)) * 100


def calculate_dti(monthly_debt: float, monthly_gross_income: float) -> float:
    if monthly_gross_income in (None, 0):
        raise ValueError("Monthly gross income cannot be zero or null.")
    return (float(monthly_debt) / float(monthly_gross_income)) * 100


def route_application(
    loan_amount: float,
    property_value: float,
    monthly_debt: float,
    monthly_gross_income: float,
    credit_score: int,
) -> Dict[str, Any]:
    ltv_pct = calculate_ltv(loan_amount, property_value)
    dti_pct = calculate_dti(monthly_debt, monthly_gross_income)

    reason_codes: List[str] = []

    if ltv_pct > 95:
        reason_codes.append("DECLINED_LTV_EXCEEDED")
    if dti_pct > 43:
        reason_codes.append("DECLINED_DTI_EXCEEDED")
    if credit_score < 620:
        reason_codes.append("DECLINED_CREDIT_SCORE_BELOW_620")

    if not reason_codes:
        if 620 <= credit_score <= 660 and 36 <= dti_pct <= 43:
            return {
                "decision_status": "REQUIRES_CO_SIGNER",
                "reason_codes": ["REQUIRES_CO_SIGNER"],
                "ltv_pct": round(ltv_pct, 2),
                "dti_pct": round(dti_pct, 2),
                "credit_score": credit_score,
            }

        return {
            "decision_status": "APPROVED",
            "reason_codes": ["APPROVED"],
            "ltv_pct": round(ltv_pct, 2),
            "dti_pct": round(dti_pct, 2),
            "credit_score": credit_score,
        }

    return {
        "decision_status": "DECLINED",
        "reason_codes": reason_codes,
        "ltv_pct": round(ltv_pct, 2),
        "dti_pct": round(dti_pct, 2),
        "credit_score": credit_score,
    }
