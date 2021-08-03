import bme680
import time

class Sensor:
    def __init__(self):
        self.sensor = None
        self.start_time = None
        self.burn_in_time = 300
        self.gas_baseline = 0
        self.hum_baseline = 40.0
        self.hum_weighting = 0.25
        self.burned_in = False
        self.burn_in_data = []
        self.tem_values = []
        self.pre_values = []
        self.hum_values = []
        self.gas_values = []
        self.air_quality = -1

    # get mean values of sensor
    def get(self):
        
        # calculate mean values of data
        mean_tem = sum(self.tem_values) / len(self.tem_values)
        mean_pre = sum(self.pre_values) / len(self.pre_values)
        mean_hum = sum(self.hum_values) / len(self.hum_values)

        # check if gas data avaiable
        if self.burned_in:
            
            mean_gas = sum(self.gas_values) / len(self.gas_values)

            gas_offset = self.gas_baseline - mean_gas
            hum_offset = mean_hum - self.hum_baseline

            # Calculate hum_score as the distance from the hum_baseline.
            if hum_offset > 0:
                hum_score = (100 - self.hum_baseline - hum_offset)
                hum_score /= (100 - self.hum_baseline)
                hum_score *= (self.hum_weighting * 100)

            else:
                hum_score = (self.hum_baseline + hum_offset)
                hum_score /= self.hum_baseline
                hum_score *= (self.hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (mean_gas / self.gas_baseline)
                gas_score *= (100 - (self.hum_weighting * 100))

            else:
                gas_score = 100 - (self.hum_weighting * 100)

            # Calculate air quality score.
            self.air_quality = hum_score + gas_score

        else:
            mean_gas = -1
            self.air_quality = -1

        # reset data
        self.tem_values = []
        self.pre_values = []
        self.hum_values = []
        self.gas_values = []

        return [
            mean_tem,
            mean_pre,
            mean_hum,
            mean_gas,
            self.air_quality
        ]

    # pull values from bme 680
    def pull(self):

        # check if sensor data can be received
        if self.sensor.get_sensor_data():

            # get sensor data
            temperature = self.sensor.data.temperature
            pressure = self.sensor.data.pressure
            humidity = self.sensor.data.humidity

            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                temperature,
                pressure,
                humidity)

            # save data to list
            self.tem_values.append(temperature)
            self.pre_values.append(pressure)
            self.hum_values.append(humidity)

            # check if gas sensor burned in and save value if possible
            if self.sensor.data.heat_stable:

                gas_resistance = self.sensor.data.gas_resistance
                print('{0},{1} Ohms'.format(
                    output,
                    gas_resistance))

                if self.burned_in:
                    self.gas_values.append(gas_resistance)
                else:
                    self.burn_in_data.append(gas_resistance)

            else:
                print(output)

    def burn(self):
        print("Burned in")
        self.gas_baseline = sum(self.burn_in_data[-50:]) / 50.0
        self.burned_in = True

    def init(self):

        print("""read-all.py - Displays temperature, pressure, humidity, and gas.
        Press Ctrl+C to exit!
        """)

        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):

            try:
                self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
            except (RuntimeError, IOError):
                self.sensor = None

        if self.sensor is None:
            return False

        # These calibration data can safely be commented
        # out, if desired.

        print('Calibration data:')
        for name in dir(self.sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(self.sensor.calibration_data, name)

                if isinstance(value, int):
                    print('{}: {}'.format(name, value))

        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        print('\n\nInitial reading:')
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)

            if not name.startswith('_'):
                print('{}: {}'.format(name, value))

        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

        # save start time for burn in process of gas sensor
        self.start_time = time.time()

        return True