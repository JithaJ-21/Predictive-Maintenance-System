import numpy as np
from scipy.signal import savgol_filter

def analyze_machine(signal, temperature, fault_count):

    filtered_signal = savgol_filter(signal, 21, 3)

    rms = np.sqrt(np.mean(filtered_signal**2))

    # ---------------------------------
    # Peak Detection
    # ---------------------------------
    peak = np.max(np.abs(filtered_signal))

    if peak > 1.30:
        peak_status = "HIGH IMPACT"

    elif peak > 0.90:
        peak_status = "MEDIUM IMPACT"

    else:
        peak_status = "NORMAL"

    # --------------------------
    # Status
    # --------------------------
    if (
        rms > 0.75
        or peak > 1.30
        or temperature > 46
    ):

        status = "CRITICAL"
        status_code = 2
        recommendation = "Immediate shutdown and maintenance required."

    elif (
        rms > 0.40
        or peak > 0.90
        or temperature > 37
    ):

        status = "WARNING"
        status_code = 1
        recommendation = "Inspect bearings and shaft alignment."

    else:

        status = "HEALTHY"
        status_code = 0
        recommendation = "Machine operating normally."

    # --------------------------
    # Health Score
    # --------------------------

    health_score = (
        100 
        - rms * 40
        - peak * 18
        - max(0, temperature - 35) * 2.2
        - fault_count * 2
    )

    health_score = max(0, min(100, health_score))

    # --------------------------
    # Machine Efficiency
    # --------------------------

    efficiency = (
        100
        - rms * 18
        - max(0, temperature - 35) * 1.2
    )

    efficiency = max(50, min(100, efficiency))

    return (
        filtered_signal,
        rms,
        peak,
        peak_status,
        status,
        status_code,
        recommendation,
        round(health_score,1),
        round(efficiency,1)
    )
