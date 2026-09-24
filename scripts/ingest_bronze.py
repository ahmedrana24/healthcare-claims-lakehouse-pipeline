import os
import uuid
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg2://"
    "healthcare_user:healthcare_password"
    "@localhost:5432/healthcare"
)

engine = create_engine(DATABASE_URL)

BRONZE_PATH = "data/bronze"

tables = [
    "members",
    "providers",
    "claims",
    "claim_events"
]


def ingest_table(table_name):

    print(f"Starting ingestion: {table_name}")

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, engine)

    # Pipeline metadata
    df["_source_system"] = "healthcare_postgres"

    df["_ingestion_timestamp"] = datetime.now(timezone.utc)

    df["_batch_id"] = str(uuid.uuid4())

    # Create Bronze directory
    output_directory = os.path.join(
        BRONZE_PATH,
        table_name
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = os.path.join(
        output_directory,
        f"{table_name}_{timestamp}.parquet"
    )

    df.to_parquet(
        output_file,
        index=False
    )

    print(
        f"{table_name}: "
        f"{len(df)} records written to {output_file}"
    )


def main():

    for table in tables:
        ingest_table(table)


if __name__ == "__main__":
    main()