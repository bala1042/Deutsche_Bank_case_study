import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

APPLICATIONS = [
    {
        "applicant_id": "APP-1001",
        "applicant_name": "Applicant 1001",
        "ssn": "TEST-SSN-1001",
        "loan_amount": 360000,
        "property_value": 400000,
        "monthly_gross_income": 4500,
    },
    {
        "applicant_id": "APP-1002",
        "applicant_name": "Applicant 1002",
        "ssn": "TEST-SSN-1002",
        "loan_amount": 410000,
        "property_value": 405000,
        "monthly_gross_income": 5200,
    },
    {
        "applicant_id": "APP-1003",
        "applicant_name": "Applicant 1003",
        "ssn": "TEST-SSN-1003",
        "loan_amount": 275000,
        "property_value": 300000,
        "monthly_gross_income": 6100,
    },
    {
        "applicant_id": "APP-1004",
        "applicant_name": "Applicant 1004",
        "ssn": "TEST-SSN-1004",
        "loan_amount": 330000,
        "property_value": 310000,
        "monthly_gross_income": 5000,
    },
    {
        "applicant_id": "APP-1005",
        "applicant_name": "Applicant 1005",
        "ssn": "TEST-SSN-1005",
        "loan_amount": 460000,
        "property_value": 400000,
        "monthly_gross_income": 4200,
    },
]

CREDIT_BUREAU = [
    {"applicant_id": "APP-1001", "ssn": "TEST-SSN-1001", "fico_score": 710, "monthly_debt": 1800},
    {"applicant_id": "APP-1002", "ssn": "TEST-SSN-1002", "fico_score": 640, "monthly_debt": 2100},
    {"applicant_id": "APP-1003", "ssn": "TEST-SSN-1003", "fico_score": 600, "monthly_debt": 1600},
    {"applicant_id": "APP-1004", "ssn": "TEST-SSN-1004", "fico_score": 690, "monthly_debt": 1700},
    {"applicant_id": "APP-1005", "ssn": "TEST-SSN-1005", "fico_score": 610, "monthly_debt": 2200},
]


def write_applications():
    with (DATA_DIR / "mortgage_applications.json").open("w", encoding="utf-8") as fh:
        json.dump(APPLICATIONS, fh, indent=2)


def write_credit_bureau():
    with (DATA_DIR / "credit_bureau.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["applicant_id", "ssn", "fico_score", "monthly_debt"])
        writer.writeheader()
        writer.writerows(CREDIT_BUREAU)


if __name__ == "__main__":
    write_applications()
    write_credit_bureau()
    print(f"Created sample files in {DATA_DIR}")
