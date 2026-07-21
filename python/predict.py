import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_machine(temperature, rms, peak, health, efficiency):

    features = pd.DataFrame([{
        "Temperature": temperature,
        "RMS": rms,
        "Peak": peak,
        "Health": health,
        "Efficiency": efficiency
    }])

    prediction = model.predict(features)[0]

    probs = model.predict_proba(features)[0]

    confidence = max(probs) * 100

    return prediction, confidence, probs
