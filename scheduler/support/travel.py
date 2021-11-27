from . import route

import requests
import json
import datetime


def get_mapquest_response(start_position, end_position):
    base_url = "https://open.mapquestapi.com/directions/v2/route?key="
    locations = "&from=" + start_position + "&to=" + end_position
    key = "xVp6Qgy7SK7vhjRMGbJw49weeg79JnaT"
    response = requests.get(base_url + key + locations)
    if response.status_code != 200:
        return None

    try:
        dictionary = json.loads(response.text)
    except:
        return None

    if dictionary['info']['statuscode'] != 0:
        return None
    else:
        return dictionary['route']


def get_travel_time(start_position, end_position):
    route = get_mapquest_response(start_position, end_position)
    if route is None:
        return datetime.timedelta(hours=2)

    time_format = route['formattedTime']
    time_split = time_format.split(":")
    return datetime.timedelta(
        seconds=int(time_split[2]),
        minutes=int(time_split[1]),
        hours=int(time_split[0]),
    )


def optimized_directions(location_list):
    base_url = "https://open.mapquestapi.com/directions/v2/optimizedroute?key="
    locations = "&json=" + location_list
    key = "JEq6beD60zZZFpjDPAGR9gnuO0k3B0IX"
    response = requests.get(base_url + key + locations)
    return route.Route(json.loads(response.text))
