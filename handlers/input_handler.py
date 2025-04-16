from utils.utils import Utils as u


class InputHandler:
    def __init__(self, pilot_handler, destination_handler, flight_handler):
        self.pilot_handler = pilot_handler
        self.destination_handler = destination_handler
        self.flight_handler = flight_handler

    #  Main input handler that allows users to switch between flights, pilots and destinations.

    def handle_user_input(self):
        options = {
            "Flights": self.flight_handler.handle_flight_queries,
            "Pilots": self.pilot_handler.handle_pilot_queries,
            "Destinations": self.destination_handler.handle_destination_queries,
        }

        u.present_initial_options(options)
