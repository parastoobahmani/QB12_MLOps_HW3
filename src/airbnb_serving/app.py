from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()
import os

import mlflow


from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request

from .predictor import predict_single, predict_batch
from .schema import ListingFeatures, PredictionResponse

MODEL_RUN_ID = os.getenv("MODEL_RUN_ID")
MODEL_URI = os.getenv("MODEL_URI")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_TRACKING_USERNAME = os.getenv("MLFLOW_TRACKING_USERNAME")
MLFLOW_TRACKING_PASSWORD = os.getenv("MLFLOW_TRACKING_PASSWORD")
print("MODEL_URI =", MODEL_URI)
print("MODEL_RUN_ID =", MODEL_RUN_ID)

@asynccontextmanager
async def lifespan(app:FastAPI):

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    if MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD:
        os.environ["MLFLOW_TRACKING_USERNAME"] = MLFLOW_TRACKING_USERNAME
        os.environ["MLFLOW_TRACKING_PASSWORD"] = MLFLOW_TRACKING_PASSWORD
    global model
    model = mlflow.sklearn.load_model(MODEL_URI)
    app.state.model = model

    yield

app = FastAPI(lifespan=lifespan)


@app.get('/health')
def health():
    return {"status": "ok", 
            "model_run_id": str(MODEL_RUN_ID)}


@app.post("/predict")
def predict(payload: ListingFeatures, request: Request):
    model = request.app.state.model
    return predict_single(payload, model, MODEL_RUN_ID)

@app.post('/predict/batch')
def predictBatch(payload: list[ListingFeatures])-> list[PredictionResponse]:
    return predict_batch(payload, model, MODEL_RUN_ID)
