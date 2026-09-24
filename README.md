# Healthcare Claims Lakehouse Pipeline

An end-to-end healthcare claims data engineering platform built using **Apache Airflow, PostgreSQL, PySpark, Docker, and a Bronze-Silver-Gold Lakehouse architecture**.

This project demonstrates how healthcare claims data can be ingested incrementally, validated, transformed, and delivered as business-ready analytics datasets using modern data engineering practices.

---

# Business Problem

Healthcare organizations process large volumes of claims data from multiple operational systems. Traditional batch processing approaches create challenges around:

- Processing continuously changing claims data
- Avoiding expensive full data reloads
- Maintaining data quality and trust
- Identifying reimbursement issues
- Creating analytics-ready datasets for business teams

This project solves these challenges by implementing an automated healthcare claims ELT platform with incremental processing, quality validation, and business analytics layers.

---

# Solution Overview

The platform follows a modern **Medallion Architecture**:

```
Healthcare Claims Source
          |
          ↓
     PostgreSQL Database
          |
          ↓
     Apache Airflow
    Orchestration Layer
          |
          ↓
      Bronze Layer
 Raw Claims + Metadata Storage
          |
          ↓
      Silver Layer
 Cleaning + Validation + Quality Rules
          |
          ↓
       Gold Layer
 Business Analytics Data Products
```

---

# Technology Stack

## Data Engineering

- Python
- SQL
- PySpark
- PostgreSQL
- Apache Airflow
- Parquet

## Platform & DevOps

- Docker
- Docker Compose
- GitHub Actions
- Git

## Architecture Patterns

- Medallion Architecture
- Incremental Data Processing
- Data Quality Framework
- ELT Pipeline Design
- Layered Data Architecture

---

# Architecture Flow

```
                Healthcare Claims System

                         |
                         ↓

                 PostgreSQL Database

                         |
                         ↓

                 Airflow Orchestrator

                         |
                         ↓

                    Bronze Layer

        Raw Claims + Source Metadata + Batch Tracking

                         |
                         ↓

                    Silver Layer

      Standardization + Validation + Deduplication
                + Quarantine Handling

                         |
                         ↓

                     Gold Layer

        ---------------------------------
        |               |               |
        ↓               ↓               ↓

 Provider Metrics   Denial Analysis   Member Utilization

        ---------------------------------

                         |
                         ↓

              Analytics / Reporting Layer
```

---

# Pipeline Components

## 1. Source Layer

The pipeline starts with a healthcare claims database containing:

- Members
- Providers
- Claims
- Claim Events

PostgreSQL acts as the operational source system.

Example entities:

```
members

providers

claims

claim_events
```

---

# 2. Incremental Claims Processing (CDC Pattern)

Instead of processing the entire claims table every time, the pipeline uses a watermark-based incremental processing strategy.

Process:

```
Previous Watermark Timestamp

            ↓

Identify New / Updated Claims

            ↓

Process Only Changed Records

            ↓

Update Watermark
```

Logic:

```sql
SELECT *
FROM claims
WHERE updated_at > previous_watermark;
```

Benefits:

- Reduced processing time
- Lower compute cost
- Supports continuously changing healthcare data
- Prevents unnecessary full refreshes

---

# 3. Bronze Layer

The Bronze layer stores raw ingested data.

Purpose:

- Preserve source-level information
- Maintain historical ingestion records
- Support replay and troubleshooting

Bronze includes operational metadata:

```
_source_system

_ingestion_timestamp

_batch_id
```

Example:

```
data/
 └── bronze/
      └── claims_incremental/
```

---

# 4. Silver Layer

The Silver layer creates trusted analytical datasets.

Transformations include:

- Schema standardization
- Data cleansing
- Data validation
- Duplicate handling
- Business rule enforcement

Invalid records are separated into quarantine storage.

Example:

```
Silver Claims

        |
        |
        +---- Valid Records
        |
        +---- Quarantine Records
```

Quality checks:

- Required field validation
- Claim amount validation
- Duplicate detection
- Schema validation

---

# 5. Gold Analytics Layer

The Gold layer contains business-ready datasets designed for analytics consumption.

Three business data products were created.

---

## Provider Performance Analytics

Business Question:

> How are healthcare providers performing?

Dataset:

```
gold/provider_performance
```

Metrics:

- Total claims
- Total billed amount
- Total paid amount
- Denied claims
- Denial rate

Used by:

- Provider operations
- Network management
- Financial teams

---

## Claim Denial Analytics

Business Question:

> Where are reimbursement losses occurring?

Dataset:

```
gold/claim_denial_analysis
```

Metrics:

- Total claims
- Denied claims
- Denial percentage
- Financial impact
- Denied billed amount

Used by:

