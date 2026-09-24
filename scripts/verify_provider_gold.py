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


def verify_provider_gold():

    print(
        "Starting Provider Gold validation."
    )


    spark = (
        SparkSession.builder
        .appName(
            "VerifyProviderGold"
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
            f"Provider Gold records: {count}"
        )


        if count == 0:
            raise Exception(
                "Provider Gold is empty."
            )


        required_columns = [
            "provider_id",
            "total_claims",
            "denial_rate"
        ]


        missing = [
            c for c in required_columns
            if c not in df.columns
        ]


        if missing:
            raise Exception(
                f"Missing columns: {missing}"
            )


        if df.filter(
            col("provider_id").isNull()
        ).count() > 0:

            raise Exception(
                "Null provider_id found."
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
                "Invalid denial rate."
            )


        print(
            "Provider Gold validation successful."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    verify_provider_gold()