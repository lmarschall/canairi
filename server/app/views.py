from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Measurement

import datetime

@api_view(["GET"])
def get_measurements(request):

    # http://127.0.0.1:8000/api/rooms?size=1&check_in=08.08.2020&check_out=12.08.2020

    # try:
    #     # try to get the filter parameters from the request
    #     size = request.query_params['size']
    #     check_in = request.query_params['check_in']
    #     check_out = request.query_params['check_out']

    #     date_one = datetime.date(int(check_in.split('.')[2]), int(check_in.split('.')[1]), int(check_in.split('.')[0]))
    #     date_two = datetime.date(int(check_out.split('.')[2]), int(check_out.split('.')[1]), int(check_out.split('.')[0]))

    #     # filter out avaible rooms
    #     reserved_room_ids = Reservation.objects.filter(check_out__gte=date_one).filter(check_in__lte=date_two).values_list('id', flat=True)
    #     rooms = Room.objects.filter(size__gte=size).exclude(id__in = reserved_room_ids).all()

    # except:
    #     # get all rooms if no valid paramters were given
    #     rooms = Room.objects.all()

    measurements = Measurement.objects.all()

    # parse the filtered rooms to json
    json_measurements = measurements.values('id', 'time', 'value')

    return Response(json_measurements)

@api_view(["POST"])
def post_measurements(request):

    print("Received post")

    # try to extract request data
    try:
        median = request.data["median"]
    except:
        median = -255

    # create timestamp for values
    timestamp = datetime.datetime.now()
    print(timestamp)
    print(median)

    # save value to database if valid
    if median is not -255:
        m = Measurement(time=timestamp, value=median)
        m.save()

    return Response()