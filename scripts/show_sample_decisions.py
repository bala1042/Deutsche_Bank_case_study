import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from underwriting_rules import route_application


def main() -> None:
    data_dir = PROJECT_ROOT / "data"

    with (data_dir / "mortgage_applications.json").open(encoding="utf-8") as file:
        applications = json.load(file)

    with (data_dir / "credit_bureau.csv").open(newline="", encoding="utf-8") as file:
        credit_records = {
            row["applicant_id"]: row for row in csv.DictReader(file)
        }

    print(f"{'Applicant':<14} {'Decision':<20} {'LTV':>8} {'DTI':>8} Reasons")
    for application in applications:
        applicant_id = application["applicant_id"]
        if applicant_id not in credit_records:
            raise ValueError(f"No credit bureau record for {applicant_id}")

        credit = credit_records[applicant_id]
        result = route_application(
            loan_amount=float(application["loan_amount"]),
            property_value=float(application["property_value"]),
            monthly_debt=float(credit["monthly_debt"]),
            monthly_gross_income=float(application["monthly_gross_income"]),
            credit_score=int(credit["fico_score"]),
        )
        print(
            f"{applicant_id:<14} {result['decision_status']:<20} "
            f"{result['ltv_pct']:>7.2f}% {result['dti_pct']:>7.2f}% "
            f"{', '.join(result['reason_codes'])}"
        )


if __name__ == "__main__":
    main()
