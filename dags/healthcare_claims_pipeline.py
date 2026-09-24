from datetime import datetime, timedelta
import glob
import os
import sys

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text


# ============================================================
# IMPORT PIPELINE COMPONENTS
# ============================================================

sys.path.insert(
    0,
    "/opt/airflow/scripts"
)


from ingest_claims_incremental import (
    ingest_incremental_claims
)

from build_silver_claims import (
    build_silver_claims
)

from verify_silver import (
    verify_silver
)

from build_gold_provider_metrics import (
    build_provider_metrics
)

from build_gold_denial_analysis import (
    build_denial_analysis
)

from build_gold_member_utilization import (
    build_member_utilization
)

from verify_provider_gold import (
    verify_provider_gold
)

from verify_denial_gold import (
    verify_denial_gold
)

from verify_member_gold import (
    verify_member_gold
)


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_URL = os.environ[
    "HEALTHCARE_DATABASE_URL"
]


DATA_PATH = os.getenv(
    "DATA_PATH",
    "/opt/airflow/data"
)


# ============================================================
# DEFAULT SETTINGS
# ============================================================

default_args = {

    "owner": "healthcare-data-engineering",

    "retries": 2,

    "retry_delay": timedelta(
        minutes=1
    )

}


# ============================================================
# TASK FUNCTIONS
# ============================================================

def check_source():

    engine = create_engine(
        DATABASE_URL
    )


    with engine.connect() as connection:

        result = connection.execute(
            text(
                "SELECT COUNT(*) FROM claims"
            )
        )

        count = result.scalar()


    print(
        f"Source connection successful. "
        f"Claims available: {count}"
    )



def run_incremental_ingestion():

    ingest_incremental_claims()



def verify_bronze():

    files = glob.glob(
        os.path.join(
            DATA_PATH,
            "bronze",
            "claims_incremental",
            "*.parquet"
        )
    )


    if not files:

        raise Exception(
            "Bronze validation failed. "
            "No parquet files found."
        )


    print(
        f"Bronze validation successful. "
        f"Files found: {len(files)}"
    )



def run_silver():

    build_silver_claims()



def run_verify_silver():

    verify_silver()



def run_provider_gold():

    build_provider_metrics()



def run_denial_gold():

    build_denial_analysis()



def run_member_gold():

    build_member_utilization()



def run_verify_provider_gold():

    verify_provider_gold()



def run_verify_denial_gold():

    verify_denial_gold()



def run_verify_member_gold():

    verify_member_gold()



# ============================================================
# DAG DEFINITION
# ============================================================

with DAG(

    dag_id="healthcare_claims_pipeline",

    description=(
        "Healthcare Claims Lakehouse "
        "Bronze Silver Gold ELT Pipeline"
    ),

    default_args=default_args,

    start_date=datetime(
        2026,
        9,
        1
    ),

    schedule="0 * * * *",

    catchup=False,

    tags=[
        "healthcare",
        "claims",
        "spark",
        "lakehouse"
    ]

) as dag:


    start = EmptyOperator(
        task_id="start"
    )


    check_source_task = PythonOperator(
        task_id="check_source",
        python_callable=check_source
    )


    ingest_task = PythonOperator(
        task_id="ingest_claims_incremental",
        python_callable=run_incremental_ingestion
    )


    bronze_task = PythonOperator(
        task_id="verify_bronze",
        python_callable=verify_bronze
    )


    silver_task = PythonOperator(
        task_id="build_silver_claims",
        python_callable=run_silver
    )


    silver_validation_task = PythonOperator(
        task_id="verify_silver",
        python_callable=run_verify_silver
    )


    # ========================================================
    # GOLD BUILD TASKS
    # ========================================================

    provider_gold_task = PythonOperator(
        task_id="build_gold_provider_metrics",
        python_callable=run_provider_gold
    )


    denial_gold_task = PythonOperator(
        task_id="build_gold_denial_analysis",
        python_callable=run_denial_gold
    )


    member_gold_task = PythonOperator(
        task_id="build_gold_member_utilization",
        python_callable=run_member_gold
    )


    # ========================================================
    # GOLD VALIDATION TASKS
    # ========================================================

    provider_validation_task = PythonOperator(
        task_id="verify_provider_gold",
        python_callable=run_verify_provider_gold
    )


    denial_validation_task = PythonOperator(
        task_id="verify_denial_gold",
        python_callable=run_verify_denial_gold
    )


    member_validation_task = PythonOperator(
        task_id="verify_member_gold",
        python_callable=run_verify_member_gold
    )


    end = EmptyOperator(
        task_id="end"
    )


    # ========================================================
    # PIPELINE DEPENDENCIES
    # ========================================================


    (
        start
        >> check_source_task
        >> ingest_task
        >> bronze_task
        >> silver_task
        >> silver_validation_task
    )


    # Silver produces three independent Gold products

    silver_validation_task >> [
        provider_gold_task,
        denial_gold_task,
        member_gold_task
    ]


    # Each Gold product has its own validation

    provider_gold_task >> provider_validation_task

    denial_gold_task >> denial_validation_task

    member_gold_task >> member_validation_task


    # Pipeline finishes only after all Gold validations pass

    [
        provider_validation_task,
        denial_validation_task,
        member_validation_task
    ] >> end