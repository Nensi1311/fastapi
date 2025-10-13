# FastAPI Projects in This Repository

This repository contains two FastAPI applications:

- Root app at `main.py`: A simple Hello World style API.
- ML app at `ML_WITH_FASTAPI/main.py`: An insurance premium prediction API powered by a pre-trained model (`ML_WITH_FASTAPI/model.pkl`).

The repository also includes a `Dockerfile` and `Docker/requirements.txt` to run the ML app via Docker.

---

## Prerequisites

- Python 3.11+
- pip
- Optional: Docker 24+ (for containerized run)

---

## Quick Start (Root App)

The root app is defined in `main.py` at the repository root.

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Run locally

```bash
uvicorn main:app --reload --port 8000
```

- Base URL: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

### Endpoints

- `GET /` → `{ "message": "Hello World" }`
- `GET /about` → `{ "message": "I am Nensi Pansuriya" }`

---

## ML App: Insurance Premium Prediction API

The ML app lives in `ML_WITH_FASTAPI/` and expects a trained model at `ML_WITH_FASTAPI/model.pkl`.

### Project files

- `ML_WITH_FASTAPI/main.py`: FastAPI app exposing prediction endpoints
- `ML_WITH_FASTAPI/model.pkl`: Serialized model loaded at startup
- `ML_WITH_FASTAPI/insurance.csv`: Dataset (reference)
- `ML_WITH_FASTAPI/app.py`: Additional experimenting entry point (not used below)

### Install dependencies

From the repository root:

```bash
pip install -r Docker/requirements.txt
```

This installs at least:
- `FastAPI`
- `uvicorn`

Note: The ML app also uses `pandas` and `pickle` (standard library). Ensure your model was trained with compatible versions.

### Run locally

Change directory to the ML app root for clarity or run from repo root:

```bash
cd ML_WITH_FASTAPI
uvicorn main:app --reload --port 8001
```

- Base URL: `http://127.0.0.1:8001`
- Docs: `http://127.0.0.1:8001/docs`

### Endpoints

- `GET /` → Welcome message
- `GET /health` → Health and model load status
- `POST /predict` → Predict premium category

#### Request model for `/predict`

Fields (sent as JSON):
- `Age` (int, 1–119)
- `Weight` (float, kg > 0)
- `Height` (float, cm > 0)
- `Income_LPA` (float, LPA > 0)
- `Smoker` (bool)
- `City` (string)
- `Occupation` (one of: `Teacher`, `Clerk`, `Lawyer`, `Engineer`, `Doctor`, `Manager`)

Derived features are computed internally: `bmi`, `lifestyle_risk`, `age_group`, `city_tier`.

#### Example request

```bash
curl -X POST http://127.0.0.1:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 34,
    "Weight": 72.5,
    "Height": 175.0,
    "Income_LPA": 12.0,
    "Smoker": true,
    "City": "Surat",
    "Occupation": "Engineer"
  }'
```

#### Example response

```json
{
  "Response": "Medium",
  "Confidence": 0.86,
  "Class Probabilities": {
    "Low": 0.05,
    "Medium": 0.86,
    "High": 0.09
  }
}
```

---

## Run with Docker (ML App)

The provided `Dockerfile` is configured to run the ML app from `ML_WITH_FASTAPI`.

### Build image

From the repository root:

```bash
docker build -t fastapi-ml .
```

### Run container

```bash
docker run --rm -p 8000:8000 fastapi-ml
```

- Base URL: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

Note: The container exposes port 8000 by default per the `Dockerfile` CMD: `uvicorn main:app --host 0.0.0.0 --port 8000` within the `ML_WITH_FASTAPI` workdir.