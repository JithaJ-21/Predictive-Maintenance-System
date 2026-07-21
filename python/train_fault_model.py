import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataset = os.path.join(
    BASE_DIR,
    "Dataset",
    "machine_dataset.csv"
)

df = pd.read_csv(dataset)

print(df.head())

# -----------------------------
# Features
# -----------------------------

X = df[
    [
        "Temperature",
        "RMS",
        "Peak",
        "Health",
        "Efficiency"
    ]
]

# Target

y = df["FaultType"]

# -----------------------------
# Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train
# -----------------------------

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Test
# -----------------------------

prediction = model.predict(X_test)

print("\nAccuracy :", accuracy_score(y_test, prediction) * 100)

print("\nClassification Report\n")

print(classification_report(y_test, prediction))

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, prediction))

# -----------------------------
# Save Model
# -----------------------------

joblib.dump(
    model,
    os.path.join(
        BASE_DIR,
        "python",
        "fault_model.pkl"
    )
)

print("\nFault Prediction Model Saved.")
