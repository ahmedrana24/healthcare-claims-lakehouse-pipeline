import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    when,
    round,
    current_timestamp
)


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)


SILVER_PATH = os.path.join(
    DATA_PATH,
    "silver",
    "claims"
)


GOLD_PATH = os.path.join(
    DATA_PATH,
    "gold",
    "provider_performance"
)



def build_provider_metrics():

    print(
        "Starting Gold provider metrics."
    )


    spark = (
        SparkSession.builder
        .appName(
            "GoldProviderMetrics"
        )
        .master(
            "local[*]"
        )
        .getOrCreate()
    )


    try:

        silver_df = (
            spark.read
            .parquet(
                SILVER_PATH
            )
        )


        print(
            f"Silver records read: "
            f"{silver_df.count()}"
        )


        gold_df = (

            silver_df

            .groupBy(
                "provider_id"
            )

            .agg(

                count(
                    "claim_id"
                )
                .alias(
                    "total_claims"
                ),


                sum(
                    "billed_amount"
                )
                .alias(
                    "total_billed_amount"
                ),


                sum(
                    "paid_amount"
                )
                .alias(
                    "total_paid_amount"
                ),


                sum(
                    when(
                        col(
                            "claim_status"
                        ) == "DENIED",
                        1
                    )
                    .otherwise(0)
                )
                .alias(
                    "denied_claims"
                )

            )

        )


        gold_df = (

            gold_df

            .withColumn(

                "denial_rate",

                round(

                    col(
                        "denied_claims"
                    )
                    /
                    col(
                        "total_claims"
                    )
                    *
                    100,

                    2

                )

            )

            .withColumn(

                "gold_processed_timestamp",

                current_timestamp()

            )

        )


        os.makedirs(
            GOLD_PATH,
            exist_ok=True
        )


        (
            gold_df
            .write
            .mode(
                "overwrite"
            )
            .parquet(
                GOLD_PATH
            )
        )


        print(
            "Gold provider metrics created."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    build_provider_metrics()