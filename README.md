# 🏠 Scorimo

## Overview

**Scorimo** is an automated listing quality scoring tool for French real estate platforms (SeLoger, Leboncoin, etc.).

It scores each property listing from **0 to 100** based on information completeness and consistency, helping buyers instantly filter out low-quality listings — without manual inspection.

---

## Problem Statement

Anyone who has searched for housing in France has encountered listings with:
- Vague or missing descriptions
- Too few photos
- Incomplete addresses
- Suspicious price-to-surface ratios

**Scorimo solves this** by automatically evaluating each listing's data quality and returning a structured score with explanations.

---

## What the Tool Does

The user (or platform) submits listing data:

```json
{
  "price": 320000,
  "surface": 45,
  "description_length": 80,
  "photo_count": 2,
  "location_precision": "district",
  "rooms": 2
}
```

The API returns a quality score and diagnosis:

```json
{
  "quality_score": 58,
  "tier": "LOW",
  "issues": ["Too few photos", "Short description", "No floor information"],
  "model_version": "v1.4"
}
```

### Score & Tier Logic

Scoring starts at 100 and deductions are applied based on:

| Issue | Deduction |
|-------|-----------|
| `photo_count < 3` | -20 |
| `description_length < 100` | -15 |
| `price / surface > 15,000` | -10 |
| No room information | -10 |
| Location precision = "city" | -10 |

Final tier:
- `HIGH` → score ≥ 75
- `MEDIUM` → score ≥ 50
- `LOW` → score < 50

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        DATA LAYER                        │
│         data.gouv.fr  →  cleaning  →  feature eng.      │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                     TRAINING LAYER                       │
│         train.py  →  MLflow Tracking  →  Model Registry  │
│                    (Staging / Production)                 │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    SERVING LAYER                         │
│         FastAPI  →  Docker  →  /predict endpoint         │
│         (loads Production model from Registry)           │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                   MONITORING LAYER                       │
│         Evidently  →  drift detection  →  alerts         │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
Scorimo/
│
├── data/
│   ├── raw/                  # Raw data from data.gouv.fr
│   ├── processed/            # Cleaned & feature-engineered dataset
│   └── prepare_data.py       # Data download and cleaning script
│
├── training/
│   ├── train.py              # Model training script (logs to MLflow)
│   ├── score_rules.py        # Quality scoring rule definitions
│   └── evaluate.py           # Model evaluation metrics
│
├── serving/
│   ├── app.py                # FastAPI application
│   ├── model_loader.py       # Loads Production model from MLflow Registry
│   └── Dockerfile            # Container definition
│
├── monitoring/
│   ├── monitor.py            # Evidently drift detection
│   └── reference_data.csv    # Baseline distribution for drift comparison
│
├── mlflow/
│   └── mlruns/               # MLflow tracking directory (local)
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## MLOps Pipeline

### 1. Data Layer (Member C — Haoju Li)
- Data sourced from [data.gouv.fr](https://www.data.gouv.fr)
- Cleaned and feature-engineered in `data/prepare_data.py`
- Scoring rules defined in `training/score_rules.py`

### 2. Experiment Tracking — MLflow (Member A — Hangbo Yang)
Every training run automatically logs:
- Parameters (scoring weights, thresholds)
- Metrics (MAE, accuracy)
- Model artifact

Run the MLflow UI:
```bash
mlflow ui
# → open http://localhost:5000
```

### 3. Model Registry — MLflow (Member A — Hangbo Yang)
Models are versioned and promoted through stages:
```
None  →  Staging  →  Production
```
The API always loads whichever model is tagged **Production**.

### 4. Serving — FastAPI + Docker (Member B — Ke Chen)
The API dynamically loads the Production model at startup.
Switching model versions requires **no code change** — update the Registry and restart.

Available endpoints:
- `POST /predict` — score a listing
- `GET /health` — health check
- `GET /model-info` — current model version

### 5. Monitoring — Evidently (Member C — Haoju Li)
Every prediction is logged. Evidently compares incoming distributions against a reference baseline.

```bash
python monitoring/monitor.py
# → generates drift_report.html in your browser
```

---

## Installation & Usage

### Prerequisites
- Python 3.10+
- Docker

### Run locally

```bash
# 1. Clone the repo
git clone https://github.com/audreyli0428/Scorimo.git
cd Scorimo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data
python data/prepare_data.py

# 4. Train the model
python training/train.py

# 5. Promote model to Production in MLflow UI
#    → http://localhost:5000

# 6. Start the API
docker-compose up
```

### Call the API

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"price": 320000, "surface": 45, "photo_count": 2, "description_length": 80, "rooms": 2}'
```

---

## What We Chose NOT to Build

### 1. Search history
- No database or query logging
- > Possible improvement: store queries with SQLite and export to `.xlsx`

### 2. Online hosting
- Local only (no cloud deployment)
- > Possible improvement: deploy via a serverless platform

---

## Team

| Member | Role | Owns |
|--------|------|------|
| **Hangbo Yang** | MLOps Engineer | MLflow tracking, Model Registry (`training/`) |
| **Ke Chen** | Deployment Engineer | FastAPI, Docker, model loader (`serving/`) |
| **Haoju Li** | Data & Monitoring | Data pipeline, scoring rules, Evidently (`data/`, `monitoring/`) |

---

## Branch Strategy

```
main        ← stable, demo-ready only
develop     ← integration branch
  ├── feature/data-pipeline        (Haoju Li)
  ├── feature/training-mlflow      (Hangbo Yang)
  ├── feature/serving-api          (Ke Chen)
  └── feature/monitoring-evidently (Haoju Li)
```
