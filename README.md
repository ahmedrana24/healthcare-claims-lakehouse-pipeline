You're right — let's fix it properly. The issue was likely formatting corruption. Use this **clean README from the first line**. Copy the entire block and replace your `README.md`.

```markdown
# 🏥 Healthcare Claims Lakehouse Pipeline

<p align="center">
  <img src="docs/screenshots/executive_overview.png" width="900"/>
</p>

A production-style **Healthcare Claims Lakehouse Analytics Platform** built using modern data engineering practices. This project demonstrates an end-to-end healthcare data pipeline that ingests claims data, applies **Medallion Architecture**, performs automated data quality validation, creates business-ready Gold analytics datasets, and delivers executive insights through an interactive **Streamlit dashboard**.

---

# 📊 Streamlit Analytics Dashboard

The Gold analytics layer powers an interactive Streamlit dashboard providing:

- Executive Claims Overview
- Claim Denial Analytics
- Provider Performance Analysis
- Member Utilization Analytics

Dashboard capabilities:

- Executive KPI monitoring
- Claims volume analysis
- Financial impact analysis
- Provider benchmarking
- Denial analysis
- Member utilization insights

---

# 🖼️ Dashboard Screenshots

## Executive Claims Overview

<p align="center">
  <img src="docs/screenshots/executive_overview.png" width="900"/>
</p>


## Denial Analytics

<p align="center">
  <img src="docs/screenshots/denial_analytics.png" width="900"/>
</p>


## Provider Performance

<p align="center">
  <img src="docs/screenshots/provider_performance.png" width="900"/>
</p>


## Member Utilization

<p align="center">
  <img src="docs/screenshots/member_utilization.png" width="900"/>
</p>


---

# 🏗️ Architecture

<p align="center">
  <img src="docs/architecture.png" width="1200"/>
</p>


The platform follows a **Medallion Lakehouse Architecture**:

```

Source Systems
|
v
PostgreSQL Healthcare Claims Database
|
v
Apache Airflow Orchestration
|
v
PySpark Processing
|
v
Bronze Layer
|
v
Silver Layer
|
v
Gold Analytics Layer
|
v
Streamlit Dashboard

```

---

# 🔄 Pipeline Overview

## Source Systems

Healthcare claims data originates from operational healthcare systems:

- Claims Processing System
- Member Eligibility System
- Provider Management System
- Healthcare Event System


Data is stored in a PostgreSQL healthcare claims database.

---

# 🥉 Bronze Layer — Raw Data Storage

The Bronze layer stores raw healthcare claims data after ingestion.

Responsibilities:

- Raw claims ingestion
- Source metadata tracking
- Batch identification
- Ingestion timestamp tracking
- Historical preservation

Storage format:

- Parquet

---

# 🥈 Silver Layer — Trusted Data Processing

The Silver layer applies PySpark transformations to create trusted analytical datasets.

Processing includes:

- Schema standardization
- Data cleansing
- Duplicate handling
- Business rule validation
- Transformation logic

---

# 🥇 Gold Layer — Business Analytics Products

The Gold layer contains curated analytical datasets consumed by the Streamlit dashboard.


## Provider Performance Analytics

Dataset:

```

gold/provider_performance

```

Includes:

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

Includes:

- Claim status analysis
- Denied claims
- Denial percentage
- Financial impact


---

## Member Utilization Analytics

Dataset:

```

gold/member_utilization

```

Includes:

- Member claim volume
- Total billed amount
- Total paid amount
- Average claim cost
- Service history

---

# ✅ Data Quality Framework

The pipeline uses **Great Expectations** for automated data validation.

Validation checkpoints:

## Pre-Bronze Validation

Validates incoming claims before entering Bronze storage.

Checks include:

- Schema validation
- Required field validation
- Data consistency checks


Invalid records are routed to:

```

Quarantine Storage

````

---

## Silver Validation

Validates transformed Silver data before promotion into Gold.

Checks include:

- Data completeness
- Business rule validation
- Transformation accuracy
- Data consistency

---

# ⚙️ Technology Stack

## Data Engineering

- Python
- PySpark
- Apache Airflow
- PostgreSQL
- Parquet


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

# 🚀 Running the Dashboard

Install dependencies:

```bash
pip install -r dashboard/requirements.txt
````

Run Streamlit:

```bash
streamlit run dashboard/app.py
```

Dashboard URL:

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
│       ├── executive_overview.png
│       ├── denial_analytics.png
│       ├── provider_performance.png
│       └── member_utilization.png
│
├── airflow/
├── scripts/
├── sql/
├── tests/
└── README.md
```

---

# 🔁 CI/CD

GitHub Actions validates:

* DAG syntax
* Python scripts
* Automated tests

---

# 🔐 Engineering Controls

Implemented controls:

* Data quality validation checkpoints
* Pipeline metadata tracking
* Batch tracking
* Version control
* Automated validation
* Quarantine handling

---

# 📈 Business Value

This platform enables healthcare organizations to:

* Identify claim denial patterns
* Monitor provider performance
* Analyze financial impact
* Understand member utilization behavior
* Deliver trusted analytics for operational decisions

---

# 👨‍💻 Healthcare Claims Lakehouse Analytics Platform

Built using modern data engineering practices and lakehouse architecture patterns.

````

