import time

from sensor import Sensor
from request import Request

if __name__ == "__main__":
    
    print("Start Main")

    seconds = 0
    interval = 60
    sensor = Sensor()
    request = Request()

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
            
            # pull values from sensor
            sensor.pull()

            # wait till one second passed
            time.sleep(1-(time.time()-start))     

    else:
        print("Init fail, stop program")
