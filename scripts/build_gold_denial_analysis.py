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
    "claim_denial_analysis"
)



def build_denial_analysis():

    print(
        "Starting Gold denial analysis."
    )


    spark = (
        SparkSession.builder
        .appName(
            "GoldClaimDenialAnalysis"
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


        denial_df = (

            silver_df

            .groupBy(
                "claim_status"
            )

            .agg(

                count(
                    "claim_id"
                )
                .alias(
                    "total_claims"
                ),


                sum(
                    when(
                        col("claim_status") == "DENIED",
                        1
                    )
                    .otherwise(0)
                )
                .alias(
                    "denied_claims"
                ),


                sum(
                    "billed_amount"
                )
                .alias(
                    "total_billed_amount"
                ),


                sum(
                    when(
                        col("claim_status") == "DENIED",
                        col("billed_amount")
                    )
                    .otherwise(0)
                )
                .alias(
                    "denied_billed_amount"
                )

            )

        )


        denial_df = (

            denial_df

            .withColumn(

                "denial_rate",

                round(

                    col("denied_claims")
                    /
                    col("total_claims")
                    *
                    100,

                    2

                )

            )


            .withColumn(

                "financial_impact",

                col(
                    "denied_billed_amount"
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
            denial_df
            .write
            .mode(
                "overwrite"
            )
            .parquet(
                GOLD_PATH
            )
        )


        print(
            "Gold denial analysis created."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    build_denial_analysis()