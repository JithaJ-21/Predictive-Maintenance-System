import requests
from config import WRITE_API_KEY, URL


def upload_to_thingspeak(rms, status_code, health_score, efficiency, rul, peak):

    payload = {
        "api_key": WRITE_API_KEY,
        "field3": rms,
        "field4": status_code,
        "field5": round(health_score,1),
        "field6": round(efficiency,1),
        "field7": round(rul,1),
        "field8": round(peak,2)
    }

    try:

        response = requests.post(URL, data=payload)

        if response.status_code == 200 and response.text != "0":
            print("Cloud Upload : SUCCESS")
            print(f"Entry ID : {response.text}")

        else:
            print("Cloud Upload : FAILED")

    except Exception as e:

        print("Upload Error :", e)
