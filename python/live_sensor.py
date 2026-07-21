import requests

URL="http://127.0.0.1:5000/data"

def get_live_data():

    try:

        data=requests.get(URL).json()

        return data["temperature"], data["vibration"]

    except:

        return None,None
