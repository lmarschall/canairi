import requests
import json

class Request:
    def __init__(self):
        pass

    # save values to database
    def save(values):
        global interval_values

        print("Save")

        url = "http://server:8000/measurements/post"

        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Basic M1pxqkAAjS57SAKVJ4GoyYcPnFNjbbQ99zZFYrse"
        }

        data = {
            "temperature": values[0],
            "pressure": values[1],
            "humidity": values[2],
            "gas_resistance": values[3],
            "air_quality": values[4]
        }

        try:
            requests.post(url = url, data = json.dumps(data), headers = headers)
        except:
            print("Post Request failed!")