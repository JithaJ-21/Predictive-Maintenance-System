import os
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

os.makedirs(GRAPH_DIR, exist_ok=True)


def generate_graphs(
        t,
        healthy_signal,
        fault_signal,
        filtered_signal,
        temperature
):

    # -------------------------------
    # Healthy Signal
    # -------------------------------

    plt.figure(figsize=(12,4))

    plt.plot(t, healthy_signal)

    plt.title("Healthy Machine Vibration")

    plt.xlabel("Time (s)")

    plt.ylabel("Amplitude")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR,"healthy_signal.png"),dpi=300)

    plt.close()

    # -------------------------------
    # Fault Signal
    # -------------------------------

    plt.figure(figsize=(12,4))

    plt.plot(t,fault_signal,color="orange")

    plt.title("Faulty Machine Signal")

    plt.xlabel("Time (s)")

    plt.ylabel("Amplitude")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR,"fault_signal.png"),dpi=300)

    plt.close()

    # -------------------------------
    # Filtered Signal
    # -------------------------------

    plt.figure(figsize=(12,4))

    plt.plot(t,fault_signal,label="Faulty",alpha=0.5)

    plt.plot(
        t,
        filtered_signal,
        color="green",
        linewidth=2,
        label="Filtered"
    )

    plt.title("Signal Filtering")

    plt.xlabel("Time (s)")

    plt.ylabel("Amplitude")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR,"filtered_signal.png"),dpi=300)

    plt.close()

    # -------------------------------
    # Temperature Trend
    # -------------------------------

    plt.figure(figsize=(12,4))

    temperature_curve = np.ones(len(t)) * temperature

    plt.plot(
        t,
        temperature_curve,
        color="red"
    )

    plt.title("Machine Temperature")

    plt.xlabel("Time (s)")

    plt.ylabel("Temperature (°C)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR,"temperature.png"),dpi=300)

    plt.close()

    # -------------------------------
    # FFT
    # -------------------------------

    fft = np.fft.fft(filtered_signal)

    freq = np.fft.fftfreq(
        len(filtered_signal),
        d=t[1]-t[0]
    )

    plt.figure(figsize=(12,4))

    plt.plot(
        freq[:500],
        np.abs(fft[:500])
    )

    fft_mag=np.abs(fft)

    positive=freq>0

    dominant_freq=freq[positive][
    np.argmax(fft_mag[positive])
    ]
    
    plt.axvline(
    dominant_freq,
    color="green",
    label=f"Peak {dominant_freq:.2f} Hz"
    )

    plt.title("FFT Frequency Spectrum")

    plt.xlabel("Frequency (Hz)")

    plt.ylabel("Magnitude")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig(os.path.join(GRAPH_DIR,"fft.png"),dpi=300)

    plt.close()

    print("Graphs saved successfully.")
