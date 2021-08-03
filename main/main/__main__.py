import time
from gpiozero import LEDBoard

from .sensor import Sensor
from .request import Request

if __name__ == "__main__":
    
    print("Start Main")

    seconds = 0
    interval = 60
    sensor = Sensor()
    request = Request()
    leds = LEDBoard(26, 19, 13)
    leds.value = (0, 0, 0)
    leds_on = False

    # init sensor
    success = sensor.init()

    # TODO: wait for server

    if success:

        print("Init success, start main loop")

        # main loop
        while True:

            # save start time
            start = time.time()

            # if one minute passed save values
            if(seconds >= interval):
                values = sensor.get()
                request.save(values)
                seconds = 0
            
            # check if gas sensor is ready
            if(sensor.start_time + sensor.burn_in_time < start and sensor.burned_in is False):
                sensor.burn()

            # check air quality and set leds
            if(sensor.air_quality > 0):

                # check air quality thresholds
                if(sensor.air_quality <= 50):
                    leds.value = (0, 0, 1)  # green
                elif(sensor.air_quality <= 150):
                    leds.value = (0, 1, 0)  # yellow
                else:
                    leds.value = (1, 0, 0)  # red
            else:
                # switch till burn in complete 
                if leds_on:
                    leds.value = (0, 0, 0)
                    leds_on = False
                else:
                    leds.value = (1, 1, 1)
                    leds_on = True
            
            # pull values from sensor
            sensor.pull()

            # wait till one second passed
            sleep = 2-(time.time()-start)
            if sleep > 0:
                time.sleep(sleep)

            seconds += 2

    else:
        print("Init fail, stop program")
