import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)


GOLD_PATH = os.path.join(
    DATA_PATH,
    "gold",
    "member_utilization"
)


def verify_member_gold():

    print(
        "Starting Member Gold validation."
    )


    spark = (
        SparkSession.builder
        .appName(
            "VerifyMemberGold"
        )
        .master(
            "local[*]"
        )
        .getOrCreate()
    )


    try:

        df = (
            spark.read
            .parquet(
                GOLD_PATH
            )
        )


        count = df.count()


        print(
            f"Member Gold records: {count}"
        )


        if count == 0:

            raise Exception(
                "Member Gold is empty."
            )


        required_columns = [

            "member_id",

            "total_claims",

            "total_paid_amount",

            "average_claim_cost"

        ]


        missing = [

            c for c in required_columns

            if c not in df.columns

        ]


        if missing:

            raise Exception(
                f"Missing columns: {missing}"
            )


        null_members = (
            df.filter(
                col("member_id").isNull()
            )
            .count()
        )


        if null_members > 0:

            raise Exception(
                "Null member_id detected."
            )


        negative_costs = (
            df.filter(
                col("average_claim_cost") < 0
            )
            .count()
        )


        if negative_costs > 0:

            raise Exception(
                "Negative claim cost detected."
            )


        print(
            "Member Gold validation successful."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    verify_member_gold()