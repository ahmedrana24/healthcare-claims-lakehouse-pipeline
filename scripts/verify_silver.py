import os
import glob

from pyspark.sql import SparkSession


DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)


SILVER_PATH = os.path.join(
    DATA_PATH,
    "silver",
    "claims"
)


def verify_silver():

    print("Starting Silver validation.")

    spark = (
        SparkSession.builder
        .appName("VerifySilverClaims")
        .master("local[*]")
        .getOrCreate()
    )

    try:

        files = glob.glob(
            os.path.join(
                SILVER_PATH,
                "*.parquet"
            )
        )

        if not files:

            raise Exception(
                "Silver validation failed. "
                "No Silver parquet files found."
            )


        silver_df = (
            spark.read
            .parquet(SILVER_PATH)
        )


        record_count = silver_df.count()


        print(
            f"Silver records available: "
            f"{record_count}"
        )


        if record_count == 0:

            raise Exception(
                "Silver validation failed. "
                "Silver layer contains zero records."
            )


        required_columns = [
            "claim_id",
            "member_id",
            "provider_id",
            "claim_status",
            "paid_amount"
        ]


        missing_columns = [
            column
            for column in required_columns
            if column not in silver_df.columns
        ]


        if missing_columns:

            raise Exception(
                f"Missing Silver columns: "
                f"{missing_columns}"
            )


        print(
            "Silver validation successful."
        )


    finally:

        spark.stop()



if __name__ == "__main__":

    verify_silver()