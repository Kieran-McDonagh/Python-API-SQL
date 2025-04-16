class FlightService:
    def __init__(self, flights_provider):
        self.flights_provider = flights_provider

    # Service responsible for passing data between handlers and flight provider.

    # CREATE

    def create_flight(
        self, departure_date, departure_time, destination_id, pilot_ids, status
    ):
        result = self.flights_provider.create_flight(
            departure_date, departure_time, destination_id, pilot_ids, status
        )
        return result

    # READ

    def get_all_flights(self):
        flights = self.flights_provider.get_all_flights()
        return flights

    def get_flight_by_id(self, flight_id):
        flight = self.flights_provider.get_flight_by_id(flight_id)
        return flight

    def get_flights_by_destination_id(self, destination_id):
        flights = self.flights_provider.get_flights_by_destination_id(destination_id)
        return flights

    def get_flight_count_by_destination_id(self, destination_id, completed):
        count = self.flights_provider.get_flight_count_by_destination_id(
            destination_id, completed
        )
        return count

    def get_flights_by_status(self, status):
        flights = self.flights_provider.get_flights_by_status(status)
        return flights

    def get_flights_by_pilot(self, pilot_id):
        schedule = self.flights_provider.get_flights_by_pilot(pilot_id)
        return schedule

    def get_flight_count_by_pilot(self, pilot_id, completed):
        count = self.flights_provider.get_flight_count_by_pilot(pilot_id, completed)
        return count

    def get_pilots_for_flight(self, flight_id):
        pilots_for_flight = self.flights_provider.get_pilots_by_flight_id(flight_id)
        return pilots_for_flight

    def get_flights_with_no_pilots(self):
        flights = self.flights_provider.get_flights_with_no_pilots()
        return flights

    def get_flights_for_departure_date(self, date_range, date):
        flights = self.flights_provider.get_flights_for_departure_date(date_range, date)
        return flights

    # UPDATE

    def update_flight(self, flight_id, fiefield_to_update, value):
        result = self.flights_provider.update_flight(
            flight_id, fiefield_to_update, value
        )
        return result

    def assign_pilots_to_flight(self, flight_id, pilot_ids):
        result = self.flights_provider.assign_pilots_to_flight(flight_id, pilot_ids)
        return result

    def remove_pilots_from_flight(self, flight_id, pilot_ids):
        result = self.flights_provider.remove_pilots_from_flight(flight_id, pilot_ids)
        return result

    # DELETE

    def delete_filght(self, flight_id):
        result = self.flights_provider.delete_flight(flight_id)
        return result
