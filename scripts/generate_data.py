import random
from datetime import timedelta
from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="healthcare",
    user="healthcare_user",
    password="healthcare_password"
)

cursor = conn.cursor()

# -------------------------
# 1. MEMBERS
# -------------------------

for i in range(1, 1001):

    member_id = f"M{i:05d}"

    cursor.execute("""
        INSERT INTO members (
            member_id,
            first_name,
            last_name,
            date_of_birth,
            state,
            enrollment_status
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (member_id) DO NOTHING
    """, (
        member_id,
        fake.first_name(),
        fake.last_name(),
        fake.date_of_birth(minimum_age=18, maximum_age=90),
        random.choice(["OH", "TX", "CA", "FL", "NY"]),
        random.choice(["ACTIVE", "ACTIVE", "ACTIVE", "INACTIVE"])
    ))


# -------------------------
# 2. PROVIDERS
# -------------------------

for i in range(1, 101):

    provider_id = f"P{i:04d}"

    cursor.execute("""
        INSERT INTO providers (
            provider_id,
            provider_name,
            provider_type,
            state
        )
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (provider_id) DO NOTHING
    """, (
        provider_id,
        fake.company(),
        random.choice([
            "Hospital",
            "Primary Care",
            "Cardiology",
            "Orthopedics",
            "Emergency"
        ]),
        random.choice(["OH", "TX", "CA", "FL", "NY"])
    ))


# -------------------------
# 3. CLAIMS
# -------------------------

diagnosis_codes = [
    "E11.9",
    "I10",
    "J45.909",
    "M54.50",
    "E78.5"
]

procedure_codes = [
    "99213",
    "99214",
    "93000",
    "80053",
    "71046"
]

statuses = [
    "SUBMITTED",
    "APPROVED",
    "PAID",
    "DENIED"
]

for i in range(1, 10001):

    claim_id = f"C{i:07d}"

    member_id = f"M{random.randint(1,1000):05d}"
    provider_id = f"P{random.randint(1,100):04d}"

    billed = round(random.uniform(100, 10000), 2)
    allowed = round(billed * random.uniform(0.6, 0.9), 2)

    status = random.choice(statuses)

    paid = 0 if status == "DENIED" else round(
        allowed * random.uniform(0.7, 1.0), 2
    )

    service_date = fake.date_between(
        start_date="-1y",
        end_date="today"
    )

    cursor.execute("""
        INSERT INTO claims (
            claim_id,
            member_id,
            provider_id,
            service_date,
            diagnosis_code,
            procedure_code,
            billed_amount,
            allowed_amount,
            paid_amount,
            claim_status
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (claim_id) DO NOTHING
    """, (
        claim_id,
        member_id,
        provider_id,
        service_date,
        random.choice(diagnosis_codes),
        random.choice(procedure_codes),
        billed,
        allowed,
        paid,
        status
    ))


# -------------------------
# 4. CLAIM EVENTS
# -------------------------

for i in range(1, 10001):

    claim_id = f"C{i:07d}"

    cursor.execute("""
        SELECT created_at, allowed_amount
        FROM claims
        WHERE claim_id = %s
    """, (claim_id,))

    result = cursor.fetchone()

    if not result:
        continue

    created_at, amount = result

    events = [
        ("SUBMITTED", 0),
        ("PROCESSED", 1),
        ("APPROVED", 2)
    ]

    for event_type, hours in events:

        cursor.execute("""
            INSERT INTO claim_events (
                claim_id,
                event_type,
                event_timestamp,
                claim_status,
                claim_amount
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (
            claim_id,
            event_type,
            created_at + timedelta(hours=hours),
            event_type,
            amount
        ))


conn.commit()

cursor.close()
conn.close()

print("Healthcare synthetic data generated successfully.")