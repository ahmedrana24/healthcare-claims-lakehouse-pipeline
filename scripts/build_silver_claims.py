import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    current_timestamp,
    row_number,
    trim,
    upper,
)
from pyspark.sql.window import Window


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)

BRONZE_PATH = os.path.join(
    DATA_PATH,
    "bronze",
    "claims_incremental"
)

SILVER_PATH = os.path.join(
    DATA_PATH,
    "silver",
    "claims"
)

QUARANTINE_PATH = os.path.join(
    DATA_PATH,
    "quarantine",
    "claims"
)


def build_silver_claims():

    print("Starting Silver claims transformation.")

    spark = (
        SparkSession.builder
        .appName("HealthcareSilverClaims")
        .master("local[*]")
        .getOrCreate()
    )

    try:

        # ------------------------------------------------------
        # READ BRONZE
        # ------------------------------------------------------

        bronze_df = (
            spark.read
            .parquet(BRONZE_PATH)
        )

        print(
            f"Bronze records read: "
            f"{bronze_df.count()}"
        )

        # ------------------------------------------------------
        # STANDARDIZATION
        # ------------------------------------------------------

        standardized_df = (
            bronze_df
            .withColumn(
                "claim_status",
                upper(trim(col("claim_status")))
            )
            .withColumn(
                "diagnosis_code",
                upper(trim(col("diagnosis_code")))
            )
        )

        # ------------------------------------------------------
        # DATA QUALITY RULES
        # ------------------------------------------------------

        valid_condition = (
            col("claim_id").isNotNull()
            & col("member_id").isNotNull()
            & col("provider_id").isNotNull()
            & col("diagnosis_code").isNotNull()
            & col("billed_amount").isNotNull()
            & (col("billed_amount") >= 0)
            & (
                col("paid_amount").isNotNull()
                | (col("claim_status") == "DENIED")
            )
        )

        valid_df = standardized_df.filter(
            valid_condition
        )

        invalid_df = standardized_df.filter(
            ~valid_condition
        )

        invalid_count = invalid_df.count()

        print(
            f"Invalid records found: "
            f"{invalid_count}"
        )

        # ------------------------------------------------------
        # QUARANTINE BAD RECORDS
        # ------------------------------------------------------

        if invalid_count > 0:

            (
                invalid_df
                .withColumn(
                    "_quarantine_timestamp",
                    current_timestamp()
                )
                .write
                .mode("overwrite")
                .parquet(QUARANTINE_PATH)
            )

            print(
                f"Invalid records written to "
                f"{QUARANTINE_PATH}"
            )

        # ------------------------------------------------------
        # DEDUPLICATION / LATEST VERSION
        # ------------------------------------------------------

        window = (
            Window
            .partitionBy("claim_id")
            .orderBy(
                col("updated_at").desc(),
                col("_ingestion_timestamp").desc()
            )
        )

        silver_df = (
            valid_df
            .withColumn(
                "_row_number",
                row_number().over(window)
            )
            .filter(
                col("_row_number") == 1
            )
            .drop("_row_number")
            .withColumn(
                "_silver_processed_timestamp",
                current_timestamp()
            )
        )

        silver_count = silver_df.count()

        print(
            f"Silver records produced: "
            f"{silver_count}"
        )

        # ------------------------------------------------------
        # WRITE SILVER
        # ------------------------------------------------------

        (
            silver_df
            .write
            .mode("overwrite")
            .parquet(SILVER_PATH)
        )

        print(
            f"Silver claims successfully written to "
            f"{SILVER_PATH}"
        )

    finally:

        spark.stop()


if __name__ == "__main__":
    build_silver_claims()