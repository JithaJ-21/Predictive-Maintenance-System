import os
import csv
from python.simulator import generate_machine_data
from python.anomaly import analyze_machine

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "Dataset")

os.makedirs(DATASET_DIR, exist_ok=True)

csv_path = os.path.join(DATASET_DIR, "machine_dataset.csv")

# -----------------------------
# Generate Dataset
# -----------------------------

with open(csv_path, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Temperature",
        "RMS",
        "Peak",
        "Health",
        "Efficiency",
        "Status",
        "FaultType"
    ])

    for _ in range(10000):

        t, healthy_signal, signal, temperature, fault_type = generate_machine_data()

        filtered_signal, rms, peak, peak_status, status, status_code, recommendation, health, efficiency = analyze_machine(
            signal,
            temperature,
            0
        )

        # Skip contradictory samples

        if fault_type == "Healthy" and status != "HEALTHY":
            continue

        if fault_type == "Critical" and status != "CRITICAL":
            continue

        writer.writerow([
            round(temperature,2),
            round(rms,3),
            round(peak,3),
            round(health,2),
            round(efficiency,2),
            status,
            fault_type
        ])

print("\nDataset Generated Successfully!")
print(csv_path)
