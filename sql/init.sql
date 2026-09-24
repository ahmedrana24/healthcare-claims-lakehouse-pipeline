CREATE TABLE members (
    member_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    state VARCHAR(2),
    enrollment_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE providers (
    provider_id VARCHAR(20) PRIMARY KEY,
    provider_name VARCHAR(200),
    provider_type VARCHAR(100),
    state VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE claims (
    claim_id VARCHAR(20) PRIMARY KEY,

    member_id VARCHAR(20),
    provider_id VARCHAR(20),

    service_date DATE,

    diagnosis_code VARCHAR(20),
    procedure_code VARCHAR(20),

    billed_amount DECIMAL(12,2),
    allowed_amount DECIMAL(12,2),
    paid_amount DECIMAL(12,2),

    claim_status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (member_id)
        REFERENCES members(member_id),

    FOREIGN KEY (provider_id)
        REFERENCES providers(provider_id)
);


CREATE TABLE claim_events (
    event_id SERIAL PRIMARY KEY,

    claim_id VARCHAR(20),

    event_type VARCHAR(30),
    event_timestamp TIMESTAMP,

    claim_status VARCHAR(30),
    claim_amount DECIMAL(12,2),

    FOREIGN KEY (claim_id)
        REFERENCES claims(claim_id)
);