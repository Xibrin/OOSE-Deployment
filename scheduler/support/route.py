class Route:
    def __init__(self, directions, start_position=None, end_position=None):
        self.start_position = start_position
        self.end_position = end_position
        self.directions = directions
        if directions["route"]:
            # self.tolls = directions["route"]["hasTollRoad"]
            self.distance = directions["route"]["distance"]
            self.time = directions["route"]["time"]
            self.fuel_use = directions["route"]["fuelUsed"]
            # self.start_lng = directions["route"]["latLng"]["lng"]

    # Helper Methods
    def calculate_fuel_cost(self):
        # take fuel use and calculate fuel cost based on local fuel prices
        pass

    def get_toll_price(self):
        # find toll on route and determine price based on other database
        pass

    def get_distance(self, unit):
        # take distance and return in preferred unit
        pass

    def get_time(self, time_format):
        # take time format from Json and return in local time format
        pass
