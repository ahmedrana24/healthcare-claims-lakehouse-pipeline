import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    min,
    max
)


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)


GOLD_PATH = os.path.join(
    DATA_PATH,
    "gold",
    "claim_denial_analysis"
)


def verify_denial_gold():

    print(
        "Starting Denial Gold validation."
    )


    spark = (
        SparkSession.builder
        .appName(
            "VerifyDenialGold"
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
            f"Denial Gold records: {count}"
        )


        if count == 0:

            raise Exception(
                "Denial Gold is empty."
            )


        required_columns = [

            "claim_status",

            "total_claims",

            "denied_claims",

            "denial_rate",

            "financial_impact"

        ]


        missing = [

            c for c in required_columns

            if c not in df.columns

        ]


        if missing:

            raise Exception(
                f"Missing columns: {missing}"
            )


        invalid_amounts = (
            df.filter(
                col("financial_impact") < 0
            )
            .count()
        )


        if invalid_amounts > 0:

            raise Exception(
                "Negative financial impact detected."
            )


        denial_range = (
            df.select(
                min("denial_rate"),
                max("denial_rate")
            )
            .collect()[0]
        )


        if (
            denial_range[0] < 0
            or
            denial_range[1] > 100
        ):

            raise Exception(
                "Invalid denial rate detected."
            )


        print(
            "Denial Gold validation successful."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    verify_denial_gold()