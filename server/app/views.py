from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Measurement

import datetime
from django.utils.timezone import get_current_timezone

@api_view(["GET"])
def get_measurements(request):

    # http://127.0.0.1:8000/api/rooms?size=1&check_in=08.08.2020&check_out=12.08.2020

    try:
        # try to get the filter parameters from the request
        start_date = request.query_params["start_date"]
        end_date = request.query_params["end_date"]

        # filter out avaible rooms
        measurements = Measurement.objects.filter(check_out__gte=start_date).filter(check_in__lte=end_date).all().order_by("time")

    except:
        # get all rooms if no valid paramters were given
        measurements = Measurement.objects.all().order_by("-time")[:60]

    # parse the filtered rooms to json
    json_measurements = measurements.values("id", "time", "temperature", "pressure", "humidity", "gas_resistance", "air_quality")

    return Response(json_measurements)

@api_view(["POST"])
def post_measurements(request):

    print("Received post")

    # try to extract request data
    try:
        timestamp = datetime.datetime.now(tz=get_current_timezone())
        temperature = request.data["temperature"]
        pressure = request.data["pressure"]
        humidity = request.data["humidity"]
        gas_resistance = request.data["gas_resistance"]
        air_quality = request.data["air_quality"]

        # create timestamp for values
        m = Measurement(
            time=timestamp,
            temperature=temperature,
            pressure=pressure,
            humidity=humidity,
            gas_resistance=gas_resistance,
            air_quality=air_quality)
        m.save()

        print('{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH, {3} Ohms, {4} Air Quality'.format(
            temperature,
            pressure,
            humidity,
            gas_resistance,
            air_quality))

    except:
        pass

    return Response()