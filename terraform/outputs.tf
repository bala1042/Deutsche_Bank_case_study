output "database_name" {
  value = snowflake_database.mortgage_lending.name
}

output "warehouse_name" {
  value = snowflake_warehouse.mortgage_wh.name
}

output "roles" {
  value = [
    snowflake_role.loan_analyst.name,
    snowflake_role.compliance_officer.name,
    snowflake_role.pipeline_admin.name,
  ]
}
