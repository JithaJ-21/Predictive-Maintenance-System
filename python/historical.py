import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data", "machine_log.csv")

GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

os.makedirs(GRAPH_DIR, exist_ok=True)


def generate_history_graphs():

    if not os.path.exists(DATA_FILE):
        return

    df = pd.read_csv(DATA_FILE)

    if len(df) < 2:
        return

    # ---------------- Temperature ----------------

    plt.figure(figsize=(10,4))

    plt.plot(df["Temperature"], marker='o')

    plt.title("Temperature History")

    plt.xlabel("Reading Number")

    plt.ylabel("Temperature (°C)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR, "temperature_history.png"))

    plt.close()

    # ---------------- RMS ----------------

    plt.figure(figsize=(10,4))

    plt.plot(df["RMS"], marker='o')

    plt.title("RMS History")

    plt.xlabel("Reading Number")

    plt.ylabel("RMS")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR, "rms_history.png"))

    plt.close()

    # ---------------- Health ----------------

    plt.figure(figsize=(10,4))

    plt.plot(df["Health Score"], marker='o')

    plt.title("Health Score History")

    plt.xlabel("Reading Number")

    plt.ylabel("Health (%)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR, "health_history.png"))

    plt.close()

    # ---------------- Efficiency ----------------

    plt.figure(figsize=(10,4))

    plt.plot(df["Efficiency"], marker='o')

    plt.title("Machine Efficiency History")

    plt.xlabel("Reading Number")

    plt.ylabel("Efficiency (%)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR, "efficiency_history.png"))

    plt.close()

    # ---------------- RUL ----------------

    plt.figure(figsize=(10,4))

    plt.plot(df["Remaining Useful Life"], marker='o')

    plt.title("Remaining Useful Life History")

    plt.xlabel("Reading Number")

    plt.ylabel("RUL (%)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR, "rul_history.png"))

    plt.close()

    plt.figure(figsize=(10,4))

    plt.plot(df["Peak"], marker='o')

    plt.title("Peak Value History")

    plt.xlabel("Reading Number")

    plt.ylabel("Peak")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
    os.path.join(
    GRAPH_DIR,
    "peak_history.png"
    ))

    plt.close()

    # ---------------- Fault Count ----------------

    status_map = {
        "HEALTHY":0,
        "WARNING":1,
        "CRITICAL":2
    }

    df["StatusCode"] = df["Status"].map(status_map)

    plt.figure(figsize=(10,4))

    plt.plot(df["StatusCode"], marker='o')

    plt.yticks(
        [0,1,2],
        ["Healthy","Warning","Critical"]
    )

    plt.title("Machine Status History")

    plt.xlabel("Reading")

    plt.ylabel("Status")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            GRAPH_DIR,
            "status_history.png"
        )
    )

    plt.close()

    print("Historical graphs generated successfully.")
