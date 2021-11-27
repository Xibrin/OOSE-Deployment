import requests
from dateutil import parser

from . import states

from ..models import Event


class Yelp:
    def __init__(self):
        self.BASE_URL = "https://api.yelp.com/v3/events"
        self.KEY = "ch0KHsoQZVMqSS13Q9Hsl5hsl2hAmy4WMoyeBjUVf_I4s4VJMXetUO7XnoBNj3K6d4jW0uD9DkqpkEk2lIlcpPVSqHoIw-G6dCVO6sfUNGi9zvkcQ9GpCTT6gY5cYXYx"
        self.HEADERS = {'Authorization': 'Bearer %s' % self.KEY}
        self.LIMIT = 50

    def parse_events(self, location, start_date_time):
        event_list = []

        for i in range(3):
            params = {'location': location, 'limit': self.LIMIT, 'offset': i * self.LIMIT, 'start_date': start_date_time}

            request = requests.get(self.BASE_URL, params=params, headers=self.HEADERS)
            if request.status_code != 200:
                continue

            response = request.json()

            try:
                for event in response['events']:
                    e = Yelp.parse_one_event(event)
                    if e:
                        event_list.append(e)
            except KeyError:
                return []

        return event_list

    @staticmethod
    def parse_one_event(event):
        new_event = Event()

        try:
            new_event.name = event['name']

            if event['time_start']:
                new_event.start_time = parser.parse(event['time_start'])
            else:
                return None
            if event['time_end']:
                new_event.end_time = parser.parse(event['time_end'])
            else:
                return None
            new_event.duration = new_event.end_time - new_event.start_time

            new_event.category = event['category'].lower()
            new_event.description = event['description']
            new_event.cost = float(event['cost']) if event['cost'] else None
            new_event.picture = event['image_url']
            new_event.tickets = event['tickets_url']

            new_event.address1 = event['location']['address1']
            new_event.city = event['location']['city']
            state = states.get_state_code(event['location']['state'])
            if state:
                new_event.state = state
            else:
                return None
            new_event.country = event['location']['country']
            new_event.zip_code = event['location']['zip_code']
            return new_event
        except KeyError:
            return None

