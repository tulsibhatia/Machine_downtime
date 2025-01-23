from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import joblib
import os

app = FastAPI()

MODEL_PATH = "models/model.pkl"
DATA_PATH = "data/uploaded_data.csv"
model = None

class PredictionInput(BaseModel):
    Temperature: float
    Run_Time: float

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    if not os.path.exists("data"):
        os.makedirs("data")
    file_location = DATA_PATH
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    return {"message": "File uploaded successfully"}

@app.post("/train")
def train_model():
    global model

    if not os.path.exists(DATA_PATH):
        return {"error": "No dataset uploaded. Please upload data first."}
    data = pd.read_csv(DATA_PATH)

    X = data[["Temperature", "Run_Time"]]
    y = data["Downtime_Flag"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    if not os.path.exists("models"):
        os.makedirs("models")
    joblib.dump(model, MODEL_PATH)

    return {"accuracy": accuracy, "f1_score": f1}

@app.post("/predict")
def predict(input_data: PredictionInput):
    global model

    if model is None:
        if not os.path.exists(MODEL_PATH):
            return {"error": "No trained model found."}
        model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([input_data.dict()])
    prediction = model.predict(input_df)[0]
    confidence = model.predict_proba(input_df).max()

    return {"Downtime": "Yes" if prediction == 1 else "No", "Confidence": round(confidence, 2)}
