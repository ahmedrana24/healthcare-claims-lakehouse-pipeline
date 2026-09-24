import os
import json
import uuid
from datetime import datetime, timezone

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_URL = os.getenv(
    "HEALTHCARE_DATABASE_URL",
    "postgresql+psycopg2://healthcare_user:"
    "healthcare_password@localhost:5432/healthcare"
)

DATA_PATH = os.getenv(
    "DATA_PATH",
    "data"
)

WATERMARK_FILE = os.path.join(
    DATA_PATH,
    "metadata",
    "watermarks.json"
)

BRONZE_PATH = os.path.join(
    DATA_PATH,
    "bronze",
    "claims_incremental"
)


engine = create_engine(DATABASE_URL)


# ============================================================
# BRONZE DATA CONTRACT
# ============================================================

BRONZE_SCHEMA = pa.schema([
    pa.field("claim_id", pa.string()),
    pa.field("member_id", pa.string()),
    pa.field("provider_id", pa.string()),

    pa.field("service_date", pa.date32()),

    pa.field("diagnosis_code", pa.string()),
    pa.field("procedure_code", pa.string()),

    pa.field("billed_amount", pa.float64()),
    pa.field("allowed_amount", pa.float64()),
    pa.field("paid_amount", pa.float64()),

    pa.field("claim_status", pa.string()),

    pa.field(
        "created_at",
        pa.timestamp("us")
    ),

    pa.field(
        "updated_at",
        pa.timestamp("us")
    ),

    pa.field(
        "_source_system",
        pa.string()
    ),

    pa.field(
        "_ingestion_timestamp",
        pa.timestamp(
            "us",
            tz="UTC"
        )
    ),

    pa.field(
        "_batch_id",
        pa.string()
    )
])


# ============================================================
# WATERMARK FUNCTIONS
# ============================================================

def get_watermark():

    with open(
        WATERMARK_FILE,
        "r"
    ) as file:

        watermarks = json.load(file)

    return watermarks["claims"]


def update_watermark(
    new_watermark
):

    with open(
        WATERMARK_FILE,
        "r"
    ) as file:

        watermarks = json.load(file)

    watermarks["claims"] = str(
        new_watermark
    )

    with open(
        WATERMARK_FILE,
        "w"
    ) as file:

        json.dump(
            watermarks,
            file,
            indent=2
        )


# ============================================================
# SCHEMA STANDARDIZATION
# ============================================================

def standardize_dataframe(df):

    # Standardize strings
    string_columns = [
        "claim_id",
        "member_id",
        "provider_id",
        "diagnosis_code",
        "procedure_code",
        "claim_status"
    ]

    for column in string_columns:

        df[column] = df[column].astype(
            "string"
        )

    # Standardize service date
    df["service_date"] = pd.to_datetime(
        df["service_date"]
    ).dt.date

    # Standardize numeric columns
    numeric_columns = [
        "billed_amount",
        "allowed_amount",
        "paid_amount"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).astype("float64")

    # Explicit microsecond timestamp contract
    df["created_at"] = (
        pd.to_datetime(
            df["created_at"]
        )
        .astype("datetime64[us]")
    )

    df["updated_at"] = (
        pd.to_datetime(
            df["updated_at"]
        )
        .astype("datetime64[us]")
    )

    return df


# ============================================================
# INCREMENTAL INGESTION
# ============================================================

def ingest_incremental_claims():

    last_watermark = get_watermark()

    print(
        f"Previous watermark: "
        f"{last_watermark}"
    )

    query = text("""
        SELECT *
        FROM claims
        WHERE updated_at > :watermark
        ORDER BY updated_at
    """)

    df = pd.read_sql(
        query,
        engine,
        params={
            "watermark": last_watermark
        }
    )

    if df.empty:

        print(
            "No new or updated claims."
        )

        return

    print(
        f"Changed records found: "
        f"{len(df)}"
    )

    # Capture watermark BEFORE adding
    # operational metadata
    new_watermark = (
        df["updated_at"].max()
    )

    # --------------------------------------------------------
    # STANDARDIZE SOURCE DATA
    # --------------------------------------------------------

    df = standardize_dataframe(df)

    # --------------------------------------------------------
    # ADD INGESTION METADATA
    # --------------------------------------------------------

    df["_source_system"] = (
        "healthcare_postgres"
    )

    df["_ingestion_timestamp"] = (
        datetime.now(timezone.utc)
    )

    df["_batch_id"] = str(
        uuid.uuid4()
    )

    # --------------------------------------------------------
    # CREATE BRONZE DIRECTORY
    # --------------------------------------------------------

    os.makedirs(
        BRONZE_PATH,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = os.path.join(
        BRONZE_PATH,
        f"claims_incremental_{timestamp}.parquet"
    )

    # --------------------------------------------------------
    # ENFORCE PARQUET SCHEMA
    # --------------------------------------------------------

    arrow_table = (
        pa.Table.from_pandas(
            df,
            schema=BRONZE_SCHEMA,
            preserve_index=False,
            safe=True
        )
    )

    # --------------------------------------------------------
    # WRITE BRONZE
    # --------------------------------------------------------

    pq.write_table(
        arrow_table,
        output_file
    )

    print(
        f"Bronze file created: "
        f"{output_file}"
    )

    # --------------------------------------------------------
    # UPDATE WATERMARK ONLY AFTER SUCCESSFUL WRITE
    # --------------------------------------------------------

    update_watermark(
        new_watermark
    )

    print(
        f"New watermark: "
        f"{new_watermark}"
    )


# ============================================================
# LOCAL EXECUTION
# ============================================================

if __name__ == "__main__":

    ingest_incremental_claims()