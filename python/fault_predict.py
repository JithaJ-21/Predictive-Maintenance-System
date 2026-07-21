import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "python", "fault_model.pkl")

model = joblib.load(MODEL_PATH)
classes = model.classes_

def predict_fault(
    temperature,
    rms,
    peak,
    health,
    efficiency
):

    features = pd.DataFrame([{
        "Temperature": temperature,
        "RMS": rms,
        "Peak": peak,
        "Health": health,
        "Efficiency": efficiency
    }])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    confidence = max(probabilities)*100

    return prediction, confidence, probabilities, model.classes_
