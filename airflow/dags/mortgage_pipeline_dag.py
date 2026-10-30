from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


def notify_failure(context):
    print(f"Pipeline failed: {context['task_instance'].task_id}")


with DAG(
    dag_id="mortgage_underwriting_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 6 * * *",
    catchup=False,
    default_args={
        "on_failure_callback": notify_failure,
        "retries": 1,
    },
) as dag:
    start = EmptyOperator(task_id="start")

    load_applications = BashOperator(
        task_id="load_applications_bronze",
        bash_command="echo 'Load mortgage application JSON into Snowflake Bronze stage'",
    )

    load_credit_bureau = BashOperator(
        task_id="load_credit_bureau_bronze",
        bash_command="echo 'Load credit bureau CSV into Snowflake Bronze stage'",
    )

    dbt_silver = BashOperator(
        task_id="dbt_run_silver",
        bash_command="dbt run --select silver",
    )

    dbt_gold = BashOperator(
        task_id="dbt_run_gold",
        bash_command="dbt run --select gold",
    )

    end = EmptyOperator(task_id="end")

    start >> [load_applications, load_credit_bureau]
    load_applications >> dbt_silver
    load_credit_bureau >> dbt_silver
    dbt_silver >> dbt_gold >> end
