# \# 🏠 Scorimo

# 

# > Automated listing quality scoring for French real estate — with a full MLOps pipeline.

# 

# Scorimo automatically scores property listings (0–100) based on information completeness and consistency, helping buyers filter out low-quality listings on platforms like SeLoger or Leboncoin.

# 

# \---

# 

# \## 📌 Table of Contents

# 

# \- \[Problem Statement](#problem-statement)

# \- \[Product Overview](#product-overview)

# \- \[Architecture](#architecture)

# \- \[Project Structure](#project-structure)

# \- \[Getting Started](#getting-started)

# \- \[MLOps Pipeline](#mlops-pipeline)

# \- \[Team](#team)

# 

# \---

# 

# \## Problem Statement

# 

# On French real estate platforms, many listings suffer from missing or inconsistent information: vague descriptions, few photos, incomplete addresses, or suspicious price-to-surface ratios. Buyers waste time manually filtering these out.

# 

# \*\*Scorimo solves this by automatically scoring each listing's information quality\*\*, so buyers can focus on what matters.

# 

# \---

# 

# \## Product Overview

# 

# \*\*Input\*\* — structured listing data:

# ```json

# {

# &#x20; "price": 320000,

# &#x20; "surface": 45,

# &#x20; "description\_length": 80,

# &#x20; "photo\_count": 2,

# &#x20; "location\_precision": "district",

# &#x20; "rooms": 2

# }

# ```

# 

# \*\*Output\*\* — quality score + explanation:

# ```json

# {

# &#x20; "quality\_score": 58,

# &#x20; "tier": "LOW",

# &#x20; "issues": \["Too few photos", "Short description", "No floor information"],

# &#x20; "model\_version": "v1.4"

# }

# ```

# 

# \---

# 

# \## Architecture

# ```

# ┌─────────────────────────────────────────────────────────┐

# │                        DATA LAYER                        │

# │         data.gouv.fr  →  cleaning  →  feature eng.      │

# └───────────────────────────┬─────────────────────────────┘

# &#x20;                           │

# ┌───────────────────────────▼─────────────────────────────┐

# │                     TRAINING LAYER                       │

# │         train.py  →  MLflow Tracking  →  Model Registry  │

# │                    (Staging / Production)                 │

# └───────────────────────────┬─────────────────────────────┘

# &#x20;                           │

# ┌───────────────────────────▼─────────────────────────────┐

# │                    SERVING LAYER                         │

# │         FastAPI  →  Docker  →  /predict endpoint         │

# │         (loads Production model from Registry)           │

# └───────────────────────────┬─────────────────────────────┘

# &#x20;                           │

# ┌───────────────────────────▼─────────────────────────────┐

# │                   MONITORING LAYER                       │

# │         Evidently  →  drift detection  →  alerts         │

# └─────────────────────────────────────────────────────────┘

# ```

# 

# \---

# 

# \## Project Structure

# ```

# scorimo/

# │

# ├── data/

# │   ├── raw/                  # Raw data from data.gouv.fr

# │   ├── processed/            # Cleaned \& feature-engineered dataset

# │   └── prepare\_data.py       # Data preparation script

# │

# ├── training/

# │   ├── train.py              # Model training script (logs to MLflow)

# │   ├── score\_rules.py        # Quality scoring rule definitions

# │   └── evaluate.py           # Model evaluation metrics

# │

# ├── serving/

# │   ├── app.py                # FastAPI application

# │   ├── model\_loader.py       # Loads Production model from MLflow Registry

# │   └── Dockerfile            # Container definition

# │

# ├── monitoring/

# │   ├── monitor.py            # Evidently drift detection

# │   └── reference\_data.csv    # Baseline distribution for drift comparison

# │

# ├── mlflow/

# │   └── mlruns/               # MLflow tracking directory (local)

# │

# ├── docker-compose.yml

# ├── requirements.txt

# └── README.md

# ```

# 

# \---

# 

# \## Getting Started

# 

# \### Prerequisites

# 

# \- Python 3.10+

# \- Docker

# 

# \### Run locally

# ```bash

# \# 1. Clone the repo

# git clone https://github.com/audreyli0428/Scorimo.git

# cd Scorimo

# 

# \# 2. Install dependencies

# pip install -r requirements.txt

# 

# \# 3. Generate sample data

# python data/prepare\_data.py

# 

# \# 4. Train the model

# python training/train.py

# 

# \# 5. Start the API

# docker-compose up

# ```

# 

# \### Call the API

# ```bash

# curl -X POST http://localhost:8000/predict \\

# &#x20; -H "Content-Type: application/json" \\

# &#x20; -d '{"price": 320000, "surface": 45, "photo\_count": 2, "description\_length": 80, "rooms": 2}'

# ```

# 

# \---

# 

# \## MLOps Pipeline

# 

# \### 1. Experiment Tracking (MLflow)

# Every training run logs parameters, metrics (MAE, accuracy), and the model artifact.

# 

# \### 2. Model Registry (MLflow)

# Models are promoted through stages:

# ```

# None  →  Staging  →  Production

# ```

# 

# \### 3. Serving (FastAPI + Docker)

# The API dynamically loads the Production model at startup. No code change needed to switch versions.

# 

# \### 4. Monitoring (Evidently)

# Incoming data is compared against a reference baseline to detect drift.

# ```bash

# python monitoring/monitor.py

# ```

# 

# \---

# 

# \## Team

# 

# | Member | Role | Owns |

# |--------|------|------|

# | \*\*Member A\*\* | MLOps Engineer | MLflow tracking, Model Registry (`training/`) |

# | \*\*Member B\*\* | Deployment Engineer | FastAPI, Docker, model loader (`serving/`) |

# | \*\*Member C\*\* | Data \& Monitoring | Data pipeline, scoring rules, Evidently (`data/`, `monitoring/`) |

