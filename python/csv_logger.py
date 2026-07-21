import csv
import os
from datetime import datetime

FILE_NAME = "data/machine_log.csv"


def log_data(
    timestamp,
    temperature,
    rms,
    peak,
    status,
    ai_prediction,
    actual_fault,
    ai_fault,
    confidence,
    status_code,
    fault_confidence,
    fault_count,
    health_score,
    efficiency,
    rul,
    healthy_prob,
    bearing_prob,
    imbalance_prob,
    misalignment_prob,
    critical_prob
):
    """
    Stores every machine reading into CSV.
    Creates the file automatically if it doesn't exist.
    """

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Timestamp",
                "Temperature",
                "RMS",
                "Peak",
                "Status",
                "AI Prediction",
                "Actual Fault",
                "AI Fault",
                "Confidence",
                "Status Code",
                "Fault Confidence",
                "Fault Count",
                "Health Score",
                "Efficiency",
                "Remaining Useful Life",
                "Healthy %",
                "Bearing %",
                "Imbalance %",
                "Misalignment %",
                "Critical %"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(temperature, 2),
            round(rms, 3),
            round(peak,2),
            status,
            ai_prediction,
            actual_fault,
            ai_fault,
            round(confidence, 1),
            status_code,
            round(fault_confidence, 1),
            fault_count,
            round(health_score, 2),
            round(efficiency, 2),
            round(rul, 2),
            round(healthy_prob,1),
            round(bearing_prob,1),
            round(imbalance_prob,1),
            round(misalignment_prob,1),
            round(critical_prob,1)
        ])
