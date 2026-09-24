import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    max,
    min
)


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)


GOLD_PATH = os.path.join(
    DATA_PATH,
    "gold",
    "provider_performance"
)


def verify_gold():

    print(
        "Starting Gold validation."
    )


    spark = (
        SparkSession.builder
        .appName(
            "VerifyGoldProviderMetrics"
        )
        .master(
            "local[*]"
        )
        .getOrCreate()
    )


    try:

        gold_df = (
            spark.read
            .parquet(
                GOLD_PATH
            )
        )


        record_count = (
            gold_df.count()
        )


        print(
            f"Gold records available: "
            f"{record_count}"
        )


        if record_count == 0:

            raise Exception(
                "Gold validation failed. "
                "No records found."
            )


        required_columns = [

            "provider_id",

            "total_claims",

            "total_billed_amount",

            "total_paid_amount",

            "denial_rate"

        ]


        missing_columns = [

            column

            for column in required_columns

            if column not in gold_df.columns

        ]


        if missing_columns:

            raise Exception(
                f"Missing Gold columns: "
                f"{missing_columns}"
            )


        denial_stats = (
            gold_df
            .select(
                min("denial_rate")
                .alias("min_denial_rate"),

                max("denial_rate")
                .alias("max_denial_rate")
            )
            .collect()[0]
        )


        if (
            denial_stats.min_denial_rate < 0
            or
            denial_stats.max_denial_rate > 100
        ):

            raise Exception(
                "Invalid denial rate detected."
            )


        print(
            "Gold validation successful."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    verify_gold()