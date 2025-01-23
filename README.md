# Machine_downtime

1. Install Python 3.x.
2. Install dependencies:
   pip install -r requirements.txt

Features:
Upload Data: Accepts a CSV file containing manufacturing data.

Train Model: Trains a Logistic Regression model on the uploaded dataset and saves it for future use.

Make Predictions: Accepts JSON input and returns predictions for machine downtime.

Endpoints

1. Upload Dataset

Endpoint: POST /upload

Description: Upload a CSV file containing manufacturing data.

Payload: File upload (CSV).

Example (using curl):

curl -X POST "http://127.0.0.1:8000/upload" -F "file=@path/to/your_dataset.csv"

Response:

{
  "message": "File uploaded successfully"
}

2. Train Model

Endpoint: POST /train

Description: Train a Logistic Regression model on the uploaded dataset.

Payload: None.

Example:

curl -X POST "http://127.0.0.1:8000/train"

Response:

{
  "accuracy": 0.87,
  "f1_score": 0.85
}

3. Make Predictions

Endpoint: POST /predict

Description: Make predictions for machine downtime based on input data.

Payload:

{
  "Temperature": 85,
  "Run_Time": 120
}

Example (using curl):

curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"Temperature": 85, "Run_Time": 120}'

Response:
{
  "Downtime": "No",
  "Confidence": 0.91
}
