import numpy as np
import random


def generate_machine_data():

    t = np.linspace(0, 2 * np.pi, 1000)

    # -------------------------
    # Machine condition (60-30-10)
    # -------------------------

    machine = random.choices(
        ["HEALTHY", "WARNING", "CRITICAL"],
        weights=[60, 30, 10],
        k=1
    )[0]

    # -------------------------
    # Healthy Machine
    # -------------------------

    if machine == "HEALTHY":

        temperature = np.random.uniform(28, 36)

        vibration = np.random.uniform(900, 1700)

        noise = np.random.normal(0, 0.008, 1000)

        fault = "Healthy"

    # -------------------------
    # Warning Machine
    # -------------------------

    elif machine == "WARNING":

        fault = random.choice([
            "Bearing",
            "Imbalance",
            "Misalignment"
        ])

        if fault == "Bearing":

            temperature = np.random.uniform(37,42)
            vibration = np.random.uniform(1800,2400)

        elif fault == "Imbalance":

            temperature = np.random.uniform(35,40)
            vibration = np.random.uniform(2200,2900)

        elif fault == "Misalignment":

            temperature = np.random.uniform(39,44)
            vibration = np.random.uniform(1900,2600)

        noise = np.random.normal(0,0.015,1000)

    # -------------------------
    # Critical Machine
    # -------------------------

    else:

        fault = random.choices(
            [
            "Critical",
            "Bearing",
            "Imbalance",
            "Misalignment"
            ],
            weights=[70,10,10,10],
            k=1
        )[0]

        if fault == "Critical":

            temperature = np.random.uniform(50, 55)
            vibration = np.random.uniform(3600, 4096)

        elif fault == "Bearing":

            temperature = np.random.uniform(46, 50)
            vibration = np.random.uniform(3000, 3500)

        elif fault == "Imbalance":

            temperature = np.random.uniform(44, 48)
            vibration = np.random.uniform(3300, 3900)

        elif fault == "Misalignment":

            temperature = np.random.uniform(47, 52)
            vibration = np.random.uniform(2900, 3400)

        noise = np.random.normal(0, 0.03, 1000)

    # -------------------------
    # Base vibration amplitude
    # -------------------------

    base_amp = (vibration / 4096) * np.random.uniform(0.95, 1.05)

    # -------------------------
    # Healthy reference signal
    # -------------------------

    healthy_signal = (
        np.random.uniform(0.12, 0.18)
        * np.sin(20 * t)
    )

    # -------------------------
    # Actual machine signal
    # -------------------------

    signal = (
        base_amp * np.sin(20 * t)
        + 0.25 * base_amp * np.sin(40 * t)
        + noise
    )

    # -------------------------
    # Fault signatures
    # -------------------------

    if fault == "Bearing":

        signal += (
            0.12*np.sin(90*t)
            +0.05*np.sin(180*t)
        )

    elif fault == "Imbalance":

        signal += (
            0.22*np.sin(20*t)
        )

    elif fault == "Misalignment":

        signal += (
            0.10*np.sin(50*t)
            +0.10*np.sin(70*t)
        )

    elif fault == "Critical":

        signal += (
            0.30*np.sin(70*t)
            +0.25*np.sin(110*t)
            +0.18*np.sin(180*t)
        )

    # -------------------------
    # Random sensor spikes
    # -------------------------

    if machine == "WARNING":

        for _ in range(np.random.randint(1,3)):

            idx = np.random.randint(50,950)

            signal[idx:idx+3] += np.random.uniform(0.04,0.08)

    elif machine == "CRITICAL":

        for _ in range(np.random.randint(3,6)):

            idx = np.random.randint(50,950)

            signal[idx:idx+5] += np.random.uniform(0.10,0.20)

    return (
        t,
        healthy_signal,
        signal,
        temperature,
        fault
    )
