from . import yelp
from . import ticketmaster


class EventFinder:
    def __init__(self, location, start_time):
        self.location = location
        self.start_time = start_time

    def get_yelp_events(self):
        yelp_access_object = yelp.Yelp()
        return yelp_access_object.parse_events(self.location, self.start_time)

    def get_ticketmaster_events(self):
        ticketmaster_access_object = ticketmaster.Ticketmaster()
        return ticketmaster_access_object.parse_events(self.location, self.start_time)

    def save_all_events(self):
        yelp_event_list = self.get_yelp_events()
        ticketmaster_event_list = self.get_ticketmaster_events()
        for event in yelp_event_list:
            event.save()
        for event in ticketmaster_event_list:
            event.save()
