# 🏥 Healthcare Claims Lakehouse Pipeline

A production-style **Healthcare Claims Lakehouse Analytics Platform** built using modern data engineering practices. This project demonstrates an end-to-end healthcare data pipeline that ingests claims data, applies **Medallion Lakehouse Architecture**, performs automated data quality validation, creates business-ready Gold analytics datasets, and delivers analytics through an interactive **Streamlit dashboard**.

---

# 📊 Streamlit Analytics Dashboard

The Gold analytics layer powers an interactive **Streamlit healthcare analytics dashboard**.

The dashboard provides:

- Executive Claims Overview
- Claim Denial Analytics
- Provider Performance Analysis
- Member Utilization Analytics

Dashboard capabilities include:

- Executive KPI monitoring
- Claims volume analysis
- Financial impact analysis
- Provider benchmarking
- Denial analysis
- Member utilization insights
- Gold layer analytics exploration

Dashboard screenshots are available under:

```
docs/screenshots/
```

Run the dashboard locally:

```bash
streamlit run dashboard/app.py
```

---

# 🏗️ Architecture

The platform follows a **Medallion Lakehouse Architecture**:

```
Healthcare Source Systems
            |
            v
PostgreSQL Claims Database
            |
            v
Apache Airflow Orchestration
            |
            v
PySpark Processing
            |
            v
Bronze Layer
(Raw Claims Data)
            |
            v
Silver Layer
(Cleansed & Validated Data)
            |
            v
Gold Layer
(Business Analytics Products)
            |
            v
Streamlit Dashboard
```

Complete architecture diagram:

```
docs/architecture.png
```

---

# 🔄 Pipeline Overview

## Source Systems

Healthcare claims data is generated from operational healthcare systems:

- Claims Processing System
- Member Eligibility System
- Provider Management System
- Healthcare Event System

Source data is stored in a PostgreSQL healthcare claims database.

---

# 🥉 Bronze Layer — Raw Data Storage

The Bronze layer stores raw healthcare claims data after ingestion.

Responsibilities:

- Raw claims ingestion
- Source metadata tracking
- Batch identification
- Ingestion timestamp tracking
- Historical data preservation

Storage format:

- Apache Parquet

---

# 🥈 Silver Layer — Trusted Data Processing

The Silver layer creates trusted analytical datasets using PySpark transformations.

Processing includes:

- Schema standardization
- Data cleansing
- Duplicate handling
- Business rule validation
- Data transformation
- Data quality checks

Invalid records are routed to quarantine storage.

---

# 🥇 Gold Layer — Business Analytics Products

The Gold layer contains curated datasets optimized for analytics consumption.

## Provider Performance Analytics

Dataset:

```
gold/provider_performance
```

Provides:

- Provider claim volume
- Total billed amount
- Total paid amount
- Denied claims
- Denial rates


---

## Claim Denial Analytics

Dataset:

```
gold/claim_denial_analysis
```

Provides:

- Claim status analysis
- Denied claims
- Denial percentage
- Financial impact analysis


---

## Member Utilization Analytics

Dataset:

```
gold/member_utilization
```

Provides:

- Member claim volume
- Total billed amount
- Total paid amount
- Average claim cost
- Service history

---

# ✅ Data Quality Framework

The pipeline uses **Great Expectations** for automated data validation.

Validation checkpoints are implemented throughout the pipeline.

## Pre-Bronze Validation

Validates incoming claims data before writing into Bronze.

Checks include:

- Schema validation
- Required field validation
- Data consistency checks
- Data quality expectations

Failed records are routed to:

```
Quarantine Storage
```

---

## Silver Validation

Validates transformed Silver datasets before promotion into Gold.

Checks include:

- Completeness validation
- Transformation accuracy
- Business rule validation
- Data consistency checks

---

# ⚙️ Technology Stack

## Data Engineering

- Python
- PySpark
- Apache Airflow
- PostgreSQL
- Apache Parquet

## Data Quality

- Great Expectations

## Analytics

- Streamlit
- Plotly
- Pandas

## DevOps

- Docker
- GitHub
- GitHub Actions

---

# 🚀 Running the Project

## Clone Repository

```bash
git clone <repository-url>

cd healthcare-claims-pipeline
```

---

## Install Dependencies

```bash
pip install -r dashboard/requirements.txt
```

---

## Start Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard will be available at:

```
http://localhost:8501
```

---

# 📂 Project Structure

```
healthcare-claims-pipeline/

├── dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── architecture.png
│   └── screenshots/
│
├── dags/
│
├── scripts/
│
├── sql/
│
├── tests/
│
├── docker-compose.yml
│
├── README.md
```

---

# 🔁 CI/CD

GitHub Actions provides automated validation for:

- Python scripts
- Airflow DAG validation
- Automated testing
- Code quality checks

---

# 🔐 Engineering Controls

Implemented engineering controls:

- Automated data quality validation
- Pipeline metadata tracking
- Batch tracking
- Version control
- Quarantine handling
- Layer-based data validation
- Reproducible data processing

---

# 📈 Business Value

This platform enables healthcare organizations to:

- Identify claim denial patterns
- Monitor provider performance
- Analyze financial impact
- Understand member utilization behavior
- Provide trusted analytics for business decisions

---

# 👨‍💻 Healthcare Claims Lakehouse Analytics Platform

Built using modern data engineering practices, lakehouse architecture patterns, and analytics engineering principles.