- Revenue cycle teams
- Claims operations
- Finance teams

---

## Member Utilization Analytics

Business Question:

> How are members utilizing healthcare services?

Dataset:

```
gold/member_utilization
```

Metrics:

- Total claims per member
- Total healthcare cost
- Average claim cost
- First service date
- Last service date

Used by:

- Care management teams
- Population health analytics
- Cost management teams

---

# Airflow Orchestration

The entire pipeline is automated using Apache Airflow.

Workflow:

```
START

  ↓

Source Validation

  ↓

Incremental Claims Ingestion

  ↓

Bronze Validation

  ↓

Silver Transformation

  ↓

Silver Validation

  ↓

Parallel Gold Processing

  ↓

Gold Quality Validation

  ↓

END
```

---

# Parallel Gold Processing

After Silver validation, Gold datasets run independently:

```
                 Silver Layer

                       |

        ---------------------------------

        |               |              |

        ↓               ↓              ↓

 Provider Gold    Denial Gold    Member Gold

        ↓               ↓              ↓

 Provider       Denial          Member
 Validation     Validation      Validation

        ---------------------------------

                       |

                       ↓

                      END
```

Benefits:

- Faster execution
- Independent business datasets
- Better failure isolation

---

# Data Quality Framework

The pipeline implements validation checkpoints.

## Bronze Validation

Checks:

- Data files exist
- Ingestion completed successfully

---

## Silver Validation

Checks:

- Required columns exist
- Records are available
- Data transformation completed successfully

---

## Gold Validation

Each business dataset has dedicated validation.

### Provider Validation

Checks:

- Provider ID availability
- Denial rate range
- Required metrics

### Denial Validation

Checks:

- Financial impact values
- Denial percentage
- Required denial metrics

### Member Validation

Checks:

- Member identifiers
- Claim cost validation
- Utilization metrics

---

# Project Structure

```
healthcare-claims-pipeline/

├── .github/
│   └── workflows/
│       └── pipeline-test.yml

├── dags/
│   └── healthcare_claims_pipeline.py

├── scripts/
│
│   ├── generate_data.py
│   ├── ingest_claims_incremental.py
│   ├── build_silver_claims.py
│   │
│   ├── build_gold_provider_metrics.py
│   ├── build_gold_denial_analysis.py
│   ├── build_gold_member_utilization.py
│   │
│   ├── verify_silver.py
│   ├── verify_provider_gold.py
│   ├── verify_denial_gold.py
│   └── verify_member_gold.py
│
├── sql/
│   └── init.sql
│
├── docker-compose.yml
│
├── Dockerfile.airflow
│
├── README.md
│
└── .gitignore
```

---

# Local Setup

## Clone Repository

```bash
git clone <repository-url>

cd healthcare-claims-pipeline
```

---

## Start Environment

```bash
docker compose up -d
```

---

## Access Airflow

Open:

```
http://localhost:8081
```

---

## Run Pipeline

Trigger:

```
healthcare_claims_pipeline
```

The DAG will execute:

```
PostgreSQL
     |
     ↓
Bronze
     |
     ↓
Silver
     |
     ↓
Gold Analytics
     |
     ↓
Validation Complete
```

---

# CI/CD Pipeline

GitHub Actions validates the project automatically.

Workflow:

```
Developer Push

      |

GitHub Actions

      |

Install Dependencies

      |

Validate DAG Syntax

      |

Validate Python Scripts

      |

Pipeline Approved
```

---

# Engineering Challenges Solved

## Incremental Processing

Implemented watermark-based loading to process only changed healthcare claims instead of performing expensive full reloads.

---

## Schema Drift Handling

Identified and resolved Parquet schema inconsistencies by enforcing consistent data types across ingestion batches.

---

## Data Quality Management

Implemented validation gates between Bronze, Silver, and Gold layers to prevent unreliable data from reaching analytics.

---

## Pipeline Reliability

Designed Airflow dependencies with validation checkpoints and parallel Gold processing for better scalability and fault isolation.

---

# Future Enhancements

Planned improvements:

- Deploy pipeline on AWS / Azure cloud platforms
- Add Terraform infrastructure automation
- Add Power BI dashboards
- Add centralized monitoring and alerting
- Integrate data catalog and governance tools
- Add automated data quality framework using Great Expectations

---

# Skills Demonstrated

- Healthcare Data Engineering
- Apache Airflow
- PySpark
- PostgreSQL
- Incremental Data Processing
- Medallion Architecture
- Data Quality Engineering
- ELT Pipeline Development
- Data Modeling
- Workflow Orchestration
- CI/CD Practices

---

# Author

Healthcare Claims Lakehouse Engineering Project
by Rana Ahmed

Built using modern data engineering architecture patterns.