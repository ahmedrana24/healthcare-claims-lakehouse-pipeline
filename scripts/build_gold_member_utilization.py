import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    sum,
    avg,
    min,
    max,
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
    "member_utilization"
)



def build_member_utilization():

    print(
        "Starting Gold member utilization."
    )


    spark = (
        SparkSession.builder
        .appName(
            "GoldMemberUtilization"
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


        utilization_df = (

            silver_df

            .groupBy(
                "member_id"
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


                avg(
                    "paid_amount"
                )
                .alias(
                    "average_claim_cost"
                ),


                min(
                    "service_date"
                )
                .alias(
                    "first_service_date"
                ),


                max(
                    "service_date"
                )
                .alias(
                    "last_service_date"
                )

            )

        )


        utilization_df = (

            utilization_df

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
            utilization_df
            .write
            .mode(
                "overwrite"
            )
            .parquet(
                GOLD_PATH
            )
        )


        print(
            "Gold member utilization created."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    build_member_utilization()