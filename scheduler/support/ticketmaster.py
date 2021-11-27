import requests
import datetime
from dateutil import parser

from ..models import Event


class Ticketmaster:

    def __init__(self):
        self.BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json?&apikey="
        self.KEY = "MwvGo5jGojI13TDq5rDzKB2t95MmMNsy"

    def parse_events(self, location, start_date_time):
        event_list = []

        start_date_time_iso = datetime.datetime.fromtimestamp(start_date_time).isoformat()
        end_date_time = start_date_time + 5184000
        end_date_time_iso = datetime.datetime.fromtimestamp(end_date_time).isoformat()

        added_url = "&locale=*&startDateTime=" + start_date_time_iso + \
                    "Z&endDateTime=" + end_date_time_iso + \
                    "Z&stateCode=" + location

        request = requests.get(self.BASE_URL + self.KEY + added_url)

        if request.status_code != 200:
            return []

        response = request.json()

        try:
            for event in response['_embedded']['events']:
                e = Ticketmaster.parse_one_event(event)
                if e:
                    event_list.append(e)
        except KeyError:
            return []

        return event_list

    @staticmethod
    def parse_one_event(event):
        new_event = Event()

        try:
            if event['dates']['start']['timeTBA'] is True or event['dates']['start']['noSpecificTime'] is True:
                return None

            new_event.name = event['name']

            if event['dates']['start']['dateTime']:
                new_event.start_time = parser.parse(event['dates']['start']['dateTime'])
            else:
                return None
            new_event.duration = datetime.timedelta(hours=3)
            new_event.end_time = new_event.start_time + new_event.duration

            new_event.category = event['classifications'][0]['segment']['name'].lower()
            new_event.description = event['info'] if 'info' in event else None
            new_event.cost = event['priceRanges'][0]['min'] if 'priceRanges' in event else None
            new_event.picture = event['images'][0]['url']
            new_event.tickets = event['seatmap']['staticUrl']

            new_event.address1 = event['_embedded']['venues'][0]['address']['line1']
            new_event.city = event['_embedded']['venues'][0]['city']['name']
            new_event.state = event['_embedded']['venues'][0]['state']['stateCode']
            new_event.country = event['_embedded']['venues'][0]['country']['name']
            new_event.zip_code = event['_embedded']['venues'][0]['postalCode']
            return new_event
        except KeyError:
            return None
