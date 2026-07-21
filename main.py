from python.anomaly import analyze_machine
from python.cloud import upload_to_thingspeak
from config import UPDATE_INTERVAL
from python.csv_logger import log_data
from python.analysis import generate_graphs
from python.historical import generate_history_graphs
from python.predict import predict_machine
from python.fault_predict import predict_fault
from datetime import datetime, timedelta
from python.live_sensor import get_live_data
from python.read_thingspeak import read_sensor
import numpy as np
import pandas as pd
import time

MACHINE_ID = "MTR-001"
PLANT_NAME = "UVCE Smart Factory"

print("="*60)
print("   INDUSTRIAL PREDICTIVE MAINTENANCE SYSTEM")
print("="*60)

fault_count = 0

fault_description = {
    "Healthy": "No Fault Detected",
    "Bearing": "Bearing Wear",
    "Imbalance": "Rotor Imbalance",
    "Misalignment": "Shaft Misalignment",
    "Critical": "Severe Machine Failure"
}

fault_info = {
    "Healthy": {
        "description": "No Fault Detected",
        "severity": "LOW"
    },
    "Bearing": {
        "description": "Bearing Wear",
        "severity": "MEDIUM"
    },
    "Imbalance": {
        "description": "Rotor Imbalance",
        "severity": "MEDIUM"
    },
    "Misalignment": {
        "description": "Shaft Misalignment",
        "severity": "HIGH"
    },
    "Critical": {
        "description": "Severe Machine Failure",
        "severity": "CRITICAL"
    }
}

