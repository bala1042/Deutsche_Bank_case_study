terraform {
  required_version = ">= 1.5.0"

  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.92"
    }
  }
}

provider "snowflake" {
  account  = var.snowflake_account
  username = var.snowflake_username
  password = var.snowflake_password
  region   = var.snowflake_region
  role     = "SYSADMIN"
}

resource "snowflake_database" "mortgage_lending" {
  name = "MORTGAGE_LENDING"
}

resource "snowflake_schema" "bronze" {
  database = snowflake_database.mortgage_lending.name
  name     = "BRONZE"
}

resource "snowflake_schema" "silver" {
  database = snowflake_database.mortgage_lending.name
  name     = "SILVER"
}

resource "snowflake_schema" "gold" {
  database = snowflake_database.mortgage_lending.name
  name     = "GOLD"
}

resource "snowflake_warehouse" "mortgage_wh" {
  name           = "MORTGAGE_WH"
  warehouse_size = "XSMALL"
  auto_suspend   = 60
  auto_resume    = true
  initially_suspended = true
}

resource "snowflake_role" "loan_analyst" {
  name = "LOAN_ANALYST"
}

resource "snowflake_role" "compliance_officer" {
  name = "COMPLIANCE_OFFICER"
}

resource "snowflake_role" "pipeline_admin" {
  name = "PIPELINE_ADMIN"
}

resource "snowflake_database_grant" "db_usage" {
  database_name = snowflake_database.mortgage_lending.name
  privilege      = "USAGE"
  roles          = [snowflake_role.loan_analyst.name, snowflake_role.compliance_officer.name, snowflake_role.pipeline_admin.name]
}

resource "snowflake_schema_grant" "bronze_usage" {
  database_name = snowflake_database.mortgage_lending.name
  schema_name   = snowflake_schema.bronze.name
  privilege     = "USAGE"
  roles         = [snowflake_role.pipeline_admin.name]
}

resource "snowflake_schema_grant" "silver_usage" {
  database_name = snowflake_database.mortgage_lending.name
  schema_name   = snowflake_schema.silver.name
  privilege     = "USAGE"
  roles         = [snowflake_role.loan_analyst.name, snowflake_role.compliance_officer.name]
}

resource "snowflake_schema_grant" "gold_usage" {
  database_name = snowflake_database.mortgage_lending.name
  schema_name   = snowflake_schema.gold.name
  privilege     = "USAGE"
  roles         = [snowflake_role.loan_analyst.name, snowflake_role.compliance_officer.name]
}

resource "snowflake_masking_policy" "ssn_masking_policy" {
  name     = "SSN_MASKING_POLICY"
  database = snowflake_database.mortgage_lending.name
  schema   = snowflake_schema.silver.name
  signature = {
    "INPUT" = "VARCHAR"
  }
  return_data_type = "VARCHAR"
  statement        = <<SQL
CASE
  WHEN CURRENT_ROLE() IN ('COMPLIANCE_OFFICER') THEN INPUT
  ELSE CONCAT('***-**-', RIGHT(INPUT, 4))
END
SQL
}

resource "snowflake_masking_policy" "applicant_name_masking_policy" {
  name     = "APPLICANT_NAME_MASKING_POLICY"
  database = snowflake_database.mortgage_lending.name
  schema   = snowflake_schema.silver.name
  signature = {
    "INPUT" = "VARCHAR"
  }
  return_data_type = "VARCHAR"
  statement        = <<SQL
CASE
  WHEN CURRENT_ROLE() IN ('COMPLIANCE_OFFICER') THEN INPUT
  ELSE '***' || RIGHT(INPUT, 3)
END
SQL
}
