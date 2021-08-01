import smbus2
import time
import requests
import json
import bme680

if __name__ == "__main__":
    print("Start Main")

    interval_values = []
    seconds = 0
    sensor = None

    # save values to database
    def save():
        global interval_values

        print("Save")
        
        median = sum(interval_values) / len(interval_values)

        url = "http://server:8000/measurements/post"

        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Basic M1pxqkAAjS57SAKVJ4GoyYcPnFNjbbQ99zZFYrse"
        }

        data = {
            "median": median
        }

        try:
            requests.post(url = url, data = json.dumps(data), headers = headers)
        except:
            print("Post Request failed!")

        interval_values = []

    # pull values from bme 680
    def pull():
        global sensor

        if sensor.get_sensor_data():

            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity)

            if sensor.data.heat_stable:
                print('{0},{1} Ohms'.format(
                    output,
                    sensor.data.gas_resistance))

            else:
                print(output)

            return sensor.data.temperature

        else:
            return -255

    def init():
        global sensor

        print("""read-all.py - Displays temperature, pressure, humidity, and gas.
        Press Ctrl+C to exit!
        """)

        try:
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):

            try:
                sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
            except (RuntimeError, IOError):
                sensor = None

        if sensor is None:
            return False

        # These calibration data can safely be commented
        # out, if desired.

        print('Calibration data:')
        for name in dir(sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(sensor.calibration_data, name)

                if isinstance(value, int):
                    print('{}: {}'.format(name, value))

        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.

        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)
        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        print('\n\nInitial reading:')
        for name in dir(sensor.data):
            value = getattr(sensor.data, name)

            if not name.startswith('_'):
                print('{}: {}'.format(name, value))

        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)

        return True

    success = init()

    if success:

        print("Init success, start main loop")

        # main loop
        while True:

            value = pull()
            interval_values.append(value)

            time.sleep(1)
            seconds += 1

            if(seconds >= 5):
                save()
                seconds = 0

    else:
        print("Init fail, stop program")
