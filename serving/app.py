from fastapi import FastAPI, HTTPException

from serving.schemas import InputData, OutputData
from serving.predictor import predict_one

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=OutputData)
def predict(data: InputData):
    try:
        result = predict_one(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
