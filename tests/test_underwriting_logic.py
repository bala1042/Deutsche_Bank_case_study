from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from underwriting_rules import calculate_dti, calculate_ltv, route_application


def test_ltv_calculation():
    assert calculate_ltv(360000, 400000) == 90.0


def test_dti_calculation():
    assert calculate_dti(2000, 4500) == 44.44444444444444


def test_approved_application():
    result = route_application(300000, 500000, 1200, 4500, 710)
    assert result["decision_status"] == "APPROVED"
    assert result["reason_codes"] == ["APPROVED"]


def test_requires_co_signer():
    result = route_application(280000, 350000, 1800, 4200, 640)
    assert result["decision_status"] == "REQUIRES_CO_SIGNER"
    assert result["reason_codes"] == ["REQUIRES_CO_SIGNER"]


def test_declined_application():
    result = route_application(400000, 420000, 2800, 5000, 610)
    assert result["decision_status"] == "DECLINED"
    assert "DECLINED_DTI_EXCEEDED" in result["reason_codes"]
    assert "DECLINED_CREDIT_SCORE_BELOW_620" in result["reason_codes"]
