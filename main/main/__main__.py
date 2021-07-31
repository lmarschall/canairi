import smbus2
import numpy as np
import time
import requests
import json

if __name__ == "__main__":
    print("Start Main")

    interval_values = []
    seconds = 0

    # save values to database
    def save():
        global interval_values

        print("Save")
        
        median = np.median(interval_values)

        url = "http://server:8000/measurements/post"

        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Basic M1pxqkAAjS57SAKVJ4GoyYcPnFNjbbQ99zZFYrse"
        }

        data = {
            "median": median
        }

        r = requests.post(url = url, data = json.dumps(data), headers = headers)

        interval_values = []

    # pull values from bme 680
    def pull():

        return np.random.rand(1)[0]

    # main loop
    while True:

        value = pull()
        interval_values.append(value)

        time.sleep(1)
        seconds += 1

        if(seconds >= 5):
            save()
            seconds = 0
