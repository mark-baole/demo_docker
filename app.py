from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Define the input data model
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Load the saved model
MODEL_FILE = './models/iris_model.pkl'
with open(MODEL_FILE, 'rb') as f:
    model = pickle.load(f)

# Create the FastAPI app
app = FastAPI()

# Define the root endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}

# Define the prediction endpoint
@app.post("/predict")
def predict_iris(data: IrisData):
    # Prepare the input data for prediction
    input_data = pd.DataFrame([data.dict()])

    # Make the prediction using the loaded model
    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)

    # Prepare the response
    response = {
        'prediction': prediction[0],
        'probabilities': {label: proba for label, proba in zip(model.classes_, probabilities[0])}
    }
    return response
