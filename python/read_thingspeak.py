import requests

CHANNEL_ID = "3426878"
READ_API_KEY = "AT6Y69DX3O24CHV9"

def read_sensor():

    url = (
        f"https://api.thingspeak.com/channels/"
        f"{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"
    )

    try:

        response = requests.get(url)

        print("HTTP Status:", response.status_code)

        print("Raw Response:")
        print(response.text)

        data = response.json()

        if data["field1"] is None or data["field2"] is None:
            return None, None

        vibration = float(data["field1"])
        temperature = float(data["field2"])

        print("Parsed Values")
        print("Vibration :", vibration)
        print("Temperature :", temperature)

        return temperature, vibration

    except Exception as e:

        print("ThingSpeak Error :", e)

        return None, None


if __name__ == "__main__":

    temperature, vibration = read_sensor()

    print("Returned Values:")
    print(temperature, vibration)
