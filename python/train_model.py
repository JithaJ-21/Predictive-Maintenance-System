import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import joblib

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataset = os.path.join(BASE_DIR,
                       "Dataset",
                       "machine_dataset.csv")

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

y = df["Status"]

# -----------------------------
# Train/Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Model
# -----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy :", accuracy*100)

print("\nClassification Report\n")

print(classification_report(y_test, predictions))

print("\nConfusion Matrix\n")

print(confusion_matrix(y_test, predictions))

# -----------------------------
# Save Model
# -----------------------------

joblib.dump(
    model,
    os.path.join(BASE_DIR,
                 "python",
                 "saved_model.pkl")
)

print("\nModel Saved Successfully.")