while True:
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # ----------------------------------
    # Generate Machine Data
    # ----------------------------------

    temperature, vibration = read_sensor()
    print(temperature, vibration)

    if temperature is None or vibration is None:

         print("No new sensor data available.")
         print("Waiting for ESP32/ThingSpeak update...")

         break

    if temperature < 0 or temperature > 100:

        print("Invalid temperature received.")

        continue

    t = np.linspace(0, 2*np.pi, 1000)

    base_amp = vibration / 4096

    noise = np.random.normal(0, 0.01, 1000)

    signal = (
        base_amp*np.sin(20*t)
        +0.25*base_amp*np.sin(40*t)
        +noise
    )
    if temperature>40:

        signal += 0.08*np.sin(70*t)

    if temperature>45:

        signal +=0.15*np.sin(90*t)

    def progress_bar(value):

        value = max(0, min(100, value))

        filled = int(value // 10)

        return "█" * filled + "░" * (10 - filled)
    
    # ----------------------------------
    # Analyze Machine
    # ----------------------------------

    filtered_signal, rms, peak, peak_status, status, status_code, recommendation, health_score, efficiency = analyze_machine(
        signal,
        temperature,
        fault_count
    )

    ai_prediction, confidence, status_probs = predict_machine(
        temperature,
        rms,
        peak,
        health_score,
        efficiency
    )

    # Safety override
    if status == "CRITICAL":
        ai_prediction = "CRITICAL"
        confidence = max(confidence, 92)

    ai_fault, fault_confidence, fault_probs, fault_classes = predict_fault(
        temperature,
        rms,
        peak,
        health_score,
        efficiency
    )

    fault_prob_dict = dict(zip(fault_classes, fault_probs))

    # ----------------------------
    # Final Decision Logic
    # ----------------------------

    final_status = status

    decision_reason = "Rule engine decision accepted."

    # Rule engine always wins for CRITICAL
    if status == "CRITICAL":

        final_status = "CRITICAL"

        decision_reason = "Critical thresholds exceeded."

    # Rule says WARNING but AI says HEALTHY
    elif status == "WARNING":

        if ai_prediction == "HEALTHY" and confidence < 95:

            final_status = "WARNING"

            decision_reason = "Rule engine overrides AI for safety."

        else:

            final_status = ai_prediction

            decision_reason = "Rule engine and AI agree."

    # Rule says HEALTHY but AI strongly suspects degradation
    elif status == "HEALTHY":

        if ai_prediction == "WARNING" and confidence > 96:

            final_status = "WARNING"

            decision_reason = "AI detected possible early degradation."

        else:

            final_status = "HEALTHY"

            decision_reason = "Machine operating normally."

    fault_type = ai_fault

    t = np.arange(len(signal))

    healthy_signal=0.15*np.sin(20*t)

    if status != "HEALTHY":
        generate_graphs(
            t,
            healthy_signal,
            signal,
            filtered_signal,
            temperature
        )

    # ----------------------------------
    # Count Faults
    # ----------------------------------
    if status == "WARNING":
        fault_count += 1

    elif status == "CRITICAL":
        fault_count += 2

    rul = (
        health_score
        -rms*8
        -fault_count*4
        -max(0,temperature-35)
    )

    rul = max(0, min(100, rul))

    # ----------------------------------
    # Critical
    # ----------------------------------
    if status == "CRITICAL" or ai_prediction == "CRITICAL":

        print("\n")
        print("="*70)
        print("🚨  CRITICAL MACHINE ALERT")
        print("-"*70)
        print(f"Fault Type             : {fault_description.get(ai_fault, ai_fault)}")
        print(f"Fault Severity         : {fault_info[ai_fault]['severity']}")
        print("Machine Condition       : CRITICAL")
        print("AI/Rule Engine Triggered")
        print("Immediate Action        : Shutdown Recommended")
        print("Maintenance Priority    : HIGH")
        print("Notify Maintenance Team")
        print("Generate Incident Report")
        print("Log Event to Cloud")
        print("="*70)

    # ----------------------------------
    # Print Dashboard
    # ----------------------------------

    print("="*70)
    print("          INDUSTRIAL MACHINE HEALTH REPORT")
    print("="*70)

    print(f"Plant Name           : {PLANT_NAME}")
    print(f"Machine ID           : {MACHINE_ID}")
    print(f"Timestamp : {current_time}")

    print("-"*70)

    # -----------------------------
    # Operating State
    # -----------------------------

    if status == "HEALTHY":
        operating = "RUNNING"
        maintenance="Next inspection in 30 days"

    elif status == "WARNING":
        operating = "RUNNING WITH CAUTION"
        maintenance="Schedule inspection within 7 days"

    else:
        operating = "STOP IMMEDIATELY"
        maintenance="Immediate shutdown and maintenance"

    print(f"Operating State      : {operating}")

    # -----------------------------
    # Risk
    # -----------------------------

    if health_score >= 80:
        risk = "LOW"

    elif health_score >= 60:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    print(f"Risk Level           : {risk}")

    print("-"*70)

    print(f"Temperature          : {temperature:.2f} °C")
    print(f"RMS                  : {rms:.3f}")
    print(f"Peak Value           : {peak:.2f}")
    print(f"Peak Condition       : {peak_status}")

    print("-"*70)

    # -----------------------------
    # AI + Rule Engine Summary
    # -----------------------------

    print(f"Rule Engine Status   : {status}")
    print(f"AI Suggestion        : {ai_prediction}")
    print(f"AI Confidence        : {progress_bar(confidence)} {confidence:.1f}%")

    print(f"Final Machine Status : {final_status}")
    print(f"Status Code : {status_code}")
    print(f"Decision Reason      : {decision_reason}")

    print()

    # -----------------------------
    # Fault Prediction
    # -----------------------------

    print(f"Detected Fault       : {fault_description.get(ai_fault, ai_fault)} ({fault_confidence:.1f}%)")
    print("\nPossible Alternatives")
    print("-"*70)

    sorted_probs = sorted(
        zip(fault_classes, fault_probs),
        key=lambda x: x[1],
        reverse=True
    )

    for cls, prob in sorted_probs[1:4]:
        bar = "█"*int(prob*20)

        print(f"{cls:<15} {bar:<20} {prob*100:.1f}%")

    print()

    print("Fault Probability")
    print("-"*70)

    sorted_probs = sorted(
        zip(fault_classes, fault_probs),
        key=lambda x: x[1],
        reverse=True
    )

    for cls, prob in sorted_probs:

        bar = "█" * int(prob * 20)

        print(f"{fault_description.get(cls, cls):<28} {bar:<20} {prob*100:5.1f}%")

    print(f"Fault Confidence     : {progress_bar(fault_confidence)} {fault_confidence:.1f}%")

    print("-"*70)

    # -----------------------------
    # Health Metrics
    # -----------------------------

    print(f"Health Score         : {progress_bar(health_score)} {health_score:.1f}%")

    print(f"Efficiency           : {progress_bar(efficiency)} {efficiency:.1f}%")

    print(f"Remaining Life (RUL) : {progress_bar(rul)} {rul:.1f}%")

    print("-"*70)

    print(f"Recommendation       : {recommendation}")

    today = datetime.now()
    if status == "HEALTHY":
        maintenance = "Next inspection in 30 days"
        due_date = today + timedelta(days=30)

    elif status == "WARNING":
        maintenance = "Schedule inspection within 7 days"
        due_date = today + timedelta(days=7)

    else:
        maintenance = "Immediate maintenance required"
        due_date = today

    print(f"Maintenance Due    : {due_date.strftime('%d-%m-%Y')}")
    print(f"Maintenance Plan     : {maintenance}")

    print(f"Fault Count          : {fault_count}")

    print("="*70)
    # ----------------------------------
    # Upload to Cloud
    # ----------------------------------

    upload_to_thingspeak(
        rms,
        status_code,
        health_score,
        efficiency,
        rul,
        peak
    )

    log_data(
        current_time,
        temperature,
        rms,
        peak,
        status,
        ai_prediction,
        fault_description.get(ai_fault, ai_fault),
        fault_description.get(ai_fault, ai_fault),
        confidence,
        status_code,
        fault_confidence,
        fault_count,
        health_score,
        efficiency,
        rul,
        fault_prob_dict["Healthy"]*100,
        fault_prob_dict["Bearing"]*100,
        fault_prob_dict["Imbalance"]*100,
        fault_prob_dict["Misalignment"]*100,
        fault_prob_dict["Critical"]*100
    )

    csv = pd.read_csv("data/machine_log.csv")

    if len(csv) > 200:

        csv = csv.tail(200)

        csv.to_csv(
            "data/machine_log.csv",
            index=False
        )

    generate_history_graphs()

    print("-"*60)

    time.sleep(UPDATE_INTERVAL)
