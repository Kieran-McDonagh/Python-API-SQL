import os
import sys

from services.destinations_service import DestinationService
from services.flights_service import FlightService
from services.pilots_service import PilotService
from storage.database_seeder.data_seeder import DataSeeder
from storage.database_providers.destinations_provider import DestinationsProvider
from storage.database_providers.flights_provider import FlightsProvider
from handlers.destination_handler import DestinationHandler
from handlers.flight_handler import FlightHandler
from handlers.input_handler import InputHandler
from handlers.pilot_handler import PilotHandler
from storage.database_providers.pilots_provider import PilotsProvider


class DatabaseManager:
    def __init__(self, input_handler):
        self.input_handler = input_handler

    # Runs the app with the main input handler.

    def run(self):
        try:
            self.input_handler.handle_user_input()

        except SystemExit as e:
            print(e)
            sys.exit(0)

        except Exception as e:
            print("\nUnexpected error: ", e)
            sys.exit(1)


if __name__ == "__main__":
    # Initialise storage location.

    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(base_dir, "storage/database_storage")
    os.makedirs(db_dir, exist_ok=True)
    db_storage = os.path.join(db_dir, "database_storage.db")

    # Seed if necessary.

    data_seeder = DataSeeder(db_storage)
    data_seeder.check_for_data()

    # Initialise database providers.

    pilots_provider = PilotsProvider(db_storage)
    destinations_provider = DestinationsProvider(db_storage)
    flights_provider = FlightsProvider(db_storage)

    # Initialise services.

    pilot_service = PilotService(pilots_provider)
    destination_service = DestinationService(destinations_provider)
    flight_service = FlightService(flights_provider)

    # Initialise handlers.

    pilot_handler = PilotHandler(pilot_service)
    destination_handler = DestinationHandler(destination_service)
    flight_handler = FlightHandler(flight_service, destination_service, pilot_service)
    input_handler = InputHandler(pilot_handler, destination_handler, flight_handler)

    # Initialise app.

    app = DatabaseManager(input_handler)

    app.run()